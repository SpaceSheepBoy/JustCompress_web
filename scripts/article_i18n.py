"""Compile Weblate-reviewed articles. check/build never contact a remote service."""
import argparse
import hashlib
from html import escape
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://justcompress.online'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
UI = {
    'navigation': 'Main navigation', 'guides': 'Guides (English)', 'tools': 'Free tools (English)',
    'apps': 'Apps', 'blog': 'Blog (English)', 'reviewed': 'Reviewed', 'language': 'Language',
    'jump': 'In this guide', 'choose': 'Choose the approach', 'steps': 'Follow the checks',
    'details': 'Read the details', 'chooseHeading': 'Choose the approach before changing the file',
    'stepsHeading': 'Three checks before you send', 'freeTool': 'Open the free PDF compressor (English)',
    'appDisclosure': 'Our app by Space Sheep Studio. See the App Store for current access and purchase options.',
    'store': 'Download on the App Store', 'faq': 'Common questions', 'sources': 'Sources and scope',
    'scope': 'Official help checked on {date}. Limits and interfaces may change. Read the relevant section for your platform and account.',
    'related': 'Related guides', 'english': 'English', 'privacy': 'Privacy (English)',
    'terms': 'Terms (English)', 'support': 'Support (English)',
}


def load(path):
    return json.loads(path.read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def context(page):
    return {**{key:page[key] for key in ('appId','reviewed','figure','primaryCta')},
            **({'photoExample':page['photoExample']} if page.get('photoExample') else {}),
            **{field:{row['id']:row['url'] for row in page[field]} for field in ('sources','related')}}


def documents(root=ROOT):
    directory = root/'locales/articles'
    if not (directory/'config.json').exists():
        return []
    pages = load(root/'scripts/seo-content.json')
    result = []
    for entry in load(directory/'config.json')['articles']:
        matches = [p for p in pages if p['slug'] == entry['slug']]
        if len(matches) != 1 or matches[0].get('i18n', {}).get('id') != entry['id']:
            raise ValueError('Article source/identity not found: '+entry['id'])
        page = matches[0]
        source = {key: page[key] for key in ('tag','title','description','direct','figureAlt','figureCaption')}
        for field in ('cards','sections','faqs','sources','related','steps'):
            seen = set()
            for row in page[field]:
                if not isinstance(row, dict) or not re.fullmatch('[a-z0-9-]+', row.get('id','')) or row['id'] in seen:
                    raise ValueError('Persistent unique IDs required: '+entry['id']+'/'+field)
                seen.add(row['id'])
                for key in ('heading','body','text','label'):
                    if key in row:
                        source[f'{field}.{row["id"]}.{key}'] = row[key]
        source.update({'ui.'+key: text for key, text in {**UI,**page['i18n'].get('ui',{})}.items()})
        source.update({'diagram.'+key: text for key, text in page['i18n']['diagram'].items()})
        source.update({'photo.'+key: text for key, text in page['i18n'].get('photo',{}).items()})
        source['primaryCtaLabel'] = page.get('primaryCtaLabel', UI['freeTool'])
        if any(not isinstance(v,str) or not v.strip() for v in source.values()):
            raise ValueError('Missing source text: '+entry['id'])
        result.append((entry, page, source))
    return result


def route(page, lang):
    return '/'+page['slug']+'/' + (lang+'/' if lang!='en' else '')


def validate(root=ROOT):
    result = []
    config = load(root/'locales/config.json')
    for entry, page, source in documents(root):
        folder = root/'locales/articles'/entry['id']
        if load(folder/'en.json') != source:
            raise ValueError('Article source changed; synchronize Weblate and re-review affected units: '+entry['id'])
        review = load(folder/'review.json')
        if review.get('context_sha256') != digest(context(page)):
            raise ValueError('Article links, app identity or fact date changed; review context: '+entry['id'])
        for lang in entry['locales']:
            if lang == 'en' or lang not in config:
                raise ValueError('Invalid target locale: '+lang)
            target = load(folder/(lang+'.json'))
            status = review.get('languages',{}).get(lang,{})
            if (set(source) != set(target) or any(not isinstance(v,str) or not v.strip() for v in target.values())
                or review.get('source_sha256') != digest(source)
                or review.get('catalogs',{}).get(lang) != digest(target)
                or status.get('approved') != len(source) or status.get('total') != len(source)
                or status.get('failing_check_ids') != []):
                raise ValueError('Article review/check gate failed: '+entry['id']+'/'+lang)
            for key in source:
                if set(re.findall(r'\{\w+\}',source[key])) != set(re.findall(r'\{\w+\}',target[key])):
                    raise ValueError('Placeholder changed: '+key)
                if re.findall(r'\d+(?:\.\d+)?',source[key]) != re.findall(r'\d+(?:\.\d+)?',target[key]):
                    raise ValueError('Numeric claim changed: '+key)
                if re.search(r'jiali\s+liang|[—–]',target[key],re.I):
                    raise ValueError('Prohibited public copy: '+key)
        result.append((entry,page,source))
    return result


def language_markup(entry, page, lang, text, config):
    codes = ['en']+entry['locales']
    alternates = ''.join(f'<link rel="alternate" hreflang="{code}" href="{SITE}{route(page,code)}">' for code in codes)
    alternates += f'<link rel="alternate" hreflang="x-default" href="{SITE}{route(page,"en")}">'
    nav = '<details class="i18n-selector" data-article-language><summary>'+escape(config[lang]['label'])+' · '+escape(text['ui.language'])+'</summary><nav class="i18n-languages">'
    nav += ''.join(f'<a href="{route(page,code)}" lang="{code}" hreflang="{code}"'+(' aria-current="page"' if code==lang else '')+'>'+escape(config[code]['label'])+'</a>' for code in codes)
    return alternates, nav+'</nav></details>'


def diagram(page, text):
    # HTML text wraps at phone widths; no text is baked into a small image.
    def t(key): return escape(text['diagram.'+key])
    cards = [('step-limit','limit-accounts','limit-total'),('step-copy','copy-details','copy-original'),('step-delivery','delivery-options','delivery-access')]
    return '<div class="article-workflow" role="group" aria-label="'+escape(text['figureAlt'])+'"><h3>'+t('title')+'</h3>'+''.join('<div><strong>'+t(a)+'</strong><p>'+t(b)+'</p><p>'+t(c)+'</p></div>' for a,b,c in cards)+'</div>'


def render(entry, page, text, lang, root=ROOT):
    config = load(root/'locales/config.json')
    stores = load(root/'locales/store-snapshots.json')
    app = next(a for a in load(root/'scripts/app-portfolio.json')['apps'] if a['id']==page['appId'])
    store = stores[app['slug']][lang]
    region_note = ''
    if lang=='zh-Hans':
        region_note = '<p class="storefront-note">'+escape(load(root/'locales/zh-Hans.json')['common.singapore_store_note'])+'</p>'
    def t(key): return escape(text[key])
    def ui(key): return t('ui.'+key)
    url = SITE+route(page,lang)
    alternates, languages = language_markup(entry,page,lang,text,config)
    sections = ''.join('<h2>'+t('sections.'+row['id']+'.heading')+'</h2><p>'+t('sections.'+row['id']+'.body')+'</p>' for row in page['sections'])
    cards = ''.join('<div><h3>'+t('cards.'+row['id']+'.heading')+'</h3><p>'+t('cards.'+row['id']+'.body')+'</p></div>' for row in page['cards'])
    steps = ''.join('<li>'+t('steps.'+row['id']+'.text')+'</li>' for row in page['steps'])
    faqs = ''.join('<details><summary>'+t('faqs.'+row['id']+'.heading')+'</summary><p>'+t('faqs.'+row['id']+'.body')+'</p></details>' for row in page['faqs'])
    sources = ''.join('<li><a href="'+escape(row['url'])+'">'+t('sources.'+row['id']+'.label')+(' ('+ui('english')+')' if '/en-' in row['url'] or 'hl=en' in row['url'] or 'en-us' in row['url'] else '')+'</a></li>' for row in page['sources'])
    related = ''.join('<li><a href="'+escape(row['url'])+'">'+t('related.'+row['id']+'.label')+' ('+ui('english')+')</a></li>' for row in page['related'])
    schema = [{'@type':'Article','headline':text['title'],'description':text['description'],'inLanguage':lang,'datePublished':entry['translation_date'],'dateModified':entry.get('translation_modified',entry['translation_date']),'mainEntityOfPage':url,'author':{'@type':'Organization','name':'Space Sheep Studio'},'publisher':{'@type':'Organization','name':'Space Sheep Studio'}},
              {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Just Compress','item':SITE+'/'},{'@type':'ListItem','position':2,'name':text['ui.guides'],'item':SITE+'/guides/'},{'@type':'ListItem','position':3,'name':text['title'],'item':url}]},
              {'@type':'FAQPage','inLanguage':lang,'mainEntity':[{'@type':'Question','name':text['faqs.'+r['id']+'.heading'],'acceptedAnswer':{'@type':'Answer','text':text['faqs.'+r['id']+'.body']}} for r in page['faqs']]}]
    ld = ''.join('<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org',**s},ensure_ascii=False).replace('</','<\\/')+'</script>' for s in schema)
    styles = ''.join('<link rel="stylesheet" href="/assets/'+name+'?v='+hashlib.sha256((root/'assets'/name).read_bytes()).hexdigest()[:12]+'">' for name in ['tutorial-guides.css','legacy-guides.css','i18n.css','article-i18n.css'])
    return f'''<!doctype html><html lang="{lang}" dir="ltr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t('title')} | Just Compress</title><meta name="description" content="{t('description')}"><link rel="canonical" href="{url}">{alternates}
<meta property="og:title" content="{t('title')}"><meta property="og:description" content="{t('description')}"><meta property="og:type" content="article"><meta property="og:url" content="{url}">
<link rel="icon" href="/assets/icons/just-compress-icon.svg">{styles}{ld}<script defer src="/assets/i18n-ui.js"></script><script defer src="/assets/posthog-init.js?v=20261022-3"></script></head>
<body class="guide-page"><div class="guide-shell"><nav class="guide-nav" aria-label="{ui('navigation')}"><a class="guide-brand" href="/">Just Compress</a><div><a href="/guides/">{ui('guides')}</a><a href="/tools/">{ui('tools')}</a><a href="/apps/{lang}/">{ui('apps')}</a><a href="/blog/">{ui('blog')}</a></div></nav>
{languages}<main><header class="guide-heading"><p class="guide-eyebrow">{t('tag')} · {ui('reviewed')} <time datetime="{page['reviewed']}">{page['reviewed']}</time></p><h1>{t('title')}</h1><p class="guide-lede">{t('direct')}</p></header>
<nav class="repair-jump" aria-label="{ui('jump')}"><a href="#choose">{ui('choose')}</a><a href="#steps">{ui('steps')}</a><a href="#details">{ui('details')}</a></nav>
<article class="guide-article" data-weblate-article="{entry['id']}"><section id="choose"><h2>{ui('chooseHeading')}</h2><div class="repair-cards">{cards}</div><figure>{diagram(page,text)}<figcaption>{t('figureCaption')}</figcaption></figure></section>
<section id="steps"><h2>{ui('stepsHeading')}</h2><ol>{steps}</ol><p><a class="guide-button" href="{page['primaryCta']}">{t('primaryCtaLabel')} ↗</a></p></section><section id="details">{sections}</section>
<aside class="guide-cta"><div><strong>{escape(store['trackName'])}</strong><p>{ui('appDisclosure')}</p>{region_note}</div><a class="localized-store-badge" href="{escape(store['trackViewUrl'])}"><img class="official-app-store-badge" src="/assets/brand/app-store-badges/{lang}.svg" alt="{ui('store')}" height="40" width="120"></a></aside>
<section class="guide-faq"><h2>{ui('faq')}</h2>{faqs}</section><section><h2>{ui('sources')}</h2><p>{escape(text['ui.scope'].format(date=page['reviewed']))}</p><ul>{sources}</ul></section><section><h2>{ui('related')}</h2><ul>{related}</ul></section></article></main>
<footer class="guide-footer"><span>© 2026 Space Sheep Studio</span><a href="/guides/">{ui('guides')}</a><a href="/privacy/">{ui('privacy')}</a><a href="/terms/">{ui('terms')}</a><a href="/support/">{ui('support')}</a></footer></div></body></html>\n'''


