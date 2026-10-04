#!/usr/bin/env python3
"""Fixed CPP-134-1 / geometry 34 / side_join 20 source obstruction.

The arbitrary-size tight-block and leaf-block extraction is a paper argument.
This checker retains the same source/frame identities, verifies the two-frame
degree-list accounting, and certifies finite actual-edge K5 controls.  No
predecessor table is regenerated, filtered, or treated as a source realization.
"""

import argparse
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import c5_mixed_p3_one_color_ternary_unary as c2

common, base, capacity = c2.common, c2.base, c2.capacity
ROOT = Path(__file__).resolve().parents[1]
PARENT = common.OUT
PREVIOUS = c2.OUT
OUT = ROOT / "artifacts/c5_mixed_p3_two_frame_ternary_unary/observations.json"
U, Q, CONTACTS = c2.U, c2.Q, c2.CONTACTS


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def fixed_identity():
    parent = json.loads(PARENT.read_bytes())
    previous = json.loads(PREVIOUS.read_bytes())
    for manifest in (parent["scripts_sha256"], previous["inputs_sha256"]):
        for name, expected in manifest.items():
            assert digest(ROOT / name) == expected, f"stale predecessor input: {name}"
    entry = previous["identity"]["next_entry"]
    assert (entry["case_name"], entry["geometry_id"], entry["side_join_id"]) == (
        "CPP-134-1", 34, 20)
    geometry = parent["geometry"]["retained_geometries"][34]
    case = parent["local"]["cases"][geometry["case_id"]]
    local = parent["local"]["configurations"][geometry["local_id"]]
    assert entry["geometry"] == geometry
    assert geometry["id"] == 34 and geometry["case_id"] == 86
    assert case["name"] == "CPP-134-1" and case["branch"] == 1
    assert local["id"] == 134 and 20 in case["side_join_ids"]
    assert local["actual_supports"] == [[0, 1, 4], [1, 4], [4]]
    assert geometry["actual_side_supports"] == [[1, 2], [2, 4]]
    assert geometry["J"] == [1, 4]
    assert geometry["block_lifts"] == [[1, 2], [2, 4], [4]]
    assert geometry["named_order"] == ["A_z", "A_w", "S2"]
    supports = tuple(map(tuple, local["actual_supports"]))
    lists, triples, forbidden = common.interface(supports)
    assert lists == [{3}, {0, 3}, {0, 1, 3}]
    assert triples == ((3, 0, 1), (3, 0, 3))
    assert list(map(list, triples)) == local["complete_triples"]
    assert forbidden == {(1, 3), (3, 1)}
    joins = capacity.minimal_side_joins(forbidden, 1, 1)
    join = json.loads(json.dumps(joins[20]))
    ids = parent["local"]["joins_by_a"]["1"][20]
    assert ids == entry["side_ids"] == [8, 1]
    assert join["z"] == entry["z_role"] == parent["local"]["side_roles"][8]
    assert join["w"] == entry["w_role"] == parent["local"]["side_roles"][1]
    assert join["z"]["unary_contacts"] == join["w"]["unary_contacts"] == [3]
    assert join["z"]["unary_forbidden"] == [[0, 2, 3]]
    assert join["w"]["unary_forbidden"] == [[0, 2]]
    assert join["z"]["spoke_colors"] == join["w"]["spoke_colors"] == []
    joint = frozenset(product(join["z"]["residual"], join["w"]["residual"])) - forbidden
    assert joint == {(1, 1)} and not joint - base.DELTA
    rotation_data = json.loads(common.ROTATIONS.read_bytes())
    rotation, = [r for r in rotation_data["records"] if r["local_id"] == 134
                 and r["Ez"] == [1] and r["Ew"] == [1, 3]
                 and r["side_supports"] == [[1, 2], [2, 4]]]
    skeleton = common.skeleton_edges(supports, ((1, 2), (2, 4)))
    faces = common.rotation_faces(rotation["rotation"], skeleton)
    assert [sum(v in e for e in skeleton) for v in (5, 6)] == [4, 4]
    next_ids = parent["local"]["joins_by_a"]["1"][60]
    next_join = json.loads(json.dumps(joins[60]))
    assert 60 in case["side_join_ids"] and next_ids == [27, 1]
    assert next_join["z"] == parent["local"]["side_roles"][27]
    assert next_join["w"] == join["w"]
    assert next_join["z"]["spoke_colors"] == []
    assert next_join["z"]["unary_contacts"] == [2, 1]
    assert next_join["z"]["unary_forbidden"] == [[0, 3], [2]]
    return dict(case=case, local=local, geometry=geometry, side_join_id=20,
        side_ids=ids, z_role=join["z"], w_role=join["w"], common_color_frame=Q,
        aliases=c2.ALIASES, original_context_edges=sorted(c2.original_context_edges(supports)),
        original_P3_lists=[sorted(ls) for ls in lists], original_P3_complete_tuples=triples,
        original_P3_forbidden=sorted(forbidden), preserved_original_external_path=[5, 9, 4],
        original_root_join_without_zw=sorted(joint), original_root_join_with_zw=[],
        positive_geometry_control=dict(rotation=rotation["rotation"], faces=faces,
            root_degrees=[4, 4], scope="contracted geometry only; not original root-spokes"),
        preserved_z_component=dict(name="D_z", ordered_contacts=["u0", "u1", "u2"],
            actual_support=[1, 2], root="z", root_incidence_count=3, forbidden=[0, 2, 3],
            relation="R_Dz(q) subset U^3, full original same-source relation unknown",
            required_equation="intersection_{t in R_Dz(q)} set(t) = {0,2,3}"),
        preserved_w_component=previous["identity"]["preserved_w_component"],
        next_entry=dict(case_name="CPP-134-1", geometry_id=34, side_join_id=60,
            actual_supports=local["actual_supports"], actual_side_supports=geometry["actual_side_supports"],
            complete_triples=triples, J=geometry["J"], side_ids=next_ids,
            z_role=next_join["z"], w_role=next_join["w"],
            preserved_original_external_path=[5, 9, 4],
            scope="next named incidence partition, not analyzed by this checker"))


