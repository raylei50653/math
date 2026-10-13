#!/usr/bin/env python3
"""Independent exact C8 interface verifier and finite planar graph controls.

Imports neither the producer nor frozen collar implementation. Literal graph
coloring counts use generic backtracking; no floating arithmetic is used.
"""
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def canonical(word):
    seen = []
    for c in word:
        if c not in seen:
            seen.append(c)
    return tuple(seen.index(c) for c in word)


def proper_words(n):
    return [w for w in product(range(4), repeat=n)
            if all(w[i-1] != w[i] for i in range(n))]


def set_partitions(n, word=()):
    if len(word) == n:
        yield word
    else:
        for label in range(max(word, default=-1)+2):
            yield from set_partitions(n, word+(label,))


def nc_partition(p):
    return not any(p[a] == p[c] and p[b] == p[d] and p[a] != p[b]
                   for a,b,c,d in combinations(range(len(p)), 4))


def equality_entry(word, partition):
    colors = {}
    for block, color in zip(partition, word):
        if block in colors and colors[block] != color:
            return 0
        colors[block] = color
    return 1


def require_equal(actual, expected, label):
    assert actual == json.loads(json.dumps(expected)), label


def interface_geometry(extras):
    labels = ['a0']
    supports = [(0,1)]
    for boundary in (1,2,3,4,0):
        for ordinal in range(1, extras[boundary]+1):
            labels.append(f'y{boundary}_{ordinal}')
            supports.append((boundary,))
        if boundary:
            labels.append(f'a{boundary}')
            supports.append((boundary,(boundary+1)%5))
    return labels, supports


def independently_derive_kempe(patterns, partitions):
    """Filter full NC partitions by side and actual C8 bichromatic edges."""
    splits = [((0,1),(2,3)), ((0,2),(1,3)), ((0,3),(1,2))]
    index = {w:i for i,w in enumerate(patterns)}
    table = []
    for word in patterns:
        obligations = []
        for split in splits:
            side = [int(c in split[1]) for c in word]
            swap = {c:pair[1-pair.index(c)] for pair in split for c in pair}
            possibilities = set()
            for partition in partitions:
                owners = {}
                valid = True
                for i,block in enumerate(partition):
                    if block in owners and owners[block] != side[i]:
                        valid = False
                        break
                    owners[block] = side[i]
                if not valid:
                    continue
                if any(side[i-1] == side[i] and partition[i-1] != partition[i]
                       for i in range(8)):
                    continue
                orbit = 0
                for flips in product((False, True), repeat=max(partition)+1):
                    changed = tuple(swap[c] if flips[partition[i]] else c
                                    for i,c in enumerate(word))
                    orbit |= 1 << index[canonical(changed)]
                possibilities.add(orbit)
            assert possibilities
            obligations.append(sorted(possibilities))
        table.append(obligations)
    return table


def independent_pruning(columns, obligations, target):
    allowed = {p for p,mask in enumerate(columns) if not mask & ~target}
    as_mask = lambda xs: sum(1 << p for p in xs)
    initial = as_mask(allowed)
    rounds = []
    while True:
        before = as_mask(allowed)
        removals = []
        for p in sorted(allowed):
            bad = [s for s,orbits in enumerate(obligations[p])
                   if all(orbit & ~before for orbit in orbits)]
            if bad:
                removals.append(dict(pattern_index=p, split_indices=bad))
        if not removals:
            break
        rounds.append(dict(before=before, removals=removals))
        allowed -= {removal['pattern_index'] for removal in removals}
    union = 0
    for p in allowed:
        union |= columns[p]
    return dict(initial=initial, rounds=rounds, fixed_point=as_mask(allowed),
                possible_outer_union=union, excluded=(union != target))


