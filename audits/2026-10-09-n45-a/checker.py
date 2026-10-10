#!/usr/bin/env python3
"""Independent fixed-input N45-A audit. No upstream decision code is imported.

Only BASE's 54 E4C graphs are used. Generation exclusively creates a certificate;
--check recomputes and compares without writes. Arbitrary-size claims are paper.
"""
from __future__ import annotations
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
B = frozenset(range(5))
COL = frozenset(range(4))
FRAME = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in range(5))
SELECTED = (6, 4, 1)
T4 = frozenset((2, 5, 7, 8, 9))
POS = {0: 4, 1: 3, 3: 2, 4: 1, 6: 0}


def canonical_edges(edges):
    return tuple(sorted(tuple(sorted(e)) for e in edges))


def adjacency(vertices, edges):
    ns = {v: set() for v in vertices}
    for u, v in edges:
        assert u != v and u in ns and v in ns
        ns[u].add(v)
        ns[v].add(u)
    return ns


def effective_vertices(vertices, edges):
    ns = adjacency(vertices, edges)
    return tuple(v for v in vertices if v in B or ns[v])


def components(vertices, ns):
    todo = set(vertices)
    result = []
    while todo:
        found, stack = set(), [min(todo)]
        while stack:
            v = stack.pop()
            if v in found:
                continue
            found.add(v)
            stack.extend(sorted(ns[v] & todo - found, reverse=True))
        todo -= found
        result.append(tuple(sorted(found)))
    return result


def enumerate_lifts(vertices, edges, pins, all_lifts=False):
    """MRV search on original labeled edges, with one shared vertex coordinate."""
    ns = adjacency(vertices, edges)
    f = {v: c for v, c in pins.items() if v in ns}
    if any(f[u] == f[v] for u, v in edges if u in f and v in f):
        return []
    result = []

    def visit():
        remaining = [v for v in vertices if v not in f]
        if not remaining:
            result.append([f[v] for v in vertices])
            return not all_lifts
        candidates = []
        for v in remaining:
            allowed = COL - {f[w] for w in ns[v] if w in f}
            if not allowed:
                return False
            candidates.append((len(allowed), -len(ns[v]), v, allowed))
        _, _, v, allowed = min(candidates, key=lambda x: x[:3])
        for c in sorted(allowed):
            f[v] = c
            if visit():
                del f[v]
                return True
            del f[v]
        return False

    visit()
    return result


@lru_cache(maxsize=None)
def sigma_with_lifts(vertices, edges, rows):
    lifts = []
    mask = 0
    for i, beta in enumerate(rows):
        found = enumerate_lifts(vertices, edges, dict(enumerate(beta)))
        if found:
            mask |= 1 << i
        lifts.append(found[0] if found else None)
    return mask, lifts


def sigma(vertices, edges, rows):
    return sigma_with_lifts(tuple(vertices), canonical_edges(edges), rows)


def q_of(mask):
    return sorted(POS[i] for i in POS if not (mask >> i) & 1)


def epsilon(vertices, edges):
    ns = adjacency(vertices, edges)
    return sum(len(ns[v]) - 4 for v in vertices if v not in B and ns[v])


def proper_lift(vertices, edges, beta, lift):
    if lift is None or len(lift) != len(vertices):
        return False
    f = dict(zip(vertices, lift))
    return all(f[i] == beta[i] for i in B) and all(f[u] != f[v] for u, v in edges)


def face_check(vertices, edges, rotation):
    ns = adjacency(vertices, edges)
    rot = {int(v): list(ws) for v, ws in rotation.items()}
    assert set(rot) == set(vertices)
    assert all(len(ws) == len(set(ws)) and set(ws) == ns[v] for v, ws in rot.items())
    unseen = {(v, w) for v in vertices for w in ns[v]}
    faces = []
    while unseen:
        dart = first = min(unseen)
        face = []
        while True:
            assert dart in unseen
            unseen.remove(dart)
            a, b = dart
            face.append(a)
            ws = rot[b]
            dart = (b, ws[(ws.index(a) + 1) % len(ws)])
            if dart == first:
                break
        faces.append(face)
    assert len(vertices) - len(edges) + len(faces) == 2
    outer = [f for f in faces if len(f) == 5 and set(f) == B
             and canonical_edges(zip(f, f[1:] + f[:1])) == tuple(sorted(FRAME))]
    assert len(outer) == 1
    return {'faces': faces, 'C5_outer': outer[0], 'Euler': 2}


