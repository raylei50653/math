#!/usr/bin/env python3
"""Read-only N45-U-LP source validator; stdlib, original edges are the oracle.

Adapted interface concepts from frozen J/SU-J, with no worker-module imports.
Every supplied declaration is checked even when LP applicability is absent.
The solver enumerates a supplied graph, never searches or bounds a graph family.
"""
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

COL = set(range(4))
PATTERNS = [list(map(int, s)) for s in (
    "01012", "01021", "01023", "01201", "01202",
    "01203", "01212", "01213", "01231", "01232")]
PAIRS = list(product(range(4), repeat=2))
QINDEX = [6, 4, 3, 1, 0]


class DataError(ValueError):
    """A supplied, checkable declaration contradicts its original source."""


def need(ok, message):
    if not ok:
        raise DataError(message)


def enc(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def order(v):
    return (0, v) if type(v) is int else (1, v)


def sv(vs):
    return sorted(vs, key=order)


def edge(u, v):
    return tuple(sv((u, v)))


def se(es):
    return sorted(es, key=lambda e: (order(e[0]), order(e[1])))


def adjacency(vs, es):
    a = {v: set() for v in vs}
    for u, v in es:
        a[u].add(v)
        a[v].add(u)
    return a


def components(vs, es):
    vs = set(vs)
    a = adjacency(vs, [e for e in es if set(e) <= vs])
    remaining, result = set(vs), []
    while remaining:
        todo, found = [min(remaining, key=order)], set()
        while todo:
            v = todo.pop()
            if v in found:
                continue
            found.add(v)
            todo.extend(a[v] - found)
        remaining -= found
        result.append(sv(found))
    return result


def bridges(vs, es):
    n = len(components(vs, es))
    return [list(e) for e in es if len(components(vs, [f for f in es if f != e])) > n]


def colors(vs, es, pins, first=False):
    """Direct MRV backtracking on original edges, independent of relations."""
    need(set(pins) <= set(vs), "pin outside source vertices")
    need(all(type(c) is int and c in COL for c in pins.values()), "invalid pin color")
    a, f, out = adjacency(vs, es), dict(pins), []
    if any(f[u] == f[v] for u, v in es if u in f and v in f):
        return []

    def visit():
        if len(f) == len(vs):
            out.append([f[v] for v in vs])
            return first
        choices = []
        for v in vs:
            if v not in f:
                opts = sorted(COL - {f[w] for w in a[v] if w in f})
                choices.append((len(opts), -len(a[v]), order(v), v, opts))
        _, _, _, v, opts = min(choices)
        for c in opts:
            f[v] = c
            stop = visit()
            del f[v]
            if stop:
                return True
        return False

    visit()
    return sorted(out)


def legal(vs, es, pins, lift):
    need(isinstance(lift, list) and len(lift) == len(vs), "missing/wrong-size full lift")
    need(all(type(c) is int and c in COL for c in lift), "invalid lift color")
    f = dict(zip(vs, lift))
    need(all(f[v] == c for v, c in pins.items()), "literal frame/root pins drift")
    need(all(f[u] != f[v] for u, v in es), "full lift violates original edge")
    return f


def faces(vs, es, rot):
    a = adjacency(vs, es)
    need(set(rot) == set(vs), "rotation vertex set differs from source")
    for v in vs:
        need(len(rot[v]) == len(set(rot[v])) and set(rot[v]) == a[v], "rotation neighborhood differs from original edges")
    unseen = {(u, v) for e in es for u, v in (e, e[::-1])}
    result, face_of = [], {}
    while unseen:
        start = min(unseen, key=lambda e: (order(e[0]), order(e[1])))
        d, walk = start, []
        while True:
            need(d in unseen, "rotation repeats a dart")
            unseen.remove(d)
            face_of[d] = len(result)
            u, v = d
            walk.append(u)
            ring = rot[v]
            d = (v, ring[(ring.index(u) + 1) % len(ring)])
            if d == start:
                break
        result.append(walk)
    return result, face_of


def frame_edges(frame):
    return {edge(frame[i], frame[(i + 1) % 5]) for i in range(5)}


def layer(ok=None, missing=(), detail=None):
    result = {"status": "not triggered" if missing else ("triggered and holds" if ok else "counterexample"),
              "missing_sufficient_premises": list(missing)}
    if detail is not None:
        result["detail"] = detail
    return result


def normalize(raw, frame=None, roots=None, declarations=None):
    need(isinstance(raw, dict), "graph must be a JSON object")
    vs = raw["vertices"]
    need(all(type(v) in (int, str) for v in vs), "named vertices must be integer or string")
    need(len(vs) == len(set(vs)) and len({str(v) for v in vs}) == len(vs), "duplicate/ambiguous named vertex")
    vs = sv(vs)
    need(all(isinstance(e, list) and len(e) == 2 for e in raw["edges"]), "malformed original edge")
    es = se([edge(*e) for e in raw["edges"]])
    need(len(es) == len(set(es)) and all(u != v and set((u, v)) <= set(vs) for u, v in es), "source is not a finite simple graph")
    frame = frame if frame is not None else raw.get("frame", list(range(5)))
    need(len(frame) == 5 and len(set(frame)) == 5 and set(frame) <= set(vs), "ordered frame is not five distinct original vertices")
    B, fe, a = set(frame), frame_edges(frame), adjacency(vs, es)
    need({e for e in es if set(e) <= B} == fe, "ordered frame is not induced C5")
    roots = roots if roots is not None else raw.get("roots", sv(v for v in vs if v not in B and len(a[v]) == 5))
    need(len(roots) == 2 and len(set(roots)) == 2 and set(roots) <= set(vs) - B, "two distinct named original roots required")
    isolated = sv(v for v in vs if v not in B and not a[v])
    H = set(vs) - B - set(isolated)
    layers = {}
    degree_ok = (all(len(a[r]) == 5 for r in roots) and edge(*roots) not in es and
                 all(len(a[v]) == 4 for v in H - set(roots)))
    layers["original_degrees_rs_epsilon2"] = layer(True) if degree_ok else layer(missing=["exactly two nonadjacent original degree5 roots; other effective interiors degree4"])
    touch = sv(B & set().union(*(a[v] for v in H)))
    layers["full_B_touch_H_connected"] = layer(True) if set(touch) == B and len(components(H, es)) == 1 else layer(missing=["original H connected and full B-touch"])
    rot, face_list = None, []
    if "rotation" not in raw:
        layers["ordered_induced_C5_disk"] = layer(missing=["original named rotation"])
    else:
        need(set(raw["rotation"]) == {str(v) for v in vs}, "rotation has missing/extra vertex")
        rot = {v: raw["rotation"][str(v)] for v in vs}
        # Isolated vertices are explicitly ignored in the effective disk embedding.
        ev = [v for v in vs if v not in isolated]
        face_list, _ = faces(ev, es, {v: rot[v] for v in ev})
        need(all(rot[v] == [] for v in isolated), "isolated vertex has a rotation dart")
        outer = [f for f in face_list if len(f) == 5 and set(f) == B and frame_edges(f) == fe]
        disk_ok = len(components(ev, es)) == 1 and len(ev) - len(es) + len(face_list) == 2 and len(outer) == 1
        layers["ordered_induced_C5_disk"] = layer(disk_ok, detail={"faces": face_list, "outer": outer, "ignored_isolated": isolated})
    pieces = []
    actual_components = components(H - set(roots), es)
    if declarations is None:
        declarations = raw.get("pieces")
    if declarations is not None:
        need(isinstance(declarations, list), "piece declarations must be a list")
        need(len(declarations) == len(actual_components), "declared pieces are not all complete original H-root components")
        need(all(isinstance(p, dict) and isinstance(p.get("id"), str) for p in declarations), "each declared piece needs a string id")
        need(len({p["id"] for p in declarations}) == len(declarations), "duplicate piece id")
    for i, pv in enumerate(actual_components):
        old = None
        if declarations is not None:
            matches = [p for p in declarations if p.get("vertices") == pv]
            need(len(matches) == 1, "declared piece splits, truncates, duplicates, or merges an original component")
            old = matches[0]
        ps = set(pv)
        contacts = {str(r): sv(a[r] & ps) for r in roots}
        owners = [r for r in roots if contacts[str(r)]]
        actual_order = sv(set().union(*(set(c) for c in contacts.values())))
        contact_order = old.get("contact_order", actual_order) if old else actual_order
        need(len(contact_order) == len(set(contact_order)) and set(contact_order) == set(actual_order), "ordered contacts omit/duplicate a shared original coordinate")
        internal = [e for e in es if set(e) <= ps]
        attachments = [e for e in es if set(e) & ps and set(e) & B]
        support = sv(B & set().union(*(a[v] for v in pv)))
        one = len(components(H - ps, es)) == 1
        p = {"id": old["id"] if old else f"P{i}", "vertices": pv, "contacts": contacts,
             "owners": owners, "contact_order": contact_order,
             "shared_contacts": sv(set(contacts[str(roots[0])]) & set(contacts[str(roots[1])])),
             "support": support, "attachments": list(map(list, attachments)), "internal_edges": list(map(list, internal)),
             "incidences": [len(contacts[str(r)]) for r in roots],
             "kind": "mixed" if len(owners) == 2 else ("unary" if len(owners) == 1 else "root-free"),
             "one_sided": one, "original_internal_bridges": bridges(pv, internal)}
        if one and rot is not None and layers["ordered_induced_C5_disk"]["status"] == "triggered and holds" and support:
            kv = sv(B | ps)
            ke = [e for e in es if set(e) <= set(kv)]
            kr = {v: [w for w in rot[v] if w in kv] for v in kv}
            kfaces, faceof = faces(kv, ke, kr)
            occupied = set()
            for v in kv:
                ring = rot[v]
                for j, w in enumerate(ring):
                    if w in kv:
                        continue
                    predecessor = (j - 1) % len(ring)
                    while ring[predecessor] not in kv:
                        predecessor = (predecessor - 1) % len(ring)
                    occupied.add(faceof[(ring[predecessor], v)])
            need(len(occupied) == 1, "original one-sided complement occupies multiple piece faces")
            cf = kfaces[next(iter(occupied))]
            boundary = {edge(cf[j], cf[(j + 1) % len(cf)]) for j in range(len(cf))}
            shield = se(fe - boundary)
            p["shield"] = {"complement_face": cf, "edges": list(map(list, shield)), "length": len(shield)}
        if old is not None:
            for key in ("contacts", "owners", "contact_order", "support", "attachments", "internal_edges", "incidences", "kind", "one_sided", "shared_contacts"):
                if key in old:
                    need(old[key] == p[key], "declared original piece " + p["id"] + " has wrong " + key)
            for key in ("original_bridges", "original_internal_bridges"):
                if key in old:
                    need(old[key] == p["original_internal_bridges"], "declared original bridges differ")
            if "shield" in old:
                sh = p.get("shield")
                need(sh is not None and old["shield"]["edges"] == sh["edges"], "declared original shield differs from rotation")
                for key in ("complement_face", "length"):
                    if key in old["shield"]:
                        need(old["shield"][key] == sh[key], "declared original shield " + key + " differs")
        pieces.append(p)
    all_one = all(p["one_sided"] and p["support"] and p["owners"] for p in pieces)
    layers["complete_components_one_sided"] = layer(True) if all_one else layer(missing=["every complete original piece one-sided with nonempty support and root contact"])
    return {"id": raw.get("id", "named-source"), "vertices": vs, "edges": list(map(list, es)), "frame": frame,
            "roots": roots, "rotation": raw.get("rotation"), "faces": face_list, "pieces": pieces,
            "ignored_isolated": isolated, "touch": touch, "H_bridges": bridges(sv(H), [e for e in es if set(e) <= H]), "layers": layers}


def local_relation(g, p, beta):
    vs = sv(set(g["frame"]) | set(p["vertices"]))
    es = [tuple(e) for e in g["edges"] if set(e) <= set(vs)]
    pins = dict(zip(g["frame"], beta))
    all_lifts = colors(vs, es, pins)
    groups = {}
    for lift in all_lifts:
        f = legal(vs, es, pins, lift)
        t = tuple(f[x] for x in p["contact_order"])
        groups.setdefault(t, []).append([f[x] for x in p["vertices"]])
    tuples = [{"tuple": list(t), "lifts": sorted(groups[t])} for t in sorted(groups)]
    fibres = []
    for pair in PAIRS:
        ix = [j for j, t in enumerate(tuples) if all(t["tuple"][p["contact_order"].index(x)] != pair[k]
              for k, r in enumerate(g["roots"]) for x in p["contacts"][str(r)])]
        fibres.append({"pins": list(pair), "tuple_indices": ix})
    F = {str(r): sorted(c for c in COL if tuples and all(any(t["tuple"][p["contact_order"].index(x)] == c
         for x in p["contacts"][str(r)]) for t in tuples)) for r in p["owners"]}
    return {"tuples": tuples, "fibres": fibres, "F": F}


def joined_row(g, vs, es, active, beta, relations):
    pins = dict(zip(g["frame"], beta))
    direct = colors(vs, es, pins)
    groups = {pair: [] for pair in PAIRS}
    for lift in direct:
        f = legal(vs, es, pins, lift)
        groups[tuple(f[r] for r in g["roots"])].append(lift)
    roots, fe = g["roots"], frame_edges(g["frame"])
    sides = {}
    for r in roots:
        factors = [{"id": ["spoke", r, b], "n": 1, "F": [pins[b]]}
                   for b in g["frame"] if edge(r, b) in es]
        factors += [{"id": ["unary", p["id"]], "n": len(p["contacts"][str(r)]), "F": relations[p["id"]]["F"][str(r)]}
                    for p in active if p["kind"] == "unary" and r in p["owners"]]
        union = set().union(*(set(f["F"]) for f in factors))
        sides[str(r)] = {"factors": factors, "E": sorted(COL - union)}
    cells = []
    for k, pair in enumerate(PAIRS):
        selected = {p["id"]: relations[p["id"]]["fibres"][k]["tuple_indices"] for p in active}
        base = pins | dict(zip(roots, pair))
        direct_edges_ok = all(base[u] != base[v] for u, v in es if u in base and v in base)
        # Cartesian product of full local lifts, with one coordinate for a shared contact.
        choices = [[lift for j in selected[p["id"]] for lift in relations[p["id"]]["tuples"][j]["lifts"]] for p in active]
        assembled = []
        if direct_edges_ok:
            for combination in product(*choices):
                f = dict(base)
                for p, lift in zip(active, combination):
                    f.update(zip(p["vertices"], lift))
                missing_vertices = [v for v in vs if v not in f]
                for extra in product(range(4), repeat=len(missing_vertices)):
                    ff = f | dict(zip(missing_vertices, extra))
                    lift = [ff[v] for v in vs]
                    legal(vs, es, base, lift)
                    assembled.append(lift)
        need(sorted(assembled) == groups[pair], "complete tuple join differs from all original-edge full lifts")
        cells.append({"pins": list(pair), "tuple_indices": selected, "full_lifts": groups[pair]})
    return {"literal_beta": list(beta), "sides": sides, "all_16_fibres": cells,
            "root_pairs": [list(pair) for pair in PAIRS if groups[pair]]}


def compute_graph(raw, frame=None, roots=None, declarations=None):
    g = normalize(raw, frame, roots, declarations)
    ds = declarations if declarations is not None else raw.get("pieces")
    for p in g["pieces"]:
        p["rows"] = [local_relation(g, p, beta) for beta in PATTERNS]
        old = next((d for d in ds or [] if d["id"] == p["id"]), None)
        if old and "rows" in old:
            need(len(old["rows"]) == 10, "declared complete relation lacks one of ten literal rows")
            for i, (row, saved) in enumerate(zip(p["rows"], old["rows"])):
                need(saved.get("index", i) == i, "declared piece row index drift")
                need(saved["tuples"] == row["tuples"], f"complete relation/full lifts differ: {p['id']} row {i}")
                need(saved["fibres"] == row["fibres"], f"complete empty/nonempty fibres differ: {p['id']} row {i}")
                if "F" in saved:
                    need(saved["F"] == row["F"], "declared forbidden colors differ")
                if "available" in saved:
                    available = {str(r): sorted({f["pins"][k] for f in row["fibres"] if f["tuple_indices"]})
                                 for k, r in enumerate(g["roots"]) if r in p["owners"]}
                    need(saved["available"] == available, "declared available root colors differ from full fibres")
    es = [tuple(e) for e in g["edges"]]
    g["rows"] = [joined_row(g, g["vertices"], es, g["pieces"], beta,
                 {p["id"]: p["rows"][i] for p in g["pieces"]}) for i, beta in enumerate(PATTERNS)]
    g["sigma"] = sum(1 << i for i, row in enumerate(g["rows"]) if row["root_pairs"])
    if "sigma" in raw and frame is None:
        need(g["sigma"] == raw["sigma"], "declared complete Sigma differs from original-edge oracle")
    g["layers"]["complete_relations_fibres_full_lifts"] = layer(True, detail={"rows": 10, "pieces": len(g["pieces"])})
    g["critical_witnesses"] = []
    for e in es:
        if e in frame_edges(g["frame"]):
            continue
        found = []
        for i, row in enumerate(g["rows"]):
            if row["root_pairs"]:
                continue
            cuts = colors(g["vertices"], [f for f in es if f != e], dict(zip(g["frame"], PATTERNS[i])), first=True)
            if cuts:
                legal(g["vertices"], [f for f in es if f != e], dict(zip(g["frame"], PATTERNS[i])), cuts[0])
                found.append({"index": i, "full_lift": cuts[0]})
        g["critical_witnesses"].append({"edge": list(e), "gained_rows": found})
    critical = all(w["gained_rows"] for w in g["critical_witnesses"])
    g["layers"]["each_nonframe_edge_Sigma_critical"] = layer(True) if critical else layer(missing=["every original nonframe edge has a gained literal-row witness"], detail=[w["edge"] for w in g["critical_witnesses"] if not w["gained_rows"]])
    return g


def normalize_colors(pattern):
    d = {}
    return tuple(d.setdefault(c, len(d)) for c in pattern)


def d5_targets():
    index = {tuple(p): i for i, p in enumerate(PATTERNS)}
    records = []
    for sigma in (933, 941):
        for sign in (1, -1):
            for offset in range(5):
                perm = [(offset + sign * j) % 5 for j in range(5)]
                mask = 0
                for i, beta in enumerate(PATTERNS):
                    if sigma & (1 << i):
                        # All coordinates undergo one whole-frame transport.
                        row = index[normalize_colors([beta[j] for j in perm])]
                        mask |= 1 << row
                records.append({"canonical_sigma": sigma, "whole_frame_positions": perm, "sigma": mask})
    return records


def support_kind(g, p):
    support = set(p["support"])
    pair = len(support) == 2 and any(support == set(e) for e in frame_edges(g["frame"]))
    short = bool(support) and any(support <= set(e) for e in frame_edges(g["frame"]))
    return "short edge-pair" if pair else ("short singleton" if short else "long")


def lp_geometry(g, roles=None):
    mixed = [p for p in g["pieces"] if p["kind"] == "mixed"]
    unary = [p for p in g["pieces"] if p["kind"] == "unary"]
    candidates = []
    for u in unary:
        for l in mixed:
            for s in mixed:
                if l["id"] == s["id"]:
                    continue
                missing = []
                if len(g["pieces"]) != 3 or len(mixed) != 2 or len(unary) != 1:
                    missing.append("exactly two complete mixed pieces and unique original unary U")
                if sum(u["incidences"]) != 1:
                    missing.append("original U incidence one")
                if support_kind(g, l) != "long":
                    missing.append("original L actual support long")
                if support_kind(g, s) != "short edge-pair":
                    missing.append("original S actual support exactly a frame edge pair")
                if not all(p["one_sided"] for p in (u, l, s)):
                    missing.append("all three original pieces one-sided")
                shields = [p.get("shield") for p in (u, l, s)]
                sets = [set(map(tuple, sh["edges"])) if sh else set() for sh in shields]
                if [len(x) for x in sets] != [2, 2, 1] or sum(map(len, sets)) != len(set().union(*sets)) or set().union(*sets) != frame_edges(g["frame"]):
                    missing.append("original shield lengths 2+2+1 partition all five frame edges")
                for p in (u, l):
                    if not any(set(p["support"]) == {g["frame"][(j + k) % 5] for k in range(3)} for j in range(5)):
                        missing.append("original " + p["id"] + " support three consecutive frame points")
                candidates.append({"U": u["id"], "L": l["id"], "S": s["id"], "check": layer(True) if not missing else layer(missing=missing)})
    holds = [c for c in candidates if c["check"]["status"] == "triggered and holds"]
    result = layer(True, detail=holds) if holds else layer(missing=["complete unique-unit-U + long-L + short-edge-pair-S geometry"], detail=candidates)
    if roles is not None and all(roles.get(k) is not None for k in ("U", "L", "S")):
        need(len({roles[k] for k in ("U", "L", "S")}) == 3, "declared U/L/S roles are not distinct")
        matches = [c for c in candidates if all(c[k] == roles[k] for k in ("U", "L", "S"))]
        need(len(matches) == 1, "declared U/L/S roles are not complete original components")
        need(matches[0]["check"]["status"] == "triggered and holds", "declared U/L/S geometry contradicts actual original supports/rotation")
    return result


def omit_unit(g, unit, beta, declared_X=None):
    p = next((p for p in g["pieces"] if p["id"] == unit), None)
    need(p is not None and p["kind"] == "unary" and sum(p["incidences"]) == 1, "declared omitted unit is not a complete original incidence-one unary")
    need(isinstance(beta, list) and len(beta) == 5 and all(type(c) is int and c in COL for c in beta), "invalid literal beta")
    need(all(beta[j] != beta[(j + 1) % 5] for j in range(5)), "literal beta is not a proper frame coloring")
    vs = [v for v in g["vertices"] if v not in p["vertices"]]
    es = [tuple(e) for e in g["edges"] if set(e) <= set(vs)]
    if declared_X is not None:
        need(declared_X.get("vertices") == vs and declared_X.get("edges") == list(map(list, es)), "declared X is not exactly G minus the whole original U (retained edge mismatch)")
    active = [t for t in g["pieces"] if t["id"] != unit]
    rows = [joined_row(g, vs, es, active, pat, {t["id"]: t["rows"][i] for t in active}) for i, pat in enumerate(PATTERNS)]
    xsigma = sum(1 << i for i, row in enumerate(rows) if row["root_pairs"])
    literal_rel = {t["id"]: local_relation(g, t, beta) for t in g["pieces"]}
    brow = joined_row(g, vs, es, active, beta, literal_rel)
    r = p["owners"][0]
    s = next(t for t in g["roots"] if t != r)
    a = adjacency(vs, es)
    contact = edge(r, p["contacts"][str(r)][0])
    # Entire-U omission and deletion of its sole original contact remain distinct graphs/lifts.
    cut_es = [tuple(e) for e in g["edges"] if tuple(e) != contact]
    contact_rows = []
    forcing = []
    for i, row in enumerate(rows):
        cs = colors(g["vertices"], cut_es, dict(zip(g["frame"], PATTERNS[i])))
        pairs = sorted({tuple(dict(zip(g["vertices"], lift))[t] for t in g["roots"]) for lift in cs})
        need([list(x) for x in pairs] == row["root_pairs"], "whole U omission and sole contact deletion root pairs differ")
        contact_rows.append({"index": i, "vertices": g["vertices"], "all_full_lifts": cs})
        if row["root_pairs"] and not g["rows"][i]["root_pairs"]:
            rel = p["rows"][i]
            palette = sorted({t["tuple"][0] for t in rel["tuples"]})
            projection = sorted({pair[g["roots"].index(r)] for pair in row["root_pairs"]})
            ok = len(palette) == 1 and palette == projection
            forcing.append({"index": i, "contact_palette": palette, "all_X_r_projection": projection, "check": layer(ok)})
    edge_witnesses = []
    if not brow["root_pairs"]:
        for e in es:
            if e in frame_edges(g["frame"]):
                continue
            lifts = colors(vs, [f for f in es if f != e], dict(zip(g["frame"], beta)), first=True)
            edge_witnesses.append({"edge": list(e), "full_lift": lifts[0] if lifts else None})
    minimum = not brow["root_pairs"] and all(w["full_lift"] is not None for w in edge_witnesses)
    missing_core = []
    if brow["root_pairs"]:
        missing_core.append("X rejects this literal beta")
    if [len(a[r]), len(a[s])] != [4, 5]:
        missing_core.append("r drops to degree4, s retains degree5")
    if not minimum:
        missing_core.append("every retained nonframe edge deletion accepts the same beta")
    columns = []
    er, ess = set(brow["sides"][str(r)]["E"]), set(brow["sides"][str(s)]["E"])
    missing_cap = list(missing_core)
    if not ess:
        missing_cap.append("E_s nonempty")
    if any(not literal_rel[t["id"]]["tuples"] for t in active):
        missing_cap.append("all active original local relations nonempty")
    if not missing_cap:
        factors = brow["sides"][str(r)]["factors"]
        for b in sorted(ess):
            cols = []
            for t in active:
                if t["kind"] != "mixed":
                    continue
                bad = [c for c in range(4) if not literal_rel[t["id"]]["fibres"][4*c+b if r == g["roots"][0] else 4*b+c]["tuple_indices"]]
                cols.append({"piece": t["id"], "k": len(t["contacts"][str(r)]), "forbidden": bad})
            union = set().union(*(set(c["forbidden"]) for c in cols))
            fsets = [set(f["F"]) for f in factors]
            terms = [sum(f["n"] - len(f["F"]) for f in factors),
                     sum(map(len, fsets)) - len(set().union(*fsets)),
                     sum(c["k"] - len(c["forbidden"]) for c in cols),
                     sum(len(c["forbidden"]) for c in cols) - len(union), len(union - er)]
            ok = terms == [0]*5 and union == er and all(len(c["forbidden"]) == c["k"] for c in cols)
            columns.append({"b": b, "columns": cols, "E_r_X": sorted(er), "D_O_delta_o_lambda": terms, "check": layer(ok)})
    result = {"piece": unit, "r": r, "s": s, "contact_edge": list(contact), "vertices_X": vs, "edges_X": list(map(list, es)),
              "sigma_X": xsigma, "rows_X": rows, "contact_deleted_rows": contact_rows, "literal_beta": beta, "literal_beta_X": brow,
              "retained_edge_beta_witnesses": edge_witnesses, "Delta": [i for i in range(10) if xsigma & (1 << i) and not g["sigma"] & (1 << i)],
              "new_gamma_singleton_forcing": forcing, "zero_slack_columns": columns,
              "layers": {"exact_whole_U_omission": layer(True),
                         "rejecting_beta_minimal_45_54_core": layer(True) if not missing_core else layer(missing=missing_core),
                         "core_zero_slack_full_partition": layer(all(c["check"]["status"] == "triggered and holds" for c in columns), missing_cap, columns),
                         "all_Delta_gamma_singleton_forcing": layer(all(f["check"]["status"] == "triggered and holds" for f in forcing)) if forcing else layer(missing=["nonempty Delta of new accepted rows"])}}
    return result


def validate_proposal(path):
    """Only reads the proposal and its separately bound original graph file."""
    path = Path(path)
    q = json.loads(path.read_text())
    need(q.get("schema") == "n45-pc-v1", "unknown proposal schema")
    graph_path = path.parent / q["graph_file"]
    need(q.get("source_sha256") == digest(graph_path), "stale source_sha256 for the same original graph file")
    raw = json.loads(graph_path.read_text())
    g = compute_graph(raw, q.get("frame"), q.get("roots"), q.get("pieces"))
    if "critical_witnesses" in q:
        declared = q["critical_witnesses"]
        expected_edges = [w["edge"] for w in g["critical_witnesses"]]
        need(len(declared) == len(expected_edges) and {tuple(w["edge"]) for w in declared} == set(map(tuple, expected_edges)),
             "declared critical witnesses do not cover every original nonframe edge exactly once")
        for w in declared:
            i = w["index"]
            need(type(i) is int and i in range(10) and not g["rows"][i]["root_pairs"], "declared critical witness row does not reject G")
            legal(g["vertices"], [tuple(e) for e in g["edges"] if e != w["edge"]],
                  dict(zip(g["frame"], PATTERNS[i])), w["full_lift"])
    layers = dict(g["layers"])
    layers["source_hash_binding"] = layer(True)
    matches = [x for x in d5_targets() if x["sigma"] == g["sigma"]]
    layers["full_ten_row_target_whole_D5"] = layer(True, detail=matches) if matches else layer(missing=["complete Sigma 933/941 or one whole-frame D5 image"], detail={"actual_sigma": g["sigma"]})
    roles = q.get("roles", {})
    for role in ("L", "S"):
        if roles.get(role) is not None:
            p = next((p for p in g["pieces"] if p["id"] == roles[role]), None)
            need(p is not None and p["kind"] == "mixed", "declared " + role + " is not an original mixed component")
            need(support_kind(g, p) == ("long" if role == "L" else "short edge-pair"), "declared " + role + " has wrong original actual support")
    layers["LP_original_geometry"] = lp_geometry(g, roles)
    layers["declared_U_L_S"] = layer(True) if all(roles.get(k) is not None for k in ("U", "L", "S")) else layer(missing=["distinct named U,L,S roles"])
    layers["declared_complete_original_pieces"] = layer(True) if "pieces" in q else layer(missing=["complete original component declarations with ordered contacts"])
    u = None
    if roles.get("U") is not None:
        need("beta" in q, "declared U requires a proper literal beta")
        u = omit_unit(g, roles["U"], q["beta"], q.get("X"))
        if "beta_deletion_witnesses" in q:
            declared = q["beta_deletion_witnesses"]
            expected_edges = [e for e in u["edges_X"] if tuple(e) not in frame_edges(g["frame"])]
            need(len(declared) == len(expected_edges) and {tuple(w["edge"]) for w in declared} == set(map(tuple, expected_edges)),
                 "declared beta witnesses do not cover every retained nonframe edge exactly once")
            for w in declared:
                legal(u["vertices_X"], [tuple(e) for e in u["edges_X"] if e != w["edge"]],
                      dict(zip(g["frame"], q["beta"])), w["full_lift"])
        layers.update(u["layers"])
        layers["declared_X_identity"] = layer(True) if "X" in q else layer(missing=["declared complete vertices/edges of X=G-V(U)"])
    else:
        layers["exact_whole_U_omission"] = layer(missing=["named original incidence-one U and literal beta"])
        layers["rejecting_beta_minimal_45_54_core"] = layer(missing=["named whole-U X and same rejected literal beta"])
        layers["core_zero_slack_full_partition"] = layer(missing=["named beta-minimal degree4-side core"])
        layers["all_Delta_gamma_singleton_forcing"] = layer(missing=["named whole-U X and nonempty Delta"])
        layers["declared_X_identity"] = layer(missing=["declared exact X"])
    # Derived LP beta and cross-row conditions are never certified on an absent antecedent.
    prerequisites = [k for k in ("original_degrees_rs_epsilon2", "ordered_induced_C5_disk", "full_B_touch_H_connected",
                     "complete_components_one_sided", "each_nonframe_edge_Sigma_critical", "full_ten_row_target_whole_D5",
                     "LP_original_geometry", "rejecting_beta_minimal_45_54_core") if layers[k]["status"] != "triggered and holds"]
    if prerequisites:
        layers["LP_common_D_and_spokes"] = layer(missing=prerequisites)
        layers["LP_cross_row_Q_Delta"] = layer(missing=prerequisites)
    else:
        beta = q["beta"]
        active = [p for p in g["pieces"] if p["id"] != roles["U"]]
        D = COL - set(beta)
        r, s = u["r"], u["s"]
        es = list(map(tuple, u["edges_X"]))
        distinct = all(len([beta[g["frame"].index(b)] for b in g["frame"] if edge(root, b) in es]) ==
                       len({beta[g["frame"].index(b)] for b in g["frame"] if edge(root, b) in es}) for root in (r, s))
        er = set(u["literal_beta_X"]["sides"][str(r)]["E"])
        ess = set(u["literal_beta_X"]["sides"][str(s)]["E"])
        rels = {p["id"]: local_relation(g, p, beta) for p in active}
        d = next(iter(D)) if len(D) == 1 else None
        dcheck = d is not None and d in er & ess and bool(rels[roles["S"]]["fibres"][5*d]["tuple_indices"]) and not rels[roles["L"]]["fibres"][5*d]["tuple_indices"]
        layers["LP_common_D_and_spokes"] = layer(distinct and dcheck, detail={"common_unused_D": sorted(D), "spokes_distinct_each_side": distinct})
        qg = [i for i, bit in enumerate(QINDEX) if not g["sigma"] & (1 << bit)]
        qx = [i for i, bit in enumerate(QINDEX) if not u["sigma_X"] & (1 << bit)]
        qshape = len(qx) <= 1 or len(qx) == 2 and (qx[1] - qx[0]) % 5 in (1, 4)
        threshold = 2 if g["sigma"].bit_count() == 6 else 1
        layers["LP_cross_row_Q_Delta"] = layer(qshape and set(qx) <= set(qg) and len(u["Delta"]) >= threshold,
                                               detail={"Q_G": qg, "Q_X": qx, "Delta": u["Delta"], "required_Delta_min": threshold})
    missing = [k for k, v in layers.items() if v["status"] != "triggered and holds"]
    if any(v["status"] == "counterexample" for v in layers.values()):
        status = "counterexample"
    elif missing:
        status = "not triggered"
    else:
        status = "triggered and holds"
    return {"proposal_sha256": digest(path), "source_sha256": digest(graph_path), "graph": g, "omission": u,
            "layers": layers, "source_contract": {"status": status, "missing_sufficient_premises": missing,
            "meaning": "Finite contract validation for this named source only; no source exclusion or arbitrary-size theorem."}}
