#!/usr/bin/env python3
"""Finite boundary-list audit for two rejected rows; no graph search."""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_sector_rejection_lists/observations.json'
UPSTREAM = ROOT / 'artifacts/c5_sector_corner_gates/observations.json'
ROWS = ((0, 1, 2, 1, 2), (0, 1, 2, 1, 3))


def build():
    upstream = json.loads(UPSTREAM.read_text())
    for name, digest in upstream['input_sha256'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    entries = []
    groups = {}
    for k in range(5):
        for neighbors in combinations(range(5), k):
            lists = [sorted(set(range(4)) - {row[i] for i in neighbors}) for row in ROWS]
            tight = all(len(colors) == 4-k for colors in lists)
            assert tight == (not {1, 3} <= set(neighbors) and not {2, 4} <= set(neighbors))
            entries.append(dict(boundary_neighbors=list(neighbors), inner_degree=4-k,
                                lists=lists, both_tight=tight))
            if tight:
                groups.setdefault((k, tuple(map(tuple, lists))), []).append(list(neighbors))
    # The joint list pair recovers attachments modulo exchanging frame 1 and 3.
    def quotient(ns):
        return sorted(1 if v == 3 else v for v in ns)
    for members in groups.values():
        assert len({tuple(quotient(ns)) for ns in members}) == 1
    tight = [e for e in entries if e['both_tight']]
    for a in tight:
        for b in tight:
            assert (a['lists'] == b['lists']) == (quotient(a['boundary_neighbors']) == quotient(b['boundary_neighbors']))
    leaves = [e for e in tight if e['inner_degree'] == 1]
    assert len(leaves) == 4 and all(0 in e['boundary_neighbors'] for e in leaves)
    # In the nonempty branch only b,w touch frame 0; w has inner degree 3.
    # Properness of the already fixed old coloring c(b)=1 leaves one triple.
    old = (0, 1, 0, 2, 1)
    b_cases = [e for e in leaves if all(old[i] != 1 for i in e['boundary_neighbors'])]
    assert [e['boundary_neighbors'] for e in b_cases] == [[0, 2, 3]]
    # Edge b--2 would be an S' path avoiding frame 1. Both orders require
    # two distinct saturated stars on this path, whose only interior point is b.
    required = [case['alternating_barriers']['2'] for case in upstream['cases']]
    assert required == [['P', 'R', 'U'], ['Q', 'U']]
    b_survivors = [e['boundary_neighbors'] for e in tight
                   if 0 in e['boundary_neighbors'] and 2 not in e['boundary_neighbors']
                   and all(old[i] != 1 for i in e['boundary_neighbors'])]
    assert b_survivors == [[0], [0, 3]]
    # Explicit coloring checks the negative control, rather than just recording it.
    negative_lists, negative_colors = ({0}, {1}), (0, 1)
    assert all(c in ls and len(ls) == 1 for c, ls in zip(negative_colors, negative_lists))
    assert negative_colors[0] != negative_colors[1]
    inputs = {UPSTREAM, Path(__file__).resolve()}
    inputs.update(ROOT / name for name in upstream['input_sha256'])
    return dict(schema=1, scope='Local list arithmetic plus inherited corner barriers; no sector realization.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)},
                rejected_rows=ROWS, entries=entries,
                joint_classes=[dict(boundary_count=k, lists=pair, neighborhoods=members)
                               for (k, pair), members in groups.items()],
                possible_leaf_neighborhoods=[e['boundary_neighbors'] for e in leaves],
                old_coloring_leaf_b_candidates=[e['boundary_neighbors'] for e in b_cases],
                inherited_b_to_2_barriers=required, surviving_b_boundary_neighborhoods=b_survivors,
                negative_control=dict(inner_edges=[[0, 1]], lists=[[0], [1]], coloring=[0, 1],
                                      meaning='Tight lists alone do not imply rejection.'),
                summary=dict(boundary_subsets=len(entries), tight_subsets=len(tight),
                             joint_list_classes=len(groups), leaf_neighborhoods=len(leaves),
                             old_coloring_leaf_b_candidates=len(b_cases),
                             inherited_profiles=603, profile_deletions=0,
                             fixed_point_recomputed=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
