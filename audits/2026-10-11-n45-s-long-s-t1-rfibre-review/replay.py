#!/usr/bin/env python3
"""Native T1 read-only replay guarded by exact immutable input/old-B pins."""
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TARGET = REPO / 'audits/2026-10-11-n45-s-long-s-t1-rfibre'
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'
UTILITY = REPO / 'audits/2026-10-11-n45-s-long-s-t2-q2-restore-review/capture.py'
spec = importlib.util.spec_from_file_location('root_native_capture_utility', UTILITY)
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)


def snapshot():
    inputs = json.loads((TARGET / 'custody-before.json').read_bytes())['immutable_inputs']
    old_manifest = REPO / 'audits/2026-10-11-n45-s-long-s-rfibre-dispatch/authority/sealed/audits/2026-10-11-n45-s-long-s-fibre/delivery.json'
    payload = json.loads(old_manifest.read_bytes())['files']
    original_B = REPO / 'audits/2026-10-11-n45-s-long-s-fibre'
    guarded = dict(inputs)
    for item in payload:
        name = str((original_B / item['path']).relative_to(REPO))
        value = {k: item[k] for k in ('bytes', 'sha256')}
        assert name not in guarded or guarded[name] == value
        guarded[name] = value
    live = {name: capture.pin(REPO / name) for name in sorted(guarded)}
    assert live == guarded, 'immutable or original B payload drift'
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()
    diff = subprocess.check_output(['git', 'diff', '--binary', 'HEAD'], cwd=REPO)
    assert head == BASE and diff == b''
    return {'target_tree': capture.tree(TARGET), 'guarded_original_files': live,
            'head': head, 'tracked_diff_bytes': len(diff), 'capture_utility': capture.pin(UTILITY)}


def main():
    before = snapshot()
    capture.write(HERE, 'custody-before.json', before)
    command = [sys.executable, '-B', str(TARGET / 'calibrate.py'), '--check']
    specs = [('normal', command, {}, 0), ('seed17', command, {'PYTHONHASHSEED': '17'}, 0),
             ('corrupt-certificate', command + ['--certificate', str(TARGET / 'negative-corrupt-certificate.json')], {}, 1),
             ('contents-manifest', [sys.executable, '-B', str(TARGET / 'validate.py'), '--contents', '--manifest'], {}, 0)]
    with ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(lambda args: capture.run(HERE, *args), specs))
    after = snapshot()
    capture.write(HERE, 'custody-after.json', after)
    assert before == after
    equality = all((HERE / f'logs/normal.{kind}.log').read_bytes() == (HERE / f'logs/seed17.{kind}.log').read_bytes()
                   for kind in ('stdout', 'stderr'))
    negative_stage = 'certificate bytes mismatch' in (HERE / 'logs/corrupt-certificate.stderr.log').read_text()
    good = equality and negative_stage and all(r['expected_exit_observed'] for r in records)
    capture.write(HERE, 'checks.json', {'base': BASE, 'checks_pass': good, 'runs': records,
                                      'normal_seed17_stdout_stderr_byte_equal': equality,
                                      'corrupt_certificate_expected_stage': negative_stage,
                                      'original_tree_and_guarded_inputs_zero_drift': True,
                                      'guarded_distinct_original_files': len(before['guarded_original_files']),
                                      'immutable_inputs': 49, 'old_B_payload': 846,
                                      'reviewed_delivery': capture.pin(TARGET / 'delivery.json'),
                                      'utility_use': 'root native capture helper only; no same-wave mathematical result used',
                                      'scope': 'bounded palettes and named minor skeletons, no target source'})
    assert good
    print(json.dumps({'checks_pass': good, 'seed_byte_equal': equality, 'zero_drift': True}))


if __name__ == '__main__':
    main()
