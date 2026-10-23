#!/usr/bin/env python3
"""Read-only independent face-domain, disk-topology and complete-lift replay."""
import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations,product
import json
from pathlib import Path
import random

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
PREV='audits/2026-10-23-941-gamma8-u-link-6b09cd4/certificate.json'
SOURCE='audits/2026-10-23-three-mask-round3-cb8f859/941/certificate.json'
BOUND=['U','p_d','d','zeta','x','p_x']
INNER=['r','T','s','tau','m','n','u','v']


def require(ok,why):
    if not ok:raise ValueError(why)


def custody():
    data=json.loads((HERE/'INPUTS-v2.json').read_text())
    require(data['base']==BASE and len(data['inputs'])==12,'input BASE/domain')
    for row in data['inputs']:
        for path in [HERE/row['snapshot'],ROOT/row['path']]:
            raw=path.read_bytes();require((len(raw),sha256(raw).hexdigest())==(row['bytes'],row['sha256']),'input drift '+str(path))
    manifest=json.loads((HERE/'frozen/audits/2026-10-23-941-types-wrong-side-6b09cd4/FINAL_MANIFEST.json').read_text())
    entries=[r for r in manifest['entries'] if r['path'].startswith('audits/2026-10-23-941-gamma8-u-link-6b09cd4/')]
    require(len(entries)==data['previous_final_manifest_entries_checked']==29,'previous final-manifest coverage')
    for row in entries:
        raw=(ROOT/row['path']).read_bytes();require((len(raw),sha256(raw).hexdigest())==(row['bytes'],row['sha256']),'previous final-manifest drift '+row['path'])
    return dict(previous_final_manifest_entries=29,direct_inputs=12,immutable_drift=0)


def read_source():return json.loads((HERE/'frozen'/SOURCE).read_text())['source_rows']


def rebuild_faces(rows):
    out=[]
    for row in rows:
        phi={('Y' if z=='HL_0' else z):c for z,c in row['original_boundary_colors'].items()}
        contacts=row['complete_predecessor_record']['complete_initial_02_contacts']
        L=next(block for block in contacts if 'z4' in block)
        B=next(block for block in contacts if 'V' in block)
        L2=sorted(v for v in L if phi[v]==2);B3=sorted(v for v in B if phi.get(v,phi.get('Y'))==3)
        require(L2==['s'] and B3==['q'],'original complete-frame alternatives')
        successor=row['complete_predecessor_record']['full_03_successor_boundary_contacts']
        norm=[{'Y' if v=='HL_0' else v for v in block} for block in successor]
        owner=lambda v:next(i for i,block in enumerate(norm) if v in block)
        require(owner('V')!=owner('s') and owner('z4')!=owner('q'),'successor C/D or A/Q distinction')
        for nonempty in [True,False]:
            branch='nonempty_M2_six_points' if nonempty else 'empty_M2_five_points'
            pool={v:('frame',c) for v,c in phi.items() if c in [2,3]}
            pool.update(zeta=('K',2),p_d=('K',2),p_x=('K',2),W=('B',3),tau=('N',3))
            pool.update(dict(m=('M',2),n=('N',3),v=('N',3)) if nonempty else dict(a=('N',3),b=('N',3)))
            tested=[];allowed=[]
            for v,(label,color) in pool.items():
                if label=='frame':
                    if color==2:
                        if v not in L:why='wrong_original_02_component'
                        else:
                            require(owner(v)!=owner('V'),'frame s would merge C/D');why='C_D_merge'
                    else:
                        if v not in B:why='wrong_original_13_component'
                        else:
                            require(v=='q','unexpected B3 frame');why='fixed_V_Y_common_neighbor'
                elif color==2:
                    require(label!='L','unaccounted private L2');why='wrong_original_02_component'
                elif label!='B':why='wrong_original_13_component'
                else:
                    require(v=='W','unaccounted private B3');why='A_Q_merge'
                tested.append(dict(vertex=v,ownership=label,original_color=color,rejection=why))
            # Canonical order is frame vertices first, then private vertices.
            tested.sort(key=lambda r:(r['ownership']!='frame',r['vertex']))
            out.append(dict(target=row['target'],type02=row['initial_02_type'],branch=branch,
                complete_L_contacts=L,complete_B_contacts=B,frame_L2=L2,frame_B3=B3,
                tested_third_points=tested,admissible_third_points=allowed))
    return out


