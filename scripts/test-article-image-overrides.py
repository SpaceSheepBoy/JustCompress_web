"""Regressions for article-specific illustrations without losing verified evidence."""
from pathlib import Path
import json,tempfile
from bs4 import BeautifulSoup
from article_image_overrides import apply, normalize, ROOT

with tempfile.TemporaryDirectory() as td:
    root=Path(td);(root/'scripts').mkdir();(root/'assets/guides/editorial').mkdir(parents=True)
    (root/'assets/guides/editorial/topic.png').write_bytes(b'fixture')
    (root/'guides/topic').mkdir(parents=True)
    file=root/'guides/topic/index.html'
    file.write_text('<html><head></head><body><article class="guide-article"><h2>Steps</h2><p>Keep original.</p><figure><img src="/assets/old-generic.jpg"><figcaption>Old generic figure</figcaption></figure><figure><img src="/assets/real-step.webp"><figcaption>Actual App step</figcaption></figure><a class="guide-store-badge" href="https://apps.apple.com/us/app/id6812821310"><img src="/assets/brand/app-store-badges/en.svg"></a></article></body></html>')
    entry={'src':'/assets/guides/editorial/topic.png','width':1024,'height':1024,'alt':'Topic illustration','caption':'AI-generated conceptual illustration, not an App export.','tool':'built-in imagegen','provenance':'fixture test','remove_sources':['/assets/old-generic.jpg']}
    config=root/'scripts/article-image-overrides.json'
    config.write_text(json.dumps({'articles':{'guides/topic/index.html':entry}}))
    assert apply(root)==['guides/topic/index.html']
    first=file.read_text();assert apply(root)==[] and file.read_text()==first
    soup=BeautifulSoup(first,'html.parser')
    assert len(soup.select('[data-editorial-image]'))==1
    assert soup.select_one('meta[property="og:image"]')['content'].endswith('/topic.png')
    assert soup.select_one('[src="/assets/real-step.webp"]') and 'Actual App step' in soup.get_text()
    assert not soup.select_one('[src="/assets/old-generic.jpg"]')
    assert soup.select_one('a.guide-store-badge')['href'].endswith('id6812821310')
    assert 'Keep original.' in soup.get_text() and 'aspect-ratio:auto' in soup.select_one('[data-editorial-image] img')['style']
    entry['src']='/assets/guides/editorial/missing.png';config.write_text(json.dumps({'articles':{'guides/topic/index.html':entry}}))
    try:
        apply(root)
        raise AssertionError('Missing source asset accepted')
    except ValueError:
        pass
    assert file.read_text()==first,'Failed validation partially wrote article'
print('PASS article-image replacement, real step/CTA preservation, natural ratio, idempotence and prewrite asset validation')

# Actual legacy layouts contain neighboring newline nodes around replaced figures.
# Exercise them in memory; the production article files are never rewritten here.
for path, removed in [
    ('blog/local-file-tool-vs-cloud-tool/index.html', ['/assets/local-file-processing.svg']),
    ('guides/hdr-vs-sdr-video/index.html', ['/assets/guides/hdr-sdr/simulated-color-mismatch.jpg']),
]:
    raw=(ROOT/path).read_text()
    metadata={'src':'/assets/guides/editorial/topic.png','width':1536,'height':1024,
              'alt':'Topic illustration','caption':'AI-generated conceptual illustration, not an App export.',
              'remove_sources':removed}
    first=normalize(raw,metadata)
    assert normalize(first,metadata)==first, ('Real-layout second pass changed output',path)
    assert normalize(normalize(first,metadata),metadata)==first, ('Real-layout third pass changed output',path)
print('PASS real blog/HDR in-memory layouts are byte-stable after first image override')
