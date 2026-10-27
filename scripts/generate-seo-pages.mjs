// Maintained legacy URLs. Rebuild complete articles without compacting their answers.
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
const root = path.resolve(new URL('..', import.meta.url).pathname);
const site = 'https://justcompress.online';
// ID-bearing records retain their translation identity when reordered or edited.
const pages = JSON.parse(fs.readFileSync(path.join(root, 'scripts/seo-content.json'), 'utf8')).map(page => ({...page,
  ...Object.fromEntries(['cards','sections','faqs','sources','related'].map(field => [field,page[field].map(row => Array.isArray(row) ? row : field==='sources'||field==='related' ? [row.label,row.url] : [row.heading,row.body])])),
  steps:page.steps.map(step => typeof step==='string' ? step : step.text)
}));
execFileSync('python3',[path.join(root,'scripts/article_i18n.py'),'check'],{stdio:'inherit'});
const products = JSON.parse(fs.readFileSync(path.join(root, 'scripts/tutorial-products.json'), 'utf8'));
const esc = value => String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const ld = value => `<script type="application/ld+json">${JSON.stringify({'@context':'https://schema.org', ...value}).replaceAll('</', '<\\/')}</script>`;
const links = [['Guides','/guides/'],['Free tools','/tools/'],['Apps','/apps/'],['Blog','/blog/']];
function render(page) {
  const labels={jump:'In this guide',choose:'Choose the approach',steps:'Follow the checks',details:'Read the details',chooseHeading:'Choose the approach before changing the file',stepsHeading:'Three checks before you send',...page.i18n?.ui};
  const url = `${site}/${page.slug}/`, product = products[page.appId];
  const schema = ld({'@type':'Article',headline:page.title,description:page.description,dateModified:page.reviewed,mainEntityOfPage:url,author:{'@type':'Organization',name:'Space Sheep Studio'},publisher:{'@type':'Organization',name:'Space Sheep Studio'}})
    + ld({'@type':'BreadcrumbList',itemListElement:[{'@type':'ListItem',position:1,name:'Just Compress',item:site+'/'},{'@type':'ListItem',position:2,name:'Guides',item:site+'/guides/'},{'@type':'ListItem',position:3,name:page.title,item:url}]})
    + ld({'@type':'FAQPage',mainEntity:page.faqs.map(([q,a])=>({'@type':'Question',name:q,acceptedAnswer:{'@type':'Answer',text:a}}))});
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(page.title)} | Just Compress</title><meta name="description" content="${esc(page.description)}"><link rel="canonical" href="${url}">
<meta property="og:title" content="${esc(page.title)}"><meta property="og:description" content="${esc(page.description)}"><meta property="og:type" content="article"><meta property="og:url" content="${url}"><meta property="og:image" content="${site}${page.figure}">
<link rel="icon" href="/assets/icons/just-compress-icon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/tutorial-guides.css?v=20261022"><link rel="stylesheet" href="/assets/legacy-guides.css?v=20261024">
${schema}</head><body class="guide-page"><div class="guide-shell">
<nav class="guide-nav" aria-label="Main navigation"><a class="guide-brand" href="/">Just Compress</a><div>${links.map(([n,u])=>`<a href="${u}">${n}</a>`).join('')}</div></nav>
<main><header class="guide-heading"><p class="guide-eyebrow">${esc(page.tag)} · REVIEWED <time datetime="${page.reviewed}">${page.reviewed}</time></p><h1>${esc(page.title)}</h1><p class="guide-lede">${esc(page.direct)}</p></header>
<nav class="repair-jump" aria-label="${esc(labels.jump)}"><a href="#choose">${esc(labels.choose)}</a><a href="#steps">${esc(labels.steps)}</a><a href="#details">${esc(labels.details)}</a></nav>
<article class="guide-article" data-maintained-article>
<section id="choose"><h2>${esc(labels.chooseHeading)}</h2><div class="repair-cards">${page.cards.map(([h,b])=>`<div><h3>${esc(h)}</h3><p>${esc(b)}</p></div>`).join('')}</div>
<figure id="workflow"><img src="${page.figure}" alt="${esc(page.figureAlt)}" width="${page.figureWidth||640}" height="${page.figureHeight||580}"><figcaption>${esc(page.figureCaption)}</figcaption></figure></section>
<section id="steps"><h2>${esc(labels.stepsHeading)}</h2><ol>${page.steps.map(s=>`<li>${esc(s)}</li>`).join('')}</ol><p><a class="guide-button" href="${page.primaryCta}">${esc(page.primaryCtaLabel||('Open the free '+(page.appId==='6769762323'?'PDF':'video')+' compressor'))} ↗</a></p></section>
<section id="details">${page.sections.map(([h,b])=>`<h2>${esc(h)}</h2><p>${esc(b)}</p>`).join('')}</section>
<aside class="guide-cta"><div><strong>${esc(product.name)}</strong><p>Our App by Space Sheep Studio. See the App Store for current access and purchase options.</p></div><a class="guide-button" href="${esc(product.url)}">Get the iPhone app ↗</a></aside>
<section class="guide-faq"><h2>Common questions</h2>${page.faqs.map(([q,a])=>`<details><summary>${esc(q)}</summary><p>${esc(a)}</p></details>`).join('')}</section>
<section><h2>Sources and scope</h2><p>Official help checked on ${page.reviewed}. Limits and interfaces may change. Read the relevant section for your platform and account.</p><ul>${page.sources.map(([n,u])=>`<li><a href="${esc(u)}">${esc(n)}</a></li>`).join('')}</ul></section>
<section><h2>Related guides</h2><ul>${page.related.map(([n,u])=>`<li><a href="${u}">${esc(n)}</a></li>`).join('')}</ul></section>
</article></main><footer class="guide-footer"><span>© 2026 Space Sheep Studio</span><a href="/guides/">Guides</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a><a href="/support/">Support</a></footer></div></body></html>\n`;
}
for (const page of pages) {
  const dir = path.join(root, page.slug);
  fs.mkdirSync(dir, {recursive:true});
  fs.writeFileSync(path.join(dir,'index.html'),render(page));
}
// Touch dates only for the articles actually revised, preserving their original URLs.
const sitemapPath=path.join(root,'sitemap.xml');
let sitemap=fs.readFileSync(sitemapPath,'utf8');
for (const page of pages) {
  const url=`${site}/${page.slug}/`;
  sitemap=sitemap.replace(/<url>[\s\S]*?<\/url>/g, block=>{
    if(!block.includes(`<loc>${url}</loc>`))return block;
    return /<lastmod>/.test(block)?block.replace(/<lastmod>.*?<\/lastmod>/,`<lastmod>${page.reviewed}</lastmod>`):block.replace('</loc>',`</loc><lastmod>${page.reviewed}</lastmod>`);
  });
}
fs.writeFileSync(sitemapPath,sitemap);
const llmsPath=path.join(root,'llms.txt');
if(fs.existsSync(llmsPath)){
  let lines=fs.readFileSync(llmsPath,'utf8').split('\n');
  for(const page of pages){const url=`${site}/${page.slug}/`;lines=lines.map(line=>line.includes(url)?`- [${page.title}](${url}): ${page.description}`:line);}
  fs.writeFileSync(llmsPath,lines.join('\n'));
}
console.log(`Generated ${pages.length} complete guides at their existing URLs`);
execFileSync('python3',[path.join(root,'scripts/article_i18n.py'),'build'],{stdio:'inherit'});
