#!/usr/bin/env python3
"""Turn a numerical point of the normalized X-only model into an exact candidate.

  1. support guess S from the discovery point (restricting to S only removes
     columns, so any exact point found is a point of the full cone);
  2. HiGHS crossover/simplex on the S-restricted LP -> vertex basis;
  3. exact rational solve of the basis system (exact_tools.rational_solve);
  4. X integer = common multiple; Z = (R X)/2 recovered exactly from the
     reference half-rows, scaled so Z is integral;
  5. the full certificate is written only if the independent checker passes.
"""
import argparse
import json
import resource
import sys
import time
from fractions import Fraction
from math import lcm
from pathlib import Path
from types import SimpleNamespace

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from model import Model  # noqa: E402
import exact_tools as et  # noqa: E402
from solve_lp import build  # noqa: E402


def log(**kw):
    kw['t'] = round(time.monotonic() - T0, 2)
    kw['rss_mb'] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
    print(json.dumps(kw), flush=True)
    LOG.append(kw)


def restricted_vertex(A, lo, hi, c, S, x0, seconds, threads):
    import highspy
    from scipy.sparse import csr_matrix
    AS = A[:, S].tocsr()
    rows = np.flatnonzero(np.diff(AS.indptr) > 0)
    AS = AS[rows]
    lp = highspy.HighsLp()
    lp.num_col_, lp.num_row_ = AS.shape[1], AS.shape[0]
    lp.col_cost_ = c[S]
    lp.col_lower_ = np.zeros(len(S))
    lp.col_upper_ = np.full(len(S), highspy.kHighsInf)
    lp.row_lower_ = lo[rows]
    lp.row_upper_ = np.where(np.isinf(hi[rows]), highspy.kHighsInf, hi[rows])
    lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
    lp.a_matrix_.start_ = AS.indptr
    lp.a_matrix_.index_ = AS.indices
    lp.a_matrix_.value_ = AS.data
    h = highspy.Highs()
    for k, v in {'time_limit': seconds, 'threads': threads, 'output_flag': True,
                 'log_file': str(OUT / 'highs-restricted.log')}.items():
        h.setOptionValue(k, v)
    h.passModel(lp)
    if x0 is not None:
        sol = highspy.HighsSolution()
        sol.col_value = list(x0)
        sol.value_valid = True
        st = h.crossover(sol)
        log(step='crossover', status=str(st), model_status=str(h.getModelStatus()),
            basis_valid=h.getBasis().valid)
    h.setOptionValue('solver', 'simplex')
    h.run()
    info = h.getInfo()
    log(step='restricted simplex', status=str(h.getModelStatus()), columns=len(S),
        rows=len(rows), simplex_iterations=info.simplex_iteration_count,
        objective=info.objective_function_value)
    basis = h.getBasis()
    cs = np.array([int(v) for v in basis.col_status])
    rs = np.array([int(v) for v in basis.row_status])
    return rows, cs, rs, np.array(h.getSolution().col_value), str(h.getModelStatus())


