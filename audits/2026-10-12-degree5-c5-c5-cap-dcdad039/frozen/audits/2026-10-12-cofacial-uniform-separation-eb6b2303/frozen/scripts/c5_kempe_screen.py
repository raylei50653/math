#!/usr/bin/env python3
"""Necessary C5 disk-relation screens; no graph catalogue enumeration.

python3 scripts/c5_kempe_screen.py [--check]
The exterior screen assumes 4CT and disk gluing. Neither screen is a
realizability oracle or a Lean proof. Source catalogue is read only.
"""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / 'artifacts/c5_cells/cells.json'
OUT = ROOT / 'artifacts/c5_cells/kempe_screen.json'
PAIRS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def normalize(values):
    seen = {}
    return tuple(seen.setdefault(v, len(seen)) for v in values)


REPS = tuple(sorted({normalize(b) for b in product(range(4), repeat=5)
                     if all(b[i] != b[(i + 1) % 5] for i in range(5))}))
INDEX = {b: j for j, b in enumerate(REPS)}


def partitions(xs):
    if not xs:
        yield ()
        return
    x, *rest = xs
    for p in partitions(rest):
        yield ((x,),) + p
        for j in range(len(p)):
            yield p[:j] + ((x,) + p[j],) + p[j + 1:]


def noncrossing(blocks):
    owner = {v: j for j, block in enumerate(blocks) for v in block}
    return not any(owner[a] == owner[c] and owner[b] == owner[d]
                   and owner[a] != owner[b]
                   for a, b, c, d in combinations(sorted(owner), 4))


def obligations(planar=True):
    """For each pattern and complementary color split, possible swap-orbit masks."""
    table = []
    for b in REPS:
        row = []
        for pairs in PAIRS:
            options = set()
            left = [i for i in range(5) if b[i] in pairs[0]]
            right = [i for i in range(5) if b[i] in pairs[1]]
            for p in partitions(left):
                for q in partitions(right):
                    blocks = p + q
                    if planar and not noncrossing(blocks):
                        continue
                    owner = {v: j for j, block in enumerate(blocks) for v in block}
                    # A boundary edge with both colors in a pair joins its endpoints.
                    if any(any(b[i] in pair and b[(i + 1) % 5] in pair
                               for pair in pairs)
                           and owner[i] != owner[(i + 1) % 5] for i in range(5)):
                        continue
                    orbit = 0
                    for selected in range(1 << len(blocks)):
                        c = list(b)
                        for j, block in enumerate(blocks):
                            if selected >> j & 1:
                                pair = next(pair for pair in pairs if b[block[0]] in pair)
                                for i in block:
                                    c[i] = pair[1] if b[i] == pair[0] else pair[0]
                        orbit |= 1 << INDEX[normalize(c)]
                    options.add(orbit)
            assert options
            row.append(sorted(options))
        table.append(row)
    return table


def failure(mask, table):
    for j, row in enumerate(table):
        if mask >> j & 1:
            for split, options in enumerate(row):
                if not any(mask & orbit == orbit for orbit in options):
                    return dict(pattern=j, split=split, required_alternatives=options)
    return None


def act(mask, rotation, reflection):
    image = [INDEX[normalize(tuple(b[((-i if reflection else i) + rotation) % 5]
                                    for i in range(5)))] for b in REPS]
    return sum(1 << image[j] for j in range(10) if mask >> j & 1)


def orbits(masks):
    remaining = set(masks)
    result = []
    while remaining:
        s = min(remaining)
        orbit = {act(s, r, f) for r in range(5) for f in (False, True)}
        assert orbit <= remaining
        result.append(sorted(orbit))
        remaining -= orbit
    return result


def push(mask, v, spoke):
    """Expose new v adjacent to old v's two boundary neighbors, optionally old v.

    Old v becomes private; retain the old C5 edges. This attaches a disk along
    the two-edge boundary arc and exposes a new ordered C5.
    """
    result = 0
    for j, b in enumerate(REPS):
        for color in range(4):
            if color in (b[(v - 1) % 5], b[(v + 1) % 5]):
                continue
            if spoke and color == b[v]:
                continue
            old = list(b)
            old[v] = color
            if mask >> INDEX[normalize(old)] & 1:
                result |= 1 << j
                break
    return result


