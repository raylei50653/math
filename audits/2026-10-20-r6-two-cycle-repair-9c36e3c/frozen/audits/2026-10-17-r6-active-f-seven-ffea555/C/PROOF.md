# C. The all-distinct R100 reference and its exact separation obligation

Frozen BASE `ffea555fc2a896d8166ce198ca28ed9262912f25`, 2026-10-17.
Independent write scope: this audit's `C/` directory only. This note proves
an arbitrary-size conditional descent theorem and exact reference/move
rules. Existence of the required separating reference remains **OPEN**.

## 1. Same source and one complete reference colouring

Keep the same original minimum completed no4ct C5 source G, support,
ordered contacts, attachments, rotation, complete U319 fibres including
empty fibres, and all original r lifts. The actual graphs and marks are

`J=U/(s=t)`, `m=[s=t]`, `D=J*`,
`e=(vw)*`, `f=(pq)*`, `g=(mz)*`.

No original `d_G(v)=5` premise is added. Nothing below changes G, J, D,
or reconstructs a different completed source.

Fix any actual `M in P101`: e,g belong to M and f does not. Suppose
`F=D-M` has a nonfacial seven-component C containing f. Put `X=V(C)`.
The frozen seven-cap classification supplies the actual chorded-seven
subgraph and its five matching spokes `B=delta_D(X) subseteq M`.
The descent theorem below needs only that C is an odd complete F
component; its use for the surviving seven-cap is therefore legitimate
without extra local matching assumptions.

The frozen [full-distinct source result](../frozen/audits/2026-10-16-r6-319-joint-parity-f1faf74/A/PROOF.md)
supplies an actual complete all-distinct colouring. Take **one** such
colouring chi on this same graph, and normalize its three Tait colours as

`chi(e)=alpha`, `chi(f)=beta`, `chi(g)=gamma`.

Its three whole colour classes, simultaneously from chi, are

`R100=chi^{-1}(alpha)`, `R010=chi^{-1}(beta)`,
`R001=chi^{-1}(gamma)`.

Every class is a perfect matching. The complement of a class consists
of alternating cycles in the other two colours, hence is even. This
does not independently choose three private-colour witnesses or three
local cap extensions. The full source condition FJ and its frozen
[same-circle table](../frozen/audits/2026-10-15-route-round4-6ddea32/FULL_J_BRIDGE.md)
give, in this same chi,

`e and f lie on one alpha/beta cycle`,
`e and g lie on one alpha/gamma cycle`.

FJ supplies no corresponding requirement that f and g share a
beta/gamma cycle. Absence of that requirement is not existence of a
separating chi.

## 2. Complete-region exchange for any even reference

Let R be any actual perfect matching of D with even complement, and put

`L_R=D-(M intersect R)=(D-M) union (D-R)`.

Retain every vertex and every whole component of both complements.
Every alternating cycle of `M triangle R` lies in one component W of
L_R. For a component W, let A_W be **all** those difference cycles
contained in W, and define

`N=M triangle E(A_W)`.

Then

`(D-N)[W]=(D-R)[W]`,
`(D-N)[V(D)\W]=(D-M)[V(D)\W]`,
`odd(D-N)=odd(D-M)-odd((D-M)[W])`.                 (C1)

Here each restriction is a union of complete complementary cycles.
Every D edge crossing W is absent from L_R and so is a common matching
edge of M and R. It is absent from both complements and is unchanged by
the batch. Within W every noncommon matching edge is on one of the
selected whole difference cycles. Flipping all these cycles therefore
replaces the full complement on W by the even reference complement and
leaves the full complement outside W unchanged. This proves (C1).

Also W is a disjoint union of complete even cycles of D-R, so |W| is
even. The complete old F cycles on the same vertex set consequently
have an even number of odd members. If W contains C, then

`odd(F[W]) >= 2`.                                (C2)

This is the same complete-region argument as frozen
[A1](../frozen/audits/2026-10-17-r6-seven-five-repair-5b9a7b3/A/PROOF.md),
now stated for an arbitrary actual even reference. It does not discard
remote cycles or assume that removing C alone lowers full oddness.

## 3. Exact R100 conditional theorem

Set R=R100. At the three literal marks,

`e in M intersect R`, `f notin M union R`, `g in M\R`.

Thus e is deleted from L_R, whereas f and g are both **present** in L_R.
Let W_C(R) be its component containing C, and W_g(R) its component
containing the complete literal g edge. These objects are well-defined:
C is an F cycle and g belongs to D-R.

Every difference batch from M toward this R fixes membership of e and f.
Exactly one difference cycle contains g, and a complete-region batch
toggles g exactly when its component is selected. In particular:

**Theorem C1 (conditional R100 descent).** If an actual full all-distinct
chi has

`W_C(R100) != W_g(R100)`,                         (SEP)

flipping all actual difference cycles in W_C(R100) produces an actual
matching `N in P101` satisfying

`odd(D-N)=odd(D-M)-odd((D-M)[W_C(R100)])`
`          <= odd(D-M)-2`.

**Proof.** The selected region avoids g, so e,g remain matched and f
remains unmatched. Apply (C1) and (C2). QED.

All old complementary components outside the selected complete region
persist. The operation is on the same graph and has zero reconstruction
cost. It assumes neither oddness minimality nor a three-spoke reference.

For this fixed reference, (SEP) is also the exact condition for existence
of a batch of **whole L_R components** that includes W_C and remains in P101: including
the g component changes the marked identity to 100, and other regions
cannot restore it. This is a restriction on the specified exchanges,
not on all possible alternating batches in D.

Consequently an oddness-minimal M in the joint family must satisfy
`W_C(R100)=W_g(R100)` for every actual all-distinct reference chi.
Contradicting this universal blocking statement is the remaining task;
the minimizer observation does not by itself contradict it.

