#!/usr/bin/env python3
"""Complete C0 split-cube annotations: a source-covered relaxation adds no rows.

This does not solve exact common-exterior realizability. No graph-size bound,
colouring oracle, or truncation of the old partition fixed point is used.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import subprocess

import ck_kempe_obstruction as old

ROOT = Path(__file__).resolve().parents[1]
SPLITS = old.PAIRS
CYCLE = (2, 3, 4, 7, 5, 6)
PRIOR = 'audits/2026-10-29-three-step-relation-control-e1a90fe/results.json'
ZV = 'audits/2026-10-30-three-step-shared-exterior-e1a90fe/results.json'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def literal_options(row, split):
    """Transport complete normalized options using ONE common colour map."""
    normalized = old.normalize(row)
    mapping = {}
    for actual, canonical in zip(row, normalized):
        mapping[canonical] = actual
    for canonical, actual in zip(sorted(set(range(4)) - mapping.keys()),
                                 sorted(set(range(4)) - set(mapping.values()))):
        mapping[canonical] = actual
    canonical_split = next(s for s, pairs in enumerate(SPLITS)
                           if {frozenset(mapping[c] for c in p) for p in pairs}
                           == {frozenset(p) for p in SPLITS[split]})
    i = old.patterns(6).index(normalized)
    return tuple(blocks for _, blocks in old.partition_options(6, i, canonical_split))


def switched(row, blocks, split, selected):
    mate = {a: b for pair in SPLITS[split] for a, b in (pair, pair[::-1])}
    changed = list(row)
    for i, block in enumerate(blocks):
        if selected >> i & 1:
            for v in block:
                changed[v] = mate[row[v]]
    return tuple(changed)


def annotations(mask):
    canonical = {row for i, row in enumerate(old.patterns(6)) if mask >> i & 1}
    rows = sorted({tuple(p[c] for c in row) for row in canonical
                   for p in permutations(range(4))})
    support = set(rows)
    states = []
    for row in rows:
        choices = [tuple(blocks for blocks in literal_options(row, s)
                         if all(switched(row, blocks, s, t) in support
                                for t in range(1 << len(blocks))))
                   for s in range(3)]
        assert all(choices)
        states.extend((row, partitions) for partitions in product(*choices))
    states.sort()
    groups = defaultdict(list)
    for i, (row, partitions) in enumerate(states):
        for s, blocks in enumerate(partitions):
            groups[row, s, blocks].append(i)
    cubes = []
    full_transition_count = 0
    transition_hash = sha256()
    for i, (row, partitions) in enumerate(states):
        for s, blocks in enumerate(partitions):
            targets = []
            for t in range(1 << len(blocks)):
                changed = switched(row, blocks, s, t)
                alternatives = groups[changed, s, blocks] if t else [i]
                assert alternatives
                targets.append(alternatives[0])
                full_transition_count += len(alternatives)
                record = [i, s, t, alternatives]
                transition_hash.update(json.dumps(record, separators=(',', ':')).encode() + b'\n')
            assert len(set(states[j][0] for j in targets)) == len(targets)
            cubes.append([i, s, targets])
    projections = []
    for size in range(7):
        for positions in combinations(range(6), size):
            fibres = defaultdict(list)
            for i, (row, _) in enumerate(states):
                fibres[tuple(row[p] for p in positions)].append(i)
            complete = [fibres.get(word, []) for word in product(range(4), repeat=size)]
            assert {tuple(row[p] for p in positions) for row in rows} == set(fibres)
            projections.append(dict(positions=positions, full_fibres=complete))
    return dict(states=[dict(row=row, partitions=parts) for row, parts in states],
                cubes=cubes, full_transition_count=full_transition_count,
                transition_sha256=transition_hash.hexdigest(),
                canonical_state_count=sum(old.normalize(row) == row for row, _ in states),
                projections=projections), rows


def controls(prior, zv):
    core = [tuple(e) for e in prior['core_edges']]
    kernel = prior['kernel']
    boundary = kernel['boundary_order']
    actual = []
    for row in product(range(4), repeat=6):
        fixed = dict(zip(boundary, row))
        actual.append([lift for lift in product(range(4), repeat=3)
                       if all((fixed | dict(enumerate(lift)))[a]
                              != (fixed | dict(enumerate(lift)))[b] for a, b in core)])
    assert actual == [[tuple(lift) for lift in fibre] for fibre in kernel['full_fibres']]
    # Keep the historical *proper-interface* empty example, not an improper edge.
    empty_word = (0, 1, 1, 0, 0, 1)
    empty_index = sum(c * 4 ** (5-i) for i, c in enumerate(empty_word))
    assert actual[empty_index] == []
    remaining_edges = [(a, b) for a, b in core if a >= 3]
    colors = dict(zip(boundary, empty_word))
    assert all(colors[a] != colors[b] for a, b in remaining_edges)
    counts = zv['outer']['full_counts']
    assert len(counts) == 4 ** 8
    proper_count = 0
    for word, count in zip(product(range(4), repeat=8), counts):
        proper = all(word[i] != word[(i+1) % 8] for i in range(8))
        assert (count > 0) == proper
        proper_count += proper
        if proper:
            # Recheck the constructive extension, using the original Dv,zv.
            eta = dict(zip(zv['contract']['C_order'], word))
            h = eta[15]
            p = next(c for c in range(4) if c not in {h, eta[9], eta[11]})
            q = next(c for c in range(4) if c not in {h, p, eta[13]})
            r = next(c for c in range(4) if c not in {h, p, q})
            f = eta | dict(enumerate((r, q, h, p, q, p, r, h, p)))
            assert all(f[a] != f[b] for a, b in zv['contract']['original_edges'])
    assert proper_count == 6564
    return dict(planar_kernel=dict(nonempty=sum(map(bool, actual)),
                                    empty=sum(not f for f in actual),
                                    lifts=sum(map(len, actual)),
                                    proper_empty_word=empty_word),
                zv=dict(proper=proper_count, accepted=proper_count,
                        literal_lifts=sum(counts),
                        complete_old_counts_retained=True,
                        constructive_extension_rechecked=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    prior = json.loads((ROOT / PRIOR).read_text())
    zv = json.loads((ROOT / ZV).read_text())
    core = prior['d_control']['original_edges']
    accepted = 0
    for i, row in enumerate(old.patterns(6)):
        fixed = dict(zip(CYCLE, row))
        if any(all((fixed | {0: a, 1: b})[u] != (fixed | {0: a, 1: b})[v]
                   for u, v in core) for a, b in product(range(4), repeat=2)):
            accepted |= 1 << i
    fixed = old.obstruction(6, accepted)
    assert accepted == 4969575 and fixed['residual_mask'] == 2075405200
    annotation, rows = annotations(fixed['residual_mask'])
    result = dict(claim='Existential full split-cube trace annotations equal the old '
                       'component-partition fixed point. Exact common-graph realizability OPEN.',
                  contract=dict(original_cycle=CYCLE, core_edges=core),
                  old=dict(patterns=old.patterns(6), accepted_mask=accepted,
                           initial_mask=((1 << 31)-1) ^ accepted,
                           removed_masks=[r['removed_mask'] for r in fixed['rounds']],
                           residual_mask=fixed['residual_mask']),
                  candidate=dict(name='PAIR-C0-D16',
                                 patterns=[r for i, r in enumerate(old.patterns(6))
                                           if fixed['residual_mask'] >> i & 1], literal_rows=rows),
                  annotation=annotation, controls=controls(prior, zv))
    args.out_dir.mkdir(parents=True, exist_ok=False)
    path = args.out_dir / 'results.json'
    path.write_text(json.dumps(result, separators=(',', ':'), sort_keys=True) + '\n')
    inputs = [PRIOR, ZV, 'scripts/ck_kempe_obstruction.py',
              'scripts/four_color_three_step_annotations.py',
              'scripts/four_color_three_step_annotation_replay.py']
    manifest = dict(baseline=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                                                      text=True).strip(),
                    sources={p: digest(ROOT / p) for p in inputs},
                    outputs={'results.json': digest(path)})
    (args.out_dir / 'verification.json').write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(states=len(annotation['states']), cubes=len(annotation['cubes']),
                          full_transitions=annotation['full_transition_count'],
                          candidate_patterns=len(result['candidate']['patterns']),
                          candidate_literal_rows=len(rows), new_rows_excluded=0)))


if __name__ == '__main__':
    main()
