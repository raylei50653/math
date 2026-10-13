# Original N2-55 one-long topology and independent closure audit

2026-10-13. This note works only in the complete original N2 contract used by
`docs/c5_excess_two_n2_diagonal_three_row.md`, its long-synchrony successor,
the partition rule, and unary-Diff closure. All graphs, boundary labels,
contact ownership, attachments, rotations, bridges and whole-piece fibres are
the original ones. A minor below disproves planarity of that original graph;
no colouring relation is transferred to the minor. This directory is exclusive
to the topology subtask. No shared report or previous evidence is changed.

## 1. Source and inherited exclusions

The original graph is a finite simple disk with ordered induced boundary
`B=(0,1,2,3,4)`, complete Sigma 933/941 (or one common whole-graph D5 image),
accepted T4 rows, every non-boundary edge Sigma-critical, and epsilon 2.
The effective interior H is connected and full-B-touch. Its only degree-five
vertices are nonadjacent roots r,s; every other effective interior vertex has
original complete degree four. `H-{r,s}` has exactly two original mixed
pieces, here long L and short S, and no unary piece. Both pieces are
one-sided. Free isolated coordinates, if present in the original convention,
retain their full nonempty four-colour factor.

We use the jointly fixed rows
`q0=01212`, `q1=01202`, `q3=01021`, and D=3.

Inherited results, used without enlarging their scope, give:

* H is two-connected; every non-boundary edge deletion accepts all rows.
* Every interior vertex, including either root, has at most two adjacent
  original boundary neighbours.
* The pieces are original bridge/odd-cycle cacti. Every leaf block of a
  multiblock piece has a private root contact. Each odd cycle has at most one
  ordinary private vertex. The actual boundary edges attached to distinct
  H-degree-two vertices are distinct.
* Each piece has at least two root incidences. The sum of mixed incidences is
  `kL+kS=10-t`, where t counts original root spokes.
* S accepts every common root colour in every proper row, with a whole-S
  lift (the original N-diagonal/hub result).
* In a surviving one-long branch, L has no shared root contact and `kL>=4`.
  The leaf-contact tree subdomain was previously excluded. The new proof
  below does not use a bound on the length of L.
* Long actual support is at least three vertices, forming its original
  shield interval; short support is nonempty. A short singleton is possible
  only when t=0. We do not assume S is a pair until this is justified.

For every original piece and fixed external pins, degree-four lists satisfy
`|L(v)|>=d_piece(v)`. One strict vertex in a connected piece gives a full
colouring by a rooted spanning-tree greedy order. Rejection makes all lists
tight and yields disjoint incident Gallai block palettes. These are the
already adopted degree-list inputs, not new external theorems here.

## 2. Fixed diagonal and literal closure

Let T be the set, rather than multiset, of original root-spoke endpoints.
Let W be the set of boundary neighbours of original L root contacts.
If a colour a belongs to `q_i(W)` but not `q_i(T)`, assign both roots a.
The corresponding contact has two differently named external neighbours
of equal colour, so L has strict list slack and a whole-L lift. S has its
whole-piece diagonal lift; the pins satisfy all original spokes. The two
same-row, same-pin complete lifts join in the original graph. Therefore

`q_i(W) subset q_i(T)` for each i=0,1,3.                 (C)

Define the literal closure
`cl(T)={h: q_i(h) belongs to q_i(T) for every i=0,1,3}`.
Thus W is contained in cl(T), with all boundary names retained. Direct
inspection of the three five-entry rows gives the useful exact form

`cl(T)-T subset {2,4}`,

where `2 in cl(T)-T` iff `2 notin T` and `{0,4} subset T`,
and `4 in cl(T)-T` iff `4 notin T` and `{1,2} subset T`.
These two extra points cannot occur simultaneously. This is a five-label
identity, not a two-bit replacement for a four/five-contact interface.

Since S accepts the D diagonal, L must reject `(D,D)` in all three rows.
At a private vertex of a cycle block, its list is exactly the cycle palette.
A private contact omits D, whereas an ordinary private vertex contains D.
Hence a cycle with a private contact cannot have an ordinary private vertex.
Each private cycle contact has one original root edge and exactly one actual
boundary neighbour h. All its private vertices therefore have palettes
`[4]-{D,q_i(h)}`. Equality of these palettes in all three rows forces the same
original h for all of them, because the five boundary colour signatures are
distinct. This argument retains the original root owners.

