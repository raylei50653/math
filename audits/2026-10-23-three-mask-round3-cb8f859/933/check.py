#!/usr/bin/env python3
"""Read-only exact audit of fourteen same-E hexagon completions.

--build creates certificate.json exclusively. No exterior graph is enumerated.
"""
import argparse,copy,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BASE='cb8f8593e273a7426ecadd59797a6e643cc4768e'
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
PIN=('a','n','R','L','q','c','x','y')
HEX=('a','n','R','L','q','b')
SOURCE='audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json'
PREV='audits/2026-10-23-three-mask-methods-cb8f859/933/certificate.json'
CAT='audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/artifacts/c5_cells/cells.json'
SPLITS=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))

def digest(data):return hashlib.sha256(data).hexdigest()
def canonical(t):
 d={};return tuple(d.setdefault(c,len(d)) for c in t)
def frozen(p):return (HERE/'frozen'/p).read_bytes()
def inputs():
 m=json.loads((HERE/'INPUTS.json').read_text());assert m['base']==BASE
 for e in m['files']:
  d=frozen(e['path']);assert len(d)==e['bytes'] and digest(d)==e['sha256'],'frozen bytes: '+e['path']
  assert (ROOT/e['path']).read_bytes()==d,'immutable authority drift: '+e['path']
 return m

def rref(matrix):
 if not matrix:return [],[]
 a=[[F(x) for x in row] for row in matrix];piv=[]
 for c in range(len(a[0])):
  i=next((i for i in range(len(piv),len(a)) if a[i][c]),None)
  if i is None:continue
  j=len(piv);a[i],a[j]=a[j],a[i];v=a[j][c];a[j]=[x/v for x in a[j]]
  for i in range(len(a)):
   if i!=j and a[i][c]:
    v=a[i][c];a[i]=[x-v*y for x,y in zip(a[i],a[j])]
  piv.append(c)
 return a,piv

