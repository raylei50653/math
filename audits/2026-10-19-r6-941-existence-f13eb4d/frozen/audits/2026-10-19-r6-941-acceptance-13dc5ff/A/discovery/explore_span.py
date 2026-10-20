exec((__import__("pathlib").Path(__file__).parent/"explore.py").read_text().split('k=m.kempe')[0])
k=m.kempe(8,f["eight"])
obs={"a1":f["M"]["Q1"][9],"a2":f["M"]["Q2"][9]}
for g in ("Q1","Q2","GB"):
 for j,s in ((1,"T"),(4,"U"),(6,"V")):obs[g+s]=f["M"][g][j]
obs.update({"Aa":f["sectors"]["Aa"],"Ab":f["sectors"]["Ab"]})
base=[i for i in range(274) if all(f["M"]["G"][j][i]==0 for j in (1,4,6))]
for name in ("base","Q1","Q2"):
 initial=base if name=="base" else [i for i in base if not f["M"][name][9][i]]
 live,rounds=m.close(k,initial);parts,A,basis=m.planar_basis(f["eight"],live)
 rows=[[sum(x*y for x,y in zip(v,b)) for v in obs.values()] for b in basis]
 red,piv=m.rref(rows)
 identities=[]
 for free in range(len(obs)):
  if free in piv:continue
  c=[0]*len(obs);c[free]=1
  for j,p in enumerate(piv):c[p]=-red[j][free]
  identities.append({key:str(a) for key,a in zip(obs,c) if a})
 print(name,len(initial),[len(r) for r in rounds],len(live),len(basis),len(piv),identities,flush=True)