def piece_inventory(vertices, edges, roots):
    ns = adjacency(vertices, edges)
    pieces = []
    h = set(vertices) - B
    for vs in components(h - set(roots), ns):
        contacts = {str(r): sorted(ns[r] & set(vs)) for r in roots}
        owners = [r for r in roots if contacts[str(r)]]
        assert owners
        attachments = [list(e) for e in edges if set(e) & set(vs) and set(e) & B]
        order = sorted(set().union(*(set(contacts[str(r)]) for r in roots)))
        pieces.append({'id': 'P' + str(len(pieces)), 'vertices': list(vs),
                       'contacts': contacts, 'contact_order': order, 'owners': owners,
                       'incidences': [len(contacts[str(r)]) for r in roots],
                       'attachments': attachments,
                       'support': sorted(set().union(*(ns[v] & B for v in vs))),
                       'internal_edges': [list(e) for e in edges if set(e) <= set(vs)],
                       'one_sided': len(components(h - set(vs), ns)) == 1,
                       'kind': 'mixed' if len(owners) == 2 else 'unary'})
    return pieces


def minimize_same_sigma(vertices, edges, rows, target):
    """Reverse edge order, independently chosen; the returned Y need not be saved Y."""
    ee = set(edges)
    for e in sorted(ee - FRAME, reverse=True):
        candidate = ee - {e}
        if sigma(vertices, candidate, rows)[0] == target:
            ee = candidate
    yy = canonical_edges(ee)
    vv = effective_vertices(vertices, yy)
    assert sigma(vv, yy, rows)[0] == target
    ns = adjacency(vv, yy)
    assert all(len(ns[v]) >= 4 for v in vv if v not in B)
    critical = []
    for e in sorted(set(yy) - FRAME):
        mask, lifts = sigma(vv, set(yy) - {e}, rows)
        gained = [i for i in range(10) if (mask >> i) & 1 and not (target >> i) & 1]
        assert gained, e
        critical.append({'edge': list(e), 'gained': gained,
                         'full_lifts': {str(i): lifts[i] for i in gained}})
    original_ns = adjacency(vertices, edges)
    removed = [v for v in vertices if v not in B and original_ns[v] and v not in vv]
    terms = [sum(len(original_ns[v]) - 4 for v in removed),
             sum(len(original_ns[v]) - len(ns[v]) for v in vv if v not in B)]
    assert min(terms) >= 0
    assert sum(terms) == epsilon(vertices, edges) - epsilon(vv, yy)
    return {'vertices': list(vv), 'edges': list(yy), 'sigma': target,
            'epsilon': epsilon(vv, yy), 'epsilon_difference_terms': terms,
            'accepted_full_lifts': sigma(vv, yy, rows)[1],
            'critical_edges': critical}


def local_relations(vertices, edges, beta, roots, pieces):
    ns = adjacency(vertices, edges)
    records = []
    for p in pieces:
        pv = tuple(sorted(B | set(p['vertices'])))
        pe = tuple(e for e in edges if set(e) <= set(pv))
        all_lifts = enumerate_lifts(pv, pe, dict(enumerate(beta)), all_lifts=True)
        by_tuple = {}
        for lift in all_lifts:
            f = dict(zip(pv, lift))
            t = tuple(f[v] for v in p['contact_order'])
            by_tuple.setdefault(t, []).append([f[v] for v in p['vertices']])
        tuples = sorted(by_tuple)
        fibres = []
        accepted = set()
        for a, b in product(range(4), repeat=2):
            pins = dict(zip(roots, (a, b)))
            inds = []
            for j, t in enumerate(tuples):
                f = dict(zip(p['contact_order'], t))
                if all(f[v] != pins[r] for r in roots for v in p['contacts'][str(r)]):
                    inds.append(j)
            if inds:
                accepted.add((a, b))
            fibres.append({'pins': [a, b], 'tuple_indices': inds})
        records.append({'piece_id': p['id'], 'contact_order': p['contact_order'],
                        'tuples': [{'tuple': list(t), 'full_piece_lifts': sorted(by_tuple[t])}
                                   for t in tuples], 'fibres': fibres,
                        'accepted_pairs': [list(t) for t in sorted(accepted)]})
    er = {r: set(COL) - {beta[v] for v in ns[r] & B} for r in roots}
    unary_f = {r: [] for r in roots}
    for p, rel in zip(pieces, records):
        if p['kind'] == 'unary':
            r = p['owners'][0]
            k = roots.index(r)
            available = {t[k] for t in rel['accepted_pairs']}
            f = COL - available
            unary_f[r].append((p, f))
            er[r] &= available
    joint = {(a, b) for a in er[roots[0]] for b in er[roots[1]]}
    for p, rel in zip(pieces, records):
        if p['kind'] == 'mixed':
            joint &= {tuple(t) for t in rel['accepted_pairs']}
    return records, er, unary_f, joint


