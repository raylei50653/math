# Independent reconstruction of R6-CHORDED-FIVE

Review date: 2026-10-16. Research BASE: `0b639cf`.
Reviewer: a separately delegated research agent. The reviewed file is
[`R6-CHORDED-FIVE/PROOF.md`](../2026-10-16-r6-chorded-five-c4c3d99/PROOF.md).
I read that proof and the source/barrier dependencies before reading any
previous REVIEW. No previous REVIEW was used in this reconstruction, and
no earlier audit file was changed.

**Verdict: the arbitrary-size five-cut conclusion passes this review,
conditional on the stated frozen original-source theorems.** It applies
to every five-cut component of every maximum-cardinality 101 violating
set. It does not exclude the double-W5 case or the nonwheel seven-cut
case. There is no numerical source-realizability claim.

## 1. Inputs independently checked

The actual source geometry gives a simple sphere triangulation J in
which every triangle is facial. This is stronger than saying that an
arbitrary triangulation has triangular faces. Its proof separates old
triangles from new crossed triangles `mAB`: the original cycle
`r-s-A-B-t-r` traps each of v,w not already on its boundary. The proper-C5
small-cap theorem leaves only the original crossed edge vw; the other
cases would force one of the forbidden edges sw,tv. This justifies the
facial-triangle input, including triangles arising from a chord.

References: frozen source-geometry PROOF, sections 2--4 (especially its
lines 81--128); original small-cap theorem in
[`w5/PROOF.md`](../2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md),
sections 2--4. The latter explicitly permits proper C4/C5 cycles meeting
the original outer boundary: the number of strictly internal original
vertices is less than the global source minimum because at least one
original inner vertex is on the cycle. Thus the induced-C4 sector theorem
does not silently need an all-inner-cycle assumption.

The literal sector decompositions and their endpoint exceptions are
also needed. At m, deleting link edges `vw,z-alpha,z-beta` leaves the
two original s/t paths and the isolated vertex z. At z, deleting
`m-alpha,m-beta` leaves the original alpha-to-beta path through p,q;
pq is the unique transition from the a fan to the c fan. The induced-C4
sector theorem follows by lifting same-sector cycles to original C4s,
whose required diagonals survive the quotient. In the both-hub case,
the original C4s `t-a-u-v-t` and `s-c-u-v-s` exclude exactly the
uncrossed alternatives. These are restrictions of this original J,
not facts about arbitrarily marked triangulations.

The common-111 saturation theorem is used before any claim about
`H[C]=D[C]`: for every common matching, the count
`|S|+2 <= sum_C |M intersect delta(C)| <= |S|+2` is exact. Hence f
joins distinct odd components, neither endpoint is in S or X, and f
is internal to no component. A maximum-cardinality violating set has
only odd factor-critical components. Both qualifications matter.

## 2. Facial ear and the induced expanded C4

Fix an arbitrary five-cut component C. Its connected complement follows
from three-edge-connectivity: two complementary components would each
need at least three edges of the five-cut. Consequently the actual
primal boundary is a simple Jordan five-cycle Q, and C is its entire
dual face set on one side. This side assignment is not an abstract cap
witness. Since f is internal to no component, deleting X and f removes
no edge internal to C; therefore `H[C]=D[C]`.

For a chord xy and the shorter Q path `x-t-y`, the triangle xty is a
triangle of J. One of its sides is an actual facial disk. The other two
vertices of Q are outside that facial disk, so the facial disk is the
ear bounded by xy and the shorter path. If the chord lies on the C side,
its facial dual vertex has only its xy edge internal to C. This is
impossible: a connected nontrivial factor-critical graph has minimum
degree at least two. Indeed, deleting the unique neighbour of a degree-one
vertex isolates it in an even graph of order at least two.

The ear F is therefore exterior and has two distinct edges to C. It
cannot be in another residual component, since the only possible edge
between residual components in D is the single deleted edge f. Thus
`F in S union X`. Adjoining this actual triangular ear produces a disk
whose simple boundary is Q with `x-t-y` replaced by xy, a four-cycle Q'.

