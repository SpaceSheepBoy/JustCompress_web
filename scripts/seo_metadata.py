"""Finalize static search metadata and X cards without reserializing page content."""
import argparse
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import unquote, urljoin, urlsplit

from bs4 import BeautifulSoup
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://justcompress.online'
MIN_DESCRIPTION_LENGTH = 100
MAX_TITLE_LENGTH = 70
MAX_CARD_DESCRIPTION_LENGTH = 200
COPY = json.loads((ROOT / 'scripts/seo-metadata-copy.json').read_text())
META_TAG = re.compile(r"""<meta\b(?:[^"'<>]|"[^"]*"|'[^']*')*>""", re.I)
TITLE_TAG = re.compile(r'<title\b[^>]*>.*?</title\s*>', re.I | re.S)
BRAND_SUFFIX = re.compile(r'(?:\s*\|\s*|\s*,\s*)(?:Just Compress(?: iPhone Tutorial| Blog)?|Space Sheep Studio)$')
RASTER_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}


def localized_description(soup, current):
    # These sentences are already in the reviewed product catalog for this language.
    features = [node.get_text(' ', strip=True) for node in soup.select('.feature-list li')]
    if not features:
        return current
    separator = '' if soup.html.get('lang', '').startswith(('ja', 'zh')) else ' '
    description = ''
    for sentence in features:
        description = separator.join(filter(None, [description, sentence]))
        if len(description) >= MIN_DESCRIPTION_LENGTH:
            return description
    combined = separator.join([current, description])
    return combined if len(combined) >= MIN_DESCRIPTION_LENGTH else current


def share_image(value, route, root):
    if not value:
        return ''
    url = urljoin(SITE + route, value)
    parts = urlsplit(url)
    path = Path(unquote(parts.path))
    if parts.scheme != 'https' or path.suffix.lower() not in RASTER_EXTENSIONS:
        return ''
    if parts.netloc == urlsplit(SITE).netloc and not (root / str(path).lstrip('/')).is_file():
        return ''
    return url


def large_preview(image, root):
    parts = urlsplit(image)
    if parts.netloc != urlsplit(SITE).netloc:
        return False
    with Image.open(root / unquote(parts.path).lstrip('/')) as asset:
        width, height = asset.size
    return width >= 300 and height >= 157 and width / height >= 1.4


def indexable(soup):
    if soup.select_one('[data-site-redirect],meta[http-equiv="refresh"]'):
        return False
    robots = soup.find('meta', attrs={'name': 'robots'})
    return not robots or 'noindex' not in robots.get('content', '').lower()


def normalize(raw, route, root=ROOT):
    soup = BeautifulSoup(raw, 'html.parser')
    if not soup.head or not indexable(soup):
        return raw

    metadata = {node.get('name', node.get('property', '')).lower(): node
                for node in reversed(soup.head.find_all('meta'))}

    def content(name):
        return metadata[name].get('content', '').strip() if name in metadata else ''

    starts = [0, *(match.end() for match in re.finditer('\n', raw))]
    changes = []
    additions = []

    def source_offset(node):
        return starts[node.sourceline - 1] + node.sourcepos

    def put(name, value):
        node = metadata.get(name)
        attr = 'property' if name.startswith('og:') else 'name'
        if node and content(name) == value and node.get(attr) == name:
            return
        tag = f'<meta {attr}="{name}" content="{escape(value, quote=True)}"/>'
        if node:
            match = META_TAG.match(raw, source_offset(node))
            changes.append((match.start(), match.end(), tag))
        else:
            additions.append(tag)

    old_title = soup.title.get_text(strip=True) if soup.title else ''
    title = COPY['titles'].get(route, old_title)
    if len(title) > MAX_TITLE_LENGTH:
        title = BRAND_SUFFIX.sub('', title)
    if title != old_title:
        updated = f'<title>{escape(title)}</title>'
        if soup.title:
            match = TITLE_TAG.match(raw, source_offset(soup.title))
            changes.append((match.start(), match.end(), updated))
        else:
            additions.append(updated)
        if 'og:title' in metadata:
            put('og:title', title)

    old_description = content('description')
    description = old_description
    if not MIN_DESCRIPTION_LENGTH <= len(description) <= MAX_CARD_DESCRIPTION_LENGTH:
        description = COPY['descriptions'].get(route, description)
    if len(description) < MIN_DESCRIPTION_LENGTH:
        if soup.html.get('lang') != 'en':
            description = localized_description(soup, description)
        else:
            lede = soup.select_one('.guide-lede')
            summary = lede.get_text(' ', strip=True) if lede else ''
            if MIN_DESCRIPTION_LENGTH <= len(summary) <= 165:
                description = summary
    if description != old_description:
        put('description', description)
        if 'og:description' in metadata:
            put('og:description', description)

    if title:
        # Keep the existing editorial Open Graph image or a page-specific illustration.
        features = soup.select_one('[data-editorial-image] img, article figure img')
        editorial_image = share_image(features.get('src') if features else '', route, root)
        image = (share_image(content('og:image'), route, root)
                 or share_image(content('twitter:image'), route, root) or editorial_image)
        icon = soup.select_one('.product-heading img')
        thumbnail = image or share_image(icon.get('src') if icon else '', route, root)
        put('twitter:card', 'summary_large_image' if image and large_preview(image, root) else 'summary')
        social_title = content('og:title')
        if title != old_title or not 0 < len(social_title) <= MAX_TITLE_LENGTH:
            social_title = title
        put('twitter:title', social_title)
        if description:
            social_description = content('og:description')
            if description != old_description or not 0 < len(social_description) <= MAX_CARD_DESCRIPTION_LENGTH:
                social_description = description
            put('twitter:description', social_description)
        if thumbnail:
            put('twitter:image', thumbnail)
            illustration = content('og:image:alt') or (features.get('alt', '') if image == editorial_image and features else '')
            if image and illustration:
                put('twitter:image:alt', illustration)

    if additions:
        end = re.search(r'</head\s*>', raw[source_offset(soup.head):], re.I)
        position = source_offset(soup.head) + end.start()
        changes.append((position, position, '\n' + '\n'.join(additions) + '\n'))
    for start, end, value in sorted(changes, reverse=True):
        raw = raw[:start] + value + raw[end:]
    return raw


