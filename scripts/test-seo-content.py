"""Regressions for complete legacy guides and truthful generated FAQ output."""
from pathlib import Path
import json,subprocess,tempfile,shutil
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
for p in json.loads((ROOT/'scripts/seo-content.json').read_text()):
 s=BeautifulSoup((ROOT/p['slug']/'index.html').read_text(),'html.parser')
 text=s.get_text(' ',strip=True)
 for heading,body in p['sections']:
  assert heading in text and body in text,(p['slug'],'missing maintained section')
 assert len(s.select('h1'))==1
 assert s.select_one('img[alt]')
 for node in s.select('script[type="application/ld+json"]'):json.loads(node.string)
 assert '100MB' not in text and '16MB' not in text
 assert s.select_one('link[rel="canonical"]')['href']=='https://justcompress.online/'+p['slug']+'/'
for f in (ROOT/'blog').glob('*/index.html'):
 s=BeautifulSoup(f.read_text(),'html.parser');a=s.select_one('article.prose')
 assert s.select_one('#full-guide[open]') and s.select_one('a[href*="apps.apple.com"]'),(f,'missing open guide or store CTA')
 assert a and len(a.select('h2'))>=5,(f,'truncated article')
 assert a.select_one('img[alt]'),(f,'missing explanatory image')
 for script in s.select('script[type="application/ld+json"]'):
  data=json.loads(script.string)
  if data.get('@type')=='FAQPage':
   for q in data['mainEntity']:assert q['acceptedAnswer']['text'] in a.get_text(' ',strip=True),(f,'FAQ differs from visible answer')
assert 'jc_blog_views' not in (ROOT/'blog/index.html').read_text()
# A realistic compacting fixture proves that all sections and steps survive the layout pass.
with tempfile.TemporaryDirectory() as td:
 p=Path(td);(p/'scripts').mkdir();(p/'assets').mkdir()
 shutil.copy(ROOT/'scripts/compact-pages.py',p/'scripts/compact-pages.py')
 html='<html><head></head><body><article class="prose"><p>First sentence. Essential second sentence.</p><h2>Keep this heading</h2><p>Keep the entire explanation.</p><ol>'+''.join('<li>Step '+str(i)+'</li>' for i in range(6))+'</ol></article></body></html>'
 (p/'index.html').write_text(html)
 subprocess.run(['python3',str(p/'scripts/compact-pages.py')],check=True,capture_output=True)
 s=BeautifulSoup((p/'index.html').read_text(),'html.parser')
 assert 'Essential second sentence.' in s.get_text() and s.h2 and len(s.select('article li'))==6
print('PASS: complete maintained sections, FAQ/body parity, metadata, diagrams, no synthetic counts, non-destructive compacting')
