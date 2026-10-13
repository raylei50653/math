# N2-BRIDGE: local witnesses, five-row slack, and the LL interface

BASE: `243a125a80e4d8de40957f59d8da0bdbc974cf69`.
This paper separates new implications from inherited inputs. All graphs,
boundary positions, contacts, owners, attachments, rotations and fibres are
the original ones. No contraction below is asserted to preserve Sigma.

## 1. Literal rows and the smaller witness obligation

Write `q0=01212, q1=01202, q2=01201, q3=01021, q4=01012`.
The selected set is `I={0,1,3}` and the unused color is `D=3`.
Let G be a finite simple induced-C5 disk with ordered boundary B, connected
effective H touching all B, two nonadjacent full-degree-five roots r,s, and
all other effective interior vertices of full degree four. Assume there
are exactly two original mixed components of H minus the roots; other
components are unary. Free isolated coordinates retain their independent
four-color factors in every comparison.

For a component C, let E_C be all original edges incident with C. The
following local witness condition is substantially more precise than
requiring a fixed complete Sigma:

**CW(J).** For every original C and every i in J, there is one e in E_C
such that G-e has a complete coloring extending the literal q_i.

Whenever G rejects q_i, CW for that C,i is equivalent to G-C accepting
q_i. Moreover it implies every edge in E_C releases q_i. Indeed, full
degree four gives residual lists at least d_C. Deleting an external edge
provides one strict slack point if the original assignment was tight;
deleting an internal edge provides an endpoint with strict slack in each
resulting component. Greedy coloring toward that endpoint extends every
fixed complete outside coloring. Thus, on the full outside vertex set W,

`projection_W Col_q(G-e) = Col_q(G-C)` for every e in E_C.

The equality concerns full outside assignments, not root marginals. It
does not identify the different internal fibres. Root-spokes are not in
E_C and are not covered by this assertion.

If G is minimal for **each** q_i in I, CW(I) follows immediately. The
ordinary triple-critical premise only asserts that each edge releases
**some** member of I, and does not establish CW(I).

## 2. Three-row witness bridge

**Lemma BR-CW3.** Suppose G rejects all rows in I and satisfies CW(I).
Then each nonroot interior vertex has at most two boundary neighbors,
which are adjacent when there are two. Each original C is a Gallai tree;
every leaf C-block has a private root-contact; and each C has at least
two root incidences. Every odd-cycle C-block has at most one ordinary
private vertex (a vertex that is neither a C-cutvertex nor a root-contact).

*Proof.* A nonadjacent boundary pair repeats a color in at least one row
of I. Such a pair at v in C provides strict list slack for every choice
of root pins in that row. CW supplies an actual complete coloring of
G-C; filling C contradicts rejection. Three boundary neighbors contain
a nonadjacent pair, proving the attachment assertion.

