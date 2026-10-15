#!/usr/bin/env python3
"""An exact finite switch system; NOT a graph/source realizability checker."""
import argparse,hashlib,importlib.util,itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
TRANSFER='audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/check_transfer.py'
COUNTS='audits/2026-10-14-c4-c5-recursion-fdd3e22/fibre/r6_counts/counts.json'
spec=importlib.util.spec_from_file_location('frozen_transfer',HERE/'frozen'/TRANSFER)
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
P=h.PAIRINGS
PERMS=tuple(itertools.permutations(range(4)))
def need(ok,msg):
 if not ok:raise ValueError(msg)
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def norm(parts):return tuple(sorted(tuple(sorted(b)) for b in parts))
def row(s):return tuple('ABCD'.index(c) for c in s)
def rename(r,perm):return tuple(perm[c] for c in r)
def canon(r):
 d={};rr=tuple(d.setdefault(c,len(d)) for c in r)
 for c in range(4):d.setdefault(c,len(d))
 return rr,tuple(d[c] for c in range(4))
def transport(j,parts,perm):
 images=[tuple(sorted(perm[c] for c in pair)) for pair in P[j]]
 jj=P.index(tuple(sorted(images)))
 return jj,tuple(norm(parts[images.index(pair)]) for pair in P[jj])
def canon_option(r,j,parts):
 rr,perm=canon(r);jj,ps=transport(j,parts,perm)
 return rr,jj,ps
def switch(r,j,parts,mask):
 out=list(r);blocks=[(b,pair) for ps,pair in zip(parts,P[j]) for b in ps]
 for i,(block,pair) in enumerate(blocks):
  if mask>>i&1:
   for v in block:out[v]=sum(pair)-out[v]
 return tuple(out)
def cube(r,j,parts):return tuple(switch(r,j,parts,m) for m in range(1<<sum(map(len,parts))))
def direct_allowed(r):
 if any(r[a]==r[b] for a,b in h.EDGES):return False
 z,s,v,w,t,p,q=r
 for rr in set(range(4))-set((s,v,w,t)):
  if z==rr:
   if s!=t or {p,q}!=set(range(4))-{z,s}:return False
  elif s==t:
   if not ({p,q}&(set(range(4))-{z,s,rr})):return False
  elif {p,q}!={s,t}:return False
 return True

def custody():
 manifest=json.loads((HERE/'INPUTS.json').read_text())
 for record in manifest['inputs']:
  name=record['path'];sha=record['sha256']
  need(digest(HERE/'frozen'/name)==sha,'frozen input drift: '+name)
  need(digest(ROOT/name)==sha,'live authority drift: '+name)
 return manifest

def solve_layer(rows):
 """Small exact cover, no numerical solver; all tie-breaks deterministic."""
 choices={}
 for r in sorted(rows):
  for j in range(3):
   choices[r,j]=[tuple(norm(g) for g in ps) for ps,orb in h.options(r,P[j],h.EDGES) if orb<=rows]
 classes=set()
 for (r,j),options in choices.items():
  for ps in options:
   orbit=frozenset(canon_option(rr,j,ps) for rr in cube(r,j,ps))
   variables=[(rr,jj) for rr,jj,pp in orbit]
   if len(set(variables))!=len(variables):continue
   if any(pp not in choices.get((rr,jj),[]) for rr,jj,pp in orbit):continue
   classes.add(orbit)
 classes=sorted(classes,key=lambda c:sorted(c))
 covers=[{(r,j):ps for r,j,ps in c} for c in classes]
 index={v:{i for i,c in enumerate(covers) if v in c} for v in choices}
 def search(todo,live,picked):
  if not todo:return picked
  v=min(todo,key=lambda v:(len(index[v]&live),v))
  for i in sorted(index[v]&live):
   used=set(covers[i]);banned=set().union(*(index[w] for w in used))
   answer=search(todo-used,live-banned,picked+[i])
   if answer is not None:return answer
  return None
 solution=search(set(choices),set(range(len(covers))),[])
 need(solution is not None,'no deterministic layer model')
 chosen={v:ps for i in solution for v,ps in covers[i].items()}
 return {r:tuple(chosen[r,j] for j in range(3)) for r in sorted(rows)}

