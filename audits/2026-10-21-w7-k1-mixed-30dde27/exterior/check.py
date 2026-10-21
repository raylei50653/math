#!/usr/bin/env python3
"""Six literal original-E mixed-palette orbits with complete strip/cap joins.

The NC family is regenerated specifically for E, without the filtered D family.
No partition is treated as an actual source realization.
"""
from collections import Counter
from copy import deepcopy
from functools import lru_cache
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
PREFIX = 'audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/'
COLLAR = 'audits/2026-10-21-w7-profile0-13e51db/check.py'
P = ('n', 'u4', 'u3', 'u2', 'u1', 'L')
PC = (1, 2, 1, 2, 1, 2)
TAIL = ('c', 's', 'v', 'w', 't')
RIM = ('a', *P, 'q', *TAIL)
ROWS = ('01012', '01021', '01023', '01201', '01202',
        '01203', '01212', '01213', '01231', '01232')
ZERO = {'G': {'01021', '01202', '01212'}, 'Q1': {'01232'},
        'J1': {'01202', '01212'}}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def packed(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def canonical(word):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in word)


def inputs():
    manifest = json.loads((HERE / 'BASE.json').read_text())
    require(manifest['base'] == BASE, 'exclusive BASE changed')
    for row in manifest['inputs']:
        raw = (HERE / 'frozen' / row['path']).read_bytes()
        require(len(raw) == row['bytes'] and sha256(raw).hexdigest() == row['sha256'],
                'frozen input drift: ' + row['path'])
    cap = json.loads(gzip.decompress((HERE / 'frozen' / PREFIX / 'caps.json.gz').read_bytes()))
    require(tuple(cap['ordered_rim']) == RIM, 'ordered original cap rim changed')
    require(len(cap['states']) == 66430, 'original complete cap matrix domain changed')
    spec = importlib.util.spec_from_file_location('original_collar', HERE / 'frozen' / COLLAR)
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    require(tuple(source.P) == P, 'original P identities changed')
    return source, cap


@lru_cache(None)
def cap_lifts(rim):
    """All original full cap assignments; no pre-filtered orbit information."""
    a, n, u4, u3, u2, u1, L, q, c, s, v, w, t = rim
    spokes = {n, u4, u3, u2, u1, L}
    right = [(x, y, r) for x, y, r in product(range(4), repeat=3)
             if r not in (s, v, w, t, x, y) and x not in (c, s, y)
             and y not in (a, t)]
    left = {
        'G': [(b, p, h, R) for b, p, h, R in product(range(4), repeat=4)
              if R not in spokes and b not in (a, c, q, p)
              and p not in (a, q, n, h) and h not in (q, L, R, n)],
        'Q1': [(b, R) for b, R in product(range(4), repeat=2)
               if R not in spokes and b == n and R == q and b not in (a, c, q)],
        'J1': [(b, R) for b, R in product(range(4), repeat=2)
               if R not in spokes and b == L and a != R and b not in (a, c, q)],
    }
    fibres = {g: {row: [] for row in ROWS} for g in ZERO}
    for g in ZERO:
        for ls in left[g]:
            for rs in right:
                row = ''.join(map(str, canonical((rs[0], rs[1], a, ls[0], c))))
                require(row in ROWS, 'cap frame not proper')
                fibres[g][row].append([*ls, *rs])
    for g in ZERO:
        for row in ROWS:
            fibres[g][row].sort()
    bad = any(fibres[g][row] for g in ZERO for row in ZERO[g])
    return fibres, bad


def nc_specific(colors, palette, word=(0,), stack=(0,), blocks=1):
    """Full active-block NC recursion, restricted by this literal membership."""
    i, n = len(word), len(colors)
    if i == n:
        if ((colors[-1] in palette) == (colors[0] in palette) and word[-1] != word[0]):
            return
        if sum(word[j] != word[(j + 1) % n] for j in range(n)) == 2 * (blocks - 1):
            yield word
        return
    side = colors[i] in palette
    if (colors[i - 1] in palette) == side:
        yield from nc_specific(colors, palette, word + (word[-1],), stack, blocks)
        return
    for j, b in enumerate(stack):
        if (colors[word.index(b)] in palette) == side:
            yield from nc_specific(colors, palette, word + (b,), stack[:j + 1], blocks)
    yield from nc_specific(colors, palette, word + (blocks,), stack + (blocks,), blocks + 1)


