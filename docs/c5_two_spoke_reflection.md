# Two-spoke (2,1): q-preserving reflection and the remaining adjacent orbit

後續（2026-09-24）：[split-support 完整列分類](c5_two_spoke_split_support.md)
已完成 §4–5 的任意大小單缺失問題：兩種接點次序均有精確全列 F／Z 公式；
S={b4,b0} 僅由本頁形式化反射搬運。下文停止點保留當輪語境。

2026-09-24. Dependencies: the [necessary sector table](c5_degree5_two_spoke_sectors.md),
[R10 interfaces](c5_degree5_interfaces.md), the established
[adjacent exclusion](c5_two_spoke_adjacent_21.md) and
[middle exclusion](c5_two_spoke_middle_21.md). Priority: [HANDOFF](HANDOFF.md).

**Results.** Reflection discharges both S={b2,b3} entries from S={b0,b1}.
Six of the original 18 (2,1) entries are now excluded; 12 remain: four in
S={b3,b4}/{b4,b0} and eight nonadjacent entries. The next adjacent orbit
has an exact necessary boundary-support separation, stated in §3. It has
existing disk realizations in one forbidden-color order, so a blanket
exclusion would be false. General single-missing-pattern separation is
not proved by these realizations.

## 1. Same-source transport, including the full relations

Use the source hypotheses of the sector table: finite simple induced-C5
disk graph, ordered boundary B=(b0,...,b4), q=01012, connected minimal
q-obstruction H, unique complete degree-five vertex z with two boundary
neighbors S, other interior degrees four, and T4 acceptance. H−z consists
of C₂ and C₁, with their original ordered contacts (s,t) and (r). The
reflection itself does not require degree bounds or minimality.

Define, with indices modulo 5,

```
ρ(i)=3−i:          (0,1,2,3,4) ↦ (3,2,1,0,4),
π=(0 1):          (0,1,2,3)   ↦ (1,0,2,3),
(Tb)_i = π(b_ρ(i)).
```

Both maps are involutions, T²=id, and Tq=q. The only elements of D5×S4
fixing this labeled q are the identity and (ρ,π): the unique occurrence
of color 2 fixes position 4, leaving only identity/reflection in D5;
the color map on the three used colors is then forced and fixes 3.
The checker verifies this small stabilizer directly.

Keep the same interior vertices, internal edges, component identities,
contact ordering and all intermediate bridges. Replace each actual
attachment v–b_i by v–b_ρ(i), including z's spokes. Reflect the disk
embedding, reversing its orientation and every rotation; the new boundary
has the same named cyclic order. This is an isomorphic reflected source,
not a minor or an identification of boundary vertices. Components do not
exchange their two/one contact roles.

For each component C, let A(v) be its actual boundary neighbors as an
index set, L_b(v)=U\b(A(v)), and R_C(b) its complete ordered contact
relation. A single whole-component coloring f maps to π∘f. Consequently,

```
L*_(Tb)(v) = π(L_b(v)),
R*_C(Tb)  = {π∘t : t∈R_C(b)},
F*_C(Tb)  = π(F_C(b)),
Z_G*(Tb)  = π(Z_G(b)).                                  (1)
```

The last identity follows from the unchanged exact join
Z_G(b)=(U\b(S))\(F_C₂(b)∪F_C₁(b)). Equation (1) holds on every labeled
row and at every z query, including queries excluded by the spokes when
considered componentwise. In particular the residual lists at z=a map
to those at z=π(a), at the same named contacts. No product of marginal
endpoint lists occurs.

The same graph isomorphism and color bijection transport every nonboundary
edge-deletion coloring to deletion of its corresponding edge. They
preserve q-rejection, minimality, T4 acceptance, inducedness, all complete
degrees, connectedness and disk realizability. These are paper consequences
of the explicit isomorphism; no new topology axiom is introduced in Lean.

The ordinary Lean proofs in [TwoSpokeReflection.lean](../Math/TwoSpokeReflection.lean)
formalize `rho_cycle`, `reflectRow_q`, `reflectRow_involutive`,
`boundaryLists_transport`, `listProper_transport`, `contactRelation_transport`,
`forbidden_transport`, `q_contactRelation`, `q_forbidden`, and
`adjacent_orbits`. The generic relation lemmas apply separately with
P=Fin 2 and P=Unit to the same color permutation. They also apply to an
edge-deleted component graph without changing the transport proof.
[The axiom audit](../Math/TwoSpokeReflectionAudit.lean) records their trust
boundary. The disk/K5 paper theorems are not Lean theorems.

