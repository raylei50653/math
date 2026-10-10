#!/usr/bin/env python3
"""HIGH1 fixed-domain semantic controls; never a finite source validator."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = "dc8e9aa7d6fccb51f63d30aa3f9c132296d44744"
INPUT_INDEX_SHA256 = "8295f37e0b931e49cce54961439903d2b515c2909123cad7f9c96f0e0b13e5a8"
COL = set(range(4))
Q = [(0, 1, 2, 1, 2), (0, 1, 2, 0, 2), (0, 1, 2, 0, 1),
     (0, 1, 0, 2, 1), (0, 1, 0, 1, 2)]
ROWS = [b for b in it.product(range(4), repeat=5)
        if all(b[i] != b[(i + 1) % 5] for i in range(5))]
EDGE = [frozenset((i, (i + 1) % 5)) for i in range(5)]


def encode(x):
    return (json.dumps(x, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def digest(b):
    return hashlib.sha256(b).hexdigest()


def need(ok, message):
    if not ok:
        raise ValueError(message)


def inputs(path):
    need(digest(path.read_bytes()) == INPUT_INDEX_SHA256, 'frozen input index binding')
    doc = json.loads(path.read_bytes())
    need(doc['BASE'] == BASE and doc['HEAD'] == BASE, 'input identity')
    need(len(doc['inputs']) == 34 and doc['pins_verified'] == 9, 'input coverage')
    need(len({x['frozen'] for x in doc['inputs']}) == 34, 'duplicate inputs')
    pinned = json.loads((HERE / 'frozen/current/audits/2026-10-10-n45-low2-supervision/high1-task-pins.json').read_bytes())
    lookup = {(x['layer'], x.get('path')): x for x in doc['inputs']}
    for p in pinned['pins']:
        need(lookup[('current', p['path'])]['sha256'] == p['sha256'], 'task pin mismatch')
    need(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == BASE, 'HEAD drift')
    for rec in doc['inputs']:
        need(digest((HERE / rec['frozen']).read_bytes()) == rec['sha256'], 'frozen input drift: ' + rec['frozen'])
        if rec['layer'] == 'BASE':
            live = subprocess.check_output(['git', 'show', BASE + ':' + rec['path']], cwd=ROOT)
        elif rec['layer'] == 'current':
            live = (ROOT / rec['path']).read_bytes()
        else:
            need(rec['layer'] == 'external', 'unknown input layer')
            continue
        need(digest(live) == rec['sha256'], 'original input drift: ' + rec['path'])
    return doc


def canonical(b):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in b)


def transform(b, shift, sign):
    answer = [None] * 5
    for i, c in enumerate(b):
        answer[(shift + sign * i) % 5] = c
    return tuple(answer)


def normalize(b):
    m = next(i for i in range(5) if b.count(b[i]) == 1)
    shift = (4 - m) % 5
    moved = transform(b, shift, 1)
    names = {c: Q[4][i] for i, c in enumerate(moved)}
    names[next(iter(COL - set(moved)))] = 3
    need(tuple(names[c] for c in moved) == Q[4], 'whole-row normalization')
    return shift, names


def sector_mapping():
    entries = []
    for mask, missing in ((941, (0, 1, 3)), (933, (0, 1, 2, 3))):
        for shift, sign in it.product(range(5), (1, -1)):
            whole_missing = sorted((shift + sign * k) % 5 for k in missing)
            for old_beta in missing:
                beta = transform(Q[old_beta], shift, sign)
                norm_shift, cmap = normalize(beta)
                table = []
                for spokes in it.combinations(range(5), 2):
                    ns = sorted((i + norm_shift) % 5 for i in spokes)
                    if beta[spokes[0]] == beta[spokes[1]]:
                        status = 'not triggered'
                        result = 'X minimality excludes duplicate beta spoke colors'
                        j = []
                    else:
                        c = next(iter(set(beta) - {beta[i] for i in spokes}))
                        j = [i for i in range(5) if beta[i] == c]
                        status = 'triggered and holds'
                        key = tuple(ns)
                        if key in ((0, 1), (1, 2), (2, 3)):
                            result = 'BASE arbitrary-size K5 exclusion; both orders covered'
                        elif key in ((3, 4), (0, 4)):
                            result = 'BASE split-support all-row formula; G restore query still separate'
                        elif key in ((1, 4), (2, 4)):
                            result = 'BASE pA/pB extension of X; both C regions retained; G restore separate'
                        else:
                            need(key == (0, 3), 'unexpected spoke orbit')
                            result = 'BASE sector theorem excludes (2,1) region placement'
                    table.append(dict(spokes=spokes, normalized_spokes=ns,
                                      retained_r_spoke_candidates=j, status=status, conclusion=result))
                entries.append(dict(source_mask=mask, whole_D5=[shift, sign],
                                    original_beta_singleton=old_beta, beta=beta,
                                    missing_singletons=whole_missing,
                                    normalize_whole_D5=[norm_shift, 1],
                                    normalize_whole_S4=[cmap[i] for i in range(4)],
                                    table=table, source_instantiated=False))
    need(len(entries) == 70, '933 q2 coverage')
    return entries


def topological_schema():
    adjacent, disjoint = [], []
    for p, q in it.permutations(range(5), 2):
        common = EDGE[p] & EDGE[q]
        complement = set(range(5)) - {p, q}
        arcs = [set((start + k) % 5 for k in range(length))
                for start in range(5) for length in (2, 3, 4, 5)]
        allowed = sorted({tuple(sorted(a)) for a in arcs if a <= complement})
        if common:
            v = next(iter(common))
            for rs, ss in it.product(it.combinations(range(5), 2), repeat=2):
                r_edge = next(i for i in rs if i != v)
                s_edge = next(i for i in ss if i != v)
                # P,Q are unchanged connected component bags, O is B minus v.
                witnesses = [['P', 'r'], ['P', 's'], ['P', 'b' + str(v)],
                             ['Q', 'r'], ['Q', 's'], ['Q', 'b' + str(v)],
                             ['O', 'r', r_edge], ['O', 's', s_edge],
                             ['O', 'b' + str(v), (v + 1) % 5]]
                o = set(range(5)) - {v}
                need(r_edge in o and s_edge in o and (v + 1) % 5 in o, 'K33 exterior adjacency')
                # The four vertices of O occur consecutively on the original B.
                need({(v + k) % 5 for k in range(1, 5)} == o, 'O connectivity')
                need(len(witnesses) == 9 and v in EDGE[p] and v in EDGE[q], 'K33 nine edges')
                adjacent.append(dict(P_edge=p, Q_edge=q, common=v,
                                     original_r_spokes=rs, original_s_spokes=ss,
                                     nine_adjacencies=witnesses, kind='schema, not source'))
        else:
            need(len(allowed) == 1 and len(allowed[0]) == 2, 'unique U arc')
            support = sorted(set().union(*(EDGE[i] for i in allowed[0])))
            need(len(support) == 3, 'three-point U support')
            disjoint.append(dict(P_edge=p, Q_edge=q, U_shield_edges=allowed[0],
                                 U_actual_support=support, kind='metadata, not source'))
    need(len(adjacent) == 1000 and len(disjoint) == 10, 'support partition coverage')
    return dict(K33=adjacent, disjoint_supports=disjoint)


def unary_stabilizers():
    records, missing_checks = [], []
    for start in range(5):
        support = sorted((start + i) % 5 for i in range(3))
        for b in ROWS:
            allowed_F = []
            for candidate in [set()] + [{c} for c in range(4)]:
                stable = True
                for perm in it.permutations(range(4)):
                    if all(perm[b[i]] == b[i] for i in support):
                        stable &= {perm[c] for c in candidate} == candidate
                if stable:
                    allowed_F.append(sorted(candidate))
            unused = sorted(COL - set(b))
            if len(set(b)) == 3 and len({b[i] for i in support}) < 3:
                d = unused[0]
                need(all(d not in f for f in allowed_F), 'unused-color unary escape')
            records.append(dict(support=support, boundary=b,
                                stabilizer_invariant_F_with_capacity_one=allowed_F))
        possible = [i for i, q in enumerate(Q) if len({q[j] for j in support}) == 3]
        need(possible == support, 'singleton positions on a consecutive triple')
        for mask, bad in ((941, {0, 1, 3}), (933, {0, 1, 2, 3})):
            for shift, sign in it.product(range(5), (1, -1)):
                transported = {(shift + sign * i) % 5 for i in bad}
                need(not transported <= set(possible), 'source missing-position contradiction')
                missing_checks.append(dict(source_mask=mask, whole_D5=[shift, sign],
                                          U_support=support, permitted_rejection_positions=possible,
                                          source_rejection_positions=sorted(transported),
                                          forced_accepted_position=min(transported - set(possible))))
    return dict(stabilizers=records, missing_position_checks=missing_checks)


def colorings(vertices, edges, attachments, b):
    vs = sorted(vertices)
    neighbors = {v: set() for v in vs}
    for u, v in edges:
        if u in neighbors and v in neighbors:
            neighbors[u].add(v)
            neighbors[v].add(u)
    lists = {v: sorted(COL - {b[i] for i in attachments.get(v, ())}) for v in vs}
    result, chosen = [], {}

    def go(n):
        if n == len(vs):
            result.append(tuple(chosen[v] for v in vs))
            return
        v = vs[n]
        for c in lists[v]:
            if all(chosen.get(w) != c for w in neighbors[v]):
                chosen[v] = c
                go(n + 1)
                del chosen[v]
    go(0)
    return result


def calibration():
    # This is one prescribed algebra graph. No disk/minimality/Sigma source claim.
    r, s, free = 5, 6, 11
    pv, qv, uv = [7, 8], [9], [10]
    ce = [(5, 7), (5, 8), (5, 9), (7, 8)]
    contacts = (7, 9)
    c_vertices = [5, 7, 8, 9]
    att = {5: [2], 6: [1, 4], 7: [1], 8: [1, 2], 9: [3, 4], 10: [4, 0, 1], 11: []}
    xe = ce + [(6, 7), (6, 9), (6, 10)]
    vertices = [5, 6, 7, 8, 9, 10]
    canonical_rows = sorted({canonical(b) for b in ROWS})
    need(len(canonical_rows) == 10, 'ten-row domain')
    saved, all_rows, marginal_failures, blocked = [], [], [], []
    for b in ROWS:
        cs = colorings(c_vertices, ce, att, b)
        us = colorings(uv, [], att, b)
        p_assignments = colorings(pv, [(7, 8)], att, b)
        q_assignments = colorings(qv, [], att, b)
        pq_join = set()
        for c in COL - {b[2]}:
            for fp, fq in it.product(p_assignments, q_assignments):
                # Shared P port 7 and shared Q port 9 each use one value.
                if all(x != c for x in fp) and fq[0] != c:
                    pq_join.add((c, *fp, fq[0]))
        need(pq_join == set(cs), 'r-pinned P/Q full-lift union')
        joined = set()
        queries = []
        for a in range(4):
            for c in range(4):
                fc = [f for f in cs if f[0] == c and f[1] != a and f[3] != a]
                fu = [f for f in us if f[0] != a]
                full = []
                if a not in {b[1], b[4]}:
                    for f, g in it.product(fc, fu):
                        full.append((c, a, f[1], f[2], f[3], g[0]))
                joined.update(full)
                queries.append(dict(s_pin=a, r_pin=c, C_full=fc, U_full=fu,
                                    X_full=full, G_full=[f for f in full if c != b[3]]))
        direct = set(colorings(vertices, xe, att, b))
        g_att = dict(att)
        g_att[r] = [2, 3]
        gd = set(colorings(vertices, xe, g_att, b))
        need(joined == direct, 'X whole-graph full lifts')
        need({f for f in joined if f[0] != b[3]} == gd, 'G restored-spoke full lifts')
        # A retained original isolated vertex contributes a free factor in both graphs.
        direct_free = set(colorings(vertices + [free], xe, att, b))
        need({(*f, c) for f in direct for c in range(4)} == direct_free, 'free isolated factor')
        tuples = sorted({(f[1], f[3]) for f in cs})
        marg = [set(t[i] for t in tuples) for i in range(2)]
        for a in range(4):
            full_query = any(all(x != a for x in t) for t in tuples)
            marginal_query = all(any(x != a for x in m) for m in marg)
            if marginal_query and not full_query:
                marginal_failures.append(dict(boundary=b, s_query=a, tuples=tuples,
                                              marginal_product_would_accept=True))
        if direct and not gd:
            blocked.append(dict(boundary=b, X_full=sorted(direct), G_full=[],
                                all_X_r_colors=sorted({f[0] for f in direct}), lost_spoke_color=b[3]))
        record = dict(boundary=b, C_vertices=c_vertices, C_ordered_contacts=contacts,
                      C_tuples=tuples,
                      C_ambient_fibres=[dict(tuple=t, r_pin=c,
                                            full=[f for f in cs if (f[1], f[3]) == t and f[0] == c])
                                        for t in it.product(range(4), repeat=2) for c in range(4)],
                      U_ambient_fibres=[dict(contact_color=c, full=[f for f in us if f[0] == c]) for c in range(4)],
                      all_16_root_queries=queries, X_full=sorted(direct), G_full=sorted(gd),
                      free_vertex=free, free_factor_colors=list(range(4)))
        if tuple(b) in canonical_rows:
            saved.append(record)
        all_rows.append(dict(boundary=b, X_count=len(direct), G_count=len(gd),
                             free_X_count=len(direct_free), full_record_sha256=digest(encode(record))))
    return dict(kind='one fixed relation calibration; not a HIGH1 source',
                edges_X=xe, attachments_X=att, restored_edge=[r, 3],
                P_vertices=pv, Q_vertices=qv, U_vertices=uv,
                P_r_ordered_contacts=[7, 8], P_s_ordered_contacts=[7],
                Q_r_ordered_contacts=[9], Q_s_ordered_contacts=[9], U_s_ordered_contacts=[10],
                rotation='not supplied; no disk claim',
                ten_canonical_full_records=saved, all_240_rows=all_rows,
                marginal_counterexamples=marginal_failures[:1],
                restoring_edge_blocks_all_X_lifts=blocked[:1],
                source_prerequisites='not established or tested')


def result(index):
    return dict(task='N45-S-HIGH1', BASE=BASE, input_index_sha256=digest(index.read_bytes()),
                inputs=inputs(index), controls=[
                    dict(name='complete same-source relation toy', status='triggered and holds', scope='calibration only'),
                    dict(name='C5 support/spoke K33 schemas', status='triggered and holds', scope='finite metadata only'),
                    dict(name='capacity-one unary stabilizer arithmetic', status='triggered and holds', scope='240 labeled rows'),
                    dict(name='all source beta/D5/spoke mappings', status='triggered and holds', scope='70 labeled tasks, 933 q2 included'),
                    dict(name='finite HIGH1 source', status='not triggered', scope='not established; not executed; trigger count not defined')],
                theorem_mapping=sector_mapping(), topology=topological_schema(),
                unary_arithmetic=unary_stabilizers(), relations=calibration(),
                evidence=dict(paper='candidate only; REPORT and claims.json',
                              arbitrary_size_proof_checked_by_python=False,
                              finite_source_established=False, source_trigger_count=None,
                              new_Lean=False, broader_N2_E='OPEN'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    parser.add_argument('--input-index', type=Path, default=HERE / 'inputs.json')
    args = parser.parse_args()
    stage = 'input validation / fixed-domain reconstruction'
    try:
        payload = encode(result(args.input_index))
        if args.check:
            stage = 'certificate byte comparison'
            need(args.certificate.read_bytes() == payload, 'certificate bytes differ')
        else:
            stage = 'exclusive certificate create'
            with args.certificate.open('xb') as f:
                f.write(payload)
        print(json.dumps(dict(status='PASS: artifact controls only', stage=stage,
                              certificate_sha256=digest(payload), bytes=len(payload),
                              finite_HIGH1_source='not established / not executed / no trigger count'), sort_keys=True))
        return 0
    except (ValueError, KeyError, OSError, TypeError) as error:
        print(json.dumps(dict(status='REJECT', stage=stage, reason=str(error)), sort_keys=True), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
