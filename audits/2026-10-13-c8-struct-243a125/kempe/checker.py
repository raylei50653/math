#!/usr/bin/env python3
"""Independent, solver-free complete fixed-split cone and rational proof checker."""
import argparse, copy, itertools, json, math
from collections import Counter
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'frozen/audits/2026-10-13-c8-joint-count-3097ef5'
Q=Fraction

def restricted(words):
 out=[]
 for word in words:
  labels={};out.append(tuple(labels.setdefault(c,len(labels)) for c in word))
 return out

def setpart(items):
 if not items:
  yield ();return
 a,*rest=items
 for parts in setpart(rest):
  yield ((a,),)+parts
  for j in range(len(parts)):
   yield parts[:j]+((a,)+parts[j],)+parts[j+1:]

def nc(blocks):
 owner={v:j for j,b in enumerate(blocks) for v in b}
 return not any(owner[a]==owner[c] and owner[b]==owner[d] and owner[a]!=owner[b]
                for a,b,c,d in itertools.combinations(range(8),4))

def enumeration():
 # Enumerate all 6564 literal words, quotient only by fixed-split normalizer.
 group=[g for g in itertools.permutations(range(4)) if {g[0],g[1]} in ({0,1},{2,3})]
 words=[w for w in itertools.product(range(4),repeat=8) if all(w[i]!=w[(i+1)%8] for i in range(8))]
 literal_to_rep={w:min(tuple(g[c] for c in w) for g in group) for w in words}
 rows=sorted(set(literal_to_rep.values()));row_index={w:i for i,w in enumerate(rows)}
 ri={w:row_index[r] for w,r in literal_to_rep.items()};sizes=Counter(ri.values())
 patterns=sorted(set(restricted(words)));pattern_index={p:i for i,p in enumerate(patterns)}
 rp=[pattern_index[p] for p in restricted(rows)]
 parts=[b for b in setpart(list(range(8))) if nc(b)]
 allcols=set();tricol=set()
 for r,w in enumerate(rows):
  wanted=1+sum(w[i]//2!=w[(i+1)%8]//2 for i in range(8))//2
  for blocks in parts:
   if any(any(w[v]//2!=w[b[0]]//2 for v in b) for b in blocks):continue
   owner={v:j for j,b in enumerate(blocks) for v in b}
   if any(w[i]//2==w[(i+1)%8]//2 and owner[i]!=owner[(i+1)%8] for i in range(8)):continue
   # Count orbit words directly; disjoint nonempty blocks imply distinct words.
   orbit=set()
   for subset in itertools.product((False,True),repeat=len(blocks)):
    v=list(w)
    for j,block in enumerate(blocks):
     if subset[j]:
      for pos in block:v[pos]=v[pos]^1
    orbit.add(tuple(v))
   assert len(orbit)==2**len(blocks)
   counts=Counter(ri[v] for v in orbit)
   averaged={i:n*(8//sizes[i]) for i,n in counts.items()}
   divisor=math.gcd(*averaged.values())
   col=tuple(sorted((i,v//divisor) for i,v in averaged.items()))
   allcols.add(col)
   if len(blocks)==wanted:tricol.add(col)
 return rows,sizes,patterns,rp,sorted(allcols),sorted(tricol)

def load_check_cones():
 rows,sizes,patterns,rp,generic,tri=enumeration()
 assert (len(rows),len(patterns),len(generic),len(tri))==(821,274,1552,981)
 for name,expected in [('generic',generic),('triangulated',tri)]:
  data=json.loads((HERE/f'cone.{name}.json').read_text())
  assert data['rows']==list(map(list,rows)) and data['row_to_pattern']==rp
  assert data['row_sizes']==[sizes[i] for i in range(821)]
  assert [[list(t) for t in col] for col in expected]==[c['entries'] for c in data['columns']], 'incomplete or corrupted cone'
  # Independently validate each stored named seed/partition and its full D8 sum.
  group=[g for g in itertools.permutations(range(4)) if {g[0],g[1]} in ({0,1},{2,3})]
  assert data['group']==list(map(list,group))
  repindex={r:i for i,r in enumerate(rows)}
  for rec,expectedcol in zip(data['columns'],expected):
   seed=rows[rec['seed_row']];part=rec['partition'];blocks=[[i for i,b in enumerate(part) if b==j] for j in range(max(part)+1)]
   assert nc(blocks) and all(len({seed[v]//2 for v in b})==1 for b in blocks)
   assert all(seed[i]//2!=seed[(i+1)%8]//2 or part[i]==part[(i+1)%8] for i in range(8))
   if name=='triangulated':assert len(blocks)==1+sum(seed[i]//2!=seed[(i+1)%8]//2 for i in range(8))//2
   direct=Counter()
   for bits in itertools.product((0,1),repeat=len(blocks)):
    w=tuple(c^bits[part[i]] for i,c in enumerate(seed))
    for g in group:
     v=tuple(g[c] for c in w)
     if v in repindex:direct[repindex[v]]+=1
   gcd=math.gcd(*direct.values());assert gcd==rec['gcd']
   assert tuple(sorted((i,v//gcd) for i,v in direct.items()))==expectedcol
 return patterns,rp,generic,tri

def vector(entries,n):
 out=[Q(0)]*n;seen=set()
 for i,value in entries:
  assert type(i) is int and 0<=i<n and i not in seen and Q(value)
  seen.add(i);out[i]=Q(value)
 return out

def orbit_counts(entries,columns):
 out=[Q(0)]*821;ls=vector(entries,len(columns));assert all(v>=0 for v in ls)
 for col,value in zip(columns,ls):
  if value:
   for i,c in col:out[i]+=value*c
 return out

def verify(cert,ctx):
 patterns,rp,generic,tri=ctx
 old=json.loads((OLD/'counts/certificate.v2.json').read_text());interface=json.loads((OLD/'interface.json').read_text())
 assert cert['schema']=='c8-struct-fixed-split-count-v1' and cert['color_frame']==[0,1,2,3]
 assert cert['pattern_order']==old['pattern_order']==list(map(list,patterns))
 qs={(q['case_id'],q['target']):q for q in old['queries'] if q['status']=='necessary_condition_residual'}
 cases={c['id']:c for c in interface['cases']};E=old['equality_rows']
 assert len(cert['queries'])==10 and {(r['case_id'],r['target']) for r in cert['queries']}==set(qs)
 results=[]
 for r in cert['queries']:
  q=qs[r['case_id'],r['target']];case=cases[r['case_id']];upper=q['final_upper_mask']
  assert r['status']=='necessary-condition residual' and r['old_upper']==upper
  assert all(r[k]==case[k] for k in ('boundary_order','supports','extras'))
  allowed=[j for j,col in enumerate(tri) if all(upper>>rp[i]&1 for i,v in col)]
  assert r['allowed_columns']==allowed
  x=list(map(Q,r['counts']));cs=list(map(Q,r['partition_coefficients']))
  assert len(x)==274 and len(cs)==91 and all(v>=0 for v in x)
  assert all(x[i]==sum(Q(a)*v for a,v in zip(row,cs)) for i,row in enumerate(E))
  assert all(x[i]==0 for i in range(274) if not upper>>i&1)
  b=orbit_counts(r['orbit_coefficients'],tri)
  assert all(b[i]==x[p] for i,p in enumerate(rp)), 'incorrect common orbit multiplicity'
  support=sum(1<<i for i,v in enumerate(x) if v)
  assert support==r['support'] and support&~upper==0
  assert all(any(o&~support==0 for o in opts) for i in range(274) if support>>i&1 for opts in interface['kempe_obligations'][i]), 'new support violates Boolean closure'
  outer=[sum(Q(t)*v for t,v in zip(row,x)) for row in case['transfer']]
  assert list(map(str,outer))==r['outer_counts']
  assert all(v>0 if r['target']>>i&1 else v==0 for i,v in enumerate(outer))
  forced=set()
  for f in r['forced_zeros']:
   i=f['pattern'];assert f['word']==list(patterns[i]) and upper>>i&1 and i not in forced
   forced.add(i);z=vector(f['normalizer_dual'],821);a=vector(f['zero_count_dual'],274)
   assert all(not upper>>j&1 for j,v in enumerate(a) if v)
   for j in range(91):
    assert -sum(z[k]*E[p][j] for k,p in enumerate(rp))+sum(a[k]*E[k][j] for k in range(274))==E[i][j], 'invalid forced-zero identity'
   # Check on every GENERIC planar column; theorem does not need triangulation.
   assert all(sum(z[k]*v for k,v in col)>=0 for col in generic if all(upper>>rp[k]&1 for k,v in col)), 'negative orbit coefficient in forced-zero proof'
  assert forced=={i for i in range(274) if upper>>i&1 and not support>>i&1}
  oldx=list(map(Q,q['counts']));ov=r['old_vector']
  if ov['status']=='passes new necessary condition':
   b=orbit_counts(ov['orbit_coefficients'],tri)
   assert all(b[i]==oldx[p] for i,p in enumerate(rp))
  else:
   assert ov['status']=='counterexample to weakened claim'
   z=vector(ov['normalizer_dual'],821)
   assert all(sum(z[i]*v for i,v in col)>=0 for col in generic),'old-vector separator not universally nonnegative'
   dot=sum(z[i]*oldx[p] for i,p in enumerate(rp));assert str(dot)==ov['dot'] and dot<0
  if r['case_id'] not in ('c16','c32'):
   assert all(sum(Q(E[i][j])*x[i] for i in range(274))>0 for j in range(91)), 'cofacial positivity failure'
  results.append({'cofacial_positive_columns':sum(sum(Q(E[i][j])*x[i] for i in range(274))>0 for j in range(91)),'query':f"{r['case_id']}-{r['target']}",'support':support.bit_count(),'forced_zero_patterns':sorted(forced),'old_vector_status':ov['status']})
 return {'status':'PASS','arithmetic':'Fraction only','queries_excluded':0,'queries_residual':10,'generic_columns':1552,'triangulated_columns':981,'normalizer_rows':821,'forced_zero_fibres':4,'results':results}

def controls(cert,ctx):
 changes=[]
 v=copy.deepcopy(cert);v['queries'][0]['orbit_coefficients'][0][1]=str(Q(v['queries'][0]['orbit_coefficients'][0][1])+1);changes.append(('orbit-multiplicity',v))
 v=copy.deepcopy(cert);v['queries'][0]['old_vector']['normalizer_dual']=[ [i,str(-Q(a))] for i,a in v['queries'][0]['old_vector']['normalizer_dual']];changes.append(('old-vector-dual-sign',v))
 v=copy.deepcopy(cert);f=next(r for r in v['queries'] if r['forced_zeros'])['forced_zeros'][0];f['word'][0]=3;changes.append(('named-fibre',v))
 v=copy.deepcopy(cert);f=next(r for r in v['queries'] if r['forced_zeros'])['forced_zeros'][0];f['normalizer_dual'][0][1]=str(Q(f['normalizer_dual'][0][1])+1);changes.append(('forced-zero-identity',v))
 v=copy.deepcopy(cert);v['queries'][0]['boundary_order'].reverse();changes.append(('named-boundary-order',v))
 rejected=[]
 for name,value in changes:
  try:verify(value,ctx)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('negative control accepted: '+name)
 return {'status':'PASS','rejected':rejected}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json');ap.add_argument('--negative-controls',action='store_true');args=ap.parse_args()
 ctx=load_check_cones();cert=json.loads(args.certificate.read_text());print(json.dumps(verify(cert,ctx),sort_keys=True))
 if args.negative_controls:print(json.dumps(controls(cert,ctx),sort_keys=True))
if __name__=='__main__':main()
