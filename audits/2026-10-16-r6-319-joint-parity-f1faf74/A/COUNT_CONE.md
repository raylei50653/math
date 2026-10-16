# Final count-cone attempt: the common-count relaxation is exactly feasible

This uses C's conditional original-v5 screen, in which each original
source mask932,933,941 leaves the same58 canonical H rows and forces
both actual cap masks to1022. It adds a multiplicity test to those
necessary support conditions. **The test is feasible and gives no
complete319 or v5 exclusion.** The feasibility certificate is exact
rational arithmetic; it is not a graph realization.

## 1. Why the variables represent one common count vector

Use the same actual H with ordered pins `(z,s,j,i,w,t,p,q)`.
Let `n_r` be the number of full H colourings restricting to a fixed
literal representative r of one of the58 canonical rows. A common
permutation of all four colours acts bijectively on full colourings,
including private vertices. The retained triangle zpq uses three
colours, so each canonical row has exactly24 distinct literal colour
frames. Every such frame has exactly the same count n_r.

The relaxation explicitly expands these into1392 labelled rows. It
never assigns weight one to a normalized orbit set while discarding
multiple literal members with the same normalization.

Fix one of the three absolute complementary palette partitions.
For one full colouring, all actual two-colour component swaps form
a complete cube. Its component vertex sets remain unchanged throughout
that cube, so these cubes partition the entire set of full colourings
for this fixed palette partition. If b components meet the eight pins
and h components miss them, each of the `2^b` distinct literal pin rows
occurs exactly `2^h` times in that complete cube. Distinct choices on
a pin-touching component change a pin and therefore give different
literal rows. Thus its restriction count vector is a common positive
multiple of the **labelled** orbit indicator vector.

All actual cubes occur among the necessary options constructed by
first pulling the colouring to the original nine-boundary graph
`(c,s,j,i,w,t,a,p,q)` with c=a=z, imposing the actual nine-boundary
Jordan restriction, and then merging only components containing a or
c. The split copies need not be connected before identification.
Every option keeps all component subsets, not only selected moves.
Options leaving the58-row necessary relation are discarded.

There are290 distinct labelled cube-orbit vectors for each of the
three absolute palette partitions. For every labelled row l and each
partition P, introduce nonnegative cube weights x and impose

`sum_{O containing l} x_(P,O) = n_(canonical(l))`.        (1)

All three systems share the same58 numbers n. They do not separately
choose three different row-count distributions. There are4176 exact
row equations. The x variables remain a necessary relaxation: their
three independent decompositions are not asserted to arise from one
actual collection of full colourings and compatible component systems.

## 2. Full support positivity is imposed on that same n

For each of the nine nonempty outer patterns in each actual cap, sum
n_r over the H rows projecting to that cap pattern and require the sum
positive. A row with s=i has no V_i projection; a row with j=w has no
V_j projection. The other implication is enforced on the same row.
For each of the seven U319 patterns, sum over H rows having at least
one legal v lift with that outer pattern and require it positive.

These give25 positivity constraints. Because all equations are
homogeneous, a finite positive common solution can be scaled to make
each of these sums at least one. Empty v and r fibres remain present
in the underlying58-row domain; they are not replaced by invented
lifts or omitted from the count variables.

## 3. An exact feasible witness

`count_cone.py --solve` used SciPy only to find a candidate. The candidate
was converted to `fractions.Fraction`, then every equation (1), every
nonnegativity condition and all25 support inequalities were rechecked
exactly. The active certificate is `count-cone-feasible-v2.json`.
The initial certificate and initial checker remain archived separately.

The exact solution has:

| Quantity | Value |
| --- | ---: |
| Shared canonical row variables | 58 |
| Positive row variables | 52 |
| Sum of canonical counts | 28 |
| Values taken by row variables | 0, 1/2, 1 |
| Nonzero cube weights for the three partitions | 154,159,160 |
| Denominators of all cube weights | 1 or 2 |

Multiplying every variable by two gives an integer feasible vector.
These numbers describe the relaxation, not the colour counts of any
actual graph. In particular they are not source witnesses.

Normal and seed17 verification use stdlib Python and need no numerical
solver. Negative controls remove the third palette decomposition,
remove a whole cube weight, change one shared row count, or delete a
positive projection obligation. All are rejected. A second solve
targeting the active certificate fails with FileExistsError and leaves
its SHA256 unchanged. Full receipts are in COUNT_CONE_VERIFICATION.json
and `logs/count-*.json`.

## 4. Exact stopping point

The count-cone strengthening does not contradict the surviving58-row
necessary domain, even after all25 required support counts are positive
and all three palette partitions share one row-count vector. Therefore
this finite relaxation supplies no Farkas certificate and no exclusion.

The remaining issue is realization and simultaneous component structure
on the same original planar graph, including the original five-vertex
source reconstruction. The feasible vector does not preserve or prove
those missing structures. No new graph, smaller bad source, forbidden
full J colouring, or `W110+W101>0` member has been constructed.
Source realizability remains `not triggered`; full319 remains OPEN.
