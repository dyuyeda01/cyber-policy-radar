(async function () {
  const res = await fetch('data/articles.json');
  const data = await res.json();
  const items = (data.items || []).sort((a,b) => new Date(b.published||0) - new Date(a.published||0));

  const list = document.getElementById('list');
  const count = document.getElementById('count');
  const lastUpdated = document.getElementById('lastUpdated');
  const regionSelect = document.getElementById('regionSelect');
  const sourceSelect = document.getElementById('sourceSelect');
  const searchInput = document.getElementById('searchInput');

  if (data.generated_at) {
    const dt = new Date(data.generated_at);
    lastUpdated.textContent = `Last updated: ${dt.toLocaleString()}`;
  }

  // Build filter dropdowns
  const regions = [...new Set(items.map(i => i.region).filter(Boolean))].sort();
  const sources = [...new Set(items.map(i => i.source).filter(Boolean))].sort();
  regionSelect.innerHTML = `<option value="all">All regions</option>` + regions.map(r=>`<option>${r}</option>`).join('');
  sourceSelect.innerHTML = `<option value="all">All sources</option>` + sources.map(s=>`<option>${s}</option>`).join('');

  // Render list
  function render(listItems) {
    count.textContent = `${listItems.length} article(s)`;
    list.innerHTML = listItems.map(i => {
      const hasImage = i.image && !i.image.includes('placeholder');
      const date = i.published ? new Date(i.published).toLocaleString() : '';
      return `
        <div class="card">
          ${hasImage ? `<img src="${i.image}" alt="" loading="lazy" onerror="this.remove()">` : ''}
          <div class="card-content">
            <div class="meta">${i.region || ''} ${i.source ? '• ' + i.source : ''}${date ? '<br>' + date : ''}</div>
            <h3><a href="${i.url}" target="_blank" rel="noopener noreferrer">${i.title}</a></h3>
            ${i.summary ? `<p>${i.summary.substring(0,150)}…</p>` : ''}
          </div>
        </div>`;
    }).join('');
  }

  function applyFilters() {
    const q = (searchInput.value || '').toLowerCase();
    const r = regionSelect.value;
    const s = sourceSelect.value;
    const filtered = items.filter(i =>
      (r === 'all' || i.region === r) &&
      (s === 'all' || i.source === s) &&
      (!q || (i.title || '').toLowerCase().includes(q))
    );
    render(filtered);
  }

  [searchInput, regionSelect, sourceSelect].forEach(el =>
    el.addEventListener('input', applyFilters)
  );

  render(items);
})();
