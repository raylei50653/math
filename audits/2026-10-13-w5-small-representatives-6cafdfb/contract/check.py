#!/usr/bin/env python3
"""Complete named fibres of legal prism examples; stdlib only.

--write creates evidence exclusively. --check regenerates both files without
writing. Optional --certificate permits a copied-certificate negative control.
"""
import argparse
from collections import Counter
import gzip
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
B = tuple(range(5))
U = tuple(range(5, 10))
C = tuple(range(4))
TAUS = tuple(itertools.product(C, repeat=5))


def proper(t):
    return all(t[i] != t[(i + 1) % 5] for i in range(5))


def normalize(t):
    d = {}
    return tuple(d.setdefault(x, len(d)) for x in t)


BETAS = tuple(sorted({normalize(t) for t in TAUS if proper(t)}))


def edge(a, b):
    return tuple(sorted((a, b)))


def verify_map(g, capped=False):
    vs, es, fs = g['vertices'], g['edges'], g['faces']
    assert len(set(vs)) == len(vs)
    assert len(set(map(tuple, es))) == len(es)
    assert all(a < b and a in vs and b in vs for a, b in es)
    assert fs[0] == [0, 4, 3, 2, 1]
    if not capped:
        assert fs[-1] == list(U)
    for pins in (B, U):
        actual = {tuple(e) for e in es if set(e) <= set(pins)}
        expected = {edge(pins[i], pins[(i + 1) % 5]) for i in B}
        assert actual == expected
    darts = Counter((f[i], f[(i + 1) % len(f)]) for f in fs for i in range(len(f)))
    assert darts == Counter(d for e in es for d in (tuple(e), tuple(e)[::-1]))
    assert len(vs) - len(es) + len(fs) == 2
    rotation = {}
    for v in vs:
        links = {}
        for f in fs:
            for i, x in enumerate(f):
                if x == v:
                    assert f[i - 1] not in links
                    links[f[i - 1]] = f[(i + 1) % len(f)]
        assert set(links) == set(links.values())
        start = min(links)
        cyc, x = [], start
        while x not in cyc:
            cyc.append(x)
            x = links[x]
        assert x == start and len(cyc) == len(links)
        rotation[str(v)] = cyc
    seen, pending = set(), [0]
    while pending:
        v = pending.pop()
        if v not in seen:
            seen.add(v)
            pending.extend(rotation[str(v)])
    assert seen == set(vs)
    return rotation


def graph(kind, private=0):
    assert kind in ('prism', 'triangulated_prism')
    assert not private or kind == 'prism'
    vs = list(range(10 + private))
    es = {edge(i, (i + 1) % 5) for i in B}
    es |= {edge(5 + i, 5 + (i + 1) % 5) for i in B}
    es |= {edge(i, 5 + i) for i in B}
    fs = [[0, 4, 3, 2, 1]]
    for i in B:
        a, b, c, d = i, (i + 1) % 5, 5 + (i + 1) % 5, 5 + i
        if kind == 'triangulated_prism':
            es.add(edge(a, c))
            fs.extend([[a, b, c], [a, c, d]])
        else:
            fs.append([a, b, c, d])
    fs.append(list(U))
    insertions = []
    if private:
        old = [0, 1, 6, 5]
        index = fs.index(old)
        fs[index:index + 1] = [[0, 1, 10], [1, 6, 10], [6, 5, 0, 10]]
        es |= {edge(10, p) for p in (0, 1, 6)}
        insertions.append({'vertex': 10, 'old_face': old, 'neighbours': [0, 1, 6]})
        target = [0, 1, 10]
        for z in range(11, 10 + private):
            index = fs.index(target)
            a, b, c = target
            fs[index:index + 1] = [[a, b, z], [b, c, z], [c, a, z]]
            es |= {edge(z, p) for p in target}
            insertions.append({'vertex': z, 'old_face': target[:], 'neighbours': target[:]})
            target = [a, b, z]
    g = {'name': kind + '_r' + str(private), 'vertices': vs, 'edges': sorted(es),
         'faces': fs, 'B': list(B), 'U': list(U), 'private': vs[10:],
         'insertions': insertions,
         'ownership': {'annular_private': vs[10:], 'inner_open_disk': [],
                       'B_and_U_distinct_ordered_pins': True}}
    g['rotation'] = verify_map(g)
    return g


