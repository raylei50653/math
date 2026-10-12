# Independent same-row reduction and original K5 obstruction

2026-10-12. This report uses the eighteen inputs sealed by
[BASE](../BASE.json), at HEAD `8b76dcc82adabba679e7b0d2ef6dbe6eb9cc37f3`.
Only this new report is written by its author. No shared documentation, frozen
input, prior certificate, source graph, or remote state is changed.

## 1. Exact scope

The target is the full original N2/55 source contract of the frozen
`docs/c5_excess_two_n2_partition_rule.md`, specifically `(ell,u)=(1,1)`.
The already adopted reduction gives an original unary U, owned by r, with
`k_U=2`, actual support exactly the consecutive original arc `A=(a,b,c)`, and
for every fixed rejected row `i in I={0,1,3}`:

`F_U(q_i)={c_i}`, where `c_i` is a used color on the actual support.

Here `F_U(q)` consists of owner colors with an **empty complete original U
fibre**; all original U coordinates and attachments remain fixed. The full
source also has: original degree four at every U point; bridges/odd-cycle
cactus blocks; a private owner-contact in every leaf block; at most one
ordinary private point in an odd-cycle block; adjacent-pair upper bound on
frame attachments; and injectivity of original frame-edge attachments at
H-degree-two points. These are adopted source inputs, not local conclusions
from the finite controls.

The proof below shows that every proper row whose three support colors are
pairwise different has `F_U(q)=empty` in a planar source. At least one of the
three named rows has this property for each original three-point arc. This is
a same-row contradiction to the adopted capacity conclusion. It closes this
one parameter subdomain, not the two no-unary long subdomains or E-ARC2.

## 2. Arbitrary-size classification from original attachments

Every U point of H-degree two has exactly two original frame neighbors. Those
neighbors form an original frame edge, and the edge lies inside `A`. Thus its
attachment is either `ab` or `bc`. The adopted attachment injectivity gives
at most **two** such U points. This is an original graph bound; no component
is shortened or replaced.

Since the graph is simple and U has only owner r, its two root incidences are
two distinct original contact points. If U has multiple blocks, the block-cut
tree has at least two leaves, each requiring its own private contact. Hence
there are exactly two leaves, each has exactly one contact, and there is no
contact at a cutpoint or in an interior block. A finite tree with exactly two
leaves is a path, so the whole block-cut tree is a path.

Each leaf bridge contributes an H-degree-two private contact. Each leaf
triangle contributes an H-degree-two ordinary private point. An odd-cycle
leaf longer than a triangle would have at least three ordinary private
points, already impossible. Every interior triangle would contribute an
additional ordinary private H-degree-two point. Every junction of two bridge
blocks would be a noncontact C-degree-two point, hence another H-degree-two
point. The two leaf contributions exhaust the budget. Therefore no interior
triangle and no bridge/bridge junction occur.

For a single block, a bridge is possible; an odd cycle longer than a triangle
has at least three ordinary private H-degree-two points and is impossible.
Consequently U is one of the following five exact original graphs:

1. One bridge, with both ends contacts.
2. One triangle, with two contacts and one ordinary private point.
3. A leaf triangle joined to one terminal bridge.
4. Two triangles sharing their cutpoint.
5. Two triangles joined by one bridge.

For each of the last three forms, the two H-degree-two attachment edges are
the two **different** edges `ab` and `bc`: distinctness follows from the
original injection, and there are no other edges available inside the
actual support. The ordinary private point in each triangular leaf supplies
its edge; a terminal bridge contact supplies the other edge in form 3.

## 3. Original degree-list analysis in a Diff row

Fix a proper original frame row `q` with pairwise distinct
`x=q(a)`, `y=q(b)`, `z=q(c)`. Fix one owner color `alpha` and suppose its full
original U fibre is empty. The inherited degree-list theorem makes every
list tight and expresses it as the disjoint union of palettes of the
incident original blocks. An original bridge has a singleton palette; an
original triangle has a two-color palette. We use no marginal relation.

For an ordinary private point attached to an edge `e`, its triangular
palette is `P_e=[4] minus q(e)`. For a private contact in that same triangle,
its single frame attachment `h` satisfies

`{alpha,q(h)}=q(e)`.

In particular `alpha in q(e)`. At a noncontact triangle/bridge cutpoint, the
joining bridge color `d` must lie in `q(e)`, since it is disjoint from `P_e`.
The root color `alpha` need not differ from `d`: the cutpoint has no original
root edge. That distinction is essential in form 5.

For form 1, the two contact attachments are `ab` and `bc`. If alpha is used
on the support, at least one contact has two distinct external neighbors of
the same color, so the adopted strict-list/slack argument gives a complete
lift. If alpha is the fourth color, the two singleton lists are respectively
`{z}` and `{x}`; they differ, so the bridge is colorable. Thus no alpha is
forbidden in a Diff row.

For form 2, the ordinary point's attachment is a frame edge `e`. The palette
equality forces both private contact frame attachments to have the other
color of `q(e)` from alpha. Because the support is Diff, frame colors identify
the three named support points individually. Both contacts therefore attach
to a single endpoint of `e`. The actual support is contained in `e`, contrary
to the original support being all three points. Thus no alpha is forbidden.

