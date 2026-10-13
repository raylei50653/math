#!/usr/bin/env python3
"""Finite named-interface controls; stdlib only, no source-minimality claim.

--write creates certificate.json.gz and summary.json exclusively.
--check regenerates all controls and compares every cell, including empties.
The index of a cell is its index in the explicit global tau_domain.
"""
import argparse
import gzip
import hashlib
import itertools
import json
import random
from collections import Counter
from pathlib import Path

B = tuple(range(5))
U = tuple(range(5, 10))
V = 10
C = tuple(range(4))
TAUS = tuple(itertools.product(C, repeat=5))
DFS_SEED = None


def edge(a, b):
    return tuple(sorted((a, b)))


def normalized(xs):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in xs)


def cycle_proper(xs):
    return all(xs[i] != xs[(i + 1) % 5] for i in range(5))


BETAS = tuple(sorted({normalized(t) for t in TAUS if cycle_proper(t)}))


def checked(test, message):
    if not test:
        raise ValueError(message)


def enumerate_lifts(vertices, edges, beta):
    """Independent graph DFS with B fixed and all original colour names kept."""
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
    if DFS_SEED is not None:
        rng = random.Random(DFS_SEED)
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


def check_faces(vertices, edges, faces, outer):
    """Certify a connected orientable sphere map with the named outer face.

    Every directed edge occurs once, each vertex link is one cycle, and Euler
    characteristic is two. Deleting the distinguished outer open face yields
    the claimed disk embedding. Lists can contain repeated vertices in general.
    """
    checked(faces[0] == list(outer), "wrong distinguished outer boundary")
    darts = Counter()
    links = {x: {} for x in vertices}
    for face in faces:
        checked(len(face) >= 3, "short face")
        for i, x in enumerate(face):
            prev, nxt = face[i - 1], face[(i + 1) % len(face)]
            checked(x in links, "unknown face vertex")
            checked(prev not in links[x], "duplicate vertex-link input")
            links[x][prev] = nxt
            darts[x, nxt] += 1
    expected = Counter((a, b) for e in edges for a, b in (e, e[::-1]))
    checked(darts == expected, "oriented face darts do not equal edges")
    for x in vertices:
        link = links[x]
        checked(link and set(link) == set(link.values()), "invalid vertex link")
        start = next(iter(link))
        seen, current = set(), start
        while current not in seen:
            seen.add(current)
            current = link[current]
        checked(current == start and len(seen) == len(link), "split vertex link")
    reached, todo = set(), [vertices[0]]
    while todo:
        x = todo.pop()
        if x not in reached:
            reached.add(x)
            todo.extend(links[x])
    checked(reached == set(vertices), "disconnected map")
    checked(len(vertices) - len(edges) + len(faces) == 2, "non-spherical map")
    return {str(x): rotation_cycle(links[x]) for x in vertices}


def rotation_cycle(link):
    start = min(link)
    out, x = [start], link[start]
    while x != start:
        out.append(x)
        x = link[x]
    return out


def graph_domain():
    graphs = []
    for mask in [None] + list(range(32)):
        edges = {edge(i, (i + 1) % 5) for i in B}
        edges |= {edge(5 + i, 5 + (i + 1) % 5) for i in B}
        edges |= {edge(i, 5 + i) for i in B}
        annular_faces = []
        for i in B:
            nxt = (i + 1) % 5
            a, b, c, d = i, nxt, 5 + nxt, 5 + i
            if mask is None:
                annular_faces.append([a, b, c, d])
            elif (mask >> i) & 1:
                edges.add(edge(a, c))
                annular_faces.extend([[a, b, c], [a, c, d]])
            else:
                edges.add(edge(b, d))
                annular_faces.extend([[a, b, d], [b, c, d]])
        graphs.append({
            "id": "prism" if mask is None else f"triangulated_{mask:02d}",
            "mask": mask,
            "h_vertices": list(range(10)),
            "h_edges": sorted(edges),
            "annular_faces": annular_faces,
        })
    # Embed vertex 11 in the first annular quadrangle, adjacent to B0 and U0.
    # Each legal H colouring then has exactly two choices at this vertex.
    decorated = dict(graphs[0])
    decorated.update({
        "id": "prism_decorated",
        "h_vertices": list(range(10)) + [11],
        "h_edges": sorted(set(graphs[0]["h_edges"]) | {edge(0, 11), edge(5, 11)}),
        "annular_faces": [[5, 0, 11], [0, 1, 6, 5, 11]] + graphs[0]["annular_faces"][1:],
    })
    graphs.append(decorated)
    return graphs


