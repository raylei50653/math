#!/usr/bin/env python3
"""Original omission identities and two spoke restorations at a mixed core.

The fixed domain is inherited degree-four cores, with both original roots on
one triangle. Paper coverage keeps their joint relation and all original
attachments. This is not a census of epsilon-two source graphs.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, T4, U, components
from c5_941_two_spoke import Q4, base_record, relabel_mask, search
from c5_941_three_spoke import bare_triangles
from c5_excess_two_triangle_edge import graph, inherited_bases

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_spokes/observations.json'
BRANCHES = ROOT / 'artifacts/c5_triangle_branches/observations.json'
PATHS = ROOT / 'artifacts/c5_triangle_path_reduction/observations.json'
DOUBLE = ROOT / 'artifacts/c5_two_triangle_blocks/observations.json'


def encoded(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1) + '\n'


def partitions(n, minimum=1):
    if n == 0:
        yield ()
    for first in range(minimum, n + 1):
        for rest in partitions(n - first, first):
            yield (first,) + rest


def omission_controls():
    """All budget-four sides with exactly one named mixed component.

    These are incidence identities only; no abstract entry is asserted to be
    a graph, boundary support, or realizable relation.
    """
    records, total = [], 0
    for k, ell in product(range(1, 5), repeat=2):
        for tz, tw in product(range(5-k), range(5-ell)):
            for pz, pw in product(tuple(partitions(4-k-tz)),
                                  tuple(partitions(4-ell-tw))):
                factors = [dict(id='C', kind='mixed', incidence=[k, ell])]
                for side, t, partition in ((0, tz, pz), (1, tw, pw)):
                    for i in range(t):
                        v = [0, 0]
                        v[side] = 1
                        factors.append(dict(id=f'{side}:spoke:{i}', kind='spoke', incidence=v))
                    for i, size in enumerate(partition):
                        v = [0, 0]
                        v[side] = size
                        factors.append(dict(id=f'{side}:unary:{i}', kind='unary', incidence=v))
                assert [sum(f['incidence'][s] for f in factors) for s in (0, 1)] == [4, 4]
                unit = [[f['id'] for f in factors if f['incidence'] == v]
                        for v in ([1, 0], [0, 1])]
                expected = {(): (5, 5)}
                expected.update({(f,): (4, 5) for f in unit[0]})
                expected.update({(f,): (5, 4) for f in unit[1]})
                expected.update({tuple(sorted((f, g))): (4, 4)
                                 for f, g in product(*unit)})
                if (k, ell) == (1, 1):
                    expected[('C',)] = (4, 4)
                actual = {}
                for mask in range(1 << len(factors)):
                    total += 1
                    omitted = [f for j, f in enumerate(factors) if mask >> j & 1]
                    loss = [sum(f['incidence'][s] for f in omitted) for s in (0, 1)]
                    if max(loss) <= 1:
                        actual[tuple(sorted(f['id'] for f in omitted))] = tuple(5-d for d in loss)
                assert actual == expected
                records.append(dict(mixed_incidences=[k, ell], spokes=[tz, tw],
                    unary_partitions=[pz, pw], factors=factors,
                    possible_omissions=[dict(ids=ids, root_degrees=degrees)
                                        for ids, degrees in sorted(actual.items())]))
    return dict(scope='Exhaustive integer incidence identities, not graph or support enumeration',
                configurations=len(records), subset_checks=total, records=records)


def witnesses(interior, edges, row, pair):
    """Independent whole-graph backtracking with one witness for every tuple."""
    result = {}
    for f in search(interior, edges, dict(enumerate(row))):
        result.setdefault(tuple(f[v] for v in pair), [f[v] for v in sorted(B | set(interior))])
    return result


def validate_witness(witness, order, edges, row, pair, value):
    f = dict(zip(order, witness, strict=True))
    assert [f[b] for b in range(5)] == list(row)
    assert all(c in U for c in witness)
    assert all(f[a] != f[b] for a, b in edges)
    assert tuple(f[v] for v in pair) == value


def load_forms():
    single, switches = inherited_bases()
    forms = []
    for index, base in enumerate(single):
        forms.append(dict(base, family='single_triangle', input_index=index))
    for index, other in sorted(switches.items()):
        base = single[index]
        first, leaf = base['neighborhoods'][3:5]
        forms.append(dict(graph(base, [[first, other, other, leaf]]),
                          family='single_triangle_two_runs', input_index=index))
    for base in bare_triangles():
        if base['accepts_T4']:
            forms.append(dict(base, interior_order=list(range(5, base['vertices']))))
    double = json.loads(DOUBLE.read_text())['disk_templates']
    assert len(double) == 128
    for index, base in enumerate(double):
        original_edges = set(map(tuple, base['edges']))
        original_interior = range(5, 5+len(base['neighborhoods']))
        sigma = sum(1 << j for j, row in enumerate(ROWS)
                    if next(search(original_interior, original_edges, dict(enumerate(row))), None))
        assert sigma == base['sigma']
        if sigma != 1022:
            continue
        verified = base_record('double_triangle', index, base)
        forms.append(dict(verified, neighborhoods=base['neighborhoods'],
                          interior_order=list(range(5, verified['vertices']))))
    assert Counter(f['family'] for f in forms) == {
        'single_triangle': 18, 'single_triangle_two_runs': 8,
        'bare_triangle': 36, 'double_triangle': 64}
    return forms


def original_regions(interior, edges, pair):
    result = []
    for index, vs in enumerate(components(set(interior)-set(pair), edges)):
        contacts = [[v for v in vs if tuple(sorted((r, v))) in edges] for r in pair]
        owners = [r for r, cs in zip(pair, contacts, strict=True) if cs]
        assert owners
        support = {v: sorted(b for b in B if (b, v) in edges) for v in vs}
        result.append(dict(id=index, vertices=vs,
            kind='mixed' if len(owners) == 2 else 'unary', owners=owners,
            root_order=pair, root_contacts=contacts,
            contact_order=sorted(set().union(*map(set, contacts))),
            boundary_attachments=support,
            actual_support=sorted(set().union(*map(set, support.values()))),
            internal_edges=sorted(e for e in edges if set(e) <= set(vs)),
            incident_edges=sorted(e for e in edges if set(e) & set(vs))))
    mixed, = [r for r in result if r['kind'] == 'mixed']
    assert mixed['root_contacts'][0] == mixed['root_contacts'][1]
    assert len(mixed['root_contacts'][0]) == 1
    return result


def build():
    orbits = {str(mask): sorted({relabel_mask(mask, [(s*j+t) % 5 for j in range(5)])
        for s in (-1, 1) for t in range(5)}) for mask in (933, 941)}
    targets = set().union(*map(set, orbits.values()))
    forms = load_forms()
    saved, histogram, t4_histogram, n_histogram = [], Counter(), Counter(), Counter()
    cases, queries, omission_queries, long_queries, long_cases = 0, 0, 0, 0, 0
    actual_marginal_collision = None
    for fi, form in enumerate(forms):
        edges = set(map(tuple, form['edges']))
        interior = form['interior_order']
        order = sorted(B | set(interior))
        assert all(sum(v in e for e in edges) == 4 for v in interior)
        assert [[b for b in sorted(B) if (b, v) in edges] for v in interior] == [
        sorted(s) for s in form['neighborhoods']]
        triangles = [t for t in combinations(interior, 3)
                     if all(e in edges for e in combinations(t, 2))]
        root_pairs = sorted({e for t in triangles for e in combinations(t, 2)})
        assert len(root_pairs) == (6 if form['family'] == 'double_triangle' else 3)
        critical = []
        assert not witnesses(interior, edges, Q4, root_pairs[0])
        for edge in sorted(edges-FRAME):
            f = next(search(interior, edges-{edge}, dict(enumerate(Q4))), None)
            assert f is not None
            critical.append(dict(edge=edge, coloring=[f[v] for v in order]))
        marked = []
        for pair in root_pairs:
            z, w = pair
            cut_edges = edges-{pair}
            regions = original_regions(interior, edges, pair)
            ports = list(pair) + sorted(set().union(*(set(r['contact_order']) for r in regions)))
            joint_kernel = [witnesses(interior, cut_edges, row, ports) for row in ROWS]
            kernel = [{t[:2]: f for t, f in ws.items()} for ws in joint_kernel]
            core = [{t: f for t, f in ws.items() if t[0] != t[1]} for ws in kernel]
            for row, rel in zip(ROWS, core, strict=True):
                assert set(rel) == set(witnesses(interior, edges, row, pair))
            assert sum(1 << i for i, rel in enumerate(core) if rel) == 1022
            assert all(kernel)  # q-criticality of the original root edge.
            additions = []
            for bz, bw in product([b for b in sorted(B) if (b, z) not in edges],
                                  [b for b in sorted(B) if (b, w) not in edges]):
                restored = [(bz, z), (bw, w)]
                g_edges = edges | set(restored)
                n_edges = g_edges-{pair}
                rows, masks = [], [0, 0, 0, 0]
                for ri, (row, ws) in enumerate(zip(ROWS, kernel, strict=True)):
                    n_rel = {t: f for t, f in ws.items() if t[0] != row[bz] and t[1] != row[bw]}
                    g_rel = {t: f for t, f in n_rel.items() if t[0] != t[1]}
                    assert set(n_rel) == set(witnesses(interior, n_edges, row, pair))
                    assert set(g_rel) == set(witnesses(interior, g_edges, row, pair))
                    queries += 1
                    for t, f in n_rel.items():
                        validate_witness(f, order, n_edges, row, pair, t)
                    for t, f in g_rel.items():
                        validate_witness(f, order, g_edges, row, pair, t)
                    # Every named subset retains the same original components
                    # and uses the same whole-graph tuple, never marginals.
                    subsets = []
                    for subset in range(4):
                        child_edges = edges | {restored[j] for j in (0, 1) if subset >> j & 1}
                        child = {t: f for t, f in core[ri].items()
                                 if all(t[j] != row[restored[j][0]]
                                        for j in (0, 1) if subset >> j & 1)}
                        assert set(child) == set(witnesses(interior, child_edges, row, pair))
                        omission_queries += 1
                        if child:
                            masks[subset] |= 1 << ri
                        subsets.append(dict(retained_spoke_indices=[j for j in (0, 1)
                            if subset >> j & 1], ordered_relation=sorted(child)))
                    joint = joint_kernel[ri]
                    tuples = sorted(joint)
                    lookup = {t: j for j, t in enumerate(tuples)}
                    rows.append(dict(row_index=ri,
                        N_tuple_indices=[lookup[t] for t in tuples if t[0] != row[bz] and t[1] != row[bw]],
                        G_tuple_indices=[lookup[t] for t in tuples if t[0] != row[bz] and t[1] != row[bw] and t[0] != t[1]],
                        original_spoke_subsets=subsets))
                    if n_rel and not g_rel and len(n_rel) >= 2 and actual_marginal_collision is None:
                        marginals = [{t[j] for t in n_rel} for j in (0, 1)]
                        false_pairs = sorted((a, b) for a, b in product(*map(sorted, marginals)) if a != b)
                        if false_pairs:
                            actual_marginal_collision = dict(form=fi, roots=pair,
                                restored_spokes=restored, row_index=ri,
                                complete_N_relation=sorted(n_rel),
                                tuple_witnesses=[n_rel[t] for t in sorted(n_rel)],
                                false_off_diagonal_pairs=false_pairs)
                sigma, nsigma = masks[3], sum(1 << i for i, row in enumerate(rows) if row['N_tuple_indices'])
                assert masks[0] == 1022 and sigma not in targets
                histogram[sigma] += 1
                t4 = sigma & T4 == T4
                if t4:
                    t4_histogram[sigma] += 1
                    n_histogram[nsigma] += 1
                additions.append(dict(original_omitted_spokes=restored,
                    G_edges=sorted(g_edges), N_edges=sorted(n_edges),
                    G_root_degrees=[5, 5], core_root_degrees=[4, 4],
                    sigma=sigma, N_sigma=nsigma, accepts_T4=t4,
                    original_spoke_subset_sigmas=masks, rows=rows))
                cases += 1
            kernel_rows = []
            for row, ws, joint in zip(ROWS, kernel, joint_kernel, strict=True):
                for value, f in joint.items():
                    validate_witness(f, order, cut_edges, row, ports, value)
                kernel_rows.append(dict(row=row, ordered_relation=sorted(ws),
                    complete_tuple_witnesses=[ws[t] for t in sorted(ws)],
                    complete_joint_port_relation=sorted(joint),
                    complete_joint_tuple_witnesses=[joint[t] for t in sorted(joint)]))
            marked.append(dict(root_order=pair, original_root_edge=pair,
                core_edges=sorted(edges), original_components=regions,
                complete_port_order=ports, source_coloring_order=order,
                root_edge_deleted_kernel=kernel_rows,
                restorations=additions))

        long_control = None
        if form['family'].startswith('single_triangle'):
            tails, branch_sets = [], [[v] for v in form['triangle']]
            next_vertex = 8
            for path in form['branch_paths']:
                tail, start = [], 0
                ns = [form['neighborhoods'][v-5] for v in path]
                while start < len(ns)-1:
                    end = start+1
                    while end < len(ns)-1 and ns[end] == ns[start]:
                        end += 1
                    run = ns[start:end]
                    # X in the inherited switched form remains a singleton.
                    growth = 0 if form['family'].endswith('two_runs') and start == 0 else 2
                    tail.extend(run+[run[-1]]*growth)
                    for j in range(len(run)):
                        size = 1+growth if j == len(run)-1 else 1
                        branch_sets.append(list(range(next_vertex, next_vertex+size)))
                        next_vertex += size
                    start = end
                tail.append(ns[-1])
                branch_sets.append([next_vertex])
                next_vertex += 1
                tails.append(tail)
            long_graph = graph(form, tails)
            long_edges = set(map(tuple, long_graph['edges']))
            mapping = {v: 5+j for j, vs in enumerate(branch_sets) for v in vs}
            mapping.update({b: b for b in B})
            assert set(mapping) == set(range(long_graph['vertices']))
            quotient = {tuple(sorted((mapping[a], mapping[b]))) for a, b in long_edges
                        if mapping[a] != mapping[b]}
            assert quotient == edges
            long_marked = []
            for mark in marked:
                pair = tuple(mark['root_order'])
                assert all(branch_sets[v-5] == [v] for v in pair)
                long_regions = original_regions(long_graph['interior_order'], long_edges, pair)
                long_ports = list(pair) + sorted(set().union(*(
                    set(r['contact_order']) for r in long_regions)))
                long_joint = [witnesses(long_graph['interior_order'], long_edges-{pair}, row, long_ports)
                              for row in ROWS]
                long_kernel = [{t[:2]: f for t, f in ws.items()} for ws in long_joint]
                for row, ws, short in zip(ROWS, long_kernel, mark['root_edge_deleted_kernel'], strict=True):
                    assert sorted(ws) == short['ordered_relation']
                    for value, f in ws.items():
                        validate_witness(f, list(range(long_graph['vertices'])), long_edges-{pair}, row, pair, value)
                    long_queries += 1
                # All four original omission identities and N use these same
                # retained roots, hence equality survives every spoke filter.
                for restoration in mark['restorations']:
                    bz, bw = [e[0] for e in restoration['original_omitted_spokes']]
                    restored_edges = long_edges | set(map(tuple, restoration['original_omitted_spokes']))
                    assert {tuple(sorted((mapping[a], mapping[b]))) for a, b in restored_edges
                            if mapping[a] != mapping[b]} == set(map(tuple, restoration['G_edges']))
                    for row, ws, short in zip(ROWS, long_kernel, restoration['rows'], strict=True):
                        nr = {t for t in ws if t[0] != row[bz] and t[1] != row[bw]}
                        gr = {t for t in nr if t[0] != t[1]}
                        short_tuples = mark['root_edge_deleted_kernel'][short['row_index']]['complete_joint_port_relation']
                        assert nr == {tuple(short_tuples[j][:2]) for j in short['N_tuple_indices']}
                        assert gr == {tuple(short_tuples[j][:2]) for j in short['G_tuple_indices']}
                        long_cases += 1
                long_rows = []
                for row, ws, joint in zip(ROWS, long_kernel, long_joint, strict=True):
                    for value, f in joint.items():
                        validate_witness(f, list(range(long_graph['vertices'])), long_edges-{pair}, row, long_ports, value)
                    long_rows.append(dict(row=row, ordered_relation=sorted(ws),
                        complete_tuple_witnesses=[ws[t] for t in sorted(ws)],
                        complete_joint_port_relation=sorted(joint),
                        complete_joint_tuple_witnesses=[joint[t] for t in sorted(joint)]))
                long_marked.append(dict(root_order=pair, complete_port_order=long_ports,
                    original_components=long_regions, rows=long_rows))
            long_control = dict(original_graph=long_graph, quotient_to_form=mapping,
                interior_branch_sets=branch_sets, retained_triangle=form['triangle'],
                complete_coloring_order=list(range(long_graph['vertices'])), marked_roots=long_marked)
        saved.append(dict(form_id=fi, family=form['family'], input_index=form['input_index'],
            vertices=form['vertices'], interior_order=interior,
            neighborhoods=form['neighborhoods'], edges=sorted(edges), triangles=triangles,
            q4_critical_witnesses=critical, marked_cores=marked, long_control=long_control))
    assert cases == 6068 and queries == 60680 and omission_queries == 242720
    assert actual_marginal_collision is not None
    dependencies = [Path(__file__).resolve(), ROOT/'scripts/c5_excess_two_triangle_edge.py',
                    ROOT/'scripts/c5_941_three_spoke.py', ROOT/'scripts/c5_941_two_spoke.py',
                    ROOT/'scripts/c5_independent_support_capacity.py', BRANCHES, PATHS, DOUBLE]
    controls = omission_controls()
    return dict(schema=1, scope='Original proper-core incidence identities; exclusion of the retained-mixed, two-omitted-spokes branch for fixed 933/941 epsilon-two disk sources. Arbitrary-size coverage is paper, not graph enumeration or Lean.',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in dependencies},
        pattern_order=ROWS, normalized_core_rejection=Q4, target_D5_orbits=orbits,
        tuple_witness_semantics='Indices refer to the complete joint root/contact relation of the root-edge-deleted core kernel in the same row and same literal frame; restoration filters guarantee these complete witnesses also color the named original N/G. Long controls retain their own complete contact relations; only the original triangle/root relation is asserted equal after reduction.',
        original_omission_controls=controls, necessary_forms=saved,
        actual_marginal_collision=actual_marginal_collision,
        summary=dict(necessary_forms=len(forms), reconstructed_double_triangle_inputs=128,
            marked_original_root_edges=sum(len(f['marked_cores']) for f in saved),
            original_spoke_pair_restorations=cases, complete_ten_row_queries=queries,
            complete_original_spoke_subset_queries=omission_queries,
            target_hits=0, Sigma_histogram=dict(sorted(histogram.items())),
            T4_Sigma_histogram=dict(sorted(t4_histogram.items())), T4_N_Sigma_histogram=dict(sorted(n_histogram.items())),
            fixed_original_long_graphs=sum(f['long_control'] is not None for f in saved),
            long_root_pair_queries=long_queries, long_restoration_row_equalities=long_cases,
            integer_identity_configurations=controls['configurations'], integer_subset_checks=controls['subset_checks']))


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
