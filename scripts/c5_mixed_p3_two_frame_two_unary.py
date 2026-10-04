#!/usr/bin/env python3
"""Fixed CPP-134-1 / geometry34 / side_join60 componentwise obstruction.

The paper proof acts on full original coloring lifts, including every bridge.
The finite certificate exhausts the nine necessary support covers and the exact
saturated contact-relation candidates.  Parent data are read without mutation.
"""

import argparse
from itertools import combinations, product
import json
from pathlib import Path

import c5_mixed_p3_two_frame_ternary_unary as c3

c2, common, base, capacity = c3.c2, c3.common, c3.base, c3.capacity
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_mixed_p3_two_frame_two_unary/observations.json"
Q, U, SIGMA = c3.Q, c3.U, (0, 1, 3, 2)
D2_CONTACTS, D1_CONTACTS = (10, 11), (12,)
SUPPORTS = ((), (1,), (2,), (1, 2))


def permute(t):
    return tuple(SIGMA[c] for c in t)


def forbidden(relation):
    assert relation
    return frozenset.intersection(*(frozenset(t) for t in relation))


def fibers(relation):
    return [dict(z=h, complete_contact_tuples=sorted(t for t in relation if h not in t))
            for h in range(4)]


def fixed_identity():
    previous = json.loads(c3.OUT.read_bytes())
    for name, expected in previous["inputs_sha256"].items():
        assert c3.digest(ROOT / name) == expected, f"stale C3 input: {name}"
    inherited = c3.fixed_identity()
    entry = previous["identity"]["next_entry"]
    assert entry == json.loads(json.dumps(inherited["next_entry"]))
    assert (entry["case_name"], entry["geometry_id"], entry["side_join_id"]) == (
        "CPP-134-1", 34, 60)
    assert entry["side_ids"] == [27, 1]
    parent = json.loads(c3.PARENT.read_bytes())
    case = parent["local"]["cases"][86]
    assert 60 in case["side_join_ids"]
    assert entry["z_role"]["unary_contacts"] == [2, 1]
    assert entry["z_role"]["unary_forbidden"] == [[0, 3], [2]]
    assert entry["w_role"]["unary_contacts"] == [3]
    assert entry["w_role"]["unary_forbidden"] == [[0, 2]]
    assert entry["z_role"]["spoke_colors"] == entry["w_role"]["spoke_colors"] == []
    assert entry["actual_side_supports"] == [[1, 2], [2, 4]]
    assert entry["actual_supports"] == [[0, 1, 4], [1, 4], [4]]
    joint = frozenset(product(entry["z_role"]["residual"], entry["w_role"]["residual"]))
    joint -= frozenset(map(tuple, inherited["original_P3_forbidden"]))
    assert joint == {(1, 1)} and not joint - base.DELTA
    components = [dict(name="D_z2", ordered_contacts=["u0", "u1"],
        root_incidence_count=2, forbidden=[0, 3],
        actual_support="A_2: exact original support unknown; subset {b1,b2}",
        relation="T_2(q): full original two-contact relation, not marginals"),
        dict(name="D_z1", ordered_contacts=["r0"], root_incidence_count=1,
        forbidden=[2], actual_support="A_1: exact original support unknown; subset {b1,b2}",
        relation="T_1(q): full original one-contact relation")]
    return dict(case=case, local=inherited["local"], geometry=inherited["geometry"],
        side_join_id=60, side_ids=entry["side_ids"], z_role=entry["z_role"],
        w_role=entry["w_role"], common_color_frame=Q, parent_entry=entry,
        original_context_edges=inherited["original_context_edges"],
        original_P3_complete_tuples=inherited["original_P3_complete_tuples"],
        original_P3_lists=inherited["original_P3_lists"],
        original_P3_forbidden=inherited["original_P3_forbidden"],
        original_root_join_without_zw=sorted(joint), original_root_join_with_zw=[],
        original_external_paths=[[5, 9, 4], [5, 9, 4, 3, 2, 1]],
        original_z_components=components,
        original_support_cover_equation="A_2 union A_1 = {b1,b2}; no support chosen",
        original_bridges="all E(D_z2), E(D_z1), including bridges, retained in full lifts",
        preserved_w_component=inherited["preserved_w_component"],
        positive_geometry_control=inherited["positive_geometry_control"],
        scope="only the named join60 key; detached unary relations precede root queries")


