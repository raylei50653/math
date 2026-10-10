#!/usr/bin/env python3
"""Exclusive-create fixed-control proposals and deliberate negative copies.

Only the already frozen 19 N2 and four N1 controls are read. No graph search.
"""
import copy
import json
from pathlib import Path
import validator as v

HOME = Path(__file__).resolve().parent
N2 = ["NA7-0002", "NA8-0014", "NA8-0015", "NA8-0016", "NA8-0017", "NA8-0018", "NA8-0020", "NA8-0021", "NA8-0022", "NA9-0010", "NA9-0011", "NA9-0020", "NA9-0021", "NA9-0022", "NA9-0023", "NA9-0024", "NA9-0025", "NA9-0026", "NA9-0027"]
N1 = ["NA8-0003", "NA8-0007", "NA8-0009", "NA8-0010"]


def write(path, data):
    with path.open("xb") as f:
        f.write(v.enc(data))


def main():
    (HOME / "controls-v2").mkdir()
    (HOME / "negative-inputs-v2").mkdir()
    proposals = []
    for name in N2 + N1:
        path = HOME / "source/artifacts/c5_excess_two_e4c/controls" / (name + ".json")
        raw = json.loads(path.read_text())
        g = v.compute_graph(raw)
        for p in g["pieces"]:
            if p["kind"] != "unary" or sum(p["incidences"]) != 1:
                continue
            index = next(i for i, row in enumerate(g["rows"]) if not row["root_pairs"])
            q = {"schema": "n45-pc-v1", "graph_file": "../source/artifacts/c5_excess_two_e4c/controls/" + name + ".json",
                 "source_sha256": v.digest(path), "frame": g["frame"], "roots": g["roots"],
                 "pieces": copy.deepcopy(raw["pieces"]), "roles": {"U": p["id"], "L": None, "S": None},
                 "beta": v.PATTERNS[index], "purpose": "Fixed N2 control" if name in N2 else "N1 interface calibration only",
                 "X": {"vertices": [x for x in g["vertices"] if x not in p["vertices"]],
                       "edges": [e for e in g["edges"] if not set(e) & set(p["vertices"])]}}
            fname = name + "-" + p["id"] + ".json"
            write(HOME / "controls-v2" / fname, q)
            proposals.append({"id": name, "piece": p["id"], "family": "N2" if name in N2 else "N1 calibration", "proposal": "controls-v2/" + fname})
    write(HOME / "controls-v2/index.json", proposals)
    original_q = json.loads((HOME / "controls-v2/NA7-0002-P1.json").read_text())
    raw = json.loads((HOME / "source/artifacts/c5_excess_two_e4c/controls/NA7-0002.json").read_text())
    piece = next(p for p in raw["pieces"] if p["id"] == "P0")
    t = piece["rows"][0]["tuples"][0]
    tuple_oracle = {"piece": "P0", "index": 0, "literal_beta": v.PATTERNS[0],
                    "original_contact_tuple": t["tuple"], "original_legal_piece_lift": t["lifts"][0],
                    "original_root_contact_edges": [[5, 9], [6, 9]], "shared_original_vertex": 9}
    whole_oracle = {"literal_beta": v.PATTERNS[0], "legal_whole_lift": raw["witnesses"]["0"], "original_edge": [0, 5]}
    cases = []
    q = copy.deepcopy(original_q)
    q["pieces"][0]["rows"][0]["tuples"].pop(0)
    cases.append(("missing-complete-tuple", q, "complete relation/full lifts differ", tuple_oracle))
    q = copy.deepcopy(original_q)
    q["pieces"][0]["contacts"]["6"].remove(9)
    cases.append(("wrong-shared-ownership", q, "has wrong contacts", tuple_oracle))
    q = copy.deepcopy(original_q)
    q["source_sha256"] = "0" * 64
    cases.append(("stale-source-hash", q, "stale source_sha256", whole_oracle))
    q = copy.deepcopy(original_q)
    q["X"]["edges"].remove([0, 5])
    cases.append(("wrong-whole-unit-X", q, "declared X is not exactly", whole_oracle))
    q = copy.deepcopy(original_q)
    q["roles"]["U"] = "P0"
    cases.append(("wrong-declared-unit", q, "not a complete original incidence-one unary", tuple_oracle))
    index = []
    for name, q, error, oracle in cases:
        write(HOME / "negative-inputs-v2" / (name + ".json"), q)
        index.append({"id": name, "proposal": "negative-inputs-v2/" + name + ".json", "expected_error": error, "oracle": oracle,
                      "scope": "Deliberately incorrect declaration of an unchanged original graph; not a source counterexample."})
    write(HOME / "negative-inputs-v2/index.json", index)
    print(json.dumps({"fixed_proposals": len(proposals), "N2": sum(p["family"] == "N2" for p in proposals),
                      "N1_calibration": sum(p["family"] != "N2" for p in proposals), "negative_copies": len(cases)}, sort_keys=True))


if __name__ == "__main__":
    main()
