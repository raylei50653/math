#!/usr/bin/env python3
"""Replay one frozen completed graph; no search over disks or exteriors."""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = 'e1617a2756813327d7ad333cfdd0fd92fa9efc38'
SOURCE = ROOT.parent / 'frozen/audits/2026-10-18-smaller-source-9f1fe84'
INPUTS = {
    'C/check_bridge.py': 'e973a77532a4393dab55663168a47b6d7e01b6efb732e4567ad1a8303f920bb9',
    'C/certificate.json': '1d2a80e7dd62aeda079980e1cb779c8f55ae00c659af4287d1b035eac047fad9',
    'B/REVIEW-C-FULL-FIBRES.json': '9c574758e05f28bfce3bd7d0735106c61a468d3f6f8059293a70bba627fbc88a',
}
for path, digest in INPUTS.items():
    assert hashlib.sha256((SOURCE / path).read_bytes()).hexdigest() == digest
OLD = json.loads((SOURCE / 'C/certificate.json').read_text())
REVIEW = json.loads((SOURCE / 'B/REVIEW-C-FULL-FIBRES.json').read_text())
assert OLD['script_sha256'] == INPUTS['C/check_bridge.py']
assert REVIEW['source_certificate_sha256'] == INPUTS['C/certificate.json']
OUTER = tuple('xyabc')
RIM = ('a', 'b', 'q', 'L', 'R', 'n')
ROWS = REVIEW['rows']
NEGATIVE_ROWS = ('01021', '01202', '01212')
PAIRS = tuple(itertools.combinations(range(4), 2))


def edge(u, v):
    return tuple(sorted((u, v)))


def cycle(vs):
    return {edge(vs[i], vs[(i + 1) % len(vs)]) for i in range(len(vs))}


def proper(chi, edges):
    return all(chi[u] != chi[v] for u, v in edges)


def components(vertices, edges, chi, pair):
    """Actual maximal components, including singletons, in a full colouring."""
    remaining = {v for v in vertices if chi[v] in pair}
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    result = []
    while remaining:
        seen = {min(remaining)}
        frontier = set(seen)
        while frontier:
            neighbours = {v for u in frontier for v in adjacency[u]}
            frontier = (neighbours & remaining) - seen
            seen |= frontier
        remaining -= seen
        result.append(sorted(seen))
    return sorted(result)


def block_at(partition, v):
    return next(block for block in partition if v in block)


def joined(partitions):
    """Join actual same-colouring partitions on their shared vertices."""
    blocks = [set(block) for partition in partitions for block in partition]
    while True:
        for i, left in enumerate(blocks):
            j = next((j for j in range(i + 1, len(blocks))
                      if left & blocks[j]), None)
            if j is not None:
                blocks[i] |= blocks.pop(j)
                break
        else:
            return sorted(sorted(block) for block in blocks)


def switched(chi, block, pair):
    result = dict(chi)
    for v in block:
        result[v] = pair[1] if chi[v] == pair[0] else pair[0]
    return result


def word(chi):
    return ''.join(str(chi[v]) for v in OUTER)


def rainbow(chi):
    return len({chi[v] for v in ('a', 'b', 'q', 'n')}) == 4


def all_fibres(vertices, edges):
    """Independent sequential backtracking, preserving all literal colours."""
    previous = {v: [] for v in vertices}
    for u, v in edges:
        if vertices.index(u) > vertices.index(v):
            u, v = v, u
        previous[v].append(u)
    result = []
    for row in ROWS:
        chi = dict(zip(OUTER, map(int, row)))
        full = []

        def visit(i):
            if i == len(vertices):
                full.append([chi[v] for v in vertices])
                return
            v = vertices[i]
            for colour in range(4):
                if all(chi[u] != colour for u in previous[v]):
                    chi[v] = colour
                    visit(i + 1)
                    del chi[v]

        assert proper(chi, [e for e in edges if set(e) <= set(OUTER)])
        visit(5)
        result.append(sorted(full))
    return result


