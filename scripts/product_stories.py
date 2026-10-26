"""Build the three leading Apps' product pages from separate, evidence-based briefs.

Only the presentation is shared. Copy, palette, limits, screenshots and use cases
belong to each product. Existing localized and legal pages are maintained separately.
"""
from html import escape as E
from pathlib import Path
import json
import product_depth as depth

SITE = 'https://justcompress.online'
ROOT = Path(__file__).resolve().parents[1]
STORIES = json.loads((ROOT / 'scripts/product-stories.json').read_text())
GUIDES = {
    '6812821310': [
        ('/guides/hdr-to-sdr-iphone/', 'Convert HDR to SDR', 'Follow the standard-color export workflow with your iPhone video.'),
        ('/guides/hevc-to-mp4-iphone/', 'Make an H.264 MP4 copy', 'Check the destination’s format requirement before converting HEVC.'),
        ('/guides/batch-convert-hdr-videos-iphone/', 'Convert several clips', 'Apply a consistent export goal, then check each finished result.')],
    '6769563659': [
        ('/iphone-video-tutorials/15-how-to-trim-audio-on-iphone/', 'Trim a recording', 'Choose the section you need and save a separate clip.'),
        ('/iphone-video-tutorials/14-how-to-split-an-audio-file-on-iphone/', 'Split a long audio file', 'Follow the recording-to-segments workflow.'),
        ('/compress-audio-file-iphone/', 'Make an audio file smaller', 'Choose a practical size and sound-quality tradeoff.')],
    '6810266264': [
        ('/guides/combine-photos-iphone/', 'Combine photos on iPhone', 'Follow the photo selection, layout and export walkthrough.'),
        ('/combine-photos/', 'Combine photos in a browser', 'Use the separate online tool when that suits your task.'),
        ('/apps/collage-maker/support/', 'Get help with your image', 'Find support for the app, exports and purchase questions.')]
}


def ld(data):
    return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', **data}, ensure_ascii=False).replace('</', '<\\/') + '</script>'


def lines(parts):
    return '<br>'.join(E(p) for p in parts)


def picture(screen, alt, eager=False):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="{screen["src"]}" width="{screen["width"]}" height="{screen["height"]}" alt="{E(alt)}" {loading} decoding="async">'


def policy_links(root, app):
    links = []
    for part, label in [('privacy', 'Privacy'), ('terms', 'Terms'), ('support', 'Support')]:
        url = '/apps/' + app['slug'] + '/' + part + '/'
        if (root / url.strip('/') / 'index.html').exists():
            links.append((url, label))
        elif part == 'terms':
            links.append(('https://www.apple.com/legal/internet-services/itunes/dev/stdeula/', 'Apple EULA'))
    return ''.join(f'<a href="{url}">{label}</a>' for url, label in links)


