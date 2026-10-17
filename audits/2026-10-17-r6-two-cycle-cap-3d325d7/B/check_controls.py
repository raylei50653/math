#!/usr/bin/env python3
"""Read-only fixed graph scope controls; no source-realizability authority."""

import json


def edge(a, b):
    return tuple(sorted((a, b)))


def cycle(vertices):
    return {edge(vertices[i], vertices[(i + 1) % len(vertices)])
            for i in range(len(vertices))}


def components(vertices, edges):
    unseen = set(vertices)
    result = []
    while unseen:
        todo = [min(unseen)]
        seen = set()
        while todo:
            v = todo.pop()
            if v in seen:
                continue
            seen.add(v)
            todo.extend(b if a == v else a for a, b in edges
                        if (a == v or b == v)
                        and (b if a == v else a) not in seen)
        unseen -= seen
        result.append(frozenset(seen))
    return sorted(result, key=lambda c: (min(c), len(c)))


def validate_matching(vertices, edges, matching):
    assert matching <= edges, "reference uses a nonedge"
    used = [v for e in matching for v in e]
    assert len(used) == len(vertices) and set(used) == set(vertices), \
        "reference is not a perfect matching"


def matchings(vertices, edges):
    def visit(remaining, selected):
        if not remaining:
            yield frozenset(selected)
            return
        a = min(remaining)
        for b in sorted(remaining - {a}):
            e = edge(a, b)
            if e in edges:
                yield from visit(remaining - {a, b}, selected | {e})
    yield from visit(set(vertices), set())


def check(name, vertices, edges, matching):
    validate_matching(vertices, edges, matching)
    assert len(components(vertices, edges)) == 1
    assert all(sum(v in e for e in edges) == 3 for v in vertices)
    old = components(vertices, edges - matching)
    refs = []
    for reference in matchings(vertices, edges):
        validate_matching(vertices, edges, reference)
        complement = components(vertices, edges - reference)
        if any(len(c) % 2 for c in complement):
            continue
        regions = components(vertices, edges - (matching & reference))
        odd_per_region = [sum(len(c) % 2 for c in old if c <= w)
                          for w in regions]
        assert all(x % 2 == 0 for x in odd_per_region)
        assert all(sum(c <= w for w in regions) == 1 for c in old)
        if len(old) == 2 and all(len(c) % 2 for c in old):
            assert len(regions) == 1
        refs.append((reference, regions))
    assert refs
    return {
        "name": name,
        "vertices": len(vertices),
        "perfect_matchings": sum(1 for _ in matchings(vertices, edges)),
        "F_cycle_lengths": sorted(map(len, old)),
        "even_references": len(refs),
        "region_orders_over_all_even_references": sorted(
            [sorted(map(len, w)) for _, w in refs]),
    }


def main():
    prism_vertices = set(range(6))
    prism_f = cycle([0, 1, 2]) | cycle([3, 4, 5])
    prism_m = {edge(0, 3), edge(1, 4), edge(2, 5)}
    prism_edges = prism_f | prism_m
    positive = check("two total odd cycles", prism_vertices,
                     prism_edges, prism_m)
    assert positive["even_references"] == 3
    assert all(x == [6] for x in
               positive["region_orders_over_all_even_references"])
    assert len(components(prism_vertices, prism_edges - prism_m)) == 2
    positive["non_even_reference_R_equals_M_region_orders"] = [3, 3]

    extended_vertices = set(range(10))
    extended_f = cycle([0, 1, 2]) | cycle([3, 4, 5]) | cycle([6, 7, 8, 9])
    extended_m = {edge(0, 6), edge(3, 8), edge(1, 4),
                  edge(2, 5), edge(7, 9)}
    extended_edges = extended_f | extended_m
    scope = check("two odd cycles plus an extra even cycle",
                  extended_vertices, extended_edges, extended_m)
    explicit_r = {edge(0, 6), edge(3, 8), edge(1, 2),
                  edge(4, 5), edge(7, 9)}
    validate_matching(extended_vertices, extended_edges, explicit_r)
    assert sorted(map(len, components(extended_vertices,
                                     extended_edges - explicit_r))) == [4, 6]
    explicit_l = components(extended_vertices,
                            extended_edges - (extended_m & explicit_r))
    assert sorted(map(len, explicit_l)) == [4, 6]
    assert any({0, 1, 2, 3, 4, 5} == w for w in explicit_l)
    scope["explicit_even_reference_edges"] = sorted(explicit_r)
    scope["explicit_reference_region_orders"] = [4, 6]

    try:
        validate_matching(prism_vertices, prism_edges,
                          prism_m - {edge(0, 3)})
    except AssertionError as exc:
        assert str(exc) == "reference is not a perfect matching"
        rejected = True
    else:
        raise AssertionError("malformed reference was accepted")

    print(json.dumps({
        "authority": "fixed graph scope controls; no source control",
        "controls": [positive, scope],
        "malformed_reference_rejected": rejected,
        "source_realizability": "not triggered",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