def exact_relation_candidates(arity, required_forbidden):
    # |f| = arity forces every tuple to use each required color exactly once.
    assert len(required_forbidden) == arity
    allowed = tuple(t for t in product(range(4), repeat=arity)
                    if set(t) == set(required_forbidden))
    rows = []
    for n in range(1, len(allowed) + 1):
        for ts in combinations(allowed, n):
            relation, image = frozenset(ts), frozenset(map(permute, ts))
            assert forbidden(relation) == frozenset(required_forbidden)
            assert forbidden(image) == frozenset(SIGMA[c] for c in required_forbidden)
            assert relation.isdisjoint(image)
            for h in range(4):
                assert {permute(t) for t in relation if h not in t} == {
                    t for t in image if SIGMA[h] not in t}
            rows.append(dict(id=len(rows), ordered_complete_relation=sorted(relation),
                required_forbidden=sorted(required_forbidden),
                sigma_image_complete_relation=sorted(image),
                sigma_image_forbidden=sorted(forbidden(image)),
                forced_missing_tuples=sorted(image - relation),
                root_avoidance_fibers=fibers(relation), image_root_avoidance_fibers=fibers(image),
                compatible_with_full_original_lift_involution=relation == image))
    assert len(rows) == (3 if arity == 2 else 1)
    return rows


def support_controls(binary, unary):
    own, covers = [], []
    binary_survivors = [r["id"] for r in binary
        if r["compatible_with_full_original_lift_involution"]]
    unary_survivors = [r["id"] for r in unary
        if r["compatible_with_full_original_lift_involution"]]
    assert not binary_survivors and not unary_survivors
    for support in SUPPORTS:
        seen = sorted({Q[b] for b in support})
        assert all(SIGMA[c] == c for c in seen)
        own.append(dict(actual_support_candidate=support, actual_attachment_colors=seen,
            sigma_fixes_every_possible_attachment=True,
            binary_complete_relation_candidate_ids=[r["id"] for r in binary],
            unary_complete_relation_candidate_ids=[r["id"] for r in unary],
            binary_survivors=binary_survivors, unary_survivors=unary_survivors))
    for a2, a1 in product(SUPPORTS, repeat=2):
        if set(a2) | set(a1) != {1, 2}:
            continue
        covers.append(dict(id=len(covers), D_z2_actual_support_candidate=a2,
            D_z1_actual_support_candidate=a1,
            D_z2_sigma_fixed_attachment_colors=sorted({Q[b] for b in a2}),
            D_z1_sigma_fixed_attachment_colors=sorted({Q[b] for b in a1}),
            candidate_complete_relation_pairs=[dict(binary_relation_id=r["id"],
                unary_relation_id=unary[0]["id"],
                binary_compatible=r["compatible_with_full_original_lift_involution"],
                unary_compatible=unary[0]["compatible_with_full_original_lift_involution"])
                for r in binary], survivors=[(b, u) for b in binary_survivors for u in unary_survivors]))
    assert len(own) == 4 and len(covers) == 9
    return dict(scope="exhaustive necessary covers; no arbitrary assignment or realization",
        individual_support_candidates=own, ordered_original_component_support_covers=covers)


