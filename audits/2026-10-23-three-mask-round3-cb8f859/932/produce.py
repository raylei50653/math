#!/usr/bin/env python3
"""Exclusive producer for fixed C9 geometric data; no source graph search."""
import gzip, hashlib, itertools, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
BASE='cb8f8593e273a7426ecadd59797a6e643cc4768e'
R2='audits/2026-10-23-three-mask-round2-cb8f859/932/'
R1='audits/2026-10-23-three-mask-methods-cb8f859/932/'
T2='audits/2026-10-13-c9-932-source-d521163/'
FRONT=T2+'frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/c9/'

def dump(path,data):
    with path.open('x') as f:json.dump(data,f,indent=2,sort_keys=True);f.write('\n')

def freeze():
    paths=[R2+p for p in ['REPORT.md','SOURCE_CONTRACT.md','paper/PROOF.md','certificate.json.gz','VERIFICATION.json','INPUTS.json']]
    paths += [R1+p for p in ['REPORT.md','SOURCE_CONTRACT.md','paper/PROOF.md','certificate.json','INPUTS.json']]
    paths += [T2+'geometry/PROOF.md',T2+'SOURCE_CONTRACT.md',FRONT+'geometry/PROOF.md',FRONT+'geometry/DEPENDENCIES.md',FRONT+'finite/certificate.v2.json.gz']
    paths += ['audits/2026-10-23-three-mask-round3-cb8f859/'+p for p in ['BASE.json','START.md']]
    records=[]
    for path in paths:
        blob=(REPO/path).read_bytes();dest=HERE/'frozen'/path;dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('xb') as f:f.write(blob)
        records.append({'path':path,'frozen_path':str(dest.relative_to(HERE)),'bytes':len(blob),'sha256':hashlib.sha256(blob).hexdigest(),
                        'authority':'immutable exact Git BASE' if path.startswith(T2) else 'immutable predecessor/round3 entry bytes'})
    entry=json.loads((HERE.parent/'BASE.json').read_text());routing=[]
    for r in entry['routing_snapshots']:
        blob=(HERE.parent/r['snapshot']).read_bytes();dest=HERE/'frozen/routing'/r['path'];dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('xb') as f:f.write(blob)
        routing.append({**r,'frozen_path':str(dest.relative_to(HERE))})
    dump(HERE/'INPUTS.json',{'schema':'C9-distance-four-inputs-v1','base':BASE,'inputs':records,'routing_background':routing,
                          'write_boundary':str(HERE.relative_to(REPO)),'policy':'immutable drift fails; live routing drift reported separately'})

def crossing(p,q):
    a,b=sorted(p);c,d=sorted(q)
    return len({a,b,c,d})==4 and ((a<c<b)!=(a<d<b))

def mesh(two):
    c=['c'+str(i) for i in range(9)];t=['t'+str(i) for i in range(9)]
    x='x';y='y' if two else 'x';faces=[]
    for i in range(9):faces.append([c[i],c[(i+1)%9],t[i]])
    for i in [1,2,3,5,6,7,8]:faces.append([c[i],t[i],t[i-1]])
    faces += [['c0','t0',x],['c4',x,'t3'],['c4','t4',y],['c0',y,'t8']]
    if two:faces += [['c0',x,y],['c4',y,x]]
    rings=[[x]+t[:4],[y]+t[4:]]
    for j,ring in enumerate(rings):
        for a,b in zip(ring,ring[1:]+ring[:1]):faces.append([a,b,'s'+str(j)])
    private=t+[x]+(['y'] if two else [])+['s0','s1']
    return {'id':'two_double_m13' if two else 'one_double_m12','boundary':c,'private_vertices':private,'oriented_faces':faces,
            'face_third_vertices':t,'distance_four_vertices':[x,y] if two else [x],
            'source_claim':False,'status':{'triangulated_degree_contact_control':'triggered and holds',
                                        'complete_932_global_minimal_source':'not triggered'}}

def main():
    freeze();pairs=[[i,(i+4)%9] for i in range(9)];witnesses=[]
    for i,j in itertools.combinations(range(9),2):
        p,q=pairs[i],pairs[j]
        if crossing(p,q):witnesses.append({'pair_indices':[i,j],'kind':'alternating','cyclic_terminals':sorted(p+q)})
        else:
            a=next(iter(set(p)&set(q)));b=next(iter(set(p)-{a}));d=next(iter(set(q)-{a}))
            pocket=['c'+str(a),'x','c'+str(b),'c'+str(d),'y']
            witnesses.append({'pair_indices':[i,j],'kind':'shared_endpoint_C5','shared_endpoint':a,'adjacent_other_ends':[b,d],
                              'pocket_order':pocket,'only_allowed_diagonal':['x','y'],'forbidden_wheel_C_contacts':sorted([a,b,d])})
    templates=[{'pair_index':None,'multiplicity':0}]+[{'pair_index':i,'multiplicity':n} for i in range(9) for n in [1,2]]
    old=json.loads(gzip.decompress((HERE/'frozen'/R2/'certificate.json.gz').read_bytes()))
    bindings=[]
    for b in old['case_bindings']:
        order=b['C9_original_names'];bindings.append({'query_id':b['query_id'],'extras':b['extras'],'C9_original_names':order,
            'retained_frozen_case_sha256':b['retained_frozen_case_sha256'],
            'face_third_definitions':[{'name':'t'+str(i),'original_edge':[order[i],order[(i+1)%9]],'complete_C_contacts':[order[i],order[(i+1)%9]]} for i in range(9)],
            'distance_four_pairs':[[order[i],order[(i+4)%9]] for i in range(9)],'templates':templates,
            'full_820_row_order_preserved':True,'new_row_deletions':[]})
    data={'schema':'C9-distance-four-common-embedding-v1','base':BASE,'distance_four_pairs':pairs,'distinct_pair_witnesses':witnesses,
          'same_pair_lenses':[{'pair_index':i,'C4_order':['c'+str(i),'x','c'+str((i+4)%9),'y'],
                              'forbidden_C_diagonal':['c'+str(i),'c'+str((i+4)%9)],'forced_original_diagonal':['x','y'],
                              'three_paths_outer_indices':[0,2],'three_paths_strict_interior_index':1} for i in range(9)],
          'templates':templates,'case_bindings':bindings,'geometric_controls':[mesh(False),mesh(True)],
          'conclusions':{'maximum_distinct_distance_four_pairs':1,'maximum_vertices_per_distance_four_pair':2,
                         'two_centres_force_original_edge':True,'necessary_templates_each_collar':19,'necessary_named_templates':380,
                         'new_C9_row_deletions':0,'all_distance_four_contacts_excluded':False,'no_triple_h4_branch':'OPEN',
                         'general_932':'OPEN','h_ge_5':'OPEN','smaller_bad':'OPEN','K_infinity':'OPEN','new_Lean':False,
                         'k_common_minimum_inherited':23,'new_k_bound':False,'source_graph_controls':'not triggered'}}
    dump(HERE/'certificate.json',data)
    print(json.dumps({'status':'produced exclusively','distinct_pair_witnesses':len(witnesses),'templates_each_collar':len(templates),'named_templates':len(bindings)*len(templates)}))

if __name__=='__main__':main()
