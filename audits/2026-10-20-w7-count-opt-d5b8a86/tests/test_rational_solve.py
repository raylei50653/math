"""rational_solve recovers exact rational solutions of sparse integer systems."""
import sys
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.sparse import random as sprandom, identity, csc_matrix
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import exact_tools as et

rng = np.random.default_rng(1)
for n in (5, 200, 3000):
    M = sprandom(n, n, density=min(1, 4 / n), random_state=rng, data_rvs=lambda k: rng.integers(-2, 3, k))
    B = csc_matrix((M + identity(n) * 3).astype(np.int64))
    B.eliminate_zeros()
    r = [int(v) for v in rng.integers(-5, 6, n)]
    out = et.rational_solve(B, r)
    assert out is not None, n
    num, den = out
    assert et.int_matvec(B, num) == [den * v for v in r]
    print('n', n, 'denominator bits', den.bit_length(), 'OK')
# singular system must not produce a false solution
B = csc_matrix(np.array([[1, 1], [1, 1]], dtype=np.int64))
try:
    assert et.rational_solve(B, [1, 2]) is None
except RuntimeError:
    pass
print('singular rejected OK')
