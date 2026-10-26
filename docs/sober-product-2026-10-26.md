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
