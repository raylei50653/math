#!/usr/bin/env python3
"""Independent original-edge replay of the 75-vertex two-sheet graph."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
GRAPH = REPO / 'audits/2026-10-15-kempe-state-covers-6ddea32/probe-realization-101.json'
SOURCE = REPO / 'audits/2026-10-15-kempe-compatibility-6ddea32/certificate.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    graph = json.loads(GRAPH.read_text())
    n, edges, pins = len(graph['functions']), graph['edges'], graph['pins']
    assert n == 75 and len(edges) == 353 and len(set(pins)) == 7
    adj = [set() for _ in range(n)]
    for a, b in edges:
        assert a != b
        adj[a].add(b)
        adj[b].add(a)
    fixed = {pins[0]: 0, pins[5]: 1, pins[6]: 2}
    for a, b in itertools.combinations(fixed, 2):
        assert b in adj[a]
    found, current = [], dict(fixed)
    nodes = 0

    def visit():
        nonlocal nodes
        nodes += 1
        if len(current) == n:
            found.append(tuple(current[i] for i in range(n)))
            return
        candidates = []
        for v in range(n):
            if v not in current:
                available = set(range(4)) - {current[w] for w in adj[v] if w in current}
                if not available:
                    return
                candidates.append((len(available), -len(adj[v]), v, sorted(available)))
        _, _, v, available = min(candidates)
        for colour in available:
            current[v] = colour
            visit()
            del current[v]
    visit()
    assert len(found) == 36
    permutations = list(itertools.permutations(range(4)))
    all_rows = {tuple(p[c] for c in row) for row in found for p in permutations}
    columns = [tuple(f[i] for f in graph['functions']) for i in range(36)]
    selected = {tuple(p[c] for c in row) for row in columns for p in permutations}
    assert all_rows == selected and len(all_rows) == 864
    assert all(all(row[a] != row[b] for a, b in edges) for row in all_rows)
    old = json.loads(SOURCE.read_text())
    states = {s['id']: s for s in old['states'] if s['layer'] == 0}
    literal = {tuple('ABCD'.index(c) for c in s['literal_row']): s for s in states.values()}
    assert len(literal) == len(states) == 432
    fibres = {}
    for row in all_rows:
        pinrow = tuple(row[p] for p in pins)
        assert pinrow in literal
        fibres.setdefault(pinrow, []).append(row)
    assert all(len(rows) == 2 for rows in fibres.values())
    switches = cubes = hidden = 0
    canonical_full = {row: i for i, row in enumerate(columns)}
    assert len(canonical_full) == 36
    equations = set()

    def normalise(row):
        order = list(dict.fromkeys(row[p] for p in pins))
        order += [c for c in range(4) if c not in order]
        return tuple(order.index(c) for c in row)

    for row in sorted(all_rows):
        state = literal[tuple(row[p] for p in pins)]
        actual = {}
        for pair in itertools.combinations(range(4), 2):
            active = {v for v in range(n) if row[v] in pair}
            while active:
                component, todo = set(), [min(active)]
                while todo:
                    v = todo.pop()
                    if v in component:
                        continue
                    component.add(v)
                    todo.extend(adj[v] & active - component)
                active -= component
                block = tuple(i for i, p in enumerate(pins) if p in component)
                hidden += not block
                assert block
                actual[(pair, block)] = component
        for part in state['pairings']:
            bits = [(tuple(pair), tuple(block)) for pair, blocks in zip(part['pairing'], part['terminal_parts']) for block in blocks]
            assert set(bits) == {key for key in actual if list(key[0]) in part['pairing']}
            for mask, target in enumerate(part['cube_targets_by_bitmask']):
                changed = list(row)
                for bit, key in enumerate(bits):
                    if mask >> bit & 1:
                        for v in actual[key]:
                            changed[v] = sum(key[0]) - changed[v]
                changed = tuple(changed)
                assert changed in all_rows
                assert tuple(changed[p] for p in pins) == tuple('ABCD'.index(c) for c in states[target]['literal_row'])
                cubes += 1
                if mask.bit_count() == 1:
                    switches += 1
                    if row in canonical_full:
                        source_i = canonical_full[row]
                        target_i = canonical_full[normalise(changed)]
                        equations.add((source_i // 2, target_i // 2, (source_i ^ target_i) & 1))
    assert hidden == 0 and switches == 8160 and cubes == 26112
    # An equivariant section chooses one sheet at each free canonical orbit.
    # The actual switches impose x_u XOR x_v=b; test the complete equation set.
    eq_adj = [[] for _ in range(18)]
    for u, v, b in sorted(equations):
        eq_adj[u].append((v, b))
        eq_adj[v].append((u, b))
    values, conflict = {}, None
    for seed in range(18):
        if seed in values:
            continue
        values[seed] = 0
        queue = [seed]
        while queue:
            u = queue.pop()
            for v, b in eq_adj[u]:
                if v not in values:
                    values[v] = values[u] ^ b
                    queue.append(v)
                elif values[v] != values[u] ^ b:
                    conflict = [u, v, b, values[u], values[v]]
    assert conflict is not None
    return {'graph_path': str(GRAPH.relative_to(REPO)), 'graph_sha256': sha(GRAPH),
            'base_state_sha256': sha(SOURCE), 'vertices': n, 'edges': len(edges),
            'pins': pins, 'search_nodes': nodes, 'all_fixed_zpq_012_colourings': sorted(found),
            'complete_labelled_colourings': 864, 'base_rows': 432, 'every_fibre_size': 2,
            'actual_single_component_switches': switches, 'actual_complementary_pair_cubes': cubes,
            'hidden_components': hidden, 'equivariant_section_equations': sorted(equations),
            'equivariant_section_conflict': conflict,
            'scope': 'This explicit graph realizes the complete two-sheet Layer0 cover; no planar-source realization follows.'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--certificate', type=Path, default=HERE / 'cover75-independent.json')
    args = ap.parse_args()
    result = json.loads(json.dumps(build()))
    if args.write:
        with args.certificate.open('x') as f:
            json.dump(result, f, indent=2, sort_keys=True)
            f.write('\n')
    else:
        assert json.loads(args.certificate.read_text()) == result
    print(json.dumps({k: result[k] for k in ('vertices', 'edges', 'search_nodes', 'complete_labelled_colourings',
                                            'actual_single_component_switches', 'actual_complementary_pair_cubes',
                                            'hidden_components', 'equivariant_section_conflict')} | {'status': 'PASS'}, sort_keys=True))


if __name__ == '__main__':
    main()
