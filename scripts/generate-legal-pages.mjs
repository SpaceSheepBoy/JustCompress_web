import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const site = "https://justcompress.online";
const contact = "abel0911@icloud.com";
const updated = "June 4, 2026";

const badgeBlack = (alt) =>
  `<img src="https://tools.applemediaservices.com/api/badges/download-on-the-app-store/black/en-us?size=250x83" alt="${alt}" loading="lazy">`;

const apps = [
  {
    slug: "pdf-compressor",
    name: "Just PDF Compressor",
    shortName: "Just PDF Compressor",
    category: "PDF utility",
    icon: "/assets/icons/app-pdf.png",
    appStore: "https://apps.apple.com/us/app/pdf-compressor-sign-merge/id6769762323",
    legacy: "https://spacesheepboy.github.io/PDFCompressorApp-legal",
    summary: "Compress, sign, merge, convert JPG images to PDF, and export PDF pages as JPEG on iPhone and iPad.",
    features: ["Compress PDFs locally on device", "Sign PDF documents", "Merge several PDFs into one file", "Convert JPG or JPEG photos into a PDF", "Export PDF pages as JPEG images"],
    fileTypes: "PDF documents and selected JPG/JPEG images",
    permissions: ["Files access is limited to documents you choose.", "Photo access is limited to selected images when you import photos for JPG to PDF workflows."],
    localData: ["Recent local workflow state and app preferences may be stored on your device.", "Output files are saved only when you choose to export or share them."],
    purchases: "Some advanced features may be offered through Apple in-app purchases. Apple processes payment and purchase history.",
    effective: "May 15, 2026"
  },
  {
    slug: "pdf-watermarker",
    name: "Just PDF Watermark",
    shortName: "Just PDF Watermark",
    category: "PDF utility",
    icon: "/assets/icons/app-watermark.png",
    appStore: "https://apps.apple.com/us/app/pdf-watermarker-stamp-docs/id6769761016",
    legacy: "https://spacesheepboy.github.io/PDFWatermarkApp-legal",
    summary: "Add visible text watermarks and stamps to PDF documents with preview, opacity, size, color, and export controls.",
    features: ["Add text watermarks to PDF pages", "Stamp drafts, confidential files, invoices, and proofs", "Adjust text, opacity, size, color, and placement", "Preview marked documents before export", "Save or share a marked copy"],
    fileTypes: "PDF documents you select",
    permissions: ["Files access is limited to PDF documents you choose."],
    localData: ["Watermark presets, recent settings, and app preferences may be stored on your device.", "Output files are saved only when you choose to export or share them."],
    purchases: "The app is distributed through the App Store. Any purchase or download transaction is handled by Apple.",
    effective: "May 15, 2026"
  },
  {
    slug: "audio-compressor",
    name: "Just Audio Compressor",
    shortName: "Just Audio Compressor",
    category: "Audio utility",
    icon: "/assets/icons/app-audio.png",
    appStore: "https://apps.apple.com/us/app/audio-compressor-reduce-size/id6769563659",
    legacy: "https://spacesheepboy.github.io/AudioCompressorApp-legal",
    summary: "Compress, convert, split, trim, merge, and change audio files on iPhone and iPad.",
    features: ["Compress recordings and music files", "Convert common audio formats", "Split long recordings into parts", "Trim and merge audio", "Extract audio from selected videos"],
    fileTypes: "Audio files and selected media files",
    permissions: ["Files access is limited to files you choose.", "Photo or media picker access is limited to selected videos when extracting audio."],
    localData: ["Recent local workflow state, output choices, and app preferences may be stored on your device.", "Processed audio is saved only when you choose to export or share it."],
    purchases: "Advanced features are offered through Apple in-app purchases as Just Audio Compressor Pro, available either as a one-time Lifetime Unlock or as an auto-renewable monthly subscription. Both give access to the same Pro features. Apple processes payment and purchase history.",
    subscription: {
      plans: [
        ["Lifetime Unlock", "a single payment that does not expire and does not renew."],
        ["Pro Monthly", "an auto-renewable subscription billed once a month."]
      ],
      renewal: "The monthly subscription renews automatically for another month at the price shown on the purchase screen, unless it is cancelled at least 24 hours before the end of the current period. Payment is charged to your Apple Account when you confirm the purchase, and again at the start of each renewal period.",
      cancel: "You can manage or cancel the subscription at any time in your Apple Account settings, or from Manage Subscription inside the app. Cancelling stops future renewals; access continues until the end of the period you have already paid for.",
      prices: "Current prices are shown in the app before you buy and on the App Store listing. Prices vary by country or region and may change; Apple will notify you of a price increase and ask for your consent where required."
    },
    effective: "September 7, 2026"
  },
  {
    slug: "vidkit",
    name: "Just Video Compressor",
    shortName: "Just Video Compressor",
    category: "Video and photo utility",
    icon: "/assets/icons/app-video.png",
    appStore: "",
    legacy: "https://spacesheepboy.github.io/VideoCompressorApp-legal",
    summary: "Compress videos and photos, convert MP4, HEVC, MOV, and GIF workflows, and change video speed on iPhone and iPad.",
    features: ["Compress videos and reduce file size", "Convert HEVC, H.264, MP4, and MOV workflows", "Create GIFs from short videos", "Change video speed", "Compress selected photos"],
    fileTypes: "Selected videos and photos",
    permissions: ["Photo library or file picker access is limited to media you select.", "Camera access is not required for normal conversion or compression workflows."],
    localData: ["Recent local workflow state, output choices, and app preferences may be stored on your device.", "Processed media is saved only when you choose to export or share it."],
    purchases: "Some advanced features may be offered through Apple in-app purchases. Apple processes payment and purchase history.",
    effective: "May 14, 2026",
    pendingStore: true
  }
];

