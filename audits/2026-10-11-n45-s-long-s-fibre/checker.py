#!/usr/bin/env python3
"""Frozen finite interface calibration; never a source-exclusion oracle."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import re

OUT=Path(__file__).resolve().parent
COL=range(4)
ROWS=[tuple(map(int,s)) for s in ('01012','01021','01023','01201','01202',
                                  '01203','01212','01213','01231','01232')]
QROWS=[ROWS[i] for i in (6,4,3,1,0)]

def need(ok,msg):
    if not ok: raise ValueError(msg)

def dumps(x):
    return (json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()

def solutions(vertices,edges,fixed):
    vertices=sorted(vertices); es=[(u,v) for u,v in edges if u in vertices and v in vertices]
    adj={v:set() for v in vertices}
    for u,v in es: adj[u].add(v);adj[v].add(u)
    cur={v:c for v,c in fixed.items() if v in adj}; ans=[]
    if any(cur[u]==cur[v] for u,v in es if u in cur and v in cur): return []
    def search():
        if len(cur)==len(vertices):
            ans.append(tuple(cur[v] for v in vertices));return
        choices=[]
        for v in vertices:
            if v not in cur:
                allow=set(COL)-{cur[w] for w in adj[v] if w in cur}
                if not allow:return
                choices.append((len(allow),-len(adj[v]),v,sorted(allow)))
        _,_,v,allow=min(choices)
        for c in allow:cur[v]=c;search();del cur[v]
    search();return sorted(ans)

def component_data(vertices,edges,gamma,contacts,r=None):
    vertices=sorted(vertices)
    full=solutions(list(range(5))+vertices,edges,dict(enumerate(gamma)))
    assignments=[f[5:] for f in full]
    index={v:i for i,v in enumerate(vertices)}
    ambient=[]; tuples=[]
    for tau in it.product(COL,repeat=len(contacts)):
        pre=[j for j,f in enumerate(assignments) if tuple(f[index[v]] for v in contacts)==tau]
        tuples.append({'tuple':tau,'preimages':pre})
        if r is not None:
            for a in COL:
                ambient.append({'tuple':tau,'r':a,'preimages':[j for j in pre if assignments[j][index[r]]==a]})
    relation=[t['tuple'] for t in tuples if t['preimages']]
    need(bool(relation),'calibration component must have an unpinned coloring')
    forbidden=sorted(set.intersection(*(set(t) for t in relation)))
    return dict(vertices=vertices,contacts=contacts,assignments=assignments,
                tuples=tuples,r_fibres=ambient,forbidden=forbidden)

def calibrate(d):
    vertices=d['vertices']; es=sorted(tuple(e) for e in d['edges'])
    pieces=d['pieces']; unary=[p for p in pieces if len(p['owners'])==1]
    mixed=[p for p in pieces if len(p['owners'])==2]
    need(len(unary)==1 and len(mixed)==2,'frozen control inventory changed')
    u=unary[0];s=u['owners'][0];r=next(v for v in mixed[0]['owners'] if v!=s)
    cv=sorted([r]+[v for p in mixed for v in p['vertices']]);uv=sorted(u['vertices'])
    pc=[v for p in mixed for v in p['contact_order'] if v in p['contacts'][str(s)]]
    pu=[v for v in u['contact_order'] if v in u['contacts'][str(s)]]
    need(len(set(pc))==len(pc),'shared contact must have one actual coordinate')
    free=sorted(set(vertices)-set(range(5))-set(cv)-set(uv)-{s})
    need(all(not any(v in e for e in es) for v in free),'unlisted effective vertex')
    spokes=[e for e in es if r in e and min(e)<5]; records=[]
    for e in spokes:
        xe=[f for f in es if f!=e];rows=[]
        for i,gamma in enumerate(ROWS):
            c=component_data(cv,xe,gamma,pc,r);ud=component_data(uv,xe,gamma,pu)
            # Independently reconstruct C from unpinned L/S assignments and the same r.
            joined_c=[]
            local=[]
            for p in mixed:
                pv=sorted(p['vertices']); lifts=solutions(list(range(5))+pv,xe,dict(enumerate(gamma)))
                local.append((p,pv,[f[5:] for f in lifts]))
            for a in COL:
                if any(r in f and min(f)<5 and a==gamma[min(f)] for f in xe):continue
                opts=[]
                for p,pv,lifts in local:
                    opts.append([f for f in lifts if all(f[pv.index(v)]!=a for v in p['contacts'][str(r)])])
                for ff in it.product(*opts):
                    ca={r:a}
                    for (_,pv,_),f in zip(local,ff):ca.update(zip(pv,f))
                    joined_c.append(tuple(ca[v] for v in cv))
            need(sorted(joined_c)==c['assignments'],'unpinned C/whole-piece full lifts differ')
            directx=solutions(vertices,xe,dict(enumerate(gamma)))
            directg=solutions(vertices,es,dict(enumerate(gamma)))
            pins=[]
            for a,b in it.product(COL,repeat=2):
                joined=[]
                if not any(s in f and min(f)<5 and b==gamma[min(f)] for f in xe):
                    for cf,uf in it.product(c['assignments'],ud['assignments']):
                        cm=dict(zip(cv,cf));um=dict(zip(uv,uf))
                        if cm[r]!=a or any(cm[v]==b for v in pc) or any(um[v]==b for v in pu):continue
                        for iso in it.product(COL,repeat=len(free)):
                            whole=dict(enumerate(gamma))|cm|um|{s:b}|dict(zip(free,iso))
                            joined.append(tuple(whole[v] for v in vertices))
                dx=[f for f in directx if f[vertices.index(r)]==a and f[vertices.index(s)]==b]
                dg=[f for f in directg if f[vertices.index(r)]==a and f[vertices.index(s)]==b]
                need(sorted(joined)==dx,'C/U joint differs from all direct X lifts')
                restored=dx if a!=gamma[min(e)] else []
                need(restored==dg,'restoring original named spoke differs from all G lifts')
                pins.append({'r':a,'s':b,'X_full_lifts':dx,'G_full_lifts':dg})
            rows.append({'literal_index':i,'gamma':gamma,'C':c,'U':ud,'pins':pins})
        records.append({'id':d['id'],'r':r,'s':s,'e':e,'vertices':vertices,'X_edges':xe,
          'G_edges':es,'free_isolates':free,'original_piece_data':[
           {k:p[k] for k in ('id','vertices','owners','contacts','contact_order','attachments',
                             'support','internal_edges','short','shield')} for p in pieces],
          'rotation':d['rotation'],'rows':rows,
          'SigmaG':sum(1<<i for i,row in enumerate(rows) if any(p['G_full_lifts'] for p in row['pins'])),
          'SigmaX':sum(1<<i for i,row in enumerate(rows) if any(p['X_full_lifts'] for p in row['pins']))})
    return records

def maps():
    obs=json.loads((OUT/'frozen/artifacts/c5_single_spoke_two_two/observations.json').read_text())
    final={int(m.group(1)) for m in re.finditer(r'^\| (\d+) \|',
       (OUT/'frozen/artifacts/c5_single_spoke_residual_locality/support_table.md').read_text(),re.M)}
    mapped=[]
    for j,row in enumerate(QROWS):
        move=[(i+4-j)%5 for i in range(5)]; rotated=[0]*5
        for i in range(5):rotated[move[i]]=row[i]
        pi={rotated[i]:ROWS[0][i] for i in range(5)};pi[next(c for c in COL if c not in pi)]=3
        for spoke in (0,2):
            sp=move[spoke]; su=[sorted(move[x] for x in S) for S in ((0,2,3,4),(0,1,2))]
            refl=sp in (2,3);rho=[3,2,1,0,4]
            pp=dict(pi)
            if refl:
                sp=rho[sp];su=[sorted(rho[x] for x in S) for S in su]
                pp={a:({0:1,1:0,2:2,3:3}[b]) for a,b in pi.items()}
            avail=set(COL)-{row[spoke]}
            for a in sorted(avail):
                bans=[[pp[a]],sorted(pp[b] for b in avail-{a})]
                hits=[z for z in obs['records'] if z['spoke']==sp and z['supports']==su and z['bans']==bans]
                mapped.append({'beta_q':j,'original_s_spoke':spoke,'FC_beta':[a],
                  'FU_beta':sorted(avail-{a}),'boundary_move':move,'color_move':pp,
                  'reflection_applied':refl,'BASE_record_ids':[z['id'] for z in hits],
                  'T4_retained':[z['id'] for z in hits if z['T4_status']=='retained'],
                  'final_retained':[z['id'] for z in hits if z['id'] in final]})
    need(len(mapped)==30,'pair query coverage changed')
    return mapped

def build():
    inputs=json.loads((OUT/'inputs.json').read_text())
    for x in inputs['entries']:
        need(hashlib.sha256((OUT/x['frozen_path']).read_bytes()).hexdigest()==x['sha256'],'frozen input drift')
    controls=[]
    for x in inputs['entries']:
        if '/controls/' in x['path'] and x['path'].endswith('.json'):
            controls+=calibrate(json.loads((OUT/x['frozen_path']).read_text()))
    qmap=maps()
    role_cases=[]
    for t in (1,2):
        for banned in it.combinations(COL,t):
            avail=set(COL)-set(banned)
            for cf in (set(z) for k in (1,2) for z in it.combinations(sorted(avail),k)):
                for uf in (set(z) for k in range(1,4-t) for z in it.combinations(sorted(avail),k)):
                    if cf|uf==avail and cf-uf and uf-cf:
                        role_cases.append({'t_s':t,'spoke_colors':banned,'FC':sorted(cf),'FU':sorted(uf)})
    # Full rejected-set schedule, after one common geometry normalization.
    masks={941:sorted({tuple(sorted((sgn*i+k)%5 for i in (0,1,3))) for sgn in (1,-1) for k in range(5)}),
           933:sorted({tuple(i for i in range(5) if i!=k) for k in range(5)})}
    schedules=[]
    for t,beta_domain in ((1,(3,4)),(2,(0,2))):
        for mask,qs in masks.items():
            for q in qs:
                for j in beta_domain:
                    if j not in q:continue
                    schedules.append({'t_s':t,'SigmaG_orbit':mask,'QG':q,'beta_q':j,'QX':[j],
                      'rows':[{'q':h,'literal':QROWS[h],
                         'X_status':'rejected beta' if h==j else 'accepted',
                         'G_status':'rejected' if h in q else 'accepted',
                         'required_r_on_all_X_lifts':QROWS[h][4] if h in q and h!=j else None,
                         'BASE_neighbor_target':h in ((j-1)%5,(j+1)%5)} for h in range(5)]})
    need(all(c['SigmaX']==1023 for c in controls),'calibration inventory changed: inspect rather than claiming source')
    # An explicit marginal/product counterexample and lost-r counterexample.
    relation={(0,1),(1,0)}; marginal=set(it.product({0,1},repeat=2))
    forbidden=lambda R:set.intersection(*(set(t) for t in R))
    need(forbidden(relation)=={0,1} and forbidden(marginal)==set(),'marginal negative failed')
    projected={(2,1,0)}; restored={z for z in projected if z[0]!=2}
    need(projected and not restored,'lost-r negative failed')
    return {'task_id':'N45-S-LONG-S-FIBRE','scope':'finite interface and necessary-table arithmetic only',
       'finite_source':{'established':False,'executed':False,'trigger_count':None,'status':'not triggered'},
       'controls':controls,'role_cases':role_cases,'pair_t1_BASE_mapping':qmap,'schedules':schedules,
       'negative_controls':{'endpoint_marginals':'counterexample','discard_r_projection':'counterexample'},
       'counts':{'graphs':19,'omissions':len(controls),'literal_rows':10*len(controls),
         'root_pin_fibres':160*len(controls),'ambient_C_r_fibres':sum(len(row['C']['r_fibres']) for c in controls for row in c['rows']),
         'empty_C_r_fibres':sum(not f['preimages'] for c in controls for row in c['rows'] for f in row['C']['r_fibres']),
         'pair_t1_necessary_queries':30,'joint_Q_schedules':len(schedules)}}

if __name__=='__main__':
    parser=argparse.ArgumentParser();g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--write',action='store_true');g.add_argument('--check',action='store_true')
    parser.add_argument('--certificate',type=Path,default=OUT/'certificate.json');args=parser.parse_args()
    data=build();raw=dumps(data)
    if args.write:
        with args.certificate.open('xb') as f:f.write(raw)
    else:need(args.certificate.read_bytes()==raw,'certificate mismatch')
    print(json.dumps({'status':'triggered and holds','controls':data['counts'],
       'finite_source':data['finite_source'],'certificate_sha256':hashlib.sha256(raw).hexdigest()},sort_keys=True))
