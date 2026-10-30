#!/usr/bin/env python3
"""Exact six-lift rank, cut witnesses, and complete two-terminal fibres.

No 4CT oracle. Edge indices distinguish parallel original edges. The finite
checks support the paper contracts; they do not prove a separator exists.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from four_color_counts_cone_verification import compatible, signatures

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'audits/2026-10-29-bernhart-endpoint-ray/r2-support-actions.json'
DEFAULT = ROOT / 'audits/2026-10-30-bernhart-marked-separation/verification.json'
CONTROL = DEFAULT.parent / 'control-input.json'
PAIRS = ((1, 2), (1, 3), (2, 3))


def complete_colorings(edges):
    """Exhaust all proper Tait assignments; no quotient by color permutations."""
    inc = defaultdict(list)
    for e, uv in enumerate(edges):
        assert uv[0] != uv[1]
        for v in uv:
            inc[v].append(e)
    assert all(len(row) in (1, 3) for row in inc.values())
    adj = [set(inc[a] + inc[b]) - {e} for e, (a, b) in enumerate(edges)]
    phi = [0] * len(edges)
    result = []

    def rec():
        best, choices = None, None
        for e, c in enumerate(phi):
            if c:
                continue
            avail = tuple(c for c in (1, 2, 3) if all(phi[j] != c for j in adj[e]))
            if not avail:
                return
            if choices is None or len(avail) < len(choices):
                best, choices = e, avail
        if best is None:
            result.append(tuple(phi))
            return
        for c in choices:
            phi[best] = c
            rec()
        phi[best] = 0

    rec()
    return sorted(result)


def components(edges, phi, pair):
    inc = defaultdict(list)
    for e, (a, b) in enumerate(edges):
        if phi[e] in pair:
            inc[a].append(e)
            inc[b].append(e)
    todo = set(inc)
    result = []
    while todo:
        verts, ee = {min(todo)}, set()
        queue = list(verts)
        for v in queue:
            for e in inc[v]:
                ee.add(e)
                for u in edges[e]:
                    if u not in verts:
                        verts.add(u)
                        queue.append(u)
        todo -= verts
        ends = sorted(v for v in verts if len(inc[v]) == 1)
        assert len(ends) in (0, 2)
        result.append((ends, sorted(ee)))
    return result


def observation(edges, phi, leaves):
    leaf_index = {v: i for i, v in enumerate(leaves)}
    word = tuple(phi[next(e for e, uv in enumerate(edges) if v in uv)] for v in leaves)
    sigs = []
    for pair in PAIRS:
        sigs.append(tuple(sorted((min(leaf_index[a], leaf_index[b]),
                                 max(leaf_index[a], leaf_index[b]),
                                 -1 if len(ee) % 2 else 1)
                                for ends, ee in components(edges, phi, pair) if ends
                                for a, b in [ends])))
    return word, tuple(sigs)


def marked_orbits(edges, colorings, marked, leaves):
    """Actual original-edge cycle swaps, retaining each full coloring token."""
    inc = defaultdict(list)
    for e, uv in enumerate(edges):
        for v in uv:
            inc[v].append(e)
    p, q = edges[marked]
    assert len(inc[p]) == len(inc[q]) == 3
    universe = set(colorings)

    def sign(phi, v):
        row = [phi[e] for e in inc[v]]
        return (-1) ** sum(row[i] > row[j] for i in range(3) for j in range(i + 1, 3))

    adjacency = {}
    for phi in colorings:
        targets = []
        word, _ = observation(edges, phi, leaves)
        for other in (1, 2, 3):
            if other == phi[marked]:
                continue
            pair = (phi[marked], other)
            ends, ee = next(part for part in components(edges, phi, pair) if marked in part[1])
            assert not ends
            changed = list(phi)
            for e in ee:
                changed[e] = sum(pair) - changed[e]
            target = tuple(changed)
            assert target in universe
            assert observation(edges, target, leaves)[0] == word
            assert sign(target, p) == -sign(phi, p) and sign(target, q) == -sign(phi, q)
            targets.append(target)
        assert len(set(targets)) == 2
        adjacency[phi] = targets
    assert all(phi in adjacency[psi] for phi, targets in adjacency.items() for psi in targets)
    pending, result = set(colorings), []
    while pending:
        seed = min(pending)
        orbit, queue = {seed}, [seed]
        for phi in queue:
            for target in adjacency[phi]:
                if target not in orbit:
                    orbit.add(target)
                    queue.append(target)
        pending -= orbit
        buckets = Counter((phi[marked], sign(phi, p)) for phi in orbit)
        assert len(orbit) % 6 == 0
        assert len(buckets) == 6 and set(buckets.values()) == {len(orbit) // 6}
        assert len({sign(phi, p) * sign(phi, q) for phi in orbit}) == 1
        result.append(dict(length=len(orbit), word=observation(edges, seed, leaves)[0],
                           six_bucket_size=len(orbit) // 6,
                           endpoint_sign_product=sign(seed, p) * sign(seed, q)))
    return result


def determinant(matrix):
    a = [list(map(Fraction, row)) for row in matrix]
    answer = Fraction(1)
    for j in range(len(a)):
        p = next(i for i in range(j, len(a)) if a[i][j])
        if p != j:
            a[p], a[j] = a[j], a[p]
            answer = -answer
        pivot = a[j][j]
        answer *= pivot
        for i in range(j + 1, len(a)):
            factor = a[i][j] / pivot
            for k in range(j, len(a)):
                a[i][k] -= factor * a[j][k]
    assert answer.denominator == 1
    return int(answer)


def target_checks():
    saved = json.loads(SOURCE.read_text())
    receipt = json.loads((SOURCE.parent / 'RECEIPT.json').read_text())
    digest = sha256(SOURCE.read_bytes()).hexdigest()
    assert receipt['sources_sha256'][str(SOURCE.relative_to(ROOT))] == digest
    six_sigs = tuple(signatures(6))
    positive = saved['signature_factorization']['pairs']
    indices = sorted(r['six_signature_index'] for r in positive)
    ss = [six_sigs[i] for i in indices]
    assert len(ss) == 23 and all(r['weight'] == 1 for r in positive)
    h = {tuple(r['six_word']): r['three_cap_colors'][0]
         for r in saved['word_factorization']['rows']}
    assert len(h) == 729 and Counter(h.values()) == {0: 648, 1: 75, 2: 6}
    basis, rows, matrix = {}, [], []
    for w in product((1, 2, 3), repeat=6):
        for pair in PAIRS:
            row = [int(compatible(w, pair, s)) for s in ss]
            assert sum(row) == h[w]
            reduced = list(map(Fraction, row))
            for col, b in sorted(basis.items()):
                if reduced[col]:
                    factor = reduced[col]
                    reduced = [a - factor * x for a, x in zip(reduced, b)]
            pivot = next((i for i, x in enumerate(reduced) if x), None)
            if pivot is not None:
                factor = reduced[pivot]
                basis[pivot] = [x / factor for x in reduced]
                rows.append(dict(word=w, pair=pair))
                matrix.append(row)
    det = determinant(matrix)
    assert len(basis) == 23 and abs(det) == 1
    witnesses, balanced = [], []
    for mask in range(64):
        ports = [i for i in range(6) if mask >> i & 1]
        witness = next((w for w, value in sorted(h.items()) if value and
                        reduce(int.__xor__, (w[i] for i in ports), 0)), None)
        if witness is None:
            balanced.append(ports)
        else:
            witnesses.append(dict(ports=ports, positive_word=witness, h=h[witness],
                                  boundary_xor=reduce(int.__xor__, (witness[i] for i in ports), 0)))
    assert balanced == [[], list(range(6))] and len(witnesses) == 62
    return dict(source_sha256=digest, positive_six_signature_indices=indices,
                incidence_equations=2187, minor_rows=rows, minor_matrix=matrix,
                minor_determinant=det, rank=23, balanced_leaf_subsets=balanced,
                leaf_split_two_cut_witnesses=witnesses)


def two_terminal_checks():
    base = [(i, (i + 1) % 6) for i in range(6)] + [(i, 6 + i) for i in range(6)]
    leaves = list(range(6, 12))
    core = complete_colorings(base)
    controls = []
    # Each replacement has two terminal stems and a leaf-free cubic interior.
    regions = [
        ('parallel_two', [(0, 12), (12, 13), (12, 13), (13, 1)], [12, 13], 2),
        ('K4_minus_edge', [(0, 12), (13, 1), (12, 14), (12, 15),
                           (13, 14), (13, 15), (14, 15)], [12, 13, 14, 15], 2),
        ('two_parallel_pairs', [(0, 12), (12, 13), (12, 13), (13, 14),
                                (14, 15), (14, 15), (15, 1)], [12, 13, 14, 15], 4),
    ]
    for name, replacement, interior, expected in regions:
        original = base[1:] + replacement
        full = complete_colorings(original)
        fibres = defaultdict(list)
        for phi in full:
            left, right = phi[len(base) - 1], phi[-1] if name != 'K4_minus_edge' else phi[len(base)]
            assert left == right
            projected = (left,) + phi[:len(base) - 1]
            assert projected in core
            assert observation(original, phi, leaves) == observation(base, projected, leaves)
            fibres[projected].append(phi)
        assert set(fibres) == set(core)
        assert {len(v) for v in fibres.values()} == {expected}
        base_table = Counter(observation(base, phi, leaves) for phi in core)
        full_table = Counter(observation(original, phi, leaves) for phi in full)
        assert full_table == Counter({key: value * expected for key, value in base_table.items()})
        controls.append(dict(name=name, edges=original, interior=interior,
                             ordered_cut_edge_indices=[len(base) - 1,
                                 len(base) if name == 'K4_minus_edge' else len(original) - 1],
                             core_edges=base, leaves=leaves, multiplier=expected,
                             core_complete_colorings=core, complete_colorings=full,
                             projection_fibres=[dict(core_coloring=p, extensions=v)
                                                for p, v in sorted(fibres.items())],
                             complete_signature_tuples_preserved=True,
                             all_729_boundary_fibres_including_empty_checked=True))
    return controls


def marked_control():
    fixture = json.loads(CONTROL.read_text())
    edges = fixture['edges']
    rotation = {int(v): row for v, row in fixture['rotations'].items()}
    leaves, marked = fixture['boundary_order'], fixture['marked_edge']
    for v, row in rotation.items():
        assert sorted(row) == [e for e, uv in enumerate(edges) if v in uv]
        assert len(row) == (1 if v in leaves else 3)
    pending = {(e, v) for e, uv in enumerate(edges) for v in uv}
    faces = []
    while pending:
        root = min(pending)
        dart, face = root, []
        while True:
            assert dart in pending
            pending.remove(dart)
            e, v = dart
            face.append([v, e])
            a, b = edges[e]
            w = a if b == v else b
            row = rotation[w]
            dart = row[(row.index(e) - 1) % len(row)], w
            if dart == root:
                break
        faces.append(face)
    assert len(rotation) - len(edges) + len(faces) == 2
    outer = [face for face in faces if set(leaves) <= {v for v, e in face}
             and marked in {e for v, e in face}]
    assert len(outer) == 1
    order = [v for v, e in outer[0] if v in leaves]
    start = order.index(min(order))
    assert order[start:] + order[:start] == leaves
    full = complete_colorings(edges)
    assert len(full) == 576
    orbits = marked_orbits(edges, full, marked, leaves)
    assert Counter(r['length'] for r in orbits) == {6: 96}

    def connected_parts(removed):
        todo, answer = set(rotation), []
        while todo:
            vs, queue = {min(todo)}, [min(todo)]
            for v in queue:
                for e in rotation[v]:
                    if e not in removed:
                        for w in edges[e]:
                            if w not in vs:
                                vs.add(w)
                                queue.append(w)
            todo -= vs
            answer.append(vs)
        return answer

    assert len(connected_parts(set())) == 1
    regions = {}
    for cut in combinations(range(len(edges)), 2):
        for vs in connected_parts(set(cut)):
            if not vs.intersection(leaves):
                delta = [e for e, (a, b) in enumerate(edges) if (a in vs) != (b in vs)]
                if len(delta) == 2:
                    regions[tuple(sorted(vs))] = delta
    assert list(regions) == [tuple(range(40))]
    interior, cut = next(iter(regions.items()))
    assert len(connected_parts(set(cut))) == 3
    assert all(len(connected_parts({e})) == 2 for e in cut)
    inside = set(interior)
    assert set(edges[marked]) <= inside
    retained = [e for e, (a, b) in enumerate(edges) if a not in inside and b not in inside]
    outside = [next(v for v in edges[e] if v not in inside) for e in cut]
    core_edges = [edges[e] for e in retained] + [outside]
    core = complete_colorings(core_edges)
    assert len(core) == 48 and len(core_edges) == len(set(sum(core_edges, []))) - 1
    fibres = defaultdict(list)
    for phi in full:
        assert phi[cut[0]] == phi[cut[1]]
        psi = tuple(phi[e] for e in retained) + (phi[cut[0]],)
        assert psi in core
        assert observation(edges, phi, leaves) == observation(core_edges, psi, leaves)
        fibres[psi].append(phi)
    assert set(fibres) == set(core) and {len(v) for v in fibres.values()} == {12}

    n, obs_counts, word_ids = Counter(), Counter(), defaultdict(list)
    for coloring_id, phi in enumerate(full):
        w, sigs = observation(edges, phi, leaves)
        n[w] += 1
        word_ids[w].append(coloring_id)
        for pair, s in zip(PAIRS, sigs):
            obs_counts[w, pair, s] += 1
    y = []
    for s in signatures(6):
        values = {obs_counts[w, pair, s] for w in product((1, 2, 3), repeat=6)
                  for pair in PAIRS if compatible(w, pair, s)}
        assert len(values) == 1
        y.append(dict(signature=s, count=values.pop()))
    assert len(n) == 48 and set(n.values()) == {12}
    assert sum(r['count'] > 0 for r in y) == 13
    assert {r['count'] for r in y if r['count']} == {12}
    coloring_index = {phi: i for i, phi in enumerate(full)}
    return dict(name=fixture['name'], input_sha256=sha256(CONTROL.read_bytes()).hexdigest(),
                sphere_faces=faces, outer_face=outer[0],
                complete_coloring_encoding='Each string lists colors 1/2/3 in original edge-index order.',
                complete_colorings=[''.join(map(str, phi)) for phi in full],
                n=[dict(word=w, count=n[w], complete_coloring_ids=word_ids[w])
                   for w in product((1, 2, 3), repeat=6)], y=y, marked_orbits=orbits,
                two_edge_deletions_checked=len(edges) * (len(edges) - 1) // 2,
                leaf_free_regions=[dict(vertices=interior, cut=cut, marked_location='strictly_inside')],
                region_complement_components=2, region_cut_edges_are_bridges=True,
                reduced_core_edges=core_edges, reduced_core_complete_colorings=core,
                projection_fibres=[dict(core_coloring=p, extension_coloring_ids=[coloring_index[phi] for phi in v])
                                   for p, v in sorted(fibres.items())],
                all_signature_tuples_preserved=True, multiplier=12, reduced_core_is_tree=True,
                target_positive_words=81, actual_positive_words=48,
                target_positive_signatures=23, actual_positive_signatures=13,
                scope='Refutes automatic preservation of the marked-edge condition under two-terminal deletion. Does not refute unmarked separation existence; does not realize the target lift.')


def report():
    return json.loads(json.dumps(dict(target=target_checks(),
        two_terminal_controls=two_terminal_checks(),
        marked_control=marked_control(),
        conclusion='Marked-safe deletion is not automatic; unmarked separator existence under the full target lift and r2 exclusion remain OPEN.'), sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = report()
    if args.check:
        assert json.loads(args.check.read_text()) == result
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(rank=result['target']['rank'], determinant=result['target']['minor_determinant'],
                         proper_leaf_subset_witnesses=62,
                         two_terminal_controls=len(result['two_terminal_controls']),
                         marked_control_complete_colorings=len(result['marked_control']['complete_colorings']),
                         marked_control_orbits=len(result['marked_control']['marked_orbits']),
                         marked_control_multiplier=result['marked_control']['multiplier'],
                         excluded_rays=[]), sort_keys=True))


if __name__ == '__main__':
    main()