const ensureDir = (dir) => fs.mkdirSync(path.join(root, dir), { recursive: true });
const write = (file, html) => {
  const full = path.join(root, file);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, html);
};
const esc = (value) =>
  String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");

function brandMark() {
  return `<svg class="mark" viewBox="0 0 28 28" fill="none" aria-hidden="true">
        <rect x="1" y="1" width="26" height="26" rx="8" stroke="currentColor" stroke-width="1.6"/>
        <path d="M8 9.5 11.5 14 8 18.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M20 9.5 16.5 14 20 18.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>`;
}

function nav(active = "legal") {
  const link = (href, label, key) => `<a${active === key ? ' class="active"' : ""} href="${href}">${label}</a>`;
  return `<div class="topline"></div>
<div class="shell">
  <nav class="nav">
    <a class="brand" href="/">
      ${brandMark()}
      Just Compress
    </a>
    <div class="nav-links">
      ${link("/compress-pdf/", "Compress PDF", "pdf")}
      ${link("/compress-audio/", "Compress Audio", "audio")}
      ${link("/compress-video/", "Compress Video", "video")}
      ${link("/tutorials/", "Help", "help")}
      ${link("/legal/", "Legal", "legal")}
    </div>
  </nav>
</div>`;
}

function footer() {
  return `<footer class="site-foot">
  <div class="shell">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="brand" href="/">
          ${brandMark()}
          Just Compress
        </a>
        <p>Free online file tools. Private by default. Your files stay on your device.</p>
      </div>
      <div class="foot-col">
        <h4>Popular tools <span class="free-badge">Free</span></h4>
        <a href="/compress-pdf/">🔥 Compress PDF</a>
        <a href="/compress-audio/">🔥 Compress Audio</a>
        <a href="/compress-photos/">🔥 Compress Photos</a>
        <a href="/m4a-to-mp3/">🔥 M4A to MP3</a>
        <a href="/mov-to-mp4/">🔥 MOV to MP4</a>
      </div>
      <div class="foot-col">
        <h4>Audio tools <span class="free-badge">Free</span></h4>
        <a href="/compress-audio/">Compress Audio</a>
        <a href="/m4a-to-mp3/">M4A to MP3</a>
        <a href="/mp3-to-m4a/">MP3 to M4A</a>
        <a href="/audio-speed-changer/">Audio Speed Changer</a>
        <a href="/trim-audio/">Trim Audio</a>
        <a href="/split-audio/">Split Audio</a>
      </div>
      <div class="foot-col">
        <h4>PDF tools <span class="free-badge">Free</span></h4>
        <a href="/compress-pdf/">Compress PDF</a>
        <a href="/watermark-pdf/">Watermark PDF</a>
        <a href="/merge-pdf/">Merge PDF</a>
        <a href="/sign-pdf/">Sign PDF</a>
        <a href="/jpg-to-pdf/">JPG to PDF</a>
        <a href="/pdf-to-jpg/">PDF to JPG</a>
      </div>
      <div class="foot-col">
        <h4>Video &amp; photos <span class="free-badge">Free</span></h4>
        <a href="/compress-video/">Compress Video</a>
        <a href="/mov-to-mp4/">MOV to MP4</a>
        <a href="/compress-photos/">Compress Photos</a>
        <a href="/jpg-to-pdf/">JPG to PDF</a>
        <a href="/pdf-to-jpg/">PDF to JPG</a>
      </div>
      <div class="foot-col">
        <h4>Help &amp; legal</h4>
        <a href="/tutorials/">Find the right tool</a>
        <a href="/iphone-video-tutorials/">iPhone video tutorials</a>
        <a href="/legal/">Legal center</a>
        <a href="/privacy/">Privacy Policy</a>
        <a href="/terms/">Terms</a>
        <a href="/support/">Support</a>
      </div>
    </div>
    <div class="foot-bottom">
      <span>&copy; Just Compress</span>
      <span>Files never leave your device.</span>
      <div class="foot-platforms" aria-label="Just Compress platforms">
        <a class="platform-link youtube" href="https://www.youtube.com/@iphonetooltips" rel="noopener" aria-label="Just Compress YouTube tutorials">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.6 7.2a3 3 0 0 0-2.1-2.1C17.7 4.6 12 4.6 12 4.6s-5.7 0-7.5.5a3 3 0 0 0-2.1 2.1A31 31 0 0 0 2 12a31 31 0 0 0 .4 4.8 3 3 0 0 0 2.1 2.1c1.8.5 7.5.5 7.5.5s5.7 0 7.5-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 22 12a31 31 0 0 0-.4-4.8ZM10 15.4V8.6l5.8 3.4L10 15.4Z"/></svg>
          <span>YouTube</span>
        </a>
      </div>
    </div>
  </div>
</footer>`;
}

