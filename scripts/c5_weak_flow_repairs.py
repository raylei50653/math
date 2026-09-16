#!/usr/bin/env python3
"""Repair-set form of the adjacent-pair weak-exit problem and one control.

uv run --with networkx==3.5 python scripts/c5_weak_flow_repairs.py [--check]
No parent generation, k=4 disk search, or deletion-audit replay.
"""
import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import networkx as nx

from c5_cell_enumerator import REPS, compat_tables
from c5_disk_deletions import CYCLE, relation, sha
from c5_disk_weak_successors import members

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'artifacts/c5_weak_critical_cores/observations.json'
OUT = ROOT / 'artifacts/c5_weak_flow_repairs/observations.json'


def digest(value):
    return sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def minimal_repairs(sigma, root, pattern):
    """Inclusion-minimal deleted-edge masks enabling one boundary pattern."""
    candidates = sorted((root ^ kept for kept, s in enumerate(sigma) if s >> pattern & 1),
                        key=lambda m: (m.bit_count(), m))
    result = []
    for deleted in candidates:
        if not any(repair & deleted == repair for repair in result):
            result.append(deleted)
    return result


def exit_criteria(families):
    p, q = families
    p_only = [(r, None) for r in p if not any(s & r == s for s in q)]
    q_only = [(None, s) for s in q if not any(r & s == r for r in p)]
    both = []
    for r in p:
        for s in q:
            for e in members(r & s):
                silent = (r | s) ^ (1 << e)
                if not any(t & silent == t for family in families for t in family):
                    both.append((r, s, e, silent))
    return p_only, q_only, both


def repair_row(edges, sigma, source):
    root = len(sigma) - 1
    missing = [j for j in range(10) if not sigma[root] >> j & 1]
    assert len(missing) == 2
    families = [minimal_repairs(sigma, root, j) for j in missing]
    p_only, q_only, both = exit_criteria(families)
    weak = set()
    for kept, s in enumerate(sigma):
        if s == sigma[root]:
            for i in members(kept):
                target = sigma[kept ^ (1 << i)]
                if target != s:
                    weak.add(target)
    predicted = []
    for kind, witnesses in [('first_only', p_only), ('second_only', q_only), ('both', both)]:
        if witnesses:
            predicted.append(kind)
    return dict(source=source, sigma=sigma[root], missing_patterns=missing,
                edges=edges, repair_families=[
                    dict(pattern=j, masks=rs,
                         deleted_edges=[[[*edges[i]] for i in members(r)] for r in rs])
                    for j, rs in zip(missing, families)],
                criteria=dict(first_only=len(p_only), second_only=len(q_only), both=len(both),
                              predicted_types=predicted),
                weak_exits=sorted(weak), table_sha256=digest(sigma))


def disk_representatives(source):
    rows = []
    for run in source['runs']:
        row = repair_row([tuple(e) for e in run['edges']], run['sigma_by_mask'],
                         dict(kind='sealed_disk_representative', parent=run['parent'],
                              parent_mask=run['parent_mask']))
        assert row['sigma'] == run['sigma']
        assert row['weak_exits'] == run['weak_exits']
        families = [r['masks'] for r in row['repair_families']]
        assert all(all(m.bit_count() == 1 for m in family) for family in families)
        assert len(families[0]) == len(families[1]) == 9
        assert len(set(families[0]) & set(families[1])) == 8
        assert len(set(families[0]) - set(families[1])) == 1
        assert len(set(families[1]) - set(families[0])) == 1
        assert row['criteria']['predicted_types'] == ['first_only', 'second_only', 'both']
        rows.append(row)
    return rows


def control_table(extra):
    k = 4
    size = 1 << len(extra)
    tables, full = compat_tables(k, extra)
    sigma = [0] * size
    for j, boundary in enumerate(REPS):
        viable = [full] * size
        for mask in range(1, size):
            bit = mask & -mask
            viable[mask] = viable[mask ^ bit] & tables[bit.bit_length()-1][j]
        # Independent complete assignments, then downward subset OR.
        exists = bytearray(size)
        for inner in product(range(4), repeat=k):
            colors = boundary + inner
            satisfied = sum(1 << i for i, (u, v) in enumerate(extra)
                            if colors[u] != colors[v])
            exists[satisfied] = 1
        for i in range(len(extra)):
            bit = 1 << i
            for mask in range(size):
                if not mask & bit:
                    exists[mask] |= exists[mask | bit]
        for mask in range(size):
            assert bool(viable[mask]) == bool(exists[mask])
            sigma[mask] |= int(exists[mask]) << j
    return sigma


