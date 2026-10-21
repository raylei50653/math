#!/usr/bin/env python3
"""Exact zero-fibre propagation for the eight fixed u3v profiles; no LP.

The input is the already complete frozen W7 family, not new graph enumeration.
Default execution checks the existing complete residual read-only.
"""
from array import array
from collections import deque
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = HERE.parents[2]
OLD = 'audits/2026-10-21-w7-structural-30f2d19'
SOURCE = 'audits/2026-10-20-r6-941-j1-five-edge-417732f/counting'
EXPECTED_PROFILES = [10, 11, 12, 13, 14, 15, 43, 44]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(relative):
    raw = (ROOT / relative).read_bytes()
    return json.loads(gzip.decompress(raw) if relative.endswith('.gz') else raw)


def prepare():
    manifest = json.loads((AUDIT / 'BASE.json').read_text())
    consumed = [SOURCE + '/orbits.json.gz', SOURCE + '/caps.json.gz',
                OLD + '/review/profile_orbits.json']
    frozen = {r['path']: r for r in manifest['inputs']}
    hashes = {}
    for name in consumed:
        raw = (ROOT / name).read_bytes()
        require(len(raw) == frozen[name]['bytes'] and
                hashlib.sha256(raw).hexdigest() == frozen[name]['sha256'],
                'frozen input drift: ' + name)
        hashes[name] = frozen[name]['sha256']
    orbit, caps, parent = [read(p) for p in consumed]
    profiles = [p for p in parent['profiles'] if
                p['retained_columns']['44459_only'] == [66582, 67755]]
    require([p['original_profile_id'] for p in profiles] == EXPECTED_PROFILES,
            'eight fixed profiles changed')
    row_codes = array('I', (h for h, s in orbit['rowids']))
    row_states = array('I', (s for h, s in orbit['rowids']))
    lookup = {h: i for i, h in enumerate(row_codes)}
    state_rows = [[] for _ in caps['states']]
    for i, s in enumerate(row_states):
        state_rows[s].append(i)
    columns = []
    degree = array('I', [0]) * len(row_codes)
    for original in orbit['columns']:
        rows = array('I', (lookup[h] for h in original))
        columns.append(rows)
        for h in rows:
            degree[h] += 1
    live = orbit['live']
    require(all(len(state_rows[s]) == 3 and all(degree[h] for h in state_rows[s])
                for s in live), 'original closed family is incomplete')
    offsets = array('I', [0])
    for d in degree:
        offsets.append(offsets[-1] + d)
    reverse = array('I', [0]) * offsets[-1]
    cursor = array('I', offsets[:-1])
    for j, rows in enumerate(columns):
        for h in rows:
            reverse[cursor[h]] = j
            cursor[h] += 1
    return (hashes, caps, profiles, row_codes, row_states, state_rows,
            columns, degree, live, offsets, reverse)


def close_profile(profile, prepared):
    (hashes, caps, _, row_codes, row_states, state_rows,
     columns, original_degree, original_live, offsets, reverse) = prepared
    rim = caps['ordered_rim']
    index = {name: i for i, name in enumerate(rim)}
    chords = profile['original_chords']
    alive = bytearray(len(caps['states']))
    for s in original_live:
        alive[s] = 1
    active = bytearray([1]) * len(columns)
    degrees = array('I', original_degree)
    queue = deque()
    zero_steps = []
    killed_by = array('i', [-1]) * len(columns)
    for s in original_live:
        row = caps['states'][s]
        bad = next((edge for edge in chords if row[index[edge[0]]] == row[index[edge[1]]]), None)
        if bad is not None:
            alive[s] = 0
            queue.append(s)
            zero_steps.append([s, 'original-chord', bad])
    initial_chord_zeros = len(zero_steps)
    while queue:
        state = queue.popleft()
        for row in state_rows[state]:
            for at in range(offsets[row], offsets[row+1]):
                j = reverse[at]
                if not active[j]:
                    continue
                active[j] = 0
                killed_by[j] = state
                for h in columns[j]:
                    require(degrees[h] > 0, 'negative surviving degree')
                    degrees[h] -= 1
                    s = row_states[h]
                    if degrees[h] == 0 and alive[s]:
                        alive[s] = 0
                        queue.append(s)
                        zero_steps.append([s, 'empty-halfrow', row_codes[h]])
    live_states = [s for s in original_live if alive[s]]
    live_columns = [j for j, bit in enumerate(active) if bit]
    require(all(all(alive[row_states[h]] for h in columns[j]) for j in live_columns),
            'a surviving column meets a zero fibre')
    require(all(all(degrees[h] > 0 for h in state_rows[s]) for s in live_states),
            'a surviving fibre has an empty half-row')
    return {'original_profile_id': profile['original_profile_id'],
            'all_original_chords': chords, 'initial_chord_zero_count': initial_chord_zeros,
            'new_zero_steps': zero_steps,
            'live_state_ids': live_states, 'live_column_ids': live_columns,
            'killed_column_zero_state_witness': list(killed_by),
            'counts': {'live_states': len(live_states), 'live_columns': len(live_columns),
                       'propagated_state_zeros': len(zero_steps)-initial_chord_zeros},
            'target_A_live': bool(alive[44459]), 'target_B_live': bool(alive[44466]),
            'two_column_live': [bool(active[j]) for j in (66582, 67755)]}


def compute():
    prepared = prepare()
    records = [close_profile(profile, prepared) for profile in prepared[2]]
    return {'status': 'exact necessary support propagation; common count feasibility and source existence not inferred',
            'input_sha256': prepared[0], 'profile_ids': EXPECTED_PROFILES,
            'all_original_columns': len(prepared[6]), 'all_original_live_states': len(prepared[8]),
            'profiles': records,
            'source_exclusion_profiles': [r['original_profile_id'] for r in records if not r['target_A_live']],
            'no_LP': True, 'no_new_original_graph_enumeration': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    start = time.monotonic()
    result = compute()
    encoded = json.dumps(result, sort_keys=True, separators=(',', ':')).encode()
    path = HERE / 'result.json.gz'
    if args.build:
        with path.open('xb') as stream:
            stream.write(gzip.compress(encoded, mtime=0))
    else:
        require(json.loads(gzip.decompress(path.read_bytes())) == result,
                'complete support residual differs')
    print(json.dumps({'seconds': round(time.monotonic()-start, 3),
                      'excluded_profiles': result['source_exclusion_profiles'],
                      'profiles': [{k: r[k] for k in ('original_profile_id', 'counts',
                         'target_A_live', 'target_B_live', 'two_column_live')} for r in result['profiles']]}, indent=2))


if __name__ == '__main__':
    main()
