#!/usr/bin/env python3
"""Independent integral Fourier rank review; no LP or large global elimination.

For each local template B, exact FWHT(B) checks the Fourier upper bound.
For each allowed frequency, a signed sum of one subgroup's complete coset
columns reconstructs that Walsh character, giving the matching lower bound.
Derived parent artifacts are pinned by their observed bytes SHA in the result.
"""
import argparse,collections,gzip,hashlib,json,math,sys,time
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]; AUD=HERE.parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check',action='store_true',help='read-only replay (also the default)')
parser.add_argument('--seed',type=int,default=0,help='permute local transform columns and constructive witnesses')
parser.add_argument('--output',type=Path,help='write a new result under algebra/; existing files are never overwritten')
args=parser.parse_args()
if args.check and args.output: parser.error('--check and --output are mutually exclusive')
rng=np.random.default_rng(args.seed)
start=time.monotonic()
def read_gz(path): return json.loads(gzip.decompress(path.read_bytes()))
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
templates=read_gz(AUD/'templates/templates.json.gz')
rowmap=read_gz(AUD/'templates/row_map.json.gz')['rows']
colmap=read_gz(AUD/'templates/column_map.json.gz')['original_column_order']
# Independently price every literal incidence entry against the exported map.
base=json.loads((AUD/'BASE.json').read_text())
original_path=ROOT/'audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/orbits.json.gz'
expected=next(x['sha256'] for x in base['inputs'] if x['path']==str(original_path.relative_to(ROOT)))
assert digest(original_path)==expected
original=read_gz(original_path)
assert len(original['rowids'])==len(rowmap)
live=set(original['live']); rowlookup={}
for (h,s),mapped in zip(original['rowids'],rowmap):
 assert mapped[:2]==[h,s]
 colors=[(h>>(2*(12-i)))&3 for i in range(13)]
 palettes=[c//2 for c in colors]
 assert palettes[0]==0
 membership=sum(q<<i for i,q in enumerate(palettes))
 contacts=[0]+[i for i in range(1,13) if palettes[i]!=palettes[i-1]]
 if palettes[-1]==palettes[0]: contacts.pop()
 assert len(contacts)%2==0 and len(contacts)>=2
 assert colors[0]==0 and colors[contacts[1]]==2
 phase=sum((colors[i]&1)<<(r-2) for r,i in enumerate(contacts) if r>=2)
 assert mapped[2:]==[membership,len(contacts)//2,phase,int(s in live)]
 rowlookup[h]=mapped
assert len(colmap)==len(original['columns'])
for mapped,col in zip(colmap,original['columns']):
 q,k,j=mapped
 coords=[rowlookup[h] for h in col]
 assert all(r[2]==q and r[3]==k and r[5] for r in coords)
 assert sorted(r[4] for r in coords)==templates[str(k)][j]
del original,rowlookup
claimed=json.loads((AUD/'fourier/ranks.json').read_text())
metadata={r['k']:r for r in claimed['templates']}
parity=np.asarray([i.bit_count()&1 for i in range(1024)],dtype=np.int8)
results=[]
for k0,cols in templates.items():
 k=int(k0); n=4**(k-1)
 B=np.zeros((n,len(cols)),dtype=np.int16)
 groups=collections.defaultdict(list)
 for j,col in enumerate(cols):
  B[col,j]=1
  # The subgroup of an affine coset is obtained by translating its minimum.
  seed=min(col); subgroup=tuple(sorted(x^seed for x in col))
  groups[subgroup].append(j)
 F=B[:,rng.permutation(B.shape[1])].astype(np.int32)
 step=1
 while step<n:
  # Each reshape group is one butterfly; copies avoid write/read overlap.
  V=F.reshape(-1,2*step,F.shape[1])
  a=V[:,:step].copy(); b=V[:,step:].copy()
  V[:,:step]=a+b; V[:,step:]=a-b
  step*=2
 allowed=np.flatnonzero(np.any(F!=0,axis=1))
 assert allowed.tolist()==metadata[k]['allowed_frequencies']
 # Each column is an affine subgroup indicator, so all cosets sharing the
 # subgroup are disjoint and cover the entire local phase cube.
 witnesses={}
 group_items=list(groups.items())
 for group_index in rng.permutation(len(group_items)):
  subgroup,js=group_items[int(group_index)]
  assert np.all(B[:,js].sum(axis=1)==1)
  assert len(js)==n//len(subgroup)
  # The annihilator consists exactly of these zero-parity frequencies.
  ann=[a for a in range(n) if all(parity[a&h]==0 for h in subgroup)]
  for a in ann:
   if a in witnesses: continue
   signs=np.asarray([1-2*int(parity[a&cols[j][0]]) for j in js],dtype=np.int16)
   character=1-2*parity[np.arange(n)&a]
   assert np.array_equal(B[:,js]@signs,character)
   witnesses[a]=js
 assert set(witnesses)==set(map(int,allowed))
 # Walsh characters are pairwise orthogonal (norm squared n); this exact
 # reconstruction proves rank >= len(allowed), while F proves <=.
 results.append({'k':k,'rows':n,'columns':len(cols),'subgroups':len(groups),
  'exact_rank':len(allowed),'all_forbidden_Fourier_coefficients_zero':True,
  'every_allowed_character_reconstructed_as_signed_column_sum':True})
ranks={r['k']:r['exact_rank'] for r in results}
rows_by_q=collections.defaultdict(set)
ks={}
for h,s,q,k,phase,live in rowmap:
 ks[q]=k
 if live: rows_by_q[q].add(phase)
cols_by_q=collections.Counter(q for q,k,j in colmap)
cap_by_k=collections.Counter(); details=[]
for q,rows in rows_by_q.items():
 k=ks[q]; cap=min(len(rows),cols_by_q[q],ranks[k]); cap_by_k[k]+=cap
 details.append([q,k,len(rows),cols_by_q[q],cap])
fullrank=sum(math.comb(13,2*k)*ranks[k] for k in ranks)
cap=sum(cap_by_k.values())
out={'status':'independent exact local rank review; no cone verdict',
 'input_sha256':{str(p.relative_to(AUD)):digest(p) for p in
   [AUD/'templates/templates.json.gz',AUD/'templates/row_map.json.gz',
    AUD/'templates/column_map.json.gz',AUD/'fourier/ranks.json']},
 'literal_row_and_column_mapping_rechecked_against_frozen_original':True,
 'templates':results,'full_C_rank':fullrank,
 'full_C_rows':sum(math.comb(13,2*k)*4**(k-1) for k in ranks),
 'full_C_columns':sum(math.comb(13,2*k)*len(templates[str(k)]) for k in ranks),
 'cheap_live_C_rank_upper_bound':cap,'cheap_live_cap_by_k':dict(sorted(cap_by_k.items())),
 'D_rows':122616,'D_rank_upper_bound':cap,'D_row_dependencies_at_least':122616-cap,
 'D_plus_ten_positivity_rank_upper_bound':cap+10,
 'proof_of_global_bound':'C_full is block diagonal by literal palette membership q. C_live is its row/column restriction. D=L C_live, hence rank(D)<=sum_q min(live rows_q,live columns_q,rank local B_k).',
 'limitations':'This is a rank upper bound for live D, not a selected independent row set. It changes neither nonnegativity nor positivity and supplies no primal/dual point. LU pivots may include slack/artificial columns.',
 'seconds':time.monotonic()-start}
if args.output:
 destination=args.output.resolve()
 if not destination.is_relative_to(HERE): parser.error('--output must stay within algebra/')
 with destination.open('x') as f: f.write(json.dumps(out,indent=2)+'\n')
else:
 expected=json.loads((HERE/'rank_review.json').read_text())
 substantive=lambda x:json.dumps({k:v for k,v in x.items() if k!='seconds'},sort_keys=True)
 assert substantive(out)==substantive(expected), 'read-only replay differs from frozen rank_review.json'
print(json.dumps({'seed':args.seed,'read_only_replay':not bool(args.output),**out},indent=2))
