# Original long mixed pieces: diagonal slack and the contact-three transfer

Scope: the exact working tree snapshots named in the parent `BASE.json`, with
the complete source contract in the frozen spoke-closure §1 and residual
unification §1. This report writes only this new `long/` audit directory. No
source generation, graph replacement, independent normalization, commit, push,
or Graphify was performed. Original `(u,t)=(0,0)` singleton-support mixed pieces
remain allowed wherever the existing contract allows them.

Write `I={0,1,3}`, `q=(01212,01202,01021)`, and `D=3`. For an original mixed
component C, define

`M_C={i in I : (D,D) is absent from the full A_C(q_i)}`.

Every assertion concerns the same original C and the same literal frame. A
local extension means a coloring of all its original vertices, preserving every
original internal edge, boundary attachment, root contact, and literal shared
contact. It is not a product of contact marginals.

## 1. Literal shared contact gives full diagonal acceptance

**Lemma L-SHARED.** If an original vertex v of C is adjacent to both roots,
then `M_C` is empty. More generally C accepts `(a,a)` for every common color
a in every proper boundary row.

For a fixed row and common color a use the original lists

`L(x)=[4] \ (q(N_B(x)) union {a : x sees at least one root})`.

For every x, full original degree four gives `|L(x)| >= d_C(x)`. At the literal
shared vertex v, the two different original edges rv and sv delete only one
color a, so `|L(v)| >= d_C(v)+1`. A connected graph with degree lists and one
strict inequality is list-colorable: root a spanning tree at v, color the other
vertices from the leaves towards v, and color v last. Each nonroot vertex has
an uncolored parent when colored, while v has the spare color. This colors all
original C; neither root is identified or contracted.

The shared contact lemma only needs connected C and complete degree four.
It does not require a same-row external coloring, source realization of a
control, or a common owner.

## 2. At most three total root incidences gives a three-row escape

**Lemma L-CONTACT-THREE.** Suppose C is a long original mixed piece in the
complete target contract and

`k_C=|N_C(r)|+|N_C(s)| <= 3`.

Then `M_C` is a proper subset of I.

The proof transfers the frozen unary three-row proof §§2–4 directly on the
original graph, not through a synthetic unary source. If C has a literal
shared contact, Lemma L-SHARED already proves more. Otherwise put

`X=N_C(r) union N_C(s)`.

The two original contact sets are disjoint and `|X|=k_C`. For both roots fixed
to D, the lists are exactly

`L_i(v)=[4] \ (q_i(N_B(v)) union {D : v in X})`.

In every step of frozen unary §§2–4 replace “r-contact” by “member of X”.
The following are all the local premises actually used there:

* C is connected and every original vertex has complete degree four. Its
  original blocks are bridges or odd cycles, by frozen size-bound §4.
* Each vertex has at most two adjacent boundary neighbors, by frozen
  spoke-closure §6. A long one-sided piece with support of size at least two
  has its exact support equal to the vertices of its shield arc, by frozen
  shield-budget §2 Lemma 2. Thus long C has support of size at least three.
* Every leaf block of a multiblock C has a private original root contact,
  by frozen spoke-closure §3 Lemma 1. Its owner does not occur in the proof.
* Each odd-cycle block has at most one ordinary private vertex, where
  “ordinary” means a noncut vertex with no contact in X, by frozen
  spoke-closure §2.
* Vertices of H-degree two have distinct original boundary-edge attachments,
  by frozen size-bound §3 Lemma 2. In the no-shared-contact setting, a C
  bridge leaf with one contact has H-degree two, precisely as in the unary
  proof.

These give the same complete case split, with the same literal signature
table, as follows. Each cycle has length at most `1+|X|<=4`: every cut vertex
provides a different contact in an exterior leaf branch, each private contact
provides itself, and there is at most one ordinary private vertex. Hence every
cycle is a triangle. A triangle whose palette excludes D cannot have an
ordinary private vertex. Its three terminal directions use three different
contacts, and a contact at a cut vertex would require a fourth contact.

A leaf bridge has singleton palette `T(e)` from its actual boundary edge e.
Its first vertex toward the interior cannot be an ordinary bridge cutpoint
(it would repeat e at two H-degree-two vertices), an ordinary triangle
cutpoint (the third-color signature is no actual boundary-vertex signature),
or a contact-triangle cutpoint (the bridge would have to use D). These are
the three original-vertex checks in frozen unary §3; splitting contacts
between r and s changes none of the lists or equations.

There are one, two, or three leaf blocks. A single block is respectively an
impossible singleton, a bridge repeating its boundary edge, or a triangle
whose three private contact attachments all name the same boundary vertex,
contrary to support size at least three. With two leaves, a cycle leaf uses
two contacts, and the remaining bridge end fails one of the first-neighbor
checks. Two bridge leaves either fail the same checks, or, with the third
contact at the only interior cutpoint, form the three-vertex path excluded
by the literal two-edge signature table. With three leaves, all three leaves
are contact bridges. The unique branching node is either a cut vertex
(three D-free bridges cannot supply its list containing D; a triangle plus
two bridges fails the first-neighbor check) or a triangle block. The latter
uses three distinct actual leaf boundary edges and is excluded by the
frozen unary §2 three-edge signature lemma. This is the original unbounded
block-tree argument, including arbitrary bridge chains and side branches.

Therefore all three rows cannot reject the diagonal pins. This transfer does
not assert that r and s coincide, that an exterior coloring uses the same
color on them, or that a unary degree-five source has been constructed.

## 3. A row-independent necessary block pattern

This is an additional necessary reduction; it does not prove a general long
escape or a same-row joint.

