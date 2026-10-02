const $=id=>document.getElementById(id);
const items=[];
let busy=false, outputURL;
const message=text=>{$('message').textContent=text;};
function controls(){ $('download').disabled=busy||!items.length; $('files').disabled=busy; $('demo').disabled=busy; }
function clearDownload(){if(outputURL){URL.revokeObjectURL(outputURL);outputURL=null;} $('save').hidden=true;}
function draw(){
 clearDownload();const canvas=$('canvas'),ctx=canvas.getContext('2d');
 if(!items.length){canvas.width=900;canvas.height=500;ctx.fillStyle='#f0edf5';ctx.fillRect(0,0,900,500);$('empty').hidden=false;$('dimensions').textContent='Your combined image appears here';controls();return;}
 $('empty').hidden=true;
 const layout=$('layout').value,gap=Number($('gap').value),cols=layout==='horizontal'?items.length:layout==='vertical'?1:Math.ceil(Math.sqrt(items.length)),rows=Math.ceil(items.length/cols);
 const cell=600,scale=Math.min(1,4096/(cols*cell+(cols+1)*gap),4096/(rows*cell+(rows+1)*gap));
 canvas.width=Math.round((cols*cell+(cols+1)*gap)*scale);canvas.height=Math.round((rows*cell+(rows+1)*gap)*scale);
 ctx.fillStyle=$('background').value;ctx.fillRect(0,0,canvas.width,canvas.height);
 items.forEach((item,i)=>{const ratio=Math.min(cell/item.img.width,cell/item.img.height),w=item.img.width*ratio*scale,h=item.img.height*ratio*scale,x=(gap+(i%cols)*(cell+gap))*scale+(cell*scale-w)/2,y=(gap+Math.floor(i/cols)*(cell+gap))*scale+(cell*scale-h)/2;ctx.drawImage(item.img,x,y,w,h);});
 $('dimensions').textContent=`${items.length} images · ${canvas.width} × ${canvas.height} px`;controls();
}
function list(){
 $('thumbnails').replaceChildren();
 items.forEach((item,i)=>{const li=document.createElement('li'),img=document.createElement('img');img.src=item.url;img.alt=item.name;li.append(img);
 const title=document.createElement('span');title.textContent=item.name;li.append(title);
 for(const [label,delta] of [['Move earlier',-1],['Move later',1],['Remove',0]]){const b=document.createElement('button');b.type='button';b.textContent=delta<0?'←':delta>0?'→':'×';b.setAttribute('aria-label',`${label}: ${item.name}`);b.disabled=busy||(delta<0&&i===0)||(delta>0&&i===items.length-1);b.onclick=()=>{if(busy)return;if(delta){[items[i],items[i+delta]]=[items[i+delta],items[i]];}else{URL.revokeObjectURL(item.url);items.splice(i,1);}list();draw();};li.append(b);}
 $('thumbnails').append(li);});
}
async function add(files){
 if(busy)return;busy=true;controls();list();let errors=[];
 for(const file of files){
  if(items.length>=12){errors.push('Maximum 12 images.');break;}
  if(!/^image\/(jpeg|png|webp)$/.test(file.type)){errors.push(`${file.name}: use JPG, PNG or WebP.`);continue;}
  if(file.size>20*1024*1024){errors.push(`${file.name}: maximum 20 MB per image.`);continue;}
  if(items.reduce((n,x)=>n+x.size,0)+file.size>80*1024*1024){errors.push('Maximum 80 MB total.');break;}
  let url=URL.createObjectURL(file);
  try{const img=new Image();img.src=url;await img.decode();if(img.width*img.height>40000000)throw Error('Image exceeds 40 megapixels.');items.push({img,url,name:file.name,size:file.size});}catch(e){URL.revokeObjectURL(url);errors.push(`${file.name}: could not read this image (up to 40 megapixels).`);}
 }
 busy=false;$('files').value='';list();draw();message(errors.join(' ')||'Ready. Choose a layout, then download.');
}
$('files').onchange=e=>add([...e.target.files]);
for(const id of ['layout','gap','background'])$(id).oninput=draw;
$('format').onchange=clearDownload;
$('drop').ondragover=e=>{e.preventDefault();};$('drop').ondrop=e=>{e.preventDefault();add([...e.dataTransfer.files]);};
$('demo').onclick=async()=>{
 if(busy)return;
 busy=true;controls();
 try {
 const names=['Sunrise','Mountains','Evening'];
 const files=await Promise.all(names.map(async(name,i)=>{const response=await fetch(`/assets/combine-demo-${i+1}.svg`);const blob=await response.blob();const url=URL.createObjectURL(blob);try{const img=new Image();img.src=url;await img.decode();const c=document.createElement('canvas');c.width=600;c.height=600;c.getContext('2d').drawImage(img,0,0,600,600);return new File([await new Promise(r=>c.toBlob(r,'image/png'))],`${name} demo.png`,{type:'image/png'});}finally{URL.revokeObjectURL(url);}}));
 busy=false; await add(files);message('Example illustrations loaded. Add your own photos whenever you’re ready.');
 } catch (_) {message('Could not load examples. Please add your own JPG or PNG images.');}
 finally {busy=false;controls();list();}
};
$('download').onclick=()=>{
 if(busy||!items.length)return;
 const mime=$('format').value;busy=true;controls();list();message('Preparing your image…');
 $('canvas').toBlob(blob=>{busy=false;controls();list();if(!blob){message('Could not export. Try fewer images.');return;}clearDownload();outputURL=URL.createObjectURL(blob);const save=$('save');save.href=outputURL;save.download=`combined-photos.${mime==='image/png'?'png':'jpg'}`;save.hidden=false;save.textContent=`Save image · ${(blob.size/1024).toFixed(0)} KB`;save.click();message('Your image is ready. If the download did not start, tap Save image.');},mime,.92);
};
draw();
