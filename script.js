(async function(){
  const res = await fetch('data/articles.json');
  const data = await res.json();
  const items = data.items || [];
  const grid = document.getElementById('grid');
  const count = document.getElementById('count');
  count.textContent = `${items.length} article(s)`;

  grid.innerHTML = items.map(i => `
    <div class="card">
      <div class="meta">${i.region || ''} ${i.country || ''} ${i.published ? new Date(i.published).toLocaleDateString() : ''}</div>
      <h3><a href="${i.url}" target="_blank">${i.title}</a></h3>
      <p>${i.summary || ''}</p>
      <div class="meta">Source: ${i.source}</div>
    </div>
  `).join('');
})();