function shell({ title, description, canonical, bodyClass = "t-pdf", active = "legal", schema = "", main }) {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(description)}">
<link rel="canonical" href="${canonical}">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="${canonical}">
<meta name="theme-color" content="#FBFAF6">
<link rel="stylesheet" href="/assets/app.css?v=20260604-spacing">
${schema}
</head>
<body class="${bodyClass}">
${nav(active)}
${main}
${footer()}
</body>
</html>
`;
}

function appBadge(app) {
  if (app.pendingStore) {
    return `<span class="appstore pending" aria-label="Just Video Compressor App Store listing coming soon">${badgeBlack("Download Just Video Compressor on the App Store")}</span>`;
  }
  return `<a class="appstore" href="${app.appStore}" rel="noopener">${badgeBlack(`Download ${app.shortName} on the App Store`)}</a>`;
}

function legalHero(kicker, h1, lede) {
  return `<header class="measure hero">
  <span class="kicker rise d1"><span class="led"></span>${kicker}</span>
  <h1 class="rise d2">${h1}</h1>
  <p class="lede rise d3">${lede}</p>
</header>`;
}

function appHero(app, sectionLabel = "Official app page") {
  return `<section class="app-legal-hero rise d4" aria-label="${sectionLabel}">
    <img class="app-ic lg" src="${app.icon}" alt="${app.shortName} app icon" width="64" height="64">
    <div>
      <span>${app.category}</span>
      <h2>${app.name}</h2>
      <p>${app.summary}</p>
    </div>
    ${appBadge(app)}
  </section>`;
}

function linkCard(type, href, title, text) {
  return `<a class="article-row featured" href="${href}">
    <span class="article-type">${type}</span>
    <b>${title}</b>
    <p>${text}</p>
  </a>`;
}

function appCard(app) {
  return `<a class="legal-app-card" href="/apps/${app.slug}/">
    <img class="app-ic md" src="${app.icon}" alt="${app.shortName} app icon" width="56" height="56">
    <span>${app.category}</span>
    <b>${app.name}</b>
    <p>${app.summary}</p>
  </a>`;
}

function writeLegalHome() {
  const main = `${legalHero("LEGAL CENTER", "Legal, privacy,<br><span class=\"thin\">and support.</span>", "Official Just Compress policies for the website, browser tools, and iOS apps. These pages are public, app-specific, and ready to use as future App Store metadata URLs while legacy GitHub pages remain available.")}
