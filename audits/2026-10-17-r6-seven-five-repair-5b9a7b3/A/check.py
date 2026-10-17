#!/usr/bin/env python3
"""Full-component calibration of the arbitrary-size A1 paper theorem."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(a, b):
    return tuple(sorted((a, b)))


def parts(vertices, edges):
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    remaining = set(vertices)
    out = []
    while remaining:
        seen = {min(remaining)}
        todo = list(seen)
        while todo:
            a = todo.pop()
            for b in adjacency[a] - seen:
                seen.add(b)
                todo.append(b)
        out.append(seen)
        remaining -= seen
    return out


def whole_cycles(vertices, edges):
    adjacency = {v: [] for v in vertices}
    for a, b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)
    assert all(len(n) == 2 for n in adjacency.values())
    out = []
    for component in parts(vertices, edges):
        start = min(component)
        previous, current = None, start
        cycle = []
        while current not in cycle:
            cycle.append(current)
            nxt = min(v for v in adjacency[current] if v != previous)
            previous, current = current, nxt
        assert current == start and set(cycle) == component
        out.append(cycle)
    return out


def assert_matching(vertices, matching):
    flattened = list(itertools.chain.from_iterable(matching))
    assert sorted(flattened) == sorted(vertices)


def odd(cycles):
    return sum(len(cycle) % 2 for cycle in cycles)


def graph_from_sphere(faces):
    faces = sorted(tuple(sorted(f)) for f in faces)
    assert len(set(faces)) == len(faces)
    primal_edges = sorted({edge(a, b) for f in faces
                           for a, b in itertools.combinations(f, 2)})
    dual_edges = []
    for primal in primal_edges:
        incident = [i for i, f in enumerate(faces) if set(primal) <= set(f)]
        assert len(incident) == 2
        dual_edges.append(tuple(incident))
    vertices = set(range(len(faces)))
    edges = set(dual_edges)
    assert len(edges) == len(dual_edges)
    assert all(sum(v in e for e in edges) == 3 for v in vertices)
    return vertices, edges, faces, primal_edges


def all_matchings(vertices, edges):
    adjacency = {v: [] for v in vertices}
    for a, b in sorted(edges):
        adjacency[a].append(b)
        adjacency[b].append(a)

    def recurse(remaining, chosen):
        if not remaining:
            yield frozenset(chosen)
            return
        a = min(remaining)
        for b in sorted(adjacency[a]):
            if b in remaining:
                yield from recurse(remaining - {a, b}, chosen + [edge(a, b)])

    return list(recurse(set(vertices), []))


def symmetric_cycles(vertices, matching, reference):
    difference = matching ^ reference
    used = set(itertools.chain.from_iterable(difference))
    return [set(edge(c[i], c[(i + 1) % len(c)]) for i in range(len(c)))
            for c in whole_cycles(used, difference)] if difference else []


def assert_cluster_theorem(vertices, edges, matching, reference):
    old = edges - matching
    zero = edges - reference
    old_cycles = whole_cycles(vertices, old)
    assert not odd(whole_cycles(vertices, zero))
    difference_cycles = symmetric_cycles(vertices, matching, reference)
    records = []
    for component in parts(vertices, edges - (matching & reference)):
        assert len(component) % 2 == 0
        batch = set().union(*(q for q in difference_cycles
                              if set(itertools.chain.from_iterable(q)) <= component))
        changed = matching ^ batch
        assert_matching(vertices, changed)
        actual = edges - changed
        expected = {e for e in zero if set(e) <= component} | {
            e for e in old if not set(e) <= component}
        assert actual == expected
        assert all((a in component) == (b in component)
                   for a, b in actual)
        old_odd = sum(len(c) % 2 for c in old_cycles if set(c) <= component)
        assert old_odd % 2 == 0
        new_cycles = whole_cycles(vertices, actual)
        assert odd(new_cycles) == odd(old_cycles) - old_odd
        boundary = {e for e in edges if len(set(e) & component) == 1}
        assert boundary <= matching & reference
        assert len(boundary) % 2 == 0
        records.append({'vertices': sorted(component), 'old_odd': old_odd,
                        'boundary': sorted(boundary),
                        'new_cycles': new_cycles})
    return records


def frozen_control():
    provenance = json.loads((HERE / 'INPUT.json').read_text())
    frozen = HERE / provenance['frozen_path']
    assert sha(frozen) == provenance['sha256']
    raw = json.loads(frozen.read_text())
    vertices, edges, faces, primal_edges = graph_from_sphere(raw['J_faces'])
    matchings = all_matchings(vertices, edges)
    assert len(matchings) == 38
    cycles = {m: whole_cycles(vertices, edges - m) for m in matchings}
    even = [m for m in matchings if not odd(cycles[m])]
    all_pairs = []
    cap_records = []
    for matching in matchings:
        for reference in even:
            records = assert_cluster_theorem(vertices, edges, matching, reference)
            all_pairs.append({'M': sorted(matching), 'M0': sorted(reference),
                              'components': records})
            for cap in cycles[matching]:
                if len(cap) != 7:
                    continue
                cap_set = set(cap)
                chords = {e for e in matching if set(e) <= cap_set}
                if not chords:
                    continue
                assert len(chords) == 1
                boundary = {e for e in edges if len(set(e) & cap_set) == 1}
                assert len(boundary) == 5 and boundary <= matching
                assert len(reference & boundary) in (1, 3)
                if len(reference & boundary) != 3:
                    continue
                qs = symmetric_cycles(vertices, matching, reference)
                touching = [q for q in qs if q & boundary]
                assert len(touching) == 1
                q = touching[0]
                assert len(q & boundary) == 2
                new = matching ^ q
                cap_records.append({'M': sorted(matching),
                                    'M0': sorted(reference), 'C': cap,
                                    'boundary': sorted(boundary), 'Q': sorted(q),
                                    'old_cycles': cycles[matching],
                                    'new_cycles': whole_cycles(vertices, edges - new)})
    assert cap_records
    return {'provenance': provenance, 'vertices': sorted(vertices),
            'edges': sorted(edges), 'primal_faces': faces,
            'primal_edges': primal_edges,
            'stats': {'PMs': len(matchings), 'even_PM': len(even),
                      'all_PM_even_reference_pairs': len(all_pairs),
                      'cluster_components': sum(len(r['components']) for r in all_pairs),
                      'value3_nonfacial7_pairs': len(cap_records)},
            'all_pairs': all_pairs, 'value3_cap_records': cap_records}


def safe_no_descent_control():
    vertices = set(range(20))
    old_cycles = [list(range(7)), list(range(7, 15)), list(range(15, 20))]
    old = {edge(c[i], c[(i + 1) % len(c)]) for c in old_cycles
           for i in range(len(c))}
    matching = {edge(*e) for e in [(0, 3), (1, 7), (2, 8), (4, 9), (5, 10),
                                  (6, 19), (11, 15), (12, 16), (13, 17), (14, 18)]}
    edges = old | matching
    assert not old & matching
    assert_matching(vertices, matching)
    faces = [[0, 3, 4, 5, 6], [0, 1, 2, 3],
             [0, 6, 19, 18, 14, 7, 1], [1, 7, 8, 2], [2, 8, 9, 4, 3],
             [4, 9, 10, 5], [5, 10, 11, 15, 19, 6],
             [7, 14, 13, 12, 11, 10, 9, 8], [11, 12, 16, 15],
             [12, 13, 17, 16], [13, 14, 18, 17], [15, 16, 17, 18, 19]]
    darts = [(f[i], f[(i + 1) % len(f)]) for f in faces for i in range(len(f))]
    assert len(set(darts)) == len(darts) == 2 * len(edges)
    assert set(darts) == {(u, v) for a, b in edges for u, v in [(a, b), (b, a)]}
    assert len(vertices) - len(edges) + len(faces) == 2
    assert len(parts(vertices, edges)) == 1
    # Verify every oriented link is one cycle, so this is an oriented sphere.
    for v in vertices:
        links = {}
        for f in faces:
            if v in f:
                i = f.index(v)
                links[f[i - 1]] = f[(i + 1) % len(f)]
        assert len(links) == 3
        a = min(links)
        assert links[a] != a and links[links[a]] != a
        assert links[links[links[a]]] == a
    q = {edge(1, 2), edge(2, 8), edge(8, 7), edge(7, 1)}
    h = {edge(11, 12), edge(12, 16), edge(16, 15), edge(15, 11)}
    reference = matching ^ q ^ h
    assert_matching(vertices, reference)
    assert set(map(frozenset, symmetric_cycles(vertices, matching, reference))) == {
        frozenset(q), frozenset(h)}
    marks = [edge(0, 3), edge(4, 9), edge(11, 12)]
    assert [e in matching for e in marks] == [True, True, False]
    assert all(e in reference for e in marks)
    assert not q & set(marks)
    cap_set = set(range(7))
    boundary = {e for e in edges if len(set(e) & cap_set) == 1}
    assert len(boundary) == 5 and boundary <= matching
    assert len(boundary & reference) == 3
    after_q = matching ^ q
    after_cycles = whole_cycles(vertices, edges - after_q)
    reference_cycles = whole_cycles(vertices, edges - reference)
    assert sorted(map(len, after_cycles)) == [5, 15]
    assert list(map(len, reference_cycles)) == [20]
    assert odd(old_cycles) == odd(after_cycles) == 2
    records = assert_cluster_theorem(vertices, edges, matching, reference)
    assert len(records) == 1
    return {'scope': 'plane control only; source and minimality not asserted',
            'vertices': sorted(vertices), 'edges': sorted(edges), 'faces': faces,
            'M': sorted(matching), 'M0': sorted(reference),
            'marks_e_f_g': marks, 'Q': sorted(q), 'H': sorted(h),
            'cap_boundary': sorted(boundary), 'old_cycles': old_cycles,
            'after_Q_cycles': after_cycles, 'M0_cycles': reference_cycles,
            'cluster_components': records}


def build():
    return {'base': '5b9a7b3190c84bc10ff99608e372a9b4be57a0f6',
            'scope': 'paper calibration; not literal-source enumeration or exclusion',
            'local_bindings': {p: sha(HERE / p)
                               for p in ['PROOF.md', 'check.py', 'INPUT.json']},
            'frozen_control': frozen_control(),
            'safe_no_descent_control': safe_no_descent_control()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate-v2.json')
    parser.add_argument('--create', action='store_true')
    args = parser.parse_args()
    certificate = json.loads(json.dumps(build()))
    data = json.dumps(certificate, sort_keys=True, indent=2) + '\n'
    if args.create:
        with args.certificate.open('x') as handle:
            handle.write(data)
    else:
        assert json.loads(args.certificate.read_text()) == certificate, 'certificate mismatch'
    print(json.dumps({'ok': True, 'certificate_sha256': hashlib.sha256(data.encode()).hexdigest(),
                      'stats': certificate['frozen_control']['stats'],
                      'safe_Q_old_new_oddness': [2, 2]}, sort_keys=True))


if __name__ == '__main__':
    main()
