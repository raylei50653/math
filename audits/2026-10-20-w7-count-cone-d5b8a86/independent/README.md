# Independent exact checking of the frozen W7 cone

This directory checks the necessary count cone at BASE
`d5b8a8605bcbcef7aebbcf1934dad7ba255ccf02`. The source scope is the strict
only-R/W7 subtype under the inherited J1 source contract. A dual certificate
does not exclude general J1 or a general five-edge path; a primal certificate
does not realize an original graph.

`check.py` uses only the Python standard library. It imports neither the
discovery solver nor any baseline audit Python module. It pins the exact
`caps.json.gz` and `orbits.json.gz` bytes, independently enumerates canonical
C13 states, reconstructs every full-star cap and the two sectors from original
edges, reconstructs C10 inherited zero conditions, and reconstructs the three
H-half-rows per state by minimizing over the eight palette-preserving global
permutations. It checks every retained orbit column against this independently
constructed row map. The already frozen complete orbit family is an input;
its full enumeration is not rerun in this directory.

The checked system has 61,308 live state coordinates Z, 307,197 nonnegative
orbit coordinates X, and 183,924 simultaneous equalities

```
2 Z[state(h)] = sum(X[j] : half-row h belongs to column j).
```

Every omitted state coordinate is zero, including 5,098 initial zeros and the
24 further support-closure zeros. All ten strict positive quantities use the
same Z vector, in this order:

1. G[01012]
2. G[01023]
3. G[01201]
4. G[01203]
5. G[01213]
6. G[01231]
7. G[01232]
8. G[01232, h=a]
9. G[01232, h=b]
10. Z[44459] + Z[44466]

A primal certificate is a JSON object with `kind: "primal"` (optional),
`z: [[canonical_state_id, positive_integer], ...]`, and
`x: [[frozen_surviving_column_index, positive_integer], ...]`. Column indices
are zero-based. Coordinates must be strictly sorted and unique; omitted
coordinates equal zero. Exact integer equalities and all ten strict
positivities are checked. Rational certificates can first be multiplied by
a common positive denominator.

A dual certificate has `kind: "dual"`, sparse signed integer
`y: [[encoded_half_row_id, nonzero_integer], ...]`, and ten nonnegative
integer `lambda` values, at least one positive. The checker verifies

```
2 sum(y[h] : state(h)=i) >= sum(lambda[l] P[l,i])   for every live i,
sum(y[h] : h belongs to column j) <= 0             for every column j.
```

Multiplication of the common equalities by y then gives
`0 >= sum(lambda[l] P[l] Z) > 0`, using nonnegativity. This is an exact
contradiction to the specified source positivity. There is no tolerance or
floating-point arithmetic in either certificate check.

Model-only replay and malformed-input controls:

```
python3 -B audits/2026-10-20-w7-count-cone-d5b8a86/independent/check.py --model-controls --malformed-controls
python3 -B audits/2026-10-20-w7-count-cone-d5b8a86/independent/check.py --seed 17 --malformed-controls
```

Certificate replay, including alterations of integer coordinates and removal
of the required positivity:

```
python3 -B audits/2026-10-20-w7-count-cone-d5b8a86/independent/check.py --certificate CERTIFICATE.json --controls
python3 -B audits/2026-10-20-w7-count-cone-d5b8a86/independent/check.py --certificate CERTIFICATE.json --controls --seed 17
```

The seed changes summation traversal of orbit rows while preserving all
coordinate IDs. Output can be written with `--output FILE`.

Independent review of `../solve.py` confirmed the full active equality model,
nonnegative Z/X bounds, and all ten positivity coefficient rows and their
order. A target-only discovery run is a relaxation: its infeasibility suffices
for exclusion, while a feasible point still requires all ten positive
quantities to pass the independent checker.
