#!/usr/bin/env python3
"""Assemble the flat submission package, matching the course example's layout.

Produces: report.md, slides.html, app.zip, analysis-transcript.md, ddls-interview.md,
AGENTS.md, spec.md
"""
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PKG = Path(__file__).resolve().parent
HANDIN = ROOT / 'ddls_claude' / 'handin'

# ---- straight copies -----------------------------------------------------------------
shutil.copy(HANDIN / 'code_and_app.zip', PKG / 'app.zip')
shutil.copy(ROOT / 'ouput' / 'md' / 'AGENTS.md', PKG / 'AGENTS.md')
shutil.copy(ROOT / 'ouput' / 'md' / 'spec.md', PKG / 'spec.md')

# ---- interview transcripts -> one markdown file --------------------------------------
INTERVIEWS = [
    ('First data-owner interview', '2026-10-20', 'data/20261020_pi_transcript.txt'),
    ('Second data-owner interview', '2026-10-23', 'data/20261023_ddls_project_meeting2_transcript.txt'),
]
parts = [
    '# Data-owner interview transcripts\n',
    'Automatically transcribed from recorded meetings with the data owner. **These are raw '
    'machine transcripts and contain recognition errors** — for example "Western blood" for '
    'Western blot and "fault change" for fold change. They were never treated as verified '
    'technical terms; where a reading mattered it was checked against the workbook or raised '
    'with the owner.\n',
]
for title, date, rel in INTERVIEWS:
    text = (ROOT / rel).read_text(encoding='utf-8', errors='replace').strip()
    parts += [f'\n---\n\n## {title}\n', f'**Date:** {date} · **Source:** `{rel}`\n', text, '\n']
(PKG / 'ddls-interview.md').write_text('\n'.join(parts), encoding='utf-8')

# ---- Claude session JSONL -> readable markdown ---------------------------------------
MAX_BLOCK = 2000   # characters kept per tool result / long block


def clip(s, n=MAX_BLOCK):
    s = s.rstrip()
    return s if len(s) <= n else s[:n] + f'\n… [truncated, {len(s) - n} more characters]'


def render(jsonl_bytes, heading):
    out = [heading]
    for line in jsonl_bytes.decode('utf-8', errors='replace').splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        role = e.get('type') or e.get('role')
        msg = e.get('message') or {}
        content = msg.get('content', e.get('content'))
        if role not in ('user', 'assistant') or content is None:
            continue
        blocks = content if isinstance(content, list) else [{'type': 'text', 'text': str(content)}]
        rendered = []
        for b in blocks:
            if not isinstance(b, dict):
                continue
            t = b.get('type')
            if t == 'text' and b.get('text', '').strip():
                rendered.append(clip(b['text']))
            elif t == 'thinking' and b.get('thinking', '').strip():
                rendered.append('> *(reasoning)* ' + clip(b['thinking'], 800).replace('\n', '\n> '))
            elif t == 'tool_use':
                inp = json.dumps(b.get('input', {}), indent=1)[:MAX_BLOCK]
                rendered.append(f"**▸ tool call — `{b.get('name')}`**\n\n```json\n{inp}\n```")
            elif t == 'tool_result':
                c = b.get('content')
                if isinstance(c, list):
                    c = '\n'.join(x.get('text', '') for x in c if isinstance(x, dict))
                if c and str(c).strip():
                    rendered.append(f'**◂ result**\n\n```\n{clip(str(c))}\n```')
        if rendered:
            who = 'Person (prompt)' if role == 'user' else 'Claude'
            out.append(f'\n### {who}\n\n' + '\n\n'.join(rendered))
    return '\n'.join(out)


src = HANDIN / 'transcripts' / 'claude-session-export.zip'
md = ['# Analysis transcript — Claude Code session\n',
      'Complete record of the AI-assisted analysis: every prompt, tool call, script and '
      'intermediate result, including the mistakes and dead ends. Long tool outputs are '
      'truncated for readability; the unabridged JSONL is in `app.zip`-adjacent session '
      'export held by the author.\n',
      '**Roles:** *Person (prompt)* is the author directing the work. *Claude* is the AI '
      'assistant. Tool calls and their results are shown inline.\n']
with zipfile.ZipFile(src) as z:
    names = z.namelist()
    main = next(n for n in names if n.endswith('transcript.jsonl'))
    md.append(render(z.read(main), '\n---\n\n## Main session\n'))
    for n in sorted(x for x in names if '/subagents/' in x and x.endswith('.jsonl')):
        agent = n.split('/')[-1].replace('.jsonl', '')
        md.append(render(z.read(n), f'\n---\n\n## Subagent: {agent}\n'
                                    '\nLaunched to read one of the supplied PDFs in full.\n'))
(PKG / 'analysis-transcript.md').write_text('\n'.join(md), encoding='utf-8')

print('Package assembled:')
for p in sorted(PKG.iterdir()):
    if p.suffix in ('.md', '.html', '.zip'):
        print(f'  {p.name:28s} {p.stat().st_size/1024:8.0f} KB')
