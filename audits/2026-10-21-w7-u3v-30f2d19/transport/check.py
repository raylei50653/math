#!/usr/bin/env python3
"""Two actual-component involutions excluding the u3v source, without an LP.

Authority: frozen complete family, not the root support-closure transcript.
All incident columns at the two source half-rows are scanned, not sampled.
"""
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import json

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parents[1]
SOURCE = 'audits/2026-10-20-r6-941-j1-five-edge-417732f'
PREVIOUS = 'audits/2026-10-21-w7-structural-30f2d19/review/profile_orbits.json'
PROFILE_IDS = [10, 11, 12, 13, 14, 15, 43, 44]
STATE_IDS = [44459, 44111, 44127]
TUPLES = [
    [0, 1, 2, 1, 2, 1, 2, 3, 1, 2, 0, 1, 2],
    [0, 1, 2, 1, 2, 1, 2, 0, 2, 1, 3, 1, 2],
    [0, 1, 2, 1, 2, 1, 2, 0, 2, 3, 1, 3, 2],
]
INCIDENT = [[306985], [147448, 147449, 167802, 226130, 231666]]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def packed(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def encode(t):
    return sum(colour << (2 * (12 - i)) for i, colour in enumerate(t))


def decode(row):
    return [(row >> (2 * (12 - i))) & 3 for i in range(13)]


def halfrow(t, mate):
    other = [c for c in (1, 2, 3) if c != mate]
    perm = {0: 0, mate: 1, other[0]: 2, other[1]: 3}
    u = [perm[c] for c in t]
    a = u[0]
    b = next(c for c in u if c // 2 != a // 2)
    normal = {a: 0, a ^ 1: 1, b: 2, b ^ 1: 3}
    return encode([normal[c] for c in u])


def components(column):
    rows = [decode(row) for row in column]
    first = rows[0]
    groups = defaultdict(list)
    for i in range(13):
        require(all(row[i] // 2 == first[i] // 2 for row in rows),
                'one orbit changed its literal palette membership')
        profile = tuple((row[i] ^ first[i]) & 1 for row in rows)
        groups[(first[i] // 2, profile)].append(i)
    blocks = sorted(groups.values(), key=lambda block: block[0])
    anchors = [next(b for b, block in enumerate(blocks)
                    if first[block[0]] // 2 == palette) for palette in (0, 1)]
    generated = [column[0]]
    for b, block in enumerate(blocks):
        if b not in anchors:
            mask = sum(1 << (2 * (12 - i)) for i in block)
            generated += [row ^ mask for row in generated]
    require(sorted(generated) == column, 'recovered complete component flips do not regenerate the column')
    return blocks


def swap(t, block, pair, names):
    out = list(t)
    for name in block:
        i = names.index(name)
        require(out[i] in pair, 'a component has a color outside its fixed palette')
        out[i] = pair[0] ^ pair[1] ^ out[i]
    return out


def verify_incident(families):
    require(families == INCIDENT, 'the complete incident-column families changed')


def verify_final_component(block):
    require(block == ['s','v','w'], 'the final operation omitted part of its actual component')


def compute():
    manifest = json.loads((AUDIT / 'BASE.json').read_text())
    require(manifest['base'] == '30f2d19275657393b7354ed75eca31439d8ee12b', 'BASE changed')
    frozen = {record['path']: record for record in manifest['inputs']}
    needed = [SOURCE + '/SOURCE_CONTRACT.md', SOURCE + '/counting/PROOF.md',
              SOURCE + '/counting/caps.json.gz', SOURCE + '/counting/orbits.json.gz', PREVIOUS]
    inputs, objects = {}, {}
    for name in needed:
        data = (ROOT / name).read_bytes()
        require(len(data) == frozen[name]['bytes'] and sha256(data).hexdigest() == frozen[name]['sha256'],
                'frozen source drift: ' + name)
        inputs[name] = {'bytes': len(data), 'sha256': sha256(data).hexdigest()}
        if name.endswith('.gz'):
            objects[name] = json.loads(gzip.decompress(data))
        elif name.endswith('.json'):
            objects[name] = json.loads(data)
    caps = objects[SOURCE + '/counting/caps.json.gz']
    orbit = objects[SOURCE + '/counting/orbits.json.gz']
    parent = objects[PREVIOUS]
    names = caps['ordered_rim']
    require(names == ['a','n','u4','u3','u2','u1','L','q','c','s','v','w','t'], 'original rim changed')
    require([caps['states'][s] for s in STATE_IDS] == TUPLES, 'the three literal states changed')
    row_to_state = dict(orbit['rowids'])
    a, middle, leaf = TUPLES
    h_a, h_middle = halfrow(a, 3), halfrow(middle, 2)
    h_middle_in_a, h_leaf = halfrow(middle, 3), halfrow(leaf, 2)
    require([h_a, h_middle, h_middle_in_a, h_leaf] ==
            [12302027, 10064313, 12301211, 10064365], 'normalized half-rows changed')
    require([row_to_state[h] for h in [h_a, h_middle, h_middle_in_a, h_leaf]] ==
            [44459, 44111, 44111, 44127], 'complete shared-state map changed')
    incident = [[j for j, column in enumerate(orbit['columns']) if h in column]
                for h in (h_a, h_middle)]
    verify_incident(incident)
    columns = []
    for j in INCIDENT[0] + INCIDENT[1]:
        column = orbit['columns'][j]
        blocks = [[names[i] for i in block] for block in components(column)]
        columns.append({'column_id': j, 'half_rows': column,
                        'canonical_states': [row_to_state[h] for h in column],
                        'boundary_components': blocks})
        if j == 306985:
            require(blocks == [['a'], ['n','u4','u3','u2','u1','L','w','t'], ['q','v'], ['c','s']],
                    'the first source component partition changed')
            require(h_middle_in_a in column, 'first source orbit lost the middle fibre')
        else:
            verify_final_component(next(block for block in blocks if 'v' in block))
            require(h_leaf in column, 'a middle orbit does not contain the common direct-zero leaf')
    first = swap(a, ['q','v'], (0,3), names)
    first = swap(first, ['c','s'], (1,2), names)
    first_reverse_order = swap(a, ['c','s'], (1,2), names)
    first_reverse_order = swap(first_reverse_order, ['q','v'], (0,3), names)
    require(first == first_reverse_order == middle, 'the two disjoint-palette component flips differ')
    require(swap(swap(first, ['c','s'], (1,2), names), ['q','v'], (0,3), names) == a,
            'the first boundary operation is not an involution')
    second = swap(middle, ['s','v','w'], (1,3), names)
    require(second == leaf and swap(leaf, ['s','v','w'], (1,3), names) == middle,
            'the second boundary operation is not an involution')
    require(leaf[names.index('u3')] == leaf[names.index('v')] == 1,
            'the direct original-edge zero disappeared')
    other_target = caps['states'][44466]
    require(other_target[names.index('u3')] == other_target[names.index('v')] == 1,
            'the other target is not directly zero on the original edge')
    # Explicitly recover all eight fixed original profiles; do not take a union.
    profiles = []
    for record in parent['profiles']:
        if record['original_profile_id'] in PROFILE_IDS:
            require(['u3','v'] in record['original_chords'], 'a source profile lost its common actual edge')
            profiles.append({'original_profile_id': record['original_profile_id'],
                             'all_original_chords': record['original_chords']})
    require([r['original_profile_id'] for r in profiles] == PROFILE_IDS, 'the eight fixed sources changed')
    require(all(halfrow(a,1) in orbit['columns'][j] for j in (66582,67755)),
            'one of the two target columns no longer contains the full A fibre')
    # Meaningful corruptions: omit one admissible partition, or swap only v
    # in the final step. Both must fail the exact complete-source statement.
    omitted = [list(family) for family in incident]
    omitted[1].pop()
    try:
        verify_incident(omitted)
    except ValueError:
        omitted_partition_rejected = True
    else:
        omitted_partition_rejected = False
    try:
        verify_final_component(['v'])
    except ValueError:
        wrong_swap_rejected = True
    else:
        wrong_swap_rejected = False
    require(swap(middle, ['v'], (1,3), names) != leaf,
            'the false boundary-only shortcut accidentally matched the true operation')
    require(omitted_partition_rejected and wrong_swap_rejected, 'negative control failed')
    return {
        'status': 'EXACT TWO-OPERATION ORIGINAL-SOURCE EXCLUSION: u3v implies Z44459=0',
        'inputs': inputs, 'ordered_rim': names,
        'state_ids': STATE_IDS, 'literal_tuples': TUPLES,
        'all_original_surviving_columns_checked': len(orbit['columns']),
        'source_half_rows': [h_a,h_middle], 'all_incident_columns': incident,
        'intermediate_half_row_in_first_orbit': h_middle_in_a,
        'common_direct_zero_leaf_half_row': h_leaf,
        'complete_columns': columns,
        'full_fibre_injection_chain': 'Z44459 <= Z44111 <= Z44127 = 0',
        'operations': [
            {'from':44459,'to':44111,'whole_actual_components':[
                {'palette':[0,3],'anchor':'q','boundary_contacts':['q','v']},
                {'palette':[1,2],'anchor':'c','boundary_contacts':['c','s']}]},
            {'from':44111,'to':44127,'whole_actual_components':[
                {'palette':[1,3],'anchor':'v','boundary_contacts':['s','v','w']}]}],
        'profiles': profiles,
        'zero_columns':[66582,67755], 'other_target_zero_by_original_edge':44466,
        'negative_controls': {'omitted_middle_partition_rejected':omitted_partition_rejected,
                              'swapping_only_v_rejected':wrong_swap_rejected},
        'strict_u3v_branch_excluded':True,
        'general_strict_W7_excluded':False,
        'source_realized':False,
        'no_LP':True,
        'no_new_original_graph_enumeration':True,
        'support_closure_transcript_consumed':False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    result = compute()
    path = HERE / 'certificate.json'
    if args.build:
        with path.open('x') as stream:
            json.dump(result,stream,indent=2,sort_keys=True)
            stream.write('\n')
    else:
        require(result == json.loads(path.read_text()), 'transport certificate changed')
    print(json.dumps({key:result[key] for key in ['status','state_ids','all_incident_columns',
        'full_fibre_injection_chain','zero_columns','negative_controls',
        'support_closure_transcript_consumed']},sort_keys=True))


if __name__ == '__main__':
    main()
