#!/usr/bin/env python3
"""Bounded symbolic and minor calibration; never a K1-K12 source checker."""
import argparse
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
COL = frozenset(range(4))


def subsets(xs):
    xs = tuple(xs)
    return [set(xs[i] for i in range(len(xs)) if mask & (1 << i))
            for mask in range(1 << len(xs))]


def stabilizes(pair, values):
    for pi in itertools.permutations(range(4)):
        if all(pi[c] == c for c in values):
            if {pi[c] for c in pair} != set(pair):
                return False
    return True


def edge(a, b):
    return tuple(sorted((a, b)))


def connected(vertices, edges):
    vertices = set(vertices)
    if not vertices:
        return False
    seen = {min(vertices)}
    while True:
        nxt = seen | {v for u in seen for v in vertices
                      if edge(u, v) in edges}
        if nxt == seen:
            return seen == vertices
        seen = nxt


def verify_minor(edges, bags):
    assert len(bags) == 5
    for a, b in itertools.combinations(bags, 2):
        assert not set(a) & set(b), "overlapping bags"
        assert any(edge(x, y) in edges for x in a for y in b), "missing adjacency"
    assert all(connected(b, edges) for b in bags), "disconnected bag"
    return {"edges": [list(e) for e in sorted(edges)],
            "bags": [sorted(b) for b in bags], "all_ten_original_adjacencies": True}


def cycle_path_minor(kind, length, index):
    root = "r" if kind == "S" else "s"
    edges = {edge("b" + str(i), "b" + str((i + 1) % 5)) for i in range(5)}
    path = ["x" + str(i) for i in range(length + 1)]
    edges.update(edge(path[i], path[i+1]) for i in range(length))
    edges.update([edge(root, path[0]), edge(root, path[-1])])
    left, right = path[index], path[index+1]
    target = "b2" if kind == "S" else "b4"
    edges.update([edge(root, "exterior"), edge("exterior", target)])
    for x in [left, right]:
        edges.add(edge(x, "b0"))
        edges.add(edge(x, "b4" if kind == "S" else "b2"))
    z = {root, "exterior", *path} - {left, right}
    if kind == "S":
        z.update(["b1", "b2", "b3"])
        bags = [{left}, {right}, {"b0"}, {"b4"}, z]
    else:
        z.update(["b3", "b4"])
        bags = [{left}, {right}, {"b0"}, {"b1", "b2"}, z]
    return {"kind": kind, "path_length": length, "chosen_edge_index": index,
            **verify_minor(edges, bags)}


def leaf_minor(length):
    cyc = ["c" + str(i) for i in range(length)]
    edges = {edge("b" + str(i), "b" + str((i + 1) % 5)) for i in range(5)}
    edges.update(edge(cyc[i], cyc[(i + 1) % length]) for i in range(length))
    edges.update([edge("c0", "path_root"), edge("path_root", "r"),
                  edge("r", "exterior"), edge("exterior", "b2")])
    for x in ["c1", "c2"]:
        edges.update([edge(x, "b0"), edge(x, "b4")])
    z = set(cyc) - {"c1", "c2"}
    z.update(["path_root", "r", "exterior", "b1", "b2", "b3"])
    return {"leaf_cycle_length": length,
            **verify_minor(edges, [{"c1"}, {"c2"}, {"b0"}, {"b4"}, z])}


