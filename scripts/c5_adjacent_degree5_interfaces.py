#!/usr/bin/env python3
"""Replay ordered two-root interfaces on fixed controls; no graph catalogue.

Paper proofs cover arbitrary finite degree-four components. These fixtures do not
certify disk realizability, T4, or separation of adjacent degree-five cores.
"""
import argparse
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_adjacent_degree5_interfaces/observations.json"
U = tuple(range(4))
PAIRS = frozenset(product(U, repeat=2))
DELTA = frozenset((a, a) for a in U)
Q = (0, 1, 0, 1, 2)
Z, W = 5, 6
CYCLE = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in range(5))
ROWS = tuple(row for row in product(U, repeat=5)
             if all(row[i] != row[j] for i, j in CYCLE))


def edge(u, v):
    return tuple(sorted((u, v)))


def normalized(row):
    labels = {}
    return tuple(labels.setdefault(c, len(labels)) for c in row)


CANONICAL = tuple(row for row in ROWS if normalized(row) == row)


def mask(relation):
    return sum(1 << (4 * a + b) for a, b in relation)


def first_coloring(vertices, edges, fixed):
    """Independent full-graph backtracking, retaining actual precolored vertices."""
    adjacent = {v: set() for v in vertices}
    for u, v in edges:
        adjacent[u].add(v)
        adjacent[v].add(u)
    colors = dict(fixed)
    if any(u in colors and v in colors and colors[u] == colors[v] for u, v in edges):
        return None

    def visit():
        if len(colors) == len(vertices):
            return dict(colors)
        available = {v: set(U) - {colors[x] for x in adjacent[v] if x in colors}
                     for v in vertices if v not in colors}
        v = min(available, key=lambda x: (len(available[x]), -len(adjacent[x]), x))
        for c in sorted(available[v]):
            colors[v] = c
            result = visit()
            if result is not None:
                return result
        colors.pop(v, None)
        return None

    return visit()


def make_region(name, internal, attachments):
    vertices = tuple(sorted(attachments))
    edges = frozenset(edge(*e) for e in internal) | frozenset(
        edge(v, u) for v, neighbors in attachments.items() for u in neighbors)
    # The w order is deliberately opposite to vertex order. Identity, not position,
    # is what binds a vertex appearing in both contact sequences.
    return dict(name=name, vertices=vertices, edges=edges,
                ports_z=tuple(v for v in vertices if edge(v, Z) in edges),
                ports_w=tuple(v for v in reversed(vertices) if edge(v, W) in edges))


def controls():
    return [
        make_region("shared_singleton", [], {7: (Z, W, 1, 4)}),
        make_region("one_root_singleton", [], {7: (Z, 0, 1, 4)}),
        make_region("shared_edge", [(7, 8)], {7: (Z, W, 4), 8: (Z, W, 4)}),
        make_region("mixed_path", [(7, 8), (8, 9)],
                    {7: (Z, W, 4), 8: (W, 0), 9: (Z, 1, 4)}),
        make_region("triangle", [(7, 8), (8, 9), (7, 9)],
                    {7: (Z, 4), 8: (W, 4), 9: (Z, W)}),
        make_region("even_cycle", [(7, 8), (8, 9), (9, 10), (7, 10)],
                    {7: (Z, W), 8: (Z, 4), 9: (W, 1), 10: (0, 2)}),
        make_region("odd_cycle", [(7, 8), (8, 9), (9, 10), (10, 11), (7, 11)],
                    {7: (Z, W), 8: (Z, 4), 9: (W, 1), 10: (Z, 4), 11: (W, 4)}),
        make_region("triangle_bridge", [(7, 8), (8, 9), (7, 9), (7, 10)],
                    {7: (Z,), 8: (W, 4), 9: (Z, W), 10: (Z, 1, 4)}),
        make_region("k4", list(combinations(range(7, 11), 2)),
                    {7: (Z,), 8: (W,), 9: (1,), 10: (4,)}),
    ]