def reconstruct_interface(data):
    literal = proper_words(8)
    patterns = sorted({canonical(w) for w in literal})
    outer_literal = proper_words(5)
    outer = sorted({canonical(w) for w in outer_literal})
    index = {w:i for i,w in enumerate(patterns)}
    outer_index = {w:i for i,w in enumerate(outer)}
    literal_to_pattern = [index[canonical(w)] for w in literal]
    sizes = [literal_to_pattern.count(i) for i in range(len(patterns))]
    by_colors = Counter(len(set(w)) for w in patterns)
    require_equal(data['color_frame'], [0,1,2,3], 'literal color frame')
    require_equal(data['boundary_order'], [f'b{i}' for i in range(5)], 'outer labels')
    require_equal(data['pattern_order'], patterns, 'mixed inner row labels')
    require_equal(data['outer_pattern_order'], outer, 'mixed outer row labels')
    require_equal(data['literal_assignments'], literal, 'incomplete literal C8 assignments')
    require_equal(data['literal_to_pattern'], literal_to_pattern, 'literal orbit indexing')
    require_equal(data['orbit_sizes'], sizes, 'wrong orbit weights')
    require_equal(data['orbit_counts_by_colors'], dict(by_colors), 'color use counts')
    # The chromatic polynomial formula is separately evaluated, not used to build words.
    assert len(literal) == 3**8+3 and len(patterns) == 274
    assert by_colors == {2:1,3:42,4:231}
    assert Counter(sizes) == {12:1,24:273}
    assert len(outer_literal) == 3**5-3 and len(outer) == 10
    partitions = [p for p in set_partitions(8) if nc_partition(p)]
    assert len(partitions) == 1430
    obligations = independently_derive_kempe(patterns, partitions)
    require_equal(data['kempe_obligations'], obligations, 'NC Kempe obligations')
    distributions = [a for a in product(range(4),repeat=5) if sum(a)==3]
    assert len(distributions) == 35
    assert len(data['cases']) == 35
    expected_cases = []
    for case_number,(case,extras) in enumerate(zip(data['cases'], distributions)):
        require_equal(case['extras'], extras, 'weak composition coverage')
        require_equal(case['id'], f'c{case_number:02d}', 'case order')
        labels,supports = interface_geometry(extras)
        require_equal(case['boundary_order'], labels, 'C8 labels')
        require_equal(case['supports'], supports, 'actual attachments')
        collar_edges = [(f'b{i}',f'b{(i+1)%5}') for i in range(5)]
        collar_edges += [(labels[i],labels[(i+1)%8]) for i in range(8)]
        collar_edges += [(f'b{i}',labels[j]) for j,support in enumerate(supports) for i in support]
        require_equal(case['collar_edges'], collar_edges, 'literal collar edges')
        def compatible(inner,boundary):
            return not any(inner[j] == boundary[i] for j,s in enumerate(supports) for i in s)
        transfer = [[0]*len(patterns) for _ in outer]
        for inner,p in zip(literal,literal_to_pattern):
            for r,boundary in enumerate(outer):
                if compatible(inner,boundary):
                    transfer[r][p] += 1
        lifts = [[boundary for boundary in outer_literal if compatible(inner,boundary)]
                 for inner in patterns]
        reverse = [[sum(outer_index[canonical(b)] == r for b in lifts[p])
                    for p in range(len(patterns))] for r in range(10)]
        columns = [sum(1<<r for r in range(10) if transfer[r][p]) for p in range(len(patterns))]
        for r in range(10):
            for p in range(len(patterns)):
                assert 24*transfer[r][p] == sizes[p]*reverse[r][p], 'orbit detailed balance'
        require_equal(case['transfer'], transfer, 'literal transfer coefficient')
        require_equal(case['column_masks'], columns, 'transfer support')
        require_equal(case['outer_lifts_for_each_named_inner_row'], lifts, 'incomplete reverse literal lifts')
        full_preimages = {str(r):[p for p in range(len(patterns)) if transfer[r][p]] for r in range(10)}
        require_equal(case['full_preimages'], full_preimages, 'incomplete full preimages')
        assert [q['target'] for q in case['targets']] == [933,941]
        for query in case['targets']:
            expected = independent_pruning(columns,obligations,query['target'])
            for key,value in expected.items():
                require_equal(query[key], value, 'pruning '+key)
            require_equal(query['query_id'], case['id']+'-'+str(query['target']), 'query identity')
            accepted_preimages = {str(r):[p for p in range(len(patterns))
                                         if expected['fixed_point']>>p&1 and transfer[r][p]]
                                  for r in range(10) if query['target']>>r&1}
            require_equal(query['accepted_preimages'], accepted_preimages, 'missing necessary accepted preimage')
        expected_cases.append(dict(transfer=transfer,lifts=lifts,columns=columns,
                                   full_preimages=full_preimages,extras=extras,supports=supports))
    return patterns, outer, partitions, expected_cases


