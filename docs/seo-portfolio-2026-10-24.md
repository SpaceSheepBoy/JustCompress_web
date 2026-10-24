# Website portfolio refresh, 2026-10-24

The Just Compress website now describes the 11 released Apps in the curated portfolio, using their current public US App Store versions. This changes website content, not iOS binaries or App Store metadata. Two unrelated products were excluded at the owner's request. Public availability that could not be verified remains clearly qualified and excluded from the sitemap at the product landing page level.

## Maintained sources

- `scripts/app-portfolio.json`: names, versions, access limitations, features, release notes and local official screenshot assets.
- `scripts/collage-localizations.json`: verified storefront titles and source descriptions. Website translations are distinguished from official localized descriptions.
- `scripts/seo-content.json`: seven complete legacy guides at their original URLs.
- `scripts/public-copy-fixes.json`: visible FAQ and structured FAQ answers.

The portfolio builder owns the directory, product pages, support/legal indexes and localized Combine Photos pages. Existing privacy and terms bodies are preserved. The old legal generator delegates to the maintained builders rather than overwriting policies.

## Rebuild and verify

```sh
python3 scripts/enhance-tutorials.py
node scripts/generate-seo-pages.mjs
python3 scripts/refresh-public-pages.py
python3 scripts/install-posthog.py
python3 scripts/update-sitemap.py
python3 scripts/test-app-portfolio.py
python3 scripts/test-seo-content.py
node scripts/test-posthog.cjs
node --test tests/hdr-classify.test.mjs
git diff --check
```

Review the build diff. The sitemap script updates modification dates only for added or changed HTML, and excludes noindex pages. Keep original publication dates distinct from review dates. Do not promote pending builds based on approval or submission status alone. Do not restore destructive content compacting.

Validation covers 149 HTML routes, 26 inline scripts, local links/assets, metadata, schema parsing, 11 product identities, language alternatives and 142 indexable sitemap entries. Responsive browser checks cover 320, 390, 430 and 1280 px widths. The directory search and copy action were exercised; file-processing algorithms were not changed by this portfolio pass. Existing consent and HDR classifier checks pass.

Deployment success, public page readback, search indexing and App Store attribution are separate outcomes. This update does not establish new indexing or conversion performance. Keep the existing daily editorial schedule unchanged.

## Directory ordering

`scripts/app-display-order.json` holds the explicit order from the growth workspace's latest verified 30-day sales window. The order combines normalized first-download and net paid-unit volume with equal weights. It is separate from editorial article allocation. Keep raw sales counts in private growth evidence. The builder requires the ordered IDs to match the curated portfolio exactly and does not fall back to alphabetical or hard-coded featured ordering. Refresh through the growth workspace's `scripts/refresh_website_app_order.py` during the existing weekly data review, preserving the previous order on missing or stale data.
