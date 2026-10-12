# Task B: frozen same-source star relations and candidate predicates

This contract is written before inspecting finite operation outcomes. The fixed
control sources and their provenance are recorded in `../INPUTS.json` and the
frozen task. It does not depend on Tasks A or C. Candidate identifiers below are
fixed before the checker evaluates them. A predicate being false on a control
does not assert that the control satisfies the globally minimal outside-K source
identity. A predicate surviving every control is only fixed-domain calibration.

## Named source, colors, and complete fibres

Let G be one finite simple disk graph with fixed ordered outer cycle
B=(b0,b1,b2,b3,b4), a marked interior vertex v of degree five, and its five
distinct neighbors L=(l0,l1,l2,l3,l4) in the chosen source rotation. G, all vertex
labels, original edges, attachments, supports, components, bridges, and their
ownership stay fixed throughout a comparison. A repeated identity between B and
L is an actual shared vertex and imposes literal color equality. No independent
renaming of B, L, components, or colors is allowed.

Use the common color set C={0,1,2,3}. Let beta range over all ten proper C5
boundary patterns, with one fixed representative of each global color-renaming
orbit. For a literal graph X preserving the named B, write C_X(beta) for **all**
proper maps V(X)->C restricting to beta on B. Empty sets are retained. Recovering
arbitrary proper outer color names uses one common permutation on the entire
lift, never a separate permutation on individual pieces.

Put H=G-v. Define the complete interface fibre

    R_beta(tau) = { eta in C_H(beta) : eta(L)=tau }, tau in C^5.

Thus R_beta is a mapping on all 4^5 ordered tuples, including its empty fibres,
and each nonempty fibre retains its full literal H lifts. Shared B/L labels and
all original H edges are tested inside the fibre. A lossless representation may
store all full lifts and the total 4^5 tuple domain, with omitted entries
unambiguously defined as empty. This is not a collection of unary or pair
marginals. Set

    M(tau) = C \ {tau_0,tau_1,tau_2,tau_3,tau_4},
    O_beta = { (tau,eta,c) : eta in R_beta(tau), c in M(tau) }.

There is a bijection O_beta <-> C_G(beta): assign v color c, or restrict a G lift
to H and record its original v color. In particular

    beta in Sigma(G)
      iff exists tau,eta in R_beta(tau): M(tau) != empty
      iff exists eta in C_H(beta): |eta(L)| <= 3.                 (CENTER)

CENTER is true for each individual H lift: that particular lift extends to v
if and only if its five neighbors use at most three colors. This does not say
that every H lift extends whenever one lift does. The statement needs no edge
between consecutive neighbors. Call L a C5 link only after checking all five
consecutive edges literally; no wheel decomposition is otherwise asserted.

## Spoke deletion and legal flip on one common graph

For each original spoke e_i=v l_i let D_i=G-e_i. Every D_i lift can be written
uniquely as (eta,c) with eta in C_H(beta) and

    c notin { eta(l_j) : j != i }.

Set A_i(eta,c)=[c != eta(l_i)]. Then

    C_G(beta) = { delta in C_Di(beta) : A_i(delta) }.             (DELETE)

All old lifts therefore survive deletion with identical colors, but deletion
may add lifts and may add boundary rows. Exact relation preservation means

    for all ten beta:
      C_Di(beta)!=empty iff exists delta in C_Di(beta): A_i(delta).
                                                                  (D-EQ)

Equivalently, each accepted D_i row has at least one lift restoring the original
spoke. It is stronger, and unnecessary, to require every D_i lift to restore it.

A flip is considered only when the two actual incident internal faces of e_i
are triangles (v,l_i,a) and (l_i,v,b), with four distinct quadrilateral vertices,
and the new opposite edge ab is absent. The edge ab must be inserted through
that actual union of faces, preserving the outer cycle and source rotation.
The transformed graph is F_i=D_i+ab. Define the second condition on **the same**
D_i lift by Z_i(delta)=[delta(a)!=delta(b)]. Then

    C_Fi(beta) = { delta in C_Di(beta) : Z_i(delta) },            (FLIP)
    beta in Sigma(G)  iff exists delta in C_Di(beta): A_i(delta),
    beta in Sigma(Fi) iff exists delta in C_Di(beta): Z_i(delta).

