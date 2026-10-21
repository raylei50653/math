#!/usr/bin/env python3
"""Type-I six-degree z5: fixed-exterior seven-point fibres and literal C14 orbits.

Only three specific splits of the two named literal C14 inputs are enumerated.
The V=w alias uses actual E-component actions, never a simple-C14 assumption.
"""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import argparse
import gzip
import importlib.util
import json
import random
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = '30dde27293b5d3ad63c75fae73cda5be96db705b'
COUNT = 'audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/'
COLLAR = 'audits/2026-10-21-w7-profile0-13e51db/check.py'
HELPER = 'audits/2026-10-21-w7-k1-mixed-30dde27/exterior/check.py'
OLD = 'audits/2026-10-21-w7-k1-mixed-30dde27/full-exterior-v2.json.gz'
P = ('n', 'u4', 'u3', 'u2', 'u1', 'L')
MUTABLE = (*P, 'z5')
Y = 'HL_0'
TAIL = ('c', 's', 'v', 'w', 't')
B14 = ('a', 'z1', 'z2', 'z3', 'z4', 'V', 'U', Y, 'q', *TAIL)
B13 = ('a', 'z1', 'z2', 'z3', 'z4', 'z5', Y, 'q', *TAIL)
RIM = ('a', *P, 'q', *TAIL)
ROWS = ('01012', '01021', '01023', '01201', '01202',
        '01203', '01212', '01213', '01231', '01232')


def require(ok, why):
    if not ok:
        raise ValueError(why)


def packed(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def canonical(word):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in word)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def inputs():
    manifest = json.loads((HERE / 'BASE.json').read_text())
    require(manifest['base'] == BASE, 'exclusive BASE changed')
    for row in manifest['inputs']:
        raw = (HERE / 'frozen' / row['path']).read_bytes()
        require(len(raw) == row['bytes'] and sha256(raw).hexdigest() == row['sha256'], 'frozen input drift')
    cap = json.loads(gzip.decompress((HERE / 'frozen' / COUNT / 'caps.json.gz').read_bytes()))
    old = json.loads(gzip.decompress((HERE / 'frozen' / OLD).read_bytes()))
    source = load_module('frozen_collar', HERE / 'frozen' / COLLAR)
    helper = load_module('frozen_mixed_helpers', HERE / 'frozen' / HELPER)
    return source, helper, cap, old


def graph_type_I(source, alias=False):
    _, raw = source.collar(0, [0, 0, 0, 0, 0, 1], with_graph=True)
    graph = {v: set(row) for v, row in raw.items()}
    for a, b in [('z5', 'U'), ('z5', 'V'), (Y, 'U'), ('U', 'V'), ('V', 'z4')]:
        a = 'w' if alias and a == 'V' else a
        b = 'w' if alias and b == 'V' else b
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    require(graph['z5'] == {'L', 'u1', 'z4', 'w' if alias else 'V', 'U', Y},
            'six-degree complete z5 star changed')
    return graph


def check_ordinary_strip_topology(source):
    graph = graph_type_I(source)
    A = B14[:9]
    vertices = set(P) | set(A) | {'z5'}
    faces = [face for face in combinations(sorted(vertices), 3)
             if all(b in graph[a] for a, b in combinations(face, 2))]
    incidence = Counter(tuple(sorted(edge)) for face in faces for edge in combinations(face, 2))
    boundary = ['a', *P, 'q', *reversed(A[1:-1])]
    rim_edges = {tuple(sorted((boundary[i], boundary[(i + 1) % len(boundary)])))
                 for i in range(len(boundary))}
    require(len(vertices) == 16 and len(boundary) == len(set(boundary)) == 15,
            'ordinary original-face strip vertex count changed')
    require(len(faces) == 15 and vertices - set(boundary) == {'z5'},
            'complete z5 fan was not glued into the original strip')
    require({edge for edge, count in incidence.items() if count == 1} == rim_edges,
            'ordinary original-face strip has the wrong single boundary')
    require(all(count in (1, 2) for count in incidence.values()) and
            len(vertices) - len(incidence) + len(faces) == 1, 'ordinary strip disk incidence/Euler failed')


