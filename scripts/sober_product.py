"""Maintained Sober Wins story and first-party guides, based on the published 1.2 listing.

Called by build-app-portfolio.py so a portfolio refresh preserves this product page.
Screenshots are unmodified public App Store assets; provenance lives beside them.
"""
from html import escape as E
import json

SITE = 'https://justcompress.online'
BASE = '/apps/sober-wins/'
LEGACY = '/apps/brew-day/'
DATE = '2026-10-26'

GUIDES = [
    {
        'slug': 'track-alcohol-free-days',
        'title': 'How to track alcohol-free days on iPhone',
        'summary': 'Make a daily entry, revisit your history, and keep your record on your own device with Sober Wins.',
        'image': 'track',
        'sections': [
            ('Start with one honest entry', '''<p>You do not need a long journal entry to keep a useful daily record. Sober Wins gives you two choices: <strong>No alcohol</strong> and <strong>Had a drink</strong>. Log what happened, then use your history to see the days together.</p><p>The tracker is free to use and does not require an app account. Your daily records stay on your iPhone.</p>'''),
            ('Log and review your days', '''<ol><li><strong>Open Sober Wins.</strong> Find the daily choices on the home screen.</li><li><strong>Choose the answer for today.</strong> Tap No alcohol or Had a drink. The entry records your day; virtual collection rewards are a separate part of the app.</li><li><strong>Open History.</strong> Use the history control near the app title to review your recorded days. If an entry is wrong, use the available correction controls in History.</li><li><strong>Return the next day.</strong> Keep each entry accurate rather than trying to make every day look the same.</li></ol>'''),
            ('What if I record a drinking day?', '''<p>Record it as a drinking day. Sober Wins keeps a history as well as the current alcohol-free period, so an earlier entry still has a place in your record. A counter is one view of your progress; the history gives it context.</p><p>A missed entry and a confirmed alcohol-free day are different things. Review the actual daily entries before interpreting a number or a weekly pattern.</p>'''),
            ('Keep your record and your purchase separate', '''<p>Sober Wins has no app account or developer cloud sync. Removing the app can remove local records. Device backups depend on your Apple settings, so keep any important exports before changing or removing the app.</p><p>Restore Purchases restores eligible Pro access through Apple. It does not recover deleted tracking history or cabinet arrangements. See the <a href="/apps/sober-wins/privacy/">app privacy policy</a> for storage and sharing details.</p>'''),
        ],
    },
    {
        'slug': 'daily-rewards-and-collection',
        'title': 'How daily rewards work in Sober Wins',
        'summary': 'Turn daily check-ins into a virtual collection, then arrange your finds in the mini fridge.',
        'image': 'cabinet',
        'sections': [
            ('A small reason to come back', '''<p>Sober Wins pairs a daily alcohol log with virtual collectibles. The collection adds something visual to a routine that otherwise consists of dates and numbers. It is optional: you can use the tracker without arranging a cabinet.</p><p>The collectibles are illustrated beer items. Consider whether that theme suits you before choosing the app; it will not suit everyone looking for an alcohol-free tracker.</p>'''),
            ('From a daily entry to your collection', '''<ol><li><strong>Log your day.</strong> On the home screen, choose No alcohol or Had a drink. Record the true answer; collection points are not a reason to change your log.</li><li><strong>Check reward progress.</strong> The home screen shows progress toward the next collectible.</li><li><strong>Open Collection.</strong> Review your unlocked items and new finds when available.</li><li><strong>Arrange your mini fridge.</strong> Use the cabinet controls to place your collected items and revisit your arrangement.</li></ol>'''),
            ('What is free, and what does Pro add?', '''<p>Basic tracking, history, collectibles, the mini fridge and basic poster sharing are free. Pro adds premium nine-position cabinets, poster export and a 4× daily collection boost.</p><p>Lifetime is a one-time purchase. Existing active Monthly subscriptions also provide Pro while valid. Buying Lifetime does not cancel an existing subscription; manage that separately in your Apple Account. Check the current local offer in the app before buying.</p>'''),
            ('What the rewards mean', '''<p>These are virtual collection items. They have no cash value and cannot be redeemed for alcohol. A cabinet is not a medical measure or proof of recovery.</p><p>Your collection and arrangement are stored on your device. Restoring a purchase restores eligible paid access, not deleted collectibles or local records. For purchase help, use the <a href="/apps/sober-wins/support/">Sober Wins support page</a>.</p>'''),
        ],
    },
    {
        'slug': 'breathing-pause',
        'title': 'How to take a breathing pause in Sober Wins',
        'summary': 'Find the breathing exercise, use it without the camera, and understand what stays on your iPhone.',
        'image': 'breathe',
        'sections': [
            ('Make room for a short pause', '''<p>Sober Wins includes a breathing pause alongside daily tracking and collection features. It gives you an activity to open when you want to step away from the log and focus on the present moment.</p><p>You can use the breathing exercise without connecting Apple HealthKit or turning on the camera.</p>'''),
            ('Open the breathing exercise', '''<ol><li><strong>Open Sober Wins.</strong> Find the Panic button on the home screen.</li><li><strong>Choose Breathing.</strong> Follow the breathing guidance at a pace that feels comfortable.</li><li><strong>Keep the camera optional.</strong> If a mirror option appears, you can decline camera access and continue using breathing without it.</li><li><strong>Return when you are ready.</strong> Go back to your daily log or close the app. You do not need to share the exercise or your records.</li></ol>'''),
            ('What happens if I enable the mirror?', '''<p>The optional mirror uses the front camera for a live view. According to the app’s privacy policy, Sober Wins does not take photos, record video or audio, analyze faces, or upload camera images.</p><p>Only enable the mirror if you want it. You can manage camera permission in iPhone Settings. See the <a href="/apps/sober-wins/privacy/">privacy policy</a> for the full permission explanation.</p>'''),
            ('A pause has limits', '''<p>The in-app Panic button opens activities; it does not contact emergency services or provide medical care. A breathing exercise is not a treatment for alcohol withdrawal or a substitute for professional support.</p><p>If your situation needs urgent help, contact local emergency services. Use the app as a tracking and reflection tool within the support that is right for you.</p>'''),
        ],
    },
]


