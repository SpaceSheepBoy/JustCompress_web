import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve(new URL('..',import.meta.url).pathname);
const assets=JSON.parse(fs.readFileSync(path.join(root,'scripts/store-visuals.json'),'utf8'));
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;');
function subject(slug){return /watermark/.test(slug)?'watermark':/photo/.test(slug)?'photo':/audio|voice|m4a|mp3/.test(slug)?'audio':/video|mov/.test(slug)?'video':'pdf';}
export function visualPage(html,slug){
 if(html.includes('seo-visual'))return html;
 if(!/<header[^>]*class="[^"]*hero/.test(html))return html;
 const kind=subject(slug),a=assets[kind], tool=/id="tool"/.test(html);
 html=html.replace(/<body class="([^"]*)"/,`<body class="$1 seo-visual ${tool?'tool-first':'guide-first'}"`);
 html=html.replace('</head>','<link rel="stylesheet" href="/assets/seo-visual.css?v=20261002"></head>');
 html=html.replace(/<header\b[\s\S]*?<\/header>/,header=>{
 const title=(header.match(/<h1[^>]*>([\s\S]*?)<\/h1>/)||[])[1]||'Private file tools';
 const lead=tool?'Free in your browser. No account. Your files stay on your device.':`See the ${kind} workflow. Try the free browser tool or find the iPhone app.`;
 const preview=tool?'':`<div class="visual-proof"><div class="visual-shots">${a.screens.map((url,i)=>`<img src="${esc(url)}" alt="${esc(a.name)} App Store preview ${i+1}" width="392" height="852" ${i?'loading="lazy"':''}>`).join('')}</div><div class="visual-caption"><img src="${esc(a.icon)}" width="44" height="44" alt=""><div><b>${esc(a.name)}</b><span>iPhone app · App Store previews</span></div><a href="/apps/#${a.slug}">View app ↗</a></div></div>`;
 return `<header class="measure hero"><div class="visual-intro"><span class="kicker">${tool?'FREE BROWSER TOOL':'QUICK GUIDE'}</span><h1>${title}</h1><p class="lede">${lead}</p>${tool?'':`<div class="visual-links"><a class="btn-primary" href="${a.tool}">Try the free tool ↗</a><a href="#full-guide" onclick="document.getElementById('full-guide').open=true">Read the guide ↓</a></div>`}</div>${preview}</header>`;
 });
 if(!tool)html=html.replace(/<article class="prose">([\s\S]*?)<\/article>/, '<details class="visual-guide" id="full-guide"><summary>Steps, answers & details</summary><article class="prose">$1</article></details>');
 if(tool){
 const start=html.indexOf('id="tool"'),end=html.indexOf('</section>',start);
 if(end!==-1){const card=`<aside class="visual-app"><img src="${esc(a.icon)}" width="48" height="48" alt=""><div><b>Prefer an iPhone app?</b><p>${esc(a.name)}</p></div><a href="/apps/#${a.slug}">See the app ↗</a></aside>`;html=html.slice(0,end+10)+card+html.slice(end+10);}
 }
 html=html.replace(/<div class="nav-links">/, '<div class="nav-links"><a href="/tools/">Free tools</a>');
 if(!html.includes('property="og:image"'))html=html.replace('</head>',`<meta property="og:image" content="${esc(a.screens[0])}"></head>`);
 return html;
}
