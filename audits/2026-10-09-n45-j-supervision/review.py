#!/usr/bin/env python3
"""Read-only N45-J acceptance check; no project/checker module imports.

Enumerate full graph and local colorings using bit domains and forced-color
propagation, then compare all joint fibres and capacity columns independently.
"""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
DELIVERY = ROOT / "audits/2026-10-09-n45-j"
BASE = "dc8e9aa7d6fccb51f63d30aa3f9c132296d44744"
ROWS = [tuple(map(int, s)) for s in (
    "01012", "01021", "01023", "01201", "01202", "01203",
    "01212", "01213", "01231", "01232")]


def require(ok, label):
    if not ok:
        raise ValueError(label)


def digest(raw):
    return sha256(raw).hexdigest()


def colorings(vertices, edges, pins):
    """All solutions; singleton propagation on bit domains, no tuple inputs."""
    index = {v: i for i, v in enumerate(vertices)}
    adjacency = [set() for _ in vertices]
    for u, v in edges:
        adjacency[index[u]].add(index[v])
        adjacency[index[v]].add(index[u])
    initial = [15] * len(vertices)
    for v, c in pins.items():
        initial[index[v]] = 1 << c

    def search(domains):
        queue = [i for i, d in enumerate(domains) if d.bit_count() == 1]
        processed = set()
        while queue:
            i = queue.pop()
            if i in processed:
                continue
            processed.add(i)
            for j in adjacency[i]:
                new = domains[j] & ~domains[i]
                if new == 0:
                    return
                if new != domains[j]:
                    domains[j] = new
                    if new.bit_count() == 1:
                        queue.append(j)
        choices = [i for i, d in enumerate(domains) if d.bit_count() > 1]
        if not choices:
            yield tuple(d.bit_length() - 1 for d in domains)
            return
        i = max(choices, key=lambda j: (len(adjacency[j]), -j))
        for c in range(4):
            if domains[i] & (1 << c):
                trial = domains.copy()
                trial[i] = 1 << c
                yield from search(trial)

    yield from search(initial)


def lift_ok(vertices, edges, pins, lift):
    if lift is None or len(lift) != len(vertices) or any(c not in range(4) for c in lift):
        return False
    f = dict(zip(vertices, lift))
    return all(f[v] == c for v, c in pins.items()) and all(f[u] != f[v] for u, v in edges)


