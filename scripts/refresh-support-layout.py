from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
r=Path(__file__).resolve().parents[1]
nav='<nav class="legacy-nav" aria-label="Main navigation"><a class="legacy-brand" href="/">Just Compress<span>●</span></a><div><a href="/tools/">Tools</a><a href="/apps/">iPhone apps</a><a href="/support/">Support</a></div></nav>'
footer='<footer class="legacy-footer"><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a><a href="/legal/">App policies</a><a href="mailto:abel0911@icloud.com">Contact</a></footer>'
# Shared legacy frame; policy and troubleshooting body text is preserved.
changed=[]
for p in r.rglob('index.html'):
 if p.parent.name not in ['privacy','terms','support','legal']:continue
 s=BeautifulSoup(p.read_text(),'html.parser')
 if not s.select_one('link[href^="/assets/app.css"]'):continue
 old=s.select_one('nav.nav')
 if old:old.replace_with(BeautifulSoup(nav,'html.parser'))
 old=s.select_one('footer.site-foot')
 if old:old.replace_with(BeautifulSoup(footer,'html.parser'))
 
 if not s.select_one('link[href^="/assets/legacy.css"]'):s.head.append(s.new_tag('link',rel='stylesheet',href='/assets/legacy.css?v=20261002'))
 s.body['class']=list(dict.fromkeys(s.body.get('class',[])+['legacy-page']))
 for el in s.select('.article-row p'):el.decompose()
 p.write_text(str(s));changed.append(str(p))
# Use actual catalog names and icons, and existing app-specific support destinations.
catalog=BeautifulSoup((r/'apps/index.html').read_text(),'html.parser');cards=[]
for card in catalog.select('.app-card'):
 slug=card['id'];name=card.h2.get_text();icon=card.select_one('.app-icon')['src'];target=f'/apps/{slug}/support/'
 if not (r/target.strip('/')/'index.html').exists():
  target='mailto:abel0911@icloud.com?subject='+__import__('urllib.parse',fromlist=['quote']).quote(name+' support')
 cards.append(f'<a class="help-app" href="{escape(target,quote=True)}"><img src="{escape(icon,quote=True)}" alt="" width="44" height="44" loading="lazy"><span>{escape(name)}</span><b aria-hidden="true">↗</b></a>')
p=r/'support/index.html';s=BeautifulSoup(p.read_text(),'html.parser');s.body.clear();s.body.append(BeautifulSoup(nav+'''<header class="help-header"><h1>How can we help?</h1><a class="contact-button" href="mailto:abel0911@icloud.com">✉️ Email support</a><p>Include the app name, device and a short description.</p></header><main class="help-main"><section class="help-checks" aria-label="Quick help"><details><summary>📁 Export failed?</summary><p>Keep your original. Try a smaller file and check available storage.</p></details><details><summary>☁️ File in iCloud?</summary><p>Download the original in Photos or Files, then try again.</p></details><details><summary>🛍️ Purchase help?</summary><p>Use Restore Purchases in the app with the Apple Account used to buy it. For billing help, <a href="https://support.apple.com/billing">visit Apple Support ↗</a>.</p></details></section><h2>Choose your app</h2><section class="help-apps">'''+''.join(cards)+'''</section><details class="older-help"><summary>Other apps</summary><a href="/apps/photofix/support/">PhotoFix ↗</a><a href="/apps/retrophone/support/">RetroPhone ↗</a></details></main>'''+footer,'html.parser'));p.write_text(str(s))
# Make the policy directory complete by listing every existing app policy folder.
p=r/'legal/index.html';s=BeautifulSoup(p.read_text(),'html.parser');main=s.find('main');main.clear();main['class']='help-main'
html='<section class="help-apps"><a class="help-app" href="/privacy/">🔒 Website privacy</a><a class="help-app" href="/terms/">📄 Website terms</a><a class="help-app" href="/support/">✉️ Support</a></section><h2>App policies</h2><div class="policy-list">'
for folder in sorted((r/'apps').iterdir()):
 if not folder.is_dir() or not (folder/'privacy/index.html').exists():continue
 app=catalog.find(id=folder.name);name=app.h2.get_text() if app else {'photofix':'PhotoFix','retrophone':'RetroPhone','dying-soon':'Dying Soon'}.get(folder.name,folder.name.replace('-',' ').title())
 links=[]
 for part,label in [('privacy','Privacy'),('terms','Terms'),('support','Support')]:
  if (folder/part/'index.html').exists():links.append(f'<a href="/apps/{folder.name}/{part}/">{label}</a>')
 html+=f'<div><b>{escape(name)}</b><span>'+''.join(links)+'</span></div>'
