#!/usr/bin/env python3
"""Finite minor obstructions and normal forms for triangle blocks with path tails.

The arbitrary-length reduction is explained in docs/c5_triangle_path_reduction.md.
No classification of branching trees or additional cycle blocks is asserted.
"""
import argparse
from collections import Counter
from itertools import product
import json
from pathlib import Path

from c5_cell_enumerator import REPS
from c5_disk_deletions import BOUNDARY, sha
from c5_root_interfaces import root_mask, bridge_mask, pinned_search, substitute
from c5_tree_cores import Q, options, disk_check, exact_core

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'artifacts/c5_triangle_branches/observations.json'
PRIOR = ROOT / 'artifacts/c5_root_interfaces/observations.json'
OUT = ROOT / 'artifacts/c5_triangle_path_reduction/observations.json'


def build():
    bases = json.loads(BASE.read_text())['disk_templates']
    counts, obstructions, two_runs, normal_forms = Counter(), [], [], []
    for bi, base in enumerate(bases):
        for slot, c in enumerate(base['branch_colors']):
            first, leaf = base['neighborhoods'][3+2*slot:5+2*slot]
            # Preserve the actual root and leaf of the canonical endpoint minor.
            for a in range(3):
                if a == c:
                    continue
                for middle in options(k for k in range(3) if k != a):
                    ns = [first, middle, leaf]
                    n, edges = substitute(base, slot, ns)
                    disk, topology = disk_check(n, edges)
                    assert not disk
                    counts['palette_switch_obstructions'] += 1
                    obstructions.append(dict(kind='palette_switch', base=bi, slot=slot,
                                             palette=a, neighborhoods=ns, edges=edges,
                                             topology=topology))
            choices = options(k for k in range(3) if k != c)
            assert len(choices) == 2
            other, = [ns for ns in choices if list(ns) != first]
            ns = [first, other, first, leaf]
            n, edges = substitute(base, slot, ns)
            disk, topology = disk_check(n, edges)
            assert not disk
            counts['three_run_obstructions'] += 1
            obstructions.append(dict(kind='three_runs', base=bi, slot=slot,
                                     neighborhoods=ns, edges=edges, topology=topology))
            # Any two-run tail contracts to this, regardless of run parity.
            ns = [first, other, leaf]
            n, edges = substitute(base, slot, ns)
            disk, topology = disk_check(n, edges)
            counts['two_run_minors'] += 1
            counts['two_run_disk'] += int(disk)
            two_runs.append(dict(base=bi, slot=slot, neighborhoods=ns,
                                 edges=edges, disk=disk, topology=topology))
            if not disk:
                continue
            assert len(base['branch_colors']) == 1
            # Nonleaf path length is odd: the two run lengths have opposite parity.
            for lengths in ((1, 2), (2, 1)):
                ns = [first]*lengths[0] + [other]*lengths[1] + [leaf]
                n, edges = substitute(base, slot, ns)
                disk, topology = disk_check(n, edges)
                if not disk:
                    assert lengths == (2, 1)
                    counts['repeated_first_run_obstructions'] += 1
                    obstructions.append(dict(kind='repeated_first_run', base=bi, slot=slot,
                                             lengths=lengths, neighborhoods=ns, edges=edges,
                                             topology=topology))
                    continue
                assert lengths == (1, 2)
                assert [root_mask(ns, b) for b in BOUNDARY] == [pinned_search(ns, b) for b in BOUNDARY]
                long_bridge = [bridge_mask(root_mask(ns, b)) for b in BOUNDARY]
                short_bridge = [bridge_mask(root_mask([first, leaf], b)) for b in BOUNDARY]
                assert long_bridge == short_bridge
                exact = exact_core(n, edges)
                assert exact['full_relation'] == base['full_relation']
                counts['two_run_normal_forms'] += 1
                normal_forms.append(dict(base=bi, slot=slot, lengths=lengths,
                                         neighborhoods=ns, edges=edges, **exact,
                                         bridge_masks=[bridge_mask(root_mask(ns, b)) for b in REPS],
                                         topology=topology))
    # Check the run-transfer identity for all actual boundary-induced lists
    # and endpoint colors. The general parity argument remains a paper proof.
    transfer = []
    for mask in range(16):
        allowed = [c for c in range(4) if mask >> c & 1]
        if len(allowed) < 2:
            continue
        def accepts(length, left, right):
            possible = {left}
            for _ in range(length):
                possible = {c for c in allowed if any(c != d for d in possible)}
            return any(c != right for c in possible)
        odd = [accepts(1, x, y) for x, y in product(range(4), repeat=2)]
        even = [accepts(2, x, y) for x, y in product(range(4), repeat=2)]
        for length in (3, 4, 5, 6):
            assert [accepts(length, x, y) for x, y in product(range(4), repeat=2)] == (odd if length % 2 else even)
        transfer.append(dict(allowed_mask=mask, odd=odd, even=even))
    # Independent checks on the prior corpus: variable attachments really occur,
    # but in this corpus endpoint compression preserves the bridge interface.
    prior = json.loads(PRIOR.read_text())
    nonconstant = []
    for ci, context in enumerate(prior['contexts']):
        row = prior['paths'][context['path']]
        ns = row['neighborhoods']
        assert len({tuple(n) for n in ns[:-1]}) <= 2
        runs = 1 + sum(x != y for x, y in zip(ns[:-2], ns[1:-1]))
        assert runs <= 2
        assert row['bridge_masks'] == [bridge_mask(root_mask([ns[0], ns[-1]], b)) for b in REPS]
        if runs > 1:
            nonconstant.append(ci)
    counts['prior_nonconstant_contexts'] = len(nonconstant)
    assert dict(counts) == dict(palette_switch_obstructions=120,
                               three_run_obstructions=20, two_run_minors=20,
                               two_run_disk=8, two_run_normal_forms=8,
                               repeated_first_run_obstructions=8,
                               prior_nonconstant_contexts=32)
    dependencies = ['c5_triangle_path_reduction', 'c5_root_interfaces',
                    'c5_triangle_branches', 'c5_tree_cores', 'c5_odd_join_cores',
                    'c5_cell_enumerator', 'c5_disk_deletions', 'local_closure',
                    'boundary_relations']
    return dict(schema=1, scope=__doc__, fixed_pattern=Q, counts=dict(sorted(counts.items())),
                source_sha256={f'scripts/{name}.py': sha(ROOT / 'scripts' / f'{name}.py')
                               for name in dependencies},
                input_sha256={str(p.relative_to(ROOT)): sha(p) for p in (BASE, PRIOR)},
                obstructions=obstructions, two_run_minors=two_runs,
                normal_forms=normal_forms, transfer_checks=transfer,
                prior_nonconstant_contexts=nonconstant)


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
