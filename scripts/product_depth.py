"""Shared rendering for product-specific galleries, practical examples and web tryouts.

Content lives in product-depth.json. Existing real captures and the existing photo
combiner are reused; no synthetic ratings, reviews or usage statistics are generated.
"""
from html import escape as E
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DEPTH = json.loads((ROOT / 'scripts/product-depth.json').read_text())


def resources(slug):
    photo = '<script defer src="/assets/combine-photos.js"></script>' if slug == 'collage-maker' else ''
    return '<link rel="stylesheet" href="/assets/product-depth.css?v=20261026-depth"><script type="module" src="/assets/product-depth.js?v=20261026-depth"></script>' + photo


def jump_links():
    return '<nav class="depth-jumps" aria-label="Explore this app"><a href="#screenshots">See the screens</a><a href="#try-it">Try it here</a><a href="#use-cases">Everyday uses</a><a href="#choose">Find your fit</a><a href="#faq">Questions</a></nav>'


def heading(eyebrow, title, intro=''):
    return f'<div class="section-heading"><p class="eyebrow">{E(eyebrow)}</p><h2>{E(title)}</h2>' + (f'<p>{E(intro)}</p>' if intro else '') + '</div>'


def gallery(slug, sources, brand):
    d = DEPTH[slug]
    images = sources['hero_screens'] if slug == 'sober-wins' else sources['screens']
    items = ''
    for index, title, body in d['gallery']:
        if isinstance(index, int):
            image = images[index]
        elif index == 'detail':
            image = sources['detail_screen']
        else:
            image = next(s for s in sources['screenshots'] if s['name'] == index)
        items += f'<figure class="gallery-item"><a href="{image["src"]}" target="_blank" rel="noopener" aria-label="Open {E(brand + ": " + title)} full size"><img src="{image["src"]}" width="{image["width"]}" height="{image["height"]}" loading="lazy" decoding="async" alt="{E(brand + ": " + title)}"></a><figcaption><h3>{E(title)}</h3><p>{E(body)}</p></figcaption></figure>'
    return '<section class="section depth-gallery" id="screenshots">' + heading('Take a closer look', d['gallery_title'], d['gallery_intro']) + '<div class="gallery-toolbar"><p>Swipe, scroll or use the arrows. Select a screen to open the original image.</p><div class="gallery-controls" hidden><button type="button" data-gallery-prev aria-label="Previous app screens">←</button><button type="button" data-gallery-next aria-label="Next app screens">→</button></div></div><div class="gallery-track" tabindex="0" aria-label="' + E(brand) + ' screenshot gallery">' + items + '</div></section>'


def cases(slug):
    d = DEPTH[slug]
    return '<section class="section" id="use-cases">' + heading('Everyday uses', d['scenes_title']) + '<div class="depth-cases">' + ''.join(f'<article><span class="case-number">0{i+1}</span><h3>{E(title)}</h3><p>{E(body)}</p><a class="text-link" href="{url}">{E(label)} ↗</a></article>' for i, (title, body, url, label) in enumerate(d['scenes'])) + '</div></section>'


def choices(slug):
    d = DEPTH[slug]
    return '<section class="section" id="choose">' + heading('Choose for your task', d['choice_title'], d['choice_intro']) + '<div class="choice-table-wrap"><table class="choice-table"><caption class="visually-hidden">Choose a workflow for your task</caption><thead><tr><th scope="col">What you need</th><th scope="col">A starting point</th><th scope="col">What to check</th></tr></thead><tbody>' + ''.join(f'<tr><th scope="row">{E(need)}</th><td>{E(choice)}</td><td>{E(check)}</td></tr>' for need,choice,check in d['choices']) + '</tbody></table></div></section>'


def studio(slug, app):
    d = DEPTH[slug]
    route = '/apps/' + slug + '/'
    return '<section class="section" id="made-by"><div class="depth-studio"><div>' + heading('Made by Space Sheep Studio', d['studio_title']) + f'<p>{E(d["studio_body"])}</p><a class="text-link" href="/apps/">Explore the studio’s apps ↗</a></div><aside class="source-card"><h3>Check the source.</h3><p>Published iPhone version {E(app["version"])}. Screens and access details were checked against the US App Store on October 26, 2026.</p><ul><li><a href="{E(app["store_url"])}">Read the official App Store listing</a></li><li><a href="{route}support/">Get app-specific support</a></li><li><a href="{route}privacy/">Read this app’s privacy policy</a></li></ul><p class="fine-print">The store is the source for current availability, user reviews and local purchase offers.</p></aside></div></section>'


