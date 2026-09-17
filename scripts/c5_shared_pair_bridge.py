#!/usr/bin/env python3
"""Rooted shared-pair interfaces and bridge-forcer replacement controls.

Topology is delegated to the existing two-triangle certificate; no new search.
"""
import argparse
from itertools import combinations, product
import json
from pathlib import Path
from c5_disk_deletions import sha

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_shared_pair_bridge/observations.json'
U = set(range(4))
CORE = [(0, 1), (0, 2), (1, 2), (0, 3), (0, 4), (3, 4)]


def build():
    pairs = list(combinations(range(4), 2))
    records, singletons = [], []
    # Shared vertex 0; bridge root 1; other vertex 2; opposite petals 3,4.
    for root, side, a, b in product(list(combinations(range(4), 3)), pairs, pairs, pairs):
        lists = [range(4), root, side, a, b]
        actual = sorted({cs[1] for cs in product(*lists)
                         if all(cs[u] != cs[v] for u, v in CORE)})
        shared = U-set(a) if a == b else U
        forbidden = set(side) if shared == set(side) else set()
        expected = sorted(set(root)-forbidden)
        assert actual == expected
        record = dict(root=root, side=side, petals=[a, b], available=actual)
        records.append(record)
        if len(actual) == 1:
            c = actual[0]
            assert a == b and set(side) == U-set(a)
            assert set(root) == set(side) | {c} and c in a
            singletons.append(record)
    assert len(records) == 864 and len(singletons) == 12
    assert all(sum(r['available'] == [c] for r in singletons) == 3 for c in range(4))

    # For every possible root availability set, replacement preserves colorability.
    # The original outside component has root availability exactly {c}.
    bridge_controls = []
    for mask, c in product(range(16), range(4)):
        available = {x for x in U if mask & (1 << x)}
        original = any(x != c for x in available)
        replacement = (bool(available-{c}) if c != 3 else
                       any(x != y for x in available for y in U-{0, 1, 2}))
        assert original == replacement
        bridge_controls.append(dict(root_mask=mask, forced=c, colorable=original))
    # A deleted D-leaf spoke of color s frees s; original root can take D.
    released_spokes = []
    for s in range(3):
        leaf_available = U-({0, 1, 2}-{s})
        assert 3 in leaf_available and s in leaf_available and s != 3
        released_spokes.append(dict(deleted_color=s, root=3, leaf=s))

    # With c=D, the normalized pair plus two D leaves is exactly the existing
    # shared template, up to the permutation (0,3,4,1,2) of the five core points.
    from c5_two_triangle_blocks import templates
    prior_shared = [row for row in templates() if row[0] == 'shared']
    d_controls = []
    for record in singletons:
        if record['available'] != [3]:
            continue
        p = set(record['petals'][0])
        lists = [U, p, p, (U-p) | {3}, (U-p) | {3}, {3}, {3}]
        inner = CORE + [(3, 5), (4, 6)]
        matched = [metadata for _, metadata, old_lists, old_inner in prior_shared
                   if lists == old_lists and inner == old_inner]
        assert len(matched) == 1
        d_controls.append(dict(petal_palette=sorted(p), existing_shared_metadata=matched[0]))
    assert len(d_controls) == 3
    sources = ['c5_shared_pair_bridge', 'c5_two_triangle_blocks', 'c5_triangle_forks',
               'c5_tree_cores', 'c5_odd_join_cores', 'c5_disk_deletions',
               'c5_cell_enumerator', 'local_closure', 'boundary_relations',
               'c5_shared_triangle_blocks', 'c5_three_triangle_blocks',
               'c5_four_triangle_chain', 'c5_four_triangle_star']
    priors = [ROOT / f'artifacts/{name}/observations.json' for name in
              ['c5_two_triangle_blocks', 'c5_shared_triangle_blocks',
               'c5_three_triangle_blocks', 'c5_four_triangle_chain', 'c5_four_triangle_star']]
    return dict(schema=1, scope='Rooted shared pair; paper bridge-pruning reduction, not a topology theorem.',
                root_assignments=records, singleton_assignments=singletons,
                bridge_controls=bridge_controls, released_D_spokes=released_spokes,
                D_template_matches=d_controls,
                source_sha256={f'scripts/{s}.py': sha(ROOT/'scripts'/f'{s}.py') for s in sources},
                dependency_sha256={str(prior.relative_to(ROOT)): sha(prior) for prior in priors})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(dict(root_assignments=len(result['root_assignments']),
                          singleton_assignments=len(result['singleton_assignments']),
                          bridge_controls=len(result['bridge_controls']),
                          D_template_matches=len(result['D_template_matches'])), indent=2))


if __name__ == '__main__':
    main()
