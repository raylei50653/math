#!/usr/bin/env python3
"""Reproduce the finite-set viable specification against production on every prefix for k<=2.

uv run --with rustworkx==0.17.1 python scripts/c5_viable_check.py --check

All edge subsets are included, including nonplanar graphs. The oracle computes
R1+SYM directly on complete graphs, then projects their prefixes. No graph search
or catalogue generation runs. The Lean model is not extracted into this checker.
"""
import argparse
import hashlib
import json
from pathlib import Path

import c5_cell_reduced as R

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'artifacts/c5_cells/viable_check.json'


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def layout(k):
    # Construct edges by their combinatorial coordinates, not production block metadata.
    chords = [(i, j) for i in range(5) for j in range(i + 1, 5)
              if (j - i) not in (1, 4)]
    edges = chords + [(u, 5 + m) for m in range(k) for u in range(5 + m)]
    actual, blocks = R.block_edge_order(k)
    require(set(chords) == set(actual[:5]), 'chord universe mismatch')
    # Chord ordering is immaterial to R1/SYM, but retain production coordinates for masks.
    edges[:5] = actual[:5]
    require(tuple(edges) == actual, 'production block edges differ from coordinate model')
    starts = [5 + 5 * m + m * (m - 1) // 2 for m in range(k)]
    require(blocks == [(s, s + 5, s + 4 + m) for m, s in enumerate(starts)], 'block offsets differ')
    touch = [{j for j, (u, v) in enumerate(edges) if 5 + m in (u, v)} for m in range(k)]
    attachments = [[edges.index((i, 5 + m)) for i in range(5)] for m in range(k)]
    return edges, starts, touch, attachments


def att_values(selected, attachments):
    return [sum(2 ** i for i, edge in enumerate(row) if edge in selected) for row in attachments]


def finite_viable(selected, cut, starts, touch, attachments):
    values = att_values(selected, attachments)
    for m, start in enumerate(starts):
        if start < cut:
            if len(selected & touch[m]) + len({e for e in touch[m] if e >= cut}) < 4:
                return False
            if m and values[m] > values[m - 1]:
                return False
    return True


def compare_decision(actual, specification, extendible, context):
    require(actual == specification, f'production/specification mismatch: {context}')
    require(actual or not extendible, f'false rejection: {context}')


def check_k(k):
    edges, starts, touch, attachments = layout(k)
    edge_count = len(edges)
    R._setup(k)
    require(R._W['touch'] == [sum(1 << e for e in row) for row in touch], 'touch table mismatch')
    extendible = [set() for _ in range(edge_count + 1)]
    survivors = 0
    for mask in range(1 << edge_count):
        selected = {e for e in range(edge_count) if mask >> e & 1}
        values = att_values(selected, attachments)
        valid = (all(len(selected & row) >= 4 for row in touch)
                 and all(a >= b for a, b in zip(values, values[1:])))
        if valid:
            survivors += 1
            for cut in range(edge_count + 1):
                extendible[cut].add(mask & ((1 << cut) - 1))
    states = rejected = conservative = 0
    first_conservative = None
    for cut in range(edge_count + 1):
        for mask in range(1 << cut):
            selected = {e for e in range(cut) if mask >> e & 1}
            specification = finite_viable(selected, cut, starts, touch, attachments)
            actual = R.viable(mask, cut)
            has_completion = mask in extendible[cut]
            compare_decision(actual, specification, has_completion, (k, cut, mask))
            if actual and not has_completion:
                conservative += 1
                if first_conservative is None:
                    first_conservative = dict(cut=cut, mask=mask)
            if cut == edge_count:
                require(actual == has_completion, 'terminal guard does not equal R1+SYM')
            rejected += int(not actual)
            states += 1
    return dict(k=k, edge_bits=edge_count, full_graphs=1 << edge_count, survivor_graphs=survivors,
                prefix_states=states, rejected_states=rejected, false_rejections=0,
                specification_mismatches=0, passing_without_completion=conservative,
                first_passing_without_completion=first_conservative, terminal_guard_exact=True)


def negative_controls():
    for args, expected in [((False, True, True, 'mutated rejection'), 'production/specification'),
                           ((False, False, True, 'unsound specification'), 'false rejection')]:
        try:
            compare_decision(*args)
        except AssertionError as error:
            require(expected in str(error), 'negative control failed for wrong reason')
        else:
            raise AssertionError('negative control was accepted')
    return dict(production_disagreement_rejected=True, shared_unsound_rejection_rejected=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    paths = ['scripts/c5_cell_reduced.py', 'scripts/c5_viable_check.py',
             'Math/ReducedViable.lean', 'artifacts/c5_cells/cells.json']
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}
    for k in range(13):
        layout(k)
    report = dict(scope='all prefix states k<=2; no planarity assumption; layout-only k<=12',
                  source_sha256=hashes, negative_controls=negative_controls(), cases=[])
    for k in range(3):
        row = check_k(k)
        report['cases'].append(row)
        print(json.dumps(row, sort_keys=True), flush=True)
    require(all(hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == h for p, h in hashes.items()),
            'source changed during audit')
    payload = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.check:
        require(REPORT.read_text() == payload, 'report differs from deterministic replay')
        print('viable report replay: PASS')
    else:
        REPORT.write_text(payload)
        print(f'wrote {REPORT}')


if __name__ == '__main__':
    main()
