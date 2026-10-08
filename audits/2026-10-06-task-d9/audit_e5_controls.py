#!/usr/bin/env python3
"""D9 E5 / E6 D-G independent finite controls; imports no repository module.

Only frozen named input graphs are coloured. No producer lemma/decision fields
are read. Exact source premises and generic intermediate mechanisms have
separate three-way results. Colourings are exhaustive complete assignments,
never contact marginals or a four-colour-theorem oracle.
"""
from pathlib import Path
from itertools import product, combinations
from functools import lru_cache
import argparse, hashlib, json

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name('e5_controls.json')
B = tuple(range(5))
FRAME = frozenset(tuple(sorted((i,(i+1)%5))) for i in B)
QROWS = ((0,1,2,1,2),(0,1,2,0,2),(0,1,2,0,1),(0,1,0,2,1),(0,1,0,1,2))
TRIPLE = (0,1,3)


def restricted(rowsize=5):
    ans=[]
    for p in product(range(4), repeat=rowsize):
        if p[0] != 0 or any(p[i]>1+max(p[:i]) for i in range(1,rowsize)): continue
        if all(p[i]!=p[(i+1)%rowsize] for i in range(rowsize)): ans.append(p)
    return tuple(ans)
ROWS=restricted()
QIND=tuple(ROWS.index(q) for q in QROWS)
T4=tuple(i for i,q in enumerate(ROWS) if len(set(q))==4)


def canon(p):
    names={};return tuple(names.setdefault(c,len(names)) for c in p)


def adjacent_pair(q):
    return len(q)<=1 or (len(q)==2 and (q[1]-q[0])%5 in (1,4))


def neighbours(vertices,edges):
    ns={v:set() for v in vertices}
    for u,v in edges: ns[u].add(v);ns[v].add(u)
    return ns


def components(vertices,ns):
    todo=set(vertices); ans=[]
    while todo:
        comp={todo.pop()}; stack=list(comp)
        while stack:
            v=stack.pop()
            for w in ns[v] & todo: todo.remove(w);comp.add(w);stack.append(w)
        ans.append(tuple(sorted(comp)))
    return sorted(ans)


@lru_cache(maxsize=None)
def colourings(vertices,edges,beta):
    ns=neighbours(vertices,edges); fixed={i:beta[i] for i in B}
    if any(fixed[u]==fixed[v] for u,v in edges if u in fixed and v in fixed): return ()
    remain=set(vertices)-set(B); answers=[]
    def dfs():
        if not remain:
            answers.append(tuple(fixed[v] for v in vertices));return
        legal={v:tuple(c for c in range(4) if all(fixed.get(w)!=c for w in ns[v])) for v in remain}
        v=min(remain,key=lambda w:(len(legal[w]),-len(ns[w]),w))
        remain.remove(v)
        for c in legal[v]: fixed[v]=c;dfs()
        fixed.pop(v,None);remain.add(v)
    dfs();return tuple(sorted(answers))


def sigma(vertices,edges):
    return sum((bool(colourings(vertices,edges,beta))<<i) for i,beta in enumerate(ROWS))


def qset(mask): return tuple(i for i,j in enumerate(QIND) if not mask & (1<<j))


def subgraph(vertices,edges,keep):
    vv=tuple(sorted(set(B)|set(keep)))
    return vv,tuple(e for e in edges if e[0] in vv and e[1] in vv)


def face_walk(rotation):
    todo={(v,w) for v in rotation for w in rotation[v]}; faces=[]
    while todo:
        dart=min(todo);start=dart; face=[]
        while True:
            if dart not in todo: raise AssertionError('rotation walk reused dart')
            todo.remove(dart);face.append(dart)
            u,v=dart; around=rotation[v];dart=(v,around[(around.index(u)-1)%len(around)])
            if dart==start:break
        faces.append(face)
    return faces


