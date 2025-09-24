const DJANGO_API = 'http://localhost:8000/api';
const FLASK_API = 'http://localhost:5000';

const getTokens = () => {
  try { return JSON.parse(localStorage.getItem('tokens') || 'null'); } catch { return null; }
};
const setTokens = (tokens) => localStorage.setItem('tokens', JSON.stringify(tokens));
const clearTokens = () => localStorage.removeItem('tokens');

const setStatus = (id, msg) => { const el = document.getElementById(id); if (el) el.textContent = msg || ''; };

const withTimeout = (promise, ms = 8000) => {
  return new Promise((resolve, reject) => {
    const id = setTimeout(() => reject(new Error('Request timed out')), ms);
    promise.then((res) => { clearTimeout(id); resolve(res); }, (err) => { clearTimeout(id); reject(err); });
  });
};

async function apiFetch(path, { method = 'GET', body, useFlask = false, auth = true, timeoutMs = 8000 } = {}) {
  const base = useFlask ? FLASK_API : DJANGO_API;
  const headers = { 'Content-Type': 'application/json' };
  if (auth) {
    const tokens = getTokens();
    if (tokens?.access) headers['Authorization'] = `Bearer ${tokens.access}`;
  }
  const req = fetch(`${base}${path}`, { method, headers, body: body ? JSON.stringify(body) : undefined });
  const res = await withTimeout(req, timeoutMs);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  const text = await res.text();
  try { return text ? JSON.parse(text) : {}; } catch { return { raw: text } }
}

// Auth
const registerForm = document.getElementById('register-form');
const loginForm = document.getElementById('login-form');
const logoutButton = document.getElementById('logout-button');

registerForm?.addEventListener('submit', async (e) => {
  e.preventDefault();
  setStatus('auth-status', 'Registering...');
  const phone_number = document.getElementById('register-phone').value.trim();
  const password = document.getElementById('register-password').value;
  try {
    const data = await apiFetch('/users/auth/register/', { method: 'POST', body: { phone_number, password }, auth: false });
    setTokens(data.tokens);
    setStatus('auth-status', 'Registered and logged in.');
  } catch (err) { setStatus('auth-status', `Register failed: ${err.message}`); }
});

loginForm?.addEventListener('submit', async (e) => {
  e.preventDefault();
  setStatus('auth-status', 'Logging in...');
  const phone_number = document.getElementById('login-phone').value.trim();
  const password = document.getElementById('login-password').value;
  try {
    const data = await apiFetch('/users/auth/login/', { method: 'POST', body: { phone_number, password }, auth: false });
    setTokens(data.tokens);
    setStatus('auth-status', 'Logged in.');
  } catch (err) { setStatus('auth-status', `Login failed: ${err.message}`); }
});

logoutButton?.addEventListener('click', async () => {
  const tokens = getTokens();
  if (!tokens?.refresh) { setStatus('auth-status', 'Not logged in.'); return; }
  try {
    await apiFetch('/users/auth/logout/', { method: 'POST', body: { refresh: tokens.refresh } });
    clearTokens();
    setStatus('auth-status', 'Logged out.');
  } catch (err) { setStatus('auth-status', `Logout failed: ${err.message}`); }
});

// Onboarding
const contactForm = document.getElementById('contact-form');
const fetchPolicyBtn = document.getElementById('fetch-policy');
const requestPermsBtn = document.getElementById('request-permissions');

contactForm?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('contact-name').value.trim();
  const phone = document.getElementById('contact-phone').value.trim();
  try {
    await apiFetch('/onboarding/emergency-contact/', { method: 'POST', body: { name, phone } });
    alert('Contact added');
  } catch (err) { alert('Failed to add contact: ' + err.message); }
});

fetchPolicyBtn?.addEventListener('click', async () => {
  setStatus('policy-output', 'Loading policy...');
  try {
    const data = await apiFetch('/onboarding/policy/', { method: 'GET' });
    document.getElementById('policy-output').textContent = JSON.stringify(data, null, 2);
  } catch (err) { setStatus('policy-output', 'Failed to load policy: ' + err.message); }
});

