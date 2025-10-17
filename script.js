(async function () {
  const res = await fetch('data/articles.json');
  const data = await res.json();
  const items = (data.items || []).sort((a, b) => new Date(b.published || 0) - new Date(a.published || 0));

  const grid = document.getElementById('grid');
  const count = document.getElementById('count');
  const lastUpdated = document.getElementById('lastUpdated');
  const regionSelect = document.getElementById('regionSelect');
  const sourceSelect = document.getElementById('sourceSelect');
  const searchInput = document.getElementById('searchInput');

  // Last updated timestamp
  if (data.generated_at) {
    const dt = new Date(data.generated_at);
    lastUpdated.textContent = `Last updated: ${dt.toLocaleString()}`;
  }

  // Build filter options from data
  const regions = [...new Set(items.map(i => i.region).filter(Boolean))].sort();
  const sources = [...new Set(items.map(i => i.source).filter(Boolean))].sort();
  regionSelect.innerHTML = `<option value="all">All regions</option>` + regions.map(r => `<option>${r}</option>`).join('');
  sourceSelect.innerHTML = `<option value="all">All sources</option>` + sources.map(s => `<option>${s}</option>`).join('');

  // Render helpers
  function safeText(s) { return (s || '').toString(); }
  function hasUsableImage(url) {
    if (!url) return false;
    if (url.includes('placeholder')) return false;
    return true;
  }

  function render(list) {
    count.textContent = `${list.length} article(s)`;

    grid.innerHTML = list.map(i => {
      const showImg = hasUsableImage(i.image);
      // onerror removes the image node if it fails (prevents blank boxes on mobile)
      const imgHTML = showImg
        ? `<div class="thumb">
             <img loading="lazy" referrerpolicy="no-referrer"
                  src="${i.image}"
                  alt=""
                  onerror="this.closest('.thumb').remove()">
           </div>`
        : '';

      const date = i.published ? new Date(i.published).toLocaleString() : '';

      return `
        <div class="card">
          ${imgHTML}
          <div class="content">
            <div class="meta">${safeText(i.region)} ${i.source ? '• ' + safeText(i.source) : ''}${date ? '<br>' + date : ''}</div>
            <h3 class="title"><a href="${i.url}" target="_blank" rel="noopener noreferrer">${safeText(i.title)}</a></h3>
            ${i.summary ? `<p class="summary">${safeText(i.summary).slice(0, 180)}…</p>` : ''}
          </div>
        </div>
      `;
    }).join('');
  }

  function applyFilters() {
    const q = (searchInput.value || '').toLowerCase();
    const r = regionSelect.value;
    const s = sourceSelect.value;

    const filtered = items.filter(i =>
      (r === 'all' || i.region === r) &&
      (s === 'all' || i.source === s) &&
      (!q || safeText(i.title).toLowerCase().includes(q))
    );

    render(filtered);
  }

  // Wire up events
  [searchInput, regionSelect, sourceSelect].forEach(el =>
    el.addEventListener('input', applyFilters)
  );

  // Initial paint
  render(items);
})();
