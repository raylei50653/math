#!/usr/bin/env python3
"""Deterministic exhaustive labelled C5-supergraph search; no 4CT oracle.

Run: uv run --with networkx==3.5 python scripts/search_boundary.py
JSON certificates are data, not trusted proofs. Lean replay is generated separately.
"""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import networkx as nx

CYCLE = tuple(sorted({tuple(sorted((i, (i + 1) % 5))) for i in range(5)}))

def normalize(c):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in c)

def canonical(c):
    return min(normalize(tuple(c[(r + s*i) % 5] for i in range(5)))
               for r in range(5) for s in (1, -1))

COLORINGS = tuple(c for c in it.product(range(4), repeat=5)
                  if all(c[u] != c[v] for u, v in CYCLE))
REPS = tuple(sorted({normalize(c) for c in COLORINGS}))

def raw_mask(colors):
    accepted = set(colors)
    return sum(1 << i for i,c in enumerate(COLORINGS) if c in accepted)

def sigma(n, edges):
    result = []
    for b in REPS:
        for inside in it.product(range(4), repeat=n-5):
            c = b + inside
            if all(c[u] != c[v] for u, v in edges):
                result.append(b)
                break
    return tuple(result)

def planar_data(n, edges):
    g = nx.Graph()
    g.add_nodes_from(range(n))
    g.add_edges_from(edges)
    planar, emb = nx.check_planarity(g)
    if not planar:
        return None
    faces, seen = [], set()
    for u in range(n):
        for v in emb.neighbors_cw_order(u):
            if (u, v) not in seen:
                faces.append(emb.traverse_face(u, v, seen))
    apex = g.copy()
    apex.add_edges_from((n, i) for i in range(5))
    # Computational cofacial-cycle test; its topological equivalence is not a Lean theorem.
    disk = nx.check_planarity(apex)[0]
    return g, emb, sorted(faces), disk

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-n', type=int, default=6)
    parser.add_argument('--output', default='artifacts/boundary')
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    levels = ['planar_C5', 'cofacial_C5', 'induced_C5', 'interior_degree_ge_5',
              'boundary_degree_ge_4', 'apex_triangulation', 'apex_5_connected']
    counts = {k: {'graphs': 0, 'bad': 0} for k in levels}
    independent = {k: {'graphs': 0, 'bad': 0} for k in levels}
    per_n, bads = {}, []
    for n in range(5, args.max_n+1):
        optional = tuple(e for e in it.combinations(range(n), 2) if e not in CYCLE)
        per_n[n] = {'examined': 0, 'planar': 0, 'bad': 0}
        for mask in range(1 << len(optional)):
            per_n[n]['examined'] += 1
            edges = tuple(sorted(CYCLE + tuple(e for j, e in enumerate(optional) if mask >> j & 1)))
            if len(edges) > 3*n-6:
                continue
            data = planar_data(n, edges)
            if data is None:
                continue
            g, emb, faces, disk = data
            per_n[n]['planar'] += 1
            s = sigma(n, edges)
            bad = bool(s) and all(len(set(b)) == 4 for b in s)
            per_n[n]['bad'] += bad
            flags = [True, disk, all(u >= 5 or v >= 5 or (u,v) in CYCLE for u,v in edges),
                     all(g.degree(v) >= 5 for v in range(5,n)),
                     all(g.degree(v) >= 4 for v in range(5)),
                     disk and len(edges)+5 == 3*(n+1)-6,
                     False]
            if disk and min(dict(g.degree()).values()) >= 4:
                apex = g.copy()
                apex.add_edges_from((n,i) for i in range(5))
                flags[-1] = nx.node_connectivity(apex) >= 5
            keep = True
            for name, flag in zip(levels, flags):
                if flag:
                    independent[name]['graphs'] += 1
                    independent[name]['bad'] += bad
                keep &= flag
                if keep:
                    counts[name]['graphs'] += 1
                    counts[name]['bad'] += bad
            if bad:
                full = [c for c in COLORINGS if normalize(c) in s]
                cert = {'n': n, 'edges': edges, 'boundary': list(range(5)),
                        'sigma': full, 'color_orbits': s,
                        'sigma_bits_hex': format(raw_mask(full), '060x'),
                        'dihedral_orbits': sorted({canonical(b) for b in s}),
                        'rotation': [list(emb.neighbors_cw_order(v)) for v in range(n)],
                        'faces': faces, 'cofacial_test': disk,
                        'constraints': dict(zip(levels, flags))}
                cert['sha256'] = hashlib.sha256(json.dumps(cert, sort_keys=True, separators=(',',':')).encode()).hexdigest()
                bads.append(cert)
        print(n, per_n[n], flush=True)
    bads.sort(key=lambda c: (c['n'],len(c['edges']),c['edges']))
    (out/'bad_certificates.jsonl').write_text(''.join(json.dumps(c, sort_keys=True,separators=(',',':'))+'\n' for c in bads))
    summary = {'networkx': nx.__version__, 'max_n': args.max_n, 'per_n': per_n,
               'c5': {'count':len(COLORINGS), 'color_reps':REPS,
                      'raw_bit_order':COLORINGS,
                      'dihedral_reps':sorted({canonical(c) for c in COLORINGS})},
               'cumulative_constraints': counts, 'independent_constraints': independent,
               'minimal_bad': bads[0] if bads else None}
    # A concrete context showing loss of alignment after pointwise D5 quotient.
    disks = []
    optional = tuple(e for e in it.combinations(range(5),2) if e not in CYCLE)
    for mask in range(1 << len(optional)):
        edges = tuple(sorted(CYCLE + tuple(e for j,e in enumerate(optional) if mask >> j & 1)))
        data = planar_data(5,edges)
        if data and data[-1]:
            s = set(sigma(5,edges))
            disks.append((edges,s,{canonical(b) for b in s}))
    for a in disks:
        for b in disks:
            union = tuple(sorted(set(a[0]) | set(b[0])))
            data = planar_data(5,union)
            if a[2] == b[2] and data and a[1]&b[1] and all(len(set(c))==4 for c in a[1]&b[1]):
                summary['composition_witness'] = {'left':a[0], 'right':b[0],
                    'left_sigma': sorted(a[1]), 'right_sigma':sorted(b[1]),
                    'intersection':sorted(a[1]&b[1]), 'abstract_both':sorted(a[2])}
                break
        if 'composition_witness' in summary:
            break
    (out/'summary.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
    print('BAD certificates:',len(bads), 'output:',out, flush=True)

if __name__ == '__main__':
    main()