All four truth-value fibres of (A_i,Z_i), for every beta, retain complete D_i
lifts, including empty fibres. Restriction/inclusion with identical colors is
the two-way full-lift construction in DELETE and FLIP. Thus exact ten-row
equality is

    for all beta:
      (exists delta: A_i(delta)) iff (exists delta: Z_i(delta)), (F-EQ)

where both quantifiers range over that same C_Di(beta). There need not be a
common lift witnessing both existentials. For a designated beta, the claim
"all old lifts survive" is instead

    for all delta in C_Di(beta): A_i(delta) => Z_i(delta).        (OLD-ALL)

If OLD-ALL holds for every beta then Sigma(G) is a subset of Sigma(F_i). It
does not by itself prove reverse inclusion. A sufficient equality condition is

    (i) for every accepted old beta, some delta has A_i and Z_i;
    (ii) for every beta and delta, Z_i(delta) => A_i(delta).     (F-SOUND)

Condition (i) establishes old-to-new row coverage; condition (ii) gives literal
new-to-old lifts. Both conditions are sufficient; neither is claimed necessary.
The exact equality predicate remains F-EQ.

## Center deletion followed by a legal equality quotient

A proposed quotient is a set partition P of the actual neighbors L; unlisted
vertices are singleton blocks. A nontrivial block identifies its actual vertex
labels, not their positions alone. Let pi:V(H)->V(Q_P) be the quotient map. The
candidate is admitted only after the following source checks:

* every block contains at most one original outer label; each nonsingleton
  block consequently contains at least one original interior vertex;
* no original H edge has both endpoints in one block (no self-loop);
* each nontrivial identification is supported by arcs through the disk vacated
  by the original star, compatible with the original cyclic order; simultaneous
  blocks have disjoint connecting trees, in particular no alternating blocks;
* identify along those arcs, remove v, and simplify only parallel edges, keeping
  each original edge's image and the surviving named B in the embedding record;
* the resulting literal simple graph has the original ordered outer C5 as its
  disk boundary. An abstract planarity flag alone does not certify this face.

The five-neighbor cyclic noncrossing test specifies which connecting trees can
be drawn locally; a literal embedding/face certificate must additionally verify
the resulting disk and B. A pair is nonadjacent precisely when its two actual vertices are
not joined by an H edge; consecutive cyclic positions are allowed when that
edge is absent. Actual H-adjacency is checked independently of the rotation. If the source literal certificate
does not carry a historical rotation, a newly certified rotation is explicitly
an audit embedding choice, not a recovered historical fact.

Define

    E_P(tau) = [ tau_j=tau_k whenever l_j,l_k belong to one P block ].

The exact quotient correspondence is

    C_QP(beta) <-> { eta in C_H(beta) : E_P(eta(L)) },          (QUOTIENT)

with quotient-to-source pullback eta=chi o pi. Conversely a source lift constant
on each block descends uniquely to chi([x])=eta(x). These maps are inverse.
Properness holds because every quotient edge is the image of an H edge and
internal-block edges are forbidden. Removing parallel copies changes no color
condition. Outer labels are not merged, so both maps retain the same beta.
Neither map inserts a center color: this requires a further choice in M(tau).

Therefore

    beta in Sigma(Q_P) iff exists tau,eta in R_beta(tau): E_P(tau),
    Sigma(Q_P)=Sigma(G)
      iff for all ten beta:
        (exists tau,eta: E_P(tau)) iff (exists tau,eta: M(tau)!=empty).
                                                                  (Q-EQ)

An explicit sufficient condition with both lift directions is

    (i) every accepted old beta has some eta with E_P and M!=empty;
    (ii) every eta satisfying E_P has M!=empty.                (Q-SOUND)

For (i), choose that H lift, descend it to the quotient and choose a missing
color to rebuild G. For (ii), pull a quotient lift back and choose a missing
color to rebuild G. The chosen H lift in (i) may differ from a given old lift:
Q-SOUND asserts equality of boundary relations, not preservation of every old
full lift. Preserving all old lifts would require every old (eta,c) to satisfy
E_P(eta(L)); it is a distinct stronger old-to-new property.

