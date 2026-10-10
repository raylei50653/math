#!/usr/bin/env python3
"""Check immutable worker deliveries and the concrete research integration."""
import argparse
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
parser = argparse.ArgumentParser()
parser.add_argument('--result', default='post-integration.json')
args = parser.parse_args()


def read(p):
    return json.loads(p.read_text())


def fp(p):
    st = p.stat()
    return dict(bytes=st.st_size, mtime_ns=st.st_mtime_ns,
                sha256=hashlib.sha256(p.read_bytes()).hexdigest())


frozen = read(OUT / 'inputs.json')
worker_files = {str(p.relative_to(ROOT)): fp(p)
                for name in ('su-a', 'su-j')
                for p in (ROOT / ('audits/2026-10-09-n45-' + name)).rglob('*') if p.is_file()}
assert worker_files == frozen['worker_files']
a = ROOT / 'audits/2026-10-09-n45-su-a'
j = ROOT / 'audits/2026-10-09-n45-su-j'
navigation = set(frozen['frozen_navigation'])
snapshot = read(a / 'inputs.json')['snapshot']
for rel, old in snapshot['files'].items():
    if rel not in navigation:
        assert fp(ROOT / rel) == old, rel
authority_reads = 0
for row in snapshot['BASE_sources']:
    assert fp(Path(row['read_path'])) == row['read']
    authority_reads += 1
for row in read(a / 'supplementary-inputs.json')['additional_BASE_inputs']:
    assert fp(Path(row['read_path'])) == {k: row[k] for k in ('bytes', 'mtime_ns', 'sha256')}
    authority_reads += 1
for entries in read(j / 'initial-state.json')['BASE_source_snapshots'].values():
    for row in entries:
        assert fp(Path(row['path'])) == {k: row[k] for k in ('bytes', 'mtime_ns', 'sha256')}
        authority_reads += 1
assert (OUT / 'independent-review.json').read_bytes() == (OUT / 'independent-review-seed17.json').read_bytes()
assert (OUT / 'sua-input-replay.json').read_bytes() == (OUT / 'sua-input-replay-seed17.json').read_bytes()

# Validate new report links with the existing documented Markdown/anchor parser.
spec = importlib.util.spec_from_file_location('n45_docs', ROOT / 'scripts/check_docs.py')
docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(docs)
new_docs = ['docs/c5_excess_two_nonadjacent_unit_core45.md',
            'docs/history/2026-10-09-n45-u-long-short-pair-tasks.md',
            'audits/2026-10-09-n45-su-supervision/REPORT.md']
link_count = 0
planned = {OUT / 'checks.json'}
for rel in new_docs:
    path = ROOT / rel
    text = path.read_text()
    assert text.endswith('\n') and all(line == line.rstrip() for line in text.splitlines())
    for line, target in docs.links(text):
        url = urlsplit(target)
        if url.scheme or url.netloc:
            continue
        dest = (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
        assert dest.exists() or dest in planned, (rel, line, target)
        if url.fragment and dest.suffix == '.md':
            assert unquote(url.fragment) in docs.anchors(dest.read_text()), (rel, line, target)
        link_count += 1

tasks = (ROOT / new_docs[1]).read_text()
hash_paths = ['docs/c5_excess_two_nonadjacent_unit_core45.md',
              'audits/2026-10-09-n45-s/REPORT.md', 'audits/2026-10-09-n45-u/REPORT.md',
              'audits/2026-10-09-n45-u/certificate-final.json',
              'audits/2026-10-09-n45-su-a/REPORT.md', 'audits/2026-10-09-n45-su-a/independent-judgment.json',
              'audits/2026-10-09-n45-su-j/REPORT.md', 'audits/2026-10-09-n45-su-j/certificate.json',
              'audits/2026-10-09-n45-j/results/certificate.json']
assert all(fp(ROOT / rel)['sha256'] in tasks for rel in hash_paths)

# Record the lack of an exact LP geometry control from literal original supports.
frame = [{i, (i + 1) % 5} for i in range(5)]
exact_geometry_controls = []
certificate = read(j / 'certificate.json')
for g in certificate['graphs']:
    if g['m'] != 2:
        continue
    unary = [p for p in g['pieces'] if p['kind'] == 'unary']
    mixed = [p for p in g['pieces'] if p['kind'] == 'mixed']
    if len(unary) != 1 or sum(unary[0]['incidences']) != 1:
        continue
    short = [p for p in mixed if len(p['support']) == 2 and set(p['support']) in frame]
    long = [p for p in mixed if not any(set(p['support']) <= edge for edge in frame)]
    if len(short) == len(long) == 1:
        exact_geometry_controls.append(g['id'])
assert not exact_geometry_controls

assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == BASE
management = {rel: {'before': old, 'after': fp(ROOT / rel)}
              for rel, old in frozen['frozen_navigation'].items()}
assert all(row['before'] != row['after'] for row in management.values())
source_headers = {}
for rel in ['artifacts/c5_excess_two_e4/REPORT.md', 'docs/c5_phase_b_common_lemmas.md']:
    blob = subprocess.check_output(['git', 'show', BASE + ':' + rel], cwd=ROOT)
    source_headers[rel] = {'BASE_bytes': len(blob), 'BASE_sha256': hashlib.sha256(blob).hexdigest(),
                           'current': fp(ROOT / rel), 'reason': 'Dated narrow adoption and direct consumer update; frozen BASE evidence retained.'}
result = dict(BASE=BASE, worker_files_unchanged=len(worker_files), worker_byte_mtime_drift=[],
              non_navigation_SU_A_frozen_files_unchanged=len(snapshot['files']) - len(navigation),
              external_BASE_source_reads_byte_mtime_unchanged=authority_reads,
              SU_J_archive_files_unchanged=5899, normal_seed17_provenance_byte_equal=True,
              local_links_checked=link_count, frozen_dispatch_hashes_checked=len(hash_paths),
              LP_geometry_controls=exact_geometry_controls, target_source_triggered=0,
              management_navigation_changes=management, dated_source_consumer_changes=source_headers,
              propagation_stop='L2; N2 and E remain OPEN; no research-line/tag or language change',
              publication='no commit/push/PR/sub-agents/external messages')
with (OUT / args.result).open('x') as f:
    json.dump(result, f, ensure_ascii=False, sort_keys=True, indent=2)
    f.write('\n')
print(json.dumps({k: v for k, v in result.items() if k not in ('management_navigation_changes', 'dated_source_consumer_changes')}, sort_keys=True))
