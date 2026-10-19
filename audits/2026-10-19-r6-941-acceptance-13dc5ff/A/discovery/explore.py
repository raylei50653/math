import importlib.util,json,time
from pathlib import Path
D=Path(__file__).resolve().parent
P=D.parents[2]/"2026-10-19-r6-941-quotients-13dc5ff/A/model.py"
spec=importlib.util.spec_from_file_location("model",P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
f=m.interfaces(); print("interfaces",flush=True)
k=m.kempe(10,f["ten"]);print("K10",flush=True)
base=[i for i in range(2461) if all(f["C"]["G"][j][i]==0 for j in (1,4,6))]
for name in ("base","Q1","Q2"):
 initial=base if name=="base" else [i for i in base if not f["C"][name][9][i]]
 live,rounds=m.close(k,initial)
 obs={g:{m.ROWS[j]:sum(f["C"][g][j][i] for i in live) for j in (1,4,6,9)} for g in ("G","Q1","Q2","GB")}
 print(name,len(initial),[len(r) for r in rounds],len(live),obs,flush=True)
 (D/(name+"-closure.json")).write_text(json.dumps({"initial":initial,"rounds":rounds,"live":live,"observables":obs},indent=2)+"\n")
