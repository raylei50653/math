#!/usr/bin/env python3
"""ES: exhaustive fixed epsilon=2 induced-C5 disk search (NA/AD/D6).

No four-colour-theorem oracle. JSON writes are exclusive, replay is byte exact.
See docs/c5_excess_two_finite_search.md for coverage and proof boundaries.
"""
from __future__ import annotations
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from math import factorial
from multiprocessing import Pool
from pathlib import Path
import sys
import time
import networkx as nx
import rustworkx as rx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_finite_search'
from c5_kempe_screen import REPS

T4 = 932
T4_ROWS = [i for i in range(10) if T4 >> i & 1]
REJ_IDX = [6, 4, 3, 1, 0]          # singleton row with unique colour at frame vertex p
NROW = len(REPS)
assert NROW == 10
for _p, _qi in enumerate(REJ_IDX):
    _r = REPS[_qi]
    assert len(set(_r)) == 3 and _r.count(_r[_p]) == 1
# D5 as maps i -> g[i] on frame vertices
D5 = [tuple((s * i + r) % 5 for i in range(5)) for s in (1, -1) for r in range(5)]
assert len(set(D5)) == 10
# row q, frame subset mask -> forbidden colour mask
FORB = [[0] * 32 for _ in range(NROW)]
for _q in range(NROW):
    for _m in range(32):
        f = 0
        for s in range(5):
            if _m >> s & 1:
                f |= 1 << REPS[_q][s]
        FORB[_q][_m] = f
SUBSETS = {n: [sum(1 << s for s in c) for c in combinations(range(5), n)] for n in range(6)}


def popcount(x):
    return x.bit_count()


def bits(x):
    i = 0
    while x:
        if x & 1:
            yield i
        x >>= 1
        i += 1


# ---------------------------------------------------------------- H generation
def target_deg(k, kind='NA'):
    return ([6] + [4] * (k - 1)) if kind == 'D6' else [5, 5] + [4] * (k - 2)


def root_count(kind):
    return 1 if kind == 'D6' else 2


def private_group_size(kind, k):
    r = root_count(kind)
    return factorial(r) * factorial(k-r)


def pair_table(k):
    pb = [[-1] * k for _ in range(k)]
    n = 0
    for a in range(k):
        for b in range(a + 1, k):
            pb[a][b] = pb[b][a] = n
            n += 1
    return pb


def refine(k, adj, kind):
    """Isomorphism-invariant colour refinement; initial colour (non-root, degree)."""
    col0 = [(0 if v < root_count(kind) else 1, popcount(adj[v])) for v in range(k)]
    keys = sorted(set(col0))
    col = [keys.index(c) for c in col0]
    while True:
        sig = [(col[v], tuple(sorted(col[u] for u in bits(adj[v])))) for v in range(k)]
        keys = sorted(set(sig))
        new = [keys.index(s) for s in sig]
        if len(keys) == len(set(col)):
            return new
        col = new


def canon_H(k, adj, pb, kind):
    """Canonical code of H under S, and |Aut_S(H)|.
    Valid relabellings put colour classes on consecutive labels (in colour order);
    every element of Aut_S(H) preserves the refined colours."""
    col = refine(k, adj, kind)
    cells = {}
    for v in range(k):
        cells.setdefault(col[v], []).append(v)
    order = [cells[c] for c in sorted(cells)]
    edges = [(a, b) for a in range(k) for b in bits(adj[a]) if a < b]
    best = None
    cnt = 0
    for perms in product(*[permutations(c) for c in order]):
        lab = [0] * k
        n = 0
        for p in perms:
            for v in p:
                lab[v] = n
                n += 1
        code = 0
        for a, b in edges:
            code |= 1 << pb[lab[a]][lab[b]]
        if best is None or code < best:
            best, cnt = code, 1
        elif code == best:
            cnt += 1
    return best, cnt


