#!/usr/bin/env python3
"""Stdlib calibration; no original-source realizability authority."""
from __future__ import annotations

import copy
import itertools
import json

BASE = "9c36e3c4789dfec07d60ec4e042f0bafe17451d1"
PORTS = (1, 2, 4, 5, 6)


def edge(a, b):
    return tuple(sorted((a, b)))


CAP = frozenset(
    [edge(i, (i + 1) % 7) for i in range(7)] + [(0, 3)]
)


def components(vertices, edges):
    adj = {v: [] for v in vertices}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    unseen = set(vertices)
    result = []
    while unseen:
        start = min(unseen)
        todo, seen = [start], set()
        while todo:
            v = todo.pop()
            if v in seen:
                continue
            seen.add(v)
            todo.extend(adj[v])
        unseen -= seen
        deg = [len(adj[v]) for v in seen]
        assert all(d in (1, 2) for d in deg)
        ends = sorted(v for v in seen if len(adj[v]) == 1)
        assert len(ends) in (0, 2)
        result.append({
            "vertices": sorted(seen),
            "ends": ends,
            "length": sum(deg) // 2,
        })
    return sorted(result, key=lambda c: c["vertices"])


def recursive_matchings(vertices, edges):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)

    def rec(left):
        if not left:
            yield frozenset()
            return
        u = min(left)
        for v in sorted(adj[u] & left):
            for rest in rec(left - {u, v}):
                yield rest | {edge(u, v)}

    yield from rec(set(vertices))


def cap_rows():
    rows = []
    # Keep all 32 masks, including every empty fibre.
    for mask in range(32):
        selected = [p for i, p in enumerate(PORTS) if mask & (1 << i)]
        remaining = set(range(7)) - set(selected)
        states = []
        for local in recursive_matchings(remaining,
                                        [e for e in CAP
                                         if set(e) <= remaining]):
            comps = components(range(7), CAP - local)
            states.append({
                "matching": [list(e) for e in sorted(local)],
                "components": comps,
                "no_internal_odd_cycle": all(
                    c["ends"] or c["length"] % 2 == 0 for c in comps
                ),
            })
        rows.append({"mask": mask, "selected_ports": selected,
                     "states": sorted(states, key=lambda s: s["matching"])})
    return rows


def validate_rows(rows):
    if len(rows) != 32 or [r["mask"] for r in rows] != list(range(32)):
        raise ValueError("missing or reordered complete spoke-mask fibre")
    if rows != cap_rows():
        raise ValueError("cap matching/path/length fibre differs from graph")


def make_control(name, outer, spokes, chords, e, f, g, inside):
    outer_edges = frozenset(
        edge(outer[i], outer[(i + 1) % len(outer)])
        for i in range(len(outer))
    )
    spoke_edges = frozenset(edge(p, t) for p, t in spokes.items())
    chords = frozenset(edge(*x) for x in chords)
    matching = chords | spoke_edges | {(0, 3)}
    graph = CAP | outer_edges | spoke_edges | chords
    vertices = set(range(7)) | set(outer)
    assert all(sum(v in z for z in graph) == 3 for v in vertices)
    assert all(sum(v in z for z in matching) == 1 for v in vertices)
    assert e in matching and g in matching and f not in matching
    return dict(name=name, outer=outer, outer_edges=outer_edges,
                spokes=spokes, chords=chords, matching=matching,
                graph=graph, vertices=vertices, e=e, f=f, g=g,
                inside=frozenset(edge(*x) for x in inside))


def full_even(c, pm):
    cycles = components(c["vertices"], c["graph"] - pm)
    assert all(not x["ends"] for x in cycles)
    return all(x["length"] % 2 == 0 for x in cycles)


def interface_even(cap_state, outer_components):
    if not cap_state["no_internal_odd_cycle"]:
        return False
    cycles = [x for x in outer_components if not x["ends"]]
    if any(x["length"] % 2 for x in cycles):
        return False
    cap_paths = [x for x in cap_state["components"] if x["ends"]]
    out_paths = [x for x in outer_components if x["ends"]]
    if len(cap_paths) == 1:
        assert len(out_paths) == 1
        assert cap_paths[0]["length"] % 2 == 0
        assert out_paths[0]["length"] % 2 == 0
        return True
    assert len(cap_paths) == len(out_paths) == 2
    assert sum(x["length"] for x in cap_paths) % 2 == 1
    assert sum(x["length"] for x in out_paths) % 2 == 1
    cpair = {tuple(x["ends"]): x["length"] % 2 for x in cap_paths}
    opair = {tuple(x["ends"]): x["length"] % 2 for x in out_paths}
    if cpair.keys() != opair.keys():
        return True
    return cpair == opair


