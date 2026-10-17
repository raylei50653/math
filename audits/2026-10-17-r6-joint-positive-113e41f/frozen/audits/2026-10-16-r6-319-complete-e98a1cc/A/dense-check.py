#!/usr/bin/env python3
"""Exact local calibration for the source cofacial equality quotients.

Finite controls are not realizations of the globally minimum source.
"""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FROZEN = ROOT / 'frozen'
COLORS = tuple(range(4))
AUTHORITY = (
    'audits/2026-10-15-j-source-geometry-6ddea32/PROOF.md',
    'audits/2026-10-15-route-round4-6ddea32/FULL_J_BRIDGE.md',
    'audits/2026-10-14-cofacial-fibres-676b102/r6/PROOF.md',
    'audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/R6_TRANSFER.md',
    'audits/2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md',
    'audits/2026-10-14-c4-mask13-joint6-fdd3e22/JOINT_FIBRES.md',
    'docs/tasks/c5_no4ct_handoff.md',
)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(row):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in row)


def name(row):
    return ''.join('ABCD'[c] for c in row)


def fj(m, z, v, w, p, q):
    return ((v ^ w) == (p ^ q)) == ((v ^ w) == (m ^ z))


def subsets(items):
    return [list(x) for k in range(len(items) + 1)
            for x in combinations(items, k)]


def fibre_algebra():
    rows = []
    for merge in ('p', 'q'):
        for m, v, w, other in product(COLORS, repeat=4):
            if len({m, v, w}) != 3 or other == m:
                continue
            p, q = (m, other) if merge == 'p' else (other, m)
            for missing in subsets([c for c in COLORS if c not in {m, other}]):
                direct = all(fj(m, z, v, w, p, q) for z in missing)
                formula = not missing or (
                    other in {v, w} and set(missing) == {v, w} - {other})
                need(direct == formula, 'exact universal missing-set formula')
                rows.append({'merge': merge, 'mvw': [m, v, w],
                             'pq': [p, q], 'missing': missing,
                             'all_lifts_fj': direct})
    need(len(rows) == 576, 'complete local missing-set row count')
    return rows


def colorings(vertices, edges):
    neighbors = {v: set() for v in vertices}
    for a, b in edges:
        need(a != b, 'quotient loop')
        neighbors[a].add(b)
        neighbors[b].add(a)
    order = sorted(vertices, key=lambda v: (-len(neighbors[v]), v))
    row = {}
    out = []

    def rec(i):
        if i == len(order):
            out.append([row[v] for v in vertices])
            return
        v = order[i]
        used = {row[u] for u in neighbors[v] if u in row}
        for c in COLORS:
            if c not in used:
                row[v] = c
                rec(i + 1)
                del row[v]

    rec(0)
    return sorted(out)