def set_partitions(size, word=(0,), blocks=1):
    if len(word) == size:
        yield word
        return
    for b in range(blocks + 1):
        yield from set_partitions(size, word + (b,), max(blocks, b + 1))


def is_nc(word):
    """Independent ABAB crossing test on complete block-position sets."""
    for a, b in combinations(set(word), 2):
        reduced = []
        for x in word:
            if x in (a, b) and (not reduced or reduced[-1] != x):
                reduced.append(x)
        if len(reduced) >= 4:
            return False
    return True


def independent_partitions(colors, palette):
    """Bell(6)^2 enumeration of same-palette boundary runs, not NC recursion."""
    runs = []
    for i, col in enumerate(colors):
        if runs and (colors[runs[-1][-1]] in palette) == (col in palette):
            runs[-1].append(i)
        else:
            runs.append([i])
    require((colors[0] in palette) != (colors[-1] in palette), 'named literal seam changed')
    sides = [[run for run in runs if (colors[run[0]] in palette) == side] for side in (False, True)]
    require([len(x) for x in sides] == [6, 6], 'literal boundary run coverage changed')
    family = list(set_partitions(6))
    require(len(family) == 203, 'Bell(6) independent coverage changed')
    out = set()
    for left, right in product(family, repeat=2):
        if max(left) + max(right) + 2 != 7:
            continue
        word = [None] * len(colors)
        for side, partition in enumerate((left, right)):
            for run, b in zip(sides[side], partition):
                for i in run:
                    word[i] = (side, b)
        canon = canonical(word)
        if is_nc(canon):
            require(sum(canon[j] != canon[(j + 1) % 13] for j in range(13)) == 12,
                    'independent transition count changed')
            out.add(canon)
    return sorted(out)


def original_case(source, center, target):
    counts = [int(t == center) for t in P]
    data, graph = source.collar(0, counts, with_graph=True)
    A = data['boundary'][1:]
    Y = next(v for v in A if v.startswith('H'))
    colors = {'a': 0, 'q': 3, Y: 3 - PC[P.index(center)]}
    cut = A.index(Y)
    for i in range(1, cut):
        colors[A[i]] = 3 - colors[A[i - 1]]
    for i in range(len(A) - 2, cut, -1):
        colors[A[i]] = 3 - colors[A[i + 1]]
    colors.update(dict(zip(TAIL, (1, 2, target, 1 - target, 2))))
    boundary = [*A, *TAIL]
    require(len(boundary) == len(set(boundary)) == 13, 'actual E interface not C13')
    literal = tuple(colors[v] for v in boundary)
    require(all(literal[i] != literal[(i + 1) % 13] for i in range(13)), 'initial E frame improper')
    require(all((colors | dict(zip(P, PC)))[v] != (colors | dict(zip(P, PC)))[w]
                for v in P for w in graph[v] if w in colors or w in P),
            'initial original strip not proper')
    return graph, A, Y, boundary, literal


def literal_cap_witness(rim, canonical_rim, full_caps):
    inverse = {c: original for c, original in zip(canonical_rim, rim)}
    for canonical_missing, literal_missing in zip(sorted(set(range(4)) - inverse.keys()),
                                                sorted(set(range(4)) - set(rim))):
        inverse[canonical_missing] = literal_missing
    require(set(inverse) == set(range(4)), 'whole-color inverse incomplete')
    for g in ZERO:
        for row in sorted(ZERO[g]):
            if full_caps[g][row]:
                literal_cap = [inverse[c] for c in full_caps[g][row][0]]
                b, x, y = literal_cap[0], literal_cap[-3], literal_cap[-2]
                frame = [x, y, rim[0], b, rim[8]]
                require(''.join(map(str, canonical(frame))) == row, 'fixed literal cap join changed')
                return {'graph': g, 'row': row, 'literal_cap_colors': literal_cap,
                        'literal_outer_frame': frame}
    return None


