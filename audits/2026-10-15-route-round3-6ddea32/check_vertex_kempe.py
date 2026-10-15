#!/usr/bin/env python3
"""Independent ordinary vertex-Kempe closure of the named sphere control."""
from itertools import combinations
import json
from pathlib import Path
import argparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def check():
    source = json.loads((ROOT / 'audits/2026-10-15-six-pin-lifts-6ddea32/certificate.json').read_text())
    graph = next(c for c in source['controls'] if c['name'] == 'icosahedral')
    n = len(graph['vertices'])
    assert graph['vertices'] == list(range(n))
    edges = {tuple(e) for e in graph['edges']}
    adjacency = [{v if u == i else u for u, v in edges if i in (u, v)} for i in range(n)]
    assert {len(row) for row in adjacency} == {5}
    triangles = {triple for triple in combinations(range(n), 3)
                 if all(tuple(sorted(e)) in edges for e in combinations(triple, 2))}
    assert triangles == {tuple(sorted(face)) for face in graph['faces']}
    rows = []

    def enumerate_rows(prefix):
        vertex = len(prefix)
        if vertex == n:
            rows.append(tuple(prefix))
            return
        for colour in range(4):
            if all(prefix[u] != colour for u in adjacency[vertex] if u < vertex):
                enumerate_rows(prefix + [colour])

    enumerate_rows([])
    assert rows == [tuple(r) for r in graph['all_full_J_colourings']]
    row_index = {row: i for i, row in enumerate(rows)}
    pins = graph['pins']

    def event(row):
        return {row[pins['p']], row[pins['q']]}.isdisjoint({row[pins['v']], row[pins['w']]})

    failed = [i for i, row in enumerate(rows) if not event(row)]
    moves = []
    for i in failed:
        row = rows[i]
        for pair in combinations(range(4), 2):
            unseen = {v for v in range(n) if row[v] in pair}
            while unseen:
                start = min(unseen)
                component, stack = {start}, [start]
                unseen.remove(start)
                while stack:
                    vertex = stack.pop()
                    for nxt in sorted(adjacency[vertex] & unseen):
                        unseen.remove(nxt)
                        component.add(nxt)
                        stack.append(nxt)
                target = tuple(sum(pair) - c if v in component else c for v, c in enumerate(row))
                assert target in row_index and not event(target)
                moves.append([i, list(pair), sorted(component), row_index[target]])
    u = graph['U']
    degrees = {name: sum(vertex in e for e in u['edges']) for name, vertex in u['pins'].items()}
    assert [degrees[x] for x in ('z', 's', 't')] == [6, 4, 2]
    assert (len(rows), len(failed)) == (240, 216)
    return {'status': 'PASS', 'all_J_rows': rows, 'E_free_row_ids': failed,
            'ordinary_vertex_Kempe_moves': moves, 'full_colourings': len(rows),
            'E_free_colourings': len(failed), 'complete_moves': len(moves),
            'all_triangles_facial': True, 'all_degrees_five': True,
            'split_U_pin_degrees': degrees,
            'scope': 'One explicit non-source control; closure under every ordinary vertex component switch.'}


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
                      if key not in ('all_J_rows', 'E_free_row_ids', 'ordinary_vertex_Kempe_moves')}))


if __name__ == '__main__':
    main()
