"""Targeted rejection controls for the independent multirow checker."""
from pathlib import Path
import copy
import importlib.util
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('independent_checker', HERE / 'check.py')
C = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(C)


def main():
    original = json.loads((HERE / 'CAP_0_COMPACT.json').read_text())
    source = json.loads(C.SOURCE.read_text())
    controls = []

    broken = copy.deepcopy(original)
    dropped = broken['remaining'].pop()
    broken['necessary_controls'] = [x for x in broken['necessary_controls'] if x[0] != dropped]
    controls.append(('missing-relative-palette-state', broken, source))

    broken = copy.deepcopy(original)
    first_choice = broken['choice_catalogue'][broken['necessary_controls'][0][1]]
    pi = first_choice[0]
    mask = broken['partition_catalogue'][pi][0]
    broken['partition_catalogue'][pi][0] = mask & (mask - 1)
    controls.append(('missing-component-contact', broken, source))

    broken = copy.deepcopy(original)
    deleted = broken['remaining'].pop(0)
    broken['necessary_controls'] = [x for x in broken['necessary_controls'] if x[0] != deleted]
    counts = broken['rounds'][0]['before'][:]
    removed_counts = [int(i == deleted // 65536) for i in range(7)]
    final_counts = [a - b for a, b in zip(counts, removed_counts)]
    broken['rounds'] = [dict(before=counts, removed=[deleted], removed_counts=removed_counts),
                        dict(before=final_counts, removed=[], removed_counts=[0] * 7)]
    controls.append(('invented-state-exclusion', broken, source))

    broken_source = copy.deepcopy(source)
    fibre = next(f for f in broken_source['caps'][0]['complete_fibres'] if f['full_lifts'])
    fibre['full_lifts'].pop()
    controls.append(('missing-full-cap-lift', original, broken_source))

    broken_source = copy.deepcopy(source)
    fibres = broken_source['caps'][0]['complete_fibres']
    empty = next(f for f in fibres if not f['full_lifts'])
    fibres.remove(empty)
    controls.append(('missing-empty-cap-fibre', original, broken_source))

    broken = copy.deepcopy(original)
    broken['source_realization'] = True
    controls.append(('invented-source-realization-authority', broken, source))

    broken = copy.deepcopy(original)
    broken['strong'] = False
    controls.append(('weakened-annular-scope', broken, source))

    broken = copy.deepcopy(original)
    broken['base'] = '0' * 40
    controls.append(('wrong-frozen-base', broken, source))

    broken = copy.deepcopy(original)
    broken['source_sha256'] = '0' * 64
    controls.append(('wrong-frozen-source', broken, source))

    results = []
    for name, certificate, candidate_source in controls:
        try:
            C.check(certificate, candidate_source)
        except AssertionError as error:
            results.append(dict(control=name, rejected=True, reason=str(error)))
        else:
            raise AssertionError(('negative control accepted', name))
    optimized = subprocess.run([sys.executable, '-O', str(HERE / 'check.py')], capture_output=True, text=True)
    assert optimized.returncode != 0 and 'requires active assertions' in optimized.stderr
    results.append(dict(control='python-optimized-assertion-bypass', rejected=True,
                        reason='checker refuses Python -O before certificate work'))
    output = dict(schema='941-k8-seven-row-negative-controls-v1', status='PASS', controls=results)
    with (HERE / 'NEGATIVE.json').open('x') as f:
        json.dump(output, f, indent=2, sort_keys=True)
        f.write('\n')
    print(json.dumps(output, sort_keys=True))


if __name__ == '__main__':
    main()
