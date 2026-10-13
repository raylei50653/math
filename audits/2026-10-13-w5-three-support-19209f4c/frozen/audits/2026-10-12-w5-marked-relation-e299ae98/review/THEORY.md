# Independent theory review: the full marked W5 relation

2026-10-12. Reviewed against BASE
`e299ae987fcc4cdeb55dd41bede0a3a7c9d9db86`, especially
`docs/c5_degree5_link_reductions.md` and the prior degree5-star-b
`paper/CONTRACT.md`. This is a self-contained paper derivation. It does not
claim to construct an actual minimal outside-K source, a bounded annular
representative, or a Lean theorem.

## 1. Fixed source and the complete object

Let G be a finite simple plane disk graph with fixed outer boundary
`B=(b0,...,b4)`. Let v be an interior vertex whose entire neighborhood is the
induced cycle `U=(u0,...,u4)`, disjoint from B. The closed disk bounded by U
contains precisely the five spokes and v; all remaining vertices, edges,
attachments, and their ownership lie in the closed annulus between B and U.
Write `H=G-v`. The cyclic U order, the embedding, and all original labels are
fixed. Induced means that there is no additional edge between nonconsecutive
U vertices anywhere in H, including outside the U disk.

Take the common colors `C={0,1,2,3}`. For each of the ten fixed representatives
beta of proper B colorings, and **every** `tau in C^5`, retain the full fibre

    J_beta(tau) = {eta: eta is a proper H coloring,
                        eta|B=beta, eta|U=tau}.

There are 10*1024 indexed cells; all empty cells are part of the object. The
full vertex-color map eta is retained, or represented by a provably lossless
encoding. Neither the outer ten-bit projection nor the collection of boundary
supports of five smaller graphs is this object. All color normalization uses
one permutation on the complete coloring.

Only 240 of the 1024 rim tuples are proper C5 colorings: 120 use three colors,
and 120 use four. The other 784 tuples have an empty J fibre in every beta.
These numbers are elementary consequences of the pattern proof below, not
counts of lifts of an unknown annulus.

## 2. Five disjoint sectors, with actual full lifts

Every color class in a proper C5 coloring has size at most two. A proper odd
cycle cannot use two colors. Consequently a three-color tuple has multiplicity
pattern `(2,2,1)`, and a four-color tuple has pattern `(2,1,1,1)`.

For i modulo five define

    E_i(tau) = [tau_(i+1)=tau_(i+3) AND tau_(i+2)=tau_(i+4)].

On a proper C5 tuple the three vertices `u_i,u_(i+1),u_(i+2)` have three
different colors if E_i holds: the third required inequality follows from
the rim edge `u_(i+4)u_i` and the second equality. Thus E_i specifies exactly
the pattern with singleton position i. Conversely every three-color tuple
has exactly one singleton, and the two repeated color classes are exactly
the two pairs specified by E_i. This proves a **disjoint** decomposition:

    {proper tau: |image(tau)|=3} = disjoint_union_(i=0)^4 E_i.

Each sector has 4*3*2=24 literal color tuples. Four-color tuples have a unique
monochromatic nonedge, one of the five diagonals; choosing it and assigning
the four color classes gives another 5*24=120 tuples.

For three-color tau let c(tau) be its unique missing color. For each beta the
following is an explicit bijection of full colorings:

    disjoint_union_i disjoint_union_(tau:E_i(tau)) J_beta(tau)
        <-> C_G(beta),
    eta |-> eta union {v |-> c(tau)}.

The inverse restricts to H and records the singleton i. The fibers and empty
cells are exactly those of the same original J. In particular, for the marked
branch support

    T_i(beta) = [there exists tau with E_i(tau), J_beta(tau) nonempty],

the row identity is `Sigma(G)=union_i T_i`. At this stage T_i is a predicate
on a common annular relation; it has **not** been realized by a legal smaller
disk graph. Existence of the disjoint decomposition does not put T_i in K.

## 3. Five individually legal smaller quotients give an exact duplicate rule

Let `d_j={u_j,u_(j+2)}` be the five diagonals. Draw just one new connecting arc
for d_j in the disk vacated by v, contract it, and simplify parallel edges.
Call the resulting graph Q_j and the named quotient map `pi_j:V(H)->V(Q_j)`.
There is no self-loop, because U is induced. Each identified vertex is an
original interior vertex, so the five B labels remain distinct. The arc lies
entirely in the vacated disk and contraction preserves the inherited plane
embedding and the outer B face. Thus each Q_j is a legal simple disk graph
under these hypotheses. Parallel copies impose the same coloring constraint
and can be removed, with their provenance retained.

