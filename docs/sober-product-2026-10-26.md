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

Pending deployment/readback at report creation.
