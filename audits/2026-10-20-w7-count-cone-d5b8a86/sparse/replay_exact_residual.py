#!/usr/bin/env python3
"""Stdlib replay of the incomplete exact dual residual, not a cone decision.

This independently expands supplied integer eliminated-row weights into original
half-row weights, computes every state coefficient and every surviving-column
price, and verifies every reported positive-priced column. A successful replay
only means that this unfinished conservation residual was recorded accurately.
All checks remain active under python -O; JSON booleans are never accepted as
integer coefficients, row identifiers, state identifiers, or column identifiers.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer_pairs(value, name):
    require(type(value) is list, name + ' must be a list')
    require(all(type(item) is list and len(item) == 2 for item in value),
            name + ' must contain pairs')
    require(all(type(x) is int for pair in value for x in pair),
            name + ' must contain exact integers; booleans are forbidden')
    return value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('artifact', type=Path)
    ap.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[2] /
                    '2026-10-20-r6-941-j1-five-edge-417732f/counting/orbits.json.gz')
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    raw = args.source.read_bytes()
    source = json.loads(gzip.decompress(raw))
    data = json.load(gzip.open(args.artifact, 'rt'))
    require(type(data) is dict, 'artifact must be an object')
    require(hashlib.sha256(raw).hexdigest() == data['source_orbits_sha256'],
            'source orbit bytes do not match the recorded SHA256')
    live = source['live']
    state_rows = {state: [] for state in live}
    for row, state in source['rowids']:
        if state in state_rows:
            state_rows[state].append(row)
    require(all(len(rows) == 3 for rows in state_rows.values()),
            'every live state must have exactly three half-rows')
    for rows in state_rows.values():
        rows.sort()

    terms = integer_pairs(data['integer_dual_terms'], 'integer_dual_terms')
    require(all(value != 0 for _, value in terms), 'dual terms must be nonzero')
    require(len(dict(terms)) == len(terms), 'dual row identifiers must be unique')
    coefficients = dict(terms)
    nstates = len(live)
    require(all(0 <= row <= 2 * nstates for row in coefficients),
            'dual row identifier outside eliminated-system range')
    target = data['target']
    require(type(target) is int, 'target must be an exact integer; booleans are forbidden')
    require(target in state_rows, 'target is not a live state')
    target_reference = state_rows[target][2]
    require(type(data['target_reference_halfrow']) is int,
            'target reference half-row must be an exact integer')
    require(target_reference == data['target_reference_halfrow'],
            'target reference half-row does not match the canonical reference')
    beta = coefficients.get(2 * nstates, 0)
    require(type(data['target_dual_integer']) is int,
            'target dual coefficient must be an exact integer; booleans are forbidden')
    require(beta == data['target_dual_integer'] and beta > 0,
            'target dual coefficient must agree and be positive')

    weights = {}
    for index, state in enumerate(live):
        first, second, reference = state_rows[state]
        u = coefficients.get(2 * index, 0)
        v = coefficients.get(2 * index + 1, 0)
        weights[first], weights[second], weights[reference] = u, v, -u - v
    weights[target_reference] += beta
    supplied_halfweights = integer_pairs(data['halfrow_integer_weights'],
                                        'halfrow_integer_weights')
    halfweights = sorted((row, value) for row, value in weights.items() if value)
    require(halfweights == [tuple(pair) for pair in supplied_halfweights],
            'half-row weights do not equal the expanded integer dual')
    supplied_stateweights = integer_pairs(data['state_integer_coefficients'],
                                         'state_integer_coefficients')
    stateweights = [[state, 2 * sum(weights[row] for row in state_rows[state])]
                    for state in live]
    require(stateweights == supplied_stateweights,
            'state coefficients do not equal the recomputed coefficients')
    require([[state, value] for state, value in stateweights if value] ==
            [[target, 2 * beta]], 'a non-target state coefficient is nonzero')

    supplied_prices = data['all_column_integer_prices']
    require(type(supplied_prices) is list and
            all(type(value) is int for value in supplied_prices),
            'all column prices must be exact integers; booleans are forbidden')
    prices = [sum(weights[row] for row in column) for column in source['columns']]
    require(prices == supplied_prices, 'full column-price vector disagrees')
    supplied_positive = integer_pairs(data['positive_price_columns'],
                                      'positive_price_columns')
    positive = [[column, value] for column, value in enumerate(prices) if value > 0]
    require(positive == supplied_positive, 'positive-price column list disagrees')
    selected = data['selected_columns']
    require(type(selected) is list and all(type(column) is int for column in selected),
            'selected columns must be exact integers; booleans are forbidden')
    require(len(set(selected)) == len(selected), 'selected columns must be unique')
    require(all(0 <= column < len(prices) for column in selected),
            'selected column outside the full surviving family')
    supplied_selected_positive = integer_pairs(data['selected_positive_prices'],
                                               'selected_positive_prices')
    selected_positive = [[column, prices[column]] for column in selected
                         if prices[column] > 0]
    require(selected_positive == supplied_selected_positive,
            'selected-column positive prices disagree')
    require(not selected_positive, 'a selected column has positive price')
    require(bool(positive), 'this checker requires an incomplete residual, not a certificate')

    result = {
        'result': 'EXACT RESIDUAL REPLAYED; cone feasibility remains OPEN',
        'artifact_sha256': hashlib.sha256(args.artifact.read_bytes()).hexdigest(),
        'source_orbits_sha256': data['source_orbits_sha256'], 'target': target,
        'target_state_coefficient': 2 * beta, 'other_nonzero_state_coefficients': 0,
        'all_live_states_checked': len(live), 'all_surviving_columns_priced': len(prices),
        'positive_price_columns': len(positive),
        'maximum_positive_price': max(value for _, value in positive),
        'selected_columns': len(selected), 'selected_columns_with_positive_price': 0,
        'conservation': '%d Z[%d] = sum_j integer_price[j] X[j]' % (2 * beta, target),
        'interpretation': 'the listed positive-price columns remain a concrete obstruction '
                          'to using these weights as an exclusion certificate',
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