def build_templates():
 old=json.loads((HERE/'frozen'/COUNTS).read_text())['cases'][2]
 main={row(r) for r,n in zip(old['canonical_rows'],old['row_counts']) if n}
 small=[('ABABCBC','ABACBCB','ABACDCD'),('ABABCCB','ABACBBC','ABACDDC'),
        ('ABCABBC','ABCACBC','ABCADBC'),('ABCABCB','ABCACCB','ABCADCB')]
 return [solve_layer(main)]+[solve_layer({row(r) for r in rs}) for rs in small]

def validate_partition(r,j,parts):
 flat=[v for ps in parts for block in ps for v in block]
 need(sorted(flat)==list(range(7)),'partition must cover all pins exactly once')
 need(all(block and len(set(block))==len(block) for ps in parts for block in ps),'empty/repeated block')
 for ps,pair in zip(parts,P[j]):
  need(all(r[v] in pair for block in ps for v in block),'block mixes colour pairs')
  labels={v:i for i,b in enumerate(ps) for v in b}
  need(all(labels[a]==labels[b] for a,b in h.EDGES if a in labels and b in labels),'mandatory edge split')
 labels={v:i for i,b in enumerate(parts[0]+parts[1]) for v in b}
 need(all(not(labels[a]==labels[c] and labels[b]==labels[d] and labels[a]!=labels[b])
          for a,b,c,d in itertools.combinations(range(5),4)),'outer components cross')

def complete_system(templates):
 states={}
 for layer,template in enumerate(templates):
  for r,allparts in template.items():
   for perm in PERMS:
    rr=rename(r,perm);parts=[None]*3
    for j,ps in enumerate(allparts):
     jj,pp=transport(j,ps,perm);parts[jj]=pp
    key=(layer,rr);need(key not in states,'S4 state orbit not free')
    states[key]=tuple(parts)
 ordered=sorted(states);ids={key:i for i,key in enumerate(ordered)}
 records=[];checks={'same_pairing_cube_targets':0,'cube_composition_laws':0,'S4_partition_transports':0,'S4_switch_transports':0,'whole_pair_global_swaps':0}
 for key in ordered:
  layer,r=key;allparts=states[key]
  need(direct_allowed(r),'state outside all-r upper relation')
  rec={'id':ids[key],'layer':layer,'literal_row':h.name(r),'pairings':[]}
  for j,ps in enumerate(allparts):
   validate_partition(r,j,ps)
   targets=cube(r,j,ps);need(len(targets)==len(set(targets)),'visible cube not free')
   targetids=[]
   for m,rr in enumerate(targets):
    target=(layer,rr);need(target in states,'cube leaves state system')
    need(states[target][j]==ps,'partition changed inside same pairing cube')
    targetids.append(ids[target]);checks['same_pairing_cube_targets']+=1
    for n,ss in enumerate(cube(rr,j,states[target][j])):
     need(ss==targets[m^n],'cube XOR/reversibility/commutation failed')
     checks['cube_composition_laws']+=1
   offset=0
   for ps_one,pair in zip(ps,P[j]):
    mask=((1<<len(ps_one))-1)<<offset;offset+=len(ps_one)
    perm=list(range(4));perm[pair[0]],perm[pair[1]]=pair[1],pair[0]
    need((layer,targets[mask])==(layer,rename(r,perm)),'global swap mismatch')
    checks['whole_pair_global_swaps']+=1
   rec['pairings'].append({'pairing':P[j],'terminal_parts':ps,'cube_targets_by_bitmask':targetids})
  for perm in PERMS:
   renamed=(layer,rename(r,perm));need(renamed in states,'global rename absent')
   for j,ps in enumerate(allparts):
    jj,pp=transport(j,ps,perm)
    need(states[renamed][jj]==pp,'S4 partition covariance failed')
    checks['S4_partition_transports']+=1
    oldblocks=[(b,pair) for groups,pair in zip(ps,P[j]) for b in groups]
    newblocks=[(b,pair) for groups,pair in zip(pp,P[jj]) for b in groups]
    for bit,(block,pair) in enumerate(oldblocks):
     newpair=tuple(sorted(perm[c] for c in pair));newbit=newblocks.index((block,newpair))
     a=rename(switch(r,j,ps,1<<bit),perm)
     b=switch(renamed[1],jj,pp,1<<newbit)
     need((layer,a)==(layer,b),'S4 switch covariance failed')
     checks['S4_switch_transports']+=1
  records.append(rec)
 return states,records,checks

