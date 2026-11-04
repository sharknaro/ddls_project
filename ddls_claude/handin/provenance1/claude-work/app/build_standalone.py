#!/usr/bin/env python3
"""Inline data.js into index.html to produce one shareable, self-contained file.

The result needs no server, no internet and no accompanying files: it can be emailed as an
attachment and opened by double-clicking. Run build_data.py first if the analysis changed.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'findings_standalone.html'

html = (HERE / 'index.html').read_text(encoding='utf-8')
data = (HERE / 'data.js').read_text(encoding='utf-8')

tag = '<script src="data.js"></script>'
if tag not in html:
    raise SystemExit('could not find the data.js script tag in index.html')

# Guard against the data accidentally terminating the script element.
if '</script' in data.lower():
    raise SystemExit('data.js contains a closing script tag; refusing to inline')

html = html.replace(tag, '<script>\n' + data + '</script>')
OUT.write_text(html, encoding='utf-8')
print(f'Wrote {OUT}  ({len(html) / 1024:.0f} KB, single file, no dependencies)')
