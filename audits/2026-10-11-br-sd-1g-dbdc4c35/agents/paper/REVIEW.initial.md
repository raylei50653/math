# BR-SD-1g independent paper investigation — initial findings

2026-10-11. Reviewer task: `/root/paper`. Frozen research BASE:
`dbdc4c35f785519c8e3cb0260807f0d2feb82469`.
This is an initial mathematical investigation, not acceptance of final root bytes.
The reviewer writes only `agents/paper/`; prior audits and canonical are read-only.

## Inputs actually examined

- Frozen N45 canonical §1 and §2.11, especially the BR-SD-1a/1c/1e complete contracts.
- Frozen BR-SD-1a, BR-SD-1c and BR-SD-1e `PROOF.md`.
- Frozen author PDF `external/gallai.pdf`, pages 5–6, through direct text extraction:
  degree assignment means `|L(y)|≥d_C(y)`; Theorem 10 gives the exact blockwise
  union and pairwise disjointness at intersecting blocks, including equality/tightness
  as a consequence of non-colorability rather than an initial assumption.
- New audit `authority/INPUTS.json`, which identifies the above frozen bytes.

## Two old proof routes really have different boundaries

For `J1=(r,a1,x1)` and a finite nonempty connected W1 whose only skeleton neighbor
is x1, removing x1 separates W1 from the remaining skeleton. Thus x1 is a C-cutpoint,
and the unique member of `J1−{r,a1}` is no longer a private noncutpoint witness.
No second point in that set exists. J2, on the other hand, is untouched: W1 only
touches x1 in J1 and W2 only touches J3 or the q arm. Every
`w2∈J2−{r,u}` remains a noncutpoint, belongs only to J2, and is not an s-contact.

The direct 1e two-witness contradiction therefore has a missing premise. It is
invalid to repair it by inferring `D∈P_J1` from `D∈L(x1)`.
For example, an abstract W1 path of three edges may have singleton palettes
`{D},{A},{D}` while `P_J1={A,B}`. Every W1 vertex list contains D but the J1 palette
does not. Its final degree-one vertex would require three B attachments for
complete M-degree4; this is a local list illustration only, with no claimed actual
disk source, Σ, minimality, witnesses, or full source validation. It explains why
an arbitrary W1 leaf argument must respect parity and cannot force D into J1.

The formal 1c terminal lemma remains directly applicable when W2 attaches at v or
a3 (subject first to the original degree/s-contact table): J3's extra block
attachments are still only at its named v/a3, and all off-cycle arm points retain
their original C-neighbors. The coincidence `a3=v` admits no nonempty W2 by the
original complete degree equation, for either zero or positive q-arm length.
At an ordinary J3 point, W2 adds a third block attachment location and can occupy
the only triangle witness; at q or an arm interior point it changes the endpoint
or no-extra-C-edge premise. These are premise failures, not actual counterexamples.
For longer J3 a substitute private witness may preserve the old local calculation,
but the formal location premise should not silently be waived.

## Independently checked new finite chase

The root's proposed two-color chase appears mathematically sound under the exact
BR-SD-1g structural contract. Let the actual adjacent S-support pair have distinct
literal β colors A and B; let T be the third used color and D the unused fourth.
Then every noncontact vertex in S has both T and D in its complete original list,
while q has T and excludes D. No vertex of W2 is an s-contact.

The preserved J2 private witness is in the same original S. Its C-degree2 and
complete M-degree4 force two actual B attachments. Simplicity and S's pair support
force those attachments to be exactly the pair, whence
`L(w2)=P_J2={T,D}`. This is stronger than the old fact that P_J2 contains D.

The same-source block separation must be proved explicitly: the subgraph on
`S∪{r}` is attached to the L-side only through r, and J2 is its sole original block
at r. Unique attachment of W1 at x1 and W2 at its S skeleton point prevents merging
old blocks or creating a second exit. Consequently any block reached on the S-side
whose palette contains exactly one of T,D cannot meet J2 or escape through r:
an intersecting palette would share that literal color with `P_J2={T,D}`.

At q, the union formula for the complete list yields an incident block K0 carrying
T but not D. Every block has at least two vertices. Choose another vertex y in K0,
different from q. It lies in S, is a noncontact, and so needs D in its list. D must
come from another incident block K1. Disjointness at y excludes T from K1. Choose
a vertex z of K1 different from y; z needs T in a further block, whose palette
cannot contain D. Continuing alternates the two colors.

The block-cut tree, oriented away from q, certifies that each step leaves through
a vertex different from the incoming cutpoint and selects a block different from
the incoming block. The walk therefore never returns to q, revisits an earlier
block, or enters J2. If a chosen vertex is not a cutpoint, its missing color is
already an immediate contradiction; otherwise it forces the next outward block.
Finiteness rules out an indefinitely growing path. This is a genuine contradiction
for the same literal T,D, without independent color renaming or the false assertion
that every incident palette contains D.

This chase does not depend on W1's internal shape or on W2's legal attachment
position. It bypasses the W1 parity issue and the modified terminal degrees. The
proposed final theorem must nevertheless claim only the exact two-branch source
domain requested, not a new closure of general multipendant Gallai trees.

## Obligations before final acceptance

1. Root PROOF must retain the full original G/M contract, including M's own β
   inclusion-minimality and all retained-edge witnesses, without inferring it from G.
2. The complete degree-list/full-lift equivalence must account for every original
   edge and any original point ignored by effective H, retaining actual boundary
   attachments and all full-lift coordinates.
3. The root's final source mapping must make J2 ownership, the S-only contact q,
   and the unique r exit explicit; capacity rows are only necessary conditions.
4. Controls must distinguish abstract palette patterns, synthetic complete
   assignments, and `not triggered` actual-source tests. Source existence is not
   supplied by this paper argument.
5. A final independent review must identify and hash the exact root PROOF/MAPPING/
   REPORT bytes. Custody success and finite checks do not themselves prove the paper.

Initial outcome: no mathematical blocker found in the proposed finite chase.
Final acceptance remains pending. The full parent identity remains OPEN and the
new unconditional parent-closure count remains 0.
