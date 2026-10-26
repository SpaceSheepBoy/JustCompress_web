import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
const source = readFileSync(new URL('../assets/product-depth.js',import.meta.url),'utf8');
const {estimateAudio,videoWorkflow}=await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'));
assert.equal(estimateAudio(60,128,25).sizeMB,57.6);
assert.ok(Math.abs(estimateAudio(60,128,25).ceilingKbps-55.5555555556)<1e-8);
assert.equal(estimateAudio(1,64,1).sizeMB,.48);
assert.equal(estimateAudio(2,64,1).sizeMB,2*estimateAudio(1,64,1).sizeMB);
for (const args of [[0,128,25],[60,Infinity,25],[60,128,NaN],[-1,128,25],[60,500,25],[60,128,0],[10081,128,25]]) assert.equal(estimateAudio(...args),null);
for (const source of ['hdr','log','hevc','sdr']) {
 for (const goal of ['sdr','h264','fps','audio']) assert.equal(videoWorkflow(source,goal).length,2);
 assert.equal(videoWorkflow(source,'audio')[0],'Extract Audio');
}
assert.match(videoWorkflow('sdr','sdr')[0],/already SDR/);
assert.match(videoWorkflow('hevc','sdr')[1],/not needed/);
assert.match(videoWorkflow('hdr','sdr')[0],/Rec.709/);
assert.match(videoWorkflow('log','h264')[1],/standard-color SDR/);
assert.match(videoWorkflow('sdr','h264')[1],/keep the original/);
assert.equal(videoWorkflow('unknown','sdr'),null);
console.log('PASS: audio units, attachment ceiling, scaling, invalid bounds and all 16 video choices');
