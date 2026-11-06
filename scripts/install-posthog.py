#!/usr/bin/env python3
"""Run after page generation to attach optional website analytics."""
from pathlib import Path
import argparse
root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--only', nargs='+', help='Process only these repository-relative HTML paths')
args = parser.parse_args()
pages = [root/path for path in args.only] if args.only else root.rglob('*.html')
tag = '<script defer src="/assets/posthog-init.js?v=20261022-3"></script>'
count = 0
for page in pages:
    if not page.resolve().is_relative_to(root) or page.suffix != '.html':
        raise ValueError('Expected a site HTML path')
    relative = page.relative_to(root)
    if any(part.startswith('.') or part in ('node_modules', 'vendor') for part in relative.parts):
        continue
    # Never instrument authenticated, activation or billing screens.
    if str(relative).startswith(('api/account/', 'api/stats/', 'mac/manage/', 'mac/thanks/')):
        continue
    if relative.parts[0] == 'apps' and any(part in ('privacy', 'terms', 'support') for part in relative.parts[1:-1]):
        continue
    text = page.read_text()
    if 'src="/assets/posthog-init.js?v=20261022-2"' in text:
        text = text.replace('src="/assets/posthog-init.js?v=20261022-2"', 'src="/assets/posthog-init.js?v=20261022-3"')
        page.write_text(text)
    if 'src="/assets/posthog-init.js?v=20261022"' in text:
        text = text.replace('src="/assets/posthog-init.js?v=20261022"', 'src="/assets/posthog-init.js?v=20261022-3"')
        page.write_text(text)
    if 'src="/assets/posthog-init.js"' in text:
        text = text.replace('src="/assets/posthog-init.js"', 'src="/assets/posthog-init.js?v=20261022-3"')
        page.write_text(text)
    if '/assets/posthog-init.js' not in text and '</head>' in text:
        page.write_text(text.replace('</head>', tag + '\n</head>', 1))
        count += 1
print(f'Attached analytics to {count} pages')
