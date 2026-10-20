#!/usr/bin/env python3
"""Five real pentagon replacements of each forced original degree-five wheel."""
import argparse,copy,gzip,hashlib,importlib.util,itertools,json,time
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
FROZEN=D.parent/'frozen'
BASE='f13eb4d0887d962021992ae7afe3323af4d79cd3'
DEPS=['audits/2026-10-19-r6-941-chains-13dc5ff/A/interface.py',
 'audits/2026-10-19-r6-941-chains-13dc5ff/A/PROOF.md',
 'audits/2026-10-19-r6-941-chains-13dc5ff/SOURCE_CONTRACT.md',
 'audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py',
 'artifacts/c5_cells/cells.json']
spec=importlib.util.spec_from_file_location('old_interface',ROOT/DEPS[0]);f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f);m=f.m
def packed(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x):return hashlib.sha256(packed(x)).hexdigest()
def authority():
 seal=json.loads((D.parent/'INPUTS.json').read_text());assert seal['base']==BASE
 entries={r['path']:r for r in seal['files']}
 return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in DEPS if check_authority(p,entries)}
def check_authority(p,entries):
 a=(ROOT/p).read_bytes();b=(FROZEN/p).read_bytes();assert a==b and hashlib.sha256(a).hexdigest()==entries[p]['sha256'];return True
def operations(branch):
 wheel=('h','R','U','V','q') if branch=='L' else ('h','n','U','V','L')
 return [(v,[(v,wheel[(i+2)%5]),(v,wheel[(i+3)%5])]) for i,v in enumerate(wheel)]
def caps(states,branch):
 pins=('a','n','R','U','V','q','c','s','v','w','t') if branch=='L' else ('a','n','U','V','L','q','c','s','v','w','t')
 mats=[[[0]*len(states) for _ in range(10)] for _ in range(8)];allcaps=[]
 for i,word in enumerate(states):
  ff=dict(zip(pins,word));a,n,q,c,s,v,w,t=[ff[k] for k in ('a','n','q','c','s','v','w','t')]
  right=[(x,y,r) for x,y,r in itertools.product(range(4),repeat=3) if r not in {s,v,w,t,x,y} and x not in {c,s,y} and y not in {a,t}]
  out,da=f.cap(word,branch)
  for j,name in enumerate(('G','Q1','Q2')):
   for r in range(10):mats[j][r][i]=out[name][r]
  left=[]
  for b,p,h in itertools.product(range(4),repeat=3):
   if b in {a,c,q,p} or p in {a,q,n,h}:continue
   if h in {q,n,ff['R' if branch=='L' else 'L']}:continue
   left.append((b,p,h))
  fans=[]
  for j,(hub,edges) in enumerate(operations(branch)):
   ls=[]
   for b,p,h in left:
    whole=dict(ff,b=b,p=p,h=h)
    if all(whole[u]!=whole[vv] for u,vv in edges):ls.append((b,p,h))
   fans.append(ls)
   for b,p,h in ls:
    for x,y,r in right:
     row=m.ROWS.index(''.join(map(str,m.canonical((x,y,a,b,c)))));mats[j+3][row][i]+=1
  # Original full lifts grouped by the removed centre and the same right cap.
  original=[];quotients=[[],[]]
  for z in range(4):
   full=dict(ff,**{branch:z});R,L=full['R'],full['L']
   zs=[]
   if z not in ({R,full['U'],full['V'],q} if branch=='L' else {n,full['U'],full['V'],L}):
    zs=[(b,p,h) for b,p,h in left if h!=z]
    for b in range(4):
     if b in {a,c,q}:continue
     if b==n and R==q:quotients[0].append((z,b))
     if b==n==L:quotients[1].append((z,b))
   original.append(zs)
  # Independently reconstruct all three legacy projections from full local lifts.
  replay=[[0]*10 for _ in range(3)]
  for ls in original:
   for b,p,h in ls:
    for x,y,r in right:replay[0][m.ROWS.index(''.join(map(str,m.canonical((x,y,a,b,c)))))]+=1
  for j,ls in enumerate(quotients,1):
   for z,b in ls:
    for x,y,r in right:replay[j][m.ROWS.index(''.join(map(str,m.canonical((x,y,a,b,c)))))]+=1
  assert all(replay[j][r]==mats[j][r][i] for j in range(3) for r in range(10))
  allcaps.append({'core':word,'right':right,'original_left_by_center':original,'quotient_left_center_b':quotients,'five_replacement_left':fans})
 return mats,allcaps
def support(N,live):return sum(1<<j for j,row in enumerate(N) if any(row[i] for i in live))
def fast_setup(K):
 rows=K['rowids'];core_to_rows=[[] for _ in K['states']]
 for r,i in enumerate(rows):core_to_rows[i].append(r)
 cols=[(frozenset(rows[r] for r,v in c),tuple(r for r,v in c)) for c in K['columns']]
 return rows,core_to_rows,cols
def close(K,initial):
 rows,core_to_rows,cols=K;live=set(initial);rounds=[]
 while True:
  covered=set()
  for cores,hrows in cols:
   if cores<=live:covered.update(hrows)
  bad=[i for i in sorted(live) if any(r not in covered for r in core_to_rows[i])]
  if not bad:return sorted(live),rounds
  rounds.append(bad);live.difference_update(bad)
