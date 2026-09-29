#!/usr/bin/env python3
"""Sole mixed uv with Pz=Pw={u}: full tuples, minimality, source exclusion.

Paper Gallai/Jordan arguments cover arbitrary sources. Finite relations,
actual graph controls and necessary placements are recorded separately.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import c5_adjacent_degree5_interfaces as base
import c5_adjacent_degree5_shared_singleton as unary
from c5_adjacent_degree5_mixed_edge_shared import schemas_for
from c5_single_spoke_three_one import edge, validate_minor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_adjacent_degree5_mixed_edge_same_endpoint/observations.json"
TABLE = OUT.with_name("exclusion_table.md")
U, Q = frozenset(base.U), base.Q


def region_for(i, sv):
    return base.make_region("same_endpoint_uv", [(7, 8)],
                            {7: (base.Z, base.W, i), 8: tuple(sv)})


def full_tuples(row, i, sv):
    return frozenset((x, y) for x in U - {row[i]}
                     for y in U - {row[j] for j in sv} if x != y)


def effective(x, y):
    return frozenset(c for c in x if y - {c})


def local_audit():
    records, attachments, counts = [], [], Counter()
    for i, sv in product(range(5), combinations(range(5), 3)):
        region = region_for(i, sv)
        assert region["ports_z"] == region["ports_w"] == (7,)
        assert all(sum(v in e for e in region["edges"]) == 4 for v in (7, 8))
        canonical, transcript = [], []
        for row in base.ROWS:
            tuples = full_tuples(row, i, sv)
            relation, ports, witnesses = base.joint_interface(region, row)
            x, y = U - {row[i]}, U - {row[j] for j in sv}
            projected = effective(x, y)
            assert {a for a, _ in tuples} == projected
            assert len(projected) >= 2 and ports == (7,)
            assert set(witnesses) == {(a,) for a in projected}
            banned = frozenset(product(projected, projected)) - base.DELTA if len(projected) == 2 else frozenset()
            assert relation == base.PAIRS - banned
            transcript.append([row, sorted(tuples), base.mask(relation)])
            counts["attachment_row_checks"] += 1
            if row not in base.CANONICAL:
                continue
            canonical.append(dict(row=row, full_uv_tuples=sorted(tuples),
                                  contact_tuples=sorted(witnesses), forbidden=sorted(banned)))
            for a, b in sorted(base.PAIRS):
                fixed = dict(enumerate(row)) | {base.Z: a, base.W: b}
                f = base.first_coloring(tuple(range(9)), region["edges"], fixed)
                assert (f is not None) == ((a, b) in relation)
                counts["pinned_queries"] += 1
                for cut in sorted(region["edges"]):
                    f = base.first_coloring(tuple(range(9)), region["edges"] - {cut}, fixed)
                    assert f is not None
                    if (a, b) in banned:
                        assert f[cut[0]] == f[cut[1]]
                        counts["deleted_endpoint_forcing_checks"] += 1
                    counts["deletion_queries"] += 1
            for sigma in permutations(base.U):
                moved = tuple(sigma[c] for c in row)
                assert full_tuples(moved, i, sv) == frozenset((sigma[a], sigma[b]) for a, b in tuples)
                counts["full_tuple_frame_checks"] += 1
        records.append(dict(support_u=[i], support_v=sv, edges=sorted(region["edges"]),
                            canonical_rows=canonical,
                            all_rows_sha256=sha256(json.dumps(transcript).encode()).hexdigest()))
        if len({Q[j] for j in sv}) == 3:
            attachments.append(dict(id=len(attachments), support_u=[i], support_v=sv,
                                    h=Q[i], pair=sorted({0, 1, 2} - {Q[i]}),
                                    full_uv_tuples=sorted(full_tuples(Q, i, sv))))
    assert len(attachments) == 20
    lookup = {(r["support_u"][0], tuple(r["support_v"])): r for r in attachments}
    for r in attachments:
        rho = lambda j: (3 - j) % 5
        reflected = (rho(r["support_u"][0]), tuple(sorted(rho(j) for j in r["support_v"])))
        r["reflected_id"] = lookup[reflected]["id"]
    return records, attachments, dict(counts)


def explicit_side_forms(h):
    pair = U - {h, 3}
    forms = []
    for e in (pair, *(frozenset({c}) for c in sorted(pair))):
        lost = pair - e
        forms.append((U - {h}, (2,), (frozenset({3}) | lost,)))
        forms.append((U, (3,), (frozenset({h, 3}) | lost,)))
        for single in (h, 3):
            forms.append((U, (2, 1), (frozenset({h, 3} - {single}) | lost, frozenset({single}))))
    assert len(forms) == 12
    return forms


def abstract_audit():
    options, records, counts = unary.sides(), [], Counter()
    for h in range(3):
        pair = U - {h, 3}
        forms = explicit_side_forms(h)
        for left, right in product(options, repeat=2):
            direct = unary.direct_minimality(left, right, pair)
            predicted = (left in forms and right in forms
                         and (unary.residual(left) == pair or unary.residual(right) == pair))
            assert direct == predicted, (h, left, right)
            counts["minimality_comparisons"] += 1
            if not direct:
                continue
            ez, ew = unary.residual(left), unary.residual(right)
            assert unary.allowed(ez, ew, pair, edge_present=False) == {(c, c) for c in ez & ew}
            assert unary.allowed(ez, ew, pair, shared_present=False) == set(product(ez, ew)) - base.DELTA
            for side, other, is_z in ((left, ew, True), (right, ez, False)):
                for j, ban in enumerate(side[2]):
                    private = ban - unary.union([f for k, f in enumerate(side[2]) if j != k]) - pair
                    predicted_pairs = set(product(private, other) if is_z else product(other, private))
                    actual_pairs = unary.allowed(unary.residual(side, j), other, pair) if is_z else unary.allowed(other, unary.residual(side, j), pair)
                    assert actual_pairs == predicted_pairs
            planar = left[1] != (3,) and right[1] != (3,)
            records.append(dict(id=len(records), h=h, pair=sorted(pair),
                                z=unary.encode_side(left), w=unary.encode_side(right),
                                passes_three_contact_exclusion=planar))
    assert len(records) == 240
    retained = [r for r in records if r["passes_three_contact_exclusion"]]
    assert len(retained) == 135
    schema_sets = {",".join(map(str, f)): schemas_for(set(f))
                   for n in (1, 2) for f in combinations(range(4), n)}
    for r in retained:
        r["q_schema_count"] = 1
        for side in (r["z"], r["w"]):
            side["ordered_relation_schema_keys"] = []
            for k, f in zip(side["ports"], side["forbidden"]):
                key = ",".join(map(str, f))
                side["ordered_relation_schema_keys"].append(key if k == 2 else None)
                r["q_schema_count"] *= len(schema_sets[key]) if k == 2 else 1
        r["span_lower_bound"] = 2 + sum(2 if f == [3] else 1
                                              for side in (r["z"], r["w"]) for f in side["forbidden"])
        r["exclusion"] = "span_exceeds_five" if r["span_lower_bound"] > 5 else "saturated_v_star"
        if r["span_lower_bound"] == 5:
            assert r["z"]["ports"] == r["w"]["ports"] == (2,)
            assert r["z"]["spokes_colors"] == r["w"]["spokes_colors"] == [r["h"]]
            assert sum(side["forbidden"] == [[3]] for side in (r["z"], r["w"])) == 1
    counts.update(side_candidates=len(options), abstract_records=len(records),
                  three_contact_excluded=105, planar_necessary_records=135,
                  span_excluded=sum(r["span_lower_bound"] > 5 for r in retained),
                  saturated_records=sum(r["span_lower_bound"] == 5 for r in retained),
                  expanded_q_relation_schemas=sum(r["q_schema_count"] for r in retained))
    assert counts["span_excluded"] == 123 and counts["saturated_records"] == 12
    return records, schema_sets, dict(counts)


def stable(support, ban):
    colors = {Q[i] for i in support}
    return all({sigma[c] for c in ban} == set(ban) for sigma in permutations(base.U)
               if all(sigma[c] == c for c in colors))


def arc(start, length):
    return tuple((start + j) % 5 for j in range(length + 1))


def geometry_audit(records):
    # Roles L/S retain the actual root name in each source record.
    geometry = []
    for a, reverse in product(range(5), (False, True)):
        large = arc(a, 2)
        small = arc((a + (4 if reverse else 2)) % 5, 1)
        mixed = arc((a + (2 if reverse else 3)) % 5, 2)
        geometry.append(dict(id=len(geometry), large=large, small=small, mixed=mixed,
                             order=("L", "M", "S") if reverse else ("L", "S", "M")))
    # Independent edge-mask packing with all starts free, no stipulated order.
    independently = set()
    for a, b, c in product(range(5), repeat=3):
        hulls = (arc(a, 2), arc(b, 1), arc(c, 2))
        masks = [sum(1 << x for x in h[:-1]) for h in hulls]
        if all(not (masks[i] & masks[j]) for i, j in combinations(range(3), 2)):
            independently.add(hulls)
    assert independently == {(g["large"], g["small"], g["mixed"]) for g in geometry}
    assert len(geometry) == 10
    joins, relaxed = [], []
    for r in records:
        if r.get("exclusion") != "saturated_v_star":
            continue
        large_root = "z" if r["z"]["forbidden"] == [[3]] else "w"
        small_root = "w" if large_root == "z" else "z"
        for g in geometry:
            candidates = []
            for i, sl, ss in product(g["mixed"], g["large"][::2], g["small"]):
                reasons = []
                if len({Q[j] for j in g["mixed"]}) != 3:
                    reasons.append("v_boundary_colors_repeat")
                if not stable(g["large"], {3}):
                    reasons.append("large_full_relation_support")
                if not stable(g["small"], r[small_root]["forbidden"][0]):
                    reasons.append("small_full_relation_support")
                if (Q[i], Q[sl], Q[ss]) != (r["h"],) * 3:
                    reasons.append("u_and_root_spoke_colors")
                before_sector = not reasons
                # H-v is connected and meets the complement arc: u's attachment
                # can meet S_v only at the two endpoints of that sector.
                sector = arc(g["mixed"][-1], 3)
                assert set(g["large"]) | set(g["small"]) == set(sector)
                if i not in sector:
                    reasons.append("u_outside_H_minus_v_sector")
                assert reasons
                candidate = dict(support_u=[i], support_v=g["mixed"],
                                 root_spokes={large_root: sl, small_root: ss},
                                 active_v_sector=sector, contradictions=reasons)
                candidates.append(candidate)
                if before_sector:
                    schema_ids = {}
                    for root, support in ((large_root, g["large"]), (small_root, g["small"])):
                        schemas = schemas_for(set(r[root]["forbidden"][0]))
                        fixed_colors = {Q[j] for j in support}
                        ids = [k for k, relation in enumerate(schemas) if all(
                            {(sigma[a], sigma[b]) for a, b in relation} == set(relation)
                            for sigma in permutations(base.U) if all(sigma[c] == c for c in fixed_colors))]
                        assert len(ids) == (95 if root == large_root else 1)
                        schema_ids[root] = ids
                    relaxed.append(dict(source_id=r["id"], geometry_id=g["id"],
                                        large_root=large_root, small_root=small_root,
                                        full_uv_tuples=sorted(full_tuples(Q, i, g["mixed"])),
                                        compatible_complete_schema_ids=schema_ids, **candidate))
            joins.append(dict(source_id=r["id"], geometry_id=g["id"], large_root=large_root,
                              small_root=small_root, actual_attachment_candidates=candidates,
                              # All four orientations of the two named pair contacts.
                              pair_contact_orders=list(product(((0, 1), (1, 0)), repeat=2))))
    assert len(joins) == 120 and len(relaxed) == 4
    # Reflection and root swap retain full source identities.
    key = lambda r: (r["h"], json.dumps(r["z"], sort_keys=True), json.dumps(r["w"], sort_keys=True))
    lookup = {key(r): r["id"] for r in records}
    for r in records:
        r["root_swapped_id"] = lookup[(r["h"], key(r)[2], key(r)[1])]
    return dict(geometries=geometry, joins=joins, controls_without_v_sector=relaxed), dict(
        saturated_geometries=len(geometry), source_geometry_joins=len(joins),
        attachment_candidates=sum(len(j["actual_attachment_candidates"]) for j in joins),
        false_survivors_without_v_sector=len(relaxed), source_retained=0, target_queries=0)


def cross_row_audit():
    cases = 0
    nonempty = [s for s in unary.subsets(U) if s]
    for h in U:
        for y in nonempty:
            if len(y) > 3:
                continue
            x, s = U - {h}, effective(U - {h}, y)
            tuples = {(c, d) for c in x for d in y if c != d}
            for ez, ew in product(nonempty, repeat=2):
                actual = any(a != b and any(c not in {a, b} for c, _ in tuples)
                             for a, b in product(ez, ew))
                reject = (len(ez) == 1 and ez == ew) or (len(s) == 2 and ez <= s and ew <= s)
                assert actual != reject
                cases += 1
    return dict(cases=cases, scope="row-specific same-source residuals; no target query")


def fixed_graph_audit():
    result = []
    # The triangle with a forced-3 leaf has pair-contact forbidden set {3}.
    # An edge whose ends see the other two q colors has forbidden set {3,c}.
    for lost_z, lost_w in ((None, None), (1, None), (2, None), (None, 1), (None, 2)):
        regions, next_vertex = [region_for(0, (0, 1, 4))], 9
        for root, lost in ((base.Z, lost_z), (base.W, lost_w)):
            a, b = next_vertex, next_vertex + 1
            if lost is None:
                t, leaf = next_vertex + 2, next_vertex + 3
                region = base.make_region(f"unary_{root}", [(a, b), (a, t), (b, t), (t, leaf)],
                    {a: (root, 0), b: (root, 0), t: (0,), leaf: (0, 1, 4)})
                next_vertex += 4
            else:
                other = 4 if lost == 1 else 1
                region = base.make_region(f"unary_{root}", [(a, b)],
                                          {a: (root, 0, other), b: (root, 0, other)})
                next_vertex += 2
            contact = base.joint_interface(region, Q)[2]
            assert set.intersection(*(set(t) for t in contact)) == ({3} if lost is None else {3, lost})
            regions.append(region)
        edges = (base.CYCLE | {base.edge(base.Z, base.W), base.edge(base.Z, 0), base.edge(base.W, 0)}
                 | unary.union([r["edges"] for r in regions]))
        vertices = tuple(range(next_vertex))
        assert [sum(v in e for e in edges) for v in vertices[5:]] == [5, 5] + [4] * (next_vertex - 7)
        assert not base.whole_pairs(vertices, edges, Q)
        deletions = []
        for cut in sorted(edges - base.CYCLE):
            f = base.first_coloring(vertices, edges - {cut}, dict(enumerate(Q)))
            assert f is not None and f[cut[0]] == f[cut[1]]
            deletions.append(dict(edge=cut, coloring=[f[v] for v in vertices]))
        canonical, transcript = [], []
        for row in base.ROWS:
            relations = [base.joint_interface(r, row)[0] for r in regions]
            actual = base.whole_pairs(vertices, edges, row)
            assert actual == base.glued_pairs(regions, relations, edges, row, frozenset())
            transcript.append([row, base.mask(actual)])
            if row in base.CANONICAL:
                canonical.append(dict(row=row, root_pairs=sorted(actual),
                    full_uv_tuples=sorted(full_tuples(row, 0, (0, 1, 4))),
                    unary_full_tuples=[sorted(base.joint_interface(r, row)[2]) for r in regions[1:]]))
        result.append(dict(scope="actual minimal q-core with required degrees; no disk or T4 claim",
                           lost_colors=[lost_z, lost_w], vertices=vertices, edges=sorted(edges),
                           regions=[dict(name=r["name"], vertices=r["vertices"], edges=sorted(r["edges"]),
                                         ports_z=r["ports_z"], ports_w=r["ports_w"]) for r in regions],
                           canonical_rows=canonical, deletion_witnesses=deletions,
                           all_rows_sha256=sha256(json.dumps(transcript).encode()).hexdigest()))
    return result


def minor_audit():
    records = []
    for root, i, lengths, long in product(("z", "w"), range(5),
            ((0, 0, 0), (0, 2, 0), (2, 2, 2), (1, 1, 1)), (False, True)):
        es = {edge(f"b{j}", f"b{(j + 1) % 5}") for j in range(5)}
        es |= {edge("z", "w"), edge("z", "u"), edge("w", "u"), edge("u", "v"), edge("u", f"b{i}")}
        es |= {edge("v", f"b{j}") for j in (0, 1, 4)}
        core = [f"a{k}" for k in range(3)]
        es |= {edge(a, b) for a, b in combinations(core, 2)}
        groups = [{root}] + [{v} for v in core] + [{"u"} | {f"b{j}" for j in range(5)}]
        for k, (v, length) in enumerate(zip(core, lengths)):
            arm = [v] + [f"arm{k}_{j}" for j in range(length)]
            es.update(edge(a, b) for a, b in zip(arm, arm[1:]))
            es.add(edge(root, arm[-1]))
            groups[k + 1].update(arm)
            tether = [v] + ([f"t{k}_0", f"t{k}_1"] if long else []) + [f"b{(i + k) % 5}"]
            es.update(edge(a, b) for a, b in zip(tether, tether[1:]))
            groups[4].update(tether[1:])
        witness = dict(edges=sorted(es), branch_sets=[sorted(g) for g in groups])
        assert validate_minor(witness)
        assert not validate_minor(dict(witness, edges=sorted(es - {edge(root, "u")})))
        records.append(dict(root=root, support_u=[i], arm_lengths=lengths,
                            long_tethers=long, **witness))
    assert len(records) == 80
    return records


def negative_controls():
    tuples = full_tuples(Q, 0, (0, 1, 4))
    assert tuples == {(1, 3), (2, 3)}
    assert not any(c not in {1, 2} for c, _ in tuples)
    assert any(c != 1 for c, _ in tuples) and any(c != 2 for c, _ in tuples)
    bad = dict(enumerate(Q)) | {base.Z: 1, base.W: 2, 7: 2, 8: 3}
    region = region_for(0, (0, 1, 4))
    assert all(bad[a] != bad[b] for a, b in region["edges"] - {base.edge(base.Z, 7), base.edge(base.W, 7)})
    assert bad[base.W] == bad[7]
    return dict(splitting_u_falsely_accepts=[1, 2], full_uv_tuples=sorted(tuples),
                deleting_zu_must_keep_wu=dict(coloring=[bad[v] for v in range(9)], retained_edge=[base.W, 7]),
                same_singleton_residuals="mixed deletion fails", distinct_singleton_residuals="zw deletion fails")


def build():
    local, attachments, lc = local_audit()
    records, schemas, ac = abstract_audit()
    geometry, gc = geometry_audit(records)
    cross, graphs, minors = cross_row_audit(), fixed_graph_audit(), minor_audit()
    inputs = ["scripts/c5_adjacent_degree5_interfaces.py", "scripts/c5_adjacent_degree5_shared_singleton.py",
              "scripts/c5_adjacent_degree5_mixed_edge_shared.py", "scripts/c5_single_spoke_three_one.py",
              "docs/c5_no_spoke_exterior.md", "docs/c5_single_spoke_three_one.md",
              "docs/c5_adjacent_degree5_mixed_edge_order.md"]
    return dict(schema=1, source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                inputs_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
                scope="all same-endpoint K2 disk sources excluded by paper proof; finite controls are not realizations",
                summary=dict(**lc, **ac, **gc, local_q_supports=len(attachments),
                    cross_row_cases=cross["cases"], fixed_graphs=len(graphs), fixed_graph_rows=len(graphs) * len(base.ROWS),
                    fixed_graph_deletions=sum(len(g["deletion_witnesses"]) for g in graphs), K5_skeletons=len(minors)),
                abstract_relations=records, two_contact_schemas=schemas, local_controls=local,
                local_q_supports=attachments, geometry=geometry, cross_row_conditions=cross,
                fixed_graphs=graphs, minor_skeletons=minors, negative_controls=negative_controls())


def table(result):
    lines = ["# Same-endpoint mixed K2 source exclusions", "",
             "Pz=Pw={u}; v retains all three actual boundary attachments.", "",
             "240 necessary relation records: 105 three-contact K5, 123 span, 12 saturated v-star exclusions.",
             "These are not counts of realizable graphs. Target queries: 0.", "",
             "| ID | h | z spokes / ports / bans | w spokes / ports / bans | Span bound | Exclusion |",
             "| ---: | ---: | --- | --- | ---: | --- |"]
    for r in result["abstract_relations"]:
        sides = [f"{r[k]['spokes_colors']} / {r[k]['ports']} / {r[k]['forbidden']}" for k in ("z", "w")]
        lines.append(f"| {r['id']} | {r['h']} | {sides[0]} | {sides[1]} | {r.get('span_lower_bound', '')} | "
                     f"{r.get('exclusion', 'three_contact_K5')} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    payload, rendered = json.dumps(result, sort_keys=True, indent=2) + "\n", table(result)
    if args.check:
        assert OUT.read_bytes() == payload.encode(), "certificate differs"
        assert TABLE.read_bytes() == rendered.encode(), "table differs"
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
        TABLE.write_text(rendered)
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