<main class="measure">
  <section class="article-index">
    <div class="article-section">
      <span class="eyebrow">Core policies</span>
      ${linkCard("Privacy", "/privacy/", "Just Compress Privacy Policy", "How Just Compress web tools and iOS apps handle files, diagnostics, purchases, and user data.")}
      ${linkCard("Terms", "/terms/", "Just Compress Terms of Service", "Terms for using Just Compress browser tools, app pages, and companion iOS apps.")}
      ${linkCard("Support", "/support/", "Just Compress Support", "Get help with file tools, app downloads, purchases, exports, and privacy questions.")}
    </div>
  </section>

  <section class="prose">
    <div class="tldr">
      <b>App-specific legal pages</b>
      Each iOS app has its own privacy, terms, and support pages. The older GitHub-hosted pages continue to work for older app versions and existing App Store metadata.
    </div>
    <div class="legal-app-grid">
      ${apps.map(appCard).join("\n      ")}
    </div>
  </section>
</main>`;
  write("legal/index.html", shell({
    title: "Legal, Privacy, Terms & Support - Just Compress",
    description: "Official Just Compress legal center with privacy policies, terms, support, and app-specific legal pages for Just PDF Compressor, Just PDF Watermark, Just Audio Compressor, and Just Video Compressor.",
    canonical: `${site}/legal/`,
    main
  }));
}

function writeGlobalPrivacy() {
  const main = `${legalHero("PRIVACY POLICY", "Privacy Policy,<br><span class=\"thin\">plain and specific.</span>", "Just Compress is designed around local file processing. Web tools run in your browser where possible, and iOS app pages below describe each app's exact data handling.")}
<main class="measure">
  <article class="prose">
    <div class="tldr"><b>Summary</b>Just Compress does not require an account. Browser tools process selected files on your device and do not upload those files to Just Compress. Companion iOS apps are designed for local processing and have app-specific privacy pages.</div>
    <p><strong>Effective date:</strong> ${updated}</p>
    <h2>Information we do not intentionally collect</h2>
    <ul>
      <li>Your selected documents, photos, videos, or audio files.</li>
      <li>Your name, email address, phone number, precise location, contacts, or advertising identifiers.</li>
      <li>Account credentials, because Just Compress does not require accounts for the browser tools.</li>
    </ul>
    <h2>Browser tools</h2>
    <p>Just Compress web tools use browser APIs and WebAssembly libraries to process files locally when you choose a file. Selected files stay in your browser session and are not uploaded to Just Compress servers.</p>
    <h2>iOS apps</h2>
    <p>Each iOS app has its own public privacy policy describing permissions, local data, purchases, diagnostics, and third-party services. Use the app-specific pages below for App Store metadata and in-app legal links.</p>
    <div class="article-index compact-legal-list">
      ${apps.map((app) => linkCard("App", `/apps/${app.slug}/privacy/`, `${app.name} Privacy Policy`, app.summary)).join("\n      ")}
    </div>
    <h2>Diagnostics and analytics</h2>
    <p>Apple may provide aggregated crash reports, performance information, and App Store analytics to developers. These reports are controlled by Apple and depend on user device settings. Just Compress uses them to improve reliability.</p>
    <h2>Privacy choices</h2>
    <p>You can manage app permissions in iOS Settings. You can delete app-local files and preferences by deleting the app from your device. For questions, contact <a href="mailto:${contact}">${contact}</a>.</p>
    <h2>Changes</h2>
    <p>We may update this policy as Just Compress changes. Material updates will be reflected on this page with a new effective date.</p>
  </article>
</main>`;
  write("privacy/index.html", shell({
    title: "Privacy Policy - Just Compress",
    description: "Just Compress privacy policy for browser tools and iOS apps. Files are processed locally when possible, no account is required, and app-specific privacy pages are provided.",
    canonical: `${site}/privacy/`,
    main
  }));
}

function writeGlobalTerms() {
  const main = `${legalHero("TERMS OF SERVICE", "Terms of Service,<br><span class=\"thin\">for Just Compress.</span>", "These terms cover the Just Compress website, browser tools, app pages, and companion iOS app workflows.")}
