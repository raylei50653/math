# Independent adversarial review of the strengthened proof

Reviewed `../paper/TOPOLOGY.md` against the frozen BASE
`3097ef5be241b7777451a5ef8a663f3987d6b866`, with direct reads of the frozen
arc-spoke closure, arc-size bound, diagonal-three-row, shield-budget and
upstream joint/structure arguments. Reviewer produced the separate basic
profile catalogue and did not author the strengthened topology proof.

**Verdict: the arbitrary-size LL-CUT+diag proof is valid on the stated full
original55 double-long contract. The basic S-only certificate mechanism is
not proved by it.** No abstract feasible profile is certified as a source.

## 1. Premise chain checked

The arc-spoke closure's §1 has the same complete Sigma, criticality, degree55,
nonadjacent roots, two original mixed components, connected full-B-touch H,
one-sidedness and actual-source custody requirements. Its §3 leaf-contact
lemma therefore applies. Its §6 common-boundary-attachment corollary uses
the previously adopted `Sigma(G-e)=Omega` result; it is not a consequence of
arbitrary three-row rejection alone. The strengthened proof keeps that
full-source dependency.

The size-bound §1 repeats this contract. Its §3 **Lemma 2** is the global
injection for original H-degree-two boundary-edge attachments; its §4
**Lemma 3** excludes K4 blocks using the actual connected exterior. The
latter is connected here because the other long is mixed with nonempty
actual support. Thus using bridge/odd-cycle blocks does not import a
minimal-interior/maximal-edge source or a degree-at-least-five/W5 premise.
The new proof never uses the numerical size bound.

The diagonal-three-row §3 low-incidence lemma applies to long mixed C with
at most three actual root incidences. Shared contacts are handled directly;
without sharing, its lists at the fixed pair `(D,D)` coincide with the
already checked owner-independent contact lists. Leaf contacts, cycle
private-point restriction, attachment injection, and support at least three
all hold in the present full source. No root contraction is performed.

For every newly assumed failed diagonal, full degree-four lists satisfy
`|L(v)|>=degree_C(v)` on the entire original C. Tightness and the disjoint
incident block-palette representation are exactly the adopted degree-list
input. The proof reasons about the complete fibre being empty; it does not
infer global rejection from an isolated block calculation.

## 2. Original bags, edges and connectivity

For K5-H, choose `a` in the other long's support outside h and `b` in C's
support outside `{a,h}`. Both exist by support size at least three. The
boundary a-h arc A avoiding b and the complementary arc A' containing b
partition B as claimed. The fifth bag contains the interior of A', including
b; thus A' has at least two edges, and both the h-to-fifth and fourth-to-fifth
boundary cross edges genuinely exist. The fourth bag attaches to the other
long at a. The fifth attaches to C0 at b; p,z only attach to h, so the b edge
survives. The triangle case leaves one C0 vertex and both remaining cycle
edges still give the required adjacencies. Neither a nor b is contracted
because of a color equation. All five bags are nonempty, disjoint and
connected, and all ten required cross edges are original.

For K33-O, `r union C'` is connected because C' is mixed. The second s-C
edge ends in C0: s has at least two distinct original contact edges, z uses
one and p is nonshared and r-owned. The B-C0 edge exists because p,z remove
at most two actual support positions while C has at least three. The other
long supplies both its r connection and the original s-C' and B-C' edges.
The six bags are disjoint and connected, and all nine required cross edges
are present. Extra edges inside or between bags do not invalidate a minor.

## 3. Leaf, sole-block and shared cases

A shared contact has repeated external D at its two root edges, giving
strict slack and a full diagonal lift. Hence every assumed diagonal failure
is legitimately restricted to no-shared C.

At a private cycle contact the list excludes D, while an ordinary private
cycle vertex's list contains D. Equality with one cycle palette forces all
private vertices to be contacts. There are at least two adjacent private
vertices in a leaf odd cycle. In a sole cycle, every vertex is private and
mixedness supplies a contact. These cases require no unstated leaf theorem
for a one-block graph.

A private bridge endpoint in a failed diagonal has one root edge and two
distinct adjacent B attachments by complete degree four. A sole bridge has
two such endpoints; it therefore has exactly two root incidences when
nonshared. A singleton long is impossible because it has support at most
two. Multiple blocks always have at least two distinct leaf blocks.

PF correctly uses one fixed original C and the same `(D,D)` in all three
rows. Equality of private cycle lists forces equality of the three-row
signatures of their actual attachment positions. Those five signatures are
injective. K5-H then excludes every leaf/sole cycle. It would be invalid to
choose different attachment representatives in different rows; the proof
does not do so.

## 4. Domain coverage and joins

For (1,1), the incidence totals are (4,4). The only case without a piece
having both incidences at least two is the crossed `(1,3)/(3,1)` split,
which is cut by total capacities. Otherwise a high/high piece accepts all
three diagonals, and its partner is either high/high or has at most three
incidences. Thus an existential low-incidence escape is paired with a
universal all-three acceptance, not another unrelated existential row.

For (2,1), the piece Q with two r incidences has at least two s incidences
after the explicit basic total-capacity cut. A failed diagonal has no leaf
bridge. K33-O makes each private cycle path have one owner; s-owned paths
contradict K5-H, and two r-owned leaf paths require four r incidences while
Q has two. A sole cycle cannot change owner and would cease to be mixed.
The other piece has at most three incidences and joins in the same row.

For (2,0), Q similarly accepts all three diagonals: s-owned private cycle
contacts are impossible because W_Q^s is empty; two r-owned leaves exceed
its two r incidences. Only P=(1,3), Q=(2,2) remains after the low-incidence
cases. If P has no diagonal escape, PF leaves at least two bridge leaves.
They must be s-owned because the permitted r attachment set contains no B
edge. Original attachment injection makes their two boundary edges distinct.
A three-vertex support has exactly those two boundary edges, yielding
W_P^s=S_P. A literal three-color row then forces three zeros in each of the
two 2-by-4 matrix rows, contradicting their lower bound two. This final
`2<=1` cut is justified by original edges; it is not an assumed complete
acceptance table.

Every successful join uses one original q_i, the same pins r=s=D, and both
complete original piece lifts. No root-root edge exists, D is absent from
B, and there are no cross edges between P,Q as original components. Hence
all original edges are covered; free isolated coordinates retain the product
factor. The complete Sigma assumption supplies the designated rejection
contradiction, with all structural consequences retained.

## 5. Scope and evidentiary limits

The 19,229 basic feasible projections in `../profiles/profiles.json` remain
valid projected data with their three explicitly feasible matrices; adding
a proven diagonal lift changes the sufficient acceptance sets. Accordingly,
source exclusion by +diag must not be phrased as a failure of those basic
matrices or as a proof of the basic certificate route.

The proof has no complete-source positive control and introduces no Lean
theorem. Finite controls can test arithmetic, exact original bags and full
lifts on their own stated local hypotheses; zero full-source triggers are
not an empirical source exclusion. Parent N2 / E-ARC2 adoption requires its
separate frozen classification coverage check.
