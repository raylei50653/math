# High-contact long pieces: a leaf-contact tree escape and its exact boundary

Scope is the complete original N2-55 source contract frozen by the parent
`BASE.json`, at HEAD `5f0979793c19e452dbb5fc7e9fe7e43cb8a991cc`.
Only this `high-contact/` directory is written. There is no source census,
replacement graph, shared-document edit, commit, push, or Graphify. The paper
results below are candidates for the parent's independent adoption; local
controls do not provide a complete target source realization.

Write `I={0,1,3}`, `q=(01212,01202,01021)`, and `D=3`. For the same original
mixed piece C write `M_C={i in I : (D,D) not in A_C(q_i)}`. Every accepted
cell means a coloring of all original C vertices, with all internal edges,
actual boundary attachments, ordered root contacts and shared coordinates
preserved. Ownership is never discarded when constructing a lift.

## 1. An arbitrary-size escape beyond the contact-three bound

**Lemma H-TREE-LEAVES.** Suppose an original mixed C is a tree, has no
shared root contact, and every vertex adjacent to a root is a leaf of C.
Then `M_C` is a proper subset of I. There is no bound on the number of
contacts or the length of an original chain in this assertion.

The local hypotheses used are: C is a finite tree, every original vertex
has complete degree four, each vertex has at most two adjacent boundary
neighbors, and distinct H-degree-two vertices have distinct actual boundary
edges. These follow from the frozen source reports. Long support is not
needed for this narrower shape statement.

*Proof.* Let X be the original contact set. No shared contact means each
member of X has exactly one root edge. Assume that all three diagonal
assignments are impossible. The original degree lists are

`L_i(v)=[4] \ (q_i(N_B(v)) union {D : v in X})`.

They have size `d_C(v)`. The degree-list characterization gives a singleton
palette on each original bridge; incident palettes at a vertex are disjoint
and their union is its list. Since D occurs in `L_i(v)` exactly when v is
ordinary (v not in X), bridges with palette D form a matching covering
every ordinary vertex and meeting no contact. This matching is the same
in all three rows: the frozen L-D-PATTERN proof applies, or uniqueness
follows by taking an endpoint of the symmetric difference of two matchings.

Every leaf is a contact. Indeed, an ordinary C leaf would need three
boundary attachments, contrary to the boundary cap. Our hypothesis says
conversely that all contacts are leaves. A contact leaf p has complete
degree four, so it attaches to an actual boundary edge e; its incident
bridge palette is exactly the literal signature T(e).

If C is a single bridge, both vertices are contact leaves. Equality of
their palettes in all three rows forces the two actual boundary edges to
be equal (the five T signatures are distinct). Both vertices have
H-degree two, contradicting attachment injection.

Otherwise ordinary vertices exist. Contract each D bridge only in an
auxiliary counting tree, retaining contact leaves. Call a contracted pair
of ordinary endpoints a unit. The subgraph induced by units is a finite
tree (possibly one vertex): the path between any two ordinary units cannot
pass through a contact leaf. Choose a terminal unit of this tree. At most
one original non-D bridge from this unit leads to another unit. At one
of its original endpoints y there is therefore no such outgoing bridge.
All its non-D bridges go directly to distinct contact leaves. Let their
number be `ell=d_C(y)-1`; ordinary vertices have `2<=d_C(y)<=4`, so
`ell` is 1, 2 or 3. These three cases exhaust every original chain and
branch, without suppressing one in the source graph.

* `ell=1`: y has two actual adjacent boundary neighbors f. Its list is
  `{D,T_i(f)}`. The contact leaf's palette T(e) must equal T(f) in all
  three rows. Thus e=f, and y and the leaf are distinct H-degree-two
  vertices with the same boundary edge, a contradiction.
* `ell=2`: y has one actual boundary neighbor h. The two distinct leaf
  edge palettes T(e),T(f) are different in each row; the third used color
  is q(h). The literal signature table admits only the unordered pairs
  `{01,23}` and `{01,34}`. Their third-color signatures are `(1,0,0)`
  and `(1,0,1)`, neither an actual q(h), a contradiction.
* `ell=3`: y has no boundary attachment. Its list is all four colors;
  the three leaf palettes must give all of `{0,1,2}` in every row. The
  three actual leaf edges are distinct by attachment injection. No triple
  of original boundary edges has T colors rainbow in all three rows.
  For a direct check, q0 forces 01,40 and one of 12,23,34; q1 then forces
  the third edge to be 12, but in q3 all of 01,12,40 have T color 2.

Every case contradicts rejection in all three rows. A coloring in an
escape row is a full list coloring on the original tree and hence the
required full original lift. The auxiliary contractions prove a counting
claim only; they do not replace C or transfer its relation. ∎

**Source corollary.** In `(ell,u)=(1,0)`, the original source is excluded
whenever its long mixed piece satisfies H-TREE-LEAVES, including its
`k_C>=4` subdomain. In its actual escape row, the other short mixed piece
has a complete `(D,D)` lift by frozen N-diagonal. Literal D avoids all
root spokes, rs is absent, and the two original pieces are disjoint. Their
full lifts therefore join to a coloring of the original G in a rejected
row, with any free isolated four-color factors retained.

For `(1,1)` this lemma provides only a proper long rejection mask: its
escape row must still coincide with a complete U lift. For `(2,0)` two
independent tree escapes also need a same-row joint. If the other long
has a shared contact, its mask is empty, so the escape does give a same-row
source exclusion. No general mask synchronization is asserted here.

## 2. The broader k=4 escape is false under the existing local premises