def quotient_control():
    pm = ['alpha', 'u', 'w', 'v', 'r0', 'beta']
    pz = ['alpha', 'p', 'q', 'j', 'beta']
    boundary = pm + list(reversed(pz[1:-1]))
    old_vertices = boundary + ['m', 'z']
    old_edges = [(boundary[i], boundary[(i + 1) % len(boundary)])
                 for i in range(len(boundary))]
    old_edges += [('m', v) for v in pm]
    old_edges += [('z', v) for v in pz] + [('m', 'z')]
    old_edges = sorted({tuple(sorted(e)) for e in old_edges})
    need(len(boundary) == 9 and len(old_vertices) == 11
         and len(old_edges) == 21, 'two-star disk Euler data')
    alias = {v: ('m' if v == 'p' else v) for v in old_vertices if v != 'z'}
    vertices = ['m', 'alpha', 'u', 'w', 'v', 'r0', 'beta', 'j', 'q']
    edges = sorted({tuple(sorted((alias[a], alias[b])))
                    for a, b in old_edges if 'z' not in (a, b)})
    all_rows = colorings(vertices, edges)
    fibres = []
    for values in all_rows:
        chi = dict(zip(vertices, values))
        lifted = {v: chi[alias[v]] for v in old_vertices if v != 'z'}
        used_link = {lifted[v] for v in ['m'] + pz}
        missing = sorted(set(COLORS) - used_link)
        direct = []
        for z in COLORS:
            full = {**lifted, 'z': z}
            if all(full[a] != full[b] for a, b in old_edges):
                direct.append(z)
        need(missing == direct, 'direct complete graph versus full z fibre')
        safe = all(fj(chi['m'], z, chi['v'], chi['w'], chi['m'], chi['q'])
                   for z in missing)
        formula = not missing or (
            chi['q'] in {chi['v'], chi['w']}
            and set(missing) == {chi['v'], chi['w']} - {chi['q']})
        need(safe == formula, 'graph fibre formula')
        fibres.append({'full_quotient_coloring': values,
                       'all_z_lifts': missing, 'all_lifts_fj': safe})
    saturated = [0, 1, 2, 3, 2, 1, 3, 2, 1]
    compatible = [0, 1, 2, 1, 3, 2, 1, 2, 1]
    need(saturated in all_rows and compatible in all_rows, 'explicit full witnesses')
    sat_fibre = next(r for r in fibres if r['full_quotient_coloring'] == saturated)
    good_fibre = next(r for r in fibres if r['full_quotient_coloring'] == compatible)
    need(sat_fibre['all_z_lifts'] == [], 'saturated empty fibre retained')
    need(good_fibre['all_z_lifts'] == [3] and good_fibre['all_lifts_fj'],
         'compatible singleton lift')
    return {'classification': 'local planar two-star quotient; not a source',
            'pm': pm, 'pz': pz, 'boundary': boundary,
            'old_vertices': old_vertices, 'old_edges': old_edges,
            'vertices': vertices, 'edges': edges,
            'complete_coloring_count': len(all_rows),
            'empty_z_fibres': sum(not row['all_z_lifts'] for row in fibres),
            'compatible_nonempty_z_fibres': sum(bool(row['all_z_lifts']) and row['all_lifts_fj']
                                                for row in fibres),
            'incompatible_nonempty_z_fibres': sum(bool(row['all_z_lifts']) and not row['all_lifts_fj']
                                                  for row in fibres),
            'explicit_saturated_witness': saturated,
            'explicit_compatible_witness': compatible,
            'empty_fibres_retained': True, 'fibres': fibres}


def old_r_rule(z, s, r, t, p, q):
    if any(a == b for a, b in ((z, s), (s, r), (r, t), (t, z))):
        return False
    if len({z, p, q}) != 3:
        return False
    if z == r:
        return s == t and {p, q} == set(COLORS) - {z, s}
    if s == t:
        return bool({p, q} & (set(COLORS) - {z, s, r, t}))
    return {p, q} == {s, t}


