import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));import model
F=model.interfaces();K=model.kempe(10,F['ten']);forbidden={i for i in range(2461) if any(F['C']['G'][j][i]>0 for j in (1,4,6))}
for name,a,b in [('Rv',2,7),('Lw',3,8),('qt',4,9)]:
 initial=set(range(2461))-forbidden-{i for i,t in enumerate(F['ten']) if t[a]==t[b]};live,rounds=model.close(K,initial);projection=model.mask([sum(F['C']['G'][j][i] for i in live) for j in range(10)]);print(name,len(live),list(map(len,rounds)),projection,flush=True)
