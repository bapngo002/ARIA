import * as T from './vendor/three.module.min.js';
import {GLTFLoader} from './vendor/GLTFLoader.js';
import {OrbitControls} from './vendor/OrbitControls.js';
const viewport=document.getElementById('viewport'),loading=document.getElementById('loading');
try {
  const renderer=new T.WebGLRenderer({alpha:true,antialias:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));
  renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;
  renderer.setClearColor(0,0);viewport.append(renderer.domElement);
  const scene=new T.Scene(),camera=new T.PerspectiveCamera(32,1,.01,30);
  const controls=new OrbitControls(camera,renderer.domElement);
  controls.enableDamping=true;controls.minDistance=.25;controls.maxDistance=4;
  function front(){camera.position.set(0,1.46,.82);controls.target.set(0,1.46,0);controls.update();}
  front();document.getElementById('front').onclick=front;
  scene.add(new T.HemisphereLight(0xfff2e6,0x6e577b,1.4));
  const light=new T.DirectionalLight(0xffe9dc,2);light.position.set(-2,3,4);scene.add(light);
  const fill=new T.DirectionalLight(0xcbd8ff,.7);fill.position.set(2,1,2);scene.add(fill);
  const gltf=await new GLTFLoader().loadAsync('/aria-concept-01-draft.glb');scene.add(gltf.scene);
  const mixer=new T.AnimationMixer(gltf.scene);
  for(const clip of gltf.animations)mixer.clipAction(clip).play();
  renderer.domElement.dataset.clips=String(gltf.animations.length);
  loading.hidden=true;
  const resize=new ResizeObserver(()=>{const w=viewport.clientWidth,h=viewport.clientHeight;if(!w||!h)return;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();});resize.observe(viewport);
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const motion=document.getElementById('motion');motion.checked=!reduced.matches;
  let last=0,frames=0;
  function draw(ms){requestAnimationFrame(draw);if(document.hidden||ms-last<33)return;const dt=Math.min((ms-last)/1000,.06);last=ms;if(motion.checked)mixer.update(dt);controls.update();renderer.render(scene,camera);if(++frames%30===0)renderer.domElement.dataset.frames=String(frames);}
  requestAnimationFrame(draw);
} catch(error){loading.textContent='KhÃ´ng má»Ÿ Ä‘Æ°á»£c báº£n 3D. Báº¡n cÃ³ thá»ƒ táº£i file GLB bÃªn dÆ°á»›i Ä‘á»ƒ xem trong Blender.';}
