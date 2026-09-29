#!/usr/bin/env python3
"""No-mixed B-B: both t=1,(2,1): budgets, supports and rejection causes.

Necessary same-source data only. Cross-component upper-bound choices are not
asserted realizable. Arbitrary-size support coverage is proved in the report.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_adjacent_degree5_no_mixed_t2 import schema_audit, stable_schema_ids
from c5_adjacent_degree5_singleton_long_arc import component_options, valid_q_support
from c5_root_degree_excess import budget
from c5_single_spoke_cores import Q, U, PI, RHO, TARGETS
from c5_adjacent_degree5_no_mixed_t2_t1_bridge import (
    component_evidence as bridge_evidence, root_pairs, swapped,
)
from c5_adjacent_degree5_no_mixed_t2_t1_endpoints import (
    component_evidence as endpoint_evidence, minor_control,
)
from c5_single_spoke_two_two_minor import verify_minor

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/c5_adjacent_degree5_no_mixed/observations.json"
HANDOFF = ROOT / "artifacts/c5_adjacent_degree5_no_mixed_t2_t0_overlap/observations.json"
OUT = ROOT / "artifacts/c5_adjacent_degree5_no_mixed_bb/observations.json"
TABLE = OUT.with_name("support_table.md")
NAMES = ("Cz", "Dz", "z0", "Cw", "Dw", "w0")
COMPONENTS = (("Cz", "z", 0, 0, 2), ("Dz", "z", 1, 1, 1), ("Cw", "w", 0, 3, 2), ("Dw", "w", 1, 4, 1))


def cardinalities(name):
    return range(2, 6) if name in ("Cz", "Dz", "Cw", "Dw") else (1,)


def geometries():
    choices = {name: [s for k in cardinalities(name) for s in combinations(range(6), k)
                      if max(s) - min(s) < 5] for name in NAMES}
    orders = set()
    for z, w in product(permutations(NAMES[:3]), permutations(NAMES[3:])):
        order = z + w
        i = order.index("Cz")
        orders.add(order[i:] + order[:i])
    result = {}
    for order in sorted(orders):
        def visit(j, end, assigned):
            if j == 6:
                for anchor in range(5):
                    supports = tuple(tuple(sorted((anchor + i) % 5 for i in assigned[n]))
                                     for n in NAMES)
                    result.setdefault(supports, []).append(dict(
                        order=order, anchor=anchor, lifts=tuple(assigned[n] for n in NAMES)))
                return
            for support in choices[order[j]]:
                if min(support) >= end and (j or min(support) == 0):
                    visit(j + 1, max(support), assigned | {order[j]: support})
        visit(0, 0, {})
    return result


def independent_geometries():
    """Actual support hulls on each whole side, with disjoint frame-edge masks."""
    sides = []
    for names in (NAMES[:3], NAMES[3:]):
        found = set()
        choices = [[s for k in cardinalities(n) for s in combinations(range(5), k)] for n in names]
        for supports in product(*choices):
            for anchor in set().union(*map(set, supports)):
                lifts = [sorted((i - anchor) % 5 for i in s) for s in supports]
                if any(not (a[-1] <= b[0] or b[-1] <= a[0])
                       for a, b in combinations(lifts, 2)):
                    continue
                span = max(s[-1] for s in lifts)
                mask = sum(1 << ((anchor + j) % 5) for j in range(span))
                found.add((supports, mask))
        sides.append(found)
    # Group by masks to avoid an unnecessarily large all-pairs product.
    groups = []
    for side in sides:
        by_mask = {}
        for supports, mask in side:
            by_mask.setdefault(mask, set()).add(supports)
        groups.append(by_mask)
    return {a + b for ma, aa in groups[0].items() for mb, bb in groups[1].items()
            if not ma & mb for a, b in product(aa, bb)}


def rotations(order):
    result = []
    for flips in product((False, True), repeat=2):
        expansion = {n: (n,) for n in NAMES}
        for name, flip in zip(("Cz", "Cw"), flips):
            ports = (name + "_0", name + "_1")
            expansion[name] = ports[::-1] if flip else ports
        expansion["Dz"] = ("Dz_0",)
        expansion["Dw"] = ("Dw_0",)
        roots = {}
        for root, own, other in (("z", NAMES[:3], "w"), ("w", NAMES[3:], "z")):
            start = next(i for i, n in enumerate(order) if n in own and order[i - 1] not in own)
            units = tuple(order[(start + j) % 6] for j in range(3))
            assert set(units) == set(own)
            roots[root] = (other,) + tuple(p for n in units for p in expansion[n])
            assert len(roots[root]) == len(set(roots[root])) == 5
        result.append(dict(contact_flips=flips, root_rotations=roots,
                           neighborhood_word=tuple(p for n in order for p in expansion[n])))
    return result


def verify_placement(supports, placement, contact_rotations):
    """Check named incidences and lifts independently of their generators."""
    order = placement["order"]
    assert len(order) == len(NAMES) and set(order) == set(NAMES) and order[0] == "Cz"
    side = [n in NAMES[:3] for n in order]
    assert sum(side[i] != side[i - 1] for i in range(6)) == 2
    lifts = dict(zip(NAMES, placement["lifts"], strict=True))
    assert len(supports) == 6 and 0 <= placement["anchor"] < 5
    assert min(lifts["Cz"]) == 0 and max(lifts[order[-1]]) <= 5
    for i, (name, support) in enumerate(zip(NAMES, supports, strict=True)):
        values = lifts[name]
        assert tuple(sorted(set(values))) == tuple(values)
        assert len(values) in cardinalities(name) and max(values) - min(values) < 5
        assert tuple(sorted((placement["anchor"] + j) % 5 for j in values)) == tuple(support)
    assert all(max(lifts[a]) <= min(lifts[b]) for a, b in zip(order, order[1:]))
    assert sum(max(lifts[n]) - min(lifts[n]) for n, _, _, _, _ in COMPONENTS) >= 4
    expected = {"z": {"w", "Cz_0", "Cz_1", "Dz_0", "z0"},
                "w": {"z", "Cw_0", "Cw_1", "Dw_0", "w0"}}
    assert len(contact_rotations) == 4
    assert {tuple(r["contact_flips"]) for r in contact_rotations} == set(product((False, True), repeat=2))
    for record in contact_rotations:
        word = record["neighborhood_word"]
        assert len(word) == len(set(word)) == 8
        assert set(word) == (expected["z"] | expected["w"]) - {"z", "w"}
        compressed = []
        for port in word:
            unit = port.split("_")[0]
            if not compressed or compressed[-1] != unit:
                compressed.append(unit)
        assert tuple(compressed) == tuple(order)
        for name, flip in zip(("Cz", "Cw"), record["contact_flips"], strict=True):
            ports = [name + "_0", name + "_1"]
            assert [p for p in word if p.startswith(name + "_")] == (ports[::-1] if flip else ports)
        for root, other, units in (("z", "w", NAMES[:3]), ("w", "z", NAMES[3:])):
            rotation = record["root_rotations"][root]
            assert len(rotation) == 5 and set(rotation) == expected[root] and rotation[0] == other
            start = next(i for i, p in enumerate(word)
                         if p.split("_")[0] in units and word[i - 1].split("_")[0] not in units)
            assert tuple(rotation[1:]) == tuple(word[(start + j) % 8] for j in range(4))


def bind_sources(data):
    sides = data["side_normal_forms"]
    records = []
    for join_id, (i, j) in enumerate(data["abstract_conditions"]["retained"]):
        z, w = sides[i], sides[j]
        if any((len(t["root_boundary"]), t["ports"]) != (1, [2, 1]) for t in (z, w)):
            continue
        budgets = {r: budget(t) for r, t in (("z", z), ("w", w))}
        assert all(v["component_deficits"] == [1, 0] for v in budgets.values())
        records.append(dict(id=len(records), retained_join_id=join_id, side_ids=(i, j),
                            common=z["common"], z=z, w=w, source_budgets=budgets))
    def key(s):
        return (tuple(s["z"]["root_boundary"]), tuple(s["w"]["root_boundary"]), s["common"],
                tuple(map(tuple, s["z"]["forbidden"])), tuple(map(tuple, s["w"]["forbidden"])))
    rebuilt = set()
    for iz, iw in product(range(5), repeat=2):
        for c in U - {Q[iz], Q[iw]}:
            for az, aw in product(permutations(sorted(U - {Q[iz], c})),
                                  permutations(sorted(U - {Q[iw], c}))):
                rebuilt.add(((iz,), (iw,), c, tuple((a,) for a in az), tuple((a,) for a in aw)))
    assert {key(s) for s in records} == rebuilt and len(records) == 236
    assert (records[0]["retained_join_id"], records[0]["side_ids"]) == (2142, (91, 91))
    frontier = json.loads(HANDOFF.read_text())["next_frontier"]
    assert frontier["source_sha256"] == sha256(SOURCE.read_bytes()).hexdigest()
    assert frontier["records"] == [dict(retained_join_id=s["retained_join_id"], side_ids=list(s["side_ids"])) for s in records]
    return records


def row_evidence(source, supports, row):
    components = [dict(name=name, **component_options(k, supports[pos], tuple(source[root]["forbidden"][col]), row))
                  for name, root, col, pos, k in COMPONENTS]
    joins = []
    for fz, dz, fw, fd in product(*(c["options"] for c in components)):
        ez = U - {row[i] for i in source["z"]["root_boundary"]} - set(fz) - set(dz)
        ew = U - {row[i] for i in source["w"]["root_boundary"]} - set(fw) - set(fd)
        pairs = sorted((a, b) for a, b in product(ez, ew) if a != b)
        direct = [(a, b) for a, b in product(range(4), repeat=2)
                  if a != b and a not in fz and a not in dz and b not in fw and b not in fd
                  and all(a != row[i] for i in source["z"]["root_boundary"])
                  and all(b != row[i] for i in source["w"]["root_boundary"])]
        assert pairs == direct
        reasons = (["empty_z"] if not ez else []) + (["empty_w"] if not ew else [])
        if len(ez) == 1 and ez == ew:
            reasons.append("same_singleton")
        assert bool(reasons) == (not pairs)
        joins.append(dict(forbidden_sets=(fz, dz, fw, fd), residuals=(sorted(ez), sorted(ew)),
                          root_pairs=pairs, witness=pairs[0] if pairs else None,
                          obstruction_reasons=reasons))
    accepted = all(j["root_pairs"] for j in joins)
    mechanism = ("complete_relation_transport" if all(c["exact"] for c in components)
                 else "transport_and_capacity_bound") if accepted else None
    return dict(row=row, components=components, joins=joins,
                status="accept" if accepted else "unresolved", closure_reason=mechanism)


def symmetry_audit(records, sources):
    def key(src):
        return tuple((tuple(src[r]["root_boundary"]), tuple(map(tuple, src[r]["forbidden"]))) for r in ("z", "w"))
    source_lookup = {key(s): s["id"] for s in sources}
    lookup = {(r["source_id"], r["supports"]): r for r in records}
    def moved_join(j):
        return (tuple(tuple(sorted(PI[c] for c in f)) for f in j["forbidden_sets"]),
                tuple(tuple(sorted(PI[c] for c in e)) for e in j["residuals"]),
                tuple(j["obstruction_reasons"]))
    count = 0
    for record in records:
        src = sources[record["source_id"]]
        moved_key = tuple((tuple(sorted(RHO[i] for i in src[r]["root_boundary"])),
                           tuple(tuple(sorted(PI[c] for c in f)) for f in src[r]["forbidden"])) for r in ("z", "w"))
        sid = source_lookup[moved_key]
        supports = tuple(tuple(sorted(RHO[i] for i in s)) for s in record["supports"])
        record["reflected_id"] = lookup[sid, supports]["id"]
        record["reflected_raw_targets"] = []
        for before in record["targets"]:
            row = tuple(PI[before["row"][RHO[i]]] for i in range(5))
            after = row_evidence(sources[sid], supports, row)
            assert before["status"] == after["status"]
            assert {moved_join(j) for j in before["joins"]} == {
                (tuple(map(tuple, j["forbidden_sets"])), tuple(map(tuple, j["residuals"])),
                 tuple(j["obstruction_reasons"])) for j in after["joins"]}
            record["reflected_raw_targets"].append(row)
            count += 1
    return count


def relation_audit(records, sources, schemas):
    by_sides = {tuple(s["side_ids"]): s["id"] for s in sources}
    lookup = {(r["source_id"], r["supports"]): r for r in records}
    transported = 0
    for r in records:
        source = sources[r["source_id"]]
        sid = by_sides[tuple(reversed(source["side_ids"]))]
        twin = lookup[sid, r["supports"][3:] + r["supports"][:3]]
        r["root_swapped_id"] = twin["id"]
        reflected = records[r["reflected_id"]]
        for name, root, col, pos, arity in COMPONENTS:
            h = source[root]["forbidden"][col][0]
            other_name = name[0] + dict(z="w", w="z")[name[1]]
            if arity == 2:
                ids = r["q_schema_ids"][name]
                assert ids == twin["q_schema_ids"][other_name]
                moved = {tuple(sorted(tuple(PI[c] for c in t) for t in schemas[h][i])) for i in ids}
                assert moved == {tuple(sorted(schemas[PI[h]][i])) for i in reflected["q_schema_ids"][name]}
                # Contact reversal acts on the entire ordered relation.
                assert {tuple(sorted(tuple(reversed(t)) for t in schemas[h][i])) for i in ids} == {
                    tuple(sorted(schemas[h][i])) for i in ids}
                relations = [schemas[h][i] for i in ids]
            else:
                relations = [r["q_single_contact_relations"][name]]
                assert relations[0] == twin["q_single_contact_relations"][other_name]
                assert reflected["q_single_contact_relations"][name] == ((PI[h],),)
            for t in r["targets"]:
                c = next(c for c in t["components"] if c["name"] == name)
                if c["exact"]:
                    perm = c["permutation"]
                    assert all(perm[Q[i]] == t["row"][i] for i in r["supports"][pos])
                    for relation in relations:
                        image = [tuple(perm[v] for v in tup) for tup in relation]
                        assert tuple(sorted(set.intersection(*map(set, image)))) == c["options"][0]
                        transported += 1
        for t, u in zip(r["targets"], twin["targets"], strict=True):
            assert t["status"] == u["status"]
            moved = {(j["forbidden_sets"][2:] + j["forbidden_sets"][:2],
                      tuple(sorted((b, a) for a, b in j["root_pairs"]))) for j in t["joins"]}
            assert moved == {(j["forbidden_sets"], tuple(j["root_pairs"])) for j in u["joins"]}
    return transported


def context(record, source):
    return dict(record_id=record["id"], root_boundary={r: source[r]["root_boundary"] for r in ("z", "w")},
        components=[dict(name=n, root=r, support=record["supports"][pos],
                         contacts=[f"{n}_{i}" for i in range(k)], source_forbidden=source[r]["forbidden"][col])
                    for n, r, col, pos, k in COMPONENTS])


def obstruction(ctx, row, bans):
    # Only invoked after the complete root join has failed.
    assert not root_pairs(ctx, row, bans)
    first = [e for k in range(len(ctx["components"]))
             if (e := bridge_evidence(ctx, row, bans, k)) is not None]
    direct = [e for e in first if e["direct_frame"]["eliminated"]]
    if direct:
        return dict(stage="fixed_frame_original_path", components=first, endpoints=[], eliminated=True)
    if any(e["eliminated"] for e in first):
        return dict(stage="shared_first_bridge", components=first, endpoints=[], eliminated=True)
    endpoints = [e for k in range(len(ctx["components"]))
                 if (e := endpoint_evidence(ctx, row, bans, k)) is not None]
    closed = any(e["eliminated"] for e in endpoints)
    return dict(stage="original_endpoints" if closed else None,
                components=first, endpoints=endpoints, eliminated=closed)


def refinement(records, sources):
    contexts = [context(r, sources[r["source_id"]]) for r in records]
    controls, failures, stages = [], [], Counter()
    checked_joins = 0
    for r, ctx in zip(records, contexts, strict=True):
        r["final_targets"] = []
        for ti, t in enumerate(r["targets"]):
            cases = []
            for ji, j in enumerate(t["joins"]):
                assert root_pairs(ctx, t["row"], j["forbidden_sets"]) == j["root_pairs"]
                assert set(root_pairs(swapped(ctx), t["row"], j["forbidden_sets"])) == {
                    (b, a) for a, b in j["root_pairs"]}
                checked_joins += 1
                if j["root_pairs"]:
                    continue
                ev = obstruction(ctx, t["row"], j["forbidden_sets"])
                stages[ev["stage"] or "unresolved"] += 1
                # Literal frame reflection and whole-source root exchange.
                raw = tuple(PI[t["row"][RHO[i]]] for i in range(5))
                moved_bans = tuple(tuple(sorted(PI[c] for c in f)) for f in j["forbidden_sets"])
                rev = obstruction(contexts[r["reflected_id"]], raw, moved_bans)
                sw = obstruction(swapped(ctx), t["row"], j["forbidden_sets"])
                assert (ev["stage"], ev["eliminated"]) == (rev["stage"], rev["eliminated"]) == (sw["stage"], sw["eliminated"])
                renamed = json.loads(json.dumps(ev))
                for c in renamed["components"] + renamed["endpoints"]:
                    c["root"] = dict(z="w", w="z")[c["root"]]
                    frames_to_move = ([c["direct_frame"]] + [b["frame"] for b in c["first_bridge"]["beta_cases"]]
                                      if "direct_frame" in c else [c["endpoint_family"]])
                    for f in frames_to_move:
                        for witness in f["witnesses"]:
                            witness["route"]["path"] = [dict(z="w", w="z").get(v, v) for v in witness["route"]["path"]]
                assert renamed == json.loads(json.dumps(sw))
                def frames(evidence):
                    return [(e["component"], e["direct_frame"]) for e in evidence["components"]] + [
                        (e["component"], e["endpoint_family"]) for e in evidence["endpoints"]]
                for (k, frame), (rk, rf) in zip(frames(ev), frames(rev), strict=True):
                    assert k == rk and frame["eliminated"] == rf["eliminated"]
                    assert {tuple(sorted(RHO[i] for i in a)) for a in frame["supports"]} == set(map(tuple, rf["supports"]))
                    witnesses = {(tuple(map(tuple, w["frame_arcs"])), w["route"]["mode"], w["route"]["component"], w["route"]["landing"]) for w in rf["witnesses"]}
                    for w in frame["witnesses"]:
                        assert (tuple(tuple(sorted(RHO[i] for i in arc)) for arc in w["frame_arcs"]),
                                w["route"]["mode"], w["route"]["component"], RHO[w["route"]["landing"]]) in witnesses
                ids = []
                selected = [(e["component"], e["direct_frame"]) for e in ev["components"] if e["direct_frame"]["eliminated"]]
                if not selected:
                    selected = [(e["component"], e["endpoint_family"]) for e in ev["endpoints"] if e["eliminated"]]
                for k, frame in selected:
                    modes = set()
                    for witness in frame["witnesses"]:
                        route_key = witness["route"]["mode"], witness["route"]["component"]
                        if route_key in modes:
                            continue
                        modes.add(route_key)
                        ids.append(len(controls))
                        controls.append(minor_control(ctx, k, witness, length=3, external_length=3))
                case = dict(record_id=r["id"], target_index=ti, join_index=ji, original_join=j,
                            evidence=ev, minor_control_ids=ids, reflected_raw_target=raw,
                            reflected_forbidden_sets=moved_bans, reflection_and_root_swap_verified=True)
                cases.append(case)
                failures.append(case)
            remaining = [c for c in cases if not c["evidence"]["eliminated"]]
            closure = t["closure_reason"] if t["status"] == "accept" else (
                None if remaining else "+".join(sorted({c["evidence"]["stage"] for c in cases})))
            r["final_targets"].append(dict(row=t["row"], status="unresolved" if remaining else "accept",
                                           closure_reason=closure, failing_candidate_cases=cases))
    # Vary path length and tether shape on actual B-B witnesses, retaining all four components.
    seed = next(c for c in failures if c["evidence"]["stage"] == "original_endpoints")
    ctx = contexts[seed["record_id"]]
    component = next(c for c in seed["evidence"]["endpoints"] if c["eliminated"])
    frame = component["endpoint_family"]
    witness = next(w for w in frame["witnesses"] if w["route"]["mode"] == "other_spoke")
    k = component["component"]
    suppliers = list(product(*(sorted(set(ctx["components"][k]["support"]) & set(a)) for a in witness["frame_arcs"][:2])))
    for length, styles, a, b, ext in product((1, 3, 5, 9), product(("direct", "shared_trunk", "separate_bridges", "shared_cycle"), repeat=2), suppliers, suppliers, (1, 3)):
        controls.append(minor_control(ctx, k, witness, length, styles, [a, b], ext))
    assert stages == {"fixed_frame_original_path": 48, "original_endpoints": 72}
    assert checked_joins == 3504
    assert all(t["status"] == "accept" for r in records for t in r["final_targets"])
    return dict(candidate_stages=dict(sorted(stages.items())), failing_candidates=failures,
                minor_controls=controls, complete_join_root_swaps=checked_joins)


def negative_controls(geometry, records, sources, refined):
    supports, placements = next(iter(sorted(geometry.items())))
    placement = placements[0]
    templates = rotations(placement["order"])
    broken = []
    def clone(x):
        return json.loads(json.dumps(x))
    p = clone(placement)
    p["order"] = ["Cz", "Cw", "Dz", "Dw", "z0", "w0"]
    broken.append(("interleaved_root_segments", supports, p, templates))
    p = clone(placement)
    p["lifts"][1] = [p["lifts"][1][0]]
    broken.append(("Dz_is_not_a_spoke", (supports[0], supports[1][:1], *supports[2:]), p, templates))
    t = clone(templates)
    t[0]["root_rotations"]["w"][-1] = "Dz_0"
    broken.append(("merged_original_single_contacts", supports, placement, t))
    t = clone(templates)
    t[0]["root_rotations"]["z"].remove("w")
    broken.append(("missing_zw_rotation", supports, placement, t))
    for label, ss, p, t in broken:
        try:
            verify_placement(ss, p, t)
        except AssertionError:
            pass
        else:
            raise AssertionError(label)
    result = [b[0] for b in broken]
    relation = ((0, 1), (2, 0))
    marginals = tuple(product({t[0] for t in relation}, {t[1] for t in relation}))
    assert set.intersection(*map(set, relation)) == {0}
    assert set.intersection(*map(set, marginals)) == set()
    result.append("endpoint_marginals_destroy_the_complete_ban")
    seed = next(c for c in refined["failing_candidates"] if c["evidence"]["stage"] == "original_endpoints")
    r = records[seed["record_id"]]
    ctx = context(r, sources[r["source_id"]])
    row = r["targets"][seed["target_index"]]["row"]
    bans = seed["original_join"]["forbidden_sets"]
    assert all(endpoint_evidence(ctx, row, bans, k) is None for k in (1, 3))
    result.append("single_contact_components_have_no_pair_path")
    component = next(c for c in seed["evidence"]["endpoints"] if c["eliminated"])
    assert component["source_forbidden"][0] not in component["fixed_colors"]
    assert not any(c["direct_frame"]["eliminated"] for c in seed["evidence"]["components"])
    result += ["nonconserved_source_color_requires_endpoint_argument", "target_family_alone_has_no_fixed_frame"]
    witness = next(w for w in component["endpoint_family"]["witnesses"] if w["route"]["mode"] == "other_spoke")
    control = minor_control(ctx, component["component"], witness, length=3, external_length=3)
    es, bs = set(map(tuple, control["edges"])), list(map(set, control["branch_sets"]))
    path = control["path"]
    route = control["expanded_external_route"]
    removals = [("original_zw", ("z", "w")), ("other_original_spoke", route[-2:]),
                ("middle_original_bridge", path[:2]), ("last_original_bridge", path[-2:]),
                ("endpoint_contact", (path[-1], ctx["components"][component["component"]]["root"])),
                ("actual_endpoint_tether", control["actual_tether_routes"][1][0][-2:])]
    tests = [(label, es - {tuple(sorted(edge))}, bs) for label, edge in removals]
    tests.append(("overlapping_branch_sets", es, [bs[0] | {"z", "w"}, *bs[1:]]))
    for label, edges, bags in tests:
        try:
            verify_minor(edges, bags)
        except AssertionError:
            result.append(label)
        else:
            raise AssertionError(label)
    # Delete each original unary route in a witness whose outside arc is {b4}.
    for name in ("Dz", "Dw"):
        case = next(c for c in refined["failing_candidates"] if c["record_id"] == 14)
        rr = records[14]
        cc = context(rr, sources[rr["source_id"]])
        frame = case["evidence"]["components"][0]["direct_frame"]
        witness = next(w for w in frame["witnesses"] if w["route"]["component"] == name and tuple(w["frame_arcs"][2]) == (4,))
        control = minor_control(cc, 2, witness, 3, external_length=3)
        es, bs = set(map(tuple, control["edges"])), list(map(set, control["branch_sets"]))
        route = control["expanded_external_route"]
        start = route.index(name + "_0")
        for label, edge in (("contact", route[start-1:start+1]), ("internal", route[start:start+2]), ("attachment", route[-2:])):
            try:
                verify_minor(es - {tuple(sorted(edge))}, bs)
            except AssertionError:
                result.append(name + "_original_" + label)
            else:
                raise AssertionError((name, label))
    return result


def coverage_and_frontier(original, sources):
    previous = json.loads(HANDOFF.read_text())["coverage_extension"]
    old = set(previous["covered_source_join_ids"])
    added = {s["retained_join_id"] for s in sources}
    assert len(old) == 936 and len(added) == 236 and not old & added
    covered = sorted(old | added)
    sides = original["side_normal_forms"]
    pending = [dict(retained_join_id=i, side_ids=pair)
               for i, pair in enumerate(original["abstract_conditions"]["retained"])
               if len(sides[pair[0]]["root_boundary"]) == 1 and sides[pair[0]]["ports"] == [2, 1]
               and not sides[pair[1]]["root_boundary"] and sides[pair[1]]["ports"] == [2, 1, 1]]
    assert len(pending) == 180
    assert all(r["retained_join_id"] not in covered for r in pending)
    return (dict(previous_covered_source_joins=936, newly_covered_source_join_ids=sorted(added),
                 covered_source_join_ids=covered, covered_source_joins=len(covered),
                 remaining_source_joins=3548-len(covered), covered_unordered_cells=6,
                 remaining_unordered_cells=9, scope="necessary parameter classes, not realizing graphs"),
            dict(scope="B-E: t_z=1,(2,1), t_w=0,(2,1,1); IDs only, no support or target audit",
                 source_sha256=sha256(SOURCE.read_bytes()).hexdigest(), records=pending,
                 first_sides=[sides[i] for i in pending[0]["side_ids"]]))


def build():
    original = json.loads(SOURCE.read_text())
    sources = bind_sources(original)
    geometry = geometries()
    assert set(geometry) == independent_geometries()
    schemas = schema_audit()
    source_lookup = {}
    for src in sources:
        key = tuple(src["z"]["root_boundary"]), tuple(src["w"]["root_boundary"])
        source_lookup.setdefault(key, []).append(src)
    records, geometry_records, templates = [], [], []
    template_ids = {}
    for supports, placements in sorted(geometry.items()):
        gid = len(geometry_records)
        for placement in placements:
            order = placement["order"]
            if order not in template_ids:
                template_ids[order] = len(templates)
                templates.append(dict(id=len(templates), order=order, contact_rotations=rotations(order)))
            placement["rotation_template_id"] = template_ids[order]
            verify_placement(supports, placement, templates[template_ids[order]]["contact_rotations"])
        geometry_records.append(dict(id=gid, supports=supports, placements=placements))
        key = supports[2], supports[5]
        for src in source_lookup.get(key, []):
            if not all(len({Q[i] for i in supports[pos]}) >= 2
                       and valid_q_support(supports[pos], tuple(src[root]["forbidden"][col]))
                       for _, root, col, pos, _ in COMPONENTS):
                continue
            ids = {name: stable_schema_ids(src[root]["forbidden"][col][0], supports[pos])
                   for name, root, col, pos, k in COMPONENTS if k == 2}
            assert all(ids.values())
            q = row_evidence(src, supports, Q)
            assert len(q["joins"]) == 1 and q["joins"][0]["residuals"] == ([src["common"]],) * 2
            records.append(dict(id=len(records), source_id=src["id"], source_side_ids=src["side_ids"],
                                geometry_id=gid, supports=supports, common=src["common"],
                                q_schema_ids=ids, q_single_contact_relations={name: ((src[root]["forbidden"][col][0],),)
                                    for name, root, col, _, k in COMPONENTS if k == 1},
                                q=q, targets=[row_evidence(src, supports, row) for row in TARGETS]))
    reflected = symmetry_audit(records, sources)
    transported = relation_audit(records, sources, schemas)
    fibers = [dict(source_id=s["id"], retained_join_id=s["retained_join_id"], side_ids=s["side_ids"],
                   support_record_ids=[r["id"] for r in records if r["source_id"] == s["id"]]) for s in sources]
    for fiber in fibers:
        fiber["classification"] = "necessary_supports_present" if fiber["support_record_ids"] else "no_compatible_disk_support"
    queries = [dict(record_id=r["id"], source_id=r["source_id"], target_index=i, row=t["row"],
                    failing_joins=[j for j in t["joins"] if not j["root_pairs"]])
               for r in records for i, t in enumerate(r["targets"]) if t["status"] == "unresolved"]
    reasons = Counter(reason for q in queries for j in q["failing_joins"] for reason in j["obstruction_reasons"])
    closures = Counter(t["closure_reason"] for r in records for t in r["targets"] if t["closure_reason"])
    outcomes = Counter(tuple(t["status"] for t in r["targets"]) for r in records)
    assert len(geometry) == sum(map(len, geometry.values())) == 2520
    assert len(records) == 888 and len(queries) == 120
    assert outcomes == {("accept", "accept"): 768, ("accept", "unresolved"): 60, ("unresolved", "accept"): 60}
    assert reasons == {"empty_z": 60, "empty_w": 60}
    assert closures == {"complete_relation_transport": 1296, "transport_and_capacity_bound": 360}
    assert sum(not f["support_record_ids"] for f in fibers) == 144
    refined = refinement(records, sources)
    negatives = negative_controls(geometry, records, sources, refined)
    coverage, frontier = coverage_and_frontier(original, sources)
    summary = dict(original_frontier=len(sources), geometric_supports=len(geometry),
                   placements=sum(map(len, geometry.values())), necessary_support_records=len(records),
                   source_records_with_support=sum(bool(f["support_record_ids"]) for f in fibers),
                   empty_source_fibers=sum(not f["support_record_ids"] for f in fibers),
                   target_queries=2 * len(records), initial_target_accepts=2 * len(records) - len(queries),
                   initial_unresolved_target_queries=len(queries), closure_reasons=dict(sorted(closures.items())),
                   failing_candidate_causes=dict(sorted(reasons.items())),
                   target_candidate_joins=sum(len(t["joins"]) for r in records for t in r["targets"]),
                   literal_target_reflections=reflected, support_records_excluded=0,
                   final_accepts=1776, final_unresolved_queries=0, both_targets_proved=888,
                   target_only_candidate_exclusions=refined["candidate_stages"],
                   whole_relation_transport_checks=transported, whole_source_root_swaps=len(records),
                   complete_join_root_swaps=refined["complete_join_root_swaps"],
                   contact_rotation_checks=4 * sum(map(len, geometry.values())),
                   minor_controls=len(refined["minor_controls"]), negative_controls=len(negatives))
    inputs = [str(p.relative_to(ROOT)) for p in (SOURCE, HANDOFF)] + ["scripts/" + name + ".py" for name in (
        "c5_adjacent_degree5_no_mixed_t2", "c5_adjacent_degree5_mixed_edge_shared",
        "c5_adjacent_degree5_singleton_long_arc", "c5_root_degree_excess", "c5_single_spoke_cores",
        "c5_adjacent_degree5_no_mixed_t2_t1_bridge", "c5_adjacent_degree5_no_mixed_t2_t1_endpoints",
        "c5_no_spoke_first_bridge", "c5_single_spoke_first_bridge", "c5_single_spoke_frame_arc",
        "c5_single_spoke_two_two_minor", "c5_single_spoke_two_two_external")]
    return dict(schema=1, scope="necessary same-source supports and complete relation bounds; no disk realization or Lean theorem",
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                inputs_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
                summary=summary, original_records=sources, source_fibers=fibers,
                geometries=geometry_records, rotation_templates=templates,
                q_complete_binary_schemas=schemas, records=records, initial_open_queries=queries, open_queries=[],
                refinement=refined, negative_controls=negatives, coverage_extension=coverage, next_frontier=frontier)


def render(data):
    lines = ["# 無 mixed B–B：兩側 t=1,(2,1) 的必要支援", "",
             "支援順序 Cz / Dz / z0 / Cw / Dw / w0；Dz、Dw 是原單接點分量，不是 root-spokes。",
             "所有原 source 兩側 (D,O,kappa)=(1,0,0)，兩側分量缺額均為 (1,0)。",
             "完整上界先接受 1,656／1,776；120 個失敗候選經原路徑／雙端點全部排除。必要表均未證來源可實現性。", "",
             "| ID | 原子表 ID | 原側 IDs | 實際支援 | p₁ 關閉原因 | p₂ 關閉原因 |",
             "| ---: | ---: | --- | --- | --- | --- |"]
    for r in data["records"]:
        supports = " / ".join("".join(map(str, s)) for s in r["supports"])
        statuses = [t["closure_reason"] or "?" for t in r["final_targets"]]
        lines.append(f'| {r["id"]} | {r["source_id"]} | {r["source_side_ids"]} | {supports} | {statuses[0]} | {statuses[1]} |')
    lines += ["", "## 原 236 份資料的完整纖維", "",
              "| 原子表 ID | 原側 IDs | 支援筆數 |", "| ---: | --- | ---: |"]
    for f in data["source_fibers"]:
        lines.append(f'| {f["source_id"]} | {f["side_ids"]} | {len(f["support_record_ids"])} |')
    lines += ["", "逐候選拒絕原因、完整 schemas、六接點 rotations 與原 ID／SHA 見 [JSON](observations.json)。",
              "任意大小覆蓋及界線見 [研究報告](../../docs/c5_adjacent_degree5_no_mixed_bb.md)。", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    for path, payload in ((OUT, json.dumps(result, sort_keys=True, indent=2) + "\n"), (TABLE, render(result))):
        if args.check:
            assert path.read_bytes() == payload.encode(), f"certificate differs: {path}"
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload)
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
