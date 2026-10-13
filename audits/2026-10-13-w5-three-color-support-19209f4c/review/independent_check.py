#!/usr/bin/env python3
"""Independent stdlib enumeration of the W5 three-colour support controls.

No primary/old checker is imported or executed. Graphs are rebuilt below from
the prism, diagonal-mask, and decorated-prism mathematical specifications.
All assignments are Cartesian products, not the primary's recursive DFS.
The input certificate is only compared after independent reconstruction.
"""
import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parents[1]
COLORS = tuple(range(4))
B = tuple(range(5))
U = tuple(range(5, 10))
CENTER = 10
TAUS = tuple(itertools.product(COLORS, repeat=5))
TAU_INDEX = {tau: i for i, tau in enumerate(TAUS)}
PERMUTATIONS = tuple(itertools.permutations(COLORS))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def json_form(obj):
    return json.loads(json.dumps(obj))


def cycle_proper(word):
    return all(a != b for a, b in zip(word, word[1:] + word[:1]))


LITERAL_BETAS = tuple(t for t in TAUS if cycle_proper(t))
# Orbit minima under *global* permutations, independently of first-use naming.
BETAS = tuple(sorted({min(tuple(p[c] for c in t) for p in PERMUTATIONS)
                      for t in LITERAL_BETAS}))


def unordered_edge(a, b):
    return (min(a, b), max(a, b))


def graph_specifications():
    answer = []
    for mask in [None] + list(range(32)):
        edges = set()
        for ring in (B, U):
            edges.update(unordered_edge(ring[i], ring[(i + 1) % 5])
                         for i in range(5))
        edges.update(zip(B, U))
        faces = []
        for i in range(5):
            k = (i + 1) % 5
            if mask is None:
                faces.append([B[i], B[k], U[k], U[i]])
            elif mask & (1 << i):
                edges.add(unordered_edge(B[i], U[k]))
                faces += [[B[i], B[k], U[k]], [B[i], U[k], U[i]]]
            else:
                edges.add(unordered_edge(B[k], U[i]))
                faces += [[B[i], B[k], U[i]], [B[k], U[k], U[i]]]
        answer.append(("prism" if mask is None else "triangulated_%02d" % mask,
                       mask, list(range(10)), sorted(edges), faces))
    plain = answer[0]
    answer.append(("prism_decorated", None, list(range(10)) + [11],
                   sorted(plain[3] + [(0, 11), (5, 11)]),
                   [[5, 0, 11], [0, 1, 6, 5, 11]] + plain[4][1:]))
    return answer


def embedding_rotation(vertices, edges, faces):
    """Use face permutation and edge reversal to recover vertex orbits.

Face cycles exhaust each dart once. The permutation F o reversal has one
orbit for every named vertex. Connectivity and Euler 2 certify the sphere
map; the distinguished outside and inside boundaries fix the disk slot.
"""
    require(faces[0] == [4, 3, 2, 1, 0], "outer B face changed")
    darts = {(a, b) for x, y in edges for a, b in ((x, y), (y, x))}
    require(len(darts) == 2 * len(edges), "edge repeats/loops")
    successor = {}
    for face in faces:
        require(len(face) >= 3, "short face")
        for i, x in enumerate(face):
            dart = (x, face[(i + 1) % len(face)])
            nxt = (face[(i + 1) % len(face)], face[(i + 2) % len(face)])
            require(dart not in successor, "duplicate oriented face edge")
            successor[dart] = nxt
    require(set(successor) == darts == set(successor.values()), "face darts differ")
    rotation = {d: successor[(d[1], d[0])] for d in darts}
    vertex_cycles = {}
    for x in vertices:
        outgoing = {d for d in darts if d[0] == x}
        require(outgoing, "isolated embedding vertex")
        start = min(outgoing)
        orbit, dart = [], start
        while dart not in orbit:
            require(dart[0] == x, "rotation changes vertex")
            orbit.append(dart)
            dart = rotation[dart]
        require(dart == start and set(orbit) == outgoing, "split vertex link")
        vertex_cycles[str(x)] = [d[1] for d in orbit]
    reached = {vertices[0]}
    while True:
        expanded = reached | {b for a, b in darts if a in reached}
        if expanded == reached:
            break
        reached = expanded
    require(reached == set(vertices), "disconnected embedding")
    require(len(vertices) - len(edges) + len(faces) == 2, "Euler characteristic != 2")
    return vertex_cycles


