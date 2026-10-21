#!/usr/bin/env python3
"""Bounded exact target-stratum audit. Default is read-only; no LP or enumeration.

Read only the frozen complete orbit family and the two target cap states.
The fifteen relevant supports are classified by boundary-component profiles.
"""
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / 'audits/2026-10-20-r6-941-j1-five-edge-417732f/counting'
INPUT_SHA = {
    'caps.json.gz': '01547476f7afdc88ab224d640eaef363cfe765dd29e8983ca9df7aa63fdd68a3',
    'orbits.json.gz': '542ee11de93a846bfbc321b098214b153c5b600318ba2e0bc5621a73ad2a55ad',
}
TARGETS = [44459, 44466]
LITERAL = [
    [0, 1, 2, 1, 2, 1, 2, 3, 1, 2, 0, 1, 2],
    [0, 1, 2, 1, 2, 1, 2, 3, 1, 2, 1, 0, 2],
]
EXPECTED = {
    'shared': [43335, 43336, 48620, 66584, 67756],
    '44459_only': [43330, 43331, 48617, 66582, 67755],
    '44466_only': [43380, 43381, 48647, 66602, 67765],
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def packed(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def encode(t):
    return sum(colour << (2 * (12 - i)) for i, colour in enumerate(t))


def decode(row):
    return [(row >> (2 * (12 - i))) & 3 for i in range(13)]


def components(column):
    """Independent component flips distinguish every pair on the same side.

    XOR profiles remove fixed bipartition parity within a component. Absolute
    low-bit profiles would incorrectly split opposite-colored adjacent vertices.
    One fixed anchor per palette does not identify two same-palette components:
    one of any two distinct components can still be independently flipped.
    """
    rows = [decode(row) for row in column]
    reference = rows[0]
    keys = defaultdict(list)
    for i in range(13):
        require(all(row[i] // 2 == reference[i] // 2 for row in rows),
                'a column changed its literal palette membership')
        profile = tuple((row[i] ^ reference[i]) & 1 for row in rows)
        keys[(reference[i] // 2, profile)].append(i)
    blocks = sorted(keys.values(), key=lambda block: block[0])
    anchors = [next(b for b, block in enumerate(blocks)
                    if reference[block[0]] // 2 == palette) for palette in (0, 1)]
    masks = [sum(1 << (2 * (12 - i)) for i in block)
             for b, block in enumerate(blocks) if b not in anchors]
    generated = [column[0]]
    for mask in masks:
        generated += [row ^ mask for row in generated]
    require(sorted(generated) == column,
            'the recovered complete component-flip coset disagrees')
    return blocks


def audit():
    inputs = {}
    source = {}
    for name, expected in INPUT_SHA.items():
        raw = (SOURCE / name).read_bytes()
        require(sha256(raw).hexdigest() == expected, 'frozen input hash drift: ' + name)
        inputs[name] = {'sha256': expected, 'bytes': len(raw)}
        source[name] = json.loads(gzip.decompress(raw))
    caps, orbit = source['caps.json.gz'], source['orbits.json.gz']
    require([caps['states'][target] for target in TARGETS] == LITERAL,
            'the named target tuples changed')
    names = caps['ordered_rim']
    require(names == ['a', 'n', 'u4', 'u3', 'u2', 'u1', 'L', 'q', 'c', 's', 'v', 'w', 't'],
            'the original ordered rim changed')
    rows = [encode(t) for t in LITERAL]
    row_to_state = dict(orbit['rowids'])
    require([row_to_state[row] for row in rows] == TARGETS, 'target half-row map changed')
    families = {name: [] for name in EXPECTED}
    records = []
    for j, column in enumerate(orbit['columns']):
        hits = [row in column for row in rows]
        if not any(hits):
            continue
        family = 'shared' if all(hits) else '44459_only' if hits[0] else '44466_only'
        families[family].append(j)
        blocks = components(column)
        require(len(blocks) == 6 and len(column) == 16,
                'target orbit is not the expected six-component boundary type')
        named = [[names[i] for i in block] for block in blocks]
        anchor = next(block for block in named if 'a' in block)
        vw = next(block for block in named if 'v' in block)
        st = next(block for block in named if 's' in block)
        require({'a', 'n', 'c'} <= set(anchor), 'a,n,c connectivity failed')
        require('w' in vw, 'the actual original vw edge was lost')
        if family == 'shared':
            require(vw == ['v', 'w'] and st == ['s', 't'],
                    'shared orbit is not the separated vw / connected st stratum')
        else:
            require(vw == anchor and st == ['s'] and ['t'] in named,
                    'exclusive orbit is not the joined vw / separated st stratum')
        records.append({'column_id': j, 'family': family, 'boundary_components': named,
                        'half_rows': column})
    require(families == EXPECTED, 'the complete target incidence classification changed')
    # Coefficients of every original X in the difference of the two actual rows.
    difference = []
    for j, column in enumerate(orbit['columns']):
        coefficient = int(rows[0] in column) - int(rows[1] in column)
        if coefficient:
            difference.append([j, coefficient])
    require(difference == sorted([[j, 1] for j in EXPECTED['44459_only']] +
                                [[j, -1] for j in EXPECTED['44466_only']]),
            'the small exact difference identity changed')
    # Negative controls address the normalized-anchor and wrong-target pitfalls.
    bad = list(orbit['columns'][EXPECTED['shared'][0]])
    bad[0] ^= 1  # toggle the low color bit at rim t in exactly one row
    bad.sort()
    try:
        components(bad)
    except ValueError:
        corruption_rejected = True
    else:
        corruption_rejected = False
    require(corruption_rejected, 'a changed full orbit support escaped reconstruction')
    require(encode(LITERAL[0]) != encode(LITERAL[1]), 'target difference collapsed')
    return {
        'status': 'EXACT TARGET COMPONENT REDUCTION; strict W7 source exclusion OPEN',
        'scope': 'same complete original core; full boundary orbits and private multiplicities retained',
        'inputs': inputs,
        'targets': TARGETS,
        'target_half_rows': rows,
        'literal_membership_word': ''.join(str(c // 2) for c in LITERAL[0]),
        'all_surviving_columns_checked': len(orbit['columns']),
        'families': families,
        'columns': records,
        'difference_identity': {'left': '2 (Z44459 - Z44466)', 'right_X_terms': difference},
        'conditional_source_identity': 'N44459_separated = N44466_separated',
        'negative_control_changed_support_rejected': corruption_rejected,
        'source_excluded': False,
        'source_realized': False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    result = audit()
    path = HERE / 'target_exchange.json'
    if args.build:
        with path.open('x') as out:
            json.dump(result, out, indent=2, sort_keys=True)
            out.write('\n')
    else:
        require(packed(json.loads(path.read_text())) == packed(result), 'recorded audit mismatch')
    print(json.dumps({key: result[key] for key in (
        'status', 'targets', 'all_surviving_columns_checked', 'families',
        'conditional_source_identity', 'negative_control_changed_support_rejected')}, sort_keys=True))


if __name__ == '__main__':
    main()
