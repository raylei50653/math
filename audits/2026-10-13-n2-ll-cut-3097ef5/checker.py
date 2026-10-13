#!/usr/bin/env python3
"""Independent literal-profile, full-bit matrix, and contact-fibre verifier.

Does not import the generator, its DP, or the upstream matrix implementation.
This verifies finite necessary interfaces, never source realizability.
"""
import argparse
import copy
import hashlib
import itertools as it
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
Q = {0: (0, 1, 2, 1, 2), 1: (0, 1, 2, 0, 2), 3: (0, 1, 0, 2, 1)}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_frozen():
    base = json.loads((HERE / 'BASE.json').read_bytes())
    require(base['base'] == '3097ef5be241b7777451a5ef8a663f3987d6b866', 'wrong BASE')
    for record in base['files']:
        raw = (HERE / 'frozen' / record['path']).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == record['sha256'], 'frozen drift: ' + record['path'])
    dep = json.loads((HERE / 'paper/DEPENDENCIES.json').read_bytes())
    require(hashlib.sha256((HERE / dep['frozen_path']).read_bytes()).hexdigest() == dep['sha256'], 'Gallai dependency drift')
    return len(base['files']) + 1


def source_row(p, g, i):
    q = Q[i]
    rows = [a for a in range(4) if all(a != q[t] for t in g['T_r'])]
    cols = [a for a in range(4) if all(a != q[t] for t in g['T_s'])]
    data = {'row': i, 'q': list(q), 'rows': rows, 'columns': cols,
            'row_bounds': [p['P']['k'][1] - 1, p['P']['k'][1]],
            'column_bounds': [p['P']['k'][0] - 1, p['P']['k'][0]]}
    for c in ('P', 'Q'):
        d = p[c]
        data['S_' + c] = [[x, y] for x in rows for y in cols
                         if any(x == q[h] for h in d['W_r'])
                         or any(y == q[h] for h in d['W_s'])
                         or (d['shared'] and x == y)]
    return data


def check_row_source(actual, expected):
    for key, value in expected.items():
        require(actual[key] == value, 'source-derived ' + key + ' mismatch')


@lru_cache(None)
def full_bit_matrices(rows, cols, rb, cb, sp, sq):
    grid = tuple(it.product(rows, cols))
    zero = sum(1 << j for j, cell in enumerate(grid) if cell in sp)
    one = sum(1 << j for j, cell in enumerate(grid) if cell in sq)
    rm = [sum(1 << j for j, (x, _) in enumerate(grid) if x == a) for a in rows]
    cm = [sum(1 << j for j, (_, y) in enumerate(grid) if y == b) for b in cols]
    answers = []
    for bits in range(1 << len(grid)):
        if bits & zero or bits & one != one:
            continue
        if any(not rb[0] <= (bits & m).bit_count() <= rb[1] for m in rm):
            continue
        if any(not cb[0] <= (bits & m).bit_count() <= cb[1] for m in cm):
            continue
        answers.append(bits)
    return tuple(answers)


def validate_matrix_record(d):
    rows, cols = tuple(d['rows']), tuple(d['columns'])
    sp, sq = set(map(tuple, d['S_P'])), set(map(tuple, d['S_Q']))
    answers = full_bit_matrices(rows, cols, tuple(d['row_bounds']), tuple(d['column_bounds']),
                                tuple(sorted(sp)), tuple(sorted(sq)))
    require(len(answers) == d['count'], 'matrix count mismatch')
    require(bool(answers) == d['feasible'], 'matrix feasibility mismatch')
    require(sorted(sp & sq) == list(map(tuple, d['common_safe_cells'])), 'overlap mismatch')
    if answers:
        assignment = d['assignment']
        require(len(assignment) == len(rows) and all(len(r) == len(cols) for r in assignment), 'assignment dimensions')
        flat = [v for row in assignment for v in row]
        require(all(type(v) is int and v in (0, 1) for v in flat), 'not binary')
        require(sum(v << j for j, v in enumerate(flat)) in answers, 'invalid witness matrix')
        require(d['violated_cut'] is None, 'cut with feasible matrix')
    elif not sp & sq:
        check_cut(d)
    return len(answers)


def check_cut(d):
    rows, cols = d['rows'], d['columns']
    sp, sq = set(map(tuple, d['S_P'])), set(map(tuple, d['S_Q']))
    free = set(it.product(rows, cols)) - sp - sq
    rf = {x: sum(a == x for a, b in sq) for x in rows}
    cf = {y: sum(b == y for a, b in sq) for y in cols}
    al = {x: max(0, d['row_bounds'][0] - rf[x]) for x in rows}
    be = {x: d['row_bounds'][1] - rf[x] for x in rows}
    ga = {y: max(0, d['column_bounds'][0] - cf[y]) for y in cols}
    de = {y: d['column_bounds'][1] - cf[y] for y in cols}
    cut = d['violated_cut']
    require(cut is not None, 'infeasibility without readable cut')
    if cut['kind'] == 'forced_upper_exceeded':
        upper = (be if cut['axis'] == 'row' else de)[cut['color']]
        require(upper == cut['remaining_upper'] and upper < 0, 'wrong forced upper cut')
    else:
        r, t = set(cut['rows']), set(cut['columns'])
        require(r <= set(rows) and t <= set(cols), 'cut outside grid')
        if cut['kind'] == 'row_lower':
            lhs = sum(al[x] for x in r)
            rhs = sum(de[y] for y in t) + sum(x in r and y not in t for x, y in free)
        elif cut['kind'] == 'column_lower':
            lhs = sum(ga[y] for y in t)
            rhs = sum(be[x] for x in r) + sum(x not in r and y in t for x, y in free)
        else:
            raise ValueError('unknown cut')
        require((lhs, rhs) == (cut['lhs'], cut['rhs']) and lhs > rhs, 'cut inequality mismatch')