def topic_cards(slug):
    return ''.join(f'<article class="guide-card"><p class="guide-type">EXPLORE THE TASK</p><h3><a href="{url}">{E(title)}</a></h3><p>{E(body)}</p><a class="text-link" href="{url}">Read the guide ↗</a></article>' for url,title,body in DEPTH[slug]['topics'])


def tool(slug):
    d = DEPTH[slug]
    if d['tool'] == 'video':
        body = '''<form class="depth-form" id="video-workflow"><label for="video-source">What is the source?</label><select id="video-source"><option value="hdr">HDR video</option><option value="log">Apple ProRes Log</option><option value="hevc">HEVC video, already SDR</option><option value="sdr">SDR video that already plays correctly</option></select><label for="video-goal">What does the destination need?</label><select id="video-goal"><option value="sdr">Standard SDR color</option><option value="h264">An H.264 MP4</option><option value="fps">A steady frame rate</option><option value="audio">Only the audio</option></select><button type="submit">Find a workflow</button><noscript><p>Use the task comparison below to choose a workflow without JavaScript.</p></noscript></form><div class="tool-result" id="video-result" role="status"><h3>Start with the destination.</h3><p>Select the source and requirement, then find a workflow. Always check the exported copy in its intended destination.</p></div>'''
    elif d['tool'] == 'audio':
        body = '''<form class="depth-form" id="audio-size"><label for="audio-minutes">Duration in minutes</label><input id="audio-minutes" type="number" min="0.1" max="10080" step="any" value="60" required inputmode="decimal"><label for="audio-bitrate">Output bitrate in kbps</label><input id="audio-bitrate" type="number" min="8" max="320" step="any" value="128" required inputmode="decimal"><label for="audio-limit">Attachment limit in MB</label><input id="audio-limit" type="number" min="0.1" max="10000" step="any" value="25" required inputmode="decimal"><button type="submit">Estimate file size</button></form><div class="tool-result" id="audio-result" role="status"><h3>60 minutes at 128 kbps ≈ 57.6 MB.</h3><p>Audio payload only. A 25 MB target gives a theoretical ceiling of 55.6 kbps before overhead. Choose a supported setting below the ceiling, leave room for overhead and listen to the result.</p></div>'''
    elif d['tool'] == 'breathing':
        body = '''<div class="breathing-demo"><div class="breathing-orb" id="breathing-orb" aria-hidden="true"><span>Pause</span></div><div><p class="breathing-phase" id="breathing-phase" role="status">Ready when you are.</p><p id="breathing-time">One minute · six gentle rounds</p><div class="tool-actions"><button type="button" id="breathing-start">Start one minute</button><button type="button" id="breathing-stop" disabled>Stop</button></div><p class="fine-print">Follow a comfortable pace; do not force your breathing. This is a simple pause, not treatment or emergency support. Switching away from this page stops the exercise.</p><noscript><p>Without a timer, breathe comfortably and use the in-app guide whenever you want a pause.</p></noscript></div></div>'''
    else:
        body = '''<div class="photo-workbench"><div class="settings"><label class="drop" id="drop"><b>Add your photos</b><span>JPG, PNG, WebP · up to 12 images</span><input id="files" type="file" accept="image/jpeg,image/png,image/webp" multiple></label><button class="secondary" id="demo" type="button">Try with example illustrations</button><ul id="thumbnails" aria-label="Images in output order"></ul><label class="field" for="layout">Layout<select id="layout"><option value="grid">Grid</option><option value="vertical">Vertical / long image</option><option value="horizontal">Side by side</option></select></label><label class="field" for="gap">Spacing<select id="gap"><option value="0">None</option><option value="16" selected>Small</option><option value="40">Large</option></select></label><label class="field" for="background">Background<input id="background" type="color" value="#ffffff"></label><label class="field" for="format">Download as<select id="format"><option value="image/png">PNG</option><option value="image/jpeg">JPG</option></select></label><button id="download" type="button" disabled>Download combined image</button><p id="message" role="status" aria-live="polite"></p><a id="save" class="story-button" hidden>Save image</a></div><div><div class="preview-box"><canvas id="canvas" aria-label="Preview of combined photos"></canvas><div id="empty">Your photos, together.</div></div><p id="dimensions"></p><p class="fine-print">Web tool limits: 20 MB per image, 80 MB total, 40 megapixels per image; output up to 4096 pixels on its longest side. Images fit inside square cells without cropping. No automatic overlap removal. The iPhone app has its own layouts and export allowance.</p></div></div>'''
    wrapper = 'photo-tool' if d['tool'] == 'photos' else 'tool-workbench'
    return '<section class="section" id="try-it">' + heading('Try it before you download', d['tool_title'], d['tool_intro']) + f'<div class="{wrapper}">{body}</div><p><a class="text-link" href="{d["tool_link"][0]}">{E(d["tool_link"][1])} ↗</a></p></section>'


