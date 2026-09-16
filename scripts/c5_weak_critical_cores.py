#!/usr/bin/env python3
"""Extract critical supports of five sealed adjacent-pair representatives.

No new parents or k=4 search; enumerate only subsets of these representatives.
uv run --with networkx==3.5 python scripts/c5_weak_critical_cores.py [--check]
"""
import argparse
from itertools import product
import json
from pathlib import Path

from c5_cell_enumerator import REPS, compat_tables
from c5_disk_deletions import CYCLE, relation, sha
from c5_disk_weak_successors import certify_parent, members

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_weak_critical_cores/observations.json'


def build():
    paths = [ROOT / f'artifacts/{name}/observations.json' for name in
             ('c5_weak_candidates', 'c5_weak_deletion_audit', 'c5_disk_deletions')]
    candidates, audit, source = [json.loads(p.read_text()) for p in paths]
    for data in (candidates, audit):
        for name, expected in (data['inputs'] | data['source_sha256']).items():
            assert sha(ROOT / name) == expected, name
    parents = {p['id']: p for p in source['parents']}
    runs = []
    for row in candidates['candidates']['adjacent_singleton_pair']:
        variant, = audit['sigma_variants'][str(row['sigma'])]
        parent_id, parent_mask = variant['representative']
        parent = parents[parent_id]
        parent_edges = sorted(set(map(tuple, parent['edges'])) - CYCLE)
        edges = [parent_edges[i] for i in members(parent_mask)]
        n = 5 + parent['k']
        size = 1 << len(edges)
        root = size - 1
        tables, full = compat_tables(parent['k'], edges)
        sigma = [0] * size
        for j, boundary in enumerate(REPS):
            viable = [full] * size
            for m in range(1, size):
                bit = m & -m
                viable[m] = viable[m ^ bit] & tables[bit.bit_length()-1][j]
            # Independent complete-assignment enumeration followed by subset OR.
            exists = bytearray(size)
            for inner in product(range(4), repeat=parent['k']):
                colors = boundary + inner
                good = sum(1 << i for i, (u, v) in enumerate(edges)
                           if colors[u] != colors[v])
                exists[good] = 1
            for i in range(len(edges)):
                for m in range(size):
                    if not m >> i & 1:
                        exists[m] |= exists[m | (1 << i)]
            for m in range(size):
                assert bool(viable[m]) == bool(exists[m])
                sigma[m] |= int(exists[m]) << j
        assert sigma[root] == row['sigma']
        missing = [j for j in range(10) if not sigma[root] >> j & 1]
        cores = {}
        for j in missing:
            cores[j] = [m for m in range(size) if not sigma[m] >> j & 1
                        and all(sigma[m ^ (1 << i)] >> j & 1 for i in members(m))]
        # Verify the entire support formula, not only root edge sensitivity.
        for m in range(size):
            predicted = 1023
            for j in missing:
                if any(m & c == c for c in cores[j]):
                    predicted ^= 1 << j
            assert predicted == sigma[m]
        assert all(len(cs) == 1 for cs in cores.values())
        a, b = [cores[j][0] for j in missing]
        assert a & b and a & ~b and b & ~a
        assert a | b == root
        weak = set()
        for m in range(size):
            if sigma[m] == sigma[root]:
                for i in members(m):
                    if sigma[m ^ (1 << i)] != sigma[root]:
                        weak.add(sigma[m ^ (1 << i)])
        assert sorted(weak) == row['actual'] == variant['weak_exits']
        witnesses = []
        for label, mask in [('first_only', a & ~b), ('second_only', b & ~a),
                            ('both', a & b)]:
            i = next(members(mask))
            child = root ^ (1 << i)
            child_edges = sorted(CYCLE | {edges[t] for t in members(child)})
            # Backtracking on all 240 labeled boundary rows, plus representative
            # enumeration, independently checks each concrete strict exit.
            assert relation(n, tuple(child_edges))[0] == sigma[child]
            witnesses.append(dict(release=label, silent_deleted=[], strict_deleted=edges[i],
                                  target=sigma[child], after_edges=child_edges))
        runs.append(dict(sigma=sigma[root], boundary_singletons=row['boundary_singletons'],
                         parent=parent_id, parent_mask=parent_mask, vertices=n,
                         geometry=certify_parent(parent, source['inputs']),
                         edges=edges, subsets_checked=size, sigma_by_mask=sigma,
                         cores=[dict(pattern=j, boundary_pattern=REPS[j],
                                     singleton=next(i for i, c in enumerate(REPS[j])
                                                    if REPS[j].count(c) == 1),
                                     mask=cores[j][0],
                                     edges=[edges[i] for i in members(cores[j][0])])
                                for j in missing],
                         shared_edges=[edges[i] for i in members(a & b)],
                         private_edges=[[edges[i] for i in members(c)]
                                        for c in (a & ~b, b & ~a)],
                         silent_states=sum(s == sigma[root] for s in sigma),
                         weak_exits=sorted(weak), witnesses=witnesses))
    # Abstract monotone support systems: controls, not disk realizations.
    controls = []
    for name, aa, bb, expected in [
            ('disjoint', [1], [2], [1, 2]),
            ('identical', [1], [1], [3]),
            ('nested', [1], [3], [2, 3])]:
        states = []
        for m in range(4):
            states.append(int(not any(m & c == c for c in aa)) |
                          (int(not any(m & c == c for c in bb)) << 1))
        exits = sorted({states[m ^ (1 << i)] for m in range(4) if states[m] == 0
                        for i in members(m) if states[m ^ (1 << i)]})
        assert exits == expected
        controls.append(dict(name=name, first_cores=aa, second_cores=bb,
                             release_masks=exits, graph_realization_claimed=False))
    dependencies = [Path(__file__).resolve()] + [ROOT / 'scripts' / f'{name}.py'
                    for name in ('c5_cell_enumerator', 'c5_disk_deletions',
                                 'c5_disk_weak_successors', 'local_closure', 'boundary_relations')]
    return dict(schema=1, scope='Five existing representatives only; no general planar theorem.',
                inputs={str(p.relative_to(ROOT)): sha(p) for p in paths},
                source_sha256={str(p.relative_to(ROOT)): sha(p) for p in dependencies},
                pattern_order=REPS, runs=runs, abstract_controls=controls,
                summary=dict(representatives=len(runs), subsets=sum(r['subsets_checked'] for r in runs),
                             unique_core_pairs=len(runs), direct_exit_witnesses=3*len(runs),
                             shared_edge_counts=[len(r['shared_edges']) for r in runs],
                             private_edge_counts=[[len(e) for e in r['private_edges']] for r in runs]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'artifact differs; rebuild explicitly'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
