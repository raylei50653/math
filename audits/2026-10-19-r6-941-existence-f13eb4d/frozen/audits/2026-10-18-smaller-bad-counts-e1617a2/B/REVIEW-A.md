# B independent review of A's counted exterior cone

Reviewed 2026-10-18, without modifying A-owned files. Verdict: **PASS** for
the stated necessary-condition and finite-certificate claims. No source
realization or smaller-bad conclusion is supplied by this review.

## Boundary block count

The medial interface construction in a triangulated disk is valid. A
mixed triangular face has exactly two cross-side edges, so its interface
segment is unambiguous. Across interior edges the segment degree is two;
at cross-side outer edges it is one. Consequently the interface consists
of disjoint simple circles and proper arcs, with exactly half the boundary
side-transition count in arcs. Cutting the disk by these disjoint arcs
creates one additional boundary-touching region per arc. Interior circles
remove regions not touching the original boundary and do not change the
number of boundary-touching regions. Side regions have exactly the
connectivity of the corresponding induced side graph: same-side vertices
in a triangular face share an edge. This proves
`b=transitions/2+1`, including the zero-transition two-colour case.

Thus applying this restriction before column deduplication is necessary
for every actual triangulated exterior. It does not assert that every
retained boundary partition can occur in an actual graph.

## Complete colouring counts and H compression

For a fixed palette split, the full components are invariant under
switching. Their action on complete vertex-colour assignments is free,
since each component is nonempty and each switched vertex changes colour.
The boundary action has exactly `2^b` distinct literal results; the z
components avoiding the boundary supply exactly the common factor `2^z`.
This justifies an integer orbit weight and includes every private vertex.

The eight palette permutations in H preserve the split, and each commutes
with the within-pair flip `c -> c XOR 1`. Every literal start can therefore
be moved to an H representative without losing its admissible partition
or changing its H-counted column. Column deduplication combines equal
histograms and sums their weights; it never replaces a multiplicity by a
Boolean support indicator.

The left side is the **sum** of extension counts over each H orbit, hence
`h_j N_i`, since N_i counts one literal S4 representative. Direct inspection
of the rebuilt data gives one H orbit of size 4 and 820 of size 8, totaling
6564 literal boundary rows. In particular the two-colour stabilizer is
handled correctly. The 981 columns have total weights distributed as
`2:1, 4:28, 8:280, 16:560, 32:112`, consistent with `2^b` boundary flips.

One fixed split gives a necessary system; common S4-invariant N lets
palette relabelling transfer it to the other two splits. There is no use
of independently chosen boundary counts for separate palettes or graphs.
H-compressed feasibility remains only a necessary condition.

## Exact verification and interpretation

Independently ran:

```
python3 -B audits/2026-10-18-smaller-bad-counts-e1617a2/A/count_cone.py --check
```

The script rebuilt all columns and returned exact success for all 821
integer equations, candidate supports, and the nonnegative integer dual.
It reproduced supports 154/189/225 and forced-zero ids 176,192 only for
source 933. The strict positive coefficients on these two count variables,
together with nonnegative coefficients on all allowed variables and a
zero linear equation, validly force both counts to zero. The simultaneous
positive witness on every other allowed row establishes maximal support
for this necessary cone, without graph-realizability implications.

The frozen original lift masks retain all b,p,h lifts; local candidate
projections are evaluated from the same N. A's explicit limit statements
are appropriate: these integer vectors are not presented as exteriors,
minimal sources, counterexamples to reduction, or complete no-go theorems.
Discovery via LP is separated from the exact replay, which uses stdlib
integer arithmetic. This review did not rerun LP discovery because the
claimed finite facts are certified by exact reconstruction and replay.

## Added 941 controls: same-vector verification

Reviewed the final A section 6 and `check_941.py`, and independently ran:

```
python3 -B audits/2026-10-18-smaller-bad-counts-e1617a2/A/check_941.py
```

The stdlib replay rebuilds the same 981 counted columns and all 91
nonzero noncrossing equal-colour columns. For each separately specified
candidate it checks nonnegative integer counts and orbit weights against
all 821 counted equations, then reconstructs that **same** 274-coordinate
count vector using exact rational signed-span coefficients. Its source
projection is exactly 941, and the specified candidate has mask 932,
including positive acceptance and empty complete projections to all
three negative rows. Replayed positive-support sizes are 30,30,66;
the Q-specified controls have candidate masks `(932,932,249)`, and the
G_B-specified control has `(249,249,932)`.

The positive orbit decomposition also provides the claimed necessary
component closure on each control's own support. A positive H-row
receives a positive orbit column, while a zero count row cannot receive
one by nonnegativity. Hence every participating column remains wholly
within this vector's positive support. Applying H to its stored start
supplies the required literal representative; S4 invariance supplies
the other palette splits. This does not require treating a partition as
an actual graph.

These are valid simultaneous **necessary-model controls**, separately
targeted at each candidate. The signed coefficients are not claimed
nonnegative graph-building instructions, and the count weights are not
claimed to realize one exterior. Thus they block extending the stated
932/933 no-go using these necessary systems alone; they do not construct
a 941 source, a smaller bad graph, or one common vector making all three
candidates bad. The added interpretation remains correctly limited.

## Reviewed final bytes

| A file | SHA256 |
| --- | --- |
| PROOF.md | `c0b06da40351ca974dc3310d4b675a35824a517eb39620a705902184faeaba52` |
| count_cone.py | `426137e961cd431783bea883a0849a84d4be7aaa7a9d68740cbc33d74fcf7176` |
| cone-triangulated.json | `5fee00e34802312570498fac5009b8e4bfc155d8f3712f96140012d01fab420b` |
| triangulated-witnesses.json | `f7b90f350e881211fe38f44b53013df0157f03747e5a110a1b9b64ad8ddef220` |
| solve_maximal.py | `7ef42cfa7a91979643e2768878eda43acd8ee7912086dfe70903e224e0b0245a` |
| check_941.py | `c1f20990a896ad4358381306a0c5edcdec6461efbac7821f2131e3b9b4a7f4ca` |
| 941-counted-candidate-probes.json | `732dcdc7fa33e5bd4613ea59034f4333749935dfe2c70b285fbba2af0392c258` |
| 941-counted-span.json | `fd16ba219fc12f40fbf50f7244698f7c50310de31dc9b1443a4f763076c33947` |
| probe941_counted.py | `65e5195256ef67d31973901fcc2a949a52103f3ed0b7f452e209116e76d54a43` |
| solve_941_span.py | `8c5b44c549ea28d0c45af47a6b9f4ec06dcead5382e979246a575589a3d35100` |

The proof, both exact checkers, and their data were read/replayed for the
conclusions above. `solve_maximal.py`, `probe941_counted.py`, and
`solve_941_span.py` are bound as discovery provenance, not proof dependencies.
Any mathematical change to these reviewed files requires renewed review.
