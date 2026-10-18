# B. Boundary response and contextual dominance for marked oddness

Frozen BASE `9f1fe84f73aabfa87a33d28754633bae6bf0b707`.
Exclusive audit scope: `B/`. These are arbitrary-size paper lemmas about
finite cubic graphs and their actual matching fragments. They do not
construct a smaller original source or establish joint positivity.

## 1. What is inherited, and what is added

The existing [seven-port interface](frozen/audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/MATCHING.md),
M3--M4, already records selected ports, an actual complementary pairing,
path parity and a closed-odd-cycle bit, including all actual matching
lifts and empty fibres. It already proves exact parity gluing, including
repeated exterior endpoints and zero-length paths. Its tight and ordinary
registries have 560 and 1206 cells before necessary emptiness restrictions.
The existing [seven-five relation](frozen/audits/2026-10-17-r6-seven-five-repair-5b9a7b3/B/PROOF.md)
already preserves all 32 spoke rows and all 15 internal matchings.
Thus calling that data a new state would only rename existing work.

The increment here is an interface for **every boundary size**, an
integer cost for full oddness, associative partial composition, and a
one-sided **contextual dominance** theorem. The theorem removes equality
of all local matching fibres as a prerequisite for a matching-level
replacement. Its reduction direction is explicit. It does not remove
the separate original-source lift and completed-size obligations.

## 2. Domain and exact fragment response

A cubic multipole P has finitely many ordinary vertices, internal
undirected edges, and individually named terminal half-edges, called
ports. Every ordinary vertex has total incidence degree three. Internal
loops are excluded; parallel edges are allowed and retain distinct edge
identities. Each terminal is incident with one ordinary vertex. Different
terminals may be incident with the same vertex. Ordinary connectedness,
planarity, factor-criticality and an odd number of ports are not needed.

When two multipoles are glued, their ordinary vertex sets are disjoint;
specified terminal pairs become actual edges. No further identifications
or cross-edges are permitted. An embedding-sensitive application must
also fix the actual terminal order and the gluing preserving that order.

A matching fragment m selects internal edges and terminals with exactly
one selected incidence at every ordinary vertex. Let X be its selected
terminal set. Delete selected incidences. Every ordinary vertex then
has complementary degree two and every remaining terminal degree one.
The complement therefore decomposes into closed cycles and paths
pairing precisely B minus X. A path joining two terminals at the same
ordinary vertex has internal length zero. Record

`s(m) = (X, pi, epsilon, mu)` and `c(m) = number of closed odd cycles`.

Here pi is the complete named terminal pairing; epsilon assigns each
path its number of internal edges modulo two; mu is the membership
vector of the specified internal marked edges. A marked terminal's
membership is already in X. Marks on an internal edge must retain the
same edge identity; no relabelling of e,f,g is licensed by this notation.

The primary relation retains every literal fragment m, every full path
and cycle, and all empty fibres. The response used only for optimization is

`a_P(s) = min { c(m) : s(m)=s }`, with `min empty = infinity`.       (B1)

All finite values have an actual minimizing fragment because P is finite.
The state must not be interpreted as claiming that every formal entry is
realizable. For example, with r complementary paths and n ordinary
vertices, counting component vertices gives the necessary identity

`sum(epsilon) + c(m) = n-r (mod 2)`.                             (B2)

Also `n = |X| (mod 2)` by matching degree counting. These restrictions
are retained as empty entries, rather than deleted from the registry.

For b ports and q internal marked edges, the number of formal structural
states is at most

`2^q sum_{r=0}^{floor(b/2)} binom(b,2r) (2r-1)!! 2^r`,          (B3)

where `(-1)!!=1`. Costs can be arbitrarily large as P grows; they are
weights, not finitely many structural states. If all ports lie in one
actual disk and the complementary paths lie in that disk, replace the
double factorial by the Catalan number C_r. This bound is independent
of the number of internal vertices. No boundary-size bound on arbitrary
original sources is claimed.

## 3. Exact gluing and associativity

**Theorem B1 (complete-cut oddness formula).** Let P and E have exactly
the same named port set B, glued label by label. Their matching fragments
m,n combine to an actual perfect matching iff their selected sets agree.
For compatible fragments, form the disjoint union of their two path
systems, and join matching terminal names by edges of parity one.
Every component is a cycle. Let kappa(s,t) be the number of these cycles
whose total parity is one. Then

