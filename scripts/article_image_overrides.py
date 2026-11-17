"""Apply maintained, topic-specific imagegen illustrations after article renderers."""
from pathlib import Path
import json
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
STYLE = ('display:block;width:100%;max-width:760px;height:auto;aspect-ratio:auto;'
         'object-fit:contain;margin:0 auto;border-radius:14px')


def validate(root, articles):
    for path, image in articles.items():
        page = root / path
        asset = root / image['src'].lstrip('/')
        if (not page.resolve().is_relative_to(root.resolve())
                or not asset.resolve().is_relative_to(root.resolve())
                or not page.is_file() or not asset.is_file()):
            raise ValueError('Article image page/asset missing or outside source root: ' + path)
        if image.get('tool') != 'built-in imagegen' or not image.get('provenance'):
            raise ValueError('Missing built-in imagegen provenance: ' + path)
        if not image.get('alt') or not image.get('caption') or not all(
                isinstance(image.get(key), int) and image[key] > 0 for key in ['width', 'height']):
            raise ValueError('Missing article illustration metadata: ' + path)


def normalize(raw, image):
    soup = BeautifulSoup(raw, 'html.parser')
    container = soup.select_one('article.guide-article,article.prose,article.tutorial-guide,article')
    if not container:
        raise ValueError('No article content container')
    # Only explicitly superseded images are removed. Real steps and diagrams remain.
    for old in soup.select('[data-editorial-image]'):
        old.decompose()
    remove_sources = set(image.get('remove_sources', []))
    for old in list(container.select('figure')):
        sources = [node.get('src', '').split('?')[0] for node in old.select('img')]
        if sources and all(source in remove_sources for source in sources):
            old.decompose()
    figure = soup.new_tag('figure', attrs={'data-editorial-image': '',
        'style': 'margin:28px 0;max-width:100%;clear:both'})
    img = soup.new_tag('img', src=image['src'], width=str(image['width']),
        height=str(image['height']), alt=image['alt'], decoding='async',
        attrs={'fetchpriority': 'high', 'style': STYLE})
    figure.append(img)
    caption = soup.new_tag('figcaption', attrs={'style': 'font-size:14px;line-height:1.6;margin-top:12px'})
    caption.string = image['caption']
    figure.append(caption)
    container.insert(0, figure)
    if soup.head:
        public_image = 'https://justcompress.online' + image['src']
        meta = soup.find('meta', attrs={'property': 'og:image'})
        if not meta:
            meta = soup.new_tag('meta', attrs={'property': 'og:image'})
            soup.head.append(meta)
        meta['content'] = public_image
        twitter = soup.find('meta', attrs={'name': 'twitter:image'})
        if twitter:
            twitter['content'] = public_image
    # Parsing after removal coalesces adjacent whitespace text nodes immediately,
    # so the first write is already stable on the next generation pass.
    return str(BeautifulSoup(str(soup), 'html.parser'))


def apply(root=ROOT):
    articles = json.loads((root / 'scripts/article-image-overrides.json').read_text())['articles']
    validate(root, articles)  # Fail before writing any page when an input is incomplete.
    writes = {}
    for path, image in articles.items():
        file = root / path
        raw = file.read_text()
        updated = normalize(raw, image)
        if updated != raw:
            writes[file] = updated
    for file, updated in writes.items():
        file.write_text(updated)
    return [str(file.relative_to(root)) for file in writes]


if __name__ == '__main__':
    print('Updated topic-specific article illustrations:', len(apply()))
