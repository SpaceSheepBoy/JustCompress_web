"""Build the website portfolio from verified, public App Store snapshots.

Only this site's curated, publicly downloadable Apps appear here.
Do not list unreleased apps, even as support-only links in the catalog. After a
public release is verified, refresh its Apple snapshot and display order before
regenerating and deploying /apps/. Keep required legal/support pages available.
Native App binaries and store metadata are never edited. Existing policy bodies are maintained separately.
"""
from pathlib import Path
from html import escape as E
import json,re
from sober_product import build as build_sober_product
from product_stories import STORIES, build as build_product_story
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'scripts/app-portfolio.json').read_text())
APPS=DATA['apps'];GUIDES=json.loads((ROOT/'scripts/tutorial-guides.json').read_text())
LOCALES=json.loads((ROOT/'scripts/collage-localizations.json').read_text())
SITE='https://justcompress.online'
def clean(t):return re.sub(r'jiali\s+liang','Space Sheep Studio',str(t),flags=re.I).replace('—',', ').replace('–','-')
def ld(d):return '<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org',**d},ensure_ascii=False).replace('</','<\\/')+'</script>'
def absolute(u):return SITE+u if u.startswith('/') else u

def page(route,title,description,body,schema='',lang='en',alternates=None):
 url=SITE+route
 alternate=''.join(f'<link rel="alternate" hreflang="{E(code)}" href="{SITE}{path}">' for code,path in (alternates or {}).items())
 html=f'''<!doctype html><html lang="{E(lang)}" dir="{'rtl' if lang=='ar' else 'ltr'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} | Just Compress</title><meta name="description" content="{E(description)}"><link rel="canonical" href="{url}">{alternate}<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{url}"><meta property="og:type" content="website"><link rel="icon" href="/assets/icons/just-compress-icon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/portfolio-v2.css?v={'20261026-card-links' if route=='/apps/' else '20261024'}">{schema}</head><body class="portfolio-page"><div class="portfolio-shell"><nav class="portfolio-nav" aria-label="Main navigation"><a class="portfolio-brand" href="/">Just Compress</a><div><a href="/apps/">Apps</a><a href="/guides/">Guides</a><a href="/tools/">Free tools</a><a href="/support/">Support</a></div></nav><main>{body}</main><footer class="portfolio-footer"><span>© 2026 Space Sheep Studio</span><a href="/apps/">Apps</a><a href="/privacy/">Website privacy</a><a href="/terms/">Website terms</a><a href="/legal/">App policies</a></footer></div></body></html>'''
 p=ROOT/route.strip('/')/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(clean(html))
def image(m,alt,klass='',lazy=True):
 return f'<img class="{klass}" src="{m["src"]}" width="{m["width"]}" height="{m["height"]}" alt="{E(alt)}"'+(' loading="lazy"' if lazy else '')+'>'
def screenshots(items,name):
 return '<figure class="store-figure"><div class="store-shots" tabindex="0" aria-label="App Store screenshots">'+''.join(image(s,name+' official App Store screenshot '+str(i)) for i,s in enumerate(items,1))+'</div><figcaption>Official App Store screenshots. Swipe or scroll to inspect each image.</figcaption></figure>'
def policy_links(a):
 links=[]
 for part,label in [('privacy','Privacy'),('terms','Terms'),('support','Support')]:
  p=ROOT/'apps'/a['slug']/part/'index.html'
  if p.exists():links.append((f'/apps/{a["slug"]}/{part}/',label))
 if not any(label=='Privacy' for u,label in links) and a.get('privacy'):links.append((a['privacy'],'Privacy'))
 if not any(label=='Terms' for u,label in links):links.append(('https://www.apple.com/legal/internet-services/itunes/dev/stdeula/','Apple EULA'))
 if not any(label=='Support' for u,label in links):links.append(('mailto:abel0911@icloud.com?subject='+a['slug'],'Email support'))
 return ' · '.join(f'<a href="{E(u)}">{E(label)}</a>' for u,label in links)
