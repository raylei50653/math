#!/usr/bin/env python3
"""Solver-free exact checker for fixed-split full Kempe orbit count cones."""
from collections import Counter
from fractions import Fraction as Q
from itertools import permutations, combinations, product
import argparse
import json
from pathlib import Path
from count_feasibility import inputs,algebra,HERE

CERT=HERE/'kempe_cone_certificate.json'


def norm(p):
    d={};return tuple(d.setdefault(c,len(d)) for c in p)


def generators(interface):
    literal=list(map(tuple,interface['literal_assignments']))
    words=list(map(tuple,interface['pattern_order']));wi={p:i for i,p in enumerate(words)}
    group=[p for p in permutations(range(4)) if p[0]//2==p[1]//2 and p[2]//2==p[3]//2]
    assert len(group)==8
    canonical={p:min(tuple(g[c] for c in p) for g in group) for p in literal}
    states=sorted(set(canonical.values()));si={p:i for i,p in enumerate(states)}
    state_of={p:si[canonical[p]] for p in literal}
    sizes=Counter(state_of.values());pattern_of=[wi[norm(p)] for p in states]
    nc,active,rows=algebra(words)
    records={}
    for p in states:
        side=[c//2 for c in p]
        for part in nc:
            if any(part[a]==part[b] and side[a]!=side[b] for a,b in combinations(range(8),2)):continue
            if any(side[a]==side[(a+1)%8] and part[a]!=part[(a+1)%8] for a in range(8)):continue
            orbit=[]
            for bits in range(1<<(max(part)+1)):
                q=tuple(c^1 if bits>>part[a]&1 else c for a,c in enumerate(p))
                assert all(q[a]!=q[(a+1)%8] for a in range(8))
                orbit.append(q)
            assert len(set(orbit))==len(orbit)
            count=Counter(state_of[q] for q in orbit)
            col=tuple((s,8*n//sizes[s]) for s,n in sorted(count.items()))
            assert all(8*n%sizes[s]==0 for s,n in count.items())
            records.setdefault(col,{'literal_word':p,'component_partition':part,'complete_flip_orbit':orbit})
    cols=sorted(records)
    assert len(states)==821 and len(cols)==1552
    return states,pattern_of,[sizes[s] for s in range(len(states))],cols,[records[col] for col in cols],rows


def build():
    interface,queries=inputs()
    states,indices,sizes,columns,witnesses,rows=generators(interface)
    discovery=json.loads((HERE/'kempe_cone_discovery.json').read_text())
    assert discovery['columns']==json.loads(json.dumps(columns))
    result={'schema':'c8-exact-kempe-count-cone-v1','fixed_split':[[0,1],[2,3]],
            'states':states,'state_pattern_indices':indices,'state_orbit_sizes':sizes,
            'columns':columns,'column_witnesses':witnesses,'queries':[]}
    for expected,q in zip(queries,discovery['queries']):
        assert q['query_id']==expected['query_id'] and q['status']==0
        v=[Q(x).limit_denominator(1000000) for x in q['solution']]
        n=len(q['column_indices']);cs=v[n:]
        counts=[sum(c*a for c,a in zip(row,cs)) for row in rows]
        result['queries'].append({'query_id':q['query_id'],'support':expected['support'],
             'column_coefficients':[[j,str(z)] for j,z in zip(q['column_indices'],v[:n]) if z],
             'partition_coefficients':list(map(str,cs)),'counts':list(map(str,counts))})
    return json.loads(json.dumps(result))


def check(result,data=None):
    interface,queries=inputs()
    states,indices,sizes,columns,witnesses,rows=generators(interface) if data is None else data
    assert result['fixed_split']==[[0,1],[2,3]]
    assert result['states']==list(map(list,states))
    assert result['state_pattern_indices']==indices and result['state_orbit_sizes']==sizes
    assert result['columns']==json.loads(json.dumps(columns))
    assert result['column_witnesses']==json.loads(json.dumps(witnesses))
    assert [q['query_id'] for q in result['queries']]==[q['query_id'] for q in queries]
    cases={c['id']:c for c in interface['cases']}
    for expected,q in zip(queries,result['queries']):
        mask=expected['support'];assert q['support']==mask
        cs=list(map(Q,q['partition_coefficients']));counts=list(map(Q,q['counts']))
        assert len(cs)==91 and len(counts)==274
        assert counts==[sum(c*a for c,a in zip(row,cs)) for row in rows]
        assert all(x>0 if mask>>i&1 else x==0 for i,x in enumerate(counts))
        expansion=[Q(0)]*len(states);seen=set()
        for j,z in q['column_coefficients']:
            z=Q(z);assert z>0 and j not in seen;seen.add(j)
            assert all(mask>>indices[s]&1 for s,_ in columns[j])
            for s,c in columns[j]:expansion[s]+=c*z
        assert expansion==[counts[i] for i in indices]
        outer=[sum(Q(a)*b for a,b in zip(row,counts)) for row in cases[expected['case_id']]['transfer']]
        assert all(x>0 if expected['target']>>i&1 else x==0 for i,x in enumerate(outer))
    return {'status':'PASS','queries':8,'G8_states':821,'complete_switch_orbit_columns':1552,
            'full_support_sizes':[q['support'].bit_count() for q in queries],
            'nonzero_cone_coefficients':[len(q['column_coefficients']) for q in result['queries']],
            'arithmetic':'int/Fraction only'}


def controls(data):
    """Derive exact cone coefficients directly from four concrete disk graphs."""
    interface,_=inputs()
    states,indices,sizes,columns,_,_=data
    words=list(map(tuple,interface['pattern_order']))
    group=[p for p in permutations(range(4)) if p[0]//2==p[1]//2 and p[2]//2==p[3]//2]
    state_index={p:i for i,p in enumerate(states)}
    def state(p):return state_index[min(tuple(g[c] for c in p) for g in group)]
    col_index={col:i for i,col in enumerate(columns)}
    cycle=[(i,(i+1)%8) for i in range(8)]
    models=[('empty_C8',8,cycle),('fan_C8',8,cycle+[(0,i) for i in range(2,7)]),
            ('wheel_C8',9,cycle+[(8,i) for i in range(8)]),
            ('adjacent_two_hubs',10,cycle+[(8,9)]+[(8,i) for i in range(5)]
             +[(9,i) for i in [0,4,5,6,7]])]
    results=[]
    for name,n,edges in models:
        direct=[]
        for word in words:
            direct.append(sum(all(p[u]!=p[v] for u,v in edges)
                for tail in product(range(4),repeat=n-8) for p in [word+tail]))
        weights=Counter();adjs=[[] for _ in range(n)]
        for u,v in edges:adjs[u].append(v);adjs[v].append(u)
        for sides in product(range(2),repeat=n):
            parity={};blocks=[];ok=True
            for root in range(n):
                if root in parity:continue
                parity[root]=0;todo=[root];block=[]
                while todo:
                    u=todo.pop();block.append(u)
                    for v in adjs[u]:
                        if sides[v]!=sides[u]:continue
                        if v in parity:
                            if parity[v]==parity[u]:ok=False
                        else:parity[v]=1-parity[u];todo.append(v)
                blocks.append(block)
            if not ok:continue
            visible=[block for block in blocks if any(v<8 for v in block)]
            h=len(blocks)-len(visible)
            owner={v:j for j,block in enumerate(visible) for v in block if v<8}
            p=tuple(2*sides[v]+parity[v] for v in range(8))
            orbit=[tuple(c^1 if bits>>owner[v]&1 else c for v,c in enumerate(p))
                   for bits in range(1<<len(visible))]
            counts=Counter(state(q) for q in orbit)
            col=tuple((s,8*z//sizes[s]) for s,z in sorted(counts.items()))
            assert col in col_index
            weights[col_index[col]]+=Q(2**h,8)
        reconstructed=[Q(0)]*len(states)
        for j,z in weights.items():
            for s,c in columns[j]:reconstructed[s]+=c*z
        assert reconstructed==[direct[p] for p in indices]
        results.append({'name':name,'vertices':n,'edges':edges,'counts':direct,
                        'column_coefficients':[[j,str(z)] for j,z in sorted(weights.items())]})
    return json.loads(json.dumps(results))


def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--negative',action='store_true');a=p.parse_args()
    result=build() if a.write else json.loads(CERT.read_text())
    data=generators(inputs()[0]);receipt=check(result,data)
    actual_controls=controls(data)
    control_path=HERE/'kempe_cone_controls.json'
    if a.write:
        with control_path.open('x') as f:json.dump(actual_controls,f,sort_keys=True,separators=(',',':'));f.write('\n')
    else:assert json.loads(control_path.read_text())==actual_controls
    receipt['actual_graph_controls']=len(actual_controls)
    if a.negative:
        mutations=[lambda b:b['queries'][0]['column_coefficients'][0].__setitem__(1,'-1'),
                   lambda b:b['column_witnesses'][0]['complete_flip_orbit'].pop(),
                   lambda b:b['states'][0].__setitem__(0,3)]
        for mutation in mutations:
            bad=json.loads(json.dumps(result));mutation(bad)
            try:check(bad,data)
            except AssertionError:pass
            else:raise AssertionError('accepted corrupted certificate')
        receipt['negative_controls_rejected']=3
    if a.write:
        with CERT.open('x') as f:json.dump(result,f,sort_keys=True,separators=(',',':'));f.write('\n')
    print(json.dumps(receipt,sort_keys=True))

if __name__=='__main__':main()
