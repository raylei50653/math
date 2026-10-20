"""Exact read-only common C10 count controls; no scipy or graph realization."""
import argparse,copy,hashlib,importlib.util,itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
FROZEN=HERE.parent/'frozen'
MODEL='audits/2026-10-19-r6-941-leakage-b89c591/A/model.py'
PATCH='audits/2026-10-19-r6-941-existence-f13eb4d/C/certificate.json'
CAT='audits/2026-10-19-r6-941-existence-f13eb4d/frozen/artifacts/c5_cells/cells.json'
PINS=['a','n','R','L','q','c','s','v','w','t']

def load_model():
 s=importlib.util.spec_from_file_location('frozen_count_model',FROZEN/MODEL)
 m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def prepare():
 m=load_model();eight,ten,index,T,hrows,hi,hist,parts,M,U=m.build()
 i8={t:i for i,t in enumerate(eight)}
 M['J1']=[[0]*274 for _ in range(10)];M['J2']=[[0]*274 for _ in range(10)]
 c=json.loads((FROZEN/PATCH).read_text());states=[tuple(t) for t in c['rim_states']]
 assert states==[t for t in m.growth(6,four=True) if m.proper(t)]
 signature_by_id={}
 # Rebuild ALL old complete patch relations, including empty fibres and centre lifts.
 for op in c['candidates']:
  internal=op['internal'];edges=op['edges'];eq=op['equality_mask'];parent=list(range(6+internal))
  def root(i):
   while parent[i]!=i:i=parent[i]
   return i
  for j,(a,b) in enumerate(edges):
   if eq>>j&1:parent[root(a)]=root(b)
  assert all(root(a)!=root(b) for a,b in [(i,(i+1)%6) for i in range(6)]+[e for j,e in enumerate(edges) if not eq>>j&1])
  assert -2+internal-(6+internal-len({root(i) for i in range(6+internal)}))==op['completed_k_delta']<0
  lifts=[]
  for t in states:
   z=[]
   for v in range(4) if internal else (None,):
    colors=t+(v,) if internal else t
    if all((colors[a]==colors[b])==bool(eq>>j&1) for j,(a,b) in enumerate(edges)):z.append(v)
   lifts.append(z)
  assert lifts==op['lifts']
  sig=tuple(map(len,lifts));sid=op['signature_id']
  assert sid not in signature_by_id or signature_by_id[sid]==sig
  signature_by_id[sid]=sig
 assert len(c['candidates'])==1552 and len(signature_by_id)==90
 i6={t:i for i,t in enumerate(states)}
 for sid in signature_by_id:M['P'+str(sid)]=[[0]*274 for _ in range(10)]
 for j,word in enumerate(m.ROWS):
  x,y,a,b,c0=map(int,word)
  for n,R,L,q in itertools.product(range(4),repeat=4):
   exterior=(a,n,R,L,q,c0,x,y)
   if not m.proper(exterior) or b in (a,c0,q):continue
   ei=i8[m.canonical(exterior)];ri=i6[m.canonical((a,b,q,L,R,n))]
   M['J1'][j][ei]+=int(b==L and a!=R)
   M['J2'][j][ei]+=int(a!=L and a!=R and b!=L)
   for sid,sig in signature_by_id.items():M['P'+str(sid)][j][ei]+=sig[ri]
 span=[]
 for p in parts:
  pairs=[(i,next(j for j in range(i) if p[j]==p[i])) for i in range(10) if p[i] in p[:i]]
  span.append([i for i,t in enumerate(ten) if all(t[a]==t[b] for a,b in pairs)])
 return m,ten,index,T,hrows,hi,hist,span,M,U