def candidate_lemma(mask):
    four = sum(1 << j for j, b in enumerate(REPS) if max(b) == 3)
    if mask & four != four:
        return True
    singletons = [next(i for i in range(5) if b.count(b[i]) == 1)
                  for j, b in enumerate(REPS) if max(b) == 2 and mask >> j & 1]
    return len(singletons) >= 3 or (len(singletons) == 2
                                   and (singletons[0] - singletons[1]) % 5 in (1, 4))


def report():
    data = json.loads(CATALOGUE.read_text())
    assert data['pattern_order'] == [list(b) for b in REPS]
    known = set(map(int, data['cells']))
    table = obligations()
    accepted = {s for s in range(1, 1024) if failure(s, table) is None}
    exterior_rejections = {str(s): min(t for t in known if not s & t)
                           for s in sorted(accepted) if any(not s & t for t in known)}
    combined = accepted - set(map(int, exterior_rejections))
    final = {s for s in combined if candidate_lemma(s)}
    assert known <= accepted and known <= combined
    assert final == known
    # A second generator of partitions (restricted-growth words) checks completeness.
    for n, bell in enumerate((1, 1, 2, 5, 15, 52)):
        generated = {frozenset(map(frozenset, p)) for p in partitions(list(range(n)))}
        independent = set()
        for word in product(range(max(n, 1)), repeat=n):
            if all(word[i] <= max(word[:i], default=-1) + 1 for i in range(n)):
                independent.add(frozenset(frozenset(i for i in range(n) if word[i] == c)
                                          for c in set(word)))
        assert generated == independent and len(generated) == bell
    assert not noncrossing(((0, 2), (1, 3), (4,)))
    assert noncrossing(((0, 3), (1, 2), (4,)))
    unrestricted = obligations(planar=False)
    unrestricted_count = sum(failure(s, unrestricted) is None for s in range(1, 1024))
    assert unrestricted_count == 1023  # Removing topology makes this screen vacuous.
    assert failure(1, table) is not None
    assert '932' in exterior_rejections  # All four-color patterns, no three-color one.
    push_failures = [(s, v, spoke) for s in sorted(accepted) for v in range(5)
                     for spoke in (False, True) if push(s, v, spoke) not in accepted]
    assert not push_failures
    known_push_failures = [(s, v, spoke) for s in sorted(known) for v in range(5)
                           for spoke in (False, True) if push(s, v, spoke) not in known]
    assert not known_push_failures
    return dict(
        trust='External finite check; disk/Kempe soundness is a paper argument; exterior uses 4CT; candidate lemma UNPROVED.',
        catalogue_sha256=sha256(CATALOGUE.read_bytes()).hexdigest(),
        script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        pattern_order=REPS, complementary_splits=PAIRS, obligations=table,
        counts=dict(nonempty_masks=1023, kempe=len(accepted), known=len(known),
                    exterior_rejected=len(exterior_rejections), combined=len(combined),
                    remaining_extra=len(combined - known), with_unproved_lemma=len(final)),
        kempe_masks=sorted(accepted), extra_orbits=orbits(accepted - known),
        kempe_rejections={str(s): failure(s, table) for s in range(1, 1024) if s not in accepted},
        exterior_rejections=exterior_rejections, remaining_extra_orbits=orbits(combined - known),
        remaining_extra=sorted(combined - known), with_unproved_lemma=sorted(final),
        controls=dict(partitions_checked_through_size=5, crossing_rejected=True,
                      no_topology_accepted=unrestricted_count, singleton_mask_1_rejected=True,
                      all_four_only_exterior_rejected=True),
        boundary_push=dict(cases=len(accepted) * 10, kempe_failures=push_failures,
                           known_cases=len(known) * 10, known_failures=known_push_failures))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = report()
    encoded = json.dumps(result, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == encoded, 'Report differs; inspect before regeneration.'
    else:
        OUT.write_text(encoded)
    print(json.dumps(result['counts'], sort_keys=True))
    print('remaining D5 orbits:', result['remaining_extra_orbits'])


if __name__ == '__main__':
    main()