def build_guides(root, app):
    """Build the five new task guides alongside the product they explain."""
    slug = app['slug']
    guides = json.loads((root / 'scripts/product-depth-guides.json').read_text()).get(slug, [])
    if not guides:
        return
    source = json.loads((root / ('assets/sober-wins/sources.json' if slug == 'sober-wins' else 'assets/product-pages/' + slug + '/sources.json')).read_text())
    brand = 'Sober Wins' if slug == 'sober-wins' else 'Combine Photos'
    for guide in guides:
        route = '/apps/' + slug + '/guides/' + guide['slug'] + '/'
        screen = source['screens'][guide['screen']] if isinstance(guide['screen'], int) else next(s for s in source['screenshots'] if s['name'] == guide['screen'])
        schema = {'@context': 'https://schema.org', '@type': 'Article', 'headline': guide['title'], 'description': guide['summary'], 'datePublished': '2026-10-26', 'dateModified': '2026-10-26', 'mainEntityOfPage': 'https://justcompress.online' + route, 'author': {'@type': 'Organization', 'name': 'Space Sheep Studio'}, 'publisher': {'@type': 'Organization', 'name': 'Space Sheep Studio'}}
        sections = ''.join(f'<section id="part-{i}"><h2>{E(title)}</h2><p>{E(body)}</p></section>' for i,(title,body) in enumerate(guide['sections'],1))
        contents = '<nav class="article-contents" aria-label="On this page"><p>In this guide</p><ul>' + ''.join(f'<li><a href="#part-{i}">{E(title)}</a></li>' for i,(title,_) in enumerate(guide['sections'],1)) + '</ul></nav>'
        theme = ' theme-collage product-detail' if slug == 'collage-maker' else ''
        html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(guide['title'])} | Space Sheep Studio</title><meta name="description" content="{E(guide['summary'])}"><link rel="canonical" href="https://justcompress.online{route}"><meta property="og:title" content="{E(guide['title'])}"><meta property="og:description" content="{E(guide['summary'])}"><meta property="og:type" content="article"><meta property="og:url" content="https://justcompress.online{route}"><meta property="og:image" content="https://justcompress.online{screen['src']}"><link rel="stylesheet" href="/assets/product-story.css?v=20261026-wins"><link rel="stylesheet" href="/assets/product-stories.css?v=20261026"><link rel="stylesheet" href="/assets/sitewide.css?v=20261024"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('</', '<' + chr(92) + '/')}</script><script defer src="/assets/posthog-init.js?v=20261022-3"></script></head><body class="product-story site-public{theme}"><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><nav class="product-nav wrap" aria-label="Main navigation"><a class="product-brand" href="/apps/{slug}/">{brand}</a><a class="text-link" href="/apps/{slug}/#guides">All app guides ↗</a></nav></header><main id="main" class="wrap"><header class="article-head"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/apps/">Apps</a><span>/</span><a href="/apps/{slug}/">{E(app['name'])}</a></nav><h1>{E(guide['title'])}</h1><p class="lede">{E(guide['summary'])}</p><p class="article-meta">By Space Sheep Studio · October 26, 2026 · iPhone app version {E(app['version'])}</p></header><div class="article-layout"><article class="article-body">{contents}{sections}<aside class="article-note"><p>Based on the <a href="{E(app['store_url'])}">published App Store listing</a> and maintained app workflows, checked October 26, 2026. Screens show example content. See <a href="/apps/{slug}/support/">app support</a> for help with your case.</p></aside><p><a class="story-button" href="{E(app['store_url'])}">View the app on the App Store ↗</a></p></article><aside class="article-aside"><figure><img src="{screen['src']}" width="{screen['width']}" height="{screen['height']}" alt="{E(app['name'])}: actual app screen" loading="lazy"><figcaption>Actual app capture with example content. Open the product page for purchase options.</figcaption></figure></aside></div><section class="section"><div class="section-heading"><h2>Keep exploring.</h2></div><div class="guide-grid">{topic_cards(slug)}</div></section></main><footer class="story-footer wrap"><span>© 2026 Space Sheep Studio</span><div><a href="/apps/{slug}/">App overview</a><a href="/apps/{slug}/privacy/">App privacy</a><a href="/apps/{slug}/support/">Support</a><a href="/privacy/">Website privacy</a></div></footer></body></html>'''
        destination = root / route.strip('/') / 'index.html'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(html)
