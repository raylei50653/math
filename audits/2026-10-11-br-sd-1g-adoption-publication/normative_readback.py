#!/usr/bin/env python3
"""Ensure the adoption preserves earlier canonical normative sections literally."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = 'c15a635e17d4be814e19aeeeeb765f3d6024099a'
NAME = 'docs/c5_excess_two_nonadjacent_unit_core45.md'

def between(text, start, end):
    return text[text.index(start):text.index(end, text.index(start))]

def main():
    before = subprocess.check_output(['git', 'show', BASE + ':' + NAME], cwd=ROOT).decode()
    after = (ROOT / NAME).read_text()
    pieces = [
        ('canonical-common-contract', '## 1. 全部共同前提與原身份', '## 2. 已採納結論與必要化約'),
        ('existing-2.1-through-2.10', '### 2.1 N45-U-LP', '### 2.11 單缺額查證'),
    ]
    rows = []
    for label, start, end in pieces:
        old, new = between(before, start, end), between(after, start, end)
        if old != new:
            raise SystemExit('unapproved normative change: ' + label)
        rows.append(dict(name=label, sha256=hashlib.sha256(old.encode()).hexdigest(), unchanged=True))
    start = '### 2.11 單缺額查證與無 U 二連通子域'
    old = between(before, start, '## 3. 精確 OPEN 與下一個窄分支')
    new = between(after, start, '**BR-SD-1g canonical 採納')
    if old != new:
        raise SystemExit('unapproved changes to SD-A or existing1a/1c/1e contracts')
    rows.append(dict(name='existing-2.11-through-1e', sha256=hashlib.sha256(old.encode()).hexdigest(), unchanged=True))
    for name in ('docs/HANDOFF.md', 'docs/STATUS_HISTORY.md', 'README.md'):
        old = subprocess.check_output(['git', 'show', BASE + ':' + name], cwd=ROOT)
        if old != (ROOT / name).read_bytes():
            raise SystemExit('unexpected routing/snapshot change: ' + name)
        rows.append(dict(name=name, sha256=hashlib.sha256(old).hexdigest(), unchanged=True))
    print(json.dumps(dict(base=BASE, status='triggered and holds', rows=rows), sort_keys=True))

if __name__ == '__main__':
    main()
