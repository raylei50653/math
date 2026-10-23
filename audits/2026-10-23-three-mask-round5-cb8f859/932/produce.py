#!/usr/bin/env python3
"""Exclusive original zero-pair Q geometry and s=0 annulus certificate."""
import gzip,hashlib,itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2]
BASE='cb8f8593e273a7426ecadd59797a6e643cc4768e'
R4='audits/2026-10-23-three-mask-round4-cb8f859/932/'
R1='audits/2026-10-23-three-mask-methods-cb8f859/932/'
T2='audits/2026-10-13-c9-932-source-d521163/'
SRC=T2+'frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/c9/finite/certificate.v2.json.gz'

def norm(w):
    d={};return tuple(d.setdefault(c,len(d)) for c in w)
def bits(m):
    while m:
        b=m&-m;yield b.bit_length()-1;m-=b
def freeze():
    paths=[R4+p for p in ['REPORT.md','SOURCE_CONTRACT.md','paper/PROOF.md','certificate.json.gz','INPUTS.json','VERIFICATION.json','MANIFEST.json','check.py']]
    paths += [R1+'certificate.json',T2+'geometry/PROOF.md',T2+'SOURCE_CONTRACT.md',T2+'counts/PAPER.md',
              T2+'frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/c9/geometry/PROOF.md',SRC]
    paths += ['audits/2026-10-23-three-mask-round5-cb8f859/'+p for p in ['START.md','BASE.json']]
    entry=json.loads((HERE.parent/'BASE.json').read_text());prior={r['path']:r for r in entry['predecessors']};records=[]
    for path in paths:
        data=(REPO/path).read_bytes();sha=hashlib.sha256(data).hexdigest()
        if path in prior:assert (len(data),sha)==(prior[path]['bytes'],prior[path]['sha256'])
        dest=HERE/'frozen'/path;dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('xb') as f:f.write(data)
        records.append({'path':path,'frozen_path':str(dest.relative_to(HERE)),'bytes':len(data),'sha256':sha,
                        'authority':'immutable exact Git BASE' if path.startswith(T2) else 'immutable predecessor/round5 entry bytes'})
    routing=[]
    for r in entry['routing']:
        data=(HERE.parent/r['snapshot']).read_bytes();dest=HERE/'frozen/routing'/r['path'];dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('xb') as f:f.write(data)
        routing.append({**r,'frozen_path':str(dest.relative_to(HERE))})
    with (HERE/'INPUTS.json').open('x') as f:json.dump({'base':BASE,'inputs':records,'routing_background':routing,'write_boundary':str(HERE.relative_to(REPO))},f,indent=2,sort_keys=True);f.write('\n')

def chord_control():
    C=['c'+str(i) for i in range(9)];T=['t'+str(i) for i in range(9)];Z={0:['z0a','z0b'],4:['z4']};Q=[]
    for i in range(9):Q += [T[i]]+Z.get((i+1)%9,[])
    faces=[[C[i],C[(i+1)%9],T[i]] for i in range(9)]
    for i in range(9):
        link=[T[(i-1)%9]]+Z.get(i,[])+[T[i]];faces += [[C[i],b,a] for a,b in zip(link,link[1:])]
    for ring,h in [(['z0b','t0','t1','t2','t3','z4'],'hA'),(['t4','t5','t6','t7','t8','z0a'],'hB')]:
        faces += [[a,b,h] for a,b in zip(ring,ring[1:]+ring[:1])]
    faces += [['z0a','z0b','t4'],['z4','t4','z0b']]
    return {'id':'s3_deep2_H23_three_Q_chords','C':C,'Q':Q,'deep_vertices':['hA','hB'],'s_by_C':[2,0,0,0,1,0,0,0,0],
            'oriented_faces':faces,'Q_chords':[['t4','z0a'],['t4','z0b'],['z0b','z4']],
            'source_control':'not triggered','induced_Q_inference':'counterexample','source_realized':False}

def variable_case(svec,word,kind):
    Q=[];links=[]
    for i in range(9):Q += ['t'+str(i)]+['z'+str((i+1)%9)+'_'+str(j+1) for j in range(svec[(i+1)%9])]
    colors=dict(zip(Q,word))
    for i in range(9):links.append(['t'+str((i-1)%9)]+['z'+str(i)+'_'+str(j+1) for j in range(svec[i])]+['t'+str(i)])
    allowed=[tuple(c for c in range(4) if all(c!=colors[v] for v in link)) for link in links]
    lifts=[list(c)+list(word) for c in itertools.product(*allowed) if all(c[i]!=c[(i+1)%9] for i in range(9))]
    return {'s_by_C':svec,'Q_order':Q,'literal_Q':word,'complete_C_plus_Q_full_lifts':lifts,'status':kind}

