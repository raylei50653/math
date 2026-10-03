#!/usr/bin/env python3
"""Marked single-triangle root-edge controls in the inherited necessary domain.

Paper coverage retains both original markers. It is not a new graph census.
Same-branch edges have an original K5 minor; the remaining marked normal forms
use complete ordered pairs in one literal boundary/color frame.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, T4, U, components
from c5_941_two_spoke import Q4, check_rotation, search
from c5_excess_two_path_edge import verify_k5

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_triangle_edge/observations.json'
BASE = ROOT / 'artifacts/c5_triangle_branches/observations.json'
PATH = ROOT / 'artifacts/c5_triangle_path_reduction/observations.json'


def encoded(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1) + '\n'


def graph(base, tails):
    ns = [sorted(s) for s in base['neighborhoods'][:3]]
    edges = FRAME | {(5, 6), (5, 7), (6, 7)}
    paths = []
    for slot, tail in enumerate(tails):
        path = list(range(5+len(ns), 5+len(ns)+len(tail)))
        paths.append(path)
        edges |= {(5+slot, path[0])} | set(zip(path, path[1:]))
        ns.extend(sorted(s) for s in tail)
    edges |= {(b, 5+j) for j, support in enumerate(ns) for b in support}
    interior = list(range(5, 5+len(ns)))
    assert all(sum(v in e for e in edges) == 4 for v in interior)
    return dict(vertices=5+len(ns), interior_order=interior,
                triangle=[5, 6, 7], branch_paths=paths,
                neighborhoods=ns, edges=sorted(edges))


def inherited_bases():
    old_bases = json.loads(BASE.read_text())['disk_templates']
    old_switches = json.loads(PATH.read_text())['normal_forms']
    assert len(old_bases) == 18 and len(old_switches) == 8
    bases = []
    for i, old in enumerate(old_bases):
        tails = [old['neighborhoods'][3+2*k:5+2*k]
                 for k in range(len(old['branch_colors']))]
        data = graph(old, tails)
        edges = set(map(tuple, data['edges']))
        assert edges == set(map(tuple, old['edges']))
        data['apex_faces'] = check_rotation(data['vertices'], edges, old['apex_rotation'])
        data['apex_rotation'] = old['apex_rotation']
        data['input_index'] = i
        data['kind'] = old['kind']
        data['branch_colors'] = old['branch_colors']
        data['q4_critical_witnesses'] = []
        for edge in sorted(edges-FRAME):
            full = next(search(data['interior_order'], edges-{edge}, dict(enumerate(Q4))), None)
            assert full is not None
            data['q4_critical_witnesses'].append(dict(
                edge=edge, coloring=[full[v] for v in range(data['vertices'])]))
        mask = sum(1 << j for j, row in enumerate(ROWS)
                   if next(search(data['interior_order'], edges, dict(enumerate(row))), None))
        assert mask == 1022 and mask & T4 == T4
        data['sigma'] = mask
        bases.append(data)
    switches = {}
    for old in old_switches:
        bi, slot = old['base'], old['slot']
        assert slot == 0 and len(bases[bi]['branch_paths']) == 1
        first, other, repeated, leaf = map(sorted, old['neighborhoods'])
        assert other == repeated and first != other
        assert first == bases[bi]['neighborhoods'][3]
        assert leaf == bases[bi]['neighborhoods'][4]
        assert all(4 in s and set(s)-{4} for s in (first, other, leaf))
        data = graph(bases[bi], [[first, other, other, leaf]])
        assert set(map(tuple, data['edges'])) == set(map(tuple, old['edges']))
        check_rotation(data['vertices'], set(map(tuple, data['edges'])),
                       old['topology']['apex_rotation'])
        switches[bi] = other
    assert len(switches) == 8
    return bases, switches


def transfer_controls():
    rows, comparisons = [], 0
    for mask in range(16):
        allowed = {c for c in U if mask >> c & 1}
        if len(allowed) < 2:
            continue
        def accepts(length, left, right):
            possible = {left}
            for _ in range(length):
                possible = {c for c in allowed if possible-{c}}
            return bool(possible-{right})
        reference = [[accepts(k, a, b) for a, b in product(range(4), repeat=2)]
                     for k in (0, 1, 2)]
        for length in range(1, 9):
            actual = [accepts(length, a, b) for a, b in product(range(4), repeat=2)]
            assert actual == reference[1 if length % 2 else 2]
            comparisons += len(actual)
        rows.append(dict(allowed_colors=sorted(allowed), empty_gap=reference[0],
                         odd_positive_gap=reference[1], even_positive_gap=reference[2]))
    # Zero is a separate gap type, not another positive even run.
    example = rows[-1]
    assert example['empty_gap'] != example['even_positive_gap']
    return dict(subsets=len(rows), endpoint_comparisons=comparisons,
                rows=rows, zero_gap_is_separate=True)


def marked_tails(base, slot, other=None):
    first, leaf = base['neighborhoods'][3+2*slot:5+2*slot]
    if other is None:
        for left, right in product(range(3), repeat=2):
            if (left+right) % 2 == 0:
                yield dict(neighborhoods=[first]*(left+1+right)+[leaf],
                           marker=left, kind='uniform_nonleaf', gaps=[left, right])
        yield dict(neighborhoods=[first, leaf], marker=1,
                   kind='uniform_leaf', gaps=[1])
    else:
        yield dict(neighborhoods=[first, other, other, leaf], marker=0,
                   kind='switched_first', gaps=[2])
        for left, right in product(range(3), repeat=2):
            if (left+right) % 2 == 1:
                yield dict(neighborhoods=[first]+[other]*(left+1+right)+[leaf],
                           marker=1+left, kind='switched_nonleaf', gaps=[left, right])
        yield dict(neighborhoods=[first, other, other, leaf], marker=3,
                   kind='switched_leaf', gaps=[2])


def dynamic_pairs(data, pair, row):
    """Triangle/tail DP with both marker coordinates and whole-graph witnesses."""
    ns = data['neighborhoods']
    available = {v: U-{row[b] for b in ns[v-5]} for v in data['interior_order']}
    result = {}
    for colors in product(*(sorted(available[v]) for v in data['triangle'])):
        if len(set(colors)) < 3:
            continue
        a, b = [colors[v-5] if v in data['triangle'] else None for v in pair]
        states = {(None, a, b): colors}
        for slot, path in enumerate(data['branch_paths']):
            states = {(colors[slot], x, y): full for (_, x, y), full in states.items()}
            for v in path:
                following = {}
                for (last, x, y), full in sorted(states.items(), key=lambda t: repr(t[0])):
                    for color in sorted(available[v]-{last}):
                        key = (color, color if v == pair[0] else x,
                               color if v == pair[1] else y)
                        following.setdefault(key, full+(color,))
                states = following
        for (_, x, y), full in sorted(states.items(), key=lambda t: repr(t[0])):
            assert x is not None and y is not None
            result.setdefault((x, y), full)
    return result


def original_components(data, pair):
    edges = set(map(tuple, data['edges'])) | {pair}
    result = []
    for i, vs in enumerate(components(set(data['interior_order'])-set(pair), edges)):
        contacts = [[v for v in vs if tuple(sorted((r, v))) in edges] for r in pair]
        ownership = [r for r, cs in zip(pair, contacts, strict=True) if cs]
        result.append(dict(id=i, vertices=vs, root_contacts=contacts,
            contact_order=sorted(set().union(*map(set, contacts))), ownership=ownership,
            kind='mixed' if len(ownership) == 2 else 'unary',
            actual_support=sorted(set().union(*(set(data['neighborhoods'][v-5]) for v in vs))),
            boundary_attachments=[dict(vertex=v, neighbors=data['neighborhoods'][v-5]) for v in vs],
            original_edges=sorted(e for e in edges if set(e) & set(vs))))
    assert any(r['kind'] == 'mixed' for r in result)
    return result


def ordered_rows(data, pair, independent=True):
    edges = set(map(tuple, data['edges']))
    assert pair not in edges
    records = []
    for row in ROWS:
        witnesses = dynamic_pairs(data, pair, row)
        relation = sorted(witnesses)
        retained = [t for t in relation if t[0] != t[1]]
        if independent:
            full = list(search(data['interior_order'], edges, dict(enumerate(row))))
            assert set(relation) == {tuple(f[v] for v in pair) for f in full}
            direct = list(search(data['interior_order'], edges | {pair}, dict(enumerate(row))))
            assert set(retained) == {tuple(f[v] for v in pair) for f in direct}
        for t, colors in witnesses.items():
            fixed = dict(enumerate(row)) | dict(zip(data['interior_order'], colors, strict=True))
            assert tuple(fixed[v] for v in pair) == t
            assert all(fixed[a] != fixed[b] for a, b in edges)
        records.append(dict(ordered_root_pair_relation=relation,
            full_original_interior_witnesses=[witnesses[t] for t in relation],
            retained_pair_tuple_indices=[i for i, t in enumerate(relation) if t in retained]))
    old_mask = sum(1 << i for i, r in enumerate(records) if r['ordered_root_pair_relation'])
    new_mask = sum(1 << i for i, r in enumerate(records) if r['retained_pair_tuple_indices'])
    assert old_mask == 1022
    return records, new_mask


def expanded_reduction(data, pair):
    """Fixed +2 growth of each positive unmarked gap; retain marker singletons.

    Branch sets certify a boundary-fixing minor of both N and N+zw. Expanded
    full witnesses use the original, longer vertex order, never a short witness.
    """
    tails, groups_by_slot = [], []
    for path in data['branch_paths']:
        groups, tail = [], []
        i = 0
        while i < len(path):
            v = path[i]
            support = data['neighborhoods'][v-5]
            if v in pair or i == len(path)-1:
                groups.append((v, len(tail), 1))
                tail.append(support)
                i += 1
                continue
            j = i+1
            while (j < len(path)-1 and path[j] not in pair
                   and data['neighborhoods'][path[j]-5] == support):
                j += 1
            assert j-i <= 2
            for k in range(i, j):
                length = 3 if k == j-1 else 1
                groups.append((path[k], len(tail), length))
                tail.extend([support]*length)
            i = j
        tails.append(tail)
        groups_by_slot.append(groups)
    expanded = graph(data, tails)
    branch_sets = {v: [v] for v in range(8)}
    for path, groups in zip(expanded['branch_paths'], groups_by_slot, strict=True):
        for target, start, length in groups:
            branch_sets[target] = path[start:start+length]
    mapping = {v: t for t, group in branch_sets.items() for v in group}
    assert set(mapping) == set(range(expanded['vertices']))
    assert all(len(branch_sets[v]) == 1 for v in pair)
    longer_pair = tuple(branch_sets[v][0] for v in pair)
    expanded_edges = set(map(tuple, expanded['edges']))
    for group in branch_sets.values():
        assert len(components(set(group), expanded_edges)) == 1
    quotient = {tuple(sorted((mapping[a], mapping[b]))) for a, b in expanded_edges
                if mapping[a] != mapping[b]}
    assert quotient == set(map(tuple, data['edges']))
    assert longer_pair not in expanded_edges
    joined_quotient = {tuple(sorted((mapping[a], mapping[b])))
                       for a, b in expanded_edges | {longer_pair} if mapping[a] != mapping[b]}
    assert joined_quotient == quotient | {pair}
    rows, mask = ordered_rows(expanded, longer_pair, independent=False)
    short_rows, short_mask = ordered_rows(data, pair, independent=False)
    assert mask == short_mask
    assert [r['ordered_root_pair_relation'] for r in rows] == [
        r['ordered_root_pair_relation'] for r in short_rows]
    return dict(original_graph=expanded, original_root_pair=longer_pair,
                original_components=original_components(expanded, longer_pair),
                reduction_branch_sets=[dict(target=t, original_vertices=vs)
                                       for t, vs in sorted(branch_sets.items())],
                original_ordered_rows=rows)


def normal_forms(bases, switches):
    result = []
    for bi, base in enumerate(bases):
        for switched in ([False, True] if bi in switches else [False]):
            for slot in range(len(base['branch_paths'])):
                for tail in marked_tails(base, slot, switches[bi] if switched else None):
                    tails = [base['neighborhoods'][3+2*k:5+2*k]
                             for k in range(len(base['branch_paths']))]
                    tails[slot] = tail['neighborhoods']
                    data = graph(base, tails)
                    for triangle_vertex in data['triangle']:
                        pair = (triangle_vertex, data['branch_paths'][slot][tail['marker']])
                        if pair in set(map(tuple, data['edges'])):
                            continue
                        result.append(dict(base=bi, family='triangle_branch',
                            switched=switched, marked_tail=tail, graph=data, root_pair=pair))
        if len(base['branch_paths']) == 2:
            for left, right in product(marked_tails(base, 0), marked_tails(base, 1)):
                data = graph(base, [left['neighborhoods'], right['neighborhoods']])
                pair = (data['branch_paths'][0][left['marker']],
                        data['branch_paths'][1][right['marker']])
                result.append(dict(base=bi, family='cross_branch', switched=False,
                    marked_tails=[left, right], graph=data, root_pair=pair))
    histogram = Counter()
    for model in result:
        data, pair = model['graph'], model['root_pair']
        model['original_components'] = original_components(data, pair)
        model['rows'], mask = ordered_rows(data, pair)
        assert mask & T4 != T4 or mask == 1022
        model['restored_sigma'] = mask
        model['fixed_longer_original_control'] = expanded_reduction(data, pair)
        histogram[mask] += 1
    assert len(result) == 528
    assert histogram == {894: 52, 990: 32, 1018: 52, 1022: 392}
    return result, histogram


def same_branch_controls(bases, switches):
    result = []
    for bi, base in enumerate(bases):
        for switched in ([False, True] if bi in switches else [False]):
            tails = []
            for slot in range(len(base['branch_paths'])):
                first, leaf = base['neighborhoods'][3+2*slot:5+2*slot]
                tails.append(([first]+[switches[bi]]*4+[leaf]) if switched
                             else [first]*5+[leaf])
            data = graph(base, tails)
            edges = set(map(tuple, data['edges']))
            restorations = []
            for path in data['branch_paths']:
                assert all(4 in data['neighborhoods'][v-5]
                           and set(data['neighborhoods'][v-5])-{4} for v in path)
                for pair in combinations(path, 2):
                    if pair in edges:
                        continue
                    middle = path[path.index(pair[0])+1:path.index(pair[1])]
                    branch_sets = [[pair[0]], middle, [pair[1]], [4],
                                   sorted((B-{4}) | {data['vertices']})]
                    apex_edges = edges | {pair} | {(b, data['vertices']) for b in B}
                    certificate = verify_k5(apex_edges, branch_sets)
                    rows, mask = ordered_rows(data, pair)
                    restorations.append(dict(root_pair=pair, apex_k5_minor=certificate,
                        original_components=original_components(data, pair),
                        rows=rows, restored_sigma=mask))
            result.append(dict(base=bi, switched=switched, original_graph=data,
                               edge_restorations=restorations))
    assert len(result) == 26
    assert sum(len(r['edge_restorations']) for r in result) == 280
    return result


def longer_backtracking_controls(normal):
    """Independent pinned backtracking on one longer original per size/family.

    All sixteen ordered pairs are queried, including absent fibers. This is a
    fixed control of the marked reduction, not its arbitrary-length proof.
    """
    seen, records, digest, queries = set(), [], sha256(), 0
    for index, model in enumerate(normal):
        longer = model['fixed_longer_original_control']
        data, pair = longer['original_graph'], longer['original_root_pair']
        key = (model['family'], model['switched'], data['vertices'])
        if key in seen:
            continue
        seen.add(key)
        edges = set(map(tuple, data['edges']))
        masks = []
        for row_index, (row, expected) in enumerate(zip(ROWS, longer['original_ordered_rows'], strict=True)):
            relation = set(map(tuple, expected['ordered_root_pair_relation']))
            actual = set()
            for colors in product(range(4), repeat=2):
                fixed = dict(enumerate(row)) | dict(zip(pair, colors, strict=True))
                full = next(search(set(data['interior_order'])-set(pair), edges, fixed), None)
                # search expects callers to enforce constraints between fixed vertices.
                valid_fixed = all(fixed[a] != fixed[b] for a, b in edges
                                  if a in fixed and b in fixed)
                accepted = full is not None and valid_fixed
                if accepted:
                    assert all(full[a] != full[b] for a, b in edges)
                    actual.add(colors)
                digest.update(f'{index}:{row_index}:{colors}:{int(accepted)}\n'.encode())
                queries += 1
            assert actual == relation
            masks.append(sum(1 << (4*a+b) for a, b in actual))
        records.append(dict(normal_form=index, original_vertices=data['vertices'],
                            relation_masks=masks))
    return dict(original_graph_controls=len(records), pinned_pair_queries=queries,
                query_sha256=digest.hexdigest(), records=records)


def build():
    bases, switches = inherited_bases()
    normal, histogram = normal_forms(bases, switches)
    same = same_branch_controls(bases, switches)
    collision = None
    for ci, control in enumerate(same):
        for ei, restoration in enumerate(control['edge_restorations']):
            for ri, row in enumerate(restoration['rows']):
                relation = row['ordered_root_pair_relation']
                marginals = [sorted({t[j] for t in relation}) for j in (0, 1)]
                if not row['retained_pair_tuple_indices'] and any(
                        a != b for a, b in product(*marginals)):
                    collision = dict(control=ci, restoration=ei, row_index=ri,
                        complete_relation=relation, marginals=marginals,
                        false_marginal_off_diagonal=sorted((a, b) for a, b in product(*marginals) if a != b))
                    break
            if collision:
                break
        if collision:
            break
    assert collision is not None
    dependencies = [Path(__file__).resolve(),
        ROOT / 'scripts/c5_independent_support_capacity.py',
        ROOT / 'scripts/c5_941_two_spoke.py',
        ROOT / 'scripts/c5_excess_two_path_edge.py', BASE, PATH]
    return dict(schema=1,
        scope='Inherited single-triangle necessary domain. Arbitrary-size coverage is the paper marked gap reduction and original same-branch K5 lemma; finite controls do not establish disk realization or a Lean theorem.',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in dependencies},
        boundary_order=sorted(B), pattern_order=ROWS, root_color_frame=sorted(U), normalized_q=Q4,
        tuple_witness_semantics='Each row and complete interior witness use the graph interior_order and one literal frame. Marker branch sets are singletons; no component normalization or marginal join.',
        inherited_bases=bases, switched_contexts=[dict(base=bi, second_run_support=ns)
                                               for bi, ns in sorted(switches.items())],
        marked_gap_transfer=transfer_controls(), marked_normal_forms=normal,
        same_branch_original_controls=same, actual_graph_marginal_collision=collision,
        longer_independent_backtracking=longer_backtracking_controls(normal),
        summary=dict(inherited_bases=len(bases), switched_contexts=len(switches),
            marked_normal_forms=len(normal), family_counts=dict(Counter(r['family'] for r in normal)),
            restored_Sigma_histogram=dict(sorted(histogram.items())),
            T4_preserving_normal_forms=histogram[1022], strict_T4_preserving_root_edges=0,
            complete_normal_form_row_queries=10*len(normal),
            fixed_longer_marker_reductions=len(normal),
            same_branch_original_graphs=len(same), same_branch_k5_certificates=280,
            complete_same_branch_row_queries=2800, candidate_sources=0))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = encoded(result)
    if args.check:
        assert OUT.read_text() == data, 'certificate differs; regenerate intentionally'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