For a literal Q_j coloring chi define its pullback `eta=chi o pi_j`. Then

    C_Qj(beta) <-> S_j(beta),
    S_j(beta) = {eta in C_H(beta): eta(u_j)=eta(u_(j+2))}.

The inverse is the unique descent of a map constant on the identified pair.
No color is renamed. All S_j now live in exactly the same full-H-lift universe.

Every three-color rim tuple has exactly two monochromatic diagonals, and
every four-color rim tuple exactly one. Therefore, coefficientwise for each
individual full H lift eta,

    sum_j 1[eta in S_j(beta)] - 1[eta in C_H(beta)]
       = 1[eta extends to v].                              (SIGNED)

The right side is 0 or 1, and an extending eta has a unique center color. In
particular,

    |C_G(beta)| = sum_j |C_Qj(beta)| - |C_H(beta)|.           (COUNT)

The same identity holds **inside every individual named tau fibre**, with
all Q_j sets pulled back to H before comparison. COUNT is a consequence of
the stronger full-lift identity SIGNED, not a replacement for it.

The branch incidences contain a second useful exact reconstruction:

    C_H(beta) = union_j S_j(beta),
    restrict_H C_G(beta)
       = disjoint_union_j (S_j(beta) intersect S_(j+1)(beta)).

Indices are modulo five. A pair of diagonals with indices j and j+2 shares
an endpoint; imposing both equalities forces the adjacent vertices
u_j,u_(j+4) equal, so that intersection is empty. Three intersections cannot
occur because a proper rim uses at least three colors. A consecutive pair
`S_j intersect S_(j+1)` is the sector with singleton `i=j-1`.

It follows that the five full quotient-coloring lists alone recover all of
J: pull each list back with its fixed pi_j and take their union. Recover all
G lifts by retaining exactly those full H colorings appearing in two lists,
then inserting the unique missing center color. Every accepted lift occurs
twice and every rejected lift once. Matching must use the same original
vertex-color map, not independently normalized colors or a row label alone.

If G has k interior vertices, H has k-1 and each Q_j has k-2. This is a
universal exact reduction of the **full named coloring data** to five smaller
legal disk graphs together with their fixed pullback maps and collision
information. It is not an ordinary positive union reduction of ten-bit
boundary relations. Even when all five Q_j lie in K, their ten-bit supports
forget precisely the common-lift collision information needed here.

The bare local counts provide a simple arithmetic check: each Q_j of the
bare C5 has 72 proper four-colorings, the C5 has 240, and W5 has 120. Thus
`5*72-240=120`. An arbitrary annulus changes the full fibres, not SIGNED.

## 4. Why the double quotients and rim-only positive branches fail

The two pairs defining E_i alternate around U. For example, with singleton
u0 the cyclic order of the four other vertices is u1,u2,u3,u4, and the pairs
are `{u1,u3}` and `{u2,u4}`. Two connecting trees for these pair blocks cannot
be disjoint in a disk: a path joining the first pair separates the second
pair's endpoints. Thus the exact three-block quotient is an algebraic
description, but is not a simultaneous legal identification in the vacated
U disk. Abstract planarity of a quotient obtained by forgetting the original
embedding does not repair this local obstruction.

In fact these are all possible three-block independent partitions of C5.
An independent block has size at most two; three blocks must therefore have
sizes `(2,2,1)`, and Section 2 identifies the unique crossing pair partition
for each singleton. A legal noncrossing independent partition has at least
four blocks. This proves that the old sufficient condition "at most three
neighbor blocks" can never be triggered by such a local quotient of an
induced C5.

There is a stronger positive-union obstruction, with a precise local scope.
Consider a branch formed only from the five rim vertices, their rim edges,
optional extra edges, and any noncrossing equality identifications through
the U disk, with no new vertices. Its pullback relation cannot be a nonempty
subset of the wheel-extension relation.

Proof: if it had a proper three-color lift, its quotient would have at least
four independent rim blocks. At least two distinct quotient vertices have
the same color. Recolor one such vertex with the unused fourth color. This
preserves every graph-edge inequality and all equality identifications,
since one changes an entire quotient vertex. It leaves the old color in use
on another quotient vertex, so the pulled-back rim now uses all four colors.
That lift does not extend to the center. Hence any branch containing one
desired lift also contains an undesired lift. Every member of a positive
union representing the target relation would have to be a subset of that
target, so no collection of these branches can represent it.

The argument includes edge-only branches without identifications. For a
single putative edge-only replacement, an even shorter proof is available:
every possible rim chord has equal endpoints in some desired three-color
tuple, so no such chord may be imposed if all desired tuples are retained;
the bare C5 itself admits four-color tuples.

