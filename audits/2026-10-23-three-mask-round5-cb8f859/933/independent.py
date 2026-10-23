#!/usr/bin/env python3
"""Independent D-first quotient relation and separate-palette orbit reconstruction."""
import argparse,hashlib,itertools,json
from pathlib import Path
P=Path(__file__).resolve().parent
SRC='audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json'
CAT='audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/artifacts/c5_cells/cells.json'
D=('a','n','R','L','q','c','s','v','w','t');E=('a','n','R','L','q','c','x','y');ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
RIGHT=(('x','y','r'),('y','t','r'),('t','w','r'),('w','v','r'),('v','s','r'),('s','x','r'),('x','s','c'),('y','a','t'))
LEFT=(('a','b','p'),('b','q','p'),('p','q','h'),('p','h','n'),('p','n','a'),('h','q','L'),('h','L','R'),('h','R','n'),('b','c','q'))
def edges(faces):return {tuple(sorted((a,b))) for f in faces for a,b in zip(f,f[1:]+f[:1])}
RE=edges(RIGHT)
def norm(t):
 d={};return tuple(d.setdefault(c,len(d)) for c in t)
def rxy(t):
 cs=dict(zip(D,t));out=[]
 if any(t[i]==t[(i+1)%10] for i in range(10)):return out
 for x,y,r in itertools.product(range(4),repeat=3):
  color=dict(cs,x=x,y=y,r=r)
  if all(color[a]!=color[b] for a,b in RE):out.append([r,x,y])
 return sorted(out)
def rgs(n,t=()):
 if len(t)==n:yield t;return
 for c in range(max(t,default=-1)+2):yield from rgs(n,t+(c,))
def possible_parts(t,split):
 classes=[[i for i,c in enumerate(t) if c in pair] for pair in split];partitions=[]
 for p in rgs(len(classes[0])):
  for q in rgs(len(classes[1])):
   raw=[None]*10
   for i,c in zip(classes[0],p):raw[i]=c
   for i,c in zip(classes[1],q):raw[i]=c+max(p,default=-1)+1
   part=norm(raw)
   if any(any(t[i] in pair and t[(i+1)%10] in pair for pair in split) and part[i]!=part[(i+1)%10] for i in range(10)):continue
   if any(part[a]==part[c] and part[b]==part[d] and part[a]!=part[b] for a,b,c,d in itertools.combinations(range(10),4)):continue
   partitions.append(part)
 return sorted(partitions)
