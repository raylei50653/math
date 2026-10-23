#!/usr/bin/env python3
"""Independent two-interface turns and all <=5-vertex colour-respecting glues."""
from collections import Counter
from itertools import combinations, permutations, product
import json
import math

ROLES = (0, 2, 3, 1)


def edge(a, b):
    return tuple(sorted((a, b)))


def turns():
    answer = []
    coordinates = {'k': (-1, 0), 'b': (1, 0), 'left': (0, 1), 'right': (0, -1)}
    for kc, bc in ((0, 3), (2, 1)):
        remaining = sorted(set(range(4)) - {kc, bc})
        for lc, rc in product(remaining, repeat=2):
            colour = {'k': kc, 'b': bc, 'left': lc, 'right': rc}
            phi_sign = {v: (1 if c in (0, 2) else -1) for v, c in colour.items()}
            psi = {v: (2 - c if c in (0, 2) else c) for v, c in colour.items()}
            psi_sign = {v: (1 if c in (1, 2) else -1) for v, c in psi.items()}
            arms = []
            for label, signs in (('alpha', phi_sign), ('beta', psi_sign)):
                for side in ('left', 'right'):
                    exits = [edge(v, side) for v in ('k', 'b') if signs[v] != signs[side]]
                    if len(exits) != 1:
                        raise ValueError('wrong exact triangle interface exits')
                    a, b = exits[0]
                    x = (coordinates[a][0] + coordinates[b][0]) / 2
                    y = (coordinates[a][1] + coordinates[b][1]) / 2
                    arms.append((math.atan2(y, x), label))
            ordered = [label for angle, label in sorted(arms)]
            crosses = all(ordered[i] != ordered[(i + 1) % 4] for i in range(4))
            if crosses != (lc != rc):
                raise ValueError('four-colour transverse crossing equivalence failed')
            answer.append({'center_colours': [kc, bc], 'third_colours': [lc, rc],
                           'cyclic_arms': ordered, 'transverse': crosses})
    return answer


def glues():
    results = []
    for split in (None, 0, 1, 2, 3):
        for diag_a, diag_b in product(((0, 3), (2, 1)), repeat=2):
            patches = []
            for number, diagonal in enumerate((diag_a, diag_b)):
                names = {c: f'{c}_{number if c == split else "shared"}' for c in range(4)}
                edges = {edge(names[a], names[b]) for a, b in zip(ROLES, ROLES[1:] + ROLES[:1])}
                center = edge(names[diagonal[0]], names[diagonal[1]])
                edges.add(center)
                patches.append((edges, center))
            edges = patches[0][0] | patches[1][0]
            vertices = sorted({v for e in edges for v in e})
            if patches[0][1] == patches[1][1]:
                verdict = 'same-center outside distinct-crossing premise'
                witness = []
            else:
                k4 = next((list(s) for s in combinations(vertices, 4)
                           if all(edge(a, b) in edges for a, b in combinations(s, 2))), None)
                if k4:
                    verdict, witness = 'forbidden K4', k4
                else:
                    cycle = next((list(s) for s in permutations(vertices, 4)
                                  if all(edge(s[i], s[(i + 1) % 4]) in edges for i in range(4))
                                  and edge(s[0], s[2]) not in edges
                                  and edge(s[1], s[3]) not in edges), None)
                    if cycle is None:
                        raise ValueError('unresolved distinct-center small glue')
                    verdict, witness = 'forbidden diagonal-free C4', cycle
            results.append({'split_colour': split, 'center_types': [list(diag_a), list(diag_b)],
                            'vertex_count': len(vertices), 'verdict': verdict, 'witness': witness})
    counts = Counter(r['verdict'] for r in results)
    if sorted(counts.values()) != [4, 6, 10]:
        raise ValueError('wrong complete schema counts')
    return results, dict(counts)


def main():
    local = turns()
    small, counts = glues()
    print(json.dumps({'status': 'PASS', 'local_turns': local,
                      'transverse_turns': sum(r['transverse'] for r in local),
                      'small_glue_schemas': small, 'schema_counts': counts,
                      'paper_dependency': 'global arc entry-exit and original small-cap theorems',
                      'full_source_status': 'not triggered', 'pair_exclusions': 0}, sort_keys=True))


if __name__ == '__main__':
    main()
