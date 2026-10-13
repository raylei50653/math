#!/usr/bin/env python3
"""Corrupted classification certificates must fail the real checker CLI."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def run():
    original = json.loads((HERE / 'classification.json').read_text())
    controls = []
    changed = deepcopy(original)
    changed['transports'][0]['inner_rows'][0:2] = reversed(changed['transports'][0]['inner_rows'][0:2])
    controls.append(('wrong_inner_pattern_map', changed))
    changed = deepcopy(original)
    t = next(t for t in changed['transports'] if t['source'] == 'c16-941')
    t['label_map']['y1_1'], t['label_map']['y1_2'] = t['label_map']['y1_2'], t['label_map']['y1_1']
    controls.append(('private_order_not_reversed', changed))
    changed = deepcopy(original)
    changed['queries'][0]['nonadjacent_pairs'][0]['positive_equal_rows'].pop()
    controls.append(('missing_positive_equality_witness', changed))
    changed = deepcopy(original)
    changed['transports'][0]['stored_vectors_equal'] = True
    controls.append(('unsupported_vector_equivalence', changed))
    changed = deepcopy(original)
    changed['queries'].pop()
    controls.append(('missing_named_residual', changed))
    changed = deepcopy(original)
    changed['stabilizers']['933'][1]['outer_rows'][0] = 9
    controls.append(('corrupted_complete_target_map', changed))
    results = []
    with tempfile.TemporaryDirectory(prefix='c8-struct-classification-controls-') as tmp:
        for name, changed in controls:
            path = Path(tmp) / (name + '.json')
            path.write_text(json.dumps(changed))
            completed = subprocess.run([sys.executable, str(HERE / 'checker.py'),
                                        '--certificate', str(path)], capture_output=True, text=True)
            assert completed.returncode != 0, f'negative control accepted: {name}'
            assert 'AssertionError' in completed.stderr, (name, completed.stderr)
            results.append(dict(name=name, status='rejected', returncode=completed.returncode))
    return dict(status='PASS', negative_controls=results)


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True))
