"""Full original-vertex assignment recurrence, not an existence/palette DP."""
from functools import lru_cache
import hashlib
from itertools import product
import json
from pathlib import Path

COLOURS=range(4)
LITERALS=['01012','01021','01023','01201','01202','01203','01212','01213','01231','01232']

def block_edges(block):
    vs=block['vertices']
    if block['type']=='bridge':
        assert len(vs)==2
        return [tuple(vs)]
    assert block['type']=='odd_cycle' and len(vs)>=3 and len(vs)%2==1
    assert len(set(vs))==len(vs)
    return list(zip(vs,vs[1:]+vs[:1]))

def actual_blocks(vertices,edges):
    """Tarjan original-edge biconnected blocks, including each bridge."""
    adj={v:[] for v in vertices}
    for i,(u,v) in enumerate(edges):
        adj[u].append((v,i)); adj[v].append((u,i))
    seen={}; low={}; stack=[]; result=[]
    def visit(u, parent_edge=None):
        seen[u]=low[u]=len(seen)
        for v,i in adj[u]:
            if i==parent_edge:
                continue
            if v not in seen:
                stack.append(i); visit(v,i); low[u]=min(low[u],low[v])
                if low[v]>=seen[u]:
                    piece=[]
                    while True:
                        j=stack.pop(); piece.append(tuple(sorted(edges[j])))
                        if j==i:
                            break
                    result.append(frozenset(piece))
            elif seen[v]<seen[u]:
                stack.append(i); low[u]=min(low[u],seen[v])
    visit('r')
    assert len(seen)==len(vertices),'C must be connected'
    return set(result)

def degree_findings(case):
    vs=case['vertices']; edges=case['original_edges']; sc=case['s_contacts']
    result=[]
    for v in vs:
        d=sum(v in e for e in edges); n=len(case['boundary_attachments'][v]); s=int(v in sc)
        if d+n+s!=4:
            result.append({'vertex':v,'deg_C':d,'boundary_attachment_count':n,
                           's_contact_incidence':s,'full_degree':d+n+s,'expected':4})
    return result

def validate_structure(case):
    vs=case['vertices']; edges=case['original_edges']; blocks=case['blocks']
    assert len(vs)==len(set(vs)) and 'r' in vs
    es=[tuple(sorted(e)) for e in edges]
    assert len(es)==len(set(es)) and all(len(set(e))==2 and set(e)<=set(vs) for e in edges)
    for v in vs:
        nb=case['boundary_attachments'][v]
        assert len(nb)==len(set(nb)) and all(b in ['b0','b1','b2','b3','b4'] for b in nb)
    supplied=[frozenset(tuple(sorted(e)) for e in block_edges(b)) for b in blocks]
    assert len(supplied)==len(set(supplied))
    assert set(supplied)==actual_blocks(vs,edges),'supplied decomposition is not actual original-edge blocks'
    assert sum(len(x) for x in supplied)==len(edges),'edge omitted or duplicated across blocks'
    assert case['original_e']==['r','b4'] and case['retained_r_spokes']==[] and case['t_r']==1
    assert case['boundary_attachments']['r']==[] and 'r' not in case['s_contacts']
    assert len(case['s_contacts'])==2 and len(set(case['s_contacts']))==2
    assert set(case['pieces']['L'])|set(case['pieces']['S'])==set(vs)-{'r'}
    assert not set(case['pieces']['L'])&set(case['pieces']['S'])
    rns={v if u=='r' else u for u,v in edges if 'r' in (u,v)}
    for i,piece in enumerate(['L','S']):
        pv=set(case['pieces'][piece]); assert case['s_contacts'][i] in pv
        assert case['r_contacts'][piece]==[v for v in case['pieces'][piece] if v in rns]
        assert len(case['r_contacts'][piece])==2
        assert {b for v in pv for b in case['boundary_attachments'][v]}==set(case['support_order'][piece])
        reach={next(iter(pv))}
        while True:
            more=reach|{w for u,v in edges for w,z in [(u,v),(v,u)] if z in reach and w in pv}
            if more==reach:
                break
            reach=more
        assert reach==pv
        assert all(not (u in pv and v not in pv|{'r'}) for u,v in edges)
        assert all(not (v in pv and u not in pv|{'r'}) for u,v in edges)
    root_blocks=[b for b in blocks if 'r' in b['vertices']]
    assert len(root_blocks)==2 and all(b['type']=='odd_cycle' for b in root_blocks)
    for v in vs:
        assert case['ownership'][v]==('root' if v=='r' else 'L' if v in case['pieces']['L'] else 'S')
        ns=[y if x==v else x for x,y in edges if v in (x,y)]+case['boundary_attachments'][v]
        if v in case['s_contacts']:
            ns.append('s')
        if v=='r':
            ns.append('b4')
        assert sorted(ns)==sorted(case['rotation'][v]),'rotation missing original neighbour at '+v
    assert case['disk_topology_verified'] is False

