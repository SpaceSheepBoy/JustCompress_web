/* Product tryouts run locally. No inputs or outputs are sent to analytics. */
export function estimateAudio(minutes, bitrate, limit) {
  if (![minutes, bitrate, limit].every(Number.isFinite) || minutes < 0.1 || minutes > 10080 || bitrate < 8 || bitrate > 320 || limit < 0.1 || limit > 10000) return null;
  return {sizeMB: minutes * 60 * bitrate / 8000, ceilingKbps: limit * 8000 / (minutes * 60)};
}
export function videoWorkflow(source, goal) {
  if (!['hdr','log','hevc','sdr'].includes(source) || !['sdr','h264','fps','audio'].includes(goal)) return null;
  if (goal === 'audio') return ['Extract Audio', 'Choose Extract Audio to save the supported first audio track as AAC in an M4A file. Play the saved audio and check the destination accepts M4A.'];
  if (goal === 'fps') return ['Match the project’s frame rate', 'Use Change Frame Rate and choose the requested steady 24, 25, 30 or 60 FPS. Check color requirements separately, and play the saved clip in the editing project to check movement and sound.'];
  if (goal === 'h264' && source === 'sdr') return ['Check whether the source already fits', 'If it is already an H.264 MP4 and plays correctly in the destination, keep the original. If the codec or container does not match, make a separate H.264 MP4 compatibility copy and check the result.'];
  if (goal === 'h264') return ['Create an H.264 MP4 copy', 'Use Convert HDR to SDR for an H.264 MP4. HDR or Apple ProRes Log sources become a standard-color SDR copy; an HEVC source that is already SDR can use this workflow for codec compatibility. Keep the source if you also need an HDR or Log master.'];
  if (source === 'hdr' || source === 'log') return ['Create a standard Rec.709 SDR copy', 'Use Convert HDR to SDR with the supported HDR or Apple ProRes Log source. Keep the original and inspect the new copy’s color, sound and playback in the actual destination.'];
  return ['Your source is already SDR', 'A color conversion is not needed for an SDR requirement alone. Keep using the original if it plays correctly. If the destination also requires H.264 instead of HEVC, choose an H.264 MP4 compatibility copy.'];
}
if (typeof document !== 'undefined') {
  document.querySelectorAll('.depth-gallery').forEach(gallery => {
    const track = gallery.querySelector('.gallery-track');
    const prev = gallery.querySelector('[data-gallery-prev]');
    const next = gallery.querySelector('[data-gallery-next]');
    gallery.querySelector('.gallery-controls').hidden = false;
    const update = () => { prev.disabled = track.scrollLeft < 2; next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 2; };
    const move = direction => track.scrollBy({left: direction * (track.querySelector('.gallery-item').getBoundingClientRect().width + 24), behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
    prev.addEventListener('click', () => move(-1)); next.addEventListener('click', () => move(1));
    track.addEventListener('scroll', update, {passive: true}); window.addEventListener('resize', update); update();
  });
  const video = document.getElementById('video-workflow');
  if (video) video.addEventListener('submit', event => {
    event.preventDefault();
    const answer = videoWorkflow(document.getElementById('video-source').value, document.getElementById('video-goal').value);
    const output = document.getElementById('video-result');
    output.querySelector('h3').textContent = answer[0]; output.querySelector('p').textContent = answer[1];
  });
  const audio = document.getElementById('audio-size');
  if (audio) audio.addEventListener('submit', event => {
    event.preventDefault();
    const minutes = Number(document.getElementById('audio-minutes').value), bitrate = Number(document.getElementById('audio-bitrate').value), limit = Number(document.getElementById('audio-limit').value);
    const answer = estimateAudio(minutes, bitrate, limit), output = document.getElementById('audio-result');
    if (!answer) { output.querySelector('h3').textContent = 'Check the duration, bitrate and limit.'; output.querySelector('p').textContent = 'Use positive numbers within the ranges shown in the form.'; return; }
    output.querySelector('h3').textContent = `${minutes} minutes at ${bitrate} kbps ≈ ${answer.sizeMB.toFixed(1)} MB.`;
    const fit = answer.sizeMB >= limit ? 'This estimate reaches or exceeds your limit.' : 'The payload estimate is below your limit; leave room for overhead.';
    const lower = answer.ceilingKbps < 8 ? 'That ceiling is below the calculator’s 8 kbps minimum. Consider a shorter clip or separate parts.' : 'Choose a supported setting below the ceiling and listen to the result.';
    output.querySelector('p').textContent = `${fit} A ${limit} MB target gives a theoretical ceiling of ${answer.ceilingKbps.toFixed(1)} kbps before overhead. ${lower} Decimal MB (1,000,000 bytes); constant-bitrate audio payload only. Metadata and encoder behavior can change the actual file size. This does not convert a file.`;
  });
  const start = document.getElementById('breathing-start');
  if (start) {
    const stop = document.getElementById('breathing-stop'), phase = document.getElementById('breathing-phase'), time = document.getElementById('breathing-time'), orb = document.getElementById('breathing-orb');
    let timer = null, started = 0, lastPhase = '';
    const end = message => { clearInterval(timer); timer = null; start.disabled = false; stop.disabled = true; orb.className = 'breathing-orb'; orb.querySelector('span').textContent = 'Pause'; phase.textContent = message; time.textContent = 'One minute · six gentle rounds'; start.textContent = 'Start again'; };
    const tick = () => {
      const elapsed = Math.floor((Date.now() - started) / 1000);
      if (elapsed >= 60) { end('One minute complete. Continue when you are ready.'); return; }
      const current = elapsed % 10 < 4 ? 'Breathe in gently' : 'Breathe out gently';
      if (current !== lastPhase) { phase.textContent = current; orb.querySelector('span').textContent = current === 'Breathe in gently' ? 'In' : 'Out'; orb.classList.toggle('inhaling', current === 'Breathe in gently'); lastPhase = current; }
      time.textContent = `Round ${Math.floor(elapsed / 10) + 1} of 6 · ${60 - elapsed} seconds remaining`;
    };
    start.addEventListener('click', () => { if (timer) return; started = Date.now(); lastPhase = ''; start.disabled = true; stop.disabled = false; tick(); timer = setInterval(tick, 250); });
    stop.addEventListener('click', () => end('Stopped. Take the pause at your own pace.'));
    document.addEventListener('visibilitychange', () => { if (document.hidden && timer) end('Stopped while you were away. Restart whenever you want.'); });
    window.addEventListener('pagehide', () => { if (timer) end('Stopped.'); });
  }
}