# Reconstruct the graph from its actual oriented triangular faces, independently
# of the predecessor's edge constructor; preserve the entire frozen exterior.
faces = OLD['whole_graph_oriented_faces']
original_edges = {edge(f[i], f[(i + 1) % 3]) for f in faces for i in range(3)}
original_vertices = tuple(REVIEW['vertices']['G'])
assert original_edges == set(map(tuple, OLD['whole_graph_control']['G']['edges']))
reduced_vertices = tuple(v for v in original_vertices if v not in {'p', 'h'})
surviving_edges = {e for e in original_edges if not (set(e) & {'p', 'h'})}
rim_edges = cycle(RIM)
# Exterior includes the actual six rim edges. Fan interior edges are separate;
# shared rim edges may occur in both pieces without changing partition joins.
exterior_edges = surviving_edges
fan_edges = {'G_a': rim_edges | {edge('a', v) for v in ('q', 'L', 'R')},
             'G_b': rim_edges | {edge('b', v) for v in ('n', 'L', 'R')}}
graphs = {'G': (original_vertices, original_edges)}
graphs.update({name: (reduced_vertices, exterior_edges | local)
               for name, local in fan_edges.items()})
fibres = {}
for name, (vertices, edges) in graphs.items():
    assert list(vertices) == REVIEW['vertices'][name]
    assert edges == set(map(tuple, OLD['whole_graph_control'][name]['edges']))
    fibres[name] = all_fibres(vertices, edges)
    assert fibres[name] == REVIEW['full_fibres'][name]
    assert list(map(len, fibres[name])) == OLD['whole_graph_control'][name]['counts']
    assert [hashlib.sha256(json.dumps(f).encode()).hexdigest()
            for f in fibres[name]] == OLD['whole_graph_control'][name]['fibres_sha256']


def lifts(chi):
    result = []
    for p, h in itertools.product(range(4), repeat=2):
        lifted = dict(chi, p=p, h=h)
        if proper(lifted, original_edges):
            result.append([lifted[v] for v in original_vertices])
    return sorted(result)


def identity(name, chi):
    return {'graph': name, 'row': word(chi),
            'full_colouring': [chi[v] for v in reduced_vertices]}


def port_record(name, chi, pair):
    vertices, edges = graphs[name]
    full = components(vertices, edges, chi, pair)
    outside = components(vertices, exterior_edges, chi, pair)
    inside = components(RIM, fan_edges[name], chi, pair)
    join = joined([outside, inside])
    assert join == full
    return dict(identity(name, chi), pair=list(pair),
                exterior_partition=outside, fan_partition=inside,
                actual_components=full, joined_components=join)


def validate_port_record(record):
    chi = dict(zip(reduced_vertices, record['full_colouring']))
    name = record['graph']
    assert proper(chi, graphs[name][1])
    assert word(chi) == record['row']
    assert record == port_record(name, chi, tuple(record['pair']))


