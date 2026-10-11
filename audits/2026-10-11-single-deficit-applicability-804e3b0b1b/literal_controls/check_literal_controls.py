#!/usr/bin/env python3
"""Fixed literal controls; no graph search, no authoritative files written.

Generate once with --generate. Replay with --check [--seed 17].
All proper literal C5 rows and every complete lift are retained.
"""
import argparse
import itertools
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
B = tuple('b' + str(i) for i in range(5))
COLORS = (0, 1, 2, 3)
BETA = (0, 1, 0, 1, 2)


def edge(a, b):
    return tuple(sorted((a, b)))


BOUNDARY = tuple(sorted(edge(B[i], B[(i + 1) % 5]) for i in range(5)))


def graph(name, interior, internal, spokes, roots, contacts, pieces):
    es = tuple(sorted(set(BOUNDARY) | {edge(*e) for e in internal + spokes}))
    vs = B + tuple(interior)
    nb = {v: sorted(w if u == v else u for u, w in es if v in (u, w)) for v in vs}
    return dict(name=name, vertices=list(vs), boundary=list(B), edges=[list(e) for e in es],
                root_order=roots, literal_beta=list(BETA), color_frame=list(COLORS),
                ordered_contacts=contacts, pieces=pieces,
                rotation={v: nb[v] for v in vs},
                rotation_status='explicit combinatorial rotation; no disk embedding asserted')


def fixed_graphs():
    art = graph('ARTICULATION_M', ('s', 'r', 'p', 'u', 'v'),
                [('s', 'r'), ('r', 'p'), ('p', 's'), ('s', 'u'), ('u', 'v'), ('v', 's')],
                [('s', 'b4'), ('r', 'b3'), ('r', 'b4'), ('p', 'b3'), ('p', 'b4'),
                 ('u', 'b0'), ('u', 'b4'), ('v', 'b0'), ('v', 'b4')], ['r', 's'],
                dict(left=['r', 'p'], right=['u', 'v']),
                [dict(name='left', vertices=['r', 'p'], owner='s', attachments=['b3', 'b4']),
                 dict(name='right', vertices=['u', 'v'], owner='s', attachments=['b0', 'b4'])])
    result = [art]
    for long in (False, True):
        private = ['x', 'y'] if long else []
        cycle = ['r', 'x', 'a', 'y', 'c'] if long else ['r', 'a', 'c']
        internal = [('s', 'p'), ('p', 'r'), ('a', 'q'), ('q', 's')]
        internal += [(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))]
        spokes = [('s', 'b0'), ('s', 'b1'), ('s', 'b4'), ('p', 'b1'), ('p', 'b4'),
                  ('q', 'b0'), ('q', 'b4'), ('r', 'b1'), ('a', 'b0'), ('c', 'b0'), ('c', 'b1')]
        spokes += [(v, b) for v in private for b in ('b0', 'b1')]
        stem = 'LONG' if long else 'TRIANGLE'
        interior = ['s', 'p', 'r', 'a', 'c', 'q'] + private
        pieces = [dict(name='P', vertices=['p'], ownership='mixed',
                       r_contacts=['p'], s_contacts=['p'], actual_support=['b1', 'b4']),
                  dict(name='Q', vertices=['a', 'c', 'q'] + private, ownership='mixed',
                       r_contacts=(['x', 'c'] if long else ['a', 'c']),
                       s_contacts=['q'], actual_support=['b0', 'b1', 'b4'])]
        contacts = dict(s=['p', 'q'], r_P=['p'], r_Q=pieces[1]['r_contacts'])
        m = graph(stem + '_M', interior, internal, spokes, ['r', 's'], contacts, pieces)
        m['derivative_definition'] = 'X_test = G_test - r b2 = M_test; M_test is beta-minimal'
        m['C_definition'] = 'H_M - s; contacts ordered (p,q); leaf bridges p-r and a-q'
        result.append(m)
        g = graph(stem + '_G', interior, internal, spokes + [('r', 'b2')],
                  ['r', 's'], contacts, pieces)
        g['omitted_edge'] = ['b2', 'r']
        result.append(g)
    return result


def proper_rows():
    return [p for p in itertools.product(COLORS, repeat=5)
            if all(p[i] != p[(i + 1) % 5] for i in range(5))]


def normalize(row):
    renaming = {}
    return tuple(renaming.setdefault(c, len(renaming)) for c in row)


def neighbors(g, removed=()):
    es = set(map(tuple, g['edges'])) - set(map(tuple, removed))
    return {v: {w if u == v else u for u, w in es if v in (u, w)} for v in g['vertices']}


def lifts(g, row, removed=(), seed=None):
    nb = neighbors(g, removed)
    order = [v for v in g['vertices'] if v not in B]
    if seed is not None:
        random.Random(seed).shuffle(order)
    out, f = [], dict(zip(B, row))
    def visit(i):
        if i == len(order):
            out.append(tuple(f[v] for v in g['vertices']))
            return
        v = order[i]
        for col in COLORS:
            if all(f[w] != col for w in nb[v] if w in f):
                f[v] = col
                visit(i + 1)
                del f[v]
    visit(0)
    return sorted(out)


