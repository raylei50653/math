#!/usr/bin/env python3
"""Independent D9 NA54 checks: raw graph/rotation input; no producer imports.

Only id, vertices, edges and rotation are read from E4C certificates. All degrees,
components, colourings, contact relations, fibres, shields and all minimal q cores
are recomputed. The classifications deliberately distinguish a forbidden
antecedent with no instance from the corresponding necessary condition.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
B = frozenset(range(5))
FRAME = frozenset((min(i, (i + 1) % 5), max(i, (i + 1) % 5)) for i in B)
COLOURS = range(4)
SELECTED = (6, 4, 1)
T4 = (2, 5, 7, 8, 9)


def boundary_patterns():
    result = []
    for beta in itertools.product(COLOURS, repeat=5):
        if beta[0] != 0 or any(beta[a] == beta[b] for a, b in FRAME):
            continue
        largest = 0
        for c in beta:
            if c > largest + 1:
                break
            largest = max(largest, c)
        else:
            result.append(beta)
    assert len(result) == 10
    return tuple(result)


PATTERNS = boundary_patterns()


def adjacency(vertices, edges):
    result = {v: set() for v in vertices}
    for a, b in edges:
        result[a].add(b)
        result[b].add(a)
    return result


def components(vertices, adj):
    pending = set(vertices)
    result = []
    while pending:
        start = min(pending)
        pending.remove(start)
        stack, component = [start], {start}
        while stack:
            v = stack.pop()
            for u in adj[v] & pending:
                pending.remove(u)
                component.add(u)
                stack.append(u)
        result.append(frozenset(component))
    return result


def colourings(vertices, edges, pins, all_solutions=False):
    """MRV DFS on actual edges, with one common literal colour frame."""
    vertices = tuple(sorted(vertices))
    adj = adjacency(vertices, edges)
    assignment = dict(pins)
    if any(assignment[a] == assignment[b] for a, b in edges
           if a in assignment and b in assignment):
        return []
    solutions = []

    def visit():
        uncoloured = [v for v in vertices if v not in assignment]
        if not uncoloured:
            solutions.append(tuple(assignment[v] for v in vertices))
            return not all_solutions
        choices = []
        for v in uncoloured:
            available = tuple(c for c in COLOURS
                              if all(assignment.get(u) != c for u in adj[v]))
            if not available:
                return False
            choices.append((len(available), -len(adj[v]), v, available))
        _, _, v, available = min(choices)
        for c in available:
            assignment[v] = c
            if visit():
                del assignment[v]
                return True
            del assignment[v]
        return False

    visit()
    return solutions


def face_cycles(vertices, edges, rotation):
    """Restrict the recorded rotation to this actual embedded subgraph."""
    adj = adjacency(vertices, edges)
    rot = {v: [u for u in rotation[v] if u in adj[v]] for v in vertices}
    darts = {(a, b) for a, b in edges} | {(b, a) for a, b in edges}
    faces, face_of = [], {}
    while darts:
        first = min(darts)
        dart, cycle = first, []
        while True:
            assert dart in darts
            darts.remove(dart)
            face_of[dart] = len(faces)
            u, v = dart
            cycle.append(u)
            around = rot[v]
            dart = (v, around[(around.index(u) - 1) % len(around)])
            if dart == first:
                break
        faces.append(cycle)
    return faces, face_of, rot


def shield(vertices, edges, rotation, piece):
    kp = B | piece
    kept = tuple(e for e in edges if e[0] in kp and e[1] in kp)
    faces, face_of, rot = face_cycles(kp, kept, rotation)
    face_ids = set()
    for v in kp:
        for u in rotation[v]:
            if u in vertices - kp:
                around = rotation[v]
                index = around.index(u)
                # In this sector the first retained neighbour clockwise bounds
                # the same face as the deleted dart v->u.
                for distance in range(1, len(around) + 1):
                    neighbour = around[(index + distance) % len(around)]
                    if neighbour in rot[v]:
                        face_ids.add(face_of[(neighbour, v)])
                        break
    assert len(face_ids) == 1, (piece, face_ids)
    fid = next(iter(face_ids))
    face_edges = {tuple(sorted((faces[fid][i], faces[fid][(i + 1) % len(faces[fid])])))
                  for i in range(len(faces[fid]))}
    sigma = sorted(FRAME - face_edges)
    support = sorted({b for a, b in edges if a in piece and b in B}
                     | {a for a, b in edges if a in B and b in piece})
    return {"edges": [list(e) for e in sigma], "length": len(sigma),
            "support": support, "face": faces[fid]}


def short(support):
    return any(set(support) <= set(edge) for edge in FRAME)


def classify(instances, failures, missing):
    if failures:
        return {"status": "counterexample", "instances": instances, "failures": failures}
    if instances:
        return {"status": "triggered and holds", "instances": instances}
    return {"status": "not triggered", "instances": 0, "reason": missing}


def check_graph(source):
    identifier = source["id"]
    vertices = frozenset(source["vertices"])
    edges = tuple(sorted(tuple(sorted(e)) for e in source["edges"]))
    rotation = {int(v): list(order) for v, order in source["rotation"].items()}
    adj = adjacency(vertices, edges)
    internal = vertices - B
    roots = tuple(v for v in sorted(internal) if len(adj[v]) == 5)
    assert len(edges) == len(set(edges)) and not any(a == b for a, b in edges)
    assert FRAME <= set(edges)
    assert {e for e in edges if set(e) <= B} == FRAME
    assert len(roots) == 2 and roots[1] not in adj[roots[0]]
    assert all(len(adj[v]) == (5 if v in roots else 4) for v in internal)
    assert len(components(internal, adj)) == 1
    assert all(set(rotation[v]) == adj[v] and len(rotation[v]) == len(adj[v]) for v in vertices)
    faces, _, _ = face_cycles(vertices, edges, rotation)
    assert len(vertices) - len(edges) + len(faces) == 2
    assert any(len(f) == 5 and set(f) == B for f in faces)
    touch = sorted({b for v in internal for b in adj[v] & B})
    full_touch = set(touch) == B
    raw_pieces = components(internal - set(roots), adj)
    pieces = []
    for i, pp in enumerate(raw_pieces):
        contacts = {r: sorted(adj[r] & pp) for r in roots}
        owners = [r for r in roots if contacts[r]]
        assert owners
        support = sorted({b for v in pp for b in adj[v] & B})
        one_sided = len(components(internal - pp, adj)) == 1
        p = {"id": f"P{i}", "vertices": sorted(pp), "owners": owners,
             "contacts": contacts, "contact_order": sorted(set().union(*(set(c) for c in contacts.values()))),
             "support": support, "incidences": [len(contacts[r]) for r in roots],
             "kind": "mixed" if len(owners) == 2 else "unary", "one_sided": one_sided,
             "attachments": [list(e) for e in edges if bool(set(e) & pp) and bool(set(e) & B)],
             "internal_edges": [list(e) for e in edges if set(e) <= pp], "rows": []}
        if one_sided:
            p["shield"] = shield(vertices, edges, rotation, pp)
        for beta in PATTERNS:
            # Enumerate the original piece plus its actual boundary attachments;
            # root constraints are imposed on full tuples only afterwards.
            local_edges = tuple(e for e in edges if set(e) <= pp | B)
            local_vertices = sorted(pp | B)
            solutions = colourings(local_vertices, local_edges, dict(enumerate(beta)), True)
            positions = {v: j for j, v in enumerate(local_vertices)}
            lifts = [tuple(s[positions[v]] for v in sorted(pp)) for s in solutions]
            tuples = sorted({tuple(s[positions[v]] for v in p["contact_order"]) for s in solutions})
            fibres = []
            for pins in itertools.product(COLOURS, repeat=2):
                valid = [list(lift) for lift in lifts if all(
                    lift[sorted(pp).index(v)] != pins[j]
                    for j, r in enumerate(roots) for v in contacts[r])]
                fibres.append({"pins": list(pins), "lifts": valid})
            p["rows"].append({"beta": list(beta), "tuples": [list(t) for t in tuples],
                              "lifts": [list(t) for t in lifts], "fibres": fibres})
        pieces.append(p)
    mixed = [p for p in pieces if p["kind"] == "mixed"]
    unary = [p for p in pieces if p["kind"] == "unary"]
    m, u = len(mixed), len(unary)

    @lru_cache(None)
    def accepts(graph_vertices, graph_edges, index):
        solutions = colourings(graph_vertices, graph_edges, dict(enumerate(PATTERNS[index])))
        return solutions[0] if solutions else None

    full_rows = []
    for index, beta in enumerate(PATTERNS):
        # Independent whole-graph enumerations for each literal root pair.
        root_pairs = []
        for pins in itertools.product(COLOURS, repeat=2):
            solution = colourings(vertices, edges, dict(enumerate(beta)) | dict(zip(roots, pins)))
            actual = bool(solution)
            side = all(beta[b] != pins[j] for j, r in enumerate(roots) for b in adj[r] & B)
            joined = side and all(p["rows"][index]["fibres"][4 * pins[0] + pins[1]]["lifts"] for p in pieces)
            assert actual == bool(joined), (identifier, index, pins)
            if actual:
                root_pairs.append({"pins": list(pins), "witness": list(solution[0])})
        full_rows.append({"beta": list(beta), "accepted": bool(root_pairs), "root_pairs": root_pairs})
    sigma = sum(1 << i for i, row in enumerate(full_rows) if row["accepted"])
    assert all(full_rows[i]["accepted"] for i in T4)
    rejected = [i for i, row in enumerate(full_rows) if not row["accepted"]]
    deletions = []
    for edge in edges:
        if edge in FRAME:
            continue
        ee = tuple(e for e in edges if e != edge)
        gains = {i: list(accepts(tuple(sorted(vertices)), ee, i)) for i in rejected
                 if accepts(tuple(sorted(vertices)), ee, i) is not None}
        assert gains, (identifier, edge, "not critical")
        deletions.append({"edge": list(edge), "new_rows": gains})

    def peel(graph_edges):
        graph_vertices = set(B) | set(itertools.chain.from_iterable(graph_edges))
        while True:
            aa = adjacency(graph_vertices, graph_edges)
            discard = {v for v in graph_vertices - B if len(aa[v]) < 4}
            if not discard:
                return tuple(sorted(graph_vertices)), tuple(sorted(graph_edges))
            graph_vertices -= discard
            graph_edges = tuple(e for e in graph_edges if not set(e) & discard)

    @lru_cache(None)
    def all_cores(graph_edges, index):
        vv, ee = peel(graph_edges)
        if ee != graph_edges:
            return all_cores(ee, index)
        children = set()
        removable = False
        for edge in ee:
            if edge in FRAME:
                continue
            reduced = tuple(e for e in ee if e != edge)
            if accepts(vv, reduced, index) is None:
                removable = True
                children.update(all_cores(reduced, index))
        return frozenset(children if removable else {(vv, ee)})

    core_rows = []
    core44 = []
    for index in rejected:
        cores = []
        for vv, ee in sorted(all_cores(edges, index)):
            aa = adjacency(vv, ee)
            assert accepts(vv, ee, index) is None
            critical_witnesses = []
            for edge in ee:
                if edge not in FRAME:
                    witness = accepts(vv, tuple(e for e in ee if e != edge), index)
                    assert witness is not None
                    critical_witnesses.append({"edge": list(edge), "witness": list(witness)})
            c = {"vertices": list(vv), "edges": [list(e) for e in ee],
                 "root_degrees": [len(aa[r]) if r in aa else 0 for r in roots],
                 "critical_witnesses": critical_witnesses}
            cores.append(c)
            if c["root_degrees"] == [4, 4]:
                core44.append(c)
        core_rows.append({"index": index, "cores": cores})

    checks = {}
    checks["N-empty-separating"] = classify(sum(not p["support"] for p in mixed),
        [p["id"] for p in mixed if not p["support"]], "No mixed piece has empty actual support.")
    empty_with_path = []
    empty_appendages = []
    for p in mixed:
        if p["support"]:
            continue
        outside = vertices - set(p["vertices"])
        outside_components = components(outside, adj)
        if any(set(roots) <= component for component in outside_components):
            empty_with_path.append(p)
        else:
            empty_appendages.append(p)
    checks["N-empty-external-path"] = classify(len(empty_with_path),
        [p["id"] for p in empty_with_path],
        "No empty-support mixed with an outside original root path exists.")
    checks["N-empty-appendage"] = classify(len(empty_appendages),
        [p["id"] for p in empty_appendages],
        "No empty-support mixed separating an unframed appendage exists.")
    checks["N-theta"] = classify(int(m >= 3),
        ["m >= 3 but all actual supports nonempty"] if m >= 3 and all(p["support"] for p in mixed) else [],
        "m < 3: no embedded theta antecedent from three mixed pieces.")
    path_trigger = m == 1 and mixed[0]["incidences"] == [2, 2] and bool(core44)
    path_failures = []
    if path_trigger:
        p = mixed[0]
        pp = set(p["vertices"])
        aa = adjacency(pp, p["internal_edges"])
        if len(pp) != 4 or sorted(len(aa[v]) for v in pp) != [1, 1, 2, 2]:
            path_failures.append("Original mixed is not the four-point path")
        if set(p["contacts"][roots[0]]) & set(p["contacts"][roots[1]]):
            path_failures.append("Original root triangles share a contact")
        for r in roots:
            x, y = p["contacts"][r]
            if y not in aa[x] or sorted(len(aa[v]) for v in (x, y)) != [1, 2]:
                path_failures.append({"root": r, "reason": "Root contacts do not form one end of the path"})
        for v in pp:
            if len(adj[v] & B) != (2 if len(aa[v]) == 1 else 1):
                path_failures.append({"vertex": v, "reason": "Wrong actual boundary attachment count"})
    checks["N1-22-44-path"] = classify(int(path_trigger), path_failures,
        "No sole mixed with incidences (2,2) and two-root (4,4) minimal q core.")
    checks["N1-22-44"] = classify(int(m == 1 and mixed[0]["incidences"] == [2, 2] and bool(core44)
        and all(i in rejected for i in SELECTED)), ["Forbidden N1-22-44 source"] if m == 1
        and mixed[0]["incidences"] == [2, 2] and core44 and all(i in rejected for i in SELECTED) else [],
        "No (4,4) core, and selected three rows are not all rejected.")
    diagonal_pieces = [p for p in mixed if full_touch and p["one_sided"] and short(p["support"])]
    diagonal_failures = [{"piece": p["id"], "index": index, "pin": a}
        for p in diagonal_pieces for index in range(10) for a in COLOURS
        if not p["rows"][index]["fibres"][5 * a]["lifts"]]
    checks["N-diagonal"] = classify(len(diagonal_pieces) * 40, diagonal_failures,
        "No full-B-touch one-sided short mixed.")
    all_short = full_touch and all(p["one_sided"] and short(p["support"]) for p in mixed)
    checks["N2-short-no-unary"] = classify(int(m == 2 and u == 0 and all_short),
        [i for i in (0, 1, 3, 4, 6) if not full_rows[i]["accepted"]] if m == 2 and u == 0 and all_short else [],
        "No m=2, all-short, no-unary, full-B-touch control.")
    intersection_failures = []
    if all_short:
        for index in rejected:
            domains = []
            beta = PATTERNS[index]
            for r in roots:
                domain = {a for a in COLOURS if all(beta[b] != a for b in adj[r] & B)}
                for p in unary:
                    if r in p["owners"]:
                        j = roots.index(r)
                        domain &= {a for a in COLOURS if any(
                            p["rows"][index]["fibres"][4 * a + b if j == 0 else 4 * b + a]["lifts"]
                            for b in COLOURS)}
                domains.append(domain)
            if domains[0] & domains[1]:
                intersection_failures.append({"index": index, "intersection": sorted(domains[0] & domains[1])})
    checks["N2-short-side-intersection"] = classify(len(rejected) if all_short else 0,
        intersection_failures, "Not all original mixed pieces satisfy the local N-diagonal premises.")
    budget_trigger = m == 2 and full_touch
    budget_failures = []
    if budget_trigger:
        long_mixed = [p for p in mixed if not short(p["support"])]
        short_pairs = [p for p in mixed if len(p["support"]) == 2 and short(p["support"])]
        if len(long_mixed) + u > 2:
            budget_failures.append("long mixed + unary count exceeds 2")
        if sum(p["shield"]["length"] for p in long_mixed + unary) + len(short_pairs) > 5:
            budget_failures.append("shield sum exceeds 5")
        if any(p["shield"]["length"] != (1 if len(p["support"]) == 2 else 0)
               for p in mixed if short(p["support"])):
            budget_failures.append("short mixed shield length disagrees")
    checks["N2-shield-budget"] = classify(int(budget_trigger), budget_failures,
        "m != 2 or full B-touch is absent.")
    checks["nonadjacent-m<=2"] = classify(1, ["m > 2"] if m > 2 else [], "")
    checks["N3-exclusion"] = classify(int(m >= 3), ["critical source has m >= 3"] if m >= 3 else [],
        "No source has m >= 3; the excluded antecedent is untriggered.")
    checks["full-contact-join"] = classify(160, [], "")
    checks["minimal-core-saturation"] = classify(sum(len(r["cores"]) for r in core_rows),
        [{"index": r["index"], "piece": p["id"]} for r in core_rows for c in r["cores"]
         for p in pieces if set(p["vertices"]) & set(c["vertices"]) and not (
             set(p["vertices"]) <= set(c["vertices"]) and all(
                 list(e) in c["edges"] for e in edges if set(e) & set(p["vertices"])))], "")
    core44_failures = []
    for core in core44:
        vv, ee = set(core["vertices"]), [tuple(e) for e in core["edges"]]
        aa = adjacency(vv, ee)
        retained = [p for p in mixed if set(p["vertices"]) <= vv]
        if len(retained) != 1:
            core44_failures.append("The (4,4) core does not retain exactly one original mixed")
            continue
        p = retained[0]
        if any(len(p["contacts"][r]) > 2 for r in roots):
            core44_failures.append("A retained mixed has more than two contacts at a root")
        for r in roots:
            cc = p["contacts"][r]
            if len(cc) == 2 and cc[1] not in aa[cc[0]]:
                core44_failures.append({"root": r, "reason": "Two original contacts do not form a triangle"})
        if p["incidences"] == [2, 2]:
            pp = set(p["vertices"])
            jj = adjacency(pp, p["internal_edges"])
            if len(pp) != 4 or sorted(len(jj[v]) for v in pp) != [1, 1, 2, 2]:
                core44_failures.append("Double-triangle mixed is not the four-point original path")
            if set(p["contacts"][roots[0]]) & set(p["contacts"][roots[1]]):
                core44_failures.append("Double-triangle contacts overlap")
            if vv - B != pp | set(roots):
                core44_failures.append("Double-triangle core has extra retained tails")
    checks["N1-44-core-identity"] = classify(len(core44), core44_failures,
        "No two-root (4,4) q core.")
    checks["selected-three-row-premise"] = classify(int(all(i in rejected for i in SELECTED)), [],
        "q0, q1, q3 are not simultaneously rejected; no three-row exclusion is calibrated.")
    return {"id": identifier, "vertices": sorted(vertices), "edges": [list(e) for e in edges],
            "roots": list(roots), "rotation": rotation, "faces": faces, "touch": touch,
            "sigma": sigma, "rejected_indices": rejected, "m": m, "u": u,
            "pieces": pieces, "full_rows": full_rows, "edge_criticality": deletions,
            "all_minimal_q_cores": core_rows, "checks": checks}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", "--repo-root", dest="repo_root", type=Path, default=ROOT,
                        help="Repository root when running a copy outside the audit directory")
    parser.add_argument("--output", type=Path, default=HERE / "e4_controls.json")
    args = parser.parse_args()
    root = args.repo_root.resolve()
    sources = sorted((root / "artifacts/c5_excess_two_e4c/controls").glob("NA*.json"))
    assert len(sources) == 54
    graphs = []
    source_hashes = {}
    for path in sources:
        raw = path.read_bytes()
        source_hashes[str(path.relative_to(root))] = hashlib.sha256(raw).hexdigest()
        data = json.loads(raw)
        graphs.append(check_graph({key: data[key] for key in ("id", "vertices", "edges", "rotation")}))
    totals = {name: dict(Counter(graph["checks"][name]["status"] for graph in graphs))
              for name in graphs[0]["checks"]}
    result = {"schema": "d9-independent-e4-na54-v1", "baseline": "b2ca4520da50c9d2898ac6f8f966ac25df3f9609",
              "input_fields": ["id", "vertices", "edges", "rotation"], "imports_producer_decision_logic": False,
              "source_sha256": source_hashes, "patterns": PATTERNS, "graphs": graphs,
              "totals": totals, "core_type_counts": dict(Counter(
                  "-".join(map(str, c["root_degrees"])) for g in graphs
                  for r in g["all_minimal_q_cores"] for c in r["cores"]))}
    encoded = (json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
    output = args.output
    if args.check:
        assert output.read_bytes() == encoded, "independent certificate byte mismatch"
    else:
        with output.open("xb") as stream:
            stream.write(encoded)
    print(json.dumps({"graphs": len(graphs), "totals": totals, "core_type_counts": result["core_type_counts"],
                      "sha256": hashlib.sha256(encoded).hexdigest(), "bytes": len(encoded)}, sort_keys=True))
    assert not any(g["checks"][name]["status"] == "counterexample" for g in graphs for name in totals)


if __name__ == "__main__":
    main()
