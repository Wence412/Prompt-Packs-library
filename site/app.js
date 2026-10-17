const RAW_BASE = 'https://raw.githubusercontent.com/Wence412/chatgpt-image-prompt-packs/main';
const PAGE_SIZE = 24;
const domain = document.body.dataset.domain || 'all';
const state = { prompts: [], query: '', collection: '', operation: '', media: '', assets: [], visibleCount: PAGE_SIZE };
const $ = selector => document.querySelector(selector);
const elements = {
  cards: $('#cards'), empty: $('#empty'), count: $('#count'), summary: $('#result-summary'),
  search: $('#search'), collection: $('#collection'), operation: $('#operation'), media: $('#media'),
  toast: $('#toast'), loadMore: $('#load-more'), themeToggle: $('#theme-toggle')
};

const unique = values => [...new Set(values)].sort((a, b) => a.localeCompare(b));
const normalizeLegacy = prompt => ({ ...prompt, domain: 'Image', collection: prompt.category, operation: 'generate', output: { aspect_ratio: 'Flexible', format: 'Prompt template' } });
const normalizeCard = card => ({ ...card, domain: 'Image', collection: card.pack });
const normalizeVideo = prompt => ({ ...prompt, collection: prompt.category });
const assetUrl = path => /^assets\/(images\/[a-z0-9-]+(?:-preview)?\.webp|pdfs\/[a-z0-9-]+\.pdf)$/.test(path) ? new URL(path, document.baseURI).href : null;

function toast(message) {
  elements.toast.textContent = message;
  elements.toast.classList.add('visible');
  window.setTimeout(() => elements.toast.classList.remove('visible'), 1800);
}

async function copyPrompt(prompt) {
  try { await navigator.clipboard.writeText(prompt.prompt); toast(`${prompt.id} copied`); }
  catch { toast('Copy is unavailable. Select the prompt text manually.'); }
}

function populateFilters() {
  unique(state.prompts.map(prompt => prompt.collection)).forEach(value => elements.collection.add(new Option(value, value)));
  unique(state.prompts.map(prompt => prompt.operation)).forEach(value => elements.operation.add(new Option(value, value)));
  if (domain === 'video') {
    const mediaFilter = elements.media.closest('label');
    mediaFilter.hidden = true;
    mediaFilter.style.display = 'none';
  }
}

function results() {
  const query = state.query.toLowerCase().trim();
  return state.prompts.filter(prompt => {
    const attachments = state.assets.filter(asset => asset.prompt_ids.includes(prompt.id));
    const haystack = [prompt.domain, prompt.id, prompt.title, prompt.collection, prompt.prompt, ...(prompt.tags || [])].join(' ').toLowerCase();
    return (!query || haystack.includes(query))
      && (!state.collection || prompt.collection === state.collection)
      && (!state.operation || prompt.operation === state.operation)
      && (!state.media || attachments.some(asset => asset.kind === state.media));
  });
}

function render() {
  const filtered = results();
  const visible = filtered.slice(0, state.visibleCount);
  elements.cards.replaceChildren();
  elements.empty.hidden = filtered.length !== 0;
  elements.summary.textContent = `${filtered.length} of ${state.prompts.length} prompt cards`;
  elements.loadMore.hidden = visible.length >= filtered.length;
  elements.loadMore.textContent = `Show ${Math.min(PAGE_SIZE, filtered.length - visible.length)} more prompts`;
  for (const prompt of visible) {
    const card = $('#card-template').content.cloneNode(true);
    card.querySelector('.card-id').textContent = prompt.id;
    card.querySelector('.card-operation').textContent = prompt.domain || prompt.operation;
    card.querySelector('.card-title').textContent = prompt.title;
    card.querySelector('.card-collection').textContent = prompt.collection;
    card.querySelector('.card-prompt').textContent = prompt.prompt;
    card.querySelector('.card-output').textContent = `${prompt.output.aspect_ratio} · ${prompt.output.format}`;
    card.querySelector('.copy').addEventListener('click', () => copyPrompt(prompt));
    const details = document.createElement('details');
    const summary = document.createElement('summary');
    summary.textContent = prompt.acceptance_criteria ? 'View full prompt and review checks' : 'View full prompt';
    const full = document.createElement('pre'); full.textContent = prompt.prompt;
    details.append(summary, full);
    if (prompt.acceptance_criteria?.length) {
      const heading = document.createElement('h3'); heading.textContent = 'Review checks';
      const list = document.createElement('ul');
      prompt.acceptance_criteria.forEach(item => { const li = document.createElement('li'); li.textContent = item; list.append(li); });
      details.append(heading, list);
    }
    card.querySelector('article').append(details);
    elements.cards.append(card);
  }
}

