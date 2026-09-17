#!/usr/bin/env python3
"""Triangle blocks with canonical forcing branches; not a general core census."""
import argparse
from collections import Counter
from itertools import combinations, product
import json
import hashlib
from pathlib import Path

import networkx as nx
from c5_tree_cores import (Q, QI, options, lifted_edges, disk_check, exact_core)
from c5_cell_enumerator import T4
from c5_disk_deletions import BOUNDARY, CYCLE, faces_of, sha
from local_closure import direct_graph_extend

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_triangle_branches/observations.json'


def templates():
    for kind, roots in [('one', (0,)), ('two_same', (0, 0)),
                        ('two_distinct', (0, 1)), ('three', (0, 1, 2))]:
        for a in range(3):
            for bs in product([b for b in range(3) if b != a], repeat=len(roots)):
                if kind == 'two_same' and bs[0] == bs[1]:
                    continue
                lists = [{3, a} for _ in range(3)]
                inner = [(0, 1), (1, 2), (0, 2)]
                for root, b in zip(roots, bs):
                    j = len(lists)
                    lists[root].add(b)
                    lists.extend([{3, b}, {3}])
                    inner.extend([(root, j), (j, j+1)])
                yield kind, [3, a], roots, bs, lists, inner
    for a, b in combinations(range(3), 2):
        yield ('no_D', [a, b], (0, 1, 2), (3, 3, 3),
               [{a, b, 3} for _ in range(3)] + [{3} for _ in range(3)],
               [(0, 1), (1, 2), (0, 2), (0, 3), (1, 4), (2, 5)])


def build():
    counts, rows, representatives = Counter(), [], []
    digests = {}
    for kind, palette, roots, bs, lists, inner in templates():
        first = True
        for ns in product(*(options(c for c in range(3) if c not in ls) for ls in lists)):
            edges = lifted_edges(inner, ns)
            n = 5 + len(lists)
            graph = nx.Graph(edges)
            graph.add_edges_from((n, b) for b in range(5))
            disk, embedding = nx.check_planarity(graph)
            counts[kind + '_templates'] += 1
            row = dict(kind=kind, palette=palette, branch_colors=bs,
                       neighborhoods=ns, disk=disk)
            if first:
                representatives.append(dict(kind=kind, palette=palette, branch_colors=bs,
                                            **exact_core(n, edges)))
                first = False
            if disk:
                counts[kind + '_disk'] += 1
                row.update(edges=edges, **exact_core(n, edges))
                rotation = [list(embedding.neighbors_cw_order(v)) for v in range(n+1)]
                assert n + 1 - graph.number_of_edges() + len(faces_of(rotation)) == 2
                row['apex_rotation'] = rotation
                if row['sigma'] & T4 == T4:
                    counts[kind + '_T4'] += 1
                    assert row['sigma'] == 1023 ^ (1 << QI)
            digests.setdefault(kind, hashlib.sha256()).update(
                (json.dumps([palette, bs, ns, disk], separators=(',', ':')) + '\n').encode())
            if disk:
                rows.append(row)
    assert counts == dict(one_templates=832, one_disk=16, one_T4=16,
                          two_same_templates=4096, two_distinct_templates=10496,
                          two_distinct_disk=2, two_distinct_T4=2,
                          three_templates=160768, no_D_templates=1088)
    long_rows = []
    for base in [r for r in rows if r['kind'] == 'two_distinct' and r['disk']]:
        for lengths in [(1, 3), (3, 1), (3, 5), (5, 3)]:
            ns = list(base['neighborhoods'][:3])
            inner = [(0, 1), (1, 2), (0, 2)]
            for root, length in enumerate(lengths):
                j = len(ns)
                ns.extend([base['neighborhoods'][3+2*root]]*length)
                ns.append(base['neighborhoods'][4+2*root])
                inner.append((root, j))
                inner.extend((v, v+1) for v in range(j, len(ns)-1))
            edges = lifted_edges(inner, ns)
            n = 5 + len(ns)
            disk, topology = disk_check(n, edges)
            assert disk
            full = format(sum(int(direct_graph_extend(n, edges, b)) << j
                              for j, b in enumerate(BOUNDARY)), '060x')
            assert full == base['full_relation']
            # All non-boundary edges remain individually pivotal for Q.
            for e in sorted(set(edges)-CYCLE):
                assert direct_graph_extend(n, tuple(f for f in edges if f != e), Q)
            long_rows.append(dict(lengths=lengths, edges=edges, full_relation=full,
                                  topology=topology))
    dependencies = ['c5_triangle_branches', 'c5_tree_cores', 'c5_odd_join_cores',
                    'c5_cell_enumerator', 'c5_disk_deletions', 'local_closure', 'boundary_relations']
    return dict(schema=1, fixed_pattern=Q,
                scope='Canonical triangle forcing-branch templates only; no arbitrary-tree relation compression asserted.',
                source_sha256={f'scripts/{name}.py': sha(ROOT / 'scripts' / f'{name}.py')
                               for name in dependencies},
                counts=dict(sorted(counts.items())), disk_templates=rows,
                enumeration_sha256={k: v.hexdigest() for k, v in sorted(digests.items())},
                list_assignment_criticality=representatives, longer_two_tail_lifts=long_rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['counts'], indent=2))


if __name__ == '__main__':
    main()
