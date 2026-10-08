#!/usr/bin/env python3
"""Independent M2 run/marker and whole-source normalization controls.

Only standard-library code; no producer/audit module imports. This finite
control does not prove the inherited unbounded attachment classification.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FRAME = {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)}


def read(name):
    return json.loads((ROOT / name).read_text())


def transfer(available, length, left, right):
    if length == 0:
        return left != right
    last = set(available) - {left}
    for _ in range(length - 1):
        last = {c for c in available if last - {c}}
    return bool(last - {right})


def extract_triangle(record):
    edges = {tuple(e) for e in record['edges']}
    vertices = set().union(*map(set, edges))
    support = {v: tuple(sorted(b for b in range(5) if (b, v) in edges))
               for v in vertices if v >= 5}
    tails = []
    for parent in (5, 6, 7):
        previous = parent
        children = [v for v in vertices - set(range(8)) if (parent, v) in edges]
        assert len(children) <= 1
        tail = []
        current = children[0] if children else None
        while current is not None:
            tail.append(support[current])
            following = [v for v in vertices if v >= 5 and v != previous
                         and tuple(sorted((current, v))) in edges]
            assert len(following) <= 1
            previous, current = current, following[0] if following else None
        tails.append(tail)
    return [support[v] for v in (5, 6, 7)], tails


def graph(triangle, tails):
    edges = set(FRAME)
    next_vertex = 8 if triangle else 5
    if triangle:
        edges.update(combinations((5, 6, 7), 2))
        for v, support in zip((5, 6, 7), triangle, strict=True):
            edges.update((b, v) for b in support)
    numbered = []
    for slot, tail in enumerate(tails):
        previous = 5 + slot if triangle else None
        numbered_tail = []
        for support in tail:
            v = next_vertex
            next_vertex += 1
            numbered_tail.append((support, v))
            edges.update((b, v) for b in support)
            if previous is not None:
                edges.add((previous, v))
            previous = v
        numbered.append(numbered_tail)
    return edges, numbered


def compress(triangle, tails, pair):
    _, numbered = graph(triangle, tails)
    reduced = []
    labels = []
    for tail in numbered:
        if not tail:
            reduced.append([])
            labels.append([])
            continue
        kept = []
        start = 0
        while start < len(tail) - 1:
            end = start + 1
            while end < len(tail) - 1 and tail[end][0] == tail[start][0]:
                end += 1
            gap = []
            for token in tail[start:end]:
                if token[1] not in pair:
                    gap.append(token)
                else:
                    if gap:
                        kept.extend(gap[:1 if len(gap) % 2 else 2])
                    kept.append(token)
                    gap = []
            if gap:
                kept.extend(gap[:1 if len(gap) % 2 else 2])
            start = end
        kept.append(tail[-1])  # Original leaf remains singleton.
        reduced.append([support for support, _ in kept])
        labels.append([v if v in pair else None for _, v in kept])
    short_edges, short_tails = graph(triangle, reduced)
    mapping = {v: v for v in pair if triangle and v in (5, 6, 7)}
    for old_labels, new_tail in zip(labels, short_tails, strict=True):
        for old_v, (_, new_v) in zip(old_labels, new_tail, strict=True):
            if old_v is not None:
                assert old_v not in mapping
                mapping[old_v] = new_v
    assert set(mapping) == set(pair)
    short_pair = tuple(mapping[v] for v in pair)
    assert short_pair in short_edges  # Original marker edge was not compressed.
    return tuple(sorted(short_edges)), short_pair


def main():
    paths = ['artifacts/c5_excess_two_mixed_omission/observations.json',
             'artifacts/c5_triangle_branches/observations.json',
             'artifacts/c5_triangle_path_reduction/observations.json']
    omitted, branches, reduction = [read(name) for name in paths]
    domain = {(tuple(map(tuple, f['edges'])), tuple(f['original_root_order'])):
              f['family'] for f in omitted['original_marked_cores']}
    assert len(domain) == 344
    counts = Counter()
    for size in (2, 3, 4):
        for available in combinations(range(4), size):
            for left, right in product(range(4), repeat=2):
                for length in range(25):
                    representative = 0 if length == 0 else 1 if length % 2 else 2
                    assert transfer(available, length, left, right) == transfer(
                        available, representative, left, right)
                    counts['run_transfer_queries'] += 1
    # An explicit forbidden collapse: empty gap cannot become positive even.
    assert not transfer((0, 1, 2), 0, 0, 0)
    assert transfer((0, 1, 2), 2, 0, 0)
    counts['zero_positive_even_negative_control'] = 1

    reached = set()
    def check(triangle, tails):
        edges, _ = graph(triangle, tails)
        bridges = [e for e in edges if e[0] >= 5 and
                   (not triangle or not set(e) <= {5, 6, 7})]
        for pair in bridges:
            key = compress(triangle, tails, pair)
            assert key in domain, ('missing marked normal form', key)
            reached.add(key)
            counts['marked_grammar_compressions'] += 1

    for base in branches['disk_templates']:
        triangle, tails = extract_triangle(base)
        lengths = [range(1, 20, 2) if tail else (0,) for tail in tails]
        for lens in product(*lengths):
            expanded = [[tail[0]] * n + [tail[-1]] if tail else []
                        for tail, n in zip(tails, lens, strict=True)]
            check(triangle, expanded)
    for base in reduction['normal_forms']:
        triangle, tails = extract_triangle(base)
        assert len(tails[0]) == 4 and not tails[1] and not tails[2]
        first, second, repeat, leaf = tails[0]
        assert second == repeat
        for n in range(2, 21, 2):
            check(triangle, [[first] + [second] * n + [leaf], [], []])
    left, right, a, c = (0, 1, 4), (2, 3, 4), (1, 4), (2, 4)
    for supports in ([], [a], [c], [a, c]):
        for lens in product(range(2, 21, 2), repeat=len(supports)):
            tail = [left] + [s for s, n in zip(supports, lens, strict=True)
                            for _ in range(n)] + [right]
            check(None, [tail])
            check(None, [list(reversed(tail))])
    # Two triangles have no run; their original sole bridge stays literal.
    reached.update(key for key, family in domain.items() if family == 'double_triangle')
    assert reached == set(domain)
    counts['covered_marked_forms'] = len(reached)
    families = Counter(domain[key] for key in reached)
    assert families == Counter(triangle_single_run=160, triangle_two_runs=64,
                               path=56, double_triangle=64)

    rows = omitted['pattern_order']
    # Source-wide D5/S4 transport of the exact TWO-spoke joint predicate.
    for row in rows:
        for sign, shift in product((-1, 1), range(5)):
            old_at_new = [(sign * j + shift) % 5 for j in range(5)]
            new_of_old = {old: new for new, old in enumerate(old_at_new)}
            for colors in permutations(range(4)):
                moved_row = [colors[row[old]] for old in old_at_new]
                for root_colors in product(range(4), repeat=2):
                    moved_roots = [colors[color] for color in root_colors]
                    for bz, bw in product(range(5), repeat=2):
                        before = root_colors[0] != row[bz] and root_colors[1] != row[bw]
                        after = moved_roots[0] != moved_row[new_of_old[bz]] and \
                                moved_roots[1] != moved_row[new_of_old[bw]]
                        assert before == after
                        counts['whole_source_spoke_transport_queries'] += 1
    print(json.dumps({'status': 'triggered_and_holds', 'candidate':
          'ba0b447f09617591d9f2ba81c988f537af771791', 'counts': dict(counts),
          'family_counts': dict(families), 'input_sha256': {
          name: sha256((ROOT / name).read_bytes()).hexdigest() for name in paths},
          'scope': 'Finite controls only; inherited attachment/topology coverage remains paper dependent',
          'producer_imports': False, 'planarity_oracle': False}, sort_keys=True))


if __name__ == '__main__':
    main()