requestPermsBtn?.addEventListener('click', async () => {
  try {
    const granted = { location: true, microphone: true, notifications: true };
    await apiFetch('/onboarding/permissions/', { method: 'POST', body: granted });
    alert('Permissions recorded');
  } catch (err) { alert('Failed to record permissions: ' + err.message); }
});

// SOS
const sosBtn = document.getElementById('sos-button');

sosBtn?.addEventListener('click', async () => {
  setStatus('sos-status', 'Sending SOS...');
  try {
    await apiFetch('/trigger/sos/', { method: 'POST', body: { source: 'web' } });
    setStatus('sos-status', 'SOS sent.');
  } catch (err) {
    setStatus('sos-status', 'SOS Failed on DRF, attempting voice flow...');
    try {
      await apiFetch('/process-emergency', { method: 'POST', useFlask: true, auth: false, body: { message: 'SOS from web UI' } });
      setStatus('sos-status', 'SOS recorded via voice pipeline.');
    } catch (e2) { setStatus('sos-status', 'SOS failed: ' + e2.message); }
  }
});

// Tracking
const locBtn = document.getElementById('location-button');
const sendLocBtn = document.getElementById('send-location');
const locOut = document.getElementById('location-output');
let lastCoords = null;

locBtn?.addEventListener('click', () => {
  if (!navigator.geolocation) { locOut.textContent = 'Geolocation not supported.'; return; }
  navigator.geolocation.getCurrentPosition((pos) => {
    lastCoords = { latitude: pos.coords.latitude, longitude: pos.coords.longitude };
    locOut.textContent = `Lat: ${lastCoords.latitude}, Lng: ${lastCoords.longitude}`;
  }, () => { locOut.textContent = 'Unable to retrieve your location.'; });
});

sendLocBtn?.addEventListener('click', async () => {
  if (!lastCoords) { alert('Get location first'); return; }
  try {
    await apiFetch('/tracking/gps/', { method: 'POST', body: lastCoords });
    alert('Location sent');
  } catch (err) { alert('Failed to send location: ' + err.message); }
});

// Journal
const journalBtn = document.getElementById('journal-submit');

journalBtn?.addEventListener('click', async () => {
  const text = document.getElementById('journal-text').value.trim();
  if (!text) { setStatus('journal-status', 'Please write something.'); return; }
  setStatus('journal-status', 'Saving...');
  try {
    await apiFetch('/resources/journal/', { method: 'POST', body: { text } });
    setStatus('journal-status', 'Saved.');
  } catch (err) { setStatus('journal-status', 'Failed: ' + err.message); }
});

// Resources buttons
const gbvBtn = document.getElementById('fetch-gbv');
const legalBtn = document.getElementById('fetch-legal');
const resourcesOut = document.getElementById('resources-output');

gbvBtn?.addEventListener('click', async () => {
  resourcesOut.textContent = 'Loading GBV resources...';
  try { const data = await apiFetch('/resources/gbv/'); resourcesOut.textContent = JSON.stringify(data, null, 2); }
  catch (err) { resourcesOut.textContent = 'Failed: ' + err.message; }
});

legalBtn?.addEventListener('click', async () => {
  resourcesOut.textContent = 'Finding legal aid...';
  try { const data = await apiFetch('/resources/legal-aid/'); resourcesOut.textContent = JSON.stringify(data, null, 2); }
  catch (err) { resourcesOut.textContent = 'Failed: ' + err.message; }
});

// Inline chatbot section
const chatInput = document.getElementById('chat-input');
const chatSend = document.getElementById('chat-send');
const chatOut = document.getElementById('chat-output');

chatSend?.addEventListener('click', async () => {
  const message = chatInput.value.trim();
  if (!message) return;
  chatOut.textContent = 'Sending...';
  try { const data = await apiFetch('/resources/chatbot/', { method: 'POST', body: { message } }); chatOut.textContent = JSON.stringify(data, null, 2); }
  catch (err) { chatOut.textContent = 'Sorry, I could not reach the assistant.'; }
});