def full_assignments(case,literal):
    """Orient the all-vertex/block incidence tree at r; return every full map."""
    vs=case['vertices']; blocks=case['blocks']; gamma=list(map(int,literal))
    incidence={('v',v):[] for v in vs}
    for i,b in enumerate(blocks):
        node=('b',i); incidence[node]=[]
        for v in b['vertices']:
            incidence[node].append(('v',v)); incidence[('v',v)].append(node)
    parents={('v','r'):None}; children={}
    def orient(n):
        children[n]=[]
        for m in incidence[n]:
            if m==parents[n]:
                continue
            assert m not in parents,'block incidence is not a tree'
            parents[m]=n; children[n].append(m); orient(m)
    orient(('v','r'))
    assert set(parents)==set(incidence)
    def join(left,right):
        both=left.keys()&right.keys()
        assert all(left[v]==right[v] for v in both),'cutvertex colour disagreement'
        return {**left,**right}
    @lru_cache(None)
    def vertex(v,c):
        if any(c==gamma[int(b[1:])] for b in case['boundary_attachments'][v]):
            return ()
        assignments=[{v:c}]
        for _,i in children[('v',v)]:
            choices=block(i,c)
            assignments=[join(f,g) for f in assignments for g in choices]
        return tuple(assignments)
    @lru_cache(None)
    def block(i,c):
        b=blocks[i]; p=parents[('b',i)][1]
        bv=[v for v in b['vertices'] if v!=p]
        result=[]
        for colours in product(COLOURS,repeat=len(bv)):
            local={p:c,**dict(zip(bv,colours))}
            if any(local[u]==local[v] for u,v in block_edges(b)):
                continue
            parts=[local]
            for v in bv:
                parts=[join(f,g) for f in parts for g in vertex(v,local[v])]
            result.extend(parts)
        return tuple(result)
    maps=[f for c in COLOURS for f in vertex('r',c)]
    assert all(set(f)==set(vs) for f in maps),'original vertex omitted'
    vectors=sorted(tuple(f[v] for v in vs) for f in maps)
    assert len(vectors)==len(set(vectors)),'restriction/union duplicated a full assignment'
    return [list(f) for f in vectors]

def row_interface(case,literal):
    vs=case['vertices']; ri=vs.index('r'); ci=[vs.index(v) for v in case['s_contacts']]
    assignments=full_assignments(case,literal)
    ambient=[]
    for tau in product(COLOURS,repeat=2):
        for a in COLOURS:
            ambient.append({'tuple':list(tau),'r':a,'preimages':[f for f in assignments if f[ri]==a and [f[i] for i in ci]==list(tau)]})
    def pins(spokes=()):
        result=[]
        for a,b in product(COLOURS,repeat=2):
            good=[f for f in assignments if f[ri]==a and all(f[i]!=b for i in ci)]
            if any(b==int(literal[int(s[1:])]) for s in spokes):
                good=[]
            result.append({'r':a,'s':b,'preimages':good,'restored_preimages':good if a!=int(literal[4]) else []})
        return result
    return {'literal':literal,'assignments':assignments,'ambient_fibres':ambient,'pins':pins(),
            'spoke_variants':[{'s_spokes':spokes,'pins':pins(spokes)} for spokes in case['s_spoke_variants']]}

def calculate(path):
    path=Path(path); data=json.loads(path.read_text())
    assert data['literals']==LITERALS
    assert len(data['cases'])<=8 and all(len(c['vertices'])<=11 for c in data['cases'])
    records=[]; failures=[]
    for case in data['cases']:
        validate_structure(case)
        findings=degree_findings(case)
        assert bool(findings)==(not case['expected_valid']),'declared validity disagrees with degrees'
        if findings:
            failures.append({'case_id':case['id'],'findings':findings}); continue
        records.append({'case_id':case['id'],'vertices':case['vertices'],
                        'rows':[row_interface(case,row) for row in data['literals']]})
    return {'schema':1,'cases_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'cases':records,'failed_cases':failures,
            'target_source':{'executed':False,'trigger_count':None,'status':'not triggered'}}

def canonical(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
