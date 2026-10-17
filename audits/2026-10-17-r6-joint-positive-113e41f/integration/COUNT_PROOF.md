# Full original nine-boundary counts remain feasible

BASE `113e41f7023aa00c8257b815ce8727035b648f26`. This calculation strengthens
the preceding 58-row H count test by retaining the actual original disk
`F=G-{x,y,b,r,v}`, its entire ordered boundary `(c,s,j,i,w,t,a,p,q)`, and
colourings with `a!=c`. The three original supports 932,933,941 are fixed
separately throughout. All original five-vertex lifts and their empty
fibres keep their frozen meaning. This is a necessary counting relaxation,
not a source realization or a proof of joint positivity.

## 1. The domain is the entire original F relation

The frozen preceding source proof supplies respective upper relations
with 362,536,662 canonical F rows. Their equal-colour slices `a=c` are
the same 58 H rows, and each row has exactly 24 literal global colour
frames: the odd nine-cycle uses at least three colours, so the colour
permutation action is free. The present checker reads those sealed upper
relations and independently reconstructs every local original lift.

For each complete F colouring, the restored vertices have their original
attachments:

* v joins s,j,i,w,r;
* r joins s,v,w,t,x,y;
* x joins c,s,r,y;
* y joins x,r,t,a;
* b joins a,c,p,q.

The complete legal lifts determine the original G projection. On `a=c`,
all legal v colours determine the U projection; adding si or jw determines
the two actual cap projections. The checker verifies that every retained
row projects inside its fixed original support, U319 and the two 1022
cap supports. Rows with no lift remain in the count domain.

## 2. Palette coordinates retain labelled multiplicity

Fix one absolute complementary partition P of the four colours. The full
colourings split into actual P-component cubes. If b components meet the
nine pins and h components miss them, the visible cube has `2^b` distinct
labelled rows, each with multiplicity `2^h` among the full colourings.
Thus actual counts are a nonnegative sum of the full labelled cube
indicator vectors. Every actual pin-component partition respects the nine
boundary edges and is noncrossing on the actual outer Jordan cycle.
The checker retains every partition satisfying these necessary conditions;
retained partitions need not be realizable by a common interior graph.

There is an exact symmetry compression of the labelled equations. A
coordinate is **(canonical F row, relative palette partition)**. After
normalizing a literal row, normalize the fixed absolute P by that same
colour map; its image is one of the three complementary partitions.
For each canonical row the three coordinates each contain eight literal
rows, the orbits of the order-eight subgroup preserving P. Actual full
colour counts therefore give the same count `8*n_row` in all three
coordinates. Write N_row for this common coordinate count.

For each complete visible cube, enumerate every labelled member before
compression. The vector coefficient of a coordinate is the **number** of
members in it, rather than an indicator of whether it occurs. Some
coefficients exceed one. Canonical rows with each of the three relative
partitions cover all cubes up to a common global colour permutation.
Writing V for these multiplicity vectors, the necessary equations are

`sum_V x_V * multiplicity(V,row,palette) = N_row`,

for all three palette coordinates of every row, with `x_V>=0`, `N_row>=0`.
The same row variable is used everywhere. No palette receives an
independently selected row-count distribution.

Finally, require positive support for every bit of the fixed original G
mask, U319 and both 1022 cap masks. Each condition is a sum over the same
row variables whose full local projection contains that bit. Since the
system is homogeneous, all these finitely many positive sums can be
scaled to be at least one. In particular this keeps the full original
support rather than choosing an original mask independently per row.

## 3. Exact witnesses for all three original source masks

`full_count_cone.py` used SciPy 1.18.1 only to find candidates. The saved
certificates verify every equality, nonnegative weight and positive
projection with `fractions.Fraction`; read-only verification is stdlib-only.

| Original mask | F rows | Compressed cube vectors | Count equations | Positive projections | Positive row counts | Witness total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 932 | 362 | 522 | 1086 | 30 | 338 | 318 |
| 933 | 536 | 1581 | 1608 | 31 | 351 | 531/2 |
| 941 | 662 | 3083 | 1986 | 32 | 285 | 193 |

All 58 equal-colour H rows have strictly positive counts in **each**
witness. All row and cube-weight denominators divide eight. Multiplying
the compressed variables by eight gives integer solutions. The totals
above describe these particular feasible witnesses; no exact optimum
or graph-colouring count is asserted.

Consequently this stronger common-count relaxation cannot exclude a
source, or force any of the 58 H rows to be absent. It retains colourings
with `a!=c` and all original support positivity, so the failure cannot be
attributed just to dropping that part of F. The remaining missing condition
is simultaneous realization of all palette component systems, all private
colourings and their transitions by the same original planar graph.
The independent decompositions in this cone do not supply that condition.

## 4. Replay and authority

For S equal to 932, 933 or 941, replay from the repository root:

```sh
python3 -B audits/2026-10-17-r6-joint-positive-113e41f/integration/full_count_cone.py --source-mask 932 --certificate audits/2026-10-17-r6-joint-positive-113e41f/integration/counts932.json
```

Replace both occurrences of 932 for the other two cases. Repeat with
`PYTHONHASHSEED=17`. Receipts, changed-count/cube-weight/projection negative
controls and exact exit codes are in [COUNT_VERIFICATION.json](COUNT_VERIFICATION.json).
The original upper relations and input identity are bound by
[BASE](../BASE.json); each certificate additionally binds the checker and
its exact input bytes. Generation uses exclusive-create.

This is constructive finite feasibility evidence. Actual minimum source
instances supplied: zero, **not triggered**. It supplies no full J colouring,
no smaller completed bad source and no ordinary-to-even matching bridge.
`W110+W101>0`, the v5 exclusion and full319 remain OPEN. Original
reconstruction still returns k+5; no new external theorem, Lean theorem,
general 4CT, commit or push is used.
