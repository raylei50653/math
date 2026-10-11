#!/usr/bin/env python3
"""Fixed same-frame controls for E-ARC2 leaf-block rigidity; no graph search.

Complete local fibres are independently recomputed in numeric vertex order and
compared with the immutable component-slack artifact.  References retain empty
cells and all tuples, rather than replacing fibres with marginal information.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/c5_excess_two_arc_component_slack/observations.json"
DEFAULT = ROOT / "artifacts/c5_excess_two_arc_leaf_blocks/observations.json"
QS = (0, 1, 3)
QROWS = {0: (0, 1, 2, 1, 2), 1: (0, 1, 2, 0, 2), 3: (0, 1, 0, 2, 1)}
PINS = tuple(product(range(4), repeat=2))
BEDGES = tuple((i, (i + 1) % 5) for i in range(5))


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode()


def digest(value):
    return sha256(encode(value)).hexdigest()


def clean(edges):
    return tuple(sorted(tuple(sorted(e)) for e in edges))


def adjacency(edges, vertices=()):
    result = {v: set() for v in vertices}
    for u, v in edges:
        result.setdefault(u, set()).add(v)
        result.setdefault(v, set()).add(u)
    return result


def full_fibres(edges, coordinates, roots, beta):
    """Independent exhaustive DFS; no imported coloring implementation."""
    adj = adjacency(edges, coordinates)
    all_fibres = []
    for pin in PINS:
        fixed = {**dict(enumerate(beta)), **dict(zip(roots, pin))}
        if any(u in fixed and v in fixed and fixed[u] == fixed[v]
               for u, v in edges):
            all_fibres.append(())
            continue
        colors, found = dict(fixed), []

        def visit(position):
            if position == len(coordinates):
                found.append(tuple(colors[v] for v in coordinates))
                return
            v = coordinates[position]
            forbidden = {colors[w] for w in adj[v] if w in colors}
            for color in range(4):
                if color not in forbidden:
                    colors[v] = color
                    visit(position + 1)
            colors.pop(v, None)

        visit(0)
        all_fibres.append(tuple(found))
    return tuple(all_fibres)


def connected(vertices, edges):
    vertices = set(vertices)
    if not vertices:
        return False
    adj = adjacency((e for e in edges if set(e) <= vertices), vertices)
    seen, stack = set(), [min(vertices)]
    while stack:
        v = stack.pop()
        if v not in seen:
            seen.add(v)
            stack.extend(sorted(adj[v] - seen))
    return seen == vertices


def blocks(vertices, edges):
    """Tarjan blocks, retaining literal coordinates and bridges as K2 blocks."""
    adj = adjacency(edges, vertices)
    order, low, stack, answer = {}, {}, [], []

    def visit(v, parent=None):
        order[v] = low[v] = len(order)
        for w in sorted(adj[v]):
            if w == parent:
                continue
            if w not in order:
                stack.append((v, w))
                visit(w, v)
                low[v] = min(low[v], low[w])
                if low[w] >= order[v]:
                    block = set()
                    while True:
                        edge = stack.pop()
                        block.update(edge)
                        if edge == (v, w):
                            break
                    answer.append(tuple(sorted(block)))
            elif order[w] < order[v]:
                stack.append((v, w))
                low[v] = min(low[v], order[w])

    visit(min(vertices))
    assert len(order) == len(vertices) and not stack
    return tuple(sorted(answer))


def edge_signature(pair):
    return tuple(tuple(sorted(QROWS[q][v] for v in pair)) for q in QS)


def inspect_component(vertices, region, roots, fibres):
    adj = adjacency(region, vertices)
    internal = tuple(e for e in region if set(e) <= set(vertices))
    bs = blocks(vertices, internal)
    multiplicity = Counter(v for block in bs for v in block)
    contacts = {v for v in vertices if set(roots) & adj[v]}
    boundary = {v: tuple(sorted(w for w in adj[v] if w < 5)) for v in vertices}
    adjacent = all(len(pair) <= 2 and
                   (len(pair) < 2 or (pair[1] - pair[0]) % 5 in (1, 4))
                   for pair in boundary.values())
    forbidden = {q: tuple(pin for pin, fibre in zip(PINS, fibres[q]) if not fibre)
                 for q in QS}
    obstruction = all(forbidden[q] for q in QS)
    result = []
    for block in bs:
        block_edges = tuple(e for e in internal if set(e) <= set(block))
        badj = adjacency(block_edges, block)
        clique = all(len(badj[v]) == len(block) - 1 for v in block)
        cycle = len(block) >= 3 and len(block) % 2 == 1 and all(
            len(badj[v]) == 2 for v in block)
        if obstruction:
            assert clique or cycle
        ordinary = tuple(v for v in block if multiplicity[v] == 1 and v not in contacts)
        private_contacts = tuple(v for v in block if multiplicity[v] == 1 and v in contacts)
        leaf = len(bs) > 1 and sum(multiplicity[v] > 1 for v in block) == 1
        if obstruction and adjacent and (cycle or len(block) == 4):
            assert all(boundary[v] for v in ordinary)
            assert len({edge_signature(boundary[v]) for v in ordinary}) <= 1
            assert len({boundary[v] for v in ordinary}) <= 1
        result.append({"vertices": block, "edges": block_edges,
            "kind": "bridge" if len(block) == 2 else "odd_cycle" if cycle else
                    "clique" if clique else "other",
            "ordinary_private_vertices": ordinary, "private_root_contacts": private_contacts,
            "leaf_block": leaf,
            "ordinary_boundary_attachments": [[v, boundary[v]] for v in ordinary]})
    return {"all_three_rows_obstructed": obstruction,
        "all_vertices_have_at_most_adjacent_two_boundary_neighbors": adjacent,
        "forbidden_pins": [{"q": q, "pins": forbidden[q]} for q in QS],
        "boundary_attachments": [[v, boundary[v]] for v in vertices],
        "root_contacts": sorted(contacts), "blocks": result}


def minor_certificate(edges, bags):
    assert all(connected(bag, edges) for bag in bags)
    assert sum(len(bag) for bag in bags) == len(set(v for bag in bags for v in bag))
    witnesses = []
    for i, j in combinations(range(5), 2):
        cross = [e for e in edges if (e[0] in bags[i] and e[1] in bags[j]) or
                 (e[1] in bags[i] and e[0] in bags[j])]
        assert cross, (i, j)
        witnesses.append({"bags": (i, j), "source_edge": cross[0]})
    return {"bags": bags, "ten_original_adjacency_witnesses": witnesses}


def produce():
    source_raw = SOURCE.read_bytes()
    saved = json.loads(source_raw)
    counts, records = Counter(), []
    betas = [tuple(row["beta"]) for row in saved["records"][0]["components"][0]["rows"]]
    assert len(set(betas)) == 10
    for graph_index, graph in enumerate(saved["records"]):
        edges, roots = clean(graph["edges"]), tuple(graph["roots"])
        adj = adjacency(edges)
        interior = tuple(graph["interior_coordinates"])
        full_touch = all(any(v >= 5 for v in adj[b]) for b in range(5))
        h_connected = connected(interior, edges)
        counts["source_graphs"] += 1
        target_source = all(q in graph["Q"] for q in QS)
        counts["target_source_triggered"] += int(target_source)
        pieces = []
        for component_index, component in enumerate(graph["components"]):
            vertices, region = tuple(component["vertices"]), clean(component["edges"])
            assert region == tuple(e for e in edges if set(e) & set(vertices))
            assert all(len(adj[v]) == 4 for v in vertices)
            fibres, refs = {}, []
            for row_index, row in enumerate(component["rows"]):
                beta = tuple(row["beta"])
                actual = full_fibres(region, vertices, roots, beta)
                assert encode(actual) == encode(row["local_full_fibres_by_pins"])
                counts["complete_local_rows_recomputed"] += 1
                counts["ambient_pin_cells_recomputed"] += 16
                counts["empty_pin_fibres_recomputed"] += sum(not f for f in actual)
                for q in QS:
                    if beta == QROWS[q]:
                        fibres[q] = actual
                refs.append({"row_index": row_index, "beta": beta,
                    "complete_fibres_json_pointer":
                        f"/records/{graph_index}/components/{component_index}/rows/{row_index}/local_full_fibres_by_pins",
                    "sha256": digest(actual), "fibre_counts_in_pin_order": [len(f) for f in actual]})
            assert set(fibres) == set(QS)
            detail = inspect_component(vertices, region, roots, fibres)
            trigger = detail["all_three_rows_obstructed"]
            adjacent = detail["all_vertices_have_at_most_adjacent_two_boundary_neighbors"]
            counts["components"] += 1
            counts["all_three_local_obstruction_triggered"] += int(trigger)
            counts["adjacent_attachment_triggered"] += int(adjacent)
            counts["joint_local_rigidity_triggered"] += int(trigger and adjacent)
            if trigger and adjacent:
                for block in detail["blocks"]:
                    ordinary = block["ordinary_private_vertices"]
                    if block["kind"] == "odd_cycle":
                        counts["cycle_rigidity_blocks_triggered"] += 1
                        counts["cycle_rigidity_ordinary_vertex_pairs"] += len(ordinary) * (len(ordinary)-1)//2
                        if full_touch and h_connected:
                            assert len(ordinary) <= 1
                    if block["leaf_block"] and full_touch and h_connected:
                        counts["leaf_contact_blocks_triggered"] += 1
                        assert block["private_root_contacts"]
            pieces.append({"vertices": vertices, "edges": region,
                "root_incidence": component["root_incidence"], "complete_fibre_references": refs,
                **detail})
        records.append({"source_record_index": graph_index,
            "pair_critical_source_id": graph["pair_critical_source_id"],
            "source": graph["source"], "source_ordinal": graph["source_ordinal"],
            "edges": edges, "roots": roots, "sigma_mask": graph["sigma_mask"],
            "Q": graph["Q"], "full_boundary_touch": full_touch,
            "interior_connected": h_connected, "target_source_triggered": target_source,
            "components": pieces})

    signature_table = [{"boundary_edge": edge, "color_pair_signature": edge_signature(edge)}
                       for edge in BEDGES]
    assert len({tuple(map(tuple, row["color_pair_signature"])) for row in signature_table}) == 5
    triples = [{"boundary_subset": subset, "duplicate_rows": tuple(q for q in QS
        if len({QROWS[q][v] for v in subset}) < 3)} for subset in combinations(range(5), 3)]
    assert len(triples) == 10 and all(row["duplicate_rows"] for row in triples)
    nonadjacent = [{"boundary_pair": pair, "duplicate_rows": tuple(q for q in QS
        if QROWS[q][pair[0]] == QROWS[q][pair[1]])} for pair in combinations(range(5), 2)
        if (pair[1] - pair[0]) % 5 not in (1, 4)]
    assert len(nonadjacent) == 5 and all(row["duplicate_rows"] for row in nonadjacent)

    positive_vertices = (7, 8, 9, 10)
    positive_edges = clean(BEDGES + ((7, 8), (7, 9), (8, 9), (7, 10), (1, 7),
        (0, 8), (1, 8), (0, 9), (1, 9), (1, 10), (5, 10), (6, 10),
        (5, 6), (2, 6), (3, 6), (4, 6)))
    positive_region = tuple(e for e in positive_edges if set(e) & set(positive_vertices))
    positive_fibres = [{"beta": beta, "fibres": full_fibres(positive_region,
        positive_vertices, (5, 6), beta)} for beta in betas]
    by_q = {q: next(row["fibres"] for row in positive_fibres if row["beta"] == QROWS[q]) for q in QS}
    assert all(not by_q[q][PINS.index((2, 3))] for q in QS)
    positive_detail = inspect_component(positive_vertices, positive_region, (5, 6), by_q)
    assert positive_detail["all_three_rows_obstructed"]
    assert positive_detail["all_vertices_have_at_most_adjacent_two_boundary_neighbors"]
    positive_minor = minor_certificate(positive_edges,
        ((8,), (9,), (0,), (1,), (2, 3, 4, 5, 6, 7, 10)))

    negative_edges = clean(((7, 8), (7, 9), (8, 9), (5, 7), (3, 7),
        (2, 8), (3, 8), (3, 9), (4, 9)))
    negative_fibres = [{"beta": beta, "fibres": full_fibres(negative_edges,
        (7, 8, 9), (5, 6), beta)} for beta in betas]
    neg_q = {q: next(row["fibres"] for row in negative_fibres if row["beta"] == QROWS[q]) for q in QS}
    assert all(not neg_q[q][PINS.index((2, b))] for q in (0, 1) for b in range(4))
    assert all(neg_q[3])
    negative_detail = inspect_component((7, 8, 9), negative_edges, (5, 6), neg_q)
    assert not negative_detail["all_three_rows_obstructed"]
    assert negative_detail["all_vertices_have_at_most_adjacent_two_boundary_neighbors"]

    assert counts["source_graphs"] == 63 and counts["components"] == 179
    assert counts["target_source_triggered"] == 0
    return {"scope": "fixed original 63 ER graphs; no new source search or embedding verification",
        "inputs": [{"path": str(SOURCE.relative_to(ROOT)), "sha256": sha256(source_raw).hexdigest()}],
        "pin_order": PINS, "q_order": QS, "literal_q_rows": QROWS,
        "adjacent_boundary_edge_signatures": signature_table,
        "all_ten_boundary_triples": triples, "all_five_nonadjacent_pairs": nonadjacent,
        "counts": dict(sorted(counts.items())), "records": records,
        "root_free_leaf_triangle_positive_control": {"edges": positive_edges,
            "component": positive_vertices, "roots": (5, 6), "rows": positive_fibres,
            **positive_detail, "K5_minor": positive_minor,
            "status": "triggered and holds: nonplanar local structural control; not a disk or target source"},
        "two_row_only_nonrigid_control": {"edges": negative_edges,
            "component": (7, 8, 9), "roots": (5, 6), "rows": negative_fibres,
            **negative_detail,
            "status": "counterexample to dropping the third-row hypothesis; no source claim"},
        "target_source_status": "not triggered", "E_ARC2": "OPEN",
        "evidence_limit": "finite local controls do not prove source exclusion, planarity, or Lean theorems"}


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
    print(json.dumps({"check": args.check, "bytes": len(raw),
                      "sha256": sha256(raw).hexdigest(), **result["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
