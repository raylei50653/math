"""Bounded exploration: J1/J2 with zero-vertex triangulations of the r-hole."""
import argparse
import hashlib
import importlib.util
import json
from itertools import product
from math import factorial
from pathlib import Path

D = Path(__file__).resolve().parent
F = D.parent / "frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, F / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


m = load("frozen/audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py", "core_model")
p = load("frozen/audits/2026-10-19-r6-941-existence-f13eb4d/C/check.py", "patch_model")
ten = [t for t in m.growth(10, four=True) if m.proper(t)]
tris = p.tris(tuple(range(6)))
names = ("a", "n", "R", "L", "q", "c", "s", "v", "w", "t")
right = ("s", "x", "y", "t", "w", "v")
ops = [(left, tri) for left in ("J1", "J2") for tri in tris]
matrices = [[[0] * len(ten) for _ in m.ROWS] for _ in ops]
full_lifts = []
for i, core in enumerate(ten):
    f = dict(zip(names, core))
    core_lifts = [[] for _ in ops]
    for b, x, y in product(range(4), repeat=3):
        ff = dict(f, b=b, x=x, y=y)
        if b in (f["a"], f["c"], f["q"]) or x == y or x in (f["c"], f["s"]) or y in (f["a"], f["t"]):
            continue
        flags = (b == f["L"] and f["a"] != f["R"],
                 f["a"] != f["L"] and f["a"] != f["R"] and b != f["L"])
        row = m.ROWS.index("".join(map(str, m.canonical((x, y, f["a"], b, f["c"])))))
        for j, (left, tri) in enumerate(ops):
            if flags[left == "J2"] and all(ff[right[u]] != ff[right[v]] for u, v in tri):
                matrices[j][row][i] += 1
                core_lifts[j].append([b, x, y])
    fac = factorial(4 - len(set(core)))
    for mat in matrices:
        for row in mat:
            assert row[i] % fac == 0
            row[i] //= fac
    full_lifts.append(core_lifts)
controls = json.loads((F / "D/certificate.json").read_text())["records"]
catpath = "frozen/audits/2026-10-19-r6-941-existence-f13eb4d/frozen/artifacts/c5_cells/cells.json"
catalogue = set(map(int, json.loads((F / catpath).read_text())["cells"]))
records = []
for rec in controls:
    z = rec["core_counts"]
    results = []
    for (left, tri), mat in zip(ops, matrices):
        counts = m.mv(mat, z)
        mask = m.mask(counts)
        results.append({"left": left, "triangles": tri, "counts": counts,
                        "mask": mask, "in_catalogue": mask in catalogue})
    records.append({"branch": rec["branch"], "results": results})
result = {
    "status": "bounded necessary-control extension; source not realized",
    "source_realized": False,
    "pins": names,
    "right_hole": right,
    "operations": [
        {"left": left, "diagonals": [[right[u], right[v]] for u, v in tri],
         "completed_k_delta": -4 if left == "J1" else -3}
        for left, tri in ops
    ],
    "core_states": len(ten),
    "complete_cap_records": len(ten) * len(ops),
    "empty_cap_records": sum(not ls for rec in full_lifts for ls in rec),
    "full_lift_count": sum(len(ls) for rec in full_lifts for ls in rec),
    "full_lifts_sha256": hashlib.sha256(json.dumps(full_lifts, separators=(",", ":")).encode()).hexdigest(),
    "matrices_sha256": hashlib.sha256(json.dumps(matrices, separators=(",", ":")).encode()).hexdigest(),
    "records": records,
}
assert len(tris) == 14 and all(v["in_catalogue"] for r in records for v in r["results"])
for entry in json.loads((D.parent / "INPUTS.json").read_text()):
    raw = (D.parent / "frozen" / entry["path"]).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == entry["sha256"]
ap = argparse.ArgumentParser()
ap.add_argument("--build", action="store_true")
ap.add_argument("--certificate", type=Path, default=D / "certificate.json")
args = ap.parse_args()
result = json.loads(json.dumps(result))
if args.build:
    with args.certificate.open("x") as out:
        json.dump(result, out, indent=2)
        out.write("\n")
else:
    assert json.loads(args.certificate.read_text()) == result
print(json.dumps({k: result[k] for k in (
    "status", "source_realized", "complete_cap_records", "empty_cap_records", "full_lift_count"
)}))
