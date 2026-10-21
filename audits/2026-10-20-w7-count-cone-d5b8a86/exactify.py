#!/usr/bin/env python3
"""Try rational reconstruction; write only candidates proved by the checker."""
import argparse
from fractions import Fraction
from functools import reduce
import importlib.util
import json
from math import gcd, lcm
from pathlib import Path
import pickle

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('independent', HERE/'independent/check.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def vectors(values):
    # Small grids are especially useful for orbit-count certificates. Each is
    # merely a candidate and must satisfy every exact integer inequality.
    for scale in (1,2,4,8,16,32,64,128,256,512,1024,3,6,12,24,48,96,192,
                  5,10,20,40,80,160,320,1000,10000,100000,1000000):
        yield 'grid-'+str(scale), [round(float(v)*scale) for v in values], scale
    for denominator in (16,64,256,1024,10000,1000000):
        rat = [Fraction(float(v)).limit_denominator(denominator) for v in values]
        scale = lcm(*(v.denominator for v in rat))
        # Avoid a huge meaningless LCM when numerical residuals dominate.
        if scale.bit_length() <= 256:
            yield 'fractions-'+str(denominator), [int(v*scale) for v in rat], scale


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('run', type=Path)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise RuntimeError('exclusive-create certificate: output already exists')
    model = checker.load_model()
    with (args.run/'solution.pickle').open('rb') as f:
        sol = pickle.load(f)
    candidates = []
    if sol['result']['value_valid']:
        candidates.append(('primal',sol['col_value']))
    if (args.run/'primal-ray.pickle').exists():
        with (args.run/'primal-ray.pickle').open('rb') as f:
            live, ray = pickle.load(f)
        if live != sol['live']:
            raise RuntimeError('primal ray variable order mismatch')
        candidates.append(('primal',ray))
    if sol['result']['dual_valid'] and not sol['active_p']:
        candidates.append(('dual',[-v for v in sol['row_dual']] + [0]*9+[1]))
    if (args.run/'dual-ray.pickle').exists():
        with (args.run/'dual-ray.pickle').open('rb') as f:
            rows, active, ray = pickle.load(f)
        lam = [0.]*10
        for k,j in enumerate(active):
            lam[j] = float(ray[len(rows)+k])
        candidates.append(('dual',[-v for v in ray[:len(rows)]] + lam))
    tested = []
    for kind, values in candidates:
        for reconstruction, ints, scale in vectors(values):
            div = reduce(gcd, ints)
            if div:
                ints = [v//div for v in ints]
            cert = {'base': checker.BASE, 'input_sha256': checker.SHA, 'kind': kind,
                    'discovery_run': str(args.run), 'reconstruction': reconstruction}
            if kind == 'primal':
                n = len(sol['live'])
                cert.update(z=[[i,v] for i,v in zip(sol['live'],ints[:n]) if v],
                            x=[[j,v] for j,v in enumerate(ints[n:]) if v])
            else:
                n = len(sol['rows'])
                cert.update(y=[[r,v] for r,v in zip(sol['rows'],ints[:n]) if v],
                            **{'lambda': ints[n:]})
            try:
                result = checker.check_certificate(model, cert)
            except checker.Rejected as exc:
                tested.append({'kind':kind,'method':reconstruction,'rejected':str(exc)})
                continue
            with args.output.open('x') as f:
                json.dump(cert,f,separators=(',',':')); f.write('\n')
            print(json.dumps({'status':'EXACT CERTIFICATE', 'result':result,
                              'path':str(args.output),'attempts':len(tested)+1}))
            return
    print(json.dumps({'status':'NO EXACT CERTIFICATE','attempts':tested},indent=2))


if __name__ == '__main__':
    main()
