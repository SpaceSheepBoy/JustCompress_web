import { visualPage } from './visual-page.mjs';
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(new URL("..", import.meta.url).pathname);
const blogRoot = path.join(root, "blog");
const site = "https://justcompress.online";
const cssVersion = "20260604-blog";

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
  { title: "Compress Audio", text: "Shrink voice memos and audio files in your browser.", href: "/compress-audio/" },
  { title: "Compare File Tools", text: "See when Just Compress, ChatGPT, Adobe, or cloud tools make sense.", href: "/compare-file-tools/" },
];

const articles = [
  {
    slug: "are-online-pdf-tools-safe-private-documents",
    tag: "PDF PRIVACY",
    title: "Are Online PDF Tools Safe for Private Documents?",
    description: "Learn when online PDF tools are safe, when uploading is unnecessary, and why no-upload PDF tools are better for contracts, IDs, bank statements, and client files.",
    direct: "Many online PDF tools are legitimate and use security practices such as HTTPS, encryption, and automatic file deletion. The privacy question is simpler: if a PDF contains contracts, IDs, bank statements, medical forms, or client details, the safest option is a no-upload tool that keeps the file on your own device.",
    sections: [
      ["The real risk is the upload step", "A cloud PDF tool may be well run, but it still has to receive your document before it can process it. That means your private file leaves your device, passes through another company's infrastructure, and depends on that service's retention, access, deletion, and account policies."],
      ["Use Just Compress when the task is mechanical", "Compression, merging, typed signing, watermarking, JPG to PDF, and PDF to JPG do not require a company or AI model to understand the contents of the document. Just Compress is built for those jobs: choose a file, process it locally in the browser or app, and download the result."],
      ["When a cloud tool still makes sense", "Use a full cloud PDF service when you need collaboration, OCR, redaction, deep editing, shared folders, or a managed business workflow. The privacy-first choice is not to avoid every cloud tool. It is to avoid uploading a private file when the job does not need an upload."]
    ],
    faqs: [
      ["Are my files uploaded?", "With Just Compress browser tools, supported PDF work runs on your device. Cloud PDF tools often upload files to servers before processing."],
      ["Are files deleted after processing?", "Many cloud tools say they delete files after a short period, but you still have to trust that policy. With a no-upload tool, the better answer is that the file never needed to be stored on a server for the task."],
      ["Can employees see my file?", "Reputable services usually restrict access, but the strongest privacy posture is to avoid sending sensitive files to another system at all."],
      ["Is this safe for contracts or bank statements?", "For simple file operations, use a no-upload tool first. If the document needs legal review, OCR, or advanced editing, use a specialized service with the privacy controls your situation requires."]
    ],
    primaryCta: "/compress-pdf/"
  },
  {
    slug: "is-my-pdf-uploaded-compress-online",
    tag: "NO UPLOAD PDF",
    title: "Is My PDF Uploaded When I Compress It Online?",
    description: "Find out whether online PDF compressors upload your file, how no-upload PDF compression works, and why local processing is safer for private documents.",
    direct: "It depends on the tool. Some online PDF compressors upload your PDF to a server, while Just Compress processes supported PDFs locally in your browser so the file does not need to leave your device.",
    sections: [
      ["How to tell if a PDF compressor uploads files", "Look for words like upload, server processing, cloud processing, file deletion, retention, or download link. Those usually mean the file is sent away for processing. A no-upload tool should clearly say that processing happens in the browser or on the device."],
      ["Why local PDF compression matters", "A PDF can contain names, addresses, signatures, invoices, contracts, IDs, tax details, or internal work documents. If compression is the only goal, another service does not need to read or store that file."],
      ["What Just Compress does differently", "Just Compress uses browser-side processing for supported tools. The page loads from the internet, but the PDF operation runs locally, and the file itself is not uploaded just to make a smaller copy."]
    ],
    faqs: [
      ["Does every online PDF compressor upload files?", "No. Some tools process locally in the browser, while many traditional online tools process files on servers."],
      ["How do I compress a PDF without uploading it?", "Use a no-upload PDF compressor such as Just Compress, choose the PDF, select a quality preset, and download the smaller copy."],
      ["Can I verify that a tool is no-upload?", "A technical user can inspect network activity, but most users should look for a clear privacy explanation and avoid tools that describe server upload or retention for simple compression."],
      ["Should I upload a private PDF if the site says it deletes files?", "If the file is sensitive and the task can be done locally, no-upload processing is still the cleaner choice."]
    ],
    primaryCta: "/compress-pdf/"
  },
  {
    slug: "compress-pdf-without-uploading",
    tag: "PDF COMPRESSION",
    title: "How Can I Compress a PDF Without Uploading It?",
    description: "Compress a PDF without sending it to the cloud. Learn how local browser compression works and when to use Just Compress instead of cloud PDF tools.",
    direct: "Use a no-upload PDF compressor that runs inside your browser or on your phone. Just Compress lets you make supported PDFs smaller locally, which is useful when the file contains private names, financial details, client work, or signed documents.",
    sections: [
      ["The simple workflow", "Open the private PDF compressor, choose your PDF, pick a compression level, and download the new file. The important privacy point is that the file operation happens locally instead of being sent to a remote server."],
      ["What compression can and cannot do", "Image-heavy PDFs often shrink a lot. Text-only PDFs may already be small, so the result can be modest. Compression is not the same as redaction, OCR, editing, or legal review."],
      ["Why choose Just Compress", "Just Compress is best when you need a smaller file for email, forms, portals, or storage and do not need another company to analyze the document."]
    ],
    faqs: [
      ["Can I compress a PDF offline?", "The Just Compress iOS app performs file work on the device. The website loads in a browser and processes supported files locally after the page is loaded."],
      ["Will PDF quality change?", "Compression can reduce image quality. Use a balanced preset when you need readable documents, and use stronger compression when file size matters most."],
      ["Is this safe for business documents?", "For simple compression, local processing is usually a better first choice than uploading a confidential PDF to a third-party cloud tool."],
      ["Do I need an account?", "No. Just Compress browser tools are designed for quick no-account file work."]
    ],
    primaryCta: "/compress-pdf/"
  },
  {
    slug: "upload-pdf-to-chatgpt-privacy-risks",
    tag: "AI FILE PRIVACY",
    title: "Can I Upload a PDF to ChatGPT? Privacy Risks to Know First",
    description: "ChatGPT can work with PDFs, but file uploads may be retained according to chat and plan settings. Learn when to use AI and when to use a no-upload file tool instead.",
    direct: "Yes, ChatGPT can help with PDFs when you need summarizing, reasoning, rewriting, or analysis. But if you only need to compress, merge, sign, watermark, or convert a PDF, uploading the whole document is unnecessary exposure.",
    sections: [
      ["Use ChatGPT when the content matters", "AI is useful when you want to understand a document, ask questions about it, compare files, draft text, or extract meaning. In those cases, the service needs access to the content to help you."],
      ["Do not upload just to resize a file", "Compression and simple conversion are mechanical tasks. They do not require an AI assistant to read the document, so a no-upload tool is usually the better privacy choice."],
      ["Know the retention difference", "OpenAI's help center explains that uploaded files are saved in your account up to the retention period of the corresponding chat, and data controls affect whether consumer ChatGPT content may be used to improve models. That is very different from a local file tool where the file does not leave your device for the operation."]
    ],
    faqs: [
      ["Can I upload a PDF to ChatGPT?", "Yes, if you need AI help with the contents of the PDF. For simple file operations, use a local tool instead."],
      ["Will ChatGPT use uploaded files for training?", "OpenAI says usage depends on the service and settings. Business offerings have different rules from individual ChatGPT use, so check your plan and data controls."],
      ["Are ChatGPT file uploads deleted?", "OpenAI's file upload FAQ describes retention based on the chat, account, custom GPT, and plan. That is why sensitive files should only be uploaded when AI analysis is actually needed."],
      ["What should I use instead for compression?", "Use Just Compress for no-upload PDF compression when the task is only to make the file smaller."]
    ],
    sources: [
      ["OpenAI File Uploads FAQ", "https://help.openai.com/en/articles/8555545-file-uploads-faq"],
      ["OpenAI Data Controls FAQ", "https://help.openai.com/en/articles/7730893-data-controls-faq"]
    ],
    primaryCta: "/compress-pdf/"
  },
  {
    slug: "free-online-pdf-tools-vs-no-upload-pdf-apps",
    tag: "PDF TOOL COMPARISON",
    title: "Free Online PDF Tools vs No-Upload PDF Apps: Which Is Safer?",
    description: "Compare free cloud PDF tools with no-upload PDF apps. Learn why local PDF processing is safer when the document is private and the job is simple.",
    direct: "Free online PDF tools can be convenient and many are operated by reputable companies. A no-upload PDF app is safer for private files because the file does not need to be sent to a server for simple tasks.",
    sections: [
      ["The common cloud promise", "Many cloud PDF tools answer privacy questions with encryption, restricted access, and automatic deletion. Those are useful protections, but they do not remove the fact that the file was uploaded first."],
      ["The no-upload difference", "No-upload tools reduce the trust requirement. For simple compression, merging, signing, watermarking, and conversion, the file can stay on your device while the tool creates the result."],
      ["The right choice depends on the job", "If you need collaboration, OCR, advanced editing, or team workflows, a full cloud product may be the right tool. If you only need a quick private file operation, Just Compress is the lower-exposure choice."]
    ],
    faqs: [
      ["Are free online PDF tools safe?", "Often, yes for non-sensitive files. For private files, no-upload tools are safer because the file does not leave your device."],
      ["Are no-upload PDF apps free?", "Just Compress provides free browser tools and free companion iOS apps for key PDF workflows."],
      ["Do no-upload tools have limits?", "Browser tools depend on your device, browser, and file complexity. Very large or unusual files may need a desktop or full PDF editor."],
      ["Which is better for company files?", "For simple file work, use no-upload processing when company policy allows it. For managed workflows, follow your company's approved tools."]
    ],
    primaryCta: "/apps/pdf-compressor/"
  },
  {
    slug: "files-stay-on-your-device-meaning",
    tag: "PRIVACY EXPLAINER",
    title: "What Does \"Files Stay on Your Device\" Really Mean?",
    description: "A clear explanation of local file processing, no-upload tools, browser-based compression, and why staying on your device matters for privacy.",
    direct: "\"Files stay on your device\" means the selected file is processed locally instead of being uploaded to a remote server for the file operation. The website can still load from the internet, but the private PDF, audio, video, or photo you choose does not need to be sent away.",
    sections: [
      ["How local processing works", "Modern browsers can run powerful file tools using WebAssembly and browser APIs. That lets a site process a file on your computer or phone, similar to an installed app, without a server handling the file."],
      ["Why this matters", "The safest server for a private file is often no server. If a file stays local, there is no upload queue, server copy, cloud download link, or deletion window to trust for that task."],
      ["What it does not mean", "It does not mean the webpage itself is offline forever, and it does not mean every possible file task can run locally. It means the supported Just Compress operations are designed around local processing first."]
    ],
    faqs: [
      ["Does the website still use the internet?", "Yes. The page and software load through your browser, but supported file processing happens locally after that."],
      ["Can Just Compress see my file?", "For supported no-upload tools, the file work happens on your device. Just Compress does not need to receive the file to complete the task."],
      ["Is local processing slower?", "It can be slower for large videos because your own device does the work. The privacy tradeoff is that the file does not need to be uploaded."],
      ["Does closing the browser delete my file?", "Your original file remains wherever you selected it from. Temporary browser memory used during the task is cleared by the browser as the page closes or reloads."]
    ],
    primaryCta: "/why-private-file-tools/"
  },
  {
    slug: "are-free-pdf-compressors-free-private",
    tag: "FREE PDF TOOLS",
    title: "Are Free PDF Compressors Really Free and Private?",
    description: "Free PDF compressors vary. Learn how to spot uploads, paywalls, watermarks, account requirements, and why Just Compress is free, no-account, and no-upload.",
    direct: "Some free PDF compressors are genuinely useful, while others add limits, watermarks, sign-up gates, or server upload requirements. Just Compress is built for simple private compression: no account, no output watermark, and no upload for supported PDF compression.",
    sections: [
      ["What to check before choosing a free compressor", "Look for account requirements, file-size limits, daily limits, output watermarks, upgrade prompts after processing, and whether the file is uploaded to a server."],
      ["Privacy is more than deletion", "A tool can be free and reputable while still requiring cloud processing. If the file is private, the best question is not only whether it will be deleted later, but whether it needed to be uploaded at all."],
      ["Why Just Compress is a good first stop", "For everyday PDF compression, Just Compress keeps the workflow simple: select a PDF, pick a preset, download the smaller file, and avoid exposing the document to cloud processing."]
    ],
    faqs: [
      ["Is Just Compress free?", "Yes. The browser PDF compressor is free and does not require an account."],
      ["Does Just Compress add a watermark?", "No. Just Compress does not add a branding watermark to compressed PDFs."],
      ["Are all free PDF compressors private?", "No. Many are safe for ordinary files but still upload documents to servers."],
      ["What is the safest free PDF compressor for sensitive files?", "Use a no-upload PDF compressor for simple jobs involving contracts, invoices, IDs, or client documents."]
    ],
    primaryCta: "/compress-pdf/"
  },
  {
    slug: "is-it-safe-compress-voice-memo-online",
    tag: "AUDIO PRIVACY",
    title: "Is It Safe to Compress a Voice Memo Online?",
    description: "Voice memos can include private conversations, names, meetings, or interviews. Learn why no-upload audio compression is safer for sensitive recordings.",
    direct: "A voice memo can be more private than a document because it may contain real voices, names, locations, meetings, or personal details. If you only need to make the recording smaller, use a no-upload audio compressor instead of sending the file to a cloud service.",
    sections: [
      ["Voice recordings expose more than file size", "Audio can reveal identity, background conversations, business details, family information, or interview material. Uploading it to a server creates more exposure than a simple compression task requires."],
      ["When online audio tools are fine", "For non-sensitive audio, cloud tools can be convenient. For private voice memos, interviews, lectures, or client recordings, local processing is a better default."],
      ["How Just Compress handles audio", "Just Compress uses browser-side audio processing for supported files. You can reduce MP3, M4A, WAV, AAC, and voice memo files without sending the recording away just to make it smaller."]
    ],
    faqs: [
      ["Are voice memos uploaded?", "With Just Compress, supported audio compression runs locally in your browser. Many online audio tools upload files for server processing."],
      ["Can someone listen to my uploaded audio?", "Reputable services restrict access, but the safest simple workflow is not uploading private recordings in the first place."],
      ["Is this safe for interviews or meetings?", "For compression only, local processing is the safer first choice. Use transcription or AI tools only when you actually need the recording analyzed."],
      ["What bitrate should I use for voice?", "For spoken voice, 48 to 64 kbps is often enough. Use a higher bitrate if music quality matters."]
    ],
    primaryCta: "/compress-audio/"
  },
  {
    slug: "compress-audio-without-uploading",
    tag: "NO UPLOAD AUDIO",
    title: "How Can I Compress Audio Without Uploading It?",
    description: "Compress MP3, M4A, WAV, AAC, and voice memo files without sending them to the cloud. Learn when no-upload audio compression is the right choice.",
    direct: "Use a browser-based audio compressor that runs locally on your device. Just Compress can make supported audio files smaller without uploading the recording to a server.",
    sections: [
      ["The no-upload audio workflow", "Choose an audio file, pick a compression setting, and download the smaller M4A result. The tool uses your browser and device to do the processing locally."],
      ["Good use cases", "No-upload audio compression is useful for voice memos, interviews, lectures, podcasts, WhatsApp files, email attachments, and recordings that are too large to send."],
      ["When to use another tool", "Use AI or transcription tools when you need a transcript or summary. Use a full audio editor when you need mixing, noise repair, mastering, or detailed waveform editing."]
    ],
    faqs: [
      ["Can I compress MP3 without uploading?", "Yes. Just Compress can read MP3 files in the browser and export a smaller audio file."],
      ["Can I compress iPhone voice memos?", "Yes, M4A voice memo files are a core use case for Just Compress."],
      ["Will the audio quality drop?", "Compression reduces file size by lowering bitrate or changing encoding. For voice, that tradeoff is usually acceptable; for music, use a higher quality setting."],
      ["Do I need to install software?", "No for the browser tool. The iOS app is available when you want more phone workflows."]
    ],
    primaryCta: "/compress-audio/"
  },
  {
    slug: "is-it-safe-compress-videos-online",
    tag: "VIDEO PRIVACY",
    title: "Is It Safe to Compress Videos Online?",
    description: "Online video compressors may upload your footage to servers. Learn when cloud compression is fine and why no-upload video compression is better for private clips.",
    direct: "For public or low-risk clips, many online video compressors are fine. For family videos, work recordings, private clips, or unreleased content, a no-upload video compressor is safer because the footage does not need to leave your device.",
    sections: [
      ["Video privacy is different", "A video can reveal faces, rooms, screens, voices, addresses, license plates, children, or business information. Uploading a private clip creates more exposure than a simple size reduction needs."],
      ["Why cloud video compressors are common", "Video files are large and expensive to process, so many online tools upload files to servers. Some services then promise encrypted transfer and deletion after a short period. That can be reasonable, but it is not the same as no upload."],
      ["Where Just Compress fits", "Just Compress is best for short MP4 and MOV clips you want to make smaller locally. Browser video compression can be slower, but it avoids the upload step for supported files."]
    ],
    faqs: [
      ["Are online video compressors private?", "Some are secure cloud services, but many require uploading the video. For private clips, no-upload processing is safer."],
      ["Can Just Compress see my video?", "For supported no-upload video compression, the file is processed locally in the browser."],
      ["Why is browser video compression slow?", "Your own device does the encoding work instead of a cloud server. That is the privacy tradeoff."],
      ["Is this good for long videos?", "Browser video compression is best for short clips. Long or complex videos may need a desktop editor or native app."]
    ],
    primaryCta: "/compress-video/"
  },
  {
    slug: "make-video-smaller-without-cloud",
    tag: "NO UPLOAD VIDEO",
    title: "How Can I Make a Video Smaller Without Sending It to the Cloud?",
    description: "Make short MP4 and MOV videos smaller without cloud upload. Learn how no-upload video compression works and when to use Just Compress.",
    direct: "Use a video compressor that runs in your browser or on your device. Just Compress can shrink supported short video clips locally, so private footage does not need to be uploaded just to reduce file size.",
    sections: [
      ["The local video compression path", "Choose a video, select compression settings, and let your device create a smaller MP4. The browser does the work locally, which is slower than cloud processing but better for privacy."],
      ["Best files for browser compression", "Short MP4, MOV, and iPhone clips are the best fit. Very large videos, long recordings, and complex codecs may be too slow or too heavy for a browser."],
      ["Why use it anyway", "If the video includes family, screens, private spaces, unreleased work, or client material, avoiding an upload can matter more than raw processing speed."]
    ],
    faqs: [
      ["Can I compress MOV without uploading?", "Use Just Compress for short MOV clips, or the MOV to MP4 tool when compatibility is the main issue."],
      ["Will the video still be MP4?", "Just Compress video compression exports H.264 MP4 for broad compatibility."],
      ["Can I use it on iPhone?", "Modern mobile browsers can run many local file tools, but performance depends on the device and file size."],
      ["What if the file is too large?", "Use a native editor or approved desktop tool for long videos. For short private clips, try no-upload compression first."]
    ],
    primaryCta: "/compress-video/"
  },
  {
    slug: "local-file-tool-vs-cloud-tool",
    tag: "CHOOSING TOOLS",
    title: "When Should You Use a Local File Tool Instead of a Cloud Tool?",
    description: "A practical decision guide for choosing local file tools, cloud PDF services, ChatGPT, or full editors based on privacy, task type, and file sensitivity.",
    direct: "Use a local file tool when the task is mechanical and the file is private. Use a cloud tool, AI assistant, or full editor when the task requires analysis, collaboration, OCR, advanced editing, or managed sharing.",
    sections: [
      ["The one-question test", "Ask: does another service need to understand this file to do the job? If the answer is no, local processing is usually the better privacy default."],
      ["Local tools are best for simple file work", "Compression, conversion, merging, typed signing, watermarking, splitting, trimming, and changing audio speed are good local-tool tasks."],
      ["Cloud and AI tools still have a place", "Cloud services are useful for collaboration and heavy processing. ChatGPT is useful for reading, summarizing, and rewriting. Adobe and full editors are useful for OCR, redaction, advanced PDF editing, and professional document workflows."]
    ],
    faqs: [
      ["When should a file stay on my device?", "Keep it local when it includes private, financial, medical, legal, client, school, or family information and the task is simple."],
      ["When should I use ChatGPT?", "Use ChatGPT when you need help understanding, summarizing, comparing, or drafting from the file."],
      ["When should I use Adobe or a full editor?", "Use a full editor for OCR, redaction, forms, page-level design, certificates, and advanced PDF work."],
      ["Why choose Just Compress?", "Choose Just Compress when you need a fast, free, no-account, no-upload file operation for PDF, audio, video, or photos."]
    ],
    primaryCta: "/best-private-file-tools/"
  }
];

