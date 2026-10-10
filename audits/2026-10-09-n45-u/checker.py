#!/usr/bin/env python3
"""N45-U fixed controls. Independent stdlib coloring; no catalogue search.

Only --generate writes, using exclusive creation. --check reconstructs bytes.
Saved conclusions are comparison data; graph computations start from original edges.
"""
import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "source"
BASE = "dc8e9aa7d6fccb51f63d30aa3f9c132296d44744"
B = set(range(5))
FRAME = {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)}
COL = set(range(4))
PATTERNS = [list(map(int, s)) for s in (
    "01012", "01021", "01023", "01201", "01202",
    "01203", "01212", "01213", "01231", "01232")]
Q_INDEX = [6, 4, 3, 1, 0]
T4 = {2, 5, 7, 8, 9}


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def neighbors(vertices, edges):
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def coloring(vertices, edges, pins, all_lifts=False):
    """Deterministic MRV enumeration; full vertices retained, including isolates."""
    adj = neighbors(vertices, edges)
    colors = dict(pins)
    assert set(colors) <= set(vertices)
    if any(u in colors and v in colors and colors[u] == colors[v] for u, v in edges):
        return []
    result = []

    def dfs():
        if len(colors) == len(vertices):
            result.append([colors[v] for v in vertices])
            return not all_lifts
        opts = [(len(cs), v, cs) for v in vertices if v not in colors
                for cs in [sorted(COL - {colors[w] for w in adj[v] if w in colors})]]
        _, v, cs = min(opts)
        for c in cs:
            colors[v] = c
            stop = dfs()
            del colors[v]
            if stop:
                return True
        return False

    dfs()
    return sorted(result)


def components(vertices, adj):
    left, result = set(vertices), []
    while left:
        todo, found = [min(left)], set()
        while todo:
            v = todo.pop()
            if v not in found:
                found.add(v)
                todo.extend(sorted(adj[v] & left - found, reverse=True))
        left -= found
        result.append(sorted(found))
    return result


def path_to_frame(start, excluded, vertices, edges):
    adj = neighbors(vertices, edges)
    queue, previous = deque([start]), {start: None}
    while queue:
        v = queue.popleft()
        if v in B:
            out = [v]
            while previous[out[-1]] is not None:
                out.append(previous[out[-1]])
            return out[::-1]
        for w in sorted(adj[v] - set(excluded)):
            if w not in previous:
                previous[w] = v
                queue.append(w)
    return None


def bridges(vertices, edges):
    baseline = len(components(vertices, neighbors(vertices, edges)))
    return [e for e in edges if len(components(vertices, neighbors(vertices, [x for x in edges if x != e]))) > baseline]


def faces_of(vertices, edges, rotation):
    rot = {int(k): list(v) for k, v in rotation.items()}
    adj = neighbors(vertices, edges)
    assert set(rot) == set(vertices)
    assert all(len(rot[v]) == len(set(rot[v])) and set(rot[v]) == adj[v] for v in vertices)
    darts = {(u, v) for a, b in edges for u, v in ((a, b), (b, a))}
    faces = []
    while darts:
        start = min(darts)
        dart, face = start, []
        while True:
            assert dart in darts
            darts.remove(dart)
            u, v = dart
            face.append(u)
            dart = (v, rot[v][(rot[v].index(u) + 1) % len(rot[v])])
            if dart == start:
                break
        faces.append(face)
    assert len(vertices) - len(edges) + len(faces) == 2
    outer = [f for f in faces if len(f) == 5 and set(f) == B]
    assert len(outer) == 1
    assert {tuple(sorted((outer[0][i], outer[0][(i + 1) % 5]))) for i in range(5)} == FRAME
    return rot, faces