`odd((P glued E) - (m glued n)) = c(m)+c(n)+kappa(s(m),s(n))`.    (B4)

**Proof.** Agreement on terminal selection covers both ends of every
selected gluing edge once and excludes all other matching incidences
there. Conversely any perfect matching restricts uniquely to such
compatible fragments. Closed complementary cycles on either side remain
whole closed components. Every other global complementary cycle is
obtained uniquely by alternating the two sides' entire paths and actual
gluing edges. Its length is the sum of the internal path lengths and
number of gluing edges, proving the parity and count formula. QED.

Equivalently, superimpose the two pairings on B minus X. Each alternating
cycle has an even number of terminals and thus an even number of gluing
edges. Its parity is the xor of its recorded path parities. The explicit
parity-one gluing edges are preferable for partial composition below.

**Theorem B2 (partial composition).** The same data suffice when only
some terminals are glued and the rest remain exposed. Compatible
selected seams disappear. In the union of complementary path systems
and parity-one seam edges, each component is either a new exposed path
or a newly closed cycle. The former contributes its endpoint pairing
and total parity; each odd latter contributes one to the new cost.
Existing closed-odd costs add. Internal mark vectors and selected
exposed ports are retained; a newly internal marked seam receives its
agreed selection bit. This composition is associative whenever
the underlying named gluing operations produce the same multipole.

**Proof.** In any parenthesization the components are the same actual
paths and cycles after all identifications. Path parity is additive
modulo two. A component becomes closed at most once; after closing it
has no exposed terminal and can never be joined later. Thus its oddness
is added exactly once, independently of the parenthesization. This
also proves that the minima (B1) compose by min-plus convolution: any
composite witness restricts to compatible actual fragments, and any
compatible minimizing fragments glue to a witness. QED.

This permits an arbitrary patch decomposition to use one composition
law, instead of a new table for each C5/C7/spoke presentation. It does
not prove that a small-width decomposition exists for the active source.

## 4. Marked context response and the correct reduction direction

Fix a target predicate A on the **literal combined** mark vector. The
present application is `e selected and exactly one of f,g selected`,
which is precisely `P110 union P101`. This combines the two directions;
separate positivity in 110 and 101 is unnecessary.

For an exterior structural state t, define

`R_P(t) = min_{s compatible with t and A} [a_P(s)+kappa(s,t)]`.    (B5)

Compatibility includes selected ports, named marks, and any explicitly
retained shared constraint key. The exterior closed-odd cost is omitted
from R_P because it is added unchanged. Write Omega_A for minimum whole
oddness among actual matchings satisfying A, with infinity if none.
By B1,

`Omega_A(P glued E) = min_t [a_E(t)+R_P(t)]`.                    (B6)

**Theorem B3 (contextual dominance).** Let P,Q have the same named ports
and compatible named-mark schema. If

`R_P(t) <= R_Q(t)` for every allowed exterior state t,             (B7)

then for every allowed exterior E,

`Omega_A(P glued E) <= Omega_A(Q glued E)`.                       (B8)

Moreover every complete A-matching on Q glued E can be transferred to
P glued E, keeping its actual exterior matching, literal mark identities,
and target predicate, with whole oddness no larger. Internal f,g
memberships may switch jointly from 101 to 110 or conversely. To preserve
each membership separately, compare responses separately for each full
mark vector instead of minimizing over A. Any positive finite improvement in (B7) at the
state of an optimal Q witness gives at least that improvement in (B8).

**Proof.** Restrict a Q witness to its actual exterior fragment n of
state t. Its whole oddness is at least `c(n)+R_Q(t)`. By (B7), choose a
minimizing actual P fragment in (B5) with cost at most R_Q(t), and glue
it to this very same n. Its oddness is at most the original witness's.
Taking a minimum proves (B8). If the original witness exists, R_Q(t)
and therefore the chosen R_P(t) are finite, so no existence step uses
infinity. QED.

It suffices to check all formal exterior states; checking exactly the
source-realizable exterior states can be strictly weaker, but requires
separate knowledge of that realizability. Pointwise `a_P(s)<=a_Q(s)`
is a sufficient stronger condition for (B7). Contextual dominance allows
different P internal states for different actual exterior states; no
single independently feasible internal witness is reused unlawfully.