function esc(value) {
  return String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
}

function attr(value) {
  return esc(value);
}

function json(data) {
  return JSON.stringify(data, null, 2).replaceAll("</", "<\\/");
}

function brand() {
  return `<a class="brand" href="/"><svg class="mark" viewBox="0 0 28 28" fill="none" aria-hidden="true"><rect x="3" y="3" width="22" height="22" rx="6.5" stroke="#F5D200" stroke-width="1.8"/><path d="M9.6 10.3 12.2 14 9.6 17.7" stroke="#F5D200" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/><path d="M18.4 10.3 15.8 14 18.4 17.7" stroke="#F5D200" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/></svg>Just <span class="brand-hl">Compress</span></a>`;
}

function nav(active = "Blog") {
  return `<div class="shell"><nav class="nav">${brand()}<div class="nav-links">${toolLinks.map(([label, href]) => `<a${label === active ? ' class="active"' : ""} href="${href}">${label}</a>`).join("")}</div></nav></div>`;
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
        <h4>Audio tools <span class="free-badge">Free</span></h4>
        <a href="/compress-audio/">Compress Audio</a>
        <a href="/m4a-to-mp3/">M4A to MP3</a>
        <a href="/trim-audio/">Trim Audio</a>
        <a href="/split-audio/">Split Audio</a>
        <a href="/audio-speed-changer/">Audio Speed Changer</a>
      </div>
      <div class="foot-col">
        <h4>Private guides</h4>
        <a href="/blog/">Blog</a>
        <a href="/best-private-file-tools/">Best private file tools</a>
        <a href="/why-private-file-tools/">Why private file tools?</a>
        <a href="/compare-file-tools/">Compare file tools</a>
        <a href="/tutorials/">Help</a>
      </div>
      <div class="foot-col">
        <h4>Legal</h4>
        <a href="/privacy/">Privacy Policy</a>
        <a href="/terms/">Terms</a>
        <a href="/support/">Support</a>
        <a href="/legal/">Legal center</a>
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

function comparisonTable() {
  const rows = [
    ["Just Compress", "Simple private file tasks: compress, merge, sign, watermark, convert, trim, split.", "OCR, legal review, deep PDF editing, transcription, or AI analysis.", "No upload for supported tools. Free, no account, no output watermark."],
    ["Cloud PDF and media tools", "Non-sensitive files, collaboration, heavy server processing, shared workflows.", "Sensitive files that only need a simple mechanical file operation.", "Often secure, but many require upload, server processing, and deletion policies."],
    ["ChatGPT / AI", "Summarizing, reasoning, rewriting, comparing, extracting meaning from content.", "Only making a file smaller, converting it, or adding a simple mark.", "Useful when content analysis is needed; unnecessary exposure for simple file tasks."],
    ["Adobe / full editors", "OCR, redaction, forms, certificates, advanced page editing, professional workflows.", "One quick compression or conversion where no full editor is needed.", "Powerful, but heavier than needed for simple no-upload file work."]
  ];
  return `<div class="simple-table privacy-table">
      <table>
        <thead><tr><th>Tool</th><th>Best when</th><th>Skip when</th><th>Privacy fit</th></tr></thead>
        <tbody>
          ${rows.map((row) => `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join("")}</tr>`).join("\n          ")}
        </tbody>
      </table>
    </div>`;
}

