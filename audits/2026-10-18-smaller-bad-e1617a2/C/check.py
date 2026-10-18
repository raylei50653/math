#!/usr/bin/env python3
"""Exact fixed-interface algebra; abstract exterior relations, no graph search."""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FROZEN = ROOT.parent / 'frozen'
BASE = 'e1617a2756813327d7ad333cfdd0fd92fa9efc38'
INPUTS = {
    'artifacts/c5_cells/cells.json': '04650cea947a5086360e895c1a7350690f53da745314379a3328b97ee02d81b8',
    'audits/2026-10-18-smaller-source-9f1fe84/C/PROOF.md': '42e29d951ef56f1dba6f4c8bdc2ff6f8c32e04ea2836a74d869bc968a54f624f',
    'audits/2026-10-18-rainbow-exterior-e1617a2/A/PROOF.md': '719f9c07ff9a20e668a07b2599aefebe3ef52adbfe223401f561d1afecf47672',
}
for path, digest in INPUTS.items():
    assert hashlib.sha256((FROZEN / path).read_bytes()).hexdigest() == digest
DATA = json.loads((FROZEN / 'artifacts/c5_cells/cells.json').read_text())
ROWS = tuple(tuple(row) for row in DATA['pattern_order'])
K = set(map(int, DATA['cells']))
assert len(K) == 132
PINS = ('x', 'y', 'a', 'c', 'q', 'L', 'R', 'n')
OUTER = tuple('xyabc')
NEW_OUTER = ('x', 'y', 'a', 'q', 'c')
CYCLE = ('a', 'n', 'R', 'L', 'q', 'c', 'x', 'y')
NAMES = ('G', 'G_a', 'G_b', 'H', 'S', 'H1', 'H2')


def edge(u, v):
    return tuple(sorted((u, v)))


def cycle(vs):
    return {edge(vs[i], vs[(i + 1) % len(vs)]) for i in range(len(vs))}


EXTERIOR = cycle(CYCLE)
SURVIVING = EXTERIOR | {edge('b', v) for v in ('a', 'c', 'q')}
FAN_A = SURVIVING | {edge('a', v) for v in ('q', 'L', 'R')}
FAN_B = SURVIVING | {edge('b', v) for v in ('n', 'L', 'R')}
OLD = SURVIVING | {edge('p', v) for v in ('a', 'b', 'q', 'n', 'h')}
OLD |= {edge('h', v) for v in ('q', 'L', 'R', 'n')}


def proper(chi, edges):
    return all(chi[u] != chi[v] for u, v in edges)


def normalize(values):
    colours = {}
    return tuple(colours.setdefault(c, len(colours)) for c in values)


def row_bit(chi, boundary=OUTER):
    return 1 << ROWS.index(normalize(tuple(chi[v] for v in boundary)))


def old_lifts(chi):
    return [[p, h] for p, h in itertools.product(range(4), repeat=2)
            if proper(dict(chi, p=p, h=h), OLD)]


def state_support(values):
    chi = dict(zip(PINS, values))
    assert proper(chi, EXTERIOR)
    masks = [0] * 7
    if proper(chi, [e for e in FAN_A if 'b' not in e]):
        masks[3] |= row_bit(chi, NEW_OUTER)
    for b in range(4):
        chi['b'] = b
        if not proper(chi, SURVIVING):
            continue
        bit = row_bit(chi)
        if old_lifts(chi):
            masks[0] |= bit
        if proper(chi, FAN_A):
            masks[1] |= bit
        if proper(chi, FAN_B):
            masks[2] |= bit
        if chi['q'] == chi['n']:
            masks[4] |= bit
        if b == chi['n'] and chi['q'] == chi['R']:
            masks[5] |= bit
        if b == chi['n'] and b == chi['L']:
            masks[6] |= bit
    return tuple(masks)