For a smaller-bad-source argument, P is the **old** patch and Q the
proposed **smaller** patch. The needed direction is (B7): every success
of smaller Q lifts back to old P. If old P glued E has no even
A-matching, (B8) implies smaller Q glued E has no even A-matching.
The opposite dominance direction does not give that implication.

Exact equality of response tables gives contextual equality of optimum
oddness. Neither equality nor dominance asserts equality of matching
counts, all matching fibres, Tait assignments, or original colour lifts.

## 5. Full source rows remain a dependent relation

In the actual research source keep the same original ordered frame,
attachments, rotation, `U319`, all original empty fibres and all original
r lifts. Let lambda denote a complete retained source/colour key, not
independent marginal keys. If admissible full witnesses factor exactly
as a relational join of actual local witnesses on a shared boundary
key, B1--B3 apply separately in each fixed lambda fibre. Empty fibres
remain infinity. A minimizing witness is chosen in that same fibre,
and joins only to its original compatible exterior witness.

That exact factorization is a hypothesis to prove for any source use.
Merely declaring lambda a tag does not prove that a new fragment extends
to a full same-row original colouring or r lift. If those constraints
span the cut, every relevant shared variable must be retained. This may
remove the boundary-only state bound (B3). In particular, the projection
to `a_P` is intentionally limited to a stated optimization query; it is
not a replacement for the full source relation.

To derive `bad -> success or smaller bad` one still needs:

1. an actual realizable Q with the named embedding/mark/source interface;
2. dominance in the needed joint source fibres, with reconstructible full
   same-row witnesses, or a separately proved colour-lift implication;
3. closure of the completed-source class and a strictly smaller completed
   measure after **all** attachments and reconstruction costs are included.

The known `k+5` completed-source cost is not removed by (B3) or (B8).
A finite number of structural states does not ensure small representatives,
dominance, source realization, or a well-founded reduction.

There is also a distinct operation boundary: a one-matching response
does not preserve reachability by specified alternating flips from a
fixed M or a fixed reference M0. It proves existence and optimized
oddness of actual target matchings. Any resulting N differs from M by
actual disjoint alternating cycles, but no prescribed local batch,
fixed-reference component, or marked influence bound is inferred.

## 6. What cannot be discarded

The signed pairing is necessary for the whole-oddness query. With four
complementary terminals and no selected ports, choose two paths both
of odd length, or two paths both of even length, in the same pairing,
with no closed odd cycle. Glue either to an exterior with that pairing
and both paths odd. The first produces two even cycles; the second
produces two odd cycles. Both fragments are realized by cubic ladder
multipoles, with respectively two and three rungs. Thus unsigned paths
are insufficient even when all other entries agree.

Pairing itself is also necessary: keep two even paths and glue to the
same two odd exterior paths. If the pairings coincide there are two odd
cycles; if the pairings differ there is one even cycle. Both pairings
can be chosen noncrossing in the same four-port cyclic order, so this
is not an artefact of nonplanarity.

A Boolean closed-odd bit suffices for existence of an all-even endpoint,
as in the old seven-port interface, but it cannot quantify strict full
oddness descent. A closed triangular prism with its rung matching has
two closed odd cycles; two disjoint copies have four. Both have the same
empty boundary and the same positive bit. The integer cost is needed.

Conversely, the exact number of **closed even** cycles is irrelevant to
the oddness objective but essential for counting all Tait lifts: each
actual even cycle independently has two alternating assignments of the
two other named Tait colours. Keep full witnesses, or additional count
data, for that stronger query. The response table alone cannot certify
the counts W110 or W101, although value zero proves existence of a
matching in their union if the source correspondence is already valid.

## 7. Evidence boundary

The lemmas are proved for arbitrary finite cubic multipoles. No external
theorem or finite search is a premise. `check_interface.py` supplies
small controls of the complete-cut formula, actual selected-port
compatibility, marked joint minima, parity/pairing negative controls,
and the loss from the closed-odd bit. They do not constitute source
enumeration. Additional predecessor bytes are frozen from BASE under
`B/frozen/`, with their provenance in `INPUTS.json`.

No original minimum source, smaller source, joint-positive theorem, or
Lean theorem is supplied. Source realizability is `not triggered`;
full319, `W110+W101>0`, and `omega_e=0` remain OPEN.