def ld(data):
    return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', **data}, ensure_ascii=False).replace('</', '<\\/') + '</script>'


def shot(name, alt, eager=False):
    return f'<img src="/assets/sober-wins/{name}.jpg" width="900" height="1950" alt="{E(alt)}" ' + ('fetchpriority="high"' if eager else 'loading="lazy"') + ' decoding="async">'


def cta(app, text='Download on the App Store', secondary=False):
    return f'<a class="story-button{" secondary" if secondary else ""}" href="{E(app["store_url"])}">{E(text)}</a>'


def document(root, route, title, description, body, app, schema='', social='track'):
    url = SITE + route
    icon = app['icon']['src']
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title) if title.startswith('Sober Wins') else E(title)+' | Sober Wins'}</title><meta name="description" content="{E(description)}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/sober-wins/{social}.jpg"><meta property="og:image:alt" content="Sober Wins official App Store screenshot"><meta name="twitter:card" content="summary_large_image">
<meta name="apple-itunes-app" content="app-id={app['id']}"><link rel="icon" href="{icon}" type="image/jpeg"><link rel="stylesheet" href="/assets/product-story.css?v=20261026-trio"><link rel="stylesheet" href="/assets/sitewide.css?v=20261024">{schema}
<script defer src="/assets/posthog-init.js?v=20261022-3"></script></head>
<body class="product-story site-public"><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><nav class="product-nav wrap" aria-label="Main navigation"><a class="product-brand" href="{BASE}"><img src="{icon}" width="512" height="512" alt="Sober Wins: Quit Drinking icon">Sober Wins</a><div class="nav-links"><a class="desktop-link" href="{BASE}#features">Features</a><a class="mobile-hide" href="{BASE}#guides">Guides</a><a class="desktop-link" href="{BASE}#faq">FAQ</a><a class="desktop-link" href="/apps/">All apps ↗</a><a class="story-button" href="{E(app['store_url'])}">Get the app ↗</a></div></nav></header>
<main id="main" class="wrap">{body}</main><footer class="story-footer wrap"><span>© 2026 Space Sheep Studio</span><div><a href="/">Just Compress</a><a href="/apps/">All apps</a><a href="{BASE}privacy/">App privacy</a><a href="{BASE}terms/">Terms</a><a href="{BASE}support/">Support</a><a href="/privacy/">Website privacy</a></div></footer></body></html>'''
    p = root / route.strip('/') / 'index.html'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html)


def guide_cards(exclude=None):
    return '<div class="guide-grid">' + ''.join(f'<article class="guide-card"><p class="guide-type">SOBER WINS GUIDE · 0{i+1}</p><h3><a href="{BASE}guides/{g["slug"]}/">{E(g["title"])}</a></h3><p>{E(g["summary"])}</p><a class="text-link" href="{BASE}guides/{g["slug"]}/">Read the guide <span aria-hidden="true">↗</span></a></article>' for i, g in enumerate(GUIDES) if g["slug"] != exclude) + '</div>'


def closing(app):
    return f'<aside class="closing"><h2>A little check-in.<br>A record that is yours.</h2><p>Start with the free tracker, then make the daily routine your own.</p>{cta(app)}<p class="fine-print">iPhone · iOS {E(app["minimum_os"])} or later · Optional Pro purchases</p></aside>'


def build(root, app):
    snapshot = json.loads((root / "assets/sober-wins/sources.json").read_text())
    if snapshot["version"] != app["version"]:
        raise ValueError("Refresh Sober Wins published screenshots and copy before changing the product version")
    faq = [
        ('Is Sober Wins free?', 'Basic tracking, history, collectibles, the mini fridge and basic poster sharing are free. Pro adds premium nine-position cabinets, poster export and a 4× daily collection boost. Apple shows the current local offer before purchase.'),
        ('Do I need an account?', 'No app account is required. Tracking records and cabinet arrangements stay on your iPhone. There is no developer cloud sync. Apple device backups depend on your settings; restoring a purchase does not restore deleted history.'),
        ('What if I have a drink or make a mistake?', 'Record what happened and continue using your history. Use the correction controls in History for an incorrect daily entry. Your record includes more than your current alcohol-free period.'),
        ('Do I have to connect Apple HealthKit?', 'No. Sleep and resting-heart-rate trends are optional and require your permission. You can use tracking and collection without them. Health trends are not medical advice or proof that a change was caused by alcohol.'),
        ('What are the collectibles?', 'They are virtual, illustrated beer items that you can collect and arrange. They have no cash value and cannot be redeemed for alcohol. This visual theme may not suit everyone; check the screenshots before choosing the app.'),
        ('Does the Panic button call for help?', 'No. It opens in-app pause activities, including breathing. It does not contact emergency services. The optional camera mirror is not required for breathing. Sober Wins does not provide treatment for alcohol withdrawal.'),
        ('Is Lifetime a subscription?', 'Lifetime is a one-time Pro purchase. Existing active Monthly subscriptions also provide Pro while valid. Lifetime does not cancel a Monthly subscription; manage any subscription separately in your Apple Account.'),
    ]
    body = f'''<header class="hero"><div class="hero-copy"><h1>Track Your Sober<br>Days Privately</h1><p class="lede">A private alcohol-free day tracker with daily check-ins, virtual collectibles, a mini fridge, and a breathing pause. Made for iPhone.</p><p class="hero-promise">No account. No cloud sync. Your progress, your privacy.</p><a class="learn-more" href="#features">Learn More</a><div class="hero-privacy"><span class="privacy-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M12 3 4.5 6v5.5c0 4.2 3.2 7.2 7.5 9.5 4.3-2.3 7.5-5.3 7.5-9.5V6L12 3Z"/><path d="m8.5 11.5 2.5 2.5 4.5-5"/></svg>Privacy-first</span><span>Your tracking data stays on your iPhone</span></div><div class="hero-download"><a class="app-store-badge" href="{E(app['store_url'])}" aria-label="Download Sober Wins on the App Store"><img src="/assets/sober-wins/download-on-the-app-store.svg" width="150" height="50" alt="Download on the App Store"></a><p>Free daily tracking · Optional Pro features</p></div></div><figure class="hero-screens" id="app-screens" aria-label="Three real Sober Wins app screens">{''.join('<img src="'+screen['src']+'" width="'+str(screen['width'])+'" height="'+str(screen['height'])+'" alt="Sober Wins: '+label+'" decoding="async"'+(' fetchpriority="high"' if i==0 else '')+'>' for i,(screen,label) in enumerate(zip(snapshot['hero_screens'], ['daily tracking and alcohol-free days','daily rewards and virtual collection','mini fridge and illustrated collectibles'])))}<figcaption class="visually-hidden">Daily tracking, Collection and the mini fridge, captured in the published iPhone app.</figcaption></figure></header>
