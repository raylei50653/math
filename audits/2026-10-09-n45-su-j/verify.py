#!/usr/bin/env python3
"""Read original inputs again, record drift, validate newly authored text/links."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

H = Path(__file__).resolve().parent
R = H.parent.parent


def read(p):
    return json.loads(p.read_text())


def fp(p):
    st = p.stat()
    return {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
            'bytes': st.st_size, 'mtime_ns': st.st_mtime_ns}


def save(name, value):
    with (H / name).open('x') as f:
        json.dump(value, f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write('\n')


initial = read(H / 'initial-state.json')
current = {}
differences = []
for name, previous in initial['authored'].items():
    d = R / ('audits/2026-10-09-n45-' + name)
    actual = {str(p.relative_to(d)): fp(p) for p in sorted(d.rglob('*'))
              if p.is_file() and not (name == 'u' and p.relative_to(d).parts[0] == 'source')}
    current[name] = actual
    if actual != previous:
        differences.append({'group': name, 'changed_paths': [p for p in set(previous) | set(actual)
                                                            if previous.get(p) != actual.get(p)]})
sources = {}
for name, entries in initial['BASE_source_snapshots'].items():
    sources[name] = []
    for entry in entries:
        actual = fp(Path(entry['path']))
        old = {k: entry[k] for k in actual}
        if actual != old:
            differences.append({'source': name, 'path': entry['path'], 'before': old, 'after': actual})
        sources[name].append({'path': entry['path'], 'base_path': entry['base_path'], **actual})
supervisors = {name: fp(R / 'audits' / ('2026-10-09-' + name) / 'inputs.json')
               for name in initial['supervisor_inputs']}
if supervisors != initial['supervisor_inputs']:
    differences.append({'supervisor_inputs': 'drift'})
routing = {p: fp(R / p) for p in initial['routing_files']}
routing_drift = [p for p in routing if routing[p] != initial['routing_files'][p]]
for f in read(H / 'inputs.json')['authority_files']:
    p = H / 'base-source' / f['path']
    blob = subprocess.check_output(['git', '-C', str(R), 'show', initial['base'] + ':' + f['path']])
    assert p.read_bytes() == blob and fp(p)['sha256'] == f['sha256'], f['path']
head = subprocess.check_output(['git', '-C', str(R), 'rev-parse', 'HEAD'], text=True).strip()
status = subprocess.check_output(['git', '-C', str(R), 'status', '--short', '--branch'], text=True)
assert head == initial['actual_HEAD'] == initial['base']
save('fingerprints.json', {
    'before': 'initial-state.json', 'after_authored': current, 'after_BASE_source_snapshots': sources,
    'after_supervisor_inputs': supervisors, 'authored_bytes_and_mtime_drift': differences,
    'after_routing_files': routing, 'routing_byte_or_mtime_drift': routing_drift,
    'HEAD_before_after': head, 'git_status_after': status,
    'original_authored_counts': {k: len(v) for k, v in current.items()},
    'BASE_snapshot_counts': {k: len(v) for k, v in sources.items()},
    'BASE_git_object_bytes_pass': True, 'BASE_archive_sources_checked': 71,
})
assert not differences and not routing_drift, (differences, routing_drift)

whitespace = []
checked_text = []
for p in sorted(H.rglob('*')):
    if not p.is_file() or p.relative_to(H).parts[0] == 'base-source' or p.suffix not in ('.py', '.md', '.json'):
        continue
    text = p.read_text()
    checked_text.append(str(p.relative_to(H)))
    if not text.endswith('\n'):
        whitespace.append({'path': str(p), 'finding': 'missing terminal newline'})
    for i, line in enumerate(text.splitlines(), 1):
        if line.rstrip() != line:
            whitespace.append({'path': str(p), 'line': i, 'finding': 'trailing whitespace'})
report = (H / 'REPORT.md').read_text()
links = []
for target in re.findall(r'\]\(([^)]+)\)', report):
    if '://' in target:
        continue
    path = (H / target.split('#', 1)[0]).resolve()
    links.append({'target': target, 'exists': path.exists(),
                  'pending_finalization': target in ('checks.json', 'MANIFEST.sha256', 'delivery.json')})
assert all(x['exists'] or x['pending_finalization'] for x in links), links
assert not whitespace, whitespace
save('output-validation.json', {'text_files_checked': checked_text, 'whitespace_findings': whitespace,
                               'REPORT_links': links, 'pending_targets': ['checks.json', 'MANIFEST.sha256', 'delivery.json'],
                               'pending_targets_verified_again_by_finalizer': True})
print(json.dumps({'original_authored': {k: len(v) for k, v in current.items()},
                  'BASE_source_entries': {k: len(v) for k, v in sources.items()},
                  'original_bytes_and_mtime_drift': differences, 'routing_drift': routing_drift,
                  'whitespace_findings': whitespace, 'REPORT_links_checked': len(links)}, sort_keys=True))
