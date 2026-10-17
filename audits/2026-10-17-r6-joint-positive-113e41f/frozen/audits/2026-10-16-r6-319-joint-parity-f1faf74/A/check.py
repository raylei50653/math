#!/usr/bin/env python3
"""Independent finite calibration of complete Kempe rectangles/link locks.

The proof, not local component patterns, has arbitrary-size source authority.
No preceding checker is imported. No supplied minimum source is tested.
"""
import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
COLOURS = tuple(range(4))
PINS = ('z', 's', 'v', 'w', 't', 'p', 'q')
EDGES_U = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
           (0, 5), (5, 6), (6, 0))
J_PINS = ('m', 'z', 'v', 'w', 'u', 'd')
J_EDGES = ((0, 1), (0, 2), (0, 3), (2, 3),
           (1, 4), (1, 5), (4, 5))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def canonical(row):
    lab = {}
    return tuple(lab.setdefault(c, len(lab)) for c in row)


def u_proper(row):
    return all(row[a] != row[b] for a, b in EDGES_U)


def r_lifts(row):
    return [c for c in COLOURS if c not in row[1:5]]


def original_return(row, r):
    # Direct condition before any J simplification.
    z, s, _, _, t, p, q = row
    if z == r:
        return s == t and {p, q} == set(COLOURS) - {z, s}
    if s == t:
        return bool({p, q} & (set(COLOURS) - {z, s, r}))
    return {p, q} == {s, t}


def table_return(row, r):
    # Independent literal R table after a single common normalization.
    z, s, _, _, t, p, q = row
    normalized = canonical((z, s, r, t, p, q))
    table = {
        (0, 1, 0, 1): {(2, 3), (3, 2)},
        (0, 1, 0, 2): set(),
        (0, 1, 2, 1): {(1, 3), (3, 1), (2, 3), (3, 2)},
        (0, 1, 2, 3): {(1, 3), (3, 1)},
    }
    return normalized[4:] in table[normalized[:4]]


def fj(row):
    m, z, v, w, u, d = row
    e, f, g = v ^ w, u ^ d, m ^ z
    return (e == f) == (e == g)


def swap(row, component, pair):
    out = list(row)
    for vertex in component:
        need(row[vertex] in pair, 'component has an alien palette colour')
        out[vertex] = pair[1] if row[vertex] == pair[0] else pair[0]
    return tuple(out)


