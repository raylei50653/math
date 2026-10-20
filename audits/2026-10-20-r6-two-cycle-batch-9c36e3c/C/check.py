#!/usr/bin/env python3
"""Exact replay on seven fixed plane controls; no R6 source enumeration."""
import argparse
import gzip
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "9c36e3c4789dfec07d60ec4e042f0bafe17451d1"
PRIOR = "audits/2026-10-20-r6-two-cycle-repair-9c36e3c"


def frozen(path):
    manifest = json.loads((ROOT / "INPUTS.json").read_text())
    assert manifest["base"] == BASE
    row = next(r for r in manifest["inputs"] if r["path"] == path)
    data = (ROOT / "frozen" / path).read_bytes()
    assert hashlib.sha256(data).hexdigest() == row["sha256"]
    assert len(data) == row["bytes"]
    return data


frozen(PRIOR + "/C/check.py")
module = importlib.util.spec_from_file_location(
    "fixed_prior_controls", ROOT / "frozen" / PRIOR / "C/check.py")
old = importlib.util.module_from_spec(module)
module.loader.exec_module(old)


def normalized(value):
    return json.loads(json.dumps(value))


def primal_data(control):
    faces = control["sphere_faces"]
    edge_faces = {}
    for i, face in enumerate(faces):
        for edge in old.cycle_edges(face):
            edge_faces.setdefault(edge, []).append(i)
    assert all(len(v) == 2 for v in edge_faces.values())
    primal = {e: tuple(v) for e, v in edge_faces.items()}
    triangles = {}
    for v in range(7 + control["outer_length"]):
        incident = [e for e in primal if v in e]
        triangle = sorted({a for e in incident for a in primal[e]})
        assert len(triangle) == 3
        assert len(incident) == 3
        triangles[v] = triangle
    return primal, triangles, [len(face) for face in faces]


def recover_cut(primal, difference):
    spin = {0: 0}
    todo = [0]
    while todo:
        a = todo.pop()
        for e, (u, v) in primal.items():
            if a not in (u, v):
                continue
            b = v if a == u else u
            value = spin[a] ^ int(e in difference)
            if b in spin:
                assert spin[b] == value
            else:
                spin[b] = value
                todo.append(b)
    assert len(spin) == len({v for e in primal.values() for v in e})
    side = sorted(v for v in spin if spin[v])
    other = sorted(v for v in spin if not spin[v])
    minimal = min((side, other), key=lambda x: (len(x), x))
    assert {e for e, (a, b) in primal.items() if (a in side) != (b in side)} == difference
    return side, minimal


def component_certificate(primal, degrees, matching, cycles):
    vertices = set(range(len(degrees)))
    comps = sorted(old.components(vertices, {primal[e] for e in matching}), key=min)
    owner = {v: i for i, comp in enumerate(comps) for v in comp}
    charges = [sum(degrees[v] for v in comp) % 2 for comp in comps]
    tree_edges = []
    for cycle in cycles:
        pairs = {old.edge(owner[primal[e][0]], owner[primal[e][1]])
                 for e in old.cycle_edges(cycle)}
        assert len(pairs) == 1
        pair = next(iter(pairs))
        assert pair[0] != pair[1]
        tree_edges.append(pair)
    assert len(set(tree_edges)) == len(tree_edges)
    assert len(tree_edges) == len(comps) - 1
    assert len(old.components(range(len(comps)), set(tree_edges))) == 1
    circle_rows = []
    for i, pair in enumerate(tree_edges):
        sides = old.components(range(len(comps)), set(tree_edges) - {pair})
        assert len(sides) == 2
        side = next(c for c in sides if pair[0] in c)
        charge = sum(charges[j] for j in side) % 2
        assert charge == len(cycles[i]) % 2
        circle_rows.append({
            "cycle_index": i, "incident_components": pair,
            "side_components": sorted(side), "side_degree_charge": charge,
            "whole_cycle_length": len(cycles[i]),
        })
    assert (all(c == 0 for c in charges)
            == all(len(c) % 2 == 0 for c in cycles))
    return {
        "components": [{"vertices": sorted(comp),
                        "original_degree_sum": sum(degrees[v] for v in comp),
                        "charge": charge} for comp, charge in zip(comps, charges)],
        "region_tree": circle_rows,
        "all_component_charges_even": all(c == 0 for c in charges),
    }


