(() => {
  const params = new URLSearchParams(location.search);
  const sent = new Set();
  const track = (event, app_id) => {
    if (navigator.globalPrivacyControl || navigator.doNotTrack === '1') return;
    const key = event + ':' + app_id;
    if (sent.has(key)) return;
    sent.add(key);
    fetch('https://justcompress-acquisition.liang-laurie.workers.dev/event', {
      method: 'POST', keepalive: true, credentials: 'omit',
      headers: {'Content-Type': 'text/plain'},
      body: JSON.stringify({event, app_id, source: params.get('utm_source') || 'direct', campaign: params.get('utm_campaign') || 'bio'})
    }).catch(() => {});
  };
  track('page_view', 'all');
  document.querySelectorAll('[data-store]').forEach(link => link.addEventListener('click', () => track('store_click', link.closest('[data-app]').dataset.app)));
  const status = document.getElementById('status');
  document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
    const input = document.getElementById(button.dataset.copy);
    try {
      await navigator.clipboard.writeText(input.value);
      track('copy_name', button.closest('[data-app]').dataset.app);
      status.textContent = 'Copied: ' + input.value + '. Paste it into App Store search.';
      button.textContent = 'Name copied ✓';
      setTimeout(() => { button.textContent = 'Copy name'; }, 2200);
    } catch (_) {
      input.type = 'text'; input.className = 'copy-fallback'; input.readOnly = true;
      input.focus(); input.select(); input.setSelectionRange(0, input.value.length);
      status.textContent = 'Select Copy, then paste this name into App Store search.';
    }
  }));
  const search = document.getElementById('find-app');
  const cards = [...document.querySelectorAll('.app-card')];
  search.addEventListener('input', () => {
    const q = search.value.toLowerCase().trim();
    if (q) document.querySelector('.more').open = true;
    cards.forEach(card => { card.hidden = !(card.textContent + card.querySelector('input').value).toLowerCase().includes(q); });
    document.getElementById('no-results').hidden = cards.some(card => !card.hidden);
  });
  if (location.hash) {
    const card = document.getElementById(location.hash.slice(1));
    if (card?.closest('.more')) card.closest('.more').open = true;
    card?.scrollIntoView();
  }
})();