This obstruction is local and universal over annular contexts. A **specific**
annulus can filter every offending four-color lift, so a legal pair quotient
can still be sound or even boundary-equivalent for that particular source.
The obstruction does not rule out such a same-source success, use of hidden
vertices, a change to the annulus, or a different globally embedded smaller
graph. A simultaneous identification outside the U disk would require a new
geometric and ownership proof; this review does not admit it automatically.

## 5. A related binary-relation obstruction

On the desired three-color C5 relation, every color occurs at every single
position. An adjacent pair has all ordered unequal assignments in its pair
projection. A nonadjacent pair has all ordered assignments, both equal and
unequal: one desired singleton sector makes it equal, another makes it
unequal, and a common global color permutation realizes every named pair.

Consequently every proper four-color C5 tuple belongs to all unary and pair
projections of the desired relation. Any conjunction of unary and binary
constraints that contains all desired tuples also contains these undesired
four-color tuples. Thus unary/pair marginals cannot recover even the local
wheel-extension relation, before the harder annular correlation is considered.
This conclusion allows arbitrary unary and binary constraints, not merely
graph edges. It does not exclude a disjunction of conjunctions of crossing
equalities: Section 2 supplies exactly such a disjunction.

## 6. Exact bounded-annulus replacement obligation

Let A=H be the old annular graph with both named cycles. Let A' be a finite
simple annular graph whose two boundaries are precisely the same named,
oriented B and U, embedded in the same annular slot with valid attachment and
edge-ownership records. Suppose A' has r vertices other than these ten pins.
For every beta and every tau require

    J_A,beta(tau) nonempty iff J_A',beta(tau) nonempty.       (ANNULUS)

Every complete fibre must be available with all its literal full lifts,
including the empty cells; (ANNULUS) compares their nonemptiness, not their
cardinality or vertex sets. Attach the original five spokes and a new center
v in the inner disk to obtain G'. A full G lift restricts to one eta in
J_A,beta(tau); choose any full lift eta' in the same A' fibre and retain the
same unique center color. This gives a full G' lift. The reverse construction
uses (ANNULUS) in the other direction. More explicitly, the relation

    { ((eta,c(tau)),(eta',c(tau))) :
         eta in J_A,beta(tau), eta' in J_A',beta(tau), |tau|=3 }

is total on each side and covers every old and every new complete lift.
Here `|tau|` means the number of distinct colors. No cardinality equality or
bijection between different annulus fibres follows or is needed. This differs
from the actual bijections in Sections 2 and 3, which compare the same source
or a fixed equality quotient.

The exact interior count is

    k(G') = 5 named U vertices + 1 center + r = 6+r.

Thus **if** a geometrically legal A' satisfying (ANNULUS) exists with r<=6,
then G' has at most twelve interior vertices and preserves the complete
outer relation of G. Under the upstream theorem `K_(<=12)=K`, this would
exclude the corresponding minimal outside-K source. Neither the ordinary
five-internal-vertex C5 theorem nor the legal quotient decomposition proves
the existence of A'.

For this fixed W5 attachment alone, equality in (ANNULUS) restricted to
three-color tau would suffice for the displayed lift correspondence. Full
(ANNULUS) remains the stated marked-annulus replacement contract, and is
what supports arbitrary further attachments. This observation cannot be
used to erase the other cells from the source J evidence.

## 7. Findings and remaining gap

* `triggered and holds` as a paper identity: five disjoint full-lift sectors;
  each accepted H lift has one center extension.
* `triggered and holds` as a paper identity: five legal individual pair
  quotients reconstruct J and G by pullback multiplicity; the signed
  full-lift/count identities hold fibre by fibre.
* `counterexample` to a universal positive rim-only realization claim:
  splitting a repeated color gives a four-color leak in every branch that
  contains a desired three-color lift. Crossing double identifications are
  not admitted local planar branches.
* `triggered and holds` conditionally: a full marked annular representative
  with r<=6 gives a twelve-interior-vertex replacement and, using the stated
  upstream theorem, contradicts an outside-K source.
* `not triggered`: an actual minimal 933/941 source, an r<=6 annular
  representative for such a source, and a new Lean verification.

The new exact reduction retains more than a row mask: it retains the five
fixed pullback maps and the complete same-source incidences of their lifts.
What remains open is converting this information into a bounded, legally
embedded representative or a positive union of actual smaller disk relations
in K. None of the signed identity, the abstract sectors, or the local
obstruction closes general degree-five reducibility or `K_infinity=K_(<=5)`.