def main():
    global OUT
    ap = argparse.ArgumentParser()
    ap.add_argument('run', type=Path)
    ap.add_argument('--name', required=True)
    ap.add_argument('--tau', type=float, default=1e-7, help='relative support threshold')
    ap.add_argument('--seconds', type=float, default=3600)
    ap.add_argument('--threads', type=int, default=8)
    ap.add_argument('--no-crossover', action='store_true')
    ap.add_argument('--rounds', type=int, default=16)
    args = ap.parse_args()
    OUT = HERE / 'exact' / args.name
    OUT.mkdir(parents=True, exist_ok=False)
    meta = json.loads((args.run / 'input.json').read_text())['arguments']
    m = Model()
    ref, A, (lo, hi), c = build(m, SimpleNamespace(**meta))
    if not np.array_equal(ref, np.load(args.run / 'vectors.npz')['ref']):
        raise RuntimeError('reference half-row choice differs from the discovery run')
    x = np.clip(np.load(args.run / 'vectors.npz')['x'], 0, None)
    S = np.flatnonzero(x > args.tau * x.max())
    log(step='support', columns=len(S), tau=args.tau, xmax=float(x.max()))
    rows, cs, rs, xs, status = restricted_vertex(
        A, lo, hi, c, S, None if args.no_crossover else x[S], args.seconds, args.threads)
    # HighsBasisStatus: 0 lower, 1 basic, 2 upper, 3 zero, 4 nonbasic
    basic_cols = np.flatnonzero(cs == 1)
    tight_rows = np.flatnonzero(rs != 1)
    log(step='basis', basic_columns=len(basic_cols), tight_rows=len(tight_rows), status=status)
    if len(basic_cols) != len(tight_rows):
        raise RuntimeError('basis is not square')
    AS = A[:, S].tocsr()[rows]
    B = AS[tight_rows][:, basic_cols].tocsc()
    rl, ru = lo[rows], hi[rows]
    rhs = []
    for k, r in enumerate(tight_rows):
        v = rl[r] if rs[r] in (0, 3, 4) or np.isinf(ru[r]) else ru[r]
        if v != int(v):
            raise RuntimeError('non-integer bound')
        rhs.append(int(v))
    sol = et.rational_solve(B, rhs, rounds=args.rounds)
    if sol is None:
        log(step='rational solve', result='FAILED')
        (OUT / 'log.json').write_text(json.dumps(LOG, indent=1) + '\n')
        return
    num, den = sol
    log(step='rational solve', result='ok', denominator_bits=den.bit_length(),
        min_num=min(num), max_num_bits=max(abs(v) for v in num).bit_length())
    if min(num) < 0:
        log(step='sign', result='negative basic value; not a point')
        (OUT / 'log.json').write_text(json.dumps(LOG, indent=1) + '\n')
        return
    # Integer X on full column index set (X = num/den; multiply by 2*den later via Z).
    X = {}
    for k, j in enumerate(basic_cols):
        if num[k]:
            X[int(S[j])] = num[k]
    # Exact Z: 2 Z_s = S_ref(s) = sum of X over columns containing the reference half-row.
    hs = {}
    for j, v in X.items():
        for k in m.cidx[m.cptr[j]:m.cptr[j + 1]]:
            hs[int(k)] = hs.get(int(k), 0) + v
    # Every half-row sum of a state must be equal; check all, then Z = sum/2.
    Zt = {}
    for k, v in hs.items():
        s = int(k) // 3
        Zt.setdefault(s, set()).add(v)
    bad = [s for s, vs in Zt.items() if len(vs) != 1 or any(3 * s + p not in hs for p in range(3))]
    if bad:
        log(step='balance', result='unbalanced states', count=len(bad))
        (OUT / 'log.json').write_text(json.dumps(LOG, indent=1) + '\n')
        return
    # Scale by 2 so that Z = sum/2 is an integer; gcd-reduce.
    from math import gcd
    xs2 = {j: 2 * v for j, v in X.items()}
    zs = {int(m.live[s]): next(iter(vs)) for s, vs in Zt.items()}
    g = 0
    for v in list(xs2.values()) + list(zs.values()):
        g = gcd(g, v)
    xs2 = {j: v // g for j, v in xs2.items()}
    zs = {s: v // g for s, v in zs.items()}
    log(step='integer point', nonzero_x=len(xs2), nonzero_z=len(zs),
        max_x_bits=max(xs2.values()).bit_length(), max_z_bits=max(zs.values()).bit_length())
    cert_path = OUT / 'certificate.json'
    et.write_primal(cert_path, m, zs, xs2, {
        'input_sha256': {'caps.json.gz': '01547476f7afdc88ab224d640eaef363cfe765dd29e8983ca9df7aa63fdd68a3',
                         'orbits.json.gz': '542ee11de93a846bfbc321b098214b153c5b600318ba2e0bc5621a73ad2a55ad'},
        'discovery_run': str(args.run.relative_to(HERE)), 'support_tau': args.tau})
    log(step='written', path=str(cert_path.relative_to(HERE)))
    (OUT / 'log.json').write_text(json.dumps(LOG, indent=1) + '\n')


T0 = time.monotonic()
LOG = []
OUT = None
if __name__ == '__main__':
    main()
