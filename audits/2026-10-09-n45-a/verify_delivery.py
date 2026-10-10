#!/usr/bin/env python3
"""Read-only verification of this delivery's source freeze, links and manifest."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--sealed', action='store_true')
a = p.parse_args()
inputs = json.loads((HERE / 'inputs.json').read_text())
root = Path(inputs['source_worktree'])
main = HERE.parents[1]
records = inputs['BASE_inputs'] + json.loads((HERE / 'validation-inputs.json').read_text())['files']
changed = []
for r in records:
    if r.get('exists') is False:
        continue
    if hashlib.sha256((root / r['path']).read_bytes()).hexdigest() != r['sha256']:
        changed.append(r['path'])
assert not changed, changed
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip() == inputs['BASE']
assert not subprocess.check_output(['git', 'status', '--porcelain'], cwd=root, text=True)
preexisting = []
for name, info in inputs['main_preexisting_nonBASE_files'].items():
    if hashlib.sha256((main / name).read_bytes()).hexdigest() != info['sha256']:
        preexisting.append(name)
# Other tasks may work in main; this audit reports any observed drift without rewriting it.
spec = importlib.util.spec_from_file_location('frozen_docs_check', root / 'scripts/check_docs.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
errors = []
links = 0
planned = {HERE / 'checks.json', HERE / 'MANIFEST.json'}
for line, destination in m.links((HERE / 'REPORT.md').read_text()):
    u = urlsplit(destination)
    if u.scheme or u.netloc:
        continue
    target = (HERE / unquote(u.path)).resolve() if u.path else HERE / 'REPORT.md'
    links += 1
    if not target.exists():
        if not a.sealed and target in planned:
            continue
        errors.append(f'line {line}: missing {destination}')
        continue
    if u.fragment and unquote(u.fragment) not in m.anchors(target.read_text()):
        errors.append(f'line {line}: bad anchor {destination}')
assert not errors, errors
whitespace = []
for path in HERE.rglob('*'):
    if path.is_file() and path.suffix in ('.py', '.md', '.json'):
        for i, line in enumerate(path.read_text().splitlines(), 1):
            if line.rstrip() != line:
                whitespace.append(f'{path.relative_to(HERE)}:{i}')
assert not whitespace, whitespace
if a.sealed:
    manifest = json.loads((HERE / 'MANIFEST.json').read_text())
    for name, info in manifest['files'].items():
        raw = (HERE / name).read_bytes()
        assert len(raw) == info['bytes'] and hashlib.sha256(raw).hexdigest() == info['sha256'], name
    actual = {p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file()}
    assert actual == set(manifest['files']) | {'MANIFEST.json'}, actual ^ set(manifest['files']) ^ {'MANIFEST.json'}
print(json.dumps({'source_inputs_unchanged': len({r['path'] for r in records}),
                  'source_HEAD': inputs['BASE'], 'source_worktree_clean': True,
                  'report_local_links': links, 'report_links_valid': True,
                  'task_output_whitespace_clean': True, 'sealed_manifest_verified': a.sealed,
                  'main_preexisting_file_drift': preexisting}, sort_keys=True))
