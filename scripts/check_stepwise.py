#!/usr/bin/env python3
"""Re-run the four stepwise trial scripts and compare key numbers with artifacts/stepwise/.

python scripts/check_stepwise.py        # ~20 s, pure stdlib

Each script rewrites its own JSON; this runner snapshots the stored JSON first, reruns,
and reports every key figure that changed.  Exit status 1 on any mismatch.
"""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/stepwise'
RUNS = {
    'stepwise_sufficiency.py': ('first_run.json', [
        ('part_a_uncoloured', 'completable'),
        ('part_b_compressed_inside_state', 'three_profile', 'distinguished'),
        ('part_b_compressed_inside_state', 'pairs', 'distinguished'),
        ('part_c_stepwise', 'window_sufficiency', '3', 'depth4', 'insufficient'),
        ('part_c_stepwise', 'dead_branch_detection', 'depth4', 'unseen_by_either'),
        ('part_c_stepwise', 'dead_branch_detection', 'depth3', 'unseen_by_either'),
    ]),
    'stepwise_local_fail.py': ('local_fail.json', [
        ('table', 'depth4', 'dead'),
        ('table', 'depth4', 'certified', 'tail3', 'fixed_outside'),
        ('table', 'depth4', 'certified', 'tail3+count', 'fixed_outside'),
        ('table', 'depth4', 'certified', 'full', 'inside_only'),
        ('table', 'depth3', 'certified', 'full', 'inside_only'),
    ]),
    'stepwise_window_state.py': ('window_state.json', [
        ('outside_separates_all_patterns',),
        ('depths', 'm=3', 'nerode_classes'),
        ('depths', 'm=3', 'full_pool_merged_classes'),
        ('depths', 'm=4', 'minimal_predicate_sets', 'size'),
        ('depths', 'm=5', 'nerode_classes'),
    ]),
    'stepwise_strip.py': ('strip.json', [
        ('width1_fan2', 'accepted_words'),
        ('width1_fan3', 'accepted_words'),
        ('width1_fan3', 'by_prefix', 'n=5', 'nerode_classes_alive'),
        ('width1_fan3', 'by_prefix', 'n=5', 'windows', 'window1', 'minimal_frontier_relations_alive'),
        ('width1_fan4', 'by_prefix', 'n=5', 'nerode_classes_alive'),
    ]),
}


def pick(data, path):
    for key in path:
        data = data[key]
    return data


def main():
    failures = 0
    for script, (artifact, keys) in RUNS.items():
        path = OUT / artifact
        before = json.loads(path.read_text()) if path.exists() else None
        subprocess.run([sys.executable, str(ROOT / 'scripts' / script)], check=True,
                       stdout=subprocess.DEVNULL)
        after = json.loads(path.read_text())
        for key in keys:
            new = pick(after, key)
            old = pick(before, key) if before is not None else None
            status = 'ok' if old == new else 'CHANGED'
            failures += status != 'ok'
            print(f"{status:8s} {script}: {'/'.join(key)} = {new!r}" + ('' if old == new else f' (stored {old!r})'))
    print('all stored figures reproduced' if not failures else f'{failures} figures changed')
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