def local_degree_lists():
    """Keep double-frame noncontacts, rather than importing C2 contact charges."""
    rows = []
    for p, s1, s2 in product((False, True), repeat=3):
        incidences = int(p) + int(s1) + int(s2)
        degree = 4 - incidences
        pins = []
        for h in range(4):
            external = ([h] if p else []) + ([Q[1]] if s1 else []) + ([Q[2]] if s2 else [])
            ls = U - set(external)
            slack = len(ls) - degree
            assert slack == incidences - len(set(external))
            assert slack == int(p and ((h == 1 and s1) or (h == 0 and s2)))
            if h == 0:
                assert (slack > 0) == (p and s2)
            if h in (2, 3):
                assert slack == 0
            pins.append(dict(z=h, external_colors=external, list=sorted(ls), slack=slack))
        retained = not (p and s2)
        kind = "T" if retained and degree == 2 and p and s1 else (
            "N" if retained and degree == 2 and not p and s1 and s2 else None)
        if retained:
            assert degree >= 2
            assert (degree == 2) == (kind is not None)
        rows.append(dict(original_z_contact=p, original_b1_attachment=s1,
            original_b2_attachment=s2, degree_in_D=degree, pinned_lists=pins,
            compatible_with_pin_zero_tightness=retained, private_degree_two_type=kind,
            exclusion_scope="pin-zero slack implies source exclusion by paper degree-list lemma" if not retained else None))
    assert len(rows) == 8 and sum(len(r["pinned_lists"]) for r in rows) == 32
    assert sum(r["compatible_with_pin_zero_tightness"] for r in rows) == 6
    return rows


def leaf_palette_controls(rows):
    private = {r["private_degree_two_type"]: r for r in rows if r["private_degree_two_type"]}
    assert set(private) == {"T", "N"}
    pins = []
    for h in (2, 3):
        palettes = {kind: row["pinned_lists"][h]["list"] for kind, row in private.items()}
        assert palettes["T"] == sorted(U - {1, h})
        assert palettes["N"] == [2, 3] and palettes["T"] != palettes["N"]
        for left, right in product(("T", "N"), repeat=2):
            assert (palettes[left] == palettes[right]) == (left == right)
        pins.append(dict(z=h, private_type_palettes=palettes,
            equal_palette_pairs=[[a, b] for a, b in product(("T", "N"), repeat=2)
                                 if palettes[a] == palettes[b]]))
    return dict(scope="finite palette accounting; Gallai uniform private leaf palette and arbitrary-size extraction are paper proof",
        pins=pins, paper_leaf_conclusions=dict(single_edge_leaf="impossible because degree_in_D >= 2",
            possible_leaf_blocks="odd cycle or K4 before original-exterior minor exclusion",
            pure_N_cycle="two adjacent private N vertices produce original K5 minor",
            pure_T_leaf="at least two distinct original contacts", total_original_contacts=3,
            multiple_blocks_minimum_T_leaf_contacts=4,
            sole_surviving_block="pure T triangle; support {b1}, incompatible with exact {b1,b2}"))


