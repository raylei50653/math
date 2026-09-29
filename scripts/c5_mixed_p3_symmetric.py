#!/usr/bin/env python3
"""Sole mixed P3, opposite end contacts, and equal two-color root residuals.

Paper Jordan/order and palette arguments exclude disk sources of arbitrary
unary size. Finite controls preserve actual attachments and complete tuples;
the annulus fixture checks topology only, not degree/minimality realization.
"""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import c5_mixed_capacity_contacts as capacity

base = capacity.base
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_mixed_p3_symmetric/observations.json"
U = frozenset(range(4))
Q = base.Q
NAMES = ("z_side", "x0", "x1", "x2", "w_side")
PERMS = tuple(permutations(range(4)))
RHO = (3, 2, 1, 0, 4)
PI = (1, 0, 2, 3)


def seen(support):
    return frozenset(Q[i] for i in support)


def stabilizer_witness(support, residual):
    return next((p for p in PERMS if all(p[c] == c for c in seen(support))
                 and {p[c] for c in residual} != set(residual)), None)


def local_audit():
    records, symmetric, roles = [], [], {}
    for supports in product(combinations(range(5), 2), repeat=3):
        lists = [U - seen(s) for s in supports]
        tuples = tuple(t for t in product(*map(sorted, lists))
                       if t[0] != t[1] and t[1] != t[2])
        contacts = frozenset((t[0], t[2]) for t in tuples)
        F = capacity.forbidden(tuples, (0,), (2,))
        region = base.make_region("P3", [(7, 8), (8, 9)], {
            7: (base.Z,) + supports[0], 8: supports[1],
            9: (base.W,) + supports[2]})
        R, ports, complete = base.joint_interface(region, Q)
        assert ports == (7, 9) and set(complete) == contacts
        assert base.PAIRS - R == F
        for a, b in sorted(base.PAIRS):
            coloring = base.first_coloring(tuple(range(10)), region["edges"],
                dict(enumerate(Q)) | {base.Z: a, base.W: b})
            assert (coloring is None) == ((a, b) in F)
        equal_pair = len(contacts) == 2 and all(a == b for a, b in contacts)
        record = dict(id=len(records), actual_supports=supports,
            vertex_tuple_mask=sum(1 << (16*a + 4*b + c) for a, b, c in tuples),
            contact_tuple_mask=base.mask(contacts), forbidden_pair_mask=base.mask(F),
            symmetric=equal_pair)
        records.append(record)
        if not equal_pair:
            continue
        T = frozenset(a for a, _ in contacts)
        assert lists == [T, T, T] and 3 in T
        assert F == frozenset(product(T, T)) - base.DELTA
        key = "".join(map(str, sorted(T)))
        if key not in roles:
            roles[key] = [j for j in capacity.minimal_side_joins(F, 1, 1)
                          if j["z"]["residual"] == j["w"]["residual"] == sorted(T)]
            assert len(roles[key]) == 25
        symmetric.append(dict(local_id=record["id"], actual_supports=supports,
            residual=sorted(T), complete_vertex_tuples=tuples,
            complete_contact_tuples=sorted(contacts), role_key=key,
            role_ids=list(range(len(roles[key])))))
    assert len(records) == 1000 and len(symmetric) == 80
    assert Counter(r["role_key"] for r in symmetric) == {"03": 8, "13": 8, "23": 64}
    return dict(configurations=records, symmetric=symmetric, full_side_roles=roles,
                independent_pin_queries=16000)


def independent_packings():
    """All named positive supports with disjoint proper cyclic hull edges."""
    choices = []
    for size in range(2, 6):
        for support in combinations(range(5), size):
            for start in support:
                length = max((i - start) % 5 for i in support)
                edge_mask = sum(1 << ((start + j) % 5) for j in range(length))
                choices.append((support, start, length, edge_mask))
    found = []

    def visit(items, used):
        if len(items) == 5:
            assert used == 31 and all(item[2] == 1 for item in items)
            found.append(items)
            return
        for choice in choices:
            if not used & choice[3]:
                visit(items + (choice,), used | choice[3])

    visit((), 0)
    assert len(found) == 120
    ordered = set()
    for items in found:
        cycle = tuple(sorted(range(5), key=lambda i: items[i][1]))
        pos = cycle.index(0)
        cycle = cycle[pos:] + cycle[:pos]
        if cycle in ((0, 1, 2, 3, 4), (0, 4, 3, 2, 1)):
            ordered.add(tuple(item[0] for item in items))
    return ordered


