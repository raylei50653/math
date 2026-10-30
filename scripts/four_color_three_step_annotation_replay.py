#!/usr/bin/env python3
"""Independent finite replay of the boundary-annotation no-gain certificate.

Only the standard library is used.  Set partitions are enumerated directly,
without the producer's forced-atom contraction or the repository D solver.
This verifies a finite boundary-trace relaxation, not common-graph realization.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLORS = tuple(range(4))
SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
CYCLE = (2, 3, 4, 7, 5, 6)
INNER_EDGES = ((0, 1), (0, 2), (0, 3), (0, 4), (0, 7), (1, 2),
               (1, 5), (1, 6), (1, 7), (2, 3), (2, 6),
               (3, 4), (4, 7), (5, 6), (5, 7))
PRIOR = 'audits/2026-10-29-three-step-relation-control-e1a90fe/results.json'
ZV = 'audits/2026-10-30-three-step-shared-exterior-e1a90fe/results.json'


def normalize(word):
    names = {}
    return tuple(names.setdefault(color, len(names)) for color in word)


def partitions(points):
    """Enumerate every set partition of literal boundary positions."""
    if not points:
        yield ()
        return
    point, *rest = points
    for partial in partitions(rest):
        yield ((point,),) + partial
        for index, block in enumerate(partial):
            yield partial[:index] + ((point,) + block,) + partial[index + 1:]


def proper(word):
    return all(word[index] != word[(index + 1) % len(word)]
               for index in range(len(word)))


def changed_row(word, split, blocks, selected):
    mate = {a: b for pair in SPLITS[split]
            for a, b in (pair, tuple(reversed(pair)))}
    changed = list(word)
    for index, block in enumerate(blocks):
        if selected >> index & 1:
            for position in block:
                changed[position] = mate[word[position]]
    return tuple(changed)


@lru_cache(maxsize=None)
def options(word, split):
    left, right = SPLITS[split]
    left_points = [index for index, color in enumerate(word) if color in left]
    right_points = [index for index, color in enumerate(word) if color in right]
    result = []
    for left_partition in partitions(left_points):
        for right_partition in partitions(right_points):
            blocks = tuple(sorted(left_partition + right_partition))
            owners = {point: index for index, block in enumerate(blocks)
                      for point in block}
            if any((word[index] in left) == (word[(index + 1) % 6] in left)
                   and owners[index] != owners[(index + 1) % 6]
                   for index in range(6)):
                continue
            if any(owners[a] == owners[c] and owners[b] == owners[d]
                   and owners[a] != owners[b]
                   for a, b, c, d in combinations(range(6), 4)):
                continue
            orbit = frozenset(changed_row(word, split, blocks, selected)
                              for selected in range(1 << len(blocks)))
            assert all(proper(target) for target in orbit)
            result.append((blocks, orbit))
    assert result and len({blocks for blocks, _ in result}) == len(result)
    return tuple(sorted(result))


def reconstruct_screen():
    patterns = sorted({normalize(word) for word in product(COLORS, repeat=6)
                       if proper(word)})
    lookup = {word: index for index, word in enumerate(patterns)}
    accepted = 0
    for index, word in enumerate(patterns):
        boundary = dict(zip(CYCLE, word))
        if any(all((boundary | {0: first, 1: second})[u] !=
                   (boundary | {0: first, 1: second})[v]
                   for u, v in INNER_EDGES)
               for first, second in product(COLORS, repeat=2)):
            accepted |= 1 << index
    orbit_masks = [[tuple(sorted({sum(1 << lookup[row] for row in
                                        {normalize(target) for target in orbit})
                                 for _, orbit in options(word, split)}))
                    for split in range(3)] for word in patterns]
    current = ((1 << len(patterns)) - 1) ^ accepted
    removed_masks = []
    while True:
        removed = sum(1 << index for index, splits in enumerate(orbit_masks)
                      if current >> index & 1 and
                      any(not any(mask & current == mask for mask in masks)
                          for masks in splits))
        if not removed:
            break
        removed_masks.append(removed)
        current &= ~removed
    assert len(patterns) == 31 and accepted == 4969575
    assert removed_masks == [67108872] and current == 2075405200
    return patterns, accepted, current, removed_masks


def reconstruct_annotations(patterns, residual):
    surviving = {word for index, word in enumerate(patterns)
                 if residual >> index & 1}
    rows = [word for word in product(COLORS, repeat=6)
            if normalize(word) in surviving]
    row_set = set(rows)
    states = []
    for word in rows:
        allowed = [[blocks for blocks, orbit in options(word, split)
                    if orbit <= row_set] for split in range(3)]
        assert all(allowed)
        for triple in product(*allowed):
            states.append((word, triple))
    assert len(rows) == 384 and len(states) == 864
    return rows, states


def serial_state(state):
    row, splits = state
    return dict(row=list(row), partitions=[[list(block) for block in partition]
                                          for partition in splits])


def canonical_state(state):
    word, partitions_at_source = state
    normalized = normalize(word)
    names = dict(zip(word, normalized))
    for color in COLORS:
        if color not in names:
            names[color] = next(candidate for candidate in COLORS
                                if candidate not in names.values())
    result = [None, None, None]
    for split, partition in enumerate(partitions_at_source):
        moved_split = frozenset(frozenset(names[color] for color in pair)
                               for pair in SPLITS[split])
        target = next(index for index, pairs in enumerate(SPLITS)
                      if moved_split == frozenset(map(frozenset, pairs)))
        result[target] = partition
    return normalized, tuple(result)


def transition_records(states):
    lookup = {}
    for index, (word, splits) in enumerate(states):
        for split, blocks in enumerate(splits):
            lookup.setdefault((word, split, blocks), []).append(index)
    for source, (word, splits) in enumerate(states):
        for split, blocks in enumerate(splits):
            for selected in range(1 << len(blocks)):
                target_row = changed_row(word, split, blocks, selected)
                targets = [source] if selected == 0 else lookup[(target_row, split, blocks)]
                assert targets
                yield [source, split, selected, targets]


def digest_records(records):
    digest = sha256()
    groups = edges = 0
    for record in records:
        digest.update(json.dumps(record, separators=(',', ':')).encode() + b'\n')
        groups += 1
        edges += len(record[3])
    return dict(groups=groups, edges=edges, sha256=digest.hexdigest())


def verify_controls(record):
    prior = json.loads((ROOT / PRIOR).read_text())
    zv = json.loads((ROOT / ZV).read_text())
    core = {tuple(edge) for edge in prior['core_edges']}
    assert core == set(INNER_EDGES) | {(2, 8)}
    complete = {}
    colorings = []
    for word in product(COLORS, repeat=9):
        if all(word[u] != word[v] for u, v in core):
            colorings.append(word)
            complete.setdefault(word[3:], []).append(word[:3])
    all_fibres = [complete.get(word, []) for word in product(COLORS, repeat=6)]
    assert prior['kernel']['boundary_order'] == list(range(3, 9))
    assert prior['kernel']['full_fibres'] == [[list(lift) for lift in fibre]
                                            for fibre in all_fibres]
    empty_word = (0, 1, 1, 0, 0, 1)
    assert empty_word not in complete
    fixed = dict(zip(range(3, 9), empty_word))
    assert all(fixed[u] != fixed[v] for u, v in core if u >= 3)
    planar = dict(nonempty=len(complete), empty=4 ** 6 - len(complete),
                  lifts=len(colorings), proper_empty_word=list(empty_word))
    assert planar == record['planar_kernel']
    assert (planar['nonempty'], planar['empty'], planar['lifts']) == (732, 3364, 936)
    contract = zv['contract']
    edges = {tuple(edge) for edge in contract['original_edges']}
    outer_cycle = contract['C_order']
    assert outer_cycle == [9, 10, 13, 12, 11, 14, 15, 16]
    attachments = {(3, 9), (4, 13), (5, 11), (6, 15), (2, 16)}
    ring_edges = {tuple(sorted(edge)) for edge in
                  zip(outer_cycle, outer_cycle[1:] + outer_cycle[:1])}
    assert edges == core | ring_edges | attachments and len(edges) == 29
    # The old control retains an actual sphere rotation and the same core.
    faces = contract['oriented_faces']
    darts = Counter(edge for face in faces for edge in zip(face, face[1:] + face[:1]))
    assert darts == Counter({(u, v): 1 for u, v in edges} |
                            {(v, u): 1 for u, v in edges})
    assert 17 - len(edges) + len(faces) == 2
    for vertex in range(17):
        following = {}
        for face in faces:
            for index, point in enumerate(face):
                if point == vertex:
                    predecessor = face[index - 1]
                    assert predecessor not in following
                    following[predecessor] = face[(index + 1) % len(face)]
        start = next(iter(following))
        seen, point = set(), start
        while point not in seen:
            seen.add(point)
            point = following[point]
        assert point == start and seen == set(following)
    counts = zv['outer']['full_counts']
    assert len(counts) == 4 ** 8
    cached_counts = {}
    proper_count = 0
    for word, stored_count in zip(product(COLORS, repeat=8), counts):
        if not proper(word):
            assert stored_count == 0
            continue
        proper_count += 1
        eta = dict(zip(outer_cycle, word))
        signature = tuple(eta[v] for v in (9, 13, 11, 15, 16))
        if signature not in cached_counts:
            cached_counts[signature] = sum(all(coloring[u] != eta[v]
                                               for u, v in attachments)
                                           for coloring in colorings)
        assert cached_counts[signature] == stored_count > 0
        h = eta[15]
        p = min(set(COLORS) - {h, eta[9], eta[11]})
        q = min(set(COLORS) - {h, p, eta[13]})
        r = (set(COLORS) - {h, p, q}).pop()
        coloring = dict(enumerate((r, q, h, p, q, p, r, h, p))) | eta
        assert all(coloring[u] != coloring[v] for u, v in edges)
    expected_zv = dict(proper=proper_count, accepted=proper_count,
                       literal_lifts=sum(counts), complete_old_counts_retained=True,
                       constructive_extension_rechecked=True)
    assert record['zv'] == expected_zv
    assert proper_count == 6564 and sum(counts) == 1529784
    return dict(planar_kernel=planar, zv=expected_zv,
                zv_complete_outer_counts_independently_recomputed=True)


def verify_manifest(results_path):
    manifest = json.loads((results_path.parent / 'verification.json').read_text())
    required = {PRIOR, ZV, 'scripts/ck_kempe_obstruction.py',
                'scripts/four_color_three_step_annotations.py',
                'scripts/four_color_three_step_annotation_replay.py'}
    assert set(manifest['sources']) == required
    for relative, expected in manifest['sources'].items():
        assert sha256((ROOT / relative).read_bytes()).hexdigest() == expected, relative
    assert manifest['outputs'] == {'results.json': sha256(results_path.read_bytes()).hexdigest()}
    return dict(source_hashes=len(required), result_hash=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.results.read_text())
    patterns, accepted, residual, removed = reconstruct_screen()
    rows, states = reconstruct_annotations(patterns, residual)
    # The certificate schema is shared with the producer, not its algorithms.
    assert data['contract']['original_cycle'] == list(CYCLE)
    assert data['contract']['core_edges'] == [list(edge) for edge in INNER_EDGES]
    assert data['old']['patterns'] == [list(word) for word in patterns]
    assert data['old']['accepted_mask'] == accepted
    assert data['old']['initial_mask'] == ((1 << len(patterns)) - 1) ^ accepted
    assert data['old']['residual_mask'] == residual
    assert data['old']['removed_masks'] == removed
    assert data['candidate']['name'] == 'PAIR-C0-D16'
    assert data['candidate']['patterns'] == [list(word) for index, word in enumerate(patterns)
                                             if residual >> index & 1]
    assert data['candidate']['literal_rows'] == [list(word) for word in rows]
    annotation = data['annotation']
    assert annotation['states'] == [serial_state(state) for state in states]
    canonical_count = len({canonical_state(state) for state in states})
    assert annotation['canonical_state_count'] == canonical_count == 36
    summary = digest_records(transition_records(states))
    assert annotation['full_transition_count'] == summary['edges']
    assert annotation['transition_sha256'] == summary['sha256']
    cubes = annotation['cubes']
    assert len(cubes) == 3 * len(states)
    for expected, cube in enumerate(cubes):
        source, split, targets = cube
        assert source == expected // 3 and split == expected % 3
        word, partitions_at_source = states[source]
        blocks = partitions_at_source[split]
        assert len(targets) == 1 << len(blocks) and targets[0] == source
        assert len(set(targets)) == len(targets)
        for selected, target in enumerate(targets):
            target_row, partitions_at_target = states[target]
            assert target_row == changed_row(word, split, blocks, selected)
            assert partitions_at_target[split] == blocks
            # Every corner has the same full cube, translated by XOR.
            for further in range(1 << len(blocks)):
                translated = targets[selected ^ further]
                translated_row, translated_partitions = states[translated]
                assert translated_row == changed_row(target_row, split, blocks, further)
                assert translated_partitions[split] == blocks
    projections = annotation['projections']
    expected_positions = [positions for size in range(7)
                          for positions in combinations(range(6), size)]
    assert len(projections) == len(expected_positions) == 64
    for projection, positions in zip(projections, expected_positions):
        assert projection['positions'] == list(positions)
        fibres = {}
        for index, (word, _) in enumerate(states):
            fibres.setdefault(tuple(word[p] for p in positions), []).append(index)
        assert projection['full_fibres'] == [fibres.get(word, []) for word in
                                             product(COLORS, repeat=len(positions))]
        assert sum(map(len, projection['full_fibres'])) == len(states)
    controls = verify_controls(data['controls'])
    manifest = verify_manifest(args.results)
    print(json.dumps(dict(status='PASS', proper_patterns=len(patterns),
                          accepted_patterns=accepted.bit_count(),
                          residual_patterns=residual.bit_count(), literal_rows=len(rows),
                          annotation_states=len(states), transitions=summary,
                          complete_projection_families=64, controls=controls,
                          manifest=manifest,
                          exact_source_realization='OPEN'), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
