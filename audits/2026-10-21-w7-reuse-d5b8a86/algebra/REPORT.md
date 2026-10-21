# W7 exact algebra reuse audit

BASE `d5b8a8605bcbcef7aebbcf1934dad7ba255ccf02`. No LP solver was run.
The frozen necessary cone and its original-source status remain OPEN. All ten
positivity forms and X nonnegativity are retained. The 112 contact types are
still outside this frozen model.

## Main result: template rank reuse is substantially stronger than deduplication

The independent [rank review](rank_review.json) checks every exported literal
half-row and every surviving column against the frozen original gzip JSON.
For each universal run template, integral Walsh transforms prove the upper
rank bound; signed sums of one subgroup's complete coset columns reconstruct
every allowed Walsh character and prove the matching lower bound.

| Half-run count k | Full template rows | Template columns | Exact rank |
| --- | ---: | ---: | ---: |
| 1 | 1 | 1 | 1 |
| 2 | 4 | 4 | 3 |
| 3 | 16 | 20 | 10 |
| 4 | 64 | 112 | 35 |
| 5 | 256 | 672 | 126 |
| 6 | 1,024 | 4,224 | 462 |

The full matrix C is block diagonal by literal palette-membership word q.
There are binomial(13,2k) full blocks of type k; hence its exact rank is
106,470. Each frozen live block has rank at most the minimum of its live row
count, its surviving column count, and its universal template rank. Summing
these cheap bounds gives **rank(C_live) <= 103,787**.

Because the X-only equality matrix is D = L C_live, **rank(D) <= 103,787**.
Its 122,616 equality rows therefore contain at least **18,829 exact linear
dependencies (15.36%)**. Adding all ten positivity rows gives augmented rank
at most 103,797. This is an upper bound, not an exported independent row set;
a lossless row-selection implementation still needs an exact reconstruction
map. LU pivot counts can include artificial/slack columns, so these numbers
alone do not identify the cause of a past crossover stall.

## Direct algebra reductions are small

The [full sparse scan](result.json) first checks every BASE SHA256 and rebuilds
every cached model array from the pinned caps/orbits JSONs, with exact equality.
For the minimum-degree reference representation D:

- No duplicate/proportional equality rows.
- No positive- or negative-proportional columns, even before including all ten
  positivity forms; therefore direct variable aggregation offers no reduction.
- No singleton, two-term, or one-sign equality rows. Minimum row degree is 4.
- Exactly 68 degree-2 columns; all have two -1 entries at one state. They can be
  made singletons by changing that state's row reference, but eliminating their
  variables must retain the induced nonnegative inequality.
- The row/column incidence graph is one connected component.

Before eliminating Z, there are 5,582 groups of literally identical half-row
sum expressions, comprising 5,956 repeated rows. A union-find quotient yields
55,395 Z classes from 61,308 original states. The exact lift sets every original
Z_s equal to its class value. Each positivity coefficient is summed over its
class, preserving the complete ten forms.

After eliminating these quotient Z variables, there are 122,573 equality rows
(only 43 fewer) and 4,677,913 nonzeros versus the original 4,700,782 (0.49% fewer).
The factorized unique-template matrix plus difference map uses 4,469,513 entry
operations, about 4.92% fewer than materialized D. Thus this quotient can reuse
sums but does not expose the main rank reduction. Exact symbolic lift checks,
deterministic integer forward/transpose checks, and all maps are in
[quotient.json](quotient.json), [quotient.py](quotient.py), and
[quotient_maps.npz](quotient_maps.npz).

## Replay

The rank review defaults to a read-only replay against rank_review.json.
Its --seed option changes local transform-column order and constructive
witness choice. Normal and seed 17 replays passed, with logs
[rank-review-check.log](rank-review-check.log) and
[rank-review-seed17.log](rank-review-seed17.log).
A new result may be written with --output pointing to a new file under this algebra directory (the path
must resolve inside this algebra directory and must not already exist).

