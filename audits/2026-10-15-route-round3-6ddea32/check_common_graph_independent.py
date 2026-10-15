#!/usr/bin/env python3
"""Independent fixed-order search of canonical-state vertex colour functions."""
import argparse
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE = ROOT / 'audits/2026-10-15-kempe-compatibility-6ddea32/certificate.json'


def canonical(text):
    order = list(dict.fromkeys(text))
    order += [c for c in 'ABCD' if c not in order]
    return ''.join('ABCD'[order.index(c)] for c in text), tuple('ABCD'.index(c) for c in order)


def check():
    states = [s for s in json.loads(SOURCE.read_text())['states'] if s['layer'] == 0]
    by_id = {s['id']: s for s in states}
    representatives = sorted({canonical(s['literal_row'])[0] for s in states})
    index = {s: i for i, s in enumerate(representatives)}
    maps = {s['id']: (index[canonical(s['literal_row'])[0]], canonical(s['literal_row'])[1]) for s in states}
    # Only canonical source states are used to derive constraints. Every complete
    # candidate is then checked against every literal transition independently.
    constraints = []
    for state in states:
        name, perm = canonical(state['literal_row'])
        if state['literal_row'] != name:
            continue
        u = index[name]
        for pairing in state['pairings']:
            bit = 0
            for pair, blocks in zip(pairing['pairing'], pairing['terminal_parts']):
                for _ in blocks:
                    v, image = maps[pairing['cube_targets_by_bitmask'][1 << bit]]
                    allowed = {(a, b) for a in range(4) for b in range(4)
                               if image[b] == a or (a in pair and image[b] == sum(pair) - a)}
                    constraints.append((u, v, allowed))
                    bit += 1
    nodes = 0
    solutions = []

    def search(prefix, domains):
        nonlocal nodes
        nodes += 1
        if len(prefix) == len(representatives):
            solutions.append(tuple(prefix))
            return
        position = len(prefix)
        for value in sorted(domains[position]):
            child = [set(d) for d in domains]
            child[position] = {value}
            okay = True
            for u, v, allowed in constraints:
                if max(u, v) <= position:
                    if not any((a, b) in allowed and (u != v or a == b)
                               for a in child[u] for b in child[v]):
                        okay = False
                        break
                elif u <= position:
                    child[v] = {b for b in child[v] if any((a, b) in allowed for a in child[u])}
                    okay &= bool(child[v])
                elif v <= position:
                    child[u] = {a for a in child[u] if any((a, b) in allowed for b in child[v])}
                    okay &= bool(child[u])
                if not okay:
                    break
            if okay:
                search(prefix + [value], child)

    search([], [set(range(4)) for _ in representatives])
    assert len(solutions) == 25
    functions = [[perm[f[u]] for state in states for u, perm in [maps[state['id']]]]
                 for f in solutions]
    positions = {s['id']: i for i, s in enumerate(states)}
    transition_checks = 0
    for function in functions:
        for i, state in enumerate(states):
            for pairing in state['pairings']:
                bit = 0
                for pair, blocks in zip(pairing['pairing'], pairing['terminal_parts']):
                    for _ in blocks:
                        value = function[i]
                        target = function[positions[pairing['cube_targets_by_bitmask'][1 << bit]]]
                        assert target == value or (value in pair and target == sum(pair) - value)
                        transition_checks += 1
                        bit += 1
    edges = [(u, v) for u, v in combinations(range(25), 2)
             if all(a != b for a, b in zip(functions[u], functions[v]))]
    pins = [functions.index(['ABCD'.index(s['literal_row'][pin]) for s in states]) for pin in range(7)]
    first = by_id[0]
    assert first['literal_row'] == 'ABABCBC'
    assert [4, 6] in first['pairings'][0]['terminal_parts'][1]
    eligible = {u for u, f in enumerate(functions) if f[positions[0]] in (2, 3)}
    seen = {pins[4]}
    todo = list(seen)
    while todo:
        u = todo.pop()
        for a, b in edges:
            v = b if a == u else a if b == u else None
            if v in eligible and v not in seen:
                seen.add(v)
                todo.append(v)
    assert pins[6] not in seen
    return {'status': 'PASS', 'states': len(states), 'canonical_rows': representatives,
            'search_nodes': nodes, 'weak_functions': solutions,
            'all_literal_transition_checks': transition_checks,
            'maximal_edges': edges, 'pin_function_ids': pins,
            'obstruction': {'state': 0, 'pair': [2, 3], 'required_block': [4, 6],
                            't_component': sorted(seen), 'q_id': pins[6]},
            'scope': 'Exact single-valued S4-equivariant state lift only; refined state covers remain open.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', type=Path)
    group.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = check()
    if args.write:
        with args.write.open('x') as stream:
            json.dump(result, stream, indent=2)
            stream.write('\n')
    else:
        assert json.loads(args.check.read_text()) == json.loads(json.dumps(result)), 'certificate mismatch'
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ('weak_functions', 'maximal_edges', 'canonical_rows')}))


if __name__ == '__main__':
    main()