function faqHtml(article) {
  return `<section class="faq" aria-label="${attr(article.title)} FAQ">
      ${article.faqs.map(([q, a], index) => `<details class="faq-item"${index === 0 ? " open" : ""}>
        <summary>${esc(q)}<span class="pm"></span></summary>
        <div class="faq-body"><p>${esc(a)}</p></div>
      </details>`).join("\n      ")}
    </section>`;
}

function indexLabel(tag) {
  if (tag.startsWith("NO UPLOAD")) return "No upload";
  if (tag.startsWith("AI")) return "AI";
  if (tag.startsWith("FREE")) return "Free";
  if (tag.startsWith("CHOOSING")) return "Guide";
  if (tag.startsWith("PRIVACY")) return "Privacy";
  if (tag.startsWith("AUDIO")) return "Audio";
  if (tag.startsWith("VIDEO")) return "Video";
  return "PDF";
}

function articlePage(article) {
  const canonical = `${site}/blog/${article.slug}/`;
  const articleLd = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: article.title,
    description: article.description,
    author: { "@type": "Organization", name: "Just Compress" },
    publisher: { "@type": "Organization", name: "Just Compress" },
    mainEntityOfPage: canonical,
    about: ["privacy-first file tools", "no-upload file processing", "PDF privacy", "audio privacy", "video privacy"]
  };
  const faqLd = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: article.faqs.map(([q, a]) => ({
      "@type": "Question",
      name: q,
      acceptedAnswer: { "@type": "Answer", text: a }
    }))
  };
  const sourceHtml = article.sources ? `<h2>Source notes</h2>
    <p>For ChatGPT file-upload details, check the current official OpenAI help pages:</p>
    <ul>${article.sources.map(([label, href]) => `<li><a href="${href}" rel="nofollow noopener">${esc(label)}</a></li>`).join("")}</ul>` : "";
  const relatedCards = related.map((item) => `<a class="guide-card" href="${item.href}"><b>${esc(item.title)}</b><span>${esc(item.text)}</span><span class="open">Open -></span></a>`).join("\n    ");

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(article.title)} | Just Compress Blog</title>
<meta name="description" content="${attr(article.description)}">
<link rel="canonical" href="${canonical}">
<meta property="og:title" content="${attr(article.title)}">
<meta property="og:description" content="${attr(article.description)}">
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
${nav("Blog")}