Every chord of a four-cycle in this J makes its two triangles the two
actual faces incident with that chord; their union is one side of the
four-cycle and has exactly two faces. Here the expanded C side has at
least four faces, while the other side contains at least three of the
four distinct X faces. This rules out either possible diagonal of Q'.
It also handles a Q with more than one initial chord: selecting any one
chord yields the same contradiction scheme, and the proof of Q'
inducedness excludes every subsequent diagonal without presupposing
that Q was induced.

References: reviewed PROOF, lines 43--71. No missing chord case was found.

## 3. Exhaustive locations of the exterior ear

If F is in S, the expanded disk avoids all of X. It cannot have mz on
its boundary, since both mz faces are outside; inducedness therefore
prevents Q' from containing both hubs. The source induced-C4 theorem
prevents it from avoiding both. At m alone the actual disk interval
avoids all three specified m faces, putting both endpoint rays in one
original sector, contrary to that theorem. At z alone opposite fans
force the interval through pq and hence through face zpq. Since an f
endpoint cannot be F in S, zpq is in C. The other f endpoint is outside
both C and F, so pq belongs to the expanded boundary. Then z,p,q all
belong to an induced four-cycle, impossible because they form a triangle.

If F is in X, the two edges from F to C cannot be F's own forced
matching edge, whose partner is also in X. Thus F's third edge is e or
g and the ear chord is exactly vw or mz. This exhausts X, including
the second face on vw.

For chord vw, an induced Q' containing vw cannot contain m, adjacent
to both v,w; it cannot contain z, adjacent to neither. This contradicts
the source localization of induced C4s.

For chord mz and ear `mz alpha`, write the original Q as
`m-alpha-z-u-v-m`. At m its C interval avoids the three X faces, so v
is in the same original t sector as alpha. The induced Q' order
`m-z-u-v-m` therefore forces u into the c fan. The original C interval
at z then crosses the a/c transition pq, placing zpq in C. Saturation
forces pq to be a boundary edge of the ORIGINAL Q. Its four edges
incident with m or z cannot be pq. The only other edge is uv, and the
induced Q' forbids zv; since both p,q neighbour z, uv cannot be pq.
The beta ear gives the corresponding s/a sectors and the same edge
list contradiction.

In particular `alpha=p` or `beta=q` does not create a missed boundary
edge. For example, if alpha=p, the two original Q edges incident with
alpha are m-p and p-z, neither pq; pq would still have to be uv, which
fails by the same nonedge. Such endpoint identifications merely shorten
the sector path; pq remains its a/c transition. The six named pins are
distinct, so neither p nor q can equal m or z.

References: reviewed PROOF, lines 75--129. All original angular
intervals used here belong to C or to the actual expanded disk, as
specified; no independently selected sector witness is substituted.

## 4. Quantifiers, consequence, and limits

C was arbitrary throughout. Its complement need only be connected
individually; no simultaneous choice of exterior sides is assumed for
different components. Every five-cut component therefore has an
induced boundary. The previously proved induced-five theorem applies
separately to each such C. Its own side-assignment argument is valid:
if C were opposite the W5 disk, all four X faces would lie in that
five-face cycle, where they induce three edges, contradicting
`D[X]={e,g}`.

Thus each five-cut component is an actual complete retained W5. The
exact budget allows at most two five-cut components and forbids
combining a five-cut with a seven-cut. The curvature theorem excludes
the row with only one W5, so the stated residual list is exactly two
W5 components or one nonwheel seven-cut component. This conclusion is
conditional on ordinary 101 failure; it supplies neither ordinary
nonemptiness nor an even complement.

No blocking mathematical defect was found in the reviewed proof. Its
authority remains the original global minimality / secondary edge
maximality contract and the cited proper-cap, sector, and same-family
saturation theorems. Extending it to arbitrary cubic controls, to
direction 110, or to an arbitrary seven-cut boundary would require
additional arguments. There is no change here to the existing k bounds,
the completed-source reconstruction cost, or the unbounded OPEN target.
