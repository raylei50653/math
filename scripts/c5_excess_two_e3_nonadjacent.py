#!/usr/bin/env python3
"""E3 nonadjacent-root necessary forms and fixed positive controls.

No graph search, Four Color Theorem oracle, or source-realizability decision is
used.  The finite incidence audit is arithmetic on the two root degrees; its
survivors are necessary forms, not graphs.  Python checks the stated fixed
controls and local identities.  The arbitrary-size topological/Gallai steps
remain the paper arguments in nonadjacent_notes.md and the E3 report.

Writes use exclusive create.  Replays read tracked cells.json and this script;
there is no dependency on ignored historical artifacts.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'artifacts/c5_excess_two_e3/nonadjacent.json'
B = frozenset(range(5))
U = frozenset(range(4))
FRAME = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in range(5))
T4 = frozenset((2, 5, 7, 8, 9))
SELECTED = frozenset((1, 4, 6))
SINGLETON = {0: 4, 1: 3, 3: 2, 4: 1, 6: 0}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def neighbors(vertices, edges):
    return {v: {b if a == v else a for a, b in edges if v in (a, b)}
            for v in vertices}


def components(vertices, edges):
    vertices = set(vertices)
    ns = neighbors(vertices, [e for e in edges if set(e) <= vertices])
    out = []
    while vertices:
        pending = [min(vertices)]
        got = set()
        while pending:
            v = pending.pop()
            if v in got:
                continue
            got.add(v)
            pending.extend(sorted(ns[v] - got, reverse=True))
        vertices -= got
        out.append(sorted(got))
    return out


def full_colorings(vertices, edges, fixed):
    """Enumerate the literal finite assignments with deterministic MRV."""
    vertices = set(vertices)
    ns = neighbors(vertices | set(fixed), edges)
    f = dict(fixed)
    found = []
    def rec():
        left = vertices - set(f)
        if not left:
            found.append(dict(f))
            return
        options = {v: sorted(U - {f[n] for n in ns[v] if n in f})
                   for v in left}
        v = min(left, key=lambda v: (len(options[v]), -len(ns[v]), v))
        for c in options[v]:
            f[v] = c
            rec()
        f.pop(v, None)
    if all(a not in f or b not in f or f[a] != f[b] for a, b in edges):
        rec()
    return sorted(found, key=lambda f: tuple(f[v] for v in sorted(vertices)))


def verify_coloring(edges, row, order, colors):
    f = dict(zip(order, colors))
    assert [f[i] for i in range(5)] == list(row)
    assert all(f[a] != f[b] for a, b in edges)


def sigma_and_witnesses(vertices, edges, rows):
    choices = [full_colorings(vertices - B, edges, dict(enumerate(row)))
               for row in rows]
    return sum((1 << i) for i, fs in enumerate(choices) if fs), choices


def projection_witnesses(choices, roles, order):
    witnesses = {}
    for f in choices:
        key = tuple(f[v] for v in roles)
        witnesses.setdefault(key, [f[v] for v in order])
    return [dict(tuple=list(key), coloring=witnesses[key])
            for key in sorted(witnesses)]


def control(mask, cell, rows):
    vertices = set(range(5 + cell['k_eff']))
    private = vertices - B
    edges = FRAME | {tuple(sorted(e)) for e in cell['edges']}
    ns = neighbors(vertices, edges)
    degree = {v: len(ns[v]) for v in private}
    roots = sorted(v for v in private if degree[v] >= 5)
    assert all(d >= 4 for d in degree.values())
    assert sum(d - 4 for d in degree.values()) == 2
    assert len(components(private, edges)) == 1
    assert set().union(*(ns[v] & B for v in private)) == B
    assert all(len(ns[v] & B) <= 3 for v in private)
    assert ([degree[v] for v in roots] == [6] if mask == 951
            else [degree[v] for v in roots] == [5, 5])
    actual, choices = sigma_and_witnesses(vertices, edges, rows)
    assert actual == mask and all(choices[i] for i in T4)
    assert any(choices[i] for i in SELECTED), 'Positive control must avoid selected triple.'
    q = sorted(SINGLETON[i] for i, fs in enumerate(choices) if not fs)
    pieces = []
    for j, pvs in enumerate(components(private - set(roots), edges)):
        vs = set(pvs)
        rcontacts = {str(r): sorted(ns[r] & vs) for r in roots}
        owners = [r for r in roots if rcontacts[str(r)]]
        contact_order = sorted(set().union(*(set(xs) for xs in rcontacts.values())))
        support = sorted(set().union(*(ns[v] & B for v in vs)))
        outside = private - vs
        one_sided = bool(outside) and len(components(outside, edges)) == 1
        assert owners
        if len(owners) == 1:
            assert one_sided
            assert not any(set(support) <= set(e) for e in FRAME)
        if one_sided and len(owners) == 2:
            assert support, 'Empty-support one-sided mixed cannot be critical.'
        piece = dict(id=f'P{j}', vertices=pvs, root_contacts=rcontacts,
                     contact_order=contact_order, adjacent_roots=owners,
                     kind='unary' if len(owners) == 1 else 'mixed',
                     actual_support=support, one_sided=one_sided,
                     boundary_attachments={str(v): sorted(ns[v] & B) for v in pvs},
                     original_internal_edges=[list(e) for e in sorted(edges) if set(e) <= vs],
                     original_incident_edges=[list(e) for e in sorted(edges) if set(e) & vs])
        # A literal single tuple includes a shared contact only once.
        local_edges = {e for e in edges if set(e) & vs}
        relations = []
        for i, row in enumerate(rows):
            all_local = full_colorings(vs, local_edges, dict(enumerate(row)))
            tuples = projection_witnesses(all_local, contact_order, pvs)
            assert tuples
            conditioned = []
            for root_values in product(range(4), repeat=len(owners)):
                fixed = dict(enumerate(row)) | dict(zip(owners, root_values))
                fs = full_colorings(vs, local_edges, fixed)
                conditioned.append(dict(root_order=owners, root_tuple=list(root_values),
                    full_contact_tuples=projection_witnesses(fs, contact_order, pvs)))
            relations.append(dict(row_index=i, row=list(row),
                unconditioned_contact_tuples=tuples, conditioned_relations=conditioned))
        piece['rows'] = relations
        pieces.append(piece)
    assert sum(p['kind'] == 'unary' for p in pieces) <= 2
    records = []
    for i, row in enumerate(rows):
        full = choices[i]
        order = sorted(vertices)
        joint = projection_witnesses(full, roots, order)
        for rec in joint:
            verify_coloring(edges, row, order, rec['coloring'])
        deletions = []
        for deleted in roots:
            child_vertices = vertices - {deleted}
            child_edges = {e for e in edges if deleted not in e}
            child = full_colorings(child_vertices - B, child_edges, dict(enumerate(row)))
            surviving = [r for r in roots if r != deleted]
            kept_pieces = [p for p in pieces if p['adjacent_roots'] == surviving]
            side_private = set(surviving) | {v for p in kept_pieces for v in p['vertices']}
            side_vertices = B | side_private
            side_edges = {e for e in edges if set(e) <= side_vertices}
            side = full_colorings(side_private, side_edges, dict(enumerate(row)))
            # Empty root tuple is the exact single-root deletion case.
            cp = projection_witnesses(child, surviving, sorted(child_vertices))
            sp = projection_witnesses(side, surviving, sorted(side_vertices))
            assert [r['tuple'] for r in cp] == [r['tuple'] for r in sp]
            deletions.append(dict(deleted_root=deleted, surviving_root_order=surviving,
                child_vertices=sorted(child_vertices), child_edges=[list(e) for e in sorted(child_edges)],
                unary_side_vertices=sorted(side_vertices),
                unary_side_edges=[list(e) for e in sorted(side_edges)],
                child_root_tuple_witnesses=cp, unary_side_root_tuple_witnesses=sp))
        records.append(dict(row_index=i, row=list(row), accepted=bool(full),
                            full_coloring_order=order, root_order=roots,
                            root_tuple_witnesses=joint, root_deletions=deletions))
    criticality = []
    for e in sorted(edges - FRAME):
        child_sigma, child_choices = sigma_and_witnesses(vertices, edges - {e}, rows)
        gained = [i for i in range(10) if child_sigma >> i & 1 and not mask >> i & 1]
        assert gained
        i = gained[0]
        f = child_choices[i][0]
        assert f[e[0]] == f[e[1]]
        witness = [f[v] for v in sorted(vertices)]
        verify_coloring(edges - {e}, rows[i], sorted(vertices), witness)
        criticality.append(dict(deleted_edge=list(e), child_sigma=child_sigma,
                                all_new_row_indices=gained, witness_row_index=i,
                                full_coloring_order=sorted(vertices), coloring=witness))
    return dict(name=f'cells-E1-scratch-Sigma-{mask}', source_cell_pointer=f'/cells/{mask}',
        vertices=sorted(vertices), frame_edges=[list(e) for e in sorted(FRAME)],
        nonframe_edges=[list(e) for e in sorted(edges - FRAME)],
        epsilon=2, degrees={str(v): degree[v] for v in sorted(private)}, roots=roots,
        roots_adjacent=len(roots) == 2 and tuple(roots) in edges,
        source_sigma=mask, Q=q, selected_triple_rejected=False,
        original_components=pieces, complete_rows=records, criticality=criticality,
        applicable_generic_assertions=['degree>=4', 'spokes<=3', 'H-connected',
            'all-five-framework-contacts', 'unary-one-sided', 'at-most-two-unaries',
            'critical-unary-not-short', 'empty-support-one-sided-mixed-absent',
            'exact-root-deletion-unary-side-joint'],
        scope='Fixed positive control; arbitrary-size lemmas remain paper results.')


def compositions(n, k):
    if k == 0:
        if n == 0:
            yield ()
    elif k == 1:
        if n >= 1:
            yield (n,)
    else:
        for a in range(1, n - k + 2):
            for tail in compositions(n - a, k - 1):
                yield (a,) + tail


def incidence_audit():
    """Check small degree arithmetic, with no graph/row/relation enumeration."""
    histogram = Counter()
    signature_count = Counter()
    profile_count = 0
    omitted_mixed_44 = Counter()
    payloads = []
    for m in range(1, 6):
        for u in range(3):
            for owners in product(range(2), repeat=u):
                for capacities in product(range(1, 5), repeat=u):
                    unary = [sum(c for o, c in zip(owners, capacities) if o == r)
                             for r in range(2)]
                    for spokes in product(range(4), repeat=2):
                        for zcs in compositions(5 - spokes[0] - unary[0], m):
                            for wcs in compositions(5 - spokes[1] - unary[1], m):
                                vectors = list(zip(zcs, wcs))
                                profile_count += 1
                                histogram[f'mixed={m},unary={u}'] += 1
                                factors = [(f'z-spoke-{j}', (1, 0)) for j in range(spokes[0])]
                                factors += [(f'w-spoke-{j}', (0, 1)) for j in range(spokes[1])]
                                factors += [(f'U{j}', (c, 0) if o == 0 else (0, c))
                                            for j, (o, c) in enumerate(zip(owners, capacities))]
                                factors += [(f'C{j}', v) for j, v in enumerate(vectors)]
                                # Degree loss is at most one per retained degree-five root.
                                # At most two factors can be omitted under that budget.
                                for n_omitted in range(3):
                                    for omitted in combinations(factors, n_omitted):
                                        lost = tuple(sum(v[r] for _, v in omitted) for r in range(2))
                                        if max(lost) > 1:
                                            continue
                                        names = tuple(name for name, _ in omitted)
                                        retained_mixed = m - sum(name.startswith('C') for name in names)
                                        if retained_mixed == 0:
                                            # Nonadjacent roots cannot be connected in this core.
                                            continue
                                        core_degrees = (5 - lost[0], 5 - lost[1])
                                        if core_degrees == (5, 5):
                                            assert not names
                                        elif core_degrees in ((4, 5), (5, 4)):
                                            assert len(names) == 1 and not names[0].startswith('C')
                                            assert omitted[0][1] in ((1, 0), (0, 1))
                                        elif core_degrees == (4, 4):
                                            if any(name.startswith('C') for name in names):
                                                assert len(names) == 1 and omitted[0][1] == (1, 1)
                                                omitted_mixed_44[str(m)] += 1
                                            else:
                                                assert len(names) == 2
                                                assert sorted(v for _, v in omitted) == [(0, 1), (1, 0)]
                                        else:
                                            raise AssertionError(core_degrees)
                                        signature_count[str(core_degrees)] += 1
                                payloads.append(dict(mixed_vectors=[list(v) for v in vectors],
                                    unary_owners=list(owners), unary_capacities=list(capacities),
                                    root_spoke_counts=list(spokes)))
    assert profile_count == 1284
    assert omitted_mixed_44.get('1', 0) == 0
    canonical = json.dumps(payloads, sort_keys=True, separators=(',', ':')).encode()
    return dict(scope='Finite integer arithmetic only: no graph keys, Sigma search, or realizability claim.',
        root_degrees=[5, 5], roots_adjacent=False, maximal_spokes=3, maximal_unary_pieces=2,
        labelled_incidence_profiles=profile_count, profile_histogram=dict(sorted(histogram.items())),
        valid_omission_signature_counts=dict(sorted(signature_count.items())),
        mixed_omission_44_by_original_mixed_count=dict(sorted(omitted_mixed_44.items())),
        canonical_profile_stream_sha256=digest(canonical),
        assertions=['(5,5) means full source', '(4,5)/(5,4) omit one one-sided unit factor',
            '(4,4) omit one unit factor per side or one (1,1) mixed',
            'sole mixed cannot be omitted while both nonadjacent roots remain'])


def hub_path_controls():
    # Abstract external paths certify actual hub connectivity/adjacency only.
    # They do not certify a degree-four rejecting piece or a source graph.
    controls = []
    for path in ([5, 6], [5, 7, 6], [5, 7, 8, 6], [5, 7, 8, 9, 6]):
        path_edges = {tuple(sorted(e)) for e in zip(path, path[1:])}
        for colors in product(range(4), repeat=2):
            if colors[0] == colors[1]:
                hubs = [path]
                boundary_colors = [colors[0]]
            else:
                hubs = [path[:-1], [path[-1]]]
                boundary_colors = list(colors)
            assert all(len(components(hub, path_edges)) == 1 for hub in hubs)
            assert sum(len(hub) for hub in hubs) == len(set().union(*(set(h) for h in hubs)))
            assert len(hubs) == 1 or any(a in hubs[0] and b in hubs[1] or
                                        b in hubs[0] and a in hubs[1] for a, b in path_edges)
            assert len(set(boundary_colors)) == len(hubs)
            assert all(len(set(hub) & {5, 6}) == 1 for hub in hubs) if len(hubs) == 2 else True
            controls.append(dict(original_path=path, path_edges=[list(e) for e in sorted(path_edges)],
                                 root_order=[5, 6], root_colors=list(colors), hubs=hubs,
                                 hub_contact_colors=boundary_colors))
    return dict(scope='64 fixed literal path/color constructions; checks hub bags only, not Gallai or planarity.',
                controls=controls, count=len(controls))


def build():
    cells_path = ROOT / 'artifacts/c5_cells/cells.json'
    raw = cells_path.read_bytes()
    cells = json.loads(raw)
    rows = [tuple(row) for row in cells['pattern_order']]
    assert len(rows) == 10
    assert {SINGLETON[i] for i in SELECTED} == {0, 1, 3}
    return dict(schema_version=1, task='E3 nonadjacent necessary forms and positive controls',
        sources={'artifacts/c5_cells/cells.json': {'sha256': digest(raw), 'bytes': len(raw)},
                 'scripts/c5_excess_two_e3_nonadjacent.py': {
                     'sha256': digest(Path(__file__).read_bytes()), 'bytes': Path(__file__).stat().st_size}},
        pattern_order=[list(row) for row in rows], T4_indices=sorted(T4),
        selected_rejected_row_indices=sorted(SELECTED), selected_singleton_positions=[0, 1, 3],
        positive_controls=[control(mask, cells['cells'][str(mask)], rows) for mask in (951, 935)],
        degree_omission_arithmetic=incidence_audit(), empty_support_hub_path_controls=hub_path_controls(),
        branch_status={
            'nonadjacent_no_mixed': 'excluded by H connectivity; no selected row identities used',
            'three_or_more_unaries': 'excluded by common 2+2+2>5 shield budget; no selected row identities used',
            'one_sided_mixed_empty_support': 'excluded by connected external path plus hub principle; no selected row identities used',
            'single_mixed_separating': 'open; mixed shield/hub path cannot be charged without extra proof',
            'multiple_mixed_44_core': 'at most two original mixed; exactly one retained mixed; source exclusion open',
            'multiple_mixed_45_54_core': 'open original single-side unit omission with all mixed retained',
            'full_source_55_core': 'open, preserving original graph and all contact relations'},
        evidence_boundary='No arbitrary-size source exclusion beyond the stated paper lemmas; no finite empty-domain inference.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--output', type=Path, default=DEFAULT)
    args = parser.parse_args()
    result = build()
    text = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert args.output.read_text() == text, 'Exact artifact replay failed.'
        print('CHECK OK: E3 nonadjacent arithmetic, literal tuples, two positive controls, and 64 hub path bags')
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as f:
            f.write(text)
        print(f'GENERATED: {args.output}; bytes={len(text.encode())}; sha256={digest(text.encode())}')
    print('BRANCH STATUS: separating mixed, proper (4,4)/(4,5)/(5,4), and original (5,5) remain open')


if __name__ == '__main__':
    main()
