import fs from 'node:fs';
import path from 'node:path';
import {visualPage} from './visual-page.mjs';
const root=path.resolve(new URL('..',import.meta.url).pathname);
let count=0;
for(const dir of fs.readdirSync(root,{withFileTypes:true})){
 if(!dir.isDirectory()||['apps','vendor','.git','assets','scripts','privacy','terms','support','legal','iphone-video-tutorials'].includes(dir.name))continue;
 const paths=dir.name==='blog'?fs.readdirSync(path.join(root,'blog'),{withFileTypes:true}).filter(x=>x.isDirectory()).map(x=>`blog/${x.name}`):[dir.name];
 for(const slug of paths){const p=path.join(root,slug,'index.html');if(!fs.existsSync(p))continue;const before=fs.readFileSync(p,'utf8');const after=visualPage(before,slug);if(before!==after){fs.writeFileSync(p,after);count++;}}
}
console.log(`Updated ${count} guide/tool pages`);
