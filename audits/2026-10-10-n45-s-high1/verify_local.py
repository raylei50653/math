#!/usr/bin/env python3
"""Read-only authored-file and original-input custody checks."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def local():
    report = HERE / 'REPORT.md'
    links = 0
    for target in re.findall(r'\]\(([^\s)]+)\)', report.read_text()):
        url = urlsplit(target)
        if not url.scheme:
            assert (report.parent / unquote(url.path)).exists(), target
            assert not url.fragment, 'new report has no unchecked anchor links'
            links += 1
    count = 0
    for p in sorted(HERE.iterdir()):
        if p.is_file() and p.suffix in ('.py', '.md', '.json'):
            for n, line in enumerate(p.read_text().splitlines(), 1):
                assert line == line.rstrip(), (p.name, n, 'trailing whitespace')
                assert not line.startswith('\t'), (p.name, n, 'tab indent')
            count += 1
    print(json.dumps({'authored_report_local_links': links, 'top_level_text_files': count,
                      'status': 'PASS', 'historical_frozen_links': 'not repaired or claimed'}))


def custody():
    import checker
    checker.inputs(HERE / 'inputs.json')
    tracked = json.loads((HERE / 'tracked-custody.json').read_bytes())
    assert all(sha(ROOT / p) == h for p, h in tracked.items()), 'tracked-file byte drift'
    scope = 'audits/2026-10-10-n45-s-high1/'
    old = (HERE / 'git-status-start.txt').read_text().splitlines()
    new = subprocess.check_output(['git', 'status', '--porcelain=v1', '--untracked-files=all'], cwd=ROOT, text=True).splitlines()
    clean = lambda xs: [x for x in xs if scope not in x]
    assert clean(old) == clean(new), 'Git state changed outside exclusive audit'
    print(json.dumps({'status': 'PASS', 'frozen_inputs': 34, 'task_pins': 9,
                      'tracked_files_unchanged': len(tracked), 'outside_audit_Git_drift': 0,
                      'old_untracked_audits': 'consulted inputs hashed; no whole untracked-tree custody claim'}))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--custody', action='store_true')
    args = p.parse_args()
    custody() if args.custody else local()
