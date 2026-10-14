#!/usr/bin/env python3
"""Finite, same-graph matching exploration; not a 933/941 exclusion proof."""
import argparse
from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_name("results.json")
sys.path.insert(0, str(ROOT / "scripts"))
import networkx as nx
from c5_edge_states import corpus, Dual, TYPE_PAIRS
from c5_kempe_connectivity import adjacency
from c5_kempe_screen import normalize
from c5_complementary_cube import singleton_distances, singleton_of
from c5_b5_face import poles, edge_counts

def matching_sector(dual,pair):
    ends=dual.ends; n=dual.f
    active=set(range(n+5))-{n+i for i in pair}
    inc={v:[] for v in active}
    for ei,(u,v) in enumerate(ends):
        if u in active and v in active:
            inc[u].append((v,ei));inc[v].append((u,ei))
    ans=[]
    def rec(rem,ms):
        if not rem:
            adj=[[] for _ in range(n+5)]
            for ei,(u,v) in enumerate(ends):
                if ei not in ms:
                    adj[u].append((v,ei));adj[v].append((u,ei))
            unseen={v for v in range(n+5) if adj[v]};lens=[];paths=[]
            while unseen:
                root=min(unseen);unseen.remove(root);queue=[root];es=set()
                for u in queue:
                    for v,ei in adj[u]:
                        es.add(ei)
                        if v in unseen:unseen.remove(v);queue.append(v)
                if any(v>=n for v in queue):paths.append(len(es))
                else:lens.append(len(es))
            assert len(paths)==1
            good=all(x%2==0 for x in lens) and paths[0]%2==0
            ans.append(dict(matching=sorted(ms),cycles=sorted(lens),path_edges=paths[0],good=good,weight=2**len(lens) if good else 0))
            return
        u=min(rem,key=lambda u:sum(v in rem for v,_ in inc[u]))
        for v,ei in inc[u]:
            if v in rem:rec(rem-{u,v},ms|{ei})
    rec(active,set())
    return ans

def metric(dual,c):
    w=tuple(c[i]^c[(i+1)%5] for i in range(5));major=Counter(w).most_common(1)[0][0]
    idx=TYPE_PAIRS.index(tuple(x for x in (1,2,3) if x!=major))
    return sum(not t for t,_ in dual.systems(c)[idx])

def one_component(dual,sd):
    vs={v for ei in sd for v in dual.ends[ei]}
    if not vs:return False
    conn=set();todo=[next(iter(vs))]
    while todo:
        u=todo.pop()
        if u in conn:continue
        conn.add(u)
        for ei in sd:
            a,b=dual.ends[ei]
            if a==u:todo.append(b)
            if b==u:todo.append(a)
    return conn==vs

def phase_compatible(dual,M,N):
    sd=M^N;inc=defaultdict(list)
    for ei,(u,v) in enumerate(dual.ends):
        if ei not in M:inc[u].append(ei);inc[v].append(ei)
    unseen=set(range(len(dual.ends)))-set(M)
    while unseen:
        e=min(unseen);par={e:0};q=[e];unseen.remove(e)
        for a in q:
            for v in dual.ends[a]:
                for b in inc[v]:
                    if b==a:continue
                    if b not in par:par[b]=1-par[a];unseen.discard(b);q.append(b)
                    else:assert par[b]!=par[a]
        if len({par[e] for e in sd if e in par})>1:return False
    return True

def integrate(g, edges, types):
    pads=[[] for _ in range(g['n'])]
    for ei,(u,v) in enumerate(edges):
        pads[u].append((v,ei));pads[v].append((u,ei))
    restored=[None]*g['n'];restored[0]=0;queue=[0]
    for u in queue:
        for v,ei in pads[u]:
            z=restored[u]^types[ei]
            if restored[v] is None:restored[v]=z;queue.append(v)
            else:assert restored[v]==z
    assert all(x is not None for x in restored)
    assert all(restored[u]!=restored[v] for u,v in edges)
    return tuple(restored)