<section class="section" id="features"><div class="section-heading"><p class="eyebrow">Small actions, visible progress</p><h2>More than a number<br>on a screen.</h2><p>Keep a record of your days, collect something along the way, and make space for a pause.</p></div><div class="benefits"><article class="benefit"><span class="symbol" aria-hidden="true">☀️</span><h3>Check in with yourself</h3><p>Log an alcohol-free day or a drinking day. Return to your history to see the record over time.</p></article><article class="benefit"><span class="symbol" aria-hidden="true">🎁</span><h3>Build your collection</h3><p>Daily logs earn progress toward virtual collectibles. Give your finds a home in the mini fridge.</p></article><article class="benefit"><span class="symbol" aria-hidden="true">🌿</span><h3>Take a breathing pause</h3><p>Open an in-app breathing exercise when you want a moment away from the daily routine.</p></article></div></section>
<section class="section" id="how-it-works"><div class="section-heading"><p class="eyebrow">Your daily routine</p><h2>One day. One honest check-in.</h2></div><div class="steps"><article class="step"><span class="step-number">01 / RECORD</span><h3>Log today</h3><p>Choose No alcohol or Had a drink. A useful record starts with what actually happened.</p></article><article class="step"><span class="step-number">02 / COLLECT</span><h3>See what is next</h3><p>Check reward progress, discover your virtual finds and arrange your mini fridge.</p></article><article class="step"><span class="step-number">03 / REFLECT</span><h3>Look back, keep going</h3><p>Review your history. Use a breathing pause when you want to take a moment for yourself.</p></article></div></section>
<section class="section" aria-labelledby="inside-title"><div class="section-heading"><p class="eyebrow">Inside the app</p><h2 id="inside-title">Make the routine your own.</h2><p>These are unmodified screenshots from the current App Store listing.</p></div><div class="feature-story"><figure class="feature-media">{shot('rewards', 'Sober Wins official App Store screenshot showing virtual collection rewards')}</figure><div class="feature-copy"><p class="eyebrow">A daily discovery</p><h3>Give small check-ins<br>something to grow.</h3><p>Earn virtual collectibles through daily logs, then revisit your finds in Collection. Basic collectibles and the mini fridge are included for free.</p><a class="text-link" href="{BASE}guides/daily-rewards-and-collection/">How daily rewards work ↗</a></div></div><div class="feature-story"><figure class="feature-media">{shot('cabinet', 'Sober Wins official App Store screenshot showing a cabinet of virtual collectibles')}</figure><div class="feature-copy"><p class="eyebrow">Your collection, your arrangement</p><h3>A little shelf<br>of your own.</h3><p>Arrange the illustrated items in your mini fridge. Pro adds premium nine-position cabinets when you want more room to display your collection.</p><p class="fine-print">Collectibles depict beer items. They are virtual, have no cash value and cannot be redeemed for alcohol.</p></div></div><div class="feature-story"><figure class="feature-media">{shot('breathe', 'Sober Wins official App Store screenshot showing the breathing pause feature')}</figure><div class="feature-copy"><p class="eyebrow">A moment for yourself</p><h3>Pause.<br>Then choose your next step.</h3><p>Open breathing from the Panic button. Follow the exercise without sharing your records or enabling the optional camera mirror.</p><a class="text-link" href="{BASE}guides/breathing-pause/">Find the breathing pause ↗</a><p class="fine-print">The button opens activities. It does not contact emergency services or provide medical treatment.</p></div></div></section>
<section class="section" id="privacy"><div class="privacy-block"><div><p class="eyebrow">Personal progress, local records</p><h2>Your record stays<br>on your iPhone.</h2><p>No app account. No developer cloud sync. You choose whether to connect Apple HealthKit or share a poster.</p><a class="text-link" href="{BASE}privacy/">Read the app privacy policy ↗</a></div><ul><li><strong>On-device tracking</strong>Daily entries, collection and arrangements are stored locally.</li><li><strong>Optional Apple HealthKit</strong>View sleep and resting heart rate with permission. Trends are not medical advice or proof of cause.</li><li><strong>Sharing is your choice</strong>Export only when you want to. Device backups depend on your Apple settings.</li></ul></div></section>
<section class="section" id="access"><div class="section-heading"><p class="eyebrow">Start with the essentials</p><h2>Track for free.<br>Choose Pro when it fits.</h2></div><div class="access-grid"><article class="access-card"><span class="pill">FREE</span><h3>Your daily essentials</h3><ul><li>Basic tracking and history</li><li>Virtual collectibles and mini fridge</li><li>Breathing pause</li><li>Basic poster sharing</li></ul></article><article class="access-card"><span class="pill">OPTIONAL PRO</span><h3>More ways to collect</h3><ul><li>Premium nine-position cabinets</li><li>Poster export</li><li>4× daily collection boost</li></ul><p class="fine-print">Lifetime is a one-time purchase. See the current local offer in the app.</p></article></div><p class="fine-print">Existing active Monthly subscriptions remain Pro while valid. Lifetime does not cancel them; manage subscriptions in your Apple Account. Restore Purchases restores eligible Pro access, not deleted history or arrangements.</p></section>
<section class="section" id="guides"><div class="section-heading"><p class="eyebrow">Practical guides</p><h2>A clear next step.</h2><p>Learn the actual app workflow before you start.</p></div>{guide_cards()}</section>
<section class="section" id="faq"><div class="section-heading"><p class="eyebrow">Before you begin</p><h2>A few useful answers.</h2></div><div class="faq">{''.join('<details><summary>'+E(q)+'</summary><p>'+E(a)+'</p></details>' for q,a in faq)}</div><p class="fine-print">Published iPhone version {E(app['version'])} · iOS {E(app['minimum_os'])} or later · US App Store checked {DATE}. The app supports 13 languages. This product page is in English.</p></section>{closing(app)}'''
    schema = ld({'@type': 'SoftwareApplication', 'name': app['name'], 'url': SITE + BASE, 'downloadUrl': app['store_url'], 'softwareVersion': app['version'], 'operatingSystem': 'iOS ' + app['minimum_os'] + ' or later', 'applicationCategory': 'LifestyleApplication', 'description': 'Track alcohol-free days, review history, earn virtual collectibles and take a breathing pause on iPhone.', 'image': SITE + app['icon']['src'], 'screenshot': [SITE + '/assets/sober-wins/' + name + '.jpg' for name in ['track', 'rewards', 'cabinet', 'breathe']], 'publisher': {'@type': 'Organization', 'name': 'Space Sheep Studio'}})
    schema += ld({'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Apps', 'item': SITE + '/apps/'}, {'@type': 'ListItem', 'position': 2, 'name': app['name'], 'item': SITE + BASE}]})
    document(root, BASE, 'Sober Wins: Quit Drinking for iPhone', 'Track alcohol-free days on iPhone with Sober Wins. Free daily logs, history, virtual collectibles and breathing pauses. No app account required.', body, app, schema)
    for guide in GUIDES:
        route = BASE + 'guides/' + guide['slug'] + '/'
        contents = '<nav class="article-contents" aria-label="On this page"><p>In this guide</p><ul>' + ''.join(f'<li><a href="#step-{i}">{E(title)}</a></li>' for i,(title,_) in enumerate(guide['sections'],1)) + '</ul></nav>'
        sections = ''.join(f'<section id="step-{i}"><h2>{E(title)}</h2>{html}</section>' for i,(title,html) in enumerate(guide['sections'],1))
        body = f'''<header class="article-head"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/apps/">Apps</a><span aria-hidden="true">/</span><a href="{BASE}">Sober Wins</a><span aria-hidden="true">/</span><span>Guide</span></nav><h1>{E(guide['title'])}</h1><p class="lede">{E(guide['summary'])}</p><p class="article-meta">By Space Sheep Studio · Published October 26, 2026 · Sober Wins {E(app['version'])}</p></header><div class="article-layout"><article class="article-body">{contents}{sections}<aside class="article-note"><p>Based on the published <a href="{E(app['store_url'])}">Sober Wins App Store listing</a> and the maintained <a href="{BASE}privacy/">app privacy policy</a>. Button wording can vary with the app language.</p></aside></article><aside class="article-aside"><figure>{shot(guide['image'], 'Sober Wins official App Store screenshot: '+guide['title'])}<figcaption>Official App Store screenshot. Shown without alteration.</figcaption></figure></aside></div><section class="section" id="guides"><div class="section-heading"><p class="eyebrow">Keep exploring</p><h2>More Sober Wins guides.</h2></div>{guide_cards(guide["slug"])}</section>{closing(app)}'''
        schema = ld({'@type': 'Article', 'headline': guide['title'], 'description': guide['summary'], 'datePublished': DATE, 'dateModified': DATE, 'mainEntityOfPage': SITE + route, 'image': SITE + '/assets/sober-wins/' + guide['image'] + '.jpg', 'author': {'@type': 'Organization', 'name': 'Space Sheep Studio', 'url': SITE + BASE}, 'publisher': {'@type': 'Organization', 'name': 'Space Sheep Studio'}})
        schema += ld({'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Apps', 'item': SITE + '/apps/'}, {'@type': 'ListItem', 'position': 2, 'name': 'Sober Wins', 'item': SITE + BASE}, {'@type': 'ListItem', 'position': 3, 'name': guide['title'], 'item': SITE + route}]})
        document(root, route, guide['title'], guide['summary'], body, app, schema, guide['image'])
    redirects(root)
    print('Built Sober Wins product story and 3 practical guides')


def redirects(root):
    paths = ['', 'privacy/', 'terms/', 'support/'] + ['guides/' + g['slug'] + '/' for g in GUIDES]
    for suffix in paths:
        target = BASE + suffix
        path = root / (LEGACY + suffix).strip('/') / 'index.html'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sober Wins: new website address</title><meta name="description" content="Sober Wins has a new website address. Continue to the current product, guide or support page."><link rel="canonical" href="{SITE}{target}"><meta http-equiv="refresh" content="0;url={target}"><script>location.replace({json.dumps(target)}+location.search+location.hash);</script></head><body data-site-redirect="{target}"><main><h1>Sober Wins has moved</h1><p><a href="{target}">Continue to Sober Wins</a></p><p>Space Sheep Studio</p></main></body></html>''')


if __name__ == '__main__':
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    app = next(a for a in json.loads((root / 'scripts/app-portfolio.json').read_text())['apps'] if a['id'] == '6811067941')
    build(root, app)
