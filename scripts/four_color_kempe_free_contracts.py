#!/usr/bin/env python3
"""Kempe-free C-reducibility screen of the 633 RSST configurations (proposal KF).

A contract X follows RSST's rules (1<=|X|<=4, no ring edge, sparse, triad when
|X|=4).  X is Kempe-free when the ring colourings of the free completion
modulo X form a non-empty subset of A(K), the ring colourings that extend
directly; no Kempe change is then needed after the reduction.

Inputs are the ancillary files of arXiv:1401.6481 (sha256 checked):
  curl -o unavoidable.conf https://arxiv.org/src/1401.6481v1/anc/unavoidable.conf
  curl -o reduce.c https://arxiv.org/src/1401.6481v1/anc/reduce.c

Checks: (1) |A(K)| equals the RSST extending-colouring count for all 633;
(2) RSST's own checkcontract, run on C_0 instead of the Kempe-closed set, agrees
on the 384 given contracts; (3) an unpruned Python enumeration of every
contract agrees for ring size <= --brute-max-ring; (4) wheel controls W3-W6;
(5) every reported RSST-contract kill witness is replayed in Python.
No four-colour-theorem oracle is used.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CPP = ROOT / 'scripts/cpp/kempe_free_contracts.cpp'
CONF_SHA256 = '1c92fc280a9b384f736b94077fc59aac75e3d830d441ffd2d18683ee4b524e84'
REDUCE_SHA256 = 'f49caf1bffe3721f2c45c9fadcf13f45f058a4c744d858ed35d6c2bf6872ec77'

CONTROLS = '''W3
4 3 0 0
 0
 1 3 2 4 3
 2 3 3 4 1
 3 3 1 4 2
 4 3 1 2 3
 0 0 0 0

W4
5 4 0 0
 0
 1 3 2 5 4
 2 3 3 5 1
 3 3 4 5 2
 4 3 1 5 3
 5 4 1 2 3 4
 0 0 0 0 0

W5
6 5 0 0
 0
 1 3 2 6 5
 2 3 3 6 1
 3 3 4 6 2
 4 3 5 6 3
 5 3 1 6 4
 6 5 1 2 3 4 5
 0 0 0 0 0 0

W6
7 6 0 0
 0
 1 3 2 7 6
 2 3 3 7 1
 3 3 4 7 2
 4 3 5 7 3
 5 3 6 7 4
 6 3 1 7 5
 7 6 1 2 3 4 5 6
 0 0 0 0 0 0 0
'''
# Expected minimum Kempe-free contract size (0 = none).
CONTROL_EXPECT = {'W3': 1, 'W4': 2, 'W5': 0, 'W6': 0}


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def parse_conf(text):
    lines = text.split('\n')
    i, out = 0, []
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        name = lines[i].strip()
        n, r, ext, maxcons = map(int, lines[i + 1].split())
        con = list(map(int, lines[i + 2].split()))
        contract = [(con[1 + 2 * j] - 1, con[2 + 2 * j] - 1) for j in range(con[0])]
        adj = []
        for j in range(n):
            t = list(map(int, lines[i + 3 + j].split()))
            assert t[0] == j + 1 and len(t) == 2 + t[1], (name, j)
            adj.append([w - 1 for w in t[2:]])
        k, seen = i + 3 + n, 0
        while seen < n:
            seen += len(lines[k].split())
            k += 1
        out.append(dict(name=name, n=n, r=r, ext=ext, maxcons=maxcons, contract=contract, adj=adj))
        i = k
    return out


def structure(c):
    n, r, adj = c['n'], c['r'], c['adj']
    eid, edges = {}, []
    for v in range(n):
        for u in adj[v]:
            key = (min(u, v), max(u, v))
            if key not in eid:
                eid[key] = len(edges)
                edges.append(key)
    ring_edges = {eid[(min(i, (i + 1) % r), max(i, (i + 1) % r))] for i in range(r)}
    tris = set()
    for v in range(n):
        d = len(adj[v])
        for h in range(d):
            if v < r and h == d - 1:
                continue
            tris.add(tuple(sorted((v, adj[v][h], adj[v][(h + 1) % d]))))
    tri_edges = [(eid[(a, b)], eid[(b, cc)], eid[(a, cc)]) for a, b, cc in sorted(tris)]
    assert len(edges) == 3 * n - 3 - r and len(tri_edges) == 2 * n - 2 - r, c['name']
    return eid, edges, ring_edges, tri_edges


def triad_ok(c, edges, X):
    ends = [x for e in X for x in edges[e]]
    for v in range(c['r'], c['n']):
        nb = set(c['adj'][v])
        if sum(u in ends for u in nb) < 3:
            continue
        if len(nb) >= 6 or any(x not in nb for x in ends):
            return True
    return False


def valid_contracts(c, edges, ring_edges, tri_edges):
    tri_of = defaultdict(list)
    for t, es in enumerate(tri_edges):
        for e in es:
            tri_of[e].append(t)
    cand = [e for e in range(len(edges)) if e not in ring_edges]
    out = []
    for size in range(1, 5):
        for X in combinations(cand, size):
            hits = [t for e in X for t in tri_of[e]]
            if len(hits) != len(set(hits)):
                continue
            if size == 4 and not triad_ok(c, edges, X):
                continue
            out.append(frozenset(X))
    return out


def brute(c):
    """Unpruned enumeration: every colouring with <=4 sparse monochromatic edges."""
    n, r, adj = c['n'], c['r'], c['adj']
    eid, edges, ring_edges, tri_edges = structure(c)
    tri_of = defaultdict(list)
    for t, es in enumerate(tri_edges):
        for e in es:
            tri_of[e].append(t)
    back = [[(u, eid[(min(u, v), max(u, v))]) for u in adj[v] if u < v] for v in range(n)]
    col = [0] * n
    tri_mono = [0] * len(tri_edges)
    seen = defaultdict(set)

    def dfs(v, mono, mx):
        if v == n:
            seen[frozenset(mono)].add(tuple(col[:r]))
            return
        top = min(mx + 1, 3) if v < r else 3
        for k in range(top + 1):
            if v == 0 and k != 0:
                continue
            new = [e for u, e in back[v] if col[u] == k]
            if any(e in ring_edges for e in new) or len(mono) + len(new) > 4:
                continue
            touched = [t for e in new for t in tri_of[e]]
            if any(tri_mono[t] for t in touched) or len(touched) != len(set(touched)):
                continue
            for t in touched:
                tri_mono[t] += 1
            col[v] = k
            dfs(v + 1, mono + new, max(mx, k) if v < r else mx)
            for t in touched:
                tri_mono[t] -= 1

    dfs(0, [], -1)
    A = seen[frozenset()]
    valid = valid_contracts(c, edges, ring_edges, tri_edges)
    by_valid, by_kf, by_vac = [0] * 4, [0] * 4, [0] * 4
    best = None
    for X in valid:
        s = len(X) - 1
        by_valid[s] += 1
        R = seen.get(X, set())
        if not R:
            by_vac[s] += 1
            continue
        bad = len(R - A)
        if bad == 0:
            by_kf[s] += 1
        if best is None or bad < best[0]:
            best = (bad, sorted(sorted((edges[e][0] + 1, edges[e][1] + 1) for e in X)))
    return dict(A=len(A), valid_by_size=by_valid, kempe_free_by_size=by_kf,
                vacuous_by_size=by_vac,
                fewest_bad=None if best is None else dict(bad=best[0], contract=best[1]))


def replay_witness(c, ring, X):
    """Ring colouring `ring` lies outside A(K) and extends with monochromatic set exactly X."""
    n, r, adj = c['n'], c['r'], c['adj']
    eid, edges, _, _ = structure(c)
    Xset = {eid[(min(u, v), max(u, v))] for u, v in X}
    col = [int(ch) for ch in ring] + [-1] * (n - r)

    def search(v, exact):
        if v == n:
            return True
        for k in range(4):
            ok = True
            for u in adj[v]:
                if u < v:
                    mono = col[u] == k
                    want = exact and eid[(min(u, v), max(u, v))] in Xset
                    if mono != want:
                        ok = False
                        break
            if ok:
                col[v] = k
                if search(v + 1, exact):
                    col[v] = -1
                    return True
        col[v] = -1
        return False

    return (not search(r, False)) and search(r, True)


def run_cpp(conf_path, threads, workdir):
    exe = Path(workdir) / 'kempe_free_contracts'
    subprocess.run(['g++', '-O2', '-std=c++17', '-pthread', '-o', str(exe), str(CPP)], check=True)
    out = subprocess.run([str(exe), str(conf_path), str(threads)], check=True,
                         capture_output=True, text=True).stdout
    return [json.loads(line) for line in out.splitlines() if line.strip()]


REDUCE_SUBS = [
    ('''      do
\t testmatch(ring, real, power, live, nchar);
      /* computes {\\cal M}_{i+1} from {\\cal M}_i, updates the bits of "real" */
      while (updatelive(live, ncodes, &nlive));
      /* computes {\\cal C}_{i+1} from {\\cal C}_i, updates "live" */
''', '''      (void) printf("\\nKFCONF %ld\\n", count + 1);
'''),
    ('''   if (!nlive) {
      if (!contract[0]) {
\t (void) printf("\\n");
\t return;
      } else {
\t (void) printf("         ***  ERROR: CONTRACT PROPOSED  ***\\n\\n");
\t exit(23);
      }
   }
   if (!contract[0]) {
      (void) printf("       ***  ERROR: NO CONTRACT PROPOSED  ***\\n\\n");
      exit(24);
   }
   if (nlive != contract[EDGES]) {
      (void) printf("       ***  ERROR: DISCREPANCY IN EXTERIOR SIZE  ***\\n\\n");
      exit(25);
   }
''', '''   if (!nlive) { (void) printf("KFRESULT EMPTYLIVE\\n"); return; }
   if (!contract[0]) { (void) printf("KFRESULT NOCONTRACT\\n"); return; }
'''),
    ('''\t    (void) printf("       ***  ERROR: INPUT CONTRACT IS INCORRECT  ***\\n\\n");
\t    exit(26);
''', '''\t    (void) printf("KFRESULT FAIL\\n");
\t    return;
'''),
]


def run_reduce_c0(reduce_path, conf_path, workdir):
    """RSST checkcontract with live = C_0: skip the Kempe (signed matching) iterations."""
    s = Path(reduce_path).read_text()
    for old, new in REDUCE_SUBS:
        assert s.count(old) == 1, old[:50]
        s = s.replace(old, new)
    old = '(void) printf("               ***  Contract confirmed  ***\\n\\n");'
    assert s.count(old) == 2
    s = s.replace(old, '(void) printf("KFRESULT PASS\\n");')
    src = Path(workdir) / 'reduce_c0.c'
    exe = Path(workdir) / 'reduce_c0'
    src.write_text(s)
    subprocess.run(['gcc', '-O2', '-std=gnu89', '-w', '-o', str(exe), str(src)], check=True)
    out = subprocess.run([str(exe), str(conf_path)], check=True, capture_output=True, text=True).stdout
    assert 'Reducibility of 633 configurations verified' in out
    results, index = {}, None
    for line in out.splitlines():
        if line.startswith('KFCONF'):
            index = int(line.split()[1])
        elif line.startswith('KFRESULT'):
            results[index] = line.split()[1]
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--conf', required=True, type=Path)
    ap.add_argument('--reduce-c', required=True, type=Path)
    ap.add_argument('--out-dir', required=True, type=Path)
    ap.add_argument('--threads', type=int, default=8)
    ap.add_argument('--brute-max-ring', type=int, default=9)
    args = ap.parse_args()
    assert digest(args.conf) == CONF_SHA256, 'unexpected unavoidable.conf'
    assert digest(args.reduce_c) == REDUCE_SHA256, 'unexpected reduce.c'
    confs = parse_conf(args.conf.read_text())
    assert len(confs) == 633
    args.out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        rows = run_cpp(args.conf, args.threads, tmp)
        ctl_path = Path(tmp) / 'controls.conf'
        ctl_path.write_text(CONTROLS)
        ctl_rows = {r['name']: r for r in run_cpp(ctl_path, 1, tmp)}
        rsst_c0 = run_reduce_c0(args.reduce_c, args.conf, tmp)
    assert [r['index'] for r in rows] == list(range(1, 634))
    checks = {}
    # (1) extending-colouring counts
    checks['A_equals_rsst_count'] = all(r['A'] == r['ext_claim'] == c['ext'] for r, c in zip(rows, confs))
    checks['no_proper_extension_of_bad_colouring'] = not any(r['proper_on_bad'] for r in rows)
    checks['rsst_contracts_valid_under_rules'] = all(r['rsst_contract_valid'] for r in rows)
    # (2) RSST checkcontract on C_0
    agree = []
    for r in rows:
        want = 'NOCONTRACT' if not r['rsst_contract'] else ('PASS' if r['rsst_contract_kempe_free'] else 'FAIL')
        agree.append(rsst_c0.get(r['index']) == want)
    checks['rsst_checkcontract_on_C0_agrees'] = all(agree)
    checks['rsst_checkcontract_on_C0_counts'] = {k: sum(v == k for v in rsst_c0.values())
                                                 for k in sorted(set(rsst_c0.values()))}
    # (3) unpruned Python enumeration for small rings, (4) controls
    brute_rows = {}
    for r, c in zip(rows, confs):
        if c['r'] <= args.brute_max_ring:
            b = brute(c)
            brute_rows[r['index']] = b
            assert b['A'] == r['A'], r['index']
            assert b['valid_by_size'] == r['valid_by_size'], r['index']
            assert b['kempe_free_by_size'] == r['kempe_free_by_size'], r['index']
            assert b['vacuous_by_size'] == r['vacuous_by_size'], r['index']
    checks['brute_force_agrees'] = dict(max_ring=args.brute_max_ring, configurations=len(brute_rows))
    controls = {}
    for c in parse_conf(CONTROLS):
        b, r = brute(c), ctl_rows[c['name']]
        assert b['kempe_free_by_size'] == r['kempe_free_by_size'], c['name']
        assert r['min_kempe_free_size'] == CONTROL_EXPECT[c['name']], c['name']
        controls[c['name']] = dict(A=r['A'], ring_colourings=r['ring_colourings'],
                                   valid_by_size=r['valid_by_size'],
                                   kempe_free_by_size=r['kempe_free_by_size'],
                                   examples=r['kempe_free_examples'])
    # (5) replay RSST-contract kill witnesses
    replayed = 0
    for r, c in zip(rows, confs):
        if r['rsst_contract'] and not r['rsst_contract_kempe_free']:
            assert r['rsst_contract_witness'], r['index']
            assert replay_witness(c, r['rsst_contract_witness'], c['contract']), r['index']
            replayed += 1
    checks['rsst_kill_witnesses_replayed'] = replayed
    assert all(v for k, v in checks.items() if isinstance(v, bool))
    keep = ['index', 'name', 'n', 'ring', 'A', 'ring_colourings', 'bad', 'rsst_contract',
            'rsst_contract_kempe_free', 'rsst_contract_witness', 'valid_by_size',
            'kempe_free_by_size', 'vacuous_by_size', 'min_kempe_free_size', 'kempe_free_examples']
    per = []
    for r in rows:
        row = {k: r[k] for k in keep}
        if r['index'] in brute_rows:
            row['fewest_bad_colourings'] = brute_rows[r['index']]['fewest_bad']
        per.append(row)
    kf = [r for r in rows if sum(r['kempe_free_by_size'])]
    summary = dict(
        configurations=len(rows),
        d_reducible=sum(not r['rsst_contract'] for r in rows),
        c_reducible=sum(bool(r['rsst_contract']) for r in rows),
        with_kempe_free_contract=len(kf),
        rsst_contract_kempe_free=sum(r['rsst_contract_kempe_free'] for r in rows),
        valid_contracts_tested=sum(sum(r['valid_by_size']) for r in rows),
        vacuous_contracts=sum(sum(r['vacuous_by_size']) for r in rows),
        ring_sizes={str(k): sum(r['ring'] == k for r in rows) for k in sorted({r['ring'] for r in rows})},
    )
    results = dict(proposal='docs/research/4ct_guide.md#7-停止點與候選路線 (KF)',
                   sources=dict(unavoidable_conf=CONF_SHA256, reduce_c=REDUCE_SHA256,
                                url='https://arxiv.org/src/1401.6481v1/anc/'),
                   summary=summary, checks=checks, controls=controls, configurations=per)
    text = json.dumps(results, ensure_ascii=False, indent=1, sort_keys=True) + '\n'
    (args.out_dir / 'results.json').write_text(text)
    (args.out_dir / 'verification.json').write_text(json.dumps(dict(
        script_sha256=digest(__file__), cpp_sha256=digest(CPP),
        results_sha256=sha256(text.encode()).hexdigest()), indent=1) + '\n')
    print(json.dumps(dict(summary=summary, checks=checks), ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