def restore_matching(g, dual, matching, pair):
    matching=set(matching)
    edgecolors=[1 if i in matching else None for i in range(len(dual.ends))]
    inc=defaultdict(list)
    for i,(u,v) in enumerate(dual.ends):inc[u].append(i);inc[v].append(i)
    for v in range(dual.f):assert sum(i in matching for i in inc[v])==1
    first=inc[dual.f+pair[0]][0]
    for root in [first]+list(range(len(dual.ends))):
        if edgecolors[root] is not None:continue
        edgecolors[root]=2;q=[root]
        for i in q:
            for v in dual.ends[i]:
                for j in inc[v]:
                    if j in matching or j==i:continue
                    c=5-edgecolors[i]
                    if edgecolors[j] is None:edgecolors[j]=c;q.append(j)
                    else:assert edgecolors[j]==c
    assert all({edgecolors[i] for i in inc[v]}=={1,2,3} for v in range(dual.f))
    assert [edgecolors[inc[dual.f+p][0]] for p in pair]==[2,3]
    c=integrate(g,dual.edges,edgecolors)
    return dict(edge_colors=edgecolors,full_primal_coloring=c,boundary=c[:5])


def probe(g):
    edges=sorted(tuple(e) for e in g['edges'])
    dual=Dual(g['n'],edges,g['faces']);adj=adjacency(g['n'],edges)
    colors,old_dist,_=singleton_distances(adj,g['n']);colors=sorted(colors)
    counts=Counter(c[:5] for c in colors)
    sectors={};states=[];raw=0
    for pair in combinations(range(5),2):
        ms=matching_sector(dual,pair);sectors[pair]=ms;raw+=len(ms)
        w=[1]*5;w[pair[0]]=2;w[pair[1]]=3;b=[0]
        for x in w[:-1]:b.append(b[-1]^x)
        assert sum(m['weight'] for m in ms)==counts[normalize(b)]
        for m in ms:
            if m['good']:states.append((pair,frozenset(m['matching']),len(m['cycles'])))
    neighbors=[[] for _ in states];incompatible=0
    for i,j in combinations(range(len(states)),2):
        if one_component(dual,states[i][1]^states[j][1]):
            neighbors[i].append(j);neighbors[j].append(i)
            incompatible+=not phase_compatible(dual,states[i][1],states[j][1])
    forbidden={(0,1),(2,3),(3,4)}
    q=deque(i for i,s in enumerate(states) if s[0] in forbidden)
    dist={i:0 for i in q};step={}
    while q:
        i=q.popleft()
        for j in neighbors[i]:
            if j not in dist:dist[j]=dist[i]+1;step[j]=i;q.append(j)
    starts=[i for i,s in enumerate(states) if s[0]==(2,4)]
    # The loop-monotonicity negative control uses every individual dual
    # bichromatic component, including closed components.
    loops={c:metric(dual,c) for c in colors};cn={c:set() for c in colors}
    for c in colors:
        initial=[c[u]^c[v] for u,v in edges]
        for pair,parts in zip(TYPE_PAIRS,dual.systems(c)):
            for terminals,swap_edges in parts:
                types=initial[:]
                for ei in swap_edges:types[ei]=pair[0]^pair[1]^types[ei]
                d=normalize(integrate(g,edges,types));assert d in loops
                cn[c].add(d)
    reached={c for c in colors if singleton_of(c) not in (None,0,2)}
    q=deque(sorted(reached))
    while q:
        c=q.popleft()
        for d in sorted(cn[c]):
            if d not in reached and loops[d]>=loops[c]:reached.add(d);q.append(d)
    failures=[c for c in colors if c in old_dist and c not in reached]
    zero_safe=[c for c in colors if len(set(c[:5]))==4 and loops[c]==0 and old_dist.get(c,0)>1]
    row=dict(name=g['name'],primal_vertices=g['n'],dual_vertices=dual.f,
             full_colorings=len(colors),raw_matchings=raw,good_matchings=len(states),
             matching_edges=sum(map(len,neighbors))//2,phase_incompatible_edges=incompatible,
             key_sector_starts=len(starts),key_sector_unreachable=sum(i not in dist for i in starts),
             key_sector_max_distance=max((dist.get(i,-1) for i in starts),default=0),
             nonincreasing_loop_escape_failures=len(failures),zero_loop_safe_states=len(zero_safe))
    detail=None
    if g['name']=='survivor-590':
        assert len(starts)==1 and dist[starts[0]]==1
        i=starts[0];j=step[i];a=states[i];b=states[j]
        detail=dict(name=g['name'],primal_edges=edges,oriented_faces=g['faces'],dual_edges=dual.ends,
                    before_pair=a[0],after_pair=b[0],before_matching=sorted(a[1]),after_matching=sorted(b[1]),
                    symmetric_difference=sorted(a[1]^b[1]),before_cycles=a[2],after_cycles=b[2],
                    phase_compatible=phase_compatible(dual,a[1],b[1]),
                    before=restore_matching(g,dual,a[1],a[0]),after=restore_matching(g,dual,b[1],b[0]))
        assert len(detail['symmetric_difference'])==20
        assert not detail['phase_compatible']
    negative=None
    if g['name']=='catalogue-199':
        c=next(c for c in failures if loops[c]==0)
        negative=dict(name=g['name'],primal_edges=edges,oriented_faces=g['faces'],coloring=c,
                      loops=loops[c],unrestricted_distance=old_dist[c],
                      successors=[dict(coloring=d,loops=loops[d],forbidden=singleton_of(d) not in (None,0,2))
                                  for d in sorted(cn[c])])
    odd=None
    if g['name']=='catalogue-189':
        for m in sectors[0,3]:
            if not m['good']:continue
            for n in sectors[3,4]:
                sd=set(m['matching'])^set(n['matching'])
                if not n['good'] and one_component(dual,sd):
                    odd=dict(name=g['name'],primal_edges=edges,oriented_faces=g['faces'],dual_edges=dual.ends,
                             before_pair=(0,3),after_pair=(3,4),before=m,after=n,switch_edges=sorted(sd))
                    break
            if odd:break
        assert odd and odd['after']['cycles']==[5]
    return row,detail,negative,odd


