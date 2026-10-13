# Fixed double-long complete-fibre and joint controls

2026-10-13. Exact input hashes and snapshots are in [BASE](BASE.json).
Only this `controls/` directory is written. The inputs are the live long-synchrony,
partition and residual reports and the retained earlier four-contact control.
This is a fixed calibration, not an original-source census or a proof of the full
N2 `(2,0)` branch. Every target-source status is `not triggered`.

## 1. Minimal local diagonal obstruction and its full relation

Retain the original path `p0-p1-p2-p3`, attachments `01,0,2,12`, and ownership
`r,r,s,s`. Every path vertex has complete degree four; contacts are distinct,
there are no shared contacts, actual support is `012`, and its two H-degree-two
vertices have distinct actual boundary edges. This is the frozen earlier
four-contact control, with all ten literal rows and sixteen ordered root pins.

Let a proper coloring of its actual support be `(A,B,C)` with `A!=B` and `B!=C`.
For **all** ordered root pins `(x,y)`, not just the selected three rows,

```
F_P(A,B,C;x,y) is empty iff
x not in {A,B} and y not in {B,C}.
```

If either root color equals one of its actual contact-boundary colors, the
original degree-four collision/slack lemma supplies a full coloring of P.
Conversely, when both avoid their indicated pairs, p0 and p3 have singleton
lists. After coloring those endpoints, the neighbors p1 and p2 are both forced
to B, violating their original edge. This proves the exact forbidden rectangle
without enumerating path templates or treating a necessary filter as sufficient
in general. Sufficiency here is specific to this original path.

In every selected `q0,q1,q3`, unused `D=3` lies in that rectangle, so `M_P=I`.
This refutes a **local** all-contact diagonal-escape lemma. The accepted
low-contact theorem excludes `k<=3` under its stated local premises; consequently
`k=4` is the first possible contact count for this obstruction. With no shared
contacts, four contacts require at least four original vertices, achieved here.
This is minimality of this local diagonal obstruction, not minimality of a full
N2 counterexample or of an arbitrary failed joint.

Every accepted cell is represented by **all** complete original tuples.
The checker recomputes these using both lexicographic DFS and independent
Cartesian color enumeration and exactly recovers the frozen earlier data.

## 2. One explicit shared original H, including the external factor

Fix `B=(0,1,2,3,4)`, `r=5,s=6`, P vertices `(7,8,9,10)`, and Q vertices
`(11,12,13,14)`. P is the preceding path on support012. Q is the literal copy on
support234, with attachments `23,2,4,34` and ownership `r,r,s,s`.
Add exactly the original root spokes `r0,s4`. The complete original edge list,
original degrees, contacts and attachments are retained in
[observations](observations.json). Thus

- roots are nonadjacent and have degree five; all eight other H vertices have
  complete degree four;
- H is biconnected, `H-{r,s}` has exactly the two original long pieces, and every
  boundary vertex has an actual H attachment;
- the external factor is precisely `x!=q(0)` and `y!=q(4)`;
- all ten literal rows and all sixteen ordered pins are retained for both pieces
  and for their complete original joint, including every empty cell.

The global original tuple order is `(r,s,7,8,9,10,11,12,13,14)`.
The checker compares the full same-row, same-pin product with a direct original
full-graph DFS; it also verifies every original edge of every resulting lift.
No rotation is invented: this graph is nonplanar, as certified below, so a disk
rotation is impossible.

Both diagonal masks are I. Nevertheless all ten literal rows have full joints;
in particular the three intended rejected rows have the following exact
accepting pin sets and sample **complete** lifts:

| Row | All accepting ordered pins | One complete original lift |
| --- | --- | --- |
| `q0=01212` | `(1,0),(1,1),(1,3),(2,1),(3,1)` | `(1,0,2,3,1,3,0,3,1,3)` |
| `q1=01202` | `(1,0),(2,1)` | `(1,0,2,3,1,3,3,0,1,3)` |
| `q3=01021` | `(1,2),(2,0)` | `(1,2,2,3,1,3,3,2,0,3)` |