def capped(g):
    v = len(g['vertices'])
    h = {'name': g['name'] + '_capped', 'vertices': g['vertices'] + [v],
         'edges': sorted(g['edges'] + [edge(v, u) for u in U]),
         'faces': g['faces'][:-1] + [[v, U[i], U[(i + 1) % 5]] for i in B],
         'center': v, 'B': list(B), 'U': list(U)}
    h['rotation'] = verify_map(h, capped=True)
    assert {x for e in h['edges'] if v in e for x in e if x != v} == set(U)
    return h


def search_rows(g):
    adj = {v: set() for v in g['vertices']}
    for a, b in g['edges']:
        adj[a].add(b)
        adj[b].add(a)
    rows = []
    for beta in BETAS:
        colours = dict(zip(B, beta))
        free = [v for v in g['vertices'] if v not in B]
        cells = [[] for _ in TAUS]

        def dfs(k):
            if k == len(free):
                lift = ''.join(str(colours[v]) for v in g['vertices'])
                ix = sum(colours[U[j]] * 4 ** (4 - j) for j in B)
                cells[ix].append(lift)
                return
            v = free[k]
            banned = {colours[w] for w in adj[v] if w in colours}
            for c in C:
                if c not in banned:
                    colours[v] = c
                    dfs(k + 1)
            colours.pop(v, None)

        dfs(0)
        rows.append({'beta': list(beta), 'cells': [sorted(ls) for ls in cells]})
    return rows


def explicit_rows(g):
    """Independent enumeration: only pins, then explicit owned insertions."""
    rows = []
    pin_edges = [e for e in g['edges'] if e[1] < 10]
    for beta in BETAS:
        cells = []
        for tau in TAUS:
            lifts = []
            pin = list(beta + tau)
            if all(pin[a] != pin[b] for a, b in pin_edges):
                lifts = [pin]
                for ins in g['insertions']:
                    lifts = [colours + [c] for colours in lifts
                             for c in C if c not in {colours[n] for n in ins['neighbours']}]
            cells.append(sorted(''.join(map(str, colours)) for colours in lifts))
        rows.append({'beta': list(beta), 'cells': cells})
    return rows


def summary(g):
    cells = [ls for row in g['rows'] for ls in row['cells']]
    r3 = [ls for row in g['rows'] for tau, ls in zip(TAUS, row['cells'])
          if proper(tau) and len(set(tau)) == 3]
    cap_cells = [ls for row in g['capped']['rows'] for ls in row['cells']]
    sigma = sum((1 << i) for i, row in enumerate(g['capped']['rows']) if any(row['cells']))
    return {'private_vertices': len(g['private']), 'capped_internal_vertices': len(g['private']) + 6,
            'cells_in_each_annulus_or_cap_table': len(cells),
            'annulus_empty_cells': sum(not ls for ls in cells),
            'annulus_full_lifts': sum(map(len, cells)),
            'three_U_cells': len(r3), 'nonempty_three_U_cells': sum(bool(ls) for ls in r3),
            'cap_empty_cells': sum(not ls for ls in cap_cells),
            'cap_full_lifts': sum(map(len, cap_cells)), 'Sigma_mask': sigma,
            'cap_lift_counts_by_beta': [sum(map(len, row['cells'])) for row in g['capped']['rows']]}


