#!/usr/bin/env python3
"""Bounded exact seven-list experiments; no original 941 realization is claimed."""
import argparse
from collections import Counter, deque
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = '30dde27293b5d3ad63c75fae73cda5be96db705b'
C = ['n', 'h', 'L', 'u1', 'u2', 'u3', 'u4']
COLORS = range(4)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def source_module():
    manifest = json.loads((HERE / 'BASE.json').read_text())
    require(manifest['base'] == BASE, 'exclusive BASE changed')
    for row in manifest['inputs']:
        raw = (HERE / 'frozen' / row['frozen']).read_bytes()
        require(len(raw) == row['bytes'] and sha256(raw).hexdigest() == row['sha256'],
                'frozen input changed: ' + row['path'])
    spec = importlib.util.spec_from_file_location('frozen_profile', HERE / 'frozen/check.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def wheel_kernel():
    return [(r, inner) for r in COLORS
            for inner in product([c for c in COLORS if c != r], repeat=7)
            if all(inner[i] != inner[(i + 1) % 7] for i in range(7))]


KERNEL = wheel_kernel()
ALL = (1 << len(KERNEL)) - 1
HUB = [sum(1 << j for j, (r, _) in enumerate(KERNEL) if r == c) for c in COLORS]
SITE = [[sum(1 << j for j, (_, inner) in enumerate(KERNEL) if inner[i] == c)
         for c in COLORS] for i in range(7)]
DOMAIN = [[sum(SITE[i][c] for c in COLORS if mask & (1 << c))
           for mask in range(16)] for i in range(7)]


def fibre(lists):
    result = ALL
    for i, mask in enumerate(lists):
        result &= DOMAIN[i][mask]
    return result


def classify(domains):
    """Exact obstruction certificate for a C7 with lists of size at most two."""
    if any(not d for d in domains):
        return 'initial_empty', []
    require(all(d.bit_count() <= 2 for d in domains), 'classifier domain is too large')
    domains = list(domains)
    queue = deque(i for i, d in enumerate(domains) if d.bit_count() == 1)
    trace = []
    while queue:
        i = queue.popleft()
        require(domains[i].bit_count() == 1, 'invalid singleton queue')
        for j in ((i - 1) % 7, (i + 1) % 7):
            updated = domains[j] & ~domains[i]
            if updated != domains[j]:
                trace.append([i, j, domains[i], domains[j], updated])
                domains[j] = updated
                if not updated:
                    return 'singleton_propagation_conflict', trace
                if updated.bit_count() == 1:
                    queue.append(j)
    if all(d == domains[0] and d.bit_count() == 2 for d in domains):
        return 'uniform_two_color_odd_cycle', trace
    return 'colorable', trace


def direct_count(graph, sigma):
    def visit(assigned):
        remaining = set(graph) - assigned.keys()
        if not remaining:
            return 1
        domains = {v: set(COLORS) - {assigned[w] for w in graph[v] if w in assigned}
                   for v in remaining}
        v = min(remaining, key=lambda x: (len(domains[x]), x))
        return sum(visit(assigned | {v: color}) for color in sorted(domains[v]))
    return visit(sigma)


def formal_domains():
    # Exhaustive six-symbol domain over three colors; no collar provenance implied.
    masks = [1, 2, 4, 3, 5, 6]
    cycle = [inner for r, inner in KERNEL if r == 3]
    require(len(cycle) == 126, 'fixed-hub kernel size changed')
    site = [[sum(1 << j for j, inner in enumerate(cycle) if mask & (1 << inner[i]))
             for mask in masks] for i in range(7)]
    counts, types, examples = [], Counter(), {}
    for codes in product(range(6), repeat=7):
        bitset = (1 << 126) - 1
        for i, code in enumerate(codes):
            bitset &= site[i][code]
        count = bitset.bit_count()
        domains = [masks[code] for code in codes]
        kind, trace = classify(domains)
        require((kind == 'colorable') == (count > 0), 'formal obstruction classification failed')
        counts.append(count)
        types[kind] += 1
        if kind not in examples:
            examples[kind] = {'lists': [decode(d) for d in domains],
                              'full_lifts_for_fixed_hub_3': count,
                              'singleton_trace_masks': trace}
    require(len(counts) == 6 ** 7, 'formal domain coverage changed')
    # With empty lists allowed, omitted tuples all have zero fibres by inspection.
    return {'domain_alphabet': [decode(d) for d in masks],
            'enumeration_order': 'itertools.product(range(6), repeat=7), C order n,h,L,u1,u2,u3,u4',
            'fixed_hub': 3, 'nonempty_domain_tuples': len(counts),
            'counts_in_enumeration_order': counts,
            'classification': dict(sorted(types.items())), 'examples': examples,
            'zero_fibres': counts.count(0),
            'additional_tuples_with_an_initial_empty_domain': 7 ** 7 - 6 ** 7,
            'additional_tuple_fibre_count': 0,
            'legal_S_color_rows': False, 'original_941_sources': False}


def decode(mask):
    return [c for c in COLORS if mask & (1 << c)]


def mutations(lists, keep):
    smaller, larger = [], []
    for i in range(7):
        for c in COLORS:
            other = list(lists)
            if lists[i] & (1 << c):
                other[i] &= ~(1 << c)
                modified = fibre(other)
                require(modified & ~keep == 0, 'shrinking created a lift')
                smaller.append([i, c, modified.bit_count()])
            else:
                other[i] |= 1 << c
                modified = fibre(other)
                require(keep & ~modified == 0, 'expanding lost a lift')
                larger.append([i, c, modified.bit_count()])
    require(len(smaller) + len(larger) == 28, 'single-site variation coverage changed')
    return smaller, larger


def local_collars(source):
    rows, totals, strata = [], Counter(), {}
    examples = {}
    by_hub_obstruction = Counter()
    for profile, width in [(0, 6), (1, 5)]:
        count_rows = [[0] * width]
        count_rows += [[int(i == j) for i in range(width)] for j in range(width)]
        for lengths in count_rows:
            data, graph = source.collar(profile, lengths, with_graph=True)
            boundary = data['boundary']
            key = f'profile_{profile}_K{sum(lengths)}'
            if key not in strata:
                strata[key] = Counter()
            for colors in source.canonical_cycle_colors(len(boundary)):
                sigma = dict(zip(boundary, colors))
                lists = [sum(1 << c for c in set(COLORS) -
                             {sigma[s] for s in graph[t] if s in sigma}) for t in C]
                require(all(d.bit_count() <= 2 for d in lists), 'proper S did not give size-at-most-two lists')
                keep = fibre(lists)
                count = keep.bit_count()
                direct = direct_count(graph, sigma)
                require(count == direct, 'generic graph count lost full lifts or empty fibre')
                hubs = [(keep & mask).bit_count() for mask in HUB]
                require(sum(hubs) == count, 'hub partition failed')
                obstruction = []
                for r in COLORS:
                    domains = [d & ~(1 << r) for d in lists]
                    kind, _ = classify(domains)
                    require((kind == 'colorable') == (hubs[r] > 0), 'collar obstruction failed')
                    obstruction.append(kind)
                    by_hub_obstruction[kind] += 1
                # An odd properly colored rim uses all three colors other than its hub.
                avoid_rim, force_rim = [], []
                for c in COLORS:
                    absent = keep
                    for i in range(7):
                        absent &= ~SITE[i][c]
                    require(absent == keep & HUB[c], 'rim-forbid/hub identity failed')
                    avoid_rim.append(absent.bit_count())
                    force_rim.append((keep & ~absent).bit_count())
                    require(force_rim[c] == count - hubs[c], 'rim force identity failed')
                site_counts = [[(keep & SITE[i][c]).bit_count() for c in COLORS] for i in range(7)]
                smaller, larger = mutations(lists, keep)
                row = {'profile': profile, 'H_lengths': lengths,
                       'ordered_S_vertices': boundary, 'ordered_S_colors': colors,
                       'lists': [decode(d) for d in lists],
                       'full_lifts': count, 'fixed_hub_lifts': hubs,
                       'fixed_hub_obstruction': obstruction,
                       'forbid_rim_color_lifts': avoid_rim,
                       'force_rim_color_to_occur_lifts': force_rim,
                       'fixed_rim_vertex_color_lifts': site_counts,
                       'single_list_delete_color': smaller,
                       'single_list_add_color': larger}
                rows.append(row)
                tally = Counter({'rows': 1, 'full_lifts': count, 'zero_fibres': int(count == 0),
                                 'marginal_accepts_but_no_lift': int(count == 0 and
                                       any(k != 'initial_empty' for k in obstruction)),
                                 'hub_color0_only_rejects_a_nonempty_fibre': int(count > 0 and hubs[0] == 0),
                                 'single_list_shrinks': len(smaller),
                                 'shrinks_losing_lifts': sum(n < count for _, _, n in smaller),
                                 'shrinks_killing_nonempty_fibre': sum(count > 0 and n == 0 for _, _, n in smaller),
                                 'single_list_expands': len(larger),
                                 'expands_gaining_lifts': sum(n > count for _, _, n in larger),
                                 'expands_reviving_empty_fibre': sum(count == 0 and n > 0 for _, _, n in larger)})
                totals.update(tally)
                strata[key].update(tally)
                conditions = {
                    'shared_hub_nonempty_but_no_joint_lift': tally['marginal_accepts_but_no_lift'],
                    'fixing_hub_0_loses_every_lift': tally['hub_color0_only_rejects_a_nonempty_fibre'],
                    'one_list_delete_color_kills_all_lifts': tally['shrinks_killing_nonempty_fibre'],
                    'one_list_add_color_revives_empty_fibre': tally['expands_reviving_empty_fibre'],
                }
                for name, yes in conditions.items():
                    if yes and name not in examples:
                        examples[name] = row
    require(len(rows) == 6655, 'K<=1 legal local sigma coverage changed')
    return {'rows': rows, 'totals': dict(totals),
            'strata': {k: dict(v) for k, v in strata.items()},
            'fixed_hub_obstruction_histogram': dict(sorted(by_hub_obstruction.items())),
            'examples': examples,
            'full_original_941_source_triggered': False,
            'list_mutations_are_formal_and_need_not_have_a_legal_same_S_realization': True}


def negative_controls():
    # Same shared hub, nonempty lists, and every edge pair feasible are insufficient.
    # All rim lists are {0,1}; every hub outside {0,1} passes marginals, C7 cannot alternate.
    uniform = [3] * 7
    require(fibre(uniform) == 0, 'uniform odd-cycle negative control failed')
    require(all((a & ~(1 << r)) for a in uniform for r in [2, 3]), 'shared hub control failed')
    require(all(any(a != b for a in decode(uniform[i]) for b in decode(uniform[(i + 1) % 7]))
                for i in range(7)), 'edgewise control failed')
    # Locally nonempty domains can fail by a forced chain rather than uniform parity.
    chain = [1, 3, 3, 1, 3, 3, 3]
    require(fibre(chain) == 0, 'singleton chain negative control failed')
    require(classify(chain)[0] == 'singleton_propagation_conflict', 'chain classification failed')
    # Swapping a single rim color without retaining full fibre is not a legal rule.
    keep = fibre([15] * 7)
    require(keep.bit_count() == 504, 'unrestricted positive control failed')
    return {'uniform_two_color_lists': [decode(d) for d in uniform],
            'uniform_full_lifts': 0, 'shared_acceptable_hubs': [2, 3],
            'every_neighbor_pair_separately_feasible': True,
            'singleton_chain_lists': [decode(d) for d in chain],
            'singleton_chain_full_lifts': 0,
            'unrestricted_positive_full_lifts': 504}


def compute():
    source = source_module()
    require(len(KERNEL) == 504, 'full 8-point wheel kernel changed')
    return {'base': BASE, 'inner_order': ['R'] + C,
            'unrestricted_inner_candidates': [[r, *inner] for r, inner in KERNEL],
            'formal_fixed_hub_domains': formal_domains(),
            'legal_local_collar_sigma': local_collars(source),
            'negative_controls': negative_controls(),
            'full_941_source_realizations': 0, 'source_exclusions': [],
            'smaller_legal_replacement_proved': False, 'new_Lean': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    result = compute()
    path = HERE / 'certificate.json'
    if args.build:
        with path.open('x') as stream:
            json.dump(result, stream, sort_keys=True, separators=(',', ':'))
            stream.write('\n')
    require(json.loads(path.read_text()) == result, 'certificate changed')
    print(json.dumps({'result': 'PASS', 'base': BASE,
                      'formal_domain_tuples': result['formal_fixed_hub_domains']['nonempty_domain_tuples'],
                      'legal_local_sigma_rows': len(result['legal_local_collar_sigma']['rows']),
                      'legal_local_summary': result['legal_local_collar_sigma']['totals'],
                      'full_941_source_realizations': 0, 'source_exclusions': []}, sort_keys=True))


if __name__ == '__main__':
    main()
