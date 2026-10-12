#!/usr/bin/env python3
"""Complete labelled degree-five wheel controls; no outside-K source claimed.

Requires NetworkX for an independent apex-planarity check.  --write creates
the certificate exclusively; --check compares all recomputed full fibres.
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import networkx as nx


def need(ok, message):
    if not ok:
        raise ValueError(message)


def edgeset(edges):
    return sorted({tuple(sorted(e)) for e in edges})


CYCLE = edgeset((i, (i + 1) % 5) for i in range(5))
RIM = edgeset((5 + i, 5 + (i + 1) % 5) for i in range(5))
SPOKES = [(5 + i, 10) for i in range(5)]


def canonical(p):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in p)


PATTERNS = sorted({canonical(p) for p in itertools.product(range(4), repeat=5)
                   if all(p[u] != p[v] for u, v in CYCLE)})


def brute(n, edges, p):
    return [p + rest for rest in itertools.product(range(4), repeat=n - 5)
            if all((p + rest)[u] != (p + rest)[v] for u, v in edges)]


def mrv(n, edges, p):
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    if any(p[u] == p[v] for u, v in edges if u < 5 and v < 5):
        return []
    colours = list(p) + [-1] * (n - 5)
    result = []

    def visit():
        options = [(tuple(c for c in range(4)
                          if c not in {colours[w] for w in adjacency[v]}), v)
                   for v in range(5, n) if colours[v] < 0]
        if not options:
            result.append(tuple(colours))
            return
        available, v = min(options, key=lambda item: (len(item[0]), item[1]))
        for c in available:
            colours[v] = c
            visit()
        colours[v] = -1

    visit()
    return sorted(result)


def fibres(n, edges):
    result = []
    for p in PATTERNS:
        row = brute(n, edges, p)
        need(row == mrv(n, edges, p), 'independent full-fibre equality')
        result.append(row)
    return result


def mask(rows):
    return sum(1 << i for i, row in enumerate(rows) if row)


def apex_planar(n, edges):
    graph = nx.Graph()
    graph.add_nodes_from(range(n + 1))
    graph.add_edges_from(edges)
    graph.add_edges_from((n, b) for b in range(5))
    return nx.check_planarity(graph)[0]


def quotient(edges, i):
    u, v = 5 + i, 5 + (i + 2) % 5
    reps = sorted(set(range(10)) - {v})
    reindex = {r: j for j, r in enumerate(reps)}
    mapping = [reindex[u if w == v else w] for w in range(10)]
    need(mapping[:5] == list(range(5)), 'boundary identity')
    qedges = edgeset((mapping[a], mapping[b]) for a, b in edges)
    need(all(a != b for a, b in qedges), 'loop-free quotient')
    return (u, v), mapping, qedges


def analyse(name, attachments):
    gedges = edgeset(CYCLE + RIM + SPOKES + attachments)
    dedges = [e for e in gedges if 10 not in e]
    need(len(gedges) == 25, 'triangulated C5 disk edge count')
    need(apex_planar(11, gedges), 'source apex planar')
    need(apex_planar(10, dedges), 'deleted source apex planar')
    need([e for e in gedges if all(5 <= w < 10 for w in e)] == RIM,
         'induced all-interior rim')
    grows, drows = fibres(11, gedges), fibres(10, dedges)
    for gs, ds in zip(grows, drows):
        need([g[:10] for g in gs] == [d for d in ds if len(set(d[5:10])) == 3],
             'wheel restoration exactly three-colour rim')
    qs = []
    for i in range(5):
        pair, mapping, qedges = quotient(dedges, i)
        need(apex_planar(9, qedges), 'quotient apex planar')
        qrows = fibres(9, qedges)
        pulled = [sorted(tuple(c[mapping[w]] for w in range(10)) for c in row)
                  for row in qrows]
        for row, ds in zip(pulled, drows):
            need(row == [c for c in ds if c[pair[0]] == c[pair[1]]],
                 'exact quotient full-lift equality fibre')
        qs.append({'diagonal_index': i, 'pair': pair, 'n': 9,
                   'edges': qedges, 'original_to_quotient': mapping,
                   'sigma': mask(qrows), 'apex_planar': True,
                   'rows': [{'pattern': p, 'quotient_full_lifts': row,
                             'pulled_back_full_lifts': back,
                             'extendible_lifts': [c for c in back
                                                 if len(set(c[5:10])) == 3],
                             'nonextendible_lifts': [c for c in back
                                                    if len(set(c[5:10])) == 4]}
                            for p, row, back in zip(PATTERNS, qrows, pulled)]})
    union = 0
    for q in qs:
        union |= q['sigma']
    degrees = [sum(v in e for e in gedges) for v in range(11)]
    return {'name': name, 'n': 11, 'edges': gedges, 'degrees': degrees,
            'boundary': list(range(5)), 'centre': 10, 'rim': list(range(5, 10)),
            'apex_planar': True, 'sigma': mask(grows), 'quotient_union': union,
            'new_rows_in_union': union & ~mask(grows),
            'rows': [{'pattern': p, 'source_full_lifts': gs,
                      'deleted_source_full_lifts': ds}
                     for p, gs, ds in zip(PATTERNS, grows, drows)],
            'quotients': qs}


def double_quotients(control):
    dedges = [e for e in control['edges'] if 10 not in e]
    result = []
    union = 0
    for p in PATTERNS:
        if len(set(p)) != 3:
            continue
        equal = [i for i in range(5) if p[i] == p[(i + 2) % 5]]
        representatives = list(range(10))
        for i in equal:
            representatives[5 + (i + 2) % 5] = 5 + i
        surviving = sorted(set(representatives))
        mapping = [surviving.index(r) for r in representatives]
        qedges = edgeset((mapping[u], mapping[v]) for u, v in dedges)
        need(len(surviving) == 8 and all(u != v for u, v in qedges),
             'double quotient has three interiors and no loops')
        rows = fibres(8, qedges)
        pulled = [sorted(tuple(c[mapping[w]] for w in range(10)) for c in row)
                  for row in rows]
        for full, original in zip(pulled, control['rows']):
            expected = [tuple(c) for c in original['deleted_source_full_lifts']
                        if all(c[5 + i] == c[5 + (i + 2) % 5] for i in equal)]
            need(full == expected, 'double quotient exact equality fibres')
            need(all(len(set(c[5:10])) == 3 for c in full),
                 'double quotient forces extendible wheel rim')
        graph = nx.Graph()
        graph.add_nodes_from(range(8))
        graph.add_edges_from(qedges)
        need(not nx.check_planarity(graph)[0], 'ICO double quotient is nonplanar')
        # Fixed K5 subdivision for equality diagonals 0,1, transported by
        # the graph's literal pentagonal rotation.  Verify every path rather
        # than relying solely on the planarity library's negative answer.
        rotation = next(r for r in range(5) if set(equal) == {r, (r + 1) % 5})
        base_paths = [[2, 3], [2, 5], [2, 6], [2, 1, 0, 9],
                      [3, 5], [3, 6], [3, 4, 9],
                      [5, 6], [5, 9], [6, 9]]

        def rotate(w):
            return (w + rotation) % 5 if w < 5 else 5 + (w - 5 + rotation) % 5

        paths = [[mapping[rotate(w)] for w in path] for path in base_paths]
        branches = sorted({path[0] for path in paths} | {path[-1] for path in paths})
        need(len(branches) == 5, 'five K5 subdivision branch vertices')
        need(edgeset((path[0], path[-1]) for path in paths)
             == list(itertools.combinations(branches, 2)), 'all ten K5 branch pairs')
        interiors = [w for path in paths for w in path[1:-1]]
        need(len(interiors) == len(set(interiors)) and not set(interiors) & set(branches),
             'internally vertex-disjoint branch paths')
        need(all(len(path) == len(set(path)) for path in paths), 'simple branch paths')
        need(all(tuple(sorted((u, v))) in qedges for path in paths
                 for u, v in zip(path, path[1:])), 'every subdivision edge is literal')
        union |= mask(rows)
        result.append({'rim_pattern': p, 'equal_diagonals': equal,
                       'n': 8, 'edges': qedges, 'original_to_quotient': mapping,
                       'planar': False, 'sigma': mask(rows),
                       'K5_subdivision': {'branch_vertices': branches, 'paths': paths},
                       'rows': [{'pattern': beta, 'quotient_full_lifts': full,
                                 'pulled_back_full_lifts': back}
                                for beta, full, back in zip(PATTERNS, rows, pulled)]})
    need(union == control['sigma'], 'exact double-quotient union is nonplanar')
    return result


def compute():
    local = []
    for p in PATTERNS:
        equal = [i for i in range(5) if p[i] == p[(i + 2) % 5]]
        ncolours = len(set(p))
        need(len(equal) == 5 - ncolours, 'five-cycle equality diagonal count')
        if ncolours == 3:
            a, b = equal
            chord_a = {a, (a + 2) % 5}
            chord_b = {b, (b + 2) % 5}
            need(not chord_a & chord_b, 'two equal pairs have disjoint ends')
            need(sum(x in {(a + 1) % 5} for x in chord_b) == 1,
                 'equal-pair endpoints alternate cyclically')
        local.append({'pattern': p, 'colours': ncolours,
                      'equal_diagonals': equal, 'extends_to_centre': ncolours == 3})
    ico = analyse('ICO-ANNULUS-K6',
                  [(i, 5 + i) for i in range(5)]
                  + [((i + 1) % 5, 5 + i) for i in range(5)])
    leak = analyse('WHEEL-QUOTIENT-LEAK-K6',
                   [(0, 5), (0, 8), (0, 9), (1, 5), (2, 5),
                    (2, 6), (3, 6), (4, 6), (4, 7), (4, 8)])
    need(ico['sigma'] == 1023, 'icosahedral source relation')
    need(ico['degrees'] == [4] * 5 + [5] * 6, 'icosahedral degrees')
    need([q['sigma'] for q in ico['quotients']] == [231, 977, 636, 442, 783],
         'icosahedral individual quotients')
    need(leak['sigma'] == 887, 'leak source relation')
    need([q['sigma'] for q in leak['quotients']] == [854, 567, 997, 854, 567],
         'leak quotient relations')
    need(leak['quotient_union'] == 1015, 'union is strictly too large')
    need(leak['new_rows_in_union'] == 128, 'only new row is 01213')
    q2 = leak['quotients'][2]
    need(bool(q2['rows'][9]['extendible_lifts']), 'original p-star lift retained')
    need(not leak['rows'][7]['source_full_lifts'], 'new row originally empty')
    need(bool(q2['rows'][7]['nonextendible_lifts']), 'new row has four-colour rim')
    need(not q2['rows'][7]['extendible_lifts'], 'no false wheel restoration')
    return {'schema': 'degree5-local-full-fibres-v1',
            'pattern_order': PATTERNS, 'local_wheel_table': local,
            'controls': [ico, leak],
            'ico_double_quotients': double_quotients(ico),
            'boundaries': [
                'Both controls are inside K; outside-K source status is not triggered.',
                'ICO satisfies the degree bounds but is not a minimal outside-K source.',
                'LEAK is only a local-quotient control, not a degree-bound control.',
                'No universal reduction or K-infinity equality is claimed.']}


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', type=Path)
    group.add_argument('--check', type=Path)
    args = parser.parse_args()
    computed = json.loads(json.dumps(compute()))
    if args.write:
        with args.write.open('x') as stream:
            json.dump(computed, stream, indent=2, sort_keys=True)
            stream.write('\n')
    else:
        need(computed == json.loads(args.check.read_text()), 'certificate exact replay')
    print('PASS: two controls, ten rows, five quotients each, complete lifts; '
          'independent product/MRV and apex-planarity checks')


if __name__ == '__main__':
    main()
