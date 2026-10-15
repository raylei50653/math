#!/usr/bin/env python3
"""Read-only exact replay; finite controls are not minimum-source realizations."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PINS = tuple("zsvwtpq")
COLORS = range(4)
BASE = "6ddea32a81349821ad3724ae1652bddb9c6a7b04"
MANDATORY = ("zs", "sv", "vw", "wt", "tz", "zp", "zq", "pq")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def seal():
    manifest = read_json(ROOT / "INPUTS.json")
    assert manifest["base"] == BASE
    for entry in manifest["entries"]:
        for path in (ROOT / entry["frozen_path"], REPO / entry["path"]):
            assert digest(path.read_bytes()) == entry["sha256"], str(path)
    return {
        "inputs_sha256": digest((ROOT / "INPUTS.json").read_bytes()),
        "checker_sha256": digest(Path(__file__).read_bytes()),
        "frozen_and_live_input_count": len(manifest["entries"]),
        "input_drift": 0,
    }


def edge_set(edges):
    return sorted({tuple(sorted(e)) for e in edges})


def proper(f, edges):
    return all(f[u] != f[v] for u, v in edges)


def colourings(vertices, edges):
    return [
        x for x in itertools.product(COLORS, repeat=len(vertices))
        if proper(dict(zip(vertices, x)), edges)
    ]


def event(f):
    return f["s"] == f["t"] and not {f["p"], f["q"]} & {f["v"], f["w"]}


def other(name):
    return {"p": "q", "q": "p", "v": "w", "w": "v"}[name]


def quotient(vertices, edges, classes, additions=()):
    mapping = {v: v for v in vertices}
    for group in classes:
        representative = "=".join(group)
        for v in group:
            assert mapping[v] == v
            mapping[v] = representative
    qvertices = tuple(dict.fromkeys(mapping[v] for v in vertices))
    original_images = edge_set((mapping[u], mapping[v]) for u, v in edges)
    qedges = edge_set(original_images + [(mapping[u], mapping[v]) for u, v in additions])
    return qvertices, qedges, mapping, len(edges) - len(original_images)


def pullbacks(vertices, qvertices, qrows, mapping):
    rows = []
    for row in qrows:
        qf = dict(zip(qvertices, row))
        rows.append(tuple(qf[mapping[v]] for v in vertices))
    return sorted(rows)


def key(row):
    return "".join(map(str, row))


def local_semantics():
    edges = edge_set(MANDATORY)
    rows = colourings(PINS, edges)
    assert len(rows) == 1440
    records = []
    for row in rows:
        f = dict(zip(PINS, row))
        lifts = sorted(set(COLORS) - {f[x] for x in "svwt"})
        target = event(f)
        branches = [d + e for d in "pq" for e in "vw"
                    if f["s"] == f["t"] == f[d] and f["z"] == f[e]
                    and f[other(d)] != f[other(e)]]
        assert len(branches) == int(target)
        if target:
            d, e = branches[0]
            assert lifts == [f[other(d)]]
            assert len({f["z"], f["s"], lifts[0]}) == 3
            missing = set(COLORS) - {f["z"], f["s"], lifts[0]}
            assert missing.isdisjoint({f["p"], f["q"]})
        records.append({"row": key(row), "r_lifts": lifts, "event": target,
                        "branches": branches})
    assert sum(r["event"] for r in records) == 96
    return {"proper_row_count": len(rows), "event_count": 96,
            "event_branch_counts": {d+e: sum(d+e in r["branches"] for r in records)
                                     for d in "pq" for e in "vw"},
            "all_rows_including_empty_r_lifts": records}


def graph_controls():
    vertices = PINS + ("h",)
    mandatory = edge_set(MANDATORY)
    local_rows = colourings(PINS, mandatory)
    result = []
    for optional in (None, "tp", "sq"):
        edges = edge_set(list(MANDATORY) + ["vh", "wh"] + ([optional] if optional else []))
        rows = colourings(vertices, edges)
        indexed = {key(row): [] for row in local_rows}
        for row in rows:
            indexed[key(row[:7])].append(key(row))
        assert sum(map(len, indexed.values())) == len(rows)
        target = [row for row in rows if event(dict(zip(vertices, row)))]
        obligations = []
        union_two, union_four = [], []
        for d in "pq":
            for e in (None, "v", "w"):
                classes = [("s", "t", d)]
                additions = [(other(d), "v"), (other(d), "w")]
                if e:
                    classes.append(("z", e))
                    additions = [(other(d), other(e))]
                qverts, qedges, mapping, duplicate_loss = quotient(vertices, edges, classes, additions)
                qrows = colourings(qverts, qedges)
                lifts = pullbacks(vertices, qverts, qrows, mapping)
                expected = [row for row in target if (lambda f:
                    f[d] == f["s"] and (e is None or f[e] == f["z"]))
                    (dict(zip(vertices, row)))]
                assert lifts == expected
                (union_four if e else union_two).extend(lifts)
                obligations.append({
                    "name": ("K_" + d + e) if e else ("H_" + d),
                    "vertices": qverts, "edges": qedges,
                    "original_to_quotient": mapping,
                    "has_loop": any(u == v for u, v in qedges),
                    "all_quotient_colourings": qrows,
                    "all_full_pullbacks": [key(row) for row in lifts],
                })
        assert sorted(union_two) == target == sorted(union_four)
        assert len(union_four) == len(set(union_four))
        result.append({
            "name": "private_h_" + (optional or "no_optional"),
            "scope": "whole_graph_control_not_minimum_source",
            "vertices": vertices, "edges": edges,
            "all_full_colourings": [key(row) for row in rows],
            "seven_pin_fibres_including_empties": indexed,
            "all_other_4^7_pin_assignments": "empty: violate a mandatory original edge",
            "event_full_colourings": [key(row) for row in target],
            "obligations": obligations,
        })
    return result


def density_arithmetic():
    # These five indicator classes exhaust a,c>=4 and a+c>=11.
    degree_classes = [(4, 7, "a=4,c>=7"), (5, 6, "a=5,c>=6"),
                      (6, 5, "a>=6,c=5"), (7, 4, "a>=7,c=4"),
                      (6, 6, "a>=6,c>=6")]
    records = []
    for a, c, label in degree_classes:
        vertices = list(PINS)
        edges = list(MANDATORY)
        if a == 4:
            edges.append("tp")
        if c == 4:
            edges.append("sq")
        if a == 5:
            vertices.append("j_a")
            edges += [("j_a", v) for v in "ztp"]
        if c == 5:
            vertices.append("j_c")
            edges += [("j_c", v) for v in "zsq"]
        edges = edge_set(edges)
        for d in "pq":
            delta = int((a if d == "p" else c) == 5) + int((c if d == "p" else a) == 4)
            blocked = (a if d == "p" else c) == 4
            assert delta <= 1
            iv, ie, mapping, loss = quotient(vertices, edges, [("s", "t", d)])
            assert any(u == v for u, v in ie) == blocked
            record = {"degree_class": label, "orientation": d,
                      "incidence_model_vertices": vertices, "incidence_model_edges": edges,
                      "blocked_by_original_loop": blocked}
            if not blocked:
                assert loss == 2 + delta
                for e in "vw":
                    kv, ke, km, kloss = quotient(vertices, edges,
                        [("s", "t", d), ("z", e)], [(other(d), other(e))])
                    assert kloss == 3 + delta
                    assert len(ke) == len(edges) - 2 - delta
                # The actual source m=3k-8 is a paper premise, not true
                # of the small incidence model itself.
                record.update({"delta": delta, "triple_duplicate_loss": loss,
                    "four_branch_duplicate_loss": 3 + delta,
                    "I_planar_excess": 2-delta, "H_planar_excess": 4-delta,
                    "K_planar_excess": 5-delta,
                    "source_counts": {"J": ["k-1", "3k-9"],
                        "I": ["k-2", f"3k-{10+delta}"],
                        "H": ["k-2", f"3k-{8+delta}"],
                        "K": ["k-3", f"3k-{10+delta}"]}})
            records.append(record)
    v, e, mapping, loss = quotient(PINS, edge_set(MANDATORY), [("s", "t")],
                                  ["pv", "pw", "qv", "qw"])
    left, right = ["z", "v", "w"], ["s=t", "p", "q"]
    crossing = edge_set(itertools.product(left, right))
    assert set(crossing).issubset(e) and len(crossing) == 9
    return {"source_status": "not triggered: no genuine minimum source supplied",
            "five_exhaustive_degree_indicator_classes": records,
            "unsplit_K33": {"parts": [left, right], "nine_edges": crossing},
            "completed_source_cost": {"U": "k+5", "I_H": "(k-2)+2+5=k+5",
                                      "K": "(k-3)+3+5=k+5"}}


def compute():
    return {"schema": "six-pin-forcing-v1", "base": BASE, "binding": seal(),
            "local_semantics": local_semantics(), "whole_graph_controls": graph_controls(),
            "density_arithmetic": density_arithmetic()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path, default=ROOT / "certificate.json")
    args = parser.parse_args()
    assert args.generate != args.check, "choose exactly one mode"
    expected = compute()
    if args.generate:
        with args.certificate.open("x") as handle:
            json.dump(expected, handle, indent=2)
            handle.write("\n")
    else:
        assert read_json(args.certificate) == json.loads(json.dumps(expected)), "certificate mismatch"
    print(json.dumps({"status": "PASS", "mode": "generate" if args.generate else "read_only_check",
        "local_proper_rows": 1440, "event_rows": 96,
        "full_control_colourings": [len(c["all_full_colourings"]) for c in expected["whole_graph_controls"]],
        "full_control_event_colourings": [len(c["event_full_colourings"]) for c in expected["whole_graph_controls"]],
        "source_status": "not triggered", "input_drift": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
