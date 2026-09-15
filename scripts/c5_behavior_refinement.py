#!/usr/bin/env python3
"""Bounded synchronous rooted Kempe experiments on the fixed survivor-811."""
import argparse
from collections import defaultdict, deque
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from c5_equal_cut_witness import ROOT, OUT as SOURCE
from c5_edge_choices import EdgeModel, Move
from c5_kempe_connectivity import PAIRS, component, components
from c5_complementary_cube import encode, singleton_of

OUT = ROOT / 'artifacts/c5_cells/behavior_refinement.json'
GRAMMAR = tuple((p, r) for p in PAIRS for r in range(5))
WORD = (((0, 1), 0), ((1, 2), 2))


class Explorer:
    def __init__(self, model):
        self.model = model

    @lru_cache(None)
    def step(self, c, action):
        pair, root = action
        if c[root] not in pair:
            return None
        block = tuple(sorted(component(self.model.adj, c, pair, root)))
        return self.model.apply(c, Move(pair, block))

    def observation(self, c, kind):
        if c is None:
            return 'illegal'
        if kind == 'escape':
            return singleton_of(c) in (1, 3, 4)
        systems = self.model.dual.systems(c)
        return (c[:5], tuple(tuple(t for t, _ in s if t) for s in systems),
                tuple(sum(not t for t, _ in s) for s in systems))

    def distinguish(self, x, y, depth, kind):
        queue = deque([(x, y, ())])
        seen = {(x, y)}  # Exact concrete pairs only; never observation buckets.
        while queue:
            a, b, word = queue.popleft()
            if self.observation(a, kind) != self.observation(b, kind):
                return word
            if len(word) == depth:
                continue
            for action in GRAMMAR:
                c, d = self.step(a, action), self.step(b, action)
                if c is None or d is None:
                    if c != d:
                        return word + (action,)
                    continue
                if self.observation(c, kind) != self.observation(d, kind):
                    return word + (action,)
                if (c, d) not in seen:
                    seen.add((c, d))
                    queue.append((c, d, word + (action,)))
        return None

    def replay(self, c, word, kind):
        start, events = c, []
        for pair, root in word:
            d = self.step(c, (pair, root))
            event = dict(source=c, pair=pair, root=root, target=d)
            if d is None:
                events.append(event)
                return dict(source=start, events=events, outcome='illegal')
            event['component'] = sorted(component(self.model.adj, c, pair, root))
            event['observation'] = self.observation(d, kind)
            events.append(event)
            c = d
        return dict(source=start, events=events, outcome=self.observation(c, kind))

    def predicate(self, c):
        """Guarded source-only induced-subgraph predicate; None = inapplicable."""
        if c[:5] != (0, 1, 2, 0, 3):
            return None
        k = component(self.model.adj, c, (0, 1), 0)
        if k & set(range(5)) != {0, 1}:
            return None
        u = {v for v, color in enumerate(c)
             if color == 2 or (color == 1 and v not in k)
             or (color == 0 and v in k)}
        blocks = components(self.model.adj, u)
        connected = any({0, 2} <= block for block in blocks)
        # Independent target recomputation checks the source formula.
        d = self.step(c, WORD[0])
        assert u == {v for v, color in enumerate(d) if color in (1, 2)}
        target = self.step(d, WORD[1])
        assert (singleton_of(target) == 4) == (not connected)
        return dict(connected=connected, selected_component=sorted(k),
                    induced_vertices=sorted(u), blocks=sorted(map(sorted, blocks)))

    def framed_predicate(self, c):
        """Same lemma instantiated at the actual boundary colors, without renaming states."""
        a, b, spectator, repeat, last = c[:5]
        if repeat != a or len({a, b, spectator, last}) != 4:
            return None
        first = (tuple(sorted((a, b))), 0)
        second = (tuple(sorted((b, spectator))), 2)
        k = component(self.model.adj, c, first[0], 0)
        if k & set(range(5)) != {0, 1}:
            return None
        u = {v for v, color in enumerate(c)
             if color == spectator or (color == b and v not in k)
             or (color == a and v in k)}
        connected = any({0, 2} <= block for block in components(self.model.adj, u))
        target = self.step(self.step(c, first), second)
        assert (singleton_of(target) == 4) == (not connected)
        return dict(frame=(a, b, spectator, last), connected=connected, word=(first, second))


