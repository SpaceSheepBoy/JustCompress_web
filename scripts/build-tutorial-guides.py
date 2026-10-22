"""Rebuild the maintained tutorial guides and their index from scripts/tutorial-*.json."""
from pathlib import Path
from html import escape as E
import json
ROOT=Path(__file__).resolve().parents[1]
HOST='https://justcaptions.com' if (ROOT/'styles.css').exists() else 'https://justcompress.online'
CAPTIONS='justcaptions' in HOST
BRAND='Just Captions' if CAPTIONS else 'Just Compress'
GUIDES=json.loads((ROOT/'scripts/tutorial-guides.json').read_text())
PRODUCTS=json.loads((ROOT/'scripts/tutorial-products.json').read_text())
VIDEOS=json.loads((ROOT/'scripts/tutorial-videos.json').read_text())
DATE='2026-10-22'

def ld(value):
 return '<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org',**value},ensure_ascii=False).replace('</','<\\/')+'</script>'

def cta(app):
 p=PRODUCTS[app]
 url=p['url']+('?utm_source='+('justcaptions' if CAPTIONS else 'justcompress')+'&utm_medium=guide&utm_campaign=tutorial-library' if app!='mac' else '')
 label='Download for Mac' if app=='mac' else 'Get the iPhone app'
 note='macOS 14 or later. Website edition.' if app=='mac' else ('First 3 conversions free. Paid plans available.' if app=='6812821310' else 'See the App Store for current access and purchase options.')
 return f'<aside class="guide-cta"><div><strong>{E(p["name"])}</strong><p>{E(note)}</p></div><a class="guide-button" href="{E(url)}">{label} <span aria-hidden="true">↗</span></a></aside>'

def video(i):
 v=VIDEOS[i]
 return f'<section class="guide-video"><h2>Watch the real app walkthrough</h2><p>{E(v["title"])}</p><div class="guide-player"><iframe src="https://www.youtube-nocookie.com/embed/{i}" title="{E(v["title"])}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><p><a href="https://www.youtube.com/watch?v={i}">Watch on YouTube ↗</a></p></section>'

def card(g):
 thumb=f'<img src="{E(VIDEOS[g["video"]]["thumbnail"])}" width="480" height="360" alt="" loading="lazy">' if g.get('video') else ''
 return f'<a class="guide-card" href="/guides/{g["slug"]}/">{thumb}<div><span>{"Mac" if g["app"]=="mac" else "iPhone"} tutorial</span><h3>{E(g["title"])}</h3><p>{E(g["summary"])}</p><b>Read the steps →</b></div></a>'

def page(path,title,description,body,schema=''):
 url=HOST+path
 css='/styles.css?v=20261004-copy' if CAPTIONS else '/assets/home.css?v=20261002'
 return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)} | {BRAND}</title><meta name="description" content="{E(description)}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{url}"><meta property="og:type" content="{'website' if path in ('/guides/','/videos/') else 'article'}"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{css}"><link rel="stylesheet" href="/assets/tutorial-guides.css?v=20261022">{schema}</head>
<body class="guide-page {'guide-captions' if CAPTIONS else ''}"><div class="guide-shell"><nav class="guide-nav" aria-label="Main navigation"><a class="guide-brand" href="/">{BRAND}</a><div><a href="/guides/">Guides</a><a href="/videos/">Videos</a><a href="{'/mac/' if CAPTIONS else '/apps/'}">{'Download' if CAPTIONS else 'Apps'}</a><a href="{'/blog/' if CAPTIONS else '/tools/'}">{'Blog' if CAPTIONS else 'Free tools'}</a></div></nav>
<main>{body}</main><footer class="guide-footer"><span>© 2026 Space Sheep Studio</span><a href="/guides/">Guides</a><a href="/videos/">Videos</a><a href="/privacy/">Privacy</a><a href="{'/mac/terms/' if CAPTIONS else '/terms/'}">Terms</a><a href="{'https://spacesheepboy.github.io/JustCaptions-legal/support/' if CAPTIONS else '/support/'}">Support</a></footer></div></body></html>'''

for g in GUIDES:
 path='/guides/'+g['slug']+'/'
 schema=ld({'@type':'Article','headline':g['title'],'description':g['summary'],'datePublished':DATE,'dateModified':DATE,'mainEntityOfPage':HOST+path,'author':{'@type':'Organization','name':'Space Sheep Studio'},'publisher':{'@type':'Organization','name':'Space Sheep Studio'}})
 schema+=ld({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':BRAND,'item':HOST+'/'},{'@type':'ListItem','position':2,'name':'Guides','item':HOST+'/guides/'},{'@type':'ListItem','position':3,'name':g['title'],'item':HOST+path}]})
 if g.get('video') and VIDEOS[g['video']].get('published'):
  v=VIDEOS[g['video']]
  obj={'@type':'VideoObject','name':v['title'],'description':g['summary'],'thumbnailUrl':[v['thumbnail']],'embedUrl':'https://www.youtube-nocookie.com/embed/'+g['video']}
  if v.get('published'):obj['uploadDate']=v['published']
  schema+=ld(obj)
 sections=''.join(f'<section id="section-{n}"><h2>{E(h)}</h2><p>{E(t)}</p></section>' for n,(h,t) in enumerate(g['sections'],1))
 faqs=''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in g['faq'])
 names={('/guides/'+x['slug']+'/'):x['title'] for x in GUIDES}
 labels={'/hdr-video-checker/':'Check whether a video is HDR or SDR','/combine-photos/':'Try the free photo combiner','/compress-video/':'Try the free video compressor','/mac/':'Get Just Captions for Mac','/privacy/':'Read the privacy information'}
 related=''.join(f'<li><a href="{E(u)}">{E(names.get(u,labels.get(u,u.strip("/").split("/")[-1].replace("-"," ").capitalize())))}</a></li>' for u in g['related'])
 body=f'''<header class="guide-heading"><p class="guide-eyebrow">{'MAC' if g['app']=='mac' else 'IPHONE'} GUIDE · UPDATED OCTOBER 22, 2026</p><h1>{E(g['title'])}</h1><p class="guide-lede">{E(g['summary'])}</p>{cta(g['app'])}</header>