def topology(cap):
    faces=[tuple(f) for f in cap['faces']];edges={tuple(e) for e in cap['edges']}
    incidence={e:[] for e in edges}
    for i,f in enumerate(faces):
        for a,b in zip(f,f[1:]+f[:1]):incidence[tuple(sorted((a,b)))].append((i,1 if a<b else -1))
    boundary={tuple(sorted((a,b))) for a,b in zip(BOUND,BOUND[1:]+BOUND[:1])}
    require({e for e,uses in incidence.items() if len(uses)==1}==boundary,'wrong disk boundary')
    require(all(len(uses)==(1 if e in boundary else 2) for e,uses in incidence.items()),'nonmanifold edge')
    dual={i:[] for i in range(len(faces))}
    for uses in incidence.values():
        if len(uses)==2:
            (i,s),(j,t)=uses;dual[i].append((j,-s*t));dual[j].append((i,-s*t))
    signs={0:1};todo=[0]
    while todo:
        i=todo.pop()
        for j,r in dual[i]:
            value=signs[i]*r
            if j in signs:require(signs[j]==value,'inconsistent common orientation')
            else:signs[j]=value;todo.append(j)
    require(len(signs)==len(faces),'disconnected face disk')
    for v in BOUND+INNER:
        la={}
        for f in faces:
            if v in f:
                a,b=[w for w in f if w!=v];la.setdefault(a,set()).add(b);la.setdefault(b,set()).add(a)
        ends=[w for w in la if len(la[w])==1]
        require(all(len(nbs) in [1,2] for nbs in la.values()) and len(ends)==(2 if v in BOUND else 0),'wrong vertex link')
        reached={next(iter(la))};todo=list(reached)
        while todo:
            for w in la[todo.pop()]-reached:reached.add(w);todo.append(w)
        require(len(reached)==len(la),'disconnected vertex link')
    require(len(BOUND)+len(INNER)-len(edges)+len(faces)==1,'disk Euler characteristic')
    return [list(f if signs[i]==1 else tuple(reversed(f))) for i,f in enumerate(faces)]


def boundary_words():
    result=set()
    for w in product(range(4),repeat=6):
        if any(a==b for a,b in zip(w,w[1:]+w[:1])):continue
        names={};result.add(tuple(names.setdefault(c,len(names)) for c in w))
    return [list(w) for w in sorted(result)]


def all_lifts(cap,word):
    adjacency={v:set() for v in BOUND+INNER}
    for a,b in cap['edges']:adjacency[a].add(b);adjacency[b].add(a)
    order=sorted(INNER,key=lambda v:(-len(adjacency[v]),v))
    colors=dict(zip(BOUND,word));result=[]
    def visit(i):
        if i==len(order):result.append([colors[v] for v in INNER]);return
        v=order[i];forbidden={colors[w] for w in adjacency[v] if w in colors}
        for color in range(4):
            if color not in forbidden:colors[v]=color;visit(i+1);del colors[v]
    visit(0);return sorted(result)


def rebuild_caps(prior,words):
    c=prior['complete_predecessor_certificate']['complete_predecessor_certificate']
    for _ in range(3):c=c['complete_predecessor_certificate']
    cells={r['id']:r for r in c['candidates']};grouped={}
    for row in prior['star_restrictions']:
        cell=cells[row['cell']]
        links=dict(row['full_links'],m=['r','T','n','u','v'],T=['r','tau','s','n','m'])
        # The complete tau star is reconstructed from the original ten-point
        # induced graph, rather than using the producer's face union.
        tau=set(cell['full_private_stars']['tau'])
        edges={tuple(sorted(e)) for e in cell['edges'] if set(e)<=(set(BOUND)|set(INNER))}
        for z,l in links.items():
            edges.update(tuple(sorted((z,w))) for w in l)
            edges.update(tuple(sorted((a,b))) for a,b in zip(l,l[1:]+l[:1]))
        require(all(set(e)<=set(BOUND+INNER) for e in edges),'cap vertex leak')
        adj={v:set() for v in BOUND+INNER}
        for a,b in edges:adj[a].add(b);adj[b].add(a)
        require(adj['tau']==tau,'complete original tau star')
        faces={tuple(sorted((a,b,z))) for a,b in edges for z in adj[a]&adj[b]}
        key=tuple(sorted(edges))
        if key not in grouped:
            grouped[key]=dict(boundary=BOUND,inner=INNER,edges=[list(e) for e in sorted(edges)],faces=[list(f) for f in sorted(faces)],source_rows=[])
        grouped[key]['source_rows'].append(dict(cell=row['cell'],family=row['family'],nx=row['n_x_edge']))
    result=[]
    for i,cap in enumerate(grouped.values()):
        cap['id']=i;topology(cap)
        cap['relations']=[dict(word=w,full_lifts=all_lifts(cap,w)) for w in words]
        cap['statistics']=dict(vertices=14,edges=len(cap['edges']),faces=len(cap['faces']),
            nonempty=sum(bool(r['full_lifts']) for r in cap['relations']),total_lifts=sum(len(r['full_lifts']) for r in cap['relations']))
        require(cap['statistics']['edges']==33 and cap['statistics']['faces']==20,'cap cardinalities')
        result.append(cap)
    return result


