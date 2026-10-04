#!/usr/bin/env python3
"""Independent fixed actual-shape check after the cited cyclic lemma.
No repository imports, topology or colouring oracle; complete literal tuples.
Only the three classified K shapes with the original labelled r contact pair.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

U = set(range(4))
Q1, Q0 = (0,1,2,0,2), (0,1,2,1,2)
ROOT, X, Y = 5, 6, 7
SUPPORT = (0,2,3,4)
SHAPES = {
    'triangle': ((5,6),(6,7),(5,7)),
    'two_triangles_bridge_x': ((5,6),(6,7),(5,7),(6,8),(8,9),(9,10),(8,10)),
    'two_triangles_bridge_y': ((5,6),(6,7),(5,7),(7,8),(8,9),(9,10),(8,10)),
}


def literal(vertices, edges, attachments, row):
    out = []
    domains = [sorted(U - {row[b] for b in attachments[v]}) for v in vertices]
    for values in product(*domains):
        f = dict(zip(vertices, values))
        if all(f[a] != f[b] for a,b in edges):
            out.append(f)
    return out


def forbidden(colorings):
    assert colorings
    return set.intersection(*({f[X],f[Y]} for f in colorings))


def bag(start, vertices, cut_edges):
    reached = {start}
    while True:
        next_set = reached | {a for a,b in cut_edges if b in reached} | {b for a,b in cut_edges if a in reached}
        if next_set == reached:
            return tuple(sorted(reached))
        reached = next_set


def build():
    summary, witnesses = {}, []
    for name, hedge in SHAPES.items():
        cvertices = tuple(sorted({v for e in hedge for v in e} - {ROOT}))
        cedges = tuple(e for e in hedge if ROOT not in e)
        cut = tuple(e for e in cedges if set(e) != {X,Y})
        bx, by = bag(X,cvertices,cut), bag(Y,cvertices,cut)
        assert set(bx).isdisjoint(by) and set(bx)|set(by) == set(cvertices)
        options = [tuple(combinations(SUPPORT,4-sum(v in e for e in hedge))) for v in cvertices]
        count = Counter()
        f0_counts = Counter()
        for choices in product(*options):
            count['attachment_assignments'] += 1
            at = dict(zip(cvertices,choices))
            # A rejecting q1/root=1 degree assignment must be tight at every vertex.
            if any(len({Q1[b] for b in at[v]} | ({1} if v in (X,Y) else set())) != len(at[v])+(v in (X,Y)) for v in cvertices):
                continue
            count['q1_local_tight_assignments'] += 1
            rows1 = literal(cvertices,cedges,at,Q1)
            if forbidden(rows1) != {1,3}:
                continue
            count['exact_q1_pair_assignments'] += 1
            rows0 = literal(cvertices,cedges,at,Q0)
            f0 = forbidden(rows0)
            f0_counts[','.join(map(str,sorted(f0)))] += 1
            ex1 = {f[X] for f in literal(bx,tuple(e for e in cut if set(e)<=set(bx)),at,Q1)}
            ey1 = {f[Y] for f in literal(by,tuple(e for e in cut if set(e)<=set(by)),at,Q1)}
            assert ex1 == ey1 == {1,3}
            ex0 = {f[X] for f in literal(bx,tuple(e for e in cut if set(e)<=set(bx)),at,Q0)}
            ey0 = {f[Y] for f in literal(by,tuple(e for e in cut if set(e)<=set(by)),at,Q0)}
            if 1 in f0:
                # These are the two rejecting assignments needed by the carrier proof.
                count['two_root1_rejecting_assignments'] += 1
                assert 3 in ex0 and 3 in ey0
                assert ex0-{1} == ey0-{1} == {3}
                assert 3 in f0
            assert not (len(f0)==1 and 3 not in f0)
            if not any(w['shape']==name for w in witnesses):
                witnesses.append(dict(shape=name,original_H_edges=hedge,root_spokes=(0,2),
                    original_C_vertices=cvertices,original_C_edges=cedges,
                    actual_boundary_attachments=at,original_contact_order=(X,Y),
                    q1_complete_ordered_relation=sorted({(f[X],f[Y]) for f in rows1}),
                    q0_complete_ordered_relation=sorted({(f[X],f[Y]) for f in rows0}),
                    q1_forbidden=[1,3],q0_forbidden=sorted(f0),
                    original_bag_x=bx,original_bag_y=by,
                    q1_exact_E_x=sorted(ex1),q1_exact_E_y=sorted(ey1),
                    q0_exact_E_x=sorted(ex0),q0_exact_E_y=sorted(ey0),
                    source_disk_realizability_asserted=False))
        summary[name]=dict(counts=dict(count),q0_forbidden_distribution=dict(sorted(f0_counts.items())))
    return dict(scope='Post-cyclic-lemma actual K shapes only; attachments allowed anywhere in the long envelope 2340; no disk or T4 filter is imposed, so this is an over-domain.',
        q1=Q1,q0=Q0,unused_D=3,root_spokes=(0,2),summary=summary,witnesses=witnesses,
        no_q2_q4_role_used=True,repository_checker_imports=False,arbitrary_size_scope='Supplied by the cited structural lemma, not by this probe.')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
    out=Path(__file__).with_suffix('.json')
    result=build();payload=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.check:
        assert out.read_bytes()==payload.encode()
    else:
        with out.open('x') as f:f.write(payload)
    print(json.dumps(result['summary'],sort_keys=True))

if __name__=='__main__':main()
