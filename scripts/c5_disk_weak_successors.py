#!/usr/bin/env python3
"""Exhaust all deletions of the two fixed k=3 C5 witnesses; check silent exits.

uv run --with networkx==3.5 python scripts/c5_disk_weak_successors.py [--check]
No new plantri enumeration; no k=4 search or general completion assumption.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

from c5_cell_enumerator import REPS, compat_tables
from c5_disk_deletions import CYCLE, canonical, parse_disk, relation

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'artifacts/c5_disk_deletions/observations.json'
OUT = ROOT / 'artifacts/c5_disk_weak_successors/observations.json'
WITNESSES = ('k3-t175', 'k3-t180')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def members(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def submasks(mask):
    current = mask
    while True:
        yield current
        if not current:
            break
        current = (current - 1) & mask


def certify_parent(parent, inputs):
    """Reconstruct one retained rotation system in the exact witness labels."""
    run, = [r for r in inputs['runs'] if r['k'] == parent['k']]
    path = INPUT.parent / 'plantri' / run['file']
    assert sha(path) == run['sha256']
    index, direction, shift = parent['origins'][0]
    edges, outer, rotation = parse_disk(path.read_text().splitlines()[index], parent['k'])
    order = [outer[(shift + direction * i) % 5] for i in range(5)]
    order += sorted(set(range(8)) - set(outer))
    label = {v: i for i, v in enumerate(order)}
    mapped = [(label[u], label[v]) for u, v in edges]
    assert canonical(8, mapped) == tuple(map(tuple, parent['edges']))
    return dict(source_file=str(path.relative_to(ROOT)), source_sha256=sha(path),
                source_index=index, direction=direction, shift=shift,
                rotation=rotation, outer=outer)


def lattice(parent, inputs):
    assert parent['k'] == 3
    extra = sorted(set(map(tuple, parent['edges'])) - CYCLE)
    assert len(extra) == 11
    count = 1 << len(extra)
    sigma, successors, closures, exits, traces = [], [], [], [], []
    tables, full = compat_tables(3, extra)
    strict_edges = silent_edges = 0
    for mask in range(count):
        present = list(members(mask))
        edges = tuple(sorted(CYCLE | {extra[i] for i in present}))
        actual, _ = relation(8, edges)  # Brute-force reps AND all 240 backtracking checks.
        fast = 0
        for j in range(len(REPS)):
            viable = full
            for i in present:
                viable &= tables[i][j]
            if viable:
                fast |= 1 << j
        assert actual == fast
        sigma.append(actual)
        children = [mask ^ (1 << i) for i in present]
        successors.append(children)
        closure = 1 << mask
        weak = set()
        language = {(actual,)}  # Finite observable traces, including early stopping.
        for child in children:
            assert sigma[child] & actual == actual
            if sigma[child] == actual:
                silent_edges += 1
                closure |= closures[child]
                weak |= exits[child]
                language |= traces[child]
            else:
                strict_edges += 1
                weak.add(sigma[child])
                language |= {(actual,) + tail for tail in traces[child]}
        closures.append(closure)
        exits.append(weak)
        traces.append(language)

    # Independent exhaustive submask definition of silent closure and its exits.
    # Monotonicity implies every intermediate on a path to an equal-Sigma submask
    # has that same Sigma. Conversely, silent deletion can only reach such submasks.
    for mask in range(count):
        reference = [s for s in submasks(mask) if sigma[s] == sigma[mask]]
        assert closures[mask] == sum(1 << s for s in reference)
        reference_exits = {sigma[c] for s in reference for c in successors[s]
                           if sigma[c] != sigma[mask]}
        assert exits[mask] == reference_exits
        # Recompute traces by tau* strict factoring, independently of one-edge DP.
        factored = {(sigma[mask],)}
        for s in reference:
            for child in successors[s]:
                if sigma[child] != sigma[mask]:
                    factored |= {(sigma[mask],) + tail for tail in traces[child]}
        assert traces[mask] == factored

    root = count - 1
    assert sigma[root] == parent['sigma']
    chord_index = extra.index((0, 3))
    chord_relation = sum(1 << j for j, b in enumerate(REPS) if b[0] != b[3])
    hub_relation = sum(1 << j for j, b in enumerate(REPS) if len(set(b[:4])) < 4)
    universal = (1 << len(REPS)) - 1
    # Infer the proposed support from edge sensitivity, then verify the formula
    # on ALL subsets. Sensitivity alone would not establish sufficiency.
    support = [i for i in range(11)
               if sigma[root ^ (1 << i)] & hub_relation != sigma[root ^ (1 << i)]]
    support_mask = sum(1 << i for i in support)
    assert chord_index not in support and support
    for mask in range(count):
        predicted = chord_relation if mask >> chord_index & 1 else universal
        if mask & support_mask == support_mask:
            predicted &= hub_relation
        assert sigma[mask] == predicted
    factorization = dict(chord=[0, 3], chord_relation=chord_relation,
                         high_order_relation=hub_relation,
                         high_order_predicate='boundary positions 0,1,2,3 do not use all four colors',
                         high_order_required_edges=[extra[i] for i in support],
                         globally_irrelevant_edges=[extra[i] for i in range(11)
                                                    if i not in support and i != chord_index],
                         formula='Sigma(M) = (Q if chord retained else FULL) intersect '
                                 '(H if all required edges retained else FULL)',
                         verified_subsets=count)
    root_closure = list(members(closures[root]))
    # Choose deterministic shortest deletion witnesses for each root weak exit.
    exit_witnesses = []
    for target in sorted(exits[root]):
        candidates = [(root.bit_count() - s.bit_count(), s, child)
                      for s in root_closure for child in successors[s] if sigma[child] == target]
        _, s, child = min(candidates)
        deleted = [extra[i] for i in members(root ^ s)]
        last, = list(members(s ^ child))
        exit_witnesses.append(dict(target=target, silent_deleted=deleted,
                                   strict_deleted=extra[last], before_mask=s, after_mask=child))
    groups = defaultdict(list)
    for mask, bits in enumerate(sigma):
        groups[bits].append(mask)
    summary = dict(id=parent['id'], k=3, parent_sigma=sigma[root], states=count,
                   transitions=silent_edges + strict_edges, silent_edges=silent_edges,
                   strict_edges=strict_edges, root_silent_states=len(root_closure),
                   root_silent_by_depth=dict(sorted(Counter(11-s.bit_count() for s in root_closure).items())),
                   root_weak_exits=sorted(exits[root]), reachable_relations=sorted(groups),
                   relation_state_counts={str(b): len(ms) for b, ms in sorted(groups.items())},
                   root_observable_traces=sorted(traces[root]),
                   weak_exit_variants={str(b): sorted({tuple(sorted(exits[m])) for m in ms})
                                       for b, ms in sorted(groups.items())})
    return dict(summary=summary, factorization=factorization, geometry=certify_parent(parent, inputs),
                extra_edges=extra, root_mask=root, root_silent_masks=root_closure,
                root_exit_witnesses=exit_witnesses,
                encoding='mask bit i means extra_edges[i] is retained; all five C5 edges always retained',
                sigma_by_mask=sigma,
                weak_exits_by_mask=[sorted(e) for e in exits],
                observable_traces_by_sigma={str(b): sorted({tuple(sorted(traces[m])) for m in ms})
                                            for b, ms in sorted(groups.items())})


def build():
    source = json.loads(INPUT.read_text())
    rows = [next(r for r in source['parents'] if r['id'] == name) for name in WITNESSES]
    runs = [lattice(row, source['inputs']) for row in rows]
    by_sigma = defaultdict(set)
    for run in runs:
        for bits, weak in zip(run['sigma_by_mask'], run['weak_exits_by_mask']):
            by_sigma[bits].add(tuple(weak))
    # A finite certificate that equality of Sigma is a weak bisimulation:
    # a tau edge is matched by zero steps; any strict step to Sigma=s can be
    # matched from every equal-Sigma state by tau* followed by a strict step to s.
    uniform = all(len(variants) == 1 for variants in by_sigma.values())
    assert uniform, 'Sigma fails weak bisimulation on these lattices; inspect variants'
    quotient = {str(bits): list(next(iter(variants))) for bits, variants in sorted(by_sigma.items())}
    left, right = [r['summary'] for r in runs]
    assert left['root_observable_traces'] == right['root_observable_traces']
    return dict(schema=1,
                scope='all subsets of the 11 nonboundary edges of each of TWO fixed k=3 witnesses; vertices retained',
                semantics=dict(silent='single-edge deletion preserving Sigma',
                               visible='single-edge deletion strictly enlarging Sigma; action label is target Sigma',
                               weak_exit='zero or more silent steps, then one visible step',
                               trace='finite Sigma sequence after collapsing adjacent repeats; all stopping prefixes',
                               equivalence='divergence-insensitive weak bisimulation; edge identities and step counts hidden'),
                inputs={str(INPUT.relative_to(ROOT)): sha(INPUT)},
                source_sha256={str(p.relative_to(ROOT)): sha(p) for p in [Path(__file__).resolve(),
                    ROOT / 'scripts/c5_disk_deletions.py', ROOT / 'scripts/c5_cell_enumerator.py',
                    ROOT / 'scripts/local_closure.py', ROOT / 'scripts/boundary_relations.py']},
                pattern_order=REPS, runs=runs,
                conclusion=dict(equal_root_weak_exits=left['root_weak_exits'] == right['root_weak_exits'],
                                equal_root_catalogues=left['reachable_relations'] == right['reachable_relations'],
                                equal_all_finite_root_observable_traces=True,
                                sigma_is_weak_bisimulation_on_union=uniform, weak_quotient=quotient),
                verification=dict(lattice_states=sum(r['summary']['states'] for r in runs),
                                  transitions=sum(r['summary']['transitions'] for r in runs),
                                  unique_labelled_graphs=relation.cache_info().currsize,
                                  boundary_backtracking_queries=240*relation.cache_info().currsize))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=1) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'artifact differs; rebuild explicitly'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(dict(summaries=[r['summary'] for r in result['runs']],
                          conclusion=result['conclusion'], verification=result['verification']), indent=2))


if __name__ == '__main__':
    main()