def safe_pair_audit(control, primal, triangles, degrees, matching, row_by_edges):
    labels = control["literal_primal_labels"]
    if labels is None:
        return []
    components = old.components(range(len(degrees)), {primal[e] for e in matching})
    tree = next(c for c in components if labels["v"] in c)
    rim = next(c for c in components if labels["m"] in c)
    centre = next(c for c in components if c != tree and c != rim)
    assert labels["w"] in tree and labels["z"] in rim
    assert len(centre) == 2
    assert [sum(degrees[v] for v in comp) % 2 for comp in (tree, rim, centre)] == [1, 0, 1]
    colour = {v: int(v not in rim) for v in range(len(degrees))}
    assert all((e in matching) == (colour[a] == colour[b])
               for e, (a, b) in primal.items())
    bad = {v: [t for t, triangle in triangles.items()
               if v in triangle and sum(colour[x] == colour[v] for x in triangle) == 1]
           for v in range(len(degrees))}
    for v in range(len(degrees)):
        p_degree = sum(v in primal[e] for e in matching)
        assert len(bad[v]) == degrees[v] - 2 * p_degree
    safe = [next(v for v in primal[e] if v not in centre) for e in ((4, 5), (5, 6))]
    p_edges = {primal[e] for e in matching}
    all_primal_edges = set(primal.values())
    rows = []
    for rho in safe:
        assert rho in rim
        assert any(rho in ends and bool(set(ends) & centre) for ends in all_primal_edges)
        for tau in sorted(tree - {labels["v"], labels["w"]}):
            shared_edges = [e for e, ends in primal.items() if set(ends) == {rho, tau}]
            if not shared_edges:
                continue
            shared_triangles = [t for t, triangle in triangles.items()
                                if {rho, tau} <= set(triangle)]
            rotation_pass = set(bad[rho] + bad[tau]) <= set(shared_triangles)
            cut = {e for e, ends in primal.items() if len(set(ends) & {rho, tau}) == 1}
            candidate = frozenset(matching ^ cut)
            index = row_by_edges.get(candidate)
            assert rotation_pass == (index is not None)
            if rotation_pass:
                assert not (cut & {tuple(e) for e in control["marks"]})
                assert len(bad[rho]) + len(bad[tau]) == len(shared_triangles)
            residuals = []
            for component, removed, opposite in ((tree, tau, rho), (rim, rho, tau)):
                remaining = component - {removed}
                induced = {e for e in p_edges if set(e) <= remaining}
                for part in old.components(remaining, induced):
                    touched = any(opposite in e and bool(set(e) & part) for e in all_primal_edges)
                    residuals.append({
                        "from": "T" if component == tree else "U0",
                        "vertices": sorted(part), "touched": touched,
                        "original_degree_sum": sum(degrees[v] for v in part),
                        "charge": sum(degrees[v] for v in part) % 2})
            untouched_even = all(r["charge"] == 0 for r in residuals if not r["touched"])
            if rotation_pass:
                assert untouched_even == (control["matching_rows"][index]["oddness"] == 0)
            rows.append({
                "rho": rho, "tau": tau, "original_degrees": [degrees[rho], degrees[tau]],
                "bad_corners": [bad[rho], bad[tau]], "shared_triangles": shared_triangles,
                "shared_dual_edges": shared_edges, "rotation_pass": rotation_pass,
                "matching_row": index, "residual_components": residuals,
                "all_untouched_even": untouched_even,
            })
    return rows


