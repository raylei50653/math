#!/usr/bin/env python3
"""Independent D9 E6 audit, no imports from repository decision code.

Only original graph edge/rotation data is read from ES. All colourings, full
relations, pieces, faces, shields, criticality and minimal cores are recomputed.
Standard library only; never calls a four-colour-theorem oracle.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
B = frozenset(range(5))
BEDGES = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in B)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def canonical(seq):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in seq)


ROWS = tuple(sorted({canonical(c) for c in itertools.product(range(4), repeat=5)
                     if all(c[i] != c[(i + 1) % 5] for i in B)}))
QROWS = {i: ROWS.index(tuple(map(int, q))) for i, q in
         enumerate(("01212", "01202", "01201", "01021", "01012"))}
T4ROWS = frozenset(i for i, q in enumerate(ROWS) if len(set(q)) == 4)


def adjacency(edges, vertices=None):
    if vertices is None:
        vertices = set(itertools.chain.from_iterable(edges))
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def components(vertices, edges):
    adj = adjacency(edges, vertices)
    unseen = set(vertices)
    parts = []
    while unseen:
        start = min(unseen)
        todo, comp = [start], set()
        unseen.remove(start)
        while todo:
            u = todo.pop()
            comp.add(u)
            for v in sorted(adj[u] & unseen):
                unseen.remove(v)
                todo.append(v)
        parts.append(tuple(sorted(comp)))
    return parts


def connected(vertices, edges):
    return bool(vertices) and len(components(vertices, edges)) == 1


def colourings(edges, fixed, vertices=None):
    """Independent exact DFS with MRV; return full vertex-labelled assignments."""
    adj = adjacency(edges, vertices)
    assignment = dict(fixed)
    if any(u in assignment and v in assignment and assignment[u] == assignment[v]
           for u, v in edges):
        return []
    answers = []

    def visit():
        if len(assignment) == len(adj):
            answers.append(dict(assignment))
            return
        domains = {v: tuple(c for c in range(4)
                            if c not in {assignment[w] for w in adj[v] if w in assignment})
                   for v in adj if v not in assignment}
        v = min(domains, key=lambda x: (len(domains[x]), -len(adj[x]), x))
        for c in domains[v]:
            assignment[v] = c
            visit()
        assignment.pop(v, None)

    visit()
    return answers


@lru_cache(maxsize=None)
def row_answers(edges, vertices, row):
    return colourings(edges, dict(enumerate(ROWS[row])), vertices)


def sigma(edges, vertices):
    return sum(1 << i for i in range(10) if row_answers(edges, vertices, i))


def missing_q(mask):
    return {q for q, row in QROWS.items() if not mask & (1 << row)}


def proper_profile(qs):
    return len(qs) <= 1 or len(qs) == 2 and any((q + 1) % 5 in qs for q in qs)


def faces(rotation):
    darts = {(u, v) for u, ns in rotation.items() for v in ns}
    result = []
    while darts:
        first = min(darts)
        orbit, current = [], first
        while current in darts:
            darts.remove(current)
            orbit.append(current)
            u, v = current
            around = rotation[v]
            current = (v, around[(around.index(u) + 1) % len(around)])
        assert current == first, "rotation face traversal did not close"
        result.append(orbit)
    return result


def shield(piece, roots, edges, rotation):
    kept = B | set(piece)
    kedges = tuple(e for e in edges if set(e) <= kept)
    krotation = {v: [n for n in rotation[v] if n in kept] for v in kept}
    kfaces = faces(krotation)
    sides = set()
    for p in piece:
        for root in roots:
            if root not in rotation[p]:
                continue
            around = rotation[p]
            i = around.index(root)
            before = next(around[(i - d) % len(around)] for d in range(1, len(around) + 1)
                          if around[(i - d) % len(around)] in kept)
            after = next(around[(i + d) % len(around)] for d in range(1, len(around) + 1)
                         if around[(i + d) % len(around)] in kept)
            for fi, f in enumerate(kfaces):
                if (before, p) in f and (p, after) in f:
                    j = f.index((before, p))
                    if f[(j + 1) % len(f)] == (p, after):
                        sides.add(fi)
    assert len(sides) == 1, "the outside original H does not lie in one piece-face"
    fi = next(iter(sides))
    boundary = {tuple(sorted(d)) for d in kfaces[fi]} & BEDGES
    return sorted(BEDGES - boundary)


def theta_contains_zw_on_outside(roots, mixed, edges, rotation):
    """Locate B's theta face through an actual original B-to-theta path."""
    original = adjacency(edges)
    theta = {tuple(sorted(roots))}
    for piece in mixed:
        allowed = set(piece["vertices"]) | set(roots)
        todo = [roots[0]]
        parent = {roots[0]: None}
        for v in todo:
            if v == roots[1]:
                break
            for w in sorted(original[v] & allowed):
                if set((v, w)) == set(roots) or w in parent:
                    continue
                parent[w] = v
                todo.append(w)
        v = roots[1]
        while parent[v] is not None:
            theta.add(tuple(sorted((v, parent[v]))))
            v = parent[v]
    tadj = adjacency(tuple(theta))
    trotation = {v: [w for w in rotation[v] if w in tadj[v]] for v in tadj}
    tfaces = faces(trotation)
    todo, visited = list(sorted(B)), set(B)
    exterior, terminal = None, None
    for v in todo:
        for w in sorted(original[v]):
            if w in tadj:
                exterior, terminal = v, w
                break
            if w not in visited:
                visited.add(w)
                todo.append(w)
        if terminal is not None:
            break
    assert terminal is not None
    around = rotation[terminal]
    i = around.index(exterior)
    before = next(around[(i-d) % len(around)] for d in range(1, len(around)+1)
                  if around[(i-d) % len(around)] in tadj[terminal])
    after = next(around[(i+d) % len(around)] for d in range(1, len(around)+1)
                 if around[(i+d) % len(around)] in tadj[terminal])
    selected = [f for f in tfaces if (before, terminal) in f and
                f[(f.index((before, terminal))+1) % len(f)] == (terminal, after)]
    assert len(selected) == 1
    return tuple(sorted(roots)) in {tuple(sorted(e)) for e in selected[0]}


