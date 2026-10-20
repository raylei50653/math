#!/usr/bin/env python3
"""All named d_a cap lifts for the two conditional injections."""
from pathlib import Path
import json,argparse
D=Path(__file__).resolve().parent

def check():
 out=[]
 for branch,R,L in ((1,3,1),(2,2,3)):
  for v,w in ((2,3),(3,2)):
   for x,y in ((2,3),(3,2)):
    z=dict(a=0,c=0,r=0,h=0,b=1,n=1,s=1,t=1,q=2,p=3,R=R,L=L,v=v,w=w,x=x,y=y)
    core=[z[k] for k in ('a','n','R','L','q','c','s','v','w','t')]
    assert all(core[i]!=core[(i+1)%10] for i in range(10))
    for u,vs in {'b':('a','c','p','q'),'p':('a','b','q','h','n'),'h':('p','q','L','R','n'),'r':('x','y','t','w','v','s'),'x':('y','c','r','s'),'y':('x','a','r','t')}.items():
     assert all(z[u]!=z[v] for v in vs)
    assert (z['b']==z['L'] and z['a']!=z['R']) if branch==1 else (z['a']!=z['L'] and z['a']!=z['R'] and z['b']!=z['L'])
    perm={x:0,y:1,0:2,1:3}
    normalized={k:perm[c] for k,c in z.items()}
    assert ''.join(str(normalized[k]) for k in ('x','y','a','b','c'))=='01232'
    out.append({'zero_acceptance_candidate':'Q'+str(branch),'target':'J'+str(branch),'original_named_colours':z,'global_permutation':[perm[i] for i in range(4)],'normalized_named_colours':normalized})
 for branch in (1,2):
  for v,w in ((2,3),(3,2)):
   rows=[r for r in out if r['target']=='J'+str(branch) and r['original_named_colours']['v']==v]
   assert {r['normalized_named_colours']['q'] for r in rows}=={0,1}
 return {'source_realized':False,'scope':'Interface check of universal d_a injection; an actual complete d_a fibre is supplied by the frozen theorem.','records':out,'injection_bound':'N_alpha(Ji)>=2*d_a>0 in branch ai=0; all private colours retained.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');args=ap.parse_args();d=check();p=D/'acceptance.json'
 if args.build:
  with p.open('x') as f:json.dump(d,f,separators=(',',':'));f.write('\n')
 else:assert json.loads(p.read_text())==d
 print(json.dumps({'ok':True,'named_lifts':len(d['records'])}))
if __name__=='__main__':main()
