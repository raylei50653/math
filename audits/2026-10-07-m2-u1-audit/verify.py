#!/usr/bin/env python3
"""Independent M2 finite audit, with pinned-root MRV existential searches.

This file imports no repository producer or checker. All graph decisions are
made on the literal edge sets loaded from the two immutable JSON inputs. The
existential solver tests all 16 ordered root-color pairs for each boundary row;
it neither filters a stored relation to obtain a restored relation nor builds
root-pair relations from separately normalized sides.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import subprocess


CANDIDATE = "ba0b447f09617591d9f2ba81c988f537af771791"
OLD = "artifacts/c5_excess_two_mixed_omission/observations.json"
NEW = "artifacts/c5_excess_two_no_mixed_core44/observations.json"
PRODUCER = "scripts/c5_excess_two_no_mixed_core44.py"
EXPECTED_CORES = {"double_triangle": 64, "path": 56,
                  "triangle_single_run": 160, "triangle_two_runs": 64}
EXPECTED_RESTORATIONS = {"double_triangle": 1024, "path": 458,
                         "triangle_single_run": 1440, "triangle_two_runs": 576}
EXPECTED_DOUBLE_HISTOGRAM = {830: 224, 958: 96, 1016: 224,
                             1020: 96, 1022: 384}


class AuditError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()


def json_digest(data):
    return digest_bytes(json.dumps(data, sort_keys=True, separators=(",", ":"))
                        .encode("utf-8"))


def canonical_colors(colors):
    renaming = {}
    return tuple(renaming.setdefault(c, len(renaming)) for c in colors)


def boundary_rows():
    # Generate the proper C5 partition patterns directly from all 4^5 words.
    rows = {canonical_colors(word) for word in product(range(4), repeat=5)
            if all(word[i] != word[(i + 1) % 5] for i in range(5))}
    require(len(rows) == 10, "proper C5 row count")
    return sorted(rows)


def whole_boundary_orbits(rows):
    # Apply one D5 permutation to the entire ten-row signature, then one
    # global color renaming to each representative. No component action.
    index = {row: i for i, row in enumerate(rows)}
    actions = []
    for sign in (1, -1):
        for shift in range(5):
            actions.append([index[canonical_colors(tuple(
                row[(shift + sign * v) % 5] for v in range(5)))]
                for row in rows])
    require(len({tuple(p) for p in actions}) == 10, "D5 action is faithful")
    for permutation in actions:
        require(sorted(permutation) == list(range(10)), "D5 row permutation")
    return {str(mask): sorted({sum(1 << perm[i] for i in range(10)
                                   if mask & (1 << i)) for perm in actions})
            for mask in (933, 941)}, actions


def edge_set(raw):
    edges = []
    for item in raw:
        require(isinstance(item, list) and len(item) == 2, "edge arity")
        a, b = item
        require(isinstance(a, int) and isinstance(b, int) and a < b,
                "edges must preserve canonical named endpoints")
        edges.append((a, b))
    require(len(set(edges)) == len(edges), "duplicate edge")
    return frozenset(edges)


def components(vertices, edges):
    pending = set(vertices)
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        if a in adjacency and b in adjacency:
            adjacency[a].add(b)
            adjacency[b].add(a)
    result = []
    while pending:
        todo = [min(pending)]
        reached = set(todo)
        while todo:
            v = todo.pop()
            for w in sorted(adjacency[v] - reached):
                reached.add(w)
                todo.append(w)
        pending -= reached
        result.append(sorted(reached))
    return sorted(result)


class Graph:
    """MRV forward checking, initialized with five boundary and two root pins."""

    def __init__(self, order, edges):
        self.order = tuple(order)
        require(self.order == tuple(range(len(order))), "named vertex order")
        self.n = len(order)
        self.edges = edges
        adjacency = [[] for _ in order]
        for a, b in sorted(edges):
            require(0 <= a < b < self.n, "edge outside coloring vertex order")
            adjacency[a].append(b)
            adjacency[b].append(a)
        self.adjacency = tuple(tuple(ns) for ns in adjacency)
        self.pair_queries = 0
        self.search_nodes = 0

    def witness(self, row, roots, pair):
        self.pair_queries += 1
        colors = [-1] * self.n
        for v, c in enumerate(row):
            colors[v] = c
        for v, c in zip(roots, pair):
            if colors[v] >= 0 and colors[v] != c:
                return None
            colors[v] = c
        if any(colors[a] >= 0 and colors[a] == colors[b]
               for a, b in self.edges):
            return None
        domains = [0] * self.n
        for v in self.order:
            if colors[v] < 0:
                allowed = 15
                for w in self.adjacency[v]:
                    if colors[w] >= 0:
                        allowed &= ~(1 << colors[w])
                if not allowed:
                    return None
                domains[v] = allowed

        def search():
            self.search_nodes += 1
            unassigned = [v for v in self.order if colors[v] < 0]
            if not unassigned:
                return tuple(colors)
            v = min(unassigned, key=lambda u: (domains[u].bit_count(),
                                               -len(self.adjacency[u]), u))
            remaining = domains[v]
            while remaining:
                bit = remaining & -remaining
                remaining ^= bit
                colors[v] = bit.bit_length() - 1
                changes = []
                viable = True
                for w in self.adjacency[v]:
                    if colors[w] < 0 and domains[w] & bit:
                        changes.append((w, domains[w]))
                        domains[w] &= ~bit
                        if not domains[w]:
                            viable = False
                            break
                answer = search() if viable else None
                for w, old in changes:
                    domains[w] = old
                colors[v] = -1
                if answer is not None:
                    return answer
            return None

        return search()

    def relation(self, row, roots):
        result = {}
        for pair in product(range(4), repeat=2):
            witness = self.witness(row, roots, pair)
            if witness is not None:
                result[pair] = witness
        return result


def proper_witness(graph, row, roots, pair, witness, context):
    require(len(witness) == graph.n, context + ": coloring length")
    require(all(isinstance(c, int) and 0 <= c < 4 for c in witness),
            context + ": four-color frame")
    require(tuple(witness[:5]) == row, context + ": pinned boundary frame")
    require(tuple(witness[v] for v in roots) == tuple(pair),
            context + ": ordered named root colors")
    require(all(witness[a] != witness[b] for a, b in graph.edges),
            context + ": improper whole-graph edge")


def check_core_row(graph, row, roots, certificate, computed, context):
    pairs = certificate["root_pairs"]
    require(pairs == [list(pair) for pair in sorted(computed)],
            context + ": complete ordered root-pair relation")
    witnesses = certificate["full_coloring_witnesses"]
    require(len(witnesses) == len(pairs), context + ": one witness per pair")
    for pair, witness in zip(pairs, witnesses):
        proper_witness(graph, row, roots, pair, witness, context)


def check_identity(form, inherited):
    require(form["core_edges"] == inherited["edges"], "inherited literal edges")
    require(form["family"] == inherited["family"], "inherited core family")
    require(form["original_root_order"] == inherited["original_root_order"],
            "inherited ordered roots")
    require(form["coloring_vertex_order"] == inherited["witness_vertex_order"],
            "inherited coloring order")
    require(form["original_unary_vertices"] == [piece["vertices"] for piece
            in inherited["original_retained_unaries"]], "inherited unary identities")


def check_structure(form, inherited, graph):
    internal = set(graph.order) - set(range(5))
    roots = tuple(form["original_root_order"])
    require(len(set(roots)) == 2 and set(roots) <= internal, "two named inner roots")
    bridge = tuple(sorted(roots))
    require(bridge in graph.edges, "original root edge retained")
    boundary_edges = frozenset(tuple(sorted((v, (v + 1) % 5))) for v in range(5))
    require(frozenset(e for e in graph.edges if e[1] < 5) == boundary_edges,
            "induced literal boundary C5")
    require(all(len(graph.adjacency[v]) == 4 for v in internal),
            "complete core inner degrees four")
    require(len(components(internal, graph.edges)) == 1, "connected effective interior")
    cut_components = components(internal, graph.edges - {bridge})
    require(len(cut_components) == 2 and not any(set(roots) <= set(side)
                for side in cut_components), "original zw is interior bridge")
    piece_components = components(internal - set(roots), graph.edges)
    require(piece_components == sorted(form["original_unary_vertices"]),
            "no mixed components and complete original unary partition")
    for piece in inherited["original_retained_unaries"]:
        vertices = set(piece["vertices"])
        owners = [r for r in roots if any(v in graph.adjacency[r] for v in vertices)]
        require(len(owners) == 1 and owners == piece["ownership"],
                "original unary ownership")
        attachments = [{"neighbors": [b for b in range(5)
                                      if b in graph.adjacency[v]], "vertex": v}
                       for v in sorted(vertices)]
        require(attachments == piece["boundary_attachments"],
                "actual per-vertex boundary attachments")
        support = sorted({b for item in attachments for b in item["neighbors"]})
        require(support == piece["actual_support"], "same-source actual support")
        contacts = [[v for v in sorted(vertices) if v in graph.adjacency[r]]
                    for r in roots]
        require(contacts == piece["root_contacts"], "ordered original root contacts")
        require([v for side in contacts for v in side] == piece["contact_order"],
                "contact order")
        incident = [list(edge) for edge in sorted(graph.edges)
                    if set(edge) & vertices]
        require(incident == piece["incident_edges"], "original piece incident edges")
    if form["family"] == "double_triangle":
        triangles = [set(t) for t in combinations(sorted(internal), 3)
                     if all(tuple(sorted(e)) in graph.edges for e in combinations(t, 2))]
        require(len(internal) == 6 and len(triangles) == 2 and
                not triangles[0] & triangles[1], "six-point disjoint double triangles")
        require(all(len(t & set(roots)) == 1 for t in triangles),
                "one original root on each triangle")
        require(all(len([b for b in range(5) if b in graph.adjacency[r]]) == 1
                    for r in roots), "double-triangle roots have one original spoke")


def check_restoration_coverage(form, graph):
    roots = tuple(form["original_root_order"])
    expected = set(product(*[[b for b in range(5) if b not in graph.adjacency[r]]
                            for r in roots]))
    observed = []
    for restoration in form["restorations"]:
        spokes = restoration["restored_spokes"]
        require(len(spokes) == 2 and all(len(e) == 2 for e in spokes),
                "two literal restoration spokes")
        require([e[1] for e in spokes] == list(roots),
                "restored spokes preserve original ordered roots")
        observed.append(tuple(e[0] for e in spokes))
    require(len(observed) == len(set(observed)) and set(observed) == expected,
            "exhaustive Cartesian product of every missing named spoke")


def check_indices(restoration, rows, core_rows, restored_relations):
    spokes = restoration["restored_spokes"]
    require(len(restoration["row_pair_indices"]) == 10,
            "restoration has complete ten-row fibre index list")
    for i, (row, certificate, actual) in enumerate(zip(rows, core_rows,
                                                       restored_relations)):
        indices = [j for j, (a, b) in enumerate(certificate["root_pairs"])
                   if a != row[spokes[0][0]] and b != row[spokes[1][0]]]
        require(restoration["row_pair_indices"][i] == indices,
                "literal restored spoke row_pair_indices")
        indexed = {tuple(certificate["root_pairs"][j]) for j in indices}
        require(indexed == set(actual), "fresh restored-graph relation equals indexed fibre")
    mask = sum(1 << i for i, relation in enumerate(restored_relations) if relation)
    require(restoration["sigma"] == mask, "complete restored ten-row Sigma")
    return mask


def reject_control(name, action):
    try:
        action()
    except AuditError as error:
        return {"name": name, "classification": "triggered and holds",
                "mutation_rejected": True, "rejection": str(error)}
    raise AuditError("corruption control failed to reject: " + name)


def run(root):
    head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()
    require(head == CANDIDATE, "frozen candidate HEAD")
    raw_inputs = {name: (root / name).read_bytes() for name in (OLD, NEW, PRODUCER)}
    hashes = {name: digest_bytes(raw) for name, raw in raw_inputs.items()}
    old, new = (json.loads(raw_inputs[name]) for name in (OLD, NEW))
    require(new["source_sha256"] == {name: hashes[name] for name in (OLD, PRODUCER)},
            "new certificate exact inherited input/producer byte hashes")
    rows = boundary_rows()
    require(new["pattern_order"] == [list(row) for row in rows] == old["pattern_order"],
            "independently generated complete canonical boundary row order")
    target_orbits, actions = whole_boundary_orbits(rows)
    require(target_orbits == new["target_D5_orbits"] == old["target_D5_orbits"],
            "independent whole-boundary D5 target orbits")
    targets = {mask for orbit in target_orbits.values() for mask in orbit}
    forms = new["forms"]
    inherited_forms = old["original_marked_cores"]
    require(len(forms) == len(inherited_forms) == 344, "all inherited 344 cores")
    require([f["input_form_id"] for f in forms] == list(range(344)),
            "exact inherited core ID coverage and order")
    totals = Counter()
    family_cores = Counter()
    family_restorations = Counter()
    histogram = Counter()
    double_histogram = Counter()
    per_form = []
    controls = []
    control_done = set()
    for fi, form in enumerate(forms):
        inherited = inherited_forms[fi]
        check_identity(form, inherited)
        graph = Graph(form["coloring_vertex_order"], edge_set(form["core_edges"]))
        check_structure(form, inherited, graph)
        check_restoration_coverage(form, graph)
        roots = tuple(form["original_root_order"])
        require(len(form["core_rows"]) == 10, "complete core ten-row certificate")
        relations = []
        for ri, row in enumerate(rows):
            actual = graph.relation(row, roots)
            relations.append(actual)
            check_core_row(graph, row, roots, form["core_rows"][ri], actual,
                           f"core {fi} row {ri}")
            require(inherited["rows"][ri]["original_bridge_retained_pairs"] ==
                    [list(pair) for pair in sorted(actual)],
                    f"inherited full retained-bridge relation {fi}/{ri}")
            totals["independent_core_row_queries"] += 1
            totals["core_root_pairs"] += len(actual)
            totals["certificate_core_witnesses_checked"] += len(actual)
            totals["empty_core_fibres"] += not actual
            if actual and "pair_omission" not in control_done:
                mutated = deepcopy(form["core_rows"][ri])
                mutated["root_pairs"].pop()
                mutated["full_coloring_witnesses"].pop()
                controls.append(reject_control("drop one genuine ordered pair", lambda:
                    check_core_row(graph, row, roots, mutated, actual, "pair omission control")))
                control_done.add("pair_omission")
                mutated = deepcopy(form["core_rows"][ri])
                # Corrupt an unpinned interior vertex so the boundary frame
                # and declared ordered root pair stay intact; the literal
                # whole-graph edge check must detect this mutation.
                a, b = next((a, b) for a, b in sorted(graph.edges)
                            if b >= 5 and b not in roots)
                mutated["full_coloring_witnesses"][0][b] = mutated["full_coloring_witnesses"][0][a]
                controls.append(reject_control("corrupt whole-graph witness", lambda:
                    check_core_row(graph, row, roots, mutated, actual, "witness control")))
                control_done.add("witness")
            if not actual and "empty_fibre" not in control_done:
                mutated = {"root_pairs": [[0, 1]], "full_coloring_witnesses": [[0] * graph.n]}
                controls.append(reject_control("forge a pair in a genuinely empty core fibre", lambda:
                    check_core_row(graph, row, roots, mutated, actual, "empty-fibre control")))
                control_done.add("empty_fibre")
        require(sum(1 << i for i, relation in enumerate(relations) if relation) ==
                inherited["sigma"] == 1022, "core complete Sigma=1022")
        # Inherited q-critical witnesses are checked against each literal
        # edge-deleted whole graph; these are certificates, not solver logic.
        qcerts = inherited["q4_critical_witnesses"]
        nonboundary = sorted(e for e in graph.edges if e[1] >= 5)
        require([tuple(c["edge"]) for c in qcerts] == nonboundary,
                "every nonboundary q-critical edge certificate")
        for cert in qcerts:
            deletion = Graph(graph.order, graph.edges - {tuple(cert["edge"])})
            witness = cert["coloring"]
            proper_witness(deletion, rows[0], roots, tuple(witness[r] for r in roots),
                           witness, "inherited q-critical deleted-edge witness")
            totals["inherited_q_critical_witnesses_checked"] += 1
        restored_digest_data = []
        for restoration in form["restorations"]:
            spokes = edge_set(restoration["restored_spokes"])
            require(not spokes & graph.edges, "two genuinely absent core spokes")
            restored = Graph(graph.order, graph.edges | spokes)
            require(all(len(restored.adjacency[v]) == (5 if v in roots else 4)
                        for v in graph.order if v >= 5), "literal restored degree-five roots")
            restored_relations = []
            for ri, row in enumerate(rows):
                actual = restored.relation(row, roots)
                restored_relations.append(actual)
                totals["independent_restored_row_queries"] += 1
                totals["restored_root_pairs"] += len(actual)
                totals["empty_restored_fibres"] += not actual
                for pair, witness in actual.items():
                    proper_witness(restored, row, roots, pair, witness,
                                   "fresh pinned-root restored witness")
                    totals["fresh_restored_witnesses_checked"] += 1
                for j in restoration["row_pair_indices"][ri]:
                    require(isinstance(j, int) and 0 <= j < len(form["core_rows"][ri]["root_pairs"]),
                            "row-pair witness index in bounds")
                    certificate = form["core_rows"][ri]
                    proper_witness(restored, row, roots, certificate["root_pairs"][j],
                                   certificate["full_coloring_witnesses"][j],
                                   "indexed original whole-graph restored witness")
                    totals["indexed_restored_witnesses_checked"] += 1
            sigma = check_indices(restoration, rows, form["core_rows"], restored_relations)
            require(sigma not in targets, f"target intersection at core {fi} literal spokes {sorted(spokes)}")
            histogram[sigma] += 1
            family_restorations[form["family"]] += 1
            totals["restorations"] += 1
            if form["family"] == "double_triangle":
                double_histogram[sigma] += 1
            totals["pinned_root_pair_queries"] += restored.pair_queries
            totals["MRV_search_nodes"] += restored.search_nodes
            restored_digest_data.append({"spokes": restoration["restored_spokes"],
                "pairs": [[list(p) for p in sorted(r)] for r in restored_relations], "sigma": sigma})
            if "indices" not in control_done and any(restoration["row_pair_indices"]):
                mutated = deepcopy(restoration)
                next(f for f in mutated["row_pair_indices"] if f).pop()
                controls.append(reject_control("omit a surviving restoration pair index", lambda:
                    check_indices(mutated, rows, form["core_rows"], restored_relations)))
                control_done.add("indices")
            if "restored_empty" not in control_done and any(not r for r in restored_relations):
                mutated = deepcopy(restoration)
                i = next(i for i, r in enumerate(restored_relations) if not r)
                mutated["row_pair_indices"][i] = [0]
                controls.append(reject_control("forge surviving index in empty restored fibre", lambda:
                    check_indices(mutated, rows, form["core_rows"], restored_relations)))
                control_done.add("restored_empty")
        totals["pinned_root_pair_queries"] += graph.pair_queries
        totals["MRV_search_nodes"] += graph.search_nodes
        family_cores[form["family"]] += 1
        totals["cores"] += 1
        per_form.append({"input_form_id": fi, "family": form["family"],
            "named_graph_sha256": json_digest({"edges": form["core_edges"], "roots": roots,
                                                   "unaries": form["original_unary_vertices"]}),
            "complete_core_root_pair_sha256": json_digest([[list(p) for p in sorted(r)]
                                                            for r in relations]),
            "complete_restored_root_pair_sha256": json_digest(restored_digest_data),
            "restorations": len(form["restorations"])})
    require(dict(family_cores) == EXPECTED_CORES, "family core counts")
    require(dict(family_restorations) == EXPECTED_RESTORATIONS, "family restoration counts")
    require(dict(double_histogram) == EXPECTED_DOUBLE_HISTOGRAM, "1024 double-triangle Sigma histogram")
    expected_summary = {"cores": totals["cores"], "restorations": totals["restorations"],
        "family_core_counts": dict(family_cores), "family_restoration_counts": dict(family_restorations),
        "independent_restored_row_checks": totals["independent_restored_row_queries"],
        "sigma_histogram": {str(k): v for k, v in sorted(histogram.items())}, "target_hits": 0,
        "graph_census": False, "source_realizability_claimed": False, "new_lean_theorem": False}
    require(new["summary"] == expected_summary, "all new finite summary fields")
    mutated = deepcopy(forms[0])
    mutated["restorations"].pop()
    graph = Graph(mutated["coloring_vertex_order"], edge_set(mutated["core_edges"]))
    controls.append(reject_control("omit one literal restoration graph", lambda:
                                  check_restoration_coverage(mutated, graph)))
    mutated = deepcopy(forms[0])
    mutated["core_edges"].pop()
    controls.append(reject_control("remove a literal original graph edge", lambda:
                                  check_identity(mutated, inherited_forms[0])))
    altered_orbits = deepcopy(new["target_D5_orbits"])
    altered_orbits["941"].pop()
    controls.append(reject_control("drop a whole-graph target orbit member", lambda:
        require(altered_orbits == whole_boundary_orbits(rows)[0], "independent target orbit mismatch")))
    # Small positive/negative solver controls are decided without certificates.
    cycle = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in range(5))
    positive = Graph(range(7), cycle | {(0, 5), (5, 6)})
    relation = positive.relation(rows[0], (5, 6))
    require(set(relation) == {(a, b) for a in range(4) for b in range(4)
                             if a != rows[0][0] and a != b}, "positive solver control")
    obstruction = Graph(range(7), cycle | {(0, 5), (1, 5), (4, 5), (5, 6),
                                         (0, 6), (1, 6), (4, 6)})
    require(not obstruction.relation(rows[0], (5, 6)), "negative pinned-root solver control")
    controls.extend([
        {"name": "small explicit positive graph with full ordered relation",
         "classification": "triggered and holds", "pairs": len(relation)},
        {"name": "small explicit three-color-forced adjacent roots contradiction",
         "classification": "triggered and holds", "pairs": 0},
        {"name": "complete source premise Sigma933/941 with disk and criticality",
         "classification": "not triggered", "reason": "All restored graphs are the relaxed necessary finite domain. Zero target hits provides no source-realizability positive control."},
        {"name": "arbitrary-size core to finite normal-form relation preservation",
         "classification": "not triggered", "reason": "Paper dependency; no finite run proves arbitrary-size coverage."},
        {"name": "upstream finite topology/NetworkX enumeration completeness",
         "classification": "not triggered", "reason": "Inherited enumeration trust boundary; no independent topology oracle used."}])
    hashes_after = {name: digest_bytes((root / name).read_bytes()) for name in raw_inputs}
    require(hashes_after == hashes, "immutable input zero-byte drift during audit")
    return {"schema": 1, "candidate_sha": CANDIDATE, "input_sha256": hashes,
        "input_sizes": {name: len(raw) for name, raw in raw_inputs.items()},
        "input_zero_byte_drift": True,
        "independent_checker_sha256": digest_bytes(Path(__file__).read_bytes()),
        "solver": "Pinned all 16 ordered root-color pairs; MRV forward checking on literal whole graph; fresh existential search for every core/restored row.",
        "pattern_order": [list(row) for row in rows], "whole_graph_D5_row_permutations": actions,
        "target_D5_orbits": target_orbits, "target_intersection": [],
        "counts": dict(sorted(totals.items())),
        "family_core_counts": dict(sorted(family_cores.items())),
        "family_restoration_counts": dict(sorted(family_restorations.items())),
        "sigma_histogram": {str(k): v for k, v in sorted(histogram.items())},
        "double_triangle_sigma_histogram": {str(k): v for k, v in sorted(double_histogram.items())},
        "controls": controls, "per_form": per_form,
        "classification": "triggered and holds",
        "scope": "Finite necessary domain only: 344 exact inherited marked graphs, every 3498 literal two-spoke restoration, complete ten-row ordered root-pair relations and whole-graph witnesses. Arbitrary-size coverage is a separate paper audit; topology, source realization, general theorem, Lean theorem and U2-U4 are not established by this program."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = run(args.root.resolve())
    except (AuditError, KeyError, ValueError, OSError) as error:
        print("M2 independent finite audit FAILED:", error)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("M2 independent finite audit: triggered and holds")
    print(json.dumps(result["counts"], sort_keys=True))
    print("Double-triangle histogram:", json.dumps(result["double_triangle_sigma_histogram"], sort_keys=True))
    print("Input zero-byte drift: true; target intersection: []")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