def kernel(a,width):
 rr,piv=rref(a);out=[]
 for c in range(width):
  if c in piv:continue
  v=[F(0)]*width;v[c]=1
  for j,k in enumerate(piv):v[k]=-rr[j][c]
  mult=math.lcm(*(x.denominator for x in v));v=[int(x*mult) for x in v];g=math.gcd(*v);out.append([x//g for x in v])
 return list(map(list,zip(*out))) if out else [[] for _ in range(width)]

def mm(a,b):
 cols=list(zip(*b));return [[sum(x*y for x,y in zip(r,c)) for c in cols] for r in a]
def partitions(t=(0,)):
 if len(t)==8:yield t;return
 for c in range(max(t)+2):yield from partitions(t+(c,))
def triangulations(v):
 if len(v)<=3:return [set()]
 out=[]
 for j in range(1,len(v)-1):
  for a in triangulations(v[:j+1]):
   for b in triangulations(v[j:]):
    es=a|b
    for edge in ((v[0],v[j]),(v[j],v[-1])):
     if abs(v.index(edge[0])-v.index(edge[1]))>1:es.add(tuple(sorted(edge)))
    out.append(es)
 return out

def cap(tuples,tri):
 idx={t:i for i,t in enumerate(tuples)};mats=[[[0]*274 for _ in ROWS] for _ in tri];G=[[0]*274 for _ in ROWS];records=[]
 rim=list(zip(PIN,PIN[1:]+PIN[:1]));base=rim+[('a','b'),('b','c'),('b','q')]
 original=base+[('p',v) for v in ('a','b','q','h','n')]+[('h',v) for v in ('q','L','R','n')]
 def proper(c,es):return all(c[u]!=c[v] for u,v in es)
 for ri,w in enumerate(ROWS):
  x,y,a,b,c=map(int,w)
  for n,R,L,q in itertools.product(range(4),repeat=4):
   t=(a,n,R,L,q,c,x,y);colors=dict(zip(PIN,t),b=b);eid=idx[canonical(t)] if proper(colors,rim) else None
   lifts=[[p,h] for p,h in itertools.product(range(4),repeat=2) if proper(dict(colors,p=p,h=h),original)]
   formula=[[p,h] for p,h in itertools.product(range(4),repeat=2) if eid is not None and b not in {a,c,q} and p not in {a,b,q,n,h} and h not in {p,q,L,R,n}]
   assert lifts==formula,'full original edge lifts versus independent neighbourhood formula'
   flags=[int(proper(colors,base+list(ds))) for ds in tri]
   records.append([ri,n,R,L,q,eid,lifts,flags])
   if eid is not None:
    G[ri][eid]+=len(lifts)
    for M,flag in zip(mats,flags):M[ri][eid]+=flag
 return G,mats,records

def sign_close(B,initial):
 zeros=set(initial);steps=[];width=len(B[0])
 while True:
  K=kernel([B[j] for j in sorted(zeros) if any(B[j])],width);S=mm(B,K)
  if not K[0]:return S,steps,sorted(zeros),list(range(274))
  rr,piv=rref(list(map(list,zip(*S))));T=list(map(list,zip(*rr[:len(piv)])));forced=set();witness=[]
  for j,row in enumerate(T):
   if any(row) and all(x<=0 for x in row):
    terms=[[piv[k],str(x)] for k,x in enumerate(row) if x];new={k for k,_ in terms}-zeros
    if not new:continue
    residual=[x-sum(F(c)*B[k][i] for k,c in terms) for i,x in enumerate(B[j])]
    assert not any(mm([residual],K)[0]),'sign identity exactness'
    witness.append({'row':j,'nonpositive_terms':terms});forced|=new
  if not forced:return S,steps,sorted(zeros),[j for j,row in enumerate(S) if not any(row)]
  steps.append({'dimension':len(S[0]),'witnesses':witness,'new_zeros':sorted(forced)});zeros|=forced

def component_options(t,nc,index,split,full=False):
 side={c:j for j,pair in enumerate(split) for c in pair};flip={c:pair[1-k] for pair in split for k,c in enumerate(pair)};result=[]
 for part in nc:
  blocks=[[i for i,x in enumerate(part) if x==b] for b in range(max(part)+1)]
  if any(len({side[t[i]] for i in block})>1 for block in blocks):continue
  if any(side[t[i]]==side[t[(i+1)%8]] and part[i]!=part[(i+1)%8] for i in range(8)):continue
  lifts=[];orbit=set()
  for subset in range(1<<len(blocks)):
   word=tuple(flip[c] if subset>>part[i]&1 else c for i,c in enumerate(t));eid=index[canonical(word)];orbit.add(eid)
   assert all(word[i]!=word[(i+1)%8] for i in range(8))
   if full:lifts.append([subset,list(word),eid])
  record={'partition':list(part),'orbit':sorted(orbit)}
  if full:record['all_literal_boundary_switch_lifts']=lifts
  result.append(record)
 assert result
 return result

def compute():
 inputs();src=json.loads(frozen(SOURCE));old=json.loads(frozen(PREV));tuples=[tuple(t) for t in src['tuples']]
 expected=sorted({canonical(t) for t in itertools.product(range(4),repeat=8) if all(t[i]!=t[(i+1)%8] for i in range(8))})
 assert tuples==expected and len(tuples)==274 and src['pin_order']==list(PIN)
 fours=list(itertools.combinations(range(8),4));nc=[p for p in partitions() if not any(p[i]==p[k] and p[j]==p[l] and p[i]!=p[j] for i,j,k,l in fours)]
 cols=[]
 for p in nc:
  col=[int(all(p[i]!=p[j] or t[i]==t[j] for i in range(8) for j in range(i))) for t in tuples]
  if any(col):cols.append(col)
 A=list(map(list,zip(*cols)));assert len(nc)==1430 and len(cols)==91 and len(rref(A)[1])==91
 live=set(next(r['surviving_ids'] for r in src['results'] if r['source_mask']==933));B=mm(A,kernel([r for j,r in enumerate(A) if j not in live],91));assert len(B[0])==18
 tri=sorted({tuple(sorted(t)) for t in triangulations(HEX)});assert len(tri)==14
 # Cross-check the recursion against the independent geometric definition.
 all_diags=[tuple(sorted((HEX[i],HEX[j]))) for i in range(6) for j in range(i+2,6) if (i,j)!=(0,5)]
 def cross(e,f):
  a,b=sorted(HEX.index(v) for v in e);c,d=sorted(HEX.index(v) for v in f);return a<c<b<d or c<a<d<b
 brute=sorted(tuple(sorted(t)) for t in itertools.combinations(all_diags,3) if all(not cross(e,f) for e,f in itertools.combinations(t,2)))
 assert tri==brute
 G,M,records=cap(tuples,tri);assert G==old['count_matrices']['G']
 assert len(records)==2560 and sum(len(r[6]) for r in records)==175 and sum(not r[6] for r in records)==2392
 assert M[6]==old['count_matrices']['GB'],'fixed old fan appears exactly once as T6'
 def identity(row,terms,space=B):
  residual=[x-sum(c for k,c in terms if k==i) for i,x in enumerate(row)];assert not any(mm([residual],space)[0])
 def coord(j,terms):identity([int(k==j) for k in range(274)],terms)
 coord(73,[(196,1)]);coord(76,[(198,1)]);coord(30,[(73,1),(257,1)]);coord(30,[(76,1),(259,1)])
 identity(G[9],[(30,4)])
 for i in (0,1):
  identity(M[i][1],[]);identity(M[i][4],[(73,1)]);identity(M[i][6],[(76,1)])
 identity(M[0][9],[(30,4)]);identity(M[1][9],[(257,1),(259,1)])
 nogo=[]
 for i in range(2,14):
  initial=sorted(j for j in range(274) if M[i][6][j]);S,steps,known,zeros=sign_close(B,initial)
  assert not any(mm([G[9]],S)[0]),'01212 empty kills original acceptance on T'+str(i)
  nogo.append({'candidate':i,'assumed_empty_row':'01212','initial_complete_fibre_zeros':initial,'sign_steps':steps,'known_zeros':known,'linear_zeros':zeros,'remaining_dimension':len(S[0]),'killed_required_original_positive':'01232'})
 # For the two new candidates the common reduction condition is exactly U=V=0.
 common={j for j in range(274) if any(M[0][r][j] for r in (1,4,6))};S,steps,known,zeros=sign_close(B,common);assert len(S[0])==16 and not steps
 assert all(any(row) for i,row in enumerate(mm(G,S)) if 933>>i&1),'no strict original positive row killed by this linear test'
 identity(M[0][9],[(30,4)],S);assert not any(mm([[2*a-b for a,b in zip(M[1][9],G[9])]],S)[0])
 catalogue=set(map(int,json.loads(frozen(CAT))['cells']))
 outside=[mask for mask in range(1024) if mask>>9&1 and all(not(mask>>r&1) for r in (1,4,6))]
 assert len(outside)==64 and not catalogue.intersection(outside),'same-candidate three-zero bad certificate'
 index={t:i for i,t in enumerate(tuples)};zero_set=set(zeros);survival=[]
 for j in range(274):
  if j in zero_set:continue
  for si,split in enumerate(SPLITS):
   options=component_options(tuples[j],nc,index,split);good=[o for o in options if not set(o['orbit'])&zero_set]
   assert good,'this diagnostic would add a new Kempe zero'
   survival.append({'tuple':j,'split':si,'one_necessary_surviving_partition':good[0],'compatible_partition_count':len(options),'surviving_partition_count':len(good)})
 narrow=[]
 for j in (257,259):
  for si in (1,2):
   options=component_options(tuples[j],nc,index,SPLITS[si],full=True);good=[o for o in options if not set(o['orbit'])&zero_set]
   assert len(options)==12 and len(good)==1
   narrow.append({'tuple':j,'split':si,'all_options':options,'unique_necessary_survivor':good[0]})
 return {'base':BASE,'input_manifest_sha256':digest((HERE/'INPUTS.json').read_bytes()),'source_mask':933,'row_order':list(ROWS),'pin_order':list(PIN),'hole_order':list(HEX),'triangulations':[[list(e) for e in t] for t in tri],'interior_vertex_delta':-2,'parallel_policy':'delete only the new duplicate; keep every original E edge and outer edge','original_count_matrix':G,'candidate_count_matrices':M,'complete_local_fibres':records,'full_lift_count':175,'empty_old_fibre_count':2392,'space_dimension':18,'identities':{'U_id':73,'V_id':76,'W_id':257,'Wprime_id':259,'U_alias':196,'V_alias':198,'source_alpha':'4(U+W)=4(V+Wprime)','T0_counts_01021_01202_01212_01232':['0','U','V','4(U+W)'],'T1_counts_01021_01202_01212_01232':['0','U','V','W+Wprime']},'twelve_nogos':nogo,'common_zero_condition':{'actual_E_coordinates':[73,76],'remaining_dimension':16,'linear_zero_ids':zeros,'original_positive_rows_killed':[],'bad_support_masks':outside,'all_original_strict_positives_preserved_as_nonzero_functionals':True},'necessary_component_survival_controls':survival,'four_unique_partition_controls':narrow,'minimum_original_source_consequence':'U+V>0','smaller_bad_constructed':False,'general_933_exclusion':False,'actual_source_realization':False,'necessary_system_feasibility_claimed':False,'all_fourteen_full_supports_in_K132_claimed':False,'controls':{'complete_local_fibres_and_count_identities':'triggered and holds','twelve_designated_certificate_nogos':'triggered and holds','conditional_two_new_reductions':'triggered and holds','full_original_r6_933_source_graph':'not triggered','common_16dim_space_feasibility':'not triggered','independent_palette_witnesses_form_one_source':'not triggered'}}

def verify(c,expected):assert c==expected,'complete semantic certificate mismatch'
def negatives(c,expected):
 out=[]
 def reject(name,change):
  bad=copy.deepcopy(c);change(bad)
  try:verify(bad,expected)
  except AssertionError:out.append({'name':name,'status':'counterexample rejected'})
  else:raise AssertionError('accepted corrupted certificate '+name)
 reject('change_original_rotation',lambda x:x['hole_order'].reverse())
 reject('erase_original_exterior_attachment',lambda x:x['pin_order'].__setitem__(2,'n'))
 reject('erase_an_empty_old_fibre',lambda x:x['complete_local_fibres'].pop(next(i for i,r in enumerate(x['complete_local_fibres']) if not r[6])))
 reject('erase_one_old_full_lift',lambda x:next(r[6] for r in x['complete_local_fibres'] if r[6]).pop())
 reject('lose_a_complete_ten_row_projection',lambda x:x['candidate_count_matrices'][0].pop())
 reject('swap_E_vectors_between_candidates',lambda x:x['candidate_count_matrices'].__setitem__(1,x['candidate_count_matrices'][0]))
 reject('overstate_vertex_saving',lambda x:x.__setitem__('interior_vertex_delta',-4))
 reject('change_acceptance_factor',lambda x:x['identities']['T1_counts_01021_01202_01212_01232'].__setitem__(3,'2(W+Wprime)'))
 reject('drop_one_of_twelve_nogos',lambda x:x['twelve_nogos'].pop())
 reject('omit_strict_original_positive_obligation',lambda x:x['common_zero_condition'].__setitem__('all_original_strict_positives_preserved_as_nonzero_functionals',False))
 reject('omit_one_literal_component_subset_switch',lambda x:x['four_unique_partition_controls'][0]['all_options'][0]['all_literal_boundary_switch_lifts'].pop())
 reject('invent_source_realization_from_16dim_space',lambda x:x.__setitem__('actual_source_realization',True))
 reject('invent_necessary_feasibility',lambda x:x.__setitem__('necessary_system_feasibility_claimed',True))
 reject('upgrade_designated_nogos_to_full_support',lambda x:x.__setitem__('all_fourteen_full_supports_in_K132_claimed',True))
 reject('invent_smaller_bad',lambda x:x.__setitem__('smaller_bad_constructed',True))
 return out

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--build',action='store_true');parser.add_argument('--negative',action='store_true');args=parser.parse_args();e=compute();path=HERE/'certificate.json'
 if args.build:
  with path.open('x') as f:json.dump(e,f,indent=2);f.write('\n')
 c=json.loads(path.read_text());verify(c,e)
 result={'status':'PASS','base':BASE,'candidate_count':14,'new_candidates_with_common_open_obligation':[0,1],'designated_nogos':12,'normal_source_graph_control':'not triggered','immutable_input_drift':0,'necessary_feasibility_claimed':False,'certificate_sha256':digest(path.read_bytes())}
 if args.negative:result['semantic_negative_controls']=negatives(c,e)
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
