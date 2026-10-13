#!/usr/bin/env python3
"""Exact, fixed-domain disk controls for cross-spoke full-fibre identities.

--write exclusively creates the local certificate and summary. --check is
read-only, re-enumerates every lift, and compares all cells including empties.
No catalogue-external or globally minimal source is asserted in this domain.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import random

B = tuple(range(5))
C = tuple(range(4))
SEED = None
CELL_DOMAIN = ((0, 0), (0, 1), (1, 0), (1, 1))


def edge(a, b):
    return tuple(sorted((a, b)))


def checked(condition, message):
    if not condition:
        raise ValueError(message)


def normalized(xs):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in xs)


BETAS = tuple(sorted({normalized(t) for t in itertools.product(C, repeat=5)
                      if all(t[i] != t[(i + 1) % 5] for i in B)}))


def lifts(vertices, edges, beta):
    """Direct DFS on the literal graph, retaining the four named colors."""
    adjacency = {x: set() for x in vertices}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    colors = dict(zip(B, beta))
    if any(a in colors and b in colors and colors[a] == colors[b]
           for a, b in edges):
        return []
    free = [x for x in vertices if x not in B]
    palette = list(C)
    if SEED is not None:
        rng = random.Random(SEED)
        rng.shuffle(free)
        rng.shuffle(palette)
    result = []

    def visit(k):
        if k == len(free):
            result.append(tuple(colors[x] for x in vertices))
            return
        x = free[k]
        forbidden = {colors[y] for y in adjacency[x] if y in colors}
        for color in palette:
            if color not in forbidden:
                colors[x] = color
                visit(k + 1)
        colors.pop(x, None)

    visit(0)
    return sorted(result)


def check_disk(vertices, edges, faces):
    """Connected orientable sphere map; deleting the named outer face is a disk."""
    checked(faces[0] == list(reversed(B)), "wrong ordered outer face")
    darts, links = Counter(), {x: {} for x in vertices}
    for face in faces:
        checked(len(face) >= 3, "short face")
        for j, x in enumerate(face):
            prev, nxt = face[j - 1], face[(j + 1) % len(face)]
            checked(x in links and prev not in links[x], "bad vertex link")
            links[x][prev] = nxt
            darts[x, nxt] += 1
    expected = Counter((a, b) for e in edges for a, b in (e, e[::-1]))
    checked(darts == expected, "face darts do not equal graph darts")
    rotations = {}
    for x, link in links.items():
        checked(link and set(link) == set(link.values()), "invalid link permutation")
        start = min(link)
        visited, current = [], start
        while current not in visited:
            visited.append(current)
            current = link[current]
        checked(current == start and len(visited) == len(link), "split vertex link")
        rotations[str(x)] = visited
    seen, pending = set(), [vertices[0]]
    while pending:
        x = pending.pop()
        if x not in seen:
            seen.add(x)
            pending.extend(links[x])
    checked(seen == set(vertices), "disconnected map")
    checked(len(vertices) - len(edges) + len(faces) == 2, "not a sphere map")
    return rotations


def graph_domain():
    """Five declared controls, no graph search or target-source search."""
    yield {"id": "outer_w5", "U": B, "v": 5, "h_vertices": list(B),
           "h_edges": sorted({edge(i, (i + 1) % 5) for i in B}),
           "annular_faces": [], "diagonal_mask": None}
    for mask in (None, 0, 1, 3):
        u = tuple(range(5, 10))
        he = {edge(i, (i + 1) % 5) for i in B}
        he |= {edge(u[i], u[(i + 1) % 5]) for i in B}
        he |= {edge(i, u[i]) for i in B}
        faces = []
        for i in B:
            j = (i + 1) % 5
            a, b, c, d = i, j, u[j], u[i]
            if mask is None:
                faces.append([a, b, c, d])
            elif (mask >> i) & 1:
                he.add(edge(a, c))
                faces.extend([[a, b, c], [a, c, d]])
            else:
                he.add(edge(b, d))
                faces.extend([[a, b, d], [b, c, d]])
        yield {"id": "prism" if mask is None else f"triangulated_{mask:02d}",
               "U": u, "v": 10, "h_vertices": list(range(10)),
               "h_edges": sorted(he), "annular_faces": faces,
               "diagonal_mask": mask}


def kempe_records(cmap, hv, he, u, legal_h):
    """All six color-pair components and every boundary-fixed one-component move."""
    records, reduces = [], []
    rim = tuple(cmap[x] for x in u)
    singleton_vertices = [x for x in u if rim.count(cmap[x]) == 1]
    singleton_pairs = {edge(a, b) for a, b in itertools.combinations(singleton_vertices, 2)
                       if edge(a, b) not in he} if len(set(rim)) == 4 else set()
    blockers = []
    for a, b in itertools.combinations(C, 2):
        allowed = {x for x in hv if cmap[x] in (a, b)}
        adjacency = {x: set() for x in allowed}
        for x, y in he:
            if x in allowed and y in allowed:
                adjacency[x].add(y)
                adjacency[y].add(x)
        components = []
        unseen = set(allowed)
        while unseen:
            todo, found = [min(unseen)], set()
            while todo:
                x = todo.pop()
                if x not in found:
                    found.add(x)
                    todo.extend(adjacency[x])
            unseen -= found
            components.append(sorted(found))
        components.sort()
        moves = []
        for index, component in enumerate(components):
            if set(component).intersection(B):
                continue
            switched = dict(cmap)
            for x in component:
                switched[x] = b if cmap[x] == a else a
            full = tuple(switched[x] for x in hv)
            checked(full in legal_h, "boundary-fixed Kempe move left exact H fibre")
            new_count = len({switched[x] for x in u})
            moves.append({"component_index": index, "switched_H_lift": full,
                          "new_rim_color_count": new_count})
            if len(set(rim)) == 4 and new_count == 3:
                reduces.append({"color_pair": [a, b], "component_index": index,
                                "switched_H_lift": full})
        pair_record = {"colors": [a, b], "components": components,
                       "boundary_fixed_single_component_moves": moves}
        records.append(pair_record)
        for x, y in sorted(singleton_pairs):
            if {cmap[x], cmap[y]} != {a, b}:
                continue
            ix = next(i for i, comp in enumerate(components) if x in comp)
            iy = next(i for i, comp in enumerate(components) if y in comp)
            connected = ix == iy
            both_hit_boundary = bool(set(components[ix]).intersection(B)) and bool(set(components[iy]).intersection(B))
            blockers.append({"singleton_vertices": [x, y], "colors": [a, b],
                             "component_indices": [ix, iy], "connected": connected,
                             "both_components_hit_B": both_hit_boundary,
                             "criterion_allows_reduction": not connected and not both_hit_boundary})
    if len(set(rim)) == 4:
        checked(len(blockers) == 2, "wrong nonadjacent singleton-pair domain")
        checked(bool(reduces) == any(b["criterion_allows_reduction"] for b in blockers),
                "single-move reduction criterion failed")
    return {"color_pair_records": records, "nonadjacent_singleton_pair_checks": blockers,
            "all_rim4_to_rim3_single_moves": reduces}


def graph_record(spec):
    hv, he, u, v = spec["h_vertices"], spec["h_edges"], spec["U"], spec["v"]
    gv = sorted(hv + [v])
    ge = sorted(he + [edge(v, x) for x in u])
    outer = list(reversed(B))
    hf = [outer] + spec["annular_faces"] + [list(u)]
    gf = [outer] + spec["annular_faces"] + [[v, u[i], u[(i + 1) % 5]] for i in B]
    hr, gr = check_disk(hv, he, hf), check_disk(gv, ge, gf)
    checked({x for e in ge if v in e for x in e if x != v} == set(u), "wrong center neighborhood")
    checked({e for e in he if set(e).issubset(u)} ==
            {edge(u[i], u[(i + 1) % 5]) for i in B}, "rim is not induced C5")
    spokes = []
    for i in B:
        removed = edge(v, u[i])
        opposite = [u[(i - 1) % 5], u[(i + 1) % 5]]
        touching = [f for f in gf[1:] if v in f and u[i] in f]
        checked(len(touching) == 2 and all(len(f) == 3 for f in touching), "spoke lacks two triangles")
        checked({x for f in touching for x in f if x not in removed} == set(opposite), "wrong opposite vertices")
        # Delete the two incident triangles and insert their oriented quadrangle.
        minus_faces = [f for f in gf if f not in touching]
        minus_faces.append([v, u[(i - 1) % 5], u[i], u[(i + 1) % 5]])
        minus_edges = [e for e in ge if e != removed]
        spokes.append({"i": i, "edge": removed, "opposite": opposite,
                       "minus_edges": minus_edges, "minus_faces": minus_faces,
                       "minus_rotation": check_disk(gv, minus_edges, minus_faces)})
    record = {"id": spec["id"], "diagonal_mask": spec["diagonal_mask"],
              "B": B, "U": u, "v": v, "fully_internal_w5": set(B).isdisjoint(u),
              "near_triangulated": all(len(f) == 3 for f in gf[1:]),
              "h_vertices": hv, "h_edges": he, "h_faces": hf, "h_rotation": hr,
              "g_vertices": gv, "g_edges": ge, "g_faces": gf, "g_rotation": gr,
              "spokes": spokes, "rows": []}
    for beta in BETAS:
        hs, gs = lifts(hv, he, beta), lifts(gv, ge, beta)
        maps = {h: dict(zip(hv, h)) for h in hs}
        expected_g = []
        for h, cmap in maps.items():
            for color in sorted(set(C) - {cmap[x] for x in u}):
                extended = {**cmap, v: color}
                expected_g.append(tuple(extended[x] for x in gv))
        checked(sorted(expected_g) == gs, "G reconstruction differs from DFS")
        js, projected = [], []
        for spoke in spokes:
            i, (a, b) = spoke["i"], spoke["opposite"]
            direct = lifts(gv, spoke["minus_edges"], beta)
            cells = [[] for _ in CELL_DOMAIN]
            for lift in direct:
                cmap = dict(zip(gv, lift))
                cell = 2 * int(cmap[v] != cmap[u[i]]) + int(cmap[a] != cmap[b])
                cells[cell].append(lift)
            reconstructed = [[] for _ in CELL_DOMAIN]
            for h, cmap in maps.items():
                for color in C:
                    if any(color == cmap[u[j]] for j in B if j != i):
                        continue
                    extended = {**cmap, v: color}
                    cell = 2 * int(color != cmap[u[i]]) + int(cmap[a] != cmap[b])
                    reconstructed[cell].append(tuple(extended[x] for x in gv))
            checked([sorted(cell) for cell in reconstructed] == cells, "J reconstruction differs from direct DFS")
            proj = [[tuple(dict(zip(gv, full))[x] for x in hv) for full in cell]
                    for cell in cells]
            checked(all(len(cell) == len(set(cell)) for cell in proj), "noninjective H projection within a J cell")
            js.append({"i": i, "cells": cells})
            projected.append(proj)
        # Pointwise identities work on all ten rows, regardless of rejection.
        h_records = []
        for h, cmap in maps.items():
            rim = tuple(cmap[x] for x in u)
            ncolors = len(set(rim))
            zeros = [i for i in B if h in projected[i][0]]
            ones = [i for i in B if h in projected[i][1]]
            checked(ncolors in (3, 4), "improper C5 color multiplicities")
            checked(len(zeros) == ncolors - 3 and len(ones) == ncolors - 2,
                    "pointwise cross-edge count identity failed")
            if ncolors == 4:
                k = zeros[0]
                checked(set(ones) == {(k + 2) % 5, (k + 3) % 5}, "wrong three-spoke support")
            three_singleton = [i for i in B if rim.count(rim[i]) == 1] if ncolors == 3 else []
            kempe = kempe_records(cmap, hv, he, u, set(hs))
            if not gs:
                checked(not kempe["all_rim4_to_rim3_single_moves"], "rejected row admits a reducing boundary-fixed Kempe move")
            h_records.append({"h_lift": h, "rim": rim, "rim_color_count": ncolors,
                              "J00_spokes": zeros, "J01_spokes": ones,
                              "rim3_singleton_spokes": three_singleton, "Kempe": kempe})
        # Exact all-row correction: T_i is the three-color-rim singleton part.
        three_parts = [[r["h_lift"] for r in h_records if i in r["rim3_singleton_spokes"]] for i in B]
        for i in B:
            checked(sorted(projected[i][1]) == sorted(projected[(i + 2) % 5][0] +
                                                       projected[(i + 3) % 5][0] + three_parts[i]),
                    "corrected all-row 01 decomposition failed")
        checked(sum(len(proj[1]) - 2 * len(proj[0]) for proj in projected) == len(gs),
                "all-row signed cross-edge count identity failed")
        rejected = not gs
        partitions = [proj[0] for proj in projected]
        rejected_identity = None
        if rejected:
            checked(all(r["rim_color_count"] == 4 for r in h_records), "rejected row has extendible H lift")
            checked(sorted(h for part in partitions for h in part) == hs, "00 cells do not partition H")
            for i in B:
                expected = sorted(partitions[(i + 2) % 5] + partitions[(i + 3) % 5])
                checked(sorted(projected[i][1]) == expected, "rejected-row full-fibre relation failed")
                checked(not js[i]["cells"][2] and not js[i]["cells"][3], "rejected row has a proper G lift")
            rejected_identity = {
                "R00_all_h_lifts": partitions,
                "R01_all_h_lifts": [proj[1] for proj in projected],
                "R00_counts": [len(part) for part in partitions],
                "R01_counts": [len(proj[1]) for proj in projected],
                "score": "triggered and holds" if hs else "not triggered",
                "nonempty_H": bool(hs),
            }
        record["rows"].append({"beta": beta, "h_lifts": hs, "g_lifts": gs,
                               "J": js, "rejected_by_G": rejected,
                               "pointwise_h_records": h_records,
                               "all_row_T_parts": three_parts,
                               "rejected_row_partition": rejected_identity})
    record["sigma_g"] = [bool(row["g_lifts"]) for row in record["rows"]]
    record["sigma_g_integer_in_declared_beta_order"] = sum(int(bit) << i for i, bit in enumerate(record["sigma_g"]))
    return record


def finite_witnesses(graphs):
    domain = {graph["id"]: graph for graph in graphs}
    internal = domain["triangulated_03"]
    row = next(r for r in internal["rows"] if r["beta"] == (0, 1, 2, 1, 2))
    checked(row["rejected_by_G"] and len(row["h_lifts"]) == 4, "wrong disjoint-fibre control")
    parts = row["rejected_row_partition"]["R00_all_h_lifts"]
    checked([len(p) for p in parts] == [0, 1, 1, 1, 1], "wrong rejected 00 partition")
    join = sorted(set(parts[1]).intersection(parts[2]))
    checked(not join, "wrong empty same-H join")
    outer = domain["outer_w5"]
    rejected_supports = [[r["beta"] for r in outer["rows"]
                          if r["rejected_by_G"] and r["J"][i]["cells"][0]] for i in B]
    checked(all(len(s) == 1 for s in rejected_supports), "wrong outer wheel rejected supports")
    checked(len({s[0] for s in rejected_supports}) == 5, "outer wheel has shared rejected 00 row")
    # Same graph, fixed B and color names: normalizing the U colors alone breaks attachments.
    prism = domain["prism"]
    beta = BETAS[0]
    eta = beta + (1, 0, 1, 0, 3)
    prism_row = prism["rows"][0]
    checked(eta in prism_row["h_lifts"], "normalization input is not a full H lift")
    bad = beta + normalized(eta[5:10])
    bad_edges = [e for e in prism["h_edges"] if bad[e[0]] == bad[e[1]]]
    checked(bad_edges and bad not in prism_row["h_lifts"], "normalization did not invalidate attachment")
    rejected_full = row["J"][1]["cells"][0][0]
    checked(rejected_full not in row["J"][2]["cells"][0], "literal full witnesses should differ")
    # The positive synchronized triple has an identical H restriction, but three
    # different assignments at v, each defective at its own deleted edge only.
    point = row["pointwise_h_records"][0]
    eta = point["h_lift"]
    triples = []
    for i in point["J00_spokes"] + point["J01_spokes"]:
        cell = 0 if i in point["J00_spokes"] else 1
        full = next(full for full in row["J"][i]["cells"][cell] if full[:-1] == eta)
        triples.append({"spoke": i, "cell": CELL_DOMAIN[cell], "full_lift": full})
    checked(len({t["full_lift"] for t in triples}) == 3, "synchronized triple wrongly identifies full G-e lifts")
    positive_kempe = next((g, r, h, h["Kempe"]["all_rim4_to_rim3_single_moves"][0])
                          for g in graphs for r in g["rows"] for h in r["pointwise_h_records"]
                          if h["Kempe"]["all_rim4_to_rim3_single_moves"])
    kg, kr, kh, kmove = positive_kempe
    switched = dict(zip(kg["h_vertices"], kmove["switched_H_lift"]))
    missing = sorted(set(C) - {switched[x] for x in kg["U"]})
    checked(len(missing) == 1, "positive Kempe move does not have unique extension")
    extended = {**switched, kg["v"]: missing[0]}
    restored = tuple(extended[x] for x in kg["g_vertices"])
    checked(restored in kr["g_lifts"], "positive Kempe restoration not in direct G fibre")
    return {
        "independent_rejected_00_do_not_share_H": {
            "graph": internal["id"], "beta": row["beta"], "spokes": [1, 2],
            "all_H_lifts": row["h_lifts"], "all_R00_parts": parts,
            "left_full_G_minus_e_lifts": row["J"][1]["cells"][0],
            "right_full_G_minus_e_lifts": row["J"][2]["cells"][0],
            "common_H_restrictions": join, "score": "counterexample",
            "claim_refuted": "nonempty rejected-row 00 witnesses at two spokes imply a shared full H restriction",
        },
        "independent_rejected_rows_do_not_synchronize": {
            "graph": "outer_w5", "all_five_rejected_00_row_supports": rejected_supports,
            "pair_spokes": [0, 1], "common_rejected_rows": [], "score": "counterexample",
            "claim_refuted": "separately witnessed spokes must have a common rejected row",
            "scope": "Wheel rim is the outer boundary, so full internal W5 premise is not triggered.",
        },
        "independent_inner_color_normalization": {
            "graph": "prism", "beta": beta, "legal_H_lift": beta + (1, 0, 1, 0, 3),
            "normalized_U_alone": normalized((1, 0, 1, 0, 3)),
            "incorrect_H_lift": bad, "violated_edges": bad_edges,
            "destination_H_fibre": [], "score": "counterexample",
        },
        "shared_H_does_not_mean_identical_full_lift": {
            "graph": internal["id"], "beta": row["beta"], "shared_H_lift": eta,
            "synchronized_three_spokes": triples, "score": "counterexample",
            "claim_refuted": "a synchronized triple uses an identical full vertex coloring in all three G-e graphs",
        },
        "positive_single_Kempe_move": {
            "graph": kg["id"], "beta": kr["beta"], "H_lift_before": kh["h_lift"],
            "all_pair_components_and_moves": kh["Kempe"], "chosen_move": kmove,
            "restored_full_G_lift": restored, "score": "triggered and holds",
        },
        "rejected_row_single_move_obstructions": {
            "graph": internal["id"], "beta": row["beta"],
            "all_four_H_lifts": [{"H_lift": r["h_lift"],
                                  "two_pair_checks": r["Kempe"]["nonadjacent_singleton_pair_checks"]}
                                 for r in row["pointwise_h_records"]],
            "score": "triggered and holds",
        },
    }


def add_all_degree5_wheels(graph):
    gv, ge, gf = graph["g_vertices"], graph["g_edges"], graph["g_faces"]
    centers = sorted(x for x in gv if x not in B and sum(x in e for e in ge) == 5)
    checked(graph["v"] in centers, "primary center not degree five")
    others = []
    for v in centers:
        if v == graph["v"]:
            continue
        u = list(reversed(graph["g_rotation"][str(v)]))
        hv = [x for x in gv if x != v]
        he = [e for e in ge if v not in e]
        spec = {"id": f"{graph['id']}:center_{v}", "U": tuple(u), "v": v,
                "h_vertices": hv, "h_edges": he,
                "annular_faces": [f for f in gf[1:] if v not in f],
                "diagonal_mask": graph["diagonal_mask"]}
        wheel = graph_record(spec)
        checked(wheel["g_vertices"] == gv and wheel["g_edges"] == ge, "additional wheel changed source graph")
        checked(all(a["g_lifts"] == b["g_lifts"] for a, b in zip(graph["rows"], wheel["rows"])),
                "additional wheel changed full G fibre")
        others.append(wheel)
    graph["other_degree5_wheels"] = others
    graph["all_interior_degree5_centers"] = centers
    checked(len(others) + 1 == len(centers), "missed degree-five center")
    if graph["id"] == "triangulated_00":
        checked(centers == [5, 6, 7, 8, 9, 10], "icosahedral cap lacks six degree-five centers")


def wheels(graph):
    return [graph] + graph["other_degree5_wheels"]


def deduplicate_edge_fibres(graph):
    """Check adjacent-center agreement before replacing duplicate J by references."""
    by_edge = {}
    for wheel in wheels(graph):
        for spoke in wheel["spokes"]:
            i, e = spoke["i"], spoke["edge"]
            rows = [{"beta": row["beta"], "cells": row["J"][i]["cells"]} for row in wheel["rows"]]
            if e in by_edge:
                checked(by_edge[e]["opposite"] == sorted(spoke["opposite"]), "adjacent centers changed opposite pair")
                checked(by_edge[e]["rows"] == rows, "adjacent centers disagree on exact shared-edge fibres")
                by_edge[e]["degree5_centers"].append(wheel["v"])
            else:
                by_edge[e] = {"edge": e, "opposite": sorted(spoke["opposite"]),
                              "degree5_centers": [wheel["v"]], "rows": rows}
    graph["edge_fibres"] = [by_edge[e] for e in sorted(by_edge)]
    for record in graph["edge_fibres"]:
        record["degree5_centers"].sort()
        record["m5"] = len(record["degree5_centers"])
        checked(record["m5"] == len(set(record["edge"]).intersection(graph["all_interior_degree5_centers"])),
                "wrong edge degree-five incidence multiplicity")
    graph["adjacent_degree5_center_edges"] = [r["edge"] for r in graph["edge_fibres"] if r["m5"] == 2]
    global_rows = []
    n5 = len(graph["all_interior_degree5_centers"])
    for row_index, row in enumerate(graph["rows"]):
        terms = [r["m5"] * (len(r["rows"][row_index]["cells"][1]) -
                             2 * len(r["rows"][row_index]["cells"][0])) for r in graph["edge_fibres"]]
        rhs = n5 * len(row["g_lifts"])
        checked(sum(terms) == rhs, "global shared-edge signed identity failed")
        global_rows.append({"beta": row["beta"], "edge_terms_in_edge_fibre_order": terms,
                            "weighted_sum": sum(terms), "n5_times_G_lift_count": rhs})
    graph["global_shared_edge_signed_identity"] = global_rows
    edge_index = {r["edge"]: i for i, r in enumerate(graph["edge_fibres"])}
    for wheel in wheels(graph):
        wheel["J_edge_fibre_indices_in_spoke_order"] = [edge_index[s["edge"]] for s in wheel["spokes"]]
        for row in wheel["rows"]:
            del row["J"]


def build():
    checked(len(BETAS) == 10, "wrong beta domain")
    graphs = [graph_record(spec) for spec in graph_domain()]
    for graph in graphs:
        add_all_degree5_wheels(graph)
    witnesses = finite_witnesses(graphs)
    cert = {
        "schema": "cross-edge-kempe-full-fibres-v1", "colors": C,
        "B": B, "beta_domain": BETAS, "J_cell_domain": CELL_DOMAIN,
        "semantics": "Each graph's edge_fibres[e].rows[p].cells[k] lists every coloring of that literal G-e with fixed beta and named colors. Every wheel maps its ordered spokes to these deduplicated fibres using J_edge_fibre_indices_in_spoke_order. Full vectors use g_vertices; H vectors use that wheel's h_vertices. No independent color normalization or marginal join is used.",
        "fixed_domain": [g["id"] for g in graphs],
        "provenance": "Constructed literal disk controls; no 933/941 source and no global minimality asserted.",
        "graphs": graphs, "witnesses": witnesses,
    }
    all_wheels = [wheel for g in graphs for wheel in wheels(g)]
    for graph in graphs:
        deduplicate_edge_fibres(graph)
    cells = [cell for g in graphs for e in g["edge_fibres"] for row in e["rows"] for cell in row["cells"]]
    h_count = sum(len(row["h_lifts"]) for wheel in all_wheels for row in wheel["rows"])
    rejection_rows = [row for wheel in all_wheels for row in wheel["rows"] if row["rejected_by_G"]]
    triggered = [row for row in rejection_rows if row["h_lifts"]]
    summary = {
        "schema": cert["schema"], "fixed_graph_ids": cert["fixed_domain"],
        "graph_count": len(graphs), "beta_count": len(BETAS), "spokes_per_wheel": 5,
        "total_degree5_wheels": len(all_wheels),
        "deduplicated_original_edges": sum(len(g["edge_fibres"]) for g in graphs),
        "adjacent_degree5_center_edges": sum(len(g["adjacent_degree5_center_edges"]) for g in graphs),
        "explicit_J_cells": len(cells), "empty_J_cells": sum(not cell for cell in cells),
        "complete_J_lifts": sum(len(cell) for cell in cells), "complete_H_lifts": h_count,
        "complete_G_lifts": sum(len(row["g_lifts"]) for g in graphs for row in g["rows"]),
        "rejected_rows": len(rejection_rows), "nonempty_rejected_H_rows": len(triggered),
        "rejected_H_lifts": sum(len(row["h_lifts"]) for row in triggered),
        "all_rows_full_J_reconstruction": {"score": "triggered and holds", "instances": len(all_wheels) * 50},
        "all_H_pointwise_cross_edge_counts": {"score": "triggered and holds", "instances": h_count},
        "global_shared_edge_signed_identity": {"score": "triggered and holds", "instances": len(graphs) * 10},
        "boundary_fixed_Kempe_component_analysis": {"score": "triggered and holds", "instances": h_count * 6},
        "rejected_full_fibre_partition": {"score": "triggered and holds", "instances": len(triggered)},
        "source_minimality_933_941": {"score": "not triggered", "reason": "No control is asserted to realize a globally minimal catalogue-external source."},
        "five_degree_interior_count_at_least_9_or_8": {"score": "not triggered", "reason": "Controls have one or six interior vertices only."},
        "graph_summaries": [{"id": g["id"], "sigma_g": g["sigma_g"],
                             "sigma_g_integer_in_declared_beta_order": g["sigma_g_integer_in_declared_beta_order"],
                             "fully_internal_w5": g["fully_internal_w5"],
                             "all_interior_degree5_centers": g["all_interior_degree5_centers"],
                             "adjacent_degree5_center_edges": g["adjacent_degree5_center_edges"],
                             "near_triangulated": g["near_triangulated"]} for g in graphs],
        "witnesses": witnesses,
        "trust_boundary": ["Exact finite calibration on five declared graphs only", "General theorem needs its paper proof", "No target source realization or exclusion", "No Lean theorem or external theorem verification"],
    }
    return cert, summary


def canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode() + b"\n"


def first_difference(expected, actual, path="$"):
    if type(expected) is not type(actual):
        return f"{path}: type mismatch"
    if isinstance(expected, dict):
        if set(expected) != set(actual):
            return f"{path}: missing or extra keys"
        for key in expected:
            difference = first_difference(expected[key], actual[key], f"{path}.{key}")
            if difference:
                return difference
    elif isinstance(expected, list):
        if len(expected) != len(actual):
            return f"{path}: length {len(actual)}, expected {len(expected)}"
        for i, (a, b) in enumerate(zip(expected, actual)):
            difference = first_difference(a, b, f"{path}[{i}]")
            if difference:
                return difference
    elif expected != actual:
        return f"{path}: value mismatch"
    return None


def main():
    global SEED
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    SEED = args.seed
    output = Path(__file__).resolve().parent
    cert_path = args.certificate or output / "certificate.json.gz"
    summary_path = output / "summary.json"
    checked(not args.write or args.certificate is None, "--write is limited to exclusive local output paths")
    if args.write:
        checked(not cert_path.exists() and not summary_path.exists(), "refusing to overwrite existing outputs")
    cert, summary = build()
    payload = canonical_bytes(cert)
    summary["canonical_certificate_sha256"] = hashlib.sha256(payload).hexdigest()
    if args.write:
        with cert_path.open("xb") as stream:
            stream.write(gzip.compress(payload, compresslevel=9, mtime=0))
        with summary_path.open("x") as stream:
            json.dump(summary, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
    else:
        with gzip.open(cert_path, "rb") as stream:
            actual = json.load(stream)
        difference = first_difference(json.loads(payload), actual)
        checked(difference is None, f"certificate mismatch: {difference}")
        if args.certificate is None:
            with summary_path.open() as stream:
                actual_summary = json.load(stream)
            checked(actual_summary == json.loads(canonical_bytes(summary)), "summary mismatch")
    print(json.dumps({"result": "PASS", "mode": "write" if args.write else "check", "dfs_seed": SEED,
                      **{key: summary[key] for key in (
                          "graph_count", "explicit_J_cells", "empty_J_cells", "complete_J_lifts",
                          "complete_H_lifts", "complete_G_lifts", "nonempty_rejected_H_rows",
                          "rejected_H_lifts", "canonical_certificate_sha256")}}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"FAIL: {error}")
