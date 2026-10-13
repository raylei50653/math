#!/usr/bin/env python3
"""Focused evidence corruptions; no import of either colouring checker.

Each stream has only the header and first graph. Both checkers must reject the
modified first graph, before requesting a second graph. A failure caused only
by truncation is explicitly not accepted as a successful negative control.
"""
import copy
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / 'negative'


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, separators=(',', ':')) + '\n').encode()


def main():
    OUT.mkdir(exist_ok=True)
    with gzip.open(ROOT / 'controls/certificate.jsonl.gz', 'rt') as stream:
        header, first = json.loads(next(stream)), json.loads(next(stream))
    assert first['Sigma'] == 1023
    mutations = []

    missing = copy.deepcopy(first)
    removed = None
    for row_index, row in enumerate(missing['rows']):
        for cell_index, cell in enumerate(row['cells']):
            if len(cell) == 1 and len(set(cell[0][5:10])) == 3:
                lift = cell.pop()
                centre = next(c for c in '0123' if c not in lift[5:10])
                row['wheel_full_lifts'].remove(lift + centre)
                removed = {'beta': row['beta'], 'tau': header['tau_order'][cell_index],
                           'A_lift': lift, 'G_lift': lift + centre,
                           'row_index': row_index, 'cell_index': cell_index}
                break
        if removed:
            break
    assert removed is not None
    mutations.append(('missing_necessary_lift', missing, removed, "'rows'"))

    edge_changed = copy.deepcopy(first)
    old_edge = next(e for e in edge_changed['edges'] if e[0] < 10 <= e[1])
    old_edge = old_edge[:]
    new_edge = next([a, b] for a in range(10) for b in first['private']
                    if [a, b] not in edge_changed['edges'])
    edge_changed['edges'].remove(old_edge)
    edge_changed['edges'].append(new_edge)
    edge_changed['edges'].sort()
    mutations.append(('changed_original_edge', edge_changed,
                      {'removed_edge': old_edge, 'added_edge': new_edge}, "'edges'"))

    reversed_face = copy.deepcopy(first)
    u_face_index = next(i for i, f in enumerate(reversed_face['faces'])
                        if f == list(range(5, 10)))
    reversed_face['faces'][u_face_index].reverse()
    mutations.append(('reversed_U_face', reversed_face,
                      {'face_index': u_face_index,
                       'before': first['faces'][u_face_index],
                       'after': reversed_face['faces'][u_face_index]},
                      'cyclic(list(range(5, 10)))'))

    results = []
    for name, graph, change, independent_rejection in mutations:
        path = OUT / (name + '.jsonl.gz')
        data = encoded(header) + encoded(graph)
        path.write_bytes(gzip.compress(data, mtime=0))
        for checker, command in (
                ('primary', [sys.executable, '-B', str(ROOT / 'controls/check.py'),
                             '--check', '--certificate', str(path)]),
                ('independent', [sys.executable, '-B', str(HERE / 'check.py'),
                                 '--certificate', str(path)])):
            completed = subprocess.run(command, text=True, capture_output=True)
            transcript = completed.stdout + completed.stderr
            (OUT / (name + '.' + checker + '.log')).write_text(transcript)
            assert completed.returncode != 0, (name, checker, 'corruption accepted')
            if checker == 'primary':
                assert 'certificate mismatch: ' + first['key'] in transcript
            else:
                assert independent_rejection in transcript
            results.append({'mutation': name, 'checker': checker,
                            'status': 'triggered and holds: first graph rejected',
                            'exit_code': completed.returncode,
                            'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                            'change': change,
                            'log': str(path.with_name(name + '.' + checker + '.log').relative_to(ROOT))})
    report = {'status': 'PASS all six first-graph rejections',
              'source_key': first['key'], 'results': results,
              'scope': 'evidence integrity controls; not minimal-source counterexamples'}
    (OUT / 'summary.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
