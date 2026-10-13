#!/usr/bin/env python3
"""Complete C8 polygon-dissections with optional independent face hubs.

This family is finite and explicitly defined. It is not all caps with <=5
private vertices. Every boundary fibre, including empty fibres, is retained.
"""
import argparse
import copy
import gzip
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
FROZEN = HERE / 'frozen'


def custody():
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    for row in manifest['files']:
        data = (FROZEN / row['path']).read_bytes()
        assert len(data) == row['bytes']
        assert hashlib.sha256(data).hexdigest() == row['sha256']
    return manifest['base']


def normalized(word):
    colors = {}
    return tuple(colors.setdefault(c, len(colors)) for c in word)


def cross(e, f):
    a, b = e
    c, d = f
    return a < c < b < d or c < a < d < b


def dissections(n):
    diagonals = [(a, b) for a in range(n) for b in range(a+2, n)
                 if (a, b) != (0, n-1)]
    def visit(chosen, start):
        yield chosen
        for i in range(start, len(diagonals)):
            edge = diagonals[i]
            if not any(cross(edge, old) for old in chosen):
                yield from visit(chosen + (edge,), i+1)
    yield from visit((), 0)


def faces(n, diagonals):
    result = [tuple(range(n))]
    for a, b in diagonals:
        candidates = [f for f in result if a in f and b in f]
        assert len(candidates) == 1
        face = candidates[0]
        i, j = sorted((face.index(a), face.index(b)))
        assert j-i > 1 and (i, j) != (0, len(face)-1)
        result.remove(face)
        result.extend((face[i:j+1], face[j:] + face[:i+1]))
    return sorted(tuple(f[f.index(min(f)):] + f[:f.index(min(f))])
                  for f in result)


def fibres(rows, diagonals, hub_faces):
    result = []
    for row in rows:
        if any(row[a] == row[b] for a, b in diagonals):
            result.append([])
        else:
            domains = [tuple(c for c in range(4) if c not in {row[v] for v in f})
                       for f in hub_faces]
            result.append([list(c) for c in itertools.product(*domains)])
    return result


def build():
    base = custody()
    n = 8
    literal = [p for p in itertools.product(range(4), repeat=n)
               if all(p[i] != p[(i+1) % n] for i in range(n))]
    rows = sorted({normalized(p) for p in literal})
    prior = json.loads((FROZEN / 'audits/2026-10-13-c8-joint-count-3097ef5/interface.json').read_text())
    assert rows == list(map(tuple, prior['pattern_order']))
    queries = [q for q in json.loads((FROZEN / 'audits/2026-10-13-c5-no4ct-c8-6cafdfb/RESULTS.json').read_text())['queries']
               if q['status'] == 'necessary_condition_residual']
    assert len(queries) == 8
    caps = []
    dissection_count = 0
    triangulations = 0
    histogram = Counter()
    for chords in dissections(n):
        dissection_count += 1
        polygons = faces(n, chords)
        assert sum(len(f)-2 for f in polygons) == n-2
        triangulations += all(len(f) == 3 for f in polygons)
        eligible = [f for f in polygons if len(f) >= 4]
        for mask in range(1 << len(eligible)):
            selected = [f for i, f in enumerate(eligible) if mask >> i & 1]
            assert len(selected) <= 3 <= 5
            full = fibres(rows, chords, selected)
            relation = sum(1 << i for i, f in enumerate(full) if f)
            hits = {q['query_id']: (relation & q['support']).bit_count() for q in queries}
            histogram[len(selected)] += 1
            caps.append(dict(id=len(caps), boundary_order=[f'c{i}' for i in range(n)],
                             chords=chords, dissection_faces=polygons,
                             hub_faces=selected, hub_names=[f'z{i}' for i in range(len(selected))],
                             full_hub_lifts_by_literal_row=full,
                             relation=relation, upper_support_intersection=hits))
    # Independent polygon-triangulation recurrence: Catalan C6 = 132.
    catalan = [1]
    for j in range(1, n-1):
        catalan.append(sum(catalan[i]*catalan[j-1-i] for i in range(j)))
    assert triangulations == catalan[n-2] == 132
    summary = dict(dissections=dissection_count, triangulations=triangulations,
                   named_caps=len(caps), caps_by_private_vertices=dict(sorted(histogram.items())),
                   literal_boundary_assignments=len(literal), canonical_rows=len(rows),
                   full_fibres=len(caps)*len(rows),
                   empty_fibres=sum(not f for c in caps for f in c['full_hub_lifts_by_literal_row']),
                   full_lifts=sum(len(f) for c in caps for f in c['full_hub_lifts_by_literal_row']),
                   queries=len(queries), cap_query_checks=len(caps)*len(queries),
                   newly_excluded=sorted(q['query_id'] for q in queries if any(
                       not c['upper_support_intersection'][q['query_id']] for c in caps)),
                   minimum_intersections={q['query_id']: min(
                       c['upper_support_intersection'][q['query_id']] for c in caps) for q in queries})
    return dict(schema='no4ct-generalized-cap-control-v1', base=base,
                color_frame=[0,1,2,3], boundary_rows=rows,
                lift_encoding='A full lift is literal boundary_rows[i] followed by one stored hub tuple; [] fibre means no lift; [[]] means one empty hub tuple.',
                scope='All labelled C8 noncrossing chord dissections; independently add one hub adjacent to every vertex of each selected face of length >=4. No adjacent hubs. Not all <=5-private-vertex caps.',
                source_status='Necessary support test only. No actual residual source constructed.',
                summary=summary, caps=caps)


def canonical(data):
    return json.loads(json.dumps(data))


def verify(got, expected):
    assert got == canonical(expected), 'complete cap certificate mismatch'


def negatives(expected):
    bad = copy.deepcopy(canonical(expected))
    row = next(i for i, f in enumerate(bad['caps'][0]['full_hub_lifts_by_literal_row']) if f)
    bad['caps'][0]['full_hub_lifts_by_literal_row'][row] = []
    controls = [('deleted_full_lift', bad)]
    bad = copy.deepcopy(canonical(expected));bad['caps'][0]['boundary_order'].reverse()
    controls.append(('reversed_named_boundary', bad))
    bad = copy.deepcopy(canonical(expected));bad['summary']['newly_excluded'] = ['c04-941']
    controls.append(('false_source_exclusion', bad))
    for name, bad in controls:
        try:
            verify(bad, expected)
        except AssertionError:
            continue
        raise AssertionError(f'negative control accepted: {name}')
    return [name for name, _ in controls]


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', action='store_true')
    group.add_argument('--check', action='store_true')
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    expected = build()
    path = HERE / 'caps_certificate.json.gz'
    if args.write:
        data = json.dumps(expected, sort_keys=True, separators=(',', ':')).encode()+b'\n'
        with path.open('xb') as f:
            f.write(gzip.compress(data, mtime=0))
    else:
        verify(json.loads(gzip.decompress(path.read_bytes())), expected)
    result = dict(status='PASS', **expected['summary'])
    if args.negative:
        result['negative_controls_rejected'] = negatives(expected)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
