import {classify} from './hdr-classify.mjs';
const $=id=>document.getElementById(id);
let worker,timer;
function stop(){clearTimeout(timer);worker?.terminate();worker=null;$('cancel').hidden=true;$('file').disabled=false;}
function analyze(file){
 stop();$('results').replaceChildren();$('results').hidden=true;
 if(!file)return;
 if(!/\.(mp4|mov|m4v|mkv|webm)$/i.test(file.name)){ $('status').textContent='Choose an MP4, MOV, M4V, MKV or WebM video.';return; }
 if(!file.size||file.size>2*1024**3){$('status').textContent='Choose a non-empty video under 2 GB.';return;}
 $('status').textContent='Reading video metadata on your device…';$('filename').textContent=file.name;$('file').disabled=true;$('cancel').hidden=false;
 try{worker=new Worker('/assets/hdr-worker.mjs',{type:'module'});}catch{stop();$('status').textContent='This browser could not start the checker. Try a current Safari, Chrome or Firefox browser.';return;}
 timer=setTimeout(()=>{stop();$('status').textContent='Reading took too long. Try a smaller original clip.';},90000);
 worker.onerror=()=>{stop();$('status').textContent='The checker could not load. Check your connection and try again; your video was not uploaded.';};
 worker.onmessage=({data})=>{
  stop();if(data.error){$('status').textContent=data.error;return;}
  if(!data.tracks.length){$('status').textContent='No readable video track found. Try the original video file.';return;}
  for(const [i,t] of data.tracks.entries()){
   const c=classify(t),section=document.createElement('section');section.className='hdr-result '+c.state;
   const badge=document.createElement('p');badge.className='tag';badge.textContent=`VIDEO TRACK ${i+1}`;
   const h=document.createElement('h2');h.textContent=c.title;const p=document.createElement('p');p.textContent=c.detail;section.append(badge,h,p);
   const dl=document.createElement('dl');
   for(const [label,value] of [['Codec',t.Format],['HDR format',t.HDR_Format],['Transfer',t.transfer_characteristics],['Color primaries',t.colour_primaries],['Bit depth',t.BitDepth?`${t.BitDepth}-bit`:null],['Resolution',t.Width&&t.Height?`${t.Width} × ${t.Height}`:null]]){
    const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=label;dd.textContent=value||'Not reported';dl.append(dt,dd);
   }
   section.append(dl);$('results').append(section);
  }
  $('results').hidden=false;$('status').textContent='Done. Results describe file metadata, not a visual color-quality test.';
 };
 worker.postMessage(file);
}
$('file').onchange=e=>analyze(e.target.files[0]);$('drop').ondragover=e=>e.preventDefault();$('drop').ondrop=e=>{e.preventDefault();analyze(e.dataTransfer.files[0]);};
$('cancel').onclick=()=>{stop();$('status').textContent='Check cancelled. Choose another video when ready.';};
window.addEventListener('pagehide',stop);