def complete_fibre(fixed, graph, cap, cap_index, helper, used, rng):
    domains = [sorted(set(range(4)) - {fixed[x] for x in graph[t] if x in fixed}) for t in MUTABLE]
    if rng:
        for domain in domains:
            rng.shuffle(domain)
    rows = []
    for colors in product(*domains):
        assignment = fixed | dict(zip(MUTABLE, colors))
        if not all(assignment[a] != assignment[b] for a in MUTABLE for b in graph[a] if b in assignment):
            continue
        rim = tuple(assignment[v] for v in RIM)
        require(all(rim[i] != rim[(i + 1) % 13] for i in range(13)), 'joined original D rim improper')
        normalized = canonical(rim)
        sid = cap_index[normalized]
        used.add(sid)
        fibres, bad = helper.cap_lifts(normalized)
        require(all([len(fibres[g][r]) for r in ROWS]
                    == [m[sid] for m in cap['matrices'][g]] for g in helper.ZERO),
                'complete cap assignment differs from original matrices')
        witness = helper.literal_cap_witness(rim, normalized, fibres) if bad else None
        rows.append({'mutable_colors': list(colors), 'canonical_D_cap_state': sid,
                     'forbidden_cap': witness})
    rows.sort(key=lambda row: row['mutable_colors'])
    return {'complete_seven_point_fibre': rows,
            'has_forbidden_full_join': any(row['forbidden_cap'] for row in rows)}


def independent_specific(literal, palette, helper):
    n = len(literal)
    runs = []
    for i, c in enumerate(literal):
        if runs and (literal[runs[-1][-1]] in palette) == (c in palette):
            runs[-1].append(i)
        else:
            runs.append([i])
    if (literal[0] in palette) == (literal[-1] in palette):
        runs[0] = runs[-1] + runs[0]
        runs.pop()
    sides = [[run for run in runs if (literal[run[0]] in palette) == side] for side in (False, True)]
    transitions = len(runs)
    require(len(sides[0]) == len(sides[1]), 'cyclic run counts changed')
    expected_blocks = transitions // 2 + 1
    families = [list(helper.set_partitions(len(side))) for side in sides]
    accepted = set()
    for left, right in product(*families):
        if max(left) + max(right) + 2 != expected_blocks:
            continue
        word = [None] * n
        for side, partition in enumerate((left, right)):
            for run, b in zip(sides[side], partition):
                for i in run:
                    word[i] = (side, b)
        normalized = canonical(word)
        if helper.is_nc(normalized):
            accepted.add(normalized)
    return sorted(accepted), len(families[0]) * len(families[1])


def source_E_types(old, target, mate):
    row = next(r for r in old['L_complete_residual']
               if r['literal_E_target'][10] == target and r['split_containing_0'] == [0, mate])
    result = []
    for entry in row['complete_surviving_columns']:
        partition = canonical([next(j for j, block in enumerate(entry['component_blocks']) if name in block)
                               for name in B13])
        result.append({'column_id': entry['column_id'], 'partition': partition,
                       'component_blocks': entry['component_blocks']})
    require(len(result) == {1: 4, 2: 2, 3: 1}[mate], 'original E necessary residual changed')
    return result


def add_back_z5(partition, literal, palette):
    """Exact SAME-initial-colouring component join, before any action."""
    count = max(partition) + 1
    parents = list(range(count + 1))

    def root(x):
        while parents[x] != x:
            x = parents[x]
        return x

    colors = dict(zip(B14, literal))
    for name in ('z4', 'V', 'U', Y):
        if (colors[name] in palette) == (3 in palette):
            parents[root(partition[B14.index(name)])] = root(count)
    labels = {name: partition[i] for i, name in enumerate(B14)} | {'z5': count}
    return canonical([root(labels[name]) for name in B13])


