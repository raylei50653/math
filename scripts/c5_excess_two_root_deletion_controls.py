#!/usr/bin/env python3
"""Fixed controls for deleting one of two degree-five roots.

The controls keep the original degree-four components, their actual boundary
attachments, and all ordered contacts in one literal color frame.  They carry
no planarity, edge-minimality, or 933/941-source claim.  ``build`` is intended
for the excess-two paper checker; it performs no writes or source generation.
"""

from c5_941_two_spoke import search
from c5_independent_support_capacity import B, FRAME, ROWS, T4, U, colorings, components


def _neighbors(n, edges):
    return {v: {b if a == v else a for a, b in edges if v in (a, b)}
            for v in range(n)}


def _choices(vertices, edges, fixed):
    """Cross-check every full assignment with the inherited product checker."""
    order = sorted(vertices)
    found = list(search(order, edges, fixed))
    expected = colorings(order, edges, fixed)
    encode = lambda fs: {tuple(f[v] for v in order) for f in fs}
    assert encode(found) == encode(expected)
    return found


def _witness(choices, order, predicate=lambda f: True):
    coloring = next(f for f in choices if predicate(f))
    return [coloring[v] for v in order]


def _graph(name, n, root_map, extra_edges):
    edges = FRAME | {tuple(sorted(e)) for e in extra_edges}
    roots = tuple(root_map.values())
    assert len(roots) == len(set(roots)) == 2
    interior = set(range(5, n))
    neighbors = _neighbors(n, edges)
    assert set(roots) <= interior
    assert all(len(neighbors[v]) == (5 if v in roots else 4) for v in interior)
    assert len(components(interior, edges)) == 1
    parts = components(interior - set(roots), edges)
    regions = []
    for index, vs in enumerate(parts):
        contacts = {str(r): sorted(neighbors[r] & set(vs)) for r in roots}
        attached = [r for r in roots if contacts[str(r)]]
        assert attached
        order = sorted(set().union(*(set(cs) for cs in contacts.values())))
        regions.append(dict(
            id=index, vertices=vs, kind="mixed" if len(attached) == 2 else "unary",
            owner=attached if len(attached) == 1 else None,
            root_contacts=contacts, contact_order=order,
            incidence_vector=[len(contacts[str(r)]) for r in roots],
            boundary_attachments={str(v): sorted(neighbors[v] & B) for v in vs},
            actual_support=sorted(set().union(*(neighbors[v] & B for v in vs))),
            internal_edges=sorted(e for e in edges if set(e) <= set(vs)),
            incident_edges=sorted(e for e in edges if set(e) & set(vs))))

    rows, deleted_masks = [], {r: 0 for r in roots}
    mask = 0
    comparisons, conditioned_relations = 0, 0
    for row_index, row in enumerate(ROWS):
        boundary = dict(enumerate(row))
        full = _choices(interior, edges, boundary)
        root_relation = sorted({tuple(f[r] for r in roots) for f in full})
        if full:
            mask |= 1 << row_index
        row_record = dict(
            row_index=row_index, row=row, accepted=bool(full),
            root_order=roots, ordered_root_relation=root_relation,
            source_coloring_order=list(range(n)),
            source_tuple_witnesses=[dict(tuple=t, coloring=_witness(
                full, range(n), lambda f, t=t: tuple(f[r] for r in roots) == t))
                for t in root_relation], root_deletions=[])
        for deleted in roots:
            survivor, = [r for r in roots if r != deleted]
            remaining = interior - {deleted}
            child_edges = {e for e in edges if deleted not in e}
            deleted_choices = _choices(remaining, child_edges, boundary)
            actual = {f[survivor] for f in deleted_choices}
            if deleted_choices:
                deleted_masks[deleted] |= 1 << row_index

            # Only the surviving root's original unary components constrain it.
            side_regions = [region for region in regions
                            if region["root_contacts"][str(survivor)]
                            and not region["root_contacts"][str(deleted)]]
            side_interior = {survivor} | set().union(
                *(set(region["vertices"]) for region in side_regions))
            side_edges = {e for e in child_edges if set(e) <= B | side_interior}
            side_choices = _choices(side_interior, side_edges, boundary)
            expected = {f[survivor] for f in side_choices}
            assert actual == expected
            comparisons += 1
            child_order = sorted(B | remaining)
            side_order = sorted(B | side_interior)

            # Every value of the other root uses the same boundary row.  In a
            # mixed component deletion leaves slack even when that root value
            # is unavailable in the surviving unary side.
            records = []
            for region in regions:
                conditioned = []
                local_edges = FRAME | {e for e in child_edges
                                       if set(e) & set(region["vertices"])}
                for other_color in sorted(U):
                    fixed = boundary | {survivor: other_color}
                    local = _choices(region["vertices"], local_edges, fixed)
                    relation = sorted({tuple(f[v] for v in region["contact_order"])
                                       for f in local})
                    if region["root_contacts"][str(deleted)]:
                        assert relation
                    conditioned.append(dict(
                        other_root=survivor, other_root_color=other_color,
                        ordered_contact_relation=relation,
                        coloring_order=region["vertices"],
                        tuple_witnesses=[dict(tuple=t, coloring=_witness(
                            local, region["vertices"], lambda f, t=t:
                            tuple(f[v] for v in region["contact_order"]) == t))
                            for t in relation]))
                    conditioned_relations += 1
                records.append(dict(
                    original_component=region["id"],
                    contact_order=region["contact_order"],
                    component_edges_after_root_deletion=sorted(local_edges),
                    conditioned_other_root_relations=conditioned))
            row_record["root_deletions"].append(dict(
                deleted_root=deleted, surviving_root=survivor,
                root_deleted_edges=sorted(child_edges),
                root_deleted_coloring_order=child_order,
                unary_side_original_components=[region["id"] for region in side_regions],
                unary_side_interior=sorted(side_interior),
                unary_side_edges=sorted(side_edges),
                unary_side_coloring_order=side_order,
                root_deleted_colors=sorted(actual), unary_side_colors=sorted(expected),
                accepted=bool(deleted_choices),
                root_deleted_color_witnesses=[dict(
                    root_color=c, coloring=_witness(deleted_choices, child_order,
                                                   lambda f, c=c: f[survivor] == c))
                    for c in sorted(actual)],
                unary_side_color_witnesses=[dict(
                    root_color=c, coloring=_witness(side_choices, side_order,
                                                   lambda f, c=c: f[survivor] == c))
                    for c in sorted(expected)],
                original_component_relations=records))
        rows.append(row_record)
    return dict(
        name=name, vertices=n, boundary=sorted(B), root_map=root_map,
        root_order=roots, roots_adjacent=tuple(sorted(roots)) in edges,
        edges=sorted(edges), degrees={str(v): len(neighbors[v]) for v in interior},
        excess=sum(len(neighbors[v]) - 4 for v in interior),
        root_boundary_attachments={str(r): sorted(neighbors[r] & B) for r in roots},
        original_components=regions, sigma=mask,
        root_deleted_sigmas={str(r): deleted_masks[r] for r in roots},
        rows=rows, equality_checks=comparisons,
        conditioned_component_relation_checks=conditioned_relations,
        evidence_scope="Fixed exact coloring controls; no disk, minimality, or candidate claim.")