def augment(control):
    primal, triangles, degrees = primal_data(control)
    matching = {tuple(e) for e in control["M"]}
    edges = set(primal)
    row_by_edges = {frozenset(map(tuple, row["edges"])): row["index"]
                    for row in control["matching_rows"]}
    spoke_fibres = {"".join(bits): [] for bits in itertools.product("01", repeat=5)}
    for row in control["matching_rows"]:
        candidate = {tuple(e) for e in row["edges"]}
        side, minimal = recover_cut(primal, matching ^ candidate)
        row["primal_cut_anchored_at_face0"] = side
        row["primal_cut_minimum_side"] = minimal
        row["primal_components"] = component_certificate(
            primal, degrees, candidate, row["complement_cycles"])
        mask = "".join(str(int(old.edge(a, b) in candidate))
                       for a, b in zip(old.PORTS, control["outer_ports"]))
        row["retained_spoke_mask"] = mask
        spoke_fibres[mask].append(row["index"])
    # Exhaust every subset modulo complement on this fixed graph.  Entry k
    # encodes X={i+1: bit i of k}; None means a monochromatic primal triangle.
    cut_fibres = []
    rejection_histogram = {}
    for mask in range(1 << (len(degrees) - 1)):
        side = {i for i in range(1, len(degrees)) if mask & (1 << (i - 1))}
        boundary = {e for e, (a, b) in primal.items() if (a in side) != (b in side)}
        candidate = matching ^ boundary
        bad = [v for v in triangles if sum(v in e for e in candidate) != 1]
        assert all(sum(v in e for e in candidate) == 3 for v in bad)
        if bad:
            cut_fibres.append(None)
            rejection_histogram[len(bad)] = rejection_histogram.get(len(bad), 0) + 1
        else:
            index = row_by_edges[frozenset(candidate)]
            cut_fibres.append(index)
            assert side == set(control["matching_rows"][index]["primal_cut_anchored_at_face0"])
    assert sorted(i for i in cut_fibres if i is not None) == list(range(len(row_by_edges)))
    joint = [row for row in control["matching_rows"]
             if row["joint_admissible"] and not row["oddness"]]
    singletons = [row["index"] for row in joint
                  if len(row["primal_cut_minimum_side"]) == 1]
    minsize = min((len(row["primal_cut_minimum_side"]) for row in joint), default=None)
    pairs = [row for row in joint if len(row["primal_cut_minimum_side"]) == 2]
    pair_rows = []
    for row in pairs:
        x = row["primal_cut_minimum_side"]
        pair_edges = [e for e, ends in primal.items() if set(ends) == set(x)]
        singleton_status = []
        for a in x:
            boundary = {e for e, ends in primal.items() if a in ends}
            candidate = matching ^ boundary
            valid = frozenset(candidate) in row_by_edges
            singleton_status.append({"vertex": a, "matching": valid,
                                     "row_index": row_by_edges.get(frozenset(candidate))})
        pair_rows.append({"row_index": row["index"], "vertices": x,
                          "shared_dual_edges": pair_edges,
                          "shared_edge_in_M": [e in matching for e in pair_edges],
                          "singleton_flips": singleton_status})
    control.update(
        primal_edges=[{"dual_edge": e, "primal_edge": ends} for e, ends in sorted(primal.items())],
        primal_triangles={str(k): v for k, v in triangles.items()},
        original_primal_degrees=degrees,
        parallel_primal_edge_pairs=[
            [a, b] for a, b in itertools.combinations(sorted(primal), 2)
            if set(primal[a]) == set(primal[b])],
        original_primal_components=component_certificate(
            primal, degrees, matching, control["old_complement_cycles"]),
        complete_spoke_mask_fibres=spoke_fibres,
        all_anchored_cut_masks_to_matching_rows=cut_fibres,
        rejected_cut_bad_triangle_histogram=rejection_histogram,
        joint_even_singleton_rows=singletons,
        joint_even_pair_rows=pair_rows,
        minimum_joint_even_cut_size=minsize,
        safe_pair_audit=safe_pair_audit(
            control, primal, triangles, degrees, matching, row_by_edges),
    )
    return control