<main class="measure">
  <article class="prose">
    <div class="tldr"><b>Summary</b>Use Just Compress responsibly, keep your own copies of important files, and review outputs before relying on them. App Store purchases, refunds, and downloads are handled by Apple.</div>
    <p><strong>Effective date:</strong> ${updated}</p>
    <h2>Using Just Compress</h2>
    <p>Just Compress provides file tools, educational pages, app pages, privacy policies, terms, and support information. You are responsible for making sure your use is lawful and appropriate for the files you process.</p>
    <h2>Your files</h2>
    <p>You keep ownership of your files. Just Compress browser tools are designed to process selected files locally, but you should keep backups and review outputs before deleting originals or sharing converted files.</p>
    <h2>iOS apps and Apple purchases</h2>
    <p>Downloads, purchases, subscriptions, refunds, and family sharing are handled by Apple under Apple's App Store terms. Just Compress does not receive full payment card details.</p>
    <h2>Acceptable use</h2>
    <p>Do not use Just Compress to violate laws, infringe rights, bypass security controls, distribute harmful content, or process files you do not have permission to use.</p>
    <h2>No professional advice</h2>
    <p>Just Compress is a utility product. It does not provide legal, financial, medical, compliance, or professional review services.</p>
    <h2>Availability and changes</h2>
    <p>We may update, limit, or remove features as needed. Browser performance depends on the device, browser, file size, and available memory.</p>
    <h2>Warranty disclaimer and liability</h2>
    <p>Just Compress is provided as is and as available, without warranties to the maximum extent permitted by law. To the maximum extent permitted by law, Just Compress is not liable for indirect, incidental, special, consequential, or punitive damages.</p>
    <h2>App-specific terms</h2>
    <div class="article-index compact-legal-list">
      ${apps.map((app) => linkCard("Terms", `/apps/${app.slug}/terms/`, `${app.name} Terms`, `Terms for ${app.shortName}, including local processing, exports, purchases, and acceptable use.`)).join("\n      ")}
    </div>
    <h2>Contact</h2>
    <p>Questions about these terms can be sent to <a href="mailto:${contact}">${contact}</a>.</p>
  </article>
</main>`;
  write("terms/index.html", shell({
    title: "Terms of Service - Just Compress",
    description: "Just Compress terms of service for browser tools, app pages, and companion iOS apps, including files, purchases, acceptable use, and support.",
    canonical: `${site}/terms/`,
    main
  }));
}

function writeGlobalSupport() {
  const main = `${legalHero("SUPPORT", "Support for Just Compress<br><span class=\"thin\">and our apps.</span>", "Get help with browser tools, file exports, iOS apps, purchases, privacy questions, and App Store legal links.")}
<main class="measure">
  <article class="prose">
    <div class="tldr"><b>Contact</b>Email <a href="mailto:${contact}">${contact}</a> with the app name, device model, iOS version, browser if using the website, and a short description of the issue.</div>
    <h2>Quick checks</h2>
    <ul>
      <li>Keep the original file until you have opened and checked the output.</li>
      <li>Try a shorter file or lower quality setting if the browser runs out of memory.</li>
      <li>For iOS apps, confirm Files or Photos permission in iOS Settings.</li>
      <li>For App Store purchases or refunds, use Apple's purchase history and support flow.</li>
    </ul>
    <h2>App support pages</h2>
    <div class="article-index compact-legal-list">
      ${apps.map((app) => linkCard("Support", `/apps/${app.slug}/support/`, `${app.name} Support`, `Troubleshooting, contact information, privacy links, and legacy GitHub legal URLs for ${app.shortName}.`)).join("\n      ")}
    </div>
  </article>
</main>`;
  write("support/index.html", shell({
    title: "Support - Just Compress",
    description: "Support page for Just Compress browser tools and iOS apps. Get help with exports, purchases, privacy, and app-specific legal pages.",
    canonical: `${site}/support/`,
    main
  }));
}

function writeAppHome(app) {
  const main = `${legalHero("APP LEGAL PAGE", `${app.shortName}<br><span class="thin">official links.</span>`, `${app.summary} This page collects the app's public support, privacy, terms, App Store, and legacy GitHub legal links.`)}
