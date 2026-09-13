'use strict';
let token = '', current = null, lastHistory = '', lastMemories = '', polling = false, lastServerError = '', disconnected = false;
const $ = id => document.getElementById(id);
// Continuous poses: eyelid openness, inner eyebrow lift, smile depth, mouth width.
const expressions = {happy:[.86,-1,24,41],normal:[1,0,13,32],sad:[.78,-12,-15,30],angry:[.67,12,-5,30],thinking:[.88,-6,3,23],listening:[1.12,-8,7,24]};
let restingExpression = 'happy';
try { const saved = localStorage.getItem('aria-expression'); if (['happy','normal','sad','angry'].includes(saved)) restingExpression = saved; } catch (_) {}
function paintFace(state = 'idle') {
  const name = {thinking:'thinking',listening:'listening',speaking:'happy',stopping:'normal',error:'sad'}[state] || restingExpression;
  faceTarget = expressions[name];
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
  const gradient = (id, stops) => svgNode('radialGradient',{id,cx:'35%',cy:'28%',r:'75%'},stops.map(([offset,color])=>svgNode('stop',{offset,'stop-color':color})));
  const defs = svgNode('defs',{},[
    gradient(whiteId,[['0%','#ffffff'],['48%','#f4f7ff'],['78%','#b3cedd'],['100%','#647b9e']]),
    gradient(irisId,[['0%','#d9c995'],['32%','#a58a58'],['67%','#715333'],['88%','#483428'],['100%','#29232a']]),
    gradient(skinId,[['0%','#ffe7cd'],['25%','#f4c6a5'],['58%','#e7aa87'],['83%','#c58068'],['100%','#9b6256']]),
    gradient(blushId,[['0%','#ff9b9a'],['45%','#ed7b91'],['100%','#ed7b9100']]),
    gradient(mouthId,[['0%','#492c58'],['50%','#281d38'],['100%','#100f25']])
  ]);
  const features = svgNode('g',{'class':'features'});
  const headShape='M84 26 C106 7 193 7 216 26 Q239 50 235 91 L229 130 Q221 152 194 174 Q171 192 150 194 Q129 192 106 174 Q79 152 71 130 L65 91 Q61 50 84 26 Z';
  features.append(
    svgNode('path',{d:headShape,transform:'translate(0 6)',fill:'#020a16',opacity:'.45'}),
    svgNode('ellipse',{cx:65,cy:94,rx:12,ry:23,fill:'#cb8a70'}),
    svgNode('ellipse',{cx:235,cy:94,rx:12,ry:23,fill:'#b77865'}),
    svgNode('path',{d:headShape,fill:`url(#${skinId})`,stroke:'#efc7a7','stroke-opacity':'.25','stroke-width':1}),
    svgNode('path',{d:'M64 80 C52 56 58 21 82 13 C103 -3 158 -3 181 6 C223 2 245 30 239 65 L232 84 L223 51 C208 48 189 35 185 26 C151 44 115 38 107 27 Q77 42 73 76 Z',fill:'#30282c'}),
    svgNode('path',{d:'M78 32 C97 6 147 5 175 15 M93 31 Q129 18 154 21',fill:'none',stroke:'#725045','stroke-width':4,'stroke-linecap':'round',opacity:'.55'}),
    svgNode('ellipse',{cx:88,cy:123,rx:20,ry:11,fill:`url(#${blushId})`,opacity:'.33'}),
    svgNode('ellipse',{cx:212,cy:123,rx:20,ry:11,fill:`url(#${blushId})`,opacity:'.33'}),
    svgNode('path',{d:'M151 84 Q146 100 142 111 Q139 119 150 120 Q161 120 159 114',fill:'none',stroke:'#bc7b63','stroke-width':3,'stroke-linecap':'round'}),
    svgNode('path',{d:'M149 101 L147 109',fill:'none',stroke:'#ffe3c1','stroke-width':3,'stroke-linecap':'round'})
  );
  const eyes = [103,197].map(x => {
    const pupil = svgNode('g',{},[
      svgNode('circle',{r:17,fill:`url(#${irisId})`}),
      svgNode('circle',{r:13.5,fill:'none',stroke:'#e7c694','stroke-width':'.6',opacity:'.35'}),
      svgNode('circle',{r:9,fill:'#201a21'}),
      svgNode('circle',{cx:-5,cy:-6,r:4,fill:'#fff','fill-opacity':'.95'}),
      svgNode('circle',{cx:6,cy:6,r:1.8,fill:'#c6fcff','fill-opacity':'.7'})
    ]);
    const eye = svgNode('g',{'class':'living-eye'},[
      svgNode('ellipse',{cx:0,cy:2,rx:31,ry:38,fill:'#976452',opacity:'.4'}),
      svgNode('ellipse',{cx:0,cy:0,rx:28,ry:35,fill:`url(#${whiteId})`}),pupil
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
  const [openness,browLift,smile,width]=facePose;
  for (const view of faceViews) {
    if (!view.face.getClientRects().length) continue;
    view.features.setAttribute('transform',`translate(0 ${still ? 0 : Math.sin(now/1700)*1.2})`);
    for (const [i,{x,eye,pupil,brow}] of view.eyes.entries()) {
      eye.setAttribute('transform',`translate(${x} 78) scale(.78 ${openness*blink*.67})`);
      pupil.setAttribute('transform',`translate(${gaze[0]} ${gaze[1]})`);
      const outer=i===0 ? x-23 : x+23, inner=i===0 ? x+23 : x-23;
      brow.setAttribute('d',`M${outer} 47 Q${x} ${39+browLift/2} ${inner} ${47+browLift}`);
    }
    const speech=!still && current?.state==='speaking' ? Math.sin(now/130)*3 : 0;
    const curve=smile*.5, opening=Math.max(1,smile*.72+speech);
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