def pieces_of(vertices, edges, roots, rotation):
    adj = neighbors(vertices, edges)
    inside = set(vertices) - B
    result = []
    for i, vs in enumerate(components(inside - set(roots), adj)):
        ps = set(vs)
        contacts = {r: sorted(adj[r] & ps) for r in roots}
        owners = [r for r in roots if contacts[r]]
        assert owners
        support = sorted(B & set().union(*(adj[v] for v in vs)))
        attachments = [e for e in edges if bool(set(e) & ps) and bool(set(e) & B)]
        internal = [e for e in edges if set(e) <= ps]
        order = sorted(set().union(*(set(contacts[r]) for r in roots)))
        outside = sorted(inside - ps)
        one_sided = len(components(outside, adj)) == 1
        piece = {"id": f"P{i}", "vertices": vs, "internal_edges": internal,
                 "attachments": attachments, "support": support, "owners": owners,
                 "contacts": {str(r): contacts[r] for r in roots},
                 "contact_order": order, "incidences": [len(contacts[r]) for r in roots],
                 "original_internal_bridges": bridges(vs, internal),
                 "kind": "unary" if len(owners) == 1 else "mixed",
                 "one_sided": one_sided, "rows": []}
        for index, row in enumerate(PATTERNS):
            lifts = coloring(sorted(B | ps), sorted(FRAME | set(internal) | set(attachments)),
                             dict(enumerate(row)), True)
            assert lifts  # unpinned root contacts supply strict list slack
            grouped = {}
            local_vs = sorted(B | ps)
            for lift in lifts:
                f = dict(zip(local_vs, lift))
                t = tuple(f[x] for x in order)
                grouped.setdefault(t, []).append([f[x] for x in vs])
            tuples = [{"tuple": list(t), "full_piece_lifts": sorted(grouped[t])}
                      for t in sorted(grouped)]
            fibres = []
            for a, b in product(range(4), repeat=2):
                pins = dict(zip(roots, (a, b)))
                matched = [j for j, item in enumerate(tuples)
                           if all(item["tuple"][order.index(x)] != pins[r]
                                  for r in roots for x in contacts[r])]
                fibres.append({"pins": [a, b], "tuple_indices": matched})
            forbidden = {}
            for r in owners:
                forbidden[str(r)] = [a for a in range(4)
                                     if not any(all(t[order.index(x)] != a for x in contacts[r])
                                                for t in grouped)]
                assert len(forbidden[str(r)]) <= len(contacts[r])
            piece["rows"].append({"index": index, "tuples": tuples,
                                  "fibres": fibres, "F": forbidden})
        if one_sided:
            k_vs = sorted(B | ps)
            k_edges = sorted(FRAME | set(internal) | set(attachments))
            k_rot = {str(v): [w for w in rotation[v] if tuple(sorted((v, w))) in k_edges]
                     for v in k_vs}
            _, k_faces = faces_of(k_vs, k_edges, k_rot)
            # Locate the original complement using a retained root--P dart.
            r = owners[0]
            x = contacts[r][0]
            seq = rotation[x]
            pivot = seq.index(r)
            predecessor = next(seq[(pivot - j) % len(seq)] for j in range(1, len(seq) + 1)
                               if tuple(sorted((x, seq[(pivot - j) % len(seq)]))) in k_edges)
            target = next(f for f in k_faces
                          if any((f[j], f[(j + 1) % len(f)]) == (predecessor, x)
                                 for j in range(len(f))))
            boundary_edges = {tuple(sorted((target[j], target[(j + 1) % len(target)])))
                              for j in range(len(target))}
            shield = sorted(FRAME - boundary_edges)
            piece["shield"] = {"complement_face": target, "edges": shield,
                               "length": len(shield)}
            if len(support) >= 2 and B <= set().union(*(adj[v] & B for v in inside)):
                assert set(support) == set().union(*(set(e) for e in shield))
        result.append(piece)
    return result


