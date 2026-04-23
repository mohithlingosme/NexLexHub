const API_BASE = '../backend-php/api';
const CONTENT_TYPES = ['article', 'case_law', 'bare_act', 'whitepaper', 'news', 'law_review'];

const state = { activeSectionEl: null, selectedAct: null };

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initFilters();
  loadContent();
  loadBareActs();
  loadLatestNews();
  bindForms();
});

function initNavigation() {
  const btn = document.getElementById('menuToggle');
  const nav = document.getElementById('mainNav');
  btn?.addEventListener('click', () => nav.classList.toggle('open'));
}

function initFilters() {
  const typeFilter = document.getElementById('typeFilter');
  CONTENT_TYPES.forEach((type) => {
    const opt = document.createElement('option');
    opt.value = type;
    opt.textContent = type.replace('_', ' ');
    typeFilter.appendChild(opt);
  });
  ['Criminal Law', 'Corporate Law', 'Constitutional Law', 'Technology Law', 'Finance Law', 'Taxation Law'].forEach((cat) => {
    const opt = document.createElement('option');
    opt.value = cat;
    opt.textContent = cat;
    document.getElementById('categoryFilter').appendChild(opt);
  });
  document.getElementById('searchBtn').addEventListener('click', applySearch);
}

async function loadContent(query = '') {
  const data = await fetchJson(`${API_BASE}/posts.php${query}`);
  const sections = document.querySelectorAll('.card-grid[data-type]');
  sections.forEach((grid) => {
    const type = grid.dataset.type;
    grid.innerHTML = '';
    data.filter((x) => x.type === type).forEach((item) => grid.appendChild(buildCard(item)));
  });
}

function buildCard(item) {
  const tpl = document.getElementById('contentCardTemplate');
  const node = tpl.content.cloneNode(true);
  node.querySelector('.card-title').textContent = item.title;
  node.querySelector('.card-meta').textContent = `${item.author || 'Team'} • ${item.created_at}`;
  node.querySelector('.card-summary').textContent = (item.content || '').slice(0, 180) + '...';
  const link = node.querySelector('.pdf-link');
  if (item.file_path) {
    link.href = `${API_BASE}/files.php?path=${encodeURIComponent(item.file_path)}`;
  } else {
    link.style.display = 'none';
  }
  return node;
}

function applySearch() {
  const q = document.getElementById('searchInput').value.trim();
  const type = document.getElementById('typeFilter').value;
  const category = document.getElementById('categoryFilter').value;
  const query = new URLSearchParams({ q, type, category });
  loadContent(`?${query.toString()}`);
}

async function loadBareActs() {
  const acts = await fetchJson(`${API_BASE}/acts.php`);
  const sidebar = document.getElementById('actSidebar');
  sidebar.innerHTML = '';

  acts.forEach((act) => {
    const chapterWrap = document.createElement('div');
    chapterWrap.className = 'chapter';
    const titleBtn = document.createElement('button');
    titleBtn.textContent = act.title;
    const sectionWrap = document.createElement('div');
    sectionWrap.hidden = true;

    titleBtn.addEventListener('click', () => {
      sectionWrap.hidden = !sectionWrap.hidden;
      state.selectedAct = act;
      document.getElementById('downloadActPdf').href = `${API_BASE}/files.php?path=${encodeURIComponent(act.pdf_path || '')}`;
    });

    act.chapters.forEach((ch) => {
      const chLabel = document.createElement('div');
      chLabel.textContent = ch.title;
      chLabel.style.fontWeight = '600';
      sectionWrap.appendChild(chLabel);
      ch.sections.forEach((sec) => {
        const secBtn = document.createElement('button');
        secBtn.className = 'section-link';
        secBtn.textContent = `§${sec.section_number} ${sec.title}`;
        secBtn.addEventListener('click', () => loadSection(sec.id, secBtn));
        sectionWrap.appendChild(secBtn);
      });
    });

    chapterWrap.appendChild(titleBtn);
    chapterWrap.appendChild(sectionWrap);
    sidebar.appendChild(chapterWrap);
  });
}

async function loadSection(sectionId, activeEl) {
  if (state.activeSectionEl) state.activeSectionEl.classList.remove('active');
  activeEl.classList.add('active');
  state.activeSectionEl = activeEl;

  const data = await fetchJson(`${API_BASE}/sections.php?id=${sectionId}`);
  const container = document.getElementById('actContent');
  container.innerHTML = `
    <div class="act-actions">
      <a href="#bare-acts">← Back to Bare Acts</a>
      <a href="${API_BASE}/files.php?path=${encodeURIComponent(state.selectedAct?.pdf_path || '')}" target="_blank" rel="noopener">Download full Bare Act PDF</a>
    </div>
    <h3>Section ${data.section.section_number}: ${data.section.title}</h3>
    <p>${data.section.bare_text}</p>
    <h4>Law Review Analysis</h4>
    <p>${data.analysis?.explanation || 'Analysis pending.'}</p>
    <h4>Related Case Laws</h4>
    <ul>${(data.related.case_laws || []).map((x) => `<li>${x.title}</li>`).join('')}</ul>
    <h4>Related Articles</h4>
    <ul>${(data.related.articles || []).map((x) => `<li>${x.title}</li>`).join('')}</ul>
  `;
}

async function loadLatestNews() {
  const news = await fetchJson(`${API_BASE}/news.php?latest=5`);
  document.getElementById('latestNews').textContent = news.map((n) => `${n.created_at}: ${n.title}`).join(' • ');
}

function bindForms() {
  document.getElementById('applicationForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const body = Object.fromEntries(new FormData(e.target));
    await fetchJson(`${API_BASE}/applications.php`, { method: 'POST', body: JSON.stringify(body) });
    alert('Application submitted.');
    e.target.reset();
  });

  document.getElementById('contactForm').addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Thanks! We will contact you shortly.');
    e.target.reset();
  });
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, { headers: { 'Content-Type': 'application/json' }, ...options });
  if (!response.ok) throw new Error(`Request failed: ${response.status}`);
  return response.json();
}
