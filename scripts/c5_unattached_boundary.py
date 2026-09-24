#!/usr/bin/env python3
"""Replay boundary recoloring and its two-spoke separation application.

No graph enumeration: arbitrary-size claims follow from the paper recoloring
bijection. Abstract signatures are necessary conditions, not realizability.
"""
import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_degree5_two_spoke_sectors/observations.json'
OUT = ROOT / 'artifacts/c5_unattached_boundary/observations.json'
U = set(range(4))
ROWS = tuple(b for b in product(range(4), repeat=5)
             if all(b[i] != b[(i+1) % 5] for i in range(5)))


def normalize(row):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in row)


REPS = tuple(sorted({normalize(b) for b in ROWS}))
ROW_INDEX = {b: REPS.index(normalize(b)) for b in ROWS}
T4 = sum(1 << i for i, b in enumerate(REPS) if len(set(b)) == 4)


def singleton(b):
    assert len(set(b)) == 3
    v, = [i for i, c in enumerate(b) if b.count(c) == 1]
    return v


def run():
    recolorings = []
    for b in ROWS:
        if len(set(b)) != 3:
            continue
        d, = U - set(b)
        for v in range(5):
            if v == singleton(b):
                continue
            changed = b[:v] + (d,) + b[v+1:]
            assert changed in ROWS and len(set(changed)) == 4
            assert all(b[i] == changed[i] for i in range(5) if i != v)
            recolorings.append(dict(row=b, vertex=v, T4_row=changed))
    assert len(recolorings) == 480

    # Independent check: extension factors through deletion of the v coordinate.
    # Hence each same-restriction fiber has constant acceptance. Enumerate all
    # 1024 S4-invariant signatures, not just the ones predicted by recoloring.
    signature_controls = []
    for v in range(5):
        fibers = defaultdict(set)
        for b in ROWS:
            fibers[b[:v] + b[v+1:]].add(ROW_INDEX[b])
        allowed = []
        for mask in range(1 << len(REPS)):
            if mask & T4 != T4:
                continue
            if all(len({(mask >> i) & 1 for i in f}) == 1 for f in fibers.values()):
                allowed.append(mask)
        q_index, = [i for i, b in enumerate(REPS)
                    if len(set(b)) == 3 and singleton(b) == v]
        assert allowed == [1023 ^ (1 << q_index), 1023]
        signature_controls.append(dict(vertex=v, singleton_pattern=REPS[q_index],
                                       allowed_masks=allowed, fibers=len(fibers)))

    source = json.loads(SOURCE.read_text())
    applications = []
    for index, record in enumerate(source['records']):
        if record['result'] != 'retained':
            continue
        touched_superset = set(record['spokes']).union(*map(set, record['arcs']))
        untouched = sorted(set(range(5)) - touched_superset)
        entry = dict(source_record=index, ports=record['ports'], spokes=record['spokes'],
                     guaranteed_unattached=untouched)
        if untouched:
            assert untouched == [4]
            entry['result'] = 'single_missing_q'
            entry['adjacent_recolorings'] = [r for r in recolorings
                if r['vertex'] == 4 and r['row'] in ((0, 1, 0, 2, 1), (0, 1, 2, 1, 2))]
            assert len(entry['adjacent_recolorings']) == 2
        else:
            entry['result'] = 'unresolved'
        applications.append(entry)
    assert len(applications) == 24
    solved = [r for r in applications if r['result'] == 'single_missing_q']
    assert len(solved) == 1 and solved[0]['ports'] == [3] and solved[0]['spokes'] == [0, 3]
    unresolved = [r for r in applications if r['result'] == 'unresolved']
    assert sum(r['ports'] == [3] for r in unresolved) == 5
    assert sum(r['ports'] == [2, 1] for r in unresolved) == 18
    return dict(scope='unattached boundary separation; no realizability claim',
                source_sha256=sha256(SOURCE.read_bytes()).hexdigest(), patterns=REPS,
                recolorings=recolorings, signature_controls=signature_controls,
                sector_applications=applications,
                summary=dict(labeled_recolorings=480, signature_checks=5120,
                             separated_configurations=1, unresolved_configurations=23))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