def monotone(c, a, b):
    outer = c["outer"]
    start = outer.index(c["spokes"][a])
    arc = [outer[start]]
    while arc[-1] != c["spokes"][b]:
        arc.append(outer[(start + len(arc)) % len(outer)])
    mate = {}
    for x, y in c["chords"]:
        mate[x] = y
        mate[y] = x
    used_o, jumps = [], []
    i = 0
    while i < len(arc) - 1:
        used_o.append(edge(arc[i], arc[i + 1]))
        i += 1
        if i == len(arc) - 1:
            break
        d = edge(arc[i], mate[arc[i]])
        if d not in c["inside"]:
            return {"ports": [a, b], "arc": arc,
                    "termination": "opposite_side_chord",
                    "blocker": list(d), "jumps": jumps}
        j = arc.index(mate[arc[i]])
        assert j > i
        jumps.append({"chord": list(d), "arc_length": j - i})
        i = j
    q = {edge(a, b), edge(a, c["spokes"][a]),
         edge(b, c["spokes"][b])}
    q.update(used_o)
    q.update(tuple(x["chord"]) for x in jumps)
    pm = c["matching"] ^ q
    assert all(sum(v in z for z in pm) == 1 for v in c["vertices"])
    cycles = components(c["vertices"], c["graph"] - pm)
    lengths = sorted(x["length"] for x in cycles)
    bad = sum(x["arc_length"] % 2 == 0 for x in jumps)
    assert sum(n % 2 for n in lengths) == bad + bad % 2
    assert len(cycles) == len(jumps) + 1
    pocket_lengths = [x["arc_length"] + 1 for x in jumps]
    expected = sorted(pocket_lengths +
                      [len(c["vertices"]) - sum(pocket_lengths)])
    assert lengths == expected
    mark_safe = not ({c["e"], c["f"], c["g"]} & q)
    return {"ports": [a, b], "arc": arc, "termination": "right_port",
            "jumps": jumps, "mark_safe": mark_safe,
            "full_cycle_lengths": lengths, "odd_jump_count": bad,
            "predicted_full_oddness": bad + bad % 2}


def check_control(c, rows):
    all_pm = set(recursive_matchings(c["vertices"], c["graph"]))
    by_s = {tuple(r["selected_ports"]): r["states"] for r in rows}
    reconstructed = set()
    parity_checks = 0
    joint_even = []
    outer = c["outer"]
    reverse_spoke = {t: p for p, t in c["spokes"].items()}
    for mask in range(1 << len(outer)):
        selected_o = frozenset(
            edge(outer[i], outer[(i + 1) % len(outer)])
            for i in range(len(outer)) if mask & (1 << i))
        ends = [v for x in selected_o for v in x]
        if len(ends) != len(set(ends)):
            continue
        covered = set(ends)
        if any((x in covered) != (y in covered) for x, y in c["chords"]):
            continue
        s = tuple(p for p in PORTS if c["spokes"][p] not in covered)
        removed_chords = frozenset(
            x for x in c["chords"] if x[0] in covered)
        outside_pm = (c["chords"] - removed_chords) | selected_o
        external = (c["outer_edges"] - selected_o) | removed_chords
        exterior_components = components(outer, external)
        # Transport only actual endpoints; no new pairing is selected.
        mapped = copy.deepcopy(exterior_components)
        for x in mapped:
            x["ends"] = sorted(reverse_spoke[v] for v in x["ends"])
        for state in by_s[s]:
            local = frozenset(tuple(x) for x in state["matching"])
            selected_spokes = frozenset(edge(p, c["spokes"][p]) for p in s)
            pm = local | selected_spokes | outside_pm
            reconstructed.add(pm)
            predicted = interface_even(state, mapped)
            assert predicted == full_even(c, pm)
            parity_checks += 1
            joint = c["e"] in pm and ((c["f"] in pm) != (c["g"] in pm))
            bit_joint = (c["e"][0] not in covered and
                         ((c["g"][0] in covered) == (c["f"] in local)))
            assert joint == bit_joint
            if joint and predicted:
                joint_even.append(pm)
    assert reconstructed == all_pm
    return {
        "name": c["name"], "source_realizability": "not triggered",
        "perfect_matchings": len(all_pm),
        "interface_reconstructed_matchings": len(reconstructed),
        "complete_parity_checks": parity_checks,
        "joint_even_matchings": len(joint_even),
        "safe_sector_candidate_chains": [monotone(c, 4, 5),
                                          monotone(c, 5, 6)],
    }


