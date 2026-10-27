"""Build reviewed product-page localizations from Weblate JSON catalogs.

Run after the English generators. English URLs and other existing locales stay stable.
No remote writes; Weblate synchronization and publication are separate commands.
"""
import hashlib
from datetime import datetime
from html import escape as E
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://justcompress.online'
CONFIG = json.loads((ROOT/'locales/config.json').read_text())
LOCALES = {code:entry['label'] for code,entry in CONFIG.items()}
TARGETS = tuple(code for code in LOCALES if code != 'en')


def digest(data):
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def load(name):
    return json.loads((ROOT / 'locales' / name).read_text())


def route(slug, lang):
    base = '/apps/' + (slug + '/' if slug else '')
    return base + (lang + '/' if lang != 'en' else '')


def alternatives(slug):
    result = {lang: route(slug, lang) for lang in LOCALES}
    # Keep all established Combine Photos language URLs in the same reciprocal set.
    if slug == 'collage-maker':
        old = json.loads((ROOT / 'scripts/collage-localizations.json').read_text())
        result.update({lang: route(slug, lang) for lang in old if lang not in result})
    result['x-default'] = route(slug, 'en')
    return result


def alternate_html(slug):
    return ''.join(f'<link rel="alternate" hreflang="{lang}" href="{SITE}{url}">'
                   for lang, url in alternatives(slug).items())


def language_nav(slug, lang):
    labels=dict(LOCALES)
    if slug=='collage-maker':
        old=json.loads((ROOT/'scripts/collage-localizations.json').read_text())
        labels.update({code:entry['label'] for code,entry in old.items() if code not in labels})
    label = load(lang+'.json')['common.language'] if lang in LOCALES else {'ar':'اللغة','id':'Bahasa','th':'ภาษา'}.get(lang,'Language')
    current = LOCALES.get(lang,{'ar':'العربية','id':'Bahasa Indonesia','th':'ไทย'}.get(lang,lang))
    return '<details class="i18n-selector"><summary>'+E(current)+' · '+E(label)+'</summary><nav class="i18n-languages" aria-label="'+E(label)+'">' + ''.join(
        f'<a href="{route(slug, code)}" lang="{code}" hreflang="{code}"' +
        (' aria-current="page"' if code == lang else '') + f'>{label}</a>'
        for code, label in labels.items()) + '</nav></details>'


def store_badge(url, lang, label):
    artwork = load('badge-sources.json')[lang]
    artwork={**artwork,'width':round(artwork['width']),'height':round(artwork['height'])}
    return ('<a class="localized-store-badge" href="'+E(url)+'" aria-label="'+E(label)+'">'+
            image(artwork,label,'official-app-store-badge',True)+'</a>')


def ld(data):
    return '<script type="application/ld+json">' + json.dumps(
        {'@context': 'https://schema.org', **data}, ensure_ascii=False).replace('</', '<\\/') + '</script>'


def image(item, alt, css='', eager=False):
    return (f'<img class="{css}" src="{E(item["src"])}" alt="{E(alt)}" '
            f'width="{item["width"]}" height="{item["height"]}" decoding="async" ' +
            ('fetchpriority="high"' if eager else 'loading="lazy"') + '>')