def geometry_key(g):
    return (tuple(g['P']['walk']), tuple(g['Q']['walk']), tuple(g['T_r']), tuple(g['T_s']))


def check_geometry(data):
    expect = set()
    for p in range(5):
        pw = tuple((p + j) % 5 for j in range(3))
        pe = {p, (p + 1) % 5}
        for n in (2, 3):
            for q in range(5):
                qw = tuple((q + j) % 5 for j in range(n + 1))
                qe = {(q + j) % 5 for j in range(n)}
                if pe & qe or (n == 2 and sorted(pe) >= sorted(qe)):
                    continue
                sites = set(range(5)) - set(pw[1:-1]) - set(qw[1:-1])
                for tr, ts in ((2, 0), (1, 1), (2, 1)) if n == 2 else ((1, 1),):
                    for a in it.combinations(sorted(sites), tr):
                        if tr == 2 and (a[1] - a[0]) % 5 not in (1, 4):
                            continue
                        for b in it.combinations(sorted(sites), ts):
                            expect.add((pw, qw, a, b))
    require({geometry_key(g) for g in data['geometries']} == expect, 'geometry coverage mismatch')
    require(len(expect) == data['geometry_count'] == 85, 'geometry count')
    for g in data['geometries']:
        require(g['t'] == [len(g['T_r']), len(g['T_s'])], 'spoke counts')
        for c in ('P', 'Q'):
            arc = g[c]
            require(arc['support'] == sorted(arc['walk']), 'support not actual arc')
            require(arc['interior'] == sorted(arc['walk'][1:-1]), 'wrong arc interior')
            require(arc['edges'] == sorted(arc['walk'][:-1]), 'wrong shield edges')


def independent_contacts(definition):
    """Choose shared count, then separate multisets for each owner class."""
    support = definition['support']; kr, ks = definition['k']
    wr, ws = set(definition['W_r']), set(definition['W_s'])
    choices = [()] + [(x,) for x in support] + [a for a in it.combinations(support, 2) if (a[1] - a[0]) % 5 in (1, 4)]
    ra = [a for a in choices if set(a) <= wr]
    sa = [a for a in choices if set(a) <= ws]
    ha = [a for a in choices if len(a) <= 1 and set(a) <= wr & ws]
    counts = Counter()
    for shared in range(1 if definition['shared'] else 0, min(kr, ks) + 1 if definition['shared'] else 1):
        for rr in it.combinations_with_replacement(ra, kr - shared):
            for ss in it.combinations_with_replacement(sa, ks - shared):
                for hh in it.combinations_with_replacement(ha, shared):
                    ur = set().union(*map(set, rr + hh))
                    us = set().union(*map(set, ss + hh))
                    if ur != wr or us != ws:
                        continue
                    if sum(bool(a) for a in rr + ss) + len(hh) < 2:
                        continue
                    pairs = [a for a in rr + ss if len(a) == 2]
                    if len(pairs) != len(set(pairs)):
                        continue
                    mask = sum(1 << next(i for i in range(5) if set(a) == {i, (i + 1) % 5}) for a in pairs)
                    counts[mask] += 1
    return counts


def check_contact_example(example, definition, pairmask):
    kr = ks = leaves = 0; wr = set(); ws = set(); shared = False; edges = []
    for index, c in enumerate(example):
        owners, a = c['owners'], set(c['B'])
        require(c['slot'] == index and owners in (['r'], ['s'], ['r', 's']), 'contact identity')
        require(a <= set(definition['support']) and len(a) <= 2, 'contact attachments')
        deg = 4 - len(owners) - len(a)
        require(deg == c['degree_in_C'] and deg >= 1, 'original contact degree')
        leaves += deg <= 2
        shared |= len(owners) == 2
        if 'r' in owners: kr += 1; wr |= a
        if 's' in owners: ks += 1; ws |= a
        if len(a) == 2:
            match = [i for i in range(5) if a == {i, (i + 1) % 5}]
            require(len(match) == 1, 'nonadjacent B attachments')
            edges.extend(match)
    require([kr, ks] == definition['k'] and sorted(wr) == definition['W_r'] and sorted(ws) == definition['W_s'], 'contact projection')
    require(shared == definition['shared'] and leaves >= 2, 'contact leaf/shared restriction')
    require(len(edges) == len(set(edges)) and sum(1 << e for e in edges) == pairmask, 'edge attachment injectivity')


