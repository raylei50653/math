#!/usr/bin/env python3
"""Bounded candidate-rule tests on the existing 87-state weak quotient only.

python scripts/c5_weak_candidates.py [--check]
No graph search, no deletion replay, no k=4 data, no theorem prover.
"""
import argparse
from functools import reduce
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'artifacts/c5_weak_quotient/observations.json'
OUT = ROOT / 'artifacts/c5_weak_candidates/observations.json'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def build():
    quotient = json.loads(INPUT.read_text())
    for name, expected in (quotient['inputs'] | quotient['source_sha256']).items():
        assert digest(ROOT / name) == expected, name
    patterns = quotient['pattern_order']
    omega = (1 << len(patterns)) - 1
    t4 = sum(1 << i for i, p in enumerate(patterns) if len(set(p)) == 4)
    t3 = omega ^ t4
    weak = {n['sigma']: set(n['weak_exits']) for n in quotient['nodes']}
    nodes = sorted(weak)
    edges = {(s, t) for s in nodes for t in weak[s]}
    upper = {s: {t for t in nodes if t != s and s & t == s} for s in nodes}
    rank = lambda s: (s.bit_count(), s)
    chords = [(a, b) for a in range(5) for b in range(a+1, 5)
              if (a-b) % 5 not in (1, 4)]
    equality_pairs = [{e for e in chords if p[e[0]] == p[e[1]]} for p in patterns]
    singleton_pattern = {next(i for i, c in enumerate(p) if p.count(c) == 1): j
                         for j, p in enumerate(patterns) if len(set(p)) == 3}
    adjacent_pair_rows = []
    for i in range(5):
        j = (i + 1) % 5
        a, b = 1 << singleton_pattern[i], 1 << singleton_pattern[j]
        s = omega ^ a ^ b
        predicted = {omega ^ a, omega ^ b, omega}
        assert s in weak
        adjacent_pair_rows.append(dict(boundary_singletons=[i, j], sigma=s,
                                       actual=sorted(weak[s]), predicted=sorted(predicted),
                                       extra=sorted(weak[s] - predicted), missing=sorted(predicted - weak[s])))

    # Intrinsic family: no weak-exit values are used to construct these masks.
    # A: forbid one three-color orbit.
    # B: forbid one four-color orbit q, plus any subset of the two
    #    three-color orbits satisfying q's unique diagonal equality.
    # C: forbid exactly the two four-color orbits using all four colors
    #    on a fixed four-vertex boundary subset.
    atomic = {}
    for i, p in enumerate(patterns):
        if len(set(p)) == 3:
            atomic.setdefault(omega ^ (1 << i), []).append(dict(kind='A', pattern=i))
        else:
            refinements = [j for j in range(10) if t3 >> j & 1
                           and equality_pairs[i] <= equality_pairs[j]]
            assert len(refinements) == 2
            for sub in range(4):
                forbidden = (1 << i) | sum(1 << j for b, j in enumerate(refinements) if sub >> b & 1)
                atomic.setdefault(omega ^ forbidden, []).append(
                    dict(kind='B', pattern=i, forbidden_three=[j for b, j in enumerate(refinements) if sub >> b & 1]))
    for omitted in range(5):
        indices = [j for j, p in enumerate(patterns)
                   if len({p[i] for i in range(5) if i != omitted}) == 4]
        assert len(indices) == 2 and all(t4 >> j & 1 for j in indices)
        atomic.setdefault(omega ^ sum(1 << j for j in indices), []).append(
            dict(kind='C', omitted_boundary_vertex=omitted, forbidden_four=indices))
    assert len(atomic) == 30 and set(atomic) <= set(nodes)

    complete_rows, union_rows, intersection_rows, atomic_rows = [], [], [], []
    for s in nodes:
        if s & t4 == t4:
            complete_rows.append(dict(sigma=s, actual=sorted(weak[s]), predicted=sorted(upper[s]),
                                      extra=sorted(weak[s] - upper[s]), missing=sorted(upper[s] - weak[s])))
        if s != omega:
            union_rows.append(dict(sigma=s, union=reduce(int.__or__, weak[s], 0), predicted=omega))
        if len(weak[s]) >= 2:
            intersection_rows.append(dict(sigma=s, intersection=reduce(int.__and__, weak[s], omega), predicted=s))
        atomic_rows.append(dict(sigma=s, intrinsic_member=s in atomic,
                                terminal_exit=weak[s] == {omega}, constructions=atomic.get(s, [])))

    audit_path = ROOT / 'artifacts/c5_weak_deletion_audit/observations.json'
    assert str(audit_path.relative_to(ROOT)) in quotient['inputs']
    audit = json.loads(audit_path.read_text())
    by_k = []
    for k in range(4):
        observed = {int(s) for s, entries in audit['sigma_variants'].items()
                    if any(int(i) <= k and count for i, count in entries[0]['by_k'].items())}
        comparisons = [dict(sigma=s, actual=sorted(weak[s]),
                            predicted=sorted(t for t in observed if t != s and s & t == s))
                       for s in sorted(observed) if s & t4 == t4]
        by_k.append(dict(k=k, observed_relations=len(observed), comparisons=comparisons,
                         failures=sum(r['actual'] != r['predicted'] for r in comparisons)))

    # These rules do not identify the whole quotient: add an inclusion edge
    # and its D5 orbit at sources outside the exact-rule subclasses.
    extra_orbit = sorted({(dict(a['node_map'])[165], dict(a['node_map'])[167])
                          for a in quotient['d5']['actions']})
    assert not (set(extra_orbit) & edges)
    alternative = {s: set(weak[s]) for s in nodes}
    for s, t in extra_orbit:
        assert t in upper[s]
        alternative[s].add(t)
    for s in nodes:
        if s & t4 == t4:
            assert alternative[s] == upper[s]
        assert (alternative[s] == {omega}) == (s in atomic)
        if s != omega:
            assert reduce(int.__or__, alternative[s], 0) == omega
        if len(alternative[s]) >= 2:
            assert reduce(int.__and__, alternative[s], omega) == s
    for action in quotient['d5']['actions']:
        act = dict(action['node_map'])
        assert all(alternative[act[s]] == {act[t] for t in alternative[s]} for s in nodes)

    # Negative controls: deliberately stronger or less structured hypotheses.
    # These must not be promoted to conjectures after they fail on the same data.
    controls = {}
    for name, sources in [('unrestricted_upper_cone', nodes),
                          ('all_three_color_patterns_upper_cone', [s for s in nodes if s & t3 == t3])]:
        mismatches = [dict(sigma=s, extra=sorted(weak[s] - upper[s]), missing=sorted(upper[s] - weak[s]))
                      for s in sources if weak[s] != upper[s]]
        controls[name] = dict(tested=len(sources), failures=len(mismatches), mismatches=mismatches,
                              smallest=min(mismatches, key=lambda r: rank(r['sigma']), default=None))
    pair_failures = []
    for s in sorted(nodes, key=rank):
        if len(weak[s]) < 2:
            continue
        absent = [i for i in range(10) if not s >> i & 1]
        for a in absent:
            for b in absent:
                if a != b and not any(t >> a & 1 and not t >> b & 1 for t in weak[s]):
                    pair_failures.append(dict(sigma=s, release_pattern=a, keep_forbidden_pattern=b,
                                              weak_exits=sorted(weak[s])))
    controls['independent_pair_release'] = dict(failures=len(pair_failures), witnesses=pair_failures,
                                               smallest=pair_failures[0] if pair_failures else None)
    differences = {s ^ t for s, t in edges}
    delta_edges = {(s, t) for s in nodes for t in upper[s] if s ^ t in differences}
    controls['global_release_mask_dictionary'] = dict(
        release_masks=sorted(differences), extra_edges=sorted(delta_edges - edges),
        missing_edges=sorted(edges - delta_edges))

    # Show why the two envelope laws are not consequences of monotonicity
    # or a well-defined quotient, using abstract relation-labelled DAGs.
    abstract = [dict(name='union_failure', omega=7, weak={'1': [3], '3': [7], '7': []}),
                dict(name='branch_intersection_failure', omega=15,
                     weak={'1': [7, 11], '7': [15], '11': [15], '15': []})]
    for example in abstract:
        graph = {int(s): ts for s, ts in example['weak'].items()}
        assert all(s != t and s & t == s for s, ts in graph.items() for t in ts)
    assert reduce(int.__or__, abstract[0]['weak']['1'], 0) != abstract[0]['omega']
    assert reduce(int.__and__, abstract[1]['weak']['1'], 15) != 1

    summary = dict(
        nodes=len(nodes), edges=len(edges),
        adjacent_pair_sources=len(adjacent_pair_rows),
        adjacent_pair_failures=sum(bool(r['extra'] or r['missing']) for r in adjacent_pair_rows),
        T4_upper_cone_sources=len(complete_rows), T4_upper_cone_edges=sum(len(r['actual']) for r in complete_rows),
        T4_upper_cone_failures=sum(bool(r['extra'] or r['missing']) for r in complete_rows),
        union_sources=len(union_rows), union_failures=sum(r['union'] != r['predicted'] for r in union_rows),
        branching_sources=len(intersection_rows),
        branching_intersection_failures=sum(r['intersection'] != r['predicted'] for r in intersection_rows),
        intrinsic_atomic_relations=len(atomic),
        atomic_characterization_failures=sum(r['intrinsic_member'] != r['terminal_exit'] for r in atomic_rows),
        all_three_upper_cone_failures=controls['all_three_color_patterns_upper_cone']['failures'],
        independent_pair_release_failures=len(pair_failures),
        release_dictionary_extra_edges=len(delta_edges - edges))
    return dict(schema=1, scope='Candidate rules tested only on the sealed 87-state quotient; no general theorem.',
                inputs={str(INPUT.relative_to(ROOT)): digest(INPUT)},
                source_sha256={str(Path(__file__).resolve().relative_to(ROOT)): digest(Path(__file__))},
                pattern_order=patterns, T3=t3, T4=t4, Omega=omega,
                candidates=dict(adjacent_singleton_pair=adjacent_pair_rows,
                                T4_upper_cone=complete_rows, union_envelope=union_rows,
                                branching_intersection=intersection_rows, atomic_characterization=atomic_rows,
                                T4_upper_cone_by_k=by_k),
                nonuniqueness_witness=dict(added_edges=extra_orbit, alternative_edge_count=sum(map(len, alternative.values())),
                                          note='Abstract relation DAG only; satisfies all candidate rules and D5 but is not the observed quotient or a claimed graph realization.'),
                negative_controls=controls, abstract_countermodels=abstract, summary=summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'artifact differs; rebuild explicitly'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