def problems(soup, title):
    description = soup.select_one('head meta[name="description"]')
    card = soup.select_one('head meta[name="twitter:card"]')
    errors = []
    if not 0 < len(title) <= MAX_TITLE_LENGTH:
        errors.append(f'title must contain 1–{MAX_TITLE_LENGTH} characters')
    if not description or len(description.get('content', '').strip()) < MIN_DESCRIPTION_LENGTH:
        errors.append(f'description must contain at least {MIN_DESCRIPTION_LENGTH} characters')
    if not card or card.get('content') not in {'summary', 'summary_large_image'}:
        errors.append('missing or invalid X card')
    card_title = soup.select_one('head meta[name="twitter:title"]')
    if not card_title or not 0 < len(card_title.get('content', '').strip()) <= MAX_TITLE_LENGTH:
        errors.append(f'X title must contain 1–{MAX_TITLE_LENGTH} characters')
    card_description = soup.select_one('head meta[name="twitter:description"]')
    if not card_description or not 0 < len(card_description.get('content', '').strip()) <= MAX_CARD_DESCRIPTION_LENGTH:
        errors.append(f'X description must contain 1–{MAX_CARD_DESCRIPTION_LENGTH} characters')
    return errors


def apply(paths=None, root=ROOT, check=False):
    if paths is None:
        paths = (path for path in sorted(root.rglob('index.html'))
                 if not any(part.startswith('.') or part in {'scripts', 'vendor', 'node_modules'}
                            for part in path.relative_to(root).parts))
    changed = []
    errors = []
    titles = {}
    for path in paths:
        path = root / path
        parent = path.relative_to(root).parent.as_posix()
        route = '/' if parent == '.' else f'/{parent}/'
        before = path.read_text(encoding='utf-8')
        after = normalize(before, route, root)
        if before != after:
            changed.append(route)
            if not check:
                path.write_text(after, encoding='utf-8')
        if check:
            soup = BeautifulSoup(after, 'html.parser')
            if indexable(soup):
                title = soup.title.get_text(strip=True) if soup.title else ''
                errors.extend(f'{route} {error}' for error in problems(soup, title))
                key = ' '.join(title.casefold().split())
                if key in titles:
                    errors.append(f'{route} duplicates the title of {titles[key]}')
                else:
                    titles[key] = route
    if errors:
        raise SystemExit('\n'.join(errors))
    return changed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='check that generated metadata is current')
    parser.add_argument('paths', nargs='*', type=Path, help='optional repository-relative HTML pages')
    args = parser.parse_args()
    changed = apply(args.paths or None, check=args.check)
    if args.check and changed:
        print('Outdated SEO metadata:', ', '.join(changed))
        raise SystemExit(1)
    print('Updated SEO metadata:', len(changed), 'pages')
