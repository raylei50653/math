#!/usr/bin/env python3
"""Exact decomposition of the unfinished W7 potential; no LP is invoked.

Default mode is a read-only replay. --build exclusively creates result.json.
The source contains all surviving columns, not just a restricted master.
"""
import argparse
import collections
import gzip
import hashlib
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = HERE.parents[2]
SOURCE = 'audits/2026-10-20-r6-941-j1-five-edge-417732f'
REUSE = 'audits/2026-10-21-w7-reuse-d5b8a86'
RESIDUAL = ('audits/2026-10-20-w7-count-cone-d5b8a86/sparse/'
            'warm2-44459/exact-dual-residual.json.gz')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load(relative):
    raw = (ROOT / relative).read_bytes()
    return json.loads(gzip.decompress(raw) if relative.endswith('.gz') else raw)


def colors(encoded):
    return tuple((encoded >> (2 * (12 - i))) & 3 for i in range(13))


def word(encoded):
    return ''.join(str(c // 2) for c in colors(encoded))


def compute(seed):
    base = load(str((AUDIT / 'BASE.json').relative_to(ROOT)))
    immutable = [p for p in base['inputs'] if p['authority'] == 'immutable-input']
    for item in immutable:
        raw = (ROOT / item['path']).read_bytes()
        require(len(raw) == item['bytes'] and
                hashlib.sha256(raw).hexdigest() == item['sha256'],
                'frozen input drift: ' + item['path'])
    orbit = load(SOURCE + '/counting/orbits.json.gz')
    caps = load(SOURCE + '/counting/caps.json.gz')
    geometry = load(SOURCE + '/geometry/certificate.json')
    residual = load(RESIDUAL)
    templates = load(REUSE + '/templates/templates.json.gz')
    row_map = load(REUSE + '/templates/row_map.json.gz')['rows']
    column_map = load(REUSE + '/templates/column_map.json.gz')['original_column_order']
    weights = dict(residual['halfrow_integer_weights'])
    row_state = dict(orbit['rowids'])
    mapped_rows = {r[0]: r for r in row_map}
    state_weights = collections.Counter()
    for h, w in weights.items():
        require(type(h) is int and type(w) is int, 'noninteger weight')
        state_weights[row_state[h]] += 2 * w
    require({s: w for s, w in state_weights.items() if w} == {44459: 2},
            'target conservation law changed')

    blocks = {}
    for h, w in weights.items():
        q = word(h)
        block = blocks.setdefault(q, {'halfrows': [], 'state_coefficients': {},
                                     'column_price_histogram': {},
                                     'nonzero_columns': []})
        block['halfrows'].append([h, row_state[h], w])
        state = str(row_state[h])
        block['state_coefficients'][state] = block['state_coefficients'].get(state, 0) + 2*w
    order = list(range(len(orbit['columns'])))
    random.Random(seed).shuffle(order)
    prices = [None] * len(order)
    for j in order:
        column = orbit['columns'][j]
        q = word(column[0])
        price = sum(weights.get(h, 0) for h in column)
        prices[j] = price
        if q not in blocks:
            require(price == 0, 'unlisted price block')
            continue
        require(all(word(h) == q for h in column), 'palette word changes within column')
        block = blocks[q]
        key = str(price)
        hist = block['column_price_histogram']
        hist[key] = hist.get(key, 0) + 1
        if price:
            block['nonzero_columns'].append([j, price])
    require(prices == residual['all_column_integer_prices'], 'full integer prices changed')
    for block in blocks.values():
        block['halfrows'].sort()
        block['nonzero_columns'].sort()
        signs = {1 if p > 0 else -1 for _, p in block['nonzero_columns']}
        require(len(signs) <= 1, 'mixed signs defeat same-palette obstruction')

    expected = {
        '0010101101001': {'0': 288},
        '0101010101011': {'0': 841, '-1': 93, '-2': 8},
        '0101011011001': {'0': 630, '1': 42},
        '0110101011001': {'0': 630, '1': 42},
        '0111010011001': {'0': 98, '1': 14},
        '0111101111001': {'0': 15, '1': 5},
        '0111111010010': {'0': 7, '-1': 2},
    }
    require({q: b['column_price_histogram'] for q, b in blocks.items()} == expected,
            'exact block decomposition differs')
    stars = []
    for q, block in sorted(blocks.items()):
        if '1' not in block['column_price_histogram']:
            continue
        require(len(block['halfrows']) == 1 and block['halfrows'][0][2] == 1,
                'positive family is not a single marked phase')
        h, state, _ = block['halfrows'][0]
        _, _, qint, k, phase, live = mapped_rows[h]
        require(live == 1, 'positive phase is dead')
        universal = {j for j, col in enumerate(templates[str(k)]) if phase in col}
        actual = set()
        for j, price in block['nonzero_columns']:
            mapped_q, mapped_k, local = column_map[j]
            require((mapped_q, mapped_k) == (qint, k) and price == 1,
                    'positive column mapping differs')
            actual.add(local)
        require(actual == universal, 'a universal marked-phase partition was removed')
        stars.append({'palette_word': q, 'state': state, 'halfrow': h,
                      'half_run_count': k, 'phase': phase,
                      'universal_marked_phase_columns': sorted(universal),
                      'all_universal_marked_phase_columns_survive': True,
                      'count': len(actual)})

    rim = geometry['expanded_core']['rim']
    position = {v: i for i, v in enumerate(rim)}
    optional = geometry['expanded_core']['potential_original_chords']
    interesting = (44459, 44466, 44480, 44541, 784, 37416, 46468, 66394)
    zero_edges = {}
    for state in interesting:
        row = caps['states'][state]
        zero_edges[str(state)] = [e for e in optional if row[position[e[0]]] == row[position[e[1]]]]
    require(zero_edges['44459'] == [['s', 'u2'], ['s', 'u4'], ['u1', 'w'], ['u3', 'w']],
            'target chord-zero set differs')
    require(zero_edges['66394'] == [['u1', 'w'], ['u3', 'w']],
            'last auxiliary chord-zero set differs')
    require({tuple(e) for e in zero_edges['66394']} <=
            {tuple(e) for e in zero_edges['44459']}, 'chord obstruction inclusion fails')
    profiles = []
    for i, profile in enumerate(geometry['noncrossing_joint_contact_profiles']):
        original_edges = []
        for a, b in optional:
            if ((a in profile and b in profile[a]) or
                    (b in profile and a in profile[b])):
                original_edges.append([a, b])
        killed = [s for s in interesting if any(e in zero_edges[str(s)] for e in original_edges)]
        profiles.append({'original_profile_index': i, 'original_chords': original_edges,
                         'states_forced_zero_by_these_chords': killed})
    return {
        'status': 'exact structural decomposition; necessary cone and original source remain OPEN',
        'base': base['base'],
        'immutable_input_sha256': {i['path']: i['sha256'] for i in immutable},
        'live_states': len(orbit['live']), 'all_columns_priced': len(prices),
        'global_state_coefficients': [[44459, 2]],
        'blocks': dict(sorted(blocks.items())), 'positive_full_template_stars': stars,
        'same_palette_compensation_obstruction': 'Each nonzero-price palette word has a single price sign; palette-preserving component flips cannot pair a positive contribution with a negative one.',
        'source_valid_nonnegative_chain': 'Z44459=Z44480<=Z44541<=Z784+Z37416+Z46468+Z66394',
        'optional_chords_forcing_each_state_zero': zero_edges,
        'original_112_profile_chord_checks': profiles,
        'chord_only_auxiliary_obstruction': 'Every optional chord set compatible with target44459 is also proper on auxiliary state66394. This is only a direct chord-zero obstruction, not a feasibility claim or a failure of further orbit closure.',
        'target_compensation_status': 'Weighted compensation is equivalent to target44459 emptiness under the exact identity; a new source-level mechanism is still required.',
    }


def validate_summary(result):
    """Check separate arithmetic/completeness invariants of a stored summary."""
    global_coefficients = collections.Counter()
    column_ids = set()
    for q, block in result['blocks'].items():
        require(len(q) == 13 and set(q) <= {'0', '1'}, 'malformed palette word')
        coefficients = collections.Counter()
        for h, state, value in block['halfrows']:
            require(all(type(x) is int for x in (h, state, value)), 'noninteger half-row')
            require(word(h) == q, 'half-row is assigned to wrong palette block')
            coefficients[str(state)] += 2 * value
        require(dict(coefficients) == block['state_coefficients'],
                'block state coefficients do not equal its half-row weights')
        global_coefficients.update({int(s): c for s, c in coefficients.items()})
        histogram = collections.Counter()
        for j, price in block['nonzero_columns']:
            require(type(j) is int and type(price) is int and price != 0,
                    'malformed nonzero price')
            require(0 <= j < result['all_columns_priced'] and j not in column_ids,
                    'missing uniqueness or invalid column ID')
            column_ids.add(j)
            histogram[str(price)] += 1
        require(dict(histogram) == {p: n for p, n in block['column_price_histogram'].items()
                                    if p != '0'}, 'nonzero column list is incomplete')
    expected_global = sorted([s, c] for s, c in global_coefficients.items() if c)
    require(result['global_state_coefficients'] == expected_global == [[44459, 2]],
            'global state coefficients do not give the target conservation law')
    for star in result['positive_full_template_stars']:
        q = star['palette_word']
        require(q in result['blocks'], 'positive star has an unknown palette word')
        block = result['blocks'][q]
        require(block['halfrows'] == [[star['halfrow'], star['state'], 1]],
                'positive star does not have its claimed marked phase')
        require(star['count'] == len(set(star['universal_marked_phase_columns'])) ==
                len(block['nonzero_columns']), 'positive star cardinality is inconsistent')


def controls(result):
    validate_summary(result)
    rejected = []
    for name, mutate in (
        ('lost_positive_column', lambda x: x['blocks']['0101011011001']['nonzero_columns'].pop()),
        ('wrong_target_coefficient', lambda x: x['global_state_coefficients'][0].__setitem__(1, 0)),
        ('wrong_palette_map', lambda x: x['positive_full_template_stars'][0].__setitem__('palette_word', '0'*13)),
    ):
        damaged = json.loads(json.dumps(result))
        mutate(damaged)
        require(damaged != result, 'ineffective negative control')
        try:
            validate_summary(damaged)
        except ValueError:
            rejected.append(name)
    require(len(rejected) == 3, 'a damaged summary passed its semantic invariant check')
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    result = compute(args.seed)
    path = HERE / 'result.json'
    if args.build:
        with path.open('x') as stream:
            json.dump(result, stream, indent=2, sort_keys=True)
            stream.write('\n')
    else:
        require(json.loads(path.read_text()) == result, 'stored structural certificate differs')
    print(json.dumps({'read_only': not args.build, 'seed': args.seed,
                      'all_columns_priced': result['all_columns_priced'],
                      'positive_families': [s['count'] for s in result['positive_full_template_stars']],
                      'nonnegative_chain': result['source_valid_nonnegative_chain'],
                      'negative_controls_rejected': controls(result),
                      'cone': 'OPEN', 'source_excluded': False}, indent=2))


if __name__ == '__main__':
    main()