def validate(cert,data):
 m,ten,index,T,hrows,hi,hist,span,M,U=data
 assert cert['status']=='necessary common count controls; source not realized'
 assert cert['source_realized'] is False and cert['smaller_bad_constructed'] is False and cert['main_target']=='OPEN'
 assert cert['pins']==PINS and cert['rows']==list(m.ROWS)
 assert cert['input_sha256']=={p:hashlib.sha256((FROZEN/p).read_bytes()).hexdigest() for p in (MODEL,PATCH,CAT)}
 cat=set(map(int,json.loads((FROZEN/CAT).read_text())['cells']))
 assert [r['branch'] for r in cert['records']]==['a1','a2']
 summaries=[]
 for rec in cert['records']:
  assert rec['source_realized'] is False
  z=rec['core_counts'];assert len(z)==2461 and all(type(v) is int and v>=0 for v in z),'nonnegative full core counts'
  rebuilt=[0]*2461;seen=set()
  for j,v in rec['planar_coefficients']:
   assert type(j) is int and 0<=j<603 and j not in seen and type(v) is int and v;seen.add(j)
   for i in span[j]:rebuilt[i]+=v
  assert rebuilt==z,'full signed planar span'
  residual=[-hist[t]*z[index[m.canonical(t)]] for t in hrows];seen=set()
  for orbit in rec['orbits']:
   key=tuple(orbit['start']),tuple(orbit['partition']);weight=orbit['weight']
   assert key not in seen and type(weight) is int and weight>0;seen.add(key)
   for r,v in m.orbit_column(*key,hi).items():residual[r]+=weight*v
  assert not any(residual),'complete counted component orbits'
  exterior=[sum(z[i]*v for i,v in col) for col in T]
  counts={g:m.mv(mat,exterior) for g,mat in M.items()}
  assert counts==rec['graph_counts'],'same-core complete cap projection'
  masks={g:m.mask(v) for g,v in counts.items()}
  assert masks==rec['masks'] and masks['G']==941
  assert all(mask in cat for g,mask in masks.items() if g!='G'),'all 90 patch signatures and five named candidates in K132'
  u=m.mv(U,z);assert m.mask(u)==319,'complete U319'
  positive={name:sum(z[i] for i in ids) for name,ids in m.source_positive_subsets(index).items()}
  assert all(positive.values()),'both original specified fibres positive'
  q,j=('Q1','J1') if rec['branch']=='a1' else ('Q2','J2')
  assert counts[q][9]==0 and counts[j][9]>0 and counts[j][1]>0 and counts[j][4]==counts[j][6]==0
  summaries.append({'branch':rec['branch'],'Q_masks':[masks['Q1'],masks['Q2']],'J_masks':[masks['J1'],masks['J2']],
   'target_counts':counts[j],'target_T':counts[j][1],'target_alpha':counts[j][9],
   'U_counts':u,'specified_positive_fibres':positive,'positive_core_fibres':sum(v>0 for v in z),
   'complete_counted_orbits':len(rec['orbits']),'signed_planar_columns':len(rec['planar_coefficients']),
   'patch_masks':sorted({masks['P'+str(i)] for i in range(90)}),'all_1552_patches_in_K132':True,'source_realized':False})
 return summaries

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json');ap.add_argument('--negative-controls',action='store_true');args=ap.parse_args()
 data=prepare();cert=json.loads(args.certificate.read_text());summaries=validate(cert,data);negative=[]
 if args.negative_controls:
  tests=[('source-realization',lambda c:c.__setitem__('source_realized',True)),
   ('literal-frame',lambda c:c['pins'].reverse()),
   ('cross-source-splice',lambda c:c['records'][0].__setitem__('core_counts',c['records'][1]['core_counts'])),
   ('drop-signed-column',lambda c:c['records'][0]['planar_coefficients'].pop()),
   ('orbit-multiplicity',lambda c:c['records'][0]['orbits'][0].__setitem__('weight',c['records'][0]['orbits'][0]['weight']+1)),
   ('declare-last-rejection-zero',lambda c:c['records'][0]['graph_counts']['J1'].__setitem__(1,0)),
   ('omit-one-patch',lambda c:c['records'][0]['graph_counts'].pop('P89'))]
  for name,mutate in tests:
   bad=copy.deepcopy(cert);mutate(bad)
   try:validate(bad,data)
   except AssertionError:negative.append(name)
   else:raise AssertionError('negative control accepted: '+name)
 print(json.dumps({'pass':True,'records':summaries,'negative_controls_rejected':negative,'main_target':'OPEN'},sort_keys=True))
if __name__=='__main__':main()