def verify(data):
    check_geometry(data)
    gm = {g['id']: g for g in data['geometries']}
    for d in data['row_catalog'].values():
        validate_matrix_record(d)
    for d in data['cut_catalog'].values():
        p, row = d['example_profile'], d['example_row']
        check_row_source(row, source_row(p, gm[p['geometry']], row['row']))
        for c in ('P', 'Q'):
            for cell, reasons in row['fixed_sources'][c].items():
                x, y = map(int, cell.split(','))
                require([x, y] in row['S_' + c] and reasons, 'unjustified fixed cell')
                for reason in reasons:
                    if reason['mechanism'] == 'shared_contact_slack':
                        require(p[c]['shared'] and x == y, 'false shared source')
                    else:
                        v, h = reason['root'], reason['boundary']
                        require(h in p[c]['W_' + v] and Q[row['row']][h] == (x if v == 'r' else y), 'false attachment source')
        validate_matrix_record(row)
    contacts = {}
    for cid, c in data['contact_catalog'].items():
        counts = independent_contacts(c['definition'])
        require(dict(counts) == {g['pair_mask']: g['count'] for g in c['by_pair_mask']}, 'contact fibre cardinality')
        require(sum(counts.values()) == c['count'], 'contact fibre total')
        for group in c['by_pair_mask']:
            check_contact_example(group['example'], c['definition'], group['pair_mask'])
        contacts[cid] = counts
    seen = set(); interfaces = 0
    for p in data['profiles']:
        g = gm[p['geometry']]
        require(p['id'] not in seen, 'duplicate profile')
        seen.add(p['id'])
        for j in range(2):
            require(p['P']['k'][j] + p['Q']['k'][j] + g['t'][j] == 5, 'original root degree equation')
        for c in ('P', 'Q'):
            d = data['contact_catalog'][p[c]['contact_fibre']]['definition']
            require(d == {'support': g[c]['support'], **{k: p[c][k] for k in ('k', 'W_r', 'W_s', 'shared')}}, 'wrong contact preimage')
            for v, other in (('r', 1), ('s', 0)):
                if p[c]['k'][other] >= 2:
                    require(all(q[h] in {q[t] for t in g['T_' + v]}
                                for h in p[c]['W_' + v] for q in Q.values()), 'Z necessary condition')
        for i, rid in zip(Q, p['row_certificates'], strict=True):
            actual = data['row_catalog'][rid]
            check_row_source(actual, source_row(p, g, i))
            require(actual['feasible'], 'survivor has basic cut')
        cp, cq = (contacts[p[c]['contact_fibre']] for c in ('P', 'Q'))
        expected = sorted([a, b, ca * cb] for a, ca in cp.items() for b, cb in cq.items() if not a & b)
        require(expected == sorted(p['compatible_contact_pair_masks']), 'contact pair preimages')
        interfaces += sum(a[2] for a in expected)
    # Deliberately edit the mathematical fields, not just a checksum.
    p = data['profiles'][0]; expected = source_row(p, gm[p['geometry']], 0)
    negative = []
    for name in ('capacity_bound', 'fixed_cell'):
        bad = copy.deepcopy(data['row_catalog'][p['row_certificates'][0]])
        if name == 'capacity_bound':
            bad['row_bounds'][0] += 1
        else:
            cell = [bad['rows'][0], bad['columns'][0]]
            if cell in bad['S_P']: bad['S_P'].remove(cell)
            else: bad['S_P'].append(cell)
        try:
            check_row_source(bad, expected)
        except ValueError as error:
            negative.append({'mutation': name, 'status': 'rejected', 'reason': str(error)})
        else:
            raise ValueError('negative mutation escaped')
    require(interfaces == sum(s['full_contact_interfaces'] for s in data['summary'].values()), 'interface summary')
    require(len(seen) == sum(s['common_feasible'] for s in data['summary'].values()), 'profile summary')
    return {'profiles': len(seen), 'contact_interfaces': interfaces,
            'independent_matrix_cases': len(data['row_catalog']) + len(data['cut_catalog']),
            'contact_catalogues': len(contacts), 'negative_controls': negative,
            'target_source_status': 'not triggered', 'source_realizations': 0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--profiles', type=Path, default=HERE / 'profiles/profiles.json')
    parser.add_argument('--artifact', type=Path, default=HERE / 'verification/independent.json')
    args = parser.parse_args()
    frozen = check_frozen()
    raw = args.profiles.read_bytes()
    result = verify(json.loads(raw))
    result.update({'frozen_files': frozen, 'profile_sha256': hashlib.sha256(raw).hexdigest()})
    payload = (canonical(result) + '\n').encode()
    if args.check:
        require(args.artifact.read_bytes() == payload, 'independent artifact mismatch')
    else:
        with args.artifact.open('xb') as out: out.write(payload)
    print(payload.decode().strip())


if __name__ == '__main__':
    main()