def count_colorings(vertex_count, edges, fixed):
    """Exact graph backtracking using literal colors; no interface data."""
    adjacency = [set() for _ in range(vertex_count)]
    for a,b in edges:
        assert a != b
        adjacency[a].add(b)
        adjacency[b].add(a)
    colors = [-1]*vertex_count
    for v,c in fixed.items():
        colors[v] = c
    if any(colors[a] >= 0 and colors[a] == colors[b] for a,b in edges):
        return 0
    def visit():
        uncolored = [v for v,c in enumerate(colors) if c < 0]
        if not uncolored:
            return 1
        v = max(uncolored, key=lambda v:(len({colors[u] for u in adjacency[v] if colors[u]>=0}),
                                         len(adjacency[v]),-v))
        forbidden = {colors[u] for u in adjacency[v]}
        total = 0
        for c in range(4):
            if c not in forbidden:
                colors[v] = c
                total += visit()
        colors[v] = -1
        return total
    return visit()


def finite_graphs():
    boundary = [(i,(i+1)%8) for i in range(8)]
    return [
        dict(name='bare_cycle', vertices=8, edges=boundary,
             embedding='Boundary cycle only; interior face may be untriangulated.'),
        dict(name='triangulated_fan', vertices=8, edges=boundary+[(0,i) for i in range(2,7)],
             embedding='All five chords share boundary vertex 0.'),
        dict(name='wheel', vertices=9, edges=boundary+[(8,i) for i in range(8)],
             embedding='Vertex 8 is the center, with spokes in boundary order.'),
        dict(name='two_center_disk', vertices=10,
             edges=boundary+[(8,i) for i in range(5)]+[(9,i) for i in (4,5,6,7,0)]+[(8,9)],
             embedding='Vertex 8 fans along 0,1,2,3,4; vertex 9 fans along 4,5,6,7,0; faces (0,8,9),(4,8,9).')]


def count_identity(patterns, partitions):
    """Discover a row dependence detecting Boolean wheel counts; verify all NC columns."""
    active = [p for p in partitions if any(equality_entry(w,p) for w in patterns)]
    rows = [[equality_entry(w,p) for p in active] for w in patterns]
    wheel_actual = [4-len(set(w)) for w in patterns]
    wheel_boolean = [int(c>0) for c in wheel_actual]
    basis = {}
    found = None
    for i,row in enumerate(rows):
        vector = list(map(Fraction,row))
        coefficients = {i:Fraction(1)}
        for pivot,(reduced,expansion) in sorted(basis.items()):
            scale = vector[pivot]
            if scale:
                vector = [a-scale*b for a,b in zip(vector,reduced)]
                for j,c in expansion.items():
                    coefficients[j] = coefficients.get(j,0)-scale*c
        coefficients = {j:c for j,c in coefficients.items() if c}
        if any(vector):
            pivot = next(j for j,c in enumerate(vector) if c)
            scale = vector[pivot]
            basis[pivot] = ([c/scale for c in vector],{j:c/scale for j,c in coefficients.items()})
        elif found is None and sum(c*wheel_boolean[j] for j,c in coefficients.items()):
            found = coefficients
    assert len(active) == 91 and len(basis) == 91 and found
    assert all(c.denominator == 1 for c in found.values())
    identity = {j:int(c) for j,c in sorted(found.items())}
    residuals = [sum(c*equality_entry(patterns[j],partition) for j,c in identity.items())
                 for partition in partitions]
    assert not any(residuals)
    assert sum(c*wheel_actual[j] for j,c in identity.items()) == 0
    boolean_residual = sum(c*wheel_boolean[j] for j,c in identity.items())
    assert boolean_residual != 0
    corrupted = dict(identity)
    corrupted[min(corrupted)] += 1
    bad_residuals = [sum(c*equality_entry(patterns[j],partition) for j,c in corrupted.items())
                     for partition in partitions]
    assert any(bad_residuals)
    return dict(active_columns=len(active), equality_rank=len(basis),
                coefficients=[dict(index=j,word=patterns[j],coefficient=c) for j,c in identity.items()],
                nc_residuals=residuals,wheel_actual_residual=0,wheel_boolean_residual=boolean_residual,
                corrupt_coefficient_detected=True)


def rejected_comparison(actual,expected,label):
    try:
        require_equal(actual,expected,label)
    except AssertionError:
        return True
    raise AssertionError('negative control accepted: '+label)


