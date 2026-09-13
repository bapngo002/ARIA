'use strict';
let token = '', current = null, lastHistory = '', lastMemories = '', polling = false, lastServerError = '', disconnected = false;
const $ = id => document.getElementById(id);
const expressions = {
  happy: {left:'M57 82 C52 24 108 24 105 82 C93 58 71 58 57 82 Z',right:'M195 82 C190 24 246 24 243 82 C231 58 209 58 195 82 Z',mouth:'M94 125 Q150 141 206 125 C209 180 91 180 94 125 Z',fill:true},
  normal: {left:'M65 66 A16 29 0 1 0 32 0 A16 29 0 1 0 65 66 Z',right:'M203 66 A16 29 0 1 0 32 0 A16 29 0 1 0 203 66 Z',mouth:'M105 135 C118 167 182 167 195 135',fill:false},
  sad: {left:'M51 71 H109 V78 H51 Z',right:'M191 71 H249 V78 H191 Z',mouth:'M109 159 C120 126 180 126 191 159',fill:false},
  angry: {left:'M51 40 L112 89 Q48 108 51 40 Z',right:'M249 40 L188 89 Q252 108 249 40 Z',mouth:'M106 159 Q132 139 164 130 Q194 124 194 160 Z',fill:true},
  thinking: {left:'M51 61 H109 V70 H51 Z',right:'M205 69 A14 24 0 1 0 28 0 A14 24 0 1 0 205 69 Z',mouth:'M124 147 Q148 140 174 147',fill:false},
  listening: {left:'M62 64 A19 33 0 1 0 38 0 A19 33 0 1 0 62 64 Z',right:'M200 64 A19 33 0 1 0 38 0 A19 33 0 1 0 200 64 Z',mouth:'M141 145 A9 12 0 1 0 18 0 A9 12 0 1 0 141 145 Z',fill:false}
};
let restingExpression = 'happy';
try { const saved = localStorage.getItem('aria-expression'); if (['happy','normal','sad','angry'].includes(saved)) restingExpression = saved; } catch (_) {}
function paintFace(state = 'idle') {
  const name = {thinking:'thinking',listening:'listening',speaking:'happy',stopping:'normal',error:'sad'}[state] || restingExpression;
  const expression = expressions[name];
  document.querySelectorAll('.robot-face').forEach(face => {
    face.dataset.expression = name;
    face.querySelector('.eye-left').setAttribute('d', expression.left);
    face.querySelector('.eye-right').setAttribute('d', expression.right);
    face.querySelector('.mouth').setAttribute('d', expression.mouth);
    face.querySelector('.mouth').classList.toggle('filled', expression.fill);
  });
}
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
