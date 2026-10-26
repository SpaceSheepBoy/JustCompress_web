# Sober Wins product-page sample — 2026-10-26

Scope: existing `/apps/brew-day/` product page and three new app-specific guides. The existing URL is retained to preserve inbound links and legal references. No iOS binary, App Store metadata or other product page was changed.

## Maintained implementation

- `scripts/sober_product.py` owns the English product story and all three guides; `build-app-portfolio.py` calls it for Sober Wins.
- `assets/product-story.css` holds the responsive design foundation. Keep each future product’s features, palette and copy specific to that App.
- `assets/sober-wins/sources.json` records the App Store source URLs, dimensions and SHA-256 checksums of four unmodified 900×1950 screenshots.
- The builder refuses a portfolio version that does not match the screenshot evidence. Targeted rebuild: `python3 scripts/sober_product.py`.
- Existing consent-gated PostHog integration is preserved; App Store buttons retain the normal destination URL and are eligible for existing click tracking after consent. This is not evidence of production event ingestion or installs.

## Evidence and validation

PASS: Public Apple lookup on October 26 returned Sober Wins: Quit Drinking, app ID 6811067941, version 1.2, iOS 17.0 minimum and four screenshot URLs. Published description confirms daily logs, history, collection, mini fridge, breathing, optional Health access, on-device records and free/Pro distinctions. Current local source was read to cross-check control labels; no unreleased feature was added to website claims.

PASS: Actual browser screenshots inspected at desktop 1280px and in embedded 320/390/430px viewports. Mobile hero/download controls, access cards and guide steps are readable without visible clipping in the inspected views. Desktop feature story and guide layout inspected. FAQ free-access answer expanded successfully. These checks are not a claim of testing every device/browser, assistive technology or text-size setting.

PASS: Existing `test-app-portfolio.py` (154 HTML routes, 26 inline scripts, 11 Apps, 147 sitemap URLs), `test-seo-content.py`, `test-posthog.cjs`, and `git diff --check`.

PASS: Targeted rebuild is byte-stable. A complete portfolio rebuild in a temporary directory preserves all four Sober Wins pages byte-for-byte. All new local anchor targets and screenshot checksums verified. Existing unrelated pages were restored after checking the full generator output.

PASS: Public HTML scan for the prohibited personal name. Rendered publisher and footer use Space Sheep Studio. Privacy, terms and support remain on Just Compress.

UNVERIFIED: Google indexing, ranking changes, search traffic, production analytics ingestion and App Store installation attribution. No SEO lift or installation lift is claimed; no new monitoring schedule created.

## Production

PASS: Implementation commit `24c120b5d7701915a426e006f438f06ed5b99498` pushed to the existing GitHub Pages `main` source. Pages reported `built` at 2026-10-26 13:44:57 UTC (14:44:57 Paris), without a build error.

PASS: All four product/guide pages, the shared CSS, four screenshots and sitemap were fetched over the public domain and matched the committed files byte-for-byte. Privacy, terms and support returned content with the expected heading, canonical and publisher. Existing Cloudflare email obfuscation rewrites legal-page email links, so those pages are checked semantically rather than by whole-file hashes.

PASS: Logged-out browser rendering of the live product page and app privacy page verified. The live page was opened in Codex. Screenshot: `/Users/jiali/Documents/apps/output/sober-site-2026-10-26/live-desktop.png`. The machine-readable receipt is stored beside this document.

A default Python urllib request received HTTP 403; curl and the actual browser returned the expected pages without a CAPTCHA. This client-specific discrepancy was investigated through both paths; no site access restriction was changed. Browser and curl access are observed, not proof of universal access from every client or region.


## Reference-layout correction and route migration, October 26

This revision supersedes the first sample’s single-poster hero and decision to retain the old product name in the URL. The canonical product URL is now `/apps/sober-wins/`. Three guides and privacy/terms/support use the same new prefix. The seven former URLs contain immediate HTML meta-refresh redirects plus JavaScript that preserves query strings and fragments; these are static-hosting redirects, not HTTP 301 responses. The unrelated historical wort calculator retains its existing URL.

The hero follows the user-supplied reference’s order and proportions: left-aligned two-line headline and description, blue privacy promise, outlined Learn More, privacy strip and the official black App Store badge; three actual app interfaces appear side by side on the right. Brand blue, rounded type, on-device tracking and the illustrated virtual collection are preserved. No Android badge, review score or user count is invented.

The screen files are unmodified raw captures used to compose the published English 1.2 store screenshots, copied from `SoberWins/design/sobriety/app-store-localized/raw/en-US/`. They show daily tracking, Collection and the mini fridge. They are app-screen images, without added hardware shells or camera holes. `assets/sober-wins/sources.json` records source paths and hashes. The official badge was fetched unchanged from `https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg`; Apple’s current marketing guidance was reviewed.

PASS: desktop reference comparison and 320/390/430px responsive browser checks. All three app screens remain side by side on mobile; the real layouts were inspected at the screen row as well as at the hero text/badge. The image aspect ratios are preserved. All three screens and the badge loaded successfully.

PASS: an actual browser navigation to the old product route with `?from=old-link#faq` arrived at `/apps/sober-wins/?from=old-link#faq`; canonical points to the new clean URL.

PASS: existing public-surface, SEO-content and consent tests. Public-surface checks now verify that compatibility pages have valid final destinations, no redirect chains and no sitemap entries. The full portfolio builder preserves the new story and all seven aliases. Public pages were scanned for the prohibited personal name.

Production receipt for this correction is recorded after deployment. Earlier receipts above describe the superseded first sample.