## 4. Why the other two classes have forced marked obstructions

For an even reference R, a mark common to M and R or absent from both
is fixed by every reference-difference batch. A mark in `M triangle R`
is toggled exactly when its L_R component is selected. This gives the
following statements for arbitrary batches of complete regions.

For R001, the mark identities are

`e in M\R001`, `f notin M union R001`,
`g in M intersect R001`.

The entire alpha/beta cycle of D-R001 containing e and f lies in L_R001.
Since f is on C, `W_C(R001)=W_e(R001)`. Any region batch containing C
therefore changes identity 101 to 001 and cannot remain in the joint
family `P110 union P101`.

For R010 all three marks belong to `M triangle R010`. The whole
alpha/gamma cycle of D-R010 containing e and g gives
`W_e(R010)=W_g(R010)`. A batch containing C toggles f from absent to
present. If the common e/g region is unselected, its resulting identity
is 111; if selected, its resulting identity is 010. Neither is a joint
identity. Selecting other regions does not affect the marks.

Thus the comparison distinguishes R100 for precisely the proposed
whole-region strategy. It does not establish that R100 actually
separates C from g, and it does not exclude other repairs using the
other references or exchanges outside these decompositions.

## 5. Both one-spoke and three-spoke references remain

Every colour class R from this one chi crosses B an odd number of times,
because `|X|=7`. The value five is impossible: it would force the chord
into R and leave C as a complete odd component of D-R. Hence

`|R100 intersect B|, |R010 intersect B|, |R001 intersect B| in {1,3}`.

The three classes partition all five spokes simultaneously, so their
three counts are a permutation of `(3,1,1)`. There is no proof here that
the three-spoke class can be chosen to be R100. Theorem C1 covers both
values without changing the exterior or choosing an independently
feasible boundary state.

If local matching fibres are used, the full frozen
[32-row relation](../frozen/audits/2026-10-17-r6-seven-five-repair-5b9a7b3/B/PROOF.md)
must be retained, including every empty row, every full internal state,
and the locally present but even-endpoint-incompatible state. A
one-spoke reference has two local difference paths and can have one or
two actual global difference cycles through the cap; a single global
cycle is a three-spoke conclusion. No such uniqueness is needed here.
An admissible local row is not a complete source colouring witness.

## 6. Actual Kempe moves that can change R100

The following candidates use entire actual two-colour cycles of chi.
They transport all private colours and preserve the literal normalized
frame `e=alpha,f=beta,g=gamma`.

* An alpha/beta cycle K avoiding e and f can be switched. It changes
  `R100` to `R100 triangle E(K)` and fixes all three marked colours.
* An alpha/gamma cycle K avoiding e and g has the same property.
* Every beta/gamma cycle switch leaves the whole alpha class R100,
  and therefore L_R100 and all its regions, unchanged. This remains
  true whether or not that particular switch preserves all-distinct
  marked colours.

The first two statements are direct edge-colour exchanges. FJ ensures
that the two relevant marks are on one common cycle of the respective
palette, so every other cycle of that palette avoids both marks. They
are available candidates if such other cycles exist, but existence
of a nontrivial candidate in a particular source is not asserted.

There is no missing extra move from switching the common marked cycle
and then globally renaming the two palette colours to restore the
frame: the resulting complete colouring is exactly the one obtained by
switching every other cycle of that palette. At each edge on the marked
cycle the two swaps cancel; every other edge of that palette is swapped
once. This includes the case with no other palette cycle. It makes no
claim of completeness for arbitrary mixed-palette Kempe sequences.

There is a useful exact component-update rule. For either of the first
two moves, write `R'=R triangle E(K)` with R=R100. Then

`E(L_R')=E(L_R) triangle (M intersect E(K))`.       (C3)

Indeed only the common matching edges are deleted in forming L, and
`M intersect R'=(M intersect R) triangle (M intersect E(K))`.
Thus edges of `M intersect R intersect E(K)` are added to L, while edges
of `M intersect (E(K)\R)` are deleted. Other edges are unchanged.

Changing R need not change L: it leaves L identical if K misses M.
If `M intersect (E(K)\R)` is empty, the move only adds L edges, so the
g component cannot shrink. A strict reduction of its cardinality
requires some actual current L edges to be deleted, and requires
checking the complete resulting components after all additions as well.
The deletion condition alone does not prove reduction or separation.

## 7. Exact remaining research obligation and verification scope

Let C_all be the nonempty finite set of actual complete all-distinct
source colourings, normalized at the same e,f,g. With M fixed, a choice
minimizing `|W_g(M,R100(chi))|` over `chi in C_all` exists. Each move in
section 6 that preserves the frame gives another member of this same
set, so a minimizer admits no strict reduction by such a move.

To turn this into a proof, one must show that every blocked minimizer
with `W_C=W_g` admits an actual complete-colouring move or sequence
that still has all three marked colours distinct and makes its final
g region smaller, or directly construct a member satisfying (SEP).
Neither FJ, the local seven-cap relation, nor (C3) supplies that claim.
Minimizing a region is not a substitute for proving an improving move.

The present arbitrary-size results are Theorem C1, the exact forced
obstructions for R001/R010 under complete-region exchange, and the
full-colouring move/update rules. They are paper arguments; no new
finite source-realizability control or Lean theorem is claimed. All 17
root frozen inputs were checked against their sealed byte counts and
SHA256 values in INPUTS.json before writing this note. No authority
bytes were changed; no commit or push was performed.

The residual active-f seven-cap, other odd components, the H-connected
obstruction, `W110+W101>0`, and complete319 remain **OPEN**. The earlier
complete-source reconstruction cost `k+5` is unchanged.