def union(supports):
    result = [0] * 7
    for support in supports:
        for i, mask in enumerate(support):
            result[i] |= mask
    return tuple(result)


# Existing C8 interface only. Global S4 identifies x/y with 0/1; the remaining
# swap 2/3 is quotiented jointly on all eight contacts, never separately.
BLOCKS = {}
for values in itertools.product(range(4), repeat=6):
    state = (0, 1) + values
    chi = dict(zip(PINS, state))
    swapped = tuple(5 - c if c in (2, 3) else c for c in state)
    if state > swapped or not proper(chi, EXTERIOR):
        continue
    BLOCKS[state] = state_support(state)
assert len(BLOCKS) == 274
assert sum(len(set(s)) == 2 for s in BLOCKS) == 1

# Exact ear insertion. H has outer (x,y,a,q,c); b is inserted with precisely
# the complete neighbours a,q,c. This gives a support map for actual graphs.
ear = []
for row in ROWS:
    chi = dict(zip(NEW_OUTER, row))
    mask = 0
    for b in range(4):
        if b in {chi[v] for v in ('a', 'q', 'c')}:
            continue
        chi['b'] = b
        mask |= row_bit(chi)
    ear.append(mask)
assert ear == [4, 2, 1, 256, 576, 128, 528, 32, 8, 80]


def insert_ear(mask):
    result = 0
    for i, image in enumerate(ear):
        if mask >> i & 1:
            result |= image
    return result


assert all(insert_ear(mask) in K for mask in K)


def build_model(target):
    desired = (target, 854, 91, 91, 165, 91, 935)
    allowed = [(state, support) for state, support in sorted(BLOCKS.items())
               if all(not support[i] & ~desired[i] for i in range(7))]
    assert union(support for _, support in allowed) == desired
    chosen = []
    covered = (0,) * 7
    while covered != desired:
        state, support = min(allowed, key=lambda item: (
            -sum((item[1][i] & ~covered[i]).bit_count() for i in range(7)), item[0]))
        assert sum((support[i] & ~covered[i]).bit_count() for i in range(7))
        chosen.append((state, support))
        covered = union((covered, support))
    for item in tuple(chosen):
        if union(support for other, support in chosen if other != item[0]) == desired:
            chosen.remove(item)
    chosen.sort()
    states = sorted({tuple(permutation[c] for c in state)
                     for state, _ in chosen
                     for permutation in itertools.permutations(range(4))})
    assert all(proper(dict(zip(PINS, state)), EXTERIOR) for state in states)
    assert union(state_support(state) for state in states) == desired
    fibres = {name: [[] for _ in ROWS] for name in NAMES}
    local_extensions = []
    for state_id, state in enumerate(states):
        chi = dict(zip(PINS, state))
        if proper(chi, [e for e in FAN_A if 'b' not in e]):
            literal = tuple(chi[v] for v in NEW_OUTER)
            if literal in ROWS:
                fibres['H'][ROWS.index(literal)].append([state_id])
        for b in range(4):
            chi['b'] = b
            if not proper(chi, SURVIVING):
                continue
            extensions = old_lifts(chi)
            local_extensions.append({'state': state_id, 'b': b, 'all_p_h_lifts': extensions})
            literal = tuple(chi[v] for v in OUTER)
            if literal not in ROWS:
                continue
            row = ROWS.index(literal)
            fibres['G'][row].extend([state_id, b, p, h] for p, h in extensions)
            if proper(chi, FAN_A):
                fibres['G_a'][row].append([state_id, b])
            if proper(chi, FAN_B):
                fibres['G_b'][row].append([state_id, b])
            if chi['q'] == chi['n']:
                fibres['S'][row].append([state_id, b])
            if b == chi['n'] and chi['q'] == chi['R']:
                fibres['H1'][row].append([state_id, b])
            if b == chi['n'] and b == chi['L']:
                fibres['H2'][row].append([state_id, b])
    masks = tuple(sum(1 << i for i, fibre in enumerate(fibres[name]) if fibre) for name in NAMES)
    assert masks == desired
    assert target not in K and all(mask in K for mask in desired[1:])
    assert insert_ear(desired[3]) == desired[1]
    assert not fibres['H'][9]
    # Every original accepted colouring restricts to one old fan branch. If
    # that branch is A, the two real double-identification candidates cover it.
    for state_id, b, p, h in fibres['G'][9]:
        chi = dict(zip(PINS, states[state_id])) | {'b': b}
        assert h in (chi['a'], b)
        if h == chi['a']:
            assert chi['n'] == b
            assert [state_id, b] in fibres['H1'][9] or [state_id, b] in fibres['H2'][9]
        else:
            assert chi['n'] == chi['q']
            assert [state_id, b] in fibres['S'][9]
    return {'support_order': NAMES, 'supports': desired,
            'orbit_generators': [state for state, _ in chosen],
            'orbit_supports': [support for _, support in chosen],
            'literal_exterior_states': states,
            'local_extensions_including_empty': local_extensions,
            'full_abstract_fibres_including_empty': fibres,
            'actual_exterior_graph_realized': False}