def expected():
    prior = json.loads(frozen(PRIOR + "/C/certificate-v2.json"))
    keys = ("name", "outer_length", "outer_ports", "outer_chords", "chord_sides", "marks")
    controls = []
    for control in prior["controls"]:
        replay = old.compute_control({k: control[k] for k in keys})
        assert normalized(replay) == control
        controls.append(replay)
    specs = [
        {"name": "literal_both_outside_blocked", "outer_length": 15,
         "outer_ports": [7, 8, 9, 11, 13],
         "outer_chords": [[10, 15], [16, 21], [17, 19], [18, 20], [12, 14]],
         "chord_sides": ["outside", "cap", "cap", "outside", "outside"],
         "marks": [[18, 20], [1, 2], [16, 21]]},
        {"name": "literal_parity_and_outside_blocked", "outer_length": 13,
         "outer_ports": [7, 8, 9, 13, 15],
         "outer_chords": [[10, 12], [11, 18], [17, 19], [14, 16]],
         "chord_sides": ["cap", "outside", "cap", "outside"],
         "marks": [[11, 18], [1, 2], [17, 19]]},
        {"name": "literal_both_parity_blocked", "outer_length": 15,
         "outer_ports": [7, 8, 9, 13, 17],
         "outer_chords": [[10, 12], [11, 20], [19, 21], [14, 16], [15, 18]],
         "chord_sides": ["cap", "outside", "cap", "cap", "outside"],
         "marks": [[11, 20], [1, 2], [19, 21]]},
    ]
    controls.extend(old.compute_control(spec) for spec in specs)
    controls = [augment(control) for control in controls]
    for control in controls[4:]:
        assert control["literal_primal_labels"] is not None
        assert control["source_failure_faces"]
        assert control["minimum_joint_even_cut_size"] == 2
        assert not control["joint_even_singleton_rows"]
        assert any(row["marked_type"] == "101" and row["oddness"] == 0
                   for row in control["matching_rows"])
        for walk in control["monotone_intervals"]:
            assert walk["status"] == "outside_chord_blocker" or (
                walk["mark_safe"] and walk["oddness"] == 2)
    assert all(not row["singleton_flips"][0]["matching"]
               and not row["singleton_flips"][1]["matching"]
               for row in controls[4]["joint_even_pair_rows"])
    first = controls[4]
    central = [r for r in first["safe_pair_audit"] if r["tau"] == 8]
    assert {r["rho"] for r in central} == {5, 6}
    assert all(r["original_degrees"] == [5, 5] and r["rotation_pass"]
               and not r["all_untouched_even"] for r in central)
    assert all(first["matching_rows"][r["matching_row"]]["oddness"] == 2 for r in central)
    first["degree555_double_pair_obstruction"] = {
        "safe_rim_vertices": [5, 6], "outer_third_vertex": 8,
        "original_degrees": [5, 5, 5],
        "T_without_tau": [
            {"vertices": [7, 12], "original_degree_sum": 13, "charge": 1},
            {"vertices": [9], "original_degree_sum": 3, "charge": 1}],
        "pair_matching_rows": [r["matching_row"] for r in central],
        "both_pair_oddness": [2, 2],
        "scope": "local degree555 holds; other low-degree vertices prevent R6 source authority",
    }
    return {
        "schema": 1, "base": BASE,
        "authority": "seven fixed plane cubic controls; exhaustive matching and cut fibres",
        "source_realizability": "not triggered",
        "new_lean_theorem": False,
        "controls": controls,
        "totals": {
            "controls": len(controls),
            "perfect_matchings": sum(len(c["matching_rows"]) for c in controls),
            "anchored_primal_cut_masks": sum(len(c["all_anchored_cut_masks_to_matching_rows"])
                                             for c in controls),
            "complete_spoke_mask_fibres": 32 * len(controls),
            "complete_marked_matching_fibres": 8 * len(controls),
            "safe_adjacent_pair_tests": sum(len(c["safe_pair_audit"]) for c in controls),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=HERE / "certificate.json.gz")
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()
    data = expected()
    if args.write:
        payload = (json.dumps(data, indent=2, sort_keys=True) + "\n").encode()
        if args.write.suffix == ".gz":
            payload = gzip.compress(payload, mtime=0)
        with args.write.open("xb") as stream:
            stream.write(payload)
        print("EXCLUSIVE CREATE PASS")
        return
    payload = args.certificate.read_bytes()
    if args.certificate.suffix == ".gz":
        payload = gzip.decompress(payload)
    actual = json.loads(payload)
    assert actual == normalized(data), "certificate differs from complete exact replay"
    print(json.dumps({
        "status": "PASS", "source_realizability": "not triggered", **data["totals"],
        "new_controls": [
            {"name": c["name"], **c["counts"],
             "minimum_joint_even_cut_size": c["minimum_joint_even_cut_size"],
             "pair_rows": c["joint_even_pair_rows"]} for c in data["controls"][4:]],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