def enumerate_assignments(vertices, edges, beta):
    """Direct products over every free vertex, testing literal original edges."""
    positions = {x: i for i, x in enumerate(vertices)}
    require(vertices[:5] == list(B), "enumerator expects B in initial positions")
    constraints = [(positions[a], positions[b]) for a, b in edges]
    lifts = []
    for rest in itertools.product(COLORS, repeat=len(vertices) - 5):
        candidate = tuple(beta) + rest
        if all(candidate[a] != candidate[b] for a, b in constraints):
            lifts.append(candidate)
    return lifts


def is_proper(vertices, edges, assignment):
    if len(assignment) != len(vertices) or not set(assignment) <= set(COLORS):
        return False
    coloring = dict(zip(vertices, assignment))
    return all(coloring[a] != coloring[b] for a, b in edges)


def reconstruct_graph(spec):
    name, mask, hv, he, annular_faces = spec
    gv = sorted(hv + [CENTER])
    ge = sorted(he + [unordered_edge(u, CENTER) for u in U])
    hf = [[4, 3, 2, 1, 0]] + annular_faces + [list(U)]
    gf = [[4, 3, 2, 1, 0]] + annular_faces + [
        [CENTER, U[i], U[(i + 1) % 5]] for i in range(5)]
    require(set(B).isdisjoint(U) and CENTER not in hv, "slot labels overlap")
    require({e for e in he if set(e) <= set(U)} ==
            {unordered_edge(U[i], U[(i + 1) % 5]) for i in range(5)},
            "U is not an induced C5")
    result = dict(id=name, diagonal_mask=mask,
                  h_vertices=hv, h_edges=he, h_faces=hf,
                  h_rotation=embedding_rotation(hv, he, hf),
                  g_vertices=gv, g_edges=ge, g_faces=gf,
                  g_rotation=embedding_rotation(gv, ge, gf), rows=[])
    support = []
    for bi, beta in enumerate(BETAS):
        h = enumerate_assignments(hv, he, beta)
        g = enumerate_assignments(gv, ge, beta)
        cells = [[] for _ in TAUS]
        for eta in h:
            cells[TAU_INDEX[eta[5:10]]].append(eta)
        r3 = [ti for ti, tau in enumerate(TAUS) if cells[ti] and len(set(tau)) == 3]
        support += [[bi, ti] for ti in r3]
        reconstructed = []
        for ti in r3:
            missing = (set(COLORS) - set(TAUS[ti])).pop()
            for eta in cells[ti]:
                mapping = dict(zip(hv, eta))
                mapping[CENTER] = missing
                reconstructed.append(tuple(mapping[x] for x in gv))
        require(sorted(reconstructed) == g, name + ": direct center extension differs")
        require(bool(r3) == bool(g), name + ": R3 projection differs from Sigma(G)")
        result["rows"].append(dict(beta=beta, cells=cells, g_lifts=g,
                                   h_count=len(h), g_count=len(g), r3_tau_indices=r3))
    result["r3_support"] = support
    result["full_support"] = [[bi, ti] for bi, row in enumerate(result["rows"])
                              for ti, cell in enumerate(row["cells"]) if cell]
    result["sigma_h"] = [bool(row["h_count"]) for row in result["rows"]]
    result["sigma_g"] = [bool(row["g_count"]) for row in result["rows"]]
    return result


