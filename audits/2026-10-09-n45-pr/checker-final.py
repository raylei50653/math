#!/usr/bin/env python3
"""N45-PR support transport and complete-fibre calibration; no piece/graph search.
Fresh certificate generation uses exclusive create. --check never writes.
The only graphs are 23 immutable SU-J controls, whose LP source status is separate.
"""
import argparse,hashlib,itertools,json
from collections import Counter
from pathlib import Path
OUT=Path(__file__).resolve().parent
BASE='dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
COL=set(range(4)); B=set(range(5)); PERMS=list(itertools.permutations(range(4)))
PAIRS=list(itertools.product(range(4),repeat=2))
QINDEX=[6,4,3,1,0]
def enc(x):return (json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def read(p):return json.loads(p.read_text())
def need(x,s):
 if not x:raise ValueError(s)
def canonical(vals):
 d={};return tuple(d.setdefault(v,len(d)) for v in vals)
def local_solutions(g,p,beta):
 """Enumerate only this existing piece, directly from all original incident edges."""
 vs=p['vertices'];ps=set(vs); edges=[e for e in g['edges'] if set(e)&ps]
 need(all(set(e)<=ps|B|set(g['roots']) for e in edges),'unexpected external vertex')
 inner=[e for e in edges if set(e)<=ps];atts=[e for e in edges if set(e)&B]
 need(sorted(inner)==p['internal_edges'] and sorted(atts)==p['attachments'],'attachment schema mismatch')
 f=dict(enumerate(beta));lifts=[]
 def search(n):
  if n==len(vs):lifts.append(tuple(f[v] for v in vs));return
  v=vs[n]
  for c in range(4):
   if any(c==f[w] for e in inner+atts if v in e for w in e if w!=v and w in f):continue
   f[v]=c;search(n+1);del f[v]
 search(0);return sorted(lifts)
def tuples_from_lifts(p,lifts):
 ix={v:i for i,v in enumerate(p['vertices'])};d={}
 for f in lifts:
  t=tuple(f[ix[v]] for v in p['contact_order']);d.setdefault(t,[]).append(f)
 return [{'tuple':list(t),'full_piece_lifts':[list(f) for f in sorted(fs)]} for t,fs in sorted(d.items())]
def compatible(p,t,pins):
 return all(t[p['contact_order'].index(v)]!=c for r,c in pins.items() for v in p['contacts'][str(r)])
def bad_column(p,row,r,s,b):
 side=[t for t in row['tuples'] if compatible(p,t['tuple'],{s:b})]
 need(bool(side),'degree-list strict-slack local fibre empty')
 return {a for a in COL if not any(compatible(p,t['tuple'],{r:a,s:b}) for t in side)}
def tree(vs,edges):
 vs=set(vs);need(bool(vs),'empty bag');seen={min(vs)};ans=[]
 while seen!=vs:
  choices=sorted(tuple(e) for e in edges if set(e)<=vs and len(set(e)&seen)==1)
  need(bool(choices),'bag disconnected');e=choices[0];seen.update(e);ans.append(list(e))
 return ans
def proper_lift(vs,edges,beta,pins,lift):
 need(lift is not None and len(lift)==len(vs),'missing full graph lift')
 f=dict(zip(vs,lift));need(all(c in COL for c in lift),'bad color')
 need(all(f[u]!=f[v] for u,v in edges),'bad original edge lift')
 need(all(f[i]==c for i,c in enumerate(beta)) and all(f[r]==c for r,c in pins.items()),'bad literal pins')
def support_paths(support):
 return [(i,(i+1)%5,(i+2)%5) for i in range(5) if set(support)=={i,(i+1)%5,(i+2)%5}]
def partitions_and_masks(patterns):
 frame={tuple(sorted((i,(i+1)%5))) for i in range(5)};partitions=[]
 table=[]
 for sigma,Q in [(941,{0,1,3}),(933,{0,1,2,3})]:
  qs=[{q} for q in sorted(Q)]+[{q,(q+1)%5} for q in range(5) if {q,(q+1)%5}<=Q]
  for beta in sorted(Q):
   choices=[q for q in qs if beta in q];table.append({'sigma_G':sigma,'beta_q':beta,'beta_index':QINDEX[beta],'possible_Q_X':[sorted(q) for q in choices]})
 need(len(table)==7 and sum(len(r['possible_Q_X']) for r in table)==15,'seven-cell/15-choice domain')
 for i in range(5):
  for direction in (1,-1):
   path=[(i+direction*j)%5 for j in range(5)]
   supports={'U':path[:3],'L':path[2:],'S':[path[4],path[0]]}
   arcs={'U':list(zip(path[:2],path[1:3])),'L':list(zip(path[2:4],path[3:5])),'S':[(path[4],path[0])]}
   need(set(tuple(sorted(e)) for es in arcs.values() for e in es)==frame,'shield partition')
   rows=[]
   for j,beta in enumerate(patterns):
    signatures={p:list(canonical(beta[v] for v in sup)) for p,sup in supports.items()}
    roles={'ABA':[beta[supports['U'][1]]],'ABC':[beta[supports['U'][1]],next(iter(COL-{beta[v] for v in supports['U']}))] if len({beta[v] for v in supports['U']})==3 else None}
    rows.append({'index':j,'literal_beta':beta,'support_colors':{p:[beta[v] for v in sup] for p,sup in supports.items()},'signatures':signatures,'U_singleton_allowed_after_endpoint_lemma':roles['ABC'] if signatures['U']==[0,1,2] else roles['ABA']})
   cases=[]
   for cell in table:
    QG={0,1,3} if cell['sigma_G']==941 else {0,1,2,3}
    for QX in cell['possible_Q_X']:
     delta=sorted(QG-set(QX));need(len(delta)>= (1 if cell['sigma_G']==941 else 2),'Delta lower bound')
     forced_shapes=sorted({tuple(rows[QINDEX[q]]['signatures']['U']) for q in delta})
     cases.append({'sigma_G':cell['sigma_G'],'beta_q':cell['beta_q'],'Q_X':QX,'Delta_q':delta,'forced_shapes':[list(s) for s in forced_shapes],
       'Delta':[{'q':q,'index':QINDEX[q],'U_signature':rows[QINDEX[q]]['signatures']['U'],'allowed_forced_colors':rows[QINDEX[q]]['U_singleton_allowed_after_endpoint_lemma']} for q in delta],
       'originally_accepted_escape_rows':[{'index':j,'U_signature':row['signatures']['U'],'singleton_transport_required':tuple(row['signatures']['U']) in forced_shapes,'obligation':'exists complete X lift with r unequal to transported U singleton when transport required'} for j,row in enumerate(rows) if j not in {QINDEX[q] for q in QG}],
       'source_status':'necessary mask profile before untouched-slot and single-root deductions; not a realization'})
   partitions.append({'start':i,'direction':direction,'supports':supports,'shield_edges':{k:[list(e) for e in v] for k,v in arcs.items()},'rows':rows,'cases':cases})
 # Whole-frame actions transport masks, q labels, named shield arcs and literal rows together.
 actions=[]
 for shift in range(5):
  for direction in (1,-1):
   mapping=[(shift+direction*i)%5 for i in range(5)];rowmap=[]
   for i,beta in enumerate(patterns):
    moved=[None]*5
    for v,c in enumerate(beta):moved[mapping[v]]=c
    can=canonical(moved);j=patterns.index(list(can));perms=[list(p) for p in PERMS if [p[c] for c in moved]==list(can)]
    need(bool(perms),'whole-frame color permutation missing');rowmap.append({'old_index':i,'new_index':j,'literal_after_frame_move':moved,'whole_graph_color_permutations':perms})
   masks={}
   for sigma in (941,933):
    moved_mask=sum(1<<r['new_index'] for r in rowmap if sigma&(1<<r['old_index']));masks[str(sigma)]=moved_mask
   actions.append({'vertex_map':mapping,'q_map':mapping,'rows':rowmap,'transported_target_masks':masks,'root_orders':['r,s','s,r'],'root_swap':'transpose all fibres and contact ownership on the same graph'})
 return {'seven_cells':table,'named_partitions':partitions,'whole_frame_D5_actions':actions,'unknown_tensor_count':5,'tensor_bases':['U:010','U:012','L:010','L:012','S:01'],'source_realizations_tested':0}
def calibration(patterns,raw):
 counts=Counter();records=[];hub_records=[];saturation=[];forcing=[];source_status=[];negative=None
 for g in raw['graphs']:
  roots=g['roots'];pmap={p['id']:p for p in g['pieces']};computed={}
  for p in g['pieces']:
   rows=[];solutions=[]
   for i,beta in enumerate(patterns):
    lifts=local_solutions(g,p,beta);tuples=tuples_from_lifts(p,lifts);need(tuples==p['rows'][i]['tuples'],'complete original-edge oracle differs from frozen tuples/lifts')
    need(bool(tuples),'unexpected empty local relation')
    for n,(a,b) in enumerate(PAIRS):
     ix=[j for j,t in enumerate(tuples) if compatible(p,t['tuple'],dict(zip(roots,(a,b))))]
     need(ix==p['rows'][i]['fibres'][n]['tuple_indices'],'frozen full fibre mismatch')
    rows.append({'tuples':tuples});solutions.append(lifts);counts['piece_rows']+=1;counts['complete_piece_lifts']+=len(lifts);counts['all_16_fibres']+=16
   computed[p['id']]=rows
   tests=[]
   for i in range(10):
    for j in range(10):
     maps=[pcol for pcol in PERMS if all(pcol[patterns[i][v]]==patterns[j][v] for v in p['support'])]
     if not maps:continue
     target=set(solutions[j]);mapped_pairs=[]
     for pcol in maps:
      transported={tuple(pcol[c] for c in f) for f in solutions[i]};need(transported==target,'full lift transport failed')
      for pair in PAIRS:
       src={tuple(f) for t in rows[i]['tuples'] if compatible(p,t['tuple'],dict(zip(roots,pair))) for f in t['full_piece_lifts']}
       dst={tuple(f) for t in rows[j]['tuples'] if compatible(p,t['tuple'],dict(zip(roots,(pcol[pair[0]],pcol[pair[1]])))) for f in t['full_piece_lifts']}
       need({tuple(pcol[c] for c in f) for f in src}==dst,'complete pin fibre transport failed')
      mapped_pairs.append(list(pcol));counts['full_lift_transport_maps']+=1;counts['pin_fibre_transport_maps']+=16
     tests.append({'from_index':i,'to_index':j,'color_permutations':mapped_pairs,'target_full_lifts_sha256':sha(enc(solutions[j]))})
   records.append({'graph':g['id'],'piece':p['id'],'support':p['support'],'contact_order':p['contact_order'],'shared_contacts':p['shared_contacts'],'tests':tests})
   # Calibrate endpoint hub bags only when actual original antecedents hold.
   paths=support_paths(p['support'])
   if len(paths)==1 and p['one_sided'] and set(g['touch'])==B:
    h,m,k=paths[0]
    outside=set(g['vertices'])-B-set(p['vertices']);tree(outside,g['edges'])
    for i,beta in enumerate(patterns):
     for endpoint in (h,k):
      other=k if endpoint==h else h;a=beta[endpoint]
      bag0=outside | (B-{m,other});bags=[bag0,{m},{other}]
      if beta[other]==a:bags=[bag0|{other},{m}]
      trees=[tree(bag,g['edges']) for bag in bags];adj=[]
      for z in range(len(bags)):
       for w in range(z+1,len(bags)):
        es=[e for e in g['edges'] if len(set(e)&bags[z])==1 and len(set(e)&bags[w])==1];need(bool(es),'hub adjacency missing');adj.append(es[0])
      color_of_neighbor={v:beta[v] if v in B else a for v in B|set(p['owners'])}
      neighbor=set(v for e in g['edges'] if set(e)&set(p['vertices']) for v in e if v not in p['vertices'])
      need(neighbor<=set.union(*bags),'neighbor hub coverage')
      colors=[{color_of_neighbor[v] for v in bag&neighbor} for bag in bags];need(all(len(c)==1 for c in colors) and len(set(next(iter(c)) for c in colors))==len(colors),'hub pin colors')
      pins={r:a for r in p['owners']};full=[f for t in rows[i]['tuples'] if compatible(p,t['tuple'],pins) for f in t['full_piece_lifts']];need(bool(full),'endpoint complete lift not available')
      hub_records.append({'graph':g['id'],'piece':p['id'],'index':i,'endpoint':endpoint,'pin':a,'bags':[sorted(bag) for bag in bags],'bag_original_spanning_edges':trees,'between_bag_original_edges':adj,'complete_piece_lift':full[0]});counts['endpoint_hub_pins']+=1
   else:counts['endpoint_hub_piece_not_triggered']+=1
   if negative is None and p['shared_contacts']:
    i=0;lost=rows[i]['tuples'][0];changed=rows[i]['tuples'][1:]
    need(changed!=tuples_from_lifts(p,solutions[i]),'omitted tuple not detected')
    negative={'graph':g['id'],'piece':p['id'],'row_index':i,'shared_contacts':p['shared_contacts'],'removed_complete_tuple':lost,'oracle':'all original piece edges plus literal frame, independently enumerated','status':'rejected incomplete relation; negative data only, no source counterexample'}
  # Full-fibre saturated-column lemma, calibrated on existing rejected rows.
  for row in g['joins']:
   i=row['index']
   for cap in row['capacity']:
    if cap.get('status')!='triggered and holds':continue
    r,s=cap['r'],cap['s'];b=cap['b']
    for column in cap['columns']:
     p=pmap[column['piece']];bad=bad_column(p,computed[p['id']][i],r,s,b);k=len(p['contacts'][str(r)])
     need(bad==set(column['G']),'saved column differs from complete relation')
     if len(bad)!=k:continue
     side=[t for t in computed[p['id']][i]['tuples'] if compatible(p,t['tuple'],{s:b})]
     for t in side:
      cs=[t['tuple'][p['contact_order'].index(v)] for v in p['contacts'][str(r)]];need(len(set(cs))==k and set(cs)==bad,'all-lift contact saturation failed')
     saturation.append({'graph':g['id'],'piece':p['id'],'index':i,'r':r,'s':s,'b':b,'forbidden':sorted(bad),'k':k,'all_s_compatible_tuples':len(side),'all_s_compatible_full_lifts':sum(len(t['full_piece_lifts']) for t in side)})
     counts['saturated_columns']+=1
  for der in g['unit_derivatives']:
   omitted=pmap[der['piece']];r=der['contact_edge'][0];s=next(v for v in roots if v!=r)
   active=[p for p in g['pieces'] if p['id']!=omitted['id']]
   eligible=len(active)==2 and all(p['kind']=='mixed' for p in active)
   missing=[]
   if not eligible:missing.append('X consists of exactly two retained mixed pieces and no unary')
   if g['sigma'] not in (933,941):missing.append('exact canonical target Sigma')
   LP=eligible and any(set(p['support'])==set(sp) for p in active for sp in support_paths(p['support'])) and any(len(p['support'])==2 and ((p['support'][0]-p['support'][1])%5 in (1,4)) for p in active)
   if not LP:missing.append('long L plus short true-edge S support contract')
   if not any(not row['root_pairs'] and g['sigma']&(1<<row['index'])==0 for row in der['joins_X']):missing.append('X rejects an original target core beta')
   source_status.append({'graph':g['id'],'omitted_U':omitted['id'],'LP_source_status':'not triggered' if missing else 'triggered','missing':missing})
   for row in der['joins_X']:
    i=row['index'];beta=patterns[i]
    if not eligible:continue
    E={v:COL-{beta[b] for b in B if sorted((v,b)) in der['edges_X']} for v in roots}
    pairs=[]
    for a,b in PAIRS:
     pins=dict(zip(roots,(a,b)))
     if all(pins[v] in E[v] for v in roots) and all(any(compatible(p,t['tuple'],pins) for t in computed[p['id']][i]['tuples']) for p in active):pairs.append([a,b])
    need(pairs==row['root_pairs'],'retained complete joint mismatch')
    ri=roots.index(r);proj={pair[ri] for pair in pairs}
    if len(proj)!=1:counts['forcing_row_not_triggered']+=1;continue
    a=next(iter(proj));spokes=[b for b in B if sorted((r,b)) in der['edges_X']];m_r=sum(len(p['contacts'][str(r)]) for p in active)
    d_r=len(spokes)-len({beta[b] for b in spokes})
    need(len(spokes)+m_r==4 and len(E[r])==m_r+d_r,'low-root degree/spoke surplus')
    need(d_r in (0,1),'singleton forcing duplicate-spoke bound')
    cols=[]
    for b in sorted(E[s]):
     bads=[bad_column(p,computed[p['id']][i],r,s,b) for p in active];need(all(len(F)<=len(p['contacts'][str(r)]) for p,F in zip(active,bads)),'local capacity')
     V=set.union(*bads);allowed=E[r]-V;need(allowed<= {a},'non-singleton r projection')
     delta=m_r-sum(len(F) for F in bads);overlap=sum(len(F) for F in bads)-len(V);leak=len(V-E[r]);n=len(allowed)
     need(min(delta,overlap,leak)>=0 and delta+overlap+leak==n-d_r,'forcing capacity exact identity')
     if d_r==1:need(allowed=={a} and delta==overlap==leak==0,'Cartesian forced fibre')
     cols.append({'b':b,'allowed_r':sorted(allowed),'raw_columns':[sorted(F) for F in bads],'delta_o_lambda':[delta,overlap,leak],'rhs':n-d_r})
    new=not(g['sigma']&(1<<i))
    if new:
     T={t['tuple'][0] for t in computed[omitted['id']][i]['tuples']};need(T=={a},'new gamma U palette forcing failed');counts['new_gamma_forcing_rows']+=1
    for cell in row['all_16_fibres']:
     if cell['full_graph_lift'] is not None:proper_lift(der['vertices_X'],der['edges_X'],beta,dict(zip(roots,cell['pins'])),cell['full_graph_lift'])
    forcing.append({'graph':g['id'],'omitted_U':omitted['id'],'index':i,'r':r,'s':s,'forced_a':a,'new_gamma':new,'d_r':d_r,'E_r':sorted(E[r]),'E_s':sorted(E[s]),'columns':cols,'LP_target_status':'not triggered; calibration only'})
    counts['singleton_projection_rows']+=1
 need(negative is not None,'negative oracle control missing')
 need(not any(x['LP_source_status']=='triggered' for x in source_status),'unexpected LP source; inspect separately')
 return {'counts':dict(sorted(counts.items())),'full_support_transport':records,'endpoint_hub_calibration':hub_records,'saturated_contact_fibres':saturation,'singleton_forcing_columns':forcing,'unit_omission_source_coverage':source_status,'negative_complete_tuple_control':negative,
 'coverage':{'graphs':len(raw['graphs']),'new_graphs':0,'new_pieces':0,'LP_target_sources':0,'new_source_counterexamples':0,'transport':'triggered and holds on existing complete fibres','mixed_long_endpoint_control':'not triggered: existing consecutive-triple pieces are unary','arbitrary_size':'paper lemmas, not established by finite replay','source_realizability':'OPEN'}}

def lp_exclusion(profile,patterns):
 records=[];counts=Counter()
 for partition in profile['named_partitions']:
  center=partition['supports']['U'][1]
  for case in partition['cases']:
   rec={'start':partition['start'],'direction':partition['direction'],'sigma_G':case['sigma_G'],'beta_q':case['beta_q'],'Q_X':case['Q_X'],'U_middle':center,'Q_X_after_untouched_slot':[center]}
   if case['beta_q']!=center:
    rec['elimination']='X misses U middle; T4 acceptance forces beta singleton at that middle';counts['mask_beta_mismatch']+=1
   elif case['Q_X']!=[center]:
    rec['elimination']='X misses U middle; complete Q(X) can only be its singleton';counts['mask_pair_rejected']+=1
   else:
    beta=patterns[QINDEX[center]];need(len({beta[b] for b in B-{center}})==2,'singleton exterior must use two colors')
    branches=[]
    for t in (0,1,2):
     branches.append({'t_s':t,'sole_C_contact_count':5-t,'C_vertices':'{r} union V(L) union V(S), literally retained original vertices','root_rejection_colors':4-t,'upstream':{0:'docs/c5_no_spoke_exterior.md §4: single (5)',1:'docs/c5_single_spoke_four.md §1–5: single (4)',2:'docs/c5_two_spoke_three_contacts.md §1–5: single (3), any differently beta-colored spokes'}[t],'evidence':'arbitrary-size BASE paper and external Gallai, no source enumeration','result':'contradiction after exact hypothesis mapping'})
    rec['elimination']='all sole-component unique-degree5 cases t_s=0,1,2 are excluded by established BASE results';rec['branches']=branches;counts['single_root_cases']+=1;counts['single_root_spoke_branches']+=3
   records.append(rec)
 need(len(records)==150 and counts['single_root_cases']==14,'LP case accounting')
 return {'kind':'finite accounting of a paper proof; not a finite zero-survivor source search','all_seven_cells_covered':True,'named_partition_cases':records,'counts':dict(sorted(counts.items())),'paper_closure_scope':'only N45-U-LP of the requested task, conditional on listed BASE arbitrary-size exclusions','source_controls_triggered':0,'formal_adoption':'pending independent paper review; no shared source update'}

def build():
 inputs=read(OUT/'inputs.json')
 for rel,d in inputs['anchors'].items():need(sha((OUT/'frozen'/rel).read_bytes())==d,'anchor drift')
 supplement=read(OUT/'supplementary-inputs.json')
 for row in supplement['base_inputs']:need(sha((OUT/'base-source'/row['path']).read_bytes())==row['sha256'],'supplementary BASE drift')
 patterns=read(OUT/'base-source/artifacts/c5_cells/cells.json')['pattern_order']
 raw=read(OUT/'frozen/audits/2026-10-09-n45-su-j/certificate.json')
 profile=partitions_and_masks(patterns)
 return {'task':'N45-PR','BASE':BASE,'supplementary_inputs_sha256':sha((OUT/'supplementary-inputs.json').read_bytes()),'LP_paper_branch_accounting':lp_exclusion(profile,patterns),'inputs_sha256':sha((OUT/'inputs.json').read_bytes()),'checker_sha256':sha(Path(__file__).read_bytes()),'kind':'finite necessary support/mask identities and fixed complete-lift calibration; no source exclusion',
 'support_mask_profile':profile,'fixed_controls':calibration(patterns,raw),'claims':['N45-PR-TRANSPORT','N45-PR-ENDPOINT','N45-PR-SATURATION','N45-PR-FORCING','N45-PR-ESCAPE','N45-PR-UNTOP','N45-PR-LP-EXCLUSION'],'remaining_OPEN':'independent adoption of this paper candidate; singleton short and every other excluded task scope remain OPEN'}
def main():
 ap=argparse.ArgumentParser();mode=ap.add_mutually_exclusive_group(required=True);mode.add_argument('--generate',action='store_true');mode.add_argument('--check',action='store_true');ap.add_argument('--certificate',type=Path);args=ap.parse_args();path=args.certificate or OUT/'certificate-final.json'
 if args.generate:need(not path.exists(),'exclusive-create refused existing certificate')
 data=enc(build())
 if args.generate:
  need(path.resolve().is_relative_to(OUT.resolve()),'write outside own fresh directory')
  with path.open('xb') as f:f.write(data)
 else:need(path.read_bytes()==data,'certificate byte mismatch')
 d=json.loads(data);print(json.dumps({'mode':'check' if args.check else 'generate','certificate_sha256':sha(data),'counts':d['fixed_controls']['counts'],'LP_sources':0,'support_partitions':len(d['support_mask_profile']['named_partitions']),'mask_cells':7,'beta_Q_choices':15,'status':'PASS fixed identities/calibration; LP paper candidate separately proved from BASE; adoption pending'},sort_keys=True))
if __name__=='__main__':main()