def status(trigger, holds):
    return "not triggered" if not trigger else "triggered and holds" if holds else "counterexample"


def full_relation(piece, contacts, edges, beta):
    vertices = tuple(sorted(B | set(piece)))
    localedges = tuple(e for e in edges if set(e) <= set(vertices))
    answers = colourings(localedges, dict(enumerate(beta)), vertices)
    relation = sorted({tuple(a[c] for c in contacts) for a in answers})
    forbidden = set(range(4))
    for row in relation:
        forbidden &= set(row)
    assert relation, "component alone must have nonempty complete boundary relation"
    return relation, forbidden


def derive_structure(edges, vertices):
    adj = adjacency(edges, vertices)
    interior = set(vertices) - B
    roots = tuple(v for v in sorted(interior) if len(adj[v]) == 5)
    assert len(roots) == 2 and all(len(adj[v]) == 4 for v in interior - set(roots))
    parts = []
    for comp in components(interior - set(roots), tuple(e for e in edges if set(e) <= interior - set(roots))):
        incidence = [sorted(adj[r] & set(comp)) for r in roots]
        assert any(incidence)
        parts.append({"vertices": list(comp), "contacts": incidence,
                      "incidence": list(map(len, incidence)),
                      "support": sorted(set().union(*(adj[v] & B for v in comp))),
                      "kind": "mixed" if all(incidence) else "unary"})
    return adj, roots, parts


