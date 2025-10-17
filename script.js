(async function() {
  const res = await fetch('data/articles.json');
  const data = await res.json();
  const items = data.items || [];
  const grid = document.getElementById('grid');
  const count = document.getElementById('count');
  const lastUpdated = document.getElementById('lastUpdated');
  const regionSelect = document.getElementById('regionSelect');
  const sourceSelect = document.getElementById('sourceSelect');
  const searchInput = document.getElementById('searchInput');

  // Last updated
  if (data.generated_at) {
    const dt = new Date(data.generated_at);
    lastUpdated.textContent = `Last updated: ${dt.toLocaleString()}`;
  }

  // Populate filters
  const regions = [...new Set(items.map(i => i.region).filter(Boolean))].sort();
  const sources = [...new Set(items.map(i => i.source).filter(Boolean))].sort();

  regionSelect.innerHTML = `<option value="all">All Regions</option>` +
    regions.map(r => `<option value="${r}">${r}</option>`).join('');
  sourceSelect.innerHTML = `<option value="all">All Sources</option>` +
    sources.map(s => `<option value="${s}">${s}</option>`).join('');

  function filterItems() {
    const term = searchInput.value.toLowerCase();
    const region = regionSelect.value;
    const source = sourceSelect.value;

    const filtered = items.filter(i =>
      (region === 'all' || i.region === region) &&
      (source === 'all' || i.source === source) &&
      (!term || i.title.toLowerCase().includes(term))
    );

    count.textContent = `${filtered.length} article(s)`;
    grid.innerHTML = filtered
      .sort((a,b) => new Date(b.published||0) - new Date(a.published||0))
      .map(i => `
        <div class="card">
          <div class="meta">
            ${i.region ? `<span>${i.region}</span>` : ''} 
            ${i.source ? `• ${i.source}` : ''}<br>
            ${i.published ? new Date(i.published).toLocaleString() : ''}
          </div>
          <h3><a href="${i.url}" target="_blank">${i.title}</a></h3>
          <p>${i.summary || ''}</p>
        </div>
      `)
      .join('');
  }

  [regionSelect, sourceSelect, searchInput].forEach(el =>
    el.addEventListener('input', filterItems)
  );

  filterItems();
})();