def image_kernel(word, boundary, graph, cap, index, used_states, rng):
    colors = dict(zip(boundary, word))
    domains = [sorted(set(range(4)) - {colors[v] for v in graph[t] if v in colors}) for t in P]
    if rng:
        for domain in domains:
            rng.shuffle(domain)
    paths = sorted(path for path in product(*domains)
                   if all(a != b for a, b in zip(path, path[1:])))
    lifts, witness = [], None
    for path in paths:
        full = colors | dict(zip(P, path))
        rim = tuple(full[v] for v in RIM)
        require(all(rim[j] != rim[(j + 1) % 13] for j in range(13)), 'joined D rim improper')
        normalized = canonical(rim)
        sid = index[normalized]
        used_states.add(sid)
        fibres, bad = cap_lifts(normalized)
        require(all([len(fibres[g][row]) for row in ROWS]
                    == [matrix[sid] for matrix in cap['matrices'][g]] for g in ZERO),
                'independent full cap assignments disagree with frozen matrices')
        lifts.append({'P_colors': list(path), 'canonical_D_cap_state': sid})
        if bad and witness is None:
            witness = {'strip_lift_index': len(lifts) - 1,
                       **literal_cap_witness(rim, normalized, fibres)}
    # Empty strip fibres do not imply an empty E fibre.
    return {'E_colors': list(word), 'complete_strip_fibre': lifts,
            'has_forbidden_full_join': witness is not None,
            'first_forbidden_full_join': witness}


def compute(seed):
    source, cap = inputs()
    rng = random.Random(seed) if seed is not None else None
    index = {tuple(t): i for i, t in enumerate(cap['states'])}
    used_states, cases = set(), []
    for center in ('u3', 'u1', 'L'):
        for target in (0, 1):
            graph, A, Y, boundary, literal = original_case(source, center, target)
            palette = (0, 1) if center == 'L' else (2, 3)
            partitions = sorted(nc_specific(literal, palette))
            independent = independent_partitions(literal, palette)
            require(partitions == independent and len(partitions) == 132,
                    'complete E-specific incident-partition coverage differs')
            require(all(max(p) + 1 == 7 for p in partitions), 'actual boundary-block count changed')
            orbit_words = {tuple(c ^ ((mask >> block) & 1) for c, block in zip(literal, p))
                           for p in partitions for mask in range(128)}
            require(len(orbit_words) == 1848, 'complete actual-component projection coverage changed')
            words = sorted(orbit_words)
            word_ids = {word: i for i, word in enumerate(words)}
            processing = list(range(len(words)))
            if rng:
                rng.shuffle(processing)
            kernels = {}
            for i in processing:
                word = words[i]
                require(all(word[j] != word[(j + 1) % 13] for j in range(13)), 'orbit image improper on E')
                kernels[i] = image_kernel(word, boundary, graph, cap, index, used_states, rng)
            images = [kernels[i] for i in range(len(words))]
            types, survivors = [], []
            histogram, min_steps = Counter(), Counter()
            for p in partitions:
                action = [word_ids[tuple(c ^ ((mask >> block) & 1) for c, block in zip(literal, p))]
                          for mask in range(128)]
                require(len(set(action)) == 128, 'distinct boundary components lost a complete action')
                bad_masks = [mask for mask, i in enumerate(action) if images[i]['has_forbidden_full_join']]
                best = min(bad_masks, key=lambda m: (m.bit_count(), m)) if bad_masks else None
                histogram[len(bad_masks)] += 1
                min_steps[best.bit_count() if best is not None else -1] += 1
                if not bad_masks:
                    survivors.append(list(p))
                types.append({'restricted_growth': list(p),
                              'complete_boundary_contacts': [[boundary[i] for i in range(13) if p[i] == block]
                                                             for block in range(7)],
                              'all_complete_component_action_image_ids': action,
                              'forbidden_action_masks': bad_masks,
                              'shortest_forbidden_action_mask': best,
                              'rejected_by_same_actual_E_orbit': bool(bad_masks)})
            require(len(survivors) == (38 if center == 'L' else 0), 'conditional exclusion changed')
            require(sum(image['has_forbidden_full_join'] for image in images)
                    == {'u3': 240, 'u1': 176, 'L': 128}[center], 'forbidden E image coverage changed')
            require(all(image['first_forbidden_full_join']['graph'] == 'G' and
                        image['first_forbidden_full_join']['row'] == '01021'
                        for image in images if image['has_forbidden_full_join']),
                    'the claimed original-G-01021-only exclusion changed')
            expected_steps = {'u3': {1: 121, 2: 11}, 'u1': {1: 122, 2: 10},
                              'L': {-1: 38, 1: 75, 2: 11, 3: 8}}[center]
            require(dict(min_steps) == expected_steps, 'shortest complete-action profile changed')
            cases.append({'profile': 0, 'K': 1, 'barrier_center': center, 'barrier': Y,
                          'original_target': 44459 if target == 0 else 44466,
                          'ordered_E_boundary': boundary, 'original_literal_E_colors': list(literal),
                          'mixed_palette': list(palette), 'other_palette': sorted(set(range(4)) - set(palette)),
                          'independent_partition_pairs_checked': 203 ** 2,
                          'complete_incident_E_partitions': types, 'complete_E_image_kernels': images,
                          'surviving_partitions': survivors,
                          'forbidden_action_histogram': {str(k): v for k, v in sorted(histogram.items())},
                          'minimum_component_flips_histogram': {str(k): v for k, v in sorted(min_steps.items())},
                          'same_actual_source_target_fibre_excluded': not survivors})
    cap_kernel = [{'state': sid, 'canonical_D_rim': cap['states'][sid],
                   'complete_cap_fibres': cap_lifts(tuple(cap['states'][sid]))[0]}
                  for sid in sorted(used_states)]
    return {'base': BASE,
            'scope': 'six literal original E boundary colorings; full incident NC families and complete component actions',
            'cases': cases, 'complete_original_cap_kernel': cap_kernel,
            'new_K1_profile0_centers_excluded': ['u3', 'u1'],
            'remaining_K1_profile0_centers': ['L'],
            'raw_L_surviving_partition_count_per_target': 38,
            'source_realized_by_surviving_partitions': False,
            'profile0_excluded': False, 'profile1_excluded': False,
            'palette_families_independently_joined': False,
            'destination_fibre_completed_after_action': False,
            'old_D_filtered_family_used_for_E': False,
            'empty_strip_fibre_used_as_E_zero': False,
            'new_Lean': False, 'LP_run': False}


