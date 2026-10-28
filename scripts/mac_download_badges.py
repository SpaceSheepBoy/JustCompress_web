"""Apply verified Mac download links to every maintained app directory locale."""
from pathlib import Path
import json
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]

def apply():
    data=json.loads((ROOT/'scripts/mac-downloads.json').read_text())
    pages=[ROOT/'apps/index.html',*(ROOT/'apps').glob('*/index.html')]
    changed=[]
    for page in pages:
        soup=BeautifulSoup(page.read_text(),'html.parser')
        if not soup.select('.app-catalog'): continue
        for card in soup.select('.app-card'):
            store=card.select_one('a[href*="apps.apple.com"]')
            if not store: continue
            app=next((a for a in data['apps'] if '/id'+a['id'] in store['href']),None)
            if not app: continue
            for old in card.select('.mac-download-badge'): old.decompose()
            link=soup.new_tag('a',href=app['url'])
            link['class']='mac-download-badge catalog-store-badge'
            link['aria-label']='macOS: '+card.h2.get_text(' ',strip=True)
            link['title']=app['requirement']
            artwork=json.loads((ROOT/'locales/mac-badge-sources.json').read_text())[soup.html.get('lang','en')]
            img=soup.new_tag('img',src=artwork['src'],alt='Download on the Mac App Store',width=str(artwork['width']),height=str(artwork['height']))
            img['style']='width:auto;height:50px'
            link.append(img)
            actions=card.select_one('.actions')
            copy=actions.select_one('button')
            if copy: copy.insert_before(link)
            else: actions.append(link)
        page.write_text(str(soup))
        changed.append(str(page.relative_to(ROOT)))
    return changed

if __name__=='__main__': print('Mac badges:', ', '.join(apply()))
