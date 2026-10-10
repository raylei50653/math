#!/usr/bin/env python3
"""Finite semantic/schema calibration. This does not decide the paper theorem."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
COL = set(range(4))
PERMS = list(it.permutations(range(4)))


def encoded(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(ok, stage, detail):
    if not ok:
        raise ValueError(stage + ': ' + detail)


def inputs(path):
    index = json.loads(path.read_text())
    require(index == json.loads((OUT / 'inputs-final.json').read_text()),
            'input validation', 'frozen-index binding')
    for e in index['inputs']:
        b = (OUT / e['frozen']).read_bytes()
        require(sha(b) == e['sha256'], 'input validation', e['frozen'])
        current = ((ROOT / e['path']).read_bytes() if e['origin'] == 'current' else
                   subprocess.check_output(['git', 'show', index['BASE'] + ':' + e['path']]))
        require(current == b, 'input validation', 'origin drift ' + e['path'])
    for e in index['pins']:
        require(sha((ROOT / e['path']).read_bytes()) == e['sha256'],
                'pin validation', e['path'])
    require(subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == index['BASE'],
            'input validation', 'HEAD drift')
    return {'frozen_inputs': len(index['inputs']), 'pins': len(index['pins']),
            'index_sha256': sha(path.read_bytes()), 'BASE': index['BASE']}


def proper_rows():
    return [t for t in it.product(range(4), repeat=5)
            if all(t[i] != t[(i + 1) % 5] for i in range(5))]


def canonical(t):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in t)


def toy():
    # One fixed named graph, no rotation/source claim. C=(r,p,q1,q2), U=(uL,uR).
    ce = [(0, 1), (0, 2), (0, 3), (2, 3)]
    ca = {0: [3], 1: [2, 3], 2: [4], 3: [4, 0]}
    ua = {0: [0, 1], 1: [1, 2]}
    full_vertices = ['r', 's', 'p', 'q1', 'q2', 'uL', 'uR', 'I']
    full_edges = [(0, 2), (0, 3), (0, 4), (3, 4), (1, 2), (1, 3),
                  (1, 5), (1, 6), (5, 6)]
    full_boundary = {0: [3], 1: [0], 2: [2, 3], 3: [4], 4: [4, 0],
                     5: [0, 1], 6: [1, 2]}
    evidence = []
    canonical_evidence = []
    total_x = total_g = 0
    restore_negative = None
    for row in proper_rows():
        c_assign = [t for t in it.product(range(4), repeat=4)
                    if all(t[i] != t[j] for i, j in ce) and
                    all(t[v] != row[b] for v, bs in ca.items() for b in bs)]
        u_assign = [t for t in it.product(range(4), repeat=2)
                    if t[0] != t[1] and
                    all(t[v] != row[b] for v, bs in ua.items() for b in bs)]
        cf = [[[list(t) for t in c_assign if (t[1], t[2]) == pair and t[0] == c]
               for c in range(4)] for pair in it.product(range(4), repeat=2)]
        uf = [[list(t) for t in u_assign if t == pair]
              for pair in it.product(range(4), repeat=2)]
        joined = set()
        for c, u, s, isolated in it.product(c_assign, u_assign, range(4), range(4)):
            if s != row[0] and s not in (c[1], c[2], u[0], u[1]):
                joined.add((c[0], s, c[1], c[2], c[3], u[0], u[1], isolated))
        # Independent direct whole-graph assignment check, including free I.
        direct_core = [t for t in it.product(range(4), repeat=7)
                       if all(t[i] != t[j] for i, j in full_edges) and
                       all(t[v] != row[b] for v, bs in full_boundary.items() for b in bs)]
        direct = {t + (i,) for t in direct_core for i in range(4)}
        require(joined == direct, 'full lift calibration', str(row))
        gx = {t for t in joined if t[0] != row[4]}
        gd = {t + (i,) for t in direct_core if t[0] != row[4] for i in range(4)}
        require(gx == gd, 'restore calibration', str(row))
        pins = []
        for r, s in it.product(range(4), repeat=2):
            xx = sorted(t for t in joined if t[:2] == (r, s))
            gg = sorted(t for t in gx if t[:2] == (r, s))
            require(xx == sorted(t for t in direct if t[:2] == (r, s)),
                    'pinned lift calibration', str((row, r, s)))
            pins.append({'r': r, 's': s, 'X': xx, 'G': gg})
            if xx and not gg and restore_negative is None:
                restore_negative = {'row': row, 'r': r, 's': s, 'lost_spoke_color': row[4],
                                    'X_lifts': xx, 'G_lifts': []}
        detail = {'row': row, 'C_64_ambient_fibres': cf, 'U_16_ambient_fibres': uf,
                  'all_16_root_pins': pins}
        evidence.append({'row': row, 'full_fibres_sha256': sha(encoded(detail)),
                         'X_lifts': len(joined), 'G_lifts': len(gx)})
        if canonical(row) == row:
            canonical_evidence.append(detail)
        total_x += len(joined)
        total_g += len(gx)
    require(restore_negative is not None, 'negative calibration', 'missing restored-edge counterquery')
    pair = {(2, 3), (3, 2)}
    forbidden = lambda rel: sorted(c for c in COL if all(c in t for t in rel))
    marginal_product = set(it.product({2, 3}, {2, 3}))
    require(forbidden(pair) == [2, 3] and forbidden(marginal_product) == [],
            'marginal counterexample', 'failed')
    return {'status': 'triggered and holds', 'scope': 'one fixed calibration graph; not a HIGH2 source',
            'vertices': full_vertices, 'X_internal_edges': full_edges,
            'X_boundary_attachments': full_boundary, 'G_added_edge': ['r', 'b4'],
            'rotation': None, 'source_prerequisites_verified': False,
            'rows': evidence, 'canonical_full_data': canonical_evidence,
            'X_full_lifts_including_I': total_x, 'G_full_lifts_including_I': total_g,
            'marginal_negative': {'status': 'counterexample', 'row': [0, 1, 0, 1, 2],
                                  'U_actual_relation': sorted(pair),
                                  'marginal_product': sorted(marginal_product),
                                  'actual_F': [2, 3], 'product_F': []},
            'restore_negative': {'status': 'counterexample', 'scope': 'pinned toy query',
                                 **restore_negative}}


def covers():
    cases = []
    for retained, spoke in it.product(range(3), repeat=2):
        A = COL - {spoke}
        for fc_size in [1, 2]:
            for fc in it.combinations(sorted(A), fc_size):
                for fu_size in [1, 2]:
                    for fu in it.combinations(sorted(A), fu_size):
                        fc, fu = set(fc), set(fu)
                        if fc | fu != A or not fc - fu or not fu - fc:
                            continue
                        if not fc <= {retained}:
                            continue
                        require(retained != spoke and fc == {retained} and fu == A - fc,
                                'cover arithmetic', 'role mismatch')
                        cases.append({'r_spoke': retained, 's_spoke': spoke,
                                      'FC': sorted(fc), 'FU': sorted(fu)})
    require(len(cases) == 6, 'cover arithmetic', 'wrong count')
    return {'status': 'triggered and holds', 'cases': cases}


def connected(bag, edges):
    if not bag:
        return False
    seen = {next(iter(bag))}
    while True:
        new = seen | {v for u, v in edges if u in seen and v in bag} | {
            u for u, v in edges if v in seen and u in bag}
        if new == seen:
            return seen == bag
        seen = new


def minor(bags, edges, pairs):
    require(all(connected(b, edges) for b in bags), 'minor schema', 'disconnected bag')
    require(all(not (a & b) for a, b in it.combinations(bags, 2)), 'minor schema', 'overlap')
    witnesses = []
    for i, j in pairs:
        es = sorted((a, b) for a, b in edges if
                    (a in bags[i] and b in bags[j]) or (b in bags[i] and a in bags[j]))
        require(bool(es), 'minor adjacency', str((i, j)))
        witnesses.append({'bags': [i, j], 'edges': es})
    return {'bags': [sorted(b) for b in bags], 'edges': sorted(edges), 'adjacencies': witnesses}


def k33_schemas():
    results = []
    b = ['b' + str(i) for i in range(5)]
    for v, s_spoke, r_spokes, u_attachment in it.product(
            range(5), range(5), it.combinations(range(5), 2), range(5)):
        if u_attachment == v:
            continue
        edges = {(b[i], b[(i + 1) % 5]) for i in range(5)}
        edges |= {('P', 'r'), ('P', 's'), ('P', b[v]),
                  ('Q', 'r'), ('Q', 's'), ('Q', b[v]),
                  ('s', b[s_spoke]), ('s', 'U'), ('U', b[u_attachment])}
        edges |= {('r', b[i]) for i in r_spokes}
        bags = [{'P'}, {'Q'}, set(b) - {b[v]}, {'r'}, {'s'}, {b[v]}]
        if s_spoke == v:
            bags[2].add('U')
        result = minor(bags, edges, list(it.product(range(3), range(3, 6))))
        result.update({'common_endpoint': v, 's_spoke': s_spoke,
                       'r_spokes': r_spokes, 'U_attachment': u_attachment,
                       'expanded_O': s_spoke == v})
        results.append(result)
    # Deliberately omit the exceptional s-U edge: actual missing adjacency.
    sample = next(t for t in results if t['expanded_O'])
    bad_edges = set(map(tuple, sample['edges'])) - {('s', 'U')}
    try:
        minor(list(map(set, sample['bags'])), bad_edges,
              list(it.product(range(3), range(3, 6))))
    except ValueError as e:
        negative = {'stage': str(e), 'status': 'counterexample', 'removed_edge': ['s', 'U']}
    else:
        raise ValueError('negative calibration: missing s-U edge not rejected')
    return {'status': 'triggered and holds', 'scope': 'position/adjacency schemas, not sources',
            'cases': results, 'negative': negative}


def arc_schemas():
    cases = []
    for a, bb, h in it.permutations(range(5), 3):
        marks = sorted([a, bb, h])
        arcs = {}
        for i, start in enumerate(marks):
            stop = marks[(i + 1) % 3]
            arc = []
            pos = start
            while pos != stop:
                arc.append('b' + str(pos))
                pos = (pos + 1) % 5
            arcs[start] = set(arc)
        # A fixed length-three bridge schema; includes a nonadjacent W0/W2 choice.
        for left, right in [(0, 1), (0, 2), (1, 3)]:
            edges = {('b' + str(i), 'b' + str((i + 1) % 5)) for i in range(5)}
            edges |= {('x0', 'x1'), ('x1', 'x2'), ('x2', 'x3'),
                      ('s', 'x0'), ('s', 'x3'), ('s', 'c'), ('c', 'b' + str(h))}
            for k in [left, right]:
                edges |= {('x' + str(k), 'b' + str(a)), ('x' + str(k), 'b' + str(bb))}
            A = {'x' + str(k) for k in range(left, right)}
            Ap = {'x' + str(right)}
            Z = ({'s', 'c'} | {'x' + str(k) for k in range(4)
                              if k < left or k > right} | arcs[h])
            result = minor([A, Ap, Z, arcs[a], arcs[bb]], edges,
                           list(it.combinations(range(5), 2)))
            result.update({'suppliers': [a, bb], 'external_endpoint': h,
                           'selected_W': [left, right]})
            cases.append(result)
    return {'status': 'triggered and holds', 'scope': 'K5 schemas only', 'cases': cases}


def support_and_palettes():
    support_cases = []
    palette_cases = []
    rows = proper_rows()
    for left in range(5):
        T = {(left + i) % 5 for i in range(3)}
        middle, right = (left + 1) % 5, (left + 2) % 5
        for row in rows:
            if len(set(row)) != 3:
                continue
            for required in it.combinations(sorted(set(row)), 2):
                options = [set(t) for n in range(4) for t in it.combinations(sorted(T), n)
                           if set(required) <= {row[i] for i in t}]
                surviving = [(sorted(a), sorted(b)) for a, b in it.product(options, repeat=2)
                             if len(a & b) < 2]
                if len({row[i] for i in T}) == 3:
                    require(not surviving, 'support schema', 'three-color shared supply survived')
                elif set(required) == {row[left], row[middle]}:
                    expected = {((left, middle), (middle, right)),
                                ((middle, right), (left, middle))}
                    expected = {(tuple(sorted(a)), tuple(sorted(b))) for a, b in expected}
                    require({(tuple(a), tuple(b)) for a, b in surviving} == expected,
                            'support schema', 'split mismatch')
                support_cases.append({'T': sorted(T), 'row': row, 'required': required,
                                      'two_W_survivors': surviving})
        for row in rows:
            pl = COL - {row[left], row[middle]}
            pr = COL - {row[middle], row[right]}
            relation = {(a, b) for a, b in it.product(pl, pr) if a != b}
            F = sorted(c for c in COL if all(c in t for t in relation))
            require(bool(relation), 'palette arithmetic', 'empty R')
            if len({row[i] for i in T}) == 3:
                require(F == [], 'palette arithmetic', 'three-color F not empty')
            else:
                require(set(F) == COL - {row[left], row[middle]},
                        'palette arithmetic', 'two-color F mismatch')
            palette_cases.append({'T_in_order': [left, middle, right], 'row': row,
                                  'left_palette': sorted(pl), 'right_palette': sorted(pr),
                                  'R_U': sorted(relation), 'F_U': F})
    # Exact factor algebra: pair R_U forces both full rooted palettes to equal F.
    factor_checks = 0
    subsets = [set(t) for n in range(1, 5) for t in it.combinations(range(4), n)]
    for pair in it.combinations(range(4), 2):
        target = {pair, tuple(reversed(pair))}
        for pl, pr in it.product(subsets, repeat=2):
            rel = {(a, b) for a, b in it.product(pl, pr) if a != b}
            if rel == target:
                require(pl == pr == set(pair), 'rooted palette algebra', 'spurious factor')
            factor_checks += 1
    return {'status': 'triggered and holds', 'scope': 'support and color arithmetic only',
            'support_cases': support_cases, 'all_row_palette_cases': palette_cases,
            'rooted_factor_checks': factor_checks}


def mapping_and_orbits():
    source = json.loads((OUT / 'frozen/base/artifacts/c5_single_spoke_two_two/observations.json').read_text())
    q = (0, 1, 0, 1, 2)
    rho = [3, 2, 1, 0, 4]
    pi = [1, 0, 2, 3]
    matches = []
    for T in [{0, 1, 2}, {1, 2, 3}]:
        middle = next(i for i in T if (i - 1) % 5 in T and (i + 1) % 5 in T)
        Csupport = set(range(5)) - {middle}
        for j, k in it.product(sorted(Csupport), repeat=2):
            if q[j] == q[k] or {q[j], q[k]} != {0, 1}:
                continue
            spoke, supports, bans = k, [sorted(Csupport), sorted(T)], [[q[j]], [2, 3]]
            reflected = spoke in [2, 3]
            if reflected:
                spoke = rho[spoke]
                supports = [sorted(rho[i] for i in s) for s in supports]
                bans = [sorted(pi[c] for c in f) for f in bans]
            recs = [r for r in source['records'] if r['spoke'] == spoke and
                    r['supports'] == supports and r['bans'] == bans]
            require(len(recs) == 1, 'BASE mapping', str((spoke, supports, bans)))
            r = recs[0]
            matches.append({'original_T': sorted(T), 'retained_r_spoke': j, 's_spoke': k,
                            'whole_reflection': reflected, 'record_id': r['id'],
                            'C_then_U_supports': supports, 'C_then_U_bans': bans,
                            'T4_status': r['T4_status'],
                            'query_scope': 'BASE p1/p2 extension of X; r projection still required for G'})
    orbit_checks = []
    for name, rejects in [('933', {0, 1, 2, 3}), ('941', {0, 1, 3})]:
        for direction, shift in it.product([1, -1], range(5)):
            image = {(direction * k + shift) % 5 for k in rejects}
            for left in range(5):
                T = {(left + k) % 5 for k in range(3)}
                require(not image <= set(range(5)) - T, 'orbit arithmetic', name)
                orbit_checks.append({'source': name, 'D5': [direction, shift],
                                     'all_rejects_including_933_q2': sorted(image),
                                     'T': sorted(T), 'at_least_one_acceptance_contradiction':
                                     sorted(image & T)})
    q_arithmetic = []
    for row in proper_rows():
        if len(set(row)) == 3:
            singleton = next(i for i, c in enumerate(row) if row.count(c) == 1)
            for left in range(5):
                T = {(left + k) % 5 for k in range(3)}
                require((len({row[i] for i in T}) == 3) == (singleton in T),
                        'singleton arithmetic', str(row))
                q_arithmetic.append([row, sorted(T), singleton])
    return {'status': 'triggered and holds', 'necessary_record_mapping': matches,
            'all_D5_source_shield_cases': orbit_checks,
            'all_literal_singleton_checks': q_arithmetic}


def compute(index):
    return {'task': 'N45-S-HIGH2', 'inputs': inputs(index), 'paper_status':
            'candidate under the complete frozen contract; pending independent adoption',
            'finite_HIGH2_source': {'status': 'not triggered', 'established': False,
                                    'executed': False, 'trigger_count': None},
            'new_Lean': False, 'general_N2_E': 'OPEN', 'toy': toy(),
            'cover_arithmetic': covers(), 'K33_schemas': k33_schemas(),
            'K5_frame_arc_schemas': arc_schemas(), 'support_palette_arithmetic': support_and_palettes(),
            'mapping_orbits': mapping_and_orbits()}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--check', action='store_true')
    p.add_argument('--certificate', type=Path, default=OUT / 'certificate.json')
    p.add_argument('--inputs', type=Path, default=OUT / 'inputs-final.json')
    a = p.parse_args()
    try:
        data = encoded(compute(a.inputs))
        if a.check:
            require(a.certificate.read_bytes() == data, 'certificate byte comparison', 'mismatch')
        else:
            try:
                with a.certificate.open('xb') as f:
                    f.write(data)
            except FileExistsError:
                raise ValueError('exclusive certificate create: already exists')
        print(json.dumps({'task': 'N45-S-HIGH2', 'mode': 'read-only replay' if a.check else 'generation',
                          'certificate_sha256': sha(data), 'bytes': len(data),
                          'finite_source': 'not triggered; not established or executed; no trigger count',
                          'paper': 'candidate; checker does not adjudicate', 'controls': 'triggered and holds'},
                         sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(str(e), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
