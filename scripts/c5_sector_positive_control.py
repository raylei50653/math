#!/usr/bin/env python3
"""Find 3903 only in the 648 saved tree templates; generate no new graph family."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx

from boundary_relations import normalize
from c5_k4_blocks import CYCLE, Q, coloring
from c5_odd_join_cores import kuratowski_certificate
from c5_sector_targets import FULL, QUERIES, REPS, eligible, signature, transfer

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'artifacts/c5_degree5_tree_components/observations.json'
OUT = ROOT/'artifacts/c5_sector_positive_control/observations.json'


def edge_list(g):
    return sorted(sorted(e) for e in g.edges())


def sector(edges):
    original = nx.Graph(edges)
    assert set(original[0]) == {1, 4, 5}
    assert set(original[5]) & set(range(5)) == {0, 1, 4}
    # Only the exterior b0 is removed. No edge touching C is discarded.
    graph = original.copy()
    graph.remove_node(0)
    graph = nx.relabel_nodes(graph, {5: 0})
    assert eligible(graph)
    return graph


def tree_accept(graph, row):
    """Independent exact list messages on C, ignoring only boundary-frame edges."""
    inner = set(graph)-set(range(5))
    core = graph.subgraph(inner)
    assert nx.is_tree(core)
    def visit(v, parent):
        allowed = set(range(4)) - {row[b] for b in graph[v] if b < 5}
        for w in sorted(core[v]):
            if w != parent:
                child = visit(w, v)
                allowed = {c for c in allowed if child-{c}}
        return allowed
    return bool(visit(min(inner), None))


def brute(graph, fixed):
    """Product enumeration, also used on the reconstructed original G."""
    remaining = sorted(set(graph)-set(fixed))
    for cs in product(range(4), repeat=len(remaining)):
        colors = fixed | dict(zip(remaining, cs))
        if all(colors[u] != colors[v] for u, v in graph.edges()):
            return colors
    return None


def checked_coloring(graph, fixed):
    a, b = coloring(graph, fixed), brute(graph, fixed)
    assert (a is None) == (b is None)
    if a is not None:
        assert set(a) == set(graph) and all(a[v] == c for v, c in fixed.items())
        assert all(a[u] != a[v] for u, v in graph.edges())
    return None if a is None else [[v, a[v]] for v in sorted(a)]


def validate_subdivision(graph, witness):
    branch = set(witness['branch_vertices'])
    used, links, interiors = set(), set(), set()
    for path in witness['paths']:
        assert len(path) >= 2 and len(path) == len(set(path))
        assert path[0] in branch and path[-1] in branch
        assert not set(path[1:-1]) & (branch | interiors)
        interiors.update(path[1:-1])
        link = frozenset((path[0], path[-1]))
        assert link not in links
        links.add(link)
        for u, v in zip(path, path[1:]):
            e = frozenset((u, v))
            assert graph.has_edge(u, v) and e not in used
            used.add(e)
    if witness['model'] == 'K5':
        assert len(branch) == 5 and links == {frozenset(e) for e in combinations(branch, 2)}
    else:
        assert witness['model'] == 'K3,3' and len(branch) == 6
        assert any(links == {frozenset((u, v)) for u in side for v in branch-set(side)}
                   for side in combinations(branch, 3))


def detailed(record):
    g = sector(record['edges'])
    opened = g.copy()
    opened.remove_edges_from([(0, 1), (0, 4)])
    rows = [dict(row=b, coloring=checked_coloring(opened, dict(enumerate(b)))) for b in QUERIES]
    assert sum((r['coloring'] is not None) << i for i, r in enumerate(rows)) == 3903
    sector_full, original_full = [], []
    original = nx.Graph(record['edges'])
    for b in FULL:
        k = checked_coloring(g, dict(enumerate(b)))
        original_w = checked_coloring(original, dict(enumerate(b)))
        assert (k is not None) == bool(831 >> REPS.index(normalize(b)) & 1)
        assert (original_w is not None) == bool(958 >> REPS.index(normalize(b)) & 1)
        sector_full.append(dict(row=b, coloring=k))
        original_full.append(dict(row=b, coloring=original_w))
    deletions = []
    for e in edge_list(original):
        if tuple(e) in CYCLE:
            continue
        child = original.copy()
        child.remove_edge(*e)
        w = checked_coloring(child, dict(enumerate(Q)))
        assert w is not None
        deletions.append(dict(edge=e, coloring=w))
    return dict(source_edges=record['edges'], sector_edges=edge_list(g),
                internal_vertices=sorted(set(g)-set(range(5))),
                queries=rows, sector_full=sector_full, original_full=original_full,
                original_q_deletions=deletions)


def build(saved):
    source = json.loads(SOURCE.read_text())
    assert len(source['templates']) == 648
    certificates = {} if saved is None else {r['source_index']: r['nonplanar_subdivision']
                                             for r in saved['proper_hits']}
    records, hits, counts = [], [], Counter()
    for i, row in enumerate(source['templates']):
        graph = sector(row['edges'])
        mask = signature(graph)
        independent = sum(tree_accept(graph, b) << j for j, b in enumerate(QUERIES))
        assert mask == independent
        counts[mask] += 1
        r = dict(source_index=i, proper_mask=mask & 1023,
                 E_B=bool(mask & 1024), E_C=bool(mask & 2048), signature=mask,
                 outer_sigma=transfer(mask), topology='not tested in this audit')
        if mask & 1023 == 831:
            witness = certificates[i] if saved is not None else kuratowski_certificate(graph)
            validate_subdivision(graph, witness)
            r['topology'] = 'nonplanar (hence not disk)'
            hits.append(dict(**r, sector_edges=edge_list(graph), nonplanar_subdivision=witness))
        records.append(r)
    assert len(hits) == 22 and all(r['signature'] == 3903 for r in hits)
    assert hits[0]['source_index'] == 41
    selected = detailed(source['templates'][41])
    names = ('c5_sector_positive_control', 'c5_sector_targets', 'c5_k4_blocks',
             'c5_odd_join_cores', 'boundary_relations', 'c5_cell_enumerator')
    inputs = [SOURCE] + [ROOT/'scripts'/f'{name}.py' for name in names]
    return dict(schema=1, scope='Only 648 already-saved tree templates. No new graph enumeration; no general disk exclusion.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
                query_order=QUERIES, gate_records=records, proper_hits=hits,
                selected_source_index=41, selected=selected,
                summary=dict(saved_templates=648, proper_831_hits=22, full_3903_hits=22,
                             nonplanar_hits=22, planar_non_disk_hits=0,
                             query_cross_checks=648*12, selected_sector_full_rows=240,
                             selected_original_full_rows=240,
                             selected_q_deletions=len(selected['original_q_deletions']),
                             signature_counts=dict(sorted(counts.items()))))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    saved = json.loads(OUT.read_text()) if args.check else None
    if args.check:
        def forbidden(*args, **kwargs):
            raise AssertionError('planarity oracle disabled in replay')
        nx.check_planarity = nx.is_planar = forbidden
    result = build(saved)
    data = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