def shield(piece,vertices,edges,rotation):
    outside=set(vertices)-set(B)-set(piece)
    kp=set(B)|set(piece)
    rr={v:tuple(w for w in rotation[v] if w in kp) for v in kp}
    faces=face_walk(rr)
    containing=[]
    for u in piece:
        for v in rotation[u]:
            if v in outside:
                around=rotation[u]; pos=around.index(v)
                # The next surviving neighbour locates the face sector.
                nextw=next(around[(pos+k)%len(around)] for k in range(1,len(around)+1) if around[(pos+k)%len(around)] in kp)
                containing.append(next(i for i,f in enumerate(faces) if (u,nextw) in f))
    assert containing and len(set(containing))==1
    face=faces[containing[0]]
    visible={tuple(sorted(e)) for e in face if tuple(sorted(e)) in FRAME}
    return tuple(sorted(FRAME-visible))


def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def result(trigger,ok=True,**evidence):
    return {'status':'triggered and holds' if trigger and ok else 'counterexample' if trigger else 'not triggered',**evidence}


def evaluate(path, ident, family):
    raw=json.loads(path.read_text());edges=tuple(sorted(tuple(e) for e in raw['canonical_edges']))
    vertices=tuple(sorted({v for e in edges for v in e}));ns=neighbours(vertices,edges)
    rotation={int(v):tuple(ws) for v,ws in raw['embedding']['disk_rotation'].items()}
    assert set(rotation)==set(vertices) and all(set(rotation[v])==ns[v] for v in vertices)
    faces=face_walk(rotation)
    assert len(vertices)-len(edges)+len(faces)==2
    assert any(set(e[0] for e in f)==set(B) and len(f)==5 for f in faces)
    mask=sigma(vertices,edges);q=qset(mask)
    assert mask==raw['sigma_mask']
    assert {e for e in edges if e[0] in B and e[1] in B}==set(FRAME)
    assert len(components(set(vertices)-set(B),ns))==1 and q
    assert all(mask&(1<<i) for i in T4)
    roots=tuple(v for v in vertices if v not in B and len(ns[v])==5)
    assert len(roots)==2 and all(len(ns[v])==4 for v in vertices if v not in B and v not in roots)
    ad=tuple(sorted(roots)) in edges
    assert ad==(family=='AD')
    pcs=[]
    for comp in components(set(vertices)-set(B)-set(roots),ns):
        contacts={r:tuple(sorted(ns[r]&set(comp))) for r in roots}
        owners=tuple(r for r in roots if contacts[r]);support=tuple(sorted(set().union(*(ns[v]&set(B) for v in comp))))
        pcs.append({'vertices':comp,'owners':owners,'contacts':contacts,'support':support})
    mixed=[p for p in pcs if len(p['owners'])==2];unary=[p for p in pcs if len(p['owners'])==1]
    joins={}
    for i,beta in enumerate(ROWS):
        cc=colourings(vertices,edges,beta)
        joins[str(i)]={'count':len(cc),'full_tuple_sha256':digest(cc)}
    deletions=[]
    for e in edges:
        if e in FRAME:continue
        ee=tuple(x for x in edges if x!=e);sm=sigma(vertices,ee)
        assert sm!=mask and sm|mask==sm
        deletions.append({'edge':e,'sigma':sm,'Q':qset(sm)})
    generic={}
    generic['L1_proper_profile']=result(True,all(adjacent_pair(d['Q']) for d in deletions),maximal_proper=len(deletions),all_proper_edge_subsets=(1<<len(deletions))-1)
    generic['L1_all_four_profile']=result(False,checked_rejecting_all_four_cores=0,scope='Rejecting all-degree-four candidates retaining both original roots only; root-deletion cores not enumerated')
    allfour=[]
    # Saturation makes every original degree-four piece all-in/all-out.
    factors=[((r,h), (int(r==roots[0]),int(r==roots[1])),None) for r in roots for h in sorted(ns[r]&set(B))]
    for index,p in enumerate(pcs):factors.append((None,tuple(len(p['contacts'][r]) for r in roots),index))
    for bits in product((0,1),repeat=len(factors)):
        if tuple(sum(factors[j][1][i]*bits[j] for j in range(len(factors))) for i in range(2))!=(1,1):continue
        removed=set();deleted_edges=set()
        for j,b in enumerate(bits):
            if not b:continue
            edge,_,index=factors[j]
            if edge is not None:deleted_edges.add(tuple(sorted(edge)))
            else:removed.update(pcs[index]['vertices'])
        vv,ee=subgraph(vertices,edges,set(vertices)-set(removed))
        ee=tuple(e for e in ee if e not in deleted_edges)
        nn=neighbours(vv,ee)
        if any(len(nn[v])!=4 for v in vv if v not in B):continue
        sm=sigma(vv,ee);qq=qset(sm)
        if not qq:continue
        allfour.append({'omitted_factors':[j for j,b in enumerate(bits) if b], 'vertices':vv,'edges':ee,'sigma':sm,'Q':qq})
        generic['L1_all_four_profile']['status']='counterexample' if len(qq)>1 or generic['L1_all_four_profile']['status']=='counterexample' else 'triggered and holds'
    generic['L1_all_four_profile']['checked_rejecting_all_four_cores']=len(allfour)
    generic['L1_all_four_profile']['core_payload_sha256']=digest(allfour)
    generic['L2_retained_mixed_incidence']=result(ad and bool(allfour),all(all(len(ns[r]&set(p['vertices']))==1 for r in roots) for c in allfour for p in mixed if set(p['vertices'])<=set(c['vertices'])),rejecting_all_four_core_count=len(allfour))
    j2_checks=[]
    for a,b in (roots,tuple(reversed(roots))):
        sa=tuple(sorted(ns[a]&set(B)));sb=tuple(sorted(ns[b]&set(B)))
        j2=ad and len(sa)==3 and len(sb)==2 and len(mixed)==1 and len(unary)==1 and all(len(mixed[0]['contacts'][r])==1 for r in roots) and unary[0]['owners']==(b,) and len(unary[0]['contacts'][b])==1
        if j2:
            for j in sa:
                ee=tuple(e for e in edges if e!=tuple(sorted((a,j))))
                sm=sigma(vertices,ee);j2_checks.append({'a':a,'b':b,'spoke':j,'sigma':sm,'Q':qset(sm)})
    generic['L3_J2_single_omission']=result(bool(j2_checks),all(len(c['Q'])<=1 for c in j2_checks),queries=j2_checks,scope='Weakened structural mechanism; selected triple not required by these control evaluations')
    endpoint_checks=[];membership_checks=[]
    for p in unary:
        vv,ee=subgraph(vertices,edges,p['vertices']);contact=p['contacts'][p['owners'][0]];ix=[vv.index(v) for v in contact]
        if len(p['support'])==3 and components(set(vertices)-set(B)-set(p['vertices']),ns) and len(components(set(vertices)-set(B)-set(p['vertices']),ns))==1 and set().union(*(ns[v]&set(B) for v in vertices if v not in B))==set(B):
            arc=next((tuple((h+k)%5 for k in range(3)) for h in B if set((h+k)%5 for k in range(3))==set(p['support'])),None)
            assert arc
            for row,beta in enumerate(ROWS):
                cc=colourings(vv,ee,beta);assert cc
                ff=set.intersection(*(set(t[i] for i in ix) for t in cc))
                endpoint_checks.append({'piece':p['vertices'],'row':row,'F':sorted(ff),'end_colours':[beta[arc[0]],beta[arc[2]]], 'full_relation_sha256':digest(cc)})
        if len(contact)==1:
            records=[]
            for row,beta in enumerate(ROWS):
                if len(set(beta))!=3:continue
                cc=colourings(vv,ee,beta);assert cc
                ff=set.intersection(*(set(t[i] for i in ix) for t in cc))
                for d in sorted(ff):records.append({'row':row,'owner_colour':d,'contact_contains_3':d!=3})
            if len(records)>=2:
                membership_checks.append({'piece':p['vertices'],'refusals':records,'holds':len({r['contact_contains_3'] for r in records})<=1})
    generic['E6_F_endpoint']=result(bool(endpoint_checks),all(not set(c['F'])&set(c['end_colours']) for c in endpoint_checks),query_count=len(endpoint_checks),queries=endpoint_checks)
    generic['E6_G_unused_membership']=result(bool(membership_checks),all(c['holds'] for c in membership_checks),components=membership_checks)
    full=ad and set(TRIPLE)<=set(q)
    exact={name:result(full) for name in ('L1','L2_J2','L2_J3_binary','L2_J3_ternary','L3','L4','L5','L6','L7','L8','G2_exact_two','G3_named_support','G4_exact_three','no_mixed')}
    # Every exact triple source is absent in this supplied control collection;
    # reject silently treating untriggered scope as independently verified.
    assert not full
    return {'id':ident,'family':family,'source':str(path.relative_to(ROOT)),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'vertices':vertices,'edges':edges,'rotation':rotation,'root_order':roots,'Q':q,'sigma':mask,'full_relations':joins,'pieces':pcs,'m':len(mixed),'u':len(unary),'exact_E5_family':exact,'generic_mechanisms':generic,'rejecting_all_four_cores':allfour}