def compare_graphs(expected, certificate, old=False):
    require(len(certificate["graphs"]) == len(expected), "wrong graph count")
    for key, wanted in (("B", B), ("U", U), ("v", CENTER), ("colors", COLORS),
                        ("beta_domain", BETAS), ("tau_domain", TAUS)):
        require(certificate[key] == json_form(wanted), "wrong global " + key)
    for want, got in zip(expected, certificate["graphs"]):
        for key, value in want.items():
            if old and key in ("r3_support", "full_support"):
                continue
            if key == "rows":
                require(len(got[key]) == len(BETAS), "wrong row count")
                for bi, (wr, gr) in enumerate(zip(value, got[key])):
                    for rk, rv in wr.items():
                        if old and rk == "r3_tau_indices":
                            continue
                        require(gr[rk] == json_form(rv),
                                "%s beta%d: %s mismatch" % (want["id"], bi, rk))
            else:
                require(got[key] == json_form(value), want["id"] + ": " + key + " mismatch")


def pair_audit(graphs):
    pairs, selectors, count = [], [], 0
    for left, right in itertools.combinations(graphs, 2):
        equal_r3 = left["r3_support"] == right["r3_support"]
        equal_sigma = left["sigma_g"] == right["sigma_g"]
        require(not equal_r3 or equal_sigma, "sufficiency failed")
        pairs.append(dict(graphs=[left["id"], right["id"]], equal_r3=equal_r3,
                          equal_sigma_g=equal_sigma,
                          implication_score="triggered and holds" if equal_r3 else "not triggered"))
        if not equal_r3:
            continue
        for source, target in ((left, right), (right, left)):
            rows = []
            for bi, sr in enumerate(source["rows"]):
                transfers = []
                for source_lift in sr["g_lifts"]:
                    source_map = dict(zip(source["g_vertices"], source_lift))
                    tau = tuple(source_map[u] for u in U)
                    ti = TAU_INDEX[tau]
                    target_h = min(target["rows"][bi]["cells"][ti])
                    target_map = dict(zip(target["h_vertices"], target_h))
                    target_map[CENTER] = source_map[CENTER]
                    target_g = tuple(target_map[x] for x in target["g_vertices"])
                    require(target_g in target["rows"][bi]["g_lifts"], "selector not a target G lift")
                    require(all(source_map[x] == target_map[x] for x in B + U + (CENTER,)),
                            "selector changes named pin/center/color")
                    transfers.append(dict(source_g_lift=source_lift, tau_index=ti,
                                          target_h_lift=target_h, target_g_lift=target_g))
                    count += 1
                rows.append(dict(beta_index=bi, transfers=transfers))
            selectors.append(dict(source_graph=source["id"], target_graph=target["id"],
                                  rows=rows, score="triggered and holds"))
    return dict(unordered_distinct_pair_count=len(pairs), pairs=pairs,
                equal_r3_pair_count=sum(p["equal_r3"] for p in pairs),
                directional_selectors=selectors, selector_lift_instances=count)


def full_literal_frame_audit(graphs):
    require(len(LITERAL_BETAS) == 240 and len(BETAS) == 10, "wrong C5 orbits")
    expanded_h, expanded_g, direct_rows = 0, 0, 0
    for graph in graphs:
        h_by_beta, g_by_beta = {}, {}
        for row in graph["rows"]:
            h = [eta for cell in row["cells"] for eta in cell]
            for permutation in PERMUTATIONS:
                beta = tuple(permutation[c] for c in row["beta"])
                require(beta not in h_by_beta, "canonical beta orbits overlap")
                h_by_beta[beta] = sorted(tuple(permutation[c] for c in eta) for eta in h)
                g_by_beta[beta] = sorted(tuple(permutation[c] for c in eta) for eta in row["g_lifts"])
                for eta in h_by_beta[beta]:
                    require(eta[:5] == beta and is_proper(graph["h_vertices"], graph["h_edges"], eta),
                            "global permutation invalidates H or B")
                for eta in g_by_beta[beta]:
                    require(eta[:5] == beta and is_proper(graph["g_vertices"], graph["g_edges"], eta),
                            "global permutation invalidates G or B")
        require(set(h_by_beta) == set(LITERAL_BETAS), "literal beta coverage incomplete")
        expanded_h += sum(map(len, h_by_beta.values()))
        expanded_g += sum(map(len, g_by_beta.values()))
        if graph["id"] in ("prism", "triangulated_01"):
            for beta in LITERAL_BETAS:
                require(h_by_beta[beta] == enumerate_assignments(graph["h_vertices"], graph["h_edges"], beta),
                        "literal frame H differs from direct enumeration")
                require(g_by_beta[beta] == enumerate_assignments(graph["g_vertices"], graph["g_edges"], beta),
                        "literal frame G differs from direct enumeration")
                direct_rows += 1
    return dict(literal_beta_count=240, global_permutation_count=24,
                expanded_h_lifts=expanded_h, expanded_g_lifts=expanded_g,
                independently_enumerated_literal_rows=direct_rows)


