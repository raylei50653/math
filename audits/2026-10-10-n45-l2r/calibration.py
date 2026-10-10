#!/usr/bin/env python3
"""Abstract relation semantics calibration; never a LOW2 source control."""
import itertools
import json

COL = tuple(range(4))
C_VERTICES = ('r', 'u0', 'u1', 'u2', 'p0', 'p1', 'q0')
X_VERTICES = C_VERTICES + ('s',)
C_EDGES = ((1,2),(2,3),(3,1),(4,5),(0,2),(0,3),(0,4),(0,6))
X_EDGES = C_EDGES + ((7,4),(7,5),(7,6))
ATTACH = {1:(0,1),2:(1,),3:(1,),4:(2,),5:(2,3),6:(3,4)}
K = (4,5,6)

def proper(gamma):
    return all(gamma[i] != gamma[(i+1)%5] for i in range(5))

def canon(row):
    names = {}
    return tuple(names.setdefault(x,len(names)) for x in row)

def boundary_ok(f, gamma, attach=ATTACH):
    return all(f[v] != gamma[b] for v,bs in attach.items() for b in bs)

def semantic_calibration():
    rows = [r for r in itertools.product(COL,repeat=5) if proper(r)]
    c_internal = [f for f in itertools.product(COL,repeat=7) if all(f[a]!=f[b] for a,b in C_EDGES)]
    x_internal = [f for f in itertools.product(COL,repeat=8) if all(f[a]!=f[b] for a,b in X_EDGES)]
    certificate = []
    c_cache = {}
    for gamma in rows:
        U = [f for f in itertools.product(COL,repeat=3)
             if f[0]!=f[1] and f[1]!=f[2] and f[2]!=f[0]
             and f[0]!=gamma[0] and f[0]!=gamma[1]
             and f[1]!=gamma[1] and f[2]!=gamma[1]]
        P = [f for f in itertools.product(COL,repeat=2)
             if f[0]!=f[1] and f[0]!=gamma[2]
             and f[1]!=gamma[2] and f[1]!=gamma[3]]
        Q = [f for f in COL if f!=gamma[3] and f!=gamma[4]]
        joined_c = {(c,)+u+p+(q,) for c,u,p,q in itertools.product(COL,U,P,Q)
                    if u[1]!=c and u[2]!=c and p[0]!=c and q!=c}
        direct_c = {f for f in c_internal if boundary_ok(f,gamma)}
        assert joined_c == direct_c
        # All 4*64 root/contact fibres, including empty ones, keep full assignments.
        for c,t in itertools.product(COL,itertools.product(COL,repeat=3)):
            phi_join = {f for f in joined_c if f[0]==c and tuple(f[v] for v in K)==t}
            phi_direct = {f for f in direct_c if f[0]==c and tuple(f[v] for v in K)==t}
            assert phi_join == phi_direct
        joined_x = {f+(a,) for f in joined_c for a in COL
                    if a!=gamma[0] and a!=gamma[1] and all(f[v]!=a for v in K)}
        direct_x = {f for f in x_internal if boundary_ok(f,gamma)
                    and f[7]!=gamma[0] and f[7]!=gamma[1]}
        assert joined_x == direct_x
        joined_g = {f for f in joined_x if f[0]!=gamma[4]}
        direct_g = {f for f in direct_x if f[0]!=gamma[4]}
        assert joined_g == direct_g
        c_cache[gamma] = joined_c
        certificate.append({'gamma': gamma,'full_C_lifts': sorted(joined_c),
                            'full_X_lifts':sorted(joined_x),'full_G_lifts':sorted(joined_g)})
    # S4 changes every coordinate, including r, together with the boundary row.
    for gamma, lifts in c_cache.items():
        for perm in itertools.permutations(COL):
            renamed = tuple(perm[c] for c in gamma)
            assert {tuple(perm[c] for c in f) for f in lifts} == c_cache[renamed]
    # D5 changes every boundary label and attachment simultaneously; keep interior labels.
    for gamma in rows:
        for sign,shift in itertools.product((1,-1),range(5)):
            position = lambda b: (sign*b+shift)%5
            changed_gamma = [None]*5
            for b in range(5):
                changed_gamma[position(b)] = gamma[b]
            changed_attach = {v:tuple(position(b) for b in bs) for v,bs in ATTACH.items()}
            assert all(gamma[b] == changed_gamma[position(b)] for b in range(5))
            assert {f for f in c_internal if boundary_ok(f,changed_gamma,changed_attach)} == c_cache[gamma]
    # A specific joint pair whose product of marginals admits a fake r=0 lift.
    beta = (0,1,0,1,2)
    u_lifts = [f for f in itertools.product(COL,repeat=3)
               if len(set(f))==3 and f[0] in (2,3) and f[1] in (0,2,3) and f[2] in (0,2,3)]
    pairs = {(f[1],f[2]) for f in u_lifts}
    left = {a for a,b in pairs}; right = {b for a,b in pairs}
    exact_avoiding0 = {(a,b) for a,b in pairs if a!=0 and b!=0}
    marginal_avoiding0 = {(a,b) for a,b in itertools.product(left,right) if a!=0 and b!=0}
    assert not exact_avoiding0 and marginal_avoiding0
    assert len(rows)==240 and len({canon(g) for g in rows})==10
    return {'evidence_layer':'relation semantics calibration only; not a finite LOW2 source control',
            'graph_vertices_C':C_VERTICES,'graph_vertices_X':X_VERTICES,'C_edges':C_EDGES,
            'X_edges':X_EDGES,'boundary_attachments':ATTACH,'s_spokes':(0,1),'deleted_G_spoke':4,
            'source_contract_status':'No embedding, Sigma, rejecting minimality or source identity established',
            'proper_literal_rows':240,'canonical_rows':10,'all_ambient_root_contact_fibres_checked':240*4*64,
            'S4_row_actions':240*24,'whole_graph_D5_row_actions':240*10,
            'all_full_lifts':certificate,
            'marginal_negative':{'beta':beta,'U_full_lifts':u_lifts,'U_contact_pairs':sorted(pairs),
                                 'same_root_pin':0,'exact_avoiding0':sorted(exact_avoiding0),
                                 'marginal_avoiding0':sorted(marginal_avoiding0)}}

if __name__ == '__main__':
    from pathlib import Path
    result = semantic_calibration()
    p = Path(__file__).resolve().parent / 'calibration.json'
    with p.open('x') as fh:
        json.dump(result,fh,sort_keys=True,indent=2)
        fh.write('\n')
    print(json.dumps({k:result[k] for k in ('proper_literal_rows','canonical_rows','all_ambient_root_contact_fibres_checked','S4_row_actions','whole_graph_D5_row_actions')},sort_keys=True))