def arithmetic():
    branches={}
    for name,qs in [('941',(0,1,3)),('933',(0,1,2,3)),('940',(0,1,3,4)),('932',(0,1,2,3,4))]:
        mask=1023-sum(1<<QIND[i] for i in qs)
        assert mask==int(name)
        necessary=[]; queries=[]
        for ss in combinations(B,3):
            ds={j:[i for i in qs if any(QROWS[i][j]==QROWS[i][k] for k in ss if j!=k)] for j in ss}
            queries.append({'S':ss,'D':ds})
            if all(len(d)<=1 for d in ds.values()):necessary.append(ss)
        branches[name]={'Q':qs,'mask':mask,'necessary_S_a':necessary,'all_ten_queries':queries}
    phi=(1,0,4,3,2);transports=[]
    for i,row in enumerate(ROWS):
        literal=tuple(row[phi[j]] for j in B)
        transports.append({'row':i,'literal':literal,'canonical_row':ROWS.index(canon(literal))})
    cols=[tuple(QROWS[q][i] for q in TRIPLE) for i in B]
    esigs=[tuple(tuple(sorted((QROWS[q][i],QROWS[q][(i+1)%5]))) for q in TRIPLE) for i in B]
    assert len(set(cols))==5 and len(set(esigs))==5
    assert all(any(QROWS[q][i]==QROWS[q][j] for q in TRIPLE) for i,j in combinations(B,2) if tuple(sorted((i,j))) not in FRAME)
    assert all(any(len({QROWS[q][i] for i in ss})<3 for q in TRIPLE) for ss in combinations(B,3))
    nonempty=[frozenset(c for c in range(4) if mask&(1<<c)) for mask in range(1,16)]
    guards=[{'P':sorted(p),'R':sorted(r)} for p in nonempty for r in nonempty if not any(a!=u for a in p for u in r)]
    assert guards==[{'P':[c],'R':[c]} for c in range(4)]
    g3=[]
    for arc in ((0,1,2),(1,2,3),(4,0,1),(3,4,0)):
        h0,h1,h2=arc
        q=next(q for q in TRIPLE if QROWS[q][h0]==QROWS[q][h2])
        beta=QROWS[q];c=beta[h0];r=beta[h1]
        gap=(h2,(h2+1)%5,(h2+2)%5,h0)
        supports=[gap[:3],gap[1:]]
        keep=[ss for ss in supports if beta[ss[1]]==r and r not in (beta[ss[0]],beta[ss[2]])]
        assert len(keep)==1
        g3.append({'S_a':sorted(arc),'q':q,'S_U':sorted(keep[0]),'b_spoke':sorted((h0,h2))})
    assert g3==[{'S_a':[0,1,2],'q':3,'S_U':[0,3,4],'b_spoke':[0,2]}, {'S_a':[1,2,3],'q':0,'S_U':[0,3,4],'b_spoke':[1,3]}, {'S_a':[0,1,4],'q':3,'S_U':[1,2,3],'b_spoke':[1,4]}, {'S_a':[0,3,4],'q':1,'S_U':[1,2,3],'b_spoke':[0,3]}]
    nm={}
    for name,branch in branches.items():
        candidates=[]
        for start in B:
            side=tuple((start+i)%5 for i in range(4))
            for uarc in (side[:3],side[1:]):
                spokes=tuple(sorted((set(side)-{uarc[1]})))
                ds=[tuple(q for q in branch['Q'] if any(QROWS[q][j]==QROWS[q][k] for k in spokes if k!=j)) for j in spokes]
                if all(adjacent_pair(d) for d in ds):candidates.append({'S_r':spokes,'S_U':tuple(sorted(uarc))})
        nm[name]=candidates
    assert nm['941']==[{'S_r':(0,1,3),'S_U':(1,2,3)},{'S_r':(0,1,3),'S_U':(0,3,4)}]
    assert not nm['933'] and not nm['940'] and not nm['932']
    # Same finite C5 root skeleton as E5:270-273; paths are actual edges,
    # exclude the other root, and intersect only at the named boundary h.
    root_routes=[]
    def paths(adj,start,end,avoid):
        found=[]
        def walk(path):
            if path[-1]==end:found.append(tuple(path));return
            for w in sorted(adj[path[-1]]-set(path)-{avoid}):walk(path+[w])
        walk([start]);return found
    for sa in (tuple(sorted((i,(i+1)%5))) for i in B):
        for sb in (tuple(sorted((i,(i+1)%5))) for i in B):
            if sa==sb:continue
            ee=tuple(FRAME)+tuple((5,h) for h in sa)+tuple((6,h) for h in sb)+((5,6),)
            adj=neighbours(B+(5,6),ee)
            for h in B:
                pairs=[(a,b) for a in paths(adj,5,h,6) for b in paths(adj,6,h,5) if set(a)&set(b)=={h}]
                assert pairs
                a,b=min(pairs,key=lambda pair:(len(pair[0])+len(pair[1]),pair))
                root_routes.append({'S_a':sa,'S_b':sb,'h':h,'a_route':a,'b_route':b})
    assert len(root_routes)==100
    return {'row_order':ROWS,'q_row_indices':QIND,'T4_indices':T4,'branches':branches,'reflection':phi,'full_literal_transports':transports,'column_signatures':cols,'edge_signatures':esigs,'singleton_guard':{'query_count':225,'empty_guard_cases':guards},'G3_literal_supports':g3,'no_mixed_three_spoke':nm,'L8_original_root_routes':root_routes}


