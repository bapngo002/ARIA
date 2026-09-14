'use strict';
let token = '', current = null, lastHistory = '', lastMemories = '', polling = false, lastServerError = '', disconnected = false;
const $ = id => document.getElementById(id);
function setAvatarStyle(style) {
  style = ['three','animated','portrait'].includes(style) ? style : 'three';
  $('dial').dataset.avatar = style;
  $('avatar-style').value = $('dial').dataset.avatar;
  $('expression').disabled = style === 'portrait';
  $('avatar-info').textContent = style === 'three' ? 'Nhân vật anime mẫu của pixiv: quay đầu, chớp mắt và biểu cảm. Chưa phải khuôn mặt trong ảnh bạn chọn.' : style === 'animated' ? 'Avatar có chuyển động mắt và biểu cảm theo trạng thái app.' : 'Chân dung bạn chọn · ảnh tĩnh.';
  if (style === 'three') import('/avatar3d.js').then(module => module.start()).catch(avatar3dFailed);
}
function avatar3dFailed() {
  $('dial').dataset.webgl = 'unavailable';
  if ($('dial').dataset.avatar !== 'three') return;
  setAvatarStyle('portrait');
  $('avatar-info').textContent = 'Không mở được nhân vật 3D trên trình duyệt này. Đang hiển thị ảnh bạn chọn.';
}
document.addEventListener('aria-3d-error', avatar3dFailed);
let requestedStyle;
try { requestedStyle = localStorage.getItem('aria-avatar-style-v2'); } catch (_) { requestedStyle = null; }
// Tạm thời: dùng ngay mẫu khuôn mặt đang có trong app, tránh bị ảnh tĩnh (portrait) ép mặc định.
setAvatarStyle(requestedStyle === 'animated' ? 'animated' : 'three');
$('avatar-style').onchange = () => {
  setAvatarStyle($('avatar-style').value);
  try { localStorage.setItem('aria-avatar-style-v2', $('avatar-style').value); } catch (_) {}
};
// Continuous poses: eyelid openness, inner eyebrow lift, smile depth, mouth width.
const expressions = {happy:[.86,-1,24,41],normal:[1,0,13,32],sad:[.78,-12,-15,30],angry:[.67,12,-5,30],thinking:[.88,-6,3,23],listening:[1.12,-8,7,24]};
let restingExpression = 'happy';
try { const saved = localStorage.getItem('aria-expression'); if (['happy','normal','sad','angry'].includes(saved)) restingExpression = saved; } catch (_) {}
function paintFace(state = 'idle') {
  const name = {thinking:'thinking',listening:'listening',speaking:'happy',stopping:'normal',error:'sad'}[state] || restingExpression;
  faceTarget = expressions[name];
  $('dial').dataset.expression = name;
  document.querySelectorAll('.robot-face').forEach(face => { face.dataset.expression = name; });
}
let faceTarget = expressions.happy, facePose = [...faceTarget];
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
function svgNode(tag, attrs = {}, children = []) {
  const node = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [key,value] of Object.entries(attrs)) node.setAttribute(key,value);
  node.append(...children); return node;
}
const faceViews = [...document.querySelectorAll('.robot-face')].map((face,index) => {
  const irisId = 'iris-' + index, whiteId = 'white-' + index;
  const skinId='skin-'+index, blushId='blush-'+index, mouthId='mouth-'+index, clipId='mouth-clip-'+index;
  const hairId='hair-'+index;
  const gradient = (id, stops) => svgNode('radialGradient',{id,cx:'35%',cy:'28%',r:'75%'},stops.map(([offset,color])=>svgNode('stop',{offset,'stop-color':color})));
  const defs = svgNode('defs',{},[
    gradient(whiteId,[['0%','#fffdf8'],['58%','#fff2e6'],['85%','#ead5c8'],['100%','#c3a6a1']]),
    gradient(irisId,[['0%','#d9c995'],['32%','#a58a58'],['67%','#715333'],['88%','#483428'],['100%','#29232a']]),
    gradient(skinId,[['0%','#fff0dd'],['30%','#f6d4bb'],['65%','#edba9e'],['87%','#ce947f'],['100%','#ac7069']]),
    gradient(hairId,[['0%','#a67466'],['25%','#715047'],['53%','#48323a'],['85%','#2b2331'],['100%','#191d2b']]),
    gradient(blushId,[['0%','#ff9b9a'],['45%','#ed7b91'],['100%','#ed7b9100']]),
    gradient(mouthId,[['0%','#492c58'],['50%','#281d38'],['100%','#100f25']])
  ]);
  const features = svgNode('g',{'class':'features'});
  const headShape='M84 26 C106 7 193 7 216 26 Q239 50 235 91 L229 130 Q221 152 194 174 Q171 192 150 194 Q129 192 106 174 Q79 152 71 130 L65 91 Q61 50 84 26 Z';
  features.append(
    svgNode('path',{d:'M66 37 C71 2 111 -5 150 0 C197 -7 233 10 240 45 C250 89 230 134 254 173 Q246 190 222 196 Q206 185 203 157 L95 157 Q93 185 76 197 Q52 190 45 174 C66 132 49 89 66 37 Z',fill:`url(#${hairId})`}),
    svgNode('path',{d:'M67 73 C48 116 85 139 64 180 Q86 167 76 132 Q66 109 76 87 M231 72 C250 114 219 141 239 178 Q215 168 225 135 Q235 103 222 84',fill:'#a07569',opacity:'.2'}),
    svgNode('path',{d:headShape,transform:'translate(0 6)',fill:'#020a16',opacity:'.45'}),
    svgNode('ellipse',{cx:65,cy:94,rx:12,ry:23,fill:'#cb8a70'}),
    svgNode('ellipse',{cx:235,cy:94,rx:12,ry:23,fill:'#b77865'}),
    svgNode('path',{d:headShape,fill:`url(#${skinId})`,stroke:'#efc7a7','stroke-opacity':'.25','stroke-width':1}),
    svgNode('path',{d:'M64 91 C48 52 64 17 89 10 C124 -4 168 -3 192 9 C230 10 246 38 238 78 L230 106 Q221 76 220 47 Q187 43 171 22 C149 49 103 45 84 67 Q75 83 72 114 Z',fill:`url(#${hairId})`}),
    svgNode('path',{d:'M65 62 C64 15 131 2 163 13 C124 10 86 29 65 62 Z M178 13 Q231 9 235 65 C226 35 204 34 178 13 Z',fill:'#d49c82',opacity:'.17'}),
    svgNode('path',{d:'M71 55 C91 21 130 12 158 14 M75 45 Q104 17 140 14 M187 20 Q221 29 229 52',fill:'none',stroke:'#ddb198','stroke-width':'.8','stroke-linecap':'round',opacity:'.3'}),
    svgNode('ellipse',{cx:88,cy:123,rx:20,ry:11,fill:`url(#${blushId})`,opacity:'.33'}),
    svgNode('ellipse',{cx:212,cy:123,rx:20,ry:11,fill:`url(#${blushId})`,opacity:'.33'}),
    svgNode('path',{d:'M151 88 Q145 104 142 113 Q143 121 151 122 Q160 120 158 114 Q154 102 151 88 Z',fill:'#c58b79',opacity:'.25'}),
    svgNode('ellipse',{cx:149,cy:113,rx:6,ry:4,fill:'#ffe9d1',opacity:'.65'}),
    svgNode('path',{d:'M142 119 Q145 121 147 120 M155 120 Q159 121 160 118',fill:'none',stroke:'#b87e70','stroke-width':1.2,'stroke-linecap':'round'}),
    svgNode('ellipse',{cx:70,cy:125,rx:2.2,ry:5.5,fill:'#e9c892'}),
    svgNode('ellipse',{cx:230,cy:125,rx:2.2,ry:5.5,fill:'#d5b084'})
  );
  const eyes = [103,197].map(x => {
    const almond='M-29 0 C-15 -24 15 -24 29 0 C14 19 -14 19 -29 0 Z';
    const eyeClipId=`eye-clip-${index}-${x}`;
    defs.append(svgNode('clipPath',{id:eyeClipId},[svgNode('path',{d:almond})]));
    const pupil = svgNode('g',{},[
      svgNode('circle',{r:17,fill:`url(#${irisId})`}),
      svgNode('circle',{r:13.5,fill:'none',stroke:'#e7c694','stroke-width':'.6',opacity:'.35'}),
      svgNode('circle',{r:9,fill:'#201a21'}),
      svgNode('circle',{cx:-5,cy:-6,r:4,fill:'#fff','fill-opacity':'.95'}),
      svgNode('circle',{cx:6,cy:6,r:1.8,fill:'#c6fcff','fill-opacity':'.7'})
    ]);
    const eye = svgNode('g',{'class':'living-eye'},[
      svgNode('path',{d:'M-30 -2 C-13 -29 15 -29 31 -2',fill:'none',stroke:'#b78282','stroke-width':6,opacity:'.25'}),
      svgNode('path',{d:almond,fill:`url(#${whiteId})`}),svgNode('g',{'clip-path':`url(#${eyeClipId})`},[pupil]),
      svgNode('path',{d:'M-29 0 C-15 -24 15 -24 29 0',fill:'none',stroke:'#4a333b','stroke-width':2.2,'stroke-linecap':'round'}),
      svgNode('path',{d:x<150 ? 'M-26 -4 L-32 -9 M-22 -9 L-27 -15 M-17 -13 L-20 -18' : 'M26 -4 L32 -9 M22 -9 L27 -15 M17 -13 L20 -18',fill:'none',stroke:'#46303c','stroke-width':1.6,'stroke-linecap':'round'}),
      svgNode('path',{d:'M-25 4 Q0 24 25 4',fill:'none',stroke:'#c08981','stroke-width':1,opacity:'.55'})
    ]);
    const brow = svgNode('path',{'class':'eyebrow'});
    features.append(eye,brow); return {x,eye,pupil,brow};
  });
  const mouth = svgNode('path',{'class':'volume-mouth',fill:`url(#${mouthId})`});
  const mouthClip = svgNode('path');
  defs.append(svgNode('clipPath',{id:clipId},[mouthClip]));
  const tongue = svgNode('ellipse',{cx:150,cy:163,rx:20,ry:8,fill:'#ef8ca9','clip-path':`url(#${clipId})`});
  features.append(mouth,tongue); face.replaceChildren(defs,features);
  return {face,features,eyes,mouth,mouthClip,tongue};
});
let lastFaceFrame=0, nextBlink=performance.now()+3500, blinkStart=-1000, nextLook=0, gaze=[0,0], gazeTarget=[0,0];
function animateFace(now) {
  requestAnimationFrame(animateFace);
  if (document.hidden || now-lastFaceFrame < 32) return;
  const dt=Math.min(64,now-lastFaceFrame); lastFaceFrame=now;
  const still=reducedMotion.matches, blend=still ? 1 : 1-Math.exp(-dt/160);
  facePose=facePose.map((value,i)=>value+(faceTarget[i]-value)*blend);
  if (now>nextLook) { gazeTarget=Math.random()<.4 ? [0,0] : [(Math.random()-.5)*10,(Math.random()-.5)*6]; nextLook=now+2200+Math.random()*2800; }
  gaze=gaze.map((value,i)=>still ? 0 : value+(gazeTarget[i]-value)*blend*.6);
  if (now>nextBlink) { blinkStart=now; nextBlink=now+3200+Math.random()*3800; }
  const blinkTime=now-blinkStart;
  const blink=still || blinkTime>210 ? 1 : 1-.96*Math.sin(Math.PI*blinkTime/210);
  const [openness,browLift,smile,rawWidth]=facePose;
  const width=rawWidth*.8;
  for (const view of faceViews) {
    if (!view.face.getClientRects().length) continue;
    view.features.setAttribute('transform',`translate(0 ${still ? 0 : Math.sin(now/1700)*1.2})`);
    for (const [i,{x,eye,pupil,brow}] of view.eyes.entries()) {
      eye.setAttribute('transform',`translate(${x} 82) scale(.94 ${openness*blink})`);
      pupil.setAttribute('transform',`translate(${gaze[0]} ${gaze[1]})`);
      const outer=i===0 ? x-23 : x+23, inner=i===0 ? x+23 : x-23;
      brow.setAttribute('d',`M${outer} 47 Q${x} ${39+browLift/2} ${inner} ${47+browLift}`);
    }
    const speech=!still && current?.state==='speaking' ? Math.sin(now/130)*3 : 0;
    const curve=smile*.3, opening=Math.max(1,smile*.4+speech);
    const mouthPath=`M${150-width} 143 C${150-width*.55} ${143+curve} ${150+width*.55} ${143+curve} ${150+width} 143 C${150+width*.65} ${143+curve+opening} ${150-width*.65} ${143+curve+opening} ${150-width} 143 Z`;
    view.mouth.setAttribute('d',mouthPath); view.mouthClip.setAttribute('d',mouthPath);
    view.tongue.setAttribute('cy',143+curve+opening*.78);
  }
}
requestAnimationFrame(animateFace);
let lastInteraction = performance.now();
const STANDBY_AFTER_MS = 30000;
function showStandby(visible) {
  $('standby').hidden = !visible;
  $('main-interface').hidden = visible;
  if (visible) $('standby').focus({preventScroll:true});
  else document.querySelector('[data-page].selected').focus({preventScroll:true});
  lastInteraction = performance.now();
}
function temperature(state) {
  const bme = state?.sensors?.status === 'fresh' ? state.sensors.sample?.bme280 : null;
  const valid = bme?.status === 'ok' && typeof bme.temperature_c === 'number' && Number.isFinite(bme.temperature_c);
  $('standby-temperature').textContent = valid ? bme.temperature_c.toFixed(1) + ' °C' : '— °C';
  $('standby-temperature').setAttribute('aria-label', valid ? 'Nhiệt độ phòng ' + bme.temperature_c.toFixed(1) + ' độ C' : 'Chưa có nhiệt độ mới');
}
const labels = {idle:'Tôi đang ở đây',thinking:'Đang nghĩ…',listening:'Đang nghe trong 5 giây…',speaking:'Đang trả lời…',stopping:'Đang dừng…',error:'Cần kiểm tra một chút'};
function notice(text) { $('notice').textContent = text; }
async function action(name, body = {}) {
  try {
    const response = await fetch('/api/' + name, {method:'POST', headers:{'Content-Type':'application/json','X-ARIA-Token':token}, body:JSON.stringify(body), signal:AbortSignal.timeout(8000)});
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Không thực hiện được yêu cầu.');
    notice(''); await refresh(); return true;
  } catch (error) { notice(error.message); return false; }
}
function render(state) {
  current = state; token = state.token;
  $('dial').dataset.state = state.state;
  paintFace(state.state);
  $('status').textContent = labels[state.state] || state.state;
  const busy = ['listening','thinking','speaking','stopping'].includes(state.state);
  temperature(state);
  $('rest').disabled = busy;
  if (busy) {
    if (!$('standby').hidden) showStandby(false);
    lastInteraction = performance.now();
  }
  for (const id of ['send','provider','persona','speak','reset']) $(id).disabled = busy;
  $('listen').disabled = busy || !state.voice.listen;
  $('stop').disabled = !busy;
  $('provider').value = state.settings.provider;
  $('persona').value = state.settings.persona;
  $('speak').checked = state.settings.speak;
  $('mode').textContent = {offline:'CỤC BỘ',openai:'CHATGPT',gemini:'GEMINI'}[state.settings.provider];
  $('provider-info').textContent = state.settings.provider === 'offline' ? 'Không gửi dữ liệu lên mạng. Trả lời giờ và trạng thái app.' : state.providers[state.settings.provider] ? 'Đã có cấu hình. Kết nối thật sẽ được kiểm tra khi gửi câu hỏi.' : 'Chưa cấu hình khóa API và tên model trên Pi.';
  $('voice-info').textContent = `Micro: ${state.voice.listen ? 'đã có cấu hình' : 'chưa cấu hình'}. Loa: ${state.voice.speak ? 'đã có cấu hình' : 'chưa cấu hình'}. Chưa bật nghe liên tục.`;
  if (state.sensors.detail) $('sensors').textContent = state.sensors.detail;
  else {
    const sample = state.sensors.sample, bme = sample.bme280 || {}, ina = sample.ina260 || {};
    const number = (value, unit) => typeof value === 'number' && Number.isFinite(value) ? value.toFixed(1) + unit : 'chưa có';
    $('sensors').textContent = [
      bme.status === 'ok' ? `Nhiệt độ ${number(bme.temperature_c,'°C')} · Độ ẩm ${number(bme.humidity_percent,'%')}` : 'Nhiệt độ / độ ẩm: chưa có số đo hợp lệ',
      ina.status === 'ok' ? `Nhánh INA260: ${number(ina.voltage_v,'V')} · ${number(ina.power_w,'W')}` : 'Nguồn: chưa có số đo hợp lệ',
      `Trạng thái bản ghi: ${sample.status === 'ok' ? 'các cảm biến trả dữ liệu' : 'có cảm biến chưa sẵn sàng'}`
    ].join('\n');
  }
  const history = JSON.stringify(state.history);
  if (history !== lastHistory) {
    lastHistory = history;
    if (state.history.length) {
      $('conversation').replaceChildren(...state.history.map(message => {
        const node = document.createElement('p'); node.className = 'bubble ' + message.role;
        node.textContent = message.content; return node;
      }));
    } else {
      const node = document.createElement('p'); node.className='welcome'; node.textContent='Tôi ở đây. Hôm nay bạn thế nào?';
      $('conversation').replaceChildren(node);
    }
    $('conversation').scrollTop = $('conversation').scrollHeight;
  }
  const memories = JSON.stringify(state.memories);
  if (memories !== lastMemories) {
    lastMemories = memories;
    $('memories').replaceChildren(...state.memories.map(memory => {
      const row = document.createElement('div'); row.className='memory-row';
      const text = document.createElement('p'); text.textContent = memory.text;
      const button = document.createElement('button'); button.textContent='Xóa';
      button.onclick = () => { if (confirm('Xóa ghi nhớ này và ngữ cảnh hội thoại hiện tại?')) action('forget', {id:memory.id}); };
      row.append(text, button); return row;
    }));
    if (!state.memories.length) $('memories').textContent = 'Chưa lưu ghi nhớ nào.';
  }
  if (state.error !== lastServerError || disconnected) notice(state.error || '');
  lastServerError = state.error; disconnected = false;
}
async function refresh() {
  if (polling) return;
  polling = true;
  try {
    const response = await fetch('/api/state', {signal:AbortSignal.timeout(4000)});
    if (!response.ok) throw new Error();
    render(await response.json());
  } catch (_) { disconnected = true; temperature(null); $('status').textContent='Mất kết nối app'; notice('Chưa kết nối được với ARIA trên Pi.'); }
  finally { polling = false; }
}
document.querySelectorAll('[data-page]').forEach(button => button.onclick = () => {
  document.querySelectorAll('.page').forEach(page => page.hidden = page.id !== button.dataset.page);
  document.querySelectorAll('[data-page]').forEach(tab => tab.classList.toggle('selected', tab === button));
});
document.querySelectorAll('[data-say]').forEach(button => button.onclick = () => action('chat', {text:button.dataset.say}));
$('chat').onsubmit = async event => { event.preventDefault(); if (await action('chat', {text:$('message').value})) $('message').value=''; };
$('remember').onsubmit = async event => { event.preventDefault(); if (await action('remember', {text:$('memory-text').value})) $('memory-text').value=''; };
$('listen').onclick = () => action('listen');
$('stop').onclick = () => action('cancel');
$('reset').onclick = () => { if (confirm('Xóa hội thoại hiện tại? Các ghi nhớ đã lưu vẫn còn.')) action('reset'); };
for (const key of ['provider','persona','speak']) $(key).onchange = () => action('settings', {[key]:key === 'speak' ? $(key).checked : $(key).value});
$('fullscreen').onclick = async () => { try { await document.documentElement.requestFullscreen(); } catch (_) { notice('Hãy dùng chế độ toàn màn hình của trình duyệt.'); } };
function clock() {
  const value = new Date().toLocaleTimeString('vi-VN',{hour:'2-digit',minute:'2-digit'});
  $('clock').textContent = value; $('standby-clock').textContent = value;
}
$('standby').onclick = () => showStandby(false);
$('expression').value = restingExpression;
$('expression').onchange = () => {
  restingExpression = $('expression').value;
  try { localStorage.setItem('aria-expression', restingExpression); } catch (_) {}
  paintFace(current?.state || 'idle');
};
$('rest').onclick = () => showStandby(true);
for (const event of ['pointerdown','keydown','input','wheel']) document.addEventListener(event, () => { lastInteraction = performance.now(); }, {passive:true});
setInterval(() => {
  const busy = current && ['listening','thinking','speaking','stopping'].includes(current.state);
  const draft = $('message').value.trim() || $('memory-text').value.trim();
  if ($('standby').hidden && !busy && !draft && performance.now() - lastInteraction >= STANDBY_AFTER_MS) showStandby(true);
}, 1000);
paintFace(); clock(); refresh(); setInterval(clock, 10000); setInterval(refresh, 1000);