<main class="measure">
  ${appHero(app)}
  <section class="article-index">
    <div class="article-section">
      <span class="eyebrow">Official Just Compress URLs</span>
      ${linkCard("Privacy", `/apps/${app.slug}/privacy/`, "Privacy Policy", `How ${app.shortName} handles selected files, permissions, local data, purchases, and diagnostics.`)}
      ${linkCard("Terms", `/apps/${app.slug}/terms/`, "Terms of Use", `Terms for using ${app.shortName}, processing files, exports, purchases, and acceptable use.`)}
      ${linkCard("Support", `/apps/${app.slug}/support/`, "Support", `Contact, troubleshooting, App Store links, and legacy legal URLs for ${app.shortName}.`)}
    </div>
  </section>
  <article class="prose">
    <div class="tldr"><b>Recommended future App Store URLs</b>Privacy: ${site}/apps/${app.slug}/privacy/<br>Support: ${site}/apps/${app.slug}/support/</div>
    <h2>What ${app.shortName} does</h2>
    <ul>${app.features.map((feature) => `<li>${feature}</li>`).join("")}</ul>
    <h2>Legacy GitHub pages</h2>
    <p>Older app versions and current App Store metadata may still point to GitHub Pages. Keep those URLs live while future app versions switch to Just Compress.</p>
    <ul>
      <li><a href="${app.legacy}/privacy/" rel="noopener">Legacy privacy page</a></li>
      <li><a href="${app.legacy}/terms/" rel="noopener">Legacy terms page</a></li>
      <li><a href="${app.legacy}/support/" rel="noopener">Legacy support page</a></li>
    </ul>
  </article>
</main>`;
  write(`apps/${app.slug}/index.html`, shell({
    title: `${app.name} - Privacy, Terms & Support`,
    description: `Official ${app.name} app page with privacy policy, terms of use, support, App Store links, and legacy GitHub legal URLs.`,
    canonical: `${site}/apps/${app.slug}/`,
    main
  }));
}

function writeAppPrivacy(app) {
  const main = `${legalHero("APP PRIVACY POLICY", `${app.shortName}<br><span class="thin">Privacy Policy.</span>`, `Privacy details for ${app.name}. This page is public and suitable for App Store privacy metadata and in-app legal links.`)}
<main class="measure">
  ${appHero(app, "App privacy overview")}
  <article class="prose">
    <div class="tldr"><b>Summary</b>${app.shortName} is designed to process ${app.fileTypes} on your device. We do not intentionally collect your files, require an account, or use advertising trackers.</div>
    <p><strong>Effective date:</strong> ${app.effective}</p>
    <h2>What this policy covers</h2>
    <p>This Privacy Policy applies to ${app.name}, including the app's file processing, export, support, and purchase-related workflows.</p>
    <h2>Files and media processing</h2>
    <p>${app.shortName} works with ${app.fileTypes} that you choose. Processing is designed to happen locally on your device. Your selected files are not intentionally uploaded to Just Compress servers.</p>
    <h2>Data we do not intentionally collect</h2>
    <ul>
      <li>The contents of your selected files, documents, photos, videos, or audio recordings.</li>
      <li>Your name, email address, phone number, contacts, precise location, or advertising identifiers.</li>
      <li>Account credentials, because the app does not require a Just Compress account.</li>
    </ul>
    <h2>Local app data</h2>
    <ul>${app.localData.map((item) => `<li>${item}</li>`).join("")}</ul>
    <h2>Permissions</h2>
    <ul>${app.permissions.map((item) => `<li>${item}</li>`).join("")}</ul>
    <p>You can review or revoke app permissions in iOS Settings.</p>
    <h2>Purchases</h2>
    <p>${app.purchases}</p>
    <h2>Diagnostics and App Store analytics</h2>
    <p>Apple may provide aggregated crash reports, performance information, and App Store analytics to developers. These reports depend on your Apple device settings and are used to improve reliability.</p>
    <h2>Third-party services</h2>
    <p>The app may use Apple frameworks and App Store services for file picking, media access, purchases, sharing, diagnostics, and distribution. We do not use advertising SDKs or sell personal data.</p>
    <h2>Children's privacy</h2>
    <p>The app is not directed to children under 13, and we do not knowingly collect personal information from children.</p>
    <h2>Changes</h2>
    <p>We may update this policy as the app changes. Material updates will be reflected on this page with a new effective date.</p>
    <h2>Contact</h2>
    <p>Questions about privacy can be sent to <a href="mailto:${contact}">${contact}</a>.</p>
    <p class="quick-note"><b>Legacy URL:</b> <a href="${app.legacy}/privacy/" rel="noopener">${app.legacy}/privacy/</a></p>
  </article>
