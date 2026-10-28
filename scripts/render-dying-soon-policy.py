"""Maintained Dying Soon policy source; leaves other app policies untouched."""
import json,html
from pathlib import Path
R=Path(__file__).resolve().parents[1]
j=json.loads((R/'scripts/dying-soon-policy.json').read_text());escape=html.escape
body=''.join(f'<section class="product-section"><h2>{escape(title)}</h2><p>{escape(text)}</p></section>' for title,text in j['sections'])
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(j['title'])} | Just Compress</title><meta name="description" content="How Dying Soon handles local focus settings, Screen Time controls, purchases and anonymous paywall analytics."><link rel="canonical" href="https://justcompress.online/apps/dying-soon/privacy/"><link rel="stylesheet" href="/assets/portfolio-v2.css?v=20261024"><link rel="stylesheet" href="/assets/sitewide.css?v=20261024"></head><body class="portfolio-page site-public"><div class="portfolio-shell"><nav class="portfolio-nav" aria-label="Main navigation"><a class="portfolio-brand" href="/">Just Compress</a><div><a href="/apps/dying-soon/">Dying Soon</a><a href="/apps/dying-soon/support/">Support</a></div></nav><main><header class="product-heading"><h1>{escape(j['title'])}</h1><p>Updated {escape(j['updated'])}</p><p>{escape(j['intro'])}</p></header>{body}<section class="product-section"><h2>Provider policies</h2><p><a href="https://www.apple.com/legal/privacy/">Apple Privacy Policy</a> · <a href="https://www.revenuecat.com/privacy/">RevenueCat Privacy Policy</a></p><p><a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Apple Standard End User License Agreement</a> · <a href="mailto:support@justcompress.online">Contact Space Sheep Studio</a></p></section></main></div></body></html>'''
assert 'Space Sheep Studio' in page
p=R/'apps/dying-soon/privacy/index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(page+'\n')
p=R/'scripts/app-portfolio.json';data=json.loads(p.read_text());apps=data['apps'] if isinstance(data,dict) else data
for app in apps:
 if app['id']=='6758529772':app['privacy']='https://justcompress.online/apps/dying-soon/privacy/'
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Rendered app-specific policy and updated maintained URL')
