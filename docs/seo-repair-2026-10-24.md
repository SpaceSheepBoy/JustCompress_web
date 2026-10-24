# SEO repair, 2026-10-24

This repairs existing pages. It does not add an extra daily article or change public URLs.

- Rewrote the PDF email and WhatsApp guides with complete practical answers, explanatory diagrams, honest limits, official sources and verified App Store identities.
- Restored complete body sections and FAQ answers to twelve existing privacy articles. Kept their index and URLs, removed synthetic index view counts, corrected PDF watermark and native-app access claims, and put relevant App CTAs after the explanation.
- Removed destructive article truncation and summary replacement from the compacting script. The legacy visual wrapper now preserves full answers and defaults to open.
- Preserved sitemap entries and existing dates during blog regeneration. Modification dates change only for genuinely revised pages.
- Added descriptions to six existing product/legal pages and canonicals to the two PhotoFix pages. Metadata is maintained by repair-seo-metadata.py and called from the relevant generators.
- Fixed narrow PhotoFix navigation and long guide layout wrapping. No account, billing, iOS binary or App Store metadata was changed.

Build the affected existing guides:

```sh
node scripts/generate-seo-pages.mjs
node scripts/generate-privacy-blog.mjs --articles-only
python3 scripts/repair-seo-metadata.py
python3 scripts/install-posthog.py
python3 scripts/test-seo-content.py
node scripts/test-posthog.cjs
```

The documented full enhance-tutorials.py workflow remains available; it includes metadata repair. Review its diff to avoid publishing unrelated legacy formatting changes. Keep article diagrams, captions and source data. The compacting script must never delete maintained sections, steps or FAQ answers. The new regression checks cover that failure.

Independent verification found GSC and PostHog available through the existing personal Chrome session. GSC's 28-day official export for September 25 through October 22 contains 8 impressions and 2 clicks, all to the homepage. This is a baseline, not an effect of this repair. PostHog Activity shows website Pageview ingestion. Installation and purchase attribution, and unattended GSC API access, are not established by these observations.

Production deployment and final public readback are recorded in the growth workspace repair receipt. A push alone is not publication. Neither deployment nor sitemap submission guarantees Google indexing.
