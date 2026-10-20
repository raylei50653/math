"""Exact common-exterior counting identities for the new J1/J2 pair."""
import argparse
import gzip
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FROZEN = HERE / 'frozen'
BASE = 'f13eb4d0887d962021992ae7afe3323af4d79cd3'
MODEL = 'audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py'
PRIOR = 'audits/2026-10-19-r6-941-quotients-13dc5ff/A/certificate.json'


def packed(obj):
    return (json.dumps(obj, sort_keys=True, separators=(',', ':')) + '\n').encode()


def compute():
    seal = json.loads((HERE / 'INPUTS.json').read_text())
    entries = {r['path']: r for r in seal['files']}
    hashes = {}
    for path in (MODEL, PRIOR):
        raw = (FROZEN / path).read_bytes()
        hashes[path] = hashlib.sha256(raw).hexdigest()
        assert hashes[path] == entries[path]['sha256'] and len(raw) == entries[path]['bytes']
    spec = importlib.util.spec_from_file_location('frozen_E_model', FROZEN / MODEL)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    old = json.loads((FROZEN / PRIOR).read_text())
    eight = [t for t in m.growth(8, four=True) if m.proper(t)]
    index = {t: i for i, t in enumerate(eight)}
    matrices = [[[0] * len(eight) for _ in m.ROWS] for _ in range(2)]
    assignments = []
    for row, word in enumerate(m.ROWS):
        x, y, a, b, c = map(int, word)
        for n, R, L, q in itertools.product(range(4), repeat=4):
            exterior = (a, n, R, L, q, c, x, y)
            good = m.proper(exterior) and b not in (a, c, q)
            flags = (good and b == L and a != R,
                     good and a != L and a != R and b != L)
            ei = index[m.canonical(exterior)] if m.proper(exterior) else -1
            lifts = [(p, h) for p, h in itertools.product(range(4), repeat=2)
                     if good and p not in (a, b, q, n, h) and h not in (p, q, L, R, n)]
            assignments.append([row, n, R, L, q, ei, list(flags), lifts])
            for j, flag in enumerate(flags):
                if flag:
                    matrices[j][row][ei] += 1
    original = old['literal_E_count_matrices']['G']
    K = m.kempe(8, eight)
    initial = [i for i in range(len(eight)) if all(not original[r][i] for r in (1, 4, 6))]
    live, rounds = m.close(K, initial)
    assert live == old['source_E_closure']['live'] and len(live) == 225
    parts, span, basis = m.planar_basis(eight, live)
    assert len(basis) == 44
    J1, J2 = matrices
    Aa = old['original_alpha_sectors']['Aa']
    forms = [
        [x - u - v for x, u, v in zip(J1[9], J2[4], J2[6])],
        [x - u - v for x, u, v in zip(J2[9], J1[4], J1[6])],
        [x + y - a for x, y, a in zip(J1[9], J2[9], Aa)],
    ]
    residuals = [[str(sum(x * y for x, y in zip(form, vec))) for vec in basis] for form in forms]
    assert all(x == '0' for r in residuals for x in r)
    return {'base': BASE, 'inputs': hashes, 'rows': m.ROWS,
            'E_order': ('a', 'n', 'R', 'L', 'q', 'c', 'x', 'y'),
            'source_frame': ('x', 'y', 'a', 'b', 'c'),
            'complete_joint_assignments': assignments, 'E_states': eight,
            'J_matrices': matrices, 'source_E_initial': initial,
            'source_E_live': live, 'source_E_rounds': rounds,
            'planar_partitions': parts, 'planar_dimension': len(basis),
            'basis': [[str(x) for x in row] for row in basis],
            'identity_forms': forms, 'basis_residuals': residuals,
            'identities': ['b1=u2+v2', 'b2=u1+v1', 'b1+b2=Aa'],
            'source_realized': False, 'main_target': 'OPEN'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--build', action='store_true')
    ap.add_argument('--certificate', type=Path, default=HERE / 'counts.json.gz')
    args = ap.parse_args()
    cert = compute()
    expected = packed(cert)
    if args.build:
        with args.certificate.open('xb') as out:
            out.write(gzip.compress(expected, mtime=0))
    assert gzip.decompress(args.certificate.read_bytes()) == expected, 'exact complete counting certificate'
    # A wrong sign produces a nonzero linear functional on the SAME space;
    # this control tests the algebra itself, rather than metadata alone.
    from fractions import Fraction
    basis = [[Fraction(x) for x in v] for v in cert['basis']]
    wrong = [x + u + v for x, u, v in zip(cert['J_matrices'][0][9],
                                        cert['J_matrices'][1][4], cert['J_matrices'][1][6])]
    assert any(sum(x * y for x, y in zip(wrong, vec)) != 0 for vec in basis)
    print(json.dumps({'pass': True, 'identities': cert['identities'],
                      'complete_joint_assignments': len(cert['complete_joint_assignments']),
                      'same_E_live': len(cert['source_E_live']), 'exact_basis_dimension': len(basis),
                      'wrong_sign_rejected': True, 'main_target': 'OPEN'}, sort_keys=True))


if __name__ == '__main__':
    main()
