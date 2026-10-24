import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve(new URL('..',import.meta.url).pathname);
const products=Object.values(JSON.parse(fs.readFileSync(path.join(root,'scripts/tutorial-products.json'),'utf8')));
const assets=JSON.parse(fs.readFileSync(path.join(root,'scripts/store-visuals.json'),'utf8'));
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;');
function subject(slug){return /watermark/.test(slug)?'watermark':/photo/.test(slug)?'photo':/audio|voice|m4a|mp3/.test(slug)?'audio':/video|mov/.test(slug)?'video':'pdf';}
export function visualPage(html,slug){
 if(html.includes('seo-visual'))return html;
 if(!/<header[^>]*class="[^"]*hero/.test(html))return html;
 const kind=subject(slug),a=assets[kind], tool=/id="tool"/.test(html);
 html=html.replace(/<body class="([^"]*)"/,`<body class="$1 seo-visual ${tool?'tool-first':'guide-first'}"`);
 html=html.replace('</head>','<link rel="stylesheet" href="/assets/seo-visual.css?v=20261024"></head>');
 html=html.replace(/<header\b[\s\S]*?<\/header>/,header=>{
 const title=(header.match(/<h1[^>]*>([\s\S]*?)<\/h1>/)||[])[1]||'Private file tools';
 const reviewed=(header.match(/<time[^>]*>[\s\S]*?<\/time>/)||[])[0]||'';
 const lead=tool?'Free in your browser. No account. Your files stay on your device.':(header.match(/<p[^>]*class="[^"]*lede[^"]*"[^>]*>([\s\S]*?)<\/p>/)||[])[1]||'Choose the approach that fits your file and device.';
 return `<header class="measure hero"><div class="visual-intro"><span class="kicker">${tool?'FREE BROWSER TOOL':'QUICK GUIDE'}${reviewed?' · REVIEWED '+reviewed:''}</span><h1>${title}</h1><p class="lede">${lead}</p>${tool?'':`<div class="visual-links"><a href="#full-guide" onclick="document.getElementById('full-guide').open=true">Read the guide ↓</a></div>`}</div></header>`;
 });
 if(!tool)html=html.replace(/<article class="prose"([^>]*)>([\s\S]*?)<\/article>/, '<details class="visual-guide" id="full-guide" open><summary>Steps, answers & details</summary><article class="prose"$1>$2</article></details>');
 if(!tool){
 const product=products.find(p=>p.name===a.name);
 const cta=`<aside class="visual-app"><img src="${esc(a.icon)}" width="48" height="48" alt=""><div><b>${esc(a.name)}</b><p>Our App by Space Sheep Studio. See the store for current purchase options.</p></div><a href="${esc(product?product.url:'/apps/'+a.slug+'/')}">Get the iPhone app ↗</a></aside>`;
 html=html.replace('</article></details>', '</article></details>'+cta);
 }
 if(tool){
 const start=html.indexOf('id="tool"'),end=html.indexOf('</section>',start);
 if(end!==-1){const card=`<aside class="visual-app"><img src="${esc(a.icon)}" width="48" height="48" alt=""><div><b>Prefer an iPhone app?</b><p>${esc(a.name)}</p></div><a href="/apps/#${a.slug}">See the app ↗</a></aside>`;html=html.slice(0,end+10)+card+html.slice(end+10);}
 }
 html=html.replace(/<div class="nav-links">/, '<div class="nav-links"><a href="/tools/">Free tools</a>');
 if(!html.includes('property="og:image"'))html=html.replace('</head>',`<meta property="og:image" content="${esc(a.screens[0])}"></head>`);
 return html;
}