def run(data):
    patterns,outer,partitions,cases = reconstruct_interface(data)
    identity = count_identity(patterns,partitions)
    controls = []
    for graph in finite_graphs():
        counts = [count_colorings(graph['vertices'],graph['edges'],dict(enumerate(word)))
                  for word in patterns]
        identity_residual = sum(t['coefficient']*counts[t['index']] for t in identity['coefficients'])
        assert identity_residual == 0
        direct_outputs = []
        for case in cases:
            # Whole graph vertices are the five original b labels followed by
            # all actual H vertices, so joins never identify normalized colors.
            whole_edges = [(i,(i+1)%5) for i in range(5)]
            whole_edges += [(a+5,b+5) for a,b in graph['edges']]
            whole_edges += [(b,inner+5) for inner,support in enumerate(case['supports']) for b in support]
            direct = [count_colorings(graph['vertices']+5,whole_edges,dict(enumerate(word))) for word in outer]
            transfer = [sum(coefficient*x for coefficient,x in zip(row,counts)) for row in case['transfer']]
            assert direct == transfer, ('whole graph transfer',graph['name'],case['extras'])
            direct_outputs.append(direct)
        if graph['name'] == 'wheel':
            assert counts == [4-len(set(word)) for word in patterns]
        controls.append(dict(**graph,pattern_extension_counts=counts,
                             whole_graph_counts_by_case=direct_outputs,
                             count_identity_residual=identity_residual,
                             status='triggered and holds; finite implementation calibration only'))
    # Mutations target the exact comparison predicates used above.
    corrupt_transfer = deepcopy(data['cases'][0]['transfer'])
    corrupt_transfer[0][0] += 1
    corrupt_patterns = deepcopy(data['pattern_order'])
    corrupt_patterns[0],corrupt_patterns[1] = corrupt_patterns[1],corrupt_patterns[0]
    corrupt_sizes = [24]*len(patterns)
    selected = next((c,q,r) for c in data['cases'] for q in c['targets']
                    for r,ps in q['accepted_preimages'].items() if ps)
    case,query,r = selected
    corrupt_preimages = deepcopy(query['accepted_preimages'])
    removed = corrupt_preimages[r].pop()
    negatives = dict(
        altered_transfer_coefficient=rejected_comparison(corrupt_transfer,cases[0]['transfer'],'literal transfer coefficient'),
        swapped_row_labels=rejected_comparison(corrupt_patterns,patterns,'mixed inner row labels'),
        uniform_orbit_weight_24=rejected_comparison(corrupt_sizes,data['orbit_sizes'],'wrong orbit weights'),
        omitted_necessary_preimage=rejected_comparison(corrupt_preimages,query['accepted_preimages'],'missing necessary accepted preimage'),
        omitted_preimage_query=query['query_id'],omitted_preimage_outer_row=int(r),omitted_preimage_inner_row=removed,
        corrupted_count_identity=identity['corrupt_coefficient_detected'],
        boolean_support_as_counts_rejected=(identity['wheel_boolean_residual'] != 0))
    return dict(schema='independent-c8-controls-v1',interface_sha256=sha256((ROOT/'interface.json').read_bytes()).hexdigest(),
                counts=dict(named_compositions=len(cases),queries=2*len(cases),proper_orbits=len(patterns),
                            literal_assignments=len(proper_words(8)),orbit_sizes=dict(Counter(data['orbit_sizes'])),
                            noncrossing_partitions=len(partitions),finite_inner_graphs=len(controls),
                            direct_whole_graph_queries=len(controls)*len(cases)*len(outer)),
                independently_verified=['named collar coverage and attachments','all literal transfers and reverse lifts',
                                        'noncrossing Kempe obligations','all simultaneous pruning rounds',
                                        'complete accepted and full preimages','orbit detailed balance'],
                finite_graph_controls=controls,boolean_support_countercontrol=identity,negative_controls=negatives,
                interpretation='Finite controls calibrate implementation only. They do not satisfy or witness the complete minimal-source contract.')


def main():
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write',action='store_true')
    modes.add_argument('--check',action='store_true')
    parser.add_argument('--interface',type=Path,default=ROOT/'interface.json')
    parser.add_argument('--certificate',type=Path,default=HERE/'control_certificate.json')
    args = parser.parse_args()
    data = json.loads(args.interface.read_text())
    result = run(data)
    result['interface_sha256'] = sha256(args.interface.read_bytes()).hexdigest()
    if args.write:
        with args.certificate.open('x') as stream:
            json.dump(result,stream,sort_keys=True,separators=(',',':'))
            stream.write('\n')
    else:
        require_equal(json.loads(args.certificate.read_text()),result,'finite control certificate mismatch')
    print(json.dumps(dict(status='PASS',**result['counts'],negative_controls=result['negative_controls']),sort_keys=True))


if __name__ == '__main__':
    main()