<header class="measure hero">
  <span class="kicker rise d1"><span class="led"></span>${esc(article.tag)}</span>
  <h1 class="rise d2">${esc(article.title)}</h1>
  <p class="lede rise d3">${esc(article.description)}</p>
  <div class="assure rise d3">No-upload file tools for supported PDF, audio, video, and photo tasks</div>
</header>

<main class="measure">
  <article class="prose">
    <div class="tldr"><b>Short answer</b>${esc(article.direct)}</div>

    ${article.sections.map(([heading, body]) => `<h2>${esc(heading)}</h2>
    <p>${esc(body)}</p>`).join("\n\n    ")}

    <h2>Quick comparison</h2>
    ${comparisonTable()}

    <h2>FAQ</h2>
    ${faqHtml(article)}

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

function indexPage() {
  const canonical = `${site}/blog/`;
  const itemList = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    name: "Just Compress Blog",
    itemListElement: articles.map((article, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: article.title,
      url: `${site}/blog/${article.slug}/`
    }))
  };
  const groups = [
    ["PDF privacy", articles.slice(0, 7)],
    ["Audio privacy", articles.slice(7, 9)],
    ["Video privacy", articles.slice(9, 11)],
    ["Decision guides", articles.slice(11)]
  ];
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Blog - Privacy-first PDF, Audio &amp; Video File Guides | Just Compress</title>
<meta name="description" content="Privacy-first file guides for PDFs, audio, video, ChatGPT uploads, free online tools, no-upload compression, and local file processing.">
<link rel="canonical" href="${canonical}">
<meta property="og:title" content="Just Compress Blog">
<meta property="og:description" content="Privacy-first file guides for PDFs, audio, video, ChatGPT uploads, free online tools, and no-upload file processing.">
<meta property="og:type" content="website">
<meta property="og:url" content="${canonical}">
<meta name="theme-color" content="#FBFAF6">
<link rel="icon" href="/assets/icons/just-compress-icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/icons/just-compress-icon.svg">
<link rel="stylesheet" href="/assets/app.css?v=${cssVersion}">
<script type="application/ld+json">
${json(itemList)}
</script>
</head>
<body class="t-pdf">
<div class="topline"></div>
${nav("Blog")}