def components(vs, nb, deleted=None):
    todo = set(vs) - ({deleted} if deleted is not None else set())
    result = []
    while todo:
        seen, pending = set(), [min(todo)]
        while pending:
            v = pending.pop()
            if v in seen or v == deleted:
                continue
            seen.add(v)
            pending += list(nb[v] & todo - seen)
        todo -= seen
        result.append(sorted(seen))
    return sorted(result)


def blocks(vs, nb):
    times, low, stack, result = {}, {}, [], []
    def dfs(v, parent=None):
        times[v] = low[v] = len(times)
        for w in sorted(nb[v]):
            if w not in times:
                stack.append(edge(v, w))
                dfs(w, v)
                low[v] = min(low[v], low[w])
                if low[w] >= times[v]:
                    block = []
                    while True:
                        e = stack.pop()
                        block.append(e)
                        if e == edge(v, w):
                            break
                    bv = sorted({x for e in block for x in e})
                    deg = {x: sum(x in e for e in block) for x in bv}
                    kind = ('clique' if len(block) == len(bv)*(len(bv)-1)//2 else
                            'odd_cycle' if len(bv) % 2 and all(d == 2 for d in deg.values()) else 'other')
                    result.append(dict(vertices=bv, edges=[list(e) for e in sorted(block)], kind=kind))
            elif w != parent and times[w] < times[v]:
                stack.append(edge(v, w))
                low[v] = min(low[v], times[w])
    for v in sorted(vs):
        if v not in times:
            dfs(v)
    return sorted(result, key=lambda z: z['vertices'])


def structure(g):
    nb = neighbors(g)
    interior = [v for v in g['vertices'] if v not in B]
    hnb = {v: nb[v] & set(interior) for v in interior}
    cuts = {v: components(interior, hnb, v) for v in interior
            if len(components(interior, hnb, v)) > 1}
    c = sorted(set(interior) - {'s'})
    cnb = {v: hnb[v] & set(c) for v in c}
    cblocks = blocks(c, cnb)
    def bridges(vs, adj):
        baseline = len(components(vs, adj))
        result = []
        for u in vs:
            for v in sorted(adj[u]):
                if u < v:
                    modified = {x: set(ys) for x, ys in adj.items()}
                    modified[u].remove(v)
                    modified[v].remove(u)
                    if len(components(vs, modified)) > baseline:
                        result.append([u, v])
        return sorted(result)
    return dict(degrees={v: len(nb[v]) for v in interior},
                boundary_neighbors={v: sorted(nb[v] & set(B)) for v in interior},
                d_H_s=len(hnb['s']), H_components=components(interior, hnb),
                H_cut_vertices=cuts, H_biconnected=len(interior) >= 3 and not cuts,
                H_blocks=blocks(interior, hnb), H_bridges=bridges(interior, hnb), C_vertices=c,
                C_components=components(c, cnb), C_blocks=cblocks,
                C_gallai=all(b['kind'] != 'other' for b in cblocks), C_bridges=bridges(c, cnb),
                C_cut_vertices={v: components(c, cnb, v) for v in c
                                if len(components(c, cnb, v)) > len(components(c, cnb))})


def relation(g, row, assignments):
    ri, si = [g['vertices'].index(v) for v in g['root_order']]
    return dict(row=list(row), full_lifts=[list(f) for f in assignments],
                root_fibres=[dict(pin=[a, b], lift_indices=[i for i, f in enumerate(assignments)
                                                         if f[ri] == a and f[si] == b])
                             for a in COLORS for b in COLORS])


