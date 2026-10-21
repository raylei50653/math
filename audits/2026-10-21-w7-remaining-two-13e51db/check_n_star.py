#!/usr/bin/env python3
"""Read-only full original n-star audit; necessary support, never a source."""
import argparse
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREFIX = 'audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/'
BASE = '13e51db3ec3d8d7ec7eeef60167afdc19ad956c4'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def packed(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest(value):
    return hashlib.sha256(packed(value)).hexdigest()


def inputs():
    manifest = json.loads((HERE / 'BASE.json').read_text())
    require(manifest['base_commit'] == BASE, 'wrong BASE')
    for entry in manifest['inputs']:
        raw = (HERE / 'frozen' / entry['path']).read_bytes()
        require(len(raw) == entry['bytes'] and
                hashlib.sha256(raw).hexdigest() == entry['sha256'], 'frozen drift')
        if not entry['routing_only']:
            require(raw == (ROOT / entry['path']).read_bytes(), 'mathematical input drift')
    return [json.loads(gzip.decompress((HERE / 'frozen' / (PREFIX + name)).read_bytes()))
            for name in ['caps.json.gz', 'orbits.json.gz']]


def canonical(values):
    colours = {}
    return tuple(colours.setdefault(x, len(colours)) for x in values)


def n_isolated_when_required(column):
    # The only D-neighbours of n are a,u4, which are adjacent. If neither
    # is in n's palette, n itself is the entire actual component.
    reference = column[0]
    colours = [(reference >> (2 * (12 - i))) & 3 for i in range(13)]
    palette = colours[1] // 2
    if palette in (colours[0] // 2, colours[2] // 2):
        return True
    n_signature = tuple(((row ^ reference) >> 22) & 1 for row in column)
    for i in range(13):
        if i == 1 or colours[i] // 2 != palette:
            continue
        signature = tuple(((row ^ reference) >> (2 * (12 - i))) & 1 for row in column)
        if signature == n_signature:
            return False
    return True


def compute():
    caps, orbit = inputs()
    require(caps['ordered_rim'] ==
            ['a','n','u4','u3','u2','u1','L','q','c','s','v','w','t'], 'wrong rim')
    states = np.asarray(caps['states'], dtype=np.uint8)
    pairs = sorted(orbit['rowids'])
    keys = np.asarray([h for h, s in pairs], dtype=np.int64)
    row_state = np.asarray([s for h, s in pairs], dtype=np.int64)
    lengths = np.asarray([len(col) for col in orbit['columns']], dtype=np.int64)
    offsets = np.r_[0, np.cumsum(lengths)[:-1]]
    raw = np.asarray([h for col in orbit['columns'] for h in col], dtype=np.int64)
    rows = np.searchsorted(keys, raw)
    require(np.array_equal(keys[rows], raw), 'incomplete original row map')
    flat_states = row_state[rows]
    star_allowed = np.asarray([n_isolated_when_required(col) for col in orbit['columns']])
    initial = np.zeros(len(states), dtype=bool)
    initial[orbit['live']] = True
    initial &= states[:, 0] != states[:, 2]
    results = {}
    final_sets = []
    for label, allowed in [('chord_only', np.ones(len(lengths), dtype=bool)),
                           ('full_n_star', star_allowed)]:
        live = initial.copy()
        history = []
        for step in range(len(states) + 1):
            columns = allowed & np.logical_and.reduceat(live[flat_states], offsets)
            supported = np.zeros(len(keys), dtype=bool)
            np.logical_or.at(supported, rows, np.repeat(columns, lengths))
            next_live = live.copy()
            np.logical_and.at(next_live, row_state, supported)
            history.append([int(next_live.sum()), int(columns.sum())])
            if np.array_equal(next_live, live):
                break
            live = next_live
        else:
            raise ValueError('support iteration did not terminate')
        ids = np.flatnonzero(live).tolist()
        col_ids = np.flatnonzero(columns).tolist()
        results[label] = dict(rounds=history, states=len(ids), columns=len(col_ids),
                             state_ids_sha256=digest(ids), column_ids_sha256=digest(col_ids),
                             target_states=[s for s in [44459, 44466] if live[s]])
        final_sets.append((live, columns))
    require(all(np.array_equal(a, b) for a, b in zip(*final_sets)),
            'full star changed the fixed point; investigate before updating')
    live = final_sets[1][0]
    index = {tuple(row): i for i, row in enumerate(caps['states'])}
    recolour_pairs = set()
    for state_id in np.flatnonzero(live):
        row = caps['states'][int(state_id)]
        for colour in range(4):
            if colour in (row[0], row[2]):
                continue
            changed = row.copy()
            changed[1] = colour
            mate = index[canonical(changed)]
            require(bool(live[mate]), 'the exact n-recolouring reaches a zero fibre')
            recolour_pairs.add(tuple(sorted((int(state_id), mate))))
    target_mates = []
    for state_id in [44459, 44466]:
        row = caps['states'][state_id].copy()
        row[1] = 3
        target_mates.append([state_id, index[canonical(row)]])
    return dict(base=BASE, original_columns=len(lengths),
                columns_passing_n_singleton=int(star_allowed.sum()), cases=results,
                same_fixed_point=True, legal_recolour_pairs_including_identity=len(recolour_pairs),
                target_recolour_pairs=target_mates, recolour_support_closed=True,
                source_realized=False, profile1_excluded=False,
                profile0='OPEN', profile1='OPEN', new_Lean=False)


def verify(expected, actual):
    require(expected == actual, 'certificate mismatch')


def controls(actual):
    mutations = []
    bad = deepcopy(actual); bad['profile1_excluded'] = True; mutations.append(bad)
    bad = deepcopy(actual); bad['cases']['full_n_star']['target_states'] = []; mutations.append(bad)
    bad = deepcopy(actual); bad['target_recolour_pairs'][0][1] = 66242; mutations.append(bad)
    for bad in mutations:
        try:
            verify(bad, actual)
        except ValueError:
            continue
        raise ValueError('negative control accepted')
    return len(mutations)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'n-star.json')
    args = parser.parse_args()
    actual = compute()
    if args.build:
        with args.certificate.open('x') as output:
            json.dump(actual, output, indent=2); output.write('\n')
    else:
        verify(json.loads(args.certificate.read_text()), actual)
    print(json.dumps(dict(status='PASS', result=actual, negative_controls=controls(actual)), sort_keys=True))


if __name__ == '__main__':
    main()