def degree_sequences(k, kind):
    if kind == 'D6':
        roots = ((d,) for d in range(3, min(6, k-1)+1))
    else:
        limit = min(5, k-1-(kind == 'NA'))
        roots = ((a,b) for a in range(2,limit+1) for b in range(2,a+1))
    r = root_count(kind)
    for rd in roots:
        for ds in combinations_with_replacement(range(min(4,k-1),0,-1), k-r):
            d = rd + ds
            if sum(d) % 2 == 0 and sum(d)//2 >= k:
                yield d


def connected(k, adj):
    seen = 1
    frontier = 1
    while frontier:
        nb = 0
        for v in bits(frontier):
            nb |= adj[v]
        frontier = nb & ~seen
        seen |= nb
    return seen == (1 << k) - 1


def gen_H_degseq(args):
    k, d, kind = args
    pb = pair_table(k)
    cur = [0] * k
    adj = [0] * k
    out = {}

    def rec(i):
        if i == k:
            if connected(k, adj) and (kind != 'AD' or adj[0] & 2):
                code, aut = canon_H(k, adj, pb, kind)
                if code not in out:
                    out[code] = (tuple(adj), aut)
            return
        rem = d[i] - cur[i]
        if rem < 0:
            return
        cands = [j for j in range(i + 1, k) if cur[j] < d[j] and not (kind == 'NA' and i == 0 and j == 1)]
        if len(cands) < rem:
            return
        for S in combinations(cands, rem):
            for j in S:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
                cur[j] += 1
            rec(i + 1)
            for j in S:
                adj[i] &= ~(1 << j)
                adj[j] &= ~(1 << i)
                cur[j] -= 1
    rec(0)
    return [(code, adj, aut) for code, (adj, aut) in out.items()]


def gen_H(k, pool, kind):
    seqs = list(degree_sequences(k, kind))
    reps = []
    for res in pool.imap_unordered(gen_H_degseq, [(k, d, kind) for d in seqs]):
        reps.extend(res)
    reps.sort()
    return reps


# ---------------------------------------------------------------- colourings
def colourings(k, adj, maxmono):
    """All 4-colourings of H with at most maxmono monochromatic H-edges.
    Returns list of (colour tuple, mono edge or None)."""
    out = []
    c = [0] * k

    def rec(i, mono):
        if i == k:
            out.append((tuple(c), mono))
            return
        for col in range(4):
            m = mono
            ok = True
            for u in bits(adj[i] & ((1 << i) - 1)):
                if c[u] == col:
                    if m is None and maxmono:
                        m = (u, i)
                    else:
                        ok = False
                        break
            if ok:
                c[i] = col
                rec(i + 1, m)
    rec(0, None)
    return out


def bitsets(k, cols):
    B = [[0] * 4 for _ in range(k)]
    for j, (c, _) in enumerate(cols):
        for v in range(k):
            B[v][c[v]] |= 1 << j
    MA = [[0] * 16 for _ in range(k)]
    for v in range(k):
        for A in range(16):
            x = 0
            for col in range(4):
                if A >> col & 1:
                    x |= B[v][col]
            MA[v][A] = x
    # M[v][spokemask][q]
    M = [[tuple(MA[v][15 & ~FORB[q][m]] for q in range(NROW)) for m in range(32)]
         for v in range(k)]
    return B, M


class HData:
    def __init__(self, k, adj, kind='NA'):
        self.kind = kind
        self.k = k
        self.adj = adj
        self.deg = target_deg(k, kind)
        self.dint = [popcount(a) for a in adj]
        self.need = [self.deg[v] - self.dint[v] for v in range(k)]
        self.edges = [(a, b) for a in range(k) for b in bits(adj[a]) if a < b]
        cols = colourings(k, adj, 0)
        self.ncol = len(cols)
        self.full = (1 << self.ncol) - 1
        self.B, self.M = bitsets(k, cols)
        self._c1 = None

    def c1(self):
        """Universe of colourings with <= 1 monochromatic H-edge (lazy)."""
        if self._c1 is None:
            cols = colourings(self.k, self.adj, 1)
            B, M = bitsets(self.k, cols)
            P = 0
            E = {e: 0 for e in self.edges}
            for j, (_, mono) in enumerate(cols):
                if mono is None:
                    P |= 1 << j
                else:
                    E[mono] |= 1 << j
            self._c1 = (B, M, P, E)
        return self._c1


