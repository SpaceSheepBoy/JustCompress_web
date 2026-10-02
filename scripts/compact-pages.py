from bs4 import BeautifulSoup
from pathlib import Path
import re,json
root=Path(__file__).resolve().parents[1]
stats=[]
for p in root.rglob('index.html'):
 rel=p.relative_to(root)
 if any(x in rel.parts for x in ['vendor','.git','privacy','terms','legal','support']):continue
 s=BeautifulSoup(p.read_text(),'html.parser')
 if not s.body or 'compact-page' in s.body.get('class',[]):continue
 before=len(s.body.get_text(' ',strip=True).split())
 # Remove repeated sales blocks, preserving the working tool and its controls.
 for el in s.select('.band, .tool-under, .quick-note'):el.decompose()
 for el in s.select('.sec-head p, .foot-brand p, .visual-caption span'):el.decompose()
 # Shorten descriptions on navigation cards, keeping their titles and links.
 for el in s.select('.blog-grid p,.article-index p,.mini-tools p,.guide-grid p'):el.decompose()
 for el in s.select('.lede'):
  if 'seo-visual' in s.body.get('class',[]):el.string='🔒 On your device · No upload' if s.select_one('#tool') else 'A quick guide. See the app in action.'
 # Condense guides to their original introduction and first concrete steps.
 for article in s.select('article.prose'):
  intro=article.find('p',recursive=False)
  steps=article.find(['ol','ul'])
  keep=[]
  if intro:
   text=intro.get_text(' ',strip=True)
   sentence=re.split(r'(?<=[.!?])\s+',text)[0]
   if len(sentence.split())<=55: keep.append('<p>'+sentence+'</p>')
  if steps:
   lis=steps.find_all('li',recursive=False)[:3]
   keep.append('<ol>'+''.join('<li>'+re.split(r'(?<=[.!?])\s+',li.get_text(' ',strip=True))[0]+'</li>' for li in lis)+'</ol>')
  # Keep unique comparison tables when present, folded with the guide.
  table=article.find('table')
  if table:keep.append(str(table))
  if keep:
   article.clear()
   article.append(BeautifulSoup(''.join(keep),'html.parser'))
 # Keep answers available with one collapsed entrance rather than a wall of questions.
 for faq in s.select('.faq'):
  if faq.find_parent('details'):continue
  wrapper=s.new_tag('details',attrs={'class':'compact-details'})
  summary=s.new_tag('summary');summary.string='❓ Quick answers';wrapper.append(summary)
  faq.wrap(wrapper)
 # Product-page long explanations become optional. Keep price/limits intact inside.
 if rel.parts[0]=='apps' and len(rel.parts)>=3 and s.select_one('.product-visual'):
  main=s.find('main') or s.body
  extra=s.new_tag('details',attrs={'class':'compact-details'})
  summary=s.new_tag('summary');summary.string='ℹ️ Features, pricing & compatibility';extra.append(summary)
  candidates=[e for e in main.find_all(recursive=False) if e.name in ['p','h2','div'] and not e.find('a') and len(e.get_text(' ',strip=True).split())>4]
  for e in candidates:extra.append(e.extract())
  if len(candidates):main.append(extra)
 # Compact shared footer without losing legal navigation.
 for foot in s.select('footer.site-foot'):
  foot.clear();foot.append(BeautifulSoup('<div class="compact-footer"><a href="/tools/">🧰 Tools</a><a href="/apps/">📱 Apps</a><a href="/tutorials/">💡 Guides</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a><a href="/support/">Support</a></div>','html.parser'))
 if s.select_one('#tool'):
  tool=s.select_one('#tool')
  strip=s.new_tag('div',attrs={'class':'compact-steps','aria-label':'Three simple steps'})
  for text in ['📂 Choose a file','⚙️ Pick settings','⬇️ Save the result']:
   item=s.new_tag('span');item.string=text;strip.append(item)
  tool.insert_before(strip)
 if not s.select_one('link[href="/assets/compact.css"]'):
  s.head.append(s.new_tag('link',rel='stylesheet',href='/assets/compact.css'))
 s.body['class']=s.body.get('class',[])+['compact-page']
 after=len(s.body.get_text(' ',strip=True).split())
 p.write_text(str(s))
 stats.append({'page':str(rel),'before':before,'after':after})
(root/'assets/compact.css').write_text('''.compact-steps{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0 20px;font:600 14px system-ui}.compact-steps span{background:#eee9f5;color:#493d56;padding:12px 18px;border-radius:14px}.compact-details{margin:22px 0;padding:18px 20px;border:1px solid #ddd5e6;border-radius:16px;background:#faf9f6;color:#302838}.compact-details>summary{cursor:pointer;font:600 15px system-ui}.compact-details .faq{margin:14px 0}.compact-footer{display:flex;flex-wrap:wrap;gap:22px;padding:24px;font:13px system-ui}.compact-page .visual-shots{height:330px}.compact-page .nav-links{flex-wrap:wrap}.compact-page .product-visual{margin-bottom:18px}@media(max-width:700px){.compact-page .visual-shots{height:260px}.compact-steps{gap:6px;font-size:12px}.compact-steps span{padding:10px}.compact-footer{gap:16px}}''')
(root/'scripts/compact-audit.json').write_text(json.dumps(stats,indent=2))
print('Pages',len(stats),'words before',sum(x['before'] for x in stats),'after',sum(x['after'] for x in stats))