def joint(vertices, edges, roots, pieces, index, omitted=None):
    row = PATTERNS[index]
    factors, available = {}, {}
    for r in roots:
        fs = [{"name": f"spoke:{r}:{b}", "n": 1, "F": [row[b]]}
              for b in sorted(B) if tuple(sorted((r, b))) in edges]
        fs += [{"name": p["id"], "n": len(p["contacts"][str(r)]),
                "F": p["rows"][index]["F"][str(r)]}
               for p in pieces if p["kind"] == "unary" and r in p["owners"]
               and p["id"] != omitted]
        factors[r] = fs
        available[r] = COL - set().union(*(set(f["F"]) for f in fs))
    pairs, query = [], []
    for a, b in product(range(4), repeat=2):
        pins = dict(zip(roots, (a, b)))
        selected = {}
        for p in pieces:
            if p["id"] == omitted:
                continue
            selected[p["id"]] = p["rows"][index]["fibres"][4 * a + b]["tuple_indices"]
        ok = (a in available[roots[0]] and b in available[roots[1]]
              and all(selected.values()))
        direct = coloring(vertices, edges, dict(enumerate(row)) | pins)
        assert bool(direct) == bool(ok)
        if ok:
            pairs.append([a, b])
        query.append({"pins": [a, b], "tuple_indices": selected,
                      "full_graph_lift": direct[0] if direct else None})
    capacity = []
    if not pairs:
        for r, s in (roots, roots[::-1]):
            if not available[s]:
                capacity.append({"r": r, "s": s, "status": "not triggered",
                                 "missing": ["E_s nonempty"]})
                continue
            for b in sorted(available[s]):
                columns = []
                for p in pieces:
                    if p["kind"] != "mixed":
                        continue
                    bad = [a for a in range(4) if not p["rows"][index]["fibres"][
                        4 * a + b if r == roots[0] else 4 * b + a]["tuple_indices"]]
                    k = len(p["contacts"][str(r)])
                    assert len(bad) <= k
                    columns.append({"piece": p["id"], "k": k, "G": bad})
                V = set().union(*(set(c["G"]) for c in columns))
                A = available[r]
                assert A <= V
                vals = [sum(f["n"] - len(f["F"]) for f in factors[r]),
                        sum(len(f["F"]) for f in factors[r]) - (4 - len(A)),
                        sum(c["k"] - len(c["G"]) for c in columns),
                        sum(len(c["G"]) for c in columns) - len(V), len(V - A)]
                degree = sum(r in e for e in edges)
                assert all(v >= 0 for v in vals) and sum(vals) == degree - 4
                capacity.append({"r": r, "s": s, "b": b, "columns": columns,
                                 "D_O_delta_o_lambda": vals, "rhs": degree - 4,
                                 "status": "triggered and holds"})
    else:
        capacity.append({"status": "not triggered", "missing": ["rejecting complete join"]})
    return {"index": index, "factors": {str(r): factors[r] for r in roots},
            "E": {str(r): sorted(available[r]) for r in roots},
            "root_pairs": pairs, "all_16_fibres": query, "capacity": capacity}


