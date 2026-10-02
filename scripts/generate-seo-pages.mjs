import { visualPage } from './visual-page.mjs';
// Generates top-level SEO guide pages from scripts/seo-content.json.
// Mirrors the look/structure of generate-privacy-blog.mjs (nav, footer, JSON-LD).
// Pages are written to <slug>/index.html at the repo root, and sitemap.xml +
// llms.txt are updated idempotently. Does NOT deploy — review, then deploy.
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(new URL("..", import.meta.url).pathname);
const site = "https://justcompress.online";
const cssVersion = "20260604-blog";

const dataPath = path.join(root, "scripts", "seo-content.json");
const pages = JSON.parse(fs.readFileSync(dataPath, "utf8"));

const toolLinks = [
  ["Compress PDF", "/compress-pdf/"],
  ["Compress Audio", "/compress-audio/"],
  ["Compress Video", "/compress-video/"],
  ["Watermark PDF", "/watermark-pdf/"],
  ["Help", "/tutorials/"],
  ["Blog", "/blog/"],
];

const related = [
  { title: "Compress PDF", text: "Make a private PDF smaller without uploading it.", href: "/compress-pdf/" },
  { title: "Compress Video", text: "Shrink MP4 and MOV clips locally in your browser.", href: "/compress-video/" },
  { title: "Compare File Tools", text: "See when Just Compress, ChatGPT, Adobe, or cloud tools make sense.", href: "/compare-file-tools/" },
];

const esc = (v) => String(v).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
const attr = esc;
const json = (d) => JSON.stringify(d, null, 2).replaceAll("</", "<\\/");

function brand() {
  return `<a class="brand" href="/"><svg class="mark" viewBox="0 0 28 28" fill="none" aria-hidden="true"><rect x="3" y="3" width="22" height="22" rx="6.5" stroke="#F5D200" stroke-width="1.8"/><path d="M9.6 10.3 12.2 14 9.6 17.7" stroke="#F5D200" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/><path d="M18.4 10.3 15.8 14 18.4 17.7" stroke="#F5D200" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/></svg>Just <span class="brand-hl">Compress</span></a>`;
}

function nav() {
  return `<div class="shell"><nav class="nav">${brand()}<div class="nav-links">${toolLinks.map(([label, href]) => `<a href="${href}">${label}</a>`).join("")}</div></nav></div>`;
}

function footer() {
  return `<footer class="site-foot">
  <div class="shell">
    <div class="foot-grid">
      <div class="foot-brand">
        ${brand()}
        <p>Free online file tools. Private by default. Your files stay on your device.</p>
      </div>
      <div class="foot-col">
        <h4>Popular tools <span class="free-badge">Free</span></h4>
        <a href="/compress-pdf/">Compress PDF</a>
        <a href="/compress-audio/">Compress Audio</a>
        <a href="/compress-video/">Compress Video</a>
        <a href="/compress-photos/">Compress Photos</a>
        <a href="/mov-to-mp4/">MOV to MP4</a>
      </div>
      <div class="foot-col">
        <h4>PDF tools <span class="free-badge">Free</span></h4>
        <a href="/compress-pdf/">Compress PDF</a>
        <a href="/watermark-pdf/">Watermark PDF</a>
        <a href="/merge-pdf/">Merge PDF</a>
        <a href="/sign-pdf/">Sign PDF</a>
        <a href="/jpg-to-pdf/">JPG to PDF</a>
      </div>
      <div class="foot-col">
        <h4>Private guides</h4>
        <a href="/blog/">Blog</a>
        <a href="/best-private-file-tools/">Best private file tools</a>
        <a href="/compare-file-tools/">Compare file tools</a>
        <a href="/tutorials/">Help</a>
      </div>
      <div class="foot-col">
        <h4>Legal</h4>
        <a href="/privacy/">Privacy Policy</a>
        <a href="/terms/">Terms</a>
        <a href="/support/">Support</a>
      </div>
    </div>
    <div class="foot-bottom">
      <span>&copy; Just Compress</span>
      <span>Free private file tools for PDF, audio, video, and photos.</span>
      <a href="/blog/">Privacy-first file guides</a>
    </div>
  </div>
</footer>`;
}

function faqHtml(page) {
  return `<section class="faq" aria-label="${attr(page.title)} FAQ">
      ${page.faqs.map(([q, a], i) => `<details class="faq-item"${i === 0 ? " open" : ""}>
        <summary>${esc(q)}<span class="pm"></span></summary>
        <div class="faq-body"><p>${esc(a)}</p></div>
      </details>`).join("\n      ")}
    </section>`;
}

