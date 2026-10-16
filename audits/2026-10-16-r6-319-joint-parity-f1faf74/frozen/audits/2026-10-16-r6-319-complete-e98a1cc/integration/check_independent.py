#!/usr/bin/env python3
"""Independent direct-assignment replay of the fixed planar countercontrol."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def colours(n, edges):
    # Fix a triangle, enumerate every other assignment directly, then restore
    # all 24 literal frames. No propagation or previous checker is imported.
    triangle = next(t for t in itertools.combinations(range(n), 3)
                    if all(tuple(sorted(uv)) in edges for uv in itertools.combinations(t, 2)))
    private = [u for u in range(n) if u not in triangle]
    representatives = []
    for values in itertools.product(range(4), repeat=len(private)):
        c = [0] * n
        for u, value in zip(triangle, range(3)):
            c[u] = value
        for u, value in zip(private, values):
            c[u] = value
        if all(c[u] != c[v] for u, v in edges):
            representatives.append(c)
    return sorted({tuple(p[x] for x in c) for p in itertools.permutations(range(4))
                   for c in representatives})


def pms(n, edges):
    # Independent bit-mask recursion, with the most constrained unmatched
    # vertex chosen at every step rather than a fixed smallest vertex.
    adjacency = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        adjacency[u].append((v, i))
        adjacency[v].append((u, i))

    def solve(left):
        if not left:
            yield ()
            return
        options = {u: [(v, i) for v, i in adjacency[u] if left & (1 << v)]
                   for u in range(n) if left & (1 << u)}
        u = min(options, key=lambda x: (len(options[x]), -x))
        for v, i in options[u]:
            for rest in solve(left ^ (1 << u) ^ (1 << v)):
                yield tuple(sorted((i,) + rest))
    return sorted(solve((1 << n) - 1))


def cycles(n, edges, selected):
    incident = [[] for _ in range(n)]
    for i in selected:
        for u in edges[i]:
            incident[u].append(i)
    assert all(len(x) == 2 for x in incident)
    remaining, result = set(selected), []
    while remaining:
        i = min(remaining)
        start, u = edges[i]
        ordered = []
        while True:
            assert i in remaining
            remaining.remove(i)
            ordered.append(i)
            if u == start:
                break
            i = next(e for e in incident[u] if e != i)
            a, b = edges[i]
            u = b if a == u else a
        result.append(ordered)
    return result


def check_pin_grid(records, grid):
    pins = grid['ordered_pins']
    counts = [0] * (4 ** len(pins))
    indices = {}
    for j, colour in enumerate(records):
        i = 0
        for u in pins:
            i = 4 * i + colour[u]
        counts[i] += 1
        indices.setdefault(str(i), []).append(j)
    assert counts == grid['complete_fibre_counts']
    assert indices == grid['full_colour_record_indices']
    assert counts.count(0) == grid['empty_fibres']


def reconstruct():
    path = ROOT / 'C/certificate.json'
    certificate = json.loads(path.read_text())
    edges = [tuple(e) for e in certificate['edges']]
    rotation = certificate['rotation']
    n = len(rotation)
    # Independently recover every triangular face as a three-clique, and
    # identify the dual from its two incident faces on every original edge.
    faces = [t for t in itertools.combinations(range(n), 3)
             if all(tuple(sorted(uv)) in edges for uv in itertools.combinations(t, 2))]
    assert faces == [tuple(f) for f in certificate['faces']]
    assert len(faces) == 16 and n - len(edges) + len(faces) == 2
    dual = [tuple(i for i, face in enumerate(faces) if u in face and v in face)
            for u, v in edges]
    assert all(len(uv) == 2 for uv in dual)
    assert dual == [tuple(uv) for uv in certificate['dual_edges']]
    full = colours(n, edges)
    assert full == [tuple(c) for c in certificate['complete_J_colourings']]
    assert len(full) == 144
    check_pin_grid(full, certificate['J_six_pin_fibres'])
    all_pm = pms(len(faces), dual)
    assert all_pm == sorted(tuple(row['matching']) for row in certificate['perfect_matching_rows'])
    marks = certificate['marks']
    counts, weights, oddness, even111 = {}, {}, {}, []
    for matching in all_pm:
        complement = cycles(len(faces), dual, set(range(len(edges))) - set(matching))
        omega = sum(len(c) % 2 for c in complement)
        pattern = ''.join(str(int(e in matching)) for e in marks)
        counts[pattern] = counts.get(pattern, 0) + 1
        oddness[matching] = omega
        if omega == 0:
            weights[pattern] = weights.get(pattern, 0) + 2 ** len(complement)
            if pattern == '111':
                even111.append(matching)
    joint = [m for m in all_pm if marks[0] in m and
             ((marks[1] in m) != (marks[2] in m))]
    assert len(joint) == 1 and oddness[joint[0]] == 2
    assert counts.get('101') == 1 and counts.get('110', 0) == 0
    assert weights.get('111') == 6 and weights.get('101', 0) == weights.get('110', 0) == 0
    # Check every full Tait labelling with fixed alpha=1 and root colour zero.
    transition_rows = []
    for old in even111:
        new = joint[0]
        delta = set(old) ^ set(new)
        assert marks[0] not in delta and marks[2] not in delta and marks[1] in delta
        for colour in full:
            labels = [colour[u] ^ colour[v] for u, v in edges]
            if colour[0] != 0 or {i for i, x in enumerate(labels) if x == 1} != set(old):
                continue
            b_at = {u: i for i in delta - set(old) for u in dual[i]}
            transitions = {i for i in delta & set(old)
                           if labels[b_at[dual[i][0]]] != labels[b_at[dual[i][1]]]}
            new_cycles = cycles(len(faces), dual, set(range(len(edges))) - set(new))
            assert sorted(len(c) for c in new_cycles) == [7, 9]
            incidences = sorted(sum(i in transitions for i in c) for c in new_cycles)
            assert all(len(c) % 2 == sum(i in transitions for i in c) % 2 for c in new_cycles)
            assert (len(transitions), incidences) in [(2, [1, 1]), (4, [1, 3])]
            transition_rows.append(len(transitions))
    assert len(transition_rows) == 6
    assert sorted(transition_rows) == [2, 2, 2, 2, 4, 4]
    uedges = [tuple(uv) for uv in certificate['source_diagnostics']['U_edges']]
    ufull = colours(11, uedges)
    assert len(ufull) == 432
    for split in certificate['source_diagnostics']['complete_reflected_splits']:
        records = split['complete_U_fibres']
        assert ufull == sorted(tuple(row['complete_U_colour']) for row in records)
        assert sum(not row['passes_full_transfer'] for row in records) == 192
        check_pin_grid([row['complete_U_colour'] for row in records], split['seven_pin_fibres'])
    return {'status': 'PASS', 'source': 'not triggered',
            'checker_scope': 'independent direct assignments and bit-mask matching enumeration',
            'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'J_colourings': len(full), 'U_colourings': len(ufull),
            'perfect_matchings': len(all_pm), 'ordinary_joint': len(joint),
            'minimum_joint_oddness': 2, 'transition_two_split_labellings': transition_rows.count(2),
            'transition_four_split_labellings': transition_rows.count(4),
            'W111': 6, 'W110': 0, 'W101': 0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = reconstruct()
    if args.check:
        assert json.loads(args.check.read_text()) == result
    if args.output:
        with args.output.open('x') as stream:
            json.dump(result, stream, indent=2)
            stream.write('\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