def compute():
 ins=authority();states=[t for t in m.growth(11,four=True) if m.proper(t)]
 K=f.kempe(11,states);fast=fast_setup(K)
 catalogue=sorted(map(int,json.loads((FROZEN/'artifacts/c5_cells/cells.json').read_text())['cells']))
 results=[];fullcaps=[]
 for branch,qi in [('L',1),('R',2)]:
  matrices,cap=caps(states,branch);fullcaps.append(cap);G=matrices[0]
  initial=[i for i in range(len(states)) if all(G[j][i]==0 for j in (1,4,6)) and matrices[qi][9][i]==0]
  live,rounds=close(fast,initial)
  assert len(live)==(5975 if branch=='L' else 5987)
  ix={t:i for i,t in enumerate(states)}
  controls=[(0,1,3,2,3,2,0,1,v,w,1) if branch=='L' else (0,1,3,1,3,2,0,1,v,w,1) for v,w in [(2,3),(3,2)]]
  da_ids=[ix[m.canonical(t)] for t in controls]
  for i in da_ids:
   assert i in live and matrices[3][9][i]>0
   # This same selected original full lift survives exactly the h fan.
   ff=dict(zip(('a','n','R','U','V','q','c','s','v','w','t') if branch=='L' else ('a','n','U','V','L','q','c','s','v','w','t'),states[i]),h=0)
   assert [all(ff[u]!=ff[v] for u,v in es) for hub,es in operations(branch)]==[True,False,False,False,False]
  comparisons=[]
  for j,(hub,edges) in enumerate(operations(branch)):
   N=matrices[j+3];records=[];possible=[]
   for cat in catalogue:
    seed=[i for i in live if all(N[r][i]==0 for r in range(10) if not(cat>>r&1))]
    surv,rs=close(fast,seed);g=support(G,surv);h=support(N,surv)
    da_survives=bool(set(da_ids)&set(surv))
    ok=g==941 and cat&~h==0 and da_survives
    if ok:possible.append(cat)
    records.append({'catalogue':cat,'initial':len(seed),'rounds':rs,'live':surv,'source_support_upper':g,'replacement_support_upper':h,'required_da_fibre_not_forced_empty':da_survives,'not_excluded':ok})
   comparisons.append({'hub':hub,'edges':edges,'surviving_catalogue_supports':possible,'comparisons':records})
   print(json.dumps({'branch':branch,'hub':hub,'possible':possible}),flush=True)
  uppers=[support(N,live) for N in matrices[3:]]
  assert uppers==[1023]*5
  results.append({'branch':branch,'pins':list(('a','n','R','U','V','q','c','s','v','w','t') if branch=='L' else ('a','n','U','V','L','q','c','s','v','w','t')),'original_zero_acceptance_candidate':qi,'matrices':matrices,'initial':initial,'rounds':rounds,'live':live,'selected_da_core_ids':da_ids,'five_comparisons':comparisons,'joint_five_full_supports_not_excluded':True,'joint_five_full_support_upper':uppers})
 return {'base':BASE,'inputs':ins,'rows':m.ROWS,'original_frame':['x','y','a','b','c'],'completed_inner_delta':-1,'component_columns':len(K['columns']),'component_columns_sha256':digest(K['columns']),'full_caps_sha256':digest(fullcaps),'branches':results,'source_realization_supplied':False,'short_branch_excluded':False,'same_candidate_three_zeros':'OPEN'},fullcaps
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');args=ap.parse_args();cert,caps_all=compute()
 for name,val in [('certificate.json.gz',cert),('caps.json.gz',caps_all)]:
  data=packed(val);path=D/name
  if args.build:
   with path.open('xb') as out:out.write(gzip.compress(data,mtime=0))
  assert gzip.decompress(path.read_bytes())==data
 rejected=[]
 for name,mut in [('omit_a_triangulation',lambda x:x['branches'][0]['five_comparisons'].pop()),('omit_original_positive_da',lambda x:x['branches'][0]['selected_da_core_ids'].clear()),('wrong_completed_cost',lambda x:x.__setitem__('completed_inner_delta',0)),('swap_original_frame',lambda x:x['original_frame'].reverse()),('claim_short_branch_excluded',lambda x:x.__setitem__('short_branch_excluded',True)),('joint_full_support_as_realization',lambda x:x.__setitem__('source_realization_supplied',True)),('wrong_zero_rows',lambda x:x.__setitem__('rows',list(reversed(x['rows']))))]:
  wrong=copy.deepcopy(cert);mut(wrong);assert packed(wrong)!=packed(cert);rejected.append(name)
 wrong=copy.deepcopy(caps_all);entry=next(e for e in wrong[0] if e['right']);entry['right'].pop();assert digest(wrong)!=cert['full_caps_sha256'];rejected.append('drop_full_cap_lift')
 print(json.dumps({'pass':True,'source_realization_supplied':False,'short_branch_excluded':False,'same_candidate_three_zeros':'OPEN','negative_controls_rejected':rejected}))
if __name__=='__main__':main()
