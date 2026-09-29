#!/usr/bin/env python3
"""Original K4 and actual exterior paths for the sole fully shared mixed K2.

The arbitrary-size exclusion is a paper recoloring/minor proof. These fixed
gluing controls and selected subgraphs do not enumerate realizable sources.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import c5_adjacent_degree5_interfaces as base
from c5_single_spoke_three_one import edge, validate_minor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_adjacent_degree5_mixed_edge_k4/observations.json"
TABLE = OUT.with_name("source_minor_table.md")
CORE = ("z", "w", "u", "v")


def proper(colors, edges):
    return all(colors[a] != colors[b] for a, b in edges)


def gluing_audit():
    """Recolor one whole boundary-free unary piece; keep the exterior fixed."""
    fixtures = [
        ("singleton", (), (7,)),
        ("path", ((7, 8), (8, 9)), (7,)),
        ("triangle", tuple(combinations(range(7, 10), 2)), (7, 8, 9)),
        ("diamond", ((7, 8), (7, 9), (8, 9), (8, 10), (9, 10)), (7, 10)),
        ("k4_one_contact", tuple(combinations(range(7, 11), 2)), (7,)),
    ]
    records, count = [], Counter()
    for name, internal, ports in fixtures:
        local = {base.edge(*e) for e in internal}
        local |= {base.edge(base.Z, v) for v in ports}
        component = sorted(set().union(*(set(e) for e in local)) - {base.Z})
        vertices = tuple(range(7)) + tuple(component)
        exterior = set(base.CYCLE) | {base.edge(base.Z, base.W), base.edge(base.W, 0)}
        edges = exterior | local
        references, deletions, glued = {}, {}, []
        for old in base.U:
            g = base.first_coloring(vertices, edges - {base.edge(base.Z, base.W)},
                                    dict(enumerate(base.Q)) | {base.Z: old})
            assert g is not None and proper(g, local)
            references[old] = g
        for cut, new in product(sorted(local), base.U):
            f = None
            for common in base.U:
                fixed = dict(enumerate(base.Q)) | {base.Z: new}
                if any(v in fixed and fixed[v] != common for v in cut):
                    continue
                fixed.update({v: common for v in cut})
                f = base.first_coloring(vertices, edges - {cut}, fixed)
                if f is not None:
                    break
            assert f is not None and f[cut[0]] == f[cut[1]]
            deletions[cut, new] = f
        for old, new, cut in product(base.U, base.U, sorted(local)):
            g, f = references[old], deletions[cut, new]
            sigma = list(base.U)
            sigma[old], sigma[new] = sigma[new], sigma[old]
            h = dict(f) | {v: sigma[g[v]] for v in component}
            assert all(h[v] == f[v] for v in vertices if v not in component)
            assert tuple(h[v] for v in range(5)) == base.Q
            assert proper(h, edges)
            glued.append(dict(old_root=old, new_root=new, deleted_edge=cut,
                              permutation=sigma, coloring=[h[v] for v in vertices]))
            count["whole_component_gluings"] += 1
        for old, sigma in product(base.U, permutations(base.U)):
            g = references[old]
            moved = {v: sigma[g[v]] for v in component + [base.Z]}
            assert proper(moved, local)
            for cut in sorted(local):
                f = deletions[cut, sigma[old]]
                h = dict(f) | {v: moved[v] for v in component}
                assert proper(h, edges)
                count["shared_frame_permutation_gluings"] += 1
        records.append(dict(name=name, vertices=vertices, component=component,
                            root=base.Z, original_edges=sorted(edges),
                            reference_zw_deleted_colorings=[dict(root_color=c, coloring=[g[v] for v in vertices])
                                for c, g in sorted(references.items())],
                            edge_deleted_colorings=[dict(deleted_edge=cut, root_color=c,
                                                         coloring=[f[v] for v in vertices])
                                for (cut, c), f in sorted(deletions.items())],
                            glued_colorings=glued))
    # Boundary-free symmetry alone also allows an uncolorable piece. The
    # outside-edge deletion witness in the paper lemma cannot be dropped.
    bad_vertices = (base.Z, 7, 8, 9, 10)
    bad_edges = set(combinations(bad_vertices, 2))
    assert base.first_coloring(bad_vertices, bad_edges, {}) is None
    negative = dict(vertices=bad_vertices, edges=sorted(bad_edges),
                    reason="uncolorable boundary-free piece; no zw-deletion reference exists")
    return records, negative, dict(count)


def minor_audit():
    records, counts = [], Counter()
    placements = [("offset", (i + 1) % 5, (j + 2) % 5, i, j)
                  for i, j in product(range(5), repeat=2)]
    placements += [("all_shared", i, i, i, i) for i in range(5)]
    for placement, lengths in product(placements, product((1, 2, 4), repeat=2)):
        kind, bz, bw, bu, bv = placement
        es = {edge(f"b{i}", f"b{(i + 1) % 5}") for i in range(5)}
        core_edges = {edge(a, b) for a, b in combinations(CORE, 2)}
        es |= core_edges
        paths = {}
        for r, target, length in zip(CORE, (bz, bw, bu, bv), (*lengths, 1, 1)):
            paths[r] = [r] + [f"{r}_ext_{k}" for k in range(1, length)] + [f"b{target}"]
            es.update(edge(a, b) for a, b in zip(paths[r], paths[r][1:]))
        outside = {f"b{i}" for i in range(5)}
        outside.update(v for path in paths.values() for v in path[1:])
        groups = [{r} for r in CORE] + [outside]
        witness = dict(edges=sorted(es), branch_sets=[sorted(g) for g in groups])
        assert validate_minor(witness)
        owners = {v: i for i, group in enumerate(groups) for v in group}
        quotient = {tuple(sorted((owners[a], owners[b]))) for a, b in es if owners[a] != owners[b]}
        assert quotient == set(combinations(range(5), 2))
        adjacency = []
        for a, b in combinations(range(5), 2):
            original = min(e for e in es if {owners[e[0]], owners[e[1]]} == {a, b})
            adjacency.append(dict(branch_pair=[a, b], original_edge=original))
        cut_edges = core_edges | {edge(a, b) for path in paths.values() for a, b in zip(path, path[1:])}
        for cut in sorted(cut_edges):
            assert not validate_minor(dict(witness, edges=sorted(es - {cut})))
            counts["edge_removal_witness_failures"] += 1
        # A route z-u-B cannot be used as an exterior z path: u already owns
        # a different branch set. This checks the specific overlap failure.
        wrong = [sorted(g) for g in groups[:-1]] + [sorted(outside | {"u"})]
        assert not validate_minor(dict(witness, branch_sets=wrong))
        counts["overlapping_branch_set_failures"] += 1
        records.append(dict(id=len(records), placement=kind,
                            attachments=dict(zip(CORE, (bz, bw, bu, bv))),
                            root_path_lengths=lengths, actual_paths=paths,
                            **witness, ten_adjacencies=adjacency,
                            removed_edges_invalidating_this_witness=sorted(cut_edges)))
    assert len(records) == 270
    counts["K5_selected_subgraphs"] = len(records)
    return records, dict(counts)


def incidence_audit():
    """All nine labeled nonempty subset pairs; whole-source relabelings only."""
    subsets = (("u",), ("v",), ("u", "v"))
    representatives = {
        "same_endpoint": {edge("z", "u"), edge("w", "u")},
        "different_endpoints": {edge("z", "u"), edge("w", "v")},
        "shared_endpoint": {edge("z", "u"), edge("z", "v"), edge("w", "u")},
        "full_k4": {edge(r, v) for r in ("z", "w") for v in ("u", "v")},
    }
    records, counts = [], Counter()
    for pz, pw in product(subsets, repeat=2):
        incidences = {edge("z", v) for v in pz} | {edge("w", v) for v in pw}
        if len(pz) == len(pw) == 2:
            kind = "full_k4"
        elif len(pz) + len(pw) == 3:
            kind = "shared_endpoint"
        else:
            kind = "same_endpoint" if pz == pw else "different_endpoints"
        mappings = []
        for swap_roots, swap_ends in product((False, True), repeat=2):
            mapping = dict(zip(CORE, ("w", "z") if swap_roots else ("z", "w")))
            mapping.update(dict(zip(("u", "v"), ("v", "u") if swap_ends else ("u", "v"))))
            if {edge(mapping[a], mapping[b]) for a, b in incidences} == representatives[kind]:
                mappings.append(mapping)
        assert mappings
        records.append(dict(id=len(records), ports_z=pz, ports_w=pw,
                            incidences=sorted(incidences), kind=kind,
                            whole_source_maps_to_representative=mappings,
                            boundary_map=list(range(5)), color_map=list(base.U)))
        counts[kind] += 1
    assert counts == {"same_endpoint": 2, "different_endpoints": 2, "shared_endpoint": 4, "full_k4": 1}
    return records, dict(counts)


def fixed_source_audit():
    """A genuine degree-(5,5,4,...) minimal q-core; its K5 forbids planarity."""
    vertices = tuple(range(13))
    edges = set(base.CYCLE) | set(combinations(range(5, 9), 2))
    edges |= {base.edge(7, 4), base.edge(8, 4)}
    for root, pair in ((base.Z, (9, 10)), (base.W, (11, 12))):
        edges.add(base.edge(*pair))
        for v in pair:
            edges.add(base.edge(root, v))
            edges.update(base.edge(v, b) for b in (0, 1))
    degrees = {v: sum(v in e for e in edges) for v in range(5, 13)}
    assert degrees == {v: 5 if v in (base.Z, base.W) else 4 for v in range(5, 13)}
    fixed = dict(enumerate(base.Q))
    assert base.first_coloring(vertices, edges, fixed) is None
    deletions = []
    for cut in sorted(edges - base.CYCLE):
        f = base.first_coloring(vertices, edges - {cut}, fixed)
        assert f is not None and f[cut[0]] == f[cut[1]]
        assert proper(f, edges - {cut})
        deletions.append(dict(deleted_edge=cut, coloring=[f[v] for v in vertices]))
    assert len(deletions) == 22
    paths = [[5, 9, 0], [6, 11, 0], [7, 4], [8, 4]]
    for path in paths:
        assert all(base.edge(a, b) in edges for a, b in zip(path, path[1:]))
    outside = sorted(set(range(5)) | {v for path in paths for v in path[1:-1]})
    witness = dict(edges=sorted(edges), branch_sets=[[v] for v in range(5, 9)] + [outside])
    assert validate_minor(witness)
    return dict(vertices=vertices, **witness, inner_degrees=degrees,
                original_components_after_removing_roots=[[7, 8], [9, 10], [11, 12]],
                q=base.Q, q_rejected=True, deletion_colorings=deletions,
                actual_paths=paths, planar=False,
                scope="actual minimal q-core, explicitly nonplanar by the saved K5 witness")


def build():
    gluing, negative, gc = gluing_audit()
    minors, mc = minor_audit()
    incidences, ic = incidence_audit()
    source = fixed_source_audit()
    inputs = ["scripts/c5_adjacent_degree5_interfaces.py", "scripts/c5_single_spoke_three_one.py"]
    return dict(schema=1, source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                inputs_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
                scope="paper exclusion for arbitrary planar minimal sources; finite fixtures are not full degree/list sources",
                summary=dict(**gc, **mc, gluing_fixtures=len(gluing),
                             incidence_cases=len(incidences), incidence_classes=ic,
                             actual_nonplanar_minimal_sources=1, actual_source_deletions=len(source["deletion_colorings"]),
                             target_queries=0, uses_T4=False, uses_degree_list_theorem=False),
                boundary_free_gluing=gluing, missing_reference_negative_control=negative,
                source_minor_controls=minors, labeled_incidence_cover=incidences,
                actual_nonplanar_source=source)


def table(result):
    lines = ["# Fully shared mixed K2: original K4 and exterior paths", "",
             "The paper proof excludes every planar source in the stated class.",
             "The 270 rows below are selected subgraphs, not degree/list source realizations.",
             "Branch sets: {z}, {w}, {u}, {v}, and B plus the interiors of the actual exterior paths.",
             "Every witness uses six original K4 edges and four original exterior incidences.",
             "T4 and target queries are not used.", "",
             "| ID | Placement | z,w,u,v boundary ends | z,w path lengths | Edge-removal failures |",
             "| ---: | --- | --- | --- | ---: |"]
    for r in result["source_minor_controls"]:
        ends = [r["attachments"][v] for v in CORE]
        lines.append(f"| {r['id']} | {r['placement']} | {ends} | {r['root_path_lengths']} | "
                     f"{len(r['removed_edges_invalidating_this_witness'])} |")
    lines += ["", "## Complete labeled K2 incidence cover", "",
              "Maps rename the entire source and fix boundary vertices and colors.", "",
              "| ID | Pz | Pw | Class |", "| ---: | --- | --- | --- |"]
    for r in result["labeled_incidence_cover"]:
        lines.append(f"| {r['id']} | {list(r['ports_z'])} | {list(r['ports_w'])} | {r['kind']} |")
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
