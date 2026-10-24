"""Normalize maintained public pages without replacing tool logic or policy bodies."""
from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
from urllib.parse import urlsplit
import json,re
ROOT=Path(__file__).resolve().parents[1];SITE='https://justcompress.online'
APPS=json.loads((ROOT/'scripts/app-portfolio.json').read_text())['apps'];BY_ID={a['id']:a for a in APPS};BY_SLUG={a['slug']:a for a in APPS}
NAMES={'Just PDF Compressor':BY_ID['6769762323']['name'],'Just PDF Watermark':BY_ID['6769761016']['name'],'Just Audio Compressor':BY_ID['6769563659']['name'],'Just Video Compressor':BY_ID['6769563339']['name'],'Homebrew Calculator: Brew Day':BY_ID['6811067941']['name']}
ICONS={f'/assets/icons/app-{key}.png':BY_ID[appid]['icon']['src'] for key,appid in [('pdf','6769762323'),('watermark','6769761016'),('audio','6769563659'),('video','6769563339')]}
FIXES=json.loads((ROOT/'scripts/public-copy-fixes.json').read_text())
PENDING={'audiofix','dpi','livephoto','talknice','camrecorder','retrophone'}
def clean(text):
 for old,new in ICONS.items():text=text.replace(old,new)
 for old,new in NAMES.items():text=text.replace(old,new)
 for old,new in [('Audio Compressor MP3 Converter Pro','Audio Compressor Pro'),('PDF Compressor: Sign & Merge Pro','PDF Compressor Pro'),('PDF Watermark & Stamp Pro','PDF Watermark Pro'),('Video Compressor & MP4 Convert Pro','Video Compressor Pro')]:text=text.replace(old,new)
 text=text.replace('100% Private','Local file processing').replace('install the free ','install ').replace('get the free iPhone app','see the iPhone App and its purchase options')
 for a in APPS:text=text.replace('free '+a['name'],a['name'])
 return re.sub(r'jiali\s+liang','Space Sheep Studio',text,flags=re.I).replace('—',', ').replace('–','-')
def set_description(s,text):
 meta=s.find('meta',attrs={'name':'description'})
 if not meta:meta=s.new_tag('meta',attrs={'name':'description'});s.head.append(meta)
 meta['content']=text
 for key in ['og:description','twitter:description']:
  el=s.find('meta',attrs={'property':key}) or s.find('meta',attrs={'name':key})
  if el:el['content']=text