def compute():
 c=json.loads((P/'certificate.json').read_text());prior=json.loads((P/'frozen/audits/2026-10-23-three-mask-round4-cb8f859/933/certificate.json').read_text());src=json.loads((P/'frozen'/SRC).read_text());ds=[tuple(d) for d in prior['D_words']];index={d:i for i,d in enumerate(ds)};ei={tuple(t):i for i,t in enumerate(src['tuples'])};live=set(next(r['surviving_ids'] for r in src['results'] if r['source_mask']==933));local={};M=[[0]*2461 for _ in ROWS]
 # Begin with a canonical complete D boundary and restore the entire new outer
 # frame once. C5 uses at least three colours, so its S4 restoration is unique.
 for did,t in enumerate(ds):
  if not t[0]==t[2]==t[5]:continue
  outer=(t[0],t[6],t[7],t[8],t[9]);w=norm(outer);ri=ROWS.index(''.join(map(str,w)));permutation=dict(zip(outer,w))
  for old,new in zip(sorted(set(range(4))-set(permutation)),sorted(set(range(4))-set(permutation.values()))):permutation[old]=new
  literal=tuple(permutation[k] for k in t);A,n,R,L,q,cc,s,v,ww,end=literal;key=(ri,n,L,q)
  assert key not in local
  bph=[]
  if n==q:
   missing=next(iter(set(range(4))-{A,L,q}));bph=[[missing,L,missing]]
  fills=rxy(literal);local[key]=(did,bph,fills);M[ri][did]+=1
 assert len(local)==180 and M==c['complete_Hstar_to_D_count_matrix']
 for r in c['complete_640_new_outer_nLq_fibres']:
  key=(r['outer_row'],)+tuple(r['nLq'])
  if key in local:
   did,bph,fills=local[key];assert did==r['D_id'] and bph==r['all_original_bph_lifts'] and fills==r['all_original_rxy_lifts'];assert [l+rr for l in bph for rr in fills]==r['all_original_six_vertex_lifts_bph_rxy']
  else:assert r['D_id'] is None and not r['all_original_bph_lifts'] and not r['all_original_rxy_lifts']
 catalogue=set(map(int,json.loads((P/'frozen'/CAT).read_text())['cells']));assert sorted(m for m in catalogue if m&~319==0)==[271,314,319]
 from functools import lru_cache
 @lru_cache(None)
 def forbidden(t):return any(ei[norm(t[:6]+(x,y))] not in live for r,x,y in rxy(t))
 assert sum(forbidden(t) for t in ds)==552
 counts=[]
 splits=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))
 for test in c['two_positive_family_stop_tests']:
  t=tuple(test['literal_D']);per=[]
  for si,split in enumerate(splits):
   parts=possible_parts(t,split);assert parts==[tuple(o['partition']) for o in test['all_three_split_tests'][si]['all_complete_options']];good=[];swap={a:b for a,b in split}|{b:a for a,b in split}
   for part in parts:
    outputs=[tuple(swap[k] if bits[part[i]] else k for i,k in enumerate(t)) for bits in itertools.product((0,1),repeat=max(part)+1)]
    if not any(forbidden(word) for word in outputs):good.append(list(part))
   assert good==test['all_three_split_tests'][si]['surviving_necessary_partitions'];per.append([len(parts),len(good)])
  counts.append({'D_id':test['D_id'],'option_and_survivor_counts':per,'forced_zero':any(b==0 for a,b in per)})
 assert sorted(t['D_id'] for t in counts if t['forced_zero'])==[461,470,482,491]
 # Explicit genuine plane graph with one bare original D face. Its 17 original
 # cap triangles and D face have consistent sides and original outer B.
 faces=list(LEFT)+list(RIGHT)+[tuple(D)];inc={}
 for f in faces:
  for a,b in zip(f,f[1:]+f[:1]):inc.setdefault(tuple(sorted((a,b))),[]).append((a,b))
 outer_edges={tuple(sorted(e)) for e in zip(('x','y','a','b','c'),('y','a','b','c','x'))}
 assert {e for e,sides in inc.items() if len(sides)==1}==outer_edges
 assert all(len(sides)==1 if edge in outer_edges else len(sides)==2 and sides[0]==tuple(reversed(sides[1])) for edge,sides in inc.items())
 vertices=list(D)+['b','p','h','r','x','y'];assert len(vertices)-len(inc)+len(faces)==1
 quotient=lambda v:'A' if v in ('a','R','c') else v
 qedges={tuple(sorted((quotient(a),quotient(b)))) for a,b in zip(D,D[1:]+D[:1])};assert all(a!=b for a,b in qedges)
 qvertices=['A','n','L','q','s','v','w','t'];control=[]
 for ri,word in enumerate(ROWS):
  fixed=dict(zip(('A','s','v','w','t'),map(int,word)));fibres=[]
  for n,L,q in itertools.product(range(4),repeat=3):
   colors=dict(fixed,n=n,L=L,q=q)
   if all(colors[a]!=colors[b] for a,b in qedges):fibres.append([colors[v] for v in qvertices])
  assert len(fibres)==18;control.append({'outer_row':word,'all_complete_Hstar_control_fibres':fibres})
 # The r rotation finite witness is checked from its cyclic positions, using
 # the outer x/y ray to choose the bounded side.
 rotation=('x','y','t','w','v','s');sectors=[]
 for anchor,port,other in [('a','y','x'),('c','x','y')]:
  for end in ('v','w'):
   a,b=rotation.index(port),rotation.index(end);forward=rotation[a+1:b] if a<b else rotation[a+1:]+rotation[:b];backward=[v for v in rotation if v not in set(forward)|{port,end}];inside=forward if other not in forward else backward
   stored=next(z for z in c['four_original_short_path_obstructions'] if z['anchor']==anchor and z['zero_vertex']==end);assert set(inside)==set(stored['forced_strict_cap_vertices']);sectors.append({'anchor':anchor,'zero_vertex':end,'forced_inside':sorted(inside)})
 return {'status':'PASS','D_first_proper_records':180,'all_640_fibres_match':True,'all_complete_ten_row_matrix_entries_match':True,'full_support_catalogue_alternatives':[271,314,319],'bounded_positive_family_tests':counts,'four_bounded_sectors':sectors,'actual_plane_control':{'vertices':vertices,'oriented_bounded_faces':[list(f) for f in faces],'outer':['x','y','a','b','c'],'V':len(vertices),'E':len(inc),'bounded_faces':len(faces),'quotient_vertices':qvertices,'quotient_edges':[list(e) for e in sorted(qedges)],'complete_new_outer_fibres':control,'whole_control_support':1023,'relation_control':'triggered and holds','full_original_r6_933_minimum_source':'not triggered'},'source_realization_claimed':False,'certificate_sha256':hashlib.sha256((P/'certificate.json').read_bytes()).hexdigest()}
def main():
 p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');a=p.parse_args();expected=compute();path=P/'independent-certificate.json'
 if a.build:
  with path.open('x') as f:json.dump(expected,f,indent=2);f.write('\n')
 assert json.loads(path.read_text())==expected
 print(json.dumps({k:v for k,v in expected.items() if k not in ('actual_plane_control','bounded_positive_family_tests')},sort_keys=True))
if __name__=='__main__':main()