def involution_controls():
    assert all(SIGMA[SIGMA[c]] == c for c in range(4))
    internal = []
    for a, b in product(range(4), repeat=2):
        assert (a != b) == (SIGMA[a] != SIGMA[b])
        internal.append(dict(original_ordered_endpoint_colors=[a, b],
            image_ordered_endpoint_colors=[SIGMA[a], SIGMA[b]],
            proper_before=a != b, proper_after=SIGMA[a] != SIGMA[b]))
    attachments = []
    for b, c in product((1, 2), range(4)):
        assert SIGMA[Q[b]] == Q[b]
        assert (c != Q[b]) == (SIGMA[c] != Q[b])
        attachments.append(dict(actual_boundary_vertex=b, fixed_boundary_color=Q[b],
            internal_color=c, image_internal_color=SIGMA[c],
            attachment_proper_before=c != Q[b], attachment_proper_after=SIGMA[c] != Q[b]))
    domains = [dict(arity=n, tuples=[dict(original=t, image=permute(t))
        for t in product(range(4), repeat=n)]) for n in (1, 2)]
    return dict(sigma=SIGMA, action="only one detached original unary coloring lift",
        full_lift_map="phi(v) -> sigma(phi(v)), for every original v in D_i",
        preserved="vertex IDs, contact order, all internal edges/bridges and actual B attachments",
        local_root_fiber_map="T_i[h] -> T_i[sigma(h)]; not a whole-M root-coloring claim",
        unchanged_exterior="B/P3/zw/wx2/other unary/D_w; b4=2 stays fixed",
        internal_edge_and_original_bridge_truth_table=internal,
        actual_attachment_truth_table=attachments, complete_ordered_tuple_domains=domains)


def ownership_controls(binary, unary):
    rows = []
    for r in binary:
        ts = frozenset(tuple(t) + tuple(unary[0]["ordered_complete_relation"][0])
                       for t in r["ordered_complete_relation"])
        assert forbidden(ts) == {0, 2, 3}
        image = frozenset(map(permute, ts))
        assert forbidden(image) == {0, 2, 3} and image.isdisjoint(ts)
        rows.append(dict(binary_relation_id=r["id"],
            ordered_contacts_with_ownership=["D_z2.u0", "D_z2.u1", "D_z1.r0"],
            required_product_complete_relation=sorted(ts), sigma_image=sorted(image),
            aggregate_forbidden=[0, 2, 3], aggregate_forbidden_sigma_invariant=True,
            original_component_product_sigma_invariant=False,
            sigma_closure_is_not_original_relation=True))
    return rows