def inspect_one(source, image, edges, vertices, rotation):
    adj, roots, parts = derive_structure(edges, vertices)
    interior = set(vertices) - B
    m = sum(p["kind"] == "mixed" for p in parts)
    unary = [p for p in parts if p["kind"] == "unary"]
    fullmask = sigma(edges, vertices)
    qs = missing_q(fullmask)
    triple = {0, 1, 3} <= qs
    deletions, checks = [], []
    root_omissions = []

    def add(lemma, trigger, holds, data=None):
        checks.append({"lemma": lemma, "result": status(trigger, holds), "data": data})

    f = faces(rotation)
    assert len(vertices) - len(edges) + len(f) == 2
    assert any(len(face) == 5 and {tuple(sorted(d)) for d in face} == BEDGES for face in f)
    assert {e for e in edges if set(e) <= B} == BEDGES
    assert connected(interior, tuple(e for e in edges if set(e) <= interior))
    assert set().union(*(adj[v] & B for v in interior)) == B
    assert all(fullmask & (1 << row) for row in T4ROWS)
    assert tuple(sorted(roots)) in edges
    for e in edges:
        if e in BEDGES:
            continue
        subedges = tuple(x for x in edges if x != e)
        mask = sigma(subedges, vertices)
        new = [i for i in range(10) if mask & (1 << i) and not fullmask & (1 << i)]
        assert new, "original nonboundary edge is not Sigma-critical"
        data = {"edge": list(e), "sigma": mask, "Q": sorted(missing_q(mask)), "new_rows": new,
                "witnesses": {str(i): [row_answers(subedges, vertices, i)[0][v] for v in vertices] for i in new}}
        deletions.append(data)
        add("E5-L1 proper-subgraph (maximal original deletion)", True, proper_profile(missing_q(mask)), data)
    for r in roots:
        rv = tuple(v for v in vertices if v != r)
        re = tuple(e for e in edges if r not in e)
        root_omissions.append({"root": r, "sigma": sigma(re, rv)})
    add("E3 cited root and zw acceptance prerequisite", m >= 1,
        all(item["sigma"] == 1023 for item in root_omissions) and
        sigma(tuple(e for e in edges if e != tuple(sorted(roots))), vertices) == 1023,
        {"root_omissions": root_omissions})
    add("E6-A adjacent m<=2", True, m <= 2, {"m": m})
    add("E6-A four-road contradiction branch", m >= 3, False, {"m": m})
    add("E6-A m=2 outer theta boundary", m == 2,
        m != 2 or not theta_contains_zw_on_outside(roots, [p for p in parts if p["kind"] == "mixed"],
                                                   edges, rotation), {"m": m})
    for p in parts:
        comp = set(p["vertices"])
        outside = interior - comp
        p["shield"] = shield(comp, roots, edges, rotation)
        p["one_sided"] = connected(outside, tuple(e for e in edges if set(e) <= outside))
        add("E6-B one-sided original piece", True, p["one_sided"], p)
        add("E6-A N-empty", not p["support"], False, p)
        actualshield = {tuple(e) for e in p["shield"]}
        shieldvertices = set(itertools.chain.from_iterable(actualshield))
        if len(p["support"]) >= 2:
            add("E6-B actual support equals shield vertices", True,
                set(p["support"]) == shieldvertices, p)
        add("E6-B unary costs at least two", p["kind"] == "unary",
            len(actualshield) >= 2 and len(p["support"]) >= 3, p)
        longmixed = p["kind"] == "mixed" and not any(set(p["support"]) <= set(e) for e in BEDGES)
        add("E6-B long mixed costs at least two", longmixed, len(actualshield) >= 2, p)
        shorttwo = p["kind"] == "mixed" and len(p["support"]) == 2
        add("E6-B two-point short mixed costs one", shorttwo, len(actualshield) == 1, p)
    allshield = [tuple(e) for p in parts for e in p["shield"]]
    add("E6-B total disjoint shield budget", True, len(allshield) == len(set(allshield)) <= 5,
        {"total_cost": len(allshield)})
    add("E6-B unary count", True, len(unary) <= 2, {"unary": len(unary)})
    for r in roots:
        spokes = sorted(adj[r] & B)
        incidences = sum(len(adj[r] & set(p["vertices"])) for p in parts)
        add("E6-B original root incidence", True, len(spokes) + incidences == 4 and len(spokes) <= 3,
            {"root": r, "spokes": spokes, "piece_incidences": incidences})
        for j in spokes:
            D = {q for q in qs if any(ROWS[QROWS[q]][j] == ROWS[QROWS[q]][k] for k in spokes if k != j)}
            subedges = tuple(e for e in edges if e != tuple(sorted((r, j))))
            subqs = missing_q(sigma(subedges, vertices))
            add("E6-C redundant spoke", True, D <= subqs and proper_profile(D),
                {"root": r, "spoke": j, "D_e": sorted(D), "omission_Q": sorted(subqs)})
    for p in unary:
        contacts = tuple(c for side in p["contacts"] for c in side)
        sa = adjacency(tuple(tuple(e) for e in p["shield"]))
        endpoints = sorted(v for v, ns in sa.items() if len(ns) == 1)
        for ri, beta in enumerate(ROWS):
            relation, forb = full_relation(p["vertices"], contacts, edges, beta)
            trigger = len(p["support"]) == 3 and len(p["shield"]) == 2 and len(endpoints) == 2
            add("E6-F endpoint forbidden colours", trigger,
                not forb & {beta[h] for h in endpoints},
                {"piece": p["vertices"], "contacts": list(contacts), "row": ri,
                 "relation": [list(x) for x in relation], "relation_sha256": digest(relation),
                 "forbidden": sorted(forb), "endpoints": endpoints})
    mixed = [p for p in parts if p["kind"] == "mixed"]
    no_mixed_budget = (len(unary) == 2 and all(sum(p["incidence"][i] > 0 for p in unary) == 1
                                           for i in range(2)))
    add("E6-D no-mixed original two-unary budget", m == 0, no_mixed_budget, {"m": m})
    g2, g3, g4 = False, False, False
    named_ok = True
    for ai, bi in ((0, 1), (1, 0)):
        if len(mixed) != 1 or len(unary) != 1:
            continue
        a, b = roots[ai], roots[bi]
        S_a, S_b = sorted(adj[a] & B), sorted(adj[b] & B)
        C, U = mixed[0], unary[0]
        g2_here = (C["incidence"] == [1, 1] and U["incidence"][ai] == 0 and
                   U["incidence"][bi] == 1 and len(S_a) == 3 and len(S_b) == 2)
        g3_here = (C["incidence"] == [1, 1] and U["incidence"][ai] == 0 and
                   U["incidence"][bi] == 2 and len(S_a) == 3 and len(S_b) == 1)
        g4_here = (C["incidence"][ai] == 1 and C["incidence"][bi] == 2 and
                   U["incidence"][ai] == 1 and U["incidence"][bi] == 0 and
                   len(S_a) == len(S_b) == 2)
        g2, g3, g4 = g2 or g2_here, g3 or g3_here, g4 or g4_here
        if g3_here:
            table = {(0, 1, 2): ({0, 3, 4}, {0, 2}), (1, 2, 3): ({0, 3, 4}, {1, 3}),
                     (0, 1, 4): ({1, 2, 3}, {1, 4}), (0, 3, 4): ({1, 2, 3}, {0, 3})}
            selected = table.get(tuple(S_a))
            named_ok = named_ok and selected is not None and set(U["support"]) == selected[0] and S_b[0] in selected[1]
    add("E6-E G2 shield exactly two", triple and g2,
        len(unary) == 1 and len(unary[0]["shield"]) == 2)
    add("E6-E G3 shield exactly two", triple and g3,
        len(unary) == 1 and len(unary[0]["shield"]) == 2)
    add("E6-F G3 named-support corollary", triple and g3, named_ok)
    add("E6-G G4 shield exactly three", triple and g4,
        len(unary) == 1 and len(unary[0]["shield"]) == 3)
    cores = []
    spokeedges = [e for e in edges if bool(set(e) & B) and bool(set(e) & set(roots))]
    for bits in itertools.product((False, True), repeat=len(parts)):
        keptparts = [p for p, yes in zip(parts, bits) if yes]
        selected = B | set(roots) | set(itertools.chain.from_iterable(p["vertices"] for p in keptparts))
        for sbits in itertools.product((False, True), repeat=len(spokeedges)):
            removed = {e for e, keep in zip(spokeedges, sbits) if not keep}
            ce = tuple(e for e in edges if set(e) <= selected and e not in removed)
            cv = tuple(sorted(selected))
            cadj = adjacency(ce, cv)
            if any(len(cadj[v]) < 4 for v in selected - B):
                continue
            if not all(len(cadj[r]) == 4 for r in roots):
                continue
            for row in range(10):
                if row_answers(ce, cv, row):
                    continue
                minimal = all(row_answers(tuple(x for x in ce if x != e), cv, row)
                              for e in ce if e not in BEDGES)
                if not minimal:
                    continue
                retainedmixed = [p for p in keptparts if p["kind"] == "mixed"]
                omitted = [p for p, yes in zip(parts, bits) if not yes]
                core = {"row": row, "edges": [list(e) for e in ce], "vertices": list(cv),
                        "removed_spokes": [list(e) for e in sorted(removed)],
                        "omitted_pieces": omitted, "retained_mixed": retainedmixed}
                cores.append(core)
                if retainedmixed:
                    add("E6-B retained mixed44 shared contact", True,
                        len(retainedmixed) == 1 and retainedmixed[0]["incidence"] == [1, 1] and
                        retainedmixed[0]["contacts"][0] == retainedmixed[0]["contacts"][1], core)
                hretain = (len(removed) == 1 and len(omitted) == 1 and
                           omitted[0]["kind"] == "unary" and
                           sum(omitted[0]["incidence"]) == 1 and len(retainedmixed) == 1)
                if hretain:
                    spoke = next(iter(removed))
                    ar = next(r for r in roots if r in spoke)
                    ai = roots.index(ar)
                    bi = 1 - ai
                    counts = [sum(p["kind"] == "unary" and p["incidence"][i] > 0
                                  for p in keptparts) for i in range(2)]
                    unitretained = all(sum(p["incidence"]) == 1 for p in keptparts if p["kind"] == "unary")
                    add("E6-H retaining spoke and unit unary groups", True,
                        omitted[0]["incidence"][bi] == 1 and unitretained and
                        counts[ai] in (0, 1) and counts[bi] == 0 and
                        [len(adj[roots[i]] & B) for i in (ai, bi)] == [3-counts[ai], 2-counts[bi]],
                        {"row": row, "core": core, "oriented_roots": [roots[ai], roots[bi]],
                         "retained_unary_counts": [counts[ai], counts[bi]],
                         "group": "G2" if counts[ai] == 0 else "J4"})
                    add("E6-H retained J4 mixed short support", counts[ai] == 1,
                        any(set(retainedmixed[0]["support"]) <= set(e) for e in BEDGES), core)
                mixedonly = (not removed and len(omitted) == 1 and omitted[0]["kind"] == "mixed" and
                             omitted[0]["incidence"] == [1, 1] and len(parts) == len(keptparts) + 1)
                if mixedonly:
                    ks = [sum(p["incidence"][i] for p in keptparts) for i in range(2)]
                    validbinary = all(ks[i] != 2 or
                        any(p["incidence"][i] == 2 and p["kind"] == "unary" and
                            tuple(sorted(p["contacts"][i])) in edges for p in keptparts)
                        for i in range(2))
                    add("E6-H mixed-only original groups", True,
                        all(k <= 2 for k in ks) and validbinary and
                        all(len(adj[roots[i]] & B) == 3-ks[i] for i in range(2)),
                        {"row": row, "core": core, "k": ks,
                         "spokes": [len(adj[r] & B) for r in roots]})
    return {"source": source, "D5_image": list(image), "edges": [list(e) for e in edges],
            "vertices": list(vertices), "degree": {str(v): len(adj[v]) for v in vertices},
            "rotation": {str(v): list(ns) for v, ns in sorted(rotation.items())},
            "faces": [[list(d) for d in face] for face in f],
            "roots": list(roots), "sigma": fullmask, "Q": sorted(qs), "triple_triggered": triple,
            "parts": parts, "deletions": deletions, "cores": cores, "checks": checks}