def build(root=ROOT):
    articles = validate(root)  # All review gates run before any page writes.
    writes = {}
    config = load(root/'locales/config.json')
    for entry,page,source in articles:
        for lang in entry['locales']:
            text = load(root/'locales/articles'/entry['id']/(lang+'.json'))
            writes[root/route(page,lang).strip('/')/'index.html'] = render(entry,page,text,lang,root)
        english = root/page['slug']/'index.html'
        soup = BeautifulSoup(english.read_text(),'html.parser')
        for old in soup.select('[data-article-language],link[rel="alternate"][hreflang]'):
            old.decompose()
        alternates, nav = language_markup(entry,page,'en',source,config)
        soup.head.append(BeautifulSoup(alternates,'html.parser'))
        if not soup.select_one('link[href^="/assets/i18n.css"]'):
            soup.head.append(BeautifulSoup('<link rel="stylesheet" href="/assets/i18n.css">','html.parser'))
        soup.select_one('main').insert(0,BeautifulSoup(nav,'html.parser'))
        writes[english] = str(soup)
    # Stage complete render results before committing any output to disk.
    for path,html in writes.items():
        path.parent.mkdir(parents=True,exist_ok=True)
        if not path.exists() or path.read_text()!=html:
            path.write_text(html)
    file = root/'sitemap.xml'
    sitemap = file.read_text()
    existing = {n.findtext('{'+NS+'}loc') for n in ET.fromstring(sitemap)}
    additions = []
    for entry,page,_ in articles:
        for lang in entry['locales']:
            url = SITE+route(page,lang)
            if url not in existing:
                additions.append('  <url><loc>'+escape(url)+'</loc><lastmod>'+entry['translation_date']+'</lastmod></url>\n')
    if additions:
        file.write_text(sitemap.replace('</urlset>',''.join(additions)+'</urlset>'))
    index = root/'guides/index.html'
    soup = BeautifulSoup(index.read_text(),'html.parser')
    for old in soup.select('[data-article-translations]'):
        old.decompose()
    links = []
    for entry,page,_ in articles:
        for lang in entry['locales']:
            text = load(root/'locales/articles'/entry['id']/(lang+'.json'))
            links.append('<li><a href="'+route(page,lang)+'" lang="'+lang+'">'+escape(text['title'])+' ('+escape(config[lang]['label'])+')</a></li>')
    if links:
        soup.main.append(BeautifulSoup('<section data-article-translations><h2>Guides in other languages</h2><ul>'+''.join(links)+'</ul></section>','html.parser'))
        output = str(soup)
        if output != index.read_text():
            index.write_text(output)
    print('Built reviewed articles:',len(articles),'localized pages:',sum(len(a[0]['locales']) for a in articles))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['check','build'])
    args = parser.parse_args()
    if args.action=='build':
        build()
    else:
        print('Validated article catalogs:',len(validate()))
