#!/usr/bin/env python3
"""Independent small-cap calibration; not an outside-K realization search.

Enumerate all simple sphere triangulations through 11 vertices using the frozen
vendored plantri 5.8. Deleting each degree-b apex gives every simple triangulated
b-disk, up to repeated rootings, with t=n-b-1. Retain exactly those with all t
interior degrees >=5. This controls the small-patch lemma, not its global
catalogue/minimality premises.
"""
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
VENDOR = ROOT / 'artifacts/c5_excess_two_independent_search/vendor/plantri.c'
BIN = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/tmp/plantri-c5-small-separators-01a12ffa')
OUT = pathlib.Path(__file__).with_name('small_caps.json')

def parse(line):
    nstr, rest = line.split(maxsplit=1)
    n = int(nstr)
    rotation = [[ord(v)-ord('a') for v in s] for s in rest.strip().split(',')]
    assert len(rotation) == n
    adj = [set(r) for r in rotation]
    assert sum(map(len, adj)) == 6*n-12
    assert all(u != v and u in adj[v] for u in range(n) for v in adj[u])
    for u, neighbors in enumerate(rotation):
        assert len(neighbors) == len(adj[u])
        assert all(neighbors[(i+1)%len(neighbors)] in adj[v] for i,v in enumerate(neighbors))
    return adj

records = []
buckets = {(b,t): {'rooted_candidates': 0, 'min_inner_degree_5': 0, 'accepted_examples': []}
           for b,limit in [(4,3),(5,5)] for t in range(limit+1)}
for n in range(5,12):
    run = subprocess.run([str(BIN), '-a', str(n)], check=True, capture_output=True, text=True)
    lines = run.stdout.splitlines()
    records.append({'n': n, 'triangulations': len(lines), 'ascii_sha256': hashlib.sha256(run.stdout.encode()).hexdigest(), 'stderr': run.stderr.strip()})
    for index,line in enumerate(lines):
        adj = parse(line)
        for apex,neighbors in enumerate(adj):
            b = len(neighbors)
            t = n-b-1
            if (b,t) not in buckets:
                continue
            result = buckets[b,t]
            result['rooted_candidates'] += 1
            interior = set(range(n)) - neighbors - {apex}
            assert len(interior) == t
            if any(len(adj[v]) < 5 for v in interior):
                continue
            result['min_inner_degree_5'] += 1
            if len(result['accepted_examples']) < 3:
                result['accepted_examples'].append({'triangulation_index': index, 'apex': apex, 'rotation_ascii': line})
            assert t == 0 or (b,t) == (5,1), (n,index,apex)
            if t == 1:
                center, = interior
                assert adj[center] == neighbors
                assert all(len(adj[v] & neighbors) == 2 for v in neighbors)

assert buckets[5,1]['min_inner_degree_5'] > 0
report = {'status': 'PASS', 'scope': 'All rooted simple triangulated C4 disks with t<=3 and C5 disks with t<=5; duplicate rootings retained.',
          'unbounded_status': 'Finite calibration only. Global minimality, complete-relation replacement, and the catalogue premise are paper inputs.',
          'generator': {'path': str(VENDOR.relative_to(ROOT)), 'sha256': hashlib.sha256(VENDOR.read_bytes()).hexdigest(), 'binary_sha256': hashlib.sha256(BIN.read_bytes()).hexdigest(), 'arguments': ['-a', 'n']},
          'enumeration': records,
          'caps': [{'boundary_length':b, 'interior_count':t, **r} for (b,t),r in sorted(buckets.items())]}
OUT.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({'status': report['status'], 'output': str(OUT), 'counts':[{k:r[k] for k in ('boundary_length','interior_count','rooted_candidates','min_inner_degree_5')} for r in report['caps']]}))