The complete table contains 181 full original graph lifts. These are actual
same-original-H joints, not separately chosen witnesses or separately normalized
sources. The control refutes a local diagonal-only conclusion but **supports**
the off-diagonal collision lemmas. It is not a full target: it is nonplanar,
accepts all required rejected rows, and has no Sigma933/941 criticality claim.

## 3. Collision and capacity calibration

For each actual original root v, let `E_v` avoid its original spoke colors.
For original piece C, let `W_C^v` be the actual boundary neighbors of its original
v-contacts and `X_C^v=E_v intersect q(W_C^v)`. All these sets are retained per row.

The checker records the complete forbidden fibers for both root orientations,
all four fixed colors and both pieces; each forbidden column has size at most
the actual incidence count of the free root. In this fixed graph both incidence
counts equal two and `|E_r|=|E_s|=3` in every row.

For every `x in X_C^r`, C accepts all s-pins by original collision slack; the
other original piece forbids at most two of the three available s-colors. The
checker retains a same-row full original lift for each such trigger, and does
the symmetric test from s. There are 48 one-sided collision-plus-capacity
triggers, all `triggered and holds`. This is an exact finite calibration of the
parent's arbitrary-size proof, not the proof of its universal quantifier.

For every cross-collision pair `x in X_P^r,y in X_Q^s` (and P/Q reversed), both
pieces accept in that one literal cell. There are 29 such pairs with retained
complete original lifts, all `triggered and holds`. Across the 320 local cells,
240 collision filters trigger and hold; the remaining 80 are empty in this
specific path control. A nontriggering collision filter does not imply rejection
for a general original piece.

## 4. The old local obstruction is topologically blocked by an outside attachment

There is a stronger, arbitrary-size **conditional source exclusion** for the
exact P pattern of section 1. Suppose another original mixed component Q is
connected and has an actual attachment to boundary vertex3. The following
original branch sets form K3,3:

```
left:  {b2,b3}, {r,p0,p1,b1}, {s}
right: {p2},    {p3},        V(Q).
```

They are disjoint and connected. The first left bag sees p2,p3 via their actual
b2 attachments and Q via its actual b3 attachment. The second sees p2 via
p1-p2, p3 via b1-p3, and Q via an original r-contact. The third sees p2,p3 through
their actual s-contacts and Q through an original s-contact. Thus all nine
cross adjacencies use literal original edges; Q's size and internal shape are
irrelevant. No relation is assigned to the minor or transferred to a replacement.

For an attachment to vertex4, the reflected original branch sets are

```
left:  {b0,b4}, {s,p3,p2,b1}, {r}
right: {p1},    {p0},        V(Q).
```

The same direct nine-adjacency argument applies. Consequently this exact all-I
path cannot coexist in a planar original graph with a second mixed component
having any actual support outside012. Applying this to a full `(2,0)` source
still requires its actual shield/support geometry to force that outside
attachment; the finite control does not infer such geometry from local masks.

Both original K3,3 certificates are checked in the fixed graph of section 2.
This proves its nonplanarity using only connected branch sets and original
adjacencies. A planarity oracle or a proposed rotation is unnecessary.

## 5. Replay and scope

```
python3 -B audits/2026-10-13-n2-double-long-joint/controls/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-n2-double-long-joint/controls/checker.py --check
```

The retained deterministic artifact has 241,306 bytes, SHA256
`724a540c00a8248d2b45b48acdb1cd9d702f26ab68053d8926a3d3d31c406658`.
It contains 320 local ambient cells, 80 local empty cells, 856 local full tuples,
160 full joint cells, 181 complete global lifts, 48 one-sided collision-capacity
joints and 29 cross-collision joints. Normal and seed17 replay agree byte for
byte; deliberate corruption is rejected, as recorded in
[verification](verification.json). All frozen input hashes are rechecked.

No broad source enumeration, new external theorem, Lean theorem, commit or push
occurs here. Full-target status remains `not triggered`; arbitrary-size claims
are carried by the displayed proofs or the parent's independently reviewed
lemmas, not by this finite calibration.
