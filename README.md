# Just Compress

Free, privacy-first file compressors that run **entirely in the browser**. Files are processed on the user's own device with WebAssembly and are never uploaded.

- **Compress PDF** — `/compress-pdf/` — Ghostscript (WASM)
- **Compress Audio** — `/compress-audio/` — FFmpeg (WASM)
- **Compress Video** — `/compress-video/` — FFmpeg (WASM)

Static site, hosted on GitHub Pages. No build step.

## Open-source components

- **Ghostscript** (PDF engine) is loaded at runtime from `@jspawn/ghostscript-wasm` (AGPL-3.0). This site's source is public, satisfying AGPL's source-availability requirement.
- **FFmpeg** (audio/video engine) is loaded at runtime from `@ffmpeg/core` (WASM). The `@ffmpeg/ffmpeg` and `@ffmpeg/util` wrapper files vendored under `/vendor/` are MIT-licensed, included here so the worker loads same-origin (cross-origin module workers are blocked by browsers).

## Companion iOS apps

- [Just PDF Compressor on the App Store](https://apps.apple.com/us/app/pdf-compressor-sign-merge/id6769762323)
- [Just Audio Compressor on the App Store](https://apps.apple.com/us/app/audio-compressor-reduce-size/id6769563659)

## Optional PostHog website analytics (2026-10-22)

The self-hosted PostHog JS SDK is pinned to 1.438.15 in `assets/vendor/`. `assets/posthog-init.js` loads it only after explicit consent, respects DNT/GPC, and captures page visits, App Store clicks and DMG/ZIP download clicks. The `site` event property separates JustCompress and JustCaptions in the connected PostHog project. Session replay, autocapture, person profiles, exception capture and form capture are disabled. URLs are stripped of queries/fragments. Account, billing, activation and app-specific legal screens are excluded.

After generating or adding HTML pages, run `python3 scripts/install-posthog.py` (idempotent). The browser token is intentionally public; never put a personal API key or secret in static files. The website privacy disclosure is maintained at https://justcompress.online/privacy/#website-analytics.


## Tutorial content maintenance (2026-10-22)

Maintain `scripts/tutorial-guides.json`, `scripts/tutorial-products.json` and `scripts/tutorial-videos.json`. Product names and screenshots are verified against the public US App Store; unavailable new products have information pages with no broken download CTA. The video registry retains verified YouTube titles and the matching written guide, including localized and earlier walkthroughs.

After content changes, run:

```sh
python3 scripts/enhance-tutorials.py
python3 scripts/install-posthog.py
node scripts/test-posthog.cjs
```

Review generated pages at desktop and 390px width. Update sitemap entries only for genuinely changed or added pages. Check internal links, canonical URLs, JSON-LD, product availability and prohibited personal names before deploying. Keep deployment, search indexing and analytics ingestion evidence separate.

The current 11-App portfolio and all-page verification workflow are documented in [the portfolio maintenance notes](docs/seo-portfolio-2026-10-24.md). Run the final public-page normalizer after content generation and analytics installation after that. The public portfolio is explicitly curated; a developer account lookup must never automatically add every App to this website.

Sober Wins has a dedicated product story and three first-party guides, maintained in `scripts/sober_product.py` and `assets/product-story.css`. The portfolio builder calls it automatically. Use `python3 scripts/sober_product.py` for a targeted rebuild that preserves other Apps' custom pages. Screenshot sources, dimensions and checksums are recorded in `assets/sober-wins/sources.json`; refresh the published screenshot and copy evidence before changing its App version. See [the product-page delivery notes](docs/sober-product-2026-10-26.md).
