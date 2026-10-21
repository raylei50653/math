#!/usr/bin/env python3
"""Three-state same-source domination certificate, independently checked.

The checker consumes the original full frozen family, not the discovery queue
or its large residual. All inferences use one shared Z and nonnegative X.
"""
import argparse
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = HERE.parents[2]
SOURCE = 'audits/2026-10-20-r6-941-j1-five-edge-417732f/counting'
PROFILES = 'audits/2026-10-21-w7-structural-30f2d19/review/profile_orbits.json'
IDS = [10, 11, 12, 13, 14, 15, 43, 44]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def exact_integer(value):
    return type(value) is int


def read(relative):
    raw = (ROOT / relative).read_bytes()
    return json.loads(gzip.decompress(raw) if relative.endswith('.gz') else raw)


def load_inputs():
    base = json.loads((AUDIT / 'BASE.json').read_text())
    frozen = {p['path']: p for p in base['inputs']}
    names = [SOURCE + '/caps.json.gz', SOURCE + '/orbits.json.gz', PROFILES]
    hashes = {}
    custody_names = names + [SOURCE.rsplit('/',1)[0] + '/SOURCE_CONTRACT.md',
                            SOURCE + '/PROOF.md']
    for name in custody_names:
        raw = (ROOT / name).read_bytes()
        require(len(raw) == frozen[name]['bytes'] and
                hashlib.sha256(raw).hexdigest() == frozen[name]['sha256'],
                'frozen input drift: ' + name)
        if name in names:
            hashes[name] = frozen[name]['sha256']
    return hashes, *(read(n) for n in names)


def canonical(row):
    decoded = [(row >> (2*(12-i))) & 3 for i in range(13)]
    rename = {}
    answer = []
    for colour in decoded:
        if colour not in rename:
            rename[colour] = len(rename)
        answer.append(rename[colour])
    return answer


def proposed(hashes):
    return {
        'scope': 'strict original only-R/W7 source with original edge u3v',
        'input_sha256': hashes,
        'original_profile_ids': IDS,
        'original_edge': ['u3', 'v'],
        'dominations': [
            {'from_state': 44459, 'from_halfrow': 12302027,
             'incident_column_ids': [306985],
             'to_state': 44111, 'to_halfrow': 12301211},
            {'from_state': 44111, 'from_halfrow': 10064313,
             'incident_column_ids': [147448,147449,167802,226130,231666],
             'to_state': 44127, 'to_halfrow': 10064365},
        ],
        'original_edge_zero_states': [44127, 44466],
        'zero_columns': [
            {'column_id': 66582, 'contains_zero_halfrow': 6712710, 'zero_state': 44459},
            {'column_id': 67755, 'contains_zero_halfrow': 6712710, 'zero_state': 44459},
        ],
        'claimed_zero_states': [44111,44127,44459,44466],
        'witness_positive_sum': [44459,44466],
    }


