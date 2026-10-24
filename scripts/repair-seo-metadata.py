"""Preserve metadata on the existing product and legal pages after regeneration."""
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
DESCRIPTIONS={
 'apps/photofix/privacy/':'PhotoFix privacy information from Space Sheep Studio. Read about on-device processing, purchases and support data.',
 'apps/photofix/support/':'Get help with PhotoFix from Space Sheep Studio. Find support contact information and describe a photo conversion issue.',
 'apps/audiofix/':'Audio Fix is an App in development for on-device audio channel repair, normalization and conversion. Read its current product, privacy and support information.',
 'apps/audiofix/privacy/':'Read how Audio Fix handles selected media, local working files, purchases and information you choose to send for support.',
 'apps/audiofix/support/':'Audio Fix support: channel routing, normalization, conversion, export limits, saving and purchases. Contact Space Sheep Studio for help.',
 'apps/audiofix/terms/':'Audio Fix terms of use, Apple EULA, export allowance and optional purchase terms from Space Sheep Studio.'}
for route,description in DESCRIPTIONS.items():
 p=ROOT/route/'index.html'
 if not p.exists():continue
 raw=p.read_text();s=BeautifulSoup(raw,'html.parser')
 if not s.head:
  head=s.new_tag('head')
  for el in list(s.html.children):
   if getattr(el,'name',None) in ('meta','title','link','style'):head.append(el.extract())
  s.html.insert(0,head)
 if not s.body:
  body=s.new_tag('body')
  for el in list(s.html.children):
   if el is not s.head:body.append(el.extract())
  s.html.append(body)
 meta=s.find('meta',attrs={'name':'description'})
 if not meta:meta=s.new_tag('meta',attrs={'name':'description'});s.head.append(meta)
 meta['content']=description
 canonical=s.find('link',rel='canonical')
 if not canonical:canonical=s.new_tag('link',rel='canonical');s.head.append(canonical)
 canonical['href']='https://justcompress.online/'+route
 if route.startswith('apps/photofix/'):
  css=s.find('link',rel='stylesheet')
  if css:css['href']='../assets/style.css?v=20261024-seo'
 if s.title:s.title.string=s.title.get_text().replace('—',', ').replace('–',', ')
 p.write_text(str(s))
print('Verified metadata for',len(DESCRIPTIONS),'existing pages')