## 2. Discharging the reflected entries

| Source spokes | Reflected spokes | Forbidden orders (C₂,C₁) |
| --- | --- | --- |
| {b0,b1} | {b2,b3} | ({2},{3}) and ({3},{2}) are each preserved |
| {b1,b2} | {b1,b2} | both orders preserved; already excluded |
| {b3,b4} | {b4,b0} | ({0},{3}) ↔ ({1},{3}); ({3},{0}) ↔ ({3},{1}) |

If either reflected {b2,b3} core existed, its reflected source would satisfy
all hypotheses of the established {b0,b1} exclusion, with exactly the
same order. This is a contradiction. There is no new K5 case to prove;
the prior proof is used once on the transported source. The middle orbit
remains closed. The original 80-record necessary-position artifact is
preserved; the new artifact records the involutive mapping of all 18
retained (2,1) entries and the cumulative status separately.

## 3. Necessary support separation in the next orbit

Work first with S={b3,b4}. Let A forbid 0 and D forbid 3. Either component
can own either role; this notation never merges C₂ and C₁. Both lie in
Γ=(z,b3,b2,b1,b0,b4). Write B(C)=∪_{v∈C}N_B(v).

**Support theorem, for arbitrary source size:**

```
B(A)={b1,b2,b3},             B(D)={b0,b1,b4}.             (2)
```

Reflection gives for S={b4,b0}, with A forbidding 1 and D forbidding 3,

```
B(A)={b0,b1,b2},             B(D)={b2,b3,b4}.             (3)
```

These are sets of actual attachments, not permission to attach every
vertex to every listed boundary point. The two components can both touch
the shared boundary endpoint b1 in (2), or b2 in (3).

Here is the proof of (2), reusing the existing minor extraction. Color
stabilizers force A to meet at least one of b0,b2, and D to meet every
boundary color, hence b4, at least one of b0,b2, and at least one of b1,b3.
Order the boundary line opposite z as b3,b2,b1,b0,b4. Let d be D's
leftmost attachment. A simple path through D from d to b4 is a crosscut.
The open boundary interval between them is separated from z, so no A
attachment lies strictly in that interval: A is connected and has its own
z contact, disjoint from D. Thus A's attachments lie at or to the left of
d, with b4 the only possible exception. A must have a color-0 attachment
x≠b4 on the left. If A also touched b4, a path through A from x to b4
would cut off a D attachment strictly between x and b4: D has at least
three distinct attachments, so at least one is neither d nor b4. This
contradicts D's own z contact. Hence every A attachment precedes or equals
every D attachment. Sharing the endpoint d is allowed.

