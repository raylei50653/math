#!/usr/bin/env python3
"""Independent exact replay of the frozen local 5/5/5 odd-branch control.

Only the frozen sphere rotation, edges, matching and literal marks are inputs.
No prior checker is imported.  Every matching and every primal cut is rebuilt.
"""
import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "9c36e3c4789dfec07d60ec4e042f0bafe17451d1"
PRIOR = "audits/2026-10-20-r6-two-cycle-batch-9c36e3c"


def frozen(path):
    manifest = json.loads((ROOT / "INPUTS.json").read_text())
    assert manifest["base"] == BASE
    entry = next(row for row in manifest["inputs"] if row["path"] == path)
    data = (ROOT / "frozen" / path).read_bytes()
    assert len(data) == entry["bytes"]
    assert hashlib.sha256(data).hexdigest() == entry["sha256"]
    return data


def edge(a, b):
    return tuple(sorted((a, b)))


def cycle_edges(cycle):
    return {edge(a, b) for a, b in zip(cycle, cycle[1:] + cycle[:1])}


def canonical_cycle(cycle, reverse=True):
    seqs = [cycle, list(reversed(cycle))] if reverse else [cycle]
    return min(tuple(seq[i:] + seq[:i]) for seq in seqs for i in range(len(seq)))


def components(vertices, edges):
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    pending = set(vertices)
    result = []
    while pending:
        start = min(pending)
        todo = [start]
        found = {start}
        while todo:
            for other in adjacency[todo.pop()] - found:
                found.add(other)
                todo.append(other)
        pending -= found
        result.append(found)
    return result


def two_factor_cycles(vertices, edges, spanning=True):
    adjacency = {v: sorted(b if a == v else a for a, b in edges if v in (a, b))
                 for v in vertices}
    assert all(len(a) == 2 or (not spanning and not a) for a in adjacency.values())
    cycles = []
    pending = {v for v, a in adjacency.items() if a}
    while pending:
        start = min(pending)
        previous = None
        current = start
        cycle = []
        while True:
            cycle.append(current)
            pending.remove(current)
            following = next(v for v in adjacency[current] if v != previous)
            previous, current = current, following
            if current == start:
                break
        cycles.append(list(canonical_cycle(cycle)))
    return sorted(cycles)


def enumerate_matchings(vertices, edges):
    adjacency = {v: sorted(b if a == v else a for a, b in edges if v in (a, b))
                 for v in vertices}
    result = []

    def recurse(remaining, chosen):
        if not remaining:
            result.append(tuple(sorted(chosen)))
            return
        first = min(remaining)
        for second in adjacency[first]:
            if second in remaining:
                recurse(remaining - {first, second}, chosen + [edge(first, second)])

    recurse(set(vertices), [])
    assert len(result) == len(set(result))
    return sorted(result)


def reconstruct(control):
    rotation = {int(k): v for k, v in control["sphere_rotation"].items()}
    vertices = sorted(rotation)
    edges = {tuple(e) for e in control["edges"]}
    assert all(len(neighbors) == len(set(neighbors)) == 3 for neighbors in rotation.values())
    assert {edge(a, b) for a, ns in rotation.items() for b in ns} == edges
    assert all(a in rotation[b] for a, ns in rotation.items() for b in ns)
    pending = {(a, b) for a, b in edges} | {(b, a) for a, b in edges}
    faces = []
    while pending:
        start = min(pending)
        dart = start
        face = []
        while True:
            pending.remove(dart)
            a, b = dart
            face.append(a)
            neighbors = rotation[b]
            dart = (b, neighbors[(neighbors.index(a) + 1) % 3])
            if dart == start:
                break
        assert len(face) == len(set(face))
        faces.append(list(canonical_cycle(face, reverse=False)))
    # Keep literal frozen face numbering, while independently checking every face.
    assert sorted(map(tuple, faces)) == sorted(canonical_cycle(f, reverse=False)
                                             for f in control["sphere_faces"])
    faces = control["sphere_faces"]
    assert len(vertices) - len(edges) + len(faces) == 2
    primal = {e: tuple(i for i, face in enumerate(faces) if e in cycle_edges(face))
              for e in edges}
    assert all(len(ends) == 2 for ends in primal.values())
    triangles = {v: sorted({f for e, fs in primal.items() if v in e for f in fs})
                 for v in vertices}
    assert all(len(t) == 3 for t in triangles.values())
    degrees = list(map(len, faces))
    assert degrees == control["original_primal_degrees"]
    assert [{"dual_edge": list(e), "primal_edge": list(primal[e])} for e in sorted(edges)] \
        == control["primal_edges"]
    assert {str(v): t for v, t in triangles.items()} == control["primal_triangles"]
    return vertices, edges, faces, primal, triangles, degrees