def sigma_of(hd, S):
    """Sigma for a (possibly partial) spoke assignment; unassigned = None/0."""
    m = 0
    for q in range(NROW):
        x = hd.full
        for v in range(hd.k):
            x &= hd.M[v][S[v]][q]
        if x:
            m |= 1 << q
    return m


def crit_onepass(hd, S, sigma):
    """For every non-frame edge e, Sigma(G-e), computed in one pass.
    Rows gained by deleting e are exactly the rows q not in Sigma(G) having a
    colouring (frame fixed to q) whose ONLY monochromatic edge is e."""
    B, M, P, E = hd.c1()
    k = hd.k
    gained = {('h', e): 0 for e in hd.edges}
    for v in range(k):
        for s in bits(S[v]):
            gained[('s', (v, s))] = 0
    for q in range(NROW):
        if sigma >> q & 1:
            continue
        row = [M[v][S[v]][q] for v in range(k)]
        pre = [-1] * (k + 1)
        for v in range(k):
            pre[v + 1] = pre[v] & row[v]
        suf = [-1] * (k + 1)
        for v in range(k - 1, -1, -1):
            suf[v] = suf[v + 1] & row[v]
        X = pre[k]
        if X:
            for e in hd.edges:
                if X & E[e]:
                    gained[('h', e)] |= 1 << q
        for v in range(k):
            if not S[v]:
                continue
            others = pre[v] & suf[v + 1] & P
            if not others:
                continue
            for s in bits(S[v]):
                if others & M[v][S[v] & ~(1 << s)][q] & B[v][REPS[q][s]]:
                    gained[('s', (v, s))] |= 1 << q
    return {key: sigma | g for key, g in gained.items()}


def edge_label(key):
    t, (a, b) = key
    if t == 'h':
        return (5 + a, 5 + b)
    return (b, 5 + a)          # spoke: (frame, inner)


def edge_type(key, kind):
    t, (a, b) = key
    if t == 's':
        return 'root spoke' if a < root_count(kind) else 'degree-4 spoke'
    return 'internal with root' if min(a,b) < root_count(kind) else 'internal without root'


def q_shape(Q):
    return min(tuple(sorted(g[p] for p in Q)) for g in D5)


def c_of_Q(Q):
    """c(Q) = |Q| - e(Q), e(Q) = frame edges with both ends in Q
    (= number of maximal arcs for 1<=|Q|<=4; separately c(B)=1)."""
    Qs = set(Q)
    return 1 if len(Qs) == 5 else len(Qs) - sum(1 for i in range(5) if i in Qs and (i + 1) % 5 in Qs)


TRIPLES_941 = {frozenset(g[p] for p in (0, 1, 3)) for g in D5}   # two-point arc + isolated point


def contains_941(Q):
    return any(t <= set(Q) for t in TRIPLES_941)


# E3 report: |Q|+c(Q) > 4  <=>  Q contains a 941-shaped triple (check all 32 subsets)
for _m in range(32):
    _Q = [p for p in range(5) if _m >> p & 1]
    if _Q:
        assert (len(_Q) + c_of_Q(_Q) > 4) == contains_941(_Q), _Q


def component_analysis(edges, k, kind):
    g = nx.Graph(); g.add_nodes_from(range(5+k)); g.add_edges_from(edges)
    roots = list(range(5,5+root_count(kind)))
    rest = g.subgraph(range(5+root_count(kind),5+k))
    comps = []
    for C in sorted(sorted(c) for c in nx.connected_components(rest)):
        incidence = [sum(g.has_edge(r,v) for v in C) for r in roots]
        touched = sum(bool(n) for n in incidence)
        label = 'mixed' if touched == 2 else ('unary' if touched == 1 else 'detached')
        comps.append(dict(vertices=C, kind=label, root_incidence=incidence,
                          support=sorted({u for v in C for u in g[v] if u < 5}),
                          spokes=sorted([u,v] for v in C for u in g[v] if u < 5),
                          internal_edges=sorted(list(sorted(e)) for e in rest.subgraph(C).edges())))
    return dict(m=sum(c['kind']=='mixed' for c in comps),
                unary=sum(c['kind']=='unary' for c in comps), components=comps,
                root_spokes={str(r):sorted(u for u in g[r] if u < 5) for r in roots})


