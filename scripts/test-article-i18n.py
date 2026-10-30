"""Article review gates, stable identity, complete output and repeatable builds."""
import copy
import json
import re
from pathlib import Path
import shutil
import tempfile
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import article_i18n as m

root = m.ROOT
articles = m.validate()
assert articles, 'No enrolled article tested'
for entry,page,source in articles:
    for lang in ['en']+entry['locales']:
        path = root/m.route(page,lang).strip('/')/'index.html'
        soup = BeautifulSoup(path.read_text(),'html.parser')
        assert soup.html['lang']==lang and len(soup.select('h1'))==1
        assert soup.select_one('link[rel="canonical"]')['href']==m.SITE+m.route(page,lang)
        expected = {code:m.SITE+m.route(page,code) for code in ['en']+entry['locales']}
        expected['x-default']=expected['en']
        assert {a['hreflang']:a['href'] for a in soup.select('link[rel="alternate"][hreflang]')}==expected
        assert len(soup.select('[data-article-language]'))==1
        for script in soup.select('script[type="application/ld+json"]'):
            data=json.loads(script.string)
            if lang!='en' and data.get('@type')=='Article':
                assert data['datePublished']==entry['translation_date']
                assert data['dateModified']>=data['datePublished']
            if data.get('@type')=='FAQPage':
                for q in data['mainEntity']:
                    assert q['name'] in soup.get_text() and q['acceptedAnswer']['text'] in soup.get_text()
        if lang!='en':
            target=m.load(root/'locales/articles'/entry['id']/(lang+'.json'))
            for key,value in target.items():
                if key in ('title','description','figureAlt','ui.freeTool') or key.startswith('ui.'):
                    continue
                assert value in soup.get_text() or value in str(soup),(key,'missing target unit')
            assert not soup.select('img[src$="pdf-email-checks.svg"]'),'English diagram leaked'
            assert soup.select_one('.article-workflow[aria-label]')
            badge=soup.select_one('.official-app-store-badge')
            assert badge['src']==f'/assets/brand/app-store-badges/{lang}.svg'
            for link in soup.select('a[href^="/"]'):
                url=link['href'].split('#')[0].split('?')[0]
                dest=root/url.strip('/')
                assert dest.exists() or (dest/'index.html').exists(),link['href']
        assert m.SITE+m.route(page,lang) in (root/'sitemap.xml').read_text()
        assert not re.search(r'jiali\s+liang',str(soup),re.I)
ET.fromstring((root/'sitemap.xml').read_text())

with tempfile.TemporaryDirectory() as temp:
    sandbox=Path(temp)
    for path in ['locales','assets']:
        shutil.copytree(root/path,sandbox/path)
    (sandbox/'scripts').mkdir()
    for name in ['seo-content.json','app-portfolio.json']:
        shutil.copy(root/'scripts'/name,sandbox/'scripts'/name)
    shutil.copy(root/'sitemap.xml',sandbox/'sitemap.xml')
    shutil.copytree(root/'guides',sandbox/'guides')
    for entry,page,_ in articles:
        shutil.copytree(root/page['slug'],sandbox/page['slug'],dirs_exist_ok=True)
    def snapshots():
        return {str(p.relative_to(sandbox)):p.read_bytes() for p in sandbox.rglob('*') if p.is_file()}
    m.build(sandbox)
    before=snapshots()
    m.build(sandbox)
    assert before==snapshots(),'Repeated build changes output'
    file=sandbox/'scripts/seo-content.json'
    original=m.load(file)
    changed=copy.deepcopy(original)
    target=next(p for p in changed if p.get('i18n',{}).get('id')==articles[0][0]['id'])
    target['sections'].reverse()
    file.write_text(json.dumps(changed))
    reordered=m.documents(sandbox)[0][2]
    assert reordered==articles[0][2],'Reordering changed stable translation keys'
    m.validate(sandbox)
    target['sections'][0]['body']+=' New source fact.'
    file.write_text(json.dumps(changed))
    before=snapshots()
    try:
        m.build(sandbox)
        raise AssertionError('Stale translation was accepted')
    except ValueError as error:
        assert 'source changed' in str(error)
    assert before==snapshots(),'Failed review gate wrote public output'
    file.write_text(json.dumps(original))
    folder=sandbox/'locales/articles'/articles[0][0]['id']
    lang=articles[0][0]['locales'][0]
    target_file=folder/(lang+'.json')
    saved=target_file.read_text()
    target=m.load(target_file)
    target['title']='Unreviewed replacement'
    target_file.write_text(json.dumps(target))
    try:
        m.validate(sandbox)
        raise AssertionError('Unreviewed translation was accepted')
    except ValueError:
        pass
    target_file.write_text(saved)
    record=m.load(folder/'review.json')
    record['languages'][lang]['failing_check_ids']=[123]
    (folder/'review.json').write_text(json.dumps(record))
    try:
        m.validate(sandbox)
        raise AssertionError('Failing Weblate check was accepted')
    except ValueError:
        pass
print('PASS: complete translated content, reciprocal URLs, schemas, links, stable IDs, stale/unapproved/check gates, no partial writes, idempotent generation')