def quotient_spec(vertices, edges, j):
    a, b = U[j], U[(j + 2) % 5]
    representative = min(a, b)
    pi = {x: representative if x in (a, b) else x for x in vertices}
    checked(edge(a, b) not in edges, "quotient pair has original edge")
    checked(a not in B and b not in B, "quotient merges outer labels")
    preimages = {}
    for e in edges:
        image = edge(pi[e[0]], pi[e[1]])
        checked(image[0] != image[1], "quotient self-loop")
        preimages.setdefault(image, []).append(e)
    return {
        "j": j,
        "pair": [a, b],
        "vertices": sorted(set(pi.values())),
        "edges": sorted(preimages),
        "map": [[x, pi[x]] for x in vertices],
        "edge_preimages": [{"edge": e, "preimages": preimages[e]} for e in sorted(preimages)],
        "local_embedding": {
            "original_inner_face": list(U),
            "inserted_arc": [a, b],
            "operation": "insert one arc in inner face, contract it, simplify parallel edges",
            "simultaneous_with_other_quotients": False,
        },
    }


def make_graph_record(spec):
    hv, he = spec["h_vertices"], spec["h_edges"]
    gv = sorted(hv + [V])
    ge = sorted(he + [edge(V, u) for u in U])
    outer = list(reversed(B))
    hf = [outer] + spec["annular_faces"] + [list(U)]
    gf = [outer] + spec["annular_faces"] + [[V, U[j], U[(j + 1) % 5]] for j in B]
    hr, gr = check_faces(hv, he, hf, outer), check_faces(gv, ge, gf, outer)
    checked(set(hv).isdisjoint({V}) and set(B).isdisjoint(U), "wheel not fully internal")
    checked({x for e in ge if V in e for x in e if x != V} == set(U), "wrong center neighbors")
    checked(all(edge(U[j], U[(j + 1) % 5]) in he for j in B), "missing wheel rim")
    quotients = [quotient_spec(hv, he, j) for j in B]
    for q in quotients:
        q["rows"] = []
    record = {
        "id": spec["id"], "diagonal_mask": spec["mask"],
        "h_vertices": hv, "h_edges": he, "h_faces": hf, "h_rotation": hr,
        "g_vertices": gv, "g_edges": ge, "g_faces": gf, "g_rotation": gr,
        "rows": [], "quotients": quotients,
    }
    for beta in BETAS:
        h = enumerate_lifts(hv, he, beta)
        direct_g = enumerate_lifts(gv, ge, beta)
        cells = [[] for _ in TAUS]
        reconstructed_g = []
        counts = Counter()
        hmaps = {eta: dict(zip(hv, eta)) for eta in h}
        for eta, eta_map in hmaps.items():
            tau = tuple(eta_map[u] for u in U)
            index = sum(tau[i] * 4 ** (4 - i) for i in B)
            cells[index].append(eta)
            missing = sorted(set(C) - set(tau))
            checked(cycle_proper(tau), "nonproper rim in H lift")
            checked(len(missing) in (0, 1), "wheel missing-color count wrong")
            equal = [int(tau[j] == tau[(j + 2) % 5]) for j in B]
            checked(sum(equal) - 1 == int(bool(missing)), "signed identity failed pointwise")
            checked(sum(equal) == (2 if len(set(tau)) == 3 else 1), "wrong diagonal multiplicity")
            counts[f"rim_{len(set(tau))}_colors"] += 1
            for color in missing:
                extended = dict(eta_map)
                extended[V] = color
                reconstructed_g.append(tuple(extended[x] for x in gv))
        checked(sorted(reconstructed_g) == direct_g, "center reconstruction differs from direct G DFS")
        quotient_counts = []
        for q in quotients:
            qlifts = enumerate_lifts(q["vertices"], q["edges"], beta)
            pi = dict(q["map"])
            pulled = []
            for lift in qlifts:
                colors = dict(zip(q["vertices"], lift))
                pulled.append(tuple(colors[pi[x]] for x in hv))
            a, b = q["pair"]
            filtered = [eta for eta in h if hmaps[eta][a] == hmaps[eta][b]]
            checked(sorted(pulled) == filtered, "direct quotient does not pull back bijectively")
            checked(len(set(pulled)) == len(qlifts), "noninjective quotient pullback")
            q["rows"].append({"beta": beta, "lifts": qlifts})
            quotient_counts.append(len(qlifts))
        checked(len(direct_g) == sum(quotient_counts) - len(h), "row signed count failed")
        record["rows"].append({
            "beta": beta, "cells": cells, "g_lifts": direct_g,
            "h_count": len(h), "g_count": len(direct_g),
            "quotient_counts": quotient_counts, "rim_color_counts": dict(sorted(counts.items())),
        })
    record["sigma_h"] = [bool(row["h_count"]) for row in record["rows"]]
    record["sigma_g"] = [bool(row["g_count"]) for row in record["rows"]]
    return record