def verify_full_certificate_system(records):
 """Second replay of stored tables, without using solve_layer."""
 byid={r['id']:r for r in records}
 need(set(byid)==set(range(len(records))),'state ids incomplete or duplicated')
 bykey={(r['layer'],r['literal_row']):r['id'] for r in records}
 need(len(bykey)==len(records),'duplicate literal state within layer')
 for rec in records:
  rr=row(rec['literal_row']);need(direct_allowed(rr),'stored forbidden row')
  need(len(rec['pairings'])==3,'missing pairing at state')
  for j,p in enumerate(rec['pairings']):
   need(tuple(map(tuple,p['pairing']))==P[j],'stored pairing order')
   ps=tuple(tuple(tuple(b) for b in g) for g in p['terminal_parts'])
   validate_partition(rr,j,ps);ts=p['cube_targets_by_bitmask']
   need(len(ts)==1<<sum(map(len,ps)),'incomplete stored cube')
   for mask,t in enumerate(ts):
    need(t in byid,'missing cube target');target=byid[t]
    need(target['layer']==rec['layer'],'unexpected layer crossing')
    need(target['literal_row']==h.name(switch(rr,j,ps,mask)),'wrong literal switch target')
    pp=target['pairings'][j]
    need(pp['terminal_parts']==p['terminal_parts'],'stored component changed')
    for other,u in enumerate(pp['cube_targets_by_bitmask']):
     need(u==ts[mask^other],'stored involution/commutation failed')
 return True

def build():
 manifest=custody();assignments=tuple(itertools.product(range(4),repeat=7))
 need(all(direct_allowed(r)==h.allowed(r) for r in assignments),'independent all-r disagreement')
 initial=sorted({h.canonical(r) for r in assignments if direct_allowed(r)})
 live,fp=h.fixed_point(initial,h.EDGES)
 need(len(initial)==26 and len(live)==22,'old fixed-point changed')
 templates=build_templates();states,records,checks=complete_system(templates)
 need(len(states)==720,'unexpected witness size')
 support={h.canonical(r) for layer,r in states};need(support==live,'22-row coverage lost')
 patterns=sorted({h.canonical(r[:5]) for r in assignments if all(r[i]!=r[(i+1)%5] for i in range(5))})
 outer=sorted({h.canonical(r[:5]) for layer,r in states})
 mask=sum(1<<patterns.index(r) for r in outer);need(mask==319,'outer support changed')
 visible_edges=[(a,b) for a,b in itertools.combinations(range(7),2) if all(r[a]!=r[b] for layer,r in states)]
 need(set(visible_edges)=={tuple(sorted(e)) for e in h.EDGES},'maximal visible graph changed')
 extra=next(r for r in assignments if all(r[a]!=r[b] for a,b in visible_edges) and h.canonical(r) not in support)
 payload={'schema':'same-state-kempe-cubes-v1','base':manifest['BASE'],
  'binding':{'inputs_sha256':digest(HERE/'INPUTS.json'),'checker_sha256':digest(Path(__file__))},
  'pins':h.PINS,'initial_26':[h.name(r) for r in initial],'old_fixed_point':fp,
  'canonical_templates':[{'layer':i,'rows':[{'row':h.name(r),'partitions':parts} for r,parts in t.items()]} for i,t in enumerate(templates)],
  'state_count':len(states),'canonical_row_support':[h.name(r) for r in sorted(support)],
  'canonical_row_counts':{h.name(r):sum(rr==r for layer,rr in states) for r in sorted(support)},
  'outer_mask':mask,'states':records,'verified_laws':checks,
  'seven_vertices_only_nonrealizability':{'maximal_possible_edges':visible_edges,'proper_assignment_outside_model_support':h.name(extra)},
  'graph_realizability':'not asserted; no common hidden vertices or original-edge incidence supplied',
  'target_source_status':'not triggered; no source exclusion or realization','general_claim':'OPEN','new_Lean':False}
 verify_full_certificate_system(json.loads(json.dumps(payload))['states'])
 return payload

def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True)
 g.add_argument('--write',action='store_true');g.add_argument('--check',action='store_true')
 ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json');a=ap.parse_args()
 result=build();payload=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
 if a.write:
  with a.certificate.open('x') as f:f.write(payload)
 else:
  supplied=json.loads(a.certificate.read_text());verify_full_certificate_system(supplied['states'])
  need(a.certificate.read_text()==payload,'certificate differs from complete recomputation')
 print(json.dumps({'status':'PASS finite abstract switch system; genuine source not triggered','states':result['state_count'],'canonical_rows':len(result['canonical_row_support']),'outer_mask':result['outer_mask'],'verified_laws':result['verified_laws']},sort_keys=True))
if __name__=='__main__':main()
