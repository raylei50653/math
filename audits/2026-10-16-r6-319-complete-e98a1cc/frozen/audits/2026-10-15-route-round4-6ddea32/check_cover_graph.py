#!/usr/bin/env python3
"""Independent original-edge check of the fixed Layer0 two-sheet graph."""
import argparse
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def canonical(word):
    symbols = list(dict.fromkeys(word))
    symbols += [c for c in 'ABCD' if c not in symbols]
    return ''.join('ABCD'[symbols.index(c)] for c in word), tuple('ABCD'.index(c) for c in symbols)


def check():
    records = json.loads((HERE / 'COVER_INPUTS.json').read_text())['inputs']
    inputs = []
    for row in records:
        for path in (ROOT / row['path'], HERE / 'frozen' / row['path']):
            assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256'], str(path)
        inputs.append(json.loads((HERE / 'frozen' / row['path']).read_text()))
    graph, base = inputs
    states = [s for s in base['states'] if s['layer'] == 0]
    rows = sorted({canonical(s['literal_row'])[0] for s in states})
    functions, edges, pins = graph['functions'], graph['edges'], graph['pins']
    n = len(functions)
    assert len(set(pins)) == 7
    assert len(set(map(tuple, functions))) == n
    assert len(edges) == len(set(map(tuple, edges)))
    adjacent = [set() for _ in range(n)]
    for a, b in edges:
        assert 0 <= a < b < n
        adjacent[a].add(b)
        adjacent[b].add(a)
    selected = {}
    for state in states:
        canon, frame = canonical(state['literal_row'])
        index = rows.index(canon)
        for sheet in (0, 1):
            colouring = tuple(frame[f[2 * index + sheet]] for f in functions)
            assert colouring not in selected
            assert ''.join('ABCD'[colouring[p]] for p in pins) == state['literal_row']
            assert all(colouring[a] != colouring[b] for a, b in edges)
            selected[colouring] = (state['id'], sheet)
    assert len(selected) == 864
    byid = {s['id']: s for s in states}

    # Assign one vertex at a time, with no domain propagation or imported code.
    anchor = [pins[i] for i in (0, 5, 6)]
    assert all(b in adjacent[a] for a, b in combinations(anchor, 2))
    partial = [-1] * n
    for v, c in zip(anchor, range(3)):
        partial[v] = c
    solutions, nodes = [], 0

    def search(remaining):
        nonlocal nodes
        nodes += 1
        if not remaining:
            solutions.append(tuple(partial))
            return
        candidates = []
        for v in remaining:
            used = {partial[u] for u in adjacent[v] if partial[u] >= 0}
            if len(used) == 4:
                return
            candidates.append((len(used), len(adjacent[v]), -v, v, used))
        _, _, _, v, used = max(candidates)
        for c in range(4):
            if c not in used:
                partial[v] = c
                search(remaining - {v})
        partial[v] = -1

    search(set(range(n)) - set(anchor))
    normalized = {c for c in selected if tuple(c[v] for v in anchor) == (0, 1, 2)}
    assert set(solutions) == normalized
    expanded = {tuple(p[c] for c in row) for row in solutions for p in permutations(range(4))}
    assert expanded == set(selected)
    component_checks = switch_checks = cube_checks = 0
    for colouring, (sid, sheet) in selected.items():
        state = byid[sid]
        for pairing in state['pairings']:
            ordered_components = []
            for pair, blocks in zip(pairing['pairing'], pairing['terminal_parts']):
                unseen = {v for v, c in enumerate(colouring) if c in pair}
                components = {}
                while unseen:
                    start = min(unseen)
                    reached, todo = {start}, [start]
                    unseen.remove(start)
                    while todo:
                        v = todo.pop()
                        for w in adjacent[v] & unseen:
                            unseen.remove(w)
                            reached.add(w)
                            todo.append(w)
                    hit = tuple(i for i, pin in enumerate(pins) if pin in reached)
                    assert hit and hit not in components, 'hidden or duplicated pin component'
                    components[hit] = reached
                assert set(components) == set(map(tuple, blocks))
                component_checks += len(components)
                ordered_components.extend((pair, components[tuple(block)]) for block in blocks)
            for mask, expected in enumerate(pairing['cube_targets_by_bitmask']):
                target = list(colouring)
                for bit, (pair, component) in enumerate(ordered_components):
                    if mask & (1 << bit):
                        for v in component:
                            target[v] = pair[0] + pair[1] - target[v]
                assert tuple(target) in selected
                assert selected[tuple(target)][0] == expected
                cube_checks += 1
                switch_checks += bool(mask and mask & (mask - 1) == 0)
    return {'status': 'PASS', 'scope': 'Complete original-edge Layer0 graph; no planar or full720 claim.',
            'vertices': n, 'edges': len(edges), 'pins': pins, 'distinct_named_pins': 7,
            'base_states': len(states), 'sheets_per_state': 2, 'full_colourings': len(expanded),
            'normalized_colourings': [list(c) for c in sorted(solutions)],
            'dsatur_nodes': nodes, 'component_checks': component_checks,
            'single_component_switch_checks': switch_checks, 'whole_cube_checks': cube_checks,
            'hidden_components': 0, 'nonplanarity': {'edges': len(edges), 'planar_upper_bound': 3 * n - 6},
            'inputs': records}


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
        assert json.loads(args.check.read_text()) == result, 'independent certificate mismatch'
    print(json.dumps({k: v for k, v in result.items() if k not in ('normalized_colourings', 'inputs')}))


if __name__ == '__main__':
    main()