def build():
    source = load('en.json')
    reviewed = load('review.json')
    stores = load('store-snapshots.json')
    portfolio = json.loads((ROOT / 'scripts/app-portfolio.json').read_text())['apps']
    order = json.loads((ROOT / 'scripts/app-display-order.json').read_text())['app_ids']
    apps = sorted(portfolio, key=lambda a: order.index(a['id']))
    baseline = load('source-baseline.json')
    for app in apps:
        fields = {k: app[k] for k in ('benefit', 'features', 'access', 'caveat')}
        if baseline[app['slug']] != digest(fields):
            raise ValueError('English product facts changed; refresh and review translations: ' + app['slug'])
    # Verify every catalog before emitting links to the complete language set.
    catalogs = {lang:load(lang+'.json') for lang in TARGETS}
    for lang,texts in catalogs.items():
        if set(texts) != set(source) or any(not isinstance(v,str) or not v.strip() for v in texts.values()):
            raise ValueError('Missing or extra translations: '+lang)
        if reviewed['source_sha256'] != digest(source) or reviewed['catalogs'].get(lang) != digest(texts):
            raise ValueError('Catalog differs from reviewed Weblate export: '+lang)
    ui = {lang:{k.removeprefix('common.'):v for k,v in load(lang+'.json').items() if k.startswith('common.')} for lang in LOCALES}
    asset_version=hashlib.sha256((ROOT/'assets/i18n.css').read_bytes()+json.dumps(ui,ensure_ascii=False,sort_keys=True).encode()).hexdigest()[:12]
    written = []
    changed = set()
    for lang,texts in catalogs.items():
        def t(key):
            return E(texts[key])
        def shell(slug, title, description, body, schema):
            url = SITE + route(slug, lang)
            html = (f'<!doctype html><html lang="{lang}" dir="ltr"><head><meta charset="utf-8">'
                    '<meta name="viewport" content="width=device-width,initial-scale=1">'
                    f'<title>{E(title)} | Just Compress</title><meta name="description" content="{E(description)}">'
                    f'<link rel="canonical" href="{url}">{alternate_html(slug)}'
                    f'<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}">'
                    f'<meta property="og:url" content="{url}"><meta property="og:type" content="website">'
                    '<link rel="icon" href="/assets/icons/just-compress-icon.svg" type="image/svg+xml">'
                    '<link rel="stylesheet" href="/assets/portfolio-v2.css?v=20261026-card-links">'
                    f'<link rel="stylesheet" href="/assets/i18n.css?v={asset_version}">' + schema +
                    f'<script defer src="/assets/i18n-ui.js?v={asset_version}"></script>'
                    '<script defer src="/assets/posthog-init.js?v=20261027-i18n"></script>'
                    '</head><body class="portfolio-page"><div class="portfolio-shell">'
                    '<nav class="portfolio-nav" aria-label="'+t('common.navigation')+'">'
                    '<a class="portfolio-brand" href="/">Just Compress</a><div>'
                    f'<a href="{route("",lang)}">{t("common.apps")}</a>'
                    f'<a href="/guides/" lang="en">{t("common.guides_en")}</a>'
                    f'<a href="/support/" lang="en">{t("common.support_en")}</a></div></nav>'
                    + language_nav(slug, lang) + '<main>' + body + '</main>'
                    '<footer class="portfolio-footer"><span>© 2026 Space Sheep Studio</span>'
                    f'<a href="{route("",lang)}">{t("common.apps")}</a>'
                    f'<a href="/privacy/" lang="en">{t("common.website_privacy_en")}</a>'
                    f'<a href="/terms/" lang="en">{t("common.website_terms_en")}</a>'
                    '</footer></div></body></html>')
            if re.search(r'jiali\s+liang', html, re.I):
                raise ValueError('Prohibited public name')
            target = ROOT / route(slug, lang).strip('/') / 'index.html'
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists() or target.read_text() != html:
                changed.add(route(slug,lang))
            target.write_text(html)
            written.append(route(slug, lang))
        cards = []
        for app in apps:
            slug = app['slug']
            store = stores[slug][lang]
            name, store_url = store['trackName'], store['trackViewUrl']
            key = 'apps.' + slug + '.'
            screens = store['screens']
            gallery = '<figure class="store-figure"><div class="store-shots" tabindex="0" aria-label="'+t('common.screenshots')+'">'
            gallery += ''.join('<a href="'+s['src']+'" target="_blank" rel="noopener">' + image(
                s, name + ': ' + texts['common.screenshot'] + ' ' + str(i)) + '</a>' for i,s in enumerate(screens,1))
            gallery += '</div><figcaption>'+t('common.screens_note')+'</figcaption></figure>'
            body = ('<header class="product-heading"><div class="product-identity">' + image(app['icon'], '', 'product-icon', True) +
                    '<div><p class="eyebrow">'+t('common.iphone_app')+'</p><h1>'+E(name)+'</h1></div></div>'
                    '<p class="product-lede">'+t(key+'benefit')+'</p><p class="product-version">'+
                    t('common.version')+' '+E(store['version'])+' · iOS '+E(store['minimumOsVersion'])+' · '+
                    t('common.checked')+' '+E(datetime.fromisoformat(store['checked_at']).astimezone(ZoneInfo('Europe/Paris')).date().isoformat())+'</p>'+
                    store_badge(store_url,lang,texts['common.store'])+
                    ('<p class="storefront-note">'+t('common.singapore_store_note')+'</p>' if store.get('requested_country')=='cn' else '')+
                    '</header>' + gallery +
                    '<section class="product-section"><h2>'+t('common.features')+'</h2><ul class="feature-list">'+
                    ''.join('<li>'+t(key+'feature.'+str(i))+'</li>' for i in range(len(app['features'])))+'</ul></section>'
                    '<section class="product-section"><h2>'+t('common.access')+'</h2><p>'+t(key+'access')+'</p><p>'+t('common.local_offer')+'</p></section>'
                    '<section class="product-section"><h2>'+t('common.before')+'</h2><p>'+t(key+'caveat')+'</p></section>')
            body += '<section class="product-section"><h2>'+t('common.next')+'</h2><p>'+t('common.english_resources')+'</p><p>'
            body += '<a href="'+route(slug,'en')+'" lang="en">'+t('common.full_english')+'</a> · '
            body += '<a href="/apps/'+slug+'/support/" lang="en">'+t('common.support_en')+'</a></p></section>'
            body += '<aside class="product-download"><h2>'+E(name)+'</h2><p>'+t(key+'benefit')+'</p><a class="portfolio-button" href="'+E(store_url)+'">'+t('common.store')+' ↗</a><p class="product-links">'
            privacy = '/apps/'+slug+'/privacy/'
            if (ROOT / privacy.strip('/') / 'index.html').exists():
                body += '<a href="'+privacy+'" lang="en">'+t('common.privacy_en')+'</a> · '
            terms = '/apps/'+slug+'/terms/'
            if not (ROOT / terms.strip('/') / 'index.html').exists():
                terms = 'https://www.apple.com/legal/internet-services/itunes/dev/stdeula/'
            body += '<a href="'+terms+'">'+t('common.terms_en')+'</a></p><p>'+t('common.made_by')+'</p></aside>'
            schema = ld({'@type':'SoftwareApplication', 'name':name, 'url':SITE+route(slug,lang),
                         'downloadUrl':store_url, 'softwareVersion':store['version'], 'inLanguage':lang,
                         'operatingSystem':'iOS '+store['minimumOsVersion'], 'applicationCategory':'UtilitiesApplication',
                         'description':texts[key+'benefit'], 'image':SITE+app['icon']['src'],
                         'screenshot':[SITE+s['src'] for s in screens],
                         'publisher':{'@type':'Organization','name':'Space Sheep Studio'}})
            schema += ld({'@type':'BreadcrumbList','itemListElement':[
                {'@type':'ListItem','position':1,'name':texts['common.apps'],'item':SITE+route('',lang)},
                {'@type':'ListItem','position':2,'name':name,'item':SITE+route(slug,lang)}]})
            separator='。' if lang in ('zh-Hans','zh-Hant','ja') else '. '
            shell(slug, name, texts[key+'benefit']+separator+texts['common.meta_detail'], body, schema)
            cards.append('<article class="app-card"><a class="catalog-identity" href="'+route(slug,lang)+'">'+
                image(app['icon'],'','app-icon')+'<div><h2>'+E(name)+'</h2><p class="benefit">'+t(key+'benefit')+'</p></div></a>'+
                '<figure class="catalog-gallery"><div class="catalog-shots">'+''.join(image(s,name+': '+texts['common.screenshot'],'catalog-shot') for s in screens)+'</div></figure>'+
                '<input id="name-'+app['id']+'" type="hidden" value="'+E(name)+'">'+
                '<div class="actions"><a class="portfolio-button" href="'+route(slug,lang)+'">'+t('common.details')+'</a>'+
                store_badge(store_url,lang,texts['common.store'])+'<button type="button" data-copy="name-'+app['id']+'">'+t('common.copy')+'</button></div></article>')
        body = '<header class="catalog-heading"><h1>'+t('common.directory_title')+'</h1><p>'+t('common.directory_intro')+'</p><input id="find-app" type="search" aria-label="'+t('common.search_label')+'" placeholder="'+t('common.search_placeholder')+'" autocomplete="off"></header><p id="status" role="status" aria-live="polite"></p><section class="catalog-grid app-catalog">'+''.join(cards)+'</section><p id="no-results" hidden>'+t('common.no_results')+'</p><script defer src="/assets/find-app.js?v=20261027-i18n"></script>'
        schema = ld({'@type':'CollectionPage','name':texts['common.directory_title'],'url':SITE+route('',lang),'inLanguage':lang,
                     'mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':stores[a['slug']][lang]['trackName'],'url':SITE+route(a['slug'],lang)} for i,a in enumerate(apps)]}})
        shell('',texts['common.directory_title'],texts['common.directory_intro'],body,schema)
    (ROOT/'assets/i18n-ui.js').write_text('window.spaceSheepI18n = '+json.dumps(ui,ensure_ascii=False).replace('</','<\\/')+';\n')
    # Add language links to source pages without rewriting their prose or scripts.
    for slug in ['', *[a['slug'] for a in apps]]:
        languages = alternatives(slug) if slug == 'collage-maker' else {'en':route(slug,'en')}
        for lang, url in languages.items():
            if lang == 'x-default' or lang in TARGETS:
                continue
            path = ROOT / url.strip('/') / 'index.html'
            html = path.read_text()
            before = html
            html = re.sub(r'<link\b(?=[^>]*\brel=["\']alternate["\'])(?=[^>]*\bhreflang=)[^>]*>', '', html)
            html = re.sub(r'<details class="i18n-selector".*?</details>', '', html, flags=re.S)
            html = re.sub(r'<nav class="i18n-languages".*?</nav>', '', html, flags=re.S)
            if slug=='collage-maker':
                html=re.sub(r'<nav class="(?:product-languages|product-language-links)".*?</nav>','',html,flags=re.S)
            html = re.sub(r'<link rel="stylesheet" href="/assets/i18n.css[^\"]*">', '', html)
            html = html.replace('</head>', alternate_html(slug)+f'<link rel="stylesheet" href="/assets/i18n.css?v={asset_version}"></head>')
            html = html.replace('<main>', language_nav(slug,lang)+'<main>', 1)
            # Source generators with a bare main attribute are also supported.
            if 'class="i18n-languages"' not in html:
                html = re.sub(r'(<main\b[^>]*>)',language_nav(slug,lang)+r'\1',html,count=1)
            # Legacy product summaries also receive Apple's actual localized art.
            # Existing story-page and directory English badges are already official.
            if slug:
                def localize_header(match):
                    header=match.group(0)
                    return re.sub(r'<a\b[^>]*href="(https://apps\.apple\.com/[^\"]+)"[^>]*>.*?</a>',
                        lambda link: store_badge(link.group(1).replace('&amp;','&'),lang,
                            load('en.json')['common.store'] if lang=='en' else 'App Store'),header,count=1,flags=re.S)
                html=re.sub(r'<header\b(?=[^>]*\bclass="[^"]*\bproduct-heading\b)[^>]*>.*?</header>',localize_header,html,flags=re.S)
            if html != before:
                changed.add(url)
            path.write_text(html)
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', ns)
    sitemap_path = ROOT/'sitemap.xml'
    tree = ET.parse(sitemap_path)
    existing = {el.findtext('{'+ns+'}loc') for el in tree.getroot()}
    for el in tree.getroot():
        loc=el.findtext('{'+ns+'}loc')
        if loc and loc.removeprefix(SITE) in changed:
            modified=el.find('{'+ns+'}lastmod')
            if modified is None:modified=ET.SubElement(el,'{'+ns+'}lastmod')
            modified.text=datetime.now(ZoneInfo('Europe/Paris')).date().isoformat()
    for path in written:
        if SITE+path not in existing:
            el = ET.SubElement(tree.getroot(),'{'+ns+'}url')
            ET.SubElement(el,'{'+ns+'}loc').text = SITE+path
            ET.SubElement(el,'{'+ns+'}lastmod').text = '2026-10-27'
    tree.write(sitemap_path,encoding='utf-8',xml_declaration=True)
    print('Built',len(written),'reviewed localized pages; preserved English and established locale URLs')
    return written


if __name__ == '__main__':
    build()