def build():
    graphs = [graph('prism'), graph('triangulated_prism'), graph('prism', 10)]
    for g in graphs:
        g['rows'] = search_rows(g)
        assert g['rows'] == explicit_rows(g)
        h = capped(g)
        h['rows'] = search_rows(h)
        for ar, cr in zip(g['rows'], h['rows']):
            for tau, ls, cls in zip(TAUS, ar['cells'], cr['cells']):
                expected = []
                if proper(tau) and len(set(tau)) == 3:
                    centre_colour = next(iter(set(C) - set(tau)))
                    expected = [lift + str(centre_colour) for lift in ls]
                assert cls == expected
        g['capped'] = h
    prism, triangle, source = graphs
    witnesses = []
    for ar, br in zip(prism['rows'], triangle['rows']):
        i = next(j for j, tau in enumerate(TAUS)
                 if proper(tau) and len(set(tau)) == 3 and br['cells'][j])
        witnesses.append({'beta': br['beta'], 'tau': list(TAUS[i]),
                          'cap_colour': next(iter(set(C) - set(TAUS[i])))})
    # Source restriction has the whole prism support, with multiplicity allowed to differ.
    for sr, pr in zip(source['rows'], prism['rows']):
        for sl, pl in zip(sr['cells'], pr['cells']):
            assert sorted(set(x[:10] for x in sl)) == pl
    beta, tau = (0, 1, 0, 1, 2), (1, 0, 1, 0, 3)
    bi, ti = BETAS.index(beta), TAUS.index(tau)
    assert prism['rows'][bi]['cells'][ti] and source['rows'][bi]['cells'][ti]
    assert not triangle['rows'][bi]['cells'][ti]
    assert len(source['rows'][bi]['cells'][ti]) == 2
    assert len(prism['rows'][bi]['cells'][ti]) == 1
    # Two total deterministic full-lift transports preserving each original B pin.
    transports = []
    for sr, tr in zip(source['capped']['rows'], triangle['capped']['rows']):
        sl = sorted(x for cell in sr['cells'] for x in cell)
        tl = sorted(x for cell in tr['cells'] for x in cell)
        assert sl and tl
        transports.append({'beta': sr['beta'], 'source_to_target':
                           [[x, tl[0]] for x in sl], 'target_to_source': [[x, sl[0]] for x in tl]})
    cert = {'schema': 1, 'palette': list(C), 'beta_domain': [list(t) for t in BETAS],
            'tau_domain': [list(t) for t in TAUS], 'graphs': graphs,
            'triangle_full_Sigma_witnesses': witnesses,
            'strict_R3_difference': {'beta': list(beta), 'tau': list(tau),
                                    'extra_diagonal_rejecting_cell': [0, 6],
                                    'source_lifts': source['rows'][bi]['cells'][ti],
                                    'prism_lifts': prism['rows'][bi]['cells'][ti],
                                    'target_lifts': []},
            'B_preserving_bidirectional_total_cap_transports': transports}
    stats = {g['name']: summary(g) for g in graphs}
    assert {s['Sigma_mask'] for s in stats.values()} == {1023}
    report = {'graphs': stats, 'complete_cells_all_six_tables': 6 * 10 * 1024,
              'strict_replacement': {'private': '10 -> 0', 'capped_internal': '16 -> 6',
                                     'preserves_complete_Sigma': True, 'preserves_R3': False},
              'general_family': 'decorated prism with arbitrary r=m>=1 -> triangulated prism r=0',
              'source_minimum_hypotheses': 'not triggered: removable degree-three private vertices',
              'general_r_le_9_representative': 'OPEN'}
    return json.loads(json.dumps(cert)), report


def main():
    p = argparse.ArgumentParser()
    modes = p.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--check', action='store_true')
    p.add_argument('--certificate', type=Path)
    args = p.parse_args()
    cert, report = build()
    cp = args.certificate or ROOT / 'certificate.json.gz'
    sp = ROOT / 'summary.json'
    if args.write:
        assert args.certificate is None
        with cp.open('xb') as f:
            with gzip.GzipFile(fileobj=f, mode='wb', mtime=0) as z:
                z.write(json.dumps(cert, separators=(',', ':')).encode() + b'\n')
        with sp.open('x') as f:
            json.dump(report, f, indent=2)
            f.write('\n')
    else:
        with gzip.open(cp, 'rt') as f:
            assert json.load(f) == cert
        with sp.open() as f:
            assert json.load(f) == report
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