The named control `four_contact_long_path` has ordered roots r=9, s=10
and original vertices `(5,6,7,8)` on the path `5-6-7-8`. Its exact data are

| Vertex | Boundary attachments | Original root contact |
| --- | --- | --- |
| 5 | 0,1 | r |
| 6 | 0 | r |
| 7 | 2 | s |
| 8 | 1,2 | s |

Every vertex has complete degree four, there are four original root
incidences and no shared contact, and actual support is the consecutive
triple `{0,1,2}`. Its two H-degree-two vertices have distinct boundary
edges 01 and 12. It is a tree whose nonleaf vertices 6 and 7 are contacts,
precisely the hypothesis excluded from H-TREE-LEAVES.

In each selected row, the two root pins D give singleton leaf palettes
`T(01)` and `T(12)`. At 6 and 7 the bridge palettes forced by the actual
attachments 0 and 2 are compatible across the intervening bridge. Thus
all three rows reject `(D,D)`. `observations.json` retains every full lift
in all ten literal frame rows and all 16 ambient ordered pin cells,
including empties; the rejection mask is exactly I.

This is a counterexample to a **local** extension of contact-three escape
to contact four, including tree, long support, leaf contact, boundary cap,
and boundary-edge injection premises. It is not a complete Sigma933/941
N2 source: root degrees five, full B-touch, edge criticality, accepted T4
and full source rotation have not been realized. Its local full fibres do
not themselves exclude or realize a source. In particular the paper
corollary in section 1 uses the contact-at-cutpoint restriction essentially.

## 3. Independent audit of the common two-spoke-edge minor

**Lemma H-SAME-EDGE.** In the complete original source contract, if there
is a long mixed piece or u=0, the two roots cannot both be adjacent to
both ends a,b of the same boundary edge.

More locally it suffices that C and Q are distinct original mixed pieces,
that some vertex v of C has an actual attachment h outside `{a,b}`, and
that v lies on an r-s path whose interior is in C. Let T be that path,
and let W be an original r-s path with interior in Q. The five branch sets
are

`R={r} union (W-{r,s}), S={s}, A={a}, B={b},`

`F=(T-{r,s}) union (original B-{a,b}).`

F is connected using the original attachment vh; the residual boundary
path is connected because ab is a boundary edge. R is connected along W.
The five sets are disjoint. R-S uses the final W edge; R-F and S-F use
the two ends of T; each root is adjacent to a and b by its original
spokes; A-B is the original boundary edge; F-A and F-B are the two ends
of the original residual boundary path. All ten adjacencies exist, giving
a K5 minor of the original G. No relation or Sigma is assigned to the
minor; it only contradicts planarity.

For the target-source implication, frozen size-bound Lemma 1 places every
original mixed vertex in the same two-connected central block K0 as r,s.
The two-fan property in a two-connected graph gives disjoint v-r and v-s
paths except at v. Stop each path at its first root: before that first root
it remains in the original C, because C is a component of H-{r,s}.
Their union is the required original T through v. This property can also
be read as the two-terminal Menger alternative: a failure would exhibit
one vertex separating v from both roots and hence a cutvertex of K0.

If both roots have the same two-spoke edge, the boundary cap fixes all
their boundary attachments to `{a,b}`. A long mixed C has support of
size at least three and gives an actual h outside `{a,b}` directly.
More generally in u=0, full B-touch
forces such an attachment in one of C,Q, so H-SAME-EDGE follows even
without a long assumption.

The parent's `(1,0), k_L=4, k_S=2, t=4` application has both roots with
two spokes. If their actual two-spoke edges coincide, this lemma excludes
that entire arbitrary-size subdomain. Different spoke edges remain to be
analyzed by the parent. No claim about those different edges is made here.

## 4. Replay and evidence boundary

`checker.py` verifies all frozen input hashes against parent BASE, checks
the five literal signatures, all 25 edge pairs, all ten edge triples, and
recomputes complete fibres for two named original local controls. It also
checks every pairwise adjacency and every connected branch set of a
named H-SAME-EDGE K5 certificate. The finite controls calibrate the paper
arguments; arbitrary size in H-TREE-LEAVES is carried by its terminal-unit
proof, and source application of H-SAME-EDGE uses the frozen central-block
theorem. Full target source status is `not triggered`.

The retained artifact has 228,606 bytes and SHA256
`f91d8a12bdf4b4c07c2ff64b6c345f292942668ad00af224ab4b71cdaa7326b7`.
Its two controls retain 20 literal rows and 320 ambient pin cells, including
40 empty cells. The normal and seed-17 checks give identical bytes and hash.

The positive `four_leaf_contact_tree` control has four leaf contacts and
no contact at a C cutpoint. Its diagonal masks are empty. The negative
`four_contact_long_path` control has mask I. Neither claims a full target
source or a checked disk rotation. There is no new Lean theorem.

Normal replay, hash-seed-17 replay and a deliberately corrupted retained
artifact are recorded in `verification.json`. The corrupted artifact
must fail with `artifact mismatch`. A first exploratory planarity probe
failed because bare Python had no networkx; this is retained separately
in `exploration_probe_failures.json`. Successful exploratory named probes
are retained in `exploration_probes.json`; their planarity-oracle output
is not a paper premise or a claim of a target source. The generation
receipt records exclusive artifact creation. Replay needs only standard
Python and does not call a planarity oracle.

General no-shared-contact long pieces with a root contact at a C cutpoint,
pieces containing odd-cycle blocks, off-diagonal full joints, and same-row
synchronization remain residual obligations. The complete original N2,
original55 and three-point-arc proposition remain OPEN.
