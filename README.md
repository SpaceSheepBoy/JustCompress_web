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

The curated portfolio and all-page verification workflow are documented in [the portfolio maintenance notes](docs/seo-portfolio-2026-10-24.md). The current directory includes the original 11 iPhone apps and CamRecorder for Mac. Run the final public-page normalizer after content generation and analytics installation after that. The public portfolio is explicitly curated; a developer account lookup must never automatically add every App to this website.

Sober Wins lives at `/apps/sober-wins/`, with instant compatibility redirects from the seven former product/guide/legal URLs under `/apps/brew-day/`. Its hero follows the approved reference hierarchy with three unmodified raw app captures and Apple’s official App Store badge. It has a dedicated product story and three first-party guides, maintained in `scripts/sober_product.py` and `assets/product-story.css`. The portfolio builder calls it automatically. Use `python3 scripts/sober_product.py` for a targeted rebuild that preserves other Apps' custom pages. Screenshot sources, dimensions and checksums are recorded in `assets/sober-wins/sources.json`; refresh the published screenshot and copy evidence before changing its App version. See [the product-page delivery notes](docs/sober-product-2026-10-26.md).


Product-page copy must follow each App’s actual reason to use it; share layout components without copying another product’s positioning. Sober Wins leads with daily tracking, collectible rewards and the mini fridge. Keep privacy and permissions in the appropriate FAQ/legal explanations. VideoFix should explain video compatibility and color conversion; Audio Compressor should explain smaller, usable audio files; Combine Photos should explain combining images into the intended layout. Do not apply one universal headline or benefit set to the portfolio.


VideoFix, Audio Compressor and Combine Photos use the same three-screen product-page standard with independent briefs in `scripts/product-stories.json`, themes in `assets/product-stories.css`, and per-App screenshot evidence in `assets/product-pages/`. Run `python3 scripts/product_stories.py` for a targeted rebuild; the portfolio builder calls the same code. Refresh published versions, pricing/access evidence and source assets together. Existing localized Combine Photos pages and their language alternatives remain separate. See `docs/top-three-product-pages-2026-10-26.md`.

### Full product-page content and browser tryouts

The four expanded English product pages are maintained in `scripts/product_stories.py` and `scripts/sober_product.py`. Shared rendering is in `scripts/product_depth.py`; product-specific cases, choice tables, gallery captions and tool introductions live in `scripts/product-depth.json`. The five additional task guides are maintained in `scripts/product-depth-guides.json` and are rebuilt by the corresponding product builder. Run `python3 scripts/product_stories.py` and `python3 scripts/sober_product.py` for a targeted refresh. The full portfolio builder delegates to both.

`assets/product-depth.js` handles the audio estimate, video workflow guide, gallery arrows and breathing pause. `assets/combine-photos.js` is reused unchanged for the actual browser photo combiner. Run `node scripts/test-product-depth.mjs` for the calculator and video decision checks, alongside existing full-site validators. Browser-only tryouts do not synchronize app records or paid access; mathematical estimates are labeled as estimates.

### App Store screenshot quality

App Store screenshots in `app-portfolio.json` and `collage-localizations.json` must use native-resolution assets, not the Apple lookup API’s `320x480bb` thumbnails. `scripts/refresh-store-screenshots.py --receipt /absolute/path/outside-the-site/receipt.json` retrieves the same source image at Apple’s native size, verifies lossless WebP pixel identity, updates both maintained manifests and replaces existing public references and intrinsic dimensions. It never upscales a thumbnail. The portfolio validator checks actual screenshot dimensions and rejects the former low-resolution records. Icons are maintained separately.

### Mac release directory maintenance

CamRecorder's facts and native Mac screenshots live in the existing `scripts/app-portfolio.json` with `platform: macOS`. The English product, support and privacy pages remain the maintained destinations. `scripts/camrecorder_catalog.py` preserves the release card in all ten existing directory languages and explicitly labels English product links. `locales/directory-platform.json` owns only the directory introductions for this release, used for visible copy and metadata by both that renderer and `scripts/i18n_pages.py`. These local release translations are subject to the same candidate review; they are not new Weblate exports. The existing exported catalogs, approval hashes and product-fact drift gates remain intact. Do not edit generated directory prose directly or refresh old Weblate approval hashes to disguise a local copy change.

After a targeted update, run `python3 scripts/test-app-portfolio.py` and `python3 scripts/test-i18n.py`. The first checks the full curated portfolio, retaining portrait native screenshot requirements for iPhone and landscape native screenshot requirements for Mac. The second checks all original iPhone language clusters and the Mac card's download destination and labelled English fallback, without inventing translated Mac product URLs.

The portfolio builder finalizes the CamRecorder, Phone Cleaner and Sober Wins product documents with the existing public-page normalizer and analytics installer. Both support `--only` for a targeted rebuild; the installer retains its existing legal/account/billing exclusions. The full tutorial generator also runs the installer last so replacing a document cannot remove consent handling. Do not change the analytics code or consent rules as part of a product refresh. The normalizer retains the four existing Mantra Counter/TalkNice legal documents verbatim except for the missing Mantra head metadata and second-language TalkNice heading levels.

### CamRecorder screen and camera tutorial

The English guide lives at `tutorials/record-screen-and-camera-mac/index.html`. Keep its readable steps, user-selected illustrative webcam image, official English Mac App Store badges, canonical URL and existing opt-in analytics when updating. Its product-page backlink and product download badges are maintained in `scripts/build-app-portfolio.py`; keep the guide in the existing sitemap. Do not replace this web tutorial with a PDF.
