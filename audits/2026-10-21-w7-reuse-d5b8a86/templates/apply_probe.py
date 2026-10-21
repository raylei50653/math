#!/usr/bin/env python3
"""Apply frozen C and C^T by cached run-template blocks (no solver).

Use the existing pinned numerical environment:
  audits/2026-10-20-w7-count-opt-d5b8a86/py -B .../templates/apply_probe.py
Every original row and column has its own entry; shape sharing never averages
states or palette words. Cache one incidence block per exact live-row mask.
"""
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
import argparse, gzip, json, time
import numpy as np
from scipy.sparse import csc_matrix, csr_matrix

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CACHE = ROOT/'audits/2026-10-20-w7-count-opt-d5b8a86/cache/model.npz'

def read(name):
    with gzip.open(HERE/name, 'rt') as f:
        return json.load(f)

class Templates:
    def __init__(self, hrow):
        template_cols = {int(k): cols for k, cols in read('templates.json.gz').items()}
        hk = {int(h): i for i, h in enumerate(hrow)}
        self.nh = len(hrow)
        qrows = defaultdict(dict)
        for h, state, qbits, k, phase, live in read('row_map.json.gz')['rows']:
            if live:
                qrows[qbits][phase] = hk[h]
        qcols = defaultdict(dict)
        original = read('column_map.json.gz')['original_column_order']
        for j, (qbits, k, local_col) in enumerate(original):
            qcols[qbits][local_col] = j
        self.nx = len(original)
        shapes = defaultdict(list)
        for qbits, phase_to_row in qrows.items():
            # qbits has bit 0=0; include the edge rim12 -> rim0 separately.
            transitions = sum(((qbits >> i) ^ (qbits >> ((i+1) % 13))) & 1
                              for i in range(13))
            k = transitions//2
            shapes[k, tuple(sorted(phase_to_row))].append(qbits)
        self.blocks = []
        self.cached_nnz = 0
        for (k, phases), qbits_list in sorted(shapes.items()):
            qbits_list.sort()
            phase_to_local = {r: i for i, r in enumerate(phases)}
            allowed = [j for j, col in enumerate(template_cols[k])
                       if all(r in phase_to_local for r in col)]
            rr, cc = [], []
            for j, tcol in enumerate(allowed):
                for r in template_cols[k][tcol]:
                    rr.append(phase_to_local[r])
                    cc.append(j)
            B = csr_matrix((np.ones(len(rr), dtype=np.int64), (rr, cc)),
                           shape=(len(phases), len(allowed)))
            row_indices = np.array([[qrows[q][r] for q in qbits_list] for r in phases])
            col_indices = np.array([[qcols[q][j] for q in qbits_list] for j in allowed])
            assert all(set(qcols[q]) == set(allowed) for q in qbits_list)
            self.blocks.append((B, B.T.tocsr(), row_indices, col_indices))
            self.cached_nnz += B.nnz

    def apply(self, x):
        y = np.zeros(self.nh, dtype=x.dtype)
        for B, BT, row_indices, col_indices in self.blocks:
            y[row_indices] = B @ x[col_indices]
        return y

    def transpose(self, y):
        x = np.zeros(self.nx, dtype=y.dtype)
        for B, BT, row_indices, col_indices in self.blocks:
            x[col_indices] = BT @ y[row_indices]
        return x

def median_seconds(f, repeats=9):
    times = []
    for _ in range(repeats):
        t = time.perf_counter()
        f()
        times.append(time.perf_counter()-t)
    return float(np.median(times))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--build', action='store_true', help='write report; default checks read-only')
    args = ap.parse_args()
    start = time.monotonic()
    assert sha256(CACHE.read_bytes()).hexdigest() == 'f2acd4da9457c81b4903b8a4f9c4e8dcc176c6dd0a9856d64163145a7e8088e9'
    d = np.load(CACHE)
    C = csc_matrix((np.ones(len(d['cidx']), dtype=np.int64), d['cidx'], d['cptr']),
                   shape=(len(d['hrow']), len(d['cptr'])-1))
    T = Templates(d['hrow'])
    # Deterministic signed small-integer vectors: every operation stays exact.
    x = (np.arange(C.shape[1], dtype=np.int64)*17+5) % 29-14
    y = (np.arange(C.shape[0], dtype=np.int64)*23+3) % 31-15
    assert np.array_equal(C @ x, T.apply(x))
    assert np.array_equal(C.T @ y, T.transpose(y))
    # Perturb an actual cached template incidence coefficient, then restore it.
    T.blocks[0][0].data[0] += 1
    assert not np.array_equal(C @ x, T.apply(x))
    T.blocks[0][0].data[0] -= 1
    assert np.array_equal(C @ x, T.apply(x))
    # Independent coefficient perturbation control must be detected.
    x_bad = x.copy()
    x_bad[0] += 1
    assert not np.array_equal(C @ x_bad, T.apply(x))
    xf, yf = x.astype(float), y.astype(float)
    # Match the production float incidence and avoid charging either path for
    # repeated integer-to-float coefficient conversions inside the benchmark.
    Cf = C.astype(float)
    T.blocks = [(B.astype(float), BT.astype(float), ri, ci)
                for B, BT, ri, ci in T.blocks]
    report = {
        'status': 'PASS exact integer applications; benchmark only; cone OPEN',
        'shape': list(C.shape), 'frozen_nnz': int(C.nnz),
        'nonempty_cached_shapes': len(T.blocks),
        'cached_shape_nnz_once': T.cached_nnz,
        'incidence_entry_reuse_factor': C.nnz/T.cached_nnz,
        'exact_C_application_matches': True,
        'exact_CT_application_matches': True,
        'changed_input_negative_control_detected': True,
        'changed_template_coefficient_negative_control_detected': True,
        'median_of_9_seconds': {
            'frozen_C': median_seconds(lambda: Cf @ xf),
            'template_C': median_seconds(lambda: T.apply(xf)),
            'frozen_CT': median_seconds(lambda: Cf.T @ yf),
            'template_CT': median_seconds(lambda: T.transpose(yf)),
        },
        'note': 'Same arithmetic count; template implementation also gathers/scatters. '
                'No speed improvement is assumed from storage sharing.',
        'seconds': time.monotonic()-start,
    }
    path = HERE/'apply_report.json'
    if args.build:
        path.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    else:
        old = json.loads(path.read_text())
        stable = lambda obj: {k: v for k, v in obj.items()
                              if k not in ('seconds', 'median_of_9_seconds')}
        assert stable(old) == stable(report)
    print(json.dumps(report, sort_keys=True))

if __name__ == '__main__':
    main()
