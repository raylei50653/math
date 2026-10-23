#!/usr/bin/env python3
"""Frozen same-F U02 component-interface audit; no source graph enumeration."""
import argparse
from copy import deepcopy
import gzip
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[2]
BASE = 'cb8f8593e273a7426ecadd59797a6e643cc4768e'
JOINT = 'audits/2026-10-21-w7-I-joint-2c38d1d/'
SIX = 'audits/2026-10-21-w7-L-path-30dde27/six_degree/'
Y = 'HL_0'


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def packed(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def read(path):
    raw = (HERE / 'frozen' / path).read_bytes()
    return json.loads(gzip.decompress(raw) if path.endswith('.gz') else raw)


def authority():
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    require(manifest['base'] == BASE, 'BASE changed')
    for row in manifest['inputs']:
        frozen = (HERE / 'frozen' / row['path']).read_bytes()
        require(len(frozen) == row['bytes'] and sha256(frozen).hexdigest() == row['sha256'],
                'frozen authority drift: ' + row['path'])
        require((WORKSPACE / row['path']).read_bytes() == frozen,
                'live mathematical authority drift: ' + row['path'])
    for row in manifest['routing_entry']:
        frozen = (HERE / 'routing-entry' / row['path']).read_bytes()
        require(sha256(frozen).hexdigest() == row['entry_sha256'], 'routing snapshot drift')
        # Routing files are not mathematical premises. The entry bytes remain
        # frozen even if another authorized owner later changes live routing.
    return manifest


def blocks(boundary, partition):
    return [[v for v, b in zip(boundary, partition) if b == label]
            for label in sorted(set(partition))]


def alternating(boundary, vertices):
    positions = [boundary.index(v) for v in vertices]
    ordered = sorted(range(4), key=lambda i: positions[i])
    return all(ordered[i] % 2 != ordered[(i + 1) % 4] % 2 for i in range(4))


def boundary_restrictions(parent, transport, seed):
    rng = random.Random(seed)
    rows = []
    cases = {(c['target'], c['split_containing_0'][1]): c
             for c in parent['ordinary_C14_cases']}
    t_cases = {c['target']: c for c in transport['cases']
               if c['first_split_containing_0'] == [0, 2]}
    for target in (44459, 44466):
        c02, c01 = cases[target, 2], cases[target, 1]
        boundary = c02['ordered_F_boundary']
        colors = dict(zip(boundary, c02['literal_F_boundary_colors']))
        original01 = [r['complete_F_boundary_contacts']
                      for r in c01['complete_specific_F_types']
                      if r['same_initial_E_residual_gate'] and not r['forbidden_action_masks']]
        require(len(original01) == 4, 'complete initial 01 gate changed')
        for source_index, order_index in ((13, 1), (36, 3)):
            source = c02['complete_specific_F_types'][source_index]
            require(source['same_initial_E_residual_gate'] and not source['forbidden_action_masks'],
                    'named 02 type no longer surviving')
            contacts = source['complete_F_boundary_contacts']
            require(next(b for b in contacts if 'U' in b) == ['U'],
                    'K has another boundary contact')
            barrier = next(b for b in contacts if 'V' in b)
            require(Y in barrier and set(colors[v] for v in barrier) <= {1, 3},
                    'V and Y are not in one complete 13 block')
            forbidden = [b for b in contacts if set(colors[v] for v in b) <= {1, 3}
                         and b != barrier]
            require(len(forbidden) == 2, 'two other complete 13 blocks missing')
            witnesses = []
            for component in forbidden:
                anchor = next((v for v in ('z1', 'z3') if v in component), None)
                require(anchor is not None and alternating(boundary, ['U', 'V', anchor, Y]),
                        'missing alternating endpoints for full-component anticompleteness')
                witnesses.append(dict(complete_13_boundary_contacts=component,
                                      ordered_crossing_endpoints=['U', 'V', anchor, Y],
                                      no_edge_from_any_vertex_of_K=True))
            t = t_cases[target]['initial_types'][order_index]
            require(t['initial_F_partition'] == source['F_partition'], 'transport initial type mismatch')
            action = t['all_first_actions'][32]
            word = action['literal_F_boundary']
            require([(v, colors[v], c) for v, c in zip(boundary, word) if colors[v] != c]
                    == [('U', 0, 2)], 'not the complete U02-only boundary action')
            second = transport['normalized_second_palette_checks'][action['second_check_id']]
            require(len(second['surviving_type_ids']) == 1, 'unique switched 03 successor lost')
            successor = second['complete_necessary_NC_types'][second['surviving_type_ids'][0]]
            successor_blocks = blocks(boundary, successor['F_partition'])
            image = transport['complete_boundary_images'][action['first_action_image_id']]
            require(image['literal_F_boundary'] == word, 'transport image mismatch')
            kernel = transport['complete_normalized_seven_point_kernels'][image['normalized_complete_kernel_id']]
            require(not kernel['has_forbidden_full_join'], 'named switched kernel is forbidden')
            caps = {r['state']: r for r in transport['complete_original_cap_kernel']}
            full_caps = [caps[s] for s in sorted({r['canonical_D_cap_state']
                                                for r in kernel['complete_seven_point_fibre']})]
            rows.append(dict(target=target, initial_02_type=source_index,
                             complete_initial_02_contacts=contacts,
                             complete_initial_01_gate=original01,
                             barrier_complete_13_contacts=barrier,
                             forbidden_component_adjacencies=witnesses,
                             full_03_successor_boundary_contacts=successor_blocks,
                             actual_K_boundary_contacts=['U'],
                             successor_global_inverse=image['whole_colour_inverse'],
                             complete_successor_seven_point_kernel=kernel,
                             complete_successor_original_cap_records=full_caps,
                             initial_03_type_choices=[4, 9],
                             last_exit_lemma_requires_initial_03_type=4,
                             pair_excluded=False))
    rng.shuffle(rows)
    return sorted(rows, key=lambda r: (r['target'], r['initial_02_type']))


def components(vertices, edges):
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        if a in adjacency and b in adjacency:
            adjacency[a].add(b); adjacency[b].add(a)
    result = []
    while adjacency:
        todo = [min(adjacency)]; seen = set()
        while todo:
            v = todo.pop()
            if v in seen:
                continue
            seen.add(v); todo.extend(adjacency[v] - seen)
        result.append(sorted(seen))
        for v in seen:
            del adjacency[v]
    return sorted(result)


def switched_induced(colors, edges, K, palette):
    """Exact delete/insert descriptor, retaining every rootless component."""
    retained = {v for v, c in colors.items() if c in palette and (v not in K or (c ^ 2) in palette)}
    inserted = {v for v in K if colors[v] not in palette and (colors[v] ^ 2) in palette}
    selected = retained | inserted
    return sorted(selected), sorted([list(e) for e in edges if set(e) <= selected])


def local_links(seed):
    # Exhaustive finite cyclic links at a distinguished private X3, not source
    # disks. Membership bits are constrained by every original link edge.
    degree_five = set()
    degrees = {}
    wheel_checks = 0
    rng = random.Random(seed)
    for degree in (5, 6):
        words = list(product((0, 1, 2), repeat=degree)); rng.shuffle(words)
        admitted = 0; missing2 = 0
        for word in words:
            if any(word[i] == word[(i + 1) % degree] for i in range(degree)):
                continue
            indices02 = [i for i, c in enumerate(word) if c != 1]
            for values in product((False, True), repeat=len(indices02)):
                membership = dict(zip(indices02, values))
                zeros = [membership[i] for i, c in enumerate(word) if c == 0]
                if not (True in zeros and False in zeros):
                    continue
                if any(word[i] != 1 and word[(i + 1) % degree] != 1
                       and membership[i] != membership[(i + 1) % degree]
                       for i in range(degree)):
                    continue
                admitted += 1
                require(word.count(1) >= 2, 'missing two separating colour-1 neighbours')
                if degree == 5:
                    require(sorted(word) == [0, 0, 1, 1, 2], 'degree-five full link classification failed')
                    j = word.index(2)
                    adjacent0 = [i for i in ((j - 1) % degree, (j + 1) % degree) if word[i] == 0]
                    require(len(adjacent0) == 1 and membership[j] == membership[adjacent0[0]],
                            'fifth neighbour K membership is not forced by the original link edge')
                    degree_five.add(membership[j])
                if 2 not in word:
                    missing2 += 1
                    require(degree % 2 == 0 and degree >= 6, 'even high-degree branch lost')
            if word.count(0) >= 2:
                colors = {'X': 3, **{'r'+str(i): c for i, c in enumerate(word)}}
                edges = sorted({tuple(sorted(('X', 'r'+str(i)))) for i in range(degree)} |
                               {tuple(sorted(('r'+str(i), 'r'+str((i+1) % degree)))) for i in range(degree)})
                root = 'r'+str(word.index(0))
                K = set(next(c for c in components({v for v, c in colors.items() if c in {0, 2}}, edges)
                             if root in c))
                changed = {v: (c ^ 2 if v in K else c) for v, c in colors.items()}
                for palette in combinations(range(4), 2):
                    descriptor = switched_induced(colors, edges, K, set(palette))
                    actual_vertices = sorted(v for v, c in changed.items() if c in palette)
                    actual_edges = sorted([list(e) for e in edges if set(e) <= set(actual_vertices)])
                    require(descriptor == (actual_vertices, actual_edges), 'exact switch descriptor failed')
                    require(components(descriptor[0], descriptor[1]) == components(actual_vertices, actual_edges),
                            'rootless switched component omitted')
                    wheel_checks += 1
        degrees[str(degree)] = dict(admitted_complete_marked_links=admitted,
                                   admitted_without_colour2=missing2)
    require(degree_five == {False, True}, 'one fifth-neighbour side wrongly excluded')
    require(degrees['6']['admitted_without_colour2'] > 0, 'even degree-six control missing')
    return dict(complete_link_calibrations=degrees,
                fifth_neighbour_membership_sides_retained=[False, True],
                exact_six_palette_wheel_checks=wheel_checks,
                calibration_is_original_source=False)


def build(seed=None):
    manifest = authority()
    parent = read(SIX+'certificate-v2.json.gz')
    transport = read(JOINT+'transport/certificate.json.gz')
    rows = boundary_restrictions(parent, transport, seed)
    kernels = transport['complete_normalized_seven_point_kernels']
    return dict(base=BASE, scope='ordinary Type I; exact K=U02; types 13/36; full same-F components',
                component_interface_rows=rows,
                local_link_and_switch_calibration=local_links(seed),
                upstream_complete_fibre_custody=dict(
                    seven_point_kernels=len(kernels),
                    empty_seven_point_fibres=sum(not k['complete_seven_point_fibre'] for k in kernels),
                    original_cap_states=len(transport['complete_original_cap_kernel']),
                    transport_sha256=next(r['sha256'] for r in manifest['inputs']
                                          if r['path'] == JOINT+'transport/certificate.json.gz')),
                private_13_components_discarded=False,
                degree_at_least_six_branch_excluded=False,
                arbitrary_source_size_bound=None,
                new_pair_exclusions=0, original_source_realized=False,
                original_source_controls_triggered=0, new_Lean=False)


def validate(value, expected):
    require(value == expected, 'certificate differs from full frozen reconstruction')


def negatives(expected):
    trials = []
    c = deepcopy(expected); c['component_interface_rows'][0]['barrier_complete_13_contacts'].remove(Y); trials.append(c)
    c = deepcopy(expected); c['component_interface_rows'][0]['forbidden_component_adjacencies'].pop(); trials.append(c)
    c = deepcopy(expected); c['component_interface_rows'][0]['actual_K_boundary_contacts'].append('z4'); trials.append(c)
    c = deepcopy(expected); c['component_interface_rows'][0]['complete_successor_seven_point_kernel']['complete_seven_point_fibre'].pop(); trials.append(c)
    c = deepcopy(expected)
    nonempty = next(lifts for r in c['component_interface_rows'][0]['complete_successor_original_cap_records']
                    for graph in r['complete_original_cap_fibres'].values() for lifts in graph.values() if lifts)
    nonempty.pop(); trials.append(c)
    c = deepcopy(expected); c['degree_at_least_six_branch_excluded'] = True; trials.append(c)
    c = deepcopy(expected); c['new_pair_exclusions'] = 1; trials.append(c)
    for damaged in trials:
        try:
            validate(damaged, expected)
        except ValueError:
            pass
        else:
            raise ValueError('negative control accepted')
    # Non-alternating endpoint data cannot justify the Jordan implication.
    boundary = read(SIX+'certificate-v2.json.gz')['ordinary_C14_cases'][0]['ordered_F_boundary']
    require(not alternating(boundary, ['U', 'V', Y, 'z1']), 'noncrossing control misclassified')
    # A colour-2 vertex of K enters the new 03 graph. Omitting private inserted
    # vertices is a concrete incorrect surgery, even for this five-wheel.
    colors = {'X': 3, 'r0': 0, 'r1': 1, 'r2': 0, 'r3': 1, 'r4': 2}
    edges = sorted({tuple(sorted(('X', 'r'+str(i)))) for i in range(5)} |
                   {tuple(sorted(('r'+str(i), 'r'+str((i+1) % 5)))) for i in range(5)})
    K = {'r0', 'r4'}
    actual = switched_induced(colors, edges, K, {0, 3})
    wrong_vertices = sorted(v for v, c in colors.items() if c in {0, 3} and v not in K)
    require(actual[0] != wrong_vertices and 'r4' in actual[0],
            'omitted inserted private vertex was accepted as an exact switch')
    return len(trials) + 2


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build', action='store_true')
    ap.add_argument('--seed', type=int)
    ap.add_argument('--certificate', type=Path, default=HERE/'certificate.json')
    args = ap.parse_args()
    expected = json.loads(packed(build(args.seed)))
    rejected = negatives(expected)
    if args.build:
        with args.certificate.open('xb') as stream:
            stream.write(packed(expected))
    validate(json.loads(args.certificate.read_text()), expected)
    print(json.dumps(dict(result='PASS', base=BASE, full_component_antiadjacency_rows=4,
                          full_13_component_antiadjacencies=8,
                          initial_03_choices_retained_per_row=2,
                          local_calibration=expected['local_link_and_switch_calibration'],
                          complete_fibre_custody=expected['upstream_complete_fibre_custody'],
                          frozen_and_live_mathematical_input_drift=0,
                          original_source_controls_triggered=0,
                          new_pair_exclusions=0, negative_controls=rejected), sort_keys=True))


if __name__ == '__main__':
    main()