def independent_negative_audit(graphs):
    lookup = {g["id"]: g for g in graphs}
    prism, tri, uniform, decorated = [lookup[x] for x in
        ("prism", "triangulated_01", "triangulated_00", "prism_decorated")]
    require(prism["sigma_h"] == tri["sigma_h"] and prism["sigma_g"] != tri["sigma_g"],
            "outer H projection negative not triggered")
    differences = [i for i in range(10) if prism["sigma_g"][i] != tri["sigma_g"][i]]
    require(differences == [6, 7], "outer projection witness changed")
    require(prism["sigma_g"] == uniform["sigma_g"] and
            prism["r3_support"] != uniform["r3_support"], "Sigma converse negative not triggered")
    require(prism["r3_support"] == decorated["r3_support"], "decorated R3 changed")
    require(all(len(b) == 2 * len(a) for x, y in zip(prism["rows"], decorated["rows"])
                for a, b in zip(x["cells"], y["cells"])), "decorated multiplicity not two")
    legal_h = (0, 1, 0, 1, 2, 1, 0, 1, 0, 3)
    bad_h = (0, 1, 0, 1, 2, 0, 1, 0, 1, 2)
    require(legal_h in prism["rows"][0]["cells"][TAU_INDEX[legal_h[5:10]]], "normalization source absent")
    require(not prism["rows"][0]["cells"][TAU_INDEX[bad_h[5:10]]], "normalization destination nonempty")
    bad_edges = [list(e) for e in prism["h_edges"] if bad_h[e[0]] == bad_h[e[1]]]
    require(bad_edges == [[i, i + 5] for i in B], "normalization violated edges differ")
    four = (0, 1, 0, 1, 2, 1, 0, 1, 2, 3)
    require(four in prism["rows"][0]["cells"][TAU_INDEX[four[5:10]]] and
            four[5] == four[7] and len(set(four[5:10])) == 4, "single equality negative absent")
    lifts = [eta for cell in tri["rows"][0]["cells"] for eta in cell]
    left = [eta for eta in lifts if eta[6] == eta[8]]
    right = [eta for eta in lifts if eta[7] == eta[9]]
    require(left and right and not set(left).intersection(right), "mixed equality negative absent")
    require((0, 274) not in map(tuple, prism["r3_support"]) and
            [0, 275] in prism["r3_support"] and [1, 274] in prism["r3_support"],
            "beta/tau marginal negative absent")
    require(len(set(TAUS[274])) == 3 and cycle_proper(TAUS[274]), "marginal target malformed")
    return dict(outer_projection_difference_beta_indices=differences,
                same_sigma_different_r3_graphs=["prism", "triangulated_00"],
                same_sigma_different_r3_sizes=[len(prism["r3_support"]), len(uniform["r3_support"])],
                same_r3_different_fibre_multiplicity_graphs=["prism", "prism_decorated"],
                decorated_fibre_multiplier=2,
                normalization_violated_edges=bad_edges,
                separate_equality_left_lifts=left, separate_equality_right_lifts=right,
                marginal_false_cell=[0, 274], marginal_true_cells=[[0, 275], [1, 274]],
                counterexample_count=7)


