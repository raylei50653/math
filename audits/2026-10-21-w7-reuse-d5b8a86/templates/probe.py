#!/usr/bin/env python3
"""Exact run-collapse templates for the frozen W7 orbit incidence (read-only inputs).

Run with python3 -B. Default checks are read-only; --build writes exports and
report.json beside this script. No LP solve.
The optional --full-generation switch replays every original generated column,
checks its frozen ordered SHA, and verifies its collapsed template membership.
"""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
import argparse, gzip, io, json, time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SRC = ROOT / 'audits/2026-10-20-r6-941-j1-five-edge-417732f/counting'
EXPECTED_SHA = '542ee11de93a846bfbc321b098214b153c5b600318ba2e0bc5621a73ad2a55ad'
FULL_SHA = '530aeac43e108f7c94f1e120ec341c18528d36dc3fd41356b5f3b79b3b94a7d5'

def packed(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()

def verify_or_write_gzip(path, obj, build):
    raw = io.BytesIO()
    with gzip.GzipFile(fileobj=raw, mode='wb', mtime=0, filename='') as out:
        out.write(packed(obj)+b'\n')
    expected = raw.getvalue()
    if build:
        path.write_bytes(expected)
    else:
        assert path.read_bytes() == expected, 'export changed: '+path.name
    return {'bytes': path.stat().st_size, 'sha256': sha256(path.read_bytes()).hexdigest()}

def membership_code(q):
    return sum(x << i for i, x in enumerate(q))

def nc(n, t=(0,), stack=(0,), b=1):
    if len(t) == n:
        yield t
        return
    for j, x in enumerate(stack):
        yield from nc(n, t + (x,), stack[:j+1], b)
    yield from nc(n, t + (b,), stack + (b,), b+1)

def decode(x, n=13):
    return tuple((x >> (2*(n-1-i))) & 3 for i in range(n))

def layout(t):
    """Return literal membership q, run representatives, and phase-cube row id.

    Run 0 contains rim position 0 and possibly a suffix at the cyclic seam.
    The half-row normalization fixes phase(run 0)=phase(run 1)=0.
    """
    q = tuple(x // 2 for x in t)
    assert q[0] == 0
    starts = [0] + [i for i in range(1, len(t)) if q[i] != q[i-1]]
    if q[-1] == q[0]:
        starts.pop()
    assert len(starts) % 2 == 0 and len(starts) >= 2
    assert t[0] == 0 and t[starts[1]] == 2
    assert all(t[i] != t[(i+1) % len(t)] for i in range(len(t)))
    phase = sum((t[s] & 1) << (r-2) for r, s in enumerate(starts) if r >= 2)
    return q, tuple(starts), phase

def template(k):
    """All local columns on the 2k alternating palette contacts, with labels.

    Each NC contact partition has k+1 blocks. Fix the first block in each
    palette; every other block supplies one independent phase flip. The
    column family is all cosets of this phase-flip subspace.
    """
    n = 2*k
    cols = set()
    partitions = 0
    factors = [set(), set()]
    factor_pairs = set()
    for p in nc(n):
        if max(p) + 1 != k+1:
            continue
        if any(p[i] == p[(i+1) % n] for i in range(n)):
            continue
        if any(any((i-j) % 2 for j in range(i) if p[i] == p[j]) for i in range(n)):
            continue
        partitions += 1
        anchors = (p[0], p[1])
        masks = [sum(1 << (i-2) for i in range(2, n) if p[i] == b)
                 for b in range(k+1) if b not in anchors]
        subspace = [0]
        for m in masks:
            subspace += [x ^ m for x in subspace]
        covered = set()
        for seed in range(1 << (n-2)):
            if seed in covered:
                continue
            col = tuple(sorted(seed ^ x for x in subspace))
            covered.update(col)
            assert col not in cols
            cols.add(col)
            fs = []
            for side in range(2):
                positions = list(range(2+side, n, 2))
                f = tuple(sorted({sum(((r >> (i-2)) & 1) << a
                                     for a, i in enumerate(positions)) for r in col}))
                factors[side].add(f)
                fs.append(f)
            assert len(fs[0])*len(fs[1]) == len(col)
            factor_pairs.add(tuple(fs))
    assert len(cols) == partitions*(1 << (k-1))
    assert len(factor_pairs) == len(cols)
    return cols, {'k': k, 'runs': n, 'rows': 1 << (n-2),
                  'partitions': partitions, 'columns': len(cols),
                  'column_entries': 1 << (k-1),
                  'nonzeros': sum(map(len, cols)),
                  'unique_palette_factors': list(map(len, factors)),
                  'palette_factor_total_entries': [sum(map(len, fs)) for fs in factors],
                  'sha256': sha256(packed(sorted(cols))).hexdigest()}

def full_replay(templates):
    """Literal copy of original generation, with independent run-collapse tests."""
    digest = sha256()
    n = 13
    totals = Counter()
    start = time.monotonic()
    for p in nc(n):
        totals['noncrossing_partitions'] += 1
        b = max(p)+1
        if b == 1 or sum(p[i] != p[(i+1) % n] for i in range(n)) != 2*(b-1):
            continue
        adj = [set() for _ in range(b)]
        for i in range(n):
            x, y = p[i], p[(i+1) % n]
            if x != y:
                adj[x].add(y)
                adj[y].add(x)
        side = [None]*b
        side[0] = 0
        stack = [0]
        okay = True
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if side[y] is None:
                    side[y] = 1-side[x]
                    stack.append(y)
                elif side[y] == side[x]:
                    okay = False
        if not okay:
            continue
        totals['admissible_partitions'] += 1
        first = [p.index(x) for x in range(b)]
        other = next(x for x in p if side[x])
        flipblocks = [x for x in range(b) if x not in (0, other)]
        masks = [sum(1 << (2*(n-1-i)) for i in range(n) if p[i] == x)
                 for x in flipblocks]
        free = [i for i in range(1, n) if p[i] != p[i-1] and i != first[p[i]]]
        for choices in product((0, 1), repeat=len(free)):
            chosen = dict(zip(free, choices))
            bits = [0]*n
            for i in range(1, n):
                if p[i] == p[i-1]:
                    bits[i] = 1-bits[i-1]
                elif i in chosen:
                    bits[i] = chosen[i]
            if p[-1] == p[0] and bits[-1] == bits[0]:
                continue
            t = tuple(2*side[p[i]]+bits[i] for i in range(n))
            encoded = sum(x << (2*(n-1-i)) for i, x in enumerate(t))
            orbit = [encoded]
            for m in masks:
                orbit += [x ^ m for x in orbit]
            digest.update(packed(sorted(orbit)) + b'\n')
            q, starts, phase = layout(t)
            k = len(starts)//2
            pmasks = [sum(1 << (r-2) for r, s in enumerate(starts)
                          if r >= 2 and p[s] == x) for x in flipblocks]
            abstract = [phase]
            for m in pmasks:
                abstract += [x ^ m for x in abstract]
            assert tuple(sorted(abstract)) in templates[k]
            totals['columns'] += 1
    totals['ordered_full_sha256'] = digest.hexdigest()
    assert digest.hexdigest() == FULL_SHA
    totals['seconds'] = time.monotonic()-start
    return dict(totals)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--build', action='store_true', help='explicitly write artifacts; default checks read-only')
    ap.add_argument('--full-generation', action='store_true')
    args = ap.parse_args()
    start = time.monotonic()
    raw = (SRC/'orbits.json.gz').read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED_SHA
    orb = json.loads(gzip.decompress(raw))
    templates = {}
    meta = []
    for k in range(1, 7):
        templates[k], m = template(k)
        m['membership_words_before_pruning'] = comb(13, 2*k)
        meta.append(m)
    template_seconds = time.monotonic()-start
    # Keep every literal half-row and original canonical state map intact.
    live = set(orb['live'])
    qrows = defaultdict(set)
    literal_map = []
    all_literal_map = []
    for h, state in orb['rowids']:
        q, starts, phase = layout(decode(h))
        all_literal_map.append([h, state, membership_code(q), len(starts)//2, phase,
                                int(state in live)])
        if state in live:
            qrows[q].add(phase)
            literal_map.append((h, state, q, phase))
    qcols = defaultdict(list)
    col_meta = []
    for original_j, col in enumerate(orb['columns']):
        loc = [layout(decode(h)) for h in col]
        q = loc[0][0]
        assert all(row[0] == q for row in loc)
        k = len(loc[0][1])//2
        abstract = tuple(sorted(row[2] for row in loc))
        assert abstract in templates[k]
        qcols[q].append(abstract)
        col_meta.append((original_j, q, abstract))
    kept_by_k = defaultdict(Counter)
    pruned_patterns = Counter()
    for q, rows in qrows.items():
        k = sum(q[i] != q[(i+1) % 13] for i in range(13))//2
        expected = {col for col in templates[k] if all(r in rows for r in col)}
        actual = set(qcols[q])
        assert len(actual) == len(qcols[q])
        assert actual == expected
        kept_by_k[k]['membership_words'] += 1
        kept_by_k[k]['rows'] += len(rows)
        kept_by_k[k]['columns'] += len(actual)
        kept_by_k[k]['nonzeros'] += sum(map(len, actual))
        pruned_patterns[(k, tuple(sorted(rows)))] += 1
    # Check even fully deleted membership blocks so no absent blocks hide a failure.
    for membership in product((0, 1), repeat=12):
        q = (0,) + membership
        if not any(q):
            continue
        k = sum(q[i] != q[(i+1) % 13] for i in range(13))//2
        if q not in qrows:
            assert not qcols[q]
            pruned_patterns[(k, ())] += 1
    patterns_by_k = Counter(k for k, mask in pruned_patterns)
    report = {
        'status': 'exact frozen incidence relabeling and template restriction; cone OPEN',
        'source_realized': False, 'source_excluded': False,
        'input_sha256': EXPECTED_SHA,
        'template_build_plus_load_seconds': template_seconds,
        'templates': meta,
        'unique_unpruned_template_columns': sum(len(t) for t in templates.values()),
        'full_expected_columns': sum(comb(13, 2*k)*len(templates[k]) for k in templates),
        'full_expected_admissible_partitions': sum(comb(13, 2*m['k'])*m['partitions'] for m in meta),
        'frozen_surviving': {str(k): dict(kept_by_k[k]) for k in range(1, 7)},
        'distinct_surviving_row_masks_including_empty': dict(sorted(patterns_by_k.items())),
        'distinct_surviving_row_masks_total': len(pruned_patterns),
        'surviving_row_mask_multiplicities': sorted(Counter(pruned_patterns.values()).items()),
        'literal_map_sha256': sha256(packed(literal_map)).hexdigest(),
        'original_column_map_sha256': sha256(packed(col_meta)).hexdigest(),
        'all_live_half_rows': len(literal_map),
        'all_surviving_columns': len(col_meta),
        'all_columns_equal_exact_template_restriction': True,
    }
    indexed_templates = {k: sorted(cols) for k, cols in templates.items()}
    template_ids = {k: {col: j for j, col in enumerate(cols)}
                    for k, cols in indexed_templates.items()}
    compact_columns = []
    for j, q, abstract in col_meta:
        k = sum(q[i] != q[(i+1) % 13] for i in range(13))//2
        compact_columns.append([membership_code(q), k, template_ids[k][abstract]])
    template_export = indexed_templates
    row_export = {
            'fields': ['literal_encoded_half_row', 'original_canonical_state',
                       'palette_membership_sum_q_i_2pow_i', 'k_half_run_count',
                       'local_phase_index', 'is_live'],
            'rows': all_literal_map}
    column_export = {
            'fields': ['palette_membership_sum_q_i_2pow_i', 'k_half_run_count',
                       'index_in_lexicographically_sorted_template_columns'],
            'original_column_order': compact_columns}
    report['exports'] = {
        'templates.json.gz': verify_or_write_gzip(HERE/'templates.json.gz', template_export, args.build),
        'row_map.json.gz': verify_or_write_gzip(HERE/'row_map.json.gz', row_export, args.build),
        'column_map.json.gz': verify_or_write_gzip(HERE/'column_map.json.gz', column_export, args.build),
    }
    # Reconstruct an original literal column, then corrupt its template support
    # and its template-column map independently. Both must disagree with the
    # frozen literal column (not merely with a newly computed checksum).
    qphase_to_literal = defaultdict(dict)
    for h, state, qbits, k, phase, is_live in all_literal_map:
        qphase_to_literal[qbits][phase] = h
    jcontrol = next(j for j, row in enumerate(compact_columns) if row[1] >= 2)
    qcontrol, kcontrol, tcontrol = compact_columns[jcontrol]
    local_control = indexed_templates[kcontrol][tcontrol]
    reconstruct = lambda support: tuple(sorted(qphase_to_literal[qcontrol][r] for r in support))
    assert reconstruct(local_control) == tuple(orb['columns'][jcontrol])
    replacement = next(r for r in range(1 << (2*kcontrol-2)) if r not in local_control)
    changed_support = (replacement,) + local_control[1:]
    alternate_column = indexed_templates[kcontrol][(tcontrol+1) % len(indexed_templates[kcontrol])]
    assert reconstruct(changed_support) != tuple(orb['columns'][jcontrol])
    assert reconstruct(alternate_column) != tuple(orb['columns'][jcontrol])
    report['negative_controls'] = {
        'changed_template_support_rejected': True,
        'changed_original_column_mapping_rejected': True,
        'original_column_index_tested': jcontrol,
    }
    if args.full_generation:
        report['original_full_generation_replay'] = full_replay(templates)
    report['seconds'] = time.monotonic()-start
    output = HERE/'report.json'
    if args.build:
        output.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    else:
        expected = json.loads(output.read_text())
        def structural(obj):
            return {k: structural(v) if isinstance(v, dict) else v for k, v in obj.items()
                    if k not in ('seconds', 'template_build_plus_load_seconds')}
        if not args.full_generation:
            expected.pop('original_full_generation_replay', None)
        assert structural(expected) == structural(json.loads(json.dumps(report))), 'structural report changed'
    print(json.dumps(report, sort_keys=True))

if __name__ == '__main__':
    main()