def chord_controls():
    proper = [t for t in TAUS if cycle_proper(t)]
    three = [t for t in proper if len(set(t)) == 3]
    four = [t for t in proper if len(set(t)) == 4]
    shapes = sorted({normalized(t) for t in three})
    checked(len(shapes) == 5 and len(three) == len(four) == 120, "wrong C5 tuple counts")
    shape_records = []
    for shape in shapes:
        checked(sorted(Counter(shape).values()) == [1, 2, 2], "wrong three-color shape")
        shape_records.append({
            "shape": shape,
            "multiplicities": sorted(Counter(shape).values()),
            "equal_diagonals": [j for j in B if shape[j] == shape[(j + 2) % 5]],
            "literal_color_assignments": sum(normalized(t) == shape for t in three),
        })
    replacements = []
    for mask in range(32):
        selected = [j for j in B if mask & (1 << j)]
        accepted = [t for t in proper if all(t[j] != t[(j + 2) % 5] for j in selected)]
        lost = sorted(set(three) - set(accepted))
        extra = sorted(set(accepted) - set(three))
        checked(lost or extra, "unexpected exact chord-only replacement")
        replacements.append({
            "mask": mask, "chords": [[U[j], U[(j + 2) % 5]] for j in selected],
            "accepted_count": len(accepted), "lost_three_color_count": len(lost),
            "extra_four_color_count": len(extra),
            "lost_witness": lost[0] if lost else None,
            "extra_witness": extra[0] if extra else None,
            "score": "counterexample",
        })
    return {
        "proper_tuple_count": len(proper), "three_color_tuple_count": len(three),
        "four_color_tuple_count": len(four), "three_color_shapes": shape_records,
        "chord_only_replacements": replacements,
        "scope": "All 32 subsets of the five U diagonals; even nonplanar subsets admitted as a superdomain. Compares exact U predicates, not merely outer projections.",
    }