def joint_interface(region, row, deleted=frozenset()):
    """Enumerate full local colorings, then project a single ordered contact tuple.

    Original contact variables stay in scope after edge deletion. Only constraints
    are removed, including just one incidence when a common-neighbor edge is cut.
    """
    vertices = region["vertices"]
    remaining = region["edges"] - deleted
    internal = [(u, v) for u, v in remaining if u in vertices and v in vertices]
    lists = {v: tuple(c for c in U if all(
        c != row[u] for u in range(5) if edge(v, u) in remaining)) for v in vertices}
    ports = tuple(sorted(set(region["ports_z"]) | set(region["ports_w"])))
    witnesses = {}
    for values in product(*(lists[v] for v in vertices)):
        coloring = dict(zip(vertices, values))
        if all(coloring[u] != coloring[v] for u, v in internal):
            contact = tuple(coloring[v] for v in ports)
            witnesses.setdefault(contact, values)
    relation = set()
    for a, b in PAIRS:
        for contact in witnesses:
            colors = dict(zip(ports, contact))
            if all(colors[v] != a for v in region["ports_z"] if edge(v, Z) in remaining) and all(
                    colors[v] != b for v in region["ports_w"] if edge(v, W) in remaining):
                relation.add((a, b))
                break
    return frozenset(relation), ports, witnesses


def is_connected(vertices, edges):
    seen = {vertices[0]}
    while True:
        new = seen | {v for u, v in edges if u in seen and v in vertices} | {
            u for u, v in edges if v in seen and u in vertices}
        if new == seen:
            return len(seen) == len(vertices)
        seen = new


def deletion_kind(region, e):
    u, v = e
    if u in region["vertices"] and v in region["vertices"]:
        return "nonbridge" if is_connected(region["vertices"], region["edges"] - {e}) else "bridge"
    return "root_contact" if Z in e or W in e else "boundary_spoke"


def local_audit():
    records, summary = [], dict(regions=0, rows=len(ROWS), ordered_pairs=16,
                               base_pin_queries=0, deletion_relations=0,
                               deletion_pin_queries=0, equivariance_checks=0,
                               deleted_endpoint_forcing_checks=0)
    for region in controls():
        vertices, edges = region["vertices"], region["edges"]
        assert is_connected(vertices, edges)
        assert all(sum(v in e for e in edges) == 4 for v in vertices)
        relations, canonical, deletions = {}, [], []
        external = tuple(range(7))
        for row in ROWS:
            relation, ports, witnesses = joint_interface(region, row)
            relations[row] = relation
            for a, b in sorted(PAIRS):
                fixed = dict(enumerate(row)) | {Z: a, W: b}
                coloring = first_coloring(external + vertices, edges, fixed)
                assert (coloring is not None) == ((a, b) in relation), (region["name"], row, a, b)
                summary["base_pin_queries"] += 1
                if (a, b) not in relation:
                    for v in vertices:
                        external_colors = [fixed[u] for u in external if edge(v, u) in edges]
                        assert len(external_colors) == len(set(external_colors))
            if set(region["ports_z"]) & set(region["ports_w"]):
                assert DELTA <= relation
            for v in vertices:
                colors = [row[u] for u in range(5) if edge(v, u) in edges]
                if len(colors) != len(set(colors)):
                    assert relation == PAIRS
            for e in sorted(edges):
                after, _, _ = joint_interface(region, row, frozenset({e}))
                assert after == PAIRS, (region["name"], row, e)
                # Verify erasure through a separate actual-edge solver as well.
                for a, b in sorted(PAIRS):
                    fixed = dict(enumerate(row)) | {Z: a, W: b}
                    coloring = first_coloring(external + vertices, edges - {e}, fixed)
                    assert coloring is not None
                    if (a, b) not in relation:
                        assert coloring[e[0]] == coloring[e[1]]
                        summary["deleted_endpoint_forcing_checks"] += 1
                    summary["deletion_pin_queries"] += 1
                deletions.append([list(row), list(e), mask(after)])
                summary["deletion_relations"] += 1
            if row in CANONICAL:
                canonical.append(dict(row=row, mask=mask(relation),
                    tuples=[dict(contact=t, coloring=f) for t, f in sorted(witnesses.items())]))
        for row in CANONICAL:
            for sigma in permutations(U):
                moved = tuple(sigma[c] for c in row)
                expected = frozenset((sigma[a], sigma[b]) for a, b in relations[row])
                assert relations[moved] == expected
                summary["equivariance_checks"] += 1
        records.append(dict(name=region["name"], vertices=vertices, edges=sorted(edges),
            ports=ports, ports_z=region["ports_z"], ports_w=region["ports_w"],
            shared=sorted(set(region["ports_z"]) & set(region["ports_w"])),
            deletion_kinds={str(e): deletion_kind(region, e) for e in sorted(edges)},
            canonical_rows=canonical,
            all_row_masks=[[list(row), mask(relations[row])] for row in ROWS],
            deletion_sha256=sha256(json.dumps(deletions).encode()).hexdigest()))
        summary["regions"] += 1
    return records, summary