def build(root, app):
    brief = STORIES[app['id']]
    route = '/apps/' + app['slug'] + '/'
    sources = json.loads((root / 'assets/product-pages' / app['slug'] / 'sources.json').read_text())
    if sources['published_version'] != app['version']:
        raise ValueError('Refresh published content and screenshot evidence for ' + app['name'])
    screens = sources['screens']
    icon = app['icon']
    store = E(app['store_url'])
    alternatives = ''
    languages = ''
    if app['slug'] == 'collage-maker':
        locales = json.loads((root / 'scripts/collage-localizations.json').read_text())
        urls = {code: route + (code + '/' if code != 'en' else '') for code in locales}
        urls['x-default'] = route
        alternatives = ''.join(f'<link rel="alternate" hreflang="{code}" href="{SITE}{url}">' for code, url in urls.items())
        languages = '<nav class="product-language-links" aria-label="Product information language"><span>More product languages:</span>' + ''.join(f'<a href="{urls[code]}" lang="{code}">{E(value["label"])}</a>' for code, value in locales.items() if code != 'en') + '</nav>'
    badge = f'<a class="app-store-badge" href="{store}" aria-label="Download {E(brief["brand"])} on the App Store"><img src="/assets/brand/download-on-the-app-store.svg" width="150" height="50" alt="Download on the App Store"></a>'
    hero = f'''<header class="hero"><div class="hero-copy"><h1>{lines(brief['headline'])}</h1><p class="lede">{E(brief['description'])}</p><p class="hero-promise">{E(brief['promise'])}</p><a class="learn-more" href="#features">Learn More</a><div class="hero-highlights"><span class="highlight-label"><span aria-hidden="true">{brief['highlight'][0]}</span>{E(brief['highlight'][1])}</span><span>{E(brief['highlight'][2])}</span></div><div class="hero-download">{badge}<p>{E(brief['download_note'])}</p></div></div><figure class="hero-screens" id="app-screens" aria-label="Three real {E(brief['brand'])} app screens">{''.join(picture(s, brief['brand'] + ': ' + brief['screen_labels'][i], True) for i,s in enumerate(screens))}<figcaption class="visually-hidden">Real app interfaces, shown without marketing titles or drawn phone frames.</figcaption></figure></header>'''
    features = f'<section class="section" id="features"><div class="section-heading"><p class="eyebrow">{E(brief["brand"])} for iPhone</p><h2>{lines(brief["features_title"])}</h2><p>{E(brief["features_intro"])}</p></div><div class="benefits">' + ''.join(f'<article class="benefit"><span class="symbol" aria-hidden="true">{symbol}</span><h3>{E(title)}</h3><p>{E(body)}</p></article>' for symbol,title,body in brief['features']) + '</div></section>'
    comparison = ''
    if app['slug'] == 'videofix':
        comparison = '<section class="section" id="color-example"><div class="section-heading"><p class="eyebrow">A real Apple Log example</p><h2>From flat Log<br>to standard SDR color.</h2><p>The same scene, at the same moment, from a supplied VideoFix conversion.</p></div><div class="color-comparison">'
        for screen, label in zip(sources['comparison'], ['Before · Apple ProRes Log', 'After · Rec.709 SDR']):
            comparison += f'<figure><figcaption>{label}</figcaption><a href="{screen["src"]}" target="_blank" rel="noopener" aria-label="Open {label} frame full size">{picture(screen, label + ": matching portrait frame at 2.000 seconds")}</a></figure>'
        comparison += '</div><p class="fine-print">Matching frames at 2.000 seconds from the supplied original and supplied H.264 SDR export. No creative color adjustment was applied to these frames. Apple Log is not HDR; this is one conversion example, not a guarantee for every source or display. Tap a frame to inspect it.</p></section>'
    steps = f'<section class="section" id="how-it-works"><div class="section-heading"><p class="eyebrow">How it works</p><h2>{E(brief["workflow_title"])}</h2></div><div class="steps">' + ''.join(f'<article class="step"><span class="step-number">0{i+1}</span><h3>{E(title)}</h3><p>{E(body)}</p></article>' for i,(title,body) in enumerate(brief['steps'])) + '</div></section>'
    stories = '<section class="section" aria-label="Inside the app">'
    for story in brief['stories']:
        screen = sources['detail_screen'] if story['screen'] == 'detail' else screens[story['screen']]
        stories += f'<div class="feature-story"><figure class="feature-media"><a href="{screen["src"]}" target="_blank" rel="noopener" aria-label="Open {E(brief["brand"])} app screen full size">{picture(screen, brief["brand"] + ": " + " ".join(story["title"]))}</a></figure><div class="feature-copy"><p class="eyebrow">{E(story["eyebrow"])}</p><h3>{lines(story["title"])}</h3><p>{E(story["body"])}</p><a class="text-link" href="{story["link"][0]}">{E(story["link"][1])} ↗</a></div></div>'
    stories += '<p class="fine-print screen-note">Actual app screens with example media and settings. Open a screen to inspect it full size.</p>'
    if app['slug'] == 'collage-maker':
        stories += '<p class="fine-print">Example travel photography by <a href="https://unsplash.com/photos/yCVP-vBGdAc">Peter Thomas</a> and <a href="https://unsplash.com/photos/86zO-MVZbtw">Redd Francisco</a> on Unsplash.</p>'
    stories += '</section>'
    access = '<section class="section" id="access"><div class="section-heading"><p class="eyebrow">Access and purchases</p><h2>Try the workflow.<br>Choose the access you need.</h2></div><div class="access-grid">'
    for label,title,items in [('INCLUDED', brief['free_title'], brief['free_items']), ('OPTIONAL PRO', brief['pro_title'], brief['pro_items'])]:
        access += f'<article class="access-card"><span class="pill">{label}</span><h3>{E(title)}</h3><ul>' + ''.join('<li>' + E(item) + '</li>' for item in items) + '</ul></article>'
    access += f'</div><p class="fine-print">{E(brief["access_note"])}</p></section>'
    guides = '<section class="section" id="guides"><div class="section-heading"><p class="eyebrow">Practical guides & help</p><h2>See the next step.</h2></div><div class="guide-grid">' + ''.join(f'<article class="guide-card"><p class="guide-type">{E(brief["brand"]).upper()}</p><h3><a href="{url}">{E(title)}</a></h3><p>{E(body)}</p><a class="text-link" href="{url}">Open the guide ↗</a></article>' for url,title,body in GUIDES[app['id']]) + depth.topic_cards(app['slug']) + '</div></section>'
    faq = '<section class="section" id="faq"><div class="section-heading"><p class="eyebrow">Useful answers</p><h2>Before you start.</h2></div><div class="faq">' + ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in brief['faq']) + f'</div><p class="fine-print">{E(app["name"])} · Published iPhone version {E(app["version"])} · iOS {E(app["minimum_os"])} or later · US App Store checked October 26, 2026.</p>{languages}</section>'
    closing = f'<aside class="closing"><h2>{lines(brief["closing_title"])}</h2><p>{E(brief["closing_body"])}</p><a class="story-button" href="{store}">Get {E(brief["brand"])} on the App Store ↗</a><p class="fine-print">{E(brief["download_note"])}</p></aside>'
    schema = ld({'@type': 'SoftwareApplication', 'name': app['name'], 'url': SITE + route, 'downloadUrl': app['store_url'], 'softwareVersion': app['version'], 'operatingSystem': 'iOS ' + app['minimum_os'] + ' or later', 'applicationCategory': 'PhotographyApplication' if app['slug'] == 'collage-maker' else 'MultimediaApplication', 'description': brief['meta_description'], 'image': SITE + icon['src'], 'screenshot': [SITE + s['src'] for s in screens], 'publisher': {'@type': 'Organization', 'name': 'Space Sheep Studio'}})
    schema += ld({'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Apps', 'item': SITE + '/apps/'}, {'@type': 'ListItem', 'position': 2, 'name': app['name'], 'item': SITE + route}]})
    html = f'''<!doctype html><html lang="en" dir="ltr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(app['name'])} for iPhone | Just Compress</title><meta name="description" content="{E(brief['meta_description'])}"><link rel="canonical" href="{SITE}{route}">{alternatives}<meta property="og:title" content="{E(app['name'])}"><meta property="og:description" content="{E(brief['meta_description'])}"><meta property="og:type" content="website"><meta property="og:url" content="{SITE}{route}"><meta property="og:image" content="{SITE}{icon['src']}"><meta name="twitter:card" content="summary"><meta name="apple-itunes-app" content="app-id={app['id']}"><link rel="icon" href="{icon['src']}" type="image/jpeg"><link rel="stylesheet" href="/assets/product-story.css?v=20261026-wins"><link rel="stylesheet" href="/assets/product-stories.css?v=20261026"><link rel="stylesheet" href="/assets/sitewide.css?v=20261024">{schema}<script defer src="/assets/posthog-init.js?v=20261022-3"></script></head><body class="product-story product-detail theme-{brief['theme']} site-public"><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><nav class="product-nav wrap" aria-label="Main navigation"><a class="product-brand" href="{route}"><img src="{icon['src']}" width="{icon['width']}" height="{icon['height']}" alt="{E(app['name'])} icon"><span>{E(brief['brand'])}</span></a><div class="nav-links"><a class="desktop-link" href="#features">Features</a><a class="mobile-hide" href="#guides">Guides</a><a class="desktop-link" href="#faq">FAQ</a><a class="desktop-link" href="/apps/">All apps ↗</a><a class="story-button" href="{store}">Get app ↗</a></div></nav></header><main id="main" class="wrap">{hero}{features}{comparison}{steps}{stories}{access}{guides}{faq}{closing}</main><footer class="story-footer wrap"><span>© 2026 Space Sheep Studio</span><div><a href="/">Just Compress</a><a href="/apps/">All apps</a>{policy_links(root, app)}<a href="/privacy/">Website privacy</a></div></footer></body></html>'''
    html = html.replace('<link rel="stylesheet" href="/assets/sitewide.css?v=20261024">', '<link rel="stylesheet" href="/assets/sitewide.css?v=20261024">' + depth.resources(app['slug']))
    html = html.replace(hero + features, hero + depth.jump_links() + features + depth.gallery(app['slug'], sources, brief['brand']))
    html = html.replace(steps + stories, depth.tool(app['slug']) + depth.cases(app['slug']) + steps + stories + depth.choices(app['slug']))
    html = html.replace(access + guides, access + depth.studio(app['slug'], app) + guides)
    depth.build_guides(root, app)
    destination = root / route.strip('/') / 'index.html'
    destination.write_text(html)
    print('Built', app['name'], 'product story')


if __name__ == '__main__':
    for app in json.loads((ROOT / 'scripts/app-portfolio.json').read_text())['apps']:
        if app['id'] in STORIES:
            build(ROOT, app)
