"""Check the complete public surface and curated current portfolio before publishing."""
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
from urllib.parse import urlsplit,unquote
import json,re,subprocess,tempfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
apps=json.loads((ROOT/'scripts/app-portfolio.json').read_text())['apps']
display_order=json.loads((ROOT/'scripts/app-display-order.json').read_text())['app_ids']
assert len(apps)==len({a['id'] for a in apps})
assert len(display_order)==len(set(display_order)) and set(display_order)=={a['id'] for a in apps}
# The website must never render Apple lookup's 221x480 thumbnail assets as store screenshots.
shot_records=[(s,a.get('platform','iOS')) for a in apps for s in a['screenshots']]
shot_records += [(s,'iOS') for locale in json.loads((ROOT/'scripts/collage-localizations.json').read_text()).values() for s in locale['screenshots']]
for shot,platform in shot_records:
 if platform=='macOS':
  assert shot['width']>=2000 and shot['height']>=1000,(shot['src'],'low-resolution Mac screenshot')
  assert shot['source'].endswith('/0x0ss.png'),(shot['src'],'Mac screenshot must use native Apple source')
 else:
  assert shot['width']>=1000 and shot['height']>=2000,(shot['src'],'low-resolution iPhone screenshot')
 with Image.open(ROOT/shot['src'].lstrip('/')) as pixels:
  assert pixels.size==(shot['width'],shot['height']),(shot['src'],'incorrect intrinsic dimensions')
paths=[];errors=[];scripts=0
for p in ROOT.rglob('*.html'):
 rel=p.relative_to(ROOT)
 if any(x.startswith('.') or x in ('scripts','vendor','node_modules') for x in rel.parts):continue
 route='/'+str(rel.parent).strip('.')+'/' if len(rel.parts)>1 else '/'
 raw=p.read_text();s=BeautifulSoup(raw,'html.parser');paths.append(route)
 for pattern in ['jiali liang','tibetan mantra counter','paris ciné','6758589823','6758589915']:
  assert pattern not in raw.lower(),(rel,pattern)
 assert len(s.select('h1'))==1,(rel,'h1')
 description=s.select_one('meta[name="description"]')
 assert description and description.get('content','').strip(),(rel,'missing meta description')
 redirect=s.select_one('[data-site-redirect]')
 expected=redirect['data-site-redirect'] if redirect else route
 assert s.select_one('link[rel="canonical"]')['href']=='https://justcompress.online'+expected,(rel,'canonical')
 if redirect:
  assert s.select_one('meta[http-equiv="refresh"]')['content']=='0;url='+expected,(rel,'redirect')
  assert (ROOT/expected.strip('/')/'index.html').exists(),(rel,'redirect destination')
  assert not BeautifulSoup((ROOT/expected.strip('/')/'index.html').read_text(),'html.parser').select_one('[data-site-redirect]'),(rel,'redirect chain')
 for node in s.select('script[type="application/ld+json"]'):json.loads(node.string)
 for el in s.select('[href],img[src],script[src]'):
  val=el.get('href') or el.get('src');u=urlsplit(val)
  if u.scheme or u.netloc or not u.path:continue
  dest=ROOT/unquote(u.path).lstrip('/') if u.path.startswith('/') else p.parent/unquote(u.path)
  if u.path.endswith('/'):dest=dest/'index.html'
  assert dest.exists(),(rel,val,'missing local target')
 for node in s.select('script:not([src])'):
  if node.get('type','') not in ('','text/javascript','module'):continue
  with tempfile.NamedTemporaryFile(suffix='.mjs',mode='w') as f:
   f.write(node.string or node.get_text());f.flush()
   r=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
   assert r.returncode==0,(rel,r.stderr)
   scripts+=1
catalog=BeautifulSoup((ROOT/'apps/index.html').read_text(),'html.parser')
assert len(catalog.select('[data-app]'))==len(apps)
assert {el['data-app'] for el in catalog.select('[data-app]')}=={a['id'] for a in apps}
for a in apps:
 s=BeautifulSoup((ROOT/'apps'/a['slug']/'index.html').read_text(),'html.parser')
 assert (a['name'] in s.h1.get_text() or a['name'] in s.title.get_text()) and a['version'] in s.get_text(),(a['slug'],'published name/version differs from portfolio snapshot')
 assert s.select_one(f'a[href="{a["store_url"]}"]'),a['slug']
 if a.get('platform')=='macOS':
  assert 'for Mac' in s.title.get_text() and 'macOS' in s.get_text(),a['slug']
  assert 'platform=mac' in a['store_url'],a['slug']
  schema=[json.loads(n.string) for n in s.select('script[type="application/ld+json"]')]
  assert any(n.get('@type')=='SoftwareApplication' and n.get('operatingSystem','').startswith('macOS') for n in schema),a['slug']
 for shot in s.select('img'):assert shot.get('width') and shot.get('height') and shot.get('alt'),a['slug']
 languages=set(json.loads((ROOT/'locales/config.json').read_text())) | set(json.loads((ROOT/'scripts/collage-localizations.json').read_text()))
 for language in languages:
  locale='' if language=='en' else language+'/'
  s=BeautifulSoup((ROOT/'apps/collage-maker'/locale/'index.html').read_text(),'html.parser')
  alternatives=s.select('link[hreflang]')
  assert len(alternatives)==len(languages)+1,(locale,'language alternatives')
  assert {node['hreflang'] for node in alternatives}==languages|{'x-default'},(locale,'missing language alternatives')
site=ET.parse(ROOT/'sitemap.xml').getroot();ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[x.text for x in site.findall('s:url/s:loc',ns)]
assert len(urls)==len(set(urls))
for url in urls:
 p=ROOT/urlsplit(url).path.strip('/')/'index.html'
 assert p.exists(),url
 assert not BeautifulSoup(p.read_text(),'html.parser').select_one('meta[name="robots"][content*="noindex"]'),url
 assert not BeautifulSoup(p.read_text(),'html.parser').select_one('[data-site-redirect]'),url
for a in apps:assert 'https://justcompress.online/apps/'+a['slug']+'/' in urls
print(json.dumps({'pages':len(paths),'inline_scripts_syntax_checked':scripts,'apps':len(apps),'sitemap_urls':len(urls),'excluded_apps_absent':True,'result':'PASS'}))
