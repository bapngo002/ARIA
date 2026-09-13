import * as T from './vendor/three.module.min.js';
import {GLTFLoader} from './vendor/GLTFLoader.js';
import {VRMLoaderPlugin, VRMUtils} from './vendor/three-vrm.module.min.js';

// Licensed pixiv sample, not a reconstruction of the owner's photograph.
let pending;
export function start() {
  if (!pending) pending = createAvatar().catch(error => {pending=null; throw error;});
  return pending;
}
async function createAvatar() {
  const dial=document.getElementById('dial');
  dial.dataset.webgl='loading';
  const renderer=new T.WebGLRenderer({alpha:true,antialias:true,powerPreference:'low-power'});
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.25));
  renderer.setClearColor(0,0);
  renderer.outputColorSpace=T.SRGBColorSpace;
  const canvas=renderer.domElement;
  canvas.setAttribute('role','img');
  canvas.setAttribute('aria-label','Nhân vật nữ anime 3D');
  const scene=new T.Scene();
  const camera=new T.PerspectiveCamera(28,1,.01,20);
  scene.add(new T.HemisphereLight(0xfff4ec,0xc7b4c9,1.25));
  const key=new T.DirectionalLight(0xffecdf,1.1);key.position.set(-3,2,5);scene.add(key);
  const fill=new T.DirectionalLight(0xe7e3ff,.7);fill.position.set(3,1,4);scene.add(fill);
  const rim=new T.DirectionalLight(0xe5c3e9,.65);rim.position.set(1,1,-2);scene.add(rim);
  const loader=new GLTFLoader();loader.register(parser=>new VRMLoaderPlugin(parser));
  let vrm;
  try {
    const gltf=await loader.loadAsync('/models/aria-sample.vrm');
    vrm=gltf.userData.vrm;
    if(!vrm) throw new Error('Missing VRM character');
  } catch(error) {renderer.dispose();throw error;}
  VRMUtils.rotateVRM0(vrm);
  scene.add(vrm.scene);
  // Runtime styling keeps the source model and its embedded metadata unchanged.
  const styled=new Set();
  const portraitMaterials=new Map();
  const sourceGeometries=new Set();
  // Small smooth deformations calibrated only to this pinned sample's coordinates.
  // Apply the same function to every expression so blink/smile shapes stay aligned.
  function softenFace(geometry) {
    sourceGeometries.add(geometry);
    const softened=geometry.clone(),base=geometry.attributes.position;
    const deform=(x,y,z)=>{
      const chin=Math.exp(-Math.pow(x/.033,2))*Math.exp(-Math.pow((y-1.352)/.015,2));
      const nose=Math.exp(-Math.pow(x/.012,2)-Math.pow((y-1.409)/.013,2));
      return [x,y+.007*chin,z-.006*nose*Math.max(0,Math.min(1,(z-.075)/.014))];
    };
    for(let i=0;i<base.count;i++)softened.attributes.position.setXYZ(i,...deform(base.getX(i),base.getY(i),base.getZ(i)));
    for(let m=0;m<(geometry.morphAttributes.position||[]).length;m++) {
      const source=geometry.morphAttributes.position[m],dest=softened.morphAttributes.position[m];
      for(let i=0;i<base.count;i++) {
        const origin=[base.getX(i),base.getY(i),base.getZ(i)];
        const values=[source.getX(i),source.getY(i),source.getZ(i)];
        const point=deform(...values.map((v,k)=>geometry.morphTargetsRelative?v+origin[k]:v));
        const zero=deform(...origin);
        dest.setXYZ(i,...point.map((v,k)=>geometry.morphTargetsRelative?v-zero[k]:v));
      }
    }
    softened.computeVertexNormals();softened.computeBoundingBox();softened.computeBoundingSphere();
    return softened;
  }
  function refineMaterial(mat) {
    if(!mat || mat.isOutline)return mat;
    const skin=mat.name==='Face_00_SKIN'||mat.name==='Body_00_SKIN';
    const eye=mat.name==='EyeIris_00_EYE'||mat.name==='EyeWhite_00_EYE';
    if(!skin&&!eye)return mat;
    if(portraitMaterials.has(mat))return portraitMaterials.get(mat);
    // Preserve the authored UV artwork and morph-target mesh; shade its real contours.
    const refined=new T.MeshPhysicalMaterial({
      name:mat.name+' portrait',map:mat.map,color:mat.color.clone(),
      side:mat.side,transparent:mat.transparent,opacity:mat.opacity,alphaTest:mat.alphaTest,
      roughness:eye?.20:.82,metalness:0,
      clearcoat:eye?.7:0,clearcoatRoughness:eye?.12:.7,
      specularIntensity:eye?.8:.15,
      emissive:skin?new T.Color(0xb68b78):new T.Color(0x000000),
      emissiveMap:skin?mat.map:null,emissiveIntensity:skin?.16:0
    });
    portraitMaterials.set(mat,refined);return refined;
  }
  vrm.scene.traverse(object=>{
    if(object.geometry && !Array.isArray(object.material) && object.material?.name==='Face_00_SKIN')object.geometry=softenFace(object.geometry);
    for(const mat of (Array.isArray(object.material)?object.material:[object.material])) {
      if(!mat||styled.has(mat))continue;styled.add(mat);
      if(mat.map)mat.map.anisotropy=Math.min(4,renderer.capabilities.getMaxAnisotropy());
      if(mat.name.startsWith('Tops_')) {
        mat.color?.set(0xb4a3dc);
        mat.shadeColorFactor?.set(0x8171a2);
      }
      if(mat.name.includes('HAIR')) {
        mat.color?.set(0xe5c2c8);
        mat.shadeColorFactor?.set(0x9e7b8e);
      }
    }
    if(object.material)object.material=Array.isArray(object.material)?object.material.map(refineMaterial):refineMaterial(object.material);
  });
  // Lower arms from the author's neutral T pose before portrait framing.
  for(const [name,z] of [['leftUpperArm',-1.15],['rightUpperArm',1.15]]) {
    const bone=vrm.humanoid.getNormalizedBoneNode(name);if(bone) bone.rotation.z=z;
  }
  vrm.update(0);
  const head=vrm.humanoid.getNormalizedBoneNode('head');
  const neck=vrm.humanoid.getNormalizedBoneNode('neck');
  const headPosition=new T.Vector3();head.getWorldPosition(headPosition);
  const ornament=new T.Group();scene.add(ornament);
  const flower=new T.Group();flower.position.set(.093,.137,.055);flower.rotation.z=-.3;ornament.add(flower);
  const petalMaterial=new T.MeshStandardMaterial({color:0xffdfa8,roughness:.4,metalness:.25});
  const petalGeometry=new T.SphereGeometry(1,16,12);
  for(let i=0;i<5;i++) {
    const a=i*Math.PI*2/5,petal=new T.Mesh(petalGeometry,petalMaterial);
    petal.position.set(Math.cos(a)*.009,Math.sin(a)*.009,0);petal.scale.set(.008,.005,.003);
    petal.rotation.z=a;flower.add(petal);
  }
  const jewel=new T.Mesh(petalGeometry,new T.MeshStandardMaterial({color:0x51baa9,metalness:.3,roughness:.2}));
  jewel.scale.set(.005,.005,.004);jewel.position.z=.003;flower.add(jewel);
  camera.position.set(0,headPosition.y+.063,.75);
  camera.lookAt(0,headPosition.y+.063,0);
  const target=new T.Object3D();scene.add(target);target.position.set(0,headPosition.y,3);
  if(vrm.lookAt) vrm.lookAt.target=target;
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const size=new T.Vector2();
  let last=0,nextBlink=2.5,blinkAt=-10,nextGaze=0,gazeX=0,gazeY=headPosition.y,frames=0,failed=false;
  let nextGesture=0,gestureStart=-10,gestureKind=0,gestureDuration=4.2;
  let pointerUntil=0,pointerX=0,pointerY=0;
  const onPointerMove=event=>{
    const bounds=dial.getBoundingClientRect();
    pointerX=((event.clientX-bounds.left)/bounds.width-.5)*1.2;
    pointerY=headPosition.y+(.5-(event.clientY-bounds.top)/bounds.height)*.7;
    pointerUntil=performance.now()/1000+2;
  };
  dial.addEventListener('pointermove',onPointerMove,{passive:true});
  const expressionValues={happy:0,sad:0,angry:0,relaxed:0,surprised:0};
  const dispose=()=>{dial.removeEventListener('pointermove',onPointerMove);VRMUtils.deepDispose(vrm.scene);VRMUtils.deepDispose(ornament);for(const original of portraitMaterials.keys())original.dispose();for(const geometry of sourceGeometries)geometry.dispose();renderer.dispose();canvas.remove();};
  const fail=()=>{failed=true;pending=null;dispose();document.dispatchEvent(new Event('aria-3d-error'));};
  canvas.addEventListener('webglcontextlost',event=>{event.preventDefault();fail();},{once:true});
  function animate(ms) {
    if(failed)return;
    requestAnimationFrame(animate);
    if(ms-last<33||document.hidden||dial.dataset.avatar!=='three')return;
    const slot=document.getElementById(document.getElementById('standby').hidden?'main-3d':'standby-3d');
    if(!slot.getClientRects().length)return;
    if(canvas.parentElement!==slot)slot.replaceChildren(canvas);
    const width=Math.round(slot.clientWidth),height=Math.round(slot.clientHeight);
    if(!width||!height)return;
    renderer.getSize(size);
    if(size.x!==width||size.y!==height){renderer.setSize(width,height,false);camera.aspect=width/height;camera.updateProjectionMatrix();}
    const dt=Math.min((ms-last)/1000,.05);last=ms;
    const t=ms/1000,moving=!reduced.matches,ease=moving?1-Math.exp(-dt*6):1;
    const expr=dial.dataset.expression||'happy';
    const idle=dial.dataset.state==='idle';
    if(moving&&idle&&t>nextGesture){gestureStart=t;gestureKind=(gestureKind+1)%4;gestureDuration=3.5+Math.random()*1.5;nextGesture=t+gestureDuration+3+Math.random()*4;}
    const progress=Math.min(1,Math.max(0,(t-gestureStart)/gestureDuration));
    const gesture=moving&&idle?Math.sin(progress*Math.PI)**2:0;
    const smile=gestureKind===2?gesture:0;
    if(moving&&t>nextGaze){gazeX=(Math.random()-.5)*.65;gazeY=headPosition.y+(Math.random()-.5)*.22;nextGaze=t+2+Math.random()*3;}
    if(moving&&t>nextBlink){blinkAt=t;nextBlink=t+3+Math.random()*4;}
    const blink=moving?Math.max(0,1-Math.abs((t-blinkAt-.105)/.105)):0;
    head.rotation.y=T.MathUtils.lerp(head.rotation.y,moving?Math.sin(t*.48)*.035+(gestureKind===0?gesture*.16:0):0,ease);
    head.rotation.z=T.MathUtils.lerp(head.rotation.z,expr==='thinking'?-.07:moving?Math.sin(t*.64)*.012+(gestureKind===1?-gesture*.09:0):0,ease);
    head.rotation.x=T.MathUtils.lerp(head.rotation.x,moving?Math.sin(t*.8)*.012+(gestureKind===3?gesture*Math.sin(progress*Math.PI*4)*.05:0):0,ease);
    if(neck)neck.rotation.x=moving?Math.sin(t*1.4)*.008:0;
    target.position.x=T.MathUtils.lerp(target.position.x,moving?(t<pointerUntil?pointerX:gazeX):0,ease);
    target.position.y=T.MathUtils.lerp(target.position.y,moving?(t<pointerUntil?pointerY:gazeY):headPosition.y,ease);
    const chosen={happy:'happy',sad:'sad',angry:'angry',thinking:'relaxed',listening:'surprised',normal:'relaxed'}[expr];
    for(const name of Object.keys(expressionValues)){
      const value=(name===chosen?(name==='happy'?.12:name==='surprised'?.18:.2):0)+(name==='happy'&&['normal','happy'].includes(expr)?smile*.28:0);
      expressionValues[name]=T.MathUtils.lerp(expressionValues[name],value,ease);
      vrm.expressionManager.setValue(name,expressionValues[name]);
    }
    vrm.expressionManager.setValue('blink',blink);
    // State-driven speaking motion only; not phoneme or audio-synchronized lip sync.
    vrm.expressionManager.setValue('aa',moving&&dial.dataset.state==='speaking'?.12+.13*Math.sin(t*12):0);
    try {vrm.update(moving?dt:0);head.getWorldPosition(ornament.position);head.getWorldQuaternion(ornament.quaternion);renderer.render(scene,camera);}
    catch(error){fail();return;}
    dial.dataset.webgl='ready';
    if(++frames%30===0)canvas.dataset.frames=String(frames);
  }
  requestAnimationFrame(animate);
}