def capacity_rejected_row(vertices, edges, beta, roots, pieces, row_index):
    ns = adjacency(vertices, edges)
    rels, er, uf, joint = local_relations(vertices, edges, beta, roots, pieces)
    assert not joint
    # Independent whole-graph queries certify all 16 empty root fibres.
    whole = []
    for a, b in product(range(4), repeat=2):
        lifts = enumerate_lifts(vertices, edges, dict(enumerate(beta)) | dict(zip(roots, (a, b))))
        assert not lifts
        whole.append({'pins': [a, b], 'full_lift': None})
    columns = []
    for k, r in enumerate(roots):
        s = roots[1-k]
        if not er[s]:
            columns.append({'r': r, 's': s, 'status': 'not triggered', 'missing': ['E_s nonempty']})
            continue
        factors = [{beta[v]} for v in sorted(ns[r] & B)] + [f for p, f in uf[r]]
        d = sum(len(p['contacts'][str(r)]) - len(f) for p, f in uf[r])
        overlap = sum(len(f) for f in factors) - len(set().union(*factors))
        for b in sorted(er[s]):
            bars = []
            for p, rel in zip(pieces, rels):
                if p['kind'] != 'mixed':
                    continue
                ap = {tuple(t) for t in rel['accepted_pairs']}
                forbidden = {a for a in COL if ((a, b) if k == 0 else (b, a)) not in ap}
                bars.append((p, forbidden))
            v = set().union(*(g for p, g in bars))
            delta = sum(len(p['contacts'][str(r)]) - len(g) for p, g in bars)
            o = sum(len(g) for p, g in bars) - len(v)
            lam = len(v - er[r])
            terms = [d, overlap, delta, o, lam]
            assert er[r] <= v and min(terms) >= 0
            assert sum(terms) == len(ns[r]) - 4
            columns.append({'r': r, 's': s, 'b': b, 'status': 'triggered and holds',
                            'E_r': sorted(er[r]), 'E_s': sorted(er[s]), 'chi': 0,
                            'A': sorted(er[r]), 'terms_Du_Ou_delta_o_lambda': terms,
                            'degree_r_minus_4': len(ns[r]) - 4,
                            'mixed_forbidden_columns': [{'piece': p['id'], 'G': sorted(g)} for p, g in bars]})
    return {'row_index': row_index, 'beta': list(beta), 'local_complete_relations': rels,
            'whole_root_fibres': whole, 'capacity_columns': columns}