full_records, port_records, force_records, refined_records = [], [], [], []
fan_b_endpoint_records = []
for name in fan_edges:
    vertices, edges = graphs[name]
    for i, row in enumerate(ROWS):
        original_fibre = fibres['G'][i]
        for colouring in fibres[name][i]:
            chi = dict(zip(vertices, colouring))
            full_lifts = lifts(chi)
            matching_originals = [g for g in original_fibre
                                  if all(g[original_vertices.index(v)] == chi[v]
                                         for v in vertices)]
            assert full_lifts == matching_originals
            assert bool(full_lifts) == (not rainbow(chi))
            full_records.append(dict(identity(name, chi), rainbow=rainbow(chi),
                                     original_lifts=full_lifts))
            for pair in PAIRS:
                record = port_record(name, chi, pair)
                port_records.append(record)
                for block in record['actual_components']:
                    changed = switched(chi, block, pair)
                    assert proper(changed, edges)
                    assert switched(changed, block, pair) == chi
            if rainbow(chi) and row in NEGATIVE_ROWS:
                for target in ('a', 'b', 'q'):
                    pair = tuple(sorted((chi['n'], chi[target])))
                    block = block_at(components(vertices, edges, chi, pair), 'n')
                    contacts = sorted(set(block) & ({target} | set(OUTER)))
                    changed = switched(chi, block, pair)
                    failure_lifts = []
                    if not contacts:
                        assert word(changed) == row and not rainbow(changed)
                        failure_lifts = lifts(changed)
                        assert failure_lifts
                    if not original_fibre:
                        assert contacts
                    force_records.append(dict(identity(name, chi), target=target,
                                              pair=list(pair), component=block,
                                              contacts=contacts,
                                              original_fibre_empty=not original_fibre,
                                              status=('triggered' if not original_fibre
                                                      else 'not-triggered'),
                                              failure_original_lifts=failure_lifts))
                if name == 'G_a':
                    pair = tuple(sorted((chi['n'], chi['b'])))
                    block = block_at(components(vertices, edges, chi, pair), 'n')
                    anchors = {'01021': {'y', 'c'}, '01202': {'x'}, '01212': {'y'}}[row]
                    actual = sorted(set(block) & anchors)
                    generic = bool(set(block) & (set(OUTER) | {'b'}))
                    assert bool(actual) == generic
                    if not original_fibre:
                        assert actual
                    refined_records.append(dict(identity(name, chi), pair=list(pair),
                                                component=block, required_anchor_set=sorted(anchors),
                                                actual_contacts=actual,
                                                original_fibre_empty=not original_fibre,
                                                status=('triggered' if not original_fibre
                                                        else 'not-triggered')))
                if name == 'G_b':
                    tests = [('endpoint-join', (1, 3) if row != '01212' else (0, 3))]
                    if row == '01021':
                        tests.append(('q-to-a-or-x', (0, 3)))
                    for kind, pair in tests:
                        assert chi['b'] not in pair
                        partition = components(vertices, edges, chi, pair)
                        exterior = components(vertices, exterior_edges, chi, pair)
                        # Every added fan-B edge is incident to b; these
                        # palettes therefore use only original exterior edges.
                        assert partition == exterior
                        q_block = block_at(partition, 'q')
                        n_block = (block_at(partition, 'n')
                                   if chi['n'] in pair else None)
                        failing_block = None
                        if kind == 'q-to-a-or-x':
                            satisfied = bool(set(q_block) & {'a', 'x'})
                            if not satisfied:
                                failing_block = q_block
                        elif row == '01021':
                            assert 'c' in q_block  # actual original edge qc
                            satisfied = (q_block == n_block or 'y' in n_block)
                            if not satisfied:
                                failing_block = n_block
                        else:
                            satisfied = q_block == n_block
                            if not satisfied:
                                failing_block = next(block for block in (q_block, n_block)
                                                     if not (set(block) & set(OUTER)))
                        failure_lifts = []
                        switched_colours = None
                        if failing_block is not None:
                            changed = switched(chi, failing_block, pair)
                            assert word(changed) == row and not rainbow(changed)
                            assert proper(changed, edges)
                            failure_lifts = lifts(changed)
                            assert failure_lifts
                            switched_colours = [changed[v] for v in vertices]
                        if not original_fibre:
                            assert satisfied
                        fan_b_endpoint_records.append(dict(
                            identity(name, chi), kind=kind, pair=list(pair),
                            actual_components=partition, exterior_components=exterior,
                            q_component=q_block, n_component=n_block,
                            condition_satisfied=satisfied,
                            original_fibre_empty=not original_fibre,
                            status=('triggered' if not original_fibre else 'not-triggered'),
                            switched_offending_component=failing_block,
                            switched_full_colouring=switched_colours,
                            failure_original_lifts=failure_lifts))

