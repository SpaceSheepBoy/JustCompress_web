"""Maintain the original trim tutorial URL without rebuilding unrelated pages."""
from pathlib import Path
from html import escape
import json
import re
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PATH = '/iphone-video-tutorials/15-how-to-trim-audio-on-iphone/'
DATE = '2026-11-12'


def render():
    products = json.loads((ROOT / 'scripts/tutorial-products.json').read_text())
    product = products['6769563659']
    cta = ('<aside class="guide-cta guide-download"><div><strong>' + escape(product['name'])
           + '</strong><p>Free download · In-app purchases.</p></div>'
           + '<a class="guide-store-badge" href="' + escape(product['url'], quote=True)
           + '"><img src="/assets/brand/app-store-badges/en.svg" width="240" height="80" alt="Download on the App Store"></a></aside>')
    title = 'How to Trim Audio on iPhone'
    description = 'Keep the part of a recording you need. Set start and end, preview both cuts, save an M4A copy, and check it before sharing.'
    body = (ROOT / 'scripts/guide-layouts/trim-audio-iphone.html').read_text()
    body = body.replace('{{DATE}}', escape(DATE)).replace('{{CTA}}', cta)
    schema = {'@context': 'https://schema.org',
        '@type': 'Article', 'headline': title, 'description': description,
        'dateModified': DATE, 'mainEntityOfPage': 'https://justcompress.online' + PATH,
        'author': {'@type': 'Organization', 'name': 'Space Sheep Studio'},
    }
    structured = json.dumps(schema, ensure_ascii=False).replace('</', '<\\/')
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | Just Compress</title><meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="https://justcompress.online{PATH}">
<meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:url" content="https://justcompress.online{PATH}"><meta property="og:type" content="article"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/home.css?v=20261002"><link rel="stylesheet" href="/assets/tutorial-guides.css?v=20261108-badges">
<link rel="stylesheet" href="/assets/trim-audio-guide.css?v=20261112">
<script type="application/ld+json">{structured}</script></head>
<body class="guide-page"><div class="guide-shell"><nav class="guide-nav" aria-label="Main navigation"><a class="guide-brand" href="/">Just Compress</a><div><a href="/guides/">Guides</a><a href="/videos/">Videos</a><a href="/apps/">Apps</a><a href="/tools/">Free tools</a></div></nav>
<main>{body}</main><footer class="guide-footer"><span>© 2026 Space Sheep Studio</span><a href="/guides/">Guides</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a><a href="/support/">Support</a></footer></div></body></html>
''' 
    html = html.replace('</head>', '<script defer src="/assets/posthog-init.js?v=20261022-3"></script></head>')
    (ROOT / PATH.strip('/') / 'index.html').write_text(html, encoding='utf-8')
    # A real content revision changes this URL only, never experiment D0.
    sitemap = ROOT / 'sitemap.xml'
    content = sitemap.read_text(encoding='utf-8')
    pattern = r'(<loc>https://justcompress\.online' + re.escape(PATH) + r'</loc>\s*<lastmod>)[^<]*(</lastmod>)'
    content, count = re.subn(pattern, lambda match: match[1] + DATE + match[2], content)
    if count != 1:
        raise ValueError('Expected exactly one existing trim tutorial sitemap entry')
    sitemap.write_text(content, encoding='utf-8')


def render_audio_downloads():
    # Legacy browser-tool output still contains text-only App Store links.
    # Preserve tool code/URLs and normalize only these existing download anchors.
    badge_path = '/assets/brand/app-store-badges/en.svg'
    if not (ROOT / badge_path.lstrip('/')).is_file():
        raise ValueError('Official Apple badge asset is required')
    for relative in ('m4a-to-mp3/index.html', 'trim-audio/index.html'):
        page = ROOT / relative
        soup = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
        links = soup.select('a[href*="apps.apple.com"][href*="/id6769563659"]')
        if not links:
            raise ValueError('Expected existing Audio Compressor download link')
        for link in links:
            classes = [name for name in link.get('class', []) if name != 'guide-button']
            link['class'] = list(dict.fromkeys(classes + ['guide-store-badge']))
            link.clear()
            link.append(soup.new_tag('img', src=badge_path, width='240', height='80', alt='Download on the App Store'))
        if relative == 'trim-audio/index.html':
            for stars in soup.select('.proof-pill .stars'):
                if stars.get_text() == '★★★★★':
                    stars.string = ''
        page.write_text(str(soup), encoding='utf-8')


if __name__ == '__main__':
    render()
    render_audio_downloads()
