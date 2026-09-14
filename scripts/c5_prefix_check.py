#!/usr/bin/env python3
"""Audit prefix ownership against the actual reduced enumerator, without editing its output.

uv run --with rustworkx==0.17.1 python scripts/c5_prefix_check.py --check

The generic model exhausts every cut for E <= 9. Production checks use k=0..3:
monolithic DFS, instrumented reverse-order tasks, and a real two-process Pool.
Comparisons preserve every labelled mask, multiplicity, Sigma, and chosen witness.
This is computational evidence, not a formal verification of Python or planarity.
"""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import c5_cell_reduced as R

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'artifacts/c5_cells/prefix_check.json'


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def subsets(lo, hi, mask=0):
    """Independent increasing-index subset tree, including the root itself."""
    yield mask
    for edge in range(lo, hi):
        yield from subsets(edge + 1, hi, mask | (1 << edge))


def generic_partition():
    cases = targets = 0
    for edges in range(10):
        for cut in range(edges + 1):
            labels = list(subsets(0, cut))
            require(len(labels) == len(set(labels)) == 1 << cut, 'duplicate prefix label')
            visits = Counter()
            for label in labels:
                for target in subsets(cut, edges, label):
                    require(target & ((1 << cut) - 1) == label, 'wrong owner')
                    visits[target] += 1
            require(visits == Counter(range(1 << edges)), 'partition does not cover exactly once')
            cases += 1
            targets += sum(visits.values())
    return dict(max_edge_bits=9, cuts_checked=cases, target_cut_pairs=targets)


def normalized(catalogue):
    result = {}
    masks_seen = set()
    for sigma, cell in catalogue.items():
        masks = sorted(cell['masks'])
        require(len(masks) == len(set(masks)) == cell['count'], 'duplicate mask or wrong count')
        require(not masks_seen.intersection(masks), 'same graph assigned different Sigma keys')
        masks_seen.update(masks)
        require(tuple(cell['witness']) == min((m.bit_count(), m) for m in masks), 'wrong witness')
        result[str(sigma)] = dict(count=cell['count'], witness=list(cell['witness']), masks=masks)
    return result


def graph_edges():
    return {tuple(sorted(e)) for e in R._W['graph'].edge_list()}


