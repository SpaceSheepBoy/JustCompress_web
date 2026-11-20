"""Use smaller WebP copies of oversized public images, at their original dimensions."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import argparse
import re

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://justcompress.online'
MAX_BYTES = 1_000_000
TARGET_BYTES = 500_000
# Match image URLs in body markup and social/structured metadata without reserializing HTML.
IMAGE_URL = re.compile(
    r'''(?<=[\s"'(:,=])(?:(?:https:)?//justcompress\.online/|/(?!/))?[a-zA-Z0-9_.%~-][a-zA-Z0-9_./%~-]*\.(?:webp|png|jpe?g)(?=[\s"'?#),;])''',
    flags=re.IGNORECASE,
)


def source_path(root, page, url):
    base = SITE + '/' + page.relative_to(root).as_posix()
    location = urlsplit(urljoin(base, url))
    if location.netloc != 'justcompress.online':
        return None
    path = unquote(location.path).lstrip('/')
    return root / path


def make_web_copy(path):
    original = path.read_bytes()
    stamp = sha256(original).hexdigest()[:12]
    copy = path.with_name(f'{path.stem}-web-{stamp}.webp')
    if copy.is_file() and copy.stat().st_size <= MAX_BYTES:
        return copy

    with Image.open(BytesIO(original)) as image:
        if getattr(image, 'is_animated', False):
            raise ValueError(f'Oversized animated image requires a separate review: {path}')
        options = {'method': 4, 'exact': True}
        if image.info.get('icc_profile'):
            options['icc_profile'] = image.info['icc_profile']
        if image.info.get('exif'):
            options['exif'] = image.info['exif']
        for quality in (92, 88, 84, 80):
            output = BytesIO()
            image.save(output, 'WEBP', quality=quality, **options)
            if output.tell() <= TARGET_BYTES:
                break
        if output.tell() > MAX_BYTES:
            raise ValueError(f'Original-size WebP still exceeds {MAX_BYTES:,} bytes: {path}')
        with Image.open(output) as encoded:
            if encoded.size != image.size:
                raise ValueError(f'Unexpected dimension change: {path}')
    copy.write_bytes(output.getvalue())
    return copy


def optimize(root, check=False):
    pages = {}
    images = set()
    for page in sorted(root.rglob('*.html')):
        relative = page.relative_to(root)
        if any(part.startswith('.') or part in {'docs', 'scripts', 'tests', 'vendor', 'node_modules'}
               for part in relative.parts):
            continue
        html = page.read_text()
        affected = {}
        for match in IMAGE_URL.finditer(html):
            url = match.group()
            path = source_path(root, page, url)
            if path and path.is_file() and path.stat().st_size > MAX_BYTES:
                affected[url] = path
        if affected:
            pages[page] = affected
            images.update(affected.values())

    if check:
        if images:
            raise SystemExit('\n'.join(str(path.relative_to(root)) for path in sorted(images)))
        print(f'All referenced local PNG, JPEG and WebP images are at most {MAX_BYTES:,} bytes.')
        return

    with ThreadPoolExecutor(max_workers=4) as pool:
        ordered = sorted(images)
        copies = dict(zip(ordered, pool.map(make_web_copy, ordered)))
    for page, affected in pages.items():
        urls = {url: (SITE if url.startswith(('https://', '//')) else '')
                     + '/' + copies[path].relative_to(root).as_posix()
                for url, path in affected.items()}
        html = page.read_text()
        updated = IMAGE_URL.sub(lambda match: urls.get(match.group(), match.group()), html)
        if updated != html:
            page.write_text(updated)
    original_bytes = sum(path.stat().st_size for path in images)
    served_bytes = sum(path.stat().st_size for path in copies.values())
    print(f'Optimized {len(images)} images across {len(pages)} pages: {original_bytes:,} → {served_bytes:,} bytes.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='List oversized references without changing files')
    args = parser.parse_args()
    optimize(ROOT, check=args.check)
