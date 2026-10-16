# Independent audit of the unrestricted degree-excess cancellation

Research BASE `120aae90cab8bc4881916adc598cf344f2f20f4b`.
This review independently reconstructs the general argument from the
sealed seven-disk proof, without an I=5 or I+B=12 assumption. It also
checks the earlier maximum-barrier classification needed to infer
ordinary101 existence. The intermediate [RIGIDITY](RIGIDITY.md) proof
remains a valid retained special case.

**Verdict: PASS.** Every remaining seven-cut maximum101 barrier is
excluded for arbitrary source size and arbitrary nonnegative degree
excess. Together with the already established exclusions of the other
barrier rows, this proves `P101` is nonempty for the exact original
source. It does not prove even-complement positivity.

## 1. The exact graph and identities used

Fix the same original G, legal J, actual dual D, literal e,f,g, and a
maximum-cardinality violating set S for `H=D-X-f`, where
`X=V(e) union V(g)`. After the earlier exclusions, its only nonsingleton
component C has seven cut edges. The sealed seven-disk proof supplies:

* C is the complete face set of an actual disk R with simple boundary
  Q of length seven, and there are no Q chords on the R side;
* the interior avoids the six distinct `T0={m,z,v,w,p,q}`;
* every boundary vertex has `t_u>=1` strictly interior neighbours and
  disk degree `d_R(u)=2+t_u`;
* the complete monochromatic-edge set is the three literal marked
  primal edges plus every nonboundary R edge;
* all J triangles are actual faces, and induced C4s obey the exact
  source-sector restrictions;
* writing s_u for complete degree minus its parity-dependent minimum,
  every s_u is nonnegative and even, with

`Delta=sum_all s_u=I+B-2 epsilon-10`.                         (G1)

No equality restriction on I+B is imposed. Put

`Delta_i=sum_strictly_inside_R s_u`,

`beta_u=t_u mod 2`, `ell_u=2-beta_u` for u on Q.

Every strictly interior vertex is ordinary and its complete parity is
its ordinary complete degree parity. Consequently

`sum_inside (6-d_J(u))=I-Delta_i`.

The exact disk curvature formula is therefore

`sum_Q t_u=8+I-Delta_i`.                                   (G2)

This formula preserves the whole interior contribution; excess is not
discarded on an unbounded family of even interior vertices.

## 2. Recheck of every boundary bound

The marked-edge baseline is even at ordinary vertices and odd at T0.
Adding the internal disk incidences flips a boundary parity exactly
when beta is one. The resulting complete degrees are:

| Boundary class | Complete degree |
| --- | --- |
| ordinary | `6-beta+s_u` |
| v,w,p,q | `5-beta+s_u` |
| z | `7-beta+s_u` |
| m | `7+beta+s_u` |

These formulas include arbitrary excess, which is the essential
extension beyond the previously reviewed equality stratum.

### Ordinary boundary vertices

Here `d_J(u)-d_R(u)` is a nonnegative even integer. If it is zero,
the R interval uses all but one complete face at u, and the remaining
face is the actual exterior triangular ear on the two Q neighbours.
In this case

`t_u=ell_u+s_u+2`.

If it is nonzero, it is at least two and

`t_u<=ell_u+s_u`.

Let h count these ordinary actual ear centres. There is no bound on
their complete degrees: an ear may have many strictly interior
neighbours, and the displayed formula charges all of them through s_u.

### The four pins

For v,w,p,q, the difference `d_J-d_R` is odd and nonnegative, hence
at least one. Therefore `t_u<=d_J-3=ell_u+s_u`. Such a vertex cannot
be an ordinary ear centre and has at least two exterior incident faces.

### The vertex z

The face zpq is always outside R, for arbitrary I and excess. If it
belonged to C, all three vertices would be on Q, since all avoid the
strict interior. All three edges would then have to be Q edges, since
an R-side chord is forbidden. That would be a triangle in a simple
seven-cycle, impossible.

If z lies on Q, both actual mz faces and zpq are three distinct exterior
faces. Since the R interval contains t_z+1 faces, this gives
`d_J(z)-t_z>=4`. The displayed degree parity makes this difference
odd, so in fact it is at least five. Thus

`t_z<=d_J(z)-5=ell_z+s_z`.                                 (G3)

Both parts matter: retaining only the two forced mz faces would lose
the required two units. The all-size outside-zpq argument supplies the
third face without a degree-equality premise.

### The vertex m

If m lies on Q, its one C block is in exactly one original s/t sector.
That sector's complete original degree is

`d_G(u)=t_m+5+2k`.

The other sector has no C block, so its original degree is odd and
at least seven. The exact original identity therefore gives

`d_J(m)>=t_m+7`, and hence `t_m<=beta_m+s_m`.

For odd t this is `t_m<=ell_m+s_m`. For even t it is the stronger
`t_m<=ell_m+s_m-2`.

If m is absent from Q, both original sectors have no C block. Their
degrees are odd and at least seven, so d_J(m)>=9. Its parity minimum
is seven, giving at least two excess units outside R and Q. Thus in
both epsilon-zero cases there are two compulsory units, either in the
stronger boundary bound or among the excluded outside excess. These
are two alternatives, not two charges simultaneously assigned to m.

