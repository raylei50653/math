---
docgraph:
  id: c5.two-spoke-nonadjacent
  family:
    - c5
    - c5.two-spoke
  requires:
    - c5.degree5-two-spoke-sectors
    - c5.two-spoke-reflection
  related:
    - c5.two-spoke-split-support
    - c5.single-sided-exit
---
# Nonadjacent two-spoke (2,1): separation for the two exit queries

2026-09-27. **All four representatives with S={b1,b4} extend both
pA=01021 and pB=01212.** The four S={b2,b4} entries follow solely by the
existing reflection transport. Together with the previous exclusions and
adjacent split-support theorem, this completes the unique-degree-five,
two-spoke branch for [single-sided exit](c5_single_sided_exit.md).
Priority and remaining gaps: [HANDOFF](HANDOFF.md).

This is an arbitrary-size paper theorem using the existing degree-four
structure and transfer theorems, with new finite certificates. It is not
an enumeration of bounded-size sources. We do **not** classify all boundary
rows of every T4-accepting source, or claim all four configurations exist.

## 1. Hypotheses, representatives, and unchanged source relations

M is a finite simple induced-C5 disk minimal q-obstruction, q=01012,
accepting all T4 rows. Its effective interior H is connected. The unique
complete degree-five vertex z has spokes S={b1,b4}; all other interior
vertices have complete degree four. The two components of H−z are C2
with two distinct ordered contacts (s,t), and C1 with contact r.
By the [necessary region theorem](c5_degree5_two_spoke_sectors.md), they
occupy opposite sides of

```
Gamma5=(z,b1,b2,b3,b4),       Gamma4=(z,b4,b0,b1).
```

Call these components L (pentagon) and D (quadrilateral), independently
of their contact counts. The four necessary cases are:

| Case | C2 side | F_C2(q) | F_C1(q) | New conclusion |
| --- | --- | --- | --- | --- |
| I | pentagon | {0} | {3} | pA and pB extend |
| II | pentagon | {3} | {0} | pA and pB extend |
| III | quadrilateral | {0} | {3} | pA and pB extend |
| IV | quadrilateral | {3} | {0} | pA and pB extend |

Throughout, R_C(b) is the relation of **complete colorings of that same
component**, with its actual attachments and its original ordered contacts.
The [R10](c5_degree5_interfaces.md) join is exactly

```
J_M(b) = {(a,t2,t1): a not in {b1,b4},
          t2 in R_C2(b), t1 in R_C1(b), all tuple coordinates differ from a},
Z_M(b) = (U\{b1,b4}) \ (F_C2(b) union F_C1(b)).
```

No product of endpoint marginals replaces R_C2. For any row, R_C is
nonempty: before fixing z, an original contact has list slack. Taking
one complete k-tuple shows |F_C(b)|≤k, because every forbidden color must
occur in that tuple. This argument does not assume that all k-tuples occur.

## 2. What the quadrilateral side supplies

We need no general C4 classification and perform no C4-to-C5 padding.
Every actual attachment of D belongs to {b4,b0,b1}. At pB these three
values are exactly their q values. Consequently its **entire** relation,
not just its forbidden projection, is unchanged:

```
R_D(pB)=R_D(q),      F_D(pB)=F_D(q)={a},       a in {0,3}.
```

On the pentagon side, all actual boundary neighbors at pB use only 1 and
2. Swapping 0 and 3 therefore acts bijectively on complete L-colorings
and on all their contact coordinates. It follows that F_L(pB) contains
both 0,3 or neither. If pB were rejected, its available hub colors {0,3}
would be covered by F_L(pB) union {a}. Thus F_L(pB) contains both, and
its contact bound forces

```
L=C2, D=C1,                 F_L(pB)={0,3}.                 (2)
```

Cases III and IV are already separated for pB. Cases I and II are the
only ones needing the completion below. The stabilizer and cardinality
screen is formalized in `two_color_screen`; its graph hypotheses remain
paper arguments.

## 3. The pB completion preserves the actual pentagon component

Assume (2). Delete D, retain **all** of L, its actual attachments, its two
original contacts, z, both z spokes, and the original C5. Call the result K.
It is a disk subgraph of M with connected interior L union {z}. Every
interior degree is now exactly four, including z. It rejects pB by (2).

