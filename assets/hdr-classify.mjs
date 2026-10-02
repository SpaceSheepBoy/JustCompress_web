export function classify(track){
 const transfer=String(track.transfer_characteristics||''), hdr=String(track.HDR_Format||'');
 const dolby=/Dolby Vision/i.test(hdr),pq=/PQ|2084/i.test(transfer),hlg=/HLG|ARIB.*B67/i.test(transfer);
 const sdr=/BT\.?709|BT\.?601|sRGB|IEC 61966|BT\.?470|SMPTE 170/i.test(transfer);
 if((pq||hlg||dolby)&&sdr)return {state:'uncertain',title:'Mixed HDR / SDR signals',detail:'The metadata contains conflicting signals. Do not treat this as a confirmed SDR file. Check the original recording before converting.'};
 if(dolby||pq||hlg)return {state:'hdr',title:dolby?'Dolby Vision detected':hlg?'HLG HDR detected':'PQ HDR detected',detail:'This file carries HDR metadata. A correctly tone-mapped SDR copy can improve compatibility when a receiving app or display does not handle HDR correctly.'};
 if(hdr)return {state:'uncertain',title:'HDR metadata needs review',detail:'HDR-related metadata was found, but this checker cannot confidently classify the transfer function.'};
 if(sdr)return {state:'sdr',title:'Tagged as SDR',detail:'The file has SDR transfer metadata. This does not prove that its colors are correct. If it already looks gray, use the original HDR recording; another conversion may not restore lost color.'};
 return {state:'unknown',title:'HDR / SDR not confirmed',detail:'The transfer metadata is missing or unrecognized. HEVC, 10-bit or BT.2020 alone does not prove that a file is HDR.'};
}