def main():
    global ROOT, OUT
    ap=argparse.ArgumentParser()
    ap.add_argument('--check',action='store_true')
    ap.add_argument('--root',type=Path,default=ROOT)
    ap.add_argument('--output',type=Path,default=OUT)
    args=ap.parse_args()
    ROOT=args.root.resolve();OUT=args.output.resolve()
    inputs=[]
    for p in sorted((ROOT/'artifacts/c5_excess_two_e4c/controls').glob('NA*.json')):
        n=json.loads(p.read_text());inputs.append((ROOT/n['source'],n['id'],'NA'))
    for p in sorted((ROOT/'artifacts/c5_excess_two_finite_search').glob('AD_k*_validate/crit_orbits/orbit_*.json')):
        inputs.append((p,p.parent.parent.name+'/'+p.stem,'AD'))
    assert sum(f=='NA' for _,_,f in inputs)==54 and sum(f=='AD' for _,_,f in inputs)==9
    cases=[evaluate(*item) for item in inputs]
    stats={}
    for collection in ('exact_E5_family','generic_mechanisms'):
        stats[collection]={}
        for topic in cases[0][collection]:
            stats[collection][topic]={f:{s:sum(c['family']==f and c[collection][topic]['status']==s for c in cases) for s in ('triggered and holds','not triggered','counterexample')} for f in ('NA','AD')}
    payload={'baseline':'b2ca4520da50c9d2898ac6f8f966ac25df3f9609','scope':'54 NA and 9 AD frozen representatives; no additional source graphs; no imported producer decision logic','arithmetic':arithmetic(),'statistics':stats,'controls':cases}
    encoded=(json.dumps(payload,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
    if args.check:
        assert OUT.read_bytes()==encoded,'saved payload differs'
    else:
        with OUT.open('xb') as fh:fh.write(encoded)
    print(json.dumps({'controls':len(cases),'statistics':stats,'payload_sha256':hashlib.sha256(encoded).hexdigest()},sort_keys=True))

if __name__=='__main__':main()