def validate_supplied_witnesses(graphs, certificate, old_certificate):
    """Validate recorded witness payloads against independently rebuilt cells."""
    lookup = {g["id"]: g for g in graphs}
    witnesses = certificate["witnesses"]
    # The concrete old witnesses were independently checked above; require that
    # their recorded arrays and labels are precisely those controls as well.
    for name, original in old_certificate["witnesses"].items():
        for key, value in original.items():
            require(witnesses[name][key] == value, "inherited witness changed: " + name + "." + key)
    def cell_record(graph, item, h_key="h_lift", g_key="g_lift"):
        bi, ti = item["beta_index"], item["tau_index"]
        require(0 <= bi < 10 and 0 <= ti < 1024, "witness index outside domain")
        row = graph["rows"][bi]
        require(tuple(item[h_key]) in row["cells"][ti], "witness H lift outside named cell")
        require(tuple(item[g_key]) in row["g_lifts"], "witness G lift absent")
        gm = dict(zip(graph["g_vertices"], item[g_key]))
        hm = dict(zip(graph["h_vertices"], item[h_key]))
        require(tuple(gm[u] for u in U) == TAUS[ti] and
                all(gm[x] == hm[x] for x in graph["h_vertices"]), "H/G witness pin mismatch")
        require(set(TAUS[ti]) == set(COLORS) - {gm[CENTER]}, "witness center color mismatch")
    a = witnesses["sigma_not_r3"]
    left, right = [lookup[name] for name in a["graphs"]]
    require(a["sigma_g"] == left["sigma_g"] == right["sigma_g"], "Sigma witness mismatch")
    require(a["r3_support_sizes"] == [len(left["r3_support"]), len(right["r3_support"])],
            "support-size witness mismatch")
    item = a["distinguishing"]
    bi, ti = item["beta_index"], item["tau_index"]
    require(item["beta"] == list(BETAS[bi]) and item["tau"] == list(TAUS[ti]), "Sigma witness frame mismatch")
    require(not item["absent_full_cell"] and not lookup[item["absent_graph"]]["rows"][bi]["cells"][ti],
            "Sigma witness empty cell mismatch")
    cell_record(lookup[item["present_graph"]], item, "present_h_lift", "present_g_lift")
    m = witnesses["beta_tau_marginal_mix"]
    graph = lookup[m["graph"]]
    bi, ti = m["fake_beta_index"], m["fake_tau_index"]
    require(m["fake_beta"] == list(BETAS[bi]) and m["fake_tau"] == list(TAUS[ti]), "marginal frame mismatch")
    require(not m["fake_full_cell"] and not graph["rows"][bi]["cells"][ti], "marginal fake cell is present")
    require(m["actual_beta_witness"]["beta_index"] == bi and
            m["actual_tau_witness"]["tau_index"] == ti, "marginal witnesses have wrong projections")
    cell_record(graph, m["actual_beta_witness"])
    cell_record(graph, m["actual_tau_witness"])
    s = witnesses["support_not_full_lifts"]
    base, decorated = [lookup[name] for name in s["graphs"]]
    require(s["r3_equal"] and base["r3_support"] == decorated["r3_support"] and
            s["full_support_equal"] and base["full_support"] == decorated["full_support"],
            "multiplicity witness support mismatch")
    require(s["all_nonempty_cell_multiplicity_ratio"] == 2, "wrong multiplicity ratio")
    w = s["witness"]
    bi, ti = w["beta_index"], w["tau_index"]
    require(w["beta"] == list(BETAS[bi]) and w["tau"] == list(TAUS[ti]), "multiplicity frame mismatch")
    for name, graph in (("base", base), ("decorated", decorated)):
        require(w[name + "_h_lifts"] == json_form(graph["rows"][bi]["cells"][ti]), "multiplicity H lifts mismatch")
        glifts = [eta for eta in graph["rows"][bi]["g_lifts"]
                  if tuple(dict(zip(graph["g_vertices"], eta))[u] for u in U) == TAUS[ti]]
        require(w[name + "_g_lifts_at_cell"] == json_form(glifts), "multiplicity G lifts mismatch")
    require(witnesses["r3_vs_full_support"]["score"] == "not triggered" and
            witnesses["r3_vs_full_support"]["equal_r3_pair_count"] == 1 and
            not witnesses["r3_vs_full_support"]["unequal_full_support_pairs"],
            "original-domain nontrigger status changed")
    for key in ("sigma_not_r3", "beta_tau_marginal_mix", "support_not_full_lifts"):
        require(witnesses[key]["score"] == "counterexample", "wrong negative status")


