# App Store screenshot resolution correction

The user identified blurry screenshots on the remaining product pages. The maintained Apple lookup snapshots had cached `320x480bb.jpg` thumbnails, approximately 221×480 pixels, which were also referenced by the catalog and some tutorials.

Reused the exact same Apple screenshot source identities and downloaded their native `0x0ss.png` resources. All 51 source images are 1290×2796 (48) or 1284×2778 (3). No image was upscaled, sharpened, redrawn or replaced with a different design. Lossless WebP output was decoded and compared byte-for-byte as RGBA pixels with each downloaded original; color profiles are retained when present.

Updated 57 maintained screenshot records: 33 in the eleven-App portfolio and 24 in the existing photo-app locale snapshots. Duplicate images deduplicate to 49 new content-hashed files. Replaced references and intrinsic dimensions on 22 existing public pages: seven remaining English product pages, eleven localized photo-product pages, the App catalog, two guides and the tutorial index. Existing four detailed product-page hero assets remain unchanged.

The new `scripts/refresh-store-screenshots.py` preserves source identity and saves source/output dimensions, checksums and pixel validation. Existing product generators consume the updated manifests. The portfolio validator now checks actual screenshot dimensions to catch a future return to the 221×480 thumbnail records. No native App, App Store asset upload, pricing or legal-policy content was changed.

Validation: full-site link/metadata checks run against the publication candidate, retaining unrelated committed assets absent from the working tree. Browser checks cover actual original-sized screenshots on the remaining product pages and the catalog. Source/pixel evidence and the production readback receipt are retained outside the public repository. Clearer source assets do not establish a search-ranking or installation lift.

PASS: publication candidate validates all 166 public routes, 11 Apps and 152 sitemap URLs. Complete-content regressions pass. A full portfolio rebuild preserves all eleven Apps’ image sources and intrinsic dimensions. Direct checks find no sub-1000-pixel-width assets in product or catalog store galleries. PDF Watermark and GlowPop screenshot views were visually inspected in the browser.
