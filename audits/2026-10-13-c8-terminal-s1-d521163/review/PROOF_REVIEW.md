# Independent review: arbitrary-size C6 terminal support obstruction

2026-10-13. This review is confined to the frozen global-minimum-
interior, then maximum-edge no4ct source contract. It imports no general
four-colour theorem and places no bound on the number of interior vertices
of the remaining original C6 disk.

## 1. Exact support obstruction and the colour frame

Fix one original named source layout. Let D be its six **distinct original**
remaining-terminal boundary vertices, in their original cyclic order. Let P
contain the original B-C8 collar, the complete original zero-single-contact
W5 terminal, all the remaining fixed edges and D. Let L be the actual other
terminal disk. The intersection is the original D; P and L have no edge
between their disjoint private vertex sets. A boundary edge present in both
factors is tested in both, which does not change properness.

For literal colours beta on B and gamma on D, the fibre identity is

\[
 F_G(\beta)=\bigsqcup_{\gamma\in\{0,1,2,3\}^{D}}
     F_P(\beta,\gamma)\Join_D F_L(\gamma).
\]

The union is disjoint because a full original colouring has exactly one
restriction to D. The join equates the colours of the same named original
vertices. In PINCH there is exactly one shared endpoint vertex x, including
in P's fixed terminal; in BRIDGE P retains the original edge xy and tests
its endpoints for different colours. No independent normalization is
performed at either factor of this identity. Empty fibres, including all
improper D assignments, remain empty.

Let Q be the 31 global S4 orbits of proper colourings of a six-cycle. Define
M_P(q) to be the subset of the ten original B rows for which there is a
complete P colouring whose D restriction lies in q. This definition can be
computed while fixing each B row to the original literal representative;
one then records the S4 orbit of its actual D restriction.

Let R_L be the set of orbits that have a nonempty L fibre. Since L is an
ordinary graph with no preassigned colours, an orbit belongs to R_L if and
only if **every** literal member of that orbit has a nonempty L fibre.
Indeed a single global permutation of all colours of a complete L lift
transports it to any prescribed member of the orbit. Therefore

\[
 \Sigma_B(G)=\bigcup_{q\in R_L}M_P(q).                 \tag{R1}
\]

For the forward inclusion, restrict one original full G lift. For the
reverse inclusion, choose the complete P lift witnessing its B row and
actual literal gamma; take any full L lift in q and apply a global S4
permutation to that **entire** L lift to make its D restriction exactly
gamma. Its private vertices are disjoint from P's, so the common literal
join gives the required full G lift. Nothing about the internal size,
degrees, chords or relation of L is assumed in this argument.

For the original target T (933 or 941), put

\[
 A_T=\{q\in Q:M_P(q)\subseteq T\},\qquad
 V_T=\bigcup_{q\in A_T}M_P(q).
\]

If Sigma_B(G)=T, (R1) implies R_L is a subset of A_T, and hence T is a
subset of V_T. Since V_T is already a subset of T by definition, equality
is necessary. Thus

\[
                       V_T\ne T
\]

excludes the entire named layout for **every** actual L, regardless of its
interior size. Empty M_P(q) are correctly permitted; they contribute no B
row and cannot repair a missing target row. This is stronger than checking
only that an accepted target row can be reached, or only a C8 marginal
upper bound. It uses all forbidden and accepted rows of the original
complete B relation simultaneously.

## 2. Independent finite verification

`independent_transfer.py` does not import the primary P assembler,
terminal kernel, colouring routine or transfer routine. It reconstructs
the actual edges from these original data:

* the named B-C8 collar contacts;
* t_i adjacent to c_i and c_(i+1), with the fixed original cyclic order;
* one original endpoint for PINCH, or x, y and the original bridge for
  BRIDGE, each with the original antipodal C8 contacts;
* the two terminal boundary cycles, with the sole single-contact vertex w
  inserted in its specified one of five slots and joined to the
  corresponding original C8 vertex;
* the zero-single-contact terminal's W5 centre and all five original
  spokes.

An independent bit-mask constraint solver then enumerates **every** full
P colouring with each of the ten original B representatives pinned. It
extracts all 31 M_P(q), including zero masks, from these complete colourings.
There are two types, four antipodal pairs, two choices of the occupied
side, five original insertion slots and eight original collar queries:
640 instances. No layout is selected separately for different colour rows.

The independent enumeration counted 2,515,696 full P lifts across the 640
query instances (the two targets sharing a collar deliberately repeat its
counts). All 640 necessary equalities V_T=T fail. In 498 cases V_T is
empty; in the remaining cases it is a proper subset of T. At most three
six-cycle orbits are permitted in any instance. The full independently
computed matrices and ten direct P lift counts are retained in
`independent_transfer.json`.

The final comparison uses `transfer/certificate.json.gz`, not the exploratory
summary. It compares the complete named vertex lists, edge lists, D orders,
all 31 masks, all ten full-lift counts, allowed and missing masks, and every
per-orbit forbidden-row witness. Both ordinary and `PYTHONHASHSEED=17`
replays reproduce the same independent JSON.

Six independent negative controls exercise this comparison and the actual
source graph. Corrupting the allowed union, missing-target mask, an orbit
matrix entry, or one full-lift count is rejected. For the original
`BRIDGE-0-0-0-c15-933` P and B row `01012`, dropping the original bridge
raises the direct complete P colouring count from 660 to 1212. Splitting
the original PINCH shared endpoint into independent copies changes its
corresponding count from 552 to 1212. These controls alter the complete
source patch and expose the additional invalid colourings; they do not
merely compare independent endpoint palettes. Exact results are retained
in `negative_controls.json`.

These computations enumerate a **fixed exterior patch only**. They do not
enumerate L, bound its size, or replace it with any six-private-vertex cap.
The original structural classification proves that every s=1 source has
exactly one of these finite exteriors; (R1) universally quantifies its
unbounded remaining disk.

## 3. Scope of the accepted conclusion

Together with the original zero-single-contact terminal theorem and the
complete source layout classification, the obstruction excludes every
h=3, p in {1,2}, s=1 source. Combined with the previously excluded s=0
branch, it proves h=3 and p>0 imply s>=2 under the stated source contract.

This review does not claim a general C6 extension theorem, a smaller graph
representative for the W5 terminal, fixed-width peeling, elimination of
the eight unbounded h=3 contracts, an h>=4 conclusion, or a Lean proof.
No larger cap search or s=2 search was needed.
