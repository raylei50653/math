#!/usr/bin/env python3
"""Independent D6 finite checks; no imports of repository checkers.

Reads frozen source data, independently reconstructs the small P3 relation,
counts components from the root-side partition, and verifies verdict bindings.
Topology and the unbounded Gallai argument remain paper evidence.
"""
import argparse
import ast
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FRAME = {(i, (i + 1) % 5) for i in range(5)}
Q = (0, 1, 0, 1, 2)


def digest(value):
    return sha256(value).hexdigest()


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False,
                       separators=(",", ":")) + "\n").encode()


def resolve(value, pointer):
    for part in pointer.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def connected(vertices, edges):
    vertices = set(vertices)
    if not vertices:
        return False
    reached = {next(iter(vertices))}
    frontier = list(reached)
    while frontier:
        v = frontier.pop()
        for a, b in edges:
            t = b if a == v else a if b == v else None
            if t in vertices and t not in reached:
                reached.add(t)
                frontier.append(t)
    return reached == vertices


def read(rel):
    return json.loads((HERE / "snapshot" / rel).read_text())


def hub_controls():
    """Check explicit hub sets even for empty/singleton hypothetical support.

    This is a wiring control, not a realization or a Gallai theorem proof.
    The root color is arbitrary; only colors on N(D) must be constant per hub.
    """
    checked = 0
    tight_checked = 0
    bverts = {f"b{i}" for i in range(5)}
    bedges = {(f"b{a}", f"b{b}") for a, b in FRAME}
    for support0 in combinations(range(5), 3):
        for a, b in sorted(FRAME):
            h = next(i for i in support0 if i not in (a, b))
            route = ["r", "x2", "x1", "x0", f"b{h}"]
            edges = bedges | set(zip(route, route[1:]))
            for bitmask, color in product(range(4), range(4)):
                support = {v for j, v in enumerate((a, b)) if bitmask & (1 << j)}
                neighbors = {f"b{i}" for i in support} | {"r"}
                colors = {f"b{i}": Q[i] for i in range(5)} | {"r": color}
                if color in (Q[a], Q[b]):
                    other = b if color == Q[a] else a
                    hubs = [{f"b{other}"}, (bverts - {f"b{other}"}) | set(route)]
                    labels = [Q[other], color]
                else:
                    hubs = [{f"b{a}"}, {f"b{b}"},
                            (bverts - {f"b{a}", f"b{b}"}) | set(route)]
                    labels = [Q[a], Q[b], color]
                assert len(set(labels)) == len(labels)
                assert neighbors <= set.union(*hubs)
                assert all(connected(hub, edges) for hub in hubs)
                for i, hub in enumerate(hubs):
                    assert all(colors[v] == labels[i] for v in hub & neighbors)
                    for j in range(i):
                        assert not hub & hubs[j]
                        assert any((u in hub and v in hubs[j]) or
                                   (v in hub and u in hubs[j]) for u, v in edges)
                checked += 1
                # Tightness means each D vertex has distinct outside colors.
                for size in range(4):
                    for ext in combinations(sorted(neighbors), size):
                        if len({colors[v] for v in ext}) != len(ext):
                            continue
                        assert all(len(set(ext) & hub) <= 1 for hub in hubs)
                        tight_checked += 1
    return {"explicit_short_support_hub_instances": checked,
            "tight_outside_neighbor_subsets": tight_checked,
            "includes_empty_and_singleton_support": True}


