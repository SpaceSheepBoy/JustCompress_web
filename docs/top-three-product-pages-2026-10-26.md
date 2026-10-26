# Three leading App product pages — October 26, 2026

## Selection and scope

Read-only official Apple sales reports in the growth workspace identify VideoFix, Audio Compressor and Combine Photos as the top three by net paid units over September 25–October 24 (30 complete days). Net units include reported renewals and refunds, not unique purchasers. Private amounts and download counts were kept outside this public repository. This selection is not website attribution.

Updated existing English product URLs only: `/apps/videofix/`, `/apps/audio-compressor/`, `/apps/collage-maker/`. No app binary, App Store metadata, purchase configuration, automation or legal-policy body was changed. The public catalog adopts current icons and store screenshots for these three Apps. Existing localized product URLs and hreflang links are retained.

## Distinct product positioning

- VideoFix: “HDR to SDR. Ready to Share.” Purple/green palette, compatible video copies, color conversion, batch processing and frame-rate choices. A large matching Apple ProRes Log/Rec.709 SDR comparison is supplied conversion evidence, not an independent new conversion test or a claim that Log equals HDR.
- Audio Compressor: “Trim. Split. Convert Audio.” Yellow/navy palette, recordings to useful clips and files, plus compression. One successful export is included; recording/playback remain free. This allowance is supported by the published 1.1.8 release review notes, not inferred solely from the download price.
- Combine Photos: “Your Photos. One Image.” Coral/cream/green palette and serif titles matching its app. Two to thirty images, eleven layouts, JPEG/PNG exports and one included free export.

Shared presentation: two-column hero, three real app interfaces, official black App Store badge, feature explanations, workflow, purchase disclosures, useful existing guides, FAQ and download CTA. Positioning is configured independently rather than replacing only the product name. Privacy is not promoted as a universal hero benefit.

## Current production sources

Public US Apple lookup on October 26 returned VideoFix 1.0.6, Audio Compressor 1.1.8 and Combine Photos 1.4, each released October 24. `scripts/app-portfolio.json` records the refreshed snapshots. The native source screenshot sets used in current store artwork provide the hero images. Example media/settings and possible storefront price differences are identified on the pages.

`assets/product-pages/<slug>/sources.json` records original file paths, dimensions and SHA-256 checksums. WebP encoding was lossless: decoded RGB pixels and dimensions were compared with the source before publication. VideoFix comparison frames are from the same supplied original and supplied conversion at 2.000 seconds, with no creative color adjustment. The app-screen captures have no added device shells or camera holes. The official badge is copied unchanged from the previously verified Apple asset into `assets/brand/`.

## Maintenance

`scripts/product_stories.py` renders these three pages from `scripts/product-stories.json`; `build-app-portfolio.py` delegates by stable Apple App ID. A changed published version requires refreshed matching screenshot evidence. `assets/product-story.css` provides the existing shared rhythm and `assets/product-stories.css` provides App-specific palettes/type. Per-page Privacy choices placement avoids overlapping the primary App Store badge, preserving the consent mechanism.

## Verification

PASS: actual browser desktop review of all three heroes and the VideoFix comparison, plus embedded 320/390/430 CSS-pixel viewport reviews of the three mobile heroes. Two-line headlines fit, badges and short navigation controls are readable, and screen aspect ratios are preserved in inspected views. Further mobile screen-row/comparison checks are recorded in the local evidence bundle. This is not a real-iPhone, every-browser, RTL or enlarged-text test.

PASS: targeted generation and a complete portfolio build in a temporary copy preserve the dedicated product HTML. The public normalizer preserves the three screens, badge, canonical identity and independent positioning.

Full-site validation runs against the staged publication candidate. Unrelated working-tree image deletions are intentionally excluded from this commit and remain local. The candidate retains previously committed assets.

PASS: staged candidate full-site checks: 161 routes, 33 inline scripts, 11 Apps and 147 sitemap URLs; SEO-content validator; PostHog consent regressions; source asset checksums; byte-stable targeted generation; staged whitespace checks. Public-page changes were checked for the prohibited personal name before publishing.

UNVERIFIED: search indexing, rankings, conversion lift, production analytics ingestion, installation attribution and Core Web Vitals. No performance or revenue lift is claimed.

Production deployment/readback receipt is saved after publishing.
