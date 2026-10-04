#!/usr/bin/env python3
"""Replay the 20 archived witnesses and exhaust small effective C5 disks.

The frame is literally ordered 0..4. Isolated private vertices are excluded,
as clarified by the user; no D5 quotient or independent colour normalisation
is applied. --check recomputes the whole saved finite search without writes.
NetworkX 3.5 is required. Optional rustworkx accelerates planarity decisions;
every saved witness is independently checked with NetworkX and backtracking.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import random

import networkx as nx

try:
    import rustworkx as rx
except ImportError:
    rx = None

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/c5_cells/cells.json"
OUT = ROOT / "artifacts/c5_excess_rejection_law/observations.json"
FRAME = tuple(range(5))
CYCLE = tuple(sorted(tuple(sorted((i, (i + 1) % 5))) for i in FRAME))
T4_INDICES = (2, 5, 7, 8, 9)
T4 = sum(1 << i for i in T4_INDICES)
OMEGA = (1 << 10) - 1


def normalise(row):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in row)


PATTERNS = tuple(sorted({normalise(row) for row in product(range(4), repeat=5)
                         if all(row[u] != row[v] for u, v in CYCLE)}))
THREE = tuple(i for i, p in enumerate(PATTERNS) if len(set(p)) == 3)
SINGLETON = {i: next(v for v in FRAME if PATTERNS[i].count(PATTERNS[i][v]) == 1)
             for i in THREE}
assert len(PATTERNS) == 10
assert tuple(i for i, p in enumerate(PATTERNS) if len(set(p)) == 4) == T4_INDICES


def profile(mask):
    q = sorted(SINGLETON[i] for i in THREE if not mask >> i & 1)
    e = sum(u in q and v in q for u, v in CYCLE)
    c = len(q) - e if 0 < len(q) < 5 else int(bool(q))
    bound = 2 * len(q) - e - 2
    if len(q) == 1:
        shape = "singleton"
    elif len(q) == 2:
        shape = "adjacent_pair" if e else "nonadjacent_pair"
    elif len(q) == 3:
        shape = "three_vertex_arc" if c == 1 else "pair_plus_singleton"
    elif len(q) == 4:
        shape = "four_vertex_arc"
    else:
        shape = "outside_conjecture"
    return dict(Q=q, c=c, e=e, lower_bound=bound, shape=shape)


def private_vertices(edges):
    return tuple(sorted({v for edge in edges for v in edge if v >= 5}))


def degrees(edges):
    count = Counter(v for edge in CYCLE + tuple(edges) for v in edge)
    return {v: count[v] for v in FRAME + private_vertices(edges)}


def epsilon(edges):
    d = degrees(edges)
    return sum(d[v] - 4 for v in private_vertices(edges))


@lru_cache(maxsize=None)
def extension(edges, pattern_index):
    """Independent MRV backtracking in one shared literal four-colour frame."""
    verts = FRAME + private_vertices(edges)
    adjacency = {v: set() for v in verts}
    for u, v in CYCLE + edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    colours = dict(zip(FRAME, PATTERNS[pattern_index]))
    if any(colours[u] == colours[v] for u, v in edges if u < 5 and v < 5):
        return None

    def visit():
        choices = []
        for v in verts:
            if v in colours:
                continue
            forbidden = {colours[w] for w in adjacency[v] if w in colours}
            allowed = tuple(c for c in range(4) if c not in forbidden)
            if not allowed:
                return None
            choices.append((len(allowed), -len(adjacency[v]), v, allowed))
        if not choices:
            return tuple(colours[v] for v in verts)
        _, _, v, allowed = min(choices)
        for colour in allowed:
            colours[v] = colour
            result = visit()
            if result is not None:
                del colours[v]
                return result
        del colours[v]
        return None

    return visit()


def sigma(edges):
    return sum(1 << i for i in range(10) if extension(edges, i) is not None)


def disk_embedding(edges):
    """Cone the entire frame into the exterior; planarity forces a disk side."""
    apex = max(FRAME + private_vertices(edges)) + 1
    graph = nx.Graph()
    graph.add_nodes_from(FRAME + private_vertices(edges) + (apex,))
    graph.add_edges_from(CYCLE + edges + tuple((v, apex) for v in FRAME))
    planar, embedding = nx.check_planarity(graph)
    if not planar:
        return None
    embedding.check_structure()
    rotations = {v: [w for w in embedding.neighbors_cw_order(v) if w != apex]
                 for v in FRAME + private_vertices(edges)}
    plane = nx.PlanarEmbedding()
    plane.set_data(rotations)
    plane.check_structure()
    face = None
    for u, v in CYCLE:
        for a, b in ((u, v), (v, u)):
            walk = plane.traverse_face(a, b)
            if len(walk) == 5 and set(walk) == set(FRAME):
                face = walk
                break
        if face is not None:
            break
    assert face is not None, "boundary apex must leave a C5 face"
    return dict(apex=apex, apex_rotation=list(embedding.neighbors_cw_order(apex)),
                disk_rotation={str(v): rotations[v] for v in sorted(rotations)},
                outer_face=face)


def graph_certificate(edges, expected=None):
    edges = tuple(sorted(tuple(sorted(e)) for e in edges))
    assert len(edges) == len(set(edges))
    assert all(u != v and not (u < 5 and v < 5) for u, v in edges)
    mask = sigma(edges)
    assert expected is None or mask == expected
    assert mask & T4 == T4 and 1 <= len(profile(mask)["Q"]) <= 4
    d = degrees(edges)
    assert all(d[v] >= 4 for v in private_vertices(edges))
    embedding = disk_embedding(edges)
    assert embedding is not None
    critical = []
    for e in edges:
        deleted = tuple(f for f in edges if f != e)
        new_mask = sigma(deleted)
        assert new_mask | mask == new_mask and new_mask != mask
        new_indices = [i for i in range(10) if new_mask >> i & 1 and not mask >> i & 1]
        i = new_indices[0]
        verts = FRAME + private_vertices(deleted)
        colours = extension(deleted, i)
        colouring = dict(zip(verts, colours))
        # An isolated endpoint after deletion can be assigned its other endpoint's colour.
        for v in private_vertices(edges):
            if v not in colouring:
                colouring[v] = colouring[e[0] if v == e[1] else e[1]]
        assert colouring[e[0]] == colouring[e[1]]
        assert all(colouring[u] != colouring[v] for u, v in CYCLE + deleted)
        critical.append(dict(edge=list(e), sigma_after_deletion=new_mask,
                             newly_accepted_indices=new_indices, pattern_index=i,
                             pattern=list(PATTERNS[i]),
                             colouring={str(v): colouring[v] for v in sorted(colouring)}))
    return dict(vertices=list(FRAME + private_vertices(edges)), frame=list(FRAME),
                frame_edges=[list(e) for e in CYCLE], nonframe_edges=[list(e) for e in edges],
                all_edges=[list(e) for e in sorted(CYCLE + edges)], sigma_mask=mask,
                sigma_indices=[i for i in range(10) if mask >> i & 1],
                sigma_ordered_rows=[list(PATTERNS[i]) for i in range(10) if mask >> i & 1],
                accepted_colourings={str(i): {str(v): c for v, c in
                                            zip(FRAME + private_vertices(edges), extension(edges, i))}
                                      for i in range(10) if mask >> i & 1},
                degrees={str(v): d[v] for v in sorted(d)},
                private_degree_sequence=sorted(d[v] for v in private_vertices(edges)),
                epsilon=epsilon(edges), **profile(mask), embedding=embedding,
                critical_edges=critical)


def scratch(cells, trials, seed):
    records = []
    for text, cell in sorted(cells.items(), key=lambda item: int(item[0])):
        mask = int(text)
        if mask & T4 != T4 or not profile(mask)["Q"]:
            continue
        original = tuple(sorted(tuple(sorted(e)) for e in cell["edges"]))
        assert len(private_vertices(original)) == cell["k_eff"]
        assert sigma(original) == mask
        outcomes = Counter()
        best = None
        for trial in range(trials):
            order = list(original)
            random.Random(seed + trial).shuffle(order)
            kept = original
            for e in order:
                removed = tuple(f for f in kept if f != e)
                if sigma(removed) == mask:
                    kept = removed
            d = degrees(kept)
            key = (epsilon(kept), tuple(sorted(d[v] for v in private_vertices(kept))), kept)
            outcomes[key] += 1
            if best is None or key < best:
                best = key
            if key[0] < profile(mask)["lower_bound"]:
                return records, graph_certificate(kept, mask)
        cert = graph_certificate(best[2], mask)
        records.append(dict(source_mask=mask, original_edges=[list(e) for e in original],
                            trials=trials, minimum_epsilon=best[0],
                            distinct_outcomes=len(outcomes),
                            outcomes=[dict(epsilon=k[0], private_degree_sequence=list(k[1]),
                                           edges=[list(e) for e in k[2]], count=n)
                                      for k, n in sorted(outcomes.items())],
                            witness=cert))
        print(f"scratch mask={mask} Q={cert['Q']} min_epsilon={best[0]} "
              f"degrees={cert['private_degree_sequence']} outcomes={len(outcomes)}", flush=True)
    assert len(records) == 20
    return records, None


def interior_templates(k):
    """Exhaust 2^(k choose 2) labelled interiors, quotient only private labels."""
    universe = tuple(combinations(range(k), 2))
    index = {e: i for i, e in enumerate(universe)}
    perm_maps = [tuple(1 << index[tuple(sorted((p[u], p[v])))] for u, v in universe)
                 for p in permutations(range(k))]
    templates = []
    for mask in range(1 << len(universe)):
        indices = tuple(i for i in range(len(universe)) if mask >> i & 1)
        edges = tuple(universe[i] for i in indices)
        d = [0] * k
        for u, v in edges:
            d[u] += 1
            d[v] += 1
        if not all(d):  # degree >=4 and at most three spokes imply deg_H >=1
            continue
        if any(sum(mapping[i] for i in indices) < mask for mapping in perm_maps):
            continue
        autos = [p for p, mapping in zip(permutations(range(k)), perm_maps)
                 if sum(mapping[i] for i in indices) == mask]
        templates.append((mask, edges, d, autos))
    return templates


def colouring_tables(k):
    assignments = tuple(product(range(4), repeat=k))
    full = (1 << len(assignments)) - 1
    edges = tuple((b, 5 + v) for v in range(k) for b in FRAME) + tuple(
        (5 + u, 5 + v) for u, v in combinations(range(k), 2))
    tables = {}
    for u, v in edges:
        if u >= 5:
            allowed = sum(1 << j for j, a in enumerate(assignments) if a[u - 5] != a[v - 5])
            tables[(u, v)] = (allowed,) * 10
        else:
            tables[(u, v)] = tuple(sum(1 << j for j, a in enumerate(assignments)
                                        if p[u] != a[v - 5]) for p in PATTERNS)
    support_tables = {}
    for v in range(k):
        for support in range(1 << 5):
            rows = [full] * 10
            for b in FRAME:
                if support >> b & 1:
                    rows = [a & z for a, z in zip(rows, tables[(b, 5 + v)])]
            support_tables[(v, support)] = tuple(rows)
    return full, tables, support_tables


def edge_minimal(edges, mask, full, tables):
    """A missing row is gained iff all constraints except one have a solution."""
    critical = 0
    target = (1 << len(edges)) - 1
    for row in THREE:
        if mask >> row & 1:
            continue
        prefix = [full]
        for e in edges:
            prefix.append(prefix[-1] & tables[e][row])
        suffix = full
        for i in range(len(edges) - 1, -1, -1):
            if prefix[i] & suffix:
                critical |= 1 << i
            suffix &= tables[edges[i]][row]
        if critical == target:
            return True
    return False


def fast_disk(edges, k):
    apex = 5 + k
    augmented = CYCLE + edges + tuple((v, apex) for v in FRAME)
    if rx is not None:
        graph = rx.PyGraph(multigraph=False)
        graph.add_nodes_from(range(apex + 1))
        graph.add_edges_from_no_data(augmented)
        return rx.is_planar(graph)
    graph = nx.Graph()
    graph.add_nodes_from(range(apex + 1))
    graph.add_edges_from(augmented)
    return nx.check_planarity(graph)[0]


def search_level(k):
    full, tables, support_tables = colouring_tables(k)
    stats = Counter()
    by_mask = Counter()
    histograms = {}
    best = {}
    digest = sha256()
    template_records = []
    for hmask, hedge, hd, autos in interior_templates(k):
        choices = [tuple(s for s in range(32) if max(0, 4 - d) <= s.bit_count() <= 3)
                   for d in hd]
        h_edges = tuple((5 + u, 5 + v) for u, v in hedge)
        h_allowed = full
        for e in h_edges:
            h_allowed &= tables[e][0]
        budget = 3 * k + 2 - len(h_edges)
        # suffix[i][b] counts ALL attachment completions of total size <= b.
        suffix = [[1] * (budget + 1) for _ in range(k + 1)]
        for depth in range(k - 1, -1, -1):
            suffix[depth] = [sum(suffix[depth + 1][b - s.bit_count()]
                                 for s in choices[depth] if s.bit_count() <= b)
                             for b in range(budget + 1)]
        domain = suffix[0][budget]
        stats["degree_and_edge_bound_candidates"] += domain
        template_records.append(dict(interior_mask=hmask, interior_edges=[list(e) for e in h_edges],
                                     degrees_H=hd, automorphism_count=len(autos),
                                     bounded_attachment_candidates=domain))
        supports = []

        def visit(depth, remaining, rows):
            if depth == k:
                stats["T4_attachment_leaves"] += 1
                mask = sum(1 << i for i, a in enumerate(rows) if a)
                if mask == OMEGA:
                    stats["all_rows_accepted"] += 1
                    return None
                if len(profile(mask)["Q"]) == 5:
                    stats["outside_conjecture_T4_only_leaves"] += 1
                    return None
                stats["nonempty_Q_leaves"] += 1
                a = tuple(supports)
                if any(tuple(a[p[v]] for v in range(k)) < a for p in autos):
                    stats["private_automorphism_duplicates"] += 1
                    return None
                stats["nonempty_Q_private_orbits"] += 1
                edges = tuple(sorted(h_edges + tuple((b, 5 + v) for v, s in enumerate(a)
                                                      for b in FRAME if s >> b & 1)))
                if not edge_minimal(edges, mask, full, tables):
                    stats["noncritical_orbits"] += 1
                    return None
                stats["critical_orbits_before_disk"] += 1
                if not fast_disk(edges, k):
                    stats["non_disk_critical_orbits"] += 1
                    return None
                stats["qualifying_disk_orbits"] += 1
                by_mask[mask] += 1
                eps = sum(hd) + sum(s.bit_count() for s in a) - 4 * k
                p = profile(mask)
                assert 1 <= len(p["Q"]) <= 4
                histograms.setdefault(p["shape"], Counter())[eps] += 1
                digest.update(json.dumps([k, edges, mask, eps], separators=(",", ":")).encode() + b"\n")
                key = (eps, edges)
                if mask not in best or key < best[mask]:
                    best[mask] = key
                if eps < p["lower_bound"]:
                    return graph_certificate(edges, mask)
                return None
            for s in choices[depth]:
                size = s.bit_count()
                if size > remaining:
                    continue
                count = suffix[depth + 1][remaining - size]
                if count == 0:
                    continue
                new_rows = tuple(a & b for a, b in zip(rows, support_tables[(depth, s)]))
                if any(not new_rows[i] for i in T4_INDICES):
                    stats["T4_pruned_bounded_completions"] += count
                    continue
                supports.append(s)
                counterexample = visit(depth + 1, remaining - size, new_rows)
                supports.pop()
                if counterexample is not None:
                    return counterexample
            return None

        counterexample = visit(0, budget, (h_allowed,) * 10)
        print(f"k={k} H={hmask} candidates={domain} "
              f"T4_leaves={stats['T4_attachment_leaves']} "
              f"disk_minimal={stats['qualifying_disk_orbits']}", flush=True)
        if counterexample is not None:
            return dict(k=k, complete=False, stats=dict(sorted(stats.items())),
                        counterexample=counterexample), counterexample
    assert stats["T4_attachment_leaves"] + stats["T4_pruned_bounded_completions"] == stats[
        "degree_and_edge_bound_candidates"]
    assert (stats["all_rows_accepted"] + stats["outside_conjecture_T4_only_leaves"]
            + stats["nonempty_Q_leaves"] == stats["T4_attachment_leaves"])
    assert stats["private_automorphism_duplicates"] + stats["nonempty_Q_private_orbits"] == stats[
        "nonempty_Q_leaves"]
    assert stats["noncritical_orbits"] + stats["critical_orbits_before_disk"] == stats[
        "nonempty_Q_private_orbits"]
    assert stats["qualifying_disk_orbits"] + stats["non_disk_critical_orbits"] == stats[
        "critical_orbits_before_disk"]
    result = dict(k=k, complete=True, raw_induced_edge_subsets=1 << (5 * k + k * (k - 1) // 2),
                  labelled_interior_subsets=1 << (k * (k - 1) // 2),
                  templates=template_records, stats=dict(sorted(stats.items())),
                  counts_by_sigma={str(m): n for m, n in sorted(by_mask.items())},
                  epsilon_histograms={shape: {str(e): n for e, n in sorted(h.items())}
                                      for shape, h in sorted(histograms.items())},
                  qualifying_graph_stream_sha256=digest.hexdigest(),
                  minima_by_sigma={str(m): graph_certificate(value[1], m)
                                   for m, value in sorted(best.items())})
    return result, None


def build(max_k, trials, seed):
    assert nx.__version__ == "3.5", "use NetworkX 3.5 for reproducible embeddings"
    source = SOURCE.read_bytes()
    catalogue = json.loads(source)
    assert catalogue["pattern_order"] == [list(p) for p in PATTERNS]
    assert catalogue["singleton_of_three_colour"] == {str(i): v for i, v in SINGLETON.items()}
    records, counterexample = scratch(catalogue["cells"], trials, seed)
    levels = []
    if counterexample is None:
        for k in range(1, max_k + 1):
            result, counterexample = search_level(k)
            levels.append(result)
            if counterexample is not None:
                break
    return dict(schema_version=1, task="E1", base_commit="ca3870f9b79684c2100480d0dc04523899666928",
                effective_interior=True, isolated_private_vertices="excluded_by_user_clarification",
                configuration=dict(max_k=max_k, greedy_trials=trials, seed=seed),
                source=dict(path=str(SOURCE.relative_to(ROOT)), sha256=sha256(source).hexdigest()),
                pattern_order=[list(p) for p in PATTERNS], T4_indices=list(T4_INDICES), T4_mask=T4,
                singleton_of_three_colour={str(i): v for i, v in SINGLETON.items()},
                evidence="Python finite-domain certificate; no arbitrary-size E proof or Lean theorem",
                scratch=records, exhaustive=levels, counterexample=counterexample,
                result="counterexample" if counterexample is not None else "no_counterexample_in_finite_domain")


def summary(data):
    print(f"result={data['result']} scratch_classes={len(data['scratch'])}")
    for level in data["exhaustive"]:
        print(f"k={level['k']} complete={level['complete']} stats={level['stats']}")
        print(f"epsilon_histograms={level.get('epsilon_histograms', {})}")


def audit_raw_k3(stored):
    """Independent raw-edge audit: no H/spoke/orbit/prefix search pruning."""
    k = 3
    full, tables, _ = colouring_tables(k)
    universe = tuple(tables)
    stats = Counter()
    seen = {}
    for bits in range(1 << len(universe)):
        edges = tuple(sorted(e for i, e in enumerate(universe) if bits >> i & 1))
        if len(edges) > 3 * k + 2:
            continue
        d = Counter(v for e in edges for v in e)
        if any(d[v] < 4 for v in range(5, 5 + k)):
            continue
        stats["degree_and_edge_bound_labelled"] += 1
        rows = [full] * 10
        for e in edges:
            rows = [a & b for a, b in zip(rows, tables[e])]
        mask = sum(1 << i for i, a in enumerate(rows) if a)
        # MRV is independent of the assignment-bitset calculation.
        assert mask == sigma(edges)
        if mask & T4 != T4 or not 1 <= len(profile(mask)["Q"]) <= 4:
            continue
        if not all(sigma(tuple(f for f in edges if f != e)) != mask for e in edges):
            continue
        stats["critical_labelled"] += 1
        graph = nx.Graph(CYCLE + edges + tuple((v, 5 + k) for v in FRAME))
        if not nx.check_planarity(graph)[0]:
            continue
        stats["disk_labelled"] += 1
        representatives = []
        for perm in permutations(range(k)):
            names = {5 + v: 5 + perm[v] for v in range(k)}
            representatives.append(tuple(sorted(tuple(sorted((names.get(u, u), names.get(v, v))))
                                                for u, v in edges)))
        canonical = min(representatives)
        seen[canonical] = mask
    by_mask = Counter(seen.values())
    histograms = {}
    for edges, mask in seen.items():
        histograms.setdefault(profile(mask)["shape"], Counter())[epsilon(edges)] += 1
    expected = next(level for level in stored["exhaustive"] if level["k"] == k)
    assert expected["complete"]
    assert {str(m): n for m, n in sorted(by_mask.items())} == expected["counts_by_sigma"]
    assert {shape: {str(e): n for e, n in sorted(h.items())}
            for shape, h in sorted(histograms.items())} == expected["epsilon_histograms"]
    print(f"RAW K3 AUDIT OK: subsets={1 << len(universe)} stats={dict(stats)} "
          f"private_orbits={len(seen)}; all candidate Sigma/backtracking and counts agree")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="recompute saved search; do not write")
    mode.add_argument("--audit-k3", action="store_true", help="independent raw-edge k=3 audit; do not write")
    parser.add_argument("--max-k", type=int, choices=range(1, 6), default=4)
    parser.add_argument("--greedy-trials", type=int, default=40)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    if args.greedy_trials < 1:
        parser.error("--greedy-trials must be positive")
    if args.audit_k3:
        stored = json.loads(args.output.read_text())
        if stored["configuration"]["max_k"] < 3:
            parser.error("--audit-k3 requires a saved complete level k=3")
        audit_raw_k3(stored)
    elif args.check:
        stored = json.loads(args.output.read_text())
        c = stored["configuration"]
        result = build(c["max_k"], c["greedy_trials"], c["seed"])
        assert result == stored, "recomputed finite certificate differs from saved artifact"
        summary(result)
        print("CHECK OK: exact artifact replay; NetworkX/backtracking witnesses verified")
    else:
        if args.output.exists():
            parser.error(f"refusing to overwrite existing artifact: {args.output}")
        result = build(args.max_k, args.greedy_trials, args.seed)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x") as f:
            f.write(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        summary(result)
        print(f"wrote {args.output.relative_to(ROOT) if args.output.is_relative_to(ROOT) else args.output}")


if __name__ == "__main__":
    main()