def k4_tether_controls(identity):
    context = frozenset(map(tuple, identity["original_context_edges"]))
    vertices, records = (30, 31, 32, 33), []
    for ends, subdivided in product(product((1, 2, 5), repeat=4), (False, True)):
        edges = set(context) | {base.edge(a, b) for a, b in combinations(vertices, 2)}
        hub, paths = set(range(5)) | {5, 9}, []
        for i, (v, end) in enumerate(zip(vertices, ends)):
            path = [v] + ([50+i] if subdivided else []) + [end]
            edges.update(base.edge(a, b) for a, b in zip(path, path[1:]))
            hub.update(path[1:-1])
            paths.append(path)
        groups = [{v} for v in vertices] + [hub]
        records.append(dict(tethers=paths, original_context_edges_retained=True,
            edges=sorted(edges), branch_sets=[sorted(g) for g in groups],
            adjacency=c2.minor_adjacency(edges, groups)))
    assert len(records) == 162
    return dict(scope="finite connected-exterior K4 routes; arbitrary original tethers are paper proof; no degree/minimality/source realization claim",
        endpoints=["b1", "b2", "z"], tether_lengths=[1, 2], records=records)


def n_leaf_controls(identity):
    """Nonplanar, degree-four local-critical controls, never original sources."""
    context = frozenset(map(tuple, identity["original_context_edges"]))
    records = []
    for n in (3, 5, 7, 9):
        cycle = list(range(20, 20+n))
        c, a, b = cycle[-1], cycle[0], cycle[1]
        internal = [base.edge(v, w) for v, w in zip(cycle, cycle[1:] + cycle[:1])]
        internal += list(combinations(CONTACTS, 2)) + [base.edge(c, CONTACTS[0])]
        attachments = {v: (1, 2) for v in cycle[:-1]}
        attachments |= {c: (2,), CONTACTS[0]: (5,), CONTACTS[1]: (1, 5), CONTACTS[2]: (1, 5)}
        region = base.make_region("control_N_leaf_bridge_T_triangle", internal, attachments)
        edges, vertices = region["edges"], tuple(range(7)) + region["vertices"]
        assert base.is_connected(region["vertices"], edges)
        assert all(sum(v in e for e in edges) == 4 for v in region["vertices"])
        actual_support = sorted({u for neighbors in attachments.values() for u in neighbors if u < 5})
        assert actual_support == [1, 2]
        relation, ports, full = base.joint_interface(region, Q)
        assert ports == CONTACTS and set(full) == set(permutations((0, 2, 3)))
        assert set.intersection(*(set(t) for t in full)) == {0, 2, 3}
        assert relation == frozenset((1, w) for w in range(4))
        tuple_witnesses = [dict(ordered_contact_tuple=t, coloring=dict(zip(region["vertices"], values)))
                           for t, values in sorted(full.items())]
        intact = []
        for h in range(4):
            fixed = dict(enumerate(Q)) | {5: h, 6: 1}
            coloring = base.first_coloring(vertices, edges, fixed)
            assert (coloring is None) == (h in (0, 2, 3))
            if coloring is not None:
                c2.check_coloring(vertices, edges, fixed, coloring)
            intact.append(dict(z=h, coloring=coloring))
        bridge = base.edge(c, CONTACTS[0])
        deleted_bridge = edges - {bridge}
        bridge_controls = []
        for h in (0, 2, 3):
            endpoint_lifts = []
            for left, right in product(range(4), repeat=2):
                fixed = dict(enumerate(Q)) | {5: h, 6: 1, c: left, CONTACTS[0]: right}
                coloring = base.first_coloring(vertices, deleted_bridge, fixed)
                if coloring is not None:
                    c2.check_coloring(vertices, deleted_bridge, fixed, coloring)
                    endpoint_lifts.append(dict(endpoint_colors=[left, right], coloring=coloring))
            endpoint_relation = [lift["endpoint_colors"] for lift in endpoint_lifts]
            assert endpoint_relation == [[1, 1]]
            bridge_controls.append(dict(z=h, w=1, deleted_edge=bridge,
                ordered_endpoints=[c, CONTACTS[0]], complete_endpoint_relation=endpoint_relation,
                full_same_deleted_graph_lifts=endpoint_lifts))
        projection = edges | context
        projection_vertices = tuple(range(10)) + region["vertices"]
        assert all(sum(v in e for e in projection) == 4 for v in (7, 8, 9, *region["vertices"]))
        assert sum(5 in e for e in projection) == 5
        deletions = []
        for e in sorted(edges):
            after, after_ports, _ = base.joint_interface(region, Q, frozenset({e}))
            assert after_ports == CONTACTS and after == base.PAIRS
            local_witnesses = []
            for h in range(4):
                fixed = dict(enumerate(Q)) | {5: h, 6: 1}
                coloring = base.first_coloring(vertices, edges - {e}, fixed)
                c2.check_coloring(vertices, edges - {e}, fixed, coloring)
                if h in (0, 2, 3):
                    assert coloring[e[0]] == coloring[e[1]]
                local_witnesses.append(dict(z=h, coloring=coloring))
            fixed = dict(enumerate(Q)) | {5: 0, 6: 1}
            coloring = base.first_coloring(projection_vertices, projection - {e}, fixed)
            c2.check_coloring(projection_vertices, projection - {e}, fixed, coloring)
            assert coloring[e[0]] == coloring[e[1]]
            assert tuple(coloring[v] for v in (7, 8, 9)) == (3, 0, 3)
            deletions.append(dict(deleted_edge=e, root_pair_relation_after=sorted(after),
                local_witnesses=local_witnesses, original_context_partial_witness=coloring,
                w_completion="original same-source D_w fiber avoiding w=1 exists by its role; not enumerated"))
        hub = (set(region["vertices"]) - {a, b}) | {5, 9, 0, 3, 4}
        groups = [{a}, {b}, {1}, {2}, hub]
        records.append(dict(cycle_length=n, leaf_cycle=cycle, cut_vertex=c,
            bridge=bridge, deleted_bridge_endpoint_controls=bridge_controls,
            ordered_contacts=CONTACTS, actual_support=actual_support,
            vertices=region["vertices"], actual_attachments=attachments,
            original_vertex_degrees={str(v): sum(v in e for e in edges) for v in region["vertices"]},
            edges=sorted(edges), complete_contact_tuples=sorted(full), tuple_witnesses=tuple_witnesses,
            forbidden=[0, 2, 3], root_pair_relation=sorted(relation), intact_pins=intact,
            deletions=deletions, original_context_edges_retained=True,
            original_context_projection_edges=sorted(projection),
            original_contact_path_to_z=[c, CONTACTS[0], 5],
            branch_set_names=["a", "b", "b1", "b2", "X"],
            branch_sets=[sorted(g) for g in groups], adjacency=c2.minor_adjacency(projection, groups)))
    assert [len(r["edges"]) for r in records] == [17, 23, 29, 35]
    return dict(scope="finite nonplanar degree-four, full-relation, locally edge-critical controls; never disk/source realizations or replacements for full original D_z/D_w",
        records=records)