def main():
    freeze();source=json.loads(gzip.decompress((HERE/'frozen'/SRC).read_bytes()));rows=[tuple(w) for w in source['inner_pattern_order']];lookup={w:i for i,w in enumerate(rows)}
    fibres=[];sparse=[]
    for q in rows:
        line=[[] for _ in rows];allowed=[tuple(c for c in range(4) if c not in [q[(i-1)%9],q[i]]) for i in range(9)]
        for c in itertools.product(*allowed):
            if all(c[i]!=c[(i+1)%9] for i in range(9)):line[lookup[norm(c)]].append(list(c)+list(q))
        require_nonempty=any(line);assert require_nonempty
        fibres.append(line);sparse.append({str(i):len(v) for i,v in enumerate(line) if v})
    queries=[];ob=source['kempe_obligations']
    for q in source['queries']:
        if not(q['target']==932 and q['geometry_id']=='induced' and q['status']=='necessary_condition_residual'):continue
        c_support=q['fixed_point'];initial=sum(1<<i for i,row in enumerate(sparse) if all(c_support>>int(j)&1 for j in row));current=initial;rounds=[]
        while True:
            remove=[]
            for p in bits(current):
                bad=[j for j,options in enumerate(ob[p]) if all(o&~current for o in options)]
                if bad:remove.append({'row':p,'failed_splits':bad})
            if not remove:break
            after=current&~sum(1<<r['row'] for r in remove);rounds.append({'before':current,'removals':remove,'after':after});current=after
        assert current==0;queries.append({'query_id':q['query_id'],'C_necessary_support':c_support,'Q_initial':initial,'rounds':rounds,'Q_final':current})
    types=[{'name':'T'+str(i),'C_contacts':[i,(i+1)%9]} for i in range(9)]+[{'name':'Z'+str(i),'C_contacts':[i]} for i in range(9)]
    pairs=[]
    for a,b in itertools.combinations_with_replacement(range(18),2):
        if a==b and a<9:continue
        d=min(min(abs(i-j),9-abs(i-j)) for i in types[a]['C_contacts'] for j in types[b]['C_contacts'])
        pairs.append({'endpoint_types':[a,b],'minimum_C_contact_distance':d,'if_original_Q_chord_allowed_by_local_test':d>=3})
    previous=json.loads(gzip.decompress((HERE/'frozen'/R4/'certificate.json.gz').read_bytes()))
    data={'schema':'C9-zero-single-annulus-exclusion-v1','base':BASE,'case_bindings':previous['case_bindings'],
          'C_generic_order':['c'+str(i) for i in range(9)],'Q_s0_order':['t'+str(i) for i in range(9)],
          's0_annulus_oriented_faces':[['c'+str(i),'c'+str((i+1)%9),'t'+str(i)] for i in range(9)]+[['c'+str(i),'t'+str(i),'t'+str((i-1)%9)] for i in range(9)],
          'complete_s0_Q_then_C_row_fibres':fibres,'s0_sparse_Q_to_C_counts':sparse,'s0_traces':queries,
          'contact_types':types,'contact_type_pairs':pairs,'noninduced_Q_control':chord_control(),
          'variable_single_annulus_controls':[variable_case([1]+[0]*8,[i%2 for i in range(10)],'counterexample'),
              variable_case([2,0,0,0,1,0,0,0,0],[i%3 for i in range(12)],'triggered and holds')],
          'conclusions':{'single_contact_total_minimum':1,'original_deep_vertices_minimum':2,'Q_chord_minimum_C_contact_distance':3,
              's0_original_collars_excluded':20,'Q_induced_claimed':False,'new_common_k_bound':False,'k_common_minimum_inherited':23,
              'general_932':'OPEN','zero_pair_h4_s_ge_1':'OPEN','smaller_bad':'OPEN','h_ge_5':'OPEN','K_infinity':'OPEN','new_Lean':False,
              'source_graph_controls':'not triggered','new_unconditional_C9_row_deletions':0}}
    blob=gzip.compress(json.dumps(data,sort_keys=True,separators=(',',':')).encode(),mtime=0)
    with (HERE/'certificate.json.gz').open('xb') as f:f.write(blob)
    print(json.dumps({'status':'produced exclusively','Q_to_C_nonzero_entries':sum(map(len,sparse)),'complete_full_lifts':sum(sum(r.values()) for r in sparse),
                      's0_collars_excluded':len(queries),'Q_conditional_row_deletions':sum(len(t['removals']) for q in queries for t in q['rounds'])}))
if __name__=='__main__':main()
