#!/usr/bin/env python3
"""Fixed CPP-134-1 / geometry 30 / side_join 20 source obstruction.

The arbitrary-size Gallai/leaf-block extraction is proved in the report.
This checker preserves predecessor identities, full original P3 tuples,
the forced unary relation, deletion witnesses, and actual K5 routes.
No predecessor artifact is regenerated or filtered.
"""

import argparse
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import c5_mixed_p3_common_endpoint as common

base, capacity = common.base, common.capacity
ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "artifacts/c5_mixed_p3_common_endpoint/observations.json"
OUT = ROOT / "artifacts/c5_mixed_p3_one_color_ternary_unary/observations.json"
U, Q = frozenset(range(4)), base.Q
CONTACTS = (10, 11, 12)
ALIASES = {**{str(i): f"b{i}" for i in range(5)}, "5": "z", "6": "w",
           "7": "x0", "8": "x1", "9": "x2",
           **{str(v): f"u{i}" for i, v in enumerate(CONTACTS)}}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def original_context_edges(supports):
    edges = set(base.CYCLE) | {(5, 6), (5, 9), (6, 9), (7, 8), (8, 9)}
    for v, support in zip((7, 8, 9), supports):
        edges.update(base.edge(v, b) for b in support)
    return frozenset(edges)


def fixed_identity():
    data = json.loads(PARENT.read_bytes())
    for name, expected in data["scripts_sha256"].items():
        assert digest(ROOT / name) == expected, f"stale predecessor source: {name}"
    entry = data["next_entry"]
    assert (entry["case_name"], entry["geometry_id"], entry["side_join_id"]) == (
        "CPP-134-1", 30, 20)
    geometry = data["geometry"]["retained_geometries"][30]
    case = data["local"]["cases"][geometry["case_id"]]
    local = data["local"]["configurations"][geometry["local_id"]]
    assert geometry["id"] == 30 and geometry["case_id"] == 86
    assert case["name"] == "CPP-134-1" and local["id"] == 134
    assert 20 in case["side_join_ids"] and case["branch"] == 1
    assert local["actual_supports"] == [[0, 1, 4], [1, 4], [4]]
    assert entry["actual_supports"] == local["actual_supports"]
    assert geometry["actual_side_supports"] == [[1], [2, 4]]
    assert entry["actual_side_supports"] == geometry["actual_side_supports"]
    assert entry["J"] == geometry["J"] == [1, 4]
    assert geometry["block_lifts"] == [[1], [2, 4], [4]]
    assert entry["preserved_original_external_path"] == [5, 9, 4]
    supports = tuple(map(tuple, local["actual_supports"]))
    lists, triples, forbidden = common.interface(supports)
    assert lists == [{3}, {0, 3}, {0, 1, 3}]
    assert triples == ((3, 0, 1), (3, 0, 3))
    assert list(map(list, triples)) == local["complete_triples"] == entry["complete_triples"]
    assert forbidden == {(1, 3), (3, 1)}
    joins = capacity.minimal_side_joins(forbidden, 1, 1)
    join = json.loads(json.dumps(joins[20]))
    assert join["z"] == entry["z_role"] and join["w"] == entry["w_role"]
    assert data["local"]["joins_by_a"]["1"][20] == entry["side_ids"] == [8, 1]
    assert entry["z_role"]["unary_contacts"] == entry["w_role"]["unary_contacts"] == [3]
    assert entry["z_role"]["unary_forbidden"] == [[0, 2, 3]]
    assert entry["w_role"]["unary_forbidden"] == [[0, 2]]
    assert entry["z_role"]["spoke_colors"] == entry["w_role"]["spoke_colors"] == []
    joint = frozenset(product(entry["z_role"]["residual"], entry["w_role"]["residual"])) - forbidden
    assert joint == {(1, 1)} and not joint - base.DELTA
    rotation_data = json.loads(common.ROTATIONS.read_bytes())
    matches = [r for r in rotation_data["records"] if r["local_id"] == 134
               and r["Ez"] == [1] and r["Ew"] == [1, 3]
               and r["side_supports"] == [[1], [2, 4]]]
    rotation, = matches
    skeleton = common.skeleton_edges(supports, ((1,), (2, 4)))
    faces = common.rotation_faces(rotation["rotation"], skeleton)
    assert [sum(v in e for e in skeleton) for v in (5, 6)] == [3, 4]
    next_geometry = data["geometry"]["retained_geometries"][34]
    assert next_geometry["case_name"] == "CPP-134-1"
    assert next_geometry["actual_side_supports"] == [[1, 2], [2, 4]]
    return dict(parent_entry=entry, case=case, local=local, geometry=geometry,
        aliases=ALIASES, original_context_edges=sorted(original_context_edges(supports)),
        original_P3_lists=[sorted(ls) for ls in lists], original_P3_forbidden=sorted(forbidden),
        original_root_join_without_zw=sorted(joint), original_root_join_with_zw=[],
        positive_geometry_control=dict(rotation=rotation["rotation"], faces=faces,
            root_degrees=[3, 4], scope="contracted geometry only; not original root-spokes"),
        preserved_w_component=dict(name="D_w", ordered_contacts=["v0", "v1", "v2"],
            actual_support=[2, 4], root="w", root_incidence_count=3,
            forbidden=[0, 2], relation="R_Dw(q) subset U^3, full same-source relation unknown",
            required_equation="intersection_{t in R_Dw(q)} set(t) = {0,2}",
            scope="original necessary role preserved; no new tuple set or source realization"),
        next_entry=dict(case_name="CPP-134-1", geometry_id=34, side_join_id=20,
            geometry=next_geometry, side_ids=[8, 1], z_role=entry["z_role"],
            w_role=entry["w_role"], scope="two-point own z support; not analyzed here"))