def geometry_audit():
    geometries = []
    for anchor in range(5):
        for direction in (1, -1):
            lifts = tuple((anchor + direction*i, anchor + direction*(i+1))
                          for i in range(5))
            supports = tuple(tuple(sorted(v % 5 for v in pair)) for pair in lifts)
            colors = tuple(seen(s) for s in supports)
            mixed_equal = colors[1] == colors[2] == colors[3]
            record = dict(id=len(geometries), anchor=anchor, direction=direction,
                lifts=dict(zip(NAMES, lifts)), supports=dict(zip(NAMES, supports)),
                mixed_equal_lists=mixed_equal)
            if mixed_equal:
                T = U - colors[1]
                witnesses = {r: stabilizer_witness(supports[i], T)
                             for i, r in ((0, "z_side"), (4, "w_side"))}
                assert T == {2, 3} and all(p is not None for p in witnesses.values())
                record.update(residual=sorted(T), side_stabilizer_witnesses=witnesses)
            geometries.append(record)
    assert independent_packings() == {
        tuple(g["supports"][n] for n in NAMES) for g in geometries}
    assert sum(g["mixed_equal_lists"] for g in geometries) == 2

    # At a unit edge, a pair containing unused color 3 is invariant only if
    # it is exactly the complementary pair. This includes both root-side units.
    stabilizers = []
    for i in range(5):
        support = tuple(sorted((i, (i+1) % 5)))
        for d in range(3):
            T = frozenset({d, 3})
            witness = stabilizer_witness(support, T)
            assert (witness is None) == (T == U - seen(support))
            stabilizers.append(dict(support=support, residual=sorted(T), witness=witness))
    # No pair is invariant under the stabilizer of zero or one seen color.
    for support in ((),) + tuple((i,) for i in range(5)):
        for T in combinations(range(4), 2):
            assert stabilizer_witness(support, T) is not None
    return dict(named_units=NAMES, unordered_hull_packings=120,
                ordered_geometries=geometries, edge_stabilizers=stabilizers)


def annulus_control():
    """Spherical rotation with B as outer face and shared support endpoints."""
    inner = tuple(range(5, 10))
    faces = [tuple(range(5)), tuple(reversed(inner))]
    for i in range(5):
        faces.extend((((i+1) % 5, i, inner[i]), (i, inner[(i-1) % 5], inner[i])))
    darts, rotation = Counter(), {v: {} for v in range(10)}
    for face in faces:
        for j, v in enumerate(face):
            before, after = face[j-1], face[(j+1) % len(face)]
            darts[v, after] += 1
            assert before not in rotation[v]
            rotation[v][before] = after
    assert all(n == 1 and darts[v, u] == 1 for (u, v), n in darts.items())
    edges = frozenset(base.edge(u, v) for u, v in darts)
    for links in rotation.values():
        start = min(links)
        reached, v = set(), start
        while v not in reached:
            reached.add(v)
            v = links[v]
        assert v == start and reached == set(links)
    assert base.is_connected(tuple(range(10)), edges)
    assert 10 - len(edges) + len(faces) == 2
    return dict(scope="topology only; not a degree-(5,5,4,...) minimal q-core",
                vertices=list(range(10)), edges=sorted(edges), oriented_faces=faces,
                euler_characteristic=2)


def exclusion_audit(local, geometry):
    records = []
    for case in local["symmetric"]:
        support = case["actual_supports"]
        matching = [g for g in geometry["ordered_geometries"]
                    if tuple(g["supports"][x] for x in ("x0", "x1", "x2")) == support]
        assert all(g["side_stabilizer_witnesses"] for g in matching)
        records.append(dict(local_id=case["local_id"], matching_geometry_ids=[g["id"] for g in matching],
            role_key=case["role_key"], role_ids=case["role_ids"],
            reason="side_residual_stabilizer" if matching else "original_pentagon_order"))
    counts = Counter(r["reason"] for r in records)
    assert counts == {"original_pentagon_order": 78, "side_residual_stabilizer": 2}
    by_support = {c["actual_supports"]: c for c in local["symmetric"]}
    by_id = {r["local_id"]: r for r in records}
    for case in local["symmetric"]:
        reflected = tuple(tuple(sorted(RHO[i] for i in s)) for s in case["actual_supports"])
        other = by_support[reflected]
        assert other["residual"] == sorted(PI[c] for c in case["residual"])
        assert other["complete_vertex_tuples"] == tuple(sorted(
            tuple(PI[c] for c in t) for t in case["complete_vertex_tuples"]))
        assert by_id[case["local_id"]]["reason"] == by_id[other["local_id"]]["reason"]
        swapped = by_support[tuple(reversed(case["actual_supports"]))]
        assert by_id[case["local_id"]]["reason"] == by_id[swapped["local_id"]]["reason"]
        by_id[case["local_id"]].update(reflected_local_id=other["local_id"],
                                      root_swapped_local_id=swapped["local_id"])
    return dict(records=records, support_counts=dict(counts),
                support_role_counts={k: 25*v for k, v in counts.items()},
                retained_support_role_candidates=0, target_queries=0)


def build():
    local = local_audit()
    geometry = geometry_audit()
    return dict(schema=1,
        scope="paper disk-source exclusion for sole mixed P3 with opposite-end contacts "
              "and equal pair residuals; arbitrary unary size; no T4, Gallai, Lean, "
              "target query, full Sigma, or general exit claim",
        local=local, geometry=geometry, annulus_control=annulus_control(),
        exclusions=exclusion_audit(local, geometry),
        scripts_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
            for p in (Path(__file__).resolve(), Path(capacity.__file__).resolve(),
                      Path(base.__file__).resolve())})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build()
    raw = (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    if args.check:
        assert OUT.read_bytes() == raw, f"stale artifact: {OUT}"
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(raw)
    print(json.dumps(dict(actual_P3_support_triples=len(data["local"]["configurations"]),
        symmetric_support_triples=len(data["local"]["symmetric"]),
        independent_pin_queries=data["local"]["independent_pin_queries"],
        ordered_geometries=len(data["geometry"]["ordered_geometries"]),
        support_role_exclusions=data["exclusions"]["support_role_counts"],
        retained=0, target_queries=0, artifact_bytes=len(raw)), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
