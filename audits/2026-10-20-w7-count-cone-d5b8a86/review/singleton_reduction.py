#!/usr/bin/env python3
"""Exploratory exact facial reduction from singleton half-rows, without LP.

At every step 2 Z_i=sum(X_j) over the columns through each of i's three
half-rows. A singleton half-row gives X_j=2Z_i, hence Z_k>=Z_i for
each state k met by j. Within an SCC those inequalities are equalities;
any other column through such an equality row is zero by nonnegativity.
All arithmetic/reductions are exact integers. This is not a cone verdict.
"""
from pathlib import Path
from collections import Counter, defaultdict
import argparse, gzip, hashlib, json, time


def components(vertices, edges):
    # Iterative Kosaraju, with isolated vertices retained.
    adj = {v: [] for v in vertices}
    rev = {v: [] for v in vertices}
    for a, b in edges:
        adj[a].append(b)
        rev[b].append(a)
    seen, order = set(), []
    for v in vertices:
        if v in seen:
            continue
        seen.add(v)
        stack = [(v, iter(adj[v]))]
        while stack:
            node, children = stack[-1]
            try:
                w = next(children)
            except StopIteration:
                stack.pop()
                order.append(node)
                continue
            if w not in seen:
                seen.add(w)
                stack.append((w, iter(adj[w])))
    result = {}
    for v in reversed(order):
        if v in result:
            continue
        result[v] = v
        stack = [v]
        while stack:
            for w in rev[stack.pop()]:
                if w not in result:
                    result[w] = v
                    stack.append(w)
    return result


def inspect(source):
    source = Path(source)
    payload = (source / 'orbits.json.gz').read_bytes()
    obj = json.loads(gzip.decompress(payload))
    rowids = dict(obj['rowids'])
    columns = obj['columns']
    live = set(obj['live'])
    active = set(range(len(columns)))
    history = []
    while True:
        byrow = defaultdict(list)
        for j in sorted(active):
            for r in columns[j]:
                byrow[r].append(j)
        # Existing support closure is repeated after every new exact zero.
        unsupported = {i for r, i in rowids.items() if i in live and not byrow[r]}
        if unsupported:
            live -= unsupported
            removed = {j for j in active if any(rowids[r] not in live for r in columns[j])}
            active -= removed
            history.append({'rule': 'support', 'zero_states': sorted(unsupported),
                            'zero_columns': sorted(removed)})
            continue
        singles = [(r, js[0]) for r, js in byrow.items() if len(js) == 1]
        edges = [(rowids[r], rowids[t]) for r, j in singles for t in columns[j]]
        scc = components(sorted(live), edges)
        removed = set()
        explanations = []
        for r, j in singles:
            i = rowids[r]
            for t in columns[j]:
                k = rowids[t]
                if scc[k] == scc[i]:
                    for x in byrow[t]:
                        if x != j:
                            removed.add(x)
                            explanations.append([x, r, j, t])
        if not removed:
            return {
                'status': 'exact singleton facial-reduction exploration; no LP verdict',
                'input_sha256': hashlib.sha256(payload).hexdigest(),
                'initial_live_states': len(obj['live']),
                'initial_columns': len(columns),
                'final_live_states': len(live),
                'final_columns': len(active),
                'final_singleton_rows': len(singles),
                'final_scc_sizes': dict(sorted(Counter(Counter(scc.values()).values()).items())),
                'target_survival': {str(i): i in live for i in (44459, 44466)},
                'rounds': history,
            }
        active -= removed
        history.append({'rule': 'singleton dominance SCC', 'zero_columns': sorted(removed),
                        'local_explanations': explanations})


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[2] /
                   '2026-10-20-r6-941-j1-five-edge-417732f/counting')
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    start = time.monotonic()
    out = inspect(args.source)
    if args.output:
        with args.output.open('x') as f:
            json.dump(out, f, indent=2)
            f.write('\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'rounds'} |
                     {'rounds_count': len(out['rounds']), 'seconds': time.monotonic()-start}, sort_keys=True))


if __name__ == '__main__':
    main()
