#!/usr/bin/env python3
"""Independent exact short-patch relations, initial joins and same-E alias proof.

The current graph has not been realised.  All small controls are local only.
Read-only replay checks frozen bytes, complete tuples, zeros and scope together.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
import gzip
import importlib.util
from itertools import product
import json
import os
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = '30dde27293b5d3ad63c75fae73cda5be96db705b'
P = ('n', 'u4', 'u3', 'u2', 'u1', 'L')
RIM = ('a', *P, 'q', 'c', 's', 'v', 'w', 't')
B6 = ('L', 'u1', 'z4', 'V', 'U', 'Y')
ROWS = ('01012', '01021', '01023', '01201', '01202',
        '01203', '01212', '01213', '01231', '01232')
ZERO = {'G': {'01021', '01202', '01212'}, 'Q1': {'01232'},
        'J1': {'01202', '01212'}}
COUNT = 'audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/caps.json.gz'
COLLAR = 'audits/2026-10-21-w7-profile0-13e51db/check.py'
PARENT = 'audits/2026-10-21-w7-k1-mixed-30dde27/full-exterior-v3.json.gz'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def packed(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def canonical(word):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in word)


def inputs():
    manifest = json.loads((HERE / 'BASE.json').read_text())
    require(manifest['base'] == BASE, 'BASE changed')
    for item in manifest['inputs']:
        frozen = (HERE / 'frozen' / item['path']).read_bytes()
        require(len(frozen) == item['bytes'] and sha256(frozen).hexdigest() == item['sha256'],
                'frozen input drift: ' + item['path'])
        require(frozen == (ROOT / item['path']).read_bytes(), 'authority drift: ' + item['path'])
    caps = json.loads(gzip.decompress((HERE / 'frozen' / COUNT).read_bytes()))
    parent = json.loads(gzip.decompress((HERE / 'frozen' / PARENT).read_bytes()))
    spec = importlib.util.spec_from_file_location('frozen_L_collar', HERE / 'frozen' / COLLAR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return manifest, caps, parent, module


def all_lifts(graph, fixed, variables, rng):
    result = []
    def visit(partial):
        remaining = set(variables) - partial.keys()
        if not remaining:
            result.append([partial[v] for v in variables])
            return
        whole = fixed | partial
        domains = {v: sorted(set(range(4)) - {whole[w] for w in graph[v] if w in whole})
                   for v in remaining}
        v = min(remaining, key=lambda x: (len(domains[x]), x))
        domain = domains[v]
        if rng:
            rng.shuffle(domain)
        for colour in domain:
            visit(partial | {v: colour})
    visit({})
    return sorted(result)


def boundary_relations(rng):
    cycle = [(B6[i], B6[(i + 1) % 6]) for i in range(6)]
    rows = sorted({canonical(word) for word in product(range(4), repeat=6)
                   if all(word[i] != word[(i + 1) % 6] for i in range(6))})
    require(len(rows) == 31, 'complete proper B6 coverage changed')
    result = []
    for word in rows:
        fixed = dict(zip(B6, word))
        fibres = {}
        for kind in ('I', 'II'):
            edges = cycle + ([('Z', v) for v in B6] if kind == 'I' else
                             [('Z', v) for v in ('L', 'u1', 'z4', 'Y', 'K')] +
                             [('K', v) for v in ('Y', 'U', 'V', 'z4')])
            graph = {}
            for a, b in edges:
                graph.setdefault(a, set()).add(b)
                graph.setdefault(b, set()).add(a)
            actual = all_lifts(graph, fixed, ('Z',) if kind == 'I' else ('Z', 'K'), rng)
            expected = ([[s] for s in range(4) if s not in word] if kind == 'I' else
                        [[s, k] for s, k in product(range(4), repeat=2)
                         if s not in {word[0], word[1], word[2], word[5], k}
                         and k not in {word[5], word[4], word[3], word[2], s}])
            require(actual == expected, 'complete B6 fibre formula lost a tuple or zero')
            fibres[kind] = actual
        result.append({'literal_B6': list(word), 'all_inner_lifts': fibres})
    by_word = {tuple(row['literal_B6']): row['all_inner_lifts'] for row in result}
    require(by_word[(0, 1, 0, 1, 0, 1)] == {'I': [[2], [3]], 'II': [[2, 3], [3, 2]]},
            'two-colour replacement obstruction changed')
    require(by_word[(0, 1, 0, 1, 0, 2)] == {'I': [[3]], 'II': []},
            'W6 cannot replace type II on every boundary')
    return {'ordered_interface': list(B6), 'all_31_complete_fibres': result,
            'unequal_nonemptiness_rows': sum(bool(r['all_inner_lifts']['I']) !=
                                             bool(r['all_inner_lifts']['II']) for r in result),
            'uniform_strictly_smaller_exact_boundary_relation_exists': False,
            'source_conditioned_smaller_bad_excluded': False}


def raw_caps(word):
    a, n, u4, u3, u2, u1, L, q, c, s, v, w, t = word
    spokes = {n, u4, u3, u2, u1, L}
    right = [(x, y, r) for x, y, r in product(range(4), repeat=3)
             if r not in (s, v, w, t, x, y) and x not in (c, s, y) and y not in (a, t)]
    left = {
        'G': [(b, p, h, R) for b, p, h, R in product(range(4), repeat=4)
              if b not in (a, c, q, p) and p not in (a, q, n, h)
              and h not in (q, L, R, n) and R not in spokes],
        'Q1': [(b, R) for b, R in product(range(4), repeat=2)
               if b == n and R == q and b not in (a, c, q) and R not in spokes],
        'J1': [(b, R) for b, R in product(range(4), repeat=2)
               if b == L and a != R and b not in (a, c, q) and R not in spokes]}
    result = {graph: {row: [] for row in ROWS} for graph in ZERO}
    for graph in ZERO:
        for ls, rs in product(left[graph], right):
            frame = (rs[0], rs[1], a, ls[0], c)
            row = ''.join(map(str, canonical(frame)))
            result[graph][row].append({'left_cap': list(ls), 'right_cap': list(rs),
                                       'literal_original_frame': list(frame)})
    return result


def initial_short_fibres(module, caps, rng):
    cap_index = {tuple(word): i for i, word in enumerate(caps['states'])}
    cases, cap_cache = [], {}
    for kind, target in product(('I', 'II'), (44459, 44466)):
        U_cases = ('U',) if kind == 'I' else ('U', 'v' if target == 44459 else 'w')
        V_cases = ('V', 'w') if target == 44459 else ('V',)
        for U, V in product(U_cases, V_cases):
            _, collar = module.collar(0, [0, 0, 0, 0, 0, 1], with_graph=True)
            graph = {v: adj - {'p', 'h', 'R'} for v, adj in collar.items() if v not in {'p', 'h', 'R'}}
            edges = [(RIM[i], RIM[(i + 1) % 13]) for i in range(13)]
            edges += [('HL_0', U), (U, V), (V, 'z4')]
            edges += ([('z5', U), ('z5', V)] if kind == 'I' else
                      [('K', v) for v in ('HL_0', U, V, 'z4', 'z5')])
            for a, b in edges:
                graph.setdefault(a, set()).add(b)
                graph.setdefault(b, set()).add(a)
            require(graph['z5'] == {'L', 'u1', 'z4', 'HL_0', U, V} if kind == 'I' else
                    graph['z5'] == {'L', 'u1', 'z4', 'HL_0', 'K'}, 'full original z5 star changed')
            if kind == 'II':
                require(len(graph['K']) == 5, 'full original K five-star changed')
            original = dict(zip(RIM, (0, 1, 2, 1, 2, 1, 2, 3, 1, 2,
                                      0 if target == 44459 else 1, 1 if target == 44459 else 0, 2)))
            original |= {'z1': 3, 'z2': 0, 'z3': 3, 'z4': 0, 'z5': 3,
                         'HL_0': 1, U: 0, V: 1}
            if kind == 'II':
                original['K'] = 2
            require(all(original[a] != original[b] for a in graph for b in graph[a]),
                    'initial same-point source assignment improper')
            mutable = (*P, 'z5') + (() if kind == 'I' else ('K',))
            fixed = {v: c for v, c in original.items() if v not in mutable}
            lifts = all_lifts(graph, fixed, mutable, rng)
            require(len(lifts) == 6, 'initial joint seven/eight-point fibre coverage changed')
            records = []
            for lift in lifts:
                whole = fixed | dict(zip(mutable, lift))
                rim = tuple(whole[v] for v in RIM)
                require(all(rim[i] != rim[(i + 1) % 13] for i in range(13)), 'D rim improper')
                key = ''.join(map(str, rim))
                if key not in cap_cache:
                    full = raw_caps(rim)
                    sid = cap_index[canonical(rim)]
                    require(all([len(full[g][row]) for row in ROWS] ==
                                [m[sid] for m in caps['matrices'][g]] for g in ZERO),
                            'raw original cap lifts differ from frozen matrices')
                    cap_cache[key] = {'literal_D_rim': list(rim), 'D_state': sid,
                                      'all_raw_cap_lifts_including_empty_rows': full}
                full = cap_cache[key]['all_raw_cap_lifts_including_empty_rows']
                require(not any(full[g][row] for g in ZERO for row in ZERO[g]),
                        'a short initial patch now has a forbidden cap')
                records.append({'joint_colours': lift, 'cap_key': key})
            cases.append({'kind': kind, 'target': target, 'actual_U': U, 'actual_V': V,
                          'mutable_order': list(mutable), 'all_joint_lifts': records,
                          'locally_compatible_but_same_E_excluded': kind == 'II' and target == 44466 and U == 'w',
                          'original_source_realized': False})
    require(len(cases) == 9, 'short identity-case coverage changed')
    return {'nine_identity_cases_including_the_excluded_alias_control': cases,
            'full_caps_by_literal_D_row': cap_cache}


def same_E_alias(parent):
    result = []
    for state, tip in ((560, 'v'), (572, 'w')):
        row = next(r for r in parent['L_complete_residual']
                   if r['E_state'] == state and r['split_containing_0'] == [0, 2])
        require(len(row['complete_surviving_columns']) == 2, 'two exact parent02 types changed')
        complete = []
        for column in row['complete_surviving_columns']:
            joined = any(tip in block and 'z4' in block for block in column['component_blocks'])
            require(joined == (state == 560), 'same-E actual02 separation changed')
            complete.append(column | {'tip_and_z4_same_complete_block': joined})
        result.append({'E_state': state, 'actual_zero_tip': tip, 'complete_columns': complete,
                       'II_original_path_tip_K_z4_excludes_alias': state == 572})
    require([c['column_id'] for c in result[1]['complete_columns']] == [220297, 220299],
            'named B02 columns changed')
    return result


def compute():
    manifest, caps, parent, module = inputs()
    rng = random.Random(17) if os.environ.get('PYTHONHASHSEED') == '17' else None
    return {'base': BASE, 'frozen_input_count': len(manifest['inputs']),
            'B6_complete_relations': boundary_relations(rng),
            'short_initial_full_fibres': initial_short_fibres(module, caps, rng),
            'same_original_E_02_alias_proof': same_E_alias(parent),
            'source_conditional_exclusions': ['II/44466/U=original_w'],
            'L_four_types_entirely_excluded': False, 'six_degree_entirely_excluded': False,
            'double_five_entirely_excluded': False, 'source_realized': False,
            'general_W7_excluded': False, 'new_Lean': False, 'LP_run': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json.gz')
    args = parser.parse_args()
    expected = compute()
    if args.build:
        with args.certificate.open('xb') as stream:
            stream.write(gzip.compress(packed(expected), mtime=0))
    actual = json.loads(gzip.decompress(args.certificate.read_bytes()))
    require(actual == expected, 'complete tuples, zeros or source scope altered')
    corruptions = []
    for field in ('L_four_types_entirely_excluded', 'six_degree_entirely_excluded',
                  'double_five_entirely_excluded', 'source_realized', 'general_W7_excluded'):
        bad = deepcopy(actual)
        bad[field] = True
        corruptions.append(bad)
    bad = deepcopy(actual)
    bad['B6_complete_relations']['all_31_complete_fibres'][0]['all_inner_lifts']['II'] = []
    corruptions.append(bad)
    bad = deepcopy(actual)
    bad['same_original_E_02_alias_proof'][1]['complete_columns'].pop()
    corruptions.append(bad)
    require(all(bad != expected for bad in corruptions), 'negative control was accepted')
    print(json.dumps({'result': 'PASS', 'B6_proper_rows': 31, 'short_identity_cases': 9,
                      'all_joint_initial_lifts': 54, 'negative_controls': len(corruptions),
                      'frozen_input_drift': 0, 'live_authority_drift': 0,
                      'source_conditional_exclusions': expected['source_conditional_exclusions'],
                      'entire_short_type_exclusions': [],
                      'certificate_sha256': sha256(args.certificate.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    main()