For form 3, let `e` be the ordinary triangle point's edge and `f` the terminal
bridge contact's edge. The latter's tight singleton list forces both alpha
and the bridge palette color d to avoid `q(f)`, with `alpha != d`. The
triangle forces `alpha,d in q(e)`. Therefore `q(e)` and `q(f)` would be
disjoint. They share the color of their common original endpoint b, a
contradiction. This argument works in Eq rows as well.

For form 4, the shared cutpoint's full list is `[4]`; the two triangular
palettes must be disjoint. Since `e` and `f` share the original point b,
their two-color complements cannot be disjoint. Again there is no forbidden
alpha, even in an Eq row.

For form 5, `e=ab` and `f=bc` after naming the two original triangular leaves.
Their private contacts give `alpha in q(e) intersect q(f)`. Their joining
bridge color d also lies in that intersection. In a Diff row the
intersection is exactly `{y}`, so

`alpha=d=y`.

The leaf contacts' frame attachments must therefore be the outside endpoint
of their leaf edge. At each triangle/bridge cutpoint, the list is
`P_e disjoint-union {y}` or `P_f disjoint-union {y}`, respectively. Its single
frame neighbor must also be the outside endpoint. Thus a Diff-row rejection
forces the following original attachments, using original labels
`v0,v1,v2` and `v3,v4,v5` for the triangles and joining edge `v2v3`:

`r` contacts exactly `v0,v5`; frame attachments are
`v0 -> a`, `v1 -> {a,b}`, `v2 -> a`,
`v3 -> c`, `v4 -> {b,c}`, `v5 -> c`.

This is a local uncolorable control, not yet a source contradiction. It is
excluded by the original graph minor in the next section.

## 4. Independently checked original K5 bags

For the forced form 5 above take the five disjoint original branch sets

`{a}`, `{v0}`, `{v1}`, `{v2}`, and
`X={b,r,v3,v4,v5}`.

The first four form a K4: `v0v1v2` is the original triangle, and the three
edges `av0,av1,av2` are the forced original attachments. The fifth set X is
connected by the original edges `bv4`, the second triangle, and `rv5`.
Its four adjacencies to the singleton sets are respectively

`ab`, `rv0`, `bv1`, and `v2v3`.

Thus all ten K5 adjacencies occur in the original G, with no missing
inter-bag edge and no bag overlap. No independently recolored or contracted
source is asserted to retain its relation. A planar disk G cannot contain
these branch sets. The same argument applies to the reverse leaf orientation
by naming the corresponding original vertices; it does not independently
normalize the frame or change any root ownership.

The minor uses only the original unary and frame edges and the owner r. It
does not need an L or S coloring, a new interface edge, a size bound, or a
particular value of the owner's original complete degree. Therefore the
barbell possibility is excluded in every planar full source for which its
Diff-row degree-list rejection occurs.

## 5. Exact same-row source restoration

For each of the five original three-point arcs, its Diff set among the
unchanged named rows `q0=01212`, `q1=01202`, `q3=01021` is nonempty. Choose one
such **original row** `q_i`. Sections 3 and 4 prove that the original U
accepts every owner color in that row, with a full original tuple.

There are two equivalent source contradictions:

- The adopted exact original55 capacity gives `F_U(q_i)={c_i}`, whereas the
  preceding proof gives `F_U(q_i)=empty` for that same i and same U.
- The adopted deletion result says `G-U` accepts this same q_i. Take one full
  original `G-U` coloring and its actual owner color alpha. The accepted full
  U fibre at that alpha supplies every missing original U coordinate. The
  unchanged frame, roots, other pieces, external edges, shared contacts,
  rotations, bridges, and free-coordinate factors then give a full original
  G coloring, contrary to the original rejection of q_i.

The second argument explicitly establishes a same-row, same-pin full lift;
it does not combine separate local normalization choices or different rows.
No off-diagonal L/S theorem is needed after this unary obstruction. The
previous high-contact L bounds remain historical necessary conditions for
the now-excluded `(1,1)` candidate, not separate counterexamples.

## 6. Correction and evidence boundary

An initial independent scratch derivation imposed `d != alpha` on the
internal bridge of form 5. That was incorrect: neither bridge endpoint is a
root contact. The root supplied the exact barbell control above, which
indeed forbids the middle supported color in Diff rows. This report retains
the correct palette relation `d=alpha=y` and proves its **original K5 minor**;
it does not claim that the nonplanar local barbell has an empty forbidden set.

This author independently reconstructed the classification, every palette
implication, all ten original minor adjacencies, and the same-row complete
restoration. The supplied barbell attachment pattern and earlier author's
minor suggestion were shared before this reconstruction, so this is an
independent verification of their final source argument, not an independent
discovery of that pattern.

The finite controls calibrated the local barbell and exposed the incorrect
bridge-color claim. They are not a source enumeration, do not trigger the
full N2 target, and do not prove the arbitrary-size classification. This
report adds no external theorem and no Lean theorem. The inherited external
degree-list input remains separate from the elementary original minor and
the full-lift restoration. General original55/N2, the remaining `(1,0)` and
`(2,0)` branches, E-ARC2, and the contract-external cases remain OPEN.