def verify(proposal, actual):
    require(proposal == actual, 'certificate corrupted, incomplete, or closure scope enlarged')


def controls(result):
    # Deleting one actual contact partition breaks the quantified coverage.
    damaged = deepcopy(result)
    damaged['cases'][0]['complete_incident_E_partitions'].pop()
    rejected = 0
    try:
        verify(damaged, result)
    except ValueError:
        rejected += 1
    # A surviving necessary E type is not a source realization or full exclusion.
    for field in ('profile0_excluded', 'source_realized_by_surviving_partitions',
                  'old_D_filtered_family_used_for_E', 'empty_strip_fibre_used_as_E_zero'):
        damaged = deepcopy(result)
        damaged[field] = True
        try:
            verify(damaged, result)
        except ValueError:
            rejected += 1
    require(rejected == 5, 'coverage/source/empty-fibre negative controls failed')
    return rejected


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build', action='store_true')
    ap.add_argument('--seed', type=int)
    ap.add_argument('--certificate', type=Path, default=HERE / 'certificate.json.gz')
    args = ap.parse_args()
    result = compute(args.seed)
    negative = controls(result)
    raw = packed(result)
    if args.build:
        with args.certificate.open('xb') as out:
            with gzip.GzipFile(fileobj=out, mode='wb', mtime=0) as stream:
                stream.write(raw)
    verify(json.loads(gzip.decompress(args.certificate.read_bytes())), result)
    print(json.dumps({'result': 'PASS', 'literal_cases': 6, 'incident_types_per_case': 132,
                      'complete_component_actions_per_type': 128,
                      'distinct_E_images_per_case': 1848,
                      'used_full_cap_states': len(result['complete_original_cap_kernel']),
                      'K1_profile0_new_exclusions': ['u3', 'u1'],
                      'raw_L_survivors_per_target': 38, 'negative_controls': negative,
                      'whole_profiles_still_OPEN': [0, 1]}, sort_keys=True))


if __name__ == '__main__':
    main()
