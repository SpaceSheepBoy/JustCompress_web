from pathlib import Path
import json,re,html
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'scripts/policies/phone-cleaner.json').read_text())
for kind in ['privacy','terms','support']:
 p=root/'apps/vidkit'/kind/'index.html'
 s=p.read_text().replace(html.escape(d['previous_name']),html.escape(d['name'])).replace(d['previous_name'],html.escape(d['name']))
 s=s.replace('May 14, 2026',d['effective'])
 s=s.replace('Photo library or file picker access is limited to media you select.', 'Photo library access covers the library or selected items you authorize; file picker access covers files you choose. Local Network permission enables optional direct pairing.')
 s=re.sub(r'<section id="paired-cleanup-disclosure">.*?</section>', '', s, flags=re.S)
 block=d['disclosure']
 if kind in ['terms','privacy']:block+='<section id="pro-plan-disclosure"><h2>Pro access and billing</h2><p>'+d['purchases']+'</p></section>'
 s=re.sub(r'<section id="pro-plan-disclosure">.*?</section>', '', s, flags=re.S)
 s=s.replace('</main>',block+'\n</main>')
 assert ('jiali' + ' liang') not in s.lower()
 p.write_text(s)
print('Updated three maintained policy pages; portfolio listing preserved')