def component_data(vertices, primal, degrees, matching, cycles):
    comps = components(range(len(degrees)), [primal[e] for e in matching])
    owner = {v: i for i, comp in enumerate(comps) for v in comp}
    charges = [sum(degrees[v] for v in c) % 2 for c in comps]
    tree_edges = []
    for cycle in cycles:
        incident = {edge(owner[primal[e][0]], owner[primal[e][1]])
                    for e in cycle_edges(cycle)}
        assert len(incident) == 1
        a, b = next(iter(incident))
        assert a != b
        tree_edges.append((a, b))
    assert len(tree_edges) == len(set(tree_edges)) == len(comps) - 1
    assert len(components(range(len(comps)), tree_edges)) == 1
    tree = []
    for index, pair in enumerate(tree_edges):
        shores = components(range(len(comps)), set(tree_edges) - {pair})
        assert len(shores) == 2
        shore = next(s for s in shores if pair[0] in s)
        charge = sum(charges[i] for i in shore) % 2
        assert charge == len(cycles[index]) % 2
        tree.append({"cycle_index": index, "incident_components": pair,
                     "side_components": sorted(shore), "side_degree_charge": charge,
                     "whole_cycle_length": len(cycles[index])})
    assert all(q == 0 for q in charges) == all(len(c) % 2 == 0 for c in cycles)
    return {"components": [{"vertices": sorted(c),
                            "original_degree_sum": sum(degrees[v] for v in c),
                            "charge": q} for c, q in zip(comps, charges)],
            "region_tree": tree, "all_component_charges_even": not any(charges)}


def local_555(control, data):
    vertices, edges, faces, primal, triangles, degrees = data
    labels = control["literal_primal_labels"]
    if labels is None:
        return {"status": "no_literal_primal_labels"}
    matching = {tuple(e) for e in control["M"]}
    comps = components(range(len(degrees)), [primal[e] for e in matching])
    tree = next(c for c in comps if labels["v"] in c)
    rim = next(c for c in comps if labels["m"] in c)
    centre = next(c for c in comps if c != tree and c != rim)
    assert labels["w"] in tree and labels["z"] in rim
    assert len(centre) == 2
    safe = [next(v for v in primal[e] if v not in centre) for e in [(4, 5), (5, 6)]]
    outer = [t for triangle in triangles.values() if set(safe) <= set(triangle)
             for t in triangle if t not in safe and t not in centre]
    assert len(outer) == 1
    t = outer[0]
    ds = [degrees[v] for v in safe + [t]]
    if ds != [5, 5, 5]:
        return {"status": "not_degree555", "A_B_t": safe + [t], "degrees": ds}
    assert t in tree - {labels["v"], labels["w"]}
    branches = components(tree - {t}, [primal[e] for e in matching
                                      if set(primal[e]) <= tree - {t}])
    assert len(branches) == 2
    branch_charges = [sum(degrees[v] for v in b) % 2 for b in branches]
    if branch_charges != [1, 1]:
        return {"status": "not_two_odd_branches", "branch_charges": branch_charges}
    ab = [next(v for e, ends in primal.items() if rho in ends
               for v in ends if v in tree - {t}) for rho in safe]
    return {"status": "local_degree555_two_odd_branches", "A_B_t": safe + [t],
            "a_b": ab, "a_b_degrees": [degrees[v] for v in ab],
            "centre": sorted(centre), "T": sorted(tree), "U0": sorted(rim),
            "branches": [{"vertices": sorted(b),
                          "original_degree_sum": sum(degrees[v] for v in b),
                          "charge": q} for b, q in zip(branches, branch_charges)]}


