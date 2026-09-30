#!/usr/bin/env python3
"""Exact named two-vertex joins of existing C5 classes, with graph replay.

Default: a small fixed control suite, not a successor-table enumeration.
--check recomputes the deterministic artifact without writing. Topology is
unknown; actual shared edges are recorded separately from colouring guards.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

from boundary_relations import Relation, normalize


ROOT = Path(__file__).resolve().parents[1]
CELL_SOURCE = "artifacts/c5_cells/cells.json"
OUTPUT_DIR = ROOT / "artifacts/c5_two_vertex_overlap"
FRAME = {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)}
COLOUR_PERMS = tuple(permutations(range(4)))
# Each ordered B pair is the image of the ordered A pair, including reversal.
CASES = (
    ("reference", 1023, (0, 2), 1023, (0, 1)),
    ("reference_reverse", 1023, (0, 2), 1023, (1, 0)),
    ("free_pairs", 1023, (0, 2), 1023, (0, 2)),
    ("shared_chord_frame_edge", 1016, (0, 2), 1023, (0, 1)),
    ("private_interiors", 127, (0, 2), 167, (1, 3)),
    ("private_interiors_reverse", 127, (0, 2), 167, (3, 1)),
)


def expand(rows):
    """Expand full colour orbits, including every relative colour alignment."""
    return {tuple(g[c] for c in row) for row in rows for g in COLOUR_PERMS}


def pair_type(pairs):
    equal = any(a == b for a, b in pairs)
    different = any(a != b for a, b in pairs)
    return ("free" if equal and different else "forced_equal" if equal
            else "forced_different" if different else "infeasible")


def validate_pair(pair):
    if len(pair) != 2 or len(set(pair)) != 2 or any(i not in range(5) for i in pair):
        raise ValueError("A pair must contain two distinct boundary indices in 0..4")


def joined_interface(pair_a, pair_b):
    validate_pair(pair_a)
    validate_pair(pair_b)
    map_a = tuple(f"a{i}" for i in range(5))
    shared_b = {b: map_a[a] for a, b in zip(pair_a, pair_b)}
    map_b = tuple(shared_b.get(i, f"b{i}") for i in range(5))
    ports = map_a + tuple(v for v in map_b if v not in map_a)
    assert len(ports) == len(set(ports)) == 8
    assert set(map_a) & set(map_b) == {map_a[i] for i in pair_a}
    return ports, map_a, map_b


def join_relations(rows_a, rows_b, pair_a, pair_b):
    ports, map_a, map_b = joined_interface(pair_a, pair_b)
    bucket_b = {}
    for row in expand(rows_b):
        key = tuple(row[i] for i in pair_b)
        bucket_b.setdefault(key, []).append(row)
    labelled = set()
    for row_a in expand(rows_a):
        key = tuple(row_a[i] for i in pair_a)
        for row_b in bucket_b.get(key, ()):
            assignment = dict(zip(map_a, row_a))
            for v, c in zip(map_b, row_b):
                assert v not in assignment or assignment[v] == c
                assignment[v] = c
            labelled.add(tuple(assignment[v] for v in ports))
    relation = Relation.of(ports, labelled)
    assert expand(relation.patterns) == labelled
    return relation, labelled, map_a, map_b


def source_graph(cell):
    """Catalogue edges deliberately omit the five frame edges."""
    n = 5 + cell["k_eff"]
    extra = {tuple(sorted(edge)) for edge in cell["edges"]}
    assert not extra & FRAME
    assert all(0 <= u < v < n for u, v in extra)
    return n, tuple(sorted(extra | FRAME))


def graph_extensions(n, edges, port_count):
    """Exhaust all labelled port assignments, then solve private vertices.

    This routine sees only the actual graph, never a class mask or join rows.
    One complete graph colouring is retained per global port orbit.
    """
    neighbours = [set() for _ in range(n)]
    for u, v in edges:
        assert 0 <= u < v < n
        neighbours[u].add(v)
        neighbours[v].add(u)
    port_edges = [(u, v) for u, v in edges if v < port_count]
    colours = [-1] * n

    def extend():
        uncoloured = [v for v in range(port_count, n) if colours[v] < 0]
        if not uncoloured:
            return tuple(colours)
        domains = {v: [c for c in range(4)
                       if all(colours[w] != c for w in neighbours[v])]
                   for v in uncoloured}
        v = min(uncoloured, key=lambda w: (len(domains[w]), -len(neighbours[w]), w))
        for c in domains[v]:
            colours[v] = c
            witness = extend()
            colours[v] = -1
            if witness is not None:
                return witness
        return None

    accepted = set()
    witnesses = {}
    for row in product(range(4), repeat=port_count):
        if any(row[u] == row[v] for u, v in port_edges):
            continue
        colours[:port_count] = row
        witness = extend()
        if witness is None:
            continue
        assert all(witness[u] != witness[v] for u, v in edges)
        assert witness[:port_count] == row
        accepted.add(row)
        canonical = normalize(row)
        if canonical not in witnesses:
            # Ports precede private vertices, so normalizing the full witness
            # restricts to exactly the canonical eight-port row.
            witnesses[canonical] = normalize(witness)
    assert set(witnesses) == {normalize(row) for row in accepted}
    assert all(full[:port_count] == row for row, full in witnesses.items())
    return accepted, witnesses


def relation_payload(relation):
    return {"ports": relation.ports, "patterns": sorted(relation.patterns),
            "global_s4_orbits": len(relation.patterns),
            "labelled_assignments": len(expand(relation.patterns))}


def build(specs):
    catalogue = json.loads((ROOT / CELL_SOURCE).read_text())
    patterns = tuple(tuple(p) for p in catalogue["pattern_order"])
    pattern_index = {p: i for i, p in enumerate(patterns)}

    def mask_of(rows):
        return sum(1 << pattern_index[row] for row in rows)

    @lru_cache(maxsize=None)
    def source(mask):
        if str(mask) not in catalogue["cells"]:
            raise ValueError(f"R{mask} is not in the existing catalogue")
        cell = catalogue["cells"][str(mask)]
        rows = frozenset(p for i, p in enumerate(patterns) if mask & (1 << i))
        n, edges = source_graph(cell)
        actual, _ = graph_extensions(n, edges, 5)
        assert actual == expand(rows), f"source graph mismatch: R{mask}"
        return rows, n, edges

    records = []
    for name, id_a, pair_a, id_b, pair_b in specs:
        rows_a, n_a, edges_a = source(id_a)
        rows_b, n_b, edges_b = source(id_b)
        joint, labelled, map_a, map_b = join_relations(rows_a, rows_b, pair_a, pair_b)
        ports = joint.ports
        projected_a = joint.project(map_a)
        projected_b = joint.project(map_b)
        labelled_a, labelled_b = expand(rows_a), expand(rows_b)
        pairs_a = {tuple(row[i] for i in pair_a) for row in labelled_a}
        pairs_b = {tuple(row[i] for i in pair_b) for row in labelled_b}
        guard_a = {row for row in labelled_a if tuple(row[i] for i in pair_a) in pairs_b}
        guard_b = {row for row in labelled_b if tuple(row[i] for i in pair_b) in pairs_a}
        assert expand(projected_a.patterns) == guard_a
        assert expand(projected_b.patterns) == guard_b

        # Independent complete 4^8 evaluation of the defining relation formula.
        positions_a = tuple(ports.index(v) for v in map_a)
        positions_b = tuple(ports.index(v) for v in map_b)
        exhaustive = {
            row for row in product(range(4), repeat=8)
            if normalize(tuple(row[i] for i in positions_a)) in rows_a
            and normalize(tuple(row[i] for i in positions_b)) in rows_b
        }
        assert exhaustive == labelled

        # Keep both C5 frames and the complete shared-pair projections, but
        # discard the higher-order class restrictions: this is only a relaxation.
        pair_only = {
            row for row in product(range(4), repeat=8)
            if all(row[pos[i]] != row[pos[(i + 1) % 5]]
                   for pos in (positions_a, positions_b) for i in range(5))
            and tuple(row[positions_a[i]] for i in pair_a) in pairs_a & pairs_b
        }
        assert labelled <= pair_only
        spurious = {normalize(row) for row in pair_only - labelled}

        vertices = ports + tuple(f"A_inner{i}" for i in range(5, n_a)) + tuple(
            f"B_inner{i}" for i in range(5, n_b))
        graph_map_a = map_a + tuple(f"A_inner{i}" for i in range(5, n_a))
        graph_map_b = map_b + tuple(f"B_inner{i}" for i in range(5, n_b))
        assert len(vertices) == len(set(vertices)) == n_a + n_b - 2
        assert set(graph_map_a) & set(graph_map_b) == {map_a[i] for i in pair_a}
        vertex_index = {v: i for i, v in enumerate(vertices)}

        def mapped_edges(edges, mapping):
            return {tuple(sorted((vertex_index[mapping[u]], vertex_index[mapping[v]])))
                    for u, v in edges}

        actual_a = mapped_edges(edges_a, graph_map_a)
        actual_b = mapped_edges(edges_b, graph_map_b)
        all_edges = tuple(sorted(actual_a | actual_b))
        actual, graph_witnesses = graph_extensions(len(vertices), all_edges, 8)
        assert actual == labelled, f"joined graph mismatch: {name}"
        assert len(actual) == 24 * len(joint.patterns)  # proper C5 uses >=3 colours
        assert all(all(full[u] != full[v] for u, v in all_edges)
                   for full in graph_witnesses.values())

        projections = {}
        for side, projected, expected, guard_pairs in (
                ("A", projected_a, guard_a, pairs_b),
                ("B", projected_b, guard_b, pairs_a)):
            result_mask = mask_of(projected.patterns)
            projections[side] = {
                **relation_payload(projected), "mask": result_mask,
                "catalogue_id": result_mask if str(result_mask) in catalogue["cells"] else None,
                "guard_from_other_side": pair_type(guard_pairs),
                "guard_labelled_assignments": len(expected), "guard_matches": True,
            }

        # Negative control: gluing separately normalized rows omits alignments.
        naive = set()
        for row_a in rows_a:
            for row_b in rows_b:
                if tuple(row_a[i] for i in pair_a) != tuple(row_b[i] for i in pair_b):
                    continue
                assignment = dict(zip(map_a, row_a))
                assignment.update(zip(map_b, row_b))
                naive.add(normalize(tuple(assignment[v] for v in ports)))
        assert naive <= joint.patterns
        missing = joint.patterns - naive
        if name == "reference":
            assert projections["A"]["mask"] == 1016
            assert projections["B"]["mask"] == 1023
            assert missing
        if name == "free_pairs":
            assert projections["A"]["mask"] == projections["B"]["mask"] == 1023

        records.append({
            "name": name,
            "inputs": {"A": {"class_id": id_a, "source_cell_key": str(id_a), "pair": pair_a},
                       "B": {"class_id": id_b, "source_cell_key": str(id_b), "pair": pair_b}},
            "identifications": [[f"a{a}", f"b{b}"] for a, b in zip(pair_a, pair_b)],
            "boundary_maps": {"A": map_a, "B": map_b},
            "joint": relation_payload(joint), "projections": projections,
            "graph": {
                "vertices": vertices, "edges": all_edges,
                "source_vertex_maps": {"A": graph_map_a, "B": graph_map_b},
                "source_edges_with_frames": {"A": edges_a, "B": edges_b},
                "shared_edges": sorted(actual_a & actual_b),
                "selected_pair_is_actual_edge": {
                    "A": tuple(sorted(pair_a)) in edges_a,
                    "B": tuple(sorted(pair_b)) in edges_b},
                "witnesses": [{"pattern": row, "colouring": graph_witnesses[row]}
                              for row in sorted(joint.patterns)],
            },
            "checks": {"complete_interface_assignments": 4**8,
                       "exhaustive_relation_matches_join": True,
                       "graph_backtracking_matches_join": True,
                       "both_projection_guards_match": True},
            "independently_normalized_negative_control": {
                "orbits_retained": len(naive), "orbits_lost": len(missing),
                "lost_pattern": min(missing) if missing else None},
            "pair_only_negative_control": {
                "description": "Both proper C5 frames plus the shared-pair projections only",
                "spurious_orbits": len(spurious),
                "spurious_pattern": min(spurious) if spurious else None},
            "geometry": {"abstract_planarity": "unknown",
                         "A_frame_is_disk_boundary": "unknown",
                         "B_frame_is_disk_boundary": "unknown",
                         "prescribed_sides_and_region_overlap": "unknown"},
        })

    source_paths = (CELL_SOURCE, "scripts/boundary_relations.py",
                    str(Path(__file__).resolve().relative_to(ROOT)))
    ids = sorted({spec[i] for spec in specs for i in (1, 3)})
    return {
        "schema": "c5-two-vertex-join-v1",
        "scope": "Selected named joins of existing representatives; no complete successor table or topology classification.",
        "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in source_paths},
        "pattern_order": patterns,
        "source_checks": [{"class_id": mask, "vertices": source(mask)[1],
                           "interface_assignments": 4**5,
                           "graph_matches_catalogue_relation": True} for mask in ids],
        "cases": records,
    }


def parse_pair(value):
    try:
        pair = tuple(int(i) for i in value.split(","))
        validate_pair(pair)
        return pair
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="recompute and compare without writing")
    parser.add_argument("--class-a", type=int)
    parser.add_argument("--class-b", type=int)
    parser.add_argument("--pair-a", type=parse_pair, help="ordered pair, e.g. 0,2")
    parser.add_argument("--pair-b", type=parse_pair, help="images of the ordered A pair, e.g. 1,0")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    selection = (args.class_a, args.pair_a, args.class_b, args.pair_b)
    if any(value is not None for value in selection):
        if any(value is None for value in selection):
            parser.error("Specify both class IDs and both ordered pairs together")
        specs = (("custom", *selection),)
        suffix = f"R{args.class_a}_{''.join(map(str, args.pair_a))}_R{args.class_b}_{''.join(map(str, args.pair_b))}"
        default_output = OUTPUT_DIR / f"join_{suffix}.json"
    else:
        specs = CASES
        default_output = OUTPUT_DIR / "eight_point_joins.json"
    try:
        result = build(specs)
    except ValueError as error:
        parser.error(str(error))
    output = args.output or default_output
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    if args.check:
        if not output.exists() or output.read_bytes() != payload:
            raise SystemExit(f"FAIL: saved joins differ or are missing: {output}")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(payload)
    print(json.dumps({"mode": "check" if args.check else "write", "status": "pass",
                      "bytes": len(payload), "cases": [
                          {"name": r["name"], "orbits": r["joint"]["global_s4_orbits"],
                           "labelled": r["joint"]["labelled_assignments"],
                           "projection_A": r["projections"]["A"]["mask"],
                           "projection_B": r["projections"]["B"]["mask"]}
                          for r in result["cases"]]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
