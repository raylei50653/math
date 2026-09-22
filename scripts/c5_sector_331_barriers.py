#!/usr/bin/env python3
"""Local identity and attachment audit for 397/action 2 -> 331; no graph search."""
import argparse
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UP = ROOT / 'artifacts/c5_sector_successor_audit/observations.json'
CROSS = ROOT / 'artifacts/c5_sector_cross_row/observations.json'
OUT = ROOT / 'artifacts/c5_sector_331_barriers/observations.json'
PAIRS = list(combinations(range(4), 2))
OLD = (0, 1, 0, 2, 1)
NEW = (1, 0, 1, 2, 1)
ROWS = ((0, 1, 2, 1, 2), (0, 1, 2, 1, 3))


def linked(parts, pair, u, v):
    return any(u in cc and v in cc for cc in parts[PAIRS.index(pair)])


def build():
    upstream = json.loads(UP.read_text())
    inputs = {UP, CROSS, Path(__file__).resolve()}
    for name, digest in upstream['input_sha256'].items():
        path = ROOT / name
        assert sha256(path.read_bytes()).hexdigest() == digest, name
        inputs.add(path)
    states = json.loads(CROSS.read_text())['abstract']['states']
    source = states[397]
    target = next(r for r in upstream['candidates'] if r['state'] == 331)
    assert source['row'] == list(OLD)
    old_parts, new_parts = source['partitions'], target['raw_partitions']
    assert upstream['selected_action']['raw_row'] == list(NEW)
    assert linked(old_parts, (1, 3), 1, 4)
    assert linked(old_parts, (1, 2), 1, 4)
    assert linked(new_parts, (1, 3), 0, 2)
    assert not linked(new_parts, (0, 2), 1, 3)
    for d in (2, 3):
        assert not linked(old_parts, (0, d), 0, 2)
        assert not linked(new_parts, (1, d), 0, 4)
    assert not linked(new_parts, (1, 3), 2, 4)

    # All possible same-vertex identities, with S membership explicit.
    identities = []
    for color in range(4):
        for selected in (False, True):
            if selected and color not in (0, 1):
                continue
            after = 1-color if selected else color
            identities.append(dict(old_color=color, in_S=selected, new_color=after,
                                   old12=color in (1, 2), old13=color in (1, 3),
                                   new13=after in (1, 3)))
    crossing = [r for r in identities if r['old12'] and r['new13']]
    assert [(r['old_color'], r['in_S']) for r in crossing] == [(1, False)]
    shared = [r for r in identities if r['old13'] and r['new13']]
    assert [(r['old_color'], r['in_S']) for r in shared] == [(1, False), (3, False)]

    # Four DISTINCT neighbors at crossings: the disjoint color sets certify
    # distinctness across paths; each path is simple at its internal vertex.
    saturated = []
    for colors in combinations_with_replacement((0, 2, 3), 4):
        if colors.count(2) >= 2 and colors.count(3) >= 2:
            saturated.append(list(colors))
    assert saturated == [[2, 2, 3, 3]]
    bridge_attachments = [list(ns) for size in range(5)
                          for ns in combinations(range(5), size)
                          if all(OLD[v] in (2, 3) for v in ns)]
    assert bridge_attachments == [[], [3]]

    # Rejection of alpha forces tight degree lists. Audit all possible leaves,
    # not just leaves in a chosen S or in an empty-intersection branch.
    leaves = []
    for ns in combinations(range(5), 3):
        if len({ROWS[0][v] for v in ns}) != 3:
            continue
        for color in range(4):
            if color in {OLD[v] for v in ns}:
                continue
            after = 0 if color == 1 else color  # color 1 is in S via edge v--0
            assert 0 in ns
            rejection = None
            for side, row, parts, vc in [('old', OLD, old_parts, color),
                                          ('new', NEW, new_parts, after)]:
                for u, v in combinations(ns, 2):
                    if row[u] == row[v]:
                        pair = tuple(sorted((row[u], vc)))
                        if not linked(parts, pair, u, v):
                            rejection = dict(kind='two_edge_path', side=side,
                                             pair=pair, path=[u, 'leaf', v])
                            break
                if rejection:
                    break
            if rejection is None:
                assert ns == (0, 2, 3) and color == 1
                # S path 0--leaf--2 must cross old13 1--4 at its only
                # internal vertex; that needs two additional old-3 neighbors.
                # The actual frame-3 neighbor has old color 2, so degree >= 5.
                rejection = dict(kind='T3_degree_conflict', S_path=[0, 'leaf', 2],
                                 boundary_neighbor_colors=[OLD[v] for v in ns],
                                 required_additional_colors=[3, 3], minimum_degree=5)
            leaves.append(dict(attachments=ns, old_color=color, new_color=after,
                               obstruction=rejection))
    assert len(leaves) == 7
    assert sum(r['obstruction']['kind'] == 'two_edge_path' for r in leaves) == 6
    assert len({tuple(r['attachments']) for r in leaves}) == 4

    neighbors0 = []
    for size in range(1, 5):
        for ns in combinations(range(5), size):
            if 0 not in ns or 1 in {OLD[v] for v in ns}:
                continue
            if any(len({row[v] for v in ns}) != size for row in ROWS):
                continue
            excluded = 2 in ns and 3 in ns
            neighbors0.append(dict(attachments=ns, excluded_by_T3=excluded,
                                   forced_T3=2 in ns and not excluded))
    assert [list(r['attachments']) for r in neighbors0 if not r['excluded_by_T3']] == [
        [0], [0, 2], [0, 3]]
    # For a degree-four old star leaving the new13 component, two old-3
    # neighbors and at least one S neighbor (old 0) are compulsory.
    exit_types = [list(ns) for ns in combinations_with_replacement((0, 2, 3), 4)
                  if ns.count(3) >= 2 and ns.count(0) >= 1]
    assert exit_types == [[0, 0, 3, 3], [0, 2, 3, 3], [0, 3, 3, 3]]
    return dict(schema=1,
        scope='Necessary local conditions for one disk transition; topology is proved in the report, not by this finite audit.',
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                      for p in sorted(inputs)},
        source_profile=source, target_raw_profile=target,
        vertex_identities=identities, old12_new13_crossing=crossing,
        old13_new13_shared=shared, outside_bridge_neighbor_colors=saturated,
        outside_bridge_attachments=bridge_attachments,
        leaf_cases=leaves, old1_neighbors_of_0=neighbors0,
        old13_exit_star_neighbor_colors=exit_types,
        summary=dict(identity_cases=len(identities), leaf_cases=len(leaves),
                     two_edge_leaf_exclusions=6, T3_leaf_exclusions=1,
                     outside_bridge_attachment_cases=len(bridge_attachments),
                     surviving_neighbor0_attachments=3, exit_star_degree4_types=len(exit_types),
                     inherited_profiles=603, profile_deletions=0,
                     transition331_excluded=False, graph_search_rerun=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