def compute(control, data, local):
    vertices, edges, faces, primal, triangles, degrees = data
    matching = {tuple(e) for e in control["M"]}
    marks = list(map(tuple, control["marks"]))
    assert all(sum(v in e for e in matching) == 1 for v in vertices)
    assert "".join(str(int(e in matching)) for e in marks) == "101"
    rebuilt = enumerate_matchings(vertices, edges)
    assert [list(map(list, m)) for m in rebuilt] == [r["edges"] for r in control["matching_rows"]]
    lookup = {frozenset(m): i for i, m in enumerate(rebuilt)}
    rows = []
    fibres = {"".join(v): [] for v in itertools.product("01", repeat=3)}
    even_fibres = {key: [] for key in fibres}
    for index, values in enumerate(rebuilt):
        candidate = set(values)
        cycles = two_factor_cycles(vertices, edges - candidate)
        exchange = two_factor_cycles(vertices, matching ^ candidate, spanning=False)
        assert all(sum(e in matching for e in cycle_edges(c)) * 2 == len(c) for c in exchange)
        oddness = sum(len(c) % 2 for c in cycles)
        marked_type = "".join(str(int(e in candidate)) for e in marks)
        joint = marked_type in {"101", "110"}
        row = {"index": index, "edges": sorted(candidate), "marked_type": marked_type,
               "joint_admissible": joint, "oddness": oddness,
               "complement_cycles": cycles, "difference_cycles_from_M": exchange,
               "primal_components": component_data(vertices, primal, degrees, candidate, cycles)}
        prior_row = control["matching_rows"][index]
        assert row["marked_type"] == prior_row["marked_type"]
        assert oddness == prior_row["oddness"]
        assert cycles == sorted(list(canonical_cycle(c)) for c in prior_row["complement_cycles"])
        assert exchange == sorted(list(canonical_cycle(c)) for c in prior_row["difference_cycles_from_M"])
        fibres[marked_type].append(index)
        if not oddness:
            even_fibres[marked_type].append(index)
        rows.append(row)
    assert fibres == control["matching_fibres"]
    assert even_fibres == control["even_matching_fibres"]
    masks = []
    rejected = {}
    for mask in range(1 << (len(degrees) - 1)):
        x = {i for i in range(1, len(degrees)) if mask & (1 << (i - 1))}
        cut = {e for e, (a, b) in primal.items() if (a in x) != (b in x)}
        candidate = matching ^ cut
        bad = [v for v in vertices if sum(v in e for e in candidate) != 1]
        assert all(sum(v in e for e in candidate) == 3 for v in bad)
        index = lookup.get(frozenset(candidate))
        assert (index is not None) == (not bad)
        # This is the two-sided triangle law in the actual original rotation.
        failures = []
        for v, triangle in triangles.items():
            old_pair = next(primal[e] for e in matching if v in e)
            a, b = old_pair
            c = next(c for c in triangle if c not in old_pair)
            if (a in x) == (b in x) and (a in x) != (c in x):
                failures.append(v)
        assert failures == bad
        masks.append(index)
        if bad:
            rejected[str(len(bad))] = rejected.get(str(len(bad)), 0) + 1
        else:
            minimum = min((x, set(range(len(degrees))) - x), key=lambda s: (len(s), sorted(s)))
            rows[index]["primal_cut_anchored_at_face0"] = sorted(x)
            rows[index]["primal_cut_minimum_side"] = sorted(minimum)
    assert masks == control["all_anchored_cut_masks_to_matching_rows"]
    assert sorted(i for i in masks if i is not None) == list(range(len(rows)))

    def cut_row(x):
        anchored = set(range(len(degrees))) - set(x) if 0 in x else set(x)
        mask = sum(1 << (v - 1) for v in anchored)
        index = masks[mask]
        return rows[index] if index is not None else None

    pair_audit = []
    for x in itertools.combinations(range(len(degrees)), 2):
        row = cut_row(x)
        cut = {e for e, (a, b) in primal.items() if (a in x) != (b in x)}
        candidate = matching ^ cut
        pair_audit.append({"vertices": x, "degrees": [degrees[v] for v in x],
                           "bad_original_triangles": [v for v in vertices if sum(v in e for e in candidate) != 1],
                           "changed_marks": [i for i, e in enumerate(marks) if e in cut],
                           "matching_row": row["index"] if row else None,
                           "joint_even": bool(row and row["joint_admissible"] and not row["oddness"])})
    successes = [r["index"] for r in rows if r["joint_admissible"] and not r["oddness"]]
    minsize = min(len(rows[i]["primal_cut_minimum_side"]) for i in successes)
    A, B, t = local["A_B_t"]
    a, b = local["a_b"]
    h = next(v for v in local["centre"] if degrees[v] == 5)
    u = next(v for v in local["centre"] if degrees[v] == 4)
    named_sets = {"A_t": [A, t], "B_t": [B, t], "A_a": [A, a], "B_b": [B, b],
                  "A_B": [A, B], "A_B_t": [A, B, t], "A_B_t_a_b": [A, B, t, a, b],
                  "diamond_h_A_B_t": [h, A, B, t]}
    named = {}
    for name, x in named_sets.items():
        row = cut_row(x)
        cut = {e for e, (u, v) in primal.items() if (u in x) != (v in x)}
        candidate = matching ^ cut
        named[name] = {"vertices": sorted(x),
                       "bad_original_triangles": [v for v in vertices if sum(v in e for e in candidate) != 1],
                       "changed_marks": [i for i, e in enumerate(marks) if e in cut],
                       "matching_row": row["index"] if row else None,
                       "joint_even": bool(row and row["joint_admissible"] and not row["oddness"])}
    diamond = set(named_sets["diamond_h_A_B_t"])
    diamond_row = cut_row(diamond)
    assert diamond_row is not None
    boundary = {e for e, (v, w) in primal.items() if (v in diamond) != (w in diamond)}
    internal = {e for e, (v, w) in primal.items() if v in diamond and w in diamond}
    assert len(internal) == 5 and len(boundary) == 10
    assert all(degrees[v] == 5 for v in diamond)
    assert not (boundary & set(marks))
    assert diamond_row["marked_type"] == "101" and diamond_row["oddness"] == 0
    assert len(diamond_row["difference_cycles_from_M"]) == 1
    assert len(diamond_row["difference_cycles_from_M"][0]) == 10
    original_components = {key: set(local[key]) for key in ("T", "U0")}
    predicted = [{u}, (original_components["T"] - {t}) | {A, B},
                 (original_components["U0"] - {A, B}) | {h, t}]
    actual = [set(c["vertices"]) for c in diamond_row["primal_components"]["components"]]
    assert sorted(map(sorted, predicted)) == sorted(map(sorted, actual))
    assert all(sum(degrees[v] for v in c) % 2 == 0 for c in predicted)
    original_cycles = two_factor_cycles(vertices, edges - matching)
    assert sorted(map(len, original_cycles)) == sorted([7, control["outer_length"]])
    assert sorted(map(len, diamond_row["complement_cycles"])) == sorted([4, control["outer_length"] + 3])
    diamond_witness = {"X": sorted(diamond), "u_h_A_B_t_a_b": [u, h, A, B, t, a, b],
                       "matching_row": diamond_row["index"],
                       "cut_dual_edges": sorted(boundary),
                       "removed_M_edges": sorted(boundary & matching),
                       "added_nonM_edges": sorted(boundary - matching),
                       "unchanged_marks": marks,
                       "actual_new_component_vertices": list(map(sorted, predicted)),
                       "actual_new_component_original_degree_sums": [sum(degrees[v] for v in c) for c in predicted],
                       "complete_complement_cycle_lengths": sorted(map(len, diamond_row["complement_cycles"])),
                       "all_triangle_constraints": True, "all_mark_constraints": True,
                       "all_complete_component_charges_even": True}
    return {"name": control["name"], "sphere_faces": faces,
            "sphere_rotation": control["sphere_rotation"], "dual_edges": sorted(edges),
            "M": sorted(matching), "marks": marks, "literal_primal_labels": control["literal_primal_labels"],
            "original_primal_degrees": degrees,
            "primal_rotation_dual_edges": [[edge(a, b) for a, b in zip(f, f[1:] + f[:1])] for f in faces],
            "local_configuration": local,
            "source_failure_vertices_degree_below4": [v for v in range(len(degrees)) if degrees[v] < 4],
            "parallel_primal_edges": [[e, f] for e, f in itertools.combinations(sorted(edges), 2)
                                      if primal[e] == primal[f]],
            "matching_rows": rows, "complete_marked_matching_fibres": fibres,
            "complete_even_marked_matching_fibres": even_fibres,
            "all_anchored_cut_masks_to_matching_rows": masks,
            "rejected_cut_bad_triangle_histogram": rejected,
            "all_primal_pairs": pair_audit, "named_sets": named, "diamond_witness": diamond_witness,
            "joint_even_rows": successes,
            "minimum_joint_even_cut_size": minsize,
            "minimum_joint_even_cut_rows": [i for i in successes if len(rows[i]["primal_cut_minimum_side"]) == minsize]}