def finite_witnesses(graphs):
    by_id = {g["id"]: g for g in graphs}
    first, second = by_id["prism"], by_id["triangulated_01"]
    checked(first["sigma_h"] == second["sigma_h"], "projection witness H masks differ")
    checked(first["sigma_g"] != second["sigma_g"], "projection witness G masks equal")
    differing = [i for i in range(10) if first["sigma_g"][i] != second["sigma_g"][i]]
    row_i = differing[0]
    second_h = [eta for cell in second["rows"][row_i]["cells"] for eta in cell]
    beta = BETAS[0]
    eta = tuple(beta) + (1, 0, 1, 0, 3)
    wrong_tau = normalized(eta[5:10])
    wrong_eta = tuple(beta) + wrong_tau
    legal_h = {lift for cell in first["rows"][0]["cells"] for lift in cell}
    checked(eta in legal_h and wrong_eta not in legal_h, "bad independent-normalization witness")
    wrong_index = sum(wrong_tau[i] * 4 ** (4 - i) for i in B)
    checked(not first["rows"][0]["cells"][wrong_index], "normalization destination cell not empty")
    bad_edges = [e for e in first["h_edges"] if wrong_eta[e[0]] == wrong_eta[e[1]]]
    four_eta = next(lift for lift in sorted(legal_h) if len(set(lift[5:10])) == 4)
    diagonal = next(j for j in B if four_eta[5 + j] == four_eta[5 + (j + 2) % 5])
    decorated = by_id["prism_decorated"]
    multiple = next((i, ti, cell) for i, row in enumerate(decorated["rows"])
                    for ti, cell in enumerate(row["cells"]) if len(cell) > 1)
    checked(len(multiple[2]) == 2, "decoration multiplicity should be two")
    join_row = second["rows"][0]
    join_h = [lift for cell in join_row["cells"] for lift in cell]
    left = sorted(lift for lift in join_h if lift[6] == lift[8])
    right = sorted(lift for lift in join_h if lift[7] == lift[9])
    checked(left and right and not set(left).intersection(right), "bad projected pair-join witness")
    return {
        "outer_projection_loss": {
            "graphs": [first["id"], second["id"]], "sigma_h": first["sigma_h"],
            "sigma_g": [first["sigma_g"], second["sigma_g"]],
            "differing_beta_indices": differing, "witness_beta": BETAS[row_i],
            "first_graph_g_lift": first["rows"][row_i]["g_lifts"][0],
            "second_graph_all_h_lifts_at_witness_beta": second_h,
            "score": "counterexample",
            "candidate": "Sigma(H) alone determines Sigma(H plus the named center)",
        },
        "independent_u_normalization": {
            "graph": "prism", "beta": beta, "legal_h_lift": eta,
            "legal_g_lift": eta + (2,), "normalized_u_alone": wrong_tau,
            "incorrect_h_lift": wrong_eta, "violated_edges": bad_edges,
            "destination_full_cell": [], "score": "counterexample",
        },
        "four_color_rim_branch": {
            "graph": "prism", "beta": beta, "h_lift": four_eta,
            "equal_diagonal_j": diagonal, "missing_center_colors": [],
            "candidate": "a legal single-pair quotient guarantees center extension",
            "score": "counterexample",
        },
        "nontrivial_full_fibre": {
            "graph": "prism_decorated", "beta": BETAS[multiple[0]],
            "tau": TAUS[multiple[1]], "all_h_lifts": multiple[2],
        },
        "separate_quotient_row_join": {
            "graph": second["id"], "beta": beta, "diagonal_indices": [1, 2],
            "left_all_h_lifts": left, "right_all_h_lifts": right,
            "common_h_lifts": [], "score": "counterexample",
            "candidate": "separate accepted quotient rows imply a common full H lift",
            "geometry_scope": "Each single-pair quotient is legal; no simultaneous quotient is asserted.",
        },
    }


