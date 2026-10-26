"""Replace App Store thumbnail assets with lossless, native-resolution screenshots.

Reuses each maintained screenshot's exact Apple source identity. No local upscaling
or artwork changes. Icons, app metadata, product copy and legal pages stay intact.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from PIL import Image
from datetime import datetime, timezone
import argparse, hashlib, io, json, re, subprocess

ROOT = Path(__file__).resolve().parents[1]


def original_url(url):
    if not re.match(r'https://is\d+-ssl\.mzstatic\.com/image/thumb/', url):
        raise ValueError('Expected a maintained Apple screenshot URL')
    return url.rsplit('/', 1)[0] + '/0x0ss.png'


def download(url):
    original = subprocess.check_output(['curl', '-fLsS', '--retry', '2', '--max-time', '60', url])
    image = Image.open(io.BytesIO(original))
    image.load()
    if image.width < 1000 or image.height < 2000:
        raise ValueError(f'Apple original is too small: {image.size} for {url}')
    pixels = image.convert('RGBA')
    encoded = io.BytesIO()
    options = {'lossless': True, 'method': 4, 'exact': True}
    if image.info.get('icc_profile'):
        options['icc_profile'] = image.info['icc_profile']
    pixels.save(encoded, 'WEBP', **options)
    data = encoded.getvalue()
    decoded = Image.open(io.BytesIO(data)).convert('RGBA')
    assert decoded.size == pixels.size and decoded.tobytes() == pixels.tobytes(), 'Encoding changed source pixels'
    digest = hashlib.sha256(data).hexdigest()
    return {'src': '/assets/apps/screenshots/' + digest[:20] + '.webp', 'source': url,
            'sha256': digest, 'bytes': len(data), 'width': image.width, 'height': image.height,
            'original_sha256': hashlib.sha256(original).hexdigest(), 'original_bytes': len(original),
            'transformation': 'Lossless WebP; native source dimensions; decoded RGBA pixels verified identical; no upscaling'}, data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path, required=True, help='Save a download/validation receipt outside the public site')
    args = parser.parse_args()
    portfolio_path = ROOT / 'scripts/app-portfolio.json'
    locales_path = ROOT / 'scripts/collage-localizations.json'
    portfolio = json.loads(portfolio_path.read_text())
    locales = json.loads(locales_path.read_text())
    entries = [s for a in portfolio['apps'] for s in a['screenshots']]
    entries += [s for locale in locales.values() for s in locale.get('screenshots', [])]
    urls = sorted({original_url(s['source']) for s in entries})
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = dict(zip(urls, pool.map(download, urls)))
    # Do not mutate maintained sources until every download and pixel check succeeds.
    output = ROOT / 'assets/apps/screenshots'
    output.mkdir(parents=True, exist_ok=True)
    replacements = {}
    for entry in entries:
        old_path = entry['src']
        asset, data = results[original_url(entry['source'])]
        (ROOT / asset['src'].lstrip('/')).write_bytes(data)
        replacements[old_path] = asset
        entry.update(asset)
    portfolio_path.write_text(json.dumps(portfolio, ensure_ascii=False, indent=2) + '\n')
    locales_path.write_text(json.dumps(locales, ensure_ascii=False, indent=2) + '\n')
    changed_pages = []
    dimensions = {s['src']: s for s in replacements.values()}
    for page in ROOT.rglob('*.html'):
        relative = page.relative_to(ROOT)
        if any(part.startswith('.') or part in ('scripts', 'vendor', 'node_modules') for part in relative.parts):
            continue
        before = page.read_text()
        after = before
        for old, asset in replacements.items():
            after = after.replace(old, asset['src'])
        if after == before:
            continue
        def sized(match):
            tag = match.group(0)
            node = BeautifulSoup(tag, 'html.parser').find('img')
            if node.get('src') not in dimensions:
                return tag
            asset = dimensions[node['src']]
            tag = re.sub(r'\bwidth\s*=\s*["\'][^"\']*["\']', 'width="' + str(asset['width']) + '"', tag)
            return re.sub(r'\bheight\s*=\s*["\'][^"\']*["\']', 'height="' + str(asset['height']) + '"', tag)
        after = re.sub(r'<img\b[^>]*>', sized, after)
        page.write_text(after)
        changed_pages.append(str(relative))
    receipt = {'checked_at': datetime.now(timezone.utc).isoformat(), 'entries': len(entries),
               'unique_sources': len(urls), 'unique_assets': len({asset['src'] for asset, _ in results.values()}),
               'pages': changed_pages, 'assets': [asset for asset, _ in results.values()],
               'result': 'PASS', 'pixel_identity': 'PASS', 'upscaling': False}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: receipt[key] for key in ('entries', 'unique_sources', 'unique_assets', 'result')}))
    print('Updated', len(changed_pages), 'public pages')


if __name__ == '__main__':
    main()