def report():
    source = json.loads(SOURCE.read_text())
    for path, digest in source['hashes'].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    model = EdgeModel(source['graph'])
    ex = Explorer(model)
    x, y = (tuple(w['source']) for w in source['witnesses'])
    assert ex.observation(x, 'full') == ex.observation(y, 'full')
    regressions = {}
    for kind, word in [('full', WORD[:1]), ('escape', WORD)]:
        replays = [ex.replay(c, word, kind) for c in (x, y)]
        assert replays[0]['outcome'] != replays[1]['outcome']
        found = ex.distinguish(x, y, 2, kind)
        assert found is not None and len(found) == len(word)
        regressions[kind] = dict(prescribed_word=word, replays=replays,
                                 shortest_word=found,
                                 shortest_replays=[ex.replay(c, found, kind) for c in (x, y)])
    assert [ex.predicate(c)['connected'] for c in (x, y)] == [False, True]
    # Complete radius-one corpus for this boundary-root grammar, both seeds.
    # All histories retained even when they reach an identical concrete coloring.
    corpus = defaultdict(list)
    for i, c in enumerate((x, y)):
        corpus[c].append(dict(seed=i, word=()))
        for action in GRAMMAR:
            d = ex.step(c, action)
            if d is not None:
                corpus[d].append(dict(seed=i, word=(action,)))
    rows = [dict(coloring=c, histories=histories, observation=ex.observation(c, 'full'),
                 predicate=ex.predicate(c), framed_predicate=ex.framed_predicate(c))
            for c, histories in sorted(corpus.items())]
    buckets = defaultdict(list)
    for row in rows:
        p = row['predicate']
        key = encode((row['observation'], None if p is None else p['connected']))
        buckets[key].append(tuple(row['coloring']))
    collisions, tested = [], 0
    for bucket in buckets.values():
        for a, b in combinations(bucket, 2):
            tested += 1
            word = ex.distinguish(a, b, 2, 'escape')
            if word is not None:
                collisions.append(dict(word=word, predicate=ex.predicate(a),
                    replays=[ex.replay(c, word, 'escape') for c in (a, b)]))
    framed_buckets = defaultdict(list)
    for row in rows:
        p = row['framed_predicate']
        framed_buckets[encode((row['observation'], p))].append(tuple(row['coloring']))
    framed_pairs = [(a, b) for bucket in framed_buckets.values()
                    for a, b in combinations(bucket, 2)]
    framed_conflicts = [dict(word=w, replays=[ex.replay(c, w, 'escape') for c in (a, b)])
                       for a, b in framed_pairs
                       if (w := ex.distinguish(a, b, 2, 'escape')) is not None]
    # Illegal is distinct from legal non-escape, including on subsequent steps.
    assert ex.replay(x, (((2, 3), 0),), 'escape')['outcome'] == 'illegal'
    assert ex.distinguish(x, x, 2, 'escape') is None
    files = {SOURCE, Path(__file__).resolve(), *(ROOT / p for p in source['hashes'])}
    return dict(trust='Exact bounded Python replay; no general state sufficiency or Lean claim.',
        graph=source['graph'], grammar=GRAMMAR, max_depth=2, regressions=regressions,
        corpus=rows, refined_collisions=collisions, framed_collisions=framed_conflicts,
        summary=dict(concrete_colorings=len(rows), histories=sum(map(len, corpus.values())),
            applicable_predicates=sum(r['predicate'] is not None for r in rows),
            refined_buckets=len(buckets), tested_pairs=tested, collisions=len(collisions),
            applicable_collisions=sum(c['predicate'] is not None for c in collisions),
            framed_applicable=sum(r['framed_predicate'] is not None for r in rows),
            framed_buckets=len(framed_buckets), framed_tested_pairs=len(framed_pairs),
            framed_collisions=len(framed_conflicts),
            shortest_depths={k: len(v['shortest_word']) for k, v in regressions.items()}),
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
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
