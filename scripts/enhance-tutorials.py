"""Connect maintained guides to existing pages. Re-run after legacy page generators."""
from pathlib import Path
from bs4 import BeautifulSoup
import importlib.util,json,re
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('tutorials',ROOT/'scripts/build-tutorial-guides.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
E=m.E

def read(rel):return BeautifulSoup((ROOT/rel).read_text(),'html.parser')
def save(rel,s):
 if not s.select_one('link[href^="/assets/tutorial-guides.css"]'):s.head.append(BeautifulSoup('<link rel="stylesheet" href="/assets/tutorial-guides.css?v=20261022">','html.parser'))
 text=str(s).replace('—',', ').replace('–','-')
 text=re.sub(r'Space Sheep Studio','Space Sheep Studio',text,flags=re.I)
 (ROOT/rel).write_text(text)
def fragment(html):return BeautifulSoup(html,'html.parser')
def insert(rel,html,top=False):
 s=read(rel)
 for old in s.select('[data-tutorial-library]'):old.decompose()
 block=fragment('<section class="guide-enhancement" data-tutorial-library>'+html+'</section>')
 if rel=='index.html' and m.CAPTIONS:s.select_one('#faq').insert_before(block)
 elif top and s.find('main'):s.find('main').insert(0,block)
 elif s.find('main'):s.find('main').append(block)
 elif s.find('footer'):s.find('footer').insert_before(block)
 else:s.body.append(block)
 save(rel,s)

featured=m.GUIDES[:3] if not m.CAPTIONS else [m.GUIDES[0],m.GUIDES[4],m.GUIDES[6]]
html='<h2>Watch it. Follow the steps.</h2><p>Real app tutorials with written instructions, export checks and a direct download for the task.</p><div class="guide-grid">'+''.join(m.card(g) for g in featured)+'</div><a class="guide-button" href="/guides/">Browse all guides →</a>'
insert('index.html',html)
s=read('index.html')
if m.CAPTIONS:
 nav=s.select_one('.nav-links')
 if nav and not nav.find('a',href='/guides/'):nav.append(fragment('<a href="/guides/">Guides</a>'))
 hero=s.select_one('#hero')
 if hero and not hero.find('a',href='/guides/'):
  target=hero.select_one('.container') or hero
  target.append(fragment('<p><a href="/guides/" style="font-weight:700;text-decoration:underline">Watch tutorials and read the guides →</a></p>'))
else:
 nav=s.find('nav')
 if not nav.find('a',href='/guides/'):nav.append(fragment('<a class="apps-link" href="/guides/">Video guides →</a>'))
save('index.html',s)
if m.CAPTIONS:
 insert('blog/index.html','<h2>New Mac and iPhone video tutorials</h2><p>Follow the workflows from our published videos, with written steps and checks before export.</p><div class="guide-grid">'+''.join(m.card(g) for g in m.GUIDES)+'</div><a class="guide-button" href="/guides/">All tutorial guides →</a>',True)
 pairs=[('how-to-batch-add-captions-to-videos/index.html','tcOnFMhTPyc'),('how-to-translate-captions-to-multiple-languages/index.html','REZqqA01lbY')]
 for rel,i in pairs:insert(rel,m.cta('6770354079')+m.video(i)+'<p><a href="/guides/batch-translate-captions-iphone/">Translating several clips? Read the batch translation guide →</a></p>',True)
 insert('mac/index.html','<h2>Learn the Mac app</h2><p>Watch the real captioning, editing and batch export workflows.</p><div class="guide-grid">'+''.join(m.card(g) for g in m.GUIDES[:3])+'</div><a class="guide-button" href="/guides/">All Mac and iPhone guides →</a>')
 # Add a visible conversion route to the existing educational pages.
 for rel in ['create-srt-file-on-iphone/index.html','add-captions-to-tiktok/index.html','add-captions-to-instagram-reels/index.html','add-captions-to-youtube-shorts/index.html','how-to-use-ai-to-correct-transcriptions/index.html','how-to-use-ai-to-translate-captions/index.html','blog/how-to-add-captions-to-a-video-on-iphone/index.html']:
  insert(rel,m.cta('6770354079')+'<p><a href="/guides/">Watch our app tutorials →</a></p>',True)
else:
 for rel in ['tutorials/index.html','iphone-video-tutorials/index.html','blog/index.html']:
  insert(rel,'<h2>New video and photo guides</h2><p>HDR, HEVC, Apple Log, batch conversion, photo grids and smaller sharing copies.</p><div class="guide-grid">'+''.join(m.card(g) for g in m.GUIDES[:3])+'</div><a class="guide-button" href="/guides/">Open the new tutorial library →</a>',True)
 pairs=[('m4a-to-mp3/index.html','EU0W-v6kYxA','6769563659'),('trim-audio/index.html','X8c04hiaAQc','6769563659'),('compress-audio-file-iphone/index.html','W3_ZMT3zfQ8','6769563659'),('compress-video/index.html','58vkRfxA3lQ','6769563339'),('combine-photos/index.html','nqSEzQ1BOcc','6810266264')]
 for rel,i,app in pairs:
  insert(rel,m.video(i)+m.cta(app)+'<p><a href="/guides/">More app walkthroughs →</a></p>')
 # Keep the existing fifteen tutorial URLs and their videos. Refresh app identity and CTA.
 for p in (ROOT/'iphone-video-tutorials').glob('*/index.html'):
  rel=str(p.relative_to(ROOT));s=read(rel)
  if 'audio' in str(p) or 'm4a' in str(p):app='6769563659';old='Just Audio Compressor'
  elif 'watermark' in str(p):app='6769761016';old='Just PDF Watermark'
  else:app='6769762323';old='Just PDF Compressor'
  for text in s.find_all(string=True):
   if old in text:text.replace_with(str(text).replace(old,m.PRODUCTS[app]['name']))
  save(rel,s);insert(rel,m.cta(app)+'<p><a href="/guides/">New video and photo tutorials →</a></p>',True)
 # App-specific connections, with no unrelated catalog in the captions product site.
 for app,slug in [('6812821310','videofix'),('6810266264','collage-maker'),('6769563339','vidkit'),('6769563659','audio-compressor')]:
  rel=f'apps/{slug}/index.html'
  if (ROOT/rel).exists():
   linked=[g for g in m.GUIDES if g['app']==app]
   insert(rel,m.cta(app)+'<h2>Learn with real app tutorials</h2><div class="guide-grid">'+''.join(m.card(g) for g in linked)+'</div><p><a href="/iphone-video-tutorials/">Audio and PDF walkthroughs</a> · <a href="/guides/">All guides</a></p>')
 # New, live and stale product entries use verified App Store identity and real screenshots.
 slugs={'6812821310':'videofix','6769563659':'audio-compressor','6810266264':'collage-maker','6769563339':'vidkit','6770354079':'just-captions','6769761016':'pdf-watermarker','6769762323':'pdf-compressor','6778131414':'glowpop','6816526877':'photofix','6758529772':'dying-soon','6811067941':'brew-day'}
 for app,slug in slugs.items():
  rel=f'apps/{slug}/index.html'
  if (ROOT/rel).exists() and slug not in ['photofix','brew-day']:continue
  p=m.PRODUCTS[app];paragraphs=p['description'].split('\n\n')
  text=''.join('<p>'+E(t).replace('\n','<br>')+'</p>' for t in paragraphs if not t.startswith(('Terms','Privacy')))
  shots=''.join(f'<img src="{E(u)}" alt="{E(p["name"])} official App Store screenshot" width="200" loading="lazy">' for u in p['screenshots'])
  links=''.join(f'<a href="/apps/{slug}/{d}/">{d.capitalize()}</a> ' for d in ['privacy','terms','support'] if (ROOT/f'apps/{slug}/{d}/index.html').exists())
  body=f'<header class="guide-heading"><p class="guide-eyebrow">IPHONE APP</p><h1>{E(p["name"])}</h1>{m.cta(app)}</header><article class="guide-article"><section><h2>What the app does</h2>{text}</section><section style="display:flex;gap:16px;overflow-x:auto">{shots}</section><p>{links}</p><p><a href="/guides/">Browse the tutorial guides</a> · <a href="/apps/">All apps</a></p></article>'
  dest=ROOT/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(m.page('/apps/'+slug+'/',p['name'],paragraphs[0][:160],body));save(rel,read(rel))
 pending={
  'livephoto':('Live Photo to Video: 4K','Convert selected Live Photos and videos on your device using Apple frameworks. The app supports saving results to Photos or Files.','Live Photo conversion'),
  'talknice':('TalkNice: AI Voice Keyboard','Turn speech into text and optionally rewrite messages in a kinder tone. Cloud audio and text tools require the applicable in-app consent. Read the privacy information for current providers and data flow.','Voice keyboard'),
  'camrecorder':('CamRecorder: Camera Recorder','Capture camera video and microphone audio on Mac. Camera processing and background blur run locally. Read the support page for the app workflow and permissions.','Mac camera recorder')}
 for slug,(name,desc,kind) in pending.items():
  rel=f'apps/{slug}/index.html'
  if (ROOT/rel).exists():continue
  body=f'<header class="guide-heading"><p class="guide-eyebrow">{E(kind)}</p><h1>{E(name)}</h1><p class="guide-lede">{E(desc)}</p></header><article class="guide-article"><h2>Availability</h2><p>Download availability is being confirmed. For product questions, use the support page.</p><p><a class="guide-button" href="/apps/{slug}/support/">Product support →</a></p><p><a href="/apps/{slug}/privacy/">Privacy</a> · <a href="/apps/">Browse available apps</a></p></article>'
  dest=ROOT/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(m.page('/apps/'+slug+'/',name,desc[:160],body));save(rel,read(rel))
 s=read('apps/index.html')
 s.title.string='iPhone apps, tutorials and downloads | Just Compress'
 s.find('meta',attrs={'name':'description'})['content']='Find the app from our videos. Browse verified iPhone downloads, practical tutorials and new app information from Space Sheep Studio.'
 for old in s.select('[data-tutorial-library]'):old.decompose()
 for app,slug in slugs.items():
  p=m.PRODUCTS[app];card=s.select_one(f'[data-app="{app}"]')
  if card:
   card.find('h2').string=p['name'];card.find('input')['value']=p['name']
   for a in card.select('[data-store]'):a['href']=p['url'];a['aria-label']='Download '+p['name']+' on the App Store'
   if app=='6811067941':
    b=card.select_one('.benefit')
    if b:b.string='Track your alcohol-free days'
  else:
   card=fragment(f'<article class="app-card tone-4" id="{slug}" data-app="{app}"><div class="card-body"><div class="identity"><img class="app-icon" src="{E(p["icon"])}" alt="" width="56" height="56" loading="lazy"><div><h2>{E(p["name"])}</h2><p class="benefit">{E("Convert HDR, HEIC and RAW photos" if slug=="photofix" else "Screen time and memento mori")}</p></div></div><input id="name-{app}" type="hidden" value="{E(p["name"])}"><div class="actions"><a class="store" data-store href="{E(p["url"])}">App Store ↗</a><button type="button" data-copy="name-{app}">Copy name</button></div></div></article>').article
   s.select_one('.more .app-grid').append(card)
  cb=card.select_one('.card-body')
  if not cb.find('a',href=f'/apps/{slug}/'):cb.append(fragment(f'<p><a href="/apps/{slug}/" style="text-decoration:underline">App details &amp; guides →</a></p>'))
 summary=s.select_one('.more summary, .more-title')
 if summary:summary.clear();summary.append('More apps ');summary.append(str(len(s.select('.more .app-card'))))
 catalog='<h2>New app information</h2><p>Product and support pages for our newest apps. Download availability is being confirmed.</p><ul>'+''.join(f'<li><a href="/apps/{slug}/">{E(name)}</a></li>' for slug,name in [('audiofix','Audio Fix (in development)'),('dpi','DPI Changer: 300 DPI Photo'),('livephoto','Live Photo to Video: 4K'),('talknice','TalkNice: AI Voice Keyboard'),('camrecorder','CamRecorder: Camera Recorder')])+'</ul><p><a class="guide-button" href="/guides/">Watch tutorials and follow the steps →</a></p>'
 s.find('main').append(fragment('<section class="guide-enhancement" data-tutorial-library>'+catalog+'</section>'))
 save('apps/index.html',s)
 # Source inputs must retain the verified names after the old generator is run.
 for p in ROOT.rglob('*.html'):
  if '.git' in p.parts:continue
  raw=p.read_text();new=re.sub(r'Space Sheep Studio','Space Sheep Studio',raw,flags=re.I)
  if new!=raw:p.write_text(new)
 for p in (ROOT/'scripts').iterdir():
  if p.suffix in ['.mjs','.json','.py']:
   raw=p.read_text();new=re.sub(r'Space Sheep Studio','Space Sheep Studio',raw,flags=re.I)
   if new!=raw:p.write_text(new)
print('Connected tutorials, CTAs and product entries for',m.HOST)
