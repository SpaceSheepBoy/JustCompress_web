// Preserve maintained policies. The verified portfolio builder owns product identities.
import { spawnSync } from 'node:child_process';
import path from 'node:path';
const root=path.resolve(new URL('..',import.meta.url).pathname);
for(const script of ['build-app-portfolio.py','repair-seo-metadata.py','refresh-public-pages.py']){
 const result=spawnSync('python3',[path.join(root,'scripts',script)],{cwd:root,stdio:'inherit'});
 if(result.status!==0)process.exit(result.status||1);
}
console.log('Product identities refreshed. Existing policy bodies preserved.');