def audit():
    scope = read("audits/2026-10-04-task-d5/c4/scope_ledger.json")
    ledger = read("artifacts/c5_open_leaf_ledger/ledger.json")
    verdicts = read("artifacts/c5_qcore_shield_budget/verdicts.json")
    common = read(ledger["common_source"])
    rows = {tuple(row["key"]): row for row in scope["ledger"]}
    leaves = {tuple(leaf["key"]): leaf for leaf in ledger["leaves"]}
    output = {tuple(v["key"]): v for v in verdicts["verdicts"]}
    assert len(rows) == len(scope["ledger"]) == 3500
    assert len(leaves) == len(ledger["leaves"]) == 3500
    assert rows.keys() == leaves.keys()
    assert len(output) == len(verdicts["verdicts"]) == 3497
    assert digest(canonical_bytes(sorted(map(list, rows)))) == ledger["domain_sha256"]
    assert ledger["domain_sha256"] == verdicts["domain_sha256"]
    for rel, expected in ledger["sources"].items():
        raw = (HERE / "snapshot" / rel).read_bytes()
        assert expected == {"sha256": digest(raw), "bytes": len(raw)}, rel
    unary_histogram = Counter()
    unknown_own_supports = 0
    per_key = []
    coverage = Counter()
    closed = []
    for key, row in rows.items():
        leaf = leaves[key]
        assert resolve(scope, leaf["scope_pointer"]) == row
        assert resolve(common, leaf["common_case_pointer"]) == row["case"]
        assert resolve(common, leaf["common_geometry_pointer"]) == row["geometry"]
        assert row["common_color_frame"] == list(Q)
        p3 = row["original_components"]
        assert p3["ordered_vertices"] == ["x0", "x1", "x2"]
        assert p3["root_masks"] == [0, 0, 3]
        support = row["original_P3_actual_supports"]
        assert list(map(len, map(set, support))) == [3, 2, 1]
        mixed_support = set.union(*(set(s) for s in support))
        assert not any(mixed_support <= {a, b} for a, b in FRAME)
        lists = [set(range(4)) - {Q[i] for i in s} for s in support]
        triples = sorted(t for t in product(range(4), repeat=3)
                         if all(t[i] in lists[i] for i in range(3))
                         and t[0] != t[1] and t[1] != t[2])
        assert list(map(list, triples)) == row["original_P3_complete_tuples"]
        rejected_pairs = []
        for u, v in product(range(4), repeat=2):
            lifts = [t for t in triples if t[2] not in (u, v)]
            record = row["complete_P3_root_fibres"][4 * u + v]
            assert record["root_pair"] == [u, v]
            assert record["complete_original_P3_tuples"] == list(map(list, lifts))
            assert record["full_P3_lifts"] == [dict(zip(("x0", "x1", "x2"), t))
                                               for t in lifts]
            if not lifts:
                rejected_pairs.append([u, v])
        assert rejected_pairs == row["original_P3_forbidden_pairs"]
        components = row["original_unary_components"]
        names = [d["component"] for d in components]
        assert len(set(names)) == len(names)
        contacts = [c for d in components for c in d["ordered_original_contacts"]]
        assert len(contacts) == len(set(contacts))
        independently_counted = 0
        nodes = {"z", "w", "C*"} | set(names)
        edges = {("z", "w"), ("z", "C*"), ("w", "C*")}
        for root in ("z", "w"):
            role = row[root + "_role"]
            ds = [d for d in components if d["root"] == root]
            partition = role["unary_contacts"]
            independently_counted += len(partition)
            assert len(ds) == len(partition) >= 1
            assert len(role["spoke_colors"]) + sum(partition) + 2 == 5
            assert role == common["local"]["side_roles"][row["side_ids"][0 if root == "z" else 1]]
            for d, size, forbidden in zip(ds, partition, role["unary_forbidden"], strict=True):
                assert len(d["ordered_original_contacts"]) == size
                assert d["forbidden_colors"] == forbidden
                assert 0 < len(forbidden) <= size
                edges.add((root, d["component"]))
        assert independently_counted == len(components)
        assert connected(nodes, edges)
        assert all(connected(nodes - {p}, edges) for p in ["C*"] + names)
        if row["closed_by"]:
            assert leaf["closed_by"] in row["closed_by"]
            assert key not in output
            closed.append(list(key))
            continue
        assert leaf["status"] == "open_unreviewed" and leaf["closed_by"] is None
        v = output[key]
        assert resolve(ledger, v["ledger_pointer"]) == leaf
        assert resolve(scope, v["scope_pointer"]) == row
        assert v["id"] == leaf["id"]
        assert v["complete_scope_row_sha256"] == digest(canonical_bytes(row))
        cert = verdicts["certificates"][v["certificate"]]
        assert digest(canonical_bytes(cert)) == v["certificate"]
        assert cert["original_mixed_support"] == sorted(mixed_support)
        assert {tuple(x) for x in cert["piece_owners"]} == {(d["component"], d["root"]) for d in components}
        assert {tuple(e) for e in cert["one_sided_incidence_edges"]} == edges
        assert cert["shield_lower_bounds"] == {p: 2 for p in ["C*"] + names}
        assert cert["required_frame_edges"] == 2 * (1 + independently_counted) > 5
        assert cert["available_frame_edges"] == 5
        assert len(cert["external_path_template_r_is_each_unary_owner"]) == 5
        for path in cert["external_path_template_r_is_each_unary_owner"]:
            assert tuple(path["hypothetical_short_support_edge"]) in FRAME
            assert path["h"] in support[0]
            assert path["h"] not in path["hypothetical_short_support_edge"]
            assert path["path"] == ["r", "x2", "x1", "x0", f'b{path["h"]}']
        unary_histogram[independently_counted] += 1
        unknown_own_supports += sum(d["actual_own_support"] is None for d in components)
        whole = mixed_support | set.union(*(set(s) for s in row["geometry"]["actual_side_supports"]))
        coverage[",".join(map(str, sorted(whole)))] += 1
        per_key.append({"key": list(key), "unary_components": names,
                        "contacts_are_not_counted_as_components": True,
                        "unary_count": independently_counted,
                        "shield_lower_bound": 2 * (1 + independently_counted)})
    assert output.keys() == {k for k, row in rows.items() if not row["closed_by"]}
    source_drift = []
    for rel, recorded in verdicts["sources"].items():
        raw = (HERE / "snapshot" / rel).read_bytes()
        current = {"sha256": digest(raw), "bytes": len(raw)}
        if current != recorded:
            source_drift.append({"file": rel, "recorded": recorded, "current": current})
    tree = ast.parse((HERE / "snapshot/scripts/c5_qcore_shield_screen.py").read_text())
    docs = next(ast.literal_eval(node.value) for node in tree.body
                if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "DOCS"
                                                        for t in node.targets))
    missing_docs = [rel for rel in docs if rel not in verdicts["sources"]]
    return {"scope_keys": len(rows), "open_keys": len(output), "inherited_closed_keys": closed,
            "unary_count_distribution": dict(sorted(unary_histogram.items())),
            "distinct_component_instances_across_open_keys": sum(k * v for k, v in unary_histogram.items()),
            "unknown_unary_own_support_instances": unknown_own_supports,
            "whole_source_support_census": dict(coverage), "hub_controls": hub_controls(),
            "verdict_payload_checks": "PASS", "recorded_source_hash_drift": source_drift,
            "current_script_DOCS_missing_from_verdict_sources": missing_docs,
            "strict_current_replay_source_bindings": "PASS" if not source_drift and not missing_docs else "FAIL",
            "finite_scope_limit": "Named necessary classes; unary internals remain unknown; no unbounded theorem proven by Python",
            "per_key": per_key}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "per_key"}, indent=2, ensure_ascii=False))
