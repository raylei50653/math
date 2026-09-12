#!/usr/bin/env python3
"""Validate same-C5 forcing against complete 240-colouring semantics.

Exhaust all 3^5 conjunctions on C5 diagonals (absent/EQ/NEQ) for all 87
library relations and all ten distinct pairs. Edge-EQ guards are separately
checked infeasible; edge-NEQ is redundant. Verify minimal extra implications,
source hashes, aligned meet, counterexample witnesses, and the actual
inside/outside graph by independent full-colouring backtracking.

uv run --with networkx==3.5 python scripts/check_c5_relation_library.py
"""
import hashlib
import itertools as it
import json
from pathlib import Path
import time

import networkx as nx
from boundary_relations import Literal, Relation

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/boundary_relations'


def canonical(b):
    return tuple(sorted(set(b), key=b.index).index(c) for c in b)


def main():
    catalog = json.loads((OUT / 'library.json').read_text())
    for name, digest in catalog['source_sha256'].items():
        assert hashlib.sha256((ROOT / 'artifacts/fan_pentagon' / name).read_bytes()).hexdigest() == digest
    source = json.loads((ROOT / 'artifacts/fan_pentagon/states.json').read_text())
    assert catalog['distinct_relations'] == len(catalog['entries']) == 87
    assert {e['id'] for e in catalog['entries']} == {r['sigma_bits'] for r in source['states']}
    ports = tuple(f'b{i}' for i in range(5))
    all_colors = [b for b in it.product(range(4), repeat=5) if all(b[i] != b[(i + 1) % 5] for i in range(5))]
    reps = sorted({canonical(b) for b in all_colors})
    assert catalog['pattern_order'] == [list(b) for b in reps]
    pairs = list(it.combinations(range(5), 2))
    diagonals = [p for p in pairs if p[1] - p[0] not in (1, 4)]
    guard_values = list(it.product((None, False, True), repeat=5))

    def selected(rows, values):
        return [b for b in rows if all(eq is None or (b[i] == b[j]) == eq
                                      for (i, j), eq in zip(diagonals, values))]

    def status(rows, i, j):
        outcomes = {b[i] == b[j] for b in rows}
        return ('infeasible' if not outcomes else 'free' if len(outcomes) == 2
                else 'forced_equal' if True in outcomes else 'forced_different')

    base_status = {values: {p: status(selected(all_colors, values), *p) for p in pairs}
                   for values in guard_values}
    relations, table = {}, {}
    queries = 0
    started = time.monotonic()
    for idx, entry in enumerate(catalog['entries'], 1):
        bits = entry['id']
        patterns = [p for j, p in enumerate(reps) if bits >> j & 1]
        rel = Relation.of(ports, patterns)
        relations[bits] = rel
        assert entry['relation']['patterns'] == [list(p) for p in patterns]
        assert entry['relation']['ports'] == list(ports)
        full = [b for b in all_colors if canonical(b) in rel.patterns]
        states = {}
        for values in guard_values:
            guards = [Literal(ports[i], ports[j], eq) for (i, j), eq in zip(diagonals, values) if eq is not None]
            retained = selected(full, values)
            states[values] = {}
            for i, j in pairs:
                result = rel.query(ports[i], ports[j], guards)
                answer = status(retained, i, j)
                states[values][i, j] = answer
                assert result['status'] == answer, (bits, values, i, j)
                assert result['surviving_orbits'] == len({canonical(b) for b in retained})
                raw_pair = {(b[i], b[j]) for b in retained}
                assert set(map(tuple, result['pair_projection'])) == {canonical(p) for p in raw_pair}
                for key, eq in (('equal_witness', True), ('different_witness', False)):
                    w = result[key]
                    assert (w is not None) == any((b[i] == b[j]) == eq for b in retained)
                    if w is not None:
                        assert tuple(w) in retained and (w[i] == w[j]) == eq
                queries += 1
                if all(v is None for v in values):
                    assert entry['unconditional']['pairs'][f'b{i},b{j}'] == json.loads(json.dumps(result))
        table[bits] = states
        # Exhaustive minimal live implications beyond the bare C5 constraints.
        expected_clauses = set()
        for values in guard_values:
            for t, (i, j) in enumerate(diagonals):
                answer = states[values][i, j]
                if values[t] is not None or not answer.startswith('forced_') or base_status[values][i, j] == answer:
                    continue
                reduced = [values[:k] + (None,) + values[k + 1:] for k, v in enumerate(values) if v is not None]
                if any(states[v][i, j] == answer for v in reduced):
                    continue
                given = tuple(f'b{a}{"=" if eq else "!="}b{b}'
                              for (a, b), eq in zip(diagonals, values) if eq is not None)
                expected_clauses.add((given, f'b{i}{"=" if answer == "forced_equal" else "!="}b{j}'))
        actual_clauses = {(tuple(c['given']), c['forces']) for c in entry['extra_forcings']}
        assert len(actual_clauses) == len(entry['extra_forcings']) and actual_clauses == expected_clauses
        for clause in entry['extra_forcings']:
            def parse(text):
                eq = '!=' not in text
                a, b = text.split('=' if eq else '!=')
                return Literal(a, b, eq)
            guards = [parse(text) for text in clause['given']]
            conclusion = parse(clause['forces'])
            result = rel.query(conclusion.left, conclusion.right, guards)
            assert clause['surviving_orbits'] == result['surviving_orbits']
            assert tuple(clause['witness']) in rel.condition(guards).patterns
            w = clause['witness']
            assert (w[ports.index(conclusion.left)] == w[ports.index(conclusion.right)]) == conclusion.equal
        for i in range(5):
            assert rel.query('b0', 'b2', [Literal(ports[i], ports[(i + 1) % 5])])['status'] == 'infeasible'
            assert rel.condition([Literal(ports[i], ports[(i + 1) % 5], False)]) == rel
        if idx % 20 == 0:
            print(f'{idx}/87 relations checked, {time.monotonic()-started:.1f}s', flush=True)

    # Exact counterexample to replacing full relations by their marginals.
    assert relations[767] != relations[1023]
    assert all(relations[767].query(ports[i], ports[j])['pair_projection'] ==
               relations[1023].query(ports[i], ports[j])['pair_projection'] for i, j in pairs)
    guards = [Literal('b1', 'b4'), Literal('b0', 'b2', False)]
    assert relations[767].query('b0', 'b3', guards)['status'] == 'forced_equal'
    assert relations[1023].query('b0', 'b3', guards)['status'] == 'free'
    # Verify aligned intersection for every pair of library entries, including
    # reordered storage of ports. No independent boundary symmetry quotient.
    for a, b in it.combinations_with_replacement(sorted(relations), 2):
        left, right = relations[a], relations[b]
        result = left.meet(right.reorder(tuple(reversed(ports))))
        assert result.patterns == frozenset(p for j, p in enumerate(reps) if (a & b) >> j & 1)
    # A nontrivial relabeling is explicit and can change the complete relation.
    shift = {ports[i]: ports[(i + 1) % 5] for i in range(5)}
    assert relations[767].rename(shift).reorder(ports) != relations[767]
    for rel in relations.values():
        for i, j in pairs:
            assert sorted(rel.project((ports[i], ports[j])).patterns) == rel.query(ports[i], ports[j])['pair_projection']

    example = json.loads((OUT / 'inside_outside.json').read_text())
    graph = nx.Graph()
    graph.add_nodes_from(range(15))
    graph.add_edges_from(example['graph_edges'])
    assert nx.check_planarity(graph)[0]
    emb = nx.PlanarEmbedding()
    emb.set_data({int(v): ns for v, ns in example['planar_rotation'].items()})
    emb.check_structure()
    assert set(emb.nodes) == set(graph.nodes)
    assert {frozenset(e) for e in emb.edges} == {frozenset(e) for e in graph.edges}
    apex = graph.copy()
    apex.add_edges_from((15, i) for i in range(5))
    assert nx.check_planarity(apex)[0] == example['outer_C5_cofacial'] is False
    expected_edges = set()
    for bits, offset in ((91, 0), (935, 5)):
        witness = next(r for r in source['states'] if r['sigma_bits'] == bits)
        expected_edges.update(tuple(sorted((u if u < 5 else u + offset,
                                           v if v < 5 else v + offset))) for u, v in witness['edges'])
    assert set(map(tuple, example['graph_edges'])) == expected_edges
    order = sorted(range(5, 15), key=lambda v: (-graph.degree[v], v))

    def extends(b):
        colours = dict(enumerate(b))
        def search(at):
            if at == len(order):
                return True
            v = order[at]
            forbidden = {colours[u] for u in graph[v] if u in colours}
            for c in range(4):
                if c in forbidden:
                    continue
                colours[v] = c
                if search(at + 1):
                    return True
            colours.pop(v, None)
            return False
        return search(0)

    accepted = [b for b in all_colors if extends(b)]
    assert {canonical(b) for b in accepted} == relations[91].meet(relations[935]).patterns
    assert len(accepted) == 48 and all(b[0] == b[2] for b in accepted)
    report = dict(status='PASS; same ordered C5 only', relations=87,
                  diagonal_guards_per_relation=243, pair_queries=queries,
                  aligned_meets=87 * 88 // 2, exact_inside_outside_colourings=len(accepted),
                  pairwise_information_loss_witness=[767, 1023],
                  source_sha256={name: hashlib.sha256((OUT / name).read_bytes()).hexdigest()
                                 for name in ('library.json', 'inside_outside.json')})
    (OUT / 'replay.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
