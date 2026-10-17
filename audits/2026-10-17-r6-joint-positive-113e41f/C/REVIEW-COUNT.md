# Independent C review of the full-nine-boundary count compression

Reviewed `integration/full_count_cone.py` with SHA256
`0ae5388b7e3c7727d2ecd5ffd6553f22e53bf5dd67a6927758a4df3ce35ca851`.
The reviewed 932 certificate SHA256 is
`3103cb0edd7e8115a5e3a6d5fa2684c435516cab2d234c60120802b378d12d9b`.
Other root certificate replays do not substitute for this independent
review's explicitly bounded full-labelled reconstruction below.

Verdict: the compression is a sound *necessary count relaxation*. Its
feasibility is credible. The omitted global component compatibility and
planar-source realization remain omitted and no positivity theorem follows.

## 1. The factor eight and the shared variables are correct

Fix one absolute complementary palette partition P, such as AB/CD. A
canonical proper nine-cycle row uses at least three colours. Its S4 action
is therefore free: there are exactly 24 literal rows, even when precisely
three colours occur, since the remaining fourth colour has a unique image.

As those 24 rows vary, canonicalizing the colours transports P to one of
three relative complementary partitions. The stabilizer of an absolute
partition has order eight (two independent swaps and exchanging the two
palettes). Consequently each of the three coordinate classes consists of
exactly eight literal rows. A common full-graph colour permutation gives
the same full-colouring multiplicity N_i to every literal row of canonical
class i. The projected count at each of its three coordinates is therefore
`8 N_i`. A single common variable n_i at those three coordinates is sound;
the root system uses n_i=8 N_i, with homogeneous scaling available.

The factor eight must not be silently ignored when identifying n_i with
an actual fixed-literal count. It is harmless for this homogeneous
feasibility test and positive-support inequalities. The root description
already scopes it as a projected common count.

## 2. Cube projection retains exactly the needed multiplicity

For a fixed P, independent swaps on all actual two-colour components form
a whole cube. If b components meet the pins and h miss them, all `2^b`
literal pin rows are distinct and each occurs `2^h` times. The root
`Counter` projects every literal cube member, rather than projecting a
set of canonical rows. Multiple members at the same `(canonical row,
relative palette partition)` coordinate contribute their full multiplicity.
An actual complete cube consequently contributes a positive multiple of
one of the root vectors. The private-component factor `2^h` can be part
of its nonnegative weight.

Every actual cube appears: normalize one member by a global permutation;
its absolute P then becomes exactly one of the three relative partitions
that the root enumerates. The normalized component intersections satisfy
the retained original nine-cycle edges and the noncrossing boundary rule.
The entire cube remains inside the frozen necessary full-row domain, so
it survives the root's whole-vector domain check. Relabelling that cube
back recovers the original projected vector. This does not assert that
every enumerated noncrossing partition is realizable.

Missing-colour completion in `coordinate` causes no ambiguity here: every
row has at least three colours, hence at most one missing colour. Its
image is uniquely determined. A two-colour row would require a separate
argument, but an odd nine-cycle has none.

## 3. Independent reconstruction on all 24 literal rows, source 932

`C/review_count.py` does not import the root partition, orbit or coordinate
helpers. It independently:

* builds all nine-boundary component partitions by vertex-block recursion;
* checks noncrossing by direct alternation of each two pairs of endpoints;
* enumerates every full literal component cube;
* relabels each to one fixed absolute partition;
* explicitly reconstructs the 24 literal frames and their three groups
  of eight, including every coordinate multiplicity;
* expands the supplied compressed feasible weights onto whole literal
  cubes and verifies every exact rational literal-row equation.

For the last step, take one witnessed actual pin cube for a compressed
column and all eight global permutations stabilizing P, each with
one-eighth its compressed weight. These are full component cubes for P.
The stabilizer acts transitively on the eight literal rows in each
coordinate. Thus the expansion has literal row count n_i/8. Duplicated
whole cubes retain their accumulated weights.

The exact results were:

| Quantity | Value |
| --- | ---: |
| Canonical rows | 362 |
| Literal rows | 8,688 |
| Compressed coordinates | 1,086 |
| Independently reconstructed compressed vectors | 522 |
| Whole labelled cube orbits | 1,044 |
| Positive expanded cube weights | 698 |
| Root projected count sum | 318 |
| Literal count sum | 159/4 |

Every one of the 8,688 literal-row equations passed with `Fraction`,
without a numerical solver. Normal and PYTHONHASHSEED=17 outputs agree.
Changing one common count to 999 is rejected. The exact receipts are
`COUNT-REVIEW-NORMAL.json`, `COUNT-REVIEW-SEED17.json`, and
`count-negative-common-count.json` with its retained assertion traceback.
The 933/941 branches were mathematically reviewed through the same
compression argument; this independent full-labelled execution is 932.

## 4. Limits

This verifies algebraic necessity and one supplied feasible rational
solution in a full-labelled engine. The expansion is a pin-component
count model, not a graph. It does not couple the three palette systems'
components through successive exchanges in one actual graph. In
particular it does not prove the new split-source pivotal-component
updates from C/PROOF or supply an actual minimum source. Frozen-row
completeness, all-r source geometry, reconstruction and arbitrary-size
closure retain their separate authorities. No Farkas contradiction,
source realization, even-complement matching or W110+W101 positivity is
obtained from this feasible cone.
