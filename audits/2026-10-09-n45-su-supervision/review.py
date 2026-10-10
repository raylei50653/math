#!/usr/bin/env python3
"""Independent delivery/provenance checks; does not import worker decisions.

Run before navigation changes. Results use exclusive creation. The subsequent
manager edit of shared navigation is recorded separately, not called drift-free.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
A = ROOT / 'audits/2026-10-09-n45-su-a'
J = ROOT / 'audits/2026-10-09-n45-su-j'


def read(p):
    return json.loads(p.read_text())


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def record(p):
    st = p.stat()
    return dict(bytes=st.st_size, mtime_ns=st.st_mtime_ns, sha256=sha(p.read_bytes()))


def save(name, data):
    with (OUT / name).open('x') as f:
        json.dump(data, f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write('\n')


def manifest(directory):
    rows = {}
    for line in (directory / 'MANIFEST.sha256').read_text().splitlines():
        digest, rel = line.split('  ', 1)
        assert rel not in rows and re.fullmatch('[0-9a-f]{64}', digest)
        path = directory / rel
        assert path.resolve().is_relative_to(directory.resolve())
        assert sha(path.read_bytes()) == digest, rel
        rows[rel] = digest
    actual = {str(p.relative_to(directory)) for p in directory.rglob('*') if p.is_file()}
    assert actual == set(rows) | {'MANIFEST.sha256', 'delivery.json'}
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--result', required=True)
    parser.add_argument('--freeze', action='store_true')
    args = parser.parse_args()
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == BASE
    a_delivery = read(A / 'delivery.json')
    a_rows = manifest(A)
    assert len(a_rows) == 56 and len(a_delivery['files']) == 57
    assert {r['path'] for r in a_delivery['files']} == set(a_rows) | {'MANIFEST.sha256'}
    for row in a_delivery['files']:
        rr = record(A / row['path'])
        assert rr['sha256'] == row['sha256'] and rr['bytes'] == row['bytes']
    j_delivery = read(J / 'delivery.json')
    j_rows = manifest(J)
    assert len(j_rows) == j_delivery['manifest_entries'] == 5952
    assert sum(p.startswith('base-source/') for p in j_rows) == 5899
    assert sha((J / 'MANIFEST.sha256').read_bytes()) == j_delivery['manifest_sha256']
    assert a_delivery['actual_HEAD'] == j_delivery['actual_HEAD'] == BASE

    # Recheck the paper auditor's complete frozen provenance, not its saved PASS.
    a_snapshot = read(A / 'inputs.json')['snapshot']
    for rel, old in a_snapshot['files'].items():
        assert record(ROOT / rel) == old, rel
    sources = []
    for row in a_snapshot['BASE_sources']:
        assert record(Path(row['read_path'])) == row['read']
        sources.append((row['path'], row['read_path'], row['declared_sha256']))
    supplement = read(A / 'supplementary-inputs.json')
    for key in ('A_findings_inputs', 'comparison_reports'):
        for rel, old in supplement[key].items():
            assert record(ROOT / rel) == old, rel
    for row in supplement['additional_BASE_inputs']:
        assert record(Path(row['read_path'])) == {k: row[k] for k in ('bytes', 'mtime_ns', 'sha256')}
        sources.append((row['path'], row['read_path'], row['sha256']))

    j_snapshot = read(J / 'initial-state.json')
    for group, old in j_snapshot['authored'].items():
        folder = ROOT / ('audits/2026-10-09-n45-' + group)
        current = {str(p.relative_to(folder)): record(p) for p in folder.rglob('*')
                   if p.is_file() and not (group == 'u' and p.relative_to(folder).parts[0] == 'source')}
        assert current == old, group
    for group, entries in j_snapshot['BASE_source_snapshots'].items():
        for row in entries:
            assert record(Path(row['path'])) == {k: row[k] for k in ('bytes', 'mtime_ns', 'sha256')}
            sources.append((row['base_path'], row['path'], row['sha256']))
    for rel, old in j_snapshot['routing_files'].items():
        assert record(ROOT / rel) == old, rel
    for row in read(J / 'inputs.json')['authority_files']:
        sources.append((row['path'], str(J / 'base-source' / row['path']), row['sha256']))

    # Independent batch Git-object read: all declared read paths remain literal BASE bytes.
    paths = sorted({rel for rel, _, _ in sources})
    request = ''.join(BASE + ':' + rel + '\n' for rel in paths).encode()
    raw = subprocess.check_output(['git', 'cat-file', '--batch'], input=request, cwd=ROOT)
    cursor = 0
    blobs = {}
    for rel in paths:
        end = raw.index(b'\n', cursor)
        oid, kind, size = raw[cursor:end].split()
        assert kind == b'blob'
        cursor = end + 1
        size = int(size)
        blobs[rel] = raw[cursor:cursor + size]
        cursor += size + 1
    assert cursor == len(raw)
    for rel, read_path, digest in sources:
        assert Path(read_path).read_bytes() == blobs[rel] and sha(blobs[rel]) == digest

    claims = read(A / 'independent-judgment.json')
    expected_ids = ['N45-S-' + str(i).zfill(2) for i in range(1, 7)] + [
        'N45-U-' + x for x in ('REL', 'WIT', 'CROSS', 'CAP', 'S3', 'U2', 'SHORT', 'RES')]
    assert [c['CLAIM'] for c in claims['claims']] == expected_ids
    assert claims['counts']['new_proof_gaps'] == 0
    sealed = sha((A / 'independent-judgment.json').read_bytes())
    assert sealed == (A / 'independent-judgment.sha256').read_text().split()[0]
    comparison = read(A / 'supervision-comparison.json')
    assert comparison['independent_sealed_sha256'] == sealed
    assert not comparison['disagreements'] and len(comparison['comparisons']) == 14
    assert claims['sealed_UTC'] < comparison['compared_UTC']
    assert not claims['supervision_decisions_read_before_seal']
    assert (A / 'input-verification.json').read_bytes() == (A / 'input-verification-seed17.json').read_bytes()
    assert sha((A / 'gallai.pdf').read_bytes()) == '50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea'

    # Validate the declared independent finite payload and its direct comparison data.
    certificate = read(J / 'certificate.json')
    assert sha((J / 'checker.py').read_bytes()) == certificate['checker_sha256']
    assert sha((J / 'inputs.json').read_bytes()) == certificate['inputs_sha256']
    assert sha((J / 'certificate.json').read_bytes()) == 'a4b5b4c148f823f8df22a2672700eb40516bae0fd673edf8210a477af3b508ee'
    cc = certificate['counts']
    assert cc['original_root_pair_queries'] + cc['derivative_root_pair_queries'] + cc['contact_edge_deleted_root_pair_queries'] + cc['S_spoke_root_pair_queries'] == 7952
    assert cc['piece_relations'] == 690 and cc['full_piece_lifts'] == 2986
    assert cc['capacity_G_triggered and holds'] + cc['capacity_X_triggered and holds'] == 102
    assert cc['target_source_triggered'] == cc['source_counterexamples'] == 0
    assert not read(J / 'supervisor-comparison.json')['semantic_differences']
    for command in read(J / 'checks.json')['commands_and_logs']:
        assert sha((J / command['log']).read_bytes()) == command['log_sha256']
        assert command['exit'] == command['expected_exit']

    # All new worker outputs, including the exact BASE archive, are immutable.
    frozen = {str(p.relative_to(ROOT)): record(p) for directory in (A, J)
              for p in sorted(directory.rglob('*')) if p.is_file()}
    details = {'BASE': BASE, 'SU_A_manifest_payloads': len(a_rows), 'SU_A_with_manifest_delivery': 58,
               'SU_J_manifest_entries': len(j_rows), 'SU_J_archive_files': 5899, 'SU_J_authored_with_seals': 55,
               'SU_A_frozen_files_verified': len(a_snapshot['files']),
               'SU_A_BASE_declared_rows': len(a_snapshot['BASE_sources']), 'supplementary_BASE_rows': 17,
               'unique_authority_paths_verified': len(paths), 'BASE_read_paths_checked': len(sources),
               'paper_claim_ids': expected_ids, 'finite_counts': cc,
               'independence_boundary': 'Sealed record and chronology attestations checked; read history is not mechanically provable.',
               'finite_scope': 'Worker checker read and replayed separately; this script checks provenance and payload declarations.'}
    if args.freeze:
        save('inputs.json', {'BASE': BASE, 'worker_files': frozen,
                            'frozen_navigation': {rel: record(ROOT / rel) for rel in j_snapshot['routing_files']},
                            'verified_details': details})
    else:
        assert frozen == read(OUT / 'inputs.json')['worker_files']
    save(args.result, details)
    print(json.dumps({k: v for k, v in details.items() if k not in ('finite_counts', 'paper_claim_ids')}, sort_keys=True))


if __name__ == '__main__':
    main()