def root_lists(edges, row, root):
    return set(U) - {row[i] for i in range(5) if edge(root, i) in edges}


def whole_pairs(vertices, edges, row):
    return frozenset((a, b) for a, b in PAIRS if first_coloring(
        vertices, edges, dict(enumerate(row)) | {Z: a, W: b}) is not None)


def glued_pairs(regions, relations, edges, row, deleted):
    remaining = edges - deleted
    pairs = set(product(root_lists(remaining, row, Z), root_lists(remaining, row, W)))
    if edge(Z, W) in remaining:
        pairs -= DELTA
    for region, relation in zip(regions, relations):
        if not region["edges"] & deleted:
            pairs &= relation
    return frozenset(pairs)


def whole_audit():
    # The first fixture has exact target degrees but fails minimality. A second
    # graph checks simultaneous gluing of distinct original components.
    shared = controls()[2]
    single = make_region("extra_one_root", [], {9: (Z, 0, 1, 4)})
    fixtures = [("degree_5_5_4_4_nonminimal", [shared]),
                ("two_components_algebra_only", [shared, single])]
    records, count = [], 0
    for name, regions in fixtures:
        edges = CYCLE | {edge(Z, W), edge(Z, 1), edge(Z, 4), edge(W, 1), edge(W, 4)}
        for region in regions:
            edges |= region["edges"]
        vertices = tuple(sorted(set(range(7)) | {v for r in regions for v in r["vertices"]}))
        nonboundary = sorted(edges - CYCLE)
        # All single-edge and double-edge deletions, plus complete region erasure.
        deletion_sets = [frozenset()] + [frozenset(es) for k in (1, 2)
                                       for es in combinations(nonboundary, k)]
        deletion_sets += [r["edges"] for r in regions] + [frozenset(nonboundary)]
        deletion_sets = sorted(set(deletion_sets), key=lambda es: (len(es), sorted(es)))
        transcript, q_witnesses = [], []
        for row in ROWS:
            relations = [joint_interface(r, row)[0] for r in regions]
            for deleted in deletion_sets:
                formula = glued_pairs(regions, relations, edges, row, deleted)
                direct = whole_pairs(vertices, edges - deleted, row)
                assert formula == direct, (name, row, deleted)
                transcript.append([list(row), sorted(deleted), mask(direct)])
                count += 1
                if row == Q and len(deleted) == 1:
                    q_witnesses.append(dict(deleted=sorted(deleted), pairs=sorted(direct)))
        original = whole_pairs(vertices, edges, Q)
        root_cut = whole_pairs(vertices, edges - {edge(Z, W)}, Q)
        assert not original and root_cut and root_cut <= DELTA
        if name == "degree_5_5_4_4_nonminimal":
            assert [sum(v in e for e in edges) for v in range(5, 9)] == [5, 5, 4, 4]
            assert root_cut == {(0, 0), (3, 3)}
            assert not whole_pairs(vertices, edges - {edge(Z, 1)}, Q)
            assert not whole_pairs(vertices, edges - {edge(W, 1)}, Q)
        records.append(dict(name=name, vertices=vertices, edges=sorted(edges),
            components=[r["name"] for r in regions], deletion_sets=len(deletion_sets),
            q_single_deletions=q_witnesses, root_edge_diagonal=sorted(root_cut),
            transcript_sha256=sha256(json.dumps(transcript).encode()).hexdigest(),
            scope="fixed graph algebra; no disk/T4 or minimal-core claim"))
    return records, count


