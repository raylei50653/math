#!/usr/bin/env python3
"""Necessary planar C8 Kempe closure, not enumeration of exterior graphs."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PIN = ('a', 'n', 'R', 'L', 'q', 'c', 'x', 'y')
ROWS = ('01012', '01021', '01023', '01201', '01202', '01203', '01212', '01213', '01231', '01232')
PALETTE_SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def canonical(values):
    names = {}
    return tuple(names.setdefault(v, len(names)) for v in values)


TUPLES = sorted({canonical(t) for t in itertools.product(range(4), repeat=8)
                 if all(t[i] != t[(i+1) % 8] for i in range(8))})
INDEX = {t: i for i, t in enumerate(TUPLES)}
assert len(TUPLES) == 274


def partitions(prefix=(0,)):
    if len(prefix) == 8:
        yield prefix
        return
    for x in range(max(prefix) + 2):
        yield from partitions(prefix + (x,))


FOUR = tuple(itertools.combinations(range(8), 4))
NONCROSSING = [p for p in partitions()
               if not any(p[i] == p[k] and p[j] == p[l] and p[i] != p[j]
                          for i, j, k, l in FOUR)]
assert len(NONCROSSING) == 1430


def local_old_mask(t):
    c = dict(zip(PIN, t))
    out = 0
    for b, p, h in itertools.product(range(4), repeat=3):
        if b in {c['a'], c['c'], c['q']}:
            continue
        if p in {c['a'], b, c['q'], c['n'], h}:
            continue
        if h in {c['q'], c['L'], c['R'], c['n']}:
            continue
        row = ''.join(map(str, canonical((c['x'], c['y'], c['a'], b, c['c']))))
        out |= 1 << ROWS.index(row)
    return out


OLD_MASKS = [local_old_mask(t) for t in TUPLES]


def options(t, split):
    side = {colour: j for j, pair in enumerate(split) for colour in pair}
    flip = {pair[j]: pair[1-j] for pair in split for j in (0, 1)}
    found = {}
    for partition in NONCROSSING:
        blocks = [tuple(i for i, v in enumerate(partition) if v == b)
                  for b in range(max(partition)+1)]
        if any(len({side[t[i]] for i in block}) != 1 for block in blocks):
            continue
        if any(side[t[i]] == side[t[(i+1) % 8]] and partition[i] != partition[(i+1) % 8]
               for i in range(8)):
            continue
        orbit = set()
        for chosen in range(1 << len(blocks)):
            changed = tuple(flip[colour] if chosen & (1 << partition[i]) else colour
                            for i, colour in enumerate(t))
            assert all(changed[i] != changed[(i+1) % 8] for i in range(8))
            orbit.add(INDEX[canonical(changed)])
        orbit = tuple(sorted(orbit))
        found.setdefault(orbit, partition)
    assert found, (t, split)
    return [(orbit, found[orbit]) for orbit in sorted(found)]


OPTIONS = [[options(t, split) for split in PALETTE_SPLITS] for t in TUPLES]


def close(initial):
    live = set(initial)
    rounds = []
    while True:
        removed = []
        for i in sorted(live):
            for split, choices in enumerate(OPTIONS[i]):
                if not any(set(orbit) <= live for orbit, _ in choices):
                    removed.append({'tuple_id': i, 'split': split,
                                    'obstruction': [{'partition': partition,
                                                     'missing_tuple': min(set(orbit)-live)}
                                                    for orbit, partition in choices]})
                    break
        if not removed:
            return live, rounds
        rounds.append(removed)
        live.difference_update(r['tuple_id'] for r in removed)


results = []
for mask in (932, 933, 941):
    initial = {i for i, local in enumerate(OLD_MASKS) if local & ~mask == 0}
    live, rounds = close(initial)
    projected = 0
    for i in live:
        projected |= OLD_MASKS[i]
    witnesses = []
    for i in sorted(live):
        witnesses.append({'tuple_id': i,
                          'splits': [{'split': j, 'partition': list(next(partition for orbit, partition in choices
                                                                        if set(orbit) <= live))}
                                     for j, choices in enumerate(OPTIONS[i])]})
    results.append({'source_mask': mask, 'initial_ids': sorted(initial),
                    'removal_rounds': rounds, 'surviving_ids': sorted(live),
                    'surviving_old_projection': projected,
                    'surviving_partition_witnesses': witnesses,
                    'accepted_tuple_ids': [i for i in sorted(live) if OLD_MASKS[i] & 512]})

RESULT = {'scope': 'necessary noncrossing boundary-component closure only; no graph realization',
          'pin_order': PIN, 'tuples': TUPLES, 'old_lift_masks': OLD_MASKS,
          'palette_splits': PALETTE_SPLITS,
          'noncrossing_partition_count': len(NONCROSSING), 'results': results,
          'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
parser = argparse.ArgumentParser()
parser.add_argument('--check', action='store_true')
parser.add_argument('--certificate', type=Path, default=ROOT/'kempe-consistency.json')
args = parser.parse_args()
if args.check:
    assert json.loads(args.certificate.read_text()) == json.loads(json.dumps(RESULT))
else:
    with args.certificate.open('x') as f:
        f.write(json.dumps(RESULT, indent=2)+'\n')
print(json.dumps([{'source_mask': r['source_mask'], 'initial': len(r['initial_ids']),
                   'surviving': len(r['surviving_ids']),
                   'round_removals': list(map(len, r['removal_rounds'])),
                   'accepted': len(r['accepted_tuple_ids']),
                   'old_projection': r['surviving_old_projection']} for r in results]))