def calculate():
    base = json.loads((AUDIT / 'BASE.json').read_text())
    authority_paths = [
        'audits/2026-10-16-r6-319-continuation-f1faf74/A/PROOF.md',
        'audits/2026-10-16-r6-319-continuation-f1faf74/A/FINAL_ATTEMPT.md',
        'audits/2026-10-16-r6-319-continuation-f1faf74/B/FINAL_ATTEMPT.md',
    ]
    authorities = []
    by_path = {record['path']: record for record in base['inputs']}
    for rel in authority_paths:
        expected = by_path[rel]
        need(digest(AUDIT / 'frozen' / rel) == expected['sha256'],
             'frozen authority changed: ' + rel)
        authorities.append(expected)

    local = []
    j_rows = 0
    for row in product(COLOURS, repeat=7):
        proper = u_proper(row)
        lifts = r_lifts(row) if proper else []
        direct = [original_return(row, r) for r in lifts]
        table = [table_return(row, r) for r in lifts]
        need(direct == table, 'literal original all-r table mismatch')
        is_j = proper and row[1] == row[4]
        if is_j:
            j_rows += 1
            z, m, v, w, _, p, q = row
            need(len(lifts) == 1, 'J row lost unique complete r fibre')
            need(all(direct) == fj((m, z, v, w, p, q)), 'FJ mismatch')
        local.append([int(proper), r_lifts(row), lifts,
                      [int(x) for x in direct], int(is_j)])
    need(len(local) == 16384, 'missing full seven-pin slot')

    start = (2, 0, 0, 1, 2, 1)  # A=0,B=1,C=2,D=3
    cubes = []
    total = 0
    for x, y in product((False, True), repeat=2):
        ab = ((1, 5), (2, 3)) if x else ((1, 2, 3, 5),)
        cd = ((0,), (4,)) if y else ((0, 4),)
        blocks = [(part, (0, 1)) for part in ab]
        blocks += [(part, (2, 3)) for part in cd]
        members = []
        for mask in range(1 << len(blocks)):
            row = start
            for bit, (component, pair) in enumerate(blocks):
                if mask >> bit & 1:
                    row = swap(row, component, pair)
            need(all(row[a] != row[b] for a, b in J_EDGES),
                 'cube lost a literal retained edge')
            need(fj(row), 'a listed whole cube violates FJ')
            members.append(row)
        need(len(set(members)) == len(members), 'nonfaithful visible cube')
        total += len(members)
        if x:
            comp = next(p for p in ab if 2 in p)
            target = swap(start, comp, (0, 1))
            need(target == (2, 0, 1, 0, 2, 1), 'wrong S image')
            need(swap(target, comp, (0, 1)) == start, 'S inverse failed')
        if y:
            comp = next(p for p in cd if 4 in p)
            target = swap(start, comp, (2, 3))
            need(target == (2, 0, 0, 1, 3, 1), 'wrong T image')
            need(swap(target, comp, (2, 3)) == start, 'T inverse failed')
        if x and y:
            s = next(p for p in ab if 2 in p)
            t = next(p for p in cd if 4 in p)
            st = swap(swap(start, s, (0, 1)), t, (2, 3))
            ts = swap(swap(start, t, (2, 3)), s, (0, 1))
            need(st == ts == (2, 0, 1, 0, 3, 1), 'square does not commute')
        cubes.append({'X': x, 'Y': y, 'AB': ab, 'CD': cd,
                      'all_labelled_cube_members': members})
    need(total == 36, 'whole-cube total changed')

    # Exact singleton obstruction for CD and BD cubes, using every possible
    # full-link colour set consistent with the given visible neighbours.
    singleton_rows = []
    for family in ('CD', 'BD'):
        for first, second in product((2, 3) if family == 'CD' else (1, 3),
                                     repeat=2):
            if family == 'CD':
                row = (first, 0, 0, 1, second, 1)
            else:
                if first != second:
                    continue  # w,d forced into the same BD component
                row = (2, 0, 0, first, 2, second)
            for bitmask in range(16):
                colours = {c for c in COLOURS if bitmask >> c & 1}
                if 0 in colours or not {row[0], row[4], row[5]} <= colours:
                    continue
                lifts = [c for c in COLOURS if c not in colours]
                proper_lifts = [tuple(c if i == 1 else a
                                      for i, a in enumerate(row)) for c in lifts]
                all_fj = all(fj(r) for r in proper_lifts)
                need(all_fj == (lifts == [0]), 'singleton criterion failed')
                singleton_rows.append({'family': family, 'pins': row,
                                       'full_link_colour_set': sorted(colours),
                                       'all_z_lifts': lifts,
                                       'all_lifts_satisfy_FJ': all_fj})

    link_models = []
    for footprints in product((0, 1, 2, 3), repeat=4):
        # bit 0/1 means this actual component meets L in palette colour0/1.
        mixed = 3 in footprints
        orientation_results = []
        for orientations in product((0, 1), repeat=4):
            seen = 0
            for foot, reverse in zip(footprints, orientations):
                seen |= ((foot & 1) << 1 | (foot & 2) >> 1) if reverse else foot
            orientation_results.append(seen)
        persistent_both = all(seen == 3 for seen in orientation_results)
        need(mixed == persistent_both, 'mixed-link iff cube-lock failed')
        link_models.append({'component_link_intersections': footprints,
                            'all_oriented_link_palettes': orientation_results,
                            'mixed_component': mixed})

    return {
        'schema': 'source319-complete-kempe-rectangles-link-lock-v1',
        'base': base['head'],
        'binding': {'checker_sha256': digest(Path(__file__)),
                    'proof_sha256': digest(HERE / 'PROOF.md'),
                    'base_sha256': digest(AUDIT / 'BASE.json')},
        'frozen_authorities': authorities,
        'universe': {'pins': PINS, 'retained_edges': EDGES_U,
                     'columns': ['proper', 'raw_r_avoidance', 'all_legal_r_lifts',
                                 'return_per_lift', 'is_J_row'],
                     'all_16384_slots_including_empty': local},
        'component_cubes': cubes,
        'exact_singleton_local_rows': singleton_rows,
        'mixed_link_models': link_models,
        'summary': {'seven_pin_slots': len(local), 'proper_J_rows': j_rows,
                    'complete_visible_component_patterns': len(cubes),
                    'whole_cube_labelled_members': total,
                    'mixed_link_patterns': len(link_models),
                    'actual_minimum_sources': 0,
                    'source_realizability': 'not triggered',
                    'full319_exclusion': 'OPEN',
                    'joint_even_complement_positivity': 'OPEN'},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate-v2.json')
    args = parser.parse_args()
    result = calculate()
    if args.write:
        with args.certificate.open('x') as handle:
            handle.write(json.dumps(result, separators=(',', ':')) + '\n')
    else:
        need(json.loads(args.certificate.read_text()) == json.loads(json.dumps(result)),
             'certificate mismatch: complete fibres/cubes or proof binding changed')
    print(json.dumps({'ok': True, **result['summary']}, sort_keys=True))


if __name__ == '__main__':
    main()
