#!/usr/bin/env python3
"""Stdlib-only literal annulus construction; no minimal-source assertion.

--write creates immutable certificate and summary. --check regenerates all data.
All graph vertices, rotations, directed faces and complete named fibres are kept.
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
C = range(4)
TAUS = tuple(itertools.product(C, repeat=5))

def proper(t):
    return all(t[i] != t[(i + 1) % 5] for i in range(5))

def norm(t):
    d = {}
    return tuple(d.setdefault(x, len(d)) for x in t)

BETAS = tuple(sorted({norm(t) for t in TAUS if proper(t)}))

def edge(a,b):
    return tuple(sorted((a,b)))

def verify_map(vs, es, fs, inner=True):
    assert fs[0] == [0,4,3,2,1]
    if inner: assert fs[-1] == list(U)
    darts = Counter((f[i],f[(i+1)%len(f)]) for f in fs for i in range(len(f)))
    assert darts == Counter(d for e in es for d in (e,e[::-1]))
    assert len(vs) - len(es) + len(fs) == 2
    rotation = {}
    for v in vs:
        links = {}
        for f in fs:
            for i,x in enumerate(f):
                if x == v:
                    assert f[i-1] not in links
                    links[f[i-1]] = f[(i+1)%len(f)]
        assert set(links) == set(links.values())
        start = min(links)
        cyc, x = [], start
        while x not in cyc:
            cyc.append(x)
            x = links[x]
        assert x == start and len(cyc) == len(links)
        rotation[str(v)] = cyc
    seen, todo = set(), [0]
    while todo:
        v = todo.pop()
        if v not in seen:
            seen.add(v)
            todo.extend(rotation[str(v)])
    assert seen == set(vs)
    return rotation

def make_graph(stacks):
    vs = list(range(12 + stacks))
    es = {edge(i,(i+1)%5) for i in B}
    es |= {edge(5+i,5+(i+1)%5) for i in B}
    es |= {edge(a,b) for a,b in [(1,10),(10,11),(11,1),
          (0,10),(0,11),(5,1),(5,10),(5,11)]}
    fs = [[0,4,3,2,1], [0,11,1,2,3,4], [0,1,10],
          [0,10,11], [5,10,1,5,9,8,7,6], [5,11,10],
          [5,1,11], list(U)]
    insertions = []
    target = [0,1,10]
    for z in range(12,12+stacks):
        ix = fs.index(target)
        a,b,c = target
        fs[ix:ix+1] = [[a,b,z],[b,c,z],[c,a,z]]
        es |= {edge(z,t) for t in target}
        insertions.append({'vertex':z,'face':target[:]})
        target = [a,b,z]
    es = sorted(es)
    return {'vertices':vs,'edges':es,'faces':fs,
            'rotation':verify_map(vs,es,fs),'insertions':insertions,
            'B':list(B),'U':list(U),'private':vs[10:],
            'ownership':{'annulus':vs[10:], 'inner_open_disk':[],
                         'B_and_U_labels_fixed':True}}

def enumerate_lifts(g, beta):
    adj = {v:set() for v in g['vertices']}
    for a,b in g['edges']:
        adj[a].add(b); adj[b].add(a)
    colors = dict(zip(B,beta))
    free = [v for v in g['vertices'] if v not in B]
    out = []
    def dfs(k):
        if k == len(free):
            out.append(''.join(str(colors[v]) for v in g['vertices']))
            return
        v = free[k]
        banned = {colors[w] for w in adj[v] if w in colors}
        for c in C:
            if c not in banned:
                colors[v] = c; dfs(k+1)
        colors.pop(v,None)
    dfs(0)
    return sorted(out)

def fibres(g, centered=False):
    rows = []
    for beta in BETAS:
        table = [[] for _ in TAUS]
        for lift in enumerate_lifts(g,beta):
            ix = sum(int(lift[5+j])*4**(4-j) for j in B)
            table[ix].append(lift)
        for tau,ls in zip(TAUS,table):
            assert bool(ls) == (proper(tau) and tau[0] == beta[0]
                                and (not centered or len(set(tau)) == 3))
        rows.append({'beta':list(beta),'cells':table})
    return rows

def build():
    target = make_graph(0)
    source = make_graph(5)
    target['rows'] = fibres(target)
    source['rows'] = fibres(source)
    # Explicit forward restriction and deterministic reverse insertion preserve every lift.
    for sr,tr in zip(source['rows'],target['rows']):
        for sl,tl in zip(sr['cells'],tr['cells']):
            assert sorted(x[:12] for x in sl) == tl
            for lift in tl:
                cs = list(map(int,lift))
                for ins in source['insertions']:
                    available = set(C)-{cs[v] for v in ins['face']}
                    assert len(available) == 1
                    cs.append(available.pop())
                assert ''.join(map(str,cs)) in sl
    # Restore the centre in the identical empty U slot, and independently DFS G.
    for g in (target,source):
        vs = g['vertices'] + [17]
        es = sorted(g['edges'] + [edge(17,u) for u in U])
        fs = g['faces'][:-1] + [[17,U[i],U[(i+1)%5]] for i in B]
        wheel = {'vertices':vs,'edges':es,'faces':fs,'center':17,
                 'rotation':verify_map(vs,es,fs,inner=False)}
        wheel['rows'] = fibres(wheel,centered=True)
        for hr,gr in zip(g['rows'],wheel['rows']):
            for tau,hs,gs in zip(TAUS,hr['cells'],gr['cells']):
                expected = []
                if proper(tau) and len(set(tau)) == 3:
                    color = (set(C)-set(tau)).pop()
                    expected = [h+str(color) for h in hs]
                assert gs == expected
        g['restored_wheel'] = wheel
    # Complete R3 domain used for the <=1-private obstruction.
    r3 = [beta+tau for beta in BETAS for tau in TAUS
          if proper(tau) and len(set(tau)) == 3 and tau[0] == beta[0]]
    allowed = [e for e in itertools.combinations(range(10),2)
               if all(t[e[0]] != t[e[1]] for t in r3)]
    base = {edge(i,(i+1)%5) for i in B} | {edge(5+i,5+(i+1)%5) for i in B}
    expected = sorted(base | {edge(0,6),edge(0,9),edge(5,1),edge(5,4)})
    assert allowed == expected
    # Every forbidden pin pair gets a concrete R3 witness whose endpoints agree.
    forbidden = [{'edge':list(e),'r3_equal_witness':list(next(t for t in r3 if t[e[0]]==t[e[1]]))}
                 for e in itertools.combinations(range(10),2) if e not in allowed]
    bad = (1,2,1,0,2, 0,2,0,1,2)
    assert proper(bad[:5]) and proper(bad[5:]) and len(set(bad[5:])) == 3
    assert all(bad[a]!=bad[b] for a,b in allowed) and bad[0]!=bad[5]
    assert len(set(bad)) == 3
    # Enumerate all optional private-neighbour sets, not all graph possibilities:
    # maximal allowed pin graph dominates every eligible graph, fourth color extends each.
    for neighbours in itertools.chain([()],itertools.chain.from_iterable(
            itertools.combinations(range(10),k) for k in range(1,11))):
        assert all(bad[v] != 3 for v in neighbours)
    cert = {'schema':1,'scope':'synthetic annuli only; global minimal-source hypotheses not triggered',
            'colors':list(C),'B':list(B),'U':list(U),'tau_domain':[list(t) for t in TAUS],
            'representative':target,'source_r7':source,
            'bidirectional_maps':{'forward':'restrict vertices 0 through 11',
              'reverse':'apply insertions in order, each vertex takes the unique missing face color',
              'center':'for every three-color U cell append its unique missing color at new center v'},
            'r_le_1_obstruction':{'target':'proper B,U; U uses three colors; b0=u0',
                 'r3_cells':len(r3),'allowed_pin_edges':[list(e) for e in allowed],
                 'forbidden_pin_edge_witnesses':forbidden,'false_positive_pin_colors':list(bad),
                 'private_color':3,'neighbour_subsets_checked':1024}}
    def stats(g):
        cells = [ls for row in g['rows'] for ls in row['cells']]
        three = [ls for row in g['rows'] for t,ls in zip(TAUS,row['cells']) if len(set(t))==3 and proper(t)]
        return {'private_vertices':len(g['private']),'cells':len(cells),
                'empty_cells':sum(not ls for ls in cells),'H_full_lifts':sum(map(len,cells)),
                'three_color_cells':len(three),'nonempty_three_color_cells':sum(bool(ls) for ls in three),
                'G_full_lifts':sum(map(len,three)),
                'wheel_total_internal_vertices':len(g['private'])+6}
    summary = {'representative':stats(target),'source_r7':stats(source),
               'minimum_private_for_target_relation':2,
               'r_le_1_no_go':'paper argument, independent of planarity; finite control verifies named edge witnesses',
               'source_minimality':'not triggered',
               'general_r_le_6_annulus_representative':'OPEN'}
    return json.loads(json.dumps(cert)),summary

def main():
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--write',action='store_true')
    group.add_argument('--check',action='store_true')
    args=ap.parse_args()
    cert,summary=build()
    p=ROOT/'certificate.json.gz'; s=ROOT/'summary.json'
    if args.write:
        with p.open('xb') as f:
            with gzip.GzipFile(fileobj=f,mode='wb',mtime=0) as z:
                z.write(json.dumps(cert,separators=(',',':')).encode()+b'\n')
        with s.open('x') as f:
            json.dump(summary,f,ensure_ascii=False,indent=2);f.write('\n')
    else:
        with gzip.open(p,'rt') as f: assert json.load(f)==cert
        with s.open() as f: assert json.load(f)==summary
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
