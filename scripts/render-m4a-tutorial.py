"""Maintain the original M4A-to-MP3 tutorial URL without rebuilding unrelated pages."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
PATH = '/iphone-video-tutorials/09-how-to-convert-m4a-to-mp3-on-iphone/'
DATE = '2026-11-06'


def render():
    products = json.loads((ROOT / 'scripts/tutorial-products.json').read_text())
    product = products['6769563659']
    cta = ('<aside class="guide-cta guide-download"><div><strong>' + escape(product['name'])
           + '</strong><p>Free download · In-app purchases.</p></div>'
           + '<a class="guide-button guide-app-download" href="' + escape(product['url'], quote=True)
           + '">Download on the App&nbsp;Store <span aria-hidden="true">↗</span></a></aside>')
    title = 'How to Convert M4A to MP3 on iPhone'
    description = 'Create an MP3 copy of an M4A recording on iPhone. Choose MP3 in Convert, save and play the result, then check the receiving format and size limits.'
    body = (ROOT / 'scripts/guide-layouts/m4a-to-mp3-iphone.html').read_text()
    body = body.replace('{{DATE}}', escape(DATE)).replace('{{CTA}}', cta)
    schema = {'@context': 'https://schema.org',
        '@type': 'Article', 'headline': title, 'description': description,
        'dateModified': DATE, 'mainEntityOfPage': 'https://justcompress.online' + PATH,
        'author': {'@type': 'Organization', 'name': 'Space Sheep Studio'},
    }
    structured = json.dumps(schema, ensure_ascii=False).replace('</', '<\\/')
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="apple-itunes-app" content="app-id=6769563659">
<title>{escape(title)} | Just Compress</title><meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="https://justcompress.online{PATH}">
<meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:url" content="https://justcompress.online{PATH}"><meta property="og:type" content="article"><meta property="og:image" content="https://justcompress.online/assets/m4a-mp3-guide/01.png"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/home.css?v=20261002"><link rel="stylesheet" href="/assets/tutorial-guides.css?v=20261106-cta">
<script type="application/ld+json">{structured}</script></head>
<body class="guide-page"><div class="guide-shell"><nav class="guide-nav" aria-label="Main navigation"><a class="guide-brand" href="/">Just Compress</a><div><a href="/guides/">Guides</a><a href="/videos/">Videos</a><a href="/apps/">Apps</a><a href="/tools/">Free tools</a></div></nav>
<main>{body}</main><footer class="guide-footer"><span>© 2026 Space Sheep Studio</span><a href="/guides/">Guides</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a><a href="/support/">Support</a></footer></div></body></html>
''' 
    html = html.replace('</head>', '<script defer src="/assets/posthog-init.js?v=20261022-3"></script></head>')
    (ROOT / PATH.strip('/') / 'index.html').write_text(html)


if __name__ == '__main__':
    render()
