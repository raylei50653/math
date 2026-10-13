#!/usr/bin/env python3
"""Independent replay of the proved small-cap core; no unbounded graph search."""
import argparse
import copy
import itertools
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
INTERFACE = HERE.parent / 'frozen/audits/2026-10-13-c8-joint-count-3097ef5/interface.json'
QUERIES = [('c15', 933), ('c18', 933)] + [(f'c{i:02d}', 941) for i in (4, 7, 15, 16, 18, 20, 30, 32)]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def edge(a, b):
    return tuple(sorted((a, b)))


def polygon_triangulations(n):
    diagonals = [(a, b) for a in range(n) for b in range(a + 1, n)
                 if b != a + 1 and (a, b) != (0, n - 1)]
    result = []
    for ds in itertools.combinations(diagonals, n - 3):
        if any(a < c < b < d or c < a < d < b for (a, b), (c, d) in itertools.combinations(ds, 2)):
            continue
        result.append([list(d) for d in ds])
    return result


def check_disk(control):
    """Verify an explicit oriented triangular cellulation of a disk."""
    outer = control['outer']
    faces = control['faces']
    require(len(set(outer)) == len(outer), 'outer not simple')
    require(all(len(f) == 3 and len(set(f)) == 3 for f in faces), 'not triangular')
    directed = Counter()
    vertices = set(outer)
    for face in faces + [list(reversed(outer))]:
        vertices.update(face)
        for a, b in zip(face, face[1:] + face[:1]):
            directed[(a, b)] += 1
    require(all(m == 1 and directed[(b, a)] == 1 for (a, b), m in directed.items()), 'edge orientation')
    edges = {edge(a, b) for a, b in directed}
    require(len(vertices) - len(edges) + len(faces) + 1 == 2, 'Euler characteristic')
    # Oriented edge pairing plus one cyclic link at each vertex rules out singular surfaces.
    for v in vertices:
        successor = {}
        for f in faces + [list(reversed(outer))]:
            if v in f:
                k = f.index(v)
                prev, nxt = f[k - 1], f[(k + 1) % len(f)]
                require(prev not in successor, 'duplicate link predecessor')
                successor[prev] = nxt
        seen, u = set(), next(iter(successor))
        while u not in seen:
            seen.add(u)
            u = successor[u]
        require(len(seen) == len(successor), 'vertex link not one cycle')
    degrees = Counter(v for e in edges for v in e)
    interior = vertices - set(outer)
    triangular_cycles = {frozenset(t) for t in itertools.combinations(vertices, 3)
                         if all(edge(a, b) in edges for a, b in itertools.combinations(t, 2))}
    triangular_faces = {frozenset(f) for f in faces}
    return {'vertices': len(vertices), 'edges': len(edges), 'inner_faces': len(faces),
            'strict_interior': len(interior),
            'interior_degrees': sorted(degrees[v] for v in interior),
            'boundary_degrees': [degrees[v] for v in outer],
            'all_triangles_facial': triangular_cycles == triangular_faces}


def replay(c):
    require(c['schema'] == 'c8-struct.geometry.v1', 'schema')
    require(c['scope'] == 'proved subdomain exclusion; zero complete queries excluded', 'scope')
    require(c['cap4_degree_upper'] == [4, 8, 13], 'C4 bound')
    for k, claimed in enumerate(c['cap4_degree_upper'], 1):
        require(claimed == 3 * k + 1 + k * (k - 1) // 2 < 5 * k, 'C4 arithmetic')
    expected_cap5 = [{'k': k, 'm_required_min': 2 * k - 2, 'm_outerplane_max': 2 * k - 3}
                     for k in range(2, 6)]
    require(c['cap5_contradictions'] == expected_cap5, 'C5 outerplane bounds')
    for n in (4, 5):
        actual = polygon_triangulations(n)
        require(c['empty_cap_triangulations'][str(n)] == actual, 'empty-cap enumeration')
        require(len(actual) == {4: 2, 5: 5}[n], 'Catalan count')
        for ds in actual:
            incident = {v for d in ds for v in d}
            # The chord endpoints are adjacent positions 0 and n-1.
            require(any(v not in incident for v in range(1, n - 1)), 'no intermediate ear')
    interface = json.loads(INTERFACE.read_text())
    by_id = {row['id']: row for row in interface['cases']}
    require([(q['case_id'], q['target']) for q in c['queries']] == QUERIES, 'query whitelist')
    for query in c['queries']:
        source = by_id[query['case_id']]
        boundary = source['boundary_order']
        require(query['boundary_order'] == boundary, 'original ordered C8 changed')
        require(query['extras'] == source['extras'], 'original distribution changed')
        apices = {i for i, v in enumerate(boundary) if v.startswith('a')}
        private = set(range(8)) - apices
        require(len(apices) == 5 and len(private) == 3, 'apex/private types')
        expected = []
        for a in range(8):
            for b in range(a + 1, 8):
                d = min(b - a, 8 - b + a)
                if d < 2:
                    continue
                reason = {2: 'triangle ear has H-degree 2', 3: 'empty C4 has intermediate H-degree-2 ear',
                          4: 'both C5 caps must be wheels; intermediate private vertex has H-degree 3'}[d]
                if d == 4:
                    require(bool(private - {a, b}), 'diameter covers all private points')
                expected.append({'positions': [a, b], 'vertices': [boundary[a], boundary[b]],
                                 'distance': d, 'exclusion': reason})
        require(query['chords'] == expected and len(expected) == 20, 'complete chord coverage')
    ico = check_disk(c['controls']['icosahedron_cap'])
    require(ico == c['controls']['icosahedron_cap']['expected'], 'icosahedron geometry')
    require(ico['strict_interior'] == 6 and ico['interior_degrees'] == [5] * 6 and ico['all_triangles_facial'],
            'counterexample must meet local hypotheses')
    glued = check_disk(c['controls']['two_wheels'])
    require(glued == c['controls']['two_wheels']['expected'], 'two-wheel geometry')
    require(min(glued['boundary_degrees']) == 3 and glued['interior_degrees'] == [5, 5], 'weakened y control')
    require(c['complete_queries_excluded'] == 0, 'unjustified complete exclusion')
    return {'queries': len(QUERIES), 'named_chord_subdomains_excluded': 200,
            'C4_empty_triangulations': 2, 'C5_empty_triangulations': 5,
            'complete_queries_excluded': 0, 'controls': [ico, glued]}


def negative_controls(c):
    mutations = []
    bad = copy.deepcopy(c); bad['cap4_degree_upper'][2] = 15; mutations.append(('wrong C4 bound', bad))
    bad = copy.deepcopy(c); bad['queries'][0]['chords'].pop(); mutations.append(('omitted chord', bad))
    bad = copy.deepcopy(c); bad['queries'][0]['boundary_order'].reverse(); mutations.append(('reversed named boundary', bad))
    bad = copy.deepcopy(c); bad['controls']['icosahedron_cap']['faces'].pop(); mutations.append(('missing original face', bad))
    bad = copy.deepcopy(c); bad['complete_queries_excluded'] = 1; mutations.append(('unsupported whole-query exclusion', bad))
    result = []
    for name, bad in mutations:
        try:
            replay(bad)
        except (ValueError, KeyError):
            result.append({'name': name, 'status': 'rejected'})
        else:
            raise ValueError('negative control unexpectedly accepted: ' + name)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    parser.add_argument('--negative-controls', action='store_true')
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    result = replay(certificate)
    if args.negative_controls:
        result['negative_controls'] = negative_controls(certificate)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