def ordinary_case(target, mate, source, helper, cap, index, old, used, rng):
    literal = (0, 3, 0, 3, 0, 1, 0, 1, 3, 1, 2, target, 1 - target, 2)
    palette = (0, mate)
    partitions = sorted(helper.nc_specific(literal, palette))
    independent, pairs = independent_specific(literal, palette, helper)
    require(partitions == independent, 'literal C14 NC coverage differs from independent cyclic-run enumeration')
    require(len(partitions) == {1: 42, 2: 42, 3: 14}[mate], 'specific C14 coverage changed')
    blocks = max(partitions[0]) + 1
    require(blocks == {1: 6, 2: 6, 3: 5}[mate], 'specific C14 transition/block count changed')
    allowed = source_E_types(old, target, mate)
    words = sorted({tuple(c ^ (mate if mask >> b & 1 else 0) for c, b in zip(literal, p))
                    for p in partitions for mask in range(1 << blocks)})
    word_ids = {word: i for i, word in enumerate(words)}
    processing = list(range(len(words)))
    if rng:
        rng.shuffle(processing)
    graph = graph_type_I(source)
    images = {}
    for i in processing:
        word = words[i]
        require(all(word[j] != word[(j + 1) % 14] for j in range(14)), 'F component action not proper on C14')
        images[i] = {'boundary_colors': list(word),
                     **complete_fibre(dict(zip(B14, word)), graph, cap, index, helper, used, rng)}
    images = [images[i] for i in range(len(words))]
    types, raw_survivors, gated_survivors = [], [], []
    for p in partitions:
        projection = add_back_z5(p, literal, palette)
        gate = any(projection == row['partition'] for row in allowed)
        action_ids = [word_ids[tuple(c ^ (mate if mask >> b & 1 else 0) for c, b in zip(literal, p))]
                      for mask in range(1 << blocks)]
        require(len(set(action_ids)) == 1 << blocks, 'complete F boundary action lost')
        bad = [mask for mask, i in enumerate(action_ids) if images[i]['has_forbidden_full_join']]
        if not bad:
            raw_survivors.append(list(p))
            if gate:
                gated_survivors.append(list(p))
        types.append({'F_partition': list(p),
                      'complete_F_boundary_contacts': [[B14[i] for i in range(14) if p[i] == block]
                                                       for block in range(blocks)],
                      'add_back_z5_projected_original_E_partition': list(projection),
                      'same_initial_E_residual_gate': gate,
                      'all_complete_F_action_image_ids': action_ids,
                      'forbidden_action_masks': bad})
    require(len(raw_survivors) == {1: 20, 2: 4, 3: 2}[mate], 'raw F necessary survivor count changed')
    require(len(gated_survivors) == {1: 4, 2: 4, 3: 2}[mate], 'same-initial E gate changed')
    require(sum(row['same_initial_E_residual_gate'] for row in types) == len(gated_survivors),
            'a previously stated passing E gate was killed')
    initial = complete_fibre(dict(zip(B14, literal)), graph, cap, index, helper, used, rng)
    require(len(initial['complete_seven_point_fibre']) == 6 and not initial['has_forbidden_full_join'],
            'original-phase complete seven-point relation changed')
    return {'target': 44459 if target == 0 else 44466, 'split_containing_0': [0, mate],
            'ordinary_U_V_both_original_E_private': True, 'ordered_F_boundary': list(B14),
            'literal_F_boundary_colors': list(literal), 'boundary_palette_transitions': 2 * (blocks - 1),
            'independent_cyclic_run_partition_pairs': pairs,
            'complete_initial_seven_point_fibre': initial,
            'original_E_residual_types': allowed, 'complete_specific_F_types': types,
            'complete_F_image_fibres': images, 'raw_surviving_types': raw_survivors,
            'surviving_types_after_same_initial_E_gate': gated_survivors,
            'source_subbranch_excluded': False}


def alias_case(source, helper, cap, index, old, used, rng):
    """V=w, target44459: original E acts; no NC assertion about pinched F."""
    graph = graph_type_I(source, alias=True)
    literal = (0, 3, 0, 3, 0, 3, 1, 3, 1, 2, 0, 1, 2)
    source_types = source_E_types(old, 0, 1)
    permitted = [entry for entry in source_types
                 if entry['partition'][B13.index('w')] == entry['partition'][B13.index(Y)]]
    require(len(permitted) == 2, 'V=w must use the actual Y01 block')
    rows = []
    for entry in permitted:
        p = entry['partition']; yblock = p[B13.index(Y)]; blocks = max(p) + 1
        actions = []
        for mask in range(1 << blocks):
            fixed = {name: c ^ ((mask >> b) & 1) for name, c, b in zip(B13, literal, p)}
            fixed.pop('z5')
            fixed['U'] = (mask >> yblock) & 1
            require(fixed['w'] == (1 ^ ((mask >> yblock) & 1)), 'alias component action inconsistent')
            fibre = complete_fibre(fixed, graph, cap, index, helper, used, rng)
            require(not fibre['has_forbidden_full_join'], 'alias actual-E01 action unexpectedly excludes source')
            actions.append({'complete_original_E_action_mask': mask,
                            'fixed_original_F_colors': fixed, **fibre})
        rows.append({'original_E_column_id': entry['column_id'], 'original_E_partition': list(p),
                     'all_complete_original_E01_actions': actions})
    boundary_walk = ['w' if n == 'V' else n for n in B14]
    require(len(boundary_walk) == 14 and len(set(boundary_walk)) == 13,
            'alias incorrectly asserted to expose a simple C14')
    return {'target': 44459, 'identity': 'V=w', 'U_original_E_private': True,
            'boundary_walk_with_original_w_repeated': boundary_walk,
            'simple_C14_NC_lemma_applied': False, 'actual_E01_cases': rows,
            'other_F_palettes_covered': False, 'source_subbranch_excluded': False}


