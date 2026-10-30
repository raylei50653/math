#!/usr/bin/env python3
"""Finite same-source controls for parity-free matching and five-leaf repair.

No 4CT oracle; all matchings, empty families, original edge IDs and literal
terminal order are retained. See docs/c5_parity_shared_cut_continuation.md.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import random

import c5_equivalent_forms_check as forms
import c5_dual_path_surgery as surgery
import four_color_counts_face as face
import four_color_shared_cut_obstruction as shared

ROOT = Path(__file__).resolve().parents[1]
PAIRS = tuple(combinations(range(5), 2))
STAR = tuple(p for p in PAIRS if (p[1] - p[0]) not in (1, 4))
TARGET = ((2, 3), (0, 1), (0, 4))


def components(edges, edge_ids, vertices=()):
    adj = {v: [] for v in vertices}
    for e in sorted(edge_ids):
        u, v = edges[e]
        adj.setdefault(u, []).append((v, e))
        adj.setdefault(v, []).append((u, e))
    unseen, out = set(adj), []
    while unseen:
        seed = min(unseen)
        vs, es, queue = {seed}, set(), [seed]
        for v in queue:
            for w, e in adj[v]:
                es.add(e)
                if w not in vs:
                    vs.add(w)
                    queue.append(w)
        unseen -= vs
        ends = sorted(v for v in vs if len(adj[v]) == 1)
        out.append(dict(vertices=sorted(vs), edges=sorted(es), ends=ends,
                        cycle=bool(es) and all(len(adj[v]) == 2 for v in vs)))
    return out


def matchings(edges, n, exposed):
    allowed = set(range(n + 5)) - {n + i for i in exposed}
    incident = {v: [] for v in allowed}
    for e, (u, v) in enumerate(edges):
        if u in allowed and v in allowed:
            incident[u].append((v, e))
            incident[v].append((u, e))
    out = []

    def visit(free, chosen):
        if not free:
            out.append(frozenset(chosen))
            return
        v = min(free, key=lambda z: (sum(w in free for w, _ in incident[z]), z))
        for w, e in incident[v]:
            if w in free:
                visit(free - {v, w}, chosen + [e])
    visit(allowed, [])
    return sorted(out, key=lambda m: tuple(sorted(m)))


def word(edges, n, matching):
    return tuple(int(any(n + i in edges[e] for e in matching)) for i in range(5))


def odd(edges, matching):
    return sum(c['cycle'] and len(c['edges']) % 2 for c in
               components(edges, set(range(len(edges))) - matching))


def saturated(edges, n, matching):
    counts = Counter(v for e in matching for v in edges[e])
    return all(counts[v] == 1 for v in range(n)) and all(counts[n+i] <= 1 for i in range(5))


def parity_rewire(edges, n, old, new):
    """Compress actual retained segments, with parity, before adding connectors."""
    cut = new - old
    connectors = old - new
    retained = set(range(len(edges))) - old - cut
    pieces = components(edges, retained, range(n + 5))
    links, lengths, records = [], [], []
    untouched_odd = 0
    for c in pieces:
        if c['cycle']:
            untouched_odd += len(c['edges']) % 2
            records.append(dict(kind='retained_cycle', **c, parity=len(c['edges']) % 2))
        elif c['edges']:
            assert len(c['ends']) == 2
            links.append(tuple(c['ends']))
            lengths.append(len(c['edges']) % 2)
            records.append(dict(kind='retained_segment', **c, parity=len(c['edges']) % 2))
        else:
            records.append(dict(kind='isolated_vertex', **c, parity=0))
    for e in sorted(connectors):
        links.append(edges[e])
        lengths.append(1)
    compressed = components(links, range(len(links)))
    predicted = untouched_odd + sum(sum(lengths[e] for e in c['edges']) % 2
                                   for c in compressed if c['cycle'])
    assert predicted == odd(edges, new)
    return dict(cut_edges=sorted(cut), connector_edges=sorted(connectors),
                retained_pieces=records, compressed_links=links,
                link_parities=lengths, compressed_components=compressed,
                predicted_odd=predicted, actual_odd=odd(edges, new))


def oriented_faces(raw):
    candidates = [tuple(f) for f in raw]
    root = next(i for i, f in enumerate(candidates) if 0 in f and 1 in f)
    f = candidates[root]
    a = f.index(0)
    f = f[a:] + f[:a]
    if f[1] != 1:
        f = (f[0], f[2], f[1])
    found = {root: f}
    while len(found) < len(candidates):
        progress = False
        for i, tri in enumerate(candidates):
            if i in found:
                continue
            for done in list(found.values()):
                common = set(tri) & set(done)
                if len(common) != 2:
                    continue
                u, v = next((u, v) for u, v in zip(done, done[1:] + done[:1])
                            if {u, v} == common)
                w = next(z for z in tri if z not in common)
                found[i] = (v, u, w)
                progress = True
                break
        assert progress
    return [found[i] for i in range(len(candidates))]


def double_dimer(edges, families):
    z = {p: len(ms) for p, ms in families.items()}
    rows = []
    for a, b, c, d in combinations(range(5), 4):
        lhs = z[()] * z[(a, b, c, d)] + z[(a, c)] * z[(b, d)]
        rhs = z[(a, b)] * z[(c, d)] + z[(a, d)] * z[(b, c)]
        assert lhs == rhs
        rows.append(dict(ports=[a, b, c, d], lhs=lhs, rhs=rhs))
    return rows


def region_tests(edges, n, pm):
    good = {p: [m for m in ms if odd(edges, m) == 0] for p, ms in pm.items()}
    tests, batch_count, invalid_intermediates, rewires = [], 0, 0, 0
    representative_rewire = None
    for p in TARGET:
        if not pm[p]:
            continue
        minimum = min(odd(edges, m) for m in pm[p])
        minimizers = [m for m in pm[p] if odd(edges, m) == minimum]
        for m in minimizers:
            for j in STAR:
                for r in good[j]:
                    regions = components(edges, set(range(len(edges))) - (m & r), range(n + 5))
                    rows = []
                    old_cycles = [c for c in components(edges, set(range(len(edges))) - m)
                                  if c['cycle'] and len(c['edges']) % 2]
                    wm = word(edges, n, m)
                    for region in regions:
                        vs = set(region['vertices'])
                        t = frozenset(e for e in m ^ r if set(edges[e]) <= vs)
                        q = sum(set(c['vertices']) <= vs for c in old_cycles)
                        s = tuple(int(any(n+i in edges[e] for e in t)) for i in range(5))
                        # Each syndrome coordinate is literally the unique terminal edge.
                        assert sum(s) % 2 == 0
                        rows.append(dict(vertices=region['vertices'], toggle=sorted(t), gain=q, syndrome=s))
                    positive = [x for x in rows if x['gain']]
                    changed = sum(a != b for a, b in zip(wm, word(edges, n, r)))
                    assert len(positive) <= changed // 2
                    assert all(any(x['syndrome']) for x in positive)
                    for mask in range(1 << len(rows)):
                        new, gain, syndrome = m, 0, [0]*5
                        for i, row in enumerate(rows):
                            if mask >> i & 1:
                                new ^= frozenset(row['toggle'])
                                gain += row['gain']
                                syndrome = [a ^ b for a, b in zip(syndrome, row['syndrome'])]
                        assert saturated(edges, n, new)
                        assert odd(edges, new) == minimum - gain
                        assert word(edges, n, new) == tuple(a ^ b for a, b in zip(wm, syndrome))
                        if not any(syndrome):
                            assert sum(word(edges, n, new)) == 3
                            assert gain == 0  # m minimizes in its fixed-word family
                        elif sum(word(edges, n, new)) != 3:
                            invalid_intermediates += 1
                        batch_count += 1
                    # P2 also checks individual complete alternating paths, where
                    # an invalid exposed-leaf count is explicitly retained.
                    for comp in components(edges, m ^ r):
                        new = m ^ frozenset(comp['edges'])
                        proof = parity_rewire(edges, n, m, new)
                        rewires += 1
                        if representative_rewire is None and proof['actual_odd']:
                            representative_rewire = proof
                    tests.append(dict(exposed=list(p), matching=sorted(m), minimum_odd=minimum,
                                      reference_exposed=list(j), reference=sorted(r),
                                      regions=rows, positive_regions=len(positive),
                                      terminal_support_bound=changed//2))
    return dict(good_counts={''.join(map(str,p)):len(ms) for p, ms in good.items()},
                tests=tests, checked_batches=batch_count,
                non_two_exposed_intermediates=invalid_intermediates,
                parity_rewirings=rewires, representative_rewire=representative_rewire)


def tait_reference_cuts(edges, n, reference):
    labels = [1 if e in reference else 0 for e in range(len(edges))]
    selected = [e for e in range(len(edges)) if e not in reference]
    for strand in surgery.strands([edges[e] for e in selected]):
        assert len(strand['edges']) % 2 == 0
        for j, local_e in enumerate(strand['edges']):
            labels[selected[local_e]] = 2 + j % 2
    assert all({labels[e] for e, ends in enumerate(edges) if v in ends} == {1,2,3}
               for v in range(n))
    rows = []
    for pair in face.PAIRS:
        for strand in surgery.pair_strands(edges, labels, pair):
            if not strand['ends']:
                continue
            _, cut = surgery.ordered_surgery(edges, labels, n, pair, strand)
            normalized = dict(ends=[5 + v - n for v in strand['ends']])
            sides = shared.side_assignments(normalized, cut)
            assert sides['feasible_assignments']
            rows.append(dict(pair=pair,path_edges=strand['edges'],cut=cut,
                             feasible_assignments=sides['feasible_assignments']))
    return dict(reference=sorted(reference),edge_colors=labels,actions=rows)


def pole_audit(step):
    edges = tuple((i, 5+i) for i in range(5)) + tuple((i, (i+step)%5) for i in range(5))
    pm = {p: matchings(edges, 5, p) for p in PAIRS}
    full_families = {p: matchings(edges,5,p) for k in (0,2,4) for p in combinations(range(5),k)}
    condensation = []
    for a,b,c,d in combinations(range(5),4):
        z = {p:len(ms) for p,ms in full_families.items()}
        lhs = z[()] * z[(a,b,c,d)] + z[(a,c)] * z[(b,d)]
        rhs = z[(a,b)] * z[(c,d)] + z[(a,d)] * z[(b,c)]
        condensation.append(dict(ports=[a,b,c,d],lhs=lhs,rhs=rhs,holds=lhs==rhs))
    assert all(r['holds'] == (step == 1) for r in condensation)
    rows = {''.join(map(str,p)):[dict(edges=sorted(m), odd=odd(edges,m)) for m in ms]
            for p, ms in pm.items()}
    if step == 2:
        assert all(bool(pm[p]) == (p in STAR) for p in PAIRS)
        alpha, gamma = pm[(1,4)][0], pm[(0,2)][0]
        paths = components(edges, alpha ^ gamma)
        assert {tuple(v-5 for v in c['ends']) for c in paths} == {(0,2),(1,4)}
    else:
        alpha = gamma = None
        paths = []
        assert all(bool(pm[p]) == (p not in STAR) for p in PAIRS)
    actions = shared.audit_pole(edges, shared.cycle_states(edges))
    exposure_control = None
    for p, q in combinations(PAIRS, 2):
        for m in pm[p]:
            for r in pm[q]:
                for c in components(edges, m ^ r):
                    new = m ^ frozenset(c['edges'])
                    if sum(word(edges, 5, new)) != 3:
                        exposure_control = dict(source_exposed=p,reference_exposed=q,
                            source=sorted(m),reference=sorted(r),path=c,new_matching=sorted(new),
                            new_exposed=[i for i,x in enumerate(word(edges,5,new)) if not x],
                            rewire=parity_rewire(edges,5,m,new))
                        break
                if exposure_control: break
            if exposure_control: break
        if exposure_control: break
    if step == 1:
        assert exposure_control and exposure_control['new_exposed'] == []
    return dict(exposure_negative_control=exposure_control,condensation=condensation,edges=edges, complete_pm_families=rows,
                alpha=sorted(alpha) if alpha else None, gamma=sorted(gamma) if gamma else None,
                difference_components=paths, shared_cut_actions=len(actions),
                feasible_shared_cut_actions=sum(bool(a['sides']['feasible_assignments']) for a in actions))


def report():
    rng = random.Random(20261029)
    graphs = []
    for index in range(16):
        nv, raw = forms.random_near_triangulation(rng, 2 + index % 5)
        faces = oriented_faces(raw)
        primal_edges = sorted(forms.edges_of(faces))
        surgery.check_faces(nv, primal_edges, faces)
        edges = surgery.dual(primal_edges, faces)
        n = len(faces)
        families = {p: matchings(edges, n, p) for k in (0,2,4) for p in combinations(range(5),k)}
        pm = {p: families[p] for p in PAIRS}
        if pm[(1,4)] and (pm[(0,2)] or pm[(0,3)]):
            assert any(pm[p] for p in TARGET)
        regions = region_tests(edges, n, pm)
        reference_ids = {tuple(t['reference']) for t in regions['tests'] if t['minimum_odd']}
        actual_reference_cuts = [tait_reference_cuts(edges,n,frozenset(r)) for r in sorted(reference_ids)]
        graphs.append(dict(index=index, primal_vertices=nv, primal_edges=primal_edges, oriented_faces=faces,
                           network_internal_vertices=n, network_edges=edges,
                           complete_pm_families={''.join(map(str,p)):[sorted(m) for m in ms]
                                                 for p,ms in families.items()},
                           double_dimer=double_dimer(edges,families), region_checks=regions,
                           actual_reference_cuts=actual_reference_cuts))
    deps = ['scripts/c5_parity_shared_cut_verification.py','scripts/c5_equivalent_forms_check.py',
            'scripts/c5_dual_path_surgery.py','scripts/four_color_counts_face.py',
            'scripts/four_color_shared_cut_obstruction.py','scripts/four_color_counts_cone_verification.py',
            'scripts/ck_kempe_obstruction.py','scripts/c5_kempe_connectivity.py',
            'scripts/c5_adjacent_singleton_counts.py','scripts/c5_kempe_screen.py',
            'artifacts/c5_cells/cells.json']
    return dict(base='e1a90fea41702d7c98747716a5960198aecbecb3',seed=20261029,
                scope='16 deterministic plane controls; all PM families per graph; no general source coverage or 4CT claim.',
                pentagram=pole_audit(2),pentagon=pole_audit(1),graphs=graphs,
                totals=dict(graphs=len(graphs),double_dimer_identities=5*len(graphs),
                            region_reference_tests=sum(len(g['region_checks']['tests']) for g in graphs),
                            shared_cut_reference_actions=sum(len(r['actions']) for g in graphs for r in g['actual_reference_cuts']),
                            batches=sum(g['region_checks']['checked_batches'] for g in graphs),
                            parity_rewirings=sum(g['region_checks']['parity_rewirings'] for g in graphs),
                            non_two_exposed_intermediates=sum(g['region_checks']['non_two_exposed_intermediates'] for g in graphs),
                            odd_minimizer_reference_tests=sum(t['minimum_odd']>0 for g in graphs for t in g['region_checks']['tests'])),
                source_sha256={p:sha256((ROOT/p).read_bytes()).hexdigest() for p in deps})


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path)
    parser.add_argument('--check',type=Path)
    args=parser.parse_args()
    result=report()
    payload=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    if args.check:
        assert args.check.read_text()==payload,'certificate differs'
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(payload)
    print(json.dumps(result['totals'],sort_keys=True))


if __name__=='__main__':
    main()