def validate(cert,seed=0):
    prior=json.loads((HERE/'frozen'/PREV).read_text())
    require(cert['schema']=='941-gamma8-joint-bpaths-v1' and cert['base']==BASE,'schema/BASE')
    require(cert['complete_predecessor_certificate']==prior,'predecessor full fibres/empty rows/lifts drift')
    expected=rebuild_faces(read_source())
    require(cert['face_tables']==expected,'source-face domain/value drift')
    require(cert['forced_face']==dict(edge=['z4','V'],original_colors=[0,1],third_color_options=[2,3],
        new_private_options=[dict(color=2,original_component='L02(z4)',successor_component='C12(U)'),
                             dict(color=3,original_component='B13(V)',successor_component='A03(a)')],
        strict_exterior=True,holds_for_arbitrary_Gamma8_interior=True,E_may_be_rootless=True,
        disjoint_from_all_M2_and_rootless_full_stars_and_K2_exits=True),'forced face contract drift')
    require(cert['j2_bounds']==dict(M2_nonempty_minimum=7,M2_empty_T6_minimum=6,
        full_M2_degree_bound='|M2|+3+d(m)-bGamma(m)',adjacent_T_m_bound='D+d(m)-3',
        nonadjacent_T_v_bound='D+d(v)-1',T5_nonsingleton_M2_minimum=9,
        empty_M2_bound='D',empty_M2_D_even=True),'bound arithmetic or scope drift')
    ws=boundary_words();require(len(ws)==31 and cert['proper_S4_boundary_words']==ws,'proper boundary domain drift')
    caps=rebuild_caps(prior,ws)
    order=list(range(len(caps)));random.Random(seed).shuffle(order)
    require(len(caps)==len(cert['exact_K6_caps'])==16,'exact cap coverage')
    for i in order:require(cert['exact_K6_caps'][i]==caps[i],'cap full relation drift '+str(i))
    require(cert['authority_boundaries']==dict(finite_control='triggered and holds',source_realizability='not triggered',
        paper_excluded_branches=['M2_nonempty_X6','M2_empty_T6_X5'],eleven_type_exclusions=0,
        general_wrong_side='OPEN',common_k_lower_bound=23,partial_B_path_interfaces_are_not_sources=True,
        new_Lean=False,new_LP=False,smaller_bad=False),'unsupported promotion')
    return dict(face_tables=8,remaining_old_domain_face_points=0,exact_caps=16,
        complete_boundary_rows=16*31,source_rows=sum(len(c['source_rows']) for c in caps),
        cap_nonempty_counts=sorted(set(c['statistics']['nonempty'] for c in caps)),
        cap_total_lift_counts=sorted(set(c['statistics']['total_lifts'] for c in caps)),
        source_realizability='not triggered',eleven_type_exclusions=0)


def negative(cert):
    mutations=[('drop_target',lambda c:c['face_tables'].pop()),
        ('allow_frame_s',lambda c:c['face_tables'][0]['admissible_third_points'].append('s')),
        ('allow_W_in_A',lambda c:c['face_tables'][0]['admissible_third_points'].append('W')),
        ('merge_L_K',lambda c:c['face_tables'][0]['frame_L2'].append('p_d')),
        ('wrong_chi2_owner',lambda c:c['forced_face']['new_private_options'][0].update(original_component='K02(U)')),
        ('drop_exterior',lambda c:c['forced_face'].update(strict_exterior=False)),
        ('root_E',lambda c:c['forced_face'].update(E_may_be_rootless=False)),
        ('claim_all_j_bound',lambda c:c['j2_bounds'].update(arbitrary_j_minimum=7)),
        ('wrong_degree_bound',lambda c:c['j2_bounds'].update(adjacent_T_m_bound='D+d(m)-2')),
        ('lose_cap',lambda c:c['exact_K6_caps'].pop()),
        ('lose_empty_fibre',lambda c:c['exact_K6_caps'][0]['relations'].pop()),
        ('lose_full_lift',lambda c:c['exact_K6_caps'][0]['relations'][0]['full_lifts'].pop()),
        ('fake_cap_face',lambda c:c['exact_K6_caps'][0]['faces'][0].__setitem__(0,'U')),
        ('claim_source',lambda c:c['authority_boundaries'].update(source_realizability='triggered and holds')),
        ('claim_11_types',lambda c:c['authority_boundaries'].update(eleven_type_exclusions=11))]
    rejected=[]
    for name,mutate in mutations:
        bad=deepcopy(cert);mutate(bad)
        try:validate(bad)
        except (ValueError,KeyError,TypeError):rejected.append(name)
        else:raise ValueError('negative accepted '+name)
    return dict(count=len(rejected),rejected=rejected)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--negative',action='store_true');parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    args=parser.parse_args();cert=json.loads(args.certificate.read_text())
    out=dict(custody=custody(),validation=validate(cert,args.seed))
    if args.negative:out['negative']=negative(cert)
    print(json.dumps(out,sort_keys=True))


if __name__=='__main__':main()
