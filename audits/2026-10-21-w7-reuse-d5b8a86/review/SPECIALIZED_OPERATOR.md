# Specialized operator contract and solver integration review

This is a read-only review of the current `solve_lp.py`, `solve_cuopt.py`,
`fastpath.py`, and `model.py` interfaces. It proposes no new cone constraints and
does not run a solver.

## Exact forward and adjoint

Keep the existing coordinate maps: `x[j]` uses the frozen original column ID,
`h[3*s+p]` uses the original live-state order and sorted half-row position, and
`P[l,s]` is the frozen ten-row positivity matrix. Fix one reference `r[s]` per
state, either `h2` or the existing minimum-degree choice. Let `o0[s] < o1[s]` be
the two other positions.

For the 0/1 incidence operator C, define:

```
h = C x
(D x)[2*s]   = h[3*s + o0[s]] - h[3*s + r[s]]
(D x)[2*s+1] = h[3*s + o1[s]] - h[3*s + r[s]]
(R x)[s]    = h[3*s + r[s]]
(Q x)[l]    = sum_s P[l,s] * (R x)[s]
```

These formulas define the operator on **every** input, including an infeasible
x. Equality of the three half-row sums must not be assumed in residual or
adjoint calculations. On a balanced point `Z = R x / 2`, hence
`Q x = 2 P Z`. The positivity lower bound is 2, not 1.

For `A = [D; Q_selected]`, partition a dual input into `y` for D and `v` for the
selected positivity rows. Set `p = P_selected.T v` and form one half-row buffer:

```
w[3*s + o0[s]] = y[2*s]
w[3*s + o1[s]] = y[2*s+1]
w[3*s + r[s]]  = -y[2*s] - y[2*s+1] + p[s]
A.T [y;v] = C.T w
```

For D alone, omit p. For `R.T t`, place t only in reference positions and apply
`C.T`. For `Q.T v`, use `R.T (P.T v)`. No extra factor of two belongs in these
adjoints. All ten positivity rows retain the `model.LABELS` order; a selected
subset keeps the caller's stated row order.

An implementation may fuse these stages or apply precompiled template-local
coefficients. It must produce this same full-order result. Bucket IDs, template
IDs, mask IDs, and any compact quotient IDs are internal and must never replace
the original X or half-row coordinates in saved solver vectors.

## Minimal usable interface

Expose immutable `ref`, `shape`, original input hashes, and:

```
half_sums(x, out=None)                   # C x
half_adjoint(w, out=None)                # C.T w
difference(x, out=None)                  # D x
difference_adjoint(y, out=None)          # D.T y
reference_sums(x, out=None)              # R x = 2Z when balanced
positivity(x, selected=None, out=None)   # Q_selected x
matvec(x, selected=None, out=None)       # [D;Q_selected] x
rmatvec(y, selected=None, out=None)      # [D;Q_selected].T y
```

The selected list, reference choice, dtype, and shapes are part of the operator
identity. An `out` interface and reused work buffers avoid repeated allocations;
document whether calls share buffers or are thread-safe. Validate dimensions,
supported dtypes, and aliasing before entering compiled kernels. If optional
row/column scaling is added, its transpose must include exactly the same
diagonal factors in reverse order.

The current solver matrices use float64. A float64 specialized kernel is a
numerical discovery operator even if its stored coefficients are exact small
integers. Final certificate checking remains exact integer arithmetic in the
existing independent checker.

## What integrates with the existing callers

All three existing solver wrappers materialize sparse matrices:

- HiGHS receives `HighsLp.a_matrix_.start_/index_/value_` arrays.
- OR-Tools receives `QuadraticProgram.constraint_matrix = A.tocsc()`.
- cuOpt receives `DataModel.set_csr_constraint_matrix(...)` arrays.

Those call sites do not expose a callback into which the new operator can be
inserted. A specialized `LinearOperator` wrapper alone does not make these
existing solves matrix-free. Immediate integration targets are independent
residual evaluation, dual pricing, positivity/statistics evaluation, and any
new iterative algorithm explicitly written against `matvec/rmatvec`.

A new PDHG loop could use the operator directly while preserving the existing
box formulation `lo <= A x <= hi`, `x >= 0`, objective `c.T x`. Its convergence,
preconditioning, stopping tests, warm starts, and numerical robustness would be
new work. Operator benchmarks must not be reported as LP solve speedups.

If CSR export is retained for existing solvers, record assembly time and memory
separately from specialized multiplication time. The exactifier still requires
restricted explicit matrices and an exact basis solve; this operator does not
remove that requirement by itself.

## Acceptance checks before integration

Compare all forward and adjoint functions against the existing explicit model
for both reference choices, using signed inputs as well as nonnegative inputs.
Check target-only, all-ten, and a reordered selected subset. Check each
positivity row individually and verify `dot(Ax,y) == dot(x,A.Ty)` within an
appropriate float64 error bound. Small integer input tests can additionally
compare exact expected integer outputs, with magnitudes kept below float64's
exact integer range. A random dot-product identity alone is insufficient because
the same coordinate permutation or scale error could affect both directions.

Include zero and sparse basis-vector inputs, repeated calls into reused output
buffers, and malformed shape/dtype cases. Preserve the original reference choice
when comparing existing warm-start files. A negative control should perturb an
index or sign in a copy and confirm that independent comparisons fail.
