import importlib.util,json
from pathlib import Path
from fractions import Fraction
D=Path(__file__).resolve().parent;F=D.parent/'frozen';OLD=F/'audits/2026-10-19-r6-941-existence-f13eb4d'
s=importlib.util.spec_from_file_location('m',F/'audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
I=m.interfaces();K=m.kempe(8,I['eight']);J=json.loads((OLD/'C/comparisons.json').read_text())['matrices'];out=[]
for q,g in [('Q1','J1'),('Q2','J2')]:
 M=J[g]['E'];zero=[I['M']['G'][j] for j in (1,4,6)]+[I['M'][q][9],M[4],M[6]]
 live,rounds=m.close(K,[i for i in range(274) if all(not r[i] for r in zero)])
 parts,A,basis=m.planar_basis(I['eight'],live)
 vals=[sum(x*y for x,y in zip(M[1],b)) for b in basis]
 print(q,g,'live',len(live),'basis',len(basis),'T nonzero',[(i,str(v)) for i,v in enumerate(vals) if v],flush=True)
 out.append({'q':q,'g':g,'live':live,'basis':[[str(x) for x in b] for b in basis],'T_values':list(map(str,vals))})
(D/'t_count_discovery.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