</main>`;
  write(`apps/${app.slug}/privacy/index.html`, shell({
    title: `${app.name} Privacy Policy`,
    description: `Privacy policy for ${app.name}. Learn how selected files, permissions, local data, purchases, diagnostics, and support are handled.`,
    canonical: `${site}/apps/${app.slug}/privacy/`,
    main
  }));
}

// Apple's App Review Guideline 3.1.2 expects the terms an app links to from its App Store
// metadata to spell out the subscription itself: what the plans are, how renewal and
// cancellation work, and where the price is shown. Only apps with a subscription get this.
function subscriptionSection(app) {
  const { plans, renewal, cancel, prices } = app.subscription;
  // These prose articles use a flat h2 + ul structure with no h3 anywhere, so keep to that.
  return `<h2>Subscription terms</h2>
    <p>${app.shortName} Pro is sold as two plans:</p>
    <ul>
      ${plans.map(([name, detail]) => `<li><strong>${name}</strong> &mdash; ${detail}</li>`).join("\n      ")}
    </ul>
    <p>${renewal}</p>
    <p>${cancel}</p>
    <p>${prices}</p>`;
}

function writeAppTerms(app) {
  const main = `${legalHero("APP TERMS", `${app.shortName}<br><span class="thin">Terms of Use.</span>`, `Terms for using ${app.name}, including selected files, exports, purchases, availability, and support.`)}
<main class="measure">
  ${appHero(app, "App terms overview")}
  <article class="prose">
    <div class="tldr"><b>Summary</b>Use ${app.shortName} responsibly, keep your original files until outputs are checked, and follow Apple's App Store purchase and refund rules${app.subscription ? ". Pro is available as a one-time Lifetime Unlock or an auto-renewable monthly subscription you can cancel any time" : " for app transactions"}.</div>
    <p><strong>Effective date:</strong> ${app.effective}</p>
    <h2>License to use the app</h2>
    <p>Subject to these terms and Apple's App Store terms, you may use ${app.name} for personal or business file workflows on supported Apple devices.</p>
    <h2>Your files and outputs</h2>
    <p>You keep ownership of your files. The app creates processed copies based on the settings you choose. You are responsible for reviewing outputs before relying on them, deleting originals, or sharing files.</p>
    <h2>Acceptable use</h2>
    <p>Do not use the app to violate laws, infringe rights, bypass security controls, distribute harmful content, or process files you do not have permission to use.</p>
    <h2>Purchases and refunds</h2>
    <p>${app.purchases} Refunds, billing, family sharing, and purchase history are handled by Apple according to Apple's App Store rules.</p>
    ${app.subscription ? subscriptionSection(app) : ""}
    <h2>Availability and changes</h2>
    <p>Features may change, be limited, or be removed as the app is improved. Processing speed and output quality depend on your device, file size, file type, and selected settings.</p>
    <h2>No professional advice</h2>
    <p>The app is a utility product. It does not provide legal, financial, medical, compliance, archival, or professional review services.</p>
    <h2>Warranty disclaimer and liability</h2>
    <p>The app is provided as is and as available, without warranties to the maximum extent permitted by law. To the maximum extent permitted by law, Just Compress is not liable for indirect, incidental, special, consequential, or punitive damages.</p>
    <h2>Contact</h2>
    <p>Questions about these terms can be sent to <a href="mailto:${contact}">${contact}</a>.</p>
    <p class="quick-note"><b>Legacy URL:</b> <a href="${app.legacy}/terms/" rel="noopener">${app.legacy}/terms/</a></p>
  </article>
</main>`;
  write(`apps/${app.slug}/terms/index.html`, shell({
    title: `${app.name} Terms of Use`,
    description: `Terms of use for ${app.name}, including files, exports, purchases, acceptable use, availability, warranty disclaimer, and support.`,
    canonical: `${site}/apps/${app.slug}/terms/`,
    main
  }));
}

function writeAppSupport(app) {
  const main = `${legalHero("APP SUPPORT", `${app.shortName}<br><span class="thin">Support.</span>`, `Support information for ${app.name}, including troubleshooting, contact, App Store links, and legal URLs.`)}
