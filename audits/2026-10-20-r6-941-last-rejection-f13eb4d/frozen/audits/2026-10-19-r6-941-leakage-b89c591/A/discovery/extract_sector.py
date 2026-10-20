exec((__import__('pathlib').Path(__file__).resolve().parent/'extract_exact.py').read_text().split('for name in')[0])
for name in ('Q2',):
 with (D/('combined-sector-'+name+'.pickle')).open('rb') as f:x=pickle.load(f)
 for lim in (100,1000,10000,1000000):
  rat=[F(float(v)).limit_denominator(lim) for v in x];mul=lcm(*(v.denominator for v in rat));vec=[int(v*mul) for v in rat]
  cc=AA[:-274,:].tocoo();res=[0]*cc.shape[0]
  for r,c,v in zip(cc.row,cc.col,cc.data):res[r]+=int(v)*vec[c]
  if not any(res):
   div=reduce(gcd,vec);vec=[v//div for v in vec]
   print(name,'exact','denmax',max(v.denominator for v in rat),'scale',mul//div,'maxdigits',len(str(max(map(abs,vec)))),'nz',sum(bool(v) for v in vec),flush=True)
   with (D/('exact-sector-'+name+'.pickle')).open('wb') as f:pickle.dump(vec,f)
   break
 else:print(name,'not exact',flush=True)
