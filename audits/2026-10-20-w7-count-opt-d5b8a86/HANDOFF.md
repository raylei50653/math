# W7 count cone: solver optimization handoff (2026-10-20, unfinished)

**Status: no exact certificate; the cone stays OPEN.** Every result below is
numerical discovery. Only `../2026-10-20-w7-count-cone-d5b8a86/independent/check.py`
can decide the cone. BASE `d5b8a8605bcbcef7aebbcf1934dad7ba255ccf02`. A and B are unchanged.
Nothing has been committed.

## Model (unchanged necessary cone; no 112 contact types)
`model.py` eliminates Z. For each live state there are two rows `S_other − S_ref = 0`,
where `ref` is the half-row of minimum degree. Z is recovered as `Z = S_ref/2`, and the
coordinate maps are in the `model.py` docstring. Result: 122,616 + positivity rows,
307,197 columns, 4.70M nonzeros. A single positivity is imposed as `q_l X = 2`;
`--positive -1` imposes all ten as `q_l X >= 2`. The objective is min ΣX.
Because every P_l ≥ 0, joint positivity is equivalent to each positivity being
feasible on its own (cone points add).

## Same model, 600 s (target-only)
| run | result | peak RSS |
| --- | --- | --- |
| t-dsimplex-sum (HiGHS dual simplex) | no point; dual bound 412.9; 31,217 iterations | 965 MB |
| t-ipx-sum (HiGHS IPX) | 3 IPM iterations; stuck constructing the basis | 1.86 GB |
| t-pdlp-polish (OR-Tools PDLP, 8 threads) | ‖r‖∞ = 5.3e-5; obj 15451.5 | 473 MB |
| all-cu-pdlp (cuOpt 26.10 GPU PDLP, all ten) | ‖r‖∞ = 3.0e-8; obj 15452.4425 / dual 15452.4427 | 1.0 GB |

all-pdlp-1 (CPU PDLP, all ten, 1800 s) reached only ‖r‖∞ = 1.6e-6.
At the optimum only the target row has a nonzero dual (7726.22); the other nine
positivities are not tight. The support is about 170k columns, with values spread
continuously from 1e-12 to 4.5, so the point is not a vertex.

## Dead ends
- HiGHS IPX crossover from a given point: segfault (exit 139), twice
  (`runs/*-crashed*`). Before the crash it rejected unclipped duals (flag 105).
- cuOpt barrier: the Cholesky factor would have 2.81e9 nonzeros, exceeding 12 GB VRAM.
- HiPO is not compiled into the highspy 1.15.1 wheel. SCIP's exact mode is not
  compiled into the pyscipopt 6.3 wheel.

## In progress / next
- `all-cu-pdlp-e6x`: warm PDLP reached Optimal at eps 1e-6, and cuOpt crossover
  (rank-revealing LU) was still running at handoff; 73k of 122,561 pivots took 684 s.
  If it writes `runs/all-cu-pdlp-e6x/result.json` with a vertex (≤122,561 nonzeros),
  run `./py certify_primal.py runs/all-cu-pdlp-e6x --name v1 --no-crossover --tau 0`,
  then run the two checker commands on `exact/v1/certificate.json`.
  `certify_primal.py` has **not** been tested end to end.
- `exact_tools.rational_solve` (float LU + exact integer residual refinement +
  rational reconstruction) passes `tests/test_rational_solve.py`.
- Fallback if crossover fails: build the basis yourself from columns with large
  x̃, fix the nonbasic columns at dyadic rationals, and solve x_B exactly.
- `gpy` uses a cuOpt venv in the session scratchpad, which may have been removed.
  The rebuild command is in the header of `gpy`.

## Continuation 2026-10-21 (still no certificate; cone OPEN)
- The original `all-cu-pdlp-e6x` died with its session at 73,388 LU pivots and
  never wrote `result.json`; the old scratchpad venv was gone as well. The venv
  was rebuilt with the `gpy` header command at a new scratchpad path, passed as
  `CUOPT_VENV=...`. The identical run was restarted as `all-cu-pdlp-e6x-r2`
  (log `logs/all-cu-pdlp-e6x-r2.log`, 36000 s limit). Warm PDLP was Optimal again
  in 1.1 s, and the LU retraced the same profile (73.7k pivots at 870 s, about
  3 pivots/s).
- Structural finding: the support {x~ > 1e-9} has 170,466 columns over 121,175
  touched D rows. No column of D is a singleton. A greedy lower-triangular basis
  (`triangular_probe.py`, `logs/triangular-probe.log`) gets only 63,960 pivots
  and leaves 57,215 rows unenforced, with float residual up to 7e-2, so those rows
  bind. HiGHS INVERT on a largest-x~ candidate basis (iteration limit 0) printed
  nothing in 580 s. Together with cuOpt's stall at ~73k pivots, this says any
  basis on this support has a core of about 50k rows that fills in densely after
  elimination.
- Consequence: even if crossover finishes, `rational_solve` (SuperLU + refinement)
  on that basis likely faces the same dense core. Exact denominators could be
  up to the Hadamard scale of the core (~10^5 bits), so the primal certificate
  may be impractically large unless the vertex basis turns out unimodular-like.
- Proposal (recorded before further experiments): (a) let r2 finish and measure
  the vertex basis core/denominator before exactifying; (b) look for a
  small-support primal point instead (the nine non-target positivities have slack
  61 to 2672, so only target support needs closing), e.g. PDLP with
  reweighted-L1 costs then restricted vertex on that support; (c) state-level
  aggregation to shrink the core. A restricted-support failure is not a verdict.

