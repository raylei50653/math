#!/usr/bin/env python3
"""Replay the received candidate in new directories; preserve original bytes."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT / 'candidate-original/t1_broad_probe'


def queries():
    source = ROOT / 'frozen/audits/2026-10-13-c8-terminal-s1-d521163/review/independent_transfer.py'
    tree = ast.parse(source.read_text())
    return next(ast.literal_eval(node.value) for node in tree.body
                if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'QUERIES' for t in node.targets))


def validate_slot(records, kind, pair):
    """Bind every record to its file slot and frozen source, including multiplicity."""
    expected = queries()
    assert len(records) == len(expected)
    assert [r['query'] for r in records] == [q[0] for q in expected]
    for record, (name, collar, target) in zip(records, expected):
        assert record['kind'] == kind and record['pair'] == pair
        assert record['query'] == name and record['collar'] == list(collar)
        assert record['target'] == target


def check_index(directory):
    for kind in ('PINCH', 'BRIDGE'):
        for pair in range(4):
            records = json.loads((directory / f'twohole_{kind}_{pair}.json').read_text())['records']
            validate_slot(records, kind, pair)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_custody():
    manifest = json.loads((ORIGINAL / 'MANIFEST.json').read_text())
    assert set(manifest) == {p.name for p in ORIGINAL.iterdir() if p.name != 'MANIFEST.json'}
    for name, record in manifest.items():
        path = ORIGINAL / name
        assert path.stat().st_size == record['bytes'], name
        assert digest(path) == record['sha256'], name
    inputs = json.loads((ROOT / 'INPUTS.json').read_text())
    archive = ROOT / 'frozen/T1_generalization_candidate.zip'
    assert digest(archive) == inputs['candidate_archive']['sha256']
    assert (ROOT / 'frozen/T1_generalization_notes.md').read_bytes() == (ORIGINAL / 'T1_generalization_notes.md').read_bytes()
    for record in inputs['inputs']:
        assert digest(ROOT / 'frozen' / record['path']) == record['sha256'], record['path']
    check_index(ORIGINAL)
    return len(manifest)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('normal', 'seed17', 'check'))
    parser.add_argument('--output-dir', type=Path, help='New exclusive replay directory; must not exist')
    args = parser.parse_args()
    custody_files = check_custody()
    if args.mode == 'check':
        print(json.dumps({'status': 'PASS', 'candidate_manifest_files': custody_files}))
        return
    run = (args.output_dir or (ROOT / ('replay-' + args.mode))).resolve()
    run.mkdir()  # exclusive; never overwrite an earlier replay
    for path in ORIGINAL.glob('*.py'):
        shutil.copyfile(path, run / path.name)
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env.pop('PYTHONHASHSEED', None)
    if args.mode == 'seed17':
        env['PYTHONHASHSEED'] = '17'
    commands = []
    for script in ('twohole_fast.py', 'independent_verify.py', 'negative_controls.py'):
        command = [sys.executable, '-B', script]
        with (run / (script + '.log')).open('x') as log:
            result = subprocess.run(command, cwd=run, env=env, stdout=log, stderr=subprocess.STDOUT)
        commands.append({'command': command, 'returncode': result.returncode})
        assert result.returncode == 0, (args.mode, script, result.returncode)
        print(args.mode, script, 'PASS', flush=True)
    outputs = sorted([*run.glob('twohole_*.json'), *run.glob('independent_*.json'),
                      *run.glob('independent_full_lifts_*.jsonl.gz'), run / 'controls.json'])
    assert len(outputs) == 25
    check_index(run)
    hashes = {}
    for path in outputs:
        assert path.read_bytes() == (ORIGINAL / path.name).read_bytes(), ('candidate byte mismatch', path.name)
        hashes[path.name] = digest(path)
    rectangles = {'PINCH': 0, 'BRIDGE': 0}
    cases = {'PINCH': 0, 'BRIDGE': 0}
    possible = set()
    lifts = 0
    for path in run.glob('twohole_*.json'):
        data = json.loads(path.read_text())
        assert data['rows'] == sorted(data['rows']) and len(data['rows']) == 31
        for record in data['records']:
            kind = record['kind']
            cases[kind] += 1
            rectangles[kind] += len(record['rectangles'])
            lifts += sum(record['shell_lift_counts'])
            for a, b, ka, kb, output, missing in record['rectangles']:
                assert missing & 512 and not output & 512
                possible.add(output)
    assert cases == {'PINCH': 32, 'BRIDGE': 32}
    assert rectangles == {'PINCH': 512568, 'BRIDGE': 188452}
    assert possible == {0, 165, 424, 429} and lifts == 59156
    check_custody()
    summary = {'status': 'PASS', 'mode': args.mode, 'commands': commands,
               'candidate_manifest_files': custody_files, 'byte_identical_outputs': hashes,
               'cases': cases, 'rectangles': rectangles, 'shell_literal_lifts': lifts,
               'possible_masks': sorted(possible), 'common_missing_row': '01232',
               'original_candidate_unchanged': True}
    (run / 'REPLAY.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k not in ('commands', 'byte_identical_outputs')}))


if __name__ == '__main__':
    main()