def verify(cert, inputs):
    hashes, caps, orbit, profiles = inputs
    require(cert['scope'] == 'strict original only-R/W7 source with original edge u3v',
            'the proof scope was widened beyond its frozen source contract')
    require(cert['input_sha256'] == hashes, 'certificate input custody differs')
    require(cert['original_edge'] == ['u3', 'v'], 'wrong original edge')
    require(cert['original_profile_ids'] == IDS, 'wrong fixed profile coverage')
    table = {p['original_profile_id']: p for p in profiles['profiles']}
    require(all(['u3','v'] in table[i]['original_chords'] for i in IDS),
            'a covered profile lacks the actual original edge')
    row_state = dict(orbit['rowids'])
    wanted = {step['from_halfrow'] for step in cert['dominations']}
    require(all(exact_integer(h) for h in wanted), 'noninteger half-row')
    incidence = {h: [] for h in wanted}
    for j, column in enumerate(orbit['columns']):
        for h in wanted.intersection(column):
            incidence[h].append(j)
    for step in cert['dominations']:
        a, b = step['from_state'], step['to_state']
        ha, hb = step['from_halfrow'], step['to_halfrow']
        require(all(exact_integer(x) for x in (a,b,ha,hb)), 'noninteger state or half-row')
        require(row_state.get(ha) == a and row_state.get(hb) == b,
                'half-row to original state map differs')
        require(canonical(ha) == caps['states'][a] and canonical(hb) == caps['states'][b],
                'independent literal canonicalization differs')
        ids = step['incident_column_ids']
        require(all(exact_integer(j) for j in ids) and ids == sorted(set(ids)),
                'incident columns must be unique sorted integers')
        require(ids == incidence[ha], 'incident column cover is incomplete')
        require(bool(ids) and all(hb in orbit['columns'][j] for j in ids),
                'column inclusion does not prove the claimed domination')
    position = {v:i for i,v in enumerate(caps['ordered_rim'])}
    zeros = set()
    for s in cert['original_edge_zero_states']:
        require(exact_integer(s), 'noninteger original-edge zero state')
        row = caps['states'][s]
        require(row[position['u3']] == row[position['v']],
                'claimed direct zero is proper on the original edge')
        zeros.add(s)
    for step in reversed(cert['dominations']):
        require(step['to_state'] in zeros, 'domination has no established zero upper bound')
        zeros.add(step['from_state'])
    require(sorted(zeros) == cert['claimed_zero_states'], 'zero-state conclusion differs')
    dead_columns = []
    for step in cert['zero_columns']:
        j, h, s = step['column_id'], step['contains_zero_halfrow'], step['zero_state']
        require(all(exact_integer(x) for x in (j,h,s)), 'noninteger column witness')
        require(s in zeros and row_state.get(h) == s and h in orbit['columns'][j],
                'column zero lacks its complete source-fibre witness')
        dead_columns.append(j)
    require(dead_columns == [66582,67755], 'the two requested columns were not established zero')
    require(cert['witness_positive_sum'] == [44459,44466] and
            all(s in zeros for s in cert['witness_positive_sum']),
            'positive actual-witness sum was not contradicted')
    return {'status': 'PASS: exact domination and u3v subbranch exclusion',
            'all_original_columns_scanned': len(orbit['columns']),
            'chain': '0<=Z44459<=Z44111<=Z44127=0',
            'Z44466': 0, 'zero_columns': dead_columns,
            'uniform_original_profile_coverage': IDS,
            'scope': cert['scope'], 'general_W7': 'OPEN', 'general_J1_J2': 'OPEN',
            'source_realized': False, 'Lean': 'not formalized'}


def controls(cert, inputs):
    mutations = [
        ('missing_full_column', lambda x: x['dominations'][1]['incident_column_ids'].pop()),
        ('wrong_halfrow_state', lambda x: x['dominations'][0].__setitem__('to_state', 44480)),
        ('proper_state_as_edge_zero', lambda x: x['original_edge_zero_states'].__setitem__(0,44459)),
        ('lost_common_row', lambda x: x['dominations'][1].__setitem__('to_halfrow',12301211)),
        ('bool_column_id', lambda x: x['dominations'][0]['incident_column_ids'].__setitem__(0,True)),
        ('omitted_profile', lambda x: x['original_profile_ids'].pop()),
        ('widened_source_scope', lambda x: x.__setitem__('scope','all plane disks')),
    ]
    rejected = []
    for name, mutate in mutations:
        bad = deepcopy(cert)
        mutate(bad)
        try:
            verify(bad, inputs)
        except (ValueError, KeyError, IndexError):
            rejected.append(name)
    require(len(rejected) == len(mutations), 'a corrupt proof was accepted')
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--certificate', type=Path)
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    require(not(args.build and args.certificate), 'build and certificate are mutually exclusive')
    inputs = load_inputs()
    path = args.certificate or HERE / 'compact-certificate.json'
    cert = proposed(inputs[0]) if args.build else json.loads(path.read_text())
    result = verify(cert, inputs)
    if args.controls:
        result['corrupt_proofs_rejected'] = controls(cert, inputs)
    if args.build:
        with path.open('x') as stream:
            json.dump(cert, stream, indent=2)
            stream.write('\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
