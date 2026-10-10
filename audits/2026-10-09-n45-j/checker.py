#!/usr/bin/env python3
"""N45-J: independent exact tuple joins; fixed controls, never a graph search.

No project module is imported. Local relations exhaust all piece colourings;
the independent whole-graph oracle uses MRV backtracking on original edges.
--check only reads; generation reserves a new output directory exclusively.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

BASE = "dc8e9aa7d6fccb51f63d30aa3f9c132296d44744"
HOME = Path(__file__).resolve().parent
COL = frozenset(range(4))
PATTERNS = tuple(tuple(map(int, s)) for s in (
    "01012", "01021", "01023", "01201", "01202",
    "01203", "01212", "01213", "01231", "01232"))
TARGET_ROWS = (6, 4, 1)
T4 = (2, 5, 7, 8, 9)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def order(v):
    return (0, v) if isinstance(v, int) else (1, str(v))


def sortedv(vs):
    return sorted(vs, key=order)


def edge(u, v):
    return tuple(sortedv((u, v)))


def sortededges(es):
    return sorted(set(es), key=lambda e: (order(e[0]), order(e[1])))


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + "\n").encode()


def neighbors(vertices, edges):
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def components(vertices, edges):
    adj = neighbors(vertices, [e for e in edges if set(e) <= set(vertices)])
    unseen, result = set(vertices), []
    while unseen:
        todo, found = [min(unseen, key=order)], set()
        while todo:
            v = todo.pop()
            if v in found:
                continue
            found.add(v)
            todo.extend(adj[v] - found)
        unseen -= found
        result.append(sortedv(found))
    return result


def first_coloring(vertices, edges, pins):
    """Whole-graph oracle: direct edges, no relations or projected sets."""
    adj, f = neighbors(vertices, edges), dict(pins)
    need(set(f) <= set(vertices), "pins outside graph")
    if any(f[u] == f[v] for u, v in edges if u in f and v in f):
        return None

    def visit():
        if len(f) == len(vertices):
            return [f[v] for v in vertices]
        candidates = []
        for v in vertices:
            if v not in f:
                options = sorted(COL - {f[w] for w in adj[v] if w in f})
                candidates.append((len(options), order(v), v, options))
        _, _, v, options = min(candidates)
        for c in options:
            f[v] = c
            found = visit()
            del f[v]
            if found is not None:
                return found
        return None

    return visit()


def validate_lift(vertices, edges, pins, lift):
    need(len(lift) == len(vertices), "wrong lift length")
    f = dict(zip(vertices, lift))
    need(all(c in COL for c in lift), "invalid colour")
    need(all(f[v] == c for v, c in pins.items()), "lift changes pins")
    need(all(f[u] != f[v] for u, v in edges), "lift violates an edge")


def walk_faces(vertices, edges, rotation):
    adj = neighbors(vertices, edges)
    need(set(rotation) == set(vertices), "rotation vertex set")
    for v in vertices:
        need(len(rotation[v]) == len(set(rotation[v])) and
             set(rotation[v]) == adj[v], "rotation neighborhood")
    unseen = {(u, v) for e in edges for u, v in (e, e[::-1])}
    faces, face_of = [], {}
    while unseen:
        start = min(unseen, key=lambda e: (order(e[0]), order(e[1])))
        dart, face = start, []
        while True:
            need(dart in unseen, "rotation face repeats a dart")
            unseen.remove(dart)
            face_of[dart] = len(faces)
            u, v = dart
            face.append(u)
            ns = rotation[v]
            dart = (v, ns[(ns.index(u) + 1) % len(ns)])
            if dart == start:
                break
        faces.append(face)
    return faces, face_of


def frame_edges(frame):
    return {edge(frame[i], frame[(i + 1) % 5]) for i in range(5)}


def normalize_graph(raw):
    vertices = sortedv(raw["vertices"])
    need(len(vertices) == len(set(vertices)), "duplicate vertex")
    es = [edge(*e) for e in raw["edges"]]
    need(len(es) == len(set(es)) and all(u != v for u, v in es), "not simple")
    edges = sortededges(es)
    need(all(set(e) <= set(vertices) for e in edges), "edge outside vertices")
    frame = raw.get("frame", list(range(5)))
    need(len(frame) == 5 and len(set(frame)) == 5 and set(frame) <= set(vertices), "frame")
    need({e for e in edges if set(e) <= set(frame)} == frame_edges(frame), "not induced C5")
    adj = neighbors(vertices, edges)
    roots = raw.get("roots", [v for v in vertices if v not in frame and len(adj[v]) == 5])
    need(len(roots) == 2 and len(set(roots)) == 2 and
         all(r in vertices and r not in frame for r in roots), "two named roots required")
    need(edge(*roots) not in edges, "N45-J requires chi=0")
    need(all(len(adj[r]) == 5 for r in roots), "original roots must have degree5")
    need(all(len(adj[v]) == 4 for v in vertices if v not in frame and v not in roots),
         "original nonroot private degree must be4; omit isolated private vertices explicitly")
    rotation = None
    disk = {"status": "not triggered", "missing": ["original rotation"]}
    if "rotation" in raw:
        # JSON object keys are strings; map them to the actual named vertices.
        rotation = {v: raw["rotation"][str(v)] for v in vertices}
        faces, _ = walk_faces(vertices, edges, rotation)
        need(len(components(vertices, edges)) == 1, "disk graph disconnected")
        need(len(vertices) - len(edges) + len(faces) == 2, "rotation not sphere")
        outer = [f for f in faces if len(f) == 5 and set(f) == set(frame)]
        need(len(outer) == 1, "unique C5 outer face")
        need({edge(outer[0][i], outer[0][(i + 1) % 5]) for i in range(5)} == frame_edges(frame),
             "wrong outer boundary")
        disk = {"status": "triggered and holds", "faces": faces, "outer": outer[0], "euler": 2}
    return {"id": raw["id"], "vertices": vertices, "edges": edges,
            "frame": frame, "roots": roots, "rotation": rotation, "disk": disk}


def reconstruct_pieces(g):
    vs, es, frame, roots = g["vertices"], g["edges"], g["frame"], g["roots"]
    adj = neighbors(vs, es)
    pieces = []
    for i, pv in enumerate(components(set(vs) - set(frame) - set(roots), es)):
        contacts = {str(r): sortedv(set(pv) & adj[r]) for r in roots}
        owners = [r for r in roots if contacts[str(r)]]
        need(owners, "root-free component is outside the N45-J interface")
        distinct = sortedv({v for cs in contacts.values() for v in cs})
        shared = sortedv(set(contacts[str(roots[0])]) & set(contacts[str(roots[1])]))
        attachments = [e for e in es if (e[0] in pv and e[1] in frame) or
                       (e[1] in pv and e[0] in frame)]
        internal = [e for e in es if set(e) <= set(pv)]
        bridges = [e for e in internal if len(components(pv, [x for x in internal if x != e])) > 1]
        hminus = set(vs) - set(frame) - set(pv)
        p = {"id": "P" + str(i), "vertices": pv, "kind": "mixed" if len(owners) == 2 else "unary",
             "owners": owners, "contacts": contacts, "contact_order": distinct,
             "shared_contacts": shared, "internal_edges": internal, "original_bridges": bridges,
             "attachments": attachments, "support": sortedv(set(frame) & {v for e in attachments for v in e}),
             "incidences": [len(contacts[str(r)]) for r in roots],
             "one_sided": len(components(hminus, es)) == 1}
        if g["rotation"] is not None and p["support"]:
            kv = sortedv(set(frame) | set(pv))
            ke = [e for e in es if set(e) <= set(kv)]
            kr = {v: [w for w in g["rotation"][v] if w in kv] for v in kv}
            faces, face_of = walk_faces(kv, ke, kr)
            containing = set()
            for v in kv:
                ring = g["rotation"][v]
                for j, w in enumerate(ring):
                    if w in kv:
                        continue
                    k = (j - 1) % len(ring)
                    while ring[k] not in kv:
                        k = (k - 1) % len(ring)
                    containing.add(face_of[(ring[k], v)])
            if p["one_sided"]:
                need(len(containing) == 1, "one-sided outside occupies multiple K_P faces")
                outside_face = faces[next(iter(containing))]
                boundary = {edge(outside_face[j], outside_face[(j + 1) % len(outside_face)])
                            for j in range(len(outside_face))}
                p["original_shield_edges"] = sortededges(frame_edges(frame) - boundary)
                p["outside_face"] = outside_face
        pieces.append(p)
    return pieces


def local_relation(g, p, beta):
    """Enumerate full original P lifts before looking at either root pin."""
    pv, es, frame = p["vertices"], g["edges"], g["frame"]
    selected = set(pv) | set(frame)
    constraints = [e for e in es if set(e) <= selected]
    fixed = dict(zip(frame, beta))
    tuples = {}
    for colors in product(range(4), repeat=len(pv)):
        f = fixed | dict(zip(pv, colors))
        if all(f[u] != f[v] for u, v in constraints):
            t = tuple(f[v] for v in p["contact_order"])
            tuples.setdefault(t, []).append(list(colors))
    records = [{"tuple": list(t), "lifts": tuples[t]} for t in sorted(tuples)]
    fibres = []
    for a, b in product(range(4), repeat=2):
        pins = dict(zip(g["roots"], (a, b)))
        ids = [i for i, t in enumerate(records)
               if all(t["tuple"][p["contact_order"].index(v)] != pins[r]
                      for r in p["owners"] for v in p["contacts"][str(r)])]
        fibres.append({"pins": [a, b], "tuple_indices": ids})
    return {"tuples": records, "fibres": fibres}


def side_budget(g, active, relations, beta, root, removed_spoke):
    factors, unaries = [], []
    for e in g["edges"]:
        if root in e and e != removed_spoke:
            v = e[0] if e[1] == root else e[1]
            if v in g["frame"]:
                factors.append({"id": ["spoke", root, v], "F": [beta[g["frame"].index(v)]]})
    for p in active:
        if p["kind"] == "unary" and p["owners"] == [root]:
            rel = relations[p["id"]]
            available = set()
            coordinate = 0 if root == g["roots"][0] else 1
            for fibre in rel["fibres"]:
                if fibre["tuple_indices"]:
                    available.add(fibre["pins"][coordinate])
            f = COL - available
            need(rel["tuples"], "empty unary local relation violates strict slack")
            n = len(p["contacts"][str(root)])
            need(len(f) <= n, "unary deficit negative")
            factors.append({"id": ["unary", p["id"]], "F": sorted(f)})
            unaries.append({"piece": p["id"], "incidence": n, "F": sorted(f), "D": n - len(f)})
    union = set().union(*(set(x["F"]) for x in factors))
    return {"factors": factors, "unaries": unaries, "D_u": sum(x["D"] for x in unaries),
            "O_u": sum(len(x["F"]) for x in factors) - len(union), "E": sorted(COL - union)}


def capacity(g, active, relations, sides, accepted, degrees):
    records = []
    for direction, root in enumerate(g["roots"]):
        other = g["roots"][1 - direction]
        own, opposing = sides[str(root)], sides[str(other)]
        missing = []
        if accepted:
            missing.append("complete join rejects beta")
        if not opposing["E"]:
            missing.append("E_s nonempty")
        if missing:
            records.append({"r": root, "s": other, "status": "not triggered", "missing": missing})
            continue
        for b in opposing["E"]:
            columns, union = [], set()
            for p in active:
                if p["kind"] != "mixed":
                    continue
                column = set()
                for a in range(4):
                    pair = [a, b] if direction == 0 else [b, a]
                    fibre = relations[p["id"]]["fibres"][pair[0] * 4 + pair[1]]
                    if not fibre["tuple_indices"]:
                        column.add(a)
                k = len(p["contacts"][str(root)])
                need(len(column) <= k, "mixed strict slack / deficit violation")
                columns.append({"piece": p["id"], "k": k, "G_C_b": sorted(column), "delta_C": k - len(column)})
                union |= column
            a_set = set(own["E"])
            need(a_set <= union, "rejected join does not cover A")
            delta = sum(x["delta_C"] for x in columns)
            overlap = sum(len(x["G_C_b"]) for x in columns) - len(union)
            leakage = len(union - a_set)
            terms = [own["D_u"], own["O_u"], delta, overlap, leakage]
            need(all(x >= 0 for x in terms), "capacity term negative")
            rhs = degrees[root] - 4
            need(sum(terms) == rhs, "B-C2 chi=0 equality fails")
            records.append({"r": root, "s": other, "b": b, "chi": 0,
                            "A": sorted(a_set), "V": sorted(union), "columns": columns,
                            "D_u": terms[0], "O_u": terms[1], "delta": delta, "o": overlap,
                            "lambda": leakage, "lhs": sum(terms), "rhs": rhs,
                            "status": "triggered and holds", "missing": []})
    return records


def evaluate(g, pieces, row_relations, derivative=None):
    absent_piece = derivative.get("piece") if derivative else None
    cut = tuple(derivative["edge"]) if derivative and derivative["kind"] == "spoke" else None
    active = [p for p in pieces if p["id"] != absent_piece]
    removed = next((set(p["vertices"]) for p in pieces if p["id"] == absent_piece), set())
    vs = [v for v in g["vertices"] if v not in removed]
    es = [e for e in g["edges"] if e != cut and not (set(e) & removed)]
    degrees = {v: len(ws) for v, ws in neighbors(vs, es).items()}
    if derivative:
        drop = [5 - degrees[r] for r in g["roots"]]
        need(sorted(drop) == [0, 1], "derivative does not remove exactly one root incidence")
        need(all(degrees[v] == 4 for v in vs if v not in g["frame"] and v not in g["roots"]),
             "derivative damages a retained degree4 piece")
    rows = []
    for i, beta in enumerate(PATTERNS):
        relations = row_relations[i]
        sides = {str(r): side_budget(g, active, relations, beta, r, cut) for r in g["roots"]}
        pairs = []
        for a, b in product(range(4), repeat=2):
            pair, joined = [a, b], None
            if a in sides[str(g["roots"][0])]["E"] and b in sides[str(g["roots"][1])]["E"] and all(
                    relations[p["id"]]["fibres"][a * 4 + b]["tuple_indices"] for p in active):
                f = dict(zip(g["frame"], beta)) | dict(zip(g["roots"], (a, b)))
                for p in active:
                    rel = relations[p["id"]]
                    ti = rel["fibres"][a * 4 + b]["tuple_indices"][0]
                    f.update(zip(p["vertices"], rel["tuples"][ti]["lifts"][0]))
                joined = [f[v] for v in vs]
            pins = dict(zip(g["frame"], beta)) | dict(zip(g["roots"], (a, b)))
            direct = first_coloring(vs, es, pins)
            need((joined is None) == (direct is None), f"join/oracle disagreement {g['id']} row{i} pair{pair}")
            if joined is not None:
                validate_lift(vs, es, pins, joined)
                validate_lift(vs, es, pins, direct)
            pairs.append({"pins": pair, "status": "nonempty" if joined is not None else "empty",
                          "joint_lift": joined, "direct_lift": direct})
        accepted = [x["pins"] for x in pairs if x["status"] == "nonempty"]
        rows.append({"index": i, "beta": list(beta), "sides": sides, "pairs": pairs,
                     "root_pairs": accepted,
                     "capacity": capacity(g, active, relations, sides, accepted, degrees)})
    return {"derivative": derivative, "vertices": vs, "edges": es,
            "root_degrees": [degrees[r] for r in g["roots"]],
            "epsilon": sum(max(degrees[v] - 4, 0) for v in vs if v not in g["frame"]),
            "active_pieces": [p["id"] for p in active],
            "sigma": sum(1 << r["index"] for r in rows if r["root_pairs"]), "rows": rows}


def units(g, pieces):
    result = []
    for root in g["roots"]:
        for e in g["edges"]:
            if root in e and any(v in g["frame"] for v in e):
                result.append({"kind": "spoke", "root": root, "edge": list(e)})
    for p in pieces:
        if p["kind"] == "unary" and sum(p["incidences"]) == 1:
            result.append({"kind": "unary", "root": p["owners"][0], "piece": p["id"],
                           "removed_vertices": p["vertices"], "original_support": p["support"]})
    return result


def graph_mask(vertices, edges, frame):
    lifts = [first_coloring(vertices, edges, dict(zip(frame, beta))) for beta in PATTERNS]
    return sum(1 << i for i, f in enumerate(lifts) if f is not None), lifts


def original_coverage(g, pieces, original):
    deletions = []
    for e in g["edges"]:
        if e in frame_edges(g["frame"]):
            continue
        es = [x for x in g["edges"] if x != e]
        mask, lifts = graph_mask(g["vertices"], es, g["frame"])
        gained = [i for i in range(10) if mask & (1 << i) and not original["sigma"] & (1 << i)]
        witnesses = []
        for i in gained:
            validate_lift(g["vertices"], es, dict(zip(g["frame"], PATTERNS[i])), lifts[i])
            witnesses.append({"index": i, "lift": lifts[i]})
        deletions.append({"edge": e, "sigma": mask, "gained": gained, "witnesses": witnesses})
    critical = all(x["gained"] for x in deletions)
    root_deletions = []
    for r in g["roots"]:
        vs = [v for v in g["vertices"] if v != r]
        es = [e for e in g["edges"] if r not in e]
        mask, lifts = graph_mask(vs, es, g["frame"])
        root_deletions.append({"root": r, "vertices": vs, "sigma": mask, "row_lifts": lifts})
    flags = {"finite_simple_induced_C5": True, "disk": g["disk"]["status"] == "triggered and holds",
             "Sigma_critical": critical, "epsilon2": original["epsilon"] == 2,
             "nonadjacent_degree5_roots": original["root_degrees"] == [5, 5],
             "other_effective_private_degree4": True,
             "N2": sum(p["kind"] == "mixed" for p in pieces) == 2,
             "T4_all_accepted": all(original["sigma"] & (1 << i) for i in T4),
             "specified_triple_rejected": all(not original["sigma"] & (1 << i) for i in TARGET_ROWS),
             "root_deletions_all_accepted": all(x["sigma"] == 1023 for x in root_deletions)}
    # Transport the whole frame through each D5 permutation; never components separately.
    masks = []
    for flip in (1, -1):
        for shift in range(5):
            transported = [g["frame"][(shift + flip * i) % 5] for i in range(5)]
            mask, _ = graph_mask(g["vertices"], g["edges"], transported)
            masks.append({"shift": shift, "orientation": flip, "frame": transported, "sigma": mask})
    flags["complete_933_941_or_whole_D5_image"] = any(x["sigma"] in (933, 941) for x in masks)
    missing = [name for name, value in flags.items() if not value]
    return {"flags": flags, "full_target": {"status": "triggered and holds" if not missing else "not triggered",
                                            "missing": missing},
            "whole_graph_D5_masks": masks, "nonframe_deletions": deletions,
            "root_deletions": root_deletions}


def collisions(g, pieces, row_relations):
    records = []
    counts = Counter()
    for i, relations in enumerate(row_relations):
        for p in pieces:
            rel = relations[p["id"]]
            tuples = {tuple(x["tuple"]) for x in rel["tuples"]}
            marginal = [sorted({t[j] for t in tuples}) for j in range(len(p["contact_order"]))]
            false = [list(t) for t in product(*marginal) if t not in tuples]
            if false:
                counts["tuple_vs_marginal_rows"] += 1
                records.append({"kind": "tuple_vs_marginal", "piece": p["id"], "index": i,
                                "contact_order": p["contact_order"], "marginals": marginal,
                                "false_tuple": false[0], "relation_reference": [i, p["id"]]})
            # Deliberately wrong diagnostic: the two sides may choose different
            # full tuples, losing the single shared colouring. Never used by join.
            if p["kind"] == "mixed":
                for a, b in product(range(4), repeat=2):
                    side_ok = []
                    chosen = []
                    for r, c in zip(g["roots"], (a, b)):
                        ids = [j for j, t in enumerate(rel["tuples"])
                               if all(t["tuple"][p["contact_order"].index(v)] != c for v in p["contacts"][str(r)])]
                        side_ok.append(bool(ids))
                        chosen.append(ids[0] if ids else None)
                    if all(side_ok) and not rel["fibres"][a * 4 + b]["tuple_indices"]:
                        counts["independent_side_tuple_false_pairs"] += 1
                        records.append({"kind": "shared_coordinate" if p["shared_contacts"] else "independent_side_tuple",
                                        "piece": p["id"], "index": i, "pins": [a, b],
                                        "shared_contacts": p["shared_contacts"], "incompatible_side_tuple_indices": chosen,
                                        "relation_reference": [i, p["id"]]})
    return {"counts": dict(counts), "records": records,
            "interpretation": "diagnostic false positives from actual original relations; no relation is modified"}


def compare_saved(raw, pieces, relations, original, derivatives):
    need(raw["m"] == sum(p["kind"] == "mixed" for p in pieces), "saved m drift")
    need(raw["u"] == sum(p["kind"] == "unary" for p in pieces), "saved u drift")
    need(raw["sigma"] == original["sigma"], "saved Sigma disagreement")
    for p, saved in zip(pieces, raw["pieces"]):
        need(p["id"] == saved["id"], "saved piece identity")
        for field in ("vertices", "contacts", "contact_order", "support", "owners", "incidences", "kind", "one_sided"):
            need(p[field] == saved[field], "saved piece metadata disagreement: " + field)
        for field in ("attachments", "internal_edges"):
            need(p[field] == [tuple(x) for x in saved[field]], "saved edges disagree")
        if "original_shield_edges" in p:
            need(p["original_shield_edges"] == [tuple(x) for x in saved["shield"]["edges"]], "saved original shield disagree")
        for i, computed in enumerate(relations):
            got, old = computed[p["id"]], saved["rows"][i]
            need(got["tuples"] == old["tuples"], "saved complete tuples/full lifts disagree")
            need(got["fibres"] == old["fibres"], "saved 16 fibres disagree")
    need(len(pieces) == len(raw["pieces"]), "saved piece count disagreement")
    for row, old in zip(original["rows"], raw["joins"]):
        need(row["root_pairs"] == old["root_pairs"], "saved root-pair relation disagreement")
        for r, s in row["sides"].items():
            need(s["E"] == old["side_available"][r], "saved side E disagreement")
    for der in derivatives:
        old = [x for x in raw["derivatives"] if x["vertices"] == der["vertices"] and
               [tuple(e) for e in x["edges"]] == der["edges"]]
        need(len(old) == 1 and old[0]["sigma"] == der["sigma"], "saved unit derivative disagreement")
    return {"status": "triggered and holds", "compared": ["piece topology", "complete tuples/full local lifts",
            "all 16 fibres", "joint root-pair relation", "side E", "unit derivative graph and Sigma"],
            "saved_decisions_used_as_input": False}


def calibrate(raw, fixed=True):
    g = normalize_graph(raw)
    pieces = reconstruct_pieces(g)
    relations = [{p["id"]: local_relation(g, p, beta) for p in pieces} for beta in PATTERNS]
    original = evaluate(g, pieces, relations)
    derivatives = [evaluate(g, pieces, relations, unit) for unit in units(g, pieces)]
    coverage = original_coverage(g, pieces, original)
    comparison = compare_saved(raw, pieces, relations, original, derivatives) if fixed else None
    core_inventory = []
    if fixed:
        for rc in raw["row_cores"]:
            for j, core in enumerate(rc["cores"]):
                deg = [sum(r in e for e in core["edges"]) for r in g["roots"]]
                need(deg == core["root_degrees"], "saved core degree inconsistent with its edges")
                core_inventory.append({"index": rc["index"], "occurrence": j,
                                       "root_degrees": deg, "saved_only": True})
    return {"id": g["id"], "graph": g, "pieces": pieces, "relations": relations,
            "original": original, "unit_derivatives": derivatives, "coverage": coverage,
            "saved_comparison": comparison, "saved_core_inventory": core_inventory,
            "collisions": collisions(g, pieces, relations)}


def calibration_occurrence(raw, rc, core, record):
    original, ders = record["original"], record["unit_derivatives"]
    matches = [d for d in ders if d["vertices"] == core["vertices"] and
               [list(e) for e in d["edges"]] == core["edges"]]
    need(len(matches) == 1, "N1 core is not exactly one original unit derivative")
    d = matches[0]
    need(d["root_degrees"] == core["root_degrees"] and d["sigma"] == core["sigma"], "N1 core payload disagreement")
    need(not d["rows"][rc["index"]]["root_pairs"], "saved N1 core not rejected")
    witnesses = []
    for e in d["edges"]:
        if e in frame_edges(record["graph"]["frame"]):
            continue
        es = [x for x in d["edges"] if x != e]
        pins = dict(zip(record["graph"]["frame"], PATTERNS[rc["index"]]))
        f = first_coloring(d["vertices"], es, pins)
        need(f is not None, "saved N1 core is not beta-minimal")
        validate_lift(d["vertices"], es, pins, f)
        witnesses.append({"edge": e, "lift": f})
    return {"source": raw["id"], "domain": "N1 calibration; not N2", "index": rc["index"],
            "beta": list(PATTERNS[rc["index"]]), "derivative": d["derivative"],
            "root_degrees": d["root_degrees"], "sigma": d["sigma"],
            "beta_minimality": {"status": "triggered and holds", "edge_deletion_lifts": witnesses},
            "capacity": d["rows"][rc["index"]]["capacity"]}


def stats(records):
    counts = Counter()
    for record in records:
        counts["graphs"] += 1
        for label, evaluations in (("original", [record["original"]]),
                                   ("derivative", record["unit_derivatives"])):
            counts[label + "_graphs"] += len(evaluations)
            for ev in evaluations:
                counts[label + "_rows"] += len(ev["rows"])
                for row in ev["rows"]:
                    counts[label + "_root_pair_queries"] += len(row["pairs"])
                    counts[label + "_nonempty_fibres"] += len(row["root_pairs"])
                    counts[label + "_empty_fibres"] += 16 - len(row["root_pairs"])
                    counts[label + "_rejected_rows"] += not bool(row["root_pairs"])
                    for c in row["capacity"]:
                        counts[label + "_capacity_" + c["status"]] += 1
                        if c["status"] == "triggered and holds":
                            counts[label + "_capacity_rhs_" + str(c["rhs"])] += 1
        for label, number in record["collisions"]["counts"].items():
            counts[label] += number
    return dict(counts)


def verify_frozen(home, live_base=None):
    manifest = json.loads((home / "inputs.json").read_text())
    need(manifest["BASE"] == BASE == manifest["actual_HEAD"], "input BASE drift")
    for item in manifest["files"]:
        need(digest(home / item["frozen_path"]) == item["sha256"], "frozen input drift: " + item["path"])
        if live_base:
            need(digest(live_base / item["path"]) == item["sha256"], "live input drift: " + item["path"])
    need(digest(home / manifest["task_instruction"]["snapshot"]) == manifest["task_instruction"]["sha256"], "task drift")
    return manifest


def build(home, source=None, live_base=None):
    manifest = verify_frozen(home, live_base)
    if source:
        raw = json.loads(source.read_text())
        records = [calibrate(raw, fixed=False)]
        return {"certificate.json": {"schema": 1, "BASE": BASE, "domain": "one supplied named source graph",
                "source_path": str(source.resolve()), "source_sha256": digest(source),
                "source_input": raw, "checker_sha256": digest(Path(__file__)), "records": records},
                "coverage.json": {"schema": 1, "BASE": BASE, "supplied_source": stats(records),
                                  "full_target": records[0]["coverage"]["full_target"]}}
    raw_graphs = [json.loads((home / x["frozen_path"]).read_text()) for x in manifest["files"]
                  if x["path"].startswith("artifacts/c5_excess_two_e4c/controls/")]
    need(len(raw_graphs) == 54, "fixed input inventory size")
    inventory, n2_raw, n1_raw, occurrences = [], [], {}, []
    for raw in raw_graphs:
        g = normalize_graph(raw)
        pieces = reconstruct_pieces(g)
        m = sum(p["kind"] == "mixed" for p in pieces)
        need(m == raw["m"], "inventory m disagreement")
        inventory.append({"id": raw["id"], "m": m, "u": len(pieces) - m,
                          "vertices": g["vertices"], "edges": g["edges"], "frame": g["frame"],
                          "roots": g["roots"], "disk": g["disk"], "pieces": pieces})
        if m == 2:
            n2_raw.append(raw)
        for rc in raw["row_cores"]:
            for core in rc["cores"]:
                degree = [sum(r in e for e in core["edges"]) for r in g["roots"]]
                if degree in ([4, 5], [5, 4]):
                    need(m == 1, "new N2 45/54 occurrence: update frozen scope, do not silently include")
                    n1_raw[raw["id"]] = raw
                    occurrences.append((raw, rc, core))
    need(len(n2_raw) == 19 and len(occurrences) == 12, "fixed domain disagreement")
    n2, n1 = [], {}
    for raw in n2_raw:
        n2.append(calibrate(raw))
    for name, raw in n1_raw.items():
        n1[name] = calibrate(raw)
    calibrated = [calibration_occurrence(raw, rc, core, n1[raw["id"]]) for raw, rc, core in occurrences]
    coverage = {"schema": 1, "BASE": BASE, "N2": stats(n2), "N1_separate": stats(list(n1.values())),
                "N1_45_54_occurrences": calibrated,
                "full_target_counts": dict(Counter(r["coverage"]["full_target"]["status"] for r in n2)),
                "N2_45_54_saved_core_occurrences": 0,
                "counterexample": [],
                "not_checked": ["S/U new claims", "arbitrary-size source exclusion", "new graph families",
                                "Lean", "original upstream enumeration replay"]}
    certificate = {"schema": 1, "BASE": BASE, "domain": "19 fixed N2 controls plus separately labelled saved N1 calibration",
                   "checker_sha256": digest(Path(__file__)), "inputs_sha256": digest(home / "inputs.json"),
                   "canonical_patterns": PATTERNS, "N2": n2, "N1_separate": list(n1.values())}
    return {"certificate.json": certificate, "coverage.json": coverage,
            "inventory.json": {"schema": 1, "BASE": BASE, "all_54_original_graphs": inventory,
                               "N2_selected": [g["id"] for g in n2_raw],
                               "N1_selected": list(n1_raw), "N1_45_54_occurrence_count": 12}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--out", type=Path, default=HOME / "results")
    parser.add_argument("--source", type=Path, help="one original named graph JSON; no saved decisions required")
    parser.add_argument("--live-base", type=Path, help="also check original BASE input bytes, read-only")
    args = parser.parse_args()
    if args.check:
        need(args.out.is_dir(), "no output directory to replay")
    else:
        args.out.mkdir(parents=False, exist_ok=False)
    payloads = build(HOME, args.source, args.live_base)
    for name, value in payloads.items():
        data, path = encoded(value), args.out / name
        if args.check:
            need(path.read_bytes() == data, "certificate byte/payload drift: " + name)
        else:
            with path.open("xb") as f:
                f.write(data)
    summary = payloads["coverage.json"]
    print(json.dumps({"status": "PASS", "mode": "read-only replay" if args.check else "exclusive-create",
                      "N2": summary.get("N2"), "N1": summary.get("N1_separate"),
                      "supplied_source": summary.get("supplied_source"), "counterexample": []},
                     ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        sys.exit(1)
