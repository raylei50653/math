#!/usr/bin/env python3
"""Check the compiled W7 operator against the frozen explicit model; no LP solve.

Run with the existing pinned numerical environment, optionally --benchmark.
Reports JSON on stdout, without modifying earlier evidence.
"""
import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.sparse import csr_matrix, vstack

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT/'audits/2026-10-20-w7-count-opt-d5b8a86'))
sys.path.insert(0, str(HERE))
from model import Model
from w7_operator import W7Operator


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rejected(fn):
    try:
        fn()
    except (ValueError, TypeError):
        return True
    raise RuntimeError('malformed call was accepted')


def timing(fn, batches=7, repeats=25):
    for _ in range(5):
        fn()
    values = []
    for _ in range(batches):
        t = time.perf_counter()
        for _ in range(repeats):
            fn()
        values.append((time.perf_counter()-t)/repeats)
    return {'median_seconds': float(np.median(values)),
            'batch_seconds': values, 'batches': batches, 'repeats_per_batch': repeats}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--benchmark', action='store_true')
    ap.add_argument('--seed', type=int, default=0)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    m = Model()
    cases, benchmark = [], {}
    max_forward, max_transpose, max_adjoint = 0., 0., 0.
    controls = {}
    for reference in ('mindeg', 'h2'):
        ref = m.reference(reference)
        D, Q = m.difference(ref), m.positivity_rows(ref)
        for selected in ((), (9,), (9, 0, 8), tuple(range(10))):
            A = vstack([D, csr_matrix(Q[list(selected)])], format='csr')
            AT = A.T.tocsr()
            x = rng.integers(-16, 17, size=m.nx).astype(float)
            y = rng.integers(-16, 17, size=A.shape[0]).astype(float)
            expected, expected_t = A @ x, AT @ y
            xf, yf = rng.normal(size=m.nx), rng.normal(size=A.shape[0])
            for backend in ('direct', 'template'):
                t = time.perf_counter()
                op = W7Operator(backend, selected, reference)
                setup_seconds = time.perf_counter()-t
                w, out, out_t = op.workspace(), np.empty(A.shape[0]), np.empty(m.nx)
                require(np.array_equal(op.matvec_into(x, out, w), expected), 'integer forward mismatch')
                require(np.array_equal(op.rmatvec_into(y, out_t, w), expected_t), 'integer transpose mismatch')
                require(float(expected @ y) == float(x @ expected_t), 'exact integer adjoint mismatch')
                f, ft = op.matvec(xf), op.rmatvec(yf)
                fe, te = float(np.max(np.abs(f-A@xf))), float(np.max(np.abs(ft-AT@yf)))
                require(np.allclose(f, A@xf, rtol=2e-12, atol=2e-10), 'float forward mismatch')
                require(np.allclose(ft, AT@yf, rtol=2e-12, atol=2e-10), 'float transpose mismatch')
                left, right = float(f@yf), float(xf@ft)
                ae = abs(left-right)/max(1., abs(left), abs(right))
                require(ae < 2e-11, 'float adjoint mismatch')
                max_forward, max_transpose, max_adjoint = max(max_forward, fe), max(max_transpose, te), max(max_adjoint, ae)
                require(np.array_equal(op.aslinearoperator() @ x, expected), 'LinearOperator forward mismatch')
                require(np.array_equal(op.aslinearoperator().rmatvec(y), expected_t), 'LinearOperator transpose mismatch')
                require(np.array_equal(op.recover_z(x), (m.zmap(ref)@x)/2), 'Z recovery mismatch')
                cases.append({'backend': backend, 'reference': reference, 'positive': selected,
                              'integer_forward_and_transpose_exact': True,
                              'operator_array_bytes': op.operator_storage_bytes,
                              'workspace_bytes': sum(a.nbytes for a in w)})
                if reference == 'mindeg' and len(selected) == 10:
                    controls[backend] = {
                        'wrong_input_length': rejected(lambda: op.matvec(x[:-1])),
                        'complex_input': rejected(lambda: op.matvec(x.astype(complex))),
                        'wrong_output_dtype': rejected(lambda: op.matvec_into(x, out.astype(np.float32), w)),
                        'short_workspace': rejected(lambda: op.matvec_into(x, out, (w[0][:-1], *w[1:]))),
                        'overlapping_input_output': rejected(lambda: op.matvec_into(x, x[:len(out)], w)),
                    }
                    ro = out.copy()
                    ro.flags.writeable = False
                    controls[backend]['readonly_output'] = rejected(lambda: op.matvec_into(x, ro, w))
                    if backend == 'template':
                        mapping_x = np.arange(m.nx, dtype=float)
                        mapping_expected = op.matvec(mapping_x)
                        op.cols[0], op.cols[1] = op.cols[1], op.cols[0]
                        require(not np.array_equal(op.matvec(mapping_x), mapping_expected), 'changed mapping escaped comparison')
                        op.cols[0], op.cols[1] = op.cols[1], op.cols[0]
                        require(np.array_equal(op.matvec(x), expected), 'restored mapping differs')
                        controls[backend]['changed_column_mapping_detected'] = True
                    if args.benchmark:
                        # All timed methods allocate exactly one returned output;
                        # native workspace is persistent, as in an iterative loop.
                        def native_f():
                            return op.matvec_into(xf, np.empty(op.shape[0]), w)
                        def native_t():
                            return op.rmatvec_into(yf, np.empty(op.nx), w)
                        benchmark[backend] = {
                            'setup_seconds': setup_seconds,
                            'operator_array_bytes': op.operator_storage_bytes,
                            'workspace_bytes': sum(a.nbytes for a in w),
                            'forward': timing(native_f), 'transpose': timing(native_t),
                            'build': op.build_info,
                        }
                        if 'scipy' not in benchmark:
                            benchmark['scipy'] = {
                                'forward': timing(lambda: A@xf),
                                'transpose': timing(lambda: AT@yf),
                                'both_csr_orientation_array_bytes': sum(a.nbytes for B in (A, AT)
                                        for a in (B.data, B.indices, B.indptr)),
                            }
    controls['invalid_row_selection'] = rejected(lambda: W7Operator(positive=(9, 9)))
    controls['bool_row_selection'] = rejected(lambda: W7Operator(positive=(True,)))
    result = {'status': 'PASS compiled operator equivalence; cone OPEN',
              'cases': cases, 'controls': controls,
              'max_float64_forward_absolute_error': max_forward,
              'max_float64_transpose_absolute_error': max_transpose,
              'max_float64_adjoint_relative_error': max_adjoint,
              'benchmark': benchmark,
              'benchmark_scope': 'single-thread CPU float64, 7x25 calls, median, output allocation matched; no solver run',
              'seed': args.seed}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