def expected():
    # All three named authorities are hash-verified; neither checker is imported.
    frozen(PRIOR + "/C/check.py")
    frozen(PRIOR + "/B/PROOF.md")
    prior = json.loads(gzip.decompress(frozen(PRIOR + "/C/certificate.json.gz")))
    controls = []
    classification = []
    for control in prior["controls"]:
        data = reconstruct(control)
        local = local_555(control, data)
        classification.append({"name": control["name"], **local})
        if local["status"] == "local_degree555_two_odd_branches":
            controls.append(compute(control, data, local))
    assert len(controls) == 1
    assert controls[0]["source_failure_vertices_degree_below4"]
    return {"schema": 1, "base": BASE,
            "authority": "one fixed local degree555 odd-branches plane control; all matchings and all cuts independently rebuilt",
            "source_realizability": "not triggered", "all_source_coverage": "OPEN",
            "arbitrary_size_conditional_theorem": "separate paper proof in independent A and B outputs",
            "new_lean_theorem": False, "prior_control_classification": classification,
            "controls": controls,
            "totals": {"prior_controls_classified": len(classification), "selected_controls": len(controls),
                       "perfect_matchings": sum(len(c["matching_rows"]) for c in controls),
                       "anchored_cut_masks": sum(len(c["all_anchored_cut_masks_to_matching_rows"]) for c in controls),
                       "complete_mark_fibres": 8 * len(controls), "complete_even_mark_fibres": 8 * len(controls),
                       "all_primal_pairs": sum(len(c["all_primal_pairs"]) for c in controls),
                       "joint_even_rows": sum(len(c["joint_even_rows"]) for c in controls)}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=HERE / "certificate.json.gz")
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()
    data = expected()
    if args.write:
        payload = (json.dumps(data, sort_keys=True, indent=2) + "\n").encode()
        if args.write.suffix == ".gz":
            payload = gzip.compress(payload, mtime=0)
        with args.write.open("xb") as stream:
            stream.write(payload)
        print("EXCLUSIVE CREATE PASS")
        return
    payload = args.certificate.read_bytes()
    if args.certificate.suffix == ".gz":
        payload = gzip.decompress(payload)
    assert json.loads(payload) == json.loads(json.dumps(data)), "certificate differs from independent complete replay"
    print(json.dumps({"status": "PASS", "source_realizability": "not triggered", **data["totals"],
                      "minimum_repairs": [{"control": c["name"], "cut_size": c["minimum_joint_even_cut_size"],
                                           "rows": c["minimum_joint_even_cut_rows"]} for c in data["controls"]]},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