html+='</div>';main.append(BeautifulSoup(html,'html.parser'));s.h1.clear();s.h1.string='Privacy & terms';s.select_one('.lede').string='Find the policy for your app.';p.write_text(str(s))
(r/'assets/legacy.css').write_text('''body.legacy-page{background:#faf9f6;color:#292532;font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.legacy-page:before,.legacy-page:after,.legacy-page .topline{display:none}.legacy-page .rise{opacity:1;animation:none;transform:none}.legacy-page .shell,.legacy-page .measure{max-width:980px;width:calc(100% - 40px);margin:auto}.legacy-nav{max-width:980px;margin:auto;display:flex;align-items:center;justify-content:space-between;gap:20px;padding:28px 0}.legacy-nav a{text-decoration:none;color:inherit}.legacy-brand{font-weight:800;font-size:22px;letter-spacing:-.8px}.legacy-brand span{color:#9684d9;font-size:12px;margin-left:4px}.legacy-nav div{display:flex;gap:22px;font-size:13px}.legacy-page>.legacy-nav{width:calc(100% - 40px)}.legacy-page .hero{padding:28px 0 20px}.legacy-page h1{font:750 clamp(30px,4vw,44px)/1.15 system-ui;letter-spacing:-1.2px;margin:16px 0}.legacy-page .lede{font:15px/1.5 system-ui;color:#7b7185;max-width:650px}.legacy-page .kicker{font:650 11px system-ui;letter-spacing:1px;background:none;border:0;color:#8a7b98}.legacy-page .prose{max-width:760px}.legacy-page .prose h2{font:700 21px/1.3 system-ui;letter-spacing:-.3px;margin:28px 0 12px}.legacy-page .prose p,.legacy-page .prose li{font:15px/1.7 system-ui}.legacy-page .tldr{background:#eee8f4;border:0;border-radius:14px;padding:20px}.legacy-footer{max-width:980px;width:calc(100% - 40px);margin:40px auto 0;border-top:1px solid #e3dfe7;display:flex;gap:24px;padding:24px 0;font:12px system-ui}.legacy-footer a{color:#7f748a;text-decoration:none}.help-header,.help-main{max-width:980px;width:calc(100% - 40px);margin:auto}.help-header{padding:24px 0}.help-header p{font-size:13px;color:#83788c}.contact-button{display:inline-block;background:#302638;color:white!important;text-decoration:none;padding:13px 20px;border-radius:12px;font-weight:650}.help-checks{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:0 0 30px;align-items:start}.help-checks details{padding:18px;background:#eee9f4;border-radius:16px;font-size:13px}.help-checks summary{cursor:pointer;font-weight:650}.help-checks p{margin:12px 0 0}.help-main>h2{font-size:20px;margin:24px 0 16px}.help-apps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.help-app{display:flex;align-items:center;gap:12px;padding:18px;background:white;border:1px solid #e5dfe9;border-radius:16px;text-decoration:none;color:inherit;font-size:13px;min-height:86px}.help-app img{border-radius:11px;flex-shrink:0}.help-app span{flex:1;font-weight:600;line-height:1.4}.help-app b{color:#9e91a9}.older-help{margin:24px 0;font-size:13px}.older-help summary{cursor:pointer}.older-help a{display:inline-block;margin:12px 20px 0 0}.policy-list>div{padding:18px 0;border-bottom:1px solid #e5dfe9;display:flex;justify-content:space-between;gap:18px;font-size:14px}.policy-list span{display:flex;gap:18px}.policy-list a{color:#736181}.legacy-page .article-row{padding:14px}.legacy-page .article-type{display:none}@media(max-width:680px){.help-checks,.help-apps{grid-template-columns:1fr}.help-checks{gap:8px}.help-app{min-height:72px;padding:14px}.legacy-nav{flex-wrap:wrap;gap:12px;padding:20px 0}.legacy-nav div{gap:18px}.legacy-brand{font-size:20px}.policy-list>div{flex-direction:column;gap:8px}.legacy-footer{flex-wrap:wrap;gap:18px}.help-header{padding-top:8px}}''')
print('Updated legacy frames:',len(changed),'support cards:',len(cards))
