#!/usr/bin/env python3
"""Seal/check this audit's exact regular-file inventory, not its mathematics."""
from pathlib import Path
import datetime
import hashlib
import json
import sys

OUT = Path(__file__).resolve().parent
EXCLUDED = {'MANIFEST.sha256', 'delivery.json'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inventory():
    paths = sorted(str(p.relative_to(OUT)) for p in OUT.rglob('*') if p.is_file())
    assert not any(p.is_symlink() for p in OUT.rglob('*'))
    return paths


def check():
    entries = {}
    for line in (OUT / 'MANIFEST.sha256').read_text().splitlines():
        digest, rel = line.split('  ', 1)
        assert rel not in entries
        entries[rel] = digest
    actual = inventory()
    assert set(entries) == set(actual) - EXCLUDED
    for rel, digest in entries.items():
        assert sha((OUT / rel).read_bytes()) == digest, rel
    d = json.loads((OUT / 'delivery.json').read_text())
    assert d['regular_inventory'] == actual
    assert d['payload_file_count'] == len(entries)
    assert d['regular_file_count'] == len(actual)
    assert sha((OUT / 'MANIFEST.sha256').read_bytes()) == d['manifest_sha256']
    assert sha((OUT / 'REPORT.md').read_bytes()) == d['report_sha256']
    assert sha((OUT / 'independent-judgment.json').read_bytes()) == d['judgment_sha256']
    seal = json.loads((OUT / 'judgment-seal.json').read_text())
    assert d['judgment_sha256'] == seal['sha256']
    return {'task': 'N45-SSA', 'exact_inventory_and_hashes': True,
            'payload_file_count': len(entries), 'regular_file_count': len(actual),
            'manifest_sha256': d['manifest_sha256'], 'report_sha256': d['report_sha256'],
            'judgment_sha256': d['judgment_sha256'],
            'delivery_sha256': sha((OUT / 'delivery.json').read_bytes())}


def main():
    assert sys.argv[1:] in ([], ['--check'])
    if not sys.argv[1:]:
        paths = [p for p in inventory() if p not in EXCLUDED]
        manifest = ''.join(sha((OUT / rel).read_bytes()) + '  ' + rel + '\n' for rel in paths)
        (OUT / 'MANIFEST.sha256').write_text(manifest)
        all_paths = sorted(paths + list(EXCLUDED))
        d = {'task': 'N45-SSA', 'base': 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744',
             'sealed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'output': 'audits/2026-10-10-n45-ssa', 'mathematical_decision':
             '11 SS claims hold within the complete SS contract; narrow parent U composition holds.',
             'block': False, 'formal_adoption': 'supervisor decision pending',
             'manifest': 'MANIFEST.sha256', 'manifest_sha256': sha(manifest.encode()),
             'report': 'REPORT.md', 'report_sha256': sha((OUT / 'REPORT.md').read_bytes()),
             'judgment': 'independent-judgment.json',
             'judgment_sha256': sha((OUT / 'independent-judgment.json').read_bytes()),
             'payload_file_count': len(paths), 'regular_file_count': len(all_paths),
             'excluded_from_payload_manifest': sorted(EXCLUDED),
             'exclusion_reason': 'Manifest/delivery self-reference; both are included in exact regular inventory.',
             'regular_inventory': all_paths, 'new_finite_SS_source_certificate': False,
             'new_Lean': False, 'new_source_realization': False,
             'artifact_checks_are_mathematical_proof': False,
             'shared_files_modified': False, 'original_worker_verifier_run': False,
             'commit_push_PR_external_messages_subagents': False}
        (OUT / 'delivery.json').write_text(json.dumps(d, indent=2) + '\n')
    print(json.dumps(check(), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
