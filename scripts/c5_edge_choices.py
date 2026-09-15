#!/usr/bin/env python3
"""Witness-backed sets of joint edge relations, switches, and constraint filters.

uv run --with networkx==3.5 python scripts/c5_edge_choices.py [--check]
Fixed embedded disk; explicit raw color frame; no projection-based merging.
"""
import argparse
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from c5_edge_states import Dual, TYPE_PAIRS
from c5_kempe_connectivity import adjacency, PAIRS, pair_components, swap
from c5_complementary_cube import singleton_of, encode

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_cells/edge_states.json'
OUT = ROOT / 'artifacts/c5_cells/edge_choices.json'


@dataclass(frozen=True)
class Move:
    pair: tuple
    component: tuple


@dataclass(frozen=True)
class Branch:
    coloring: tuple
    origin: int
    history: tuple = ()


class EdgeModel:
    """One fixed verified embedded disk, with vertex and color labels retained."""

    def __init__(self, graph):
        self.name = graph['name']
        self.n = graph['n']
        self.edges = tuple(tuple(e) for e in graph['edges'])
        self.faces = tuple(tuple(f) for f in graph['faces'])
        self.adj = adjacency(self.n, self.edges)
        self.dual = Dual(self.n, list(self.edges), self.faces)
        self.transition_table = []
        self.transition_index = {}

    def validate(self, c):
        if (len(c) != self.n or any(x not in range(4) for x in c)
                or any(c[u] == c[v] for u, v in self.edges)):
            raise ValueError('Expected a complete proper coloring on this disk.')

    @lru_cache(None)
    def view(self, c):
        self.validate(c)
        return self.dual.state(c)

    @lru_cache(None)
    def actions(self, c):
        self.validate(c)
        return tuple(Move(p, tuple(sorted(s))) for p in PAIRS
                     for s in sorted(pair_components(self.adj, c, p), key=lambda s: tuple(sorted(s))))

    def apply(self, c, move):
        if move not in self.actions(c):
            raise ValueError('Switch requires a maximal component of the named pair.')
        d = swap(c, move.component, move.pair)
        self.validate(d)
        return d

    @lru_cache(None)
    def compatible(self, c):
        return (singleton_of(c) not in (1, 3, 4)
                and all(singleton_of(self.apply(c, a)) not in (1, 3, 4)
                        for a in self.actions(c)))

    def edge_replay(self, c, move):
        """Reconstruct the output from switched edge types and a single anchor."""
        d = self.apply(c, move)
        block, k = set(move.component), move.pair[0] ^ move.pair[1]
        cut = {j for j, (u, v) in enumerate(self.edges) if (u in block) != (v in block)}
        old = [c[u] ^ c[v] for u, v in self.edges]
        assert all(old[j] != k for j in cut)
        delta = [t ^ k if j in cut else t for j, t in enumerate(old)]
        adj = [[] for _ in range(self.n)]
        for (u, v), t in zip(self.edges, delta):
            adj[u].append((v, t))
            adj[v].append((u, t))
        recovered = [None] * self.n
        recovered[0] = c[0] ^ k if 0 in block else c[0]
        queue = [0]
        for u in queue:
            for v, t in adj[u]:
                expected = recovered[u] ^ t
                if recovered[v] is None:
                    recovered[v] = expected
                    queue.append(v)
                assert recovered[v] == expected
        assert tuple(recovered) == d
        si = TYPE_PAIRS.index(tuple(t for t in (1, 2, 3) if t != k))
        parts = self.dual.systems(c)[si]
        selected = [i for i, (_, es) in enumerate(parts) if cut & set(es)]
        assert set().union(*(set(parts[i][1]) for i in selected)) == cut
        assert parts == self.dual.systems(d)[si]
        systems = []
        regions = []
        for i, types in enumerate(TYPE_PAIRS):
            before, after = self.dual.systems(c)[i], self.dual.systems(d)[i]
            systems.append(dict(types=types, before=before, after=after,
                retained_edge_overlap=[[sorted(set(a[1]) & set(b[1])) for b in after] for a in before],
                cycle_count_before=sum(not t for t, _ in before),
                cycle_count_after=sum(not t for t, _ in after)))
        for missing in (1, 2, 3):
            def blocks(x):
                return sorted((tuple(sorted(s)) for p in PAIRS if p[0] ^ p[1] == missing
                               for s in pair_components(self.adj, x, p)))
            before, after = blocks(c), blocks(d)
            overlaps = [[sorted(set(a) & set(b)) for b in after] for a in before]
            # These partitions use every primal vertex: an old region can split
            # and portions can merge elsewhere. Counts alone lose that distinction.
            regions.append(dict(missing_type=missing, before=before, after=after,
                vertex_overlap=overlaps,
                split_old_regions=[j for j, row in enumerate(overlaps) if sum(bool(x) for x in row) > 1],
                merged_into_new_regions=[j for j in range(len(after))
                                         if sum(bool(row[j]) for row in overlaps) > 1]))
        return dict(pair=move.pair, component=move.component, cut_edges=sorted(cut),
                    preserved_system=TYPE_PAIRS[si], selected_components=selected,
                    systems=systems, regions=regions, after=d)

    def record_move(self, c, move):
        key = (c, move)
        if key not in self.transition_index:
            self.transition_index[key] = len(self.transition_table)
            self.transition_table.append(dict(before=c, **self.edge_replay(c, move)))
        return self.transition_index[key]


