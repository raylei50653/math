# Independent review of the connected count-cone audit

Reviewed `../MODEL.md`, `../check.py`, `../exactify.py`, and the model construction
in `../solve.py`. No additional LP was run for this review.

The mathematical model and certificate directions are correct. The normalized
equalities are `2 Z[state(h)] - sum(X[j]: h in C[j]) = 0`. Nonnegative Z and X
are shared by all active half-rows. The seven original G positive rows, two
original h sectors, and the witness sum use one common Z and the agreed fixed
ten-row order. Homogeneity justifies replacing all ten strict positivities by
lower bounds of one. An exact rational point can be scaled to integers; an
exact dual with nonnegative, nonzero lambda yields a contradiction to mandatory
source positivity.

`exactify.py` treats numerical rounding and rational approximation as candidate
generation only. In particular, its HiGHS ray conversion `y=-ray_E` and
`lambda=ray_P` agrees with the independent checker's inequalities. Every output
certificate passes the full integer checker before exclusive creation of the
output file. No approximate residual, solver status, or local restricted model
is accepted as a certificate.

The full residual is fixed by the 2,649-file input manifest in `../BASE.json`,
the exact gzip input hashes in `check.py`, and `../MODEL.md`:

- All 66,430 canonical state IDs, complete cap matrices and sectors, 5,098
  initial zeros, and the target IDs are in frozen `caps.json.gz`.
- The 24 additional zero IDs, all 61,308 live IDs, the complete half-row map,
  and every one of the 307,197 retained columns are in frozen
  `orbits.json.gz`.
- The ten positivity coefficient vectors are seven named G rows, two sector
  rows, and the indicator of target IDs 44459 and 44466. No positivity row is
  omitted or substituted by a separate marginal.
- The resulting common model has 183,924 equalities, 368,505 variables, and
  4,448,132 nonzero equality coefficients.

The root replay reports `model: "PASS independent reconstruction"` separately
from `necessary_cone: "OPEN"` when no certificate is present. Its
`all_ten_mandatory_positivities_present` key reports inclusion of the coefficient
rows; it does not report simultaneous strict positivity. A model reconstruction
PASS supplies neither primal feasibility nor dual infeasibility. The current
timeout and solve-error records therefore cannot exclude the W7 source subtype
or show a realizing original graph.

Review found an assertion-based custody gap in the initial root wrapper. It
was corrected to explicit runtime checks. The three controls in
`root-custody-optimized-controls.json` confirm rejection of a wrong BASE,
changed byte count, and changed SHA256 even under `python3 -O`. The independent
integer checker itself uses explicit checks throughout.

All conclusions retain the strict only-R/W7 scope under the inherited J1
source contract. General J1, general five-edge paths, source realizability,
smaller-bad constructions, and Lean remain outside this count-cone verdict.
The 112 joint attachment profiles and their extra chord-zero conditions have
not silently been added to the frozen necessary model.
