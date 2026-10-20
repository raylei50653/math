from pathlib import Path
from fractions import Fraction
from math import lcm
import numpy as np,json
H=Path(__file__).resolve().parent
v=np.load(H/'counted-discovery.npz')['x']
fs=[Fraction(float(x)).limit_denominator(64) for x in v]
assert max(abs(float(f)-float(x)) for f,x in zip(fs,v))<1e-6
scale=lcm(*(f.denominator for f in fs))
a=[int(f*scale) for f in fs]
n,k=2461,10798
rec={'model_only':True,'source_realized':False,'scale':scale,'core_counts':a[:n], 'orbit_weights':[[j,x] for j,x in enumerate(a[n:n+k]) if x], 'planar_coefficients':[[j,x] for j,x in enumerate(a[n+k:]) if x]}
with (H.parent/'counted-control.json').open('x') as out:json.dump(rec,out,separators=(',',':'));out.write('\n')
print('scale',scale,'maxabs',max(map(abs,a)),'positive core',sum(x>0 for x in a[:n]),'orbits',len(rec['orbit_weights']),'planar',len(rec['planar_coefficients']))
