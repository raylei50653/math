#!/usr/bin/env python3
"""Small actual disk graphs validate complete joins, including all empty fibres."""
import argparse
import json
from pathlib import Path
import networkx as nx
from independent_review import patterns

HERE = Path(__file__).resolve().parent


def cycle(vertices):
    return {tuple(sorted((a, b))) for a, b in zip(vertices, vertices[1:] + vertices[:1])}


def all_lifts(n, edges, pins):
    neighbors = [set() for _ in range(n)]
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    colors = [-1] * n
    for v, c in pins.items():
        colors[v] = c
    if any(colors[a] >= 0 and colors[a] == colors[b] for a, b in edges):
        return []
    out = []
    def walk():
        options = {v: set(range(4)) - {colors[u] for u in neighbors[v]}
                   for v in range(n) if colors[v] == -1}
        if not options:
            out.append(colors.copy())
            return
        v = min(options, key=lambda x: (len(options[x]), -len(neighbors[x]), x))
        for c in sorted(options[v]):
            colors[v] = c
            walk()
        colors[v] = -1
    walk()
    return sorted(out)


def build():
    cert = json.loads((HERE / 'certificate.json').read_text())
    cells = json.loads((HERE / 'frozen/cells.json').read_text())['cells']
    supports = cert['original_collar']['inner_supports']
    controls = []
    cases = [('chord', 0, 0, 10, 165), ('chord', 1, 0, 7, 429),
             ('crosscut', 1, 2, 7, None), ('crosscut', 4, 3, 429, None)]
    for kind, s, d, shortmask, longmask in cases:
        ring = list(range(5, 12))
        edges = cycle(list(range(5))) | cycle(ring)
        edges |= {(b, ring[j]) for j, sup in enumerate(supports) for b in sup}
        next_vertex = 12
        if kind == 'chord':
            short = [ring[(s + j) % 7] for j in range(4)]
            long = [ring[(s + j) % 7] for j in range(3, 8)]
        else:
            z = next_vertex
            next_vertex += 1
            short = [ring[(s + j) % 7] for j in range(d + 1)] + [z]
            long = [ring[(s + j) % 7] for j in range(d, 8)] + [z]
        short_edges, long_edges = cycle(short), cycle(long)
        if len(short) == 4:
            if shortmask == 7:
                short_edges |= {tuple(sorted((v, next_vertex))) for v in short}
                next_vertex += 1
            elif shortmask == 10:
                short_edges.add(tuple(sorted((short[1], short[3]))))
            elif shortmask == 12:
                short_edges.add(tuple(sorted((short[0], short[2]))))
        else:
            witness = cells[str(shortmask)]
            mapping = short + list(range(next_vertex, next_vertex + witness['k_eff']))
            next_vertex += witness['k_eff']
            short_edges |= {tuple(sorted((mapping[a], mapping[b]))) for a, b in witness['edges']}
        if kind == 'chord':
            witness = cells[str(longmask)]
            mapping = long + list(range(next_vertex, next_vertex + witness['k_eff']))
            next_vertex += witness['k_eff']
            long_edges |= {tuple(sorted((mapping[a], mapping[b]))) for a, b in witness['edges']}
        elif d == 3:
            long_edges |= {tuple(sorted((v, next_vertex))) for v in long}
            next_vertex += 1
        def side_relation(boundary, side_edges):
            verts = boundary + sorted({v for edge in side_edges for v in edge} - set(boundary))
            side_map = {v: j for j, v in enumerate(verts)}
            ee = [(side_map[a], side_map[b]) for a, b in side_edges]
            fibres = [all_lifts(len(verts), ee, dict(enumerate(p))) for p in patterns(len(boundary))]
            return sum(1 << i for i, lifts in enumerate(fibres) if lifts), fibres
        actualshort, short_lifts = side_relation(short, short_edges)
        actuallong, long_lifts = side_relation(long, long_edges)
        assert actualshort == shortmask
        if longmask is not None:
            assert actuallong == longmask
        edges |= short_edges | long_edges
        edges = sorted({tuple(sorted(e)) for e in edges})
        graph = nx.Graph(edges)
        # The extra outer apex also checks that all original b_i are cofacial.
        graph.add_edges_from((next_vertex, b) for b in range(5))
        assert nx.check_planarity(graph)[0]
        fibres = [all_lifts(next_vertex, edges, dict(enumerate(p))) for p in patterns(5)]
        actual = sum(1 << i for i, lifts in enumerate(fibres) if lifts)
        if kind == 'chord':
            relation = next(r for r in cert['chords'] if r['start'] == s and
                            r['short_mask'] == shortmask and r['long_mask'] == longmask)
            expected = relation['outer_accepted_mask']
        else:
            relation = next(r for r in cert['two_edge_crosscuts'] if r['start'] == s and
                            r['distance'] == d and r['short_mask'] == shortmask)
            expected = 0
            for i, col in enumerate(relation['column_masks']):
                if actuallong >> i & 1:
                    expected |= col
        assert actual == expected
        controls.append(dict(kind=kind, start=s, distance=d, n=next_vertex, edges=edges,
                             short_cycle=short, long_cycle=long, short_mask=actualshort,
                             long_mask=actuallong, short_full_lifts=short_lifts,
                             long_full_lifts=long_lifts, original_outer_full_lifts=fibres,
                             complete_outer_mask=actual, status='triggered and holds'))
    return dict(controls=controls, target_source_status='not triggered')


def main():
    p = argparse.ArgumentParser()
    m = p.add_mutually_exclusive_group(required=True)
    m.add_argument('--write', action='store_true')
    m.add_argument('--check', action='store_true')
    a = p.parse_args()
    data = build()
    fpath = HERE / 'literal_controls.json'
    if a.write:
        with fpath.open('x') as f:
            json.dump(data, f, separators=(',', ':'), sort_keys=True)
            f.write('\n')
    else:
        assert json.loads(fpath.read_text()) == json.loads(json.dumps(data))
    print(json.dumps(dict(status='PASS', controls=[dict(kind=c['kind'], start=c['start'],
                      short_mask=c['short_mask'], long_mask=c['long_mask'],
                      outer_mask=c['complete_outer_mask'],
                      complete_lifts=sum(map(len, c['original_outer_full_lifts'])))
                      for c in data['controls']], target_source_status='not triggered')))


if __name__ == '__main__':
    main()
