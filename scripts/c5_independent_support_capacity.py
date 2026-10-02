#!/usr/bin/env python3
"""Small controls for 933/941 excess, conditional capacity, and support span.

No graph generation or realizability oracle. The arbitrary-size arguments are
in docs/c5_independent_support_capacity.md. Full tuples use one literal frame.
"""
import argparse
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_independent_support_capacity/observations.json"
U = set(range(4))
B = set(range(5))
FRAME = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}


def normalize(values):
    names = {}
    return tuple(names.setdefault(v, len(names)) for v in values)


ROWS = tuple(sorted({normalize(b) for b in product(range(4), repeat=5)
                     if all(b[i] != b[(i + 1) % 5] for i in range(5))}))
T4 = sum(1 << i for i, b in enumerate(ROWS) if len(set(b)) == 4)


def colorings(vertices, edges, fixed):
    vertices = sorted(vertices)
    result = []
    for colors in product(range(4), repeat=len(vertices)):
        assignment = dict(fixed)
        assignment.update(zip(vertices, colors))
        if all(assignment[a] != assignment[b] for a, b in edges
               if a in assignment and b in assignment):
            result.append(assignment)
    return result


def components(vertices, edges):
    todo, result = set(vertices), []
    while todo:
        seen, stack = set(), [min(todo)]
        while stack:
            v = stack.pop()
            if v in seen:
                continue
            seen.add(v)
            stack.extend(b if a == v else a for a, b in edges
                         if v in (a, b) and {a, b} <= todo)
        todo -= seen
        result.append(sorted(seen))
    return result


def span(support):
    if not support:
        return 0
    return min(length for length in range(5) for start in range(5)
               if set(support) <= {(start + j) % 5 for j in range(length + 1)})


def fixed_graph(name, n, extra_edges):
    edges = FRAME | {tuple(sorted(e)) for e in extra_edges}
    internal = set(range(5, n))
    neighbors = {v: {b if a == v else a for a, b in edges if v in (a, b)}
                 for v in range(n)}
    roots = {v for v in internal if len(neighbors[v]) >= 5}
    assert all(len(neighbors[v]) >= 4 for v in internal)
    regions = components(internal - roots, edges)
    full = [colorings(internal, edges, dict(enumerate(row))) for row in ROWS]
    mask = sum(1 << i for i, fs in enumerate(full) if fs)
    deleted = []
    for edge in sorted(edges - FRAME):
        fs = [colorings(internal, edges - {edge}, dict(enumerate(row))) for row in ROWS]
        new_mask = sum(1 << i for i, choices in enumerate(fs) if choices)
        deleted.append(dict(edge=edge, mask=new_mask,
                            newly_accepted=[dict(row=ROWS[i], coloring=[choices[0][v] for v in range(n)])
                                            for i, choices in enumerate(fs)
                                            if choices and not (mask >> i & 1)]))
    audits = []
    for r in sorted(roots):
        other_roots = sorted(roots - {r})
        for i, row in enumerate(ROWS):
            fixed = dict(enumerate(row))
            deleted_root = colorings(internal - {r}, edges, fixed)
            etas = {}
            for f in deleted_root:
                etas.setdefault(tuple(f[v] for v in other_roots), f)
            for eta, witness in sorted(etas.items()):
                conditioned = dict(fixed)
                conditioned.update(zip(other_roots, eta))
                factors, data, deficit = [], [], 0
                for v in sorted(neighbors[r] & (B | roots)):
                    factors.append({conditioned[v]})
                for region in regions:
                    contacts = sorted(neighbors[r] & set(region))
                    if not contacts:
                        continue
                    # All root contacts are kept in the same tuple, including
                    # shared contacts. Fix other roots before any projection.
                    order = sorted(set(region) & set().union(*(neighbors[x] for x in roots)))
                    choices = colorings(region, edges, conditioned)
                    assert choices
                    tuples = sorted({tuple(f[v] for v in order) for f in choices})
                    forbidden = set.intersection(*(set(f[v] for v in contacts) for f in choices))
                    assert len(forbidden) <= len(contacts)
                    factors.append(forbidden)
                    deficit += len(contacts) - len(forbidden)
                    data.append(dict(vertices=region, contacts=contacts, tuple_order=order,
                                     tuples=tuples, forbidden=sorted(forbidden),
                                     support=sorted(set().union(*(neighbors[v] & B for v in region))),
                                     other_root_contacts={str(x): sorted(neighbors[x] & set(region))
                                                          for x in other_roots},
                                     tuple_witnesses=[dict(tuple=t, coloring=[next(f for f in choices
                                         if tuple(f[v] for v in order) == t)[v] for v in region]) for t in tuples]))
                covered = set().union(*factors)
                residual = U - covered
                actual = {f[r] for f in full[i] if tuple(f[v] for v in other_roots) == eta}
                assert residual == actual
                overlap = sum(map(len, factors)) - len(covered)
                assert deficit + overlap == len(neighbors[r]) - 4 + len(residual)
                audits.append(dict(root=r, row=row, other_roots=other_roots, eta=eta,
                                   deleted_root_order=sorted(set(range(n)) - {r}),
                                   deleted_root_coloring=[witness[v] for v in range(n) if v != r],
                                   direct_neighbors=sorted(neighbors[r] & (B | roots)),
                                   components=data, residual=sorted(residual), D=deficit, O=overlap,
                                   rejected=not bool(full[i])))
    return dict(name=name, vertices=n, boundary=list(range(5)), edges=sorted(edges),
                roots=sorted(roots), degrees={str(v): len(neighbors[v]) for v in internal},
                excess=sum(len(neighbors[v]) - 4 for v in internal), mask=mask,
                deletion_records=deleted, conditional_audits=audits)


