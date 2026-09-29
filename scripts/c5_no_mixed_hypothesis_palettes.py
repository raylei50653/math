#!/usr/bin/env python3
"""Read-only support-level audit; never source/disk realizability evidence."""
import sys,json,argparse
from hashlib import sha256
from pathlib import Path
from itertools import combinations,product,permutations
from collections import Counter
sys.path.insert(0, str(Path(__file__).resolve().parent))
from c5_no_mixed_span_budget import FAMILIES,original_record,context
from c5_adjacent_degree5_no_mixed_t2_t1_bridge import frame_evidence,root_pairs,external_routes
from c5_single_spoke_first_bridge import fixed_colors
from c5_single_spoke_frame_arc import admissible_supports
from c5_no_spoke_first_bridge import FRAME_PARTITIONS
from c5_adjacent_degree5_no_mixed_t2_path_palettes import gallai_control
ROOT = Path(__file__).resolve().parents[1]
Q=(0,1,0,1,2);U=set(range(4)); PERMS=list(permutations(range(4)))
counts=Counter(); examples={}; records=[]; hashes={}
parser=argparse.ArgumentParser()
parser.add_argument("--out",type=Path,default=ROOT / 'artifacts/c5_no_mixed_hypothesis_audit/palettes.json')
parser.add_argument("--check",action="store_true")
args=parser.parse_args()
def frame_certificate(ctx,k,family):
 evidence=frame_evidence(ctx,k,family)
 witnesses=evidence['witnesses']
 # One complete original-route witness proves the same universal family
 # exclusion. Bind the remaining alternatives without duplicating them.
 return evidence | {
  'witnesses':witnesses[:1],
  'all_witnesses_count':len(witnesses),
  'all_witnesses_sha256':sha256(json.dumps(witnesses,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
 }
for cell in ('AA','AB','AC','AE','BB','BC','BE'):
 path=ROOT/f'artifacts/c5_adjacent_degree5_no_mixed_{FAMILIES[cell]}/observations.json'
 raw=path.read_bytes();hashes[str(path.relative_to(ROOT))]=sha256(raw).hexdigest()
 bundle=json.loads(raw)
 sources=bundle.get('original_records',bundle.get('original_frontier'))
 for final in bundle['records']:
  rec=original_record(final)
  if rec.get('status') in ('excluded','source_excluded'):continue
  ctx=context(rec,sources[rec['source_id']])
  final_targets=final.get('final_targets',final.get('targets'))
  assert len(final_targets)==2 and all(t['status']=='accept' for t in final_targets)
  for ti,target in enumerate(rec['targets']):
   row=tuple(target['row']); counts['target_queries']+=1
   assert row==((0,1,0,2,1),(0,1,2,1,2))[ti]==tuple(final_targets[ti]['row'])
   joins=target.get('joins',[target] if 'forbidden_sets' in target else [])
   for k,c in enumerate(ctx['components']):
    if len(c['contacts'])!=2 or len(c['source_forbidden'])!=1:continue
    d=c['source_forbidden'][0]; K=fixed_colors(Q,row,c['support'])
    if d not in K:continue
    pairs={tuple(j['forbidden_sets'][k]) for j in joins if len(j['forbidden_sets'][k])==2}
    # Independently reconstruct the entire size-two upper domain, rather
    # than trusting that the saved joins happened to include every pair.
    transports=[pi for pi in PERMS if all(pi[Q[h]]==row[h] for h in c['support'])]
    stabilizer=[pi for pi in PERMS if all(pi[row[h]]==row[h] for h in c['support'])]
    expected_pairs=set() if transports else {
     pair for pair in combinations(range(4),2)
     if all({pi[x] for x in pair}==set(pair) for pi in stabilizer)
    }
    assert pairs==expected_pairs, (cell,rec['id'],row,k,pairs,expected_pairs)
    for D in sorted(pairs):
     counts['conserved_pair_component_cases']+=1
     containing=[j for j in joins if tuple(j['forbidden_sets'][k])==D]
     accept=any(root_pairs(ctx,row,j['forbidden_sets']) for j in containing)
     fail=any(not root_pairs(ctx,row,j['forbidden_sets']) for j in containing)
     if d not in D:
      counts['conserved_d_absent_target_pair']+=1
      records.append(dict(family=cell,id=rec['id'],source_id=rec['source_id'],ctx=ctx,row=row,component=k,d=d,D=D,K=sorted(K),accepted_join_present=accept,failing_join_present=fail,reason='conserved_d_absent_target_pair',eliminated=True))
      continue
     families={}; refined={}; old_surv=[]; new_surv=[];old_evidence={};new_evidence={}
     for beta in sorted(U-{d}):
      R={d,beta}
      if R&K!=set(D)&K:continue
      fam=[T for T in admissible_supports(Q,tuple(c['support']),tuple(sorted(R))) if T in admissible_supports(row,tuple(c['support']),D)]
      fam2=[T for T in fam if all({p[x] for x in R}==set(D) for p in PERMS if all(p[Q[h]]==row[h] for h in T))]
      families[beta]=fam;refined[beta]=fam2
      old_evidence[beta]=frame_certificate(ctx,k,fam);new_evidence[beta]=frame_certificate(ctx,k,fam2)
      if not old_evidence[beta]['eliminated']:old_surv.append(beta)
      if not new_evidence[beta]['eliminated']:new_surv.append(beta)
     switches=[]
     for a,b in combinations(new_surv,2):
      uncovered=[]
      for Ta,Tb in product(refined[a],refined[b]):
       ev=frame_evidence(ctx,k,[Ta,Tb])
       if not ev['eliminated']:uncovered.append([sorted(Ta),sorted(Tb)])
      switches.append(dict(betas=[a,b],all_support_pairs_have_frame_K5=not uncovered,uncovered=uncovered))
     e=dict(old_frame_evidence=old_evidence,refined_frame_evidence=new_evidence,reason="all_odd_betas_excluded" if not old_surv else "unique_beta_forces_second_source_ban",eliminated=len(old_surv)<=1,family=cell,id=rec['id'],source_id=rec['source_id'],ctx=ctx,row=row,component=k,d=d,D=D,K=sorted(K),accepted_join_present=accept,failing_join_present=fail,old_survivors=old_surv,refined_survivors=new_surv,families={b:list(map(sorted,f)) for b,f in families.items()},refined={b:list(map(sorted,f)) for b,f in refined.items()},switches=switches)
     counts[f'{cell}_pair_cases']+=1
     counts[f'old_survivors_{len(old_surv)}']+=1;counts[f'refined_survivors_{len(new_surv)}']+=1
     if accept:counts['accepted_pair_cases']+=1
     if fail:counts['failing_pair_cases']+=1
     if len(new_surv)>1:
      counts['multi_beta_accepted' if accept else 'multi_beta_no_accepted']+=1
      examples.setdefault('multi_beta_accepted' if accept else 'multi_beta_no_accepted',e)
     if len(old_surv)>len(new_surv):examples.setdefault('locality_strengthens',e)
     for s in switches:
      counts['switch_candidates']+=1
      counts['switch_K5' if s['all_support_pairs_have_frame_K5'] else 'switch_unresolved']+=1
     records.append(e)
negative=gallai_control(3,(2,3,1),'nested')
# Independent full endpoint relation control for the bare path.
bare=gallai_control(3,(2,3,1),'bare')
assert len(records)==1780 and counts['target_queries']==4164
assert counts['conserved_d_absent_target_pair']==890
assert counts['old_survivors_0']==850 and counts['old_survivors_1']==40
assert counts['refined_survivors_0']==886 and counts['refined_survivors_1']==4
assert all(r['eliminated'] for r in records)
for module in list(sys.modules.values()):
 path=Path(getattr(module,'__file__','') or '/nonexistent')
 if path.is_file() and path.is_relative_to(ROOT/'scripts'):
  hashes[str(path.relative_to(ROOT))]=sha256(path.read_bytes()).hexdigest()
out=dict(input_sha256=hashes,scope='necessary support families only; complete original contexts preserved; no disk realization conclusion',counts=dict(counts),examples=examples,records=records,abstract_variable_controls=[negative,bare])
encoded=json.dumps(out,indent=2,sort_keys=True)+'\n'
if args.check:
 assert args.out.read_text()==encoded, 'artifact differs from recomputation'
else:
 args.out.write_text(encoded)
print(json.dumps(dict(verified=args.check,output=str(args.out),counts=counts),sort_keys=True))
