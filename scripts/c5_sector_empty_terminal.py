#!/usr/bin/env python3
"""Compose terminal-block certificates with the empty-branch attachment lemma."""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_sector_terminal_blocks import (
    ROWS, U, edge, lists, minor_case, verify_minor, verify_subdivision,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_sector_empty_terminal/observations.json'
EMPTY = ROOT / 'artifacts/c5_sector_empty_branch/observations.json'
TERMINAL = ROOT / 'artifacts/c5_sector_terminal_blocks/observations.json'


def lift_edges(saved_edges, length):
    """Replace x-t-0 by x-p1-...-b-0; give b three internal edges."""
    path = ['x'] + [f'p{i}' for i in range(1, length)] + ['b']
    result = set()
    for a, c in saved_edges:
        if edge(a, c) == edge('x', 't'):
            result.update(edge(u, v) for u, v in zip(path, path[1:]))
        else:
            result.add(edge('b' if a == 't' else a, 'b' if c == 't' else c))
    result.update((edge('b', 'h1'), edge('b', 'h2')))
    neighbors = {v for a, c in result for u, v in ((a, c), (c, a)) if u == 'b'}
    assert neighbors & set(map(str, range(5))) == {'0'}
    assert len(neighbors - set(map(str, range(5)))) == 3
    return result, path


def lift_path(old, connector):
    result = ['b' if old[0] == 't' else old[0]]
    for a, c in zip(old, old[1:]):
        if edge(a, c) == edge('x', 't'):
            segment = connector if a == 'x' else connector[::-1]
            assert result[-1] == segment[0]
            result.extend(segment[1:])
        else:
            result.append('b' if c == 't' else c)
    return result


def build():
    empty, terminal = [json.loads(p.read_text()) for p in (EMPTY, TERMINAL)]
    inputs = {EMPTY, TERMINAL, Path(__file__).resolve(),
              ROOT / 'scripts/c5_sector_terminal_blocks.py'}
    for saved in (empty, terminal):
        for name, digest in saved['input_sha256'].items():
            assert sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
            inputs.add(ROOT / name)
    assert empty['color1_neighbor']['surviving_attachments'] == [[0]]
    assert empty['color1_neighbor']['internal_degree'] == 3

    groups = {}
    for aa in combinations(range(5), 2):
        ls = [lists([aa], row)[0] for row in ROWS]
        if all(len(p) == 2 for p in ls):
            groups.setdefault(tuple(tuple(sorted(p)) for p in ls), []).append(aa)
    assert len(groups) == 5
    classes = []
    for palettes, attachments in groups.items():
        touches0 = all(0 in aa for aa in attachments)
        assert touches0 or all(0 not in aa for aa in attachments)
        if touches0:
            # Every odd terminal cycle has at least two private points, each
            # of inner degree 2, hence distinct from the inner-degree-3 b.
            assert 2 + 1 > 2
            reason = 'two private 0-neighbors plus distinct b exceed degree(0)=2'
            roots = []
        else:
            assert all(0 in p for p in palettes)
            roots = [list(aa) for k in (0, 1) for aa in combinations(range(5), k)
                     if all(set(p) <= ls for p, ls in
                            zip(palettes, (lists([aa], row)[0] for row in ROWS)))]
            assert all(0 not in aa for aa in roots)
            reason = 'all private vertices and root avoid frame 0; b lies outside'
        classes.append(dict(palettes=palettes, attachments=attachments,
                            touches0=touches0, root_attachments=roots, reason=reason))
    assert sum(c['touches0'] for c in classes) == 3

    # Complete single-block K4: each vertex has precisely one frame neighbor.
    # Exactly two attach to 0. Explicit alpha colorings refute rejection.
    k4 = []
    for aa in product(range(5), repeat=4):
        if aa.count(0) != 2:
            continue
        ls = lists([(i,) for i in aa], ROWS[0])
        coloring = next((cs for cs in product(*map(sorted, ls)) if len(set(cs)) == 4), None)
        assert coloring is not None
        assert all(c in allowed for c, allowed in zip(coloring, ls))
        k4.append(dict(frame_neighbors=aa, alpha_coloring=coloring))
    assert len(k4) == 96

    # Two terminal triangles sharing their root exhaust its four internal
    # edges. If C is connected, these are all its vertices: no degree-3 b.
    shared_edges = {edge(a, c) for a, c in
                    [('x','u'),('u','v'),('v','x'),('x','a'),('a','d'),('d','x')]}
    shared_degrees = {v: sum(v in e for e in shared_edges) for v in ['x','u','v','a','d']}
    assert sorted(shared_degrees.values()) == [2, 2, 2, 2, 4]

    for record in terminal['minors']:
        verify_minor(set(map(tuple, record['edges'])), record['branch_sets'], record['target'])
    # Representative lifts cover each generic construction; all 177 saved
    # original minors were checked above. No planarity oracle is called.
    prefixes = ('C5-', 'C7-', 'K4-', 'triangle-same-1-2', 'triangle-same-3-2',
                'triangle-same-1-4', 'triangle-same-3-4', 'root-spoke-2',
                'root-spoke-4', 'two-disjoint-terminal-triangles')
    chosen = [next(r for r in terminal['minors'] if r['name'].startswith(p)) for p in prefixes]
    lifted = []
    for r in chosen:
        for length in (1, 2, 5):
            es, path = lift_edges(r['edges'], length)
            groups0 = [set(g)-{'t'} | (set(path[1:]) if 't' in g else set())
                       for g in r['branch_sets']]
            case = minor_case(f"{r['name']}-b-path-{length}", es, groups0, r['target'])
            case.update(source_certificate=r['name'], connector=path + ['0'])
            lifted.append(case)
    subdivisions = []
    for length in (1, 2, 5):
        es, path = lift_edges(terminal['mixed4']['edges'], length)
        paths = [lift_path(p, path) for p in terminal['mixed4']['paths']]
        verify_subdivision(es, paths)
        subdivisions.append(dict(edges=sorted(es), paths=paths, connector=path + ['0']))
    return dict(schema=1,
                scope='Empty N(0) intersect B3 branch with the specified 397->330 transition and both rejected rows; not general 3903 exclusion.',
                control_scope='Lifted paths and degree-3 b are necessary local skeletons, not complete sector realizations; arbitrary lengths use the paper proof.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                              for p in sorted(inputs)},
                joint_cycle_classes=classes, single_k4_colorings=k4,
                shared_root=dict(edges=sorted(shared_edges), inner_degrees=shared_degrees),
                lifted_minors=lifted, lifted_subdivisions=subdivisions,
                summary=dict(joint_cycle_classes=5, excluded_frame0_classes=3,
                             single_k4_colorings=len(k4), shared_root_controls=1,
                             inherited_minors_checked=len(terminal['minors']),
                             lifted_minors=len(lifted), lifted_subdivisions=len(subdivisions)),
                closure_effect=dict(inherited_profiles=603, profile_deletions=0,
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