// Floating chat widget
const chatToggle = document.getElementById('chat-toggle');
const chatWidget = document.getElementById('chat-widget');
const chatClose = document.getElementById('chat-close');
const chatMessages = document.getElementById('chat-messages');
const chatWidgetInput = document.getElementById('chat-widget-input');
const chatWidgetSend = document.getElementById('chat-widget-send');

const appendMsg = (text, who = 'bot') => {
  const div = document.createElement('div');
  div.className = `msg ${who}`;
  div.textContent = text;
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return div;
};

const appendActions = () => {
  const wrap = document.createElement('div');
  wrap.className = 'row';
  wrap.style.justifyContent = 'flex-end';
  const sos = document.createElement('button'); sos.className = 'secondary'; sos.textContent = 'Send SOS';
  const loc = document.createElement('button'); loc.className = 'secondary'; loc.textContent = 'Share Location';
  const res = document.createElement('button'); res.className = 'secondary'; res.textContent = 'Open Resources';
  sos.onclick = () => document.getElementById('sos-button')?.click();
  loc.onclick = () => document.getElementById('location-button')?.click();
  res.onclick = () => document.getElementById('resources')?.scrollIntoView({ behavior: 'smooth' });
  wrap.appendChild(sos); wrap.appendChild(loc); wrap.appendChild(res);
  chatMessages.appendChild(wrap);
  chatMessages.scrollTop = chatMessages.scrollHeight;
};

const localAssistant = (message) => {
  const text = message.toLowerCase();
  if (text.includes('assault') || text.includes('danger') || text.includes('help') || text.includes('safety')) {
    return "I'm here with you. If you're in immediate danger, press ‘Send SOS’. I can also share your location and list nearby resources. Would you like me to do that now?";
  }
  if (text.includes('legal')) return 'I can help you find legal aid resources. Tap “Open Resources”.';
  if (text.includes('journal')) return 'You can record what happened in the Journal section. I can open it for you if you want.';
  return "I’m here to help. Tell me what you’re experiencing, and I’ll guide you to SOS, location sharing, or resources.";
};

const sendToChatbot = async (message) => {
  // retry up to 2 times
  for (let i = 0; i < 2; i++) {
    try {
      const data = await apiFetch('/resources/chatbot/', { method: 'POST', body: { message }, timeoutMs: 8000 });
      if (typeof data === 'string') return data;
      return data.reply || JSON.stringify(data);
    } catch (e) {
      if (i === 1) throw e;
      await new Promise(r => setTimeout(r, 600));
    }
  }
};

chatToggle?.addEventListener('click', () => {
  chatWidget.classList.toggle('chat-hidden');
  if (!chatWidget.classList.contains('chat-hidden') && chatMessages.children.length === 0) {
    appendMsg('Hi, I\'m your EveShield assistant. How can I help today?');
  }
  if (!chatWidget.classList.contains('chat-hidden')) chatWidgetInput.focus();
});

chatClose?.addEventListener('click', () => chatWidget.classList.add('chat-hidden'));

const handleSend = async () => {
  const message = chatWidgetInput.value.trim();
  if (!message) return;
  appendMsg(message, 'user');
  chatWidgetInput.value = '';
  const typing = appendMsg('Typing...');
  try {
    const reply = await sendToChatbot(message);
    typing.textContent = reply;
    typing.className = 'msg bot';
  } catch (err) {
    typing.textContent = localAssistant(message);
    typing.className = 'msg bot';
    appendActions();
  }
};

chatWidgetSend?.addEventListener('click', handleSend);
chatWidgetInput?.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') { e.preventDefault(); handleSend(); }
});

// Dashboard (Flask)
const dashBtn = document.getElementById('dashboard-refresh');
const dashOut = document.getElementById('dashboard-output');

dashBtn?.addEventListener('click', async () => {
  dashOut.textContent = 'Loading dashboard...';
  try { const data = await apiFetch('/dashboard-data', { useFlask: true, auth: false }); dashOut.textContent = JSON.stringify(data, null, 2); }
  catch (err) { dashOut.textContent = 'Failed: ' + err.message; }
});

// Initialize auth status on load
(function init() {
  const tokens = getTokens();
  setStatus('auth-status', tokens?.access ? 'Authenticated' : 'Not logged in');
})();    