def compute(seed):
    source, helper, cap, old = inputs()
    check_ordinary_strip_topology(source)
    index = {tuple(row): i for i, row in enumerate(cap['states'])}
    rng = random.Random(seed) if seed is not None else None
    used = set()
    ordinary = [ordinary_case(target, mate, source, helper, cap, index, old, used, rng)
                for target in (0, 1) for mate in (1, 2, 3)]
    alias = alias_case(source, helper, cap, index, old, used, rng)
    full_cap_kernel = [{'state': sid, 'canonical_D_rim': cap['states'][sid],
                        'complete_original_cap_fibres': helper.cap_lifts(tuple(cap['states'][sid]))[0]}
                       for sid in sorted(used)]
    return {'base': BASE, 'scope': 'original Type-I six-degree z5; complete seven-point joins and specific literal F actions',
            'mutable_original_vertices': list(MUTABLE), 'ordinary_C14_cases': ordinary,
            'V_equals_w_alias_case': alias, 'complete_original_cap_kernel': full_cap_kernel,
            'ordinary_Type_I_excluded': False, 'alias_Type_I_excluded': False,
            'profile0_excluded': False, 'actual_F_source_realized': False,
            'independent_palettes_joined_as_source': False,
            'whole_C14_family_enumerated': False, 'empty_inner_fibre_used_as_exterior_zero': False,
            'new_Lean': False, 'LP_run': False}


def verify(actual, expected):
    require(actual == expected, 'incomplete full fibre, alias abuse, or enlarged closure')


def controls(result):
    rejected = 0
    for field in ('ordinary_Type_I_excluded', 'actual_F_source_realized',
                  'independent_palettes_joined_as_source', 'whole_C14_family_enumerated',
                  'empty_inner_fibre_used_as_exterior_zero'):
        damaged = deepcopy(result); damaged[field] = True
        try:
            verify(damaged, result)
        except ValueError:
            rejected += 1
    damaged = deepcopy(result)
    damaged['ordinary_C14_cases'][0]['boundary_palette_transitions'] = 12
    try:
        verify(damaged, result)
    except ValueError:
        rejected += 1
    damaged = deepcopy(result)
    damaged['V_equals_w_alias_case']['simple_C14_NC_lemma_applied'] = True
    try:
        verify(damaged, result)
    except ValueError:
        rejected += 1
    damaged = deepcopy(result)
    damaged['ordinary_C14_cases'][0]['complete_initial_seven_point_fibre']['complete_seven_point_fibre'].pop()
    try:
        verify(damaged, result)
    except ValueError:
        rejected += 1
    require(rejected == 8, 'negative controls failed')
    return rejected


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build', action='store_true')
    ap.add_argument('--seed', type=int)
    ap.add_argument('--certificate', type=Path, default=HERE / 'certificate-v2.json.gz')
    args = ap.parse_args()
    result = json.loads(packed(compute(args.seed)))
    rejected = controls(result)
    if args.build:
        with args.certificate.open('xb') as f:
            with gzip.GzipFile(fileobj=f, mode='wb', mtime=0) as z:
                z.write(packed(result))
    verify(json.loads(gzip.decompress(args.certificate.read_bytes())), result)
    print(json.dumps({'result': 'PASS', 'ordinary_literal_split_cases': 6,
                      'specific_partition_counts_per_target': [42, 42, 14],
                      'raw_survivors_per_target': [20, 4, 2],
                      'same_initial_E_gate_survivors_per_target': [4, 4, 2],
                      'initial_complete_seven_point_lifts': 6,
                      'V_equals_w_actual_E01_cases': 2,
                      'used_original_full_cap_states': len(result['complete_original_cap_kernel']),
                      'negative_controls': rejected, 'new_source_exclusions': []}, sort_keys=True))


if __name__ == '__main__':
    main()