def run(root):
    cases = []
    paths = sorted((root / "artifacts/c5_excess_two_finite_search").glob("AD_k*_validate/crit_orbits/*.json"))
    assert len(paths) == 9
    for path in paths:
        data = json.loads(path.read_text())
        baseedges = tuple(sorted(tuple(sorted(e)) for e in data["canonical_edges"]))
        vertices = tuple(sorted(set(itertools.chain.from_iterable(baseedges))))
        base = {int(v): ns for v, ns in data["embedding"]["disk_rotation"].items()}
        for reflection in (1, -1):
            for shift in range(5):
                image = [(shift + reflection * i) % 5 for i in range(5)]
                transport = {v: image[v] if v in B else v for v in vertices}
                edges = tuple(sorted(tuple(sorted((transport[u], transport[v]))) for u, v in baseedges))
                rotation = {transport[v]: [transport[n] for n in ns] for v, ns in base.items()}
                cases.append(inspect_one(str(path.relative_to(root)), image, edges, vertices, rotation))
    totals = defaultdict(Counter)
    for case in cases:
        for check in case["checks"]:
            totals[check["lemma"]][check["result"]] += 1
    tables = []
    for mask in (941, 933, 940, 932):
        qs = missing_q(mask)
        kept = []
        for S in itertools.combinations(range(5), 3):
            Ds = [{q for q in qs if any(ROWS[QROWS[q]][j] == ROWS[QROWS[q]][k] for k in S if k != j)}
                  for j in S]
            if all(proper_profile(D) for D in Ds):
                kept.append("".join(map(str, S)))
        tables.append({"mask": mask, "Q": sorted(qs), "necessary_triples": kept})
    assert [t["necessary_triples"] for t in tables] == [
        ["012", "013", "014", "034", "123", "234"],
        ["012", "014", "034", "123", "234"],
        ["012", "014", "034", "123", "234"],
        ["012", "014", "034", "123", "234"]]
    orbit_summary = []
    for source in sorted({case["source"] for case in cases}):
        group = [case for case in cases if case["source"] == source]
        orbit_summary.append({"source": source, "input_sha256": hashlib.sha256((root / source).read_bytes()).hexdigest(),
                              "D5_cases": len(group),
                              "identity_sigma": next(case["sigma"] for case in group if case["D5_image"] == list(range(5))),
                              "m_values": sorted({sum(p["kind"] == "mixed" for p in case["parts"]) for case in group}),
                              "triple_triggered_cases": sum(case["triple_triggered"] for case in group),
                              "counterexamples": sum(check["result"] == "counterexample" for case in group for check in case["checks"])})
    result = {"source_orbit_summary": orbit_summary, "baseline": "b2ca4520da50c9d2898ac6f8f966ac25df3f9609",
              "source_orbits": 9, "D5_cases": len(cases), "rows": [list(q) for q in ROWS],
              "E6_C_tables": tables, "statistics": {k: {s: v.get(s, 0) for s in
              ("triggered and holds", "not triggered", "counterexample")} for k, v in sorted(totals.items())},
              "cases": cases}
    assert not any(c["result"] == "counterexample" for case in cases for c in case["checks"])
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=HERE / "e6_controls.json")
    args = parser.parse_args()
    result = run(args.root)
    output = args.output
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
    if args.check:
        assert output.read_text() == encoded, "independent output differs from saved audit result"
    else:
        with output.open("x") as handle:
            handle.write(encoded)
    print(json.dumps({"source_orbits": result["source_orbits"], "D5_cases": result["D5_cases"],
                      "statistics": result["statistics"], "sha256": hashlib.sha256(encoded.encode()).hexdigest()},
                     sort_keys=True))


if __name__ == "__main__":
    main()
