(() => {
  const status = document.getElementById('status');
  document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
    const input = document.getElementById(button.dataset.copy);
    try {
      await navigator.clipboard.writeText(input.value);
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
    cards.forEach(card => { card.hidden = !(card.textContent + card.querySelector('input').value).toLowerCase().includes(q); });
    document.getElementById('no-results').hidden = cards.some(card => !card.hidden);
  });
  if (location.hash) {
    const card = document.getElementById(location.hash.slice(1));
    card?.scrollIntoView();
  }
})();