def conditional_triangle(identity):
    triangle = c2.forced_triangle(identity)
    triangle["scope"] = ("conditional pure-T reduct only: exact support is {b1}, incompatible with original "
        "geometry34 support {b1,b2}; finite degree/edge-critical witnesses do not realize geometry34")
    triangle["conditional_reduct_actual_support"] = [1]
    triangle["required_original_actual_support"] = [1, 2]
    triangle["compatible_with_required_original_support"] = False
    return triangle


def build():
    identity = fixed_identity()
    rows = local_degree_lists()
    triangle = conditional_triangle(identity)
    n_controls = n_leaf_controls(identity)
    sources = (Path(__file__).resolve(), Path(c2.__file__).resolve(),
               Path(common.__file__).resolve(), Path(capacity.__file__).resolve(),
               Path(base.__file__).resolve(), PARENT, PREVIOUS, common.ROTATIONS)
    return dict(schema=1,
        scope="only CPP-134-1 / geometry34 / side_join20 source exclusion; arbitrary-size proof is paper plus external Gallai theorem; no target, disk realization, Lean or general theorem",
        identity=identity, local_degree_lists=rows, leaf_palette_controls=leaf_palette_controls(rows),
        n_leaf_controls=n_controls, conditional_triangle=triangle,
        k4_tether_controls=k4_tether_controls(identity),
        conditional_triangle_k5_subdivisions=c2.k5_subdivisions(triangle),
        summary=dict(named_source_branches_closed=1, local_vertex_types=8, pinned_list_checks=32,
            pin_zero_slack_excluded_vertex_types=2, degree_two_types=2, leaf_palette_pins=2,
            original_P3_tuples=2, preserved_w_original_contacts=3,
            n_leaf_controls=4, n_leaf_complete_tuple_checks=24, n_leaf_deleted_edges=104,
            n_leaf_local_deletion_colorings=416, n_leaf_original_context_partial_colorings=104,
            deleted_bridge_endpoint_relations=12, deleted_bridge_full_same_graph_lifts=12,
            n_leaf_k5_minors=4, conditional_triangle_complete_tuples=6,
            conditional_triangle_deleted_edges=9, conditional_triangle_local_deletion_colorings=36,
            conditional_triangle_original_context_partial_colorings=9,
            k4_tether_controls=162, conditional_triangle_k5_subdivisions=2,
            target_queries=0, predecessor_cases=36, predecessor_geometries=140,
            predecessor_joins=900, predecessor_deletions=0),
        inputs_sha256={str(p.relative_to(ROOT)): digest(p) for p in sources})


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