changed=[]
for p in ROOT.rglob('*.html'):
 rel=p.relative_to(ROOT)
 if any(x.startswith('.') or x in ['scripts','vendor','node_modules'] for x in rel.parts):continue
 raw=p.read_text();s=BeautifulSoup(raw,'html.parser')
 if not s.html:continue
 if not s.head:
  head=s.new_tag('head')
  for el in list(s.html.children):
   if getattr(el,'name',None) in ['meta','title','link','style']:head.append(el.extract())
  s.html.insert(0,head)
 if not s.body:
  body=s.new_tag('body')
  for el in list(s.html.children):
   if el is not s.head:body.append(el.extract())
  s.html.append(body)
 # Text nodes, attributes and embedded schemas retain the current full product identity.
 for text in list(s.find_all(string=True)):
  if text.parent.name=='style':continue
  new=clean(str(text))
  if text.parent.name=='script' and text.parent.get('type')!='application/ld+json':
   for app in APPS:
    new=re.sub(r'https://apps\.apple\.com/(?:[a-zA-Z-]+/)?app/[^\s\"\'<>?]+/id'+app['id'],app['store_url'],new)

  if new!=str(text):text.replace_with(new)
 for el in s.find_all(True):
  for attr in ['title','alt','aria-label','content','value']:
   if attr in el.attrs and isinstance(el[attr],str):el[attr]=clean(el[attr])
 # Keep one common document heading on existing multilingual policy/support pages.
 h1s=s.select('h1')
 if len(h1s)>1:
  for node in h1s:node.name='h2'
  title=s.new_tag('h1');title.string=clean(s.title.get_text().split('|')[0] if s.title else h1s[0].get_text(' ',strip=True))
  target=s.find('main') or s.body
  nav=target.find('nav')
  if nav:nav.insert_after(title)
  else:target.insert(0,title)
 url=SITE+'/'+str(rel).removesuffix('index.html')
 canonical=s.find('link',rel='canonical')
 if not canonical:canonical=s.new_tag('link',rel='canonical');s.head.append(canonical)
 canonical['href']=url
 if not s.select_one('meta[name="description"]'):
  heading=s.find('h1');name=heading.get_text(' ',strip=True) if heading else s.title.get_text()
  set_description(s,clean(name+'. Current product information, privacy details or support from Space Sheep Studio.')[:170])
 # Visible answers and FAQ structured data describe the same supported behavior.
 for question,answer in FIXES.get(rel.parts[0],{}).items():
  for item in s.select('.faq-item'):
   summary=item.find('summary')
   if summary and question in summary.get_text(' ',strip=True):
    body=item.select_one('.faq-body')
    if body:body.clear();paragraph=s.new_tag('p');paragraph.string=answer;body.append(paragraph)
  for node in s.select('script[type="application/ld+json"]'):
   try:data=json.loads(node.string or node.get_text())
   except Exception:continue
   if data.get('@type')=='FAQPage':
    for entry in data.get('mainEntity',[]):
     if entry.get('name')==question:entry['acceptedAnswer']['text']=answer
    node.string=json.dumps(data,ensure_ascii=False).replace('</','<\\/')
 # Current product support summaries must not advertise superseded identities or draft availability.
 if len(rel.parts)==4 and rel.parts[0]=='apps' and rel.parts[1] in BY_SLUG:
  app=BY_SLUG[rel.parts[1]]
  for para in s.select('p'):
   text=para.get_text(' ',strip=True)
   if 'listing is being prepared' in text:
    para.clear();para.append('The current published App is '+app['name']+'. ');link=s.new_tag('a',href=app['store_url']);link.string='View the current App Store listing';para.append(link)
   if rel.parts[2]=='support' and text.startswith(('Compress, convert, split, trim, merge','Compress, sign, merge, convert JPG','Use your screen as a glow light')):para.string=app['benefit']+'. See the current product page for published features and access options.'
   if 'provided by Space Sheep Studio for iPhone, iPad and Mac.' in text:para.string=text.replace('provided by Space Sheep Studio for iPhone, iPad and Mac.','provided by Space Sheep Studio. A separate native Mac App Store listing has not been verified; Mac-build details below are retained for support.')
  if rel.parts[1]=='photofix':
   for node in s.select('.pill'):
    if 'help' in node.get_text():node.string='PhotoFix '+app['version']+' support'
  if rel.parts[1]=='videofix' and rel.parts[2]=='support':
   heading=next((h for h in s.select('h2') if h.get_text(' ',strip=True)=='Convert a video'),None)
   if heading:
    para=heading.find_next_sibling('p')
    if para:para.string='Select a video and choose the conversion goal. The current listing describes Convert HDR to SDR for a standard-color H.264 MP4 copy, frame-rate conversion and audio extraction. Export a separate copy and check its size, sound, color and destination playback before using a full batch.'
   mac=next((h for h in s.select('h2') if 'on Mac' in h.get_text()),None)
   if mac and not s.select_one('[data-mac-availability]'):
    note=s.new_tag('p',attrs={'data-mac-availability':''});note.string='The following Mac-build support information is retained for existing workflows. A separate public native Mac App Store release has not been verified in the checked storefronts.';mac.insert_after(note)
 # A new CSS revision avoids stale cached tutorial presentation.
 for css in s.select('link[href^="/assets/tutorial-guides.css"]'):css['href']='/assets/tutorial-guides.css?v=20261024-portfolio'
 # Resolve legacy App Store slugs by stable numeric identity, keeping other query options.
 for link in s.select('a[href]'):
  href=link['href'];match=re.search(r'apps\.apple\.com/.*?/id(\d+)|apps\.apple\.com/app/id(\d+)',href)
  if match:
   appid=match.group(1) or match.group(2)
   if appid in BY_ID:
    suffix=('?'+href.split('?',1)[1]) if '?' in href else ''
    # Localized product URLs keep their verified target storefront.
    if not (len(rel.parts)>3 and rel.parts[:2]==('apps','collage-maker') and rel.parts[2] in ['zh-Hans','zh-Hant','fr','de','es','pt','ja','ko','ar','id','th']):link['href']=BY_ID[appid]['store_url']+suffix
 # Refresh legacy App icons and screenshots from actual current store assets.
 counters={}
 for img in s.select('img[src]'):
  src=img['src'];alt=img.get('alt','')
  if src in ICONS:img['src']=ICONS[src];continue
  if not re.search(r'https://is\d+-ssl\.mzstatic\.com',src):continue
  app=None
  for a in APPS:
   if a['name'] in alt or (a['slug']=='videofix' and 'VideoFix' in alt):app=a;break
  if not app and 'brew' in alt.lower():app=BY_ID['6811067941']
  if app:
   if 'AppIcon' in src or 'icon' in alt.lower():m=app['icon']
   else:
    n=counters.get(app['id'],0);m=app['screenshots'][n%len(app['screenshots'])];counters[app['id']]=n+1
   img['src']=m['src'];img['width']=m['width'];img['height']=m['height']
 # Open maintained guide bodies instead of hiding incomplete-looking answers.
 for details in s.select('details.visual-guide'):details['open']=''
 # Availability notes are not a claim that an unpublished native build is on sale.
 pending=len(rel.parts)==3 and rel.parts[0]=='apps' and rel.parts[1] in PENDING
 if pending:
  robots=s.find('meta',attrs={'name':'robots'})
  if not robots:robots=s.new_tag('meta',attrs={'name':'robots'});s.head.append(robots)
  robots['content']='noindex,follow'
  if not s.select_one('[data-store-availability]'):
   note=s.new_tag('aside',attrs={'data-store-availability':'','class':'availability-note'});note.string='Public App Store availability has not been verified in the checked US and French storefronts. This page is retained for product and support information. Browse our available Apps for current downloads.'
   (s.find('h1') or s.find('main')).insert_after(note)
  for a in s.select('a[href*="apps.apple.com"]'):a['href']='/apps/';a.string='Browse available iPhone apps'
 s.body['class']=list(dict.fromkeys(s.body.get('class',[])+['site-public']))
 if not s.select_one('link[href^="/assets/sitewide.css"]'):s.head.append(s.new_tag('link',rel='stylesheet',href='/assets/sitewide.css?v=20261024'))
 text=str(s)
 if text!=raw:p.write_text(text);changed.append(str(rel))
print('Normalized public pages:',len(changed))