@dataclass(frozen=True)
class Choice:
    model: EdgeModel
    seeds: tuple
    branches: tuple
    scope: str

    @classmethod
    def start(cls, model, colorings, scope):
        seeds = tuple(tuple(c) for c in colorings)
        for c in seeds:
            model.validate(c)
        return cls(model, seeds, tuple(Branch(c, i) for i, c in enumerate(seeds)), scope)

    def condition(self, predicate):
        """Filter complete witnesses; predicate receives a Branch (including history)."""
        return Choice(self.model, self.seeds,
                      tuple(b for b in self.branches if predicate(b)), self.scope)

    def switch(self, pair=None, component=None):
        """All one-step successors, or those matching one named action.

        A selector with no legal action in a branch contributes no successor.
        Different pairs are never applied simultaneously to stale components.
        """
        if pair is not None and tuple(pair) not in PAIRS:
            raise ValueError('Use an ordered distinct color pair from PAIRS.')
        if component is not None and pair is None:
            raise ValueError('A component selector requires a color pair.')
        selected = None if component is None else tuple(sorted(component))
        branches = []
        for b in self.branches:
            for action in self.model.actions(b.coloring):
                if pair is not None and action.pair != tuple(pair):
                    continue
                if selected is not None and action.component != selected:
                    continue
                branches.append(Branch(self.model.apply(b.coloring, action), b.origin,
                                       b.history + (action,)))
        return Choice(self.model, self.seeds, tuple(branches), self.scope)

    def split(self, predicate):
        return self.condition(predicate), self.condition(lambda b: not predicate(b))

    def query(self, predicate):
        yes, no = self.split(predicate)
        if not self.branches:
            return 'empty'
        return 'mixed' if yes.branches and no.branches else 'forced_true' if yes.branches else 'forced_false'

    def view(self):
        """Group only for presentation; every branch and its witness remain present."""
        groups = defaultdict(list)
        for i, b in enumerate(self.branches):
            groups[self.model.view(b.coloring)].append(i)
        return [dict(relation=t, branch_indices=indices) for t, indices in sorted(groups.items())]

    def card(self):
        return dict(branches=len(self.branches), witnesses=len({b.coloring for b in self.branches}),
                    joint_relations=len(self.view()), origins=sorted({b.origin for b in self.branches}),
                    compatible_branches=sum(self.model.compatible(b.coloring) for b in self.branches))

    def certificate(self):
        rows = []
        for b in self.branches:
            c = self.seeds[b.origin]
            path = []
            for move in b.history:
                index = self.model.record_move(c, move)
                row = self.model.transition_table[index]
                path.append(index)
                c = tuple(row['after'])
            assert c == b.coloring
            rows.append(dict(origin=b.origin, coloring=c, relation=self.model.view(c),
                             compatible_through_one_move=self.model.compatible(c), history=path))
        return dict(scope=self.scope, card=self.card(), groups=self.view(), branches=rows)


