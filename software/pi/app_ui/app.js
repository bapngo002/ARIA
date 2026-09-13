'use strict';
let token = '', current = null, lastHistory = '', lastMemories = '', polling = false, lastServerError = '', disconnected = false;
const $ = id => document.getElementById(id);
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
  $('status').textContent = labels[state.state] || state.state;
  const busy = ['listening','thinking','speaking','stopping'].includes(state.state);
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
  } catch (_) { disconnected = true; $('status').textContent='Mất kết nối app'; notice('Chưa kết nối được với ARIA trên Pi.'); }
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
function clock() { $('clock').textContent = new Date().toLocaleTimeString('vi-VN',{hour:'2-digit',minute:'2-digit'}); }
clock(); refresh(); setInterval(clock, 10000); setInterval(refresh, 1000);
