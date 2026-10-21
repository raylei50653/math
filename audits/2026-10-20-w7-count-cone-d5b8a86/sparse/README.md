# Sparse column-generation discovery and exact residual

**Status: no feasibility or infeasibility certificate.** This exploration did not
find a common nonnegative `(Z,X)` satisfying the requested ten positivities. It
also did not obtain a full-cone dual inequality. The complete cone remains OPEN.
These computations only used target state **44459** as a discovery normalization;
they did not separately decide 44466 or their positive sum.

## Model and scope

The input is the frozen `counting/orbits.json.gz` at base `d5b8a86`, SHA256
`542ee11de93a846bfbc321b098214b153c5b600318ba2e0bc5621a73ad2a55ad`.
It has 61,308 live states and 307,197 surviving columns. All inherited zero
states and columns are represented by this exact frozen support family.

For each state `i`, let its three half-rows in increasing integer order be
`h0,h1,h2` and write `S_h = sum_{j containing h} X_j`. The two equations

```
S_h0 - S_h2 = 0,
S_h1 - S_h2 = 0
```

are exactly equivalent to the three original `2 Z_i = S_h` equations after
setting the **same** `Z_i = S_h2 / 2`. We normalized `S_h2 = 1` at `i=44459`.
The full eliminated system therefore has 122,617 equations in 307,197 `X`s.
Restricting its column set sets every omitted `X` to zero. Infeasibility of such
a restriction would only concern that smaller cone.

`phase1_generate.py` and `warm_generate.py` numerically minimize one common
residual `t >= 0` subject to `|A X - b| <= t`, `X >= 0`, then price every full
column against the resulting bounded row dual. These auxiliary models omit the
other nine positivity requirements. A positive auxiliary residual is never
interpreted as a decision of the requested full cone.

## Actual stops

- The initial equality/Farkas discovery reached 10,368 selected columns and
  41,568 active difference rows, then returned `kUnknown` at 31.004 seconds.
  `target44459-batch250/history.json` retains its numerical history; that pilot
  did not retain a usable primal or dual checkpoint.
- The bounded phase-I cold-master run was manually stopped after its last valid
  optimum, at 4,197 columns / 17,793 active difference rows and `t=1/8`, to resume
  with incremental bases. Its complete numerical checkpoint is retained.
- The first warm run reached a cumulative HiGHS runtime limit at 53.700 elapsed
  seconds. Its configured limit of 50 was cumulative across incremental runs;
  this behavior was corrected for the final continuation.
- The final continuation stopped with `kTimeLimit` at 142.839 elapsed seconds,
  at 5,631 selected columns. Its reported primal infeasibility was
  `2.798124833266014`, so that stopped iterate is unusable as a primal point.
  The **last valid master** had 5,528 selected columns, `t=1/8`, and 103 improving
  full-column prices. Both the stopped iterate and last valid checkpoint remain.

No further LP was started after this continuation. The pilot triangulation
search is separately retained as an unsuccessful source-generated-point search;
it contributes no decision of this counting cone and was not extended.

## Exact unfinished conservation residual

The final `last-optimal.pickle` supplied a numerical dual with eight nonzero
terms. Rounding it to its exact integer potential gives 13 nonzero original
half-row weights. `residual.py` exported every state coefficient, all 307,197
integer column prices, and all positive-price columns to
[exact-dual-residual.json.gz](warm2-44459/exact-dual-residual.json.gz).
Its SHA256 is
`a2e9ec29a08549e099862ff98aea7abf1f495e3020143f87c4ca7b6085b1bdfe`.

The exact identity, valid for every solution of the frozen orbit equations, is

```
2 Z[44459] = sum_j integer_price[j] X[j].
```

Every other live-state coefficient, including 44466, is exactly zero. The full
prices are **103 entries +1, 95 entries -1, eight entries -2, and 306,991 zeros**.
All 5,528 selected-column prices are nonpositive. The 103 positive-price columns
are the complete explicit residual preventing these weights from excluding
positive `Z[44459]`. They are retained as a list and in the complete price array;
they are not silently discarded or treated as geometric zeros.

The stdlib-only [replay_exact_residual.py](replay_exact_residual.py) independently
expands the integer eliminated-row potential into half-row weights, recomputes
the coefficients of **all** 61,308 live states, and independently prices **every**
surviving column. It prints `EXACT RESIDUAL REPLAYED; cone feasibility remains
OPEN`, rather than a certificate PASS. Run it with:

```sh
python3 -B audits/2026-10-20-w7-count-cone-d5b8a86/sparse/replay_exact_residual.py \
  audits/2026-10-20-w7-count-cone-d5b8a86/sparse/warm2-44459/exact-dual-residual.json.gz
```

[Replay output](warm2-44459/exact-residual-replay.json) records the exact checks.
[residual_controls.py](residual_controls.py) checks three deliberate corruptions:
a half-row weight, a state coefficient, and omission of a positive-price column.
A fourth control replaces an integer coefficient by JSON `true`. All four are
rejected under both ordinary Python and `python -O`. All arithmetic fields use
`type(x) is int`, so booleans cannot pass as integers. Positive replays also agree
under normal execution, `PYTHONHASHSEED=17`, and seed 17 with `python -O`.
These controls verify recording and replay accuracy;
they provide no feasibility conclusion.