def build():
    """Return three fixed same-source controls with complete canonical rows."""
    assert len(ROWS) == 10 and T4 == 932
    graphs = [
        _graph("adjacent_roots_one_shared_contact", 8, {"z": 5, "w": 6},
               [(5, 6), (5, 7), (6, 7)]
               + [(5, b) for b in (0, 1, 4)]
               + [(6, b) for b in (0, 2, 3)]
               + [(7, b) for b in (1, 4)]),
        _graph("nonadjacent_roots_four_spokes", 8, {"z": 5, "w": 6},
               [(5, 7), (6, 7)]
               + [(5, b) for b in (0, 1, 2, 3)]
               + [(6, b) for b in (0, 1, 2, 4)]
               + [(7, b) for b in (1, 3)]),
        _graph("nonadjacent_roots_degree_four_unary_edge_exception", 10,
               {"z": 5, "w": 6},
               [(5, 7), (6, 7), (5, 8), (6, 9)]
               + [(5, b) for b in (0, 1, 4)]
               + [(6, b) for b in (0, 2, 3)]
               + [(7, b) for b in (1, 3)]
               + [(8, b) for b in (2, 3, 4)]
               + [(9, b) for b in (0, 1, 4)]),
    ]
    assert graphs[0]["root_deleted_sigmas"] == {"5": 1023, "6": 1023}
    q_index = ROWS.index((0, 1, 0, 1, 2))
    assert graphs[2]["root_deleted_sigmas"]["5"] >> q_index & 1
    assert not (graphs[2]["root_deleted_sigmas"]["6"] >> q_index & 1)
    return dict(
        boundary_pattern_order=ROWS, root_color_frame=sorted(U),
        named_source_controls=graphs,
        root_deletion_unary_side_equality_checks=sum(g["equality_checks"] for g in graphs),
        conditioned_component_relation_checks=sum(
            g["conditioned_component_relation_checks"] for g in graphs),
        scope="Three fixed epsilon-two graphs; complete tuples and witnesses, no source-family enumeration.")
