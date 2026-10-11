#!/usr/bin/env python3
"""Fixed original-graph controls for E-ARC2 component slack.

No graph search. Enumerate complete colourings on the saved 63 dual-root ER
graphs, retaining literal vertex coordinates. Generation is exclusive;
--check is a read-only, byte-for-byte replay.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_excess_two_independent_coloring import sigma_mask
from c5_kempe_screen import REPS

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/c5_excess_two_arc_pair_critical/observations.json"
DEFAULT = ROOT / "artifacts/c5_excess_two_arc_component_slack/observations.json"
ROW_INDEX = {0: 6, 1: 4, 2: 3, 3: 1, 4: 0}
PINS = tuple(product(range(4), repeat=2))


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode()


def digest(value):
    return sha256(encode(value)).hexdigest()


def clean(edges):
    return tuple(sorted(tuple(sorted(e)) for e in edges))


def lifts(edges, vertices, fixed):
    """All full tuples on the explicit ordered coordinates, including isolates."""
    vertices = tuple(vertices)
    adjacency = {v: set() for v in set(vertices) | set(fixed)}
    for u, v in edges:
        assert u in adjacency and v in adjacency
        adjacency[u].add(v)
        adjacency[v].add(u)
        if u in fixed and v in fixed and fixed[u] == fixed[v]:
            return ()
    colors = dict(fixed)
    result = []

    def visit(i):
        if i == len(vertices):
            result.append(tuple(colors[v] for v in vertices))
            return
        v = vertices[i]
        forbidden = {colors[w] for w in adjacency[v] if w in colors}
        for c in range(4):
            if c not in forbidden:
                colors[v] = c
                visit(i + 1)
        colors.pop(v, None)

    visit(0)
    return tuple(result)


def components(edges, roots):
    adjacency = {}
    for u, v in edges:
        adjacency.setdefault(u, set()).add(v)
        adjacency.setdefault(v, set()).add(u)
    pending = {v for v in adjacency if v >= 5} - set(roots)
    result = []
    while pending:
        component, stack = set(), [min(pending)]
        while stack:
            v = stack.pop()
            if v in component:
                continue
            component.add(v)
            stack.extend(sorted(adjacency[v] & pending - component))
        pending -= component
        result.append(tuple(sorted(component)))
    return result, adjacency


def repeated_rows(component, adjacency, rows):
    return sorted(q for q in rows if any(
        len({REPS[ROW_INDEX[q]][b] for b in adjacency[v] if b < 5})
        < len([b for b in adjacency[v] if b < 5]) for v in component))


def produce():
    raw = SOURCE.read_bytes()
    saved = json.loads(raw)
    counts, records = Counter(), []
    for source_id, source in enumerate(saved["records"]):
        edges = clean(source["edges"])
        degrees = Counter(v for e in edges for v in e)
        roots = tuple(sorted(v for v, d in degrees.items() if v >= 5 and d == 5))
        if len(roots) != 2:
            continue
        assert all(d == 4 for v, d in degrees.items() if v >= 5 and v not in roots)
        pieces, adjacency = components(edges, roots)
        interior = tuple(sorted(v for v in degrees if v >= 5))
        full = [lifts(edges, interior, dict(enumerate(beta))) for beta in REPS]
        mask = sum(1 << i for i, col in enumerate(full) if col)
        assert mask == source["sigma_mask"] == sigma_mask(edges)
        qset = source["Q"]
        assert 2 * len(qset) - sum((q + 1) % 5 in qset for q in qset) <= 4
        counts["source_graphs"] += 1
        counts["complete_source_rows"] += 10
        property_p = all(len(d["Q"]) <= 1 for d in source["deletions"])
        assert not source["hypothesis_triggered"] or property_p
        counts["P_triggered" if property_p else "P_not_triggered"] += 1
        no_two_root44 = not any(c["epsilon"] == 0 and
            set(roots) <= {v for e in c["edges"] for v in e} for c in source["cores"])
        zero_rows = set(source["zero_core_rows"])
        piece_records = []
        for component in pieces:
            cset = set(component)
            region_edges = tuple(e for e in edges if cset.intersection(e))
            outside_edges = tuple(e for e in edges if not cset.intersection(e))
            outside = tuple(v for v in interior if v not in cset)
            positions = tuple(interior.index(v) for v in outside)
            incidence = tuple(sum(r in adjacency[v] for v in component) for r in roots)
            nonunit = all(incidence) or max(incidence) >= 2
            repeated = repeated_rows(component, adjacency, qset)
            outside_lifts = [lifts(outside_edges, outside, dict(enumerate(beta))) for beta in REPS]
            residual_q = sorted(q for q in qset if not outside_lifts[ROW_INDEX[q]])
            assert set(repeated) <= set(residual_q)
            if property_p:
                assert len(residual_q) <= 1
            if no_two_root44 and nonunit:
                assert set(residual_q) <= zero_rows
                counts["nonunit_Z_bound_triggered"] += 1
                if not zero_rows:
                    assert not residual_q
                    counts["nonunit_all_rows_released"] += 1
            counts["components"] += 1
            counts["rejected_row_boundary_slack_triggers"] += len(repeated)
            row_records = []
            for i, beta in enumerate(REPS):
                fixed_boundary = dict(enumerate(beta))
                local = []
                for a, b in PINS:
                    fixed = {**fixed_boundary, roots[0]: a, roots[1]: b}
                    local.append(lifts(region_edges, component, fixed))
                allowed = {pins for pins, fiber in zip(PINS, local) if fiber}
                joint = []
                for exterior_tuple in outside_lifts[i]:
                    ext = dict(zip(outside, exterior_tuple))
                    pins = (ext[roots[0]], ext[roots[1]])
                    for local_tuple in local[PINS.index(pins)]:
                        assignment = {**ext, **dict(zip(component, local_tuple))}
                        joint.append(tuple(assignment[v] for v in interior))
                assert tuple(sorted(joint)) == full[i]
                counts["complete_fibre_joins_checked"] += 1
                duplicate = any(len({beta[b] for b in adjacency[v] if b < 5})
                    < len([b for b in adjacency[v] if b < 5]) for v in component)
                if duplicate:
                    assert allowed == set(PINS)
                    counts["all_row_boundary_slack_triggers"] += 1
                deletions = []
                for edge in region_edges:
                    child_edges = tuple(e for e in edges if e != edge)
                    child = lifts(child_edges, interior, fixed_boundary)
                    projected = tuple(sorted({tuple(t[j] for j in positions) for t in child}))
                    assert projected == outside_lifts[i]
                    # An independently enumerated local region checks all 16 pins,
                    # even when an outside fibre is empty or root-spokes forbid it.
                    local_child = tuple(e for e in region_edges if e != edge)
                    child_fibres = []
                    for a, b in PINS:
                        fixed = {**fixed_boundary, roots[0]: a, roots[1]: b}
                        fiber = lifts(local_child, component, fixed)
                        assert fiber
                        child_fibres.append(fiber)
                    counts["ambient_pin_cells_checked"] += 16
                    counts["complete_exterior_projection_checks"] += 1
                    deletions.append({"edge": edge, "full_lifts_count": len(child),
                        "full_lifts_sha256": digest(child),
                        "local_pin_fibres_counts": [len(f) for f in child_fibres],
                        "local_pin_fibres_sha256": digest(child_fibres),
                        "projection_sha256": digest(projected)})
                row_records.append({"row_index": i, "beta": beta,
                    "local_full_fibres_by_pins": local,
                    "outside_full_lifts": outside_lifts[i],
                    "global_full_lifts_sha256": digest(full[i]),
                    "boundary_slack": duplicate, "deletions": deletions})
            piece_records.append({"vertices": component, "edges": region_edges,
                "root_incidence": incidence, "nonunit": nonunit,
                "outside_coordinates": outside, "Q_after_piece_deletion": residual_q,
                "rejected_boundary_slack_rows": repeated, "rows": row_records})
        records.append({"pair_critical_source_id": source_id,
            "source": source["source"], "source_ordinal": source["ordinal"],
            "edges": edges, "roots": roots, "interior_coordinates": interior,
            "sigma_mask": mask, "Q": qset, "Z": sorted(zero_rows),
            "P_triggered": property_p, "no_two_root44": no_two_root44,
            "components": piece_records})

    # A fixed local path passes the old per-vertex test but fails the new
    # component test for the stipulated target rows. It is NOT a target source.
    toy_edges = clean([(0, 7), (1, 7), (2, 7), (7, 8), (8, 9),
                       (1, 9), (2, 9), (3, 9), (5, 8), (6, 8)])
    toy_pieces, toy_adj = components(toy_edges, (5, 6))
    assert toy_pieces == [(7, 8, 9)]
    toy_per_vertex = {str(v): repeated_rows((v,), toy_adj, (0, 1, 3)) for v in (7, 8, 9)}
    assert all(len(q) <= 1 for q in toy_per_vertex.values())
    assert repeated_rows((7, 8, 9), toy_adj, (0, 1, 3)) == [0, 3]
    toy_relations = []
    for q in (0, 1, 3):
        beta = REPS[ROW_INDEX[q]]
        fibers = [lifts(toy_edges, (7, 8, 9), {**dict(enumerate(beta)), 5: a, 6: b})
                  for a, b in PINS]
        if q in (0, 3):
            assert all(fibers)
        toy_relations.append({"q": q, "fibres": fibers})

    pair_table = [{"boundary_pair": pair,
                   "repeated_target_rows": [q for q in (0, 1, 3)
                       if REPS[ROW_INDEX[q]][pair[0]] == REPS[ROW_INDEX[q]][pair[1]]]}
                  for pair in combinations(range(5), 2)]
    assert counts["source_graphs"] == 63 and counts["components"] == 179
    inputs = [{"path": str(SOURCE.relative_to(ROOT)), "sha256": sha256(raw).hexdigest()}]
    for name in ("scripts/c5_excess_two_independent_coloring.py", "scripts/c5_kempe_screen.py"):
        inputs.append({"path": name, "sha256": sha256((ROOT / name).read_bytes()).hexdigest()})
    return {"scope": "fixed 63 original ER dual-root graphs; no source search",
            "inputs": inputs, "pin_order": PINS, "counts": dict(sorted(counts.items())),
            "records": records, "canonical_pair_table": pair_table,
            "vertexwise_test_insufficient_control": {"edges": toy_edges,
                "component": (7, 8, 9), "per_vertex": toy_per_vertex,
                "component_rows": [0, 3], "relations": toy_relations,
                "status": "local degree-4 control only; no target source or disk claim"},
            "target_source_status": "not triggered", "E_ARC2": "OPEN"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT)
    args = parser.parse_args()
    result = produce()
    raw = encode(result)
    if args.check:
        assert args.output.read_bytes() == raw, "artifact mismatch"
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("xb") as stream:
            stream.write(raw)
    print(json.dumps({"check": args.check, "sha256": sha256(raw).hexdigest(),
                      "bytes": len(raw), **result["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