If the quotient has at most three blocks on L, E_P implies |eta(L)|<=3 without
using any extra graph premise, so condition (ii) holds. One identified pair
leaves four blocks and gives no such implication: the proper cyclic tuple
(0,1,0,2,3) satisfies l0=l2 but uses all four colors. This tuple is an algebraic
warning; the finite checker must supply an admitted literal control before
calling Q-PAIR-CENTER a fixed-domain counterexample.

For pair constraints E_1,...,E_r, the correct simultaneous condition is

    exists eta in C_H(beta): AND_j E_j(eta(L)).

It cannot be replaced by AND_j [exists eta in C_H(beta): E_j(eta(L))]. The latter
allows different H lifts. Likewise union of branch relations means an OR of
their row predicates and does not prove a simultaneous equality quotient.

## Frozen candidate list and scoring

The following are deliberately proposed sufficient conditions to be tested,
not asserted theorems. An instance is `not triggered` when its antecedent is
false, `triggered and holds` when antecedent and conclusion are both true, and
`counterexample` when the antecedent is true and the conclusion false. Every
counterexample must name a literal source, v, L, operation, row(s), and full
witness lifts. Exact boundary equality always quantifies over all ten rows.

| ID | Admitted operation / quantified antecedent | Proposed conclusion |
|---|---|---|
| D-ANY | A spoke deletion; there exist beta and delta in C_Di(beta) with A_i(delta). | Sigma(D_i)=Sigma(G). |
| D-OLD-ALL | A spoke deletion; for every beta, every old G lift remains a proper D_i lift with identical colors. | Sigma(D_i)=Sigma(G). |
| F-ANY | A legal flip; there exist beta and delta in C_Di(beta) with A_i(delta) AND Z_i(delta). | Sigma(F_i)=Sigma(G). |
| F-OLD-ALL | A legal flip; for every beta and delta in C_Di(beta), A_i(delta) implies Z_i(delta). | Sigma(F_i)=Sigma(G). |
| Q-ANY | A legal quotient P; there exist beta and eta in C_H(beta) with E_P(eta(L)) AND M(eta(L))!=empty. | Sigma(Q_P)=Sigma(G). |
| Q-PAIR-CENTER | A legal single-pair quotient P; a specified beta and H lift eta satisfy E_P(eta(L)). | M(eta(L))!=empty. |
| Q-SEPARATE-JOIN | A legal partition P with at least two constituent pair constraints E_1,...,E_r; for a specified beta, every j has some eta_j in C_H(beta) satisfying E_j. | Some common eta in C_H(beta) satisfies every E_j. |

For Q-SEPARATE-JOIN the constituent constraints are fixed deterministically:
within each nonsingleton block, sort its actual vertex labels, take the least
actual vertex label as representative, and pair it with every other member,
then order pairs lexicographically by actual labels. These constraints are
transported to L positions through the fixed original label map. The
partition must be legal before scoring; incompatible/loop-producing partitions
do not count as counterexamples. No center extension is added to its antecedent
or conclusion: its subject is the exact quotient relation before CENTER.

D-OLD-ALL's antecedent is a universally true edge-deletion identity. Its proposed
equality conclusion is still a candidate, so a deletion expansion refutes that
candidate while leaving the identity intact. Similarly, an F-OLD-ALL
counterexample can only concern reverse inclusion; the established forward
inclusion is a theorem. Separate also F-SOUND and Q-SOUND: they are proved
sufficient paper predicates, to be calibrated by their actual trigger counts.

## Proven scope and remaining obligations

CENTER, DELETE, FLIP, QUOTIENT, their exact ten-row equality criteria, and the
two SOUND sufficient predicates are universal finite-graph identities/proofs
under the stated named-source and operation-legality premises. They do not
require edge-criticality, edge-minimality, a deficiency bound, or the catalogue
minimality assumption. Geometry is a separately verified admission condition.

The fixed 132 literal witnesses and added W5 are controls. W5 has boundary
degree three and fails the conditional minimal-source boundary-degree premise.
No computed success yields a reducible vertex in an arbitrary minimal
outside-K graph. The 933/941 conditional-source branch remains `not triggered`
unless an actual source satisfying its full identity is supplied. General
reducibility, K-infinity=K-at-most-5, and Tasks A/C remain outside this result.
No Lean formalization or Lean verification is performed by this paper proof.
