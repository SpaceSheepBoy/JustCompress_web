# Weblate-managed articles

The website's `locales/config.json` remains the authority for public locale codes,
Weblate codes, store regions and official Apple badges. Article components live in
the same local `justcompress` Weblate project and use its technical glossary.

The first enrolled article is `pdf-email`, at the unchanged English route
`/compress-pdf-for-email/` and the French route `/compress-pdf-for-email/fr/`.
This is a complete French article, not an automatic browser translation.

## Authoring and enrollment

The maintained English content is in `scripts/seo-content.json`. The enrolled
record uses objects with persistent `id` values for cards, sections, questions,
steps and source/related links. Edit text inside these objects. Reorder the objects
together with their IDs. Never derive a replacement ID from a new heading or array
position. Add a fresh ID for a genuinely new semantic unit and do not reuse deleted
IDs for unrelated content. Existing non-enrolled records retain their old format.

Register each future article in `config.json` using its unique `id`, original
`slug`, Weblate component and actually reviewed target `locales`. New articles can
be enrolled with no target locales while still publishing English. Supply the
article-specific diagram text in `i18n.diagram`, section/jump/action labels in
`i18n.ui`, and an accurate `primaryCtaLabel`. Do not reuse the PDF pilot's labels
for a different topic. This adapter currently handles the structured legacy-guide
format. Older tutorial data, custom HTML layouts and the other website need an
explicit adapter before claiming they are managed; the growth inventory lists
them as not enrolled. New SEO authoring should use this maintained structured
format, or complete and test the required adapter first.

## Synchronization and publication

The growth workspace's `scripts/website_article_weblate.py` offers `prepare`,
`sync`, `status`, `approve`, and `export`, with an explicit `--site-root` option.
Credentials stay outside both repositories. `prepare` extracts current English
source by ID. `sync` updates only the article component's source through the local
Weblate API. Review affected translations and record the exact source, context and
target hashes in `agent-review.json` before `approve`. This records agent review,
not human translator approval. `export` rereads actual Weblate source, target,
approval states and unresolved checks, then writes `review.json`.

In this repository run `python3 scripts/article_i18n.py check`, then `build`,
`python3 scripts/test-article-i18n.py`, and the existing SEO, product-i18n and
consent checks. Both the legacy SEO generator and final enhancement pass invoke
the article compiler. Source/context drift, missing or unreviewed text, changed
numeric claims/placeholders and unresolved checks stop the build. The compiler
adds only real variants to language menus, reciprocal hreflang and the sitemap.
English guide-directory discovery links are maintained by the compiler.

Use the existing publishing channel after mobile and privacy verification, then
reread the production HTML and assets. The compiler and Weblate do not deploy.
Retain separate actual deployment, indexing and conversion states. Translation
pages follow the existing editorial and daily-page limits. The initial extra
French pilot was explicitly authorized on 2026-10-27, which does not change future
daily limits. Reuse the existing daily automation; no additional scheduler exists.