## 3. The unrestricted cancellation

Since `sum_Q ell_u=14-B`, summing the preceding bounds, and assigning
the compulsory two units as just explained, gives

`sum_Q t_u`
` <= 14-B+Delta-Delta_i-2(1-epsilon)+2h`
`  = I+2-Delta_i+2h`,                                      (G4)

where the last equality is exactly (G1). Any excess strictly outside
R and Q not needed at m was dropped only in this upper bound; its
nonnegativity has the correct inequality direction.

Comparing (G2) and (G4) yields `h>=3`. The terms I, Delta_i, B and
epsilon cancel without requiring any of them to be bounded. In
particular the argument covers every higher-curvature and higher-degree
candidate left open by the earlier I=5 and I+B=12 investigations.

Two ordinary ear centres cannot be adjacent on Q: each would prescribe
a different unique exterior face on their common Q edge. Thus the
centres form an independent set of the actual seven-cycle, which has
size at most three. Hence `h=3`.

## 4. Recheck that the existing four-cycle contradiction is general

Each of the three ear faces is zero. Its two old Q edges meet its
ordinary centre and therefore cannot be pq; the complete monochromatic
edge identity gives opposite face bits across those boundary edges.
Filling all three actual faces produces the same closed disk R4 and
simple Q4 as in RIGIDITY, without adding a new source or graph edge.

All six T0 vertices remain on or outside Q4, since the only newly
interior vertices are the three ordinary ear centres. If Q4 had a
chord, one side would consist of two actual triangular faces. Its R4
side has at least six faces: C is nonsingleton odd, and three distinct
ear faces were added. Thus the exterior would have exactly two faces
and no interior vertices, forcing six distinct T0 vertices onto four
Q4 positions. Therefore Q4 is induced. This argument does not need
the former lower bound |C|>=15.

The forced-ear classification and all four source-sector contradictions
of RIGIDITY sections 3--4 use only:

* three ordinary actual zero ears;
* Q4 induced and the same actual m/z sector order;
* the four X faces and zpq's established exterior position.

They do not use I=5, degree five at an ear centre, or zero excess.
No X ear gives the original same-sector contradiction; an e-only ear
forces v,w on Q4 and excludes m, leaving the forbidden z crossing;
a g-only ear has the original compatible m ray and source-forced
opposite z ray, putting zpq inside R4; both types put m,z,v,w on an
induced Q4 containing triangle mvw. Thus all seven-cut barriers fail.

## 5. Rechecked classification-to-existence inference

The following earlier inputs were reopened and checked directly:

1. [Three-edge proof, sections 2--4](../2026-10-15-three-edge-matchings-6ddea32/PROOF.md):
   deletion/supplementation of e,g gives a literal bijection
   `P101 <-> PM(D-X-f)`. If it is empty, the adopted Tutte theorem and
   the independently proved maximum-barrier argument give an odd
   factor-critical barrier with exactly four possible rows: all
   singletons; one five-cut; two five-cuts; one seven-cut.
2. [Singleton exclusion A3](../2026-10-16-r6-joint-zero-c4c3d99/A/PROOF.md):
   the actual source has at least five odd vertices away from T0;
   the all-singleton row has at most four such monochromatic-edge
   endpoints and is impossible.
3. [Common-111 saturation B1](../2026-10-16-r6-cap-barriers-c4c3d99/B/PROOF.md):
   the source-supplied P111 member forces tau one and saturates every
   odd-component crossing in every common matching. This supplies the
   exact zero S budget in the two-five and seven rows.
4. [Five-cut theorem](../2026-10-16-r6-chorded-five-c4c3d99/PROOF.md):
   every 101 five-cut has induced actual boundary and is a retained
   W5. The [weighted curvature A3](../2026-10-16-r6-cap-barriers-c4c3d99/A/PROOF.md)
   excludes the single W5 row, including rims through a hub; it also
   excludes the complete W7 case independently.
5. [Double-W5 theorem](../2026-10-16-r6-double-w5-101-0b639cf/PROOF.md):
   the remaining pair of actual W5 components is excluded for arbitrary
   source size by its actual second-neighbourhood/source-sector proof.
   Its final exclusion does not depend on the optional finite h=3 table.

Thus ordinary101 failure necessarily reaches the sole seven-cut case
just excluded. No other row, larger odd cut, or extra nonsingleton
component is left by the exact cut budget. Therefore

`P101={M in PM(D): e,g in M and f notin M} != empty`.

It follows also that the ordinary union `P110 union P101` is nonempty.
This last statement is ordinary nonemptiness, not joint even positivity.

## 6. Evidence and stopping boundary

This audit is an arbitrary-size paper verification on the frozen source
contract. It is separate from finite arithmetic/patch controls and the
existing Lean build. No new external theorem, source reconstruction,
smaller-source measure, or realization by a finite patch is assumed.

The argument does not prove that the ordinary101 member has even
complement, that `omega_e=0`, or that `W110+W101>0`. The source all-r
condition still forces its forbidden-colouring weighted counts to
vanish; the nonempty ordinary family may contain only odd complements.
Complete319 exclusion, completed-source descent and the general
unbounded catalogue claim therefore remain OPEN. No new Lean theorem,
commit or push is asserted.