def breadcrumbs(a,route):return ld({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Just Compress','item':SITE+'/'},{'@type':'ListItem','position':2,'name':'Apps','item':SITE+'/apps/'},{'@type':'ListItem','position':3,'name':a['name'],'item':SITE+route}]})
alternates={'en':'/apps/collage-maker/',**{k:'/apps/collage-maker/'+k+'/' for k in LOCALES if k!='en'},'x-default':'/apps/collage-maker/'}
# Complete the local support route for published Apps that did not have one.
for app in APPS:
 support=ROOT/'apps'/app['slug']/'support/index.html'
 if not support.exists():
  body=f'<header class="product-heading"><h1>{E(app["name"])} support</h1><p>For help, email <a href="mailto:abel0911@icloud.com?subject={app["slug"]}">abel0911@icloud.com</a>. Include your app version, iPhone model and a short description of the problem. Do not send private photos or personal records for general troubleshooting.</p></header><section class="product-section"><h2>Current published version</h2><p>Version {E(app["version"])} was checked in the US App Store on {DATA["checked"]}. <a href="/apps/{app["slug"]}/">Review the current features and screenshots</a>.</p><h2>Access and purchases</h2><p>{E(app["access"])}</p><p>For a purchase problem, use the available restore option with the Apple Account used for the purchase. Apple handles billing and refunds.</p><h2>Before you retry</h2><p>Keep your original files and records. Describe the last completed step, any error message, and whether the issue involves importing, using a feature, saving, sharing or purchasing.</p></section>'
  page('/apps/'+app['slug']+'/support/',app['name']+' support','Support for '+app['name']+'. Current version information, access details and developer contact.',body)
for a in APPS:
 route='/apps/'+a['slug']+'/'
 if a['id']=='6811067941':
  build_sober_product(ROOT,a)
  continue
 if a['id'] in STORIES:
  build_product_story(ROOT,a)
  continue
 locales='<nav class="product-languages" aria-label="Product language">'+''.join(f'<a href="{alternates[k]}" lang="{k}">{E(v["label"])}</a>' for k,v in LOCALES.items())+'</nav>' if a['slug']=='collage-maker' else ''
 body=f'<header class="product-heading"><div class="product-identity">{image(a["icon"],a["name"]+" icon","product-icon",False)}<div><p class="eyebrow">IPHONE APP</p><h1>{E(a["name"])}</h1></div></div><p class="product-lede">{E(a["benefit"])}</p><p class="product-version">US App Store version {E(a["version"])} · iOS {E(a["minimum_os"])} or later · Checked {DATA["checked"]}</p><a class="portfolio-button" href="{E(a["store_url"])}">View on the App Store ↗</a></header>{locales}'
 body+=screenshots(a['screenshots'],a['name'])
 body+='<section class="product-section"><h2>What you can do</h2><ul class="feature-list">'+''.join('<li>'+E(f)+'</li>' for f in a['features'])+'</ul></section>'
 body+=f'<section class="product-section"><h2>Access and purchases</h2><p>{E(a["access"])}</p><p>Prices and availability can differ by storefront. Apple shows the current local offer before purchase.</p></section><section class="product-section"><h2>Before you export or share</h2><p>{E(a["caveat"])}</p></section>'
 if a.get('release_notes'):body+=f'<section class="product-section"><h2>Latest published update</h2><p class="product-version">Version {E(a["version"])} · released {E(a["release_date"])}</p><p>{E(a["release_notes"]).replace(chr(10),"<br>")}</p></section>'
 related={
  '6769563659':[('/compress-audio-file-iphone/','How to compress an audio file on iPhone')],
  '6769563339':[('/compress-video-for-whatsapp/','Video too big for WhatsApp: choose how to send it')],
  '6769762323':[('/sign-merge-compress-pdf-iphone-no-upload/','Sign, merge and compress a PDF on iPhone')]
 }.get(a['id'],[])+[(f'/guides/{g["slug"]}/',g['title']) for g in GUIDES if g['app']==a['id']]
 for p in sorted((ROOT/'iphone-video-tutorials').glob('*/index.html')):
  name=p.parent.name
  match=('audio' in name or 'm4a' in name) if a['id']=='6769563659' else ('watermark' in name) if a['id']=='6769761016' else ('pdf' in name and 'watermark' not in name) if a['id']=='6769762323' else False
  if match:related.append(('/iphone-video-tutorials/'+name+'/',name.split('-',1)[1].replace('-',' ').capitalize()))
 if a['slug']=='just-captions':related.append(('https://justcaptions.com/guides/','Just Captions guides for iPhone and Mac'))
 if related:body+='<section class="product-section"><h2>Practical guides</h2><ul>'+''.join(f'<li><a href="{u}">{E(t)}</a></li>' for u,t in related)+'</ul></section>'
 body+=f'<aside class="product-download"><h2>{E(a["name"])}</h2><p>{E(a["benefit"])}. Review the current store listing for full details and compatibility.</p><a class="portfolio-button" href="{E(a["store_url"])}">Get the iPhone app ↗</a><p class="product-links">{policy_links(a)}</p></aside>'
 schema=ld({'@type':'SoftwareApplication','name':a['name'],'url':SITE+route,'downloadUrl':a['store_url'],'softwareVersion':a['version'],'operatingSystem':'iOS '+a['minimum_os']+' or later','applicationCategory':'UtilitiesApplication','description':a['benefit'],'image':absolute(a['icon']['src']),'screenshot':[absolute(s['src']) for s in a['screenshots']],'publisher':{'@type':'Organization','name':'Space Sheep Studio'}})+breadcrumbs(a,route)
 page(route,a['name']+' for iPhone',a['benefit']+'. Current features, App Store screenshots, version details and access options.',body,schema,alternates=alternates if a['slug']=='collage-maker' else None)
# Separate stable URLs replace a single document containing twelve language versions.
labels={
 'zh-Hans':('功能与使用','App Store 截图','在 App Store 查看','隐私','条款'), 'zh-Hant':('功能與使用','App Store 截圖','在 App Store 查看','隱私','條款'),
 'fr':('Fonctions et utilisation',"Captures de l’App Store","Voir sur l’App Store",'Confidentialité','Conditions'),
 'de':('Funktionen und Nutzung','App Store Screenshots','Im App Store ansehen','Datenschutz','Nutzungsbedingungen'),
 'es':('Funciones y uso','Capturas del App Store','Ver en el App Store','Privacidad','Condiciones'),
 'pt':('Recursos e uso','Capturas da App Store','Ver na App Store','Privacidade','Termos'),
 'ja':('機能と使い方','App Storeのスクリーンショット','App Storeで見る','プライバシー','利用規約'),
 'ko':('기능 및 사용 방법','App Store 스크린샷','App Store에서 보기','개인정보 보호','이용 약관'),
 'ar':('الميزات والاستخدام','لقطات شاشة App Store','عرض في App Store','الخصوصية','الشروط'),
 'id':('Fitur dan penggunaan','Tangkapan layar App Store','Lihat di App Store','Privasi','Ketentuan'),
 'th':('คุณสมบัติและการใช้งาน','ภาพหน้าจอ App Store','ดูใน App Store','ความเป็นส่วนตัว','ข้อกำหนด')}
for lang,l in LOCALES.items():
 if lang=='en':continue
 title,shotlabel,storelabel,privacylabel,termslabel=labels[lang]
 policy_locale={'fr':'fr-FR','de':'de-DE','es':'es-MX','pt':'pt-BR','ar':'ar-SA'}.get(lang,lang)
 parts=[p for p in l['description'].split('\n\n') if not re.match(r'(?i)^(terms|privacy|conditions|confidentialit|datenschutz|nutzungsbedingungen|privacidad|términos|privacidade|termos|利用規約|プライバシー|개인정보|이용 약관|隱私|隐私|条款|條款|الخصوصية|الشروط|privasi|ketentuan|ความเป็นส่วนตัว|ข้อกำหนด)',p)]
 body=f'<header class="product-heading"><h1>{E(l["name"])}</h1><p class="product-version">App Store · {E(l["country"].upper())} · {E(l["version"])}</p><a class="portfolio-button" href="{E(l["url"])}">{storelabel} ↗</a></header><nav class="product-languages" aria-label="Language">'+''.join(f'<a href="{alternates[k]}" lang="{k}">{E(v["label"])}</a>' for k,v in LOCALES.items())+'</nav>'
 body+=f'<section class="product-section"><h2>{title}</h2>'+''.join('<p>'+E(p).replace('\n','<br>')+'</p>' for p in parts)+'</section>'
 body+=f'<section><h2>{shotlabel}</h2>'+screenshots(l['screenshots'],l['name'])+'</section>'
 body+=f'<p><a href="/apps/collage-maker/privacy/?lang={policy_locale}">{privacylabel}</a> · <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">{termslabel}</a></p>'
 route='/apps/collage-maker/'+lang+'/'
 schema=ld({'@type':'SoftwareApplication','name':l['name'],'url':SITE+route,'downloadUrl':l['url'],'softwareVersion':l['version'],'operatingSystem':'iOS 17 or later','inLanguage':lang,'description':parts[0]})
 page(route,l['name'],parts[0][:170],body,schema,lang,alternates)
# The existing copy-name and search controls remain available with current full store names.
display_order=json.loads((ROOT/'scripts/app-display-order.json').read_text())['app_ids']
assert len(display_order)==len(set(display_order)) and set(display_order)=={a['id'] for a in APPS},'Display order must match the curated released portfolio'
ordered=sorted(APPS,key=lambda a:display_order.index(a['id']))
cards=[]
for a in ordered:
 gallery='<figure class="catalog-gallery"><div class="catalog-shots" aria-label="'+E(a["name"])+' App Store screenshots">'+''.join('<a href="'+E(a['store_url'])+'" aria-label="View '+E(a['name'])+' on the App Store, screenshot '+str(i)+'">'+image(shot,a["name"]+" official App Store screenshot "+str(i),"catalog-shot")+'</a>' for i,shot in enumerate(a["screenshots"][:3],1))+'</div></figure>'
 cards.append(f'<article class="app-card" id="{a["slug"]}" data-app="{a["id"]}"><a class="catalog-identity" href="/apps/{a["slug"]}/" aria-label="About {E(a["name"])}">{image(a["icon"],"","app-icon")}<div><h2>{E(a["name"])}</h2><p class="benefit">{E(a["benefit"])}</p></div></a>{gallery}<input id="name-{a["id"]}" type="hidden" value="{E(a["name"])}"><div class="actions"><a class="catalog-store-badge" data-store href="{E(a["store_url"])}" aria-label="Download {E(a["name"])} on the App Store"><img src="/assets/brand/download-on-the-app-store.svg" width="150" height="50" alt="Download on the App Store"></a><button type="button" data-copy="name-{a["id"]}" aria-label="Copy app name: {E(a["name"])}">Copy name</button></div><p><a href="/apps/{a["slug"]}/">App details and guides →</a></p></article>')
body='<header class="catalog-heading"><h1>Find the app you saw.</h1><input id="find-app" type="search" aria-label="Search by app or task" placeholder="Search apps…" autocomplete="off"></header><p id="status" role="status" aria-live="polite"></p><section class="catalog-grid app-catalog" aria-label="Available iPhone apps">'+''.join(cards)+'</section><p id="no-results" hidden>No matching app. Try “video”, “audio”, “photo” or “PDF”.</p><script defer src="/assets/find-app.js?v=20261024-portfolio"></script>'
schema=ld({'@type':'CollectionPage','name':'Our iPhone apps','url':SITE+'/apps/','mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':a['name'],'url':SITE+'/apps/'+a['slug']+'/'} for i,a in enumerate(ordered)]}})
page('/apps/','iPhone apps, current screenshots and practical guides','Find the app from our tutorials. Browse current App Store names, screenshots, published versions and practical guides from Space Sheep Studio.',body,schema)
# Support destinations remain local when a maintained local support page exists.
support_cards=''.join(f'<a class="support-card" href="/apps/{a["slug"]}/support/">{image(a["icon"],"","app-icon")}<span>{E(a["name"])}</span></a>' for a in ordered if (ROOT/'apps'/a['slug']/'support/index.html').exists())
body='<header class="product-heading"><h1>How can we help?</h1><p>Choose your App or email <a href="mailto:abel0911@icloud.com">abel0911@icloud.com</a>. Include the published app version, device and a short description. You do not need to send private media for general help.</p></header><section class="catalog-grid" aria-label="App support">'+support_cards+'</section><section class="product-section"><h2>Other product support</h2><p>Support information for additional or earlier products remains in the <a href="/legal/">App policy directory</a>.</p></section>'
page('/support/','App support','Find help for our published iPhone Apps, current product information and support contact details.',body)
rows=[]
for folder in sorted((ROOT/'apps').iterdir()):
 if not folder.is_dir():continue
 if folder.name=='brew-day':continue
 policy=[(part,label) for part,label in [('privacy','Privacy'),('terms','Terms'),('support','Support')] if (folder/part/'index.html').exists()]
 if not policy:continue
 a=next((a for a in APPS if a['slug']==folder.name),None)
 name=a['name'] if a else {'audiofix':'Audio Fix','camrecorder':'CamRecorder','dpi':'DPI Changer','livephoto':'Live Photo to Video','talknice':'TalkNice','retrophone':'RetroPhone'}.get(folder.name,folder.name)
 row='<li><strong>'+E(name)+'</strong><div>'+''.join(f'<a href="/apps/{folder.name}/{part}/">{label}</a> ' for part,label in policy)+'</div></li>'
 rows.append(row)
body='<header class="product-heading"><h1>Privacy, terms and App support</h1><p>Find the document for the App you use. Retained support information does not establish current App Store availability.</p></header><section><h2>Website</h2><p><a href="/privacy/">Website privacy</a> · <a href="/terms/">Website terms</a> · <a href="/support/">Contact support</a></p><h2>App documents</h2><ul class="policy-directory">'+''.join(rows)+'</ul></section>'
page('/legal/','Privacy, terms and App support','Find maintained privacy policies, terms and support information for Space Sheep Studio Apps and Just Compress browser tools.',body)
print('Built',len(APPS),'verified product pages, 11 localized product URLs and the App directory')
