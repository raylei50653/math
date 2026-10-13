#!/usr/bin/env python3
"""Reject corrupted complete cofacial-equality cores via the actual CLI."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def run():
    original = json.loads((HERE / 'quotient.json').read_text())
    controls = []
    changed = deepcopy(original)
    q = next(q for q in changed['queries'] if q['query_id'] == 'c16-941')
    q['pair_witness']['equality_rows'].pop()
    controls.append(('missing_equal_pair_preimage', changed))
    changed = deepcopy(original)
    changed['queries'].pop()
    controls.append(('missing_named_query', changed))
    changed = deepcopy(original)
    changed['conditions'][0]['partition'][0] = 7
    controls.append(('corrupted_noncrossing_partition', changed))
    changed = deepcopy(original)
    q = next(q for q in changed['queries'] if q['query_id'] == 'c32-941')
    q['final_upper_mask'] |= 1 << q['pair_witness']['equality_rows'][0]
    controls.append(('corrupted_frozen_upper', changed))
    changed = deepcopy(original)
    changed['queries'][0]['status'] = 'proved exclusion'
    controls.append(('unsupported_additional_exclusion', changed))
    results = []
    with tempfile.TemporaryDirectory(prefix='c8-struct-quotient-controls-') as tmp:
        for name, changed in controls:
            path = Path(tmp) / (name + '.json')
            path.write_text(json.dumps(changed))
            result = subprocess.run([sys.executable, str(HERE / 'quotient_checker.py'),
                                     '--certificate', str(path)], capture_output=True, text=True)
            assert result.returncode != 0, f'negative control accepted: {name}'
            assert 'AssertionError' in result.stderr, (name, result.stderr)
            results.append(dict(name=name, status='rejected', returncode=result.returncode))
    return dict(status='PASS', negative_controls=results)


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True))