## 3. Boundary-arc minor excludes every leaf cycle

Suppose an original leaf cycle K of L exists. If L has one block, all its
vertices are private; otherwise only its unique cutvertex is nonprivate.
There is a private contact. Section 2 therefore says every private cycle
vertex is a contact and has one common actual boundary neighbour h. Choose
two adjacent private vertices p,q. Removing them leaves L connected: the
remaining part of K is a path, still containing the cutvertex when present.
Every boundary neighbour of p or q is h, so the remaining L retains at least
two distinct boundary neighbours other than h, since L is long.

Put `R={r,s} union S`; this is connected using the original mixed contacts
of S. It touches B because S has nonempty actual support.

If R has an actual attachment to h, set

`F=(L-{p,q}) union (B-{h})`.

F is connected using any retained L attachment outside h. The five bags
`{p},{q},{h},R,F` give K5: p-q is original; p and q each meet h, R (their
original respective owners), and F (their remaining cycle neighbours).
R-h is the stated attachment; F-h uses a boundary edge; R-F uses any
remaining L contact. Such a contact exists because `kL>=4`, contacts are
not shared, and only p,q were removed.

Otherwise choose an actual R attachment a, with a different from h.
Choose a retained L attachment `b notin {h,a}`. Of the two original a-h
boundary arcs, choose P whose interior does not contain b, and call the
other arc Q. Now take

`R'=R union (P-{h})`,

`F=(L-{p,q}) union (Q-{a,h})`.

R' is connected through its actual attachment a. F is connected through
the actual attachment b; Q has nonempty interior because it contains b.
The bags `{p},{q},{h},R',F` are pairwise disjoint. Besides the same six
adjacencies from p and q and the edge pq, the last edge of P gives R'-h,
the last edge of Q gives F-h, and the first edge of Q gives R'-F. These
are ten original adjacencies, so again the original graph contains K5.

Both cases contradict disk planarity. Consequently **L has no leaf cycle**.
This proof covers every odd cycle length and arbitrary additional original
blocks; it is not a short-chain enumeration. It does not alter rotation or
ownership and does not suppose a third root or an outside source graph.

## 4. Leaf-bridge minor and the forced spoke pattern

L cannot be a singleton (`kL>=4` and no shared contact), a single bridge
(at most two nonshared contacts), or a single cycle (the preceding minor).
Its finite block-cut tree therefore has at least two leaf blocks, all bridges.

For a leaf bridge xp with private vertex p, the inherited leaf-contact
condition makes p an original contact. It has one root edge, its bridge
edge, and exactly two adjacent boundary neighbours a,b. Thus p has H-degree
two and its actual attachment is the original boundary edge ab.

**Leaf-bridge minor.** Both a,b cannot belong to T. If they did, use bags

`{p},{a},{b},R={r,s} union S,`

`F=(L-{p}) union (B-{a,b})`.

F is connected: the long support has an attachment outside ab, and removing
p leaves L connected. R is connected. The vertex p meets each other bag
using its contact, its two actual attachments, and its leaf bridge. The
edge ab is original; R-a and R-b are original spokes, potentially from
different roots; F-a and F-b are the two end edges of the complementary
boundary path; R-F uses a remaining L contact. This gives all ten K5
adjacencies in pairwise disjoint original connected bags, a contradiction.

The endpoints of every leaf-bridge attachment edge belong to W and hence
cl(T), but at least one endpoint is outside T. The closure identity now
forces one unique extra point h in `cl(T)-T`, and every leaf-bridge edge
is incident to h. Boundary-edge injection permits at most two such leaves.
There are at least two, so there are exactly two, with the two distinct
boundary edges incident to h. Both neighbours of h must belong to T.

If h=2, closure requires 0,4 in T, and the two incident leaf edges require
1,3 in T. Thus `T={0,1,3,4}`. If h=4, the same argument gives
`T={0,1,2,3}`. In both cases there are four distinct spoke endpoints.
Each root has at most two spokes, so `t=4`; both roots have two spokes and
their endpoint sets are disjoint. Since `kL+kS=6`, `kL>=4` and `kS>=2`,