def labeled_edges(hd, S):
    es = [(i, (i + 1) % 5) for i in range(5)]
    es += [(5 + a, 5 + b) for a, b in hd.edges]
    for v in range(hd.k):
        for s in bits(S[v]):
            es.append((s, 5 + v))
    return sorted(tuple(sorted(e)) for e in es)



def vertex_order(hd):
    order = [max(range(hd.k), key=lambda v:(hd.need[v],-v))]
    while len(order)<hd.k:
        placed = sum(1<<u for u in order)
        order.append(min((v for v in range(hd.k) if v not in order),
                         key=lambda v:(-(hd.adj[v]&placed).bit_count(),-hd.need[v],v)))
    return order


def d5_reps(n):
    seen=set(); reps=[]
    for m in SUBSETS[n]:
        if m in seen: continue
        orb={sum(1<<g[s] for s in bits(m)) for g in D5}
        seen |= orb; reps.append((m,len(orb)))
    assert sum(w for _,w in reps)==len(SUBSETS[n])
    return reps


def canonical_form(edges, kind, k, with_stabilizer=False):
    """Lex minimum under D5 x degree-preserving private permutations.

    For fixed frame map the spoke incidence vectors must be descending in
    lexicographic frame order inside each degree class: moving a 1 to the
    smaller private label first decreases the first differing spoke edge.
    Thus only permutations inside equal-support cells can attain the minimum.
    Counting minimizing maps gives the exact full-group stabilizer.
    """
    edges=tuple(sorted(tuple(sorted(e)) for e in edges))
    supports=[0]*k
    for a,b in edges:
        if a<5<=b: supports[b-5] |= 1<<a
    best=None; aut=0; r=root_count(kind)
    for frame in D5:
        transformed=[sum(1<<frame[s] for s in bits(m)) for m in supports]
        cells=[]; labels=[]
        for group in (range(r),range(r,k)):
            by={}
            for v in group: by.setdefault(transformed[v],[]).append(v)
            ordered=sorted(by,key=lambda m:tuple(-((m>>s)&1) for s in range(5)))
            cells.extend(by[m] for m in ordered)
            labels.extend(group)
        for perms in product(*(permutations(c) for c in cells)):
            old_order=[v for p in perms for v in p]
            mapping=list(frame)+[0]*k
            for old,new in zip(old_order,labels): mapping[5+old]=5+new
            candidate=tuple(sorted(tuple(sorted((mapping[a],mapping[b]))) for a,b in edges))
            if best is None or candidate<best: best=candidate; aut=1
            elif candidate==best: aut+=1
    return (best,aut) if with_stabilizer else best


def data_of_edges(edges, k, kind):
    adj=[0]*k; S=[0]*k
    for a,b in edges:
        a,b=sorted((a,b))
        if a>=5:
            adj[a-5] |= 1<<(b-5); adj[b-5] |= 1<<(a-5)
        elif b>=5: S[b-5] |= 1<<a
    return HData(k,adj,kind),S


def deletion_list(hd,S,mask):
    return sorted((dict(edge=list(edge_label(key)),sigma_mask=m)
                   for key,m in crit_onepass(hd,S,mask).items()),key=lambda x:x['edge'])


