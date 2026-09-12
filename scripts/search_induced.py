#!/usr/bin/env python3
"""Exhaustive induced-C5 edge subsets within the planar edge bound.

Bit-parallel full colorings with canonical boundary colors; empty extension sets
prune only uncolorable supergraphs. Planarity is queried only for potential BADs.
"""
import argparse
import itertools as it
import json
import math
from pathlib import Path

from construct_boundary import certificate
from search_boundary import CYCLE, REPS, planar_data


def scan(n):
    optional = [e for e in it.combinations(range(n), 2) if e[1] >= 5]
    capacity = min(len(optional), 3*n - 11)
    colors = [b + c for b in REPS for c in it.product(range(4), repeat=n-5)]
    masks = [sum(1 << i for i, c in enumerate(colors) if c[u] != c[v])
             for u, v in optional]
    three = sum(1 << i for i, c in enumerate(colors) if len(set(c[:5])) <= 3)
    counts = dict(n=n, all_subsets=2**len(optional),
                  within_planar_edge_bound=sum(math.comb(len(optional), k)
                                               for k in range(capacity+1)),
                  visited=0, uncolorable_pruned=0, potential_bad=0, planar_bad=0)
    found = []

    def visit(start, state, selected):
        counts['visited'] += 1
        room = capacity - len(selected)
        if not state:
            counts['uncolorable_pruned'] += sum(
                math.comb(len(optional)-start, k) for k in range(1, room+1)
                if k <= len(optional)-start)
            return
        if not state & three:
            counts['potential_bad'] += 1
            edges = tuple(sorted(CYCLE + tuple(optional[i] for i in selected)))
            if planar_data(n, edges) is not None:
                counts['planar_bad'] += 1
                block = 4**(n-5)
                s = tuple(b for j, b in enumerate(REPS)
                          if (state >> (block*j)) & ((1 << block)-1))
                found.append(certificate(n, edges, s))
                return
        if room:
            for i in range(start, len(optional)):
                visit(i+1, state & masks[i], selected + (i,))
                if found:
                    return

    visit(0, (1 << len(colors))-1, ())
    counts['completed'] = not found
    if not found:
        assert counts['visited'] + counts['uncolorable_pruned'] == counts['within_planar_edge_bound']
    return counts, found


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--max-n', type=int, default=9)
    p.add_argument('--output', default='artifacts/induced')
    a = p.parse_args()
    out = Path(a.output)
    out.mkdir(parents=True, exist_ok=True)
    results, certs = [], []
    for n in range(5, a.max_n+1):
        counts, certs = scan(n)
        results.append(counts)
        print(counts, flush=True)
        if certs:
            break
    (out / 'summary.json').write_text(json.dumps(results, sort_keys=True, indent=2)+'\n')
    (out / 'bad_certificates.jsonl').write_text(''.join(
        json.dumps(c, sort_keys=True, separators=(',', ':'))+'\n' for c in certs))


if __name__ == '__main__':
    main()