K is minimal for pB. Deleting an edge incident to L releases all its
forbidden colors by R10; deleting a z spoke releases its color 1 or 2,
neither in F_L(pB). The singleton boundary vertex b0 of pB has no interior
attachment. Moreover K has a cycle: L connects the two distinct contacts
of z. The [unattached-singleton cyclic lemma](c5_two_spoke_split_support.md#2-a-useful-consequence-of-the-existing-degree-four-classification)
therefore applies to **this C5 graph K**, without a T4 assumption on K.
Its actual interior is a triangle or two disjoint triangles joined by a
direct bridge. This is the previously established arbitrary-size theorem,
not an assumption about the original quadrilateral.

Since z has interior degree two, it is a non-bridge vertex of a triangle.
Up to an isomorphism retaining z and transporting both contact coordinates,
the possibilities are exactly

```
z=5, ordered contacts=(6,7).
Triangle:       L={6,7},        E(L)={67}.
Two triangles:  L={6,7,8,9,10}, E(L)={67,68,89,8-10,9-10}.
```

Each vertex receives exactly 4−deg_L(v)−1_[v is a contact] distinct
neighbors from {b1,b2,b3,b4}. There are 36 and 3,456 assignments,
respectively. Enumerating their full two-contact relations at q and pB
gives **no** assignment with both

```
F_L(q) in {{0},{3}},             F_L(pB)={0,3}.
```

Both contact orders are covered: a chosen source ordering is transported
by the isomorphism; reversing it reverses both tuple coordinates. The
finite cover allows nondisk assignments and does not use planarity to
filter them. All 528 pB-rejecting completions additionally carry every
nonboundary edge-deletion coloring. Thus the contradiction is algebraic
after the actual-source structural reduction, and proves pB extends.

## 4. The pA duplicate-spoke reduction

Suppose instead that M rejects pA=01021. Here b1=b4=1. Delete zb4 and
call the result K. A pA-coloring of K would already satisfy zb4, so K
still rejects pA. Its effective interior is the unchanged H, connected,
and **every complete interior degree is four**; z still has interior
degree three. It is an induced-C5 disk subgraph and inherits T4 acceptance.

For completeness, K is a minimal pA-obstruction, not merely a graph
containing some smaller obstruction: its boundary lists have size at
least the interior degrees. Uncolorability and connected slack-greedy
coloring force equality at every vertex, hence distinct boundary colors
at every vertex. Deleting a spoke creates list slack; deleting a
nonbridge interior edge creates degree slack in a connected graph;
deleting a bridge creates slack on both sides. Each nonboundary edge
therefore releases pA. All degrees here are those of K itself.

The existing [degree-four structure](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)
and its dependencies apply at the pA frame:

* If H is a tree, the [tree theorem](c5_tree_cores.md) makes it a path.
  This contradicts deg_H(z)=3.
* If H has one triangle, the [fork](c5_triangle_forks.md) and
  [path-tail](c5_triangle_path_reduction.md) theorems make every attached
  tree a path. Thus z is a triangle vertex with one tail. The endpoint
  reduction yields one of the 18 canonical disk bases, retaining every
  triangle vertex, each tail root, and the boundary.
* If H has two triangles, the [two-triangle theorem](c5_two_triangle_blocks.md)
  says H is exactly those triangles with one direct bridge and no tails.
  Here z is a bridge endpoint. Long cycles, shared cycles, more triangles,
  and K4 blocks have already been excluded by the inherited structural
  theorems; no new size bound is imposed.

The endpoint reduction needs a precise preservation statement, since
ordinary equality of boundary signatures would not suffice after adding
zb4. The path-tail theorem preserves each tail's **bridge query for every
boundary row and every fixed parent color**. Fixing all three triangle
colors makes the different tails independent, so it preserves the entire
set of extendable triangle-color tuples. In particular it preserves the
set of feasible z colors, conditional on every boundary row. The vertex z
and its boundary spoke are retained. Adding the extra condition z≠b4
therefore commutes with this reduction.

The two C2 contacts are the other two triangle vertices and remain
individually named; the C1 contact is the retained first tail vertex.
Original source relations remain the semantic objects in §1. We do not
claim that shortening a tail preserves its full root-color set merely
because its bridge queries agree. The new finite relations belong to
the actual normal graph; lifting a coloring back uses the proven fixed
parent query, not an identification of different sources' root relations.
Intermediate bridges are retained in the proof until that transfer is used.

## 5. The pA finite contradiction, with z retained

Map the established canonical q bases to the pA frame by boundary rotation
`i -> i−1 mod 5` and color swap (0 1). Select any degree-four interior z
whose sole boundary neighbor is b1 or b4, and add its missing edge to the
other of these two boundary vertices. Allowing either choice is a generous
cover of §4, where zb4 was deleted. The complete finite list is:

| Inherited family | Eligible (base,z) entries | Augmented graphs rejecting q |
| --- | ---: | ---: |
| One triangle with canonical tails | 10 | 0 |
| Two triangles with a direct bridge | 64 | 0 |

All 74 augmented graphs have an explicit q-coloring. Their full component
relations at q, pA, pB are recorded, and their exact join is checked against
independent whole-graph colorings. Each base has complete degree four,
pA rejection, every pA edge-deletion coloring, and a replayed inherited
boundary-apex rotation. No claim is needed that an augmented graph is disk:
we prove q acceptance on a cover that can include nondisk augmentations.

The q-coloring of the normal augmentation lifts to M by §4 while keeping
z's color fixed, contradicting that M rejects q. This proves pA extends
in all four cases. The argument did not independently classify the short
region and did not assume that its C4 boundary satisfies a C5 theorem.

## 6. Reflection only, including the two target rows

Apply the existing rho=(3,2,1,0,4), pi=(0 1) to the same source, actual
attachments, all component colorings and ordered contact tuples. By
[TwoSpokeReflection.lean](../Math/TwoSpokeReflection.lean),

```
R*_C(Tb)=pi R_C(b),       F*_C(Tb)=pi F_C(b),       Tq=q.
```

The disk embedding reflects; degrees, criticality, T4 acceptance, component
identities and the number/order of contacts are unchanged. The precise table is:

| Original case | Reflected S | Reflected C2 side | F*_C2(q) | F*_C1(q) |
| --- | --- | --- | --- | --- |
| I | {b2,b4} | pentagon | {1} | {3} |
| II | {b2,b4} | pentagon | {3} | {1} |
| III | {b2,b4} | quadrilateral | {1} | {3} |
| IV | {b2,b4} | quadrilateral | {3} | {1} |

The reflected boundary arcs, in transported order, are (b2,b1,b0,b4) and
(b4,b3,b2). Notice that reflection **exchanges the two query orbits**:

```
T(pA)=21010,   (0 2) T(pA)=01212=pB;
T(pB)=02012,   (1 2) T(pB)=01021=pA.
```

Color invariance of extension therefore transfers both conclusions.
`reflection_separation` formalizes this implication using the established
transport as its hypothesis. There is no independent {b2,b4} enumeration.

## 7. Exit integration and exact scope

For a source G with Sigma(G)=Omega\{p,q}, its minimal q-obstruction M
inherits every other accepted row and T4 acceptance. The new theorem
makes its designated adjacent-singleton p extend. Hence in this **source
context** Sigma(M)=Omega\{q}. Deleting edges outside M and taking the first
step releasing p gives the existing single-sided exit.

The original 24 two-spoke configurations now have an exit-compatible
separation: six (3) cases and six adjacent (2,1) cases are excluded; four
adjacent split-support cases are single-missing; the eight nonadjacent
cases extend the two designated p rows. This completes t=2 under the
unique-degree-five hypothesis. It does not assert single-missing for
all nonadjacent sources under T4 alone, or settle their realizability.

General core existence/separation, t≤1, multiple degree-five vertices,
degree≥6, the common pivotal edge, and K-infinity=K-at-most-five remain
open. No 603-profile or fixed-point artifact changes.

## 8. Evidence and replay

[Checker](../scripts/c5_two_spoke_nonadjacent.py),
[certificate](../artifacts/c5_two_spoke_nonadjacent/observations.json),
[Lean finite algebra](../Math/TwoSpokeNonadjacent.lean), and
[axiom audit](../Math/TwoSpokeNonadjacentAudit.lean).

The arbitrary-size coverage relies on inherited paper structure/minor and
path-transfer theorems, including the external degree-list characterization
([Schweser–Stiebitz](https://arxiv.org/html/1507.04569v1), ordinary all-positive
specialization). Python checks the justified finite forms and saved concrete
colorings/rotations, using no new planarity oracle. Lean uses ordinary
`decide` for finite query algebra and ordinary proofs for transport; it
does not formalize the graph reductions or the 74/3,492 certificates.

```bash
python3 scripts/c5_two_spoke_nonadjacent.py --check
python3 scripts/c5_two_spoke_split_support.py --check
python3 scripts/c5_two_spoke_reflection.py --check
lake build
lake env lean Math/TwoSpokeNonadjacentAudit.lean
python3 scripts/check_docs.py
git diff --check
```

Actual verification and inherited checks not rerun are recorded in the
[research record](history/2026-09-27-nonadjacent-two-spoke.md).
