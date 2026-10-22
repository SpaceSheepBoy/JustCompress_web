const vm=require('node:vm'),fs=require('node:fs'),assert=require('node:assert/strict');
const source=fs.readFileSync(require('node:path').join(__dirname, '../assets/posthog-init.js'),'utf8');
function run({stored=null,gpc=false,dnt=false}={}) {
 const requests=[],events=[],elements=[],store=new Map(stored?[['spacesheep.analytics.v1',stored]]:[]);let config;
 function el(tag){const e={tag,hidden:false,children:[],listeners:{},appendChild(c){this.children.push(c);return c},setAttribute(){},addEventListener(k,v){this.listeners[k]=v}};elements.push(e);return e;}
 const ph={opt_in_capturing(){},opt_out_capturing(){events.push('opt-out')},capture(name,properties){const event=config.before_send({event:name,properties});if(event)events.push(event)}};
 const ctx={navigator:{globalPrivacyControl:gpc,doNotTrack:dnt?'1':'0'},location:{hostname:'justcaptions.com',origin:'https://justcaptions.com',href:'https://justcaptions.com/?code=SECRET#TOKEN'},URL,localStorage:{getItem:k=>store.get(k),setItem:(k,v)=>store.set(k,v)},window:{posthog:{init(token,options){assert.match(token,/^phc_/);config=options;options.loaded(ph);return ph}}},document:{createElement:el,head:{appendChild(e){if(e.tag==='script'){requests.push(e.src);e.onload()}}},body:{appendChild(){}},addEventListener(){}},console};
 vm.runInNewContext(source,ctx);return {requests,events,elements,get config(){return config}};
}
let r=run();assert.equal(r.requests.length,0,'No SDK request before consent');
r.elements.find(e=>e.textContent==='Reject').listeners.click();assert.equal(r.requests.length,0,'No SDK request after rejection');
r=run({gpc:true});assert.equal(r.elements.length,0,'GPC disables analytics');
r=run({dnt:true});assert.equal(r.requests.length,0,'DNT disables analytics');
r=run({stored:'allow'});assert.equal(r.requests.length,1);assert.equal(r.events[0].event,'$pageview');assert.equal(r.events[0].properties.$current_url,'https://justcaptions.com/');assert.equal(r.events[0].properties.site,'justcaptions');
const cleaned=r.config.before_send({properties:{$current_url:'https://justcaptions.com/?email=private#secret',$initial_referrer:'https://example.com/?token=secret',utm_source:'private',$set:{email:'private'}}});
assert.equal(cleaned.properties.$current_url,'https://justcaptions.com/');assert.equal(cleaned.properties.$initial_referrer,'https://example.com/');assert.equal(cleaned.properties.utm_source,undefined);assert.equal(cleaned.properties.$set,undefined);
r.elements.find(e=>e.textContent==='Reject').listeners.click();assert.equal(r.config.before_send({properties:{}}),null,'Withdrawal stops sends');
assert.equal(r.config.disable_session_recording,true);assert.equal(r.config.autocapture,false);
console.log('PASS: default/rejected consent, GPC/DNT, opt-in pageview, site label, URL/property sanitizing, withdrawal and disabled replay/autocapture');