def aggregate_bridge_control(identity):
    """Same-frame degree-four control; its ownership differs from join 60."""
    from itertools import product
    c2, base = c3.c2, c3.base
    context = frozenset(map(tuple, identity["original_context_edges"]))
    q = tuple(identity["common_color_frame"])
    assert q == (0, 1, 0, 1, 2)
    sigma = (0, 1, 3, 2)
    binary = base.make_region("control_binary_original_bridge", [(20, 21)],
        {20: (5, 1, 2), 21: (5, 1, 2)})
    unary = base.make_region("control_one_contact_two_N_triangles_bridge",
        [(30, 31), (31, 32), (32, 30), (33, 34), (34, 35), (35, 33), (30, 33)],
        {30: (5,), 31: (1, 2), 32: (1, 2), 33: (2,), 34: (1, 2), 35: (1, 2)})

    def all_lifts(region, deleted=frozenset(), root_pin=None, endpoint_pin=None):
        edges = region["edges"] - deleted
        vertices = region["vertices"]
        internal = [(u, v) for u, v in edges if u in vertices and v in vertices]
        lists = {v: tuple(c for c in range(4) if all(
            c != q[b] for b in range(5) if base.edge(v, b) in edges)) for v in vertices}
        lifts = []
        for values in product(*(lists[v] for v in vertices)):
            coloring = dict(zip(vertices, values))
            if not all(coloring[u] != coloring[v] for u, v in internal):
                continue
            if root_pin is not None and not all(coloring[v] != root_pin
                for v in region["ports_z"] if base.edge(v, 5) in edges):
                continue
            if endpoint_pin is not None and not all(coloring[v] == c
                for v, c in endpoint_pin.items()):
                continue
            lifts.append(coloring)
        return lifts

    records = []
    for region, requested, expected in ((binary, [0, 3], [2, 3]), (unary, [2], [0])):
        lifts = all_lifts(region)
        ports = region["ports_z"]
        full = sorted({tuple(lift[v] for v in ports) for lift in lifts})
        forbidden = sorted(set.intersection(*(set(t) for t in full)))
        assert forbidden == expected
        support = sorted({b for v in region["vertices"] for b in range(5)
                          if base.edge(v, b) in region["edges"]})
        assert support == [1, 2]
        degrees = {v: sum(v in e for e in region["edges"]) for v in region["vertices"]}
        assert set(degrees.values()) == {4}
        lift_keys = {tuple(lift[v] for v in region["vertices"]) for lift in lifts}
        for lift in lifts:
            transformed = {v: sigma[c] for v, c in lift.items()}
            assert tuple(transformed[v] for v in region["vertices"]) in lift_keys
        bridges = [e for e in sorted(region["edges"]) if all(v in region["vertices"] for v in e)
                   and not base.is_connected(region["vertices"], region["edges"] - {e})]
        assert bridges == ([(20, 21)] if region is binary else [(30, 33)])
        bridge_records = []
        for e in bridges:
            pin_records = []
            for h in range(4):
                removed = all_lifts(region, frozenset({e}), h)
                endpoint_relation = sorted({tuple(lift[v] for v in e) for lift in removed})
                pin_records.append(dict(root_z=h, ordered_endpoints=e,
                    complete_endpoint_relation=endpoint_relation,
                    full_same_deleted_component_lifts=removed))
            bridge_records.append(dict(original_edge=e, pins=pin_records,
                scope="complete joint endpoint relations of one actual deleted component; no marginal join"))
        records.append(dict(name=region["name"], vertices=region["vertices"],
            original_edges=sorted(region["edges"]), actual_support=support,
            ordered_contacts=ports, complete_contact_relation=full,
            full_same_component_lifts=lifts,
            sigma_transformed_full_lifts=[{v: sigma[c] for v, c in lift.items()} for lift in lifts],
            requested_join60_forbidden=requested, control_forbidden=forbidden,
            complete_degrees=degrees,
            original_bridge_records=bridge_records,
            fibers=[dict(root_z=h, complete_contact_fiber=[t for t in full if h not in t],
                full_same_component_lifts=all_lifts(region, root_pin=h)) for h in range(4)]))

    all_edges = context | binary["edges"] | unary["edges"]
    control_vertices = tuple(range(10)) + binary["vertices"] + unary["vertices"]
    global_contacts = binary["ports_z"] + unary["ports_z"]
    joint_lifts = []
    for binary_lift, unary_lift in product(all_lifts(binary), all_lifts(unary)):
        coloring = binary_lift | unary_lift
        joint_lifts.append(dict(ordered_contact_tuple=tuple(coloring[v] for v in global_contacts),
            full_both_component_lift=coloring))
    joint_tuples = sorted({lift["ordered_contact_tuple"] for lift in joint_lifts})
    assert joint_tuples == [(2, 3, 0), (3, 2, 0)]
    joint_forbidden = sorted(set.intersection(*(set(t) for t in joint_tuples)))
    assert joint_forbidden == [0, 2, 3]
    assert sum(5 in e for e in all_edges) == 5
    assert all(sum(v in e for e in all_edges) == 4
               for v in (7, 8, 9, *binary["vertices"], *unary["vertices"]))
    fixed = dict(enumerate(q)) | {5: 1, 6: 1}
    assert base.first_coloring(control_vertices, all_edges, fixed) is None
    partial = base.first_coloring(control_vertices, all_edges - {base.edge(5, 6)}, fixed)
    c2.check_coloring(control_vertices, all_edges - {base.edge(5, 6)}, fixed, partial)
    assert tuple(partial[v] for v in (7, 8, 9)) == (3, 0, 3)
    a, b = 34, 35
    hub = (set(unary["vertices"]) - {a, b}) | {5, 9, 0, 4, 3}
    groups = [{a}, {b}, {1}, {2}, hub]
    adjacency = c2.minor_adjacency(all_edges, groups)
    return dict(scope="fixed degree-four separate-component negative ownership control; nonplanar and no source realization or full-M minimality claim",
        original_context_edges=sorted(context), common_color_frame=q,
        actual_union_support=[1, 2], components=records,
        requested_join60_forbidden=[[0, 3], [2]], control_forbidden=[[2, 3], [0]],
        global_ordered_z_contacts=global_contacts,
        complete_global_z_contact_relation=joint_tuples,
        full_both_component_lifts=joint_lifts,
        aggregate_forbidden=joint_forbidden,
        aggregate_fibers=[dict(root_z=h, complete_contact_fiber=[t for t in joint_tuples if h not in t])
                          for h in range(4)],
        original_projection_edges=sorted(all_edges),
        original_root_z_complete_degree=5,
        context_partial_witness=dict(root_z=1, root_w=1, omitted_edge=base.edge(5, 6),
            coloring=partial, original_P3_tuple=(3, 0, 3),
            unknown_w_component="kept symbolic: same-original R_Dw(q) avoiding 1 is nonempty from F_Dw={0,2}",
            scope="proper coloring of named original context plus both controls after omitting zw; not intact M or D_w lift"),
        original_K5_minor=dict(branch_sets=[sorted(g) for g in groups], adjacency=adjacency,
            selected_N_leaf_vertices=[a, b],
            original_hub_paths=[[30, 5], [5, 9, 4], [0, 4, 3]],
            scope="original edges and original external P3 path certify nonplanarity of this control"))