def analyze(path, data):
    vertices = sorted(data["vertices"])
    edges = sorted(tuple(sorted(e)) for e in data["edges"])
    assert len(edges) == len(set(edges)) and all(u != v for u, v in edges)
    assert {e for e in edges if set(e) <= B} == FRAME
    adj = neighbors(vertices, edges)
    roots = sorted(v for v in vertices if v not in B and len(adj[v]) == 5)
    assert len(roots) == 2 and tuple(roots) not in edges
    assert all(len(adj[v]) == 4 for v in vertices if v not in B | set(roots))
    rotation, faces = faces_of(vertices, edges, data["rotation"])
    pieces = pieces_of(vertices, edges, roots, rotation)
    # Recomputed metadata and complete relations are compared to saved data.
    for p, saved in zip(pieces, data["pieces"], strict=True):
        for key in ("vertices", "support", "contacts", "contact_order", "incidences", "kind"):
            assert p[key] == saved[key], (data["id"], p["id"], key)
        for row, old in zip(p["rows"], saved["rows"], strict=True):
            assert [{"tuple": x["tuple"], "lifts": x["full_piece_lifts"]}
                    for x in row["tuples"]] == old["tuples"]
            assert row["fibres"] == old["fibres"]
    joins = [joint(vertices, edges, roots, pieces, i) for i in range(10)]
    sigma = sum(1 << j["index"] for j in joins if j["root_pairs"])
    assert sigma == data["sigma"] and sigma & sum(1 << i for i in T4) == 932
    for j, saved in zip(joins, data["joins"], strict=True):
        assert j["root_pairs"] == saved["root_pairs"]
    m = sum(p["kind"] == "mixed" for p in pieces)
    touch = sorted(set().union(*(adj[v] & B for v in vertices if v not in B)))
    deletions = []
    for e in edges:
        if e in FRAME:
            continue
        cut = [x for x in edges if x != e]
        lifts = [coloring(vertices, cut, dict(enumerate(row))) for row in PATTERNS]
        cut_sigma = sum(1 << i for i, fs in enumerate(lifts) if fs)
        gained = [i for i in range(10) if cut_sigma & (1 << i) and not sigma & (1 << i)]
        assert gained
        deletions.append({"edge": e, "sigma": cut_sigma,
                          "new_rows": [{"index": i, "full_graph_lift": lifts[i][0]} for i in gained]})
    derivative_units = []
    for p in pieces:
        if p["kind"] != "unary" or sum(p["incidences"]) != 1:
            continue
        r = p["owners"][0]
        s = next(x for x in roots if x != r)
        x = p["contacts"][str(r)][0]
        x_vertices = sorted(set(vertices) - set(p["vertices"]))
        x_edges = [e for e in edges if set(e) <= set(x_vertices)]
        cut_edges = [e for e in edges if e != tuple(sorted((r, x)))]
        xs = [joint(x_vertices, x_edges, roots, pieces, i, p["id"]) for i in range(10)]
        x_sigma = sum(1 << j["index"] for j in xs if j["root_pairs"])
        delta = [i for i in range(10) if x_sigma & (1 << i) and not sigma & (1 << i)]
        assert delta
        trichotomies, minimal_rows = [], []
        for i, j in enumerate(xs):
            for fibre in j["all_16_fibres"]:
                pins = dict(zip(roots, fibre["pins"]))
                cut = coloring(vertices, cut_edges, dict(enumerate(PATTERNS[i])) | pins)
                assert bool(cut) == (fibre["full_graph_lift"] is not None)
                fibre["contact_edge_deleted_full_lift"] = cut[0] if cut else None
            if i in delta:
                contact_colors = {t["tuple"][0] for t in p["rows"][i]["tuples"]}
                root_colors = {pins[roots.index(r)] for pins in j["root_pairs"]}
                assert len(contact_colors) == 1 and root_colors == contact_colors
            if not j["root_pairs"]:
                ef = []
                for e in x_edges:
                    if e in FRAME:
                        continue
                    fs = coloring(x_vertices, [ee for ee in x_edges if ee != e],
                                  dict(enumerate(PATTERNS[i])))
                    ef.append({"edge": e, "full_graph_lift": fs[0] if fs else None})
                if all(a["full_graph_lift"] is not None for a in ef):
                    minimal_rows.append({"index": i, "root_degrees": [len(neighbors(x_vertices, x_edges)[a]) for a in roots],
                                         "edge_deletion_lifts": ef})
                Fu = set(p["rows"][i]["F"][str(r)])
                Er = set(j["E"][str(r)])
                placement = "D" if not Fu else ("lambda" if Fu <= Er else "O")
                for old in j["capacity"]:
                    if old.get("r") != r or old["status"] != "triggered and holds":
                        continue
                    new = next(c for c in joins[i]["capacity"]
                               if c.get("r") == r and c.get("b") == old["b"])
                    assert old["D_O_delta_o_lambda"] == [0] * 5
                    wanted = {"D": [1, 0, 0, 0, 0], "O": [0, 1, 0, 0, 0],
                              "lambda": [0, 0, 0, 0, 1]}[placement]
                    assert new["D_O_delta_o_lambda"] == wanted
                    trichotomies.append({"index": i, "r": r, "s": s, "b": old["b"],
                                         "F_U": sorted(Fu), "E_r_X": sorted(Er), "placement": placement,
                                         "X": old["D_O_delta_o_lambda"], "G": new["D_O_delta_o_lambda"]})
        derivative_units.append({"piece": p["id"], "r": r, "s": s, "contact": [r, x],
                                 "vertices_X": x_vertices, "edges_X": x_edges, "epsilon_X": 1,
                                 "sigma_X": x_sigma, "new_rows": delta, "joins_X": xs,
                                 "minimal_rows": minimal_rows, "capacity_placements": trichotomies})
    witnesses = []
    for p in pieces:
        e = tuple(sorted((p["owners"][0], p["contacts"][str(p["owners"][0])][0])))
        deletion = next(d for d in deletions if d["edge"] == e)
        item = deletion["new_rows"][0]
        f = dict(zip(vertices, item["full_graph_lift"]))
        assert f[e[0]] == f[e[1]]
        lists = {v: sorted(COL - {f[w] for w in adj[v] - set(p["vertices"])}) for v in p["vertices"]}
        assert all(len(lists[v]) == len(adj[v] & set(p["vertices"])) for v in p["vertices"])
        outside_path = path_to_frame(p["owners"][0], p["vertices"], vertices, edges)
        witnesses.append({"piece": p["id"], "edge": e, "index": item["index"],
                          "full_edge_deleted_lift": item["full_graph_lift"],
                          "outside_vertices": sorted(set(vertices) - set(p["vertices"])),
                          "outside_lift": [[v, f[v]] for v in vertices if v not in p["vertices"]],
                          "tight_lists": {str(v): lists[v] for v in p["vertices"]},
                          "path_to_frame_avoiding_piece": outside_path})
    low_support = [p["id"] for p in pieces if p["kind"] == "mixed" and sum(p["incidences"]) <= 3
                   and p["one_sided"] and touch == list(range(5))]
    assert all(len(p["support"]) >= 2 for p in pieces if p["id"] in low_support)
    if m == 2 and touch == list(range(5)):
        for i in range(len(pieces)):
            for k in range(i):
                assert not set(map(tuple, pieces[i]["shield"]["edges"])) & set(map(tuple, pieces[k]["shield"]["edges"]))
        assert sum(p["shield"]["length"] for p in pieces) <= 5
    h_vertices = sorted(set(vertices) - B)
    h_edges = [e for e in edges if set(e) <= set(h_vertices)]
    return {"id": data["id"], "source": str(path.relative_to(SOURCE)),
            "source_sha256": sha256(path.read_bytes()).hexdigest(), "vertices": vertices, "edges": edges,
            "root_order": roots, "degrees": [[v, len(adj[v])] for v in vertices], "sigma": sigma,
            "original_H_bridges": bridges(h_vertices, h_edges),
            "touch": touch, "m": m, "u": len(pieces) - m, "rotation": data["rotation"], "faces": faces,
            "pieces": pieces, "joins": joins, "edge_deletions": deletions,
            "piece_rejection_witnesses": witnesses, "unit_derivatives": derivative_units,
            "low_incidence_support_claim_instances": low_support,
            "full_target_coverage": {"status": "not triggered", "missing":
                                     ["complete Sigma=933/941", "simultaneous q0/q1/q3 rejection"]}}


