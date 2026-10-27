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
 # Product pages and catalog are generated from the verified portfolio below.
print('Connected tutorials, CTAs and product entries for',m.HOST)

# Existing legal/product metadata is preserved after page generators.
import subprocess,sys
subprocess.run([sys.executable,str(ROOT/'scripts/repair-seo-metadata.py')],check=True)

# Verified public product snapshots own the App pages and directory.
subprocess.run([sys.executable,str(ROOT/'scripts/build-app-portfolio.py')],check=True)

subprocess.run([sys.executable,str(ROOT/'scripts/refresh-public-pages.py')],check=True)

# Preserve the improved tutorial at its existing URL after legacy generators run.
if not m.CAPTIONS:
 path='/iphone-video-tutorials/10-how-to-extract-audio-from-video-on-iphone/'
 title='How to Extract Audio from Video on iPhone'
 description='Save the sound from an iPhone video as a separate audio file. Three clear steps, real App images, and a recorded walkthrough.'
 body=(ROOT/'scripts/guide-layouts/extract-audio-iphone.html').read_text().replace('{{DATE}}','2026-10-26').replace('{{CTA}}',m.cta('6769563659'))
 schema=m.ld({'@type':'Article','headline':title,'description':description,'dateModified':'2026-10-26','mainEntityOfPage':m.HOST+path,'author':{'@type':'Organization','name':'Space Sheep Studio'}})
 schema+=m.ld({'@type':'HowTo','name':title,'step':[{'@type':'HowToStep','name':'Choose the clip','text':'Open Extract from Video in Audio Compressor MP3 Converter and select your video.'},{'@type':'HowToStep','name':'Extract the audio','text':'Tap Extract Audio from Video and keep the App open while it processes.'},{'@type':'HowToStep','name':'Save and listen','text':'Tap Save audio, choose a location, and play the saved file to check the sound.'}]})
 html=m.page(path,title,description,body,schema).replace('</head>','<meta name="apple-itunes-app" content="app-id=6769563659"></head>')
 (ROOT/path.strip('/')/'index.html').write_text(html)

# Weblate catalogs are compiled last so legacy normalization cannot overwrite
# localized store names, consent UI or language metadata.
if not m.CAPTIONS and (ROOT/'locales/review.json').exists():
 subprocess.run([sys.executable,str(ROOT/'scripts/i18n_pages.py')],check=True)

# Articles use the same locale registry and reviewed Weblate exports.
if not m.CAPTIONS and (ROOT/'locales/articles/config.json').exists():
 subprocess.run([sys.executable,str(ROOT/'scripts/article_i18n.py'),'build'],check=True)
