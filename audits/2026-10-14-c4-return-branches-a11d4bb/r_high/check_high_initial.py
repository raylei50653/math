#!/usr/bin/env python3
"""Named high-r all-lift frontiers; necessary terminal models, no source search."""
import argparse
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = ROOT / 'audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4'
HASHES = {
    'check_transfer.py': '0f8c67ee66af7ac4ff2d84b06a62e4f35e591b921417b620fe42f45435f56689',
    'cells.json': '04650cea947a5086360e895c1a7350690f53da745314379a3328b97ee02d81b8',
}
for file, expected in HASHES.items():
    if sha256((OLD / file).read_bytes()).hexdigest() != expected:
        raise ValueError('frozen input drift: ' + file)
spec = importlib.util.spec_from_file_location('frozen_transfer', OLD / 'check_transfer.py')
T = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T)
COLORS = tuple(range(4))


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def independent_old(boundary, pq):
    """One common normalization of all six pins, independent canonical table."""
    row = T.canonical(boundary + tuple(pq))
    table = {
        (0, 1, 0, 1): {(2, 3), (3, 2)},
        (0, 1, 0, 2): set(),
        (0, 1, 2, 1): {(1, 3), (3, 1), (2, 3), (3, 2)},
        (0, 1, 2, 3): {(1, 3), (3, 1)},
    }
    return row[4:] in table.get(row[:4], set())


def noncrossing(parts, boundary_size):
    labels = {v: i for i, block in enumerate(parts) for v in block}
    return all(not (labels[a] == labels[c] and labels[b] == labels[d]
                   and labels[a] != labels[b])
               for a, b, c, d in combinations(range(boundary_size), 4))


def closure(rows, edges, boundary_size):
    """Remove rows without a terminal partition for any complementary pairing."""
    options = {}
    for row in rows:
        all_pairings = []
        for pairing in T.PAIRINGS:
            choices = []
            for parts in product(*(T.pair_partitions(row, pair, edges) for pair in pairing)):
                if noncrossing(parts[0] + parts[1], boundary_size):
                    choices.append((parts, T.switch_orbit(row, parts, pairing)))
            all_pairings.append(choices)
        options[row] = all_pairings
    live = set(rows)
    rounds = []
    while True:
        dead = {row for row in live if any(
            not any(orbit <= live for parts, orbit in choices)
            for choices in options[row])}
        rounds.append({'live': [T.name(row) for row in sorted(live)],
                       'removed': [T.name(row) for row in sorted(dead)]})
        if not dead:
            break
        live -= dead
    witnesses = []
    for row in sorted(live):
        pairings = []
        for pairing, choices in zip(T.PAIRINGS, options[row]):
            parts, orbit = next((parts, orbit) for parts, orbit in choices if orbit <= live)
            pairings.append({'pairing': pairing, 'parts': parts,
                             'all_successors': [T.name(x) for x in sorted(orbit)]})
        witnesses.append({'row': T.name(row), 'pairings': pairings})
    return live, {'rounds': rounds, 'one_partition_per_pairing': witnesses}


def named_plane_control():
    """C5 with two chords and a single stellated central triangle."""
    edges = tuple((i, (i + 1) % 5) for i in range(5)) + ((0, 2), (2, 4), (0, 5), (2, 5), (4, 5))
    fibres = {}
    for f in product(COLORS, repeat=6):
        if all(f[a] != f[b] for a, b in edges):
            fibres.setdefault(T.name(f[:5]), []).append(T.name(f))
    canonical = sorted({T.name(T.canonical(tuple('ABCD'.index(c) for c in f)))
                        for fs in fibres.values() for f in fs})
    need(canonical == ['ABCABD', 'ABCADB', 'ABCBDB', 'ABCDBD'], 'named control full relation')
    need(sum(map(len, fibres.values())) == 96, 'named control complete count')
    return {'pins': ['z', 's', 'r', 'w', 'p', 'q'], 'edges': edges,
            'inner_faces': ['zsr', 'rwp', 'zrq', 'rpq', 'pzq'],
            'full_fibres': fibres, 'canonical_rows': canonical,
            'complete_colourings': 96,
            'source_forbidden_edges': ['zr', 'rp', 'rq'],
            'source_status': 'not a source; calibration graph has forbidden edges'}