If D touches b2, A is confined to {b3,b2}. At z=0 the actual exterior
colors of A are only 0 and 1. The established two-color argument in
[adjacent exclusion §3–5](c5_two_spoke_adjacent_21.md#3-same-source-palettes-of-a-at-z2)
applies with palettes {2,3}: a cycle's actual tethers reach two disjoint
connected exterior sets, X0=V(Q_D(z,b2)) and X1={b3}. They are adjacent
by zb3 (also b2b3). This is precisely the existing two-hub K5 extraction
with renamed colors and terminals. Thus D cannot touch b2.

D must now touch b0 and a color-1 point. It cannot touch b3, because that
would confine A to {b3}, contradicting A's color-0 support. Hence
B(D)={b0,b1,b4}, and b2∈B(A)⊆{b3,b2,b1}.

If A omits b3 or b1, reuse the same two-hub extraction with the following
actual exterior sets. In both cases all exterior color-0 neighbors of A
(z or b2) belong to X0, and all exterior color-1 neighbors belong to X1.

| A support is contained in | X0 | X1 | An edge X0–X1 |
| --- | --- | --- | --- |
| {b1,b2} | path z–b3–b2 | {b1} | b2b1 |
| {b2,b3} | Q_D(z,b0) followed by b0–b1–b2 | {b3} | zb3 |

The sets are connected, disjoint from A and from each other. Additional
vertices in a branch set need not carry its color; it is a minor set,
not a coloring replacement. The same palette/tether lemma excludes these
supports, proving both remaining attachments in (2). This includes the
case B(A)={b2}. We do not reopen or enumerate the old K5 cases.

The [checker](../scripts/c5_two_spoke_reflection.py) verifies the eight
support pairs surviving the stabilizer and interval tests, and the
set/path conditions identifying the stated extraction cases. The
crosscut and arbitrary-size tether arguments remain paper proofs.

## 4. Exact interface and structural stopping point

For S={b3,b4}, the two possibilities are still

| Order | C₂ | C₁ |
| --- | --- | --- |
| I | A, F={0}, support {b1,b2,b3} | D, F={3}, support {b0,b1,b4} |
| II | D, F={3}, support {b0,b1,b4} | A, F={0}, support {b1,b2,b3} |

At z=0, every residual list of A contains 2 and 3. The existing paired
palette argument therefore gives vertex-disjoint odd cycles with palette
{2,3}, covering all vertices of A, connected by actual bridges with
palettes {0} or {1}; K4 blocks are already excluded by the connected-exterior
lemma. Each cycle vertex has one 0 direction and one 1 direction. Actual
0-tethers terminate at z or b2; 1-tethers terminate at b1 or b3. All
contacts and bridges stay in their source positions. A need not be a
single triangle, and this does not bound cycle count or arm length.
Unlike the excluded cases, the two boundary color-1 terminals cannot
simply be identified as one exterior vertex.

At the one forbidden query z=3 on D, use only its own tight block lists
with actual boundary support {b0,b1,b4}. If D=C₁, its complete root set
is {3}. If D=C₂, retain R₂(q)⊆U²: every tuple contains 3, each other
hub color is avoided by some whole tuple, and releasing either contact
edge supplies tuples (3,y) and (x,3), x,y≠3. These may be different
colorings. The analogous statement with 0 applies when A=C₂. A's other
queries are colorable, not a second uncolorable palette decomposition.

For any proper labeled row b, (2) gives the exact partial transport laws

```
b1=b3  ⇒ F_A(b)={b2},
|{b0,b1,b4}|=3 ⇒ F_D(b)=U\{b0,b1,b4},
Z_G(b)=(U\{b3,b4})\(F_A(b)∪F_D(b)).                    (4)
```

Each implication uses one permutation on all actual attachments of that
component, applied to its full relation. Outside the stated conditions,
(4) leaves the component relation unknown; it is not an all-row
classification. The formulas reflect to (3) via (1).

## 5. Existing disk controls, evidence, and next obligation

R10 already stores eight witnesses in this orbit: source indices
12–15 have S={b3,b4}, and 32–35 have S={b4,b0}. All have order I, a
three-vertex C₂ triangle and a one-vertex C₁. No new graph search is used.
The [artifact](../artifacts/c5_two_spoke_reflection/observations.json) binds
the existing sources by SHA256 and independently checks:

- induced C5, complete degrees, two/one contact partition and exact supports;
- the stored apex rotation and its reflected rotation, all darts and Euler
  characteristic 2, supplying the existing disk witness;
- all 240 labeled rows per graph, full C₂/C₁ tuples, reflected tuples,
  forbidden sets, and direct whole-graph z colors (1,920 graph rows and
  3,840 reflected component rows);
- 120 explicit q-colorings after deleting each nonboundary edge.

Every one of these graphs rejects exactly the 24 color relabelings of q
and accepts all other proper rows, including T4. Thus order I is realized
at both spoke positions, but none of these controls is a double-missing
counterexample. They do not prove all order-I cores have that relation;
order II has no realization or exclusion established here. Finite
controls are not a replacement for arbitrary-source separation.

The next narrow problem is the split-support pair in (2), with its two
contact orders and the common color frame: determine its full-row
behavior, especially whether every T4-accepting minimal core has only q
missing, or retain an actual second-missing witness. The reflected pair
(3) needs no independent analysis. Eight nonadjacent entries, t≤1,
general core separation, common exits and K∞=K≤5 remain open. The (3),
S={b0,b1}, S={b1,b2} and now S={b2,b3} exclusions stay closed; 603 profiles
and fixed-point artifacts are unchanged.

Trust: ordinary Lean transport lemmas; paper disk/crosscut and
support/minor deductions using the established external degree-list
characterization; Python finite transport and existing disk controls.
The support theorem and inherited K5 exclusion are not formalized in Lean.

```bash
python3 scripts/c5_two_spoke_reflection.py --check
python3 scripts/c5_two_spoke_adjacent_21.py --check
python3 scripts/c5_two_spoke_middle_21.py --check
python3 scripts/c5_degree5_two_spoke_sectors.py --check
lake build
lake env lean Math/TwoSpokeReflectionAudit.lean
python3 scripts/check_docs.py
git diff --check
```

Actual validation is recorded in the [research record](history/2026-09-24-two-spoke-reflection.md).