def process_H(args):
    k,kind,code,adj,aut,mode=args
    hd=HData(k,list(adj),kind)
    weight=private_group_size(kind,k)//aut
    assert weight*aut==private_group_size(kind,k)
    counts=dict(edgesets=weight,disk=0,t4=0,q=0,crit=0)
    diagnostics=Counter(); shapes=Counter(); noncrit_edges=Counter(); noncrit_graphs=Counter()
    histogram=Counter(); typesets=Counter(); qrecords={}
    order=vertex_order(hd); S=[0]*k
    # Mutable planar graph with apex at k+5; only deterministic certificates use NX.
    g=rx.PyGraph(multigraph=False); g.add_nodes_from(range(k+6))
    g.add_edges_from_no_data([(i,(i+1)%5) for i in range(5)]+[(k+5,i) for i in range(5)]+
                             [(5+a,5+b) for a,b in hd.edges])
    if not rx.is_planar(g):
        return dict(counts=counts,diagnostics={'H_nonplanar':1},qrecords=[],shapes={},
                    noncrit_edges={},noncrit_graphs={},histogram={},typesets={})

    remaining=[sum(hd.need[v] for v in order[i+1:]) for i in range(k)]

    def leaf(acc,alive,w):
        if mode=='validate': counts['disk']+=w
        if not alive: return
        mask=sum(1<<i for i in range(NROW) if acc[i])
        assert mask&T4==T4
        counts['t4']+=w
        Q=[p for p,qi in enumerate(REJ_IDX) if not mask>>qi&1]
        if not Q: return
        counts['q']+=w
        shapes[','.join(map(str,q_shape(Q)))]+=w
        touched=0
        for support in S:touched|=support
        lemma_excluded=(len(Q)>=2 and touched!=31) or (len(Q)==1 and touched.bit_count()<4) or len(hd.edges)==k-1
        critical_candidate=(mode!='fast') or not lemma_excluded
        # The q diagnostic pass still needs every deletion mask. The proved
        # lemmas prune only critical candidates, leaving all q counts intact.
        sm=crit_onepass(hd,S,mask)
        noncrit=[key for key,m in sm.items() if m==mask]
        for key in noncrit: noncrit_edges[edge_type(key,kind)]+=w
        types=set(edge_type(key,kind) for key in noncrit)
        for t in types: noncrit_graphs[t]+=w
        histogram[str(len(noncrit))]+=w
        typesets[' + '.join(sorted(types)) or 'critical']+=w
        if not critical_candidate: assert noncrit
        if critical_candidate and not noncrit: counts['crit']+=w
        edges=labeled_edges(hd,S)
        canonical=canonical_form(edges,kind,k)
        # Local aggregation is deterministic; every visited leaf contributes its
        # H-orbit times first-support D5-orbit weight, never a marginal weight.
        qrecords[canonical]=qrecords.get(canonical,0)+w
        diagnostics['q_representatives']+=1
        if contains_941(Q): diagnostics['q_contains_941_triple_labelled']+=w

    def rec(i,acc,alive,w,untouched):
        diagnostics['nodes']+=1
        if i==k:
            leaf(acc,alive,w); return
        v=order[i]
        opts=d5_reps(hd.need[v]) if i==0 else [(m,1) for m in SUBSETS[hd.need[v]]]
        for m,mult in opts:
            newacc=tuple(acc[q]&hd.M[v][m][q] for q in range(NROW)) if alive else acc
            newalive=alive and all(newacc[q] for q in T4_ROWS)
            if mode=='fast' and not newalive:
                diagnostics['T4_pruned_nodes']+=1; continue
            if mode=='fast' and (untouched&~m).bit_count()-remaining[i]>=2:
                # E2 unattached-boundary lemma uses T4 only: every q leaf
                # touches at least four frame vertices. Even spending every
                # remaining spoke on a new vertex cannot do that here.
                diagnostics['support_lemma_pruned_nodes']+=1; continue
            # Further two-row/support and tree guards are checked at q leaves.
            # Every retained q leaf still has the full deletion diagnostic pass.
            S[v]=m
            additions=[(5+v,s) for s in bits(m)]
            for a,b in additions:g.add_edge(a,b,None)
            diagnostics['planarity_calls']+=bool(additions)
            planar=not additions or rx.is_planar(g)
            if planar: rec(i+1,newacc,newalive,w*mult,untouched&~m)
            for a,b in additions:g.remove_edge(a,b)
            S[v]=0
    rec(0,tuple(hd.full for _ in range(NROW)),True,weight,31)
    return dict(counts=counts,diagnostics=dict(diagnostics),
                qrecords=[(E,w) for E,w in sorted(qrecords.items())],shapes=dict(shapes),
                noncrit_edges=dict(noncrit_edges),noncrit_graphs=dict(noncrit_graphs),
                histogram=dict(histogram),typesets=dict(typesets))


