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
LOCALES = {'en': 'English', 'fr': 'Français', 'ja': '日本語'}


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
    label = {'fr':'Langue','ja':'言語'}.get(lang,'Language')
    return '<nav class="i18n-languages" aria-label="'+label+'">' + ''.join(
        f'<a href="{route(slug, code)}" lang="{code}" hreflang="{code}"' +
        (' aria-current="page"' if code == lang else '') + f'>{label}</a>'
        for code, label in LOCALES.items()) + '</nav>'


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
    written = []
    for lang in ('fr', 'ja'):
        texts = load(lang + '.json')
        if set(texts) != set(source) or any(not isinstance(v, str) or not v.strip() for v in texts.values()):
            raise ValueError('Missing or extra translations: ' + lang)
        if reviewed['source_sha256'] != digest(source) or reviewed['catalogs'][lang] != digest(texts):
            raise ValueError('Catalog differs from reviewed Weblate export: ' + lang)
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
                    '<link rel="stylesheet" href="/assets/i18n.css?v=20261027">' + schema +
                    '<script defer src="/assets/i18n-ui.js?v=20261027"></script>'
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
                    t('common.checked')+' '+E(datetime.fromisoformat(store['checked_at']).astimezone(ZoneInfo('Europe/Paris')).date().isoformat())+'</p>'
                    '<a class="portfolio-button" href="'+E(store_url)+'">'+t('common.store')+' ↗</a></header>' + gallery +
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
            shell(slug, name, texts[key+'benefit']+'. '+texts['common.meta_detail'], body, schema)
            cards.append('<article class="app-card"><a class="catalog-identity" href="'+route(slug,lang)+'">'+
                image(app['icon'],'','app-icon')+'<div><h2>'+E(name)+'</h2><p class="benefit">'+t(key+'benefit')+'</p></div></a>'+
                '<figure class="catalog-gallery"><div class="catalog-shots">'+''.join(image(s,name+': '+texts['common.screenshot'],'catalog-shot') for s in screens)+'</div></figure>'+
                '<input id="name-'+app['id']+'" type="hidden" value="'+E(name)+'">'+
                '<div class="actions"><a class="portfolio-button" href="'+route(slug,lang)+'">'+t('common.details')+'</a>'+
                '<a href="'+E(store_url)+'">App Store ↗</a><button type="button" data-copy="name-'+app['id']+'">'+t('common.copy')+'</button></div></article>')
        body = '<header class="catalog-heading"><h1>'+t('common.directory_title')+'</h1><p>'+t('common.directory_intro')+'</p><input id="find-app" type="search" aria-label="'+t('common.search_label')+'" placeholder="'+t('common.search_placeholder')+'" autocomplete="off"></header><p id="status" role="status" aria-live="polite"></p><section class="catalog-grid app-catalog">'+''.join(cards)+'</section><p id="no-results" hidden>'+t('common.no_results')+'</p><script defer src="/assets/find-app.js?v=20261027-i18n"></script>'
        schema = ld({'@type':'CollectionPage','name':texts['common.directory_title'],'url':SITE+route('',lang),'inLanguage':lang,
                     'mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':stores[a['slug']][lang]['trackName'],'url':SITE+route(a['slug'],lang)} for i,a in enumerate(apps)]}})
        shell('',texts['common.directory_title'],texts['common.directory_intro'],body,schema)
    ui = {lang:{k.removeprefix('common.'):v for k,v in load(lang+'.json').items() if k.startswith('common.')} for lang in LOCALES}
    (ROOT/'assets/i18n-ui.js').write_text('window.spaceSheepI18n = '+json.dumps(ui,ensure_ascii=False).replace('</','<\\/')+';\n')
    # Add language links to source pages without rewriting their prose or scripts.
    for slug in ['', *[a['slug'] for a in apps]]:
        languages = alternatives(slug) if slug == 'collage-maker' else {'en':route(slug,'en')}
        for lang, url in languages.items():
            if lang == 'x-default' or lang in ('fr','ja'):
                continue
            path = ROOT / url.strip('/') / 'index.html'
            html = path.read_text()
            html = re.sub(r'<link\b(?=[^>]*\brel=["\']alternate["\'])(?=[^>]*\bhreflang=)[^>]*>', '', html)
            html = re.sub(r'<nav class="i18n-languages".*?</nav>', '', html, flags=re.S)
            html = re.sub(r'<link rel="stylesheet" href="/assets/i18n.css[^\"]*">', '', html)
            html = html.replace('</head>', alternate_html(slug)+'<link rel="stylesheet" href="/assets/i18n.css?v=20261027"></head>')
            html = html.replace('<main>', language_nav(slug,lang)+'<main>', 1)
            # Source generators with a bare main attribute are also supported.
            if 'class="i18n-languages"' not in html:
                html = re.sub(r'(<main\b[^>]*>)',language_nav(slug,lang)+r'\1',html,count=1)
            path.write_text(html)
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', ns)
    sitemap_path = ROOT/'sitemap.xml'
    tree = ET.parse(sitemap_path)
    existing = {el.findtext('{'+ns+'}loc') for el in tree.getroot()}
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