# Full-colouring fan-A bijection. This is unconditional, and it does trigger on
# the fixed completed control (2 accepted = 1 + 1). Its rainbow corollary needs
# the original two empty fibres, which this control does not have.
assert {v for e in graphs['G_a'][1] if 'b' in e for v in e if v != 'b'} == {'a', 'c', 'q'}
accepted = fibres['G_a'][ROWS.index('01232')]
pair_targets = []
transfers = []
for colours in accepted:
    chi = dict(zip(reduced_vertices, colours))
    assert chi['q'] in (0, 1)
    changed = dict(chi, b=1 - chi['q'])
    assert proper(changed, graphs['G_a'][1])
    expected_row = '01202' if chi['q'] == 1 else '01212'
    assert word(changed) == expected_row
    changed_colours = [changed[v] for v in reduced_vertices]
    assert changed_colours in fibres['G_a'][ROWS.index(expected_row)]
    inverse = dict(changed, b=3)
    assert inverse == chi
    pair_targets.append((expected_row, changed_colours))
    transfers.append({'from': identity('G_a', chi), 'to': identity('G_a', changed),
                      'changed_vertices': ['b'], 'target_original_lifts': lifts(changed)})
expected_targets = [(row, colours) for row in ('01202', '01212')
                    for colours in fibres['G_a'][ROWS.index(row)]
                    if colours[reduced_vertices.index('q')] != 3]
assert sorted(pair_targets) == sorted(expected_targets)
original_pair_empty = all(not fibres['G'][ROWS.index(row)] for row in ('01202', '01212'))
if original_pair_empty:
    assert all(colours[reduced_vertices.index('n')] == 3 for colours in accepted)
    assert all(rainbow(dict(zip(reduced_vertices, colours)))
               for _, colours in expected_targets)

# A finite universal interface replay checks b's complete three-neighbour list
# and cap lift in every proper literal fan-A assignment with either pair row.
# This is the existing six-contact interface, not a larger patch family.
interface_transfers = []
for local in OLD['full_fibres']:
    if local['fan'] != 'a':
        continue
    rim = dict(zip(RIM, local['rim']))
    for row in ('01232', '01202', '01212'):
        chi = dict(zip(OUTER, map(int, row))) | rim
        if word(chi) != row or chi['q'] == chi['c']:
            continue
        if row == '01232':
            changed = dict(chi, b=1 - chi['q'])
            branch = 'accepted-to-pair'
            assert chi['q'] in (0, 1)
        elif chi['q'] == 3:
            if not rainbow(chi):
                continue
            changed = dict(chi, b=1 - chi['b'])
            branch = 'fourth-q-cross-lift'
            assert not rainbow(changed)
        else:
            changed = dict(chi, b=3)
            branch = 'pair-to-accepted'
        local_original = {e for e in original_edges if set(e) <= set(RIM) | {'p', 'h'}}
        assert proper(changed, fan_edges['G_a'] | cycle(OUTER) | {edge('q', 'c')})
        cap_lifts = [[p, h] for p, h in itertools.product(range(4), repeat=2)
                     if proper(dict(changed, p=p, h=h), local_original)]
        if branch == 'fourth-q-cross-lift':
            assert cap_lifts
        interface_transfers.append({'row': row, 'rim': [chi[v] for v in RIM],
                                    'branch': branch, 'target_row': word(changed),
                                    'target_rim': [changed[v] for v in RIM],
                                    'target_cap_lifts': cap_lifts})

# For pair rows with q in {0,1}, a whole 01 component can transfer the pair
# iff the bq component misses xy; no path from another colouring is imported.
component_transfers = []
for row in ('01202', '01212'):
    for colours in fibres['G_a'][ROWS.index(row)]:
        chi = dict(zip(reduced_vertices, colours))
        if chi['q'] == 3:
            continue
        partition = components(reduced_vertices, graphs['G_a'][1], chi, (0, 1))
        block = block_at(partition, 'b')
        assert 'q' in block
        blocked = bool(set(block) & {'x', 'y'})
        assert ('x' in block) == ('y' in block)
        changed = switched(chi, block, (0, 1))
        if not blocked:
            target = '01212' if row == '01202' else '01202'
            assert word(changed) == target
            assert [changed[v] for v in reduced_vertices] in fibres['G_a'][ROWS.index(target)]
        component_transfers.append(dict(identity('G_a', chi), component=block,
                                        blocked_by_xy=blocked,
                                        switched_full_colouring=[changed[v] for v in reduced_vertices],
                                        switched_row=word(changed)))