def local_degree_lists():
    rows = []
    for contact, boundary in product((False, True), repeat=2):
        degree = 4 - int(contact) - int(boundary)
        assert degree >= 2
        assert (degree == 2) == (contact and boundary)
        pins = []
        for h in range(4):
            external = ([h] if contact else []) + ([1] if boundary else [])
            ls = U - set(external)
            slack = len(ls) - degree
            assert slack == int(h == 1 and contact and boundary)
            pins.append(dict(z=h, external_colors=external, list=sorted(ls), slack=slack))
        rows.append(dict(original_z_contact=contact, original_b1_attachment=boundary,
            degree_in_D=degree, pinned_lists=pins))
    return rows


def check_coloring(vertices, edges, fixed, coloring):
    assert coloring is not None and set(coloring) == set(vertices)
    assert all(coloring[v] == c for v, c in fixed.items())
    assert all(coloring[u] != coloring[v] for u, v in edges)


def forced_triangle(identity):
    edges = frozenset(base.edge(a, b) for a, b in combinations(CONTACTS, 2)) | frozenset(
        base.edge(v, a) for v in CONTACTS for a in (1, 5))
    region = base.make_region("original_forced_D_z_triangle",
        list(combinations(CONTACTS, 2)), {v: (1, 5) for v in CONTACTS})
    assert region["edges"] == edges
    assert [sum(v in e for e in edges) for v in CONTACTS] == [4, 4, 4]
    relation, ports, full = base.joint_interface(region, Q)
    assert ports == CONTACTS and set(full) == set(permutations((0, 2, 3)))
    forbidden = set.intersection(*(set(t) for t in full))
    assert forbidden == {0, 2, 3}
    assert relation == frozenset((1, w) for w in range(4))
    vertices = tuple(range(7)) + CONTACTS
    intact = []
    for h in range(4):
        fixed = dict(enumerate(Q)) | {5: h, 6: 1}
        coloring = base.first_coloring(vertices, edges, fixed)
        assert (coloring is None) == (h in forbidden)
        if coloring is not None:
            check_coloring(vertices, edges, fixed, coloring)
        intact.append(dict(z=h, coloring=coloring))
    context_edges = frozenset(map(tuple, identity["original_context_edges"]))
    source_projection = context_edges | edges
    assert len(source_projection) == 25
    assert [sum(v in e for e in source_projection) for v in (5, 7, 8, 9, *CONTACTS)] == [5]*1 + [4]*6
    deletions = []
    for e in sorted(edges):
        after, _, _ = base.joint_interface(region, Q, frozenset({e}))
        assert after == base.PAIRS
        witnesses = []
        for h in range(4):
            fixed = dict(enumerate(Q)) | {5: h, 6: 1}
            coloring = base.first_coloring(vertices, edges - {e}, fixed)
            check_coloring(vertices, edges - {e}, fixed, coloring)
            if h in forbidden:
                assert coloring[e[0]] == coloring[e[1]]
            witnesses.append(dict(z=h, coloring=coloring))
        fixed = dict(enumerate(Q)) | {5: 0, 6: 1}
        projection_witness = base.first_coloring(tuple(range(13)), source_projection - {e}, fixed)
        check_coloring(tuple(range(13)), source_projection - {e}, fixed, projection_witness)
        assert projection_witness[e[0]] == projection_witness[e[1]]
        assert tuple(projection_witness[v] for v in (7, 8, 9)) == (3, 0, 3)
        deletions.append(dict(deleted_edge=e, local_witnesses=witnesses,
            original_context_witness=projection_witness,
            missing_w_completion="same original D_w full fiber avoiding w=1 exists by f_Dw={0,2}; not enumerated"))
    return dict(ordered_contacts=CONTACTS, actual_attachments={str(v): [1, 5] for v in CONTACTS},
        edges=sorted(edges), complete_contact_tuples=sorted(full), forbidden=sorted(forbidden),
        root_pair_relation=sorted(relation), intact_pins=intact,
        rejection_block_palettes=[dict(z=h, palette=sorted(U - {1, h})) for h in sorted(forbidden)],
        deletions=deletions, original_source_projection_edges=sorted(source_projection),
        scope="local degree and edge-critical witnesses; original D is triangle by paper proof; w remains symbolic")