def extension(edges,k,index):
    """Independent MRV backtracking witness in the single literal colour frame."""
    adjacency=[set() for _ in range(k+5)]
    for a,b in edges: adjacency[a].add(b); adjacency[b].add(a)
    colours=dict(enumerate(REPS[index]))
    def visit():
        if len(colours)==k+5:return [colours[v] for v in range(k+5)]
        choices=[]
        for v in range(5,k+5):
            if v in colours:continue
            used={colours[u] for u in adjacency[v] if u in colours}
            allowed=[c for c in range(4) if c not in used]
            if not allowed:return None
            choices.append((len(allowed),-len(adjacency[v]),v,allowed))
        _,_,v,allowed=min(choices)
        for c in allowed:
            colours[v]=c; answer=visit()
            if answer is not None:return answer
        del colours[v];return None
    return visit()


def graph_certificate(edges,k,kind):
    hd,S=data_of_edges(edges,k,kind); mask=sigma_of(hd,S)
    assert mask&T4==T4
    assert [len(list(bits(a)))+m.bit_count() for a,m in zip(hd.adj,S)]==target_deg(k,kind)
    assert kind=='D6' or bool(hd.adj[0]&2)==(kind=='AD')
    Q=[p for p,qi in enumerate(REJ_IDX) if not mask>>qi&1];assert Q
    deletions=[]
    for d in deletion_list(hd,S,mask):
        edge=tuple(d['edge']); new=d['sigma_mask']; assert new!=mask
        indices=[i for i in range(10) if (new&~mask)>>i&1]
        witnesses=[]
        minus=tuple(e for e in edges if tuple(e)!=edge)
        for i in indices:
            colouring=extension(minus,k,i);assert colouring is not None
            assert colouring[edge[0]]==colouring[edge[1]]
            assert all(colouring[a]!=colouring[b] for a,b in minus)
            witnesses.append(dict(pattern_index=i,colouring=colouring))
        deletions.append(dict(edge=list(edge),sigma_mask=new,new_indices=indices,witnesses=witnesses))
    apex=k+5; g=nx.Graph();g.add_nodes_from(range(k+6))
    g.add_edges_from(edges);g.add_edges_from((apex,b) for b in range(5))
    ok,emb=nx.check_planarity(g);assert ok;emb.check_structure()
    aug={str(v):list(emb.neighbors_cw_order(v)) for v in range(k+6)}
    rotations={v:[u for u in emb.neighbors_cw_order(v) if u!=apex] for v in range(k+5)}
    plane=nx.PlanarEmbedding();plane.set_data(rotations);plane.check_structure()
    faces=[]
    for a,b in ((i,(i+1)%5) for i in range(5)):
        for u,v in ((a,b),(b,a)):
            face=plane.traverse_face(u,v)
            if len(face)==5 and set(face)==set(range(5)):faces.append(face)
    assert faces,'critical graph must have a C5 face'
    accepted={str(i):extension(edges,k,i) for i in range(10) if mask>>i&1}
    assert all(x is not None for x in accepted.values())
    return dict(canonical_edges=[list(e) for e in edges],sigma_mask=mask,Q=Q,
                c_Q=c_of_Q(Q),Q_plus_cQ=len(Q)+c_of_Q(Q),
                contains_941_triple=contains_941(Q),structure=component_analysis(edges,k,kind),
                degrees=target_deg(k,kind),epsilon=2,accepted_colourings=accepted,
                deletion_sigmas=deletions,embedding=dict(apex=apex,augmented_rotation=aug,
                disk_rotation={str(v):rotations[v] for v in range(k+5)},outer_face=min(faces)))