def wheel_negative():
    pole=poles()[10]
    counts=edge_counts(pole)
    family={frozenset(i for i,c in enumerate(w) if c==1) for w,n in counts.items() if n}
    a=frozenset((0,3,4));b=frozenset((0,1,2));x=2
    assert a in family and b in family and x in a^b
    candidates=[dict(y=y,result=sorted(a^{x,y}),feasible=(a^{x,y}) in family) for y in sorted(a^b)]
    assert not any(c['feasible'] for c in candidates)
    return dict(pole=pole,family=sorted(sorted(s) for s in family),A=sorted(a),B=sorted(b),x=x,
                symmetric_exchange_candidates=candidates,
                scope='Real plane pentagon 5-pole. Even-complement color-class family is not a delta-matroid.')


def report():
    assert nx.__version__=='3.5', 'Pin NetworkX 3.5 for deterministic embedding replay'
    rows=[];special={}
    for g in corpus():
        if not g['faces'] or g['name'].startswith('errera'):continue
        row,detail,negative,odd=probe(g);rows.append(row)
        for key,value in [('survivor_matching_exchange',detail),('loop_monotonicity_negative',negative),('odd_cycle_exchange_negative',odd)]:
            if value:special[key]=value
    summable=('full_colorings','raw_matchings','good_matchings','matching_edges','phase_incompatible_edges',
              'key_sector_starts','key_sector_unreachable','nonincreasing_loop_escape_failures','zero_loop_safe_states')
    summary={key:sum(r[key] for r in rows) for key in summable}
    summary.update(graphs=len(rows),fixed_fibres=10*len(rows),key_sector_max_distance=max(r['key_sector_max_distance'] for r in rows))
    assert summary['graphs']==79 and summary['fixed_fibres']==790
    assert summary['full_colorings']==1351 and summary['raw_matchings']==2109 and summary['good_matchings']==868
    assert summary['key_sector_starts']==68 and summary['key_sector_unreachable']==0 and summary['key_sector_max_distance']==2
    assert summary['nonincreasing_loop_escape_failures']==229 and summary['zero_loop_safe_states']==107
    inputs=['scripts/c5_edge_states.py','scripts/c5_kempe_connectivity.py','scripts/c5_kempe_screen.py',
            'scripts/c5_complementary_cube.py','scripts/c5_b5_face.py','scripts/c5_ab_swap_cube.py',
            'artifacts/c5_cells/cells.json','artifacts/c5_cells/corner_disks.json','artifacts/c5_cells/complementary_cube.json']
    return dict(scope='Finite exploratory controls; not a 933/941 source exclusion, not a proof of exchange connectivity.',
                networkx=nx.__version__,source_sha256={p:sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},
                summary=summary,graphs=rows,examples=special,wheel_delta_matroid_negative=wheel_negative())


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=report();payload=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    if args.check:assert OUT.read_text()==payload, 'Saved exploratory result mismatch'
    else:OUT.write_text(payload)
    print(json.dumps(result['summary'],sort_keys=True))