## Fast-path pipeline plan (2026-10-21, recorded before running)
r2 was stopped by request at 74,085 LU pivots after 1563 s (rate about 0.3 pivots/s).
Pipeline `fastpath.py`, same necessary cone, no new contact types:
1. Split: piece T = target only (q_9 X = 2); piece N = the nine non-target
   positivities jointly (q_l X >= 2). Exact X_T + X_N is a joint point because
   every quantity is a nonnegative linear form.
2. Sparsify: GPU PDLP rounds with reweighted-L1 costs c_j = 1/(x_j + eps_r),
   warm-started; track support, touched rows, used states.
3. Restrict to support, take a vertex of the restricted LP (simplex), and record
   its basis plus the triangular-probe core size as an exactness proxy.
4. Exact: rational_solve on the basis, then exact integer verification per piece.
5. Combine and run the independent checker.
Baseline for speed: PDLP 600 s, then crossover at more than 24 h projected,
unfinished. Restricted-support infeasibility is never a verdict.

## External-method proposals (2026-10-21, recorded before running)
fastpath target-a: four reweighted-L1 rounds cut the support to 82,835 columns
(121,621 touched rows), but the restricted-vertex LU again stalled near 69k pivots.
The dense core survives sparsification. Two cheap measurements come first:
1. C11 pullback mismatch, full table: exact pairing r_j of the deletion-pullback
   of the 132-term lambda on all 307,197 columns, plus the Z-side coefficient of
   every live state, classified by the u4,u3 contact pattern. The question is
   whether the mismatch is sparse or diffuse. A patch delta must come from structural
   templates and keep the target sign (delta = -lambda0 gives the zero certificate).
2. Colour refinement / equitable partition (Grohe-Kersting-Mladenov-Selman 2013,
   Lemma 7.1) of the full feasibility LP (c = 0, equations, ten positivity rows,
   rhs). Record reduced sizes, the class table and the lift map. Stop if the
   partition is near-discrete.
Only if the core stays large: exact LP iterative refinement (Gleixner-Steffy-Wolter
2016, SoPlex exact; precision boosting, Eifler et al. 2023) or p-adic lifting
(Eberly et al. 2006, LinBox). Both still solve the final basis exactly, so neither
bypasses the dense core automatically. Cone-point addition (witness library) is
used only once at least one exact vector exists. No verdict from any of this.

## Results of the two measurements (2026-10-21)
- `refine.py` (logs/refine-joint.json): colour refinement of the full c = 0 system
  (183,934 rows, 368,505 columns, 4.46M nnz) is discrete after 6 rounds, with an exact
  equitability check. The equations alone, without positivity rows, are also discrete.
  LP folding gives no reduction, so this route is stopped.
- `c11_mismatch.py` (logs/c11-mismatch.json): the deletion pullback y0 gives Z-side
  coefficient -2 on exactly 14 live states (both targets among them; only the target
  positivity row is hit), so 4 * sum Z_14 = sum_j p_j X_j. 1,268 of 307,197 columns
  have p_j != 0: 667 have positive price, 601 negative, in 117 contact classes.
  Recomputed from model.incidence(). This is worse than the 13-term potential (103
  positive prices).
- Proposal (recorded before running): a restricted dual patch LP with
  y = a*y13 + b*y0 + delta, delta supported on the half-rows (and states) touched by
  the positive-price columns. Require correct sign on every column pairing, Z-side <= 0
  off target and < 0 on target, and price all columns exactly. A restricted
  infeasibility is never a verdict.

## Follow-up checks (2026-10-21)
- The first refinement used multisets of single coefficients and started with Z and X
  in separate classes. Both are stronger than the paper and could over-split.
  `refine.py --sums` (logs/refine-joint-sums.json) follows Lemma 7.1: per-class
  coefficient sums, every column in one class (c = 0, lb = 0), and rows split only
  by sense and rhs. It is still discrete after 6 rounds. The coarsest equitable
  partition from that start is unique, and hash collisions can only merge classes,
  so the conclusion holds: this folding gives no reduction on this representation.
  That does not rule out other kinds of structural reuse.
- `combine2.py` (logs/combine2.json): y = a*y13 + b*y0 with a, b of free sign, checked
  exactly against every column and state. The only feasible point is a = b = 0.
  The two seeds share 1 nonzero column and 5 half-rows. y13 needs a > 0 (it alone
  carries 44459 with w = 1, and its w on 44466 is 0), and its 103 bad columns lie where y0 is 0.
- `patch_dual.py`: the restricted delta patch. Its result is under runs/patch-<name>/.
- patch_dual.py history. Two coding errors were found and fixed before the h0 result
  counted: (1) state rows were missing outside H, although P_l reaches them; that
  produced a fake "Optimal" with lambda on G[01012]. (2) CT[H] selected the wrong
  axis; it must be CT[:, H]. That produced a fake "Optimal" whose float y violated
  5,613 columns. After both fixes, h0 (5,570 states, 16,710 half-rows, 127,846
  columns, 11,110 states) is infeasible in HiGHS presolve (float, restricted to this
  H). One ring of growth reaches 61,136 states and all columns, which is the
  full dual, so that run was stopped.
- Proposal (recorded before running): grow H along the support of the restricted
  Farkas ray (the primal X of the restricted infeasibility), one round at a time.
  Exact pricing of all columns and states goes through the independent checker.
  A restricted failure is never a verdict.
