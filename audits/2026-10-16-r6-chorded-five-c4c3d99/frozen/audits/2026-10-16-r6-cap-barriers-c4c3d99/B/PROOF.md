# R6-CAP-BARRIERS B: common matching alignment of the two barriers

BASE `c4c3d99`; retain the original minimum C5 source, its ordered contacts,
`d_G(x)=d_G(y)=d_G(b)=4`, `d_G(r)=6`, the actual retained-edge
`J=U/(s=t)`, and its spherical dual D. The three marks remain
`e=(vw)*`, `f=(pq)*`, `g=(mz)*`. Nothing below replaces that source by
the re-marked calibration graph in section 4.

The [previous complete-colouring proof](../../2026-10-16-r6-joint-zero-c4c3d99/B/PROOF.md#b2-global-minimum-with-both-directions-included)
derives from the actual Sigma319 ABCDB row an even-complement PM containing
all three marked edges. Write P111 for **all** PMs containing e,f,g;
in particular P111 is nonempty. The arguments below only need this
ordinary nonemptiness, not evenness. The original induced forced pairs
and the [frozen Tutte calculation](../frozen/audits/2026-10-15-three-edge-matchings-6ddea32/PROOF.md)
remain in force. No new external theorem or 4CT is invoked.

## 1. Every violating set is aligned with every 111 matching

Choose either direction, with forced edges a,b and forbidden edge h:
`(a,b,h)=(e,f,g)` or `(e,g,f)`. Put `X=V(a) union V(b)` and
`H=D-X-h`. Suppose S is **any** Tutte-violating set of H; it need not
have maximum cardinality. Let q be the number of odd components of H-S.
The frozen cubic degree bound gives `q=|S|+2`. Alternatively, existence
of any M in P111 proves that equation directly in the next argument.

**Theorem B1 (saturation).** For every M in P111:

1. h joins two different odd components of H-S;
2. each odd component has exactly one edge of M in its D-boundary;
3. every vertex of S is matched to a different odd component other than
   those two; all even components are matched internally;
4. M contains no edge inside S or between S and X.

**Proof.** Since a,b belong to M, no other edge of M meets X. Every odd
component C has an odd, positive number of M-edges leaving it. All such
edges go to S, except that h can contribute at most two incidences when
its endpoints lie in different odd components. There are at most |S|
matching incidences available from S. Since H has even order,
`q-|S|` is positive and even, hence at least two. Therefore

`|S|+2=q <= sum_{C odd}|M intersect delta_D(C)| <= |S|+2`.

Equality holds throughout. Each odd component consequently receives one
incidence, every S vertex supplies one, and h supplies two. These facts
give statements 1--4. In particular no matching incidence remains from S
or h to an even component, and X has none; every even component is
matched internally. This argument applies separately to every M in
P111, on the same D and the same S. QED.

For a maximum-cardinality barrier all components are odd and
factor-critical. The theorem supplies the previously undecided value
`tau=1` for **every** barrier, and turns its budget into

`sum_C mu(C)+|E_D(S)|+|E_D(S,X)|=2`.

After the previous all-singleton exclusion the surviving table is thus:

| Non-singleton components | Sum mu | `|E_D(S)|+|E_D(S,X)|` |
| --- | ---: | ---: |
| one five-cut component | 1 | 1 |
| two five-cut components | 2 | 0 |
| one seven-cut component | 2 | 0 |

This deletes the old one-five-cut `tau=0` subcase by an arbitrary-size
argument. In the first row the unique edge counted on the right is
absent from **every** M in P111.

The two endpoint components of h have boundary containing the original
edge h. In direction 110 their primal boundary contains mz whenever
that boundary is a five-cycle. Such a component cannot be a retained
W5 cap whose boundary avoids both hubs. Thus if all non-singleton
components in the 110 barrier are hub-avoiding W5 caps, the two faces
incident with mz must each be separate singleton components. For 101
the corresponding boundary contains pq; no hub-avoidance conclusion is
asserted from that fact alone.

## 2. Both barriers impose tight cuts on the same nonempty family

Assume both ordinary families are empty, and choose one maximum barrier
in each residual. By B1, every component C of either barrier satisfies

`|M intersect delta_D(C)|=1 for every M in P111`.             (B2)

The quantifier is common: the same entire P111 family satisfies all
these equations simultaneously. It is stronger than choosing a separate
matching witness for each barrier. The source-supplied even matching is
one member satisfying all equations, but B2 does not make it a joint
110/101 matching.

There is an elementary compatibility rule for crossing components.
Let C come from one barrier and K from the other, and suppose their
intersection, differences and exterior are nonempty. Both C and K
have odd cardinality. Then:

* If `|C intersect K|` is odd, both intersection and union have a tight
  cut as in B2; every M in P111 avoids edges between `C-K` and `K-C`.
* If `|C intersect K|` is even, both differences have tight cuts as in
  B2; every M in P111 avoids edges from the intersection to the exterior.

For the first case use the edge-count identity

`|M cap delta(C)|+|M cap delta(K)|`
` = |M cap delta(C cap K)|+|M cap delta(C cup K)|`
`   +2|M cap E(C-K,K-C)|`.

The left side is two. Each of the two odd sets on the right must have
at least one matching edge leaving it, so both counts are one and the
last term vanishes. For the second case use the same identity with
the two odd differences and twice the matching edges between the
intersection and exterior. This proves the rule for every common M.

This exact common-family restriction is available for further geometry;
it is not a proof that the remaining cut configurations are impossible.

## 3. The exact alternating-cycle test and its limit

Fix any M0 in P111. Then

`P110 union P101 is nonempty`

if and only if there exists an M0-alternating cycle avoiding e and
containing exactly one of f,g. Flipping such a cycle gives the forward
construction. Conversely, the symmetric difference of M0 with a joint
matching splits into disjoint alternating cycles, avoids e, and contains
exactly the omitted one of f,g. Its component containing that edge is
the required cycle. This is a whole-graph equivalence, with every edge
retained. It neither supplies the cycle nor proves that its flipped
matching has even complement.

The alternating-cycle test by itself does not imply that an obstruction
has a cyclic four-cut containing both f and g. Section 4 gives a direct
finite counterexample to that proposed auxiliary implication, even when
M0 has even complement and both forced edge pairs are induced.

## 4. A re-marked frozen control rejects an overbroad shortcut

Use the entire existing `flipped_icosahedral_return` spherical control,
with unchanged primal vertices, edges, faces and their dual indices.
For this calibration only choose dual marks `(e,f,g)=(5,9,29)`, whose
literal primal edges are `(1,8),(2,3),(10,11)`. No source pins are inferred
from this re-marking.

The independent checker enumerates every PM and all Tutte subsets of
both residuals. It verifies all of the following directly:

* the dual is cubic and all cuts of at most three edges are singleton
  cuts; the two forced edge pairs are induced;
* a PM containing all three marks has even complement;
* both ordinary joint families are empty;
* the complete list of cyclic four-cuts is
  `{9,10,13,17}` and `{17,19,23,28}`;
* neither cyclic four-cut contains both f and g.

There are 38 PMs; the unique 111 matching is index 30 and has even
complement. Each residual has four violating sets and one maximum
barrier, and those maximum barriers consist entirely of singletons.

This graph therefore refutes the implication based only on those weaker
premises. It is **not a source counterexample**: its primal maximum
degree is six, so it cannot have the required `d_J(m)>=7`; its re-marked
edges also have no declared original two-star contact assignment.
The checker explicitly records the absent source premise. The original
source task is unaffected; this control only prevents an unsupported
alternating-cycle shortcut from being imported into it.

The checker retains all PMs (including odd complements), each full
complement-cycle list, all maximum barriers and their common matching
crossings. It checks B1 also on every nonmaximum violating set and
checks the section 2 uncrossing rule between both recorded barriers;
these controls have no crossing component pairs, explicitly recorded as
zero checks. A separate K3,3 algebra control supplies 720 nonvacuous
matching/tight-odd-set checks of the same identity and carries no source
claim. The final replay artifact is [certificate-v2.json](certificate-v2.json);
the initial certificate is retained unchanged for custody.
Normal/seed17 replay, a deliberately corrupted tau value, exclusive
certificate creation and input custody are recorded in VERIFICATION.json.

## 5. Remaining obligation and authority

B1 is an arbitrary-size source-conditional structural restriction.
Section 2 is an arbitrary-size same-family identity. Section 4 is finite
negative evidence against a strictly weaker proposed lemma. No supplied
graph realizes the original globally minimum source: source-level
numerical coverage is `not triggered`.

Neither B1 nor the countercontrol settles ordinary joint nonemptiness.
Neither proves `W110+W101>0` or `omega_e=0`. The remaining capped
barriers must still be excluded using the full original geometry, and
the nonempty ordinary-family oddness case remains separate. No smaller
completed source is constructed; the original return cost stays `k+5`.
General `K<=22=K<=5`, the fixed branch `k>=25`, Lean and publication
authority are unchanged. This B directory has no shared-document,
commit or push authority.
