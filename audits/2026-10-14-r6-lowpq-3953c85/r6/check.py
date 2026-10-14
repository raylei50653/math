#!/usr/bin/env python3
"""Exhaustive eight-pin cap arithmetic, not a source-realization checker."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PINS = ('z', 's', 'v', 'w', 't', 'q', 'ell', 'm')
OUTER = ('ABABC', 'ABACB', 'ABACD', 'ABCAB', 'ABCAC', 'ABCAD',
         'ABCBC', 'ABCBD', 'ABCDB', 'ABCDC')
FACES = (('z','s'), ('s','v'), ('v','w'), ('w','t'), ('t','z'),
         ('z','q'), ('q','ell'), ('ell','m'), ('m','z'))
CAP = (('r','s'), ('r','v'), ('r','w'), ('r','t'),
       ('p','z'), ('p','q'), ('p','ell'), ('p','m'),
       ('x','z'), ('x','s'), ('x','r'), ('x','y'),
       ('y','z'), ('y','r'), ('y','t'))
INPUTS = (
 'audits/2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md',
 'audits/2026-10-14-c4-mask13-joint6-fdd3e22/JOINT_FIBRES.md',
 'audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/R6_TRANSFER.md',
 'audits/2026-10-14-cofacial-fibres-676b102/r6/PROOF.md',
 'audits/2026-10-14-lowpq-source-676b102/pq/PROOF.md',
 'audits/2026-10-14-lowpq-source-676b102/r6/PROOF.md',
)

def digest(path):
 return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical(xs):
 names = {}
 return ''.join(chr(65+names.setdefault(x,len(names))) for x in xs)

def r_contract(f):
 z,s,r,t,p,q = (f[x] for x in ('z','s','r','t','p','q'))
 row = canonical((z,s,r,t))
 pal = {p,q}
 if row == 'ABAB': return pal == set(range(4)) - {z,s}
 if row == 'ABAC': return False
 if row == 'ABCB': return len(pal)==2 and z not in pal and bool(pal & (set(range(4))-{z,s,r,t}))
 if row == 'ABCD': return pal == {s,t}
 raise AssertionError(row)

def direct_lifts(f):
 result=[]
 for vals in itertools.product(range(4), repeat=4):
  g=dict(f, **dict(zip(('r','p','x','y'),vals)))
  if all(g[a]!=g[b] for a,b in CAP):result.append(list(vals))
 return result

def product_lifts(f):
 ps=[c for c in range(4) if c not in {f[v] for v in ('z','q','ell','m')}]
 rs=[c for c in range(4) if c not in {f[v] for v in ('s','v','w','t')}]
 result=[]
 for r in rs:
  xys=[(x,y) for x,y in itertools.product(range(4), repeat=2)
       if x not in {f['z'],f['s'],r,y} and y not in {f['z'],r,f['t'],x}]
  result.extend([r,p,x,y] for p in ps for x,y in xys)
 return ps,rs,result

def build():
 rows={}; proper=0; total=0
 for vals in itertools.product(range(4), repeat=8):
  f=dict(zip(PINS,vals))
  if any(f[a]==f[b] for a,b in FACES):continue
  proper+=1
  ps,rs,product=product_lifts(f)
  direct=direct_lifts(f)
  assert direct==product, vals
  total+=len(direct)
  word=canonical(vals)
  if tuple(ord(c)-65 for c in word)!=vals:continue
  outer=canonical(vals[:5]); bit=OUTER.index(outer)
  successful=[lift for lift in direct if {lift[1],f['q']} != set(lift[2:])]
  rp_lifts=[[r,p] for r in rs for p in ps]
  bad_rp=[[r,p] for r,p in rp_lifts if not r_contract(dict(f,r=r,p=p))]
  u_ok=not ps or bool(319 & (1<<bit))
  allowed=u_ok and not bad_rp
  assert not allowed or not successful
  rows[word]={'pins':list(vals),'outer_row':outer,'p_lifts':ps,'r_lifts':rs,
   'full_rp_lifts':rp_lifts, 'r_contract_violations_rp':bad_rp,
   'full_rpxy_lifts':direct,'successful_target_lifts_rpxy':successful,
   'u_319_for_every_p_lift':u_ok,'necessary_row':allowed}
 necessary=[w for w,r in rows.items() if r['necessary_row']]
 slices={}
 def slice_rows(equalities):
  return [w for w in necessary if all(rows[w]['pins'][PINS.index(a)]==rows[w]['pins'][PINS.index(b)] for a,b in equalities)]
 specs={'sw_zell':(('s','w'),('z','ell')),'vt_zell':(('v','t'),('z','ell')),
        'sw_qm':(('s','w'),('q','m')),'vt_qm':(('v','t'),('q','m')),
        'zvell':(('z','v'),('z','ell')),'zwell':(('z','w'),('z','ell'))}
 for name,eqs in specs.items():
  selected=slice_rows(eqs)
  equal_pairs=[[a,b] for i,a in enumerate(PINS) for b in PINS[i+1:]
               if selected and all(rows[w]['pins'][PINS.index(a)]==rows[w]['pins'][PINS.index(b)] for w in selected)]
  slices[name]={'equalities':[list(e) for e in eqs], 'necessary_rows':selected,
                'all_rows_force_equal_pairs':equal_pairs}
 assert slices['sw_zell']['necessary_rows']==['ABABCBAD','ABABCCAD']
 assert slices['vt_zell']['necessary_rows']==['ABCACBAD','ABCACCAD']
 assert slices['sw_qm']['necessary_rows']==['ABABCBDB','ABABCCDC']
 assert slices['vt_qm']['necessary_rows']==['ABCACBDB','ABCACCDC']
 assert len(slices['zvell']['necessary_rows'])==16
 assert len(slices['zwell']['necessary_rows'])==16
 for name,pair in [('sw_zell',('ell','v')),('vt_zell',('ell','w'))]:
  assert list(pair) in slices[name]['all_rows_force_equal_pairs'] or list(reversed(pair)) in slices[name]['all_rows_force_equal_pairs']
  for word in slices[name]['necessary_rows']:
   row=rows[word]
   assert len(row['r_lifts'])==len(row['p_lifts'])==1
   assert row['r_lifts']==[row['pins'][-1]]
   assert len(row['full_rpxy_lifts'])==1
 fibres={outer:{'all_necessary_W_rows':[w for w in necessary if rows[w]['outer_row']==outer],
                'p_liftable_necessary_W_rows':[w for w in necessary if rows[w]['outer_row']==outer and rows[w]['p_lifts']],
                'in_U_support_319':bool(319 & (1<<i))} for i,outer in enumerate(OUTER)}
 assert all(bool(x['p_liftable_necessary_W_rows'])==x['in_U_support_319'] for x in fibres.values())
 return {'schema':'r6-lowp-common-W-full-lifts-v1',
  'base':'3953c85e334b96533e44652df065640f5463715a',
  'binding':{'checker_sha256':digest(Path(__file__).resolve()),
             'inputs':{p:digest(ROOT/p) for p in INPUTS}},
  'pins':list(PINS),'face_edges':[list(e) for e in FACES],'cap_edges':[list(e) for e in CAP],
  'summary':{'labelled_assignments':4**8,'proper_labelled_rows':proper,
             'canonical_rows':len(rows),'all_labelled_full_cap_lifts':total,
             'necessary_rows':len(necessary),
             'necessary_rows_without_p_lift':sum(not rows[w]['p_lifts'] for w in necessary),
             'necessary_rows_without_r_lift':sum(not rows[w]['r_lifts'] for w in necessary),
             'genuine_target_sources':0},
  'rows':rows,'all_outer_fibres':fibres,'quotient_slices':slices}

def main():
 ap=argparse.ArgumentParser(); modes=ap.add_mutually_exclusive_group(required=True)
 modes.add_argument('--write',action='store_true');modes.add_argument('--check',action='store_true')
 ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json');args=ap.parse_args()
 result=build()
 if args.write:
  with args.certificate.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
  print('GENERATED exclusive certificate:',args.certificate)
 else:
  expected=json.loads(args.certificate.read_text())
  if expected!=result:raise SystemExit('REJECT: certificate differs from complete recomputation')
  print('PASS: all eight-pin assignments, every full cap lift, and all ten outer fibres match')
 print(json.dumps(result['summary'],sort_keys=True))
if __name__=='__main__':main()