def build():
    assert T4 == 932
    candidates = []
    for mask in (933, 941):
        rejected = [i for i in range(10) if not (mask >> i & 1)]
        requirements = []
        for i in rejected:
            row = ROWS[i]
            singleton, = [j for j in range(5) if row.count(row[j]) == 1]
            support = sorted(B - {singleton})
            assert span(support) == 3
            d, = U - set(row)
            for v in support:
                changed = list(row)
                changed[v] = d
                assert len(set(changed)) == 4
                assert mask >> ROWS.index(normalize(changed)) & 1
            requirements.append(dict(row=row, singleton=singleton, forced_support=support, span_lower_bound=3))
        candidates.append(dict(mask=mask, rejected=requirements,
                               forced_total_support=sorted(set().union(*(set(x['forced_support']) for x in requirements))),
                               proven_excess_lower_bound=1))

    # All possible supports containing at least four named boundary vertices.
    large_supports = [set(s) for k in (4, 5) for s in combinations(range(5), k)]
    crossing = []
    for s in large_supports:
        for t in large_supports:
            witnesses = [(a, b, c, d) for a, b, c, d in combinations(range(5), 4)
                         if (a in s and c in s and b in t and d in t)]
            # Reverse the assignment of the two paths if needed.
            reverse = False
            if not witnesses:
                witnesses = [(a, b, c, d) for a, b, c, d in combinations(range(5), 4)
                             if (a in t and c in t and b in s and d in s)]
                reverse = True
            assert witnesses
            crossing.append(dict(first=sorted(s), second=sorted(t), alternating=witnesses[0], reverse=reverse))

    q = ROWS[0]
    d, = U - set(q)
    symmetry = []
    for bits in range(32):
        support = {v for v in range(5) if bits >> v & 1}
        seen = {q[v] for v in support}
        stabilizer = [p for p in permutations(range(4)) if all(p[c] == c for c in seen)]
        for fbits in range(16):
            f = {c for c in U if fbits >> c & 1}
            if d not in f or not all({p[c] for c in f} == f for p in stabilizer):
                continue
            lower = max(0, 3 - len(f))
            assert U - seen <= f and len(seen) >= 4 - len(f)
            assert span(support) >= lower
            symmetry.append(dict(support=sorted(support), seen=sorted(seen), forbidden=sorted(f),
                                 actual_min_span=span(support), lower_bound=lower))

    graphs = [
        fixed_graph("existing_943_k3_t382_submask_2045", 8,
                    [(2, 5), (2, 7), (3, 6), (3, 7), (4, 6), (5, 6), (5, 7), (6, 7), (1, 5), (0, 5)]),
        fixed_graph("conditional_mixed_control", 8,
                    [(5, 6), (5, 7), (6, 7), (0, 7), (1, 7),
                     (0, 5), (1, 5), (2, 5), (1, 6), (2, 6), (3, 6)]),
        fixed_graph("three_unseen_singletons_NONDISK", 9,
                    [(5, b) for b in (0, 1, 4)] + [(5, v) for v in (6, 7, 8)]
                    + [(v, b) for v in (6, 7, 8) for b in (0, 1, 4)]),
    ]
    old = graphs[0]
    assert old['mask'] == 943 and old['excess'] == 1
    assert all(x['mask'] != 943 for x in old['deletion_records'])
    missing = [i for i in range(10) if not (943 >> i & 1)]
    assert all(any(not (x['mask'] >> i & 1) for x in old['deletion_records']) for i in missing)
    six = next(a for a in graphs[2]['conditional_audits'] if tuple(a['row']) == q)
    assert six['rejected'] and six['D'] == 0 and six['O'] == 2
    assert all(c['forbidden'] == [d] and span(c['support']) == 2 for c in six['components'])
    assert all((b, v) in graphs[2]['edges'] for b in (0, 1, 4) for v in (6, 7, 8))
    mixed = next(a for a in graphs[1]['conditional_audits']
                 if a['root'] == 5 and tuple(a['row']) == q and a['eta'] == (2,))
    assert mixed['components'][0]['forbidden'] == [3]
    assert span(mixed['components'][0]['support']) == 1
    assert any(x['support'] == [0, 1] and x['forbidden'] == [2, 3]
               and x['lower_bound'] == 1 for x in symmetry)
    return dict(schema=1, scope="paper lower bounds and three fixed controls; no 933/941 realization or exclusion",
                script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(), pattern_order=ROWS,
                candidates=candidates, alternating_support_controls=crossing,
                stabilizer_controls=symmetry, fixed_graphs=graphs,
                six_span_obstruction=dict(unary_components=3, forbidden_each=[d],
                                          span_each_at_least=2, total_at_least=6,
                                          disk_budget=5, configuration_forced_in_candidates=False),
                summary=dict(candidate_masks=[933, 941], proven_excess_lower_bound=1,
                             alternating_support_pairs=len(crossing), stabilizer_cases=len(symmetry),
                             fixed_graphs=len(graphs),
                             conditional_audits=sum(len(g['conditional_audits']) for g in graphs),
                             new_graph_enumeration=False, candidate_exclusions=0))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f"certificate differs: {OUT}"
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == "__main__":
    main()