**Lemma L-D-PATTERN.** If C has no shared contact and rejects `(D,D)` in
all three rows, then the set of original blocks whose Gallai palettes contain
D is the same in all three rows.

Use the tight degree-list characterization, already an external dependency
of the frozen reports. For each row i and each original block K let
`y_i(K)=1[D in P_i,K]`. The disjoint palette union at each vertex gives

`sum_{K containing v} y_i(K) = 1[v not in X]`.

There is at most one real solution to these equations. Indeed, if two
solutions differ, retain every block node with nonzero difference and all its
incident vertex nodes in the block-vertex incidence forest. A retained block
node has degree at least two, since every block has at least two vertices.
A retained vertex cannot meet just one nonzero block, because the sum of
differences at that vertex is zero. Thus every node in a nonempty finite
forest would have degree at least two, a contradiction. The block-vertex
incidence graph is a tree for an original connected cactus; adding noncut
vertices as leaf nodes is harmless. The singleton case is already excluded
for long C.

This fixes D-membership only. The other colors in each block palette can
vary with the row. In particular it does not identify the remaining color
signatures between arbitrary different blocks, or show that two different
long pieces escape on the same row. Further propagation is unfinished.

## 4. Exact original-graph corollaries and residuals

All original root spokes avoid D, since the selected rows use only 0,1,2;
the original rs edge is absent. Short mixed pieces accept the full diagonal
in every row by frozen E4 §4.1, including all original shared contacts.

* `(ell,u)=(1,0)` is excluded when the long has a shared contact or
  `k_C<=3`: take the long escape row and the short full lift in that same
  row and at those same pins.
* `(1,1)` is excluded when the long has a shared contact, conditional on
  adoption of the unary escape lemma: the long accepts every selected row,
  so take the actual unary escape row and the short full lift there.
* `(2,0)` is excluded when one long has a shared contact and the other
  has a shared contact or at most three total root incidences. Both long
  full lifts exist in the escape row of the latter.

Two proper rejection masks can have union I. Consequently two separate
three-row escapes do not close `(2,0)`, and an independent unary escape
and low-contact long escape do not close `(1,1)`. A source can only be
excluded using a single row and all complete original lifts in that row.

The remaining long cases, including no-shared-contact `k_C>=4`, retain
their full joint obligation. In particular no result here eliminates the
allowed `(u,t)=(0,0)` singleton-support counterpart merely because the
other piece is long. Original55, complete N2, and E-ARC2 remain OPEN.

No new Lean theorem is asserted. The finite controls in `checker.py` check
the original local lifts and explicit controls; they do not prove arbitrary
block-tree coverage or supply a target source realization. Independent
adoption of the transferred unary proof remains separate from these checks.

## 5. Executed local controls and replay

`checker.py` reads only the component-slack JSON snapshot in the parent
BASE and verifies its exact SHA and byte count. From its 63 original graphs
it selects all 37 long mixed pieces, preserving original ordered roots,
vertices, region edges, actual attachments, contact sets and shared contact
coordinates. Numeric-order DFS recomputes every full local lift for all ten
literal boundary rows and all 16 ambient ordered pin cells, then compares
the full tuple arrays to the frozen source, including empty cells.

The frozen artifact's numeric row order differs from the named q labels.
The checker explicitly selects `01212`, `01202`, and `01021` by their literal
beta; its output records this mapping separately from source row indices.

| Control | Result and precise scope |
| --- | --- |
| Full frozen local fibres | 370 rows, 5,920 cells, 594 empty cells; exact tuple equality |
| Shared-contact, complete degree-four local controls | 34 triggered and holds; all selected diagonal masks empty |
| Frozen long support≥3 and k≤3 | 0 controls, not triggered; no finite coverage claimed |
| Named split-owner three-contact path | q0/q1 reject `(D,D)`, q3 accepts it; triggered and holds for the local lemma premises |
| Named long shared-contact bridge | All three diagonal cells nonempty; triggered and holds |
| Remove H-degree-two attachment injection | Split-owner bridge with both endpoints attached to 01 rejects all three diagonals; counterexample to that stronger local statement |
| Remove long support | Split-owner triangle with all boundary attachments at 0 rejects all three diagonals; counterexample to that stronger local statement |
| D-pattern incidence equations | Five named cactus incidence trees; every 0/1 palette-membership vector has a different vertex-sum vector |
| Complete Σ933/941 N2 target source | 0, not triggered; no source realization or exclusion certificate |

Each of the four named controls stores all ten rows and 160 complete cells,
including empties. The controls do not assert a complete disk source,
criticality, original root degree five, or an independently checked rotation.
The unbounded theorem is justified by the paper transfer, not by these counts.

Two failed generation attempts occurred before any output artifact was
created: an incorrect JSON table field, followed by an incorrect assumption
about numeric row order. Both errors and their corrections are retained in
`generation_failures.json`; no evidence was overwritten. The final artifact
has 1,386,629 bytes and SHA256
`b098f3af30610782ddfafae24f960dda8b813231a5e8c3f84cbdad1c1b6f18fc`.
Normal and hash-seed-17 read-only replay pass with identical bytes and SHA.
The deliberately corrupted copy is retained and fails with `artifact mismatch`,
exit 1. Exact outputs are retained in `verification.json`.

```bash
python3 -B audits/2026-10-11-n2-unary-adoption-long-joint/long/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n2-unary-adoption-long-joint/long/checker.py --check
```

The new canonical diagonal report §3–4 was independently read: the two
transfer proofs and the mask-based same-row corollaries match this report.
Its complete parent contract and adoption decision remain authoritative; this
long audit does not edit the shared report or older certificates.