def make_certificate():
    inventory, selected = [], []
    for path in sorted((SOURCE / "artifacts/c5_excess_two_e4c/controls").glob("*.json")):
        data = json.loads(path.read_text())
        adj = neighbors(data["vertices"], data["edges"])
        roots = sorted(v for v in data["vertices"] if v not in B and len(adj[v]) == 5)
        cs = components(set(data["vertices"]) - B - set(roots), adj)
        m = sum(all(adj[r] & set(p) for r in roots) for p in cs)
        unit_cores = [{"index": row["index"], "piece_ids": core["omitted_pieces"],
                       "root_degrees": core["root_degrees"]}
                      for row in data["row_cores"] for core in row["cores"]
                      if core["root_degrees"] in ([4, 5], [5, 4]) and core["omitted_pieces"]]
        inventory.append({"id": data["id"], "m_from_edges": m,
                          "saved_core_root_degrees": [c["root_degrees"] for row in data["row_cores"] for c in row["cores"]],
                          "saved_unit_core_occurrences": unit_cores,
                          "full_color_recalculation_selected": m == 2 or bool(unit_cores)})
        if m == 2 or unit_cores:
            graph = analyze(path, data)
            computed = [(u["piece"], row["index"]) for u in graph["unit_derivatives"]
                        for row in u["minimal_rows"]]
            assert sorted(computed) == sorted((item["piece_ids"][0], item["index"]) for item in unit_cores)
            selected.append(graph)
    masks = []
    for source_mask in (933, 941):
        Q = [q for q, i in enumerate(Q_INDEX) if not source_mask & (1 << i)]
        allowed = [list(qs) for n in (0, 1, 2) for qs in combinations(Q, n)
                   if n < 2 or (qs[1] - qs[0]) % 5 in (1, 4)]
        for beta in Q:
            choices = [qs for qs in allowed if beta in qs]
            masks.append({"sigma_G": source_mask, "beta_singleton_position": beta,
                          "possible_Q_X": choices,
                          "forced_new_rejections_removed_from_G": sorted(set(Q) - set().union(*(set(qs) for qs in choices)))})
    algebra = []
    for contact_palette_size in range(1, 5):
        for ts in combinations(range(4), contact_palette_size):
            F = [a for a in range(4) if all(t == a for t in ts)]
            assert len(F) <= 1
            algebra.append({"T_contact": ts, "F_U": F})
    counts = Counter()
    empty_example = None
    for g in selected:
        counts["graphs"] += 1
        counts["N2_graphs"] += g["m"] == 2
        counts["N1_unary_omission_graphs"] += g["m"] == 1
        counts["original_root_pair_queries"] += 160
        counts["critical_edge_deletions"] += len(g["edge_deletions"])
        counts["low_incidence_support_instances"] += len(g["low_incidence_support_claim_instances"])
        for p in g["pieces"]:
            counts["piece_relations"] += 10
            counts["local_root_pin_fibres"] += 160
            counts["full_piece_lifts"] += sum(len(t["full_piece_lifts"]) for row in p["rows"] for t in row["tuples"])
            if p["kind"] == "unary" and sum(p["incidences"]) == 1:
                for row in p["rows"]:
                    F = row["F"][str(p["owners"][0])]
                    counts["unit_F_empty_rows" if not F else "unit_F_singleton_rows"] += 1
                    if not F and (empty_example is None or (len(p["vertices"]) > 1 and len(empty_example["vertices"]) == 1)):
                        empty_example = {"graph": g["id"], "piece": p["id"], "vertices": p["vertices"],
                                         "index": row["index"], "contact": p["contact_order"],
                                         "tuples_and_full_lifts": row["tuples"], "F_U": []}
        for u in g["unit_derivatives"]:
            counts["unit_derivatives"] += 1
            counts["derivative_root_pair_queries"] += 160
            counts["contact_edge_deleted_root_pair_queries"] += 160
            counts["minimal_unary_omission_rows"] += len(u["minimal_rows"])
            counts["N2_minimal_unary_omission_rows"] += len(u["minimal_rows"]) if g["m"] == 2 else 0
            counts["capacity_placement_instances"] += len(u["capacity_placements"])
            for t in u["capacity_placements"]:
                counts["placement_" + t["placement"]] += 1
        for label, rows in [("G", g["joins"])] + [("X", u["joins_X"]) for u in g["unit_derivatives"]]:
            for row in rows:
                for item in row["capacity"]:
                    counts[f"capacity_{label}_" + item["status"]] += 1
    return {"schema": "n45-u-fixed-controls-v1", "base": BASE, "patterns": PATTERNS,
            "inventory_54": inventory, "graphs": selected, "counts": dict(sorted(counts.items())),
            "e4_u_exact_target_mask_table": masks, "unit_contact_palette_algebra_15": algebra,
            "capacity_one_F_empty_control": empty_example,
            "coverage": {"N45-U-REL_unit_F_capacity": {"status": "triggered and holds", "count": 110},
                         "N45-U-S3_low_incidence_support": {"status": "triggered and holds", "count": 22,
                                                           "missing_for_contradiction_branch": ["no singleton-support instance"]},
                         "N45-U-CAP_unit_budget": {"status": "triggered and holds", "count": 4,
                                                 "scope": "N1 low-degree-side columns, all lambda; N2 rejected derivative absent"},
                         "always_singleton_F_overclaim": {"status": "counterexample", "count": 38,
                                                         "scope": "capacity-one unary has F empty on these rows; no target source counterexample"},
                         "N2_full_target": {"status": "not triggered", "count": 0,
                                              "missing": ["complete Sigma=933/941"]},
                         "N2_unary_omission_45_54": {"status": "not triggered", "count": 0,
                                                     "missing": ["rejecting unit derivative (all N2 unit derivatives accept all ten rows)"]},
                         "two_original_unaries_exclusion": {"status": "not triggered", "count": 0,
                                                            "missing": ["two original unaries and N2 unit-omission rejected row"]}}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--generate", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=HERE / "certificate-final.json")
    args = parser.parse_args()
    manifest = json.loads((HERE / "inputs.json").read_text())
    for item in manifest["base_inputs"]:
        assert sha256((SOURCE / item["path"]).read_bytes()).hexdigest() == item["sha256"]
    result = make_certificate()
    payload = encode(result)
    out = args.output
    if args.generate:
        with out.open("xb") as f:
            f.write(payload)
    else:
        assert out.read_bytes() == payload, "certificate byte/provenance mismatch"
    print(json.dumps({"mode": "generate" if args.generate else "check", "bytes": len(payload),
                      "sha256": sha256(payload).hexdigest(), "counts": result["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