`kL=4`, `kS=2`, and `kL^r=kL^s=2`, `kS^r=kS^s=1`.

The last owner counts follow because each mixed piece meets each root,
and each root has exactly three mixed incidences after its two spokes.
The possible spoke edges, without exchanging any original labels, are

| Extra point | Leaf-bridge attachment edges | Two root-spoke edges |
| --- | --- | --- |
| h=2 | 12 and 23 | 01 and 34, in either root order |
| h=4 | 34 and 40 | 01 and 23, in either root order |

This is an arbitrary-size necessary classification obtained before any
finite local control. The root-side conclusion below excludes it.

## 5. Independent audit of the exterior reattachment lemma

Fix a rejected original row q and fix r to any colour a avoiding its actual
spokes. Consider the original connected induced graph on `S union {s}`;
its prescribed outside vertices are B and r. Each S vertex has complete
degree four, so its list has size at least its degree in this induced graph,
including shared S contacts without changing their identity. Root s has
no original edge to r. Since L has been removed, its list only excludes
its own spoke colours. Therefore

`|list(s)| >= 4-t_s = kS^s+kL^s-1`.

Its degree in this induced graph is `kS^s`. If `kL^s>=2`, s has strict
slack. A spanning-tree order rooted at s colours every original S vertex
and then s, yielding a whole `G-L` lift with the chosen r pin. All its
spokes and all original S edges and contacts are respected. This is a
same-row extension; it does not assume independently compatible masks.

Let `W_L^r` be the union of boundary neighbours of the original r-contacts
of L. If a also belongs to `q(W_L^r)`, the equal colours at r and one
actual boundary neighbour give strict list slack in L. Its whole original
lift joins the already fixed exterior lift, contradicting rejection. Thus

`kL^s>=2 implies q(W_L^r) subset q(T_r)`.

Swap r,s for the other direction. This argument is valid for arbitrarily
large S and L and for shared contacts of S; it colours the original
graphs directly. The assumption `kL^s>=2` is essential to the stated
strict inequality and is satisfied in the pattern of Section 4.

For the three literal rows, each of the individual spoke edges 01,34,23
has closure equal to itself. The displayed implication therefore gives
`W_L^r subset T_r` and `W_L^s subset T_s`. Each leaf bridge is owned by
one actual root, and both its boundary endpoints must lie in that owner's
two-element spoke set. Section 4's table shows that neither leaf edge
equals either available root-spoke edge, in either root order. This is a
contradiction.

Hence the complete original N2-55 `(long,unary)=(1,0)` source does not
exist, subject to the inherited source theorems and the independently
audited paper arguments above. No limit on long size or contact-interface
cardinality was used. The two-long branch, source contracts outside N2,
and the general E-ARC2 statement are not discharged here.

## 6. Evidence status

The new exclusion is a paper argument with original-edge branch-set
witnesses and constructive full-piece greedy lifts. The complete original
target is not supplied as a finite example: target status remains
`not triggered`. Literal closure tables and named minor controls are finite
calibrations; they do not carry the universal quantifier in Sections 3-5.
No Lean theorem, new source census, commit or push is claimed by this note.

The named controls in `minor_controls.json` preserve the graph vertices,
all original edges, five ordered bags, a spanning tree for each bag and
all ten cross-edge witnesses. They calibrate the direct leaf-cycle case,
the boundary-arc leaf-cycle case and the leaf-bridge case. Their complete
N2 source status is explicitly `not triggered`; degree completeness is not
asserted for these minor-only controls. Replays

```sh
python3 -B audits/2026-10-13-n2-one-long/topology/make_minor_controls.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-n2-one-long/topology/make_minor_controls.py --check
```

both pass, reconstructing three connected/disjoint K5 models and 30
original cross-edge witnesses. The retained artifact SHA256 is
`7cc4567aba9e24d65611bf2c53786f5ad4d89d6bd00525c643ba4ec577022435`.
Finite controls only check these named models; the original-source
existence of each needed bag is proved in Sections 3-4.
