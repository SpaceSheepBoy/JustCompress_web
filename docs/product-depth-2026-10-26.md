# Four product pages: full-page content expansion

## Baseline and authorized action

The user asked to close the content gap with the full sober-tracker.com homepage while preserving each app’s own positioning. Baseline deployment: `4f33253dfedac2f24b6b0389ecd9d585479437b8`. This pass changes the four English product pages and adds five task guides. It does not change native app binaries, purchases, store metadata or legal-policy bodies.

Counts below use the same BeautifulSoup text extraction and whitespace word count before and after, including collapsed FAQ answers, navigation and footers. These are content measurements, not ranking or quality scores.

| Page | Words before → after | FAQ before → after | Guide cards before → after | Gallery screens |
|---|---:|---:|---:|---:|
| VideoFix | 850 → 2044 | 6 → 16 | 3 → 6 | 3 |
| Audio Compressor | 777 → 1894 | 6 → 16 | 3 → 6 | 4 |
| Combine Photos | 750 → 1938 | 6 → 16 | 3 → 6 | 3 |
| Sober Wins | 1038 → 2237 | 7 → 16 | 3 → 6 | 7 |

## Changes

Every page has a jump navigation, real-image gallery with native horizontal scrolling and progressive arrow controls, three task-specific examples, a task-choice comparison, studio context and official source/support links. Existing three-screen heroes, official App Store badges, app palettes and purchase disclosures remain.

- VideoFix: source/destination workflow guide. It distinguishes HDR and Log sources, codec compatibility, a steady frame rate and AAC audio extraction. It recommends keeping a source that already meets the requirement. The existing matching Log/SDR conversion frames remain labeled as supplied conversion evidence.
- Audio Compressor: duration/bitrate/attachment-limit calculator. Uses decimal MB, calculates constant-bitrate audio payload and a theoretical bitrate ceiling. It labels metadata/encoder uncertainty, does not inspect a recording and does not promise delivery or sound quality.
- Combine Photos: actual existing browser combiner embedded directly by reusing its unchanged script and example SVG illustrations. Three basic layouts, up to twelve images; explicitly distinguished from the app’s eleven layouts and two-to-thirty-image workflow. No image upload was added.
- Sober Wins: standalone six-round, four-seconds-in/six-seconds-out breathing pause. It stops manually, at sixty seconds and when the page is hidden. No account, health record, saved log, reward, camera or app connection is involved. Reduced motion removes scaling animation. The positioning stays daily logs, collectibles and the mini fridge.

Five new maintained task guides: Combine Photos screenshot composition and JPEG/PNG choice; Sober Wins history review, poster sharing and choosing a daily routine. All five are linked from product pages and included in the sitemap.

No testimonials, ratings totals, founder recovery story or medical-outcome claims were invented. Official App Store listings are linked for current reviews and offers.

## Maintenance and sources

Product-specific briefs: `scripts/product-depth.json`; additional guides: `scripts/product-depth-guides.json`; shared rendering: `scripts/product_depth.py`. Existing `product_stories.py` and `sober_product.py` call the new renderer, so the complete portfolio builder preserves the content. Browser behavior is in `assets/product-depth.js`; style in `assets/product-depth.css`.

Screenshot identities, dimensions and provenance remain in the existing product and Sober Wins source manifests. Published app versions checked October 26: VideoFix 1.0.6, Audio Compressor 1.1.8, Combine Photos 1.4 and Sober Wins 1.2. Existing source capture limitations remain; these are website changes, not new device tests.

## Verification

PASS: full staged-candidate link/metadata/schema/script validator (166 HTML routes, 11 apps and 152 sitemap URLs), existing complete-content regressions, PostHog consent/privacy regressions, numerical calculator tests and all sixteen source/destination video combinations. Unrelated working-tree asset deletions are excluded; the publication candidate retains those committed files.

PASS: byte-identical dedicated pages after a full portfolio rebuild in a temporary checkout. Public normalization preserves all four tryouts, galleries, sixteen FAQ entries and six guide cards.

PASS: actual desktop browser checks of all four tryouts. Ten minutes at 64 kbps produces 4.8 MB. An already-working SDR source does not require SDR color conversion. The embedded photo combiner generated and triggered download of a three-image horizontal PNG (1864×632, 53 KB in the inspected run). The breathing timer ran to its one-minute completion state, and a restarted exercise stopped manually.

PASS: embedded 320/390 CSS-pixel viewport visual checks for all four tool layouts, photo/Sober gallery navigation, responsive choice cards and the two new-guide templates. FAQ expansion was observed. This is not a physical iPhone, all-browser or enlarged-text certification.

UNVERIFIED: search clicks/impressions/rankings, installs, website-to-app conversion lift, production analytics ingestion and Core Web Vitals. No effect is claimed from immediate publication. The deployment receipt records the actual live start; use the existing analytics workflow to compare equivalent complete 28-day windows before/after that start, then prioritize by observed queries and download clicks. Do not infer improvement solely from added words or small samples.

Local content baseline, browser captures and the final remote readback receipt are stored in the task’s external output evidence directory. These retain the commit identity, exact verified files and live-start timestamp without introducing a new automation.

## Catalog interaction and content cleanup follow-up

The user requested clickable catalog screenshots to open the corresponding App Store listing, the identity row to open the product webpage, and official App Store badges in place of the text buttons. Applied consistently to all eleven catalog Apps; copy-name controls remain. Removed the internal “Check the source” panel from all four expanded product pages and its maintained renderer; the short studio introduction remains, with support/legal links in the existing footer. Screenshot enlargement links inside individual product pages are unchanged.