def calculate():
    catalogue = json.loads((OLD / 'cells.json').read_text())
    patterns = [tuple(p) for p in catalogue['pattern_order']]
    masks = sorted(map(int, catalogue['cells']))
    cases = []
    # Direct t deletion: boundary (z,s,r,w,h), triangle (z,p,q).
    for alias in (False, True):
        edges = (tuple((i, (i + 1) % 5) for i in range(5)) +
                 (((0, 5), (4, 5)) if alias else ((0, 5), (0, 6), (5, 6))))
        total_pins = 6 if alias else 7

        def allowed(row, implementation):
            if any(row[a] == row[b] for a, b in edges):
                return False
            z, s, r, w, h = row[:5]
            pq = (h, row[5]) if alias else row[5:]
            return all(implementation((z, s, r, t), pq)
                       for t in COLORS if t not in (z, r, w, h))

        rows = set()
        for row in product(COLORS, repeat=total_pins):
            value = allowed(row, T.old_allowed)
            need(value == allowed(row, independent_old), 'independent t-deletion table disagrees')
            if value:
                rows.add(T.canonical(row))
        rows = sorted(rows)
        table = []
        upper = 0
        for i, boundary in enumerate(patterns):
            tails = [(q,) for q in COLORS] if alias else list(permutations(COLORS, 2))
            permitted = [T.name(tail) for tail in tails if allowed(boundary + tail, T.old_allowed)]
            if permitted:
                upper |= 1 << i
            table.append({'boundary': T.name(boundary), 'permitted_q' if alias else 'permitted_pq': permitted,
                          'all_t_lifts': T.name(tuple(c for c in COLORS
                                                    if c not in (boundary[0], boundary[2], boundary[3], boundary[4])))})
        candidates = [m for m in masks if not m & ~upper]
        surviving_masks = []
        controls = []
        for m in candidates:
            initial = [row for row in rows if m >> patterns.index(row[:5]) & 1]
            live, proof = closure(initial, edges, 5)
            support = sum(1 << i for i, b in enumerate(patterns) if any(row[:5] == b for row in live))
            if support == m:
                surviving_masks.append(m)
            controls.append({'mask': m, 'initial_rows': len(initial), 'live_rows': len(live),
                             'surviving_outer_support': support, **proof})
        need(upper == (940 if alias else 1020), 't deletion upper mask')
        need(surviving_masks == ([424] if alias else [424, 440, 632, 956, 960, 976, 1000, 1012, 1016, 1020]),
             'direct t=5 frontier')
        cases.append({'alias_h_equals_p': alias, 'pins': ['z', 's', 'r', 'w', 'p', 'q'] if alias
                      else ['z', 's', 'r', 'w', 'h', 'p', 'q'], 'edges': edges,
                      'all_labelled_rows_checked': 4 ** total_pins, 'table': table,
                      'upper_mask': upper, 'catalogue_candidates': candidates,
                      'surviving_masks': surviving_masks, 'terminal_controls': controls})
    # Original r=7: delete degree-five R boundary r, exposing induced C6.
    edges6 = tuple((i, (i + 1) % 6) for i in range(6)) + ((0, 6), (0, 7), (6, 7))
    patterns6 = sorted({T.canonical(row) for row in product(COLORS, repeat=6)
                        if all(row[i] != row[(i + 1) % 6] for i in range(6))})
    rows6 = set()
    for row in product(COLORS, repeat=8):
        if any(row[a] == row[b] for a, b in edges6):
            continue
        lifts = [r for r in COLORS if r not in row[1:6]]
        lhs = all(T.old_allowed((row[0], row[1], r, row[5]), row[6:]) for r in lifts)
        rhs = all(independent_old((row[0], row[1], r, row[5]), row[6:]) for r in lifts)
        need(lhs == rhs, 'independent r=7 table disagrees')
        if lhs:
            rows6.add(T.canonical(row))
    live6, control6 = closure(sorted(rows6), edges6, 6)
    table6 = []
    for boundary in patterns6:
        pqs = [T.name(pq) for pq in permutations(COLORS, 2)
               if len({boundary[0], *pq}) == 3 and all(
                   T.old_allowed((boundary[0], boundary[1], r, boundary[5]), pq)
                   for r in COLORS if r not in boundary[1:])]
        table6.append({'boundary': T.name(boundary), 'all_r_lifts': T.name(tuple(r for r in COLORS if r not in boundary[1:])),
                       'permitted_pq': pqs})
    need(len(patterns6) == 31 and len({row[:6] for row in rows6}) == 26, 'r=7 outer frontiers')
    need(len(rows6) == len(live6) == 111, 'r=7 necessary closure unexpectedly excludes a row')
    # Crossings and the dangerously weaker existential cap test.
    need(not noncrossing(((0, 2), (1, 3), (4,), (5,)), 6), 'C6 crossing negative control')
    negative_row = (0, 1, 2, 0, 2, 2, 3)
    z, s, r, w, h, p, q = negative_row
    lifts = [t for t in COLORS if t not in (z, r, w, h)]
    need(any(T.old_allowed((z, s, r, t), (p, q)) for t in lifts) and
         not all(T.old_allowed((z, s, r, t), (p, q)) for t in lifts), 'existential-lift negative control')
    return {'status': 'necessary frontiers checked; no new high-r source exclusion',
            'frozen_inputs': HASHES, 'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
            'direct_t5': cases,
            'r7': {'pins': ['z', 's', 'v', 'w', 'h', 't', 'p', 'q'], 'edges': edges6,
                   'proper_outer_orbits': 31, 'allowed_outer_orbits': 26, 'allowed_joint_orbits': 111,
                   'all_labelled_rows_checked': 65536, 'table': table6, **control6},
            'named_plane_control': named_plane_control(),
            'negative_controls': {'crossing_rejected': True, 'existential_cap_rejected': True},
            'actual_target_sources': 0,
            'scope': 'full local rows; component partitions necessary only; no common counts asserted for r=7'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'high.json')
    args = parser.parse_args()
    result = calculate()
    if args.check:
        need(json.loads(args.certificate.read_text()) == json.loads(json.dumps(result)), 'certificate mismatch')
    else:
        with args.certificate.open('x') as output:
            json.dump(result, output, indent=2)
            output.write('\n')
    print('PASS: t=5 frontiers 10 masks / alias424; r=7 26 outer and111 joint orbits; source exclusion OPEN')


if __name__ == '__main__':
    main()