def build(root):
    inputs = json.loads((HERE / 'inputs.json').read_text())
    for p in inputs['BASE_inputs']:
        if p.get('exists') is False:
            continue
        raw = (root / p['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == p['sha256'], p['path']
    rows = tuple(tuple(t) for t in json.loads((root / 'artifacts/c5_cells/cells.json').read_text())['pattern_order'])
    masks = []
    for bits in range(32):
        q = [i for i in range(5) if (bits >> i) & 1]
        if len(q) <= 1 or (len(q) == 2 and (q[0] - q[1]) % 5 in (1, 4)):
            masks.append(q)
    assert len(masks) == 11 and len([q for q in masks if len(q) <= 1]) == 6
    spoke_records = []
    for k in range(4):
        for support in combinations(range(5), k):
            private = {str(i): [v for v in support if sum(rows[i][w] == rows[i][v] for w in support) == 1]
                       for i in SELECTED}
            never = [v for v in support if not any(v in x for x in private.values())]
            spoke_records.append({'support': list(support), 'private': private, 'never_private': never})
    assert [x['support'] for x in spoke_records if x['never_private']] == [[0, 2, 4], [1, 2, 4]]
    graphs = []
    counts = Counter()
    for path in sorted((root / 'artifacts/c5_excess_two_e4c/controls').glob('*.json')):
        g = json.loads(path.read_text())
        vertices = tuple(g['vertices'])
        edges = canonical_edges(g['edges'])
        assert len(edges) == len(set(edges)) and FRAME <= set(edges)
        assert {e for e in edges if set(e) <= B} == FRAME
        ns = adjacency(vertices, edges)
        roots = tuple(v for v in vertices if v not in B and len(ns[v]) == 5)
        assert len(roots) == 2 and roots[1] not in ns[roots[0]]
        assert all(len(ns[v]) == 4 for v in vertices if v not in B and v not in roots)
        assert epsilon(vertices, edges) == 2
        pieces = piece_inventory(vertices, edges, roots)
        m = sum(p['kind'] == 'mixed' for p in pieces)
        u = len(pieces) - m
        assert (m, u) == (g['m'], g['u'])
        mask, lifts = sigma(vertices, edges, rows)
        assert mask == g['sigma'] and all((mask >> i) & 1 for i in T4)
        counts['graphs'] += 1
        counts['N2_graphs'] += m == 2
        counts['precise_target_graphs'] += mask in (933, 941)
        counts['triple_critical_source_antecedent'] += all(not (mask >> i) & 1 for i in SELECTED)
        cut_records = []
        for e in sorted(set(edges) - FRAME):
            new_mask, new_lifts = sigma(vertices, set(edges) - {e}, rows)
            gained = [i for i in range(10) if (new_mask >> i) & 1 and not (mask >> i) & 1]
            assert gained
            cut_records.append({'edge': list(e), 'sigma': new_mask, 'gained': gained,
                                'full_lifts': {str(i): new_lifts[i] for i in gained}})
            counts['source_critical_edges'] += 1
        root_deletions = []
        for r in roots:
            vv = tuple(v for v in vertices if v != r)
            ee = tuple(e for e in edges if r not in e)
            sm, sl = sigma(vv, ee, rows)
            assert sm == 1023
            root_deletions.append({'absent': r, 'sigma': sm, 'vertices': list(vv), 'edges': list(ee), 'full_lifts': sl})
            counts['root_deletions'] += 1
        core_records = []
        for row in g['row_cores']:
            i = row['index']
            assert bool(row['cores']) == (not (mask >> i) & 1)
            for c in row['cores']:
                cv, ce = tuple(c['vertices']), canonical_edges(c['edges'])
                cm, cl = sigma(cv, ce, rows)
                assert cm == c['sigma'] and not (cm >> i) & 1
                cn = adjacency(cv, ce)
                assert all(len(cn[v]) >= 4 for v in cv if v not in B)
                assert [len(cn[r]) if r in cn else None for r in roots] == c['root_degrees']
                assert len(components(set(cv) - B, cn)) == 1
                for e in sorted(set(ce) - FRAME):
                    found = enumerate_lifts(cv, tuple(x for x in ce if x != e), dict(enumerate(rows[i])))
                    assert found
                for p in pieces:
                    kept = set(cv) & set(p['vertices'])
                    assert not kept or kept == set(p['vertices'])
                    if kept:
                        assert all(e in ce for e in edges if set(e) & kept)
                ds = c['root_degrees']
                omitted = set(edges) - set(ce)
                unit = None
                if ds in ([4, 5], [5, 4]):
                    r = roots[ds.index(4)]
                    missing_vertices = set(vertices) - set(cv)
                    if not missing_vertices:
                        assert len(omitted) == 1
                        e = next(iter(omitted))
                        assert r in e and bool(set(e) & B)
                        unit = {'kind': 'spoke', 'root': r, 'edge': list(e)}
                    else:
                        pp = [p for p in pieces if set(p['vertices']) == missing_vertices]
                        assert len(pp) == 1 and pp[0]['kind'] == 'unary'
                        assert pp[0]['owners'] == [r] and len(pp[0]['contacts'][str(r)]) == 1
                        assert omitted == {e for e in edges if set(e) & missing_vertices}
                        unit = {'kind': 'unary', 'root': r, 'piece_id': pp[0]['id'], 'vertices': pp[0]['vertices']}
                    assert all(set(p['vertices']) <= set(cv) for p in pieces if p['kind'] == 'mixed')
                    counts['core_45' if ds == [4, 5] else 'core_54'] += 1
                    counts['core_unit_' + unit['kind']] += 1
                    counts['N2_core_45_54'] += m == 2
                elif ds == [5, 5]:
                    assert set(ce) == set(edges) and cv == vertices
                    counts['core_55'] += 1
                else:
                    raise AssertionError(('unexpected saved core degrees', ds))
                counts['saved_core_occurrences'] += 1
                core_records.append({'row_index': i, 'vertices': list(cv), 'edges': list(ce),
                                     'sigma': cm, 'root_degrees': ds, 'unit': unit,
                                     'accepted_full_lifts': cl, 'scope': 'saved occurrence validated; no exhaustive core re-enumeration'})
        units = []
        for r in roots:
            units.extend({'kind': 'spoke', 'root': r, 'edge': [b, r]} for b in sorted(ns[r] & B))
        units.extend({'kind': 'unary', 'root': p['owners'][0], 'piece_id': p['id'], 'vertices': p['vertices']}
                     for p in pieces if p['kind'] == 'unary' and sum(p['incidences']) == 1)
        derivatives = []
        for unit in units:
            if unit['kind'] == 'spoke':
                xv = vertices
                xe = tuple(e for e in edges if e != tuple(sorted(unit['edge'])))
            else:
                deleted = set(unit['vertices'])
                xv = tuple(v for v in vertices if v not in deleted)
                xe = tuple(e for e in edges if not set(e) & deleted)
            xm, xl = sigma(xv, xe, rows)
            assert epsilon(xv, xe) == 1
            assert all((xm >> i) & 1 for i in T4)
            assert q_of(xm) in masks
            yy = minimize_same_sigma(xv, xe, rows, xm)
            assert yy['epsilon'] <= 1
            xns = adjacency(xv, xe)
            own_critical = all(sigma(xv, set(xe) - {e}, rows)[0] != xm for e in xe if e not in FRAME)
            derivatives.append({'unit': unit, 'vertices': list(xv), 'edges': list(xe),
                                'root_degrees': [len(xns[r]) for r in roots],
                                'sigma': xm, 'Q': q_of(xm), 'epsilon': 1,
                                'X_is_Sigma_critical': own_critical,
                                'accepted_full_lifts': xl, 'independent_Y': yy})
            counts['unit_derivatives'] += 1
            counts['X_noncritical'] += not own_critical
            counts['derivative_all_rows'] += xm == 1023
            counts['derivative_single_rejection'] += len(q_of(xm)) == 1
        capacity = []
        if m == 2:
            for i in range(10):
                if (mask >> i) & 1:
                    continue
                record = capacity_rejected_row(vertices, edges, rows[i], roots, pieces, i)
                capacity.append(record)
                counts['BC2_rejected_N2_rows'] += 1
                for col in record['capacity_columns']:
                    counts['BC2_' + col['status']] += 1
        raw_source = (root / g['source']).read_bytes()
        assert hashlib.sha256(raw_source).hexdigest() == g['source_sha256']
        graphs.append({'id': g['id'], 'input': path.relative_to(root).as_posix(),
                       'vertices': list(vertices), 'edges': list(edges), 'roots': list(roots),
                       'rotation': g['rotation'], 'topology': face_check(vertices, edges, g['rotation']),
                       'm': m, 'u': u, 'sigma': mask, 'Q': q_of(mask), 'pieces': pieces,
                       'accepted_full_lifts': lifts, 'critical_edge_deletions': cut_records,
                       'root_deletions': root_deletions, 'saved_cores_validated': core_records,
                       'unit_derivatives': derivatives, 'BC2_rejected_rows': capacity,
                       'target_status': 'not triggered',
                       'missing_target_premises': ['complete Sigma is not 933/941 or a D5 image', 'selected q0,q1,q3 are not all rejected']
                            + (['m is not 2'] if m != 2 else [])})
    assert counts['graphs'] == 54 and counts['N2_graphs'] == 19
    assert counts['core_45'] == 10 and counts['core_54'] == 2 and counts['core_55'] == 48
    assert counts['core_unit_spoke'] == 8 and counts['core_unit_unary'] == 4
    assert counts['N2_core_45_54'] == 0 and counts['precise_target_graphs'] == 0
    assert counts['unit_derivatives'] == 172
    assert counts['derivative_all_rows'] == 160 and counts['derivative_single_rejection'] == 12
    return {'schema': 'n45-a-independent-fixed-audit-v1', 'BASE': inputs['BASE'],
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'inputs_sha256': hashlib.sha256((HERE / 'inputs.json').read_bytes()).hexdigest(),
            'summary': dict(sorted(counts.items())), 'epsilon_1_permitted_Q_sets': masks,
            'private_spoke_controls': spoke_records, 'graphs': graphs,
            'not_run': ['new source search', 'all-core exhaustive enumeration', 'BC2 for derivatives',
                        'all-row N2 local relation reconstruction (J scope)', 'Lean build or axioms audit'],
            'evidence': 'finite Python; source realizability is only for these saved rotations; no new arbitrary-size exclusion'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root', type=Path, default=Path('/tmp/math-n45-a-20261009'))
    p.add_argument('--output', type=Path, default=HERE / 'certificate.json')
    p.add_argument('--check', action='store_true')
    a = p.parse_args()
    data = build(a.source_root)
    raw = (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()
    if a.check:
        assert a.output.read_bytes() == raw, 'independent certificate byte replay differs'
        mode = 'CHECK OK (read-only)'
    else:
        with a.output.open('xb') as f:
            f.write(raw)
        mode = 'GENERATED (exclusive-create)'
    print(mode, hashlib.sha256(raw).hexdigest(), len(raw), json.dumps(data['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
