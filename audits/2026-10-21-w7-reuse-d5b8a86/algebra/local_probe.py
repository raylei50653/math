#!/usr/bin/env python3
"""Additional exact local-row-basis measurements, after probe.py input verification."""
import collections,json,sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'audits/2026-10-20-w7-count-opt-d5b8a86'))
sys.dont_write_bytecode = True
from model import Model
m=Model(); ref=m.reference('mindeg'); D=m.difference(ref).astype(np.int64); C=m.incidence().tocsr().astype(np.int64)
Dc=D.tocsc()
low=np.flatnonzero(np.diff(Dc.indptr)<=3)
records=[]
for j in low:
 s,e=Dc.indptr[j:j+2]; rr=Dc.indices[s:e]; vv=Dc.data[s:e]
 records.append({'column':int(j),'rows':rr.tolist(),'coefficients':vv.tolist(),
                 'live_states':m.live[np.unique(rr//2)].tolist()})
# Original C half-row equality implies Z equality; verify exact sparse tuples.
groups=collections.defaultdict(list)
for i in range(C.shape[0]):
 s,e=C.indptr[i:i+2]
 groups[tuple(map(int,C.indices[s:e]))].append(i)
eq=[v for v in groups.values() if len(v)>1]
out={'half_row_degree_histogram':dict(sorted(collections.Counter(map(int,np.diff(C.indptr))).items())),
     'equal_half_row_groups':len(eq),'equal_half_row_reduction':sum(len(v)-1 for v in eq),
     'equal_half_row_examples':eq[:10], 'degree_at_most_three_columns':records}
(HERE/'local.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
