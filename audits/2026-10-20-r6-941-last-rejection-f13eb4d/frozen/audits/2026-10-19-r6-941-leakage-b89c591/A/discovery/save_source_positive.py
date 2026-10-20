"""Exclusive exact source-positive controls, extracted after all integer checks."""
exec((__import__('pathlib').Path(__file__).resolve().parent/'save_certificate.py').read_text().split('records=[]')[0])
with (D/'exact-sector-Q2.pickle').open('rb') as f:vecs['Q2_source_positive']=pickle.load(f)
vecs['allK_source_positive']=vecs['allK']
idsA=[1561,1568,1743,1750,2290,2297];idsB=[507,514,871,878]
records=[];n=len(ten);k=len(columns)
for name in ('Q2_source_positive','allK_source_positive'):
 vec=vecs[name];z=vec[:n];counts=model.mv(T.toarray().tolist(),z);orbits=[]
 for j,value in enumerate(vec[n:n+k]):
  if value:
   start,p=descriptions[columns[j]];orbits.append({'start':list(start),'partition':list(p),'weight':value})
 coeff=[[j,value] for j,value in enumerate(vec[n+k:]) if value]
 graph_counts={name:model.mv(matrix,counts) for name,matrix in M.items()};ucounts=model.mv(MU,z)
 print(name,'source',model.mask(graph_counts['G']),'candidates',{x:model.mask(v) for x,v in graph_counts.items()},'U',model.mask(ucounts),'A',sum(z[i] for i in idsA),'B',sum(z[i] for i in idsB),flush=True)
 records.append({'name':name,'core_counts':z,'orbits':orbits,'planar_coefficients':coeff,'exterior_counts':counts,'graph_counts':graph_counts,'U_counts':ucounts,'source_positive_subset_counts':{'h_equals_a':sum(z[i] for i in idsA),'h_equals_b':sum(z[i] for i in idsB)}})
inputs=json.loads((D.parent/'INPUTS.json').read_text())
cert={'base':inputs['base'],'scope':'necessary joint C10 counted and planar-span controls including both mandatory D7 source-positive subsets, not graph realizations',
      'source_realized':False,'smaller_bad_source_constructed':False,'pin_order':['a','n','R','L','q','c','s','v','w','t'],
      'rows':list(model.ROWS),'records':records,'require_both_source_subsets':True,
      'source_positive_subset_ids':{'h_equals_a':idsA,'h_equals_b':idsB},
      'input_sha256':{'../INPUTS.json':hashlib.sha256((D.parent/'INPUTS.json').read_bytes()).hexdigest()}}
with (D/'source-positive-certificate.json').open('x') as f:json.dump(cert,f,indent=2);f.write('\n')