For each C and each row, fix one complete coloring of G-C, with its actual
root pins. The residual degree assignment on C is uncolorable, otherwise
it extends this same coloring. The degree-list theorem gives tight lists
and blockwise disjoint palettes. This uses Lemma 7 and Theorem 10 of
[Dvorak's 2018 notes](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf),
read in this audit; it is an external paper input, not a Lean result.
Planarity leaves bridge, odd-cycle, and K4 blocks.

An ordinary private vertex of an odd-cycle block has two original
boundary neighbors. Its two-color list is the block palette. Hence two
ordinary private vertices of the same block have equal boundary color
pairs in every witnessed row. The five boundary-edge signatures in I
are distinct, so their original boundary edges are equal. In a K4 block,
ordinary private vertices have one boundary neighbor; the five vertex
signatures are distinct, so these neighbors are equal as well. The
outside pins may differ between rows: ordinary vertices see neither root.

The following original minors then prove the leaf assertion. In a leaf
bridge, a root-free private endpoint would need three boundary neighbors.
In a leaf odd cycle of length at least five, three ordinary private points
attach to the same boundary edge ab; contract the three intervening cycle
arcs to a triangle and retain a,b, obtaining K5. For a leaf triangle xuv,
the root-free private points u,v attach to the same ab. The set
`X=(H-{u,v}) union (B-{a,b})` is connected: H minus those private points
is connected, and full B-touch gives an attachment to the remaining
boundary path. The bags `{u},{v},{a},{b},X` form K5. For a leaf K4 with
private points u,v,w, all attach to the same a; the connected bag
`X=(H-{u,v,w}) union (B-{a})`, with the four singleton bags u,v,w,a,
again gives K5. These arguments also cover a root-free leaf H-block.

For the ordinary-private-point bound on an arbitrary odd cycle J, suppose
u,v both attach to ab. A path from B minus {a,b} through H, stopped at its
first meeting x with J, meets J away from u,v because those two vertices
have no other H neighbors. Of the two u-v arcs, choose the one whose
interior contains x. Its interior, the tether and B minus {a,b} form a
connected hub; contract the interior of the other arc into u. Together
with v,a,b these are five disjoint connected bags with all ten original
cross adjacencies. This is K5.

Finally, a multiblock component with one root incidence cannot supply
private contacts to its at least two leaf blocks. A singleton cannot have
degree four with one root neighbor and at most two boundary neighbors. A
single bridge needs contacts at both endpoints. A single odd cycle with
one contact has at least two ordinary private points, already excluded.
A single K4 with one contact has three ordinary points attached to one a;
the remaining H together with B-a is the fifth K5 bag. Thus every C has
at least two root incidences. All minors use actual original edges. ∎

**Root-spoke distinction.** BR-CW3 does not by itself restrict the roots'
boundary attachments. If G is minimal for each selected row, it does:
a duplicated boundary color makes either of the two spokes redundant for
that row, contradicting its own deletion witness. The five nonadjacent
pairs are all detected by I. More economically, one may supply the direct
condition that each root has at most two adjacent boundary neighbors.
No statement about acceptance of q2 or q4 is needed for either route.

## 3. New five-row bridge before per-row criticality

The missing complete mask is 932, which rejects **all five** singleton
rows and accepts T4. The stronger rejection premise provides a different
way to produce structural witnesses; it must not be confused with adding
an acceptance premise.

**Lemma BR-5SLACK.** Retain the original graph hypotheses of Section 1.
Suppose G rejects all five q_i and every original G-C rejects at most
one singleton row. Then every conclusion of BR-CW3 holds, even though
CW(I) has not yet been established.

*Proof.* For each C, choose the at least four rows accepted by G-C.
Call this set J_C. It belongs to that exact C; distinct pieces need not
have the same exceptional row. A nonadjacent boundary pair repeats in
exactly the following two rows:

| Pair | Repeated rows |
| --- | --- |
| 02 | 3,4 |
| 03 | 1,2 |
| 13 | 0,4 |
| 14 | 2,3 |
| 24 | 0,1 |

At least one lies in J_C. Boundary repetition therefore gives slack and
contradicts the corresponding complete outside witness, exactly as above.
This proves the nonroot attachment restriction without assuming common
outside witnesses for all five rows.

For clarity, the full boundary-edge color-pair signatures are:

| Original edge | q0 | q1 | q2 | q3 | q4 |
| --- | --- | --- | --- | --- | --- |
| 01 | 01 | 01 | 01 | 01 | 01 |
| 12 | 12 | 12 | 12 | 01 | 01 |
| 23 | 12 | 02 | 02 | 02 | 01 |
| 34 | 12 | 02 | 01 | 12 | 12 |
| 40 | 02 | 02 | 01 | 01 | 02 |

After deleting any one column these five signatures remain pairwise
distinct. The same is true for the five boundary-vertex signatures,
obtained directly from the literal q_i. Thus the actual attachment
identification in BR-CW3 works on J_C. Apply exactly its original leaf
minors and incidence argument. No coloring witnesses from different rows
are combined. ∎

This result is useful before N45: **unit unary components are eliminated
without using the historical exact-mask N45-U exclusion.** Its precise
extra hypothesis is `|Q(G-C)|<=1`, separately for each original C.
The general proper-subgraph theorem P supplies it once its Z-premise
has actually been established; P is not assumed merely from criticality.

**Corollary BR-5P (including the roots).** If every proper B-preserving
subgraph of this five-rejection source rejects at most one singleton
row, then **every** interior vertex, including r,s, has at most two
adjacent boundary neighbors. Suppose v sees a nonadjacent pair a,b.
The table gives two distinct rows where a,b have equal color. In either
row, a coloring of G-va would also satisfy va through the retained vb,
so G-va still rejects both rows. This contradicts P. Three boundary
neighbors contain a nonadjacent pair. This argument uses no degree-list
theorem, per-row minimality or SD-A.

In the actual generalized N2 domain, [U4-3R](U4_TRANSFER.md) Section 6
supplies P by the following separately audited chain: the mask-free original U4 argument
excludes two-root44 cores; the root-deletion lemma and at least two
mixed incidences at each root exclude root-omitting cores; hence no
zero-excess rejected-row core exists, so Z is empty. The general
proper-subgraph theorem P from `c5_excess_two_arc_pair_critical.md`
Section 3 now applies. Its proof uses E2 at excess zero/one and
excess saturation, and does not impose q2/q4 acceptance. U4's finite
terminal coverage remains an explicit trust dependency of this chain.

**Lemma BR-RETAIN.** In addition to BR-5SLACK, assume that no rejected-row
minimal core omits a root, and no rejected-row minimal core has both
root degrees four. Then G-C accepts all ten rows for every original C,
and every edge in E_C releases every rejected row.

*Proof.* If C is mixed, each root loses at least one incidence. A minimal
core K in G-C must have interior degree at least four. If both roots are
retained, their degrees are exactly four, contrary to the second input;
omitting a root contradicts the first. If C is unary, BR-5SLACK gives at
least two root incidences. Its owner has degree at most three in G-C,
cannot occur in K, and again contradicts the first input. Thus G-C
rejects no singleton. T4 remains accepted by subgraph monotonicity.
The full outside-projection identity in Section 1 completes the claim. ∎

Neither of the two core exclusions in BR-RETAIN is proved by this lemma.
They must be provided in the actual 932 domain, not imported from the
historical 933/941 statement by name. This exposes the precise dependency
for the parent audit's separate original-core argument.

## 4. Structural transfer with arbitrary component lengths

Under either BR-CW3 or BR-5SLACK, the original block arguments give the
following consequences without reading any unassigned row status.

1. H consists of a central block K0 containing both roots and at most one
   additional leaf block at each root. The two mixed pieces give two
   internally disjoint r-s paths, placing both roots in K0. A root-free
   leaf H-block is impossible by the minors above. The block-cut tree
   therefore places every other block directly at a root. A leaf bridge
   would have a nonroot endpoint with three boundary neighbors, so every
   block is biconnected. Two leaf blocks at one root would require at
   least six incidences, contradicting degree five. Unary components are
   exactly these leaf blocks with their owner removed; hence u<=2.
2. Distinct **nonroot** vertices of H-degree two have distinct original
   boundary-edge attachments. Within one H-block use the common-cycle
   tether K5 from BR-CW3. In different blocks, removing both vertices
   leaves H connected; for a repeated edge ab the two K3,3 sides are
   `({a},{b},H-{u,v})` and `({u},{v},B-{a,b})`. Full B-touch supplies the
   last cross adjacency. This assertion intentionally excludes roots
   until their spoke bound has been established.
3. Every C has only bridge and odd-cycle blocks. A K4 block has exactly
   one external direction at each of its four vertices. Each direction
   either meets G-C directly or follows an original branch to a private
   root-contact in a leaf block. These four branches are disjoint off
   the K4 by maximal-block structure. G-C is connected: the other mixed
   piece joins the roots and has nonempty boundary support. Joining it
   to the four branches gives a fifth K5 bag. Here nonempty mixed support
   is the original N2 no-empty-support input, which is valid in the
   three-row E3 domain; it is explicitly retained, not inferred from a
   projected relation.

These are the prerequisites used by low-incidence diagonal escape and
the local unary theorems. Their proof does not need the 35-vertex bound,
a source enumeration, or global per-row root-spoke criticality.

## 5. Root-spokes when there is no unary

**Lemma BR-SPOKE0.** Assume G rejects q0,q1,q3, every original G-C accepts
these rows, the BR-CW3 structure holds, there is no unary, and each mixed
piece has nonempty support. Then every original root-spoke deletion
accepts all rows already accepted by G and every row rejected by G.
In particular every root has at most two adjacent boundary neighbors.

*Proof.* H is biconnected by Section 4. Suppose X=G-rb_j rejects a row
beta rejected by G. Full degrees in X are r=4,s=5, all others four, and
its inner graph is exactly H. The independently checked SD-A input
applies to this induced-C5 disk: its unique degree-five vertex has
H-degree two. Hence s has three original spokes. Some two have equal
color in one selected q_i, since I detects every nonadjacent pair.
Deleting one of those spokes gives Y that still rejects q_i, without
requiring X or Y to be minimal. Its same inner graph H is biconnected;
SD-A with roots exchanged gives d_H(r)=2. Both roots have three spokes.

Because H-r and H-s are connected and touch every nonspoke boundary
vertex, each three-spoke star has gaps 1,1,3. After one common D5 move
its first set is 012, and the other is 234 or 340. The original mixed
supports lie respectively in `{0,2,4}` or `{0,2,3}`, neither containing a
consecutive three-point arc. The one-sided shield theorem identifies
each long support with its shield vertices, so both mixed pieces must
be short. In a selected row, set the two original roots to D. The local
N-diagonal theorem gives both short-piece complete lifts at these same
pins. They meet only through their actual roots and B; every original
edge is satisfied. This contradicts rejection and eliminates X.

The argument used a common D5 move only for topology; the final coloring
returns to the original selected row and original coordinates. By
monotonicity no accepted row can be lost in G-e. If a root has a
nonadjacent boundary pair, one selected row repeats its color and a
spoke deletion cannot release that row, a contradiction. ∎

The external SD-A trust chain is retained exactly as stated in
`docs/c5_degree5_interfaces.md` Section 7. No degree-at-least-five result
for a different minimal-near-triangulation model is used.

## 6. The exact LL-CUT+diag transfer statement

**Theorem BR-LL.** There is no original graph of Section 1 with no unary,
two long mixed pieces, all three selected rows rejected, CW(I), and
at most two adjacent boundary neighbors at each root.

*Proof by complete interface discharge.* BR-CW3 and Section 4 supply the
nonroot spoke restriction, original Gallai palettes, private leaf
contacts, ordinary-private-point bound, bridge/odd-cycle blocks, H
biconnectivity and nonroot H-degree-two attachment injection. The roots
have H-degree at least three by the assumed spoke bound, so the last
injection covers every H-degree-two point. Two long pieces are one-sided
and have their actual full shield supports; full B-touch and disk
topology supply shield disjointness. These are exactly the structural
inputs listed in the frozen LL-CUT `paper/TOPOLOGY.md` Section 1.

The B-C2 capacity bound is a theorem for complete original fibres under
the stated degree-four and root-incidence data. With no unary and the
root spoke bound, properness gives `|E_v|=4-t_v=k_P^v+k_Q^v-1` in each
selected row. The common matrices and their cuts therefore have the
same bounds without any root-spoke deletion witness. Their local slack
cells use actual attachments and actual shared contacts. The adopted
t=0,1 arguments and the remaining (1,1),(2,1),(2,0) arguments use only
these bounds, the supplied structural inputs, the literal selected rows,
and the original K5/K3,3 bags. Low-incidence escape uses the supplied
leaf/private-point/injection facts. No line asks whether q2 or q4 is
accepted. The proof consequently yields a nonempty same-row full joint,
contradicting the selected rejection. ∎

This is a new weakening of the **source theorem**; it does not prove the
basic LL-CUT certificate mechanism. It removes the complete-mask input
by proving its actual structural consumers from CW(I), while retaining
an explicit root-spoke obligation. If G is minimal for each selected
row, both obligations hold, so its entire double-long subdomain is
excluded without first deriving all-ten-row deletion acceptance.

If the parent audit establishes BR-RETAIN in the 932 domain and excludes
its unary sources, BR-5P already supplies the root obligation and BR-LL
applies there. BR-SPOKE0 is a separate optional three-row route; **the
932 route does not need SD-A**. The separate core and unary proofs
determine whether the full 932 branch closes.

## 7. Unary capacity without the old root-spoke witnesses

**Lemma BR-U3CAP.** Suppose the original source has exactly one unary U,
owned by r, with k_U=3; two mixed pieces; full degrees 5,5,4; all selected
rows rejected; and at most three spokes at s. Then every selected row
satisfies `|F_U(q_i)|>=2`.

*Proof.* Degree five and two positive mixed incidences force r to have
no spokes and `k_P^r=k_Q^r=1`. The other root has no unary. At most three
spokes leave a legal color b at s. Let `G_C(b)` be the set of r-colors
whose **complete** C-fibre is empty at (a,b). B-C2 gives
`|G_P(b)|<=1` and `|G_Q(b)|<=1`. Every color outside F_U is a legal unary
pin at r; rejection of the original G forces it to lie in their union.
Thus `4-|F_U|<=2`, which is the claim. ∎

This proof needs neither spoke-factor disjointness nor a q_i-critical
witness at every spoke. If the structural hypotheses of the adopted
unary three-row D-escape and the used-color bound have been checked,
they give one same row with D outside F_U and `|F_U|<=1`, a contradiction.
This is the precise replacement needed when the old common-capacity
formula cited full root-spoke criticality.

## 8. One-long transfer and independent parent synthesis review

**Theorem BR-OL.** Replace the two-long hypothesis in BR-LL by one long
and one short with nonempty actual support. Retain all other hypotheses.
There is again no such original source.

The frozen one-long proof's exact consumers are as follows. CW provides
the full exterior witness for the three-hub assertion that a singleton
short support is incompatible with any root-spoke. BR-CW3 and Section 4
supply every leaf, cactus, private-point and attachment-injection fact.
The local N-diagonal supplies all same-pin short lifts; the local
low-incidence escape handles a shared long contact or at most three
long incidences. For the remaining long, permanent three-row diagonal
failure gives the original leaf-cycle K5. Its surviving leaf bridges
use actual attachment injection and the original spoke set T; the
literal closure calculation leaves exactly the two four-spoke
configurations. In each, the original degree-five equation gives the
strict slack at the unpinned root in the connected short-plus-root
graph. That full exterior coloring is kept while filling the long.
No step uses deletion of a root-spoke, the minimality of an individual
selected-row core, or the acceptance of q2/q4. Thus the entire original
OL proof body applies, including arbitrary long length and off-path
branches, and returns one complete same-row G coloring. ∎

The parent [CLOSURE](CLOSURE.md) now supplies the separate U4 and unary
arguments and uses BR-5P directly. This paper's optional BR-SPOKE0 is
not on that proof's dependency path. Its exact theorem remains the
generalized N2 source of original E4, not N1 or adjacent-root sources.
