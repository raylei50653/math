import json,pickle,numpy as np
from pathlib import Path
D=Path(__file__).resolve().parent
u=json.loads((D.parent/'C/u319-core.json').read_text());M=np.array(u['literal_U_count_matrix'])
for name in ('Q1','Q2','GB'):
 with (D/('combined-old-'+name+'.pickle')).open('rb') as f:x=pickle.load(f)
 y=M@x[:2461]
 print(name,'Ucounts',list(y),'Umask',sum(1<<i for i,v in enumerate(y) if v>1e-8))
