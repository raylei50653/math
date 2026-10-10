#!/usr/bin/env python3
"""Read-only integrity replay for this isolated audit, never whole-worktree inventory."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--preseal', action='store_true')
    args = parser.parse_args()
    out = Path(__file__).resolve().parent
    root = out.parents[1]
    inputs = json.loads((out / 'inputs.json').read_text())
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root).decode().strip()
    assert head == inputs['base'] == inputs['head']
    base_count = 0
    for item in inputs['inputs']:
        data = (out / item['frozen']).read_bytes()
        assert sha(data) == item['sha256'], item['path']
        if item['layer'] == 'BASE-original-git-blob':
            live_blob = subprocess.check_output(['git', 'show', f"{inputs['base']}:{item['path']}"], cwd=root)
            oid = subprocess.check_output(['git', 'rev-parse', f"{inputs['base']}:{item['path']}"], cwd=root).decode().strip()
            assert live_blob == data and oid == item['git_blob'], item['path']
            base_count += 1
    judgment = json.loads((out / 'independent-judgment.json').read_text())
    assert judgment['counts']['adjudicated'] == 4
    assert judgment['counts']['out_of_scope'] == 7
    assert judgment['SSA_SSC_root_current_judgments_read_before_seal'] is False
    assert judgment['minimum_geometry_T4_block_gap'] is None
    for name in ('stdout', 'stderr'):
        assert (out / f'logs/controls-normal.{name}.log').read_bytes() == (out / f'logs/controls-seed17.{name}.log').read_bytes()
        worker = out / 'frozen/current/audits/2026-10-10-n45-u-ss/seal-checks'
        assert (worker / f'verify-sealed-normal.{name}.log').read_bytes() == (worker / f'verify-sealed-seed17.{name}.log').read_bytes()
    assert (out / 'controls.json').read_bytes() == (out / 'logs/controls-normal.stdout.log').read_bytes()
    controls = json.loads((out / 'controls.json').read_text())
    assert controls['source_graphs_created'] == 0
    assert controls['original_faces_proved_by_controls'] is False
    links = []
    pending = []
    for match in re.finditer(r'\[[^\]]*\]\(([^)]+)\)', (out / 'REPORT.md').read_text()):
        target = match.group(1).split('#')[0]
        if not target or '://' in target:
            continue
        if args.preseal and target in {'MANIFEST.sha256', 'delivery.json'}:
            pending.append(target)
        else:
            assert (out / target).exists(), target
            links.append(target)
    payload_count = None
    if not args.preseal:
        delivery = json.loads((out / 'delivery.json').read_text())
        manifest = (out / 'MANIFEST.sha256').read_bytes()
        assert sha(manifest) == delivery['manifest_sha256']
        names = []
        for line in manifest.decode().splitlines():
            digest, rel = line.split('  ', 1)
            assert sha((out / rel).read_bytes()) == digest, rel
            names.append(rel)
        actual = sorted(str(p.relative_to(out)) for p in out.rglob('*')
                        if p.is_file() and p.name not in {'MANIFEST.sha256', 'delivery.json'}
                        and 'seal-checks' not in p.relative_to(out).parts)
        assert sorted(names) == actual
        assert len(names) == delivery['payload_file_count']
        assert sha((out / 'REPORT.md').read_bytes()) == delivery['report_sha256']
        assert sha((out / 'independent-judgment.json').read_bytes()) == delivery['judgment_sha256']
        payload_count = len(names)
    print(json.dumps({'task': 'N45-SSG-read-only-integrity', 'preseal': args.preseal,
                      'head': head, 'frozen_inputs_verified': len(inputs['inputs']),
                      'BASE_original_git_blobs_verified': base_count,
                      'current_input_live_bytes_requirement': 'none after seal; frozen evidence is immutable',
                      'own_controls_normal_seed17_bytes_equal': True,
                      'worker_frozen_historical_normal_seed17_bytes_equal': True,
                      'worker_whole_worktree_inventory_replayed': False,
                      'report_local_links_checked': len(links), 'pending_seal_links': pending,
                      'sealed_payload_file_count': payload_count,
                      'mathematical_scope': 'four geometry/T4 paper claims only; not a mathematical/source checker'},
                     sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