def production_case(k, fault=None):
    R._setup(k, True)
    edge_count = R._W['E']
    base = graph_edges()
    mono, stats = {}, dict(nodes=0, survivors=0, pruned=0, calls=0, rejected=0)
    R._dfs(0, 0, edge_count, (R._W['full'],) * 10, mono, stats)
    require(graph_edges() == base, 'monolithic DFS leaked graph edges')
    expected = normalized(mono)
    expected_masks = {m for c in expected.values() for m in c['masks']}
    tasks, accepted, task_outputs = [], [], []
    state = dict(label=None, pool_calls=0, attempts=0)
    original_record = R._record

    def record(mask, surviving, per_sigma):
        state['attempts'] += 1
        expected_edges = base | {tuple(sorted(e)) for j, e in enumerate(R._W['edges'])
                                 if mask >> j & 1}
        require(graph_edges() == expected_edges, 'worker graph does not match current mask')
        result = original_record(mask, surviving, per_sigma)
        if result:
            # Rebuild the entire AND from selected edges, independently of task reconstruction.
            folded = [R._W['full']] * 10
            for j in range(edge_count):
                if mask >> j & 1:
                    folded = [a & b for a, b in zip(folded, R._W['tables'][j])]
            require(tuple(folded) == surviving, 'worker lost or duplicated a colour restriction')
            accepted.append((mask, state['label']))
        return result

    class ReversePool:
        """Execute unmodified _task in reverse submission order and capture its ownership."""
        def __init__(self, jobs, initializer, initargs):
            state['pool_calls'] += 1
            initializer(*initargs)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def imap_unordered(self, function, iterable, chunksize):
            labels = list(iterable)
            if fault == 'omit':
                cut = labels[0][1]
                owner = (min(expected_masks) & ((1 << cut) - 1), cut)
                require(owner in labels, 'negative control owner missing before injection')
                labels.remove(owner)
            elif fault == 'duplicate':
                labels.append(labels[0])
            tasks.extend(labels)
            require(len(labels) == len(set(labels)), 'production submitted duplicate task')
            for label, cut in reversed(labels):
                require(label < 1 << cut, 'task label contains suffix bits')
                require(R.viable(label, cut), 'task fails production cut guard')
                require(graph_edges() == base, 'worker starts with dirty graph')
                state['label'] = (label, cut)
                result = function((label, cut))
                require(graph_edges() == base, 'task did not restore base graph')
                for cell in result[0].values():
                    for mask in cell['masks']:
                        require(mask & ((1 << cut) - 1) == label, 'task emitted another owner graph')
                # _merge intentionally adopts the first cell dictionary, then mutates it.
                # Snapshot before yielding so the order replay receives original task results.
                task_outputs.append(deepcopy(result[0]))
                yield result
            state['label'] = None

    with patch.object(R, 'Pool', ReversePool), patch.object(R, '_record', record):
        split, split_stats = R.enumerate_reduced(k, 2, log=lambda *a, **kw: None, keep=True)
    require(normalized(split) == expected, 'split and monolithic results differ')
    require(Counter(m for m, _ in accepted) == Counter(expected_masks), 'accepted records not once each')
    require(graph_edges() == base, 'split traversal leaked graph edges')
    cut = R._W['blocks'][min(1, k - 1)][2] + 1 if k else edge_count
    if cut == edge_count:
        require(state['pool_calls'] == 0 and not tasks, 'end cut must not launch workers')
        require(all(owner is None for _, owner in accepted), 'end cut was worker-recorded')
    else:
        require(state['pool_calls'] == 1, 'proper cut must launch workers')
        require(all(owner is not None for _, owner in accepted), 'proper cut recorded in parent')
        for mask, owner in accepted:
            require(owner == (mask & ((1 << cut) - 1), cut), 'accepted record has wrong owner')
        # Aggregation must not depend on task completion order.
        forward = {}
        for output in reversed(task_outputs):
            R._merge(forward, output)
        require(normalized(forward) == expected, 'merge is completion-order dependent')

    real, real_stats = R.enumerate_reduced(k, 2, log=lambda *a, **kw: None, keep=True)
    require(normalized(real) == expected, 'real Pool and monolithic results differ')
    require(real_stats['prefix_tasks'] == split_stats['prefix_tasks'], 'task count changed')
    payload = json.dumps(expected, sort_keys=True, separators=(',', ':')).encode()
    return dict(k=k, edge_bits=edge_count, prefix=cut, branch='direct' if cut == edge_count else 'workers',
                submitted_tasks=len(tasks), retained_prefixes=split_stats['prefix_tasks'],
                record_attempts=state['attempts'], accepted_masks=len(expected_masks), sigma_keys=len(expected),
                monolithic_split_real_pool_equal=True, unique_ownership=True,
                graph_restored=True, colour_fold_equal=True, result_sha256=hashlib.sha256(payload).hexdigest())


def negative_controls():
    for fault, message in [('omit', 'split and monolithic results differ'),
                           ('duplicate', 'production submitted duplicate task')]:
        try:
            production_case(3, fault=fault)
        except AssertionError as error:
            require(str(error) == message, f'{fault} failed for an unintended reason: {error}')
        else:
            raise AssertionError(f'production task {fault} was not detected')
    malformed = {1: dict(count=2, witness=(0, 0), masks=[0, 0])}
    try:
        normalized(malformed)
    except AssertionError:
        return dict(omission_rejected=True, duplication_rejected=True)
    raise AssertionError('duplicate-mask guard did not fire')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='recompute and byte-compare saved report')
    args = parser.parse_args()
    paths = ['scripts/c5_cell_reduced.py', 'scripts/c5_cell_enumerator.py', 'scripts/c5_prefix_check.py',
             'Math/PrefixPartition.lean', 'artifacts/c5_cells/cells.json']
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}
    report = dict(scope='prefix partition only; Python and planarity remain computational',
                  source_sha256=hashes, generic=generic_partition(), negative_controls=negative_controls(),
                  production=[])
    for k in range(4):
        row = production_case(k)
        report['production'].append(row)
        print(json.dumps(row, sort_keys=True), flush=True)
    require(all(hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == h for p, h in hashes.items()),
            'an input changed during the audit')
    payload = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.check:
        require(REPORT.read_text() == payload, 'saved report differs from deterministic replay')
        print('prefix report replay: PASS')
    else:
        REPORT.write_text(payload)
        print(f'wrote {REPORT}')


if __name__ == '__main__':
    main()