function reset() {
  state.query = ''; state.collection = ''; state.operation = ''; state.media = ''; state.visibleCount = PAGE_SIZE;
  elements.search.value = ''; elements.collection.value = ''; elements.operation.value = ''; elements.media.value = '';
  render();
}

async function load() {
  try {
    const [legacy, capability, video, vph] = await Promise.all([
      fetch(`${RAW_BASE}/prompts.json`).then(response => response.ok ? response.json() : Promise.reject()),
      fetch(`${RAW_BASE}/capability-packs-v2.json`).then(response => response.ok ? response.json() : Promise.reject()),
      fetch(`${RAW_BASE}/site/data/video-prompts.json`).then(response => response.ok ? response.json() : Promise.reject()),
      fetch(`${RAW_BASE}/vph-import.json`).then(response => response.ok ? response.json() : { prompts: [] })
    ]);
    const vphPrompts = Array.isArray(vph.prompts) ? vph.prompts.map(prompt => ({ ...prompt, domain: 'Image', collection: prompt.collection || 'Visual Prompts Hub' })) : [];
    let all = [...legacy.prompts.map(normalizeLegacy), ...capability.packs.map(normalizeCard), ...vphPrompts, ...video.prompts.map(normalizeVideo)];
    if (domain !== 'all') all = all.filter(prompt => prompt.domain.toLowerCase() === domain);
    state.prompts = all;
    try {
      const response = await fetch('media-library.json');
      const media = await response.json();
      state.assets = Array.isArray(media.assets) ? media.assets.filter(asset => Array.isArray(asset.prompt_ids) && assetUrl(asset.path)) : [];
    } catch { state.assets = []; }
    elements.count.textContent = `${state.prompts.length} cards`;
    populateFilters(); render();
  } catch {
    elements.count.textContent = 'Unavailable';
    elements.summary.textContent = 'The prompt data could not be loaded. Try again after the repository publishes.';
  }
}

const update = (key, value) => { state[key] = value; state.visibleCount = PAGE_SIZE; render(); };
elements.search.addEventListener('input', event => update('query', event.target.value));
elements.collection.addEventListener('change', event => update('collection', event.target.value));
elements.operation.addEventListener('change', event => update('operation', event.target.value));
elements.media.addEventListener('change', event => update('media', event.target.value));
$('#clear').addEventListener('click', reset);
$('#empty-clear').addEventListener('click', reset);
elements.loadMore.addEventListener('click', () => { state.visibleCount += PAGE_SIZE; render(); });

function setTheme(theme) {
  document.body.dataset.theme = theme;
  const isLight = theme === 'light';
  elements.themeToggle.textContent = isLight ? 'Use dark theme' : 'Use light theme';
  elements.themeToggle.setAttribute('aria-pressed', String(isLight));
  localStorage.setItem('prompt-packs-theme', theme);
}
try { setTheme(localStorage.getItem('prompt-packs-theme') || 'dark'); } catch { setTheme('dark'); }
elements.themeToggle.addEventListener('click', () => setTheme(document.body.dataset.theme === 'light' ? 'dark' : 'light'));
load();
