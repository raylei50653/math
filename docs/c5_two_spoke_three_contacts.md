# Two spokes, three contacts: a same-source K5 obstruction

2026-09-24. This resolves the adjacent (3) case requested in
[the handoff](HANDOFF.md), using the setup and list semantics of
[R10](c5_degree5_interfaces.md). In fact the argument excludes every (3)
two-spoke minimal core, including the previously separated nonadjacent case.
It does not classify (2,1), t≤1, or general degree-5 cores.

## 1. Statement and the actual six-cycle region

Keep the same finite simple disk graph G, induced boundary
B=(b0,b1,b2,b3,b4), q=01012, and U={0,1,2,3}. The effective interior H is a
minimal q-obstruction. Its unique degree-5 vertex z has boundary neighbors
S={b0,b1}; all other interior vertices have complete degree four.
Assume C=H−z is connected, with three distinct, original contacts
P=N(z)∩C. R10 gives F_C(q)={2,3}.

**Theorem. These hypotheses are contradictory.** In particular G cannot also
reject a second three-color pattern while accepting T4. Neither the second
rejection nor T4 is needed for this stronger exclusion.

C remains in the original six-cycle region
(z,b1,b2,b3,b4,b0). No spoke, contact, boundary attachment, or intermediate
bridge is removed to invoke a two-contact theorem. All constructions below
are subgraphs or branch sets in this same G. The boundary order is unchanged.

For a=2,3 put

```
M_a(v) = U \ (q(N_B(v)) ∪ ({a} if v∈P else ∅)).
```

Both assignments are uncolorable and satisfy |M_a(v)|≥deg_C(v). The connected
slack-list greedy lemma forces equality everywhere. Thus boundary colors at
every vertex are distinct. At every contact they avoid both 2 and 3, so
contacts have no b4 attachment. The difference is exactly

```
1_[c∈M_2(v)] − 1_[c∈M_3(v)]
  = 1_[v∈P] (1_[c=3] − 1_[c=2]).                 (1)
```

These are full lists on one C, not independent endpoint marginals.

## 2. Unique block differences

The external degree-list characterization says that C is a Gallai tree and
an uncolorable tight assignment has block palettes: each clique block K has
|K|−1 colors, each odd-cycle block has two, and the incident palettes at each
vertex form a disjoint union equal to its list. We use the characterization
in [Dvořák, Lemma 7 and Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf),
as in R10. It is an external theorem, not part of the Python certificate.

Write these palettes as S_K^2 and S_K^3. A useful elementary fact is that the
vertex-versus-block incidence matrix of a finite connected block graph has
linearly independent columns. Indeed a leaf block has a private vertex, so
its column coefficient is determined there; subtract that coefficient from
the cut-vertex equation and remove the leaf block. Induction ends at a single
block. This applies to real coefficients, hence to differences of indicators.

Equation (1) and column independence imply, block by block:

- Membership of 0 and 1 is identical in the two palettes.
- The changes in membership of 2 and 3 are opposite.
- Consequently a palette either stays fixed or exchanges exactly 2 and 3.

Call the latter blocks **active**. At a vertex, disjointness allows at most
one incident active block of each sign. Equation (1) therefore gives:

- Each contact belongs to exactly one active block, containing 3 in S_K^2.
- Each noncontact belongs to zero or two active blocks; in the latter case
  their signs are opposite.

Form the incidence forest whose nodes are active blocks and their vertices,
with an edge for each incidence. An active block-node has degree |V(K)|≥2.
A vertex-node has degree two, except that the three contacts have degree one.
Every nonempty finite tree has at least two leaves. There are exactly three
leaves in the whole forest, so it is one tree. The tree degree identity

```
number of leaves = 2 + Σ_(nodes of degree≥3) (degree−2)
```

now forces exactly one block-node of degree three and all other block-nodes
of degree two. Therefore the active blocks are **one triangle and three
bridge arms**, whose endpoints are precisely the original three contacts.
Arms of length zero are allowed; then a triangle vertex itself is a contact.
There are no other contacts, and no two arms share vertices away from the
triangle. Inactive blocks and their actual attachments have not disappeared.

Let ℓ_i count bridges on arm i. Signs alternate along an arm. All terminal
signs are the same, so all three ℓ_i have the same parity. If they are even,
the triangle's S_K^2 contains 3; if odd it contains 2. Its other color is a
single h∈{0,1}. This is an arbitrary-length derivation, not a bound inferred
from subdivision samples.

## 3. Every triangle vertex has an actual boundary tether

Let v0,v1,v2 be the active triangle vertices. If ℓ_i>0, v_i has its two
triangle edges and the first arm edge. If ℓ_i=0, it has its two triangle
edges and its original edge to z. In either case complete degree four leaves
**exactly one further edge** at v_i.