def finalize_orbit(args):
    """Recompute a complete canonical q graph independently in a worker."""
    kind,k,mode,E,weight=args
    lemmas=Counter()
    canonical,aut=canonical_form(E,kind,k,True);assert canonical==E
    orbit_size=10*private_group_size(kind,k)//aut
    assert weight==orbit_size,(kind,k,weight,orbit_size)
    hd,S=data_of_edges(E,k,kind);mask=sigma_of(hd,S)
    Q=[p for p,qi in enumerate(REJ_IDX) if not mask>>qi&1]
    sm=deletion_list(hd,S,mask);critical=all(d['sigma_mask']!=mask for d in sm)
    touched=0
    for m in S:touched|=m
    support_excluded=(len(Q)>=2 and touched!=31) or (len(Q)==1 and touched.bit_count()<4)
    tree_excluded=len(hd.edges)==k-1
    if mode=='fast' and (support_excluded or tree_excluded):
        assert not critical
        lemmas['critical_candidates_excluded_labelled']+=weight
    record=dict(canonical_edges=[list(e) for e in E],orbit_size=orbit_size,
                stabilizer_size=aut,sigma_mask=mask,Q=Q,c_Q=c_of_Q(Q),
                Q_plus_cQ=len(Q)+c_of_Q(Q),critical=critical)
    # Small validation levels retain every edge deletion, including failures.
    if k<=6:record['deletion_sigmas']=sm
    certificate=None
    if critical:
        certificate=graph_certificate(E,k,kind)
        certificate.update(orbit_size=orbit_size,stabilizer_size=aut)

    return record,certificate,dict(lemmas)


def run(kind,k,mode='validate',jobs=1):
    if k<root_count(kind): raise ValueError('too few private vertices for root type')
    counts=Counter();diags=Counter();qweights=Counter()
    aggregate={name:Counter() for name in ('shapes','noncrit_edges','noncrit_graphs','histogram','typesets')}
    with Pool(jobs) as pool:
        reps=gen_H(k,pool,kind)
        print(f'{kind} k={k} {mode}: H orbits={len(reps)}',file=sys.stderr,flush=True)
        tasks=[(k,kind,code,adj,aut,mode) for code,adj,aut in reps]
        tasks.sort(key=lambda t:-sum(target_deg(k,kind)[v]-t[3][v].bit_count() for v in range(k)))
        start=time.monotonic(); last=start; done=0
        for result in pool.imap_unordered(process_H,tasks,chunksize=1):
            counts.update(result['counts']);diags.update(result['diagnostics'])
            for E,w in result['qrecords']:qweights[tuple(map(tuple,E))]+=w
            for key in aggregate:aggregate[key].update(result[key])
            done+=1
            if time.monotonic()-last>30:
                last=time.monotonic()
                print(f'  {done}/{len(tasks)} H, {last-start:.1f}s, crit={counts["crit"]}',file=sys.stderr,flush=True)
    q_orbits=[]; crit_orbits=[]; lemmas=Counter()
    if qweights:
        with Pool(jobs) as pool:
            # imap retains canonical edge order; worker scheduling never enters JSON.
            tasks=[(kind,k,mode,E,w) for E,w in sorted(qweights.items())]
            for record,certificate,excluded in pool.imap(finalize_orbit,tasks,chunksize=1):
                q_orbits.append(record)
                if certificate is not None:crit_orbits.append(certificate)
                lemmas.update(excluded)
    assert sum(o['orbit_size'] for o in q_orbits)==counts['q']
    assert sum(o['orbit_size'] for o in crit_orbits)==counts['crit']
    final_counts={key:counts[key] for key in ('edgesets','disk','t4','q','crit')}
    if mode=='fast':
        final_counts['disk']=None
        final_counts['t4']=None
    return dict(schema='c5-es-v1',type=kind,k=k,mode=mode,patterns=[list(r) for r in REPS],
                T4_mask=T4,singleton_indices=REJ_IDX,group_size=10*private_group_size(kind,k),
                H_orbits=len(reps),counts=final_counts,diagnostics=dict(sorted(diags.items())),
                lemma_pruning=({'enabled':True,'subtree_pruned_nodes':diags['support_lemma_pruned_nodes'],**dict(sorted(lemmas.items()))}
                               if mode=='fast' else {'enabled':False}),
                q_shape_labelled=dict(sorted(aggregate['shapes'].items())),
                q_noncritical_edge_types=dict(sorted(aggregate['noncrit_edges'].items())),
                q_graphs_with_noncritical_type=dict(sorted(aggregate['noncrit_graphs'].items())),
                q_noncritical_edge_count_histogram=dict(sorted(aggregate['histogram'].items())),
                q_noncritical_typesets=dict(sorted(aggregate['typesets'].items())),
                q_orbits=q_orbits,crit_orbits=crit_orbits,
                counterexample_found=any(o['Q_plus_cQ']>4 for o in crit_orbits))