def main():
    manifest = json.loads((DELIVERY / "inputs.json").read_bytes())
    require(manifest["BASE"] == manifest["actual_HEAD"] == BASE, "BASE")
    for item in manifest["files"]:
        raw = (DELIVERY / item["frozen_path"]).read_bytes()
        git_raw = subprocess.check_output(["git", "show", BASE + ":" + item["path"]], cwd=ROOT)
        require(raw == git_raw and len(raw) == item["bytes"] and digest(raw) == item["sha256"], item["path"])
    listed = set()
    for line in (DELIVERY / "MANIFEST.sha256").read_text().splitlines():
        expected, path = line.split(maxsplit=1)
        path = path.lstrip("*")
        listed.add(path)
        require(digest((DELIVERY / path).read_bytes()) == expected, "manifest " + path)
    actual = {str(p.relative_to(DELIVERY)) for p in DELIVERY.rglob("*")
              if p.is_file() and p.name != "MANIFEST.sha256"}
    require(listed == actual, "manifest inventory")
    cert = json.loads((DELIVERY / "results/certificate.json").read_bytes())
    require(cert["checker_sha256"] == digest((DELIVERY / "checker.py").read_bytes()), "checker binding")
    require(cert["inputs_sha256"] == digest((DELIVERY / "inputs.json").read_bytes()), "input binding")
    counts = Counter()
    domains = {}
    for label in ("N2", "N1_separate"):
        group_counts = Counter()
        records = cert[label]
        for rec in records:
            g = rec["graph"]
            roots, frame, vs, es = g["roots"], g["frame"], g["vertices"], g["edges"]
            raw = json.loads((DELIVERY / "frozen/artifacts/c5_excess_two_e4c/controls" / (rec["id"] + ".json")).read_bytes())
            require(raw["vertices"] == vs and raw["edges"] == es, "original edge binding")
            ps = {p["id"]: p for p in rec["pieces"]}
            relations = []
            for i, beta in enumerate(ROWS):
                by_piece = {}
                for p in ps.values():
                    pv = p["vertices"]
                    selected = sorted(set(frame) | set(pv))
                    edges = [e for e in es if set(e) <= set(selected)]
                    generated = defaultdict(set)
                    for solution in colorings(selected, edges, dict(zip(frame, beta))):
                        f = dict(zip(selected, solution))
                        generated[tuple(f[v] for v in p["contact_order"])].add(tuple(f[v] for v in pv))
                    saved = rec["relations"][i][p["id"]]
                    tuples = {tuple(x["tuple"]): {tuple(v) for v in x["lifts"]} for x in saved["tuples"]}
                    require(dict(generated) == tuples, "local relation/lifts " + rec["id"])
                    require(len(tuples) == len(saved["tuples"]), "duplicate local tuple")
                    for x in saved["tuples"]:
                        require(len(x["lifts"]) == len(set(map(tuple, x["lifts"]))), "duplicate lift")
                    fibres = {}
                    for a, b in product(range(4), repeat=2):
                        pins = dict(zip(roots, (a, b)))
                        ids = [j for j, x in enumerate(saved["tuples"])
                               if all(x["tuple"][p["contact_order"].index(v)] != pins[r]
                                      for r in p["owners"] for v in p["contacts"][str(r)])]
                        require(saved["fibres"][4*a+b] == {"pins": [a, b], "tuple_indices": ids}, "local fibre")
                        fibres[(a, b)] = bool(ids)
                    by_piece[p["id"]] = fibres
                    group_counts["local_relations"] += 1
                relations.append(by_piece)
            evaluations = [("original", rec["original"])] + [("derivative", x) for x in rec["unit_derivatives"]]
            for kind, ev in evaluations:
                unit = ev["derivative"]
                removed = set(unit.get("removed_vertices", [])) if unit else set()
                cut = unit.get("edge") if unit else None
                evs = [v for v in vs if v not in removed]
                ees = [e for e in es if e != cut and not set(e) & removed]
                require(evs == ev["vertices"] and ees == ev["edges"], "derivative edge identity")
                active = [p for p in ps.values() if not unit or p["id"] != unit.get("piece")]
                degree = {r: sum(r in e for e in ees) for r in roots}
                require(ev["root_degrees"] == [degree[r] for r in roots], "root degrees")
                require(len(ev["rows"]) == 10, "row coverage")
                mask = 0
                for i, row in enumerate(ev["rows"]):
                    beta = ROWS[i]
                    require(row["index"] == i and tuple(row["beta"]) == beta, "literal beta")
                    full = list(colorings(evs, ees, dict(zip(frame, beta))))
                    root_indices = [evs.index(r) for r in roots]
                    accepted = {tuple(f[j] for j in root_indices) for f in full}
                    require(set(map(tuple, row["root_pairs"])) == accepted, "whole-edge joint oracle")
                    require(len(row["pairs"]) == 16, "pair coverage")
                    for j, pair in enumerate(row["pairs"]):
                        a, b = divmod(j, 4)
                        require(pair["pins"] == [a, b], "pair order")
                        status = (a, b) in accepted
                        require((pair["status"] == "nonempty") == status, "pair status")
                        pins = dict(zip(frame, beta)) | dict(zip(roots, (a, b)))
                        for key in ("joint_lift", "direct_lift"):
                            require(lift_ok(evs, ees, pins, pair[key]) if status else pair[key] is None, "full lift")
                    budgets = {}
                    for d, r in enumerate(roots):
                        factors = [{beta[frame.index(v)]} for e in ees if r in e
                                   for v in e if v in frame]
                        deficit = 0
                        for p in active:
                            if p["kind"] == "unary" and p["owners"] == [r]:
                                allowed = {pair[d] for pair, ok in relations[i][p["id"]].items() if ok}
                                forbidden = set(range(4)) - allowed
                                factors.append(forbidden)
                                deficit += len(p["contacts"][str(r)]) - len(forbidden)
                        union = set().union(*factors)
                        overlap = sum(map(len, factors)) - len(union)
                        available = set(range(4)) - union
                        s = row["sides"][str(r)]
                        require((s["D_u"], s["O_u"], set(s["E"])) == (deficit, overlap, available), "side budget")
                        budgets[r] = (deficit, overlap, available)
                    expected_capacity = []
                    for d, r in enumerate(roots):
                        s = roots[1-d]
                        missing = (["complete join rejects beta"] if accepted else [])
                        if not budgets[s][2]:
                            missing.append("E_s nonempty")
                        if missing:
                            expected_capacity.append({"r": r, "s": s, "status": "not triggered", "missing": missing})
                            continue
                        for b in sorted(budgets[s][2]):
                            banned, columns = set(), []
                            for p in active:
                                if p["kind"] != "mixed":
                                    continue
                                values = {a for a in range(4) if not relations[i][p["id"]][(a, b) if d == 0 else (b, a)]}
                                k = len(p["contacts"][str(r)])
                                require(len(values) <= k, "strict slack")
                                columns.append({"piece": p["id"], "k": k, "G_C_b": sorted(values), "delta_C": k-len(values)})
                                banned |= values
                            a_set = budgets[r][2]
                            require(a_set <= banned, "rejecting column cover")
                            delta = sum(x["delta_C"] for x in columns)
                            o = sum(len(x["G_C_b"]) for x in columns) - len(banned)
                            leak = len(banned - a_set)
                            terms = [budgets[r][0], budgets[r][1], delta, o, leak]
                            require(min(terms) >= 0 and sum(terms) == degree[r]-4, "capacity identity")
                            expected_capacity.append({"r": r, "s": s, "b": b, "chi": 0,
                                "A": sorted(a_set), "V": sorted(banned), "columns": columns,
                                "D_u": terms[0], "O_u": terms[1], "delta": delta, "o": o,
                                "lambda": leak, "lhs": sum(terms), "rhs": degree[r]-4,
                                "status": "triggered and holds", "missing": []})
                    require(expected_capacity == row["capacity"], "capacity record and coverage")
                    for c in expected_capacity:
                        group_counts[kind + "_capacity_" + c["status"]] += 1
                    group_counts[kind + "_root_pair_queries"] += 16
                    group_counts[kind + "_nonempty_fibres"] += len(accepted)
                    mask |= (1 << i) if accepted else 0
                require(mask == ev["sigma"], "complete Sigma")
                group_counts[kind + "_graphs"] += 1
            counts["graphs"] += 1
        domains[label] = dict(group_counts)
    result = {"status": "PASS", "BASE": BASE, "base_input_files": len(manifest["files"]),
              "manifest_files": len(listed), "checker_sha256": cert["checker_sha256"],
              "certificate_sha256": digest((DELIVERY / "results/certificate.json").read_bytes()),
              "domains": domains, "counterexamples": [],
              "method": "independent bit-domain full coloring enumeration; no N45-J import",
              "not_checked": ["S/U new claims", "arbitrary-size source proof", "Lean", "upstream enumeration completeness"]}
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
