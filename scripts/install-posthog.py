#!/usr/bin/env python3
"""Run after page generation to attach optional website analytics."""
from pathlib import Path
root = Path(__file__).resolve().parents[1]
tag = '<script defer src="/assets/posthog-init.js"></script>'
count = 0
for page in root.rglob('*.html'):
    relative = page.relative_to(root)
    if any(part.startswith('.') or part in ('node_modules', 'vendor') for part in relative.parts):
        continue
    # Never instrument authenticated, activation or billing screens.
    if str(relative).startswith(('api/account/', 'api/stats/', 'mac/manage/', 'mac/thanks/')):
        continue
    if relative.parts[0] == 'apps' and any(part in ('privacy', 'terms', 'support') for part in relative.parts[1:-1]):
        continue
    text = page.read_text()
    if '/assets/posthog-init.js' not in text and '</head>' in text:
        page.write_text(text.replace('</head>', tag + '\n</head>', 1))
        count += 1
print(f'Attached analytics to {count} pages')