def validate_frame_certificate(certificate, frame):
    record = certificate["color_frame_transports"]
    expected = []
    for literal in LITERAL_BETAS:
        candidates = [(bi, p) for bi, beta in enumerate(BETAS) for p in PERMUTATIONS
                      if tuple(p[c] for c in beta) == literal]
        require(len(candidates) == 1, "literal outer frame transporter ambiguous")
        bi, p = candidates[0]
        expected.append(dict(literal_beta=literal, beta_index=bi, canonical_to_literal=p))
    require(record["records"] == json_form(expected), "global color transport records differ")
    require(record["literal_beta_count"] == 240 and record["canonical_beta_count"] == 10 and
            record["global_h_lift_instances"] == frame["expanded_h_lifts"] and
            record["global_g_lift_instances"] == frame["expanded_g_lifts"] and
            record["score"] == "triggered and holds", "global transport summary differs")


def supplementary_audit(path):
    """Second implementation of the separate two-spoke/exterior-apex pair."""
    raw = json.loads(path.read_text())
    require(raw["schema"] == "w5-three-support-supplementary-strictness-v1", "wrong supplement schema")
    for key, value in (("B", B), ("U", U), ("center", CENTER), ("colors", COLORS),
                       ("beta_domain", BETAS), ("tau_domain", TAUS)):
        require(raw[key] == json_form(value), "supplement frame mismatch: " + key)
    require(len(raw["graphs"]) == 2, "wrong supplement graph count")
    cycle_edges = {unordered_edge(ring[i], ring[(i + 1) % 5])
                   for ring in (B, U) for i in range(5)}
    graphs = []
    for apex, supplied in zip((False, True), raw["graphs"]):
        hv = list(range(10)) + ([11] if apex else [])
        he = cycle_edges | {(0, 5), (1, 6)} | ({(u, 11) for u in U} if apex else set())
        annular = [[0, 1, 6, 5]]
        if apex:
            annular += [[1, 2, 3, 4, 0, 5, 11, 6], [11, 5, 9],
                        [11, 9, 8], [11, 8, 7], [11, 7, 6]]
        else:
            annular += [[1, 2, 3, 4, 0, 5, 9, 8, 7, 6]]
        graph = reconstruct_graph(("two_spoke_external_apex" if apex else "two_spoke",
                                   None, hv, sorted(he), annular))
        graph["h_faces"] = [graph["h_faces"][0], graph["h_faces"][-1]] + graph["h_faces"][1:-1]
        for key in ("id", "h_vertices", "h_edges", "h_faces", "g_vertices", "g_edges", "g_faces"):
            require(supplied[key] == json_form(graph[key]), "supplement graph metadata mismatch: " + key)
        require(len(supplied["rows"]) == 10, "supplement row count mismatch")
        for expected_row, supplied_row in zip(graph["rows"], supplied["rows"]):
            for key in ("beta", "cells", "g_lifts", "h_count", "g_count"):
                require(supplied_row[key] == json_form(expected_row[key]), "supplement full row mismatch: " + key)
        for kind in ("h", "g"):
            vertices, edges = graph[kind + "_vertices"], graph[kind + "_edges"]
            for deleted in vertices:
                remaining = set(vertices) - {deleted}
                reached = {min(remaining)}
                while True:
                    addition = {v for edge in edges if deleted not in edge and set(edge) & reached for v in edge}
                    if addition <= reached:
                        break
                    reached |= addition
                require(reached == remaining, "supplement has a cut vertex")
            geometry = dict(darts=2 * len(edges), euler_characteristic=2, two_connected=True,
                            rotation=graph[kind + "_rotation"], score="triggered and holds")
            require(supplied[kind + "_geometry"] == geometry, "supplement geometry mismatch")
        graphs.append(graph)
    pairs = pair_audit(graphs)
    require(pairs["equal_r3_pair_count"] == 1, "supplement R3 differs")
    totals = []
    for graph in graphs:
        totals.append(dict(id=graph["id"], support=len(graph["full_support"]), R3=len(graph["r3_support"]),
                           R4=len(graph["full_support"]) - len(graph["r3_support"]),
                           h_lifts=sum(row["h_count"] for row in graph["rows"]),
                           g_lifts=sum(row["g_count"] for row in graph["rows"]), sigma_g=graph["sigma_g"]))
    require(totals[0]["R4"] == 700 and totals[1]["R4"] == 0, "supplement four-color strictness absent")
    summary = raw["summary"]
    require(summary["graphs"] == totals and summary["explicit_cells"] == 20480 and
            summary["R3_equal"] and not summary["full_support_equal"] and
            summary["geometry"] == "triggered and holds" and summary["strictness"] == "counterexample",
            "supplement summary mismatch")
    transfers = [dict(source=direction["source_graph"], target=direction["target_graph"],
                      complete_g_lifts=sum(len(r["transfers"]) for r in direction["rows"]),
                      score="triggered and holds") for direction in pairs["directional_selectors"]]
    require(summary["transfers"] == transfers, "supplement selector count mismatch")
    witness = summary["witness"]
    require(witness["beta"] == list(BETAS[0]) and witness["tau"] == [1, 0, 1, 2, 3],
            "supplement strictness witness labels differ")
    ti = TAU_INDEX[tuple(witness["tau"])]
    require(witness["first_fibre"] == json_form(graphs[0]["rows"][0]["cells"][ti]) and
            witness["second_fibre"] == [] == graphs[1]["rows"][0]["cells"][ti],
            "supplement strictness witness cells differ")
    return dict(graph_count=2, embedding_count=4, explicit_cell_count=20480,
                empty_cell_count=sum(not cell for g in graphs for r in g["rows"] for cell in r["cells"]),
                complete_h_lift_count=2100, complete_g_lift_count=1400,
                graphs=totals, directional_selector_lift_instances=pairs["selector_lift_instances"],
                score="triggered and holds", sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primary", type=Path, default=HERE / "controls/certificate.json.gz")
    parser.add_argument("--old", type=Path, default=HERE / "frozen/audits/2026-10-12-w5-marked-relation-e299ae98/controls/certificate.json.gz")
    parser.add_argument("--supplement", type=Path, default=HERE / "review/strict_support.json")
    args = parser.parse_args()
    graphs = [reconstruct_graph(spec) for spec in graph_specifications()]
    certificate = json.load(gzip.open(args.primary, "rt"))
    require(certificate["schema"] == "w5-three-color-support-v1", "wrong certificate schema")
    compare_graphs(graphs, certificate)
    old_certificate = json.load(gzip.open(args.old, "rt"))
    compare_graphs(graphs, old_certificate, old=True)
    pairs = pair_audit(graphs)
    require(certificate["pair_controls"] == json_form(pairs), "pair controls/selectors mismatch")
    negative = independent_negative_audit(graphs)
    validate_supplied_witnesses(graphs, certificate, old_certificate)
    frame = full_literal_frame_audit(graphs)
    validate_frame_certificate(certificate, frame)
    supplementary = supplementary_audit(args.supplement)
    cells = [cell for graph in graphs for row in graph["rows"] for cell in row["cells"]]
    summary = dict(schema="w5-three-color-support-independent-v1", score="triggered and holds",
                   primary_sha256=hashlib.sha256(args.primary.read_bytes()).hexdigest(),
                   graph_count=len(graphs), embedding_count=2 * len(graphs),
                   beta_count=len(BETAS), tau_count=len(TAUS),
                   explicit_cell_count=len(cells), empty_cell_count=sum(not c for c in cells),
                   complete_h_lift_count=sum(map(len, cells)),
                   complete_g_lift_count=sum(row["g_count"] for g in graphs for row in g["rows"]),
                   r3_support_pair_count=sum(len(g["r3_support"]) for g in graphs),
                   compared_distinct_graph_pairs=len(pairs["pairs"]),
                   equal_r3_distinct_graph_pairs=pairs["equal_r3_pair_count"],
                   directional_selector_lift_instances=pairs["selector_lift_instances"],
                   literal_frame=frame, negative_controls=negative, supplementary=supplementary,
                   limitations=["34 constructed controls, no globally minimal-source admission",
                                "No general small representative constructed",
                                "No Lean verification; no finite-to-universal inference"])
    print(json.dumps(summary, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
