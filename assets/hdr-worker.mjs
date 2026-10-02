import factory from '/vendor/mediainfo/mediainfo.mjs';
self.onmessage=async({data:file})=>{
 let mi;
 try{
  mi=await factory({format:'object',locateFile:()=>'/vendor/mediainfo/MediaInfoModule.wasm'});
  const result=await mi.analyzeData(file.size,async(size,offset)=>new Uint8Array(await file.slice(offset,offset+size).arrayBuffer()));
  const fields=['Format','Format_Profile','CodecID','Width','Height','BitDepth','FrameRate','colour_primaries','transfer_characteristics','matrix_coefficients','colour_range','HDR_Format','HDR_Format_Profile','HDR_Format_Compatibility'];
  const tracks=(result.media?.track||[]).filter(t=>t['@type']==='Video').map(t=>Object.fromEntries(fields.map(k=>[k,t[k]??null])));
  self.postMessage({tracks});
 }catch{self.postMessage({error:'We could not read this file. Try an original MP4 or MOV video.'});}
 finally{mi?.close();}
};
