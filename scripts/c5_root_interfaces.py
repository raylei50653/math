#!/usr/bin/env python3
"""Bounded rooted path interfaces and single-branch triangle substitutions.

All degree-four path forcers of sizes 2, 4, 6 with a virtual parent edge
forcing a used Q color. This is not an arbitrary forcing-tree classification.
"""
import argparse
from collections import Counter
import hashlib
from itertools import product
import json
from pathlib import Path

import networkx as nx

from c5_cell_enumerator import REPS
from c5_disk_deletions import BOUNDARY, sha
from c5_tree_cores import Q, QI, options, lifted_edges, disk_check, exact_core

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_root_interfaces/observations.json'
BASE = ROOT / 'artifacts/c5_triangle_branches/observations.json'


def root_mask(neighborhoods, boundary):
    """Exact bottom-up tree message for a path rooted at its first vertex."""
    possible = 15
    for neighbors in reversed(neighborhoods):
        allowed = 15 ^ sum(1 << c for c in {boundary[b] for b in neighbors})
        possible = sum(1 << c for c in range(4)
                       if allowed >> c & 1 and possible & ~(1 << c))
    return possible


def pinned_search(neighborhoods, boundary):
    """Independent direct coloring search with each root color pinned."""
    def visit(i, previous):
        if i == len(neighborhoods):
            return True
        for c in range(4):
            if c != previous and all(c != boundary[b] for b in neighborhoods[i]):
                if visit(i + 1, c):
                    return True
        return False
    return sum(1 << c for c in range(4)
               if all(c != boundary[b] for b in neighborhoods[0]) and visit(1, c))


def bridge_mask(mask):
    """Parent colors compatible with at least one root color across one edge."""
    return sum(1 << c for c in range(4) if mask & ~(1 << c))


def paths():
    # Edge palettes from virtual parent to leaf: c,D,a1,D,a2,D,...,D.
    for n in (2, 4, 6):
        for c in range(3):
            for word in product(range(3), repeat=(n - 2) // 2):
                lists = [{3, c}] + [{3, a} for a in word for _ in range(2)] + [{3}]
                for ns in product(*(options(a for a in range(3) if a not in ls)
                                    for ls in lists)):
                    yield n, c, word, ns


def substitute(base, branch, ns):
    neighborhoods = list(base['neighborhoods'][:3])
    inner = [(0, 1), (0, 2), (1, 2)]
    for j in range(len(base['branch_colors'])):
        part = ns if j == branch else base['neighborhoods'][3+2*j:5+2*j]
        start = len(neighborhoods)
        neighborhoods.extend(part)
        inner.append((j, start))
        inner.extend((v, v+1) for v in range(start, len(neighborhoods)-1))
    return 5 + len(neighborhoods), lifted_edges(inner, neighborhoods)


def build():
    counts, rows = Counter(), []
    digest = hashlib.sha256()
    for n, c, word, ns in paths():
        edges = lifted_edges([(i, i+1) for i in range(n-1)], ns)
        graph = nx.Graph(edges)
        graph.add_edges_from((n+5, b) for b in range(5))
        disk = nx.check_planarity(graph)[0]
        counts[f'path_{n}_templates'] += 1
        digest.update((json.dumps([n, c, word, ns, disk]) + '\n').encode())
        if not disk:
            continue
        counts[f'path_{n}_disk'] += 1
        masks = [root_mask(ns, b) for b in REPS]
        full = [root_mask(ns, b) for b in BOUNDARY]
        assert full == [pinned_search(ns, b) for b in BOUNDARY]
        assert masks[QI] == 1 << c
        _, topology = disk_check(n+5, edges)
        rows.append(dict(size=n, forced_color=c, word=word, neighborhoods=ns,
                         edges=edges, masks=masks, bridge_masks=[bridge_mask(m) for m in masks], full_masks=''.join(format(m, 'x') for m in full),
                         topology=topology))
    small = {c: {tuple(r['masks']) for r in rows
                 if r['size'] == 2 and r['forced_color'] == c} for c in range(3)}
    novel = [i for i, r in enumerate(rows) if tuple(r['masks']) not in small[r['forced_color']]]
    counts['interfaces'] = len({tuple(r['masks']) for r in rows})
    counts['novel_paths'] = len(novel)
    bridge_small = {c: {tuple(r['bridge_masks']) for r in rows
                       if r['size'] == 2 and r['forced_color'] == c} for c in range(3)}
    bridge_novel = [i for i, r in enumerate(rows)
                    if tuple(r['bridge_masks']) not in bridge_small[r['forced_color']]]
    counts['bridge_interfaces'] = len({tuple(r['bridge_masks']) for r in rows})
    counts['bridge_novel_paths'] = len(bridge_novel)
    witness = rows[bridge_novel[0]]
    # A separator against every same-color two-point disk template.
    separators = []
    for i, row in enumerate(rows):
        if row['size'] != 2 or row['forced_color'] != witness['forced_color']:
            continue
        j = next(j for j in range(10) if row['bridge_masks'][j] != witness['bridge_masks'][j])
        separators.append(dict(short_path=i, pattern=j, long_mask=witness['bridge_masks'][j],
                               short_mask=row['bridge_masks'][j]))
    contexts, context_digest = [], hashlib.sha256()
    bases = json.loads(BASE.read_text())['disk_templates']
    for bi, base in enumerate(bases):
        for branch, c in enumerate(base['branch_colors']):
            for ri, row in enumerate(rows):
                if row['forced_color'] != c:
                    continue
                n, edges = substitute(base, branch, row['neighborhoods'])
                graph = nx.Graph(edges)
                graph.add_edges_from((n, b) for b in range(5))
                disk = nx.check_planarity(graph)[0]
                counts['context_tests'] += 1
                context_digest.update((json.dumps([bi, branch, ri, disk]) + '\n').encode())
                if not disk:
                    continue
                counts['context_disk'] += 1
                assert ri not in novel
                assert all(a == c for a in row['word'])
                exact = exact_core(n, edges)
                assert exact['sigma'] == 1023 ^ (1 << QI)
                _, topology = disk_check(n, edges)
                contexts.append(dict(base=bi, branch=branch, path=ri, edges=edges,
                                     **exact, topology=topology))
    counts['context_interfaces'] = len({tuple(rows[r['path']]['masks']) for r in contexts})
    assert dict(counts) == dict(path_2_templates=32, path_2_disk=27,
                               path_4_templates=768, path_4_disk=77,
                               path_6_templates=18432, path_6_disk=139,
                               interfaces=52, novel_paths=111, bridge_interfaces=41, bridge_novel_paths=99,
                               context_tests=800, context_disk=108, context_interfaces=4)
    dependencies = ['c5_root_interfaces', 'c5_triangle_branches', 'c5_tree_cores',
                    'c5_odd_join_cores', 'c5_cell_enumerator', 'c5_disk_deletions',
                    'local_closure', 'boundary_relations']
    return dict(schema=1, scope=__doc__, fixed_pattern=Q, pattern_order=REPS,
                source_sha256={f'scripts/{name}.py': sha(ROOT / 'scripts' / f'{name}.py')
                               for name in dependencies}, input_sha256={str(BASE.relative_to(ROOT)): sha(BASE)},
                counts=dict(sorted(counts.items())), path_enumeration_sha256=digest.hexdigest(),
                paths=rows, novel_paths=novel, bridge_novel_paths=bridge_novel,
                witness_path=bridge_novel[0],
                two_point_separators=separators, context_enumeration_sha256=context_digest.hexdigest(),
                contexts=contexts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['counts'], indent=2))


if __name__ == '__main__':
    main()
