#!/usr/bin/env python3
"""Fixed-predicate radius-two experiment; raw states and action labels retained."""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

from c5_behavior_refinement import Explorer, GRAMMAR, ROOT, SOURCE
from c5_complementary_cube import encode
from c5_edge_choices import EdgeModel

OUT = ROOT / 'artifacts/c5_cells/behavior_radius2.json'
PERMS = tuple(permutations(range(4)))


def recolor(c, p):
    return tuple(p[v] for v in c)


def pair_orbit(a, b):
    # Diagnostic key only: simultaneous color action, unordered pair, fixed vertices.
    return min(tuple(sorted((recolor(a, p), recolor(b, p)))) for p in PERMS)


def report():
    source = json.loads(SOURCE.read_text())
    for path, digest in source['hashes'].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    ex = Explorer(EdgeModel(source['graph']))
    seeds = tuple(tuple(w['source']) for w in source['witnesses'])
    corpus = defaultdict(list)
    frontier = [(i, c, ()) for i, c in enumerate(seeds)]
    for depth in range(3):
        following = []
        for seed, c, word in frontier:
            corpus[c].append(dict(seed=seed, word=word))
            if depth < 2:
                for action in GRAMMAR:
                    d = ex.step(c, action)
                    if d is not None:
                        following.append((seed, d, word + (action,)))
        frontier = following
    rows = []
    for c, histories in sorted(corpus.items()):
        ex.model.validate(c)
        rows.append(dict(coloring=c, histories=histories,
                         observation=ex.observation(c, 'full'),
                         predicate=ex.predicate(c), framed_predicate=ex.framed_predicate(c)))
    experiments = {}
    for radius in (1, 2):
        selected = [r for r in rows if min(len(h['word']) for h in r['histories']) <= radius]
        variants = {}
        for kind in ('base', 'fixed', 'framed'):
            buckets = defaultdict(list)
            for r in selected:
                p = None if kind == 'base' else r['predicate' if kind == 'fixed' else 'framed_predicate']
                key = encode((r['observation'], None if p is None else p['connected']))
                buckets[key].append(tuple(r['coloring']))
            pairs = [pair for bucket in buckets.values() for pair in combinations(bucket, 2)]
            conflicts, nondistinguished = [], []
            for a, b in pairs:
                equivalent = any(recolor(a, p) == b for p in PERMS)
                words = {o: ex.distinguish(a, b, 2, o) for o in ('full', 'escape')}
                record = dict(sources=(a, b), global_recoloring_equivalent=equivalent,
                              original_pair_orbit=pair_orbit(a, b) == pair_orbit(*seeds),
                              words=words,
                              replays={o: [ex.replay(c, w, o) for c in (a, b)]
                                       for o, w in words.items() if w is not None})
                for replays in record['replays'].values():
                    assert replays[0]['outcome'] != replays[1]['outcome']
                (conflicts if any(w is not None for w in words.values()) else nondistinguished).append(record)
            variants[kind] = dict(
                summary=dict(buckets=len(buckets), bucket_sizes=dict(sorted(Counter(map(len, buckets.values())).items())),
                             tested_pairs=len(pairs),
                             global_recoloring_pairs=sum(any(recolor(a, p) == b for p in PERMS) for a, b in pairs),
                             pair_color_orbits=len({pair_orbit(a, b) for a, b in pairs}),
                             full_conflicts=sum(r['words']['full'] is not None for r in conflicts),
                             escape_conflicts=sum(r['words']['escape'] is not None for r in conflicts),
                             escape_depths=dict(sorted(Counter(len(r['words']['escape']) for r in conflicts if r['words']['escape'] is not None).items())),
                             original_orbit_pairs=sum(pair_orbit(a, b) == pair_orbit(*seeds) for a, b in pairs)),
                nontrivial_buckets=[b for b in buckets.values() if len(b) > 1],
                conflicts=conflicts, nondistinguished=nondistinguished)
        experiments[str(radius)] = dict(colorings=len(selected),
            histories=sum(len(h['word']) <= radius for r in selected for h in r['histories']), variants=variants)
    assert [experiments['1']['variants'][k]['summary']['buckets'] for k in ('base', 'fixed', 'framed')] == [15, 16, 18]
    assert experiments['1']['variants']['base']['summary']['original_orbit_pairs'] == 3
    # Exact full-vertex verification of the two remaining radius-one collisions.
    expected = [((0, 2, 1, 3), False), ((0, 3, 2, 1), True)]
    actual = experiments['1']['variants']['fixed']['conflicts']
    for p, reverse in expected:
        pair = tuple(recolor(c, p) for c in seeds)
        if reverse:
            pair = pair[::-1]
        assert any(tuple(r['sources']) == pair for r in actual)
    files = {SOURCE, Path(__file__).resolve(), ROOT / 'scripts/c5_behavior_refinement.py',
             *(ROOT / p for p in source['hashes'])}
    return dict(trust='Bounded Python evidence, no closure or general sufficiency claim.',
                graph=source['graph'], grammar=GRAMMAR, radius=2, continuation_depth=2,
                corpus=rows, experiments=experiments,
                radius1_recolorings=[dict(permutation=p, reverse=rev) for p, rev in expected],
                hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(files)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = report()
    content = encode(result) + '\n'
    if args.check:
        assert OUT.read_text() == content, 'Certificate differs; inspect before regenerating.'
    else:
        OUT.write_text(content)
    print(json.dumps({r: dict(colorings=e['colorings'], histories=e['histories'],
        variants={k: v['summary'] for k, v in e['variants'].items()})
        for r, e in result['experiments'].items()}, indent=2))


if __name__ == '__main__':
    main()