That edge is either an actual boundary spoke, or a bridge v_iw_i into a
component W_i of C outside the active triangle and arms. It cannot be a
second edge to z: the three contacts have already been identified. It cannot
rejoin the active structure, because the block incidence graph is a tree.
It is a bridge since any other block at v_i would require at least two
additional incident edges. The different W_i are disjoint and have no
contacts. Their attachments are those in G, not newly chosen representatives.

**Claim. W_i has a boundary neighbor.** Suppose it has none. In C−W_i the
lists M_2 are unchanged, but v_i gains one unit of slack. This graph is
connected, so the slack-list greedy lemma colors it. Inside W_i there are
no boundary or z constraints. The endpoint w_i has degree three in W_i and
all its other vertices have degree four; the same greedy lemma with lists U
gives a proper four-coloring of W_i. Permute its colors so that w_i avoids
the already assigned color of v_i. This extends the coloring to C, contrary
to the rejection of z=2. Hence W_i really touches B.

Choose a path through W_i from w_i to an actual boundary attachment. Together
with v_iw_i this gives a tether from v_i to B, internally disjoint from the
active structure. A direct boundary spoke is the length-one tether case.
All three tethers have disjoint interiors; their boundary endpoints may
coincide. No claim about independent cross-row colorings is involved here.

## 4. Explicit K5 minor in the original graph

The active triangle, its three arms, and all three original edges zP form a
subdivision of K4 with branch vertices z,v0,v1,v2. Define five branch sets:

1. Z={z}.
2. V_i consists of v_i and every vertex on its arm, for i=0,1,2.
3. O consists of the whole actual boundary B and all internal vertices of
   the three selected tethers.

These sets are nonempty, connected, and pairwise disjoint. For a zero arm,
V_i={v_i}; the edge to z is still the original contact edge. The three
triangle edges join every pair of V_i; the three original zP edges join Z
to every V_i. Each tether joins its V_i to O. Finally zb0 (also zb1) joins
Z to O. Thus every pair of branch sets has an actual edge between it: K5 is
a minor of G, contradicting planarity.

This is an explicit source-fixed minor. It uses B as one connected branch
set only for the final planarity contradiction; it is **not** a replacement
preserving boundary coloring relations or a two-contact classification.
The argument does not need to change the given six-cycle embedding or to
infer a new rotation from abstract palettes.

## 5. Second rows, scope, and remaining cases

All four possible second three-color patterns can be named in the same
frame with p(b0)=0, p(b1)=1:
01021, 01201, 01202, 01212. Their rejection would require {2,3}⊆F_C(p).
Tightness then requires every contact attachment T to be injective in both
q and p, with q(T),p(T)⊆{0,1}. The checker records these actual named subsets.
Moreover the p=2 versus p=3 list difference is again exactly (1). Column
independence forces exactly the **same signed active blocks** as in q.
So the second row cannot select a different triangle, different arms, or
different contacts. Nevertheless the q-row K5 minor already closes the case;
no assertion about independently realizable forbidden-color rows is needed.

The proof also works for any two differently q-colored spokes: rename their
two colors 0,1 and the complementary colors 2,3. This is one global color
permutation, without permuting boundary positions. Minimality guarantees the
spoke colors differ. Therefore **all (3) two-spoke cases are excluded**.
In particular all five adjacent configurations remaining after the
[unattached-boundary separation](c5_unattached_boundary.md) are now excluded.
The earlier nonadjacent result was conditional single-missing separation,
not an existence claim; this stronger nonexistence result is compatible with it.

The two-spoke necessary table originally retained 24 cases. Its six (3)
cases are now impossible, leaving **18 (2,1) configurations unresolved**.
The old table and witnesses are unchanged. General single-sided exits,
common pivotal edges, t≤1, and K∞=K≤5 remain open.

## 6. Certificate and trust boundary

[Checker](../scripts/c5_two_spoke_three_contacts.py) and
[artifact](../artifacts/c5_two_spoke_three_contacts/observations.json):

- 63 local palette-incidence states verify the active degrees at contacts
  and noncontacts, retaining both palettes in a common color frame.
- 512 arm-parity controls verify the alternating-sign formula.
- 80 K5 subdivision certificates cover all eight zero-arm patterns and
  direct/subdivided tethers, with named contacts, boundary edges, connected
  branch sets, and an edge witness for every branch-set pair.
- Four second-row attachment tables retain actual boundary labels.

The minor samples are subgraphs with omitted unused edges, not new
candidate degree-four cores. General extraction, arbitrary lengths, and
boundary-tether existence are proved above, not inferred from these samples.
There is no full graph enumeration, new planarity oracle, two-contact
classification call, or modification of the 603 profiles/fixed point.

Trust: paper proof + the external degree-list characterization + Python
finite checks. No new Lean theorem; `lake build` does not formalize this
argument. Actual replay results are in the
[research record](history/2026-09-24-three-contact-exclusion.md).

```bash
python3 scripts/c5_two_spoke_three_contacts.py --check
python3 scripts/c5_degree5_two_spoke_sectors.py --check
python3 scripts/c5_unattached_boundary.py --check
python3 scripts/check_docs.py
git diff --check
```
