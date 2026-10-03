#!/usr/bin/env python3
"""Original path/root-edge K5 certificates, with complete ordered color pairs.

Eight inherited degree-four disk path bases and fixed run expansions are
controls for the paper argument. No marker compression or source census.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, T4, U, components
from c5_941_two_spoke import Q4, check_rotation, search

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_path_edge/observations.json'
ODD = ROOT / 'artifacts/c5_odd_join_cores/observations.json'
TREE = ROOT / 'artifacts/c5_tree_cores/observations.json'


def encoded(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1) + '\n'


def path_edges(neighborhoods):
    return (FRAME | {(5+i, 6+i) for i in range(len(neighborhoods)-1)}
            | {(b, 5+i) for i, ns in enumerate(neighborhoods) for b in ns})


def inherited_bases():
    odd, tree = json.loads(ODD.read_text()), json.loads(TREE.read_text())
    bases = []
    for case in odd['cases'][:2]:
        for old in case['disk_templates']:
            if old['kind'] not in ('K5', 'I'):
                continue
            edges = set(map(tuple, old['edges']))
            path = old['path']
            assert path == list(range(5, 5+len(path)))
            ns = [sorted(b for b in B if (b, v) in edges) for v in path]
            assert path_edges(ns) == edges
            bases.append(dict(input_path=str(ODD.relative_to(ROOT)),
                input_case_length=case['length'], input_index=old['index'],
                family='empty' if len(path) == 2 else 'one_run',
                neighborhoods=ns, apex_rotation=old['apex_rotation']))
    for index, old in enumerate(tree['path_minors']['templates']):
        if old['disk']:
            ns = old['neighborhoods']
            assert path_edges(ns) == set(map(tuple, old['edges']))
            bases.append(dict(input_path=str(TREE.relative_to(ROOT)),
                input_index=index, family='two_runs', neighborhoods=ns,
                apex_rotation=old['topology']['apex_rotation']))
    assert Counter(b['family'] for b in bases) == {
        'empty': 6, 'one_run': 8, 'two_runs': 2}
    reconstructed, selected = Counter(), []
    for base in bases:
        ns = base['neighborhoods']
        edges, n = path_edges(ns), 5+len(ns)
        assert all(sum(v in e for e in edges) == 4 for v in range(5, n))
        base['apex_faces'] = check_rotation(n, edges, base['apex_rotation'])
        rows = [list(search(range(5, n), edges, dict(enumerate(row)))) for row in ROWS]
        mask = sum(1 << i for i, full in enumerate(rows) if full)
        reconstructed[mask] += 1
        if mask & T4 != T4:
            continue
        assert mask == 1022
        assert all(4 in support and set(support)-{4} for support in ns)
        base['q4_critical_witnesses'] = []
        for edge in sorted(edges-FRAME):
            witness = next(search(range(5, n), edges-{edge}, dict(enumerate(Q4))), None)
            assert witness is not None
            base['q4_critical_witnesses'].append(dict(
                edge=edge, coloring=[witness[v] for v in range(n)]))
        selected.append(base)
    assert Counter(b['family'] for b in selected) == {
        'empty': 2, 'one_run': 4, 'two_runs': 2}
    return selected, dict(saved_disk_paths=16, reconstructed_Sigma_histogram=dict(sorted(reconstructed.items())))


def connected(vertices, edges):
    return len(components(set(vertices), edges)) == 1


def verify_k5(edges, branch_sets):
    """Check an explicit minor in the original apex edge set, not a quotient oracle."""
    sets = [set(vs) for vs in branch_sets]
    assert len(sets) == 5 and all(sets)
    assert sum(map(len, sets)) == len(set().union(*sets))
    assert all(connected(vs, edges) for vs in sets)
    links = []
    for i, j in combinations(range(5), 2):
        edge = next(e for e in sorted(edges)
                    if (e[0] in sets[i] and e[1] in sets[j])
                    or (e[1] in sets[i] and e[0] in sets[j]))
        links.append(dict(branch_pair=[i, j], original_edge=edge))
    return dict(model='K5', branch_sets=branch_sets, links=links)


def cycle_certificate(n, augmented, pair):
    z, w = pair
    # The whole original z--w path remains. Three connected cycle pieces
    # are pairwise joined by z's path edge, w's path edge, and original zw.
    branch_sets = [[z], list(range(z+1, w)), [w], [4],
                   sorted((B-{4}) | {n})]
    apex_edges = augmented | {(b, n) for b in B}
    return verify_k5(apex_edges, branch_sets)


def dynamic_pairs(ns, pair, row):
    """Complete pair relation with full original-path witnesses in one color frame."""
    # States remember both named marker colors; no independent marginal join.
    states = {(None, None, None): ()}
    for v, support in enumerate(ns, 5):
        following = {}
        for (last, a, b), witness in sorted(states.items(), key=lambda t: repr(t[0])):
            for color in sorted(U-{row[j] for j in support}):
                if color == last:
                    continue
                key = (color, color if v == pair[0] else a,
                       color if v == pair[1] else b)
                following.setdefault(key, witness+(color,))
        states = following
    witnesses = {}
    for (_, a, b), witness in sorted(states.items()):
        witnesses.setdefault((a, b), witness)
    return witnesses


def original_components(ns, edges, pair):
    regions = []
    for index, vs in enumerate(components(set(range(5, 5+len(ns)))-set(pair), edges)):
        contacts = [[v for v in vs if tuple(sorted((r, v))) in edges] for r in pair]
        attached = [r for r, cs in zip(pair, contacts, strict=True) if cs]
        regions.append(dict(id=index, vertices=vs, root_contacts=contacts,
            contact_order=sorted(set().union(*map(set, contacts))),
            ownership=attached, kind='mixed' if len(attached) == 2 else 'unary',
            boundary_attachments=[dict(vertex=v, neighbors=ns[v-5]) for v in vs],
            actual_support=sorted(set().union(*(set(ns[v-5]) for v in vs))),
            original_edges=sorted(e for e in edges if set(e) & set(vs))))
    assert sum(r['kind'] == 'mixed' for r in regions) == 1
    return regions


def path_control(base_index, base, lengths):
    old = base['neighborhoods']
    supports = ([] if base['family'] == 'empty' else [old[1]]
                if base['family'] == 'one_run' else [old[1], old[3]])
    assert len(supports) == len(lengths)
    ns = [old[0]]+[s for s, k in zip(supports, lengths, strict=True) for _ in range(k)]+[old[-1]]
    edges, n = path_edges(ns), 5+len(ns)
    assert all(4 in support and set(support)-{4} for support in ns)
    assert all(sum(v in e for e in edges) == 4 for v in range(5, n))
    full_rows = []
    for row in ROWS:
        full = list(search(range(5, n), edges, dict(enumerate(row))))
        full_rows.append(full)
    assert sum(1 << i for i, full in enumerate(full_rows) if full) == 1022
    restorations = []
    for pair in combinations(range(5, n), 2):
        if pair in edges:
            continue
        augmented = edges | {pair}
        assert all(sum(v in e for e in augmented) == (5 if v in pair else 4)
                   for v in range(5, n))
        certificate = cycle_certificate(n, augmented, pair)
        records = []
        for row, full in zip(ROWS, full_rows, strict=True):
            witnesses = dynamic_pairs(ns, pair, row)
            relation = sorted(witnesses)
            assert set(relation) == {tuple(f[v] for v in pair) for f in full}
            retained = [t for t in relation if t[0] != t[1]]
            direct = list(search(range(5, n), augmented, dict(enumerate(row))))
            assert set(retained) == {tuple(f[v] for v in pair) for f in direct}
            for t, coloring in witnesses.items():
                fixed = dict(enumerate(row)) | dict(zip(range(5, n), coloring, strict=True))
                assert tuple(fixed[v] for v in pair) == t
                assert all(fixed[a] != fixed[b] for a, b in edges)
            records.append(dict(ordered_root_pair_relation=relation,
                full_original_path_witnesses=[witnesses[t] for t in relation],
                retained_pair_tuple_indices=[i for i, t in enumerate(relation) if t in retained]))
        mask = sum(1 << i for i, r in enumerate(records) if r['retained_pair_tuple_indices'])
        assert mask & T4 != T4 or mask == 1022
        restorations.append(dict(original_root_edge=pair, original_path_positions=[v-5 for v in pair],
            port_order=pair, original_components=original_components(ns, augmented, pair),
            original_cycle=list(range(pair[0], pair[1]+1)),
            apex_k5_minor=certificate, sigma=mask, rows=records))
    return dict(base=base_index, run_lengths=lengths, vertices=n, interior_order=list(range(5, n)),
        neighborhoods=ns, edges=sorted(edges), sigma=1022, common_boundary_hub=4,
        second_original_boundary_neighbors=[min(set(s)-{4}) for s in ns],
        edge_restorations=restorations)


def build():
    bases, source_domain = inherited_bases()
    controls = []
    for i, base in enumerate(bases):
        lengths = ([()] if base['family'] == 'empty' else [(2,), (6,)]
                   if base['family'] == 'one_run' else [(2, 2), (4, 6)])
        controls.extend(path_control(i, base, ls) for ls in lengths)
    restorations = [r for c in controls for r in c['edge_restorations']]
    histogram = Counter(r['sigma'] for r in restorations)
    dependencies = [Path(__file__).resolve(), ROOT / 'scripts/c5_independent_support_capacity.py',
                    ROOT / 'scripts/c5_941_two_spoke.py', ODD, TREE]
    return dict(schema=1,
        scope='Original-graph K5 minor and ordered pair controls. Arbitrary-length coverage is the inherited path classification plus the paper cycle lemma, not a marked compression or graph census.',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in dependencies},
        boundary_order=sorted(B), pattern_order=ROWS, root_color_frame=sorted(U), normalized_q=Q4,
        tuple_witness_semantics='A row precedes the complete interior witness in interior_order; marker pair and all original attachments use this literal frame.',
        source_domain=source_domain, inherited_bases=bases, original_path_controls=controls,
        summary=dict(inherited_path_bases=len(bases), fixed_original_paths=len(controls),
            original_edge_restorations=len(restorations), apex_k5_minors=len(restorations),
            complete_pair_row_queries=10*len(restorations),
            restored_Sigma_histogram=dict(sorted(histogram.items())),
            T4_preserving_restorations=sum(count for mask, count in histogram.items() if mask & T4 == T4),
            candidate_sources=0))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    result = encoded(data)
    if args.check:
        assert OUT.read_text() == result, 'certificate differs; regenerate intentionally'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(result)
    print(json.dumps(dict(status='checked' if args.check else 'written', **data['summary']), sort_keys=True))


if __name__ == '__main__':
    main()
