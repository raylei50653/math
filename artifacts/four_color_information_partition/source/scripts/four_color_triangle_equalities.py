"""Same-source equality closure and three-colour triangles, without colouring.

Two triangles sharing an edge and confined to one three-colour palette have
equal opposite vertices. Equal vertices may be contracted for inference while
each quotient edge retains a real original-edge witness. A triangle confined
to three colours uses that entire palette, so every common neighbour avoids it.
Neither operation changes the input graph or commits a colour assignment.
"""
from __future__ import annotations


def derive_triangle_equalities(vertices, edges, domains, *, max_checks=200000,
                               charge=None):
    """Return a completed rule closure/contradiction, or no partial deductions.

    ``domains`` maps original integer vertex identities to literal colours 0..3.
    A complete, consistent result provides equality classes and narrowed domains;
    it does not assert global colourability. Proof steps record class membership,
    current domains, palettes and actual original edges used by each deduction.
    The caller must retain the provenance of supplied domain restrictions.

    A check is an inspected original edge, quotient palette, common-neighbour
    candidate, domain-colour membership, or equality merge. Initial validation,
    original adjacency preparation, sorting and union-find metadata are outside
    this logical-work count. ``charge`` runs before every counted check. Its
    exceptions propagate unchanged. Reaching the local cap returns no classes,
    domains or partial proof, and never means unsatisfiable.
    """
    if type(max_checks) is not int or max_checks < 0:
        raise ValueError("max_checks must be a nonnegative integer")
    if charge is not None and not callable(charge):
        raise ValueError("charge must be callable or None")
    vertices = tuple(vertices)
    if any(type(v) is not int for v in vertices) or len(set(vertices)) != len(vertices):
        raise ValueError("vertices must be distinct integers")
    index = {v: i for i, v in enumerate(vertices)}
    original_edges = []
    seen_edges = set()
    for edge in edges:
        if (len(edge) != 2 or any(type(v) is not int or v not in index for v in edge)
                or edge[0] == edge[1]):
            raise ValueError("edges need two distinct declared integer vertices")
        pair = tuple(sorted(index[v] for v in edge))
        if pair in seen_edges:
            raise ValueError("duplicate undirected edge")
        seen_edges.add(pair)
        original_edges.append(pair)
    original_edges.sort()
    class_domains = []
    for v in vertices:
        values = set(domains[v])
        if any(type(c) is not int or c not in range(4) for c in values):
            raise ValueError("domains need literal colours 0..3")
        class_domains.append(values)
    parent = list(range(len(vertices)))
    members = {i: {i} for i in parent}
    proof_steps = []
    used_edges = set()
    checks = 0
    check_kinds = dict(edge=0, palette=0, neighbor=0, domain=0, merge=0)

    class LocalLimit(Exception):
        pass

    def tick(kind):
        nonlocal checks
        if checks >= max_checks:
            raise LocalLimit
        if charge is not None:
            charge()
        checks += 1
        check_kinds[kind] += 1

    def root(v):
        while parent[v] != v:
            v = parent[v]
        return v

    def labels(group):
        return [vertices[v] for v in sorted(members[group])]

    def literal_edges(pairs):
        return [list(pair) for pair in sorted(
            tuple(sorted((vertices[u], vertices[v]))) for u, v in pairs)]

    def class_evidence(groups):
        return [dict(vertices=labels(group), colors=sorted(class_domains[group]))
                for group in groups]

    def result(complete, *, consistent=None, conflict=None):
        return dict(
            complete=complete, consistent=consistent, checks=checks,
            check_kinds=dict(check_kinds), truncated=not complete,
            classes=[tuple(labels(group)) for group in sorted(members)] if complete else None,
            domains={v: frozenset(class_domains[root(i)]) for i, v in enumerate(vertices)}
            if complete else None,
            proof_steps=proof_steps if complete else None,
            source_edges=literal_edges(used_edges) if complete else None,
            conflict=conflict if complete else None,
            limit_reason=None if complete else "checks")

    try:
        for group in members:
            tick("domain")
            if not class_domains[group]:
                return result(True, consistent=False,
                              conflict=dict(kind="empty_class_domain", vertices=labels(group)))
        # Validation has already rejected loops and malformed edges. Neither
        # rule can start when every class still permits all four colours.
        if all(len(values) == 4 for values in class_domains):
            return result(True, consistent=True)
        while True:
            # Rebuild after every deduction. All quotient edges have literal
            # witnesses, and no stale quotient structure crosses a merge.
            adjacency = {group: set() for group in members}
            edge_witness = {}
            for u, v in original_edges:
                tick("edge")
                a, b = root(u), root(v)
                if a == b:
                    used_edges.add((u, v))
                    return result(True, consistent=False,
                                  conflict=dict(kind="equal_edge", edge=[vertices[u], vertices[v]],
                                                equality_class=labels(a)))
                if (len(class_domains[a]) == 1
                        and class_domains[a] == class_domains[b]):
                    used_edges.add((u, v))
                    return result(True, consistent=False,
                                  conflict=dict(kind="same_singleton_edge",
                                                edge=[vertices[u], vertices[v]],
                                                classes=class_evidence((a, b))))
                adjacency[a].add(b)
                adjacency[b].add(a)
                edge_witness.setdefault(tuple(sorted((a, b))), (u, v))

            def witnesses(pairs):
                return {edge_witness[tuple(sorted(pair))] for pair in pairs}

            changed = False
            for a, b in sorted(edge_witness):
                tick("palette")
                palette = class_domains[a] | class_domains[b]
                if len(palette) != 3:
                    continue
                first = None
                neighbors = min((adjacency[a], adjacency[b]), key=len)
                for v in sorted(neighbors):
                    tick("neighbor")
                    if v not in adjacency[a] or v not in adjacency[b]:
                        continue
                    inside = True
                    for color in sorted(class_domains[v]):
                        tick("domain")
                        if color not in palette:
                            inside = False
                            break
                    if not inside:
                        continue
                    if first is None:
                        first = v
                        continue
                    u = first
                    tick("merge")
                    shared = set()
                    for color in range(4):
                        tick("domain")
                        if color in class_domains[u] and color in class_domains[v]:
                            shared.add(color)
                    original = witnesses(((a, b), (a, u), (b, u), (a, v), (b, v)))
                    proof_steps.append(dict(
                        kind="three_color_double_triangle", palette=sorted(palette),
                        shared_edge_classes=class_evidence((a, b)),
                        equal_classes=class_evidence((u, v)),
                        source_edges=literal_edges(original), intersection=sorted(shared)))
                    used_edges.update(original)
                    keep, retire = sorted((u, v))
                    parent[retire] = keep
                    members[keep].update(members.pop(retire))
                    class_domains[keep] = shared
                    if not shared:
                        return result(True, consistent=False,
                                      conflict=dict(kind="empty_class_domain", vertices=labels(keep)))
                    changed = True
                    break
                if changed:
                    break
            if changed:
                continue

            for a, b in sorted(edge_witness):
                neighbors = min((adjacency[a], adjacency[b]), key=len)
                for c in sorted(neighbors):
                    tick("neighbor")
                    if c <= b or c not in adjacency[a] or c not in adjacency[b]:
                        continue
                    tick("palette")
                    palette = class_domains[a] | class_domains[b] | class_domains[c]
                    if len(palette) != 3:
                        continue
                    candidates = min((adjacency[a], adjacency[b], adjacency[c]), key=len)
                    for hub in sorted(candidates):
                        tick("neighbor")
                        if any(hub not in adjacency[v] for v in (a, b, c)):
                            continue
                        narrowed = set()
                        for color in sorted(class_domains[hub]):
                            tick("domain")
                            if color not in palette:
                                narrowed.add(color)
                        if narrowed == class_domains[hub]:
                            continue
                        original = witnesses(((a, b), (a, c), (b, c),
                                              (a, hub), (b, hub), (c, hub)))
                        proof_steps.append(dict(
                            kind="three_color_triangle_exclusion", palette=sorted(palette),
                            triangle_classes=class_evidence((a, b, c)),
                            neighbor_class=class_evidence((hub,))[0],
                            source_edges=literal_edges(original), colors_after=sorted(narrowed)))
                        used_edges.update(original)
                        class_domains[hub] = narrowed
                        if not narrowed:
                            return result(True, consistent=False,
                                          conflict=dict(kind="empty_class_domain", vertices=labels(hub)))
                        changed = True
                        break
                    if changed:
                        break
                if changed:
                    break
            if not changed:
                return result(True, consistent=True)
    except LocalLimit:
        return result(False)