# Negative controls: the actual colouring and complete exterior partition are
# recomputed, so relabelling a record or borrowing another row cannot pass.
negative_controls = []
wrong_row = copy.deepcopy(port_records[0])
wrong_row['row'] = '01232' if wrong_row['row'] != '01232' else '01021'
negative_controls.append(('cross-row-label', wrong_row))
mixed = None
for left in port_records:
    for right in port_records:
        if (left['graph'] == right['graph'] and left['pair'] == right['pair']
                and left['row'] != right['row']
                and left['exterior_partition'] != right['exterior_partition']):
            mixed = copy.deepcopy(left)
            mixed['exterior_partition'] = right['exterior_partition']
            mixed['joined_components'] = joined([mixed['exterior_partition'], mixed['fan_partition']])
            break
    if mixed is not None:
        break
assert mixed is not None
negative_controls.append(('borrowed-other-row-exterior', mixed))
false_join = next(copy.deepcopy(r) for r in port_records if len(r['actual_components']) > 1)
false_join['joined_components'] = [sorted(v for block in false_join['actual_components'] for v in block)]
negative_controls.append(('false-component-join', false_join))
negative_results = []
for label, record in negative_controls:
    try:
        validate_port_record(record)
    except AssertionError:
        negative_results.append({'control': label, 'rejected': True, 'record': record})
    else:
        raise AssertionError('negative control accepted: ' + label)

RESULT = {
    'base': BASE, 'inputs': INPUTS,
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'scope': 'one unchanged frozen completed disk; full literal colourings and actual Kempe components',
    'vertices': {name: list(vertices) for name, (vertices, _) in graphs.items()},
    'edges': {name: sorted(edges) for name, (_, edges) in graphs.items()},
    'rows': ROWS, 'full_fibres_including_empty': fibres,
    'candidate_lift_records': full_records,
    'same_colouring_exterior_fan_joins': port_records,
    'conditional_forced_contacts': force_records,
    'conditional_fan_a_refined_anchors': refined_records,
    'conditional_fan_b_paired_endpoint_contacts': fan_b_endpoint_records,
    'fan_a_bijection': transfers,
    'fan_a_interface_transfers': interface_transfers,
    'fan_a_whole_component_pair_transfers': component_transfers,
    'original_pair_empty': original_pair_empty,
    'fan_a_pair_rainbow_and_accepted_n3_status': 'triggered' if original_pair_empty else 'not-triggered',
    'negative_controls': negative_results,
    'target_source_realized': False,
    'fan_b_three_rainbow_fibres_excluded': False,
    'smaller_bad_source_proved': False,
}
parser = argparse.ArgumentParser()
parser.add_argument('--check', action='store_true')
parser.add_argument('--certificate', type=Path)
args = parser.parse_args()
output = args.certificate or ROOT / 'certificate-v2.json'
normalized = json.loads(json.dumps(RESULT))
if args.check:
    assert json.loads(output.read_text()) == normalized, 'certificate differs'
else:
    with output.open('x') as stream:
        stream.write(json.dumps(RESULT, indent=2) + '\n')
print(json.dumps({'ok': True, 'full_fibre_counts': {name: list(map(len, fs)) for name, fs in fibres.items()},
                  'component_join_records': len(port_records),
                  'fan_a_bijection_size': len(transfers),
                  'interface_transfers': len(interface_transfers),
                  'conditional_force_statuses': sorted({r['status'] for r in force_records}),
                  'negative_controls_rejected': len(negative_results),
                  'target_source_realized': False}))