def study(model, seeds):
    start = Choice.start(model, seeds, 'Exactly two supplied Errera witnesses; switch means exactly one move.')
    assert start.card()['witnesses'] == 2 and start.card()['joint_relations'] == 1
    first = start.switch()
    second = first.switch()
    # Independent direct move sets, without Choice or EdgeModel.apply.
    expected = set(seeds)
    for state in (first, second):
        expected = {swap(c, block, pair) for c in expected for pair in PAIRS
                    for block in pair_components(model.adj, c, pair)}
        assert {b.coloring for b in state.branches} == expected

    by_origin = [{model.view(b.coloring) for b in first.branches if b.origin == i} for i in (0, 1)]
    # Choose a real target available only from the second witness.
    target = min(by_origin[1] - by_origin[0])
    constrained = first.condition(lambda b: model.view(b.coloring) == target)
    assert constrained.branches and {b.origin for b in constrained.branches} == {1}
    only_first = start.condition(lambda b: b.origin == 0).switch()
    assert not only_first.condition(lambda b: model.view(b.coloring) == target).branches
    # Both origins have the same displayed source T. Looking up transitions by T
    # alone would splice the second origin's move onto the first origin illegally.
    assert model.view(seeds[0]) == model.view(seeds[1])
    assert target in by_origin[0] | by_origin[1] and target not in by_origin[0]

    one = constrained.condition(lambda b: b.coloring == constrained.branches[0].coloring)
    impossible = one.condition(lambda b: model.view(b.coloring) != target)
    assert len({b.coloring for b in one.branches}) == 1
    assert impossible.query(lambda b: True) == 'empty'
    yes, no = first.split(lambda b: model.compatible(b.coloring))
    assert len(yes.branches) + len(no.branches) == len(first.branches)
    assert all(model.compatible(b.coloring) for b in yes.branches)
    assert not impossible.switch().branches
    prefix_safe = yes.switch().condition(lambda b: model.compatible(b.coloring))
    final_safe = second.condition(lambda b: model.compatible(b.coloring))
    prefix_keys = {(b.origin, b.history) for b in prefix_safe.branches}
    assert prefix_keys <= {(b.origin, b.history) for b in final_safe.branches}
    unsafe_prefix = [b for b in final_safe.branches if (b.origin, b.history) not in prefix_keys]
    assert unsafe_prefix
    assert all(not model.compatible(model.apply(seeds[b.origin], b.history[0]))
               for b in unsafe_prefix)
    # A valid matching boundary does not rescue a non-maximal switch component.
    try:
        model.apply(seeds[0], Move((0, 2), (0,)))
    except ValueError:
        pass
    else:
        raise AssertionError('Non-maximal component was accepted.')

    # Enumerate the exact two-step relation, then deliberately forget correlations.
    by_word = defaultdict(set)
    for b in second.branches:
        word, *pairings = model.view(b.coloring)
        by_word[word].add(tuple(pairings))
    false_rows = []
    for word, rows in sorted(by_word.items()):
        marginal_product = product(*(sorted({r[i] for r in rows}) for i in range(3)))
        false_rows.extend((word, *r) for r in marginal_product if r not in rows)
    assert false_rows
    fake = false_rows[0]
    individual = [second.condition(lambda b, i=i: model.view(b.coloring)[0] == fake[0]
                                   and model.view(b.coloring)[i] == fake[i]) for i in (1, 2, 3)]
    assert all(c.branches for c in individual)
    joint = second.condition(lambda b: model.view(b.coloring) == fake)
    assert not joint.branches
    collapse = second.condition(lambda b: model.view(b.coloring)[0] == fake[0])
    collapse_cards = [collapse.card()]
    for i in (1, 2, 3):
        collapse = collapse.condition(lambda b, i=i: model.view(b.coloring)[i] == fake[i])
        collapse_cards.append(collapse.card())
    assert not collapse.branches
    # Exact selectors compose on current witnesses, not old component snapshots.
    regression_path = start.condition(lambda b: b.origin == 0).switch(
        pair=(2, 3), component=(5, 6, 8, 10, 13, 14))
    assert len(regression_path.branches) == 1 and regression_path.branches[0].coloring == seeds[1]
    middle = regression_path.switch(pair=(0, 2), component=(0,))
    end = middle.switch(pair=(0, 3), component=(2,))
    assert end.branches and all(singleton_of(b.coloring) == 1 for b in end.branches)

    # Find an actual cycle-count drop among the exact reachable transitions.
    # Record a whole source history so this is a reachable structural event.
    cycle_loss = None
    for branch in second.branches:
        previous = model.apply(seeds[branch.origin], branch.history[0])
        move = branch.history[1]
        # Exclude a global color transposition, which only permutes system names.
        if set(move.component) == {v for v, color in enumerate(previous) if color in move.pair}:
            continue
        event = model.edge_replay(previous, move)
        if (model.compatible(previous) and model.compatible(branch.coloring)
                and any(s['cycle_count_after'] < s['cycle_count_before'] for s in event['systems'])):
            cycle_loss = dict(origin=branch.origin, source=previous,
                              prefix=model.edge_replay(seeds[branch.origin], branch.history[0]),
                              event=event, source_compatible=model.compatible(previous),
                              target_compatible=model.compatible(branch.coloring))
            break
    assert cycle_loss is not None

    stages = dict(start=start, one_switch=first, two_switches=second,
                  target_relation=constrained, target_coloring=one, incompatible_guard=impossible,
                  one_switch_compatible=yes, prefix_safe_two_switches=prefix_safe,
                  final_safe_two_switches=final_safe,
                  cd_middle=regression_path, ac_middle=middle, ad_end=end)
    result = dict(summary={name: c.card() for name, c in stages.items()},
                  successor_relation_differences=[len(by_origin[0] - by_origin[1]),
                                                  len(by_origin[1] - by_origin[0])],
                  target_relation=target,
                  structural_cycle_loss=cycle_loss,
                  unsafe_intermediate_paths=len(unsafe_prefix),
                  false_splice=dict(source_origin=0, substituted_origin=1, target=target,
                                    actual_matching_branches=0),
                  projection_counterexample=dict(scope='Unreachable in exactly two moves from these two seeds; not a general non-realizability claim.',
                      false_rows=len(false_rows), relation=fake,
                      individual_guard_cards=[c.card() for c in individual],
                      sequential_joint_guard_cards=collapse_cards,
                      individual_witnesses=[c.branches[0].coloring for c in individual]),
                  stages={name: c.certificate() for name, c in stages.items()})
    return result


def report():
    source = json.loads(SOURCE.read_text())
    g = next(g for g in source['graphs'] if g['name'] == 'errera-0')
    seeds = tuple(map(tuple, source['same_class_regression']['colorings']))
    model = EdgeModel(g)
    result = study(model, seeds)
    files = [SOURCE, Path(__file__), *(ROOT / 'scripts' / f for f in
             ('c5_edge_states.py', 'c5_kempe_connectivity.py', 'c5_complementary_cube.py',
              'c5_kempe_screen.py', 'c5_ab_swap_cube.py'))]
    result.update(trust='Exact fixed-disk Python witnesses and exhaustive transitions for supplied seeds and depths; not Lean or a complete relation for arbitrary disks.',
                  graph=dict(name=model.name, n=model.n, edges=model.edges, faces=model.faces),
                  seeds=seeds,
                  transition_table=model.transition_table,
                  hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files})
    model.dual.systems.cache_clear()
    return result


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
    print(json.dumps(dict(stages=result['summary'], projection=result['projection_counterexample'],
                         successor_relation_differences=result['successor_relation_differences']), indent=2))


if __name__ == '__main__':
    main()