def build():
    identity = fixed_identity()
    binary = exact_relation_candidates(2, (0, 3))
    unary = exact_relation_candidates(1, (2,))
    supports = support_controls(binary, unary)
    covers = supports["ordered_original_component_support_covers"]
    control = aggregate_bridge_control(identity)
    sources = (Path(__file__).resolve(), Path(c3.__file__).resolve(), Path(c2.__file__).resolve(),
        Path(common.__file__).resolve(), Path(capacity.__file__).resolve(), Path(base.__file__).resolve(),
        c3.PARENT, c3.PREVIOUS, c3.OUT, common.ROTATIONS)
    return dict(schema=1,
        scope="only CPP-134-1 / geometry34 / join60 source exclusion by full original component lifts; arbitrary-size paper proof plus finite relation controls; no target/Lean theorem",
        identity=identity, involution_controls=involution_controls(),
        binary_exact_complete_relation_candidates=binary,
        unary_exact_complete_relation_candidates=unary,
        support_controls=supports, aggregate_bridge_control=control,
        ownership_controls=ownership_controls(binary, unary),
        summary=dict(named_source_branches_closed=1, individually_impossible_original_components=2,
            own_support_candidates=4, original_support_cover_candidates=9,
            binary_exact_complete_relations=3, unary_exact_complete_relations=1,
            coupled_support_relation_checks=sum(len(r["candidate_complete_relation_pairs"]) for r in covers),
            coupled_survivors=sum(len(r["survivors"]) for r in covers),
            complete_ordered_tuple_domain_checks=20, universal_internal_edge_bridge_color_checks=16,
            actual_attachment_checks=8, root_fibers_per_relation=4,
            aggregate_ownership_negative_controls=1,
            control_complete_component_lifts=sum(len(r["full_same_component_lifts"]) for r in control["components"]),
            control_complete_joint_lifts=len(control["full_both_component_lifts"]),
            control_original_bridges=sum(len(r["original_bridge_records"]) for r in control["components"]),
            control_deleted_bridge_endpoint_relations=sum(len(b["pins"]) for r in control["components"]
                for b in r["original_bridge_records"]),
            control_deleted_bridge_lifts=sum(len(p["full_same_deleted_component_lifts"])
                for r in control["components"] for b in r["original_bridge_records"] for p in b["pins"]),
            control_k5_minors=1,
            original_P3_tuples=2, preserved_w_original_contacts=3,
            target_queries=0, predecessor_cases=36, predecessor_geometries=140,
            predecessor_joins=900, predecessor_deletions=0),
        inputs_sha256={str(p.relative_to(ROOT)): c3.digest(p) for p in sources})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build()
    raw = (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode()
    if args.check:
        assert OUT.read_bytes() == raw, f"stale artifact: {OUT}"
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(raw)
    print(json.dumps(dict(**data["summary"], artifact_bytes=len(raw)), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