def encode(payload):
    return (json.dumps(payload,sort_keys=True,ensure_ascii=False,separators=(',',':'))+'\n').encode()


def exclusive_write(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f:f.write(data)


def default_path(kind,k,mode):
    return OUT/f'{kind}_k{k}_{mode}.json'


def generate_one(kind,k,mode,jobs,path,allow_existing_certificates=False):
    if path.exists():raise SystemExit(f'refusing overwrite: {path}')
    started=time.monotonic();payload=run(kind,k,mode,jobs);elapsed=time.monotonic()-started
    certificate_paths=[path.with_suffix('')/'crit_orbits'/f'orbit_{i:04d}.json'
                       for i in range(1,len(payload['crit_orbits'])+1)]
    for target,record in zip(certificate_paths,payload['crit_orbits']):
        if target.exists():
            if not allow_existing_certificates or target.read_bytes()!=encode(record):
                raise SystemExit(f'refusing overwrite or changed certificate: {target}')
    exclusive_write(path,encode(payload))
    for target,record in zip(certificate_paths,payload['crit_orbits']):
        if not target.exists():exclusive_write(target,encode(record))
    print(f'GENERATED {path.name}: {payload["counts"]}, crit_orbits={len(payload["crit_orbits"])}, seconds={elapsed:.3f}',flush=True)
    if payload['counterexample_found']:print('COUNTEREXAMPLE: stop increasing k',flush=True)
    return payload['counterexample_found']


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--type',choices=['NA','AD','D6'])
    ap.add_argument('--k',type=int)
    modes=ap.add_mutually_exclusive_group();modes.add_argument('--validate',action='store_true');modes.add_argument('--fast',action='store_true')
    ap.add_argument('--jobs',type=int,default=32)
    ap.add_argument('--check',action='store_true')
    ap.add_argument('--output',type=Path)
    a=ap.parse_args()
    if a.jobs<1:ap.error('--jobs must be positive')
    mode='fast' if a.fast else 'validate'
    if a.check:
        paths=[a.output] if a.output else ([default_path(a.type,a.k,mode)] if a.type and a.k else sorted(OUT.glob('*_k*_*.json')))
        if not paths:ap.error('no saved search artifacts')
        for path in paths:
            old=path.read_bytes();config=json.loads(old)
            payload=run(config['type'],config['k'],config['mode'],a.jobs)
            if encode(payload)!=old:raise SystemExit(f'CHECK FAILED: byte mismatch {path}')
            directory=path.with_suffix('')/'crit_orbits'
            for i,record in enumerate(payload['crit_orbits'],1):
                target=directory/f'orbit_{i:04d}.json'
                if target.read_bytes()!=encode(record):raise SystemExit(f'CHECK FAILED: {target}')
            print(f'CHECK OK: {path.name} byte-identical ({len(payload["crit_orbits"])} crit orbits)',flush=True)
        return
    if a.type is None and a.k is None and a.output is None:
        # tools/artifacts.py runs producers without arguments. Only missing
        # outputs from this explicitly completed finite plan are created;
        # existing small orbit certificates are verified before reuse.
        for kind,minimum in [('NA',2),('AD',2),('D6',1)]:
            for k in range(minimum,10):
                for selected_mode in (['validate','fast'] if k<=6 else ['validate']):
                    path=default_path(kind,k,selected_mode)
                    if path.exists():continue
                    if generate_one(kind,k,selected_mode,a.jobs,path,True):return
        return
    if a.type is None or a.k is None:ap.error('generation requires both --type and --k')
    path=a.output or default_path(a.type,a.k,mode)
    generate_one(a.type,a.k,mode,a.jobs,path)



if __name__=='__main__':main()