def noncofacial_control():
    # Two edge-disjoint K5 precoloring obstructions on opposite sides of C5.
    first = {(0, 5), (0, 6), (1, 5), (2, 5), (3, 6), (4, 6), (5, 6)}
    second = {(0, 7), (1, 7), (1, 8), (2, 8), (3, 8), (4, 7), (7, 8)}
    extra = sorted(first | second)
    sigma = control_table(extra)
    row = repair_row(extra, sigma, dict(kind='planar_noncofacial_control'))
    root = len(sigma) - 1
    assert row['sigma'] == 943
    assert row['weak_exits'] == [959, 1007]
    assert sum(s == row['sigma'] for s in sigma) == 1
    families = [set(r['masks']) for r in row['repair_families']]
    assert all(m.bit_count() == 1 for family in families for m in family)
    assert len(families[0]) == len(families[1]) == 7 and families[0].isdisjoint(families[1])
    assert row['criteria']['predicted_types'] == ['first_only', 'second_only']
    graph = nx.Graph()
    graph.add_nodes_from(range(9))
    graph.add_edges_from(CYCLE | first | second)
    planar, _ = nx.check_planarity(graph)
    assert planar
    apex = 9
    augmented = graph.copy()
    augmented.add_node(apex)
    augmented.add_edges_from((apex, i) for i in range(5))
    apex_planar, _ = nx.check_planarity(augmented)
    assert not apex_planar
    # Explicit K3,3 subdivision in the augmented graph.  The only internal
    # vertices of its nine paths are 5 and 7, and they occur once each.
    left, right = [2, 3, 4], [6, 8, 9]
    paths = [[2, 5, 6], [2, 8], [2, 9],
             [3, 6], [3, 8], [3, 9],
             [4, 6], [4, 7, 8], [4, 9]]
    assert {(p[0], p[-1]) for p in paths} == set(product(left, right))
    assert all(all(augmented.has_edge(u, v) for u, v in zip(p, p[1:])) for p in paths)
    internal = [v for p in paths for v in p[1:-1]]
    assert len(internal) == len(set(internal)) and not set(internal) & set(left + right)
    for kept in [root] + [root ^ (1 << i) for i in range(len(extra))]:
        graph_edges = tuple(sorted(CYCLE | {extra[i] for i in members(kept)}))
        assert relation(9, graph_edges)[0] == sigma[kept]
    row.update(first_gadget_edges=sorted(first), second_gadget_edges=sorted(second),
               states_checked=len(sigma), silent_states=sum(s == row['sigma'] for s in sigma),
               planar=planar, boundary_apex_planar=apex_planar,
               k33_subdivision=dict(left=left, right=right, paths=paths))
    return row


def build():
    source = json.loads(INPUT.read_text())
    for name, expected in (source['inputs'] | source['source_sha256']).items():
        assert sha(ROOT / name) == expected, name
    disk = disk_representatives(source)
    control = noncofacial_control()
    dependencies = [Path(__file__).resolve()] + [ROOT / 'scripts' / f'{name}.py' for name in
                    ('c5_cell_enumerator', 'c5_disk_deletions', 'c5_disk_weak_successors',
                     'local_closure', 'boundary_relations')]
    return dict(schema=1,
                scope='Repair families for five sealed disk representatives and one explicit noncofacial control; no general theorem.',
                semantics=dict(repair='inclusion-minimal set of nonboundary edges whose deletion enables one missing pattern',
                               first_only='one repair contains no repair for the other pattern',
                               both='two repairs share a last edge and their union minus it contains no repair'),
                inputs={str(INPUT.relative_to(ROOT)): sha(INPUT)},
                source_sha256={str(p.relative_to(ROOT)): sha(p) for p in dependencies},
                pattern_order=REPS, disk_representatives=disk, noncofacial_control=control,
                summary=dict(disk_representatives=len(disk), disk_repairs_per_pattern=[9, 9],
                             disk_common_single_edge_repairs=8, disk_exclusive_single_edge_repairs=[1, 1],
                             control_states=control['states_checked'], control_relation=control['sigma'],
                             control_weak_exits=control['weak_exits'], control_planar=control['planar'],
                             control_boundary_apex_planar=control['boundary_apex_planar']))


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
