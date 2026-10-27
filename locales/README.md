# Website translation catalogs

Weblate: http://localhost:8096/projects/justcompress/app-pages/

`en.json` contains the maintained English source for localized product summaries
and shared UI. The target catalogs configured in `config.json` are reviewed
Weblate exports. Supported languages are English, French, Japanese, Spanish,
Simplified Chinese, Traditional Chinese, German, Brazilian Portuguese, Italian
and Korean. Official
store names, versions, destinations and screenshots come from dated Apple
storefront snapshots. They are not translated or invented by the agent.

The localized pages summarize the verified functions, access and limitations.
They link explicitly to the longer English product walkthroughs and legal pages.
Established English pages and other Combine Photos locales retain their URLs.

`badge-sources.json` records the unmodified official Apple SVG download badges,
language identifiers, intrinsic dimensions, source URLs and SHA256 values. Use
the matching badge on product pages and directory cards. Do not translate or
redraw the artwork. The compiler preserves a 40 CSS-pixel badge height with clear
space and uses a collapsed language selector on small screens. Shared UI/CSS
URLs use content hashes so updated translations cannot keep stale browser assets.

The current mainland China lookup did not return these apps. Simplified Chinese
pages use verified Chinese-localized Singapore listings and explicitly explain
that destination and account-region availability. Never substitute a broken
China storefront URL or infer mainland availability from a translated webpage.

Workflow from the growth workspace:

1. Check changes in product facts, current storefronts and existing experiments.
2. Update complete source units and source-baseline hashes after verifying facts.
3. `python3 scripts/website_weblate.py push-source --site-root SITE`
4. Translate changed/fuzzy units, inspect context, terms, numbers and purchase rules.
5. `python3 scripts/website_weblate.py approve --site-root SITE` only after that review.
6. `python3 scripts/website_weblate.py export --site-root SITE` requires all target units approved and no unresolved checks.
7. In SITE run `python3 scripts/enhance-tutorials.py`, then `python3 scripts/install-posthog.py` and applicable tests. `scripts/i18n_pages.py` compiles the approved catalogs last.
8. Verify mobile rendering, consent and language links. Publish through the established GitHub Pages flow and read the actual public pages back.

`review.json` records the exact approved source/catalog hashes and actual Weblate
unit IDs. Changed source facts or changed unreviewed catalogs block compilation.
An unchanged catalog stays reusable. A Weblate export is not a deployment receipt.
No Weblate token or admin password belongs in Git. This local service has no paid
translation provider configured and is available while the Mac and user service run.