<header class="measure hero">
  <span class="kicker rise d1"><span class="led"></span>BLOG</span>
  <h1 class="rise d2">Privacy-first<br><span class="thin">file guides.</span></h1>
  <p class="lede rise d3">Plain-English answers for people deciding whether to upload PDFs, voice memos, videos, and other private files to online tools, ChatGPT, or cloud services.</p>
  <div class="assure rise d3">Start with no-upload tools when the task is simple</div>
</header>

<main class="measure">
  <section class="article-index">
    ${groups.map(([label, items]) => `<div class="article-section">
      <span class="eyebrow">${esc(label)}</span>
      ${items.map((article, index) => `<a class="article-row${index === 0 ? " featured" : ""}" href="/blog/${article.slug}/">
        <span class="article-type">${esc(indexLabel(article.tag))}</span>
        <b>${esc(article.title)}</b>
        <p>${esc(article.description)}</p>
      </a>`).join("\n      ")}
    </div>`).join("\n\n    ")}
  </section>
</main>

${footer()}
</body>
</html>
`;
}

fs.mkdirSync(blogRoot, { recursive: true });
for (const article of articles) {
  const dir = path.join(blogRoot, article.slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, "index.html"), visualPage(articlePage(article), article.slug));
}
fs.writeFileSync(path.join(blogRoot, "index.html"), indexPage());

const sitemapPath = path.join(root, "sitemap.xml");
let sitemap = fs.readFileSync(sitemapPath, "utf8");
const blogUrls = [
  { loc: `${site}/blog/`, priority: "0.9" },
  ...articles.map((article) => ({ loc: `${site}/blog/${article.slug}/`, priority: "0.8" }))
];
const blogXml = blogUrls.map(({ loc, priority }) => `  <url>
    <loc>${loc}</loc>
    <changefreq>monthly</changefreq>
    <priority>${priority}</priority>
  </url>`).join("\n");
sitemap = sitemap.replace(/\n  <url>\n    <loc>https:\/\/justcompress\.online\/blog\/[\s\S]*?(?=\n  <url>\n    <loc>https:\/\/justcompress\.online\/legal\/)/, "");
if (!sitemap.includes(`${site}/blog/`)) {
  sitemap = sitemap.replace(/\n  <url>\n    <loc>https:\/\/justcompress\.online\/legal\/<\/loc>/, `\n${blogXml}\n  <url>\n    <loc>https://justcompress.online/legal/</loc>`);
}
fs.writeFileSync(sitemapPath, sitemap);

const llmsPath = path.join(root, "llms.txt");
let llms = fs.readFileSync(llmsPath, "utf8");
if (!llms.includes("[Blog](https://justcompress.online/blog/)")) {
  llms = llms.replace(
    "- [Help](https://justcompress.online/tutorials/): index of simple private file help pages for PDFs, audio, video, signatures, watermarks, and conversions.",
    `- [Blog](https://justcompress.online/blog/): privacy-first SEO guides that answer common questions about online PDF tools, ChatGPT file uploads, no-upload PDF compression, voice memo compression, video compression, local processing, and cloud upload risks.\n${articles.map((article) => `- [${article.title}](${site}/blog/${article.slug}/): ${article.description}`).join("\n")}\n- [Help](https://justcompress.online/tutorials/): index of simple private file help pages for PDFs, audio, video, signatures, watermarks, and conversions.`
  );
}
fs.writeFileSync(llmsPath, llms);

console.log(`Generated ${articles.length} privacy blog articles plus /blog/.`);