MODELS = {str(target): build_model(target) for target in (932, 933, 941)}
# Recompute each local extension fibre; importing a pin-marginal or deleting a
# lift is detected even if every displayed support mask remains unchanged.
def validate_model(model):
    target = model['supports'][0]
    assert json.loads(json.dumps(model)) == json.loads(json.dumps(build_model(target)))


controls = []
for label in ('deleted-full-lift', 'mixed-exterior-state', 'false-graph-realization'):
    mutated = copy.deepcopy(MODELS['932'])
    if label == 'deleted-full-lift':
        nonempty = next(r for r in mutated['local_extensions_including_empty'] if r['all_p_h_lifts'])
        nonempty['all_p_h_lifts'].pop()
    elif label == 'mixed-exterior-state':
        nonempty = next(r for r in mutated['local_extensions_including_empty'] if r['all_p_h_lifts'])
        nonempty['state'] = (nonempty['state'] + 1) % len(mutated['literal_exterior_states'])
    else:
        mutated['actual_exterior_graph_realized'] = True
    try:
        validate_model(mutated)
    except AssertionError:
        controls.append({'mutation': label, 'rejected': True})
    else:
        raise AssertionError('negative control accepted')

RESULT = {
    'base': BASE, 'inputs': INPUTS,
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'scope': 'coherent exterior-relation controls; no graph realization or smaller-bad theorem',
    'pin_order': PINS, 'exterior_cycle': CYCLE, 'rows': ROWS,
    'canonical_C8_states': 274, 'three_or_four_colour_C8_states': 273,
    'exact_ear_insertion_map': ear,
    'catalogue_ear_images': [[mask, insert_ear(mask)] for mask in sorted(K)],
    'models': MODELS, 'negative_controls': controls,
    'all_six_candidate_masks_in_catalogue': True,
    'actual_smaller_bad_source_proved': False,
}
parser = argparse.ArgumentParser()
parser.add_argument('--check', action='store_true')
parser.add_argument('--certificate', type=Path)
args = parser.parse_args()
path = args.certificate or ROOT / 'certificate.json'
normal = json.loads(json.dumps(RESULT))
if args.check:
    assert json.loads(path.read_text()) == normal, 'certificate differs'
else:
    with path.open('x') as stream:
        stream.write(json.dumps(RESULT, indent=2) + '\n')
print(json.dumps({'ok': True, 'models': {target: {'supports': model['supports'],
                  'exterior_orbits': len(model['orbit_generators']),
                  'literal_states': len(model['literal_exterior_states'])}
                  for target, model in MODELS.items()},
                  'catalogue_ear_images': len(K), 'negative_controls': len(controls),
                  'actual_smaller_bad_source_proved': False}))