function render(page) {
  const canonical = `${site}/${page.slug}/`;
  const articleLd = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: page.title,
    description: page.description,
    author: { "@type": "Organization", name: "Just Compress" },
    publisher: { "@type": "Organization", name: "Just Compress" },
    mainEntityOfPage: canonical,
  };
  const faqLd = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: page.faqs.map(([q, a]) => ({ "@type": "Question", name: q, acceptedAnswer: { "@type": "Answer", text: a } })),
  };
  const sourceHtml = page.sources ? `<h2>Source notes</h2>
    <ul>${page.sources.map(([label, href]) => `<li><a href="${href}" rel="nofollow noopener">${esc(label)}</a></li>`).join("")}</ul>` : "";
  const relatedCards = related.map((it) => `<a class="guide-card" href="${it.href}"><b>${esc(it.title)}</b><span>${esc(it.text)}</span><span class="open">Open -></span></a>`).join("\n    ");

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="apple-itunes-app" content="app-id=6769762323">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(page.title)} | Just Compress</title>
<meta name="description" content="${attr(page.description)}">
<link rel="canonical" href="${canonical}">
<meta property="og:title" content="${attr(page.title)}">
<meta property="og:description" content="${attr(page.description)}">
<meta property="og:type" content="article">
<meta property="og:url" content="${canonical}">
<meta name="theme-color" content="#FBFAF6">
<link rel="icon" href="/assets/icons/just-compress-icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/icons/just-compress-icon.svg">
<link rel="stylesheet" href="/assets/app.css?v=${cssVersion}">
<script type="application/ld+json">
${json(articleLd)}
</script>
<script type="application/ld+json">
${json(faqLd)}
</script>
</head>
<body class="t-pdf">
<div class="topline"></div>
${nav()}

<header class="measure hero">
  <span class="kicker rise d1"><span class="led"></span>${esc(page.tag)}</span>
  <h1 class="rise d2">${esc(page.title)}</h1>
  <p class="lede rise d3">${esc(page.description)}</p>
  <div class="assure rise d3">No-upload file tools for supported PDF, audio, video, and photo tasks</div>
</header>

<main class="measure">
  <article class="prose">
    <div class="tldr"><b>Short answer</b>${esc(page.direct)}</div>

    ${page.sections.map(([h, b]) => `<h2>${esc(h)}</h2>
    <p>${esc(b)}</p>`).join("\n\n    ")}

    <p class="rise"><a class="btn-primary" href="${page.primaryCta}">Open the free tool -></a></p>

    <h2>FAQ</h2>
    ${faqHtml(page)}

    ${sourceHtml}
  </article>

  <div class="guide-grid">
    ${relatedCards}
  </div>
</main>

${footer()}
</body>
</html>
`;
}

// --- write pages ---
for (const page of pages) {
  const dir = path.join(root, page.slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, "index.html"), visualPage(render(page), page.slug));
}

// --- update sitemap.xml (idempotent) ---
const sitemapPath = path.join(root, "sitemap.xml");
let sitemap = fs.readFileSync(sitemapPath, "utf8");
for (const page of pages) {
  const loc = `${site}/${page.slug}/`;
  if (!sitemap.includes(`<loc>${loc}</loc>`)) {
    const block = `  <url>\n    <loc>${loc}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n`;
    sitemap = sitemap.replace("</urlset>", `${block}</urlset>`);
  }
}
fs.writeFileSync(sitemapPath, sitemap);

// --- update llms.txt (idempotent) ---
const llmsPath = path.join(root, "llms.txt");
if (fs.existsSync(llmsPath)) {
  let llms = fs.readFileSync(llmsPath, "utf8");
  const marker = "## SEO guides";
  if (!llms.includes(marker)) llms = `${llms.trimEnd()}\n\n${marker}\n`;
  for (const page of pages) {
    const url = `${site}/${page.slug}/`;
    if (!llms.includes(url)) {
      llms = `${llms.trimEnd()}\n- [${page.title}](${url}): ${page.description}`;
    }
  }
  fs.writeFileSync(llmsPath, `${llms.trimEnd()}\n`);
}

console.log(`Generated ${pages.length} SEO guide page(s): ${pages.map((p) => p.slug).join(", ")}`);
