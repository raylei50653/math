# Independent topology review of the integrated one-long closure

2026-10-13. Reviewed the integrated
`docs/c5_excess_two_n2_one_long_closure.md`, the original local N-diagonal
statement in `artifacts/c5_excess_two_e4/REPORT.md` section 4.1, the fixed
controls report and the root adoption report. No canonical file was edited
by this reviewer.

**Decision: adopt theorem OL within its explicitly stated complete original
N2-55 source contract.** The integrated mathematical argument has no remaining
topology, ownership, row-synchronization or arbitrary-length gap identified
in this review. It closes `(ell,u)=(1,0)` only. The two wording clarifications
below do not add a mathematical premise or alter the proof.

## 1. Source prerequisites and quantifiers

The report retains complete Sigma 933/941, criticality, induced ordered
boundary, full B-touch, original degree-five nonadjacent roots, degree-four
piece vertices, and the two original one-sided pieces. It uses earlier
shared-contact and low-incidence exclusions only to restrict the surviving
long to at least four distinct nonshared contacts. No source outside this
contract is imported from a control.

The cited N-diagonal theorem explicitly applies to a local assignment on
the original N(S), without requiring that assignment first extend to a
colouring of G-S. It gives every common root pin a for every proper boundary
row. Thus OL-C may independently colour the full L and S at the same
literal row and pins; it does not silently assume the exterior extension
that it is trying to construct. The theorem's one-sided and full-B-touch
premises are inherited by the original short S.

The literal closure formula preserves all five named boundary points.
Its row quantifier is separate for each of q0,q1,q3. The resulting subset
condition is necessary for rejection, not a sufficient description of the
full piece relation. No three-point Eq/Diff shortcut is applied to a larger
interface, and no marginal is substituted for a full lift.

## 2. Leaf-cycle minor, including the exact boundary-arc split

For each fixed row, all private vertices of a cycle share that row's cycle
palette. One private contact excludes D, forcing every private vertex to
be a contact. Since the long has no shared root contacts, such a vertex has
one root incidence and exactly one actual boundary neighbour. Comparing
the within-row equalities in the three rows gives equal three-row signatures
and hence one common original boundary neighbour h. This does not require
the cycle palettes in different rows to be equal.

A leaf cycle always has two adjacent private vertices p,q: a triangle has
the two private vertices adjacent, and a longer cycle has an even longer
consecutive private path. Removing them leaves the original whole L
connected, with each of p,q adjacent to a remaining cycle vertex. Removing
p,q loses no actual boundary attachment outside h. In particular, long
support still supplies an attachment b different from h and any given a.

The set R={r,s} union S is connected using S's original mixed contacts,
and has an actual boundary attachment a because S's support is nonempty.
When a=h, the residual L contact used for the R-to-F edge exists because
at least four distinct L contacts existed and only two were removed.

When a differs from h, b is an interior point of exactly one a-h boundary
arc, Q. The other arc P has no b. The bag R union (P-h) is connected using
the original R-a attachment. The bag (L-p-q) union interior(Q) is connected
using the original L-b attachment, and its boundary portion is nonempty.
The arcs have disjoint interiors; all original L vertices, S vertices,
roots and boundary labels occupy their original disjoint classes. The
last edges of P and Q supply each bag's edge to h, while the first edge
of Q at a supplies their mutual edge. This verifies all three adjacencies
between the h/root/residual bags, not only their connection to p,q.
Together with pq and the three edges out of each of p,q, all ten K5
adjacencies are present in the original graph.

No rotation is modified and no colouring property is assigned to the
minor. The argument covers arbitrary leaf-cycle length and arbitrary
remaining block structure. It even handles t=0, since R's boundary
attachment may come from S rather than a root spoke.

## 3. Leaf bridges and the exact owner counts

A private leaf-bridge endpoint has one C edge, one root edge, and two
actual boundary edges. Its H degree is exactly two, so the inherited
boundary-edge injection applies to precisely the vertices used in the
argument. The long-support attachment outside its actual boundary edge
ab connects (L-p) to B-{a,b}; the latter is one connected path because ab
is an actual C5 edge. If both a,b are spoke endpoints, R has actual edges
to both, possibly from different roots. The remaining contact supplies
R-to-F. Thus the second K5 model is also complete.

At least two distinct leaf edges are then required in cl(T) but not wholly
in T. The explicit three-row formula has at most one additional point h;
both leaf edges must be incident to it, and edge injection makes them the
two different incident edges. Their other endpoints lie in T. Combined
with the row formula's required pair, this forces T=B-h and four distinct
root-spoke endpoints. Each root has at most two adjacent spokes, so both
have exactly two and their pairs are disjoint. The matching table in the
integrated report is the unique perfect matching on the four-vertex path
B-h, in either original root order.

The total degree equation gives kL=4,kS=2. Mixedness supplies at least one
contact of S at each root, so kS^r=kS^s=1; each root then has precisely two
contacts of L. No unproved allocation of incidences or contacts is needed.

## 4. Full exterior colouring and the last contradiction

For any legal fixed r colour a, J=S+s is connected. Every S vertex has at
least its J-degree many available colours because its complete original
degree is four. The uncoloured root s only sees its already fixed boundary
spokes outside J: rs is absent and L is removed. It has at least
4-t_s=kS^s+kL^s-1 available colours but only kS^s neighbours in J. Hence
kL^s>=2 makes s a strict-list vertex. A reverse spanning-tree order rooted
there colours all of J on its original vertices, including any shared
S contacts. The fixed r satisfies all its spokes by construction.

The resulting exterior tuple has one actual s colour. Keeping that whole
tuple fixed, a boundary collision at an r-contact of L provides L's strict
list vertex regardless of this actual s colour. The lift is therefore on
one original row and one shared root-pin pair, with every original edge
covered. Repeating the statement for the three rejected rows gives the
owner-specific closure, and the final table makes it incompatible with
either leaf edge. All quantifiers used by this last step are satisfied by
the owner counts proved in section 3 above.

The standalone greedy exterior lemma does not use the shortness of S.
The complete one-long exclusion does use shortness in N-diagonal at its
start; it cannot be exported to the two-long branch without a replacement
for that implication.

## 5. Wording clarifications and evidence limits

Two wording clarifications were sent to the root integrator:

1. Replace any wording such as "the three rows have the same palette"
   by the exact statement that private vertices share their block palette
   **within each row**, and the resulting three boundary-colour signatures
   agree. The proof requires no cross-row palette equality.
2. Describe the remaining two-long gap using the missing short all-colour
   diagonal implication, rather than claiming the standalone exterior
   greedy lemma inherently requires the other piece to be short.

Both corrections were subsequently verified in the canonical report:
section 3 now states the palette equality within each specified row, and
the final scope paragraph identifies the missing short diagonal premise.
The adoption decision above applies to this corrected integrated text.

The minor controls only check three named original-edge constructions.
The five-boundary-point tables only check their finite literal arithmetic.
The fixed full-fibre controls check whole tuples, empty cells, named
partitions and same-row joins. None realizes a complete N2 target or
replaces the arbitrary-size paper argument. The integrated report correctly
keeps target `not triggered`, the two-long branch OPEN, and Lean
formalization distinct from the existing project build.
