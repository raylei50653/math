#!/usr/bin/env python3
"""Independent boundary binding of the same-successor four-node tree path."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parents[1] / '2026-10-23-three-mask-round2-cb8f859/941/certificate.json'
BOUNDARY = ('a', 'z1', 'z2', 'z3', 'z4', 'V', 'U', 'HL_0', 'q', 'c', 's', 'v', 'w', 't')


def main():
    rows = json.loads(PREVIOUS.read_text())['source_rows']
    result = []
    for row in rows:
        colors = dict(zip(BOUNDARY, (0,3,0,3,0,1,0,1,3,1,2,
                                    0 if row['target'] == 44459 else 1,
                                    1 if row['target'] == 44459 else 0,2)))
        successor = {v: (2 if v == 'U' else c) for v, c in colors.items()}
        # All other boundary vertices are outside the same complete K.
        assert row['actual_K_boundary_contacts'] == ['U']
        parts = row['full_03_successor_boundary_contacts']
        nodes = [next(p for p in parts if v in p) for v in ('z4', 'U', 'q', 'c')]
        assert len({tuple(p) for p in nodes}) == 4
        assert all(successor[v] in ({0,3} if j in (0,2) else {1,2})
                   for j, p in enumerate(nodes) for v in p)
        for (a,b),(i,j) in zip((('z4','V'),('HL_0','q'),('q','c')),((0,1),(1,2),(2,3))):
            assert (BOUNDARY.index(a)-BOUNDARY.index(b)) % 14 in (1,13)
            assert a in nodes[i] and b in nodes[j]
        tip = 'v' if row['target'] == 44459 else 'w'
        for gate in row['complete_initial_01_gate']:
            original_block = next(p for p in gate if 'U' in p)
            assert 'c' in original_block
            boundary_choices = [v for v in BOUNDARY if colors[v] == 0
                                and v != 'U' and v in original_block and v in nodes[2]]
            assert boundary_choices == ([tip] if tip in original_block else [])
            result.append({'target': row['target'], 'initial_02': row['initial_02_type'],
                           'initial_01_U_block': original_block,
                           'specified_last_bridge_boundary_choices': boundary_choices,
                           'specified_last_bridge_forced_private': not boundary_choices})
    assert len(result) == 16
    assert sum(r['specified_last_bridge_forced_private'] for r in result) == 8
    print(json.dumps({'status': 'PASS', 'source_rows': 4, 'bridge_rows': result,
                      'path_nodes': ['A03', 'C12', 'Q03', 'D12'],
                      'pair_exclusions': 0, 'source_realization_checked': False}, sort_keys=True))


if __name__ == '__main__':
    main()
