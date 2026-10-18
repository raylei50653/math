#!/usr/bin/env python3
"""Independent audit of the root C8 Kempe certificate, with no graph search."""
import itertools
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'kempe-consistency.json').read_text())
assert data['script_sha256'] == hashlib.sha256((ROOT / 'kempe_consistency.py').read_bytes()).hexdigest()
pins = ('a', 'n', 'R', 'L', 'q', 'c', 'x', 'y')
rows = ('01012', '01021', '01023', '01201', '01202', '01203',
        '01212', '01213', '01231', '01232')
splits = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def norm(values):
    encountered = []
    answer = []
    for value in values:
        if value not in encountered:
            encountered.append(value)
        answer.append(encountered.index(value))
    return tuple(answer)


tuples = sorted({norm(t) for t in itertools.product(range(4), repeat=8)
                 if all(t[i] != t[(i+1) % 8] for i in range(8))})
lookup = {t: i for i, t in enumerate(tuples)}
assert len(tuples) == 274
assert data['pin_order'] == list(pins)
assert data['tuples'] == list(map(list, tuples))
assert data['palette_splits'] == [[list(a), list(b)] for a, b in splits]


def original_mask(t):
    base = dict(zip(pins, t))
    edges = [('b', v) for v in ('a', 'c', 'p', 'q')]
    edges += [('p', v) for v in ('a', 'q', 'h', 'n')]
    edges += [('h', v) for v in ('q', 'L', 'R', 'n')]
    mask = 0
    for colours in itertools.product(range(4), repeat=3):
        assignment = base | dict(zip(('b', 'p', 'h'), colours))
        if any(assignment[u] == assignment[v] for u, v in edges):
            continue
        outer = ''.join(map(str, norm(assignment[v] for v in ('x', 'y', 'a', 'b', 'c'))))
        mask |= 1 << rows.index(outer)
    return mask


masks = list(map(original_mask, tuples))
assert data['old_lift_masks'] == masks


def set_partitions(items):
    if not items:
        yield []
        return
    first, *rest = items
    for partition in set_partitions(rest):
        yield [[first]] + partition
        for j in range(len(partition)):
            yield partition[:j] + [[first] + partition[j]] + partition[j+1:]


def noncrossing(blocks):
    index = {point: j for j, block in enumerate(blocks) for point in block}
    return not any(index[a] == index[c] != index[b] == index[d]
                   for a, b, c, d in itertools.combinations(range(8), 4))


partitions = [p for p in set_partitions(list(range(8))) if noncrossing(p)]
assert len(partitions) == data['noncrossing_partition_count'] == 1430


def valid(t, split, blocks):
    side = {colour: j for j, pair in enumerate(split) for colour in pair}
    if any(len({side[t[i]] for i in block}) != 1 for block in blocks):
        return False
    block_index = {point: j for j, block in enumerate(blocks) for point in block}
    return all(side[t[i]] != side[t[(i+1) % 8]] or
               block_index[i] == block_index[(i+1) % 8] for i in range(8))


def orbit(t, split, blocks):
    flip = {a: b for pair in split for a, b in (pair, pair[::-1])}
    answer = set()
    for subset in itertools.product((False, True), repeat=len(blocks)):
        changed = list(t)
        for chosen, block in zip(subset, blocks):
            if chosen:
                for i in block:
                    changed[i] = flip[changed[i]]
        assert all(changed[i] != changed[(i+1) % 8] for i in range(8))
        answer.add(lookup[norm(changed)])
    return answer


summary = []
for result in data['results']:
    source = result['source_mask']
    live = {i for i, mask in enumerate(masks) if mask & ~source == 0}
    assert sorted(live) == result['initial_ids']
    initial_count = len(live)
    for round_ in result['removal_rounds']:
        removed = set()
        for record in round_:
            i = record['tuple_id']
            assert i in live and i not in removed
            split = splits[record['split']]
            possible = [blocks for blocks in partitions if valid(tuples[i], split, blocks)]
            assert possible
            # Recheck EVERY compatible noncrossing partition, including
            # distinct partitions with the same canonical flip orbit.
            assert all(not orbit(tuples[i], split, blocks) <= live for blocks in possible)
            removed.add(i)
        live -= removed
    assert sorted(live) == result['surviving_ids']
    witnesses = {w['tuple_id']: w['splits'] for w in result['surviving_partition_witnesses']}
    assert set(witnesses) == live
    for i in live:
        assert [w['split'] for w in witnesses[i]] == [0, 1, 2]
        for witness in witnesses[i]:
            p = witness['partition']
            blocks = [[j for j in range(8) if p[j] == label] for label in set(p)]
            split = splits[witness['split']]
            assert noncrossing(blocks) and valid(tuples[i], split, blocks)
            assert orbit(tuples[i], split, blocks) <= live
    projected = 0
    for i in live:
        projected |= masks[i]
    accepted = sorted(i for i in live if masks[i] & 512)
    assert projected == result['surviving_old_projection'] == source
    assert accepted == result['accepted_tuple_ids']
    summary.append({'source_mask': source, 'initial': initial_count,
                    'surviving': len(live), 'accepted': len(accepted),
                    'old_projection': projected})

print(json.dumps({'independent_replay': summary,
                  'scope': 'necessary C8 boundary partition closure; no common exterior graph witness'}))