def build(seed=None):
    rows = proper_rows()
    reps = sorted(set(map(normalize, rows)))
    assert len(rows) == 240 and len(reps) == 10
    gs = fixed_graphs()
    records = []
    for g in gs:
        entries = [relation(g, row, lifts(g, row, seed=seed)) for row in rows]
        sigma = sum(1 << i for i, row in enumerate(reps) if lifts(g, row, seed=seed))
        minimal = None
        if g['name'].endswith('_M'):
            assert not lifts(g, BETA, seed=seed), g['name']
            minimal = []
            for e in map(tuple, g['edges']):
                if e in BOUNDARY:
                    continue
                fs = lifts(g, BETA, removed=[e], seed=seed)
                assert fs, (g['name'], e)
                minimal.append(dict(deleted_edge=list(e), full_witness=list(fs[0])))
        records.append(dict(graph=g, structure=structure(g), canonical_sigma_mask=sigma,
                            all_240_proper_rows=entries, beta_minimality=minimal,
                            exact_N45_target=dict(verdict='not triggered',
                                reason=('only one degree5 point and r-s adjacent; explicit K5 minor' if
                                        g['name'] == 'ARTICULATION_M' else
                                        'full Sigma is not 933/941, or only one degree5 point'))))
    by_name = {r['graph']['name']: r for r in records}
    art = by_name['ARTICULATION_M']
    assert art['structure']['H_cut_vertices'].keys() == {'s'}
    assert art['structure']['degrees'] == dict(s=5, r=4, p=4, u=4, v=4)
    bags = [['s'], ['r'], ['p'], ['b4'], ['b0', 'b1', 'b2', 'b3', 'u']]
    nb = neighbors(art['graph'])
    assert all(len(components(bag, {v: nb[v] & set(bag) for v in bag})) == 1 for bag in bags)
    assert all(any(v in nb[u] for u in a for v in b) for a, b in itertools.combinations(bags, 2))
    art['non_disk_K5_minor'] = dict(bags=bags, verdict='triggered and holds')
    restoration = []
    for stem in ('TRIANGLE', 'LONG'):
        m, g = by_name[stem + '_M'], by_name[stem + '_G']
        assert m['structure']['H_biconnected'] and m['structure']['d_H_s'] == 2
        assert m['structure']['C_gallai'] and 'r' in m['structure']['C_cut_vertices']
        assert m['structure']['degrees']['r'] == 4 and m['structure']['degrees']['s'] == 5
        assert g['canonical_sigma_mask'] not in (933, 941), g['canonical_sigma_mask']
        assert g['canonical_sigma_mask'] == m['canonical_sigma_mask']
        ri = m['graph']['vertices'].index('r')
        filt = []
        for mr, gr in zip(m['all_240_proper_rows'], g['all_240_proper_rows']):
            retained_indices = [i for i, f in enumerate(mr['full_lifts']) if f[ri] != mr['row'][2]]
            assert [mr['full_lifts'][i] for i in retained_indices] == gr['full_lifts']
            filt.append(dict(row=mr['row'], X_lift_indices_restoring_rb2=retained_indices))
        restoration.append(dict(G=stem + '_G', X_equals_M=stem + '_M', omitted_edge=['b2', 'r'],
                                complete_literal_filter_verdict='triggered and holds',
                                original_omitted_edge_Sigma_critical=False,
                                all_240_rows=filt))
    long, tri = by_name['LONG_M'], by_name['TRIANGLE_M']
    retained = [long['graph']['vertices'].index(v) for v in tri['graph']['vertices']]
    failures, relation_diffs = [], []
    for lr, tr in zip(long['all_240_proper_rows'], tri['all_240_proper_rows']):
        projected = {tuple(f[i] for i in retained) for f in lr['full_lifts']}
        target = set(map(tuple, tr['full_lifts']))
        lost, extra = sorted(projected - target), sorted(target - projected)
        if lost or extra:
            failures.append(dict(row=lr['row'], projected_source_not_target=[list(f) for f in lost],
                                 target_without_source_preimage=[list(f) for f in extra]))
        lpins = [z['pin'] for z in lr['root_fibres'] if z['lift_indices']]
        tpins = [z['pin'] for z in tr['root_fibres'] if z['lift_indices']]
        if lpins != tpins:
            relation_diffs.append(dict(row=lr['row'], source_root_relation=lpins, target_root_relation=tpins))
    assert failures
    return dict(schema='fixed-literal-single-deficit-controls-v1', literal_color_frame=list(COLORS),
                canonical_pattern_order=[list(r) for r in reps], graphs=records,
                derivative_restoration=restoration,
                shrink=dict(source='LONG_M', target='TRIANGLE_M',
                            retained_vertex_order=tri['graph']['vertices'],
                            full_lift_projection_verdict='counterexample',
                            full_lift_projection_failures=failures,
                            complete_root_relation_differences=relation_diffs),
                claims=[dict(id='MINIMAL-DOES-NOT-IMPLY-BICONNECTED', verdict='counterexample',
                             note='beta-minimal, one degree5, connected; fails disk and N45 target'),
                        dict(id='GALLAI-INTERNAL-STRUCTURE', verdict='triggered and holds',
                             note='two fixed biconnected controls have d_H(s)=2 and Gallai H-s'),
                        dict(id='ARBITRARY-CYCLE-SHRINK-PRESERVES-FULL-LIFTS', verdict='counterexample'),
                        dict(id='LITERAL-SPOKE-RESTORATION-FILTER', verdict='triggered and holds'),
                        dict(id='EXACT-N45-SOURCE', verdict='not triggered'),
                        dict(id='LIT-SD-A', verdict='not triggered',
                             note='no frozen accepted A result; no finite test certifies theorem')])


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--generate', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'observations-v3.json')
    parser.add_argument('--seed', type=int)
    args = parser.parse_args()
    result = build(args.seed)
    if args.generate:
        if args.certificate.exists():
            raise RuntimeError('refusing to overwrite an existing certificate')
        args.certificate.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    else:
        expected = json.loads(args.certificate.read_text())
        if result != expected:
            print('FAIL: recomputed complete graph/lift/claim record differs', file=sys.stderr)
            return 1
    print(json.dumps(dict(status='PASS', graphs=len(result['graphs']),
                          proper_rows_per_graph=240,
                          full_lifts=sum(len(row['full_lifts']) for g in result['graphs']
                                         for row in g['all_240_proper_rows']),
                          projection_failure_rows=len(result['shrink']['full_lift_projection_failures']),
                          root_relation_difference_rows=len(result['shrink']['complete_root_relation_differences']),
                          exact_N45_source='not triggered'), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
