#!/usr/bin/env python3
"""Independent direct-edge C11 cap audit; imports no upstream implementation."""
from pathlib import Path
from itertools import product
import argparse,gzip,hashlib,json
D=Path(__file__).resolve().parent
RIM=('a','n','u2','u1','L','q','c','s','v','w','t')
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
LEFT=(('b','a'),('b','c'),('b','q'),('b','p'),('p','a'),('p','q'),('p','h'),('p','n'),('h','q'),('h','L'),('h','R'),('h','n'),('R','n'),('R','u2'),('R','u1'),('R','L'))
RIGHT=(('x','y'),('x','c'),('x','r'),('x','s'),('y','a'),('y','r'),('y','t'),('r','t'),('r','w'),('r','v'),('r','s'))
QL=tuple(e for e in LEFT if not {'p','h'}&set(e))
def canonical(t):
 d={};return tuple(d.setdefault(c,len(d)) for c in t)
def states():
 def grow(t):
  if len(t)==11:
   if t[-1]!=t[0]:yield t
   return
  for c in range(min(3,max(t)+1)+1):
   if c!=t[-1]:yield from grow(t+(c,))
 return list(grow((0,)))
def compute(sourcepath):
 with gzip.open(sourcepath,'rt') as f:source=json.load(f)
 sr=states();assert len(sr)==7381
 assert tuple(source['ordered_rim'])==RIM
 assert [tuple(c['core']) for c in source['caps']]==sr
 mats={g:[[0]*len(sr) for _ in ROWS] for g in ('G','Q1','J1')}
 empties={g:0 for g in ('G','Q1','J1','right')}
 for i,t in enumerate(sr):
  base=dict(zip(RIM,t));lifts={}
  for g,vs,es in (('G',('b','p','h','R'),LEFT),('Q1',('b','R'),QL),('J1',('b','R'),QL+(('a','R'),))):
   li=[]
   for v in product(range(4),repeat=len(vs)):
    c=base|dict(zip(vs,v))
    if g=='Q1' and (c['b']!=c['n'] or c['R']!=c['q']):continue
    if g=='J1' and c['b']!=c['L']:continue
    if all(c[u]!=c[v] for u,v in es):li.append(v)
   lifts[g]=li
   empties[g]+=not bool(li)
  right=[]
  for v in product(range(4),repeat=3):
   c=base|dict(zip(('x','y','r'),v))
   if all(c[u]!=c[v] for u,v in RIGHT):right.append(v)
  empties['right']+=not bool(right)
  expected={'original_left_bphR':lifts['G'],'Q1_left_bR':lifts['Q1'],'J1_left_bR':lifts['J1'],'right_xyr':right}
  assert all(tuple(map(tuple,source['caps'][i][k]))==tuple(v) for k,v in expected.items())
  for g,li in lifts.items():
   for v in li:
    for x,y,r in right:
     row=''.join(map(str,canonical((x,y,base['a'],v[0],base['c']))))
     mats[g][ROWS.index(row)][i]+=1
 packed=json.dumps(mats,sort_keys=True,separators=(',',':')).encode()
 assert hashlib.sha256(packed).hexdigest()==source['matrices_sha256']
 zero={i for i in range(len(sr)) if any(mats['G'][j][i] for j in (1,4,6)) or mats['Q1'][9][i] or any(mats['J1'][j][i] for j in (4,6))}
 assert zero==set(source['cap_zero'])
 assert zero<=set(source['initial_zero'])
 assert all(w['survives'] and w['canonical_id'] in source['live'] for w in source['witnesses'])
 profiles=[]
 for chord in (('s','u2'),('v','u2'),('v','u1'),('w','u1')):
  prof=next(p for p in source['conditional_chord_profiles'] if p['present_chords']==[list(chord)])
  live=set(prof['live_ids']);a,b=map(RIM.index,chord)
  assert all(sr[i][a]!=sr[i][b] and i not in source['initial_zero'] for i in live)
  positive=[any(mats['G'][j][i] for i in live) for j in (0,2,3,5,7,8,9)]
  assert positive==prof['original_positive_rows_survive']
  assert positive==[True]*6+[False]
  assert prof['witnesses_survive']==[False,False]
  profiles.append({'present_chord':chord,'live_states':len(live),'original_01232_has_live_coefficient':False,'original_positive_rows_survive':positive})
 return {'status':'PASS','method':'all complete assignments tested directly against named edge lists; no imported checker code','states':len(sr),'left_edges':[list(e) for e in LEFT],'right_edges':[list(e) for e in RIGHT],'empty_cap_rows':empties,'matrices_sha256':hashlib.sha256(packed).hexdigest(),'direct_cap_zero_states':len(zero),'parent_initial_zero_states':len(source['initial_zero']),'witnesses':source['witnesses'],'four_chord_profiles':profiles,'input_interface_sha256':hashlib.sha256(sourcepath.read_bytes()).hexdigest(),'closure_replayed_independently':False,'source_excluded':False,'smaller_bad_constructed':False}
def main():
 p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');p.add_argument('--source',type=Path,default=D.parent/'interface/certificate-v4.json.gz');p.add_argument('--certificate',type=Path,default=D/'interface-check-v2.json');a=p.parse_args();out=json.loads(json.dumps(compute(a.source)))
 if a.build:
  with a.certificate.open('x') as f:json.dump(out,f,sort_keys=True,indent=2);f.write('\n')
 else:assert json.loads(a.certificate.read_text())==out
 print(json.dumps({k:v for k,v in out.items() if k not in ('left_edges','right_edges','witnesses')},sort_keys=True))
if __name__=='__main__':main()
