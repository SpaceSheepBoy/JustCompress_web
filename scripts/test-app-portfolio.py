"""Check the complete public surface and curated current portfolio before publishing."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,unquote
import json,re,subprocess,tempfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
apps=json.loads((ROOT/'scripts/app-portfolio.json').read_text())['apps']
assert len(apps)==11
paths=[];errors=[];scripts=0
for p in ROOT.rglob('*.html'):
 rel=p.relative_to(ROOT)
 if any(x.startswith('.') or x in ('scripts','vendor','node_modules') for x in rel.parts):continue
 route='/'+str(rel.parent).strip('.')+'/' if len(rel.parts)>1 else '/'
 raw=p.read_text();s=BeautifulSoup(raw,'html.parser');paths.append(route)
 for pattern in ['jiali liang','tibetan mantra counter','paris ciné','6758589823','6758589915']:
  assert pattern not in raw.lower(),(rel,pattern)
 assert len(s.select('h1'))==1,(rel,'h1')
 assert s.select_one('meta[name="description"]')['content'].strip(),rel
 assert s.select_one('link[rel="canonical"]')['href']=='https://justcompress.online'+route,(rel,'canonical')
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
assert len(catalog.select('[data-app]'))==11
for a in apps:
 s=BeautifulSoup((ROOT/'apps'/a['slug']/'index.html').read_text(),'html.parser')
 assert a['name'] in s.h1.get_text() and a['version'] in s.get_text()
 assert s.select_one(f'a[href="{a["store_url"]}"]'),a['slug']
 for shot in s.select('img'):assert shot.get('width') and shot.get('height') and shot.get('alt'),a['slug']
 locales=['','zh-Hans/','zh-Hant/','fr/','de/','es/','pt/','ja/','ko/','ar/','id/','th/']
 for locale in locales:
  s=BeautifulSoup((ROOT/'apps/collage-maker'/locale/'index.html').read_text(),'html.parser')
  assert len(s.select('link[hreflang]'))==13,(locale,'language alternatives')
site=ET.parse(ROOT/'sitemap.xml').getroot();ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[x.text for x in site.findall('s:url/s:loc',ns)]
assert len(urls)==len(set(urls))
for url in urls:
 p=ROOT/urlsplit(url).path.strip('/')/'index.html'
 assert p.exists(),url
 assert not BeautifulSoup(p.read_text(),'html.parser').select_one('meta[name="robots"][content*="noindex"]'),url
for a in apps:assert 'https://justcompress.online/apps/'+a['slug']+'/' in urls
print(json.dumps({'pages':len(paths),'inline_scripts_syntax_checked':scripts,'apps':len(apps),'sitemap_urls':len(urls),'excluded_apps_absent':True,'result':'PASS'}))
