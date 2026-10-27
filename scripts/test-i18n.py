"""Audit generated locale pages and their actual local link/asset graph."""
from collections import Counter
import json
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from PIL import Image
import i18n_pages as build

ROOT = Path(__file__).resolve().parents[1]
apps = json.loads((ROOT/'scripts/app-portfolio.json').read_text())['apps']
stores = build.load('store-snapshots.json')
source = build.load('en.json')
review = build.load('review.json')
assert review['source_sha256'] == build.digest(source)
assert all(v['approved'] == v['total'] and not v['failing_check_ids'] for v in review['languages'].values())
sitemap = ET.parse(ROOT/'sitemap.xml')
listed = {x.text for x in sitemap.getroot().iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
checked = []
for lang in build.TARGETS:
    catalog = build.load(lang+'.json')
    assert set(catalog) == set(source)
    assert review['catalogs'][lang] == build.digest(catalog)
    for key, text in source.items():
        if key.startswith('apps.'):
            # Preserve explicit numeric facts and technical format numbers.
            expected = Counter(re.findall(r'\d+',text))
            actual = Counter(re.findall(r'\d+',catalog[key]))
            assert not expected-actual, (lang,key,'lost numeric fact')
    for slug in ['',*[a['slug'] for a in apps]]:
        route = build.route(slug,lang)
        raw = (ROOT/route.strip('/')/'index.html').read_text()
        assert not re.search(r'jiali\s+liang',raw,re.I), route
        assert not re.search('[—–]',raw), route
        soup = BeautifulSoup(raw,'html.parser')
        assert soup.html['lang'] == lang
        assert len(soup.select('h1')) == 1
        assert len(soup.select('link[rel=canonical]')) == 1
        assert soup.select_one('link[rel=canonical]')['href'] == build.SITE+route
        assert build.SITE+route in listed
        assert soup.select_one('script[src^="/assets/i18n-ui.js"]')
        assert soup.select_one('script[src^="/assets/posthog-init.js"]')
        badges=soup.select('a.localized-store-badge img.official-app-store-badge')
        assert len(badges)==(1 if slug else len(apps)), (route,'missing official download badge')
        artwork=build.load('badge-sources.json')[lang]
        for badge in badges:
            assert badge['src']==artwork['src'], (route,'wrong language badge')
            assert badge.parent['href'].startswith('https://apps.apple.com/')
        assert len(soup.select('details.i18n-selector'))==1
        for node in soup.select('script[type="application/ld+json"]'):
            json.loads(node.string)
        for node in soup.select('a[href],img[src],script[src],link[href]'):
            url=node.get('href',node.get('src',''))
            parts=urlsplit(url)
            if parts.scheme or parts.netloc or not parts.path.startswith('/'):
                continue
            local=ROOT/unquote(parts.path).lstrip('/')
            if local.is_dir():local=local/'index.html'
            assert local.exists(),(route,url,'broken internal destination')
        for node in soup.select('img'):
            assert 'alt' in node.attrs
        if slug:
            store=stores[slug][lang]
            if lang=='zh-Hans':
                assert store['country']=='sg' and '/sg/' in store['trackViewUrl']
                assert soup.select_one('.storefront-note') and '新加坡' in soup.select_one('.storefront-note').get_text()
            assert soup.h1.get_text() == store['trackName']
            assert len(soup.select(f'a[href="{store["trackViewUrl"]}"]')) >= 2
            for screen in store['screens']:
                im=Image.open(ROOT/screen['src'].lstrip('/'))
                assert im.size == (screen['width'],screen['height'])
                assert im.width >= 1000 and im.height >= 2000
        checked.append(route)
for locale,artwork in build.load('badge-sources.json').items():
    assert build.hashlib.sha256((ROOT/artwork['src'].lstrip('/')).read_bytes()).hexdigest()==artwork['sha256'],(locale,'official Apple SVG was modified')
# Every alternate in every affected cluster must return the identical reciprocal set.
for slug in ['',*[a['slug'] for a in apps]]:
    expected={k:build.SITE+v for k,v in build.alternatives(slug).items()}
    for code,route in build.alternatives(slug).items():
        soup=BeautifulSoup((ROOT/route.strip('/')/'index.html').read_text(),'html.parser')
        nodes=soup.select('link[rel=alternate][hreflang]')
        actual={n['hreflang']:n['href'] for n in nodes}
        assert len(nodes)==len(actual), (route,'duplicate hreflang')
        assert actual == expected, (route,'missing reciprocal language version')
# A future source edit or unreviewed translation must stop the actual compiler
# before any HTML is emitted. Exercise both failures in an isolated fixture.
with tempfile.TemporaryDirectory() as directory:
    fixture = Path(directory)
    shutil.copytree(ROOT/'locales',fixture/'locales')
    (fixture/'scripts').mkdir()
    for name in ('app-portfolio.json','app-display-order.json'):
        shutil.copy(ROOT/'scripts'/name,fixture/'scripts'/name)
    original_root = build.ROOT
    try:
        build.ROOT = fixture
        changed = build.load('fr.json')
        changed['common.store'] = 'Unreviewed change'
        (fixture/'locales/fr.json').write_text(json.dumps(changed))
        try:
            build.build()
            raise AssertionError('Unreviewed translation was accepted')
        except ValueError as error:
            assert 'reviewed Weblate export' in str(error)
        changed = json.loads((fixture/'scripts/app-portfolio.json').read_text())
        changed['apps'][0]['access'] = 'Changed purchase rules'
        (fixture/'scripts/app-portfolio.json').write_text(json.dumps(changed))
        try:
            build.build()
            raise AssertionError('Changed source facts were accepted')
        except ValueError as error:
            assert 'English product facts changed' in str(error)
        assert not (fixture/'apps').exists()
    finally:
        build.ROOT = original_root
print('PASS:',len(checked),'localized pages; approved catalogs, numbers, native screenshots, metadata, internal destinations, sitemap and reciprocal hreflang')
print('PASS: source drift and unreviewed translations block generation before HTML writes')
