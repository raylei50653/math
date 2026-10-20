#!/usr/bin/env python3
"""Read-only exact replay. --build exclusively creates the local certificate."""
import argparse,copy,hashlib,json
from pathlib import Path
import model
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
OLD=ROOT/'audits/2026-10-19-r6-941-leakage-b89c591'
BASE='13dc5ff163045c85b5c82dde438eb5f275dab999'
INPUTS=[str(p.relative_to(ROOT)) for p in [OLD/'B/SOURCE_CONTRACT.md',OLD/'B/CORE.md',OLD/'B/FORCED_SECTORS.md',OLD/'A/PROOF.md',OLD/'A/source-positive-certificate.json',ROOT/'audits/2026-10-18-smaller-bad-e1617a2/B/PROOF.md']]
def sha(value):return hashlib.sha256(json.dumps(value,separators=(',',':'),sort_keys=True).encode()).hexdigest()
def add(*pairs):return [sum(c*v[i] for c,v in pairs) for i in range(274)]

def reconstruct():
 F=model.interfaces();M=F['M'];sec=F['sectors'];eight=F['eight'];ten=F['ten']
 K8=model.kempe(8,eight)
 initial8=[i for i in range(274) if all(M['G'][j][i]==0 for j in (1,4,6))]
 live8,rounds8=model.close(K8,initial8)
 assert len(live8)==225
 parts,A,basis=model.planar_basis(eight,live8);assert len(parts)==91 and len(basis)==44
 identities={
 'a1+a2=2Aa':add((1,M['Q1'][9]),(1,M['Q2'][9]),(-2,sec['Aa'])),
 'Ab=U1+V1+U2+V2':add((1,sec['Ab']),(-1,M['Q1'][4]),(-1,M['Q1'][6]),(-1,M['Q2'][4]),(-1,M['Q2'][6])),
 'Aa=TG+2UG':add((1,sec['Aa']),(-1,M['GB'][1]),(-2,M['GB'][4])),
 'VG=TG+UG':add((1,M['GB'][6]),(-1,M['GB'][1]),(-1,M['GB'][4]))}
 residuals={name:[str(sum(x*y for x,y in zip(v,b))) for b in basis] for name,v in identities.items()}
 assert all(v=='0' for row in residuals.values() for v in row)
 obs=[M['Q1'][9],M['Q2'][9],M['Q1'][1],M['Q1'][4],M['Q1'][6],M['Q2'][1],M['Q2'][4],M['Q2'][6],M['GB'][1],M['GB'][4],M['GB'][6],sec['Aa'],M['G'][9]]
 _,piv=model.rref([[sum(x*y for x,y in zip(v,b)) for v in obs] for b in basis]);assert len(piv)==9
 K10=model.kempe(10,ten);assert len(K10['columns'])==10798 and len(K10['hrows'])==7382
 forbiddenG=[i for i in range(2461) if any(F['C']['G'][j][i]>0 for j in (1,4,6))]
 qs=[i for i,t in enumerate(ten) if t[4]==t[6]]
 initial10=sorted(set(range(2461))-set(forbiddenG)-set(qs));live10,rounds10=model.close(K10,initial10)
 assert len(live10)==756 and all(F['C']['G'][9][i]==0 for i in live10)
 # Every live core cell could be positive here; this still cannot supply alpha.
 projection=model.mask([sum(F['C']['G'][j][i] for i in live10) for j in range(10)])
 assert projection==429
 chords={}
 for name,a,b,want in (('Rv',2,7,899),('Lw',3,8,899),('qt',4,9,1019)):
  zeros=[i for i,t in enumerate(ten) if t[a]==t[b]];initial=sorted(set(range(2461))-set(forbiddenG)-set(zeros));live,rounds=model.close(K10,initial)
  assert len(live)==want and all(F['C']['G'][9][i]==0 for i in live)
  projection2=model.mask([sum(F['C']['G'][j][i] for i in live) for j in range(10)]);assert projection2==429
  chords[name]={'extra_edge':name,'extra_zero_core_ids':zeros,'initial':initial,'rounds':rounds,'live':live,'source_projection':projection2,'source_alpha_zero':True}
 controls=[]
 oldcontrols=json.loads((OLD/'A/source-positive-certificate.json').read_text())['records']
 for rec in oldcontrols:
  core=rec['core_counts'];e=[sum(core[i]*mult for i,mult in row) for row in F['T']]
  assert e==rec['exterior_counts']
  graph={name:model.mv(M[name],e) for name in model.NAMES};assert graph==rec['graph_counts']
  Aa=sum(a*b for a,b in zip(sec['Aa'],e));Ab=sum(a*b for a,b in zip(sec['Ab'],e))
  for v in identities.values():assert sum(a*b for a,b in zip(v,e))==0
  assert Aa>0 and Ab>0 and model.mask(graph['G'])==941
  controls.append({'name':rec['name'],'graph_counts':graph,'Aa':Aa,'Ab':Ab,'d_a':rec['source_positive_subset_counts']['h_equals_a'],'d_b':rec['source_positive_subset_counts']['h_equals_b'],'q_equals_s_core_count':sum(core[i] for i in qs),'source_realized':False,'survives_unconditional_c_ge_5_count_model':True})
 # A specific legal Q2 lift with a=q=R, all pin colours kept together.
 q2branch=next(r for r in F['joint'] if r[6] and r[8][1] and r[7] and (lambda vals: vals[2]==r[4]==r[2])(tuple(map(int,model.ROWS[r[0]]))))
 return {'base':BASE,'source_scope':'full r6, original p,h=ell, original support exactly 941',
 'inputs_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in INPUTS},
 'rows':list(model.ROWS),'E_order':['a','n','R','L','q','c','x','y'],'core_order':['a','n','R','L','q','c','s','v','w','t'],
 'all_joint_records':F['joint'],'complete_E_transfer':[[list(v) for v in r] for r in F['T']],
 'all_core_cap_lifts':F['core_caps'],'literal_E_count_matrices':M,'original_alpha_sectors':sec,
 'source_E_closure':{'initial':initial8,'rounds':rounds8,'live':live8,'orbit_columns':len(K8['columns']),'columns_sha256':sha(K8['columns'])},
 'planar_count_proof':{'columns':91,'restricted_dimension':44,'basis_sha256':sha([[str(v) for v in b] for b in basis]),'observable_projection_rank':9,'identities':identities,'basis_residuals':residuals},
 'c_degree4_exclusion':{'extra_edge':'qs','extra_zero_core_ids':qs,'source_reject_zero_core_ids':forbiddenG,'initial':initial10,'rounds':rounds10,'live':live10,'literal_rows':K10['literal_count'],'H_rows':len(K10['hrows']),'noncrossing_partitions':K10['noncrossing_count'],'orbit_columns':len(K10['columns']),'columns_sha256':sha(K10['columns']),'source_projection':projection,'source_alpha_zero':True,'uses_U319':False,'uses_source_positive_subsets':False,'uses_planar_signed_span':False},
 'additional_chord_exclusions':chords,'controls':controls,'q2_a_equals_q_equals_R_lift':q2branch,
 'completed_interior_cost':{'Q1':-4,'Q2':-4,'GB':-2},'main_target_closed':False}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--certificate',type=Path,default=D/'certificate.json');ap.add_argument('--negative-controls',action='store_true');args=ap.parse_args()
 expected=reconstruct();caps=expected.pop('all_core_cap_lifts');expected['cap_lifts']={'path':'cap-lifts.json','canonical_sha256':sha(caps),'entries':len(caps)};chords=expected.pop('additional_chord_exclusions');expected['additional_chords']={'path':'chord-closures.json','canonical_sha256':sha(chords),'edges':sorted(chords)}
 if args.build:
  if (D/'cap-lifts.json').exists():assert json.loads((D/'cap-lifts.json').read_text())==caps
  else:
   with (D/'cap-lifts.json').open('x') as f:json.dump(caps,f,ensure_ascii=False,indent=2);f.write('\n')
  with (D/'chord-closures.json').open('x') as f:json.dump(chords,f,ensure_ascii=False,indent=2);f.write('\n')
  with args.certificate.open('x') as f:json.dump(expected,f,ensure_ascii=False,indent=2);f.write('\n')
 actualchords=json.loads((D/'chord-closures.json').read_text());assert actualchords==chords,'chord closures differ from exact reconstruction'
 actual=json.loads(args.certificate.read_text());actualcaps=json.loads((D/'cap-lifts.json').read_text());assert actualcaps==caps,'complete cap lifts differ from exact reconstruction'
 assert actual==expected,'certificate differs from independent exact reconstruction'
 negative=[]
 if args.negative_controls:
  changes=[]
  r=copy.deepcopy(actual);r['all_joint_records'][100][8][0]^=1;changes.append(('cross_candidate_refusal_flags',r))
  r=copy.deepcopy(actual);r['q2_a_equals_q_equals_R_lift'][7]=[];changes.append(('drop_Q2_a_equals_q_branch',r))
  badcaps=copy.deepcopy(actualcaps);i=next(i for i,c in enumerate(badcaps) if c['left']);badcaps[i]['left'].pop();assert badcaps!=caps;negative.append('drop_complete_private_lift')
  r=copy.deepcopy(actual);i=next(i for i,row in enumerate(r['complete_E_transfer']) if any(v[1]>1 for v in row));j=next(j for j,v in enumerate(r['complete_E_transfer'][i]) if v[1]>1);r['complete_E_transfer'][i][j][1]=1;changes.append(('drop_transfer_multiplicity',r))
  r=copy.deepcopy(actual);r['controls'][0]['d_b']=0;changes.append(('omit_source_positive_fibre',r))
  r=copy.deepcopy(actual);r['completed_interior_cost']['Q1']=-3;changes.append(('omit_completed_identification_cost',r))
  r=copy.deepcopy(actual);r['c_degree4_exclusion']['extra_zero_core_ids']=[];changes.append(('omit_actual_qs_edge',r))
  r=copy.deepcopy(actual);r['c_degree4_exclusion']['rounds'][0].pop();changes.append(('truncate_universal_component_round',r))
  r=copy.deepcopy(actual);r['planar_count_proof']['identities']['a1+a2=2Aa'][0]+=1;changes.append(('alter_exact_count_identity',r))
  r=copy.deepcopy(actual);r['controls'][0]['graph_counts']=r['controls'][1]['graph_counts'];changes.append(('cross_source_complete_counts',r))
  for name,r in changes:
   assert r!=expected;negative.append(name)
 print(json.dumps({'pass':True,'base':BASE,'c4_closure_round_removed':[len(r) for r in expected['c_degree4_exclusion']['rounds']],'c4_live':756,'c4_alpha_zero':True,'additional_chords_excluded':sorted(chords),'count_identities':list(expected['planar_count_proof']['identities']),'restricted_space_dimension':44,'negative_controls_rejected':negative,'main_target':'OPEN'},ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