def abstract_minimality_audit():
    """Exhaust a small abstract domain, independently testing the condition table.

    These masks are not graph realizations. They test the exact roles of coverage,
    diagonal acceptance, root-spoke strips, and private ordered pairs.
    """
    domain = tuple(product((0, 3), repeat=2))
    possible = [frozenset(p for i, p in enumerate(domain) if bits & (1 << i))
                for bits in range(1 << len(domain))]
    cases = accepted = 0
    witnesses = []
    for a_list in ({3}, {0, 3}):
        for b_list in ({3}, {0, 3}):
            for r1, r2 in product(possible, repeat=2):
                rectangle = set(product(a_list, b_list))
                off = rectangle - DELTA
                original = off & r1 & r2
                root_edge = rectangle & r1 & r2
                # Abstract spokes release color 0 only when absent from a root list.
                z_cut = set(product(a_list | {0}, b_list)) - DELTA
                w_cut = set(product(a_list, b_list | {0})) - DELTA
                deletion_results = [root_edge, off & r2, off & r1]
                if 0 not in a_list:
                    deletion_results.append(z_cut & r1 & r2)
                if 0 not in b_list:
                    deletion_results.append(w_cut & r1 & r2)
                direct = not original and all(deletion_results)
                cover = off <= (PAIRS - r1) | (PAIRS - r2)
                diagonal = bool(root_edge & DELTA)
                private = bool(off & r2 - r1) and bool(off & r1 - r2)
                strips = (0 in a_list or bool({(0, b) for b in b_list if b != 0} & r1 & r2)) and (
                    0 in b_list or bool({(a, 0) for a in a_list if a != 0} & r1 & r2))
                assert direct == (cover and diagonal and private and strips)
                cases += 1
                accepted += direct
                if direct:
                    witnesses.append(dict(a=sorted(a_list), b=sorted(b_list),
                                          r1=sorted(r1), r2=sorted(r2)))
    assert accepted > 0
    return dict(cases=cases, passing=accepted, witnesses=witnesses,
                scope="abstract relation algebra only; not realizability certificates")


def negative_controls():
    relation, ports, witnesses = joint_interface(controls()[0], Q)
    assert ports == (7,) and set(witnesses) == {(0,), (3,)}
    assert PAIRS - relation == {(0, 3), (3, 0)}
    left = {a for a, _ in relation}
    right = {b for _, b in relation}
    assert set(product(left, right)) == PAIRS
    # Both separately chosen local colorings exist, but no shared coloring does.
    assert any(t[0] != 0 for t in witnesses) and any(t[0] != 3 for t in witnesses)
    assert not any(t[0] != 0 and t[0] != 3 for t in witnesses)
    r1, r2 = {(0, 1)}, {(1, 0)}
    assert not r1 & r2
    sigma = (1, 0, 2, 3)
    moved_r2 = {(sigma[a], sigma[b]) for a, b in r2}
    assert r1 & moved_r2
    higher_degree = make_region("degree_five_erasure_failure", [], {7: (Z, W, 0, 1, 4)})
    before = joint_interface(higher_degree, Q)[0]
    after = joint_interface(higher_degree, Q, frozenset({edge(7, 0)}))[0]
    assert (0, 3) not in before and (0, 3) not in after
    return [dict(name="common_neighbor_cannot_split", contact=7,
                 tuples=sorted(witnesses), false_pairs=sorted(PAIRS - relation)),
            dict(name="marginal_product_loses_correlation", exact=sorted(relation),
                 marginal_product=sorted(PAIRS)),
            dict(name="independent_component_recoloring", r1=sorted(r1), r2=sorted(r2),
                 false_join=sorted(r1 & moved_r2), scope="abstract negative control"),
            dict(name="degree_four_hypothesis_required", edges=sorted(higher_degree["edges"]),
                 deleted=edge(7, 0), still_rejected_pair=(0, 3), full_degree=5)]


def build():
    assert len(ROWS) == 240 and len(CANONICAL) == 10
    local, summary = local_audit()
    whole, count = whole_audit()
    summary["whole_graph_queries"] = count
    abstract = abstract_minimality_audit()
    summary["abstract_condition_cases"] = abstract["cases"]
    return dict(schema=1, source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                scope="fixed controls, paper theorem support; no disk realizability or separation",
                summary=summary, local_controls=local, whole_graph_controls=whole,
                abstract_conditions=abstract, negative_controls=negative_controls())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.check:
        assert OUT.read_bytes() == payload.encode(), "certificate differs"
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
