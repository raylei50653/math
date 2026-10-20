"""One-time exact extraction from private LP discovery; outputs use exclusive create."""
import hashlib,itertools,json,pickle
from pathlib import Path
import model
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
with (D/'counted10-discovery.pickle').open('rb') as f:ten,rows,hist,columns,descriptions,T,A=pickle.load(f)
with (D/'combined-matrix.pickle').open('rb') as f:AA,B,bounds=pickle.load(f)
_,ten2,_,transfer,hrows,hi,hhist,parts,M,MU=model.build()
assert ten==ten2 and rows==hrows
vecs={}
for name in ('Q1','Q2','GB','tau'):
 with (D/('exact-'+name+'.pickle')).open('rb') as f:vecs[name]=pickle.load(f)
vecs['allK']=[a+b+c for a,b,c in zip(vecs['Q1'],vecs['GB'],vecs['tau'])]
records=[];n=len(ten);k=len(columns)
for name in ('Q1','Q2','GB','allK'):
 vec=vecs[name];z=vec[:n];counts=model.mv(T.toarray().tolist(),z)
 orbits=[]
 for j,value in enumerate(vec[n:n+k]):
  if value:
   start,p=descriptions[columns[j]]
   orbits.append({'start':list(start),'partition':list(p),'weight':value})
 coeff=[[j,value] for j,value in enumerate(vec[n+k:]) if value]
 graph_counts={name:model.mv(matrix,counts) for name,matrix in M.items()}
 ucounts=model.mv(MU,z)
 print(name,'source',model.mask(graph_counts['G']),'candidates',{x:model.mask(v) for x,v in graph_counts.items()},'U',model.mask(ucounts),'max',max(map(abs,vec)),flush=True)
 records.append({'name':name,'core_counts':z,'orbits':orbits,'planar_coefficients':coeff,'exterior_counts':counts,'graph_counts':graph_counts,'U_counts':ucounts})
inputs=json.loads((D.parent/'INPUTS.json').read_text())
cert={'base':inputs['base'],'scope':'necessary joint C10 counted and planar-span controls, not graph realizations',
      'source_realized':False,'smaller_bad_source_constructed':False,'pin_order':['a','n','R','L','q','c','s','v','w','t'],
      'rows':list(model.ROWS),'records':records,
      'input_sha256':{'../INPUTS.json':hashlib.sha256((D.parent/'INPUTS.json').read_bytes()).hexdigest()}}
with (D/'certificate.json').open('x') as f:json.dump(cert,f,indent=2);f.write('\n')
