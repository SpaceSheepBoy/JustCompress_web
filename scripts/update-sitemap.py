"""Refresh the sitemap for the audited portfolio pass, excluding noindex routes."""
from pathlib import Path
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import subprocess
from datetime import date
ROOT=Path(__file__).resolve().parents[1];NS='http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('',NS);file=ROOT/'sitemap.xml';tree=ET.parse(file);root=tree.getroot()
old={n.find('{'+NS+'}loc').text:n.findtext('{'+NS+'}lastmod') for n in root}
changed=set(subprocess.check_output(['git','diff','HEAD','--name-only'],cwd=ROOT,text=True).splitlines())
changed.update(subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines())
root.clear()
for p in sorted(ROOT.rglob('index.html')):
 rel=p.relative_to(ROOT)
 if any(x.startswith('.') or x in ('scripts','vendor','node_modules') for x in rel.parts):continue
 s=BeautifulSoup(p.read_text(),'html.parser')
 if s.select_one('meta[name="robots"][content*="noindex"]') or s.select_one('[data-site-redirect]'):continue
 route='/' if len(rel.parts)==1 else '/'+str(rel.parent)+'/'
 url='https://justcompress.online'+route
 n=ET.SubElement(root,'{'+NS+'}url');ET.SubElement(n,'{'+NS+'}loc').text=url
 modified=date.today().isoformat() if str(rel) in changed or url not in old else old[url]
 if modified:ET.SubElement(n,'{'+NS+'}lastmod').text=modified
ET.indent(tree,space='  ');tree.write(file,encoding='utf-8',xml_declaration=True)
print('Sitemap:',len(root),'indexable routes')
