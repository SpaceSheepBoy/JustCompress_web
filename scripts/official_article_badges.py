"""Preserve official Apple download artwork on maintained article pages."""
from pathlib import Path
import re
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BADGE = '/assets/brand/app-store-badges/'
STYLE = 'display:block;width:min(100%,240px);max-width:240px;margin:24px 0;padding:0;background:transparent;border:0;border-radius:0;flex:0 1 240px'
IMAGE_STYLE = 'display:block;width:100%;max-width:240px;height:auto;object-fit:contain;border-radius:0'


def normalize(raw, relative):
    soup = BeautifulSoup(raw, 'html.parser')
    article = relative.parts[0] in {'guides', 'blog', 'iphone-video-tutorials'} or any(
        '"Article"' in s.get_text() for s in soup.select('script[type="application/ld+json"]'))
    if not article or not soup.head:
        return raw
    changed = False
    for link in soup.select('a[href*="apps.apple.com/"]'):
        text = link.get_text(' ', strip=True)
        # References such as "official listing" remain normal inline source links.
        action = bool(set(link.get('class', [])) & {'guide-button', 'guide-store-badge', 'official-store-badge', 'localized-store-badge', 'appstore'}) or bool(re.match(r'^(Get |Download |Open .+ (on|from) the App Store)', text))
        if not action:
            continue
        images = link.select('img')
        mac = any('mac-app-store' in str(i.get('src', '')) for i in images)
        if mac:
            continue  # Existing Mac-specific renderer owns platform selection.
        lang = soup.html.get('lang', 'en')
        asset = BADGE + lang + '.svg'
        if not (ROOT / asset.lstrip('/')).exists():
            raise ValueError('Missing official badge: ' + asset)
        label = next((i.get('alt') for i in images if i.get('alt') and 'store' in i.get('alt', '').lower()), 'Download on the App Store')
        classes = [c for c in link.get('class', []) if c not in {'guide-button', 'btn-primary', 'button', 'btn'}]
        classes = list(dict.fromkeys(classes + ['guide-store-badge']))
        before = str(link)
        link['class'] = classes
        link['style'] = STYLE
        link.clear()
        link.append(soup.new_tag('img', src=asset, width='240', height='80', alt=label, style=IMAGE_STYLE))
        # Correct the original voice-memo tutorial's misplaced PDF CTA.
        if relative.as_posix() == 'iphone-video-tutorials/08-how-to-compress-a-voice-memo-on-iphone/index.html' and 'id6769762323' in link['href']:
            link['href'] = 'https://apps.apple.com/us/app/audio-compressor-mp3-converter/id6769563659'
            aside = link.find_parent('aside')
            if aside and aside.select_one('strong'):
                aside.select_one('strong').string = 'Audio Compressor MP3 Converter'
        changed |= str(link) != before
    return str(soup) if changed else raw


def apply(root=ROOT):
    changed = []
    for file in root.rglob('index.html'):
        relative = file.relative_to(root)
        if any(part.startswith('.') or part in {'assets','scripts','vendor','node_modules','apps','privacy','terms','support','legal'} for part in relative.parts):
            continue
        raw = file.read_text()
        updated = normalize(raw, relative)
        if updated != raw:
            file.write_text(updated)
            changed.append(relative.as_posix())
    return changed


if __name__ == '__main__':
    print('Updated official article badges:', len(apply()))