<article class="guide-article">{video(g['video']) if g.get('video') else ''}<section><h2>Follow these steps</h2><ol>{''.join('<li>'+E(t)+'</li>' for t in g['steps'])}</ol></section>{sections}<section class="guide-faq"><h2>Common questions</h2>{faqs}</section>{cta(g['app'])}<section><h2>Related guides and tools</h2><ul>{related}</ul><p><a href="/guides/">Browse all guides →</a></p></section></article>'''
 dest=ROOT/path.strip('/')/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(page(path,g['title'],g['summary'],body,schema))
body=f'<header class="guide-heading"><p class="guide-eyebrow">REAL APP WALKTHROUGHS</p><h1>{"Video caption guides for Mac and iPhone" if CAPTIONS else "iPhone video, audio and photo guides"}</h1><p class="guide-lede">Watch the tutorial, follow the written steps and open the app for the task.</p></header>'
if CAPTIONS:
 links=[('/how-to-batch-add-captions-to-videos/','Batch add captions on iPhone'),('/how-to-translate-captions-to-multiple-languages/','Translate one video into several languages'),('/guides/batch-translate-captions-iphone/','Batch translate captions on iPhone'),('/create-srt-file-on-iphone/','Export an SRT subtitle file'),('/add-captions-to-tiktok/','Captions for TikTok'),('/add-captions-to-instagram-reels/','Captions for Reels'),('/add-captions-to-youtube-shorts/','Captions for Shorts')]
 body+='<section class="guide-article"><h2>iPhone captioning guides</h2><ul>'+''.join(f'<li><a href="{u}">{E(t)}</a></li>' for u,t in links)+'</ul></section><section><h2>Mac walkthroughs</h2>'
else:body+='<section><h2>Video and photo walkthroughs</h2>'
body+='<p><a class="guide-button" href="/videos/">Browse all video walkthroughs →</a></p><div class="guide-grid">'+''.join(card(g) for g in GUIDES if not CAPTIONS or g['app']=='mac')+'</div></section>'
if not CAPTIONS:body+='<section class="guide-article"><h2>Audio and PDF tutorials</h2><p>Convert M4A to MP3, trim audio, compress a voice memo, make PDFs smaller, sign documents and more.</p><a class="guide-button" href="/iphone-video-tutorials/">Watch audio and PDF tutorials →</a><p><a href="/tutorials/">Browse browser-tool help</a> · <a href="/apps/">Find your iPhone app</a></p></section>'
else:body+=cta('mac')
schema=ld({'@type':'CollectionPage','name':'Tutorial guides','url':HOST+'/guides/','mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':g['title'],'url':HOST+'/guides/'+g['slug']+'/'} for i,g in enumerate(GUIDES)]}})
(ROOT/'guides').mkdir(exist_ok=True);(ROOT/'guides/index.html').write_text(page('/guides/','Tutorial guides', 'Practical tutorials with real app videos, written steps, export checks and download links.',body,schema))

# Every verified published walkthrough remains findable without creating a thin article for each duplicate.
site='justcaptions' if CAPTIONS else 'justcompress'
items=sorted([(i,v) for i,v in VIDEOS.items() if v.get('site')==site],key=lambda pair:pair[1].get('published') or '',reverse=True)
body='<header class="guide-heading"><p class="guide-eyebrow">OUR PUBLISHED WALKTHROUGHS</p><h1>'+('Captioning video tutorials for Mac and iPhone' if CAPTIONS else 'iPhone video tutorials')+'</h1><p class="guide-lede">Watch the app in use, then open the matching written guide. Includes earlier and localized walkthroughs.</p></header><section><div class="guide-grid">'
for i,v in items:
 body+=f'<article class="guide-card"><a href="https://www.youtube.com/watch?v={i}"><img src="{E(v["thumbnail"])}" width="480" height="360" alt="" loading="lazy" style="width:100%;height:auto;aspect-ratio:16/9;object-fit:cover"></a><div><h2 style="font-size:20px">{E(v["title"])}</h2><p><a href="https://www.youtube.com/watch?v={i}">Watch on YouTube ↗</a></p><p><a href="{v["guide"]}">Written guide and app →</a></p></div></article>'
body+='</div><p><a class="guide-button" href="/guides/">Browse written guides →</a></p></section>'
(ROOT/'videos').mkdir(exist_ok=True)
(ROOT/'videos/index.html').write_text(page('/videos/','Video tutorials', 'Our published app tutorials, with YouTube videos, written guides and app links.',body,ld({'@type':'CollectionPage','name':'Video tutorial library','url':HOST+'/videos/'})))

print(HOST,len(GUIDES),'guides generated')