probe.py, local_probe.py, and quotient.py are **build-only discovery scripts**:
they overwrite their own local algebra outputs when explicitly run. They do
not run by default during the read-only rank check.

From the repository root:

```sh
audits/2026-10-20-w7-count-opt-d5b8a86/py -B audits/2026-10-21-w7-reuse-d5b8a86/algebra/probe.py
audits/2026-10-20-w7-count-opt-d5b8a86/py -B audits/2026-10-21-w7-reuse-d5b8a86/algebra/quotient.py
audits/2026-10-20-w7-count-opt-d5b8a86/py -B audits/2026-10-21-w7-reuse-d5b8a86/algebra/rank_review.py --check
audits/2026-10-20-w7-count-opt-d5b8a86/py -B audits/2026-10-21-w7-reuse-d5b8a86/algebra/rank_review.py --check --seed 17
```

The initial exact sparse scan took about 9 s; the independent literal-map and
Fourier rank review took about 2.5 s. These are structural measurements, not
primal/dual certificates or source realizations.

## Independent specialized-kernel review

The later user request for a specialized operator was checked independently
against the frozen Model with [review_kernels.py](review_kernels.py). The
review compiles its own source snapshot inside algebra/. Three integer-valued
float64 trials match the original C, C transpose, [D;all ten Q], and its
transpose exactly, including adjoints. General float64 forward/transpose
errors are 1.02e-12 / 7.11e-15, with adjoint relative error 5.33e-15.
See [kernel-review.json](kernel-review.json) for the pinned source SHA.

A single-thread CPU benchmark uses equal returned-output allocation costs,
persistent operator scratch, eight warmups, and five batches of sixty calls.
Build/setup is excluded. [raw-benchmark.json](raw-benchmark.json) records:

| Float64 operation | SciPy CSR ms | Unit-incidence native ms | Speedup |
| --- | ---: | ---: | ---: |
| C | 2.751 | 1.980 | 1.39x |
| C transpose | 2.380 | 1.321 | 1.80x |
| [D;all ten Q] | 2.884 | 2.068 | 1.39x |
| Its transpose | 2.638 | 1.402 | 1.88x |

The fused forward-plus-transpose total is 5.522 versus 3.470 ms (1.59x).
These measurements specialize unit coefficients and fuse half-row projection;
they do not yet measure repeated-template packing. Float32 SciPy baselines
are separately labeled in the artifact and are not used for same-dtype speedup
claims. This is operator timing, not end-to-end LP timing.

The public [W7Operator wrapper](../specialized/w7_operator.py) was then
reviewed independently by [review_wrapper.py](review_wrapper.py). All 16
backend/reference/positivity configurations passed exact forward, transpose,
Z recovery, adjoint, and LinearOperator checks. Empty, target-only, reordered
(9,0,7), and all-ten positivity choices were covered. Twenty-five malformed
input, read-only buffer, and alias controls were rejected, and concurrent
calls with separate workspaces passed.

The public-wrapper allocation-matched float64 measurements are recorded in
[wrapper-review.json](wrapper-review.json):

| All-ten operation | SciPy CSR ms | Direct wrapper ms | Template wrapper ms |
| --- | ---: | ---: | ---: |
| Forward | 2.890 | 2.157 | 2.258 |
| Transpose | 2.653 | 1.686 | 2.157 |
| Sum | 5.543 | 3.843 | 4.415 |

Thus this independent run measured about 1.44x for direct and 1.26x for
template, with visible batch noise. These wrapper results include validation
and argument marshalling; the raw-kernel measurements above describe a
different call boundary. The direct wrapper is the local speed choice, while
the template representation shares 333 live incidence patterns. This review
selects no solver, changes no cone constraints, and supplies no exact cone
certificate.

Review shared libraries are transient local build outputs ignored by the local
.gitignore. review_kernels.py regenerates libkernels-review.so from its pinned
source snapshot before raw/template microbenchmarks use it. No original input
files were changed; [final-input-check.json](final-input-check.json) records the
last SHA256 comparison of all nine frozen inputs.
