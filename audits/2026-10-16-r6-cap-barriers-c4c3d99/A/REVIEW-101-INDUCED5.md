# Independent review: induced five-cut components in direction 101

Verdict: **PASS**, with the induced-boundary premise retained exactly.
This reviews the proposed C corollary against the original source link
orders and B1's actual forbidden-edge placement. It adds no code and
makes no claim about noninduced five-cut boundaries.

Fix the same original source and direction 101. Thus the forced dual
edges are e=(vw)* and g=(mz)*, the forbidden edge is f=(pq)*, and X is
their four actual endpoints. Let C be any non-singleton component of a
maximum Tutte barrier whose primal five-cut boundary Q is induced.
The frozen three-edge-cut bound makes the five-cut a bond, so C is the
complete set of dual faces on one side of this simple Q.

Both faces on mz, namely mz-alpha and mz-beta, lie in X. The face mvw
also lies in X. Consequently none belongs to C. At any vertex of Q,
the faces on the C side occupy exactly one of the two intervals between
the two Q-rays in its cyclic link. This is a local Jordan-curve fact;
it does not select an independently drawable sector or omit intermediate
faces.

1. **Q contains both m,z.** Because mz is retained, inducedness forces mz
   to be a cycle edge. But both faces on mz lie in X and outside C, so
   mz cannot belong to the boundary of C. This case is impossible.

2. **Q contains m alone.** Its two m-neighbors lie in the literal
   partition L_s union L_t. If they lie in opposite sectors, one interval
   in link(m) contains the edge vw and hence the face mvw; the other
   passes through z and includes both faces mz-alpha and mz-beta.
   Each possible C interval therefore contains a forbidden X face.
   Thus the two neighbors are in the same original sector. C1's
   lifted-pentagon theorem supplies a W5 on one side of Q.

3. **Q contains z alone.** Its two z-neighbors lie in L_a union L_c.
   If they lie in opposite sectors, the two link intervals are the one
   through pq and the one through m. The latter includes both mz faces
   and cannot be the C side. The C interval must therefore contain the
   link edge pq, that is, the entire triangular face zpq.

   By B1, f joins two different H-S components. Since zpq is one endpoint
   of f and belongs to C, its other endpoint lies outside C. Thus
   f belongs to delta_D(C), and the original edge pq belongs to Q.
   But Q already contains z, so its induced subgraph would contain the
   triangle zpq, impossible for an induced five-cycle. Therefore the
   two z-neighbors lie in the same original fan. C1 again supplies W5.

4. **Q avoids both hubs.** The frozen source short-cap theorem supplies
   a retained W5 on one side of Q.

In each surviving case the W5 side is C itself, by A3's side-assignment
lemma: otherwise X would be four vertices in the dual pentagon, inducing
three edges instead of the exact source pair D[X]={e,g}.

The literal endpoint coincidences alpha=p and beta=q cause no exception.
They shorten the a/c fan intervals but retain the link edge pq and both
link edges incident with m. Likewise a Q-ray at an endpoint of a marked
face leaves that face wholly in one of its two face intervals. The
interval arguments above include such endpoint positions.

Hence every induced five-cut component in a 101 maximum barrier is an
actual W5 component. A3 excludes a sole such component. Two such
components are still governed by A4's exact two-wheel restrictions;
they are not excluded by this corollary. A sole five-cut barrier in 101
must therefore have a noninduced boundary. No noninduced case, ordinary
matching existence, or even-complement positivity has been proved here.

Reviewed dependencies:

* [Original source geometry, sections 2 and 5](../../2026-10-15-j-source-geometry-6ddea32/PROOF.md).
* [Original sector definitions](../../2026-10-16-r6-joint-zero-c4c3d99/C/PROOF.md#c1-literal-sectors-and-the-exact-small-cap-premise).
* [B1 common matching saturation](../B/PROOF.md#1-every-violating-set-is-aligned-with-every-111-matching).
* [C1 lifted pentagons and side assignment](../C/PROOF.md#c1-induced-pentagons-that-do-not-cross-an-original-sector).
* [A3 wheel exclusion and side assignment](PROOF.md#a3-no-single-wheel-barrier).