def main():
    rows = cap_rows()
    validate_rows(rows)
    negative_checks = []
    missing = copy.deepcopy(rows)
    missing.pop(0)  # Explicitly an empty complete fibre.
    try:
        validate_rows(missing)
    except ValueError:
        negative_checks.append("missing_empty_mask_rejected")
    else:
        raise AssertionError("missing empty fibre accepted")
    corrupt = copy.deepcopy(rows)
    for row in corrupt:
        if row["states"]:
            row["states"][0]["components"][0]["length"] += 1
            break
    try:
        validate_rows(corrupt)
    except ValueError:
        negative_checks.append("corrupted_complete_path_length_rejected")
    else:
        raise AssertionError("corrupted path length accepted")
    weak = make_control(
        "weak_geometry_f12_g_in_wrong_sector56",
        list(range(7, 18)), {1: 7, 2: 8, 4: 9, 5: 12, 6: 17},
        [(10, 15), (11, 14), (13, 16)],
        (10, 15), (1, 2), (13, 16), [(13, 16)])
    literal = make_control(
        "literal_sector_positive20",
        list(range(7, 20)), {1: 7, 2: 8, 4: 9, 5: 11, 6: 12},
        [(10, 13), (14, 19), (15, 17), (16, 18)],
        (16, 18), (1, 2), (14, 19), [(14, 19), (15, 17)])
    odd_jump = make_control(
        "literal_sector_odd_jump_positive20",
        list(range(7, 20)), {1: 7, 2: 8, 4: 9, 5: 14, 6: 15},
        [(10, 13), (11, 18), (12, 17), (16, 19)],
        (11, 18), (1, 2), (16, 19), [(10, 13), (16, 19)])
    even_jump = make_control(
        "literal_sector_even_jump_negative18",
        list(range(7, 18)), {1: 7, 2: 8, 4: 9, 5: 13, 6: 14},
        [(10, 12), (11, 16), (15, 17)],
        (11, 16), (1, 2), (15, 17), [(10, 12), (15, 17)])
    results = [check_control(c, rows)
               for c in (weak, literal, odd_jump, even_jump)]
    assert results[0]["joint_even_matchings"] == 0
    assert results[0]["safe_sector_candidate_chains"][1]["mark_safe"] is False
    assert results[1]["safe_sector_candidate_chains"][1]["full_cycle_lengths"] == [20]
    assert results[2]["safe_sector_candidate_chains"][0]["full_cycle_lengths"] == [4, 16]
    assert results[3]["safe_sector_candidate_chains"][0]["full_cycle_lengths"] == [3, 15]
    assert results[2]["safe_sector_candidate_chains"][0]["mark_safe"]
    assert results[3]["safe_sector_candidate_chains"][0]["mark_safe"]
    # Independent safe non-monotone exchange: avoids all marks, removes
    # C7, but retains two complete odd cycles.
    q_vertices = (5, 6, 12, 13, 10, 11)
    q = frozenset(edge(q_vertices[i], q_vertices[(i + 1) % len(q_vertices)])
                  for i in range(len(q_vertices)))
    assert not q & {literal["e"], literal["f"], literal["g"]}
    changed = literal["matching"] ^ q
    assert all(sum(v in z for z in changed) == 1 for v in literal["vertices"])
    odd_lengths = sorted(c["length"] for c in
                         components(literal["vertices"], literal["graph"] - changed))
    assert odd_lengths == [9, 11]
    result = {
        "schema": "r6-two-cycle-interface-calibration-v1",
        "base": BASE,
        "authority": "finite graph controls; no original source",
        "all_32_spoke_fibres": rows,
        "local_matching_states": sum(len(x["states"]) for x in rows),
        "states_without_internal_odd_cycle": sum(
            s["no_internal_odd_cycle"] for r in rows for s in r["states"]),
        "negative_checks": negative_checks,
        "controls": results,
        "safe_nonmonotone_negative_full_cycles": odd_lengths,
    }
    assert result["local_matching_states"] == 15
    assert result["states_without_internal_odd_cycle"] == 13
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