def minor_adjacency(edges, groups):
    assert all(groups) and sum(map(len, groups)) == len(set().union(*groups))
    for group in groups:
        assert base.is_connected(tuple(sorted(group)), edges)
    witnesses = []
    for i, j in combinations(range(5), 2):
        edge = next((base.edge(a, b) for a in sorted(groups[i]) for b in sorted(groups[j])
                     if base.edge(a, b) in edges), None)
        assert edge is not None
        witnesses.append(dict(pair=[i, j], actual_edge=edge))
    return witnesses


def k4_tether_controls(identity):
    """Finite route controls for the connected-exterior lemma, not sources."""
    context = frozenset(map(tuple, identity["original_context_edges"]))
    vertices = (20, 21, 22, 23)
    records = []
    for ends, subdivided in product(product((1, 5), repeat=4), (False, True)):
        edges = set(context) | {base.edge(a, b) for a, b in combinations(vertices, 2)}
        hub, paths = set(range(5)) | {5, 9}, []
        for i, (v, end) in enumerate(zip(vertices, ends)):
            path = [v] + ([40+i] if subdivided else []) + [end]
            edges.update(base.edge(a, b) for a, b in zip(path, path[1:]))
            hub.update(path[1:-1])
            paths.append(path)
        groups = [{v} for v in vertices] + [hub]
        adjacency = minor_adjacency(edges, groups)
        records.append(dict(tethers=paths, edges=sorted(edges),
            branch_sets=[sorted(g) for g in groups], adjacency=adjacency))
    assert len(records) == 32
    return dict(scope="K4 connected-exterior route controls; arbitrary original tether existence is paper proof; not degree/minimality realizations",
                records=records)


def k5_subdivisions(triangle):
    edges = frozenset(map(tuple, triangle["original_source_projection_edges"]))
    branches = (1, 5, *CONTACTS)
    records = []
    for outside in ((5, 9, 4, 3, 2, 1), (5, 9, 4, 0, 1)):
        routes, interiors, used_edges = [], set(), set()
        for a, b in combinations(branches, 2):
            route = tuple(reversed(outside)) if (a, b) == (1, 5) else (a, b)
            assert route[0] == a and route[-1] == b and len(set(route)) == len(route)
            inner = set(route[1:-1])
            assert not inner & set(branches) and not inner & interiors
            interiors.update(inner)
            route_edges = {base.edge(u, v) for u, v in zip(route, route[1:])}
            assert route_edges <= edges
            used_edges.update(route_edges)
            routes.append(dict(branch_pair=[a, b], original_path=route))
        for v in set(branches) | interiors:
            assert sum(v in e for e in used_edges) == (4 if v in branches else 2)
        assert len(routes) == 10
        groups = [{v} for v in CONTACTS] + [{5, *outside[1:-1]}, {1}]
        records.append(dict(branch_vertices=branches, routes=routes,
            subdivision_edges=sorted(used_edges), branch_sets=[sorted(g) for g in groups],
            minor_adjacency=minor_adjacency(edges, groups), external_path=outside))
    return records


def build():
    identity = fixed_identity()
    triangle = forced_triangle(identity)
    sources = (Path(__file__).resolve(), Path(common.__file__).resolve(),
               Path(capacity.__file__).resolve(), Path(base.__file__).resolve(), PARENT, common.ROTATIONS)
    return dict(schema=1,
        scope="only CPP-134-1 / geometry 30 / side_join 20 source exclusion; arbitrary-size paper plus external Gallai theorem; no target or Lean theorem",
        identity=identity, local_degree_lists=local_degree_lists(), forced_triangle=triangle,
        k4_tether_controls=k4_tether_controls(identity), k5_subdivisions=k5_subdivisions(triangle),
        summary=dict(named_source_branches_closed=1, local_vertex_types=4, pinned_list_checks=16,
            complete_unary_tuples=6, original_P3_tuples=2, local_deleted_edges=9,
            local_deletion_colorings=36, original_context_partial_colorings=9,
            k4_tether_controls=32, k5_subdivisions=2, target_queries=0,
            predecessor_cases=36, predecessor_geometries=140, predecessor_joins=900,
            predecessor_deletions=0),
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