<main class="measure">
  ${appHero(app, "App support overview")}
  <article class="prose">
    <div class="tldr"><b>Need help?</b>Email <a href="mailto:${contact}">${contact}</a> with the app name, iPhone or iPad model, iOS version, and what happened.</div>
    <h2>Quick checks</h2>
    <ul>
      <li>Keep the original file until you have opened and checked the output.</li>
      <li>Try a smaller file, lower quality setting, or shorter clip if processing is slow.</li>
      <li>Confirm Files or Photos permission in iOS Settings if importing does not work.</li>
      <li>Restart the app if an export sheet or file picker does not appear.</li>
    </ul>
    <h2>App Store</h2>
    <p>${app.pendingStore ? "Just Video Compressor's App Store listing is being prepared. The public legal and support pages are already available so future app versions can point here." : `Download or manage ${app.shortName} from its App Store listing.`}</p>
    ${app.pendingStore ? "" : `<p><a href="${app.appStore}" rel="noopener">Open ${app.shortName} on the App Store</a></p>`}
    <h2>Legal links</h2>
    <ul>
      <li><a href="/apps/${app.slug}/privacy/">Privacy Policy</a></li>
      <li><a href="/apps/${app.slug}/terms/">Terms of Use</a></li>
    </ul>
    <h2>Legacy GitHub links</h2>
    <p>These links remain available for older versions and current App Store metadata while future versions move to Just Compress.</p>
    <ul>
      <li><a href="${app.legacy}/privacy/" rel="noopener">Legacy privacy page</a></li>
      <li><a href="${app.legacy}/terms/" rel="noopener">Legacy terms page</a></li>
      <li><a href="${app.legacy}/support/" rel="noopener">Legacy support page</a></li>
    </ul>
  </article>
</main>`;
  write(`apps/${app.slug}/support/index.html`, shell({
    title: `${app.name} Support`,
    description: `Support page for ${app.name}. Get troubleshooting help, contact support, open legal links, and use legacy GitHub support URLs.`,
    canonical: `${site}/apps/${app.slug}/support/`,
    main
  }));
}

function updateFooters() {
  const htmlFiles = fs
    .readdirSync(root, { recursive: true, withFileTypes: true })
    .filter((entry) => entry.isFile() && entry.name === "index.html")
    .map((entry) => path.join(entry.parentPath, entry.name));

  for (const file of htmlFiles) {
    const rel = path.relative(root, file);
    let html = fs.readFileSync(file, "utf8");
    if (!html.includes('<footer class="site-foot"')) continue;
    const next = html.replace(/<footer class="site-foot">[\s\S]*?<\/footer>/, footer());
    if (next !== html) fs.writeFileSync(file, next);
  }
}

function updateSitemap() {
  const urls = [
    "/legal/",
    "/privacy/",
    "/terms/",
    "/support/",
    ...apps.flatMap((app) => [`/apps/${app.slug}/`, `/apps/${app.slug}/privacy/`, `/apps/${app.slug}/terms/`, `/apps/${app.slug}/support/`])
  ];
  let xml = fs.readFileSync(path.join(root, "sitemap.xml"), "utf8");
  for (const url of urls) {
    const loc = `${site}${url}`;
    if (xml.includes(`<loc>${loc}</loc>`)) continue;
    const block = `  <url>
    <loc>${loc}</loc>
    <changefreq>monthly</changefreq>
    <priority>${url.startsWith("/apps/") ? "0.7" : "0.8"}</priority>
  </url>
`;
    xml = xml.replace("</urlset>", `${block}</urlset>`);
  }
  fs.writeFileSync(path.join(root, "sitemap.xml"), xml);
}

function updateLlms() {
  const file = path.join(root, "llms.txt");
  let text = fs.readFileSync(file, "utf8");
  const section = `\n## Legal, privacy, and support\n- [Legal center](${site}/legal/): official Just Compress legal hub with global policies and app-specific legal pages.\n- [Privacy Policy](${site}/privacy/): site-wide privacy policy for Just Compress browser tools and iOS apps.\n- [Terms of Service](${site}/terms/): terms covering Just Compress browser tools, app pages, and app workflows.\n- [Support](${site}/support/): general support for Just Compress browser tools and iOS apps.\n${apps.map((app) => `- [${app.name} legal page](${site}/apps/${app.slug}/): app-specific privacy, terms, support, recommended future App Store URLs, and legacy GitHub legal links.`).join("\n")}\n`;
  if (!text.includes("## Legal, privacy, and support")) {
    text += section;
  }
  if (!text.includes("Just Video Compressor")) {
    text += `\n- [Just Video Compressor legal page](${site}/apps/vidkit/): public legal and support pages prepared before the App Store link is available.\n`;
  }
  fs.writeFileSync(file, text);
}

function main() {
  ensureDir("legal");
  ensureDir("privacy");
  ensureDir("terms");
  ensureDir("support");
  writeLegalHome();
  writeGlobalPrivacy();
  writeGlobalTerms();
  writeGlobalSupport();
  for (const app of apps) {
    writeAppHome(app);
    writeAppPrivacy(app);
    writeAppTerms(app);
    writeAppSupport(app);
  }
  updateFooters();
  updateSitemap();
  updateLlms();
}

main();
