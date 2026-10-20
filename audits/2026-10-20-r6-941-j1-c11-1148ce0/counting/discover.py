"""Discovery of a common C11 count vector. Numerical output is not a proof."""
from pathlib import Path
import importlib.util
import gzip
import json
import pickle
import time
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix, hstack, vstack
from scipy.optimize import linprog

D = Path(__file__).resolve().parent
OLD = D.parent / "frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c"
spec = importlib.util.spec_from_file_location("old", OLD / "interface/check.py")
o = importlib.util.module_from_spec(spec)
spec.loader.exec_module(o)
I = json.load(gzip.open(OLD / "interface/certificate-v4.json.gz", "rt"))
states = [tuple(c["core"]) for c in I["caps"]]
n = len(states)
start = time.monotonic()
K = o.old.kempe(11, states)
print("Kempe built", time.monotonic()-start, flush=True)
rr, cc, vv = [], [], []
for j, col in enumerate(K["columns"]):
    for r, v in col:
        rr.append(r); cc.append(j); vv.append(v)
B = coo_matrix((vv, (rr, cc)), shape=(len(K["hrows"]), len(K["columns"]))).tocsr()
A = coo_matrix((K["hsize"], (range(len(K["hrows"])), K["rowids"])),
               shape=(len(K["hrows"]), n)).tocsr()
parts = [p for p in o.old.ncgrowth(11) if o.m.proper(p)]
S = np.asarray(states)
columns = []
for p in parts:
    pairs = [(i, j) for i in range(11) for j in range(i) if p[i] == p[j]]
    col = np.ones(n, dtype=np.int8)
    for i, j in pairs:
        col &= S[:, i] == S[:, j]
    columns.append(col)
P = csr_matrix(np.stack(columns, axis=1))
E = vstack([hstack([A, -B, csr_matrix((A.shape[0], len(parts)))]),
            hstack([csr_matrix(np.eye(n)), csr_matrix((n, B.shape[1])), -P])]).tocsr()
M = {g: np.zeros((10, n), dtype=int) for g in ("G", "Q1", "J1")}
sectors = np.zeros((2, n), dtype=int)
for i, cap in enumerate(I["caps"]):
    a, _, _, _, _, _, c, *_ = cap["core"]
    for name, key in (("G","original_left_bphR"),("Q1","Q1_left_bR"),("J1","J1_left_bR")):
        for left in cap[key]:
            b = left[0]
            for x,y,r in cap["right_xyr"]:
                j = o.m.ROWS.index("".join(map(str,o.m.canonical((x,y,a,b,c)))))
                M[name][j,i] += 1
                if name == "G" and j == 9:
                    sectors[0,i] += left[2] == a
                    sectors[1,i] += left[2] == b
pos = [M["G"][j] for j in range(10) if 941 >> j & 1]
pos += list(sectors)
w = np.zeros(n, dtype=int)
for rec in I["witnesses"]:
    w[rec["canonical_id"]] = 1
pos.append(w)
U = hstack([-csr_matrix(np.stack(pos)), csr_matrix((len(pos), B.shape[1]+len(parts)))]).tocsr()
live = set(I["live"])
bounds = [(0,None) if i in live else (0,0) for i in range(n)]
bounds += [(0,None)] * B.shape[1] + [(None,None)] * len(parts)
print("LP", E.shape, E.nnz, "parts",len(parts),time.monotonic()-start,flush=True)
ans = linprog(np.r_[np.ones(n),np.zeros(B.shape[1]+len(parts))],
              A_eq=E,b_eq=np.zeros(E.shape[0]),A_ub=U,b_ub=-np.ones(len(pos)),
              bounds=bounds,options={"time_limit":240})
print(ans.message, time.monotonic()-start, flush=True)
with (D/"discovery.pickle").open("xb") as f:
    pickle.dump((K, parts, E, U, M, sectors, ans), f)
out = {"success":bool(ans.success),"message":ans.message,
       "elapsed_seconds":time.monotonic()-start,"source_excluded":False}
if ans.success:
    out["nonzero"] = int(np.count_nonzero(ans.x[:n]))
    out["max"] = float(np.max(np.abs(ans.x)))
    out["counts"] = {g: (mat@ans.x[:n]).tolist() for g,mat in M.items()}
    out["short_witness_sum"] = float(w@ans.x[:n])
with (D/"discovery.json").open("x") as f:
    json.dump(out,f,indent=2);f.write("\n")
print(json.dumps(out),flush=True)