def build():
    checked(len(BETAS) == 10, "wrong outer row domain")
    graphs = [make_graph_record(spec) for spec in graph_domain()]
    certificate = {
        "schema": "w5-named-full-fibres-v1",
        "provenance": "Constructed literal disk controls; no globally minimal-source identity asserted.",
        "B": B, "U": U, "v": V, "colors": C,
        "beta_domain": BETAS, "tau_domain": TAUS,
        "cell_semantics": "rows[i].cells[j] is exactly J_beta_domain[i](tau_domain[j]); every cell exists, including empties; vectors follow each graph's h_vertices.",
        "signed_identity": "For every full H lift eta: sum_j [eta(u_j)=eta(u_(j+2))] - 1 = [eta extends to v]; when extendible the center color is unique.",
        "graphs": graphs, "rim_and_chord_controls": chord_controls(),
        "witnesses": finite_witnesses(graphs),
    }
    h_count = sum(row["h_count"] for graph in graphs for row in graph["rows"])
    g_count = sum(row["g_count"] for graph in graphs for row in graph["rows"])
    cell_count = len(graphs) * len(BETAS) * len(TAUS)
    nonempty = sum(bool(cell) for graph in graphs for row in graph["rows"] for cell in row["cells"])
    summary = {
        "schema": certificate["schema"], "graph_count": len(graphs),
        "beta_count": len(BETAS), "tau_count": len(TAUS),
        "explicit_cell_count": cell_count, "empty_cell_count": cell_count - nonempty,
        "nonempty_cell_count": nonempty, "complete_h_lift_count": h_count,
        "complete_g_lift_count": g_count,
        "literal_quotient_count": len(graphs) * 5,
        "complete_quotient_lift_count": sum(sum(row["quotient_counts"]) for graph in graphs for row in graph["rows"]),
        "center_reconstruction": {"score": "triggered and holds", "instances": len(graphs) * 10},
        "pointwise_signed_identity": {"score": "triggered and holds", "instances": h_count},
        "direct_quotient_pullback": {"score": "triggered and holds", "instances": len(graphs) * 50},
        "rim_shapes": certificate["rim_and_chord_controls"]["three_color_shapes"],
        "chord_only_exact_replacements": 0, "chord_only_candidates": 32,
        "source_minimality": {"score": "not triggered", "reason": "No constructed control is admitted as a globally minimal source."},
        "witnesses": certificate["witnesses"],
        "limits": ["Finite calibration only", "No general reducibility conclusion", "No Lean verification", "No simultaneous quotient embedding is claimed"],
    }
    return certificate, summary


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
        for index, (a, b) in enumerate(zip(expected, actual)):
            difference = first_difference(a, b, f"{path}[{index}]")
            if difference:
                return difference
    elif expected != actual:
        return f"{path}: value mismatch"
    return None


def main():
    global DFS_SEED
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--seed", type=int, help="shuffle DFS order; canonical certificate remains invariant")
    args = parser.parse_args()
    DFS_SEED = args.seed
    output = Path(__file__).resolve().parent
    certificate_path = args.certificate or output / "certificate.json.gz"
    summary_path = output / "summary.json"
    checked(not args.write or args.certificate is None, "--write uses exclusive local output paths only")
    if args.write:
        checked(not certificate_path.exists() and not summary_path.exists(), "refusing to overwrite existing certificate or summary")
    certificate, summary = build()
    payload = canonical_bytes(certificate)
    summary["canonical_certificate_sha256"] = hashlib.sha256(payload).hexdigest()
    if args.write:
        with certificate_path.open("xb") as destination:
            destination.write(gzip.compress(payload, compresslevel=9, mtime=0))
        with summary_path.open("x") as destination:
            json.dump(summary, destination, ensure_ascii=False, indent=2, sort_keys=True)
            destination.write("\n")
    else:
        with gzip.open(certificate_path, "rb") as source:
            actual = json.load(source)
        expected = json.loads(payload)
        difference = first_difference(expected, actual)
        checked(difference is None, f"certificate mismatch: {difference}")
        if args.certificate is None:
            with summary_path.open() as source:
                actual_summary = json.load(source)
            expected_summary = json.loads(canonical_bytes(summary))
            checked(actual_summary == expected_summary, "summary differs from regenerated result")
    print(json.dumps({
        "result": "PASS", "mode": "write" if args.write else "check",
        "dfs_seed": DFS_SEED,
        **{key: summary[key] for key in (
            "graph_count", "explicit_cell_count", "empty_cell_count",
            "complete_h_lift_count", "complete_g_lift_count",
            "literal_quotient_count", "complete_quotient_lift_count",
            "canonical_certificate_sha256")},
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"FAIL: {error}")