def old_full_u_screen():
    edges = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 5), (5, 6), (6, 0))
    table = {
        'ABABC': ('BC', 'CB'), 'ABACB': ('BC', 'CB', 'CD', 'DC'),
        'ABACD': ('BC', 'BD', 'CB', 'CD', 'DB', 'DC'),
        'ABCAB': ('BC', 'CB', 'CD', 'DC'), 'ABCAC': ('BC', 'CB'),
        'ABCAD': ('BC', 'BD', 'CB', 'CD', 'DB', 'DC'),
        'ABCBC': (), 'ABCBD': (), 'ABCDB': ('CD', 'DC'), 'ABCDC': (),
    }
    initial = set()
    refined = set()
    dense_proper = []
    dense_lifts = []
    dense_initial = []
    dense_refined = []
    for row in product(COLORS, repeat=7):
        proper = all(row[a] != row[b] for a, b in edges)
        dense_proper.append(int(proper))
        dense_lifts.append([c for c in COLORS if c not in row[1:5]])
        if not proper:
            dense_initial.append(0)
            dense_refined.append(0)
            continue
        z, s, v, w, t, p, q = row
        allowed = all(old_r_rule(z, s, r, t, p, q)
                      for r in COLORS if r not in {s, v, w, t})
        normalized = canonical(row)
        independent = name(normalized[5:]) in table[name(normalized[:5])]
        need(allowed == independent, 'all-r versus literal table')
        dense_initial.append(int(allowed))
        new_ok = (allowed
                  and (name(normalized[:5]) != 'ABACD' or t in {p, q})
                  and (name(normalized[:5]) != 'ABCAD' or s in {p, q}))
        dense_refined.append(int(new_ok))
        if allowed:
            initial.add(name(normalized))
            if new_ok:
                refined.add(name(normalized))
    removed = sorted(initial - refined)
    expected = ['ABACDBC', 'ABACDCB', 'ABCADCD', 'ABCADDC']
    need(removed == expected and len(initial) == 26 and len(refined) == 22,
         'old elimination rows')
    old_certificate = FROZEN / 'audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/transfer.json'
    old = json.loads(old_certificate.read_text())
    case = next(c for c in old['kempe_cases'] if c['extra_edges'] == []
                and c['catalogue_mask'] == 319)
    old_live = {r['row'] for r in case['survivors']}
    need(refined == old_live, 'paper refinement already in old finite fixed point')
    need(all(len(x) == 4 ** 7 for x in (
        dense_proper, dense_lifts, dense_initial, dense_refined)), 'complete dense grid')
    need(sum(dense_initial) == 624 and sum(dense_refined) == 528,
         'labelled row counts including all zero slots')
    return {'complete_7pin_assignments_checked': 4 ** 7,
            'initial_canonical_rows': sorted(initial),
            'paper_refined_rows': sorted(refined), 'removed_rows': removed,
            'is_new_finite_exclusion': False,
            'matches_frozen_old_fixed_point': True,
            'dense_grid': {'pins': ['z', 's', 'v', 'w', 't', 'p', 'q'],
                           'shape': [4] * 7,
                           'index_order': 'lexicographic product(range(4), repeat=7)',
                           'proper_skeleton': dense_proper,
                           'all_r_lifts': dense_lifts,
                           'initial_upper_fibre': dense_initial,
                           'paper_refined_upper_fibre': dense_refined,
                           'zero_slots_retained': True}}


def calculate():
    base = json.loads((ROOT / 'BASE.json').read_text())
    need(base['head'] == 'e98a1cc1afd9a428600dcf4027d8138078c01650', 'BASE head')
    seal = {r['path']: r['sha256'] for r in base['authority_files']}
    inputs = []
    for rel in AUTHORITY:
        digest = sha256((FROZEN / rel).read_bytes()).hexdigest()
        need(seal[rel] == digest, 'authority drift: ' + rel)
        inputs.append({'path': rel, 'sha256': digest})
    return {'status': 'PASS; finite algebra/control only; source numerical coverage not triggered',
            'base': base['head'], 'inputs': inputs,
            'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
            'local_missing_set_algebra': fibre_algebra(),
            'quotient_control': quotient_control(),
            'old_complete_u_paper_lift': old_full_u_screen(),
            'actual_source_controls': 0,
            'source_nonemptiness': 'paper theorem from original cofacial face and global minimum',
            'joint_even_complement_positivity': 'OPEN'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'complete-certificate.json')
    args = parser.parse_args()
    result = json.loads(json.dumps(calculate()))
    if args.check:
        need(json.loads(args.certificate.read_text()) == result, 'certificate differs from exact recomputation')
    else:
        with args.certificate.open('x') as handle:
            json.dump(result, handle, indent=2)
            handle.write('\n')
    control = result['quotient_control']
    print(json.dumps({'ok': True, 'full_quotient_colorings': control['complete_coloring_count'],
                      'empty_z_fibres': control['empty_z_fibres'],
                      'compatible_nonempty_z_fibres': control['compatible_nonempty_z_fibres'],
                      'incompatible_nonempty_z_fibres': control['incompatible_nonempty_z_fibres'],
                      'all_7pin_assignments': 4 ** 7,
                      'old_refined_rows': 22, 'actual_sources': 0}, sort_keys=True))


if __name__ == '__main__':
    main()