def compute(spec):
    assert spec["scope"] == "bounded calibration; not target source enumeration"
    assert spec["colours"] == [0, 1, 2, 3]
    assert spec["permutations"] == "all 24 S4"
    assert spec["path_lengths"] == [1, 3, 5]
    assert spec["leaf_cycle_lengths"] == [3, 5]
    rows = {"q3": [0, 1, 0, 2, 1], "q4": [0, 1, 0, 1, 2],
            "q1": [0, 1, 2, 0, 2]}
    palette = []
    for name in ["q3", "q4"]:
        for support in subsets([0, 4]):
            for contact in [False, True]:
                values = {rows[name][i] for i in support}
                if contact:
                    values.add(1)
                for pair in itertools.combinations([0, 2, 3], 2):
                    ok = stabilizes(pair, values)
                    palette.append({"row": name, "actual_support": sorted(support),
                                    "contains_fixed_s1_contact": contact,
                                    "pair": list(pair), "stabilizer_holds": ok})
                    if name == "q4" and not contact and ok:
                        assert set(pair) == {0, 2}
                    if name == "q4" and set(pair) == {0, 2} and ok:
                        assert support == {0, 4}
                    if name == "q3" and set(pair) == {2, 3} and ok:
                        assert 0 in support and (contact or 4 in support)
    # Whole-S beta q3 stabilizer and N-diagonal exclude all but pair23.
    allowed_q3 = [list(p) for p in itertools.combinations([0, 2, 3], 2)
                  if stabilizes(p, {0, 1})]
    assert allowed_q3 == [[2, 3]]
    u_rows = []
    for support in subsets([0, 1, 2]):
        ok = stabilizes({1, 3}, {rows["q1"][i] for i in support})
        if ok:
            assert {0, 2} <= support
        u_rows.append({"row": "q1", "actual_support": sorted(support),
                       "pair": [1, 3], "stabilizer_holds": ok})
    widgets = []
    for b in [1, 3]:
        for a in range(4):
            witnesses = [[u, v] for u in range(4) for v in range(4)
                         if u not in {a, 0, 2} and v not in {a, b, 0} and u != v]
            assert witnesses
            widgets.append({"r": a, "s": b, "one_conditional_template_witness": witnesses[0]})
    minors = [cycle_path_minor(kind, n, i) for kind in ["S", "U"]
              for n in spec["path_lengths"] for i in range(n)]
    leaves = [leaf_minor(n) for n in spec["leaf_cycle_lengths"]]
    negative = []
    good = cycle_path_minor("S", 1, 0)
    ee = {tuple(e) for e in good["edges"]}
    bb = [set(b) for b in good["bags"]]
    for label, broken in [("missing actual tether", ee - {edge("x0", "b4")}),
                          ("missing exterior connection", ee - {edge("r", "exterior")})]:
        try:
            verify_minor(broken, bb)
        except AssertionError as exc:
            negative.append({"case": label, "rejected": True, "reason": str(exc)})
        else:
            raise AssertionError("negative minor accepted")
    return {"scope": spec["scope"], "status": "triggered and holds",
            "S_palette_cases": palette, "U_palette_cases": u_rows,
            "beta_q3_S_pair": allowed_q3[0], "conditional_S_widget_queries": widgets,
            "path_minor_skeletons": minors, "leaf_minor_skeletons": leaves,
            "negative_minor_skeletons": negative,
            "target_source": {"executed": False, "trigger_count": None,
                              "status": "not triggered"},
            "not_proved_by_controls": ["arbitrary-size paper induction", "source realizability", "Lean"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path, default=HERE / "calibration-certificate.json")
    args = parser.parse_args()
    assert args.generate != args.check, "choose exactly one mode"
    got = compute(json.loads((HERE / "calibration-input.json").read_text()))
    data = (json.dumps(got, sort_keys=True, ensure_ascii=False, indent=2) + "\n").encode()
    if args.generate:
        with args.certificate.open("xb") as out:
            out.write(data)
    else:
        assert args.certificate.read_bytes() == data, "certificate bytes mismatch"
    print(json.dumps({"status": "triggered and holds", "S_palette_cases": len(got["S_palette_cases"]),
                      "U_palette_cases": len(got["U_palette_cases"]),
                      "conditional_widget_queries": len(got["conditional_S_widget_queries"]),
                      "path_minor_skeletons": len(got["path_minor_skeletons"]),
                      "leaf_minor_skeletons": len(got["leaf_minor_skeletons"]),
                      "negative_minor_skeletons_rejected": len(got["negative_minor_skeletons"]),
                      "target_source_executed": False, "target_trigger_count": None}, sort_keys=True))


if __name__ == "__main__":
    main()
