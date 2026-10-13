# Two-original-piece capacity synchronization

Frozen source: `HEAD 19209f4cf68261fdce5e84a7804cfe04ae0957bf`; the source
documents are preserved in `../frozen/docs/`. This paper uses the complete
original55 N2 contract of those documents: the original induced ordered C5
disk, complete Sigma933/941 (or one common whole-graph transport), T4,
nonboundary-edge criticality, excess two, nonadjacent complete-degree-five
roots r,s, and all other effective original vertices of complete degree four.
Here H is biconnected, there are exactly the original mixed pieces P,Q and no
unary pieces. Both pieces are long in the requested application.

Every assertion keeps the original graph, ordered contacts and shared contact
identities, ownership, actual attachments, rotation, bridges, side branches,
literal frame, empty fibres, and complete original lifts. No source census or
replacement graph is used. The matrix below records necessary obstruction
capacity; it does not replace the original pieces or their full relations.

## 1. Fixed-row notation and two original inputs

Fix one of `i in I={0,1,3}`, with literal boundary rows
`q0=01212`, `q1=01202`, `q3=01021`. Set

`T_r=N_B(r)`, `T_s=N_B(s)`, `t_r=|T_r|`, `t_s=|T_s|`,

`E_r=[4]\q_i(T_r)`, `E_s=[4]\q_i(T_s)`, `A=|E_r|`, `B=|E_s|`.

Each original root has at most two adjacent boundary neighbors, so their
colors are distinct in every proper row. With no unary and no r-s edge,

`A=4-t_r=k_P^r+k_Q^r-1`,

`B=4-t_s=k_P^s+k_Q^s-1`.

Let `F_C(i;a,b)` be the complete original tuple fibre of C at these same
boundary and ordered root pins. Write `A_C(i)` for its nonempty cells. The
exact original common joint is

`J_i=(E_r x E_s) intersect A_P(i) intersect A_Q(i)`.

The adopted conditional-color capacity in B-C2 gives, for every fixed
opposite root pin,

`#{a in [4]: F_C(i;a,b)=empty} <= k_C^r`,

`#{b in [4]: F_C(i;a,b)=empty} <= k_C^s`.

These bounds count original root incidences, not distinct-contact proxies.
They apply to the complete fibres. Indeed, leaving the varied root free
gives strict list slack at its actual contacts; an original full coloring
then supplies a contact tuple whose avoided-color set bounds all forbidden
root colors. Restriction to E cannot increase these bounds.

The second input is the adopted strict-slack fact: if two different actual
external neighbors of an original C vertex receive the same color, the
complete original C fibre is nonempty. All lists have size at least the
original C degrees, one is strict, and reverse tree-order greedy coloring
constructs an original full lift.

## 2. Whole-row acceptance gives a common joint or one incidence

Define actual contact-boundary neighbor sets

`W_C^v={h in B: some original x in C has both vx and xh as original edges}`

and the available collision colors

`X_C^v(i)=q_i(W_C^v) intersect E_v`, for `v=r,s`.

**Theorem S (cross-collision synchronization).** If

`X_P^r(i) != empty and X_Q^s(i) != empty`,

or the exchanged P,Q condition holds, then `J_i != empty` with complete
original lifts.

Choose the r pin from the first displayed set and the s pin from the second.
In each piece the designated contact has repeated external color, so both
pieces have complete lifts at exactly these same pins and this same row.
All spokes are legal because the pins lie in E. The original private vertex
sets are disjoint, so the lifts join directly. This proves the theorem.

**Theorem C (collision plus surplus incidence).** For either original piece
C and either root v, if

`X_C^v(i) != empty and k_C^other >= 2`,

then `J_i != empty` with complete original lifts.

For example choose `a in X_P^r(i)`. P accepts every s pin by strict slack.
The other original piece Q rejects at most `k_Q^s` s colors, whereas
`|E_s|=k_P^s+k_Q^s-1 > k_Q^s`. Hence at least one *same-row* admissible b
accepts Q too. Take complete lifts from these two nonempty original cells.
No different row or independently normalized piece enters this argument.

Consequently, if a designated row were rejected,

`X_C^r(i) != empty => k_C^s=1`,

and symmetrically. In the equality case Q must reject exactly all E_s at the
chosen a and no additional s color: all of its conditional capacity is used.
This is a precise restriction, not a claim that the equality case exists.

For three rejected rows, define the literal signature closure

`Z(T)={h in B: q_i(h) in q_i(T) for every i in I}`.

Then `k_C^other>=2` implies `W_C^v subset Z(T_v)`. Direct evaluation of the
five named boundary signatures gives

| Original root-spoke set T | Z(T) |
| --- | --- |
| empty | empty |
| any singleton {h} | {h} |
| 01 | 01 |
| 12 | 124 |
| 23 | 23 |
| 34 | 34 |
| 40 | 024 |

This table keeps the specified literal three rows. It does not identify
boundary vertices or independently rotate either piece. The two enlarged
closures are genuine limitations of the three-row signatures.

## 3. A bounded interface theorem independent of piece size

For each piece choose a set `S_C(i) subset A_C(i) intersect (E_r x E_s)` of
certified accepting cells. A source-data-only choice is the union of

- all cells whose r color lies in `X_C^r(i)`;
- all cells whose s color lies in `X_C^s(i)`;
- every admissible diagonal cell if C has an original shared contact.

One may strengthen S with actual complete-fibre witnesses. In particular,
adopted Eq/Diff information can supply original `(D,D)` lifts; an actual
partition-preserving color permutation may transport a complete tuple into
another cell of this *same* original piece and common target row. Such a
tuple must be reconstructed before it is treated as a certified cell. The
two pieces are never independently normalized at the final join.

**Theorem M (capacity assignment matrix).** If `J_i=empty`, there exists a
zero-one matrix M with rows indexed by the literal E_r colors and columns
indexed by the literal E_s colors such that

`M(a,b)=0 on S_P(i)`, `M(a,b)=1 on S_Q(i)`,

`k_P^s-1 <= sum_b M(a,b) <= k_P^s` for every a,

`k_P^r-1 <= sum_a M(a,b) <= k_P^r` for every b.

**Proof.** At every grid cell at least one original piece rejects; assign
that cell to one rejecting piece, choosing either if both reject. Put M=1
when it is assigned to P. A P-accepting cell cannot be assigned to P; a
Q-accepting cell must be assigned to P. The number of ones in a row is at
most P's s capacity. The number of zeros is at most Q's s capacity, so the
number of ones is at least

`B-k_Q^s=k_P^s-1`.

The column argument is identical using the r capacities. This assigns a
cell once and therefore handles overlapping rejection sets correctly. QED.

Thus an overlap `S_P intersect S_Q` or infeasibility of M proves an actual
original common joint. The theorem is arbitrary in |P|,|Q| and all internal
block-chain lengths. There are at most sixteen binary cells; this bound is
from the four literal colors, not a cutoff on original graph size.

The converse is deliberately absent. A feasible matrix is only a possible
capacity allocation. It need not agree with the actual forbidden cells,
need not be realized by any graph, and supplies no negative or positive
original full lift. The precise full relations remain the authority for J.

## 4. Small cut certificates without a contact-template classification

Assume `S_P intersect S_Q=empty`. Cells in S_Q are forced ones and those in
S_P forced zeros. Let F be the remaining free cells, and let `m_a` and `n_b`
be the counts of forced ones in row a and column b. Put

`alpha_a=max(0,k_P^s-1-m_a)`, `beta_a=k_P^s-m_a`,

`gamma_b=max(0,k_P^r-1-n_b)`, `delta_b=k_P^r-n_b`.

A negative upper bound makes M impossible immediately. For subsets
`R subset E_r`, `T subset E_s`, every possible M necessarily satisfies

`sum_(a in R) alpha_a <= sum_(b in T) delta_b + |F intersect (R x (E_s\T))|`,

`sum_(b in T) gamma_b <= sum_(a in R) beta_a + |F intersect ((E_r\R) x T)|`.

For the first inequality, the required free ones in rows R either enter
columns T, whose total free-one capacity is at most the delta sum, or use
one of the displayed remaining cells. The second inequality counts the
required free ones in columns T in the other direction. These are direct
counting inequalities. No claim of their joint sufficiency is needed here,
and no additional external flow theorem is assumed.

One violated inequality, together with its literal row/column sets and
certified S cells, is therefore a compact same-row full-joint certificate.
It includes the cross-collision and single-row surplus arguments as simple
special obstructions. One can alternatively check all at most `2^16`
matrices, retaining the original data and complete witnesses for S.

## 5. An explicit remaining joint subproposition

**LL-CUT (OPEN).** Take one complete original N2-55 double-long source with
the frozen full hypotheses, including complete Sigma, T4, criticality,
original degree profile, actual shield geometry and every original
attachment, restricted to the residual after the independently proved T0
and T1 exclusions. The remaining root-spoke profiles and grid sizes, up to
exchanging the original roots together with all their data, are exactly:

| Actual support sizes | Total spokes t | Root-spoke profile | Admissible grid size |
| --- | --- | --- | --- |
| {3,3} | 2 | (2,0) | 2 by 4: eight cells |
| {3,3} | 2 | (1,1) | 3 by 3: nine cells |
| {3,3} | 3 | (2,1) | 2 by 3: six cells |
| {3,4} | 2 | (1,1) | 3 by 3: nine cells |

At least one original long still has at least four root incidences. For
each designated row build the source-data-only S of Section 3. At least
one designated row has overlapping certified cells or an infeasible
assignment matrix M of Theorem M.

This is a concrete sufficient source proposition, not a restatement of
nonempty J: it mentions only original contact-boundary incidences, root
spokes, shared-contact identities, root incidence counts, and a grid with
at most nine binary entries in this residual. Thus at most 512 assignments
are checked per designated row, with no bound on original graph size.
Theorem M retains its general sixteen-cell statement. Optional actual
Eq/Diff diagonal lifts give a separately identified strengthened version
`LL-CUT+diag`. They must not
be silently substituted when testing the source-data-only version.

Theorem M proves that either version would close the full double-long
branch. A counterexample to this stronger route would require a single
qualified original source together with one feasible matrix in each of the
three literal rows. Complete source qualification, full relations, empty
fibres and original full lifts must accompany such a claimed source
counterexample. Three matrices attached to three different graphs would
not refute the proposition. Feasible matrices in a relaxed local control
only show that the weakened local premises do not force this certificate;
they neither refute full-source LL-CUT nor establish actual rejection.

## 6. Independent review of the zero/one-spoke theorems and current scope

The separate [structure proof](../review/structure.md), Sections 2-4, has
been independently checked here. Its leaf-contact argument includes the
single-block bridge/cycle cases and correctly excludes a singleton when
there is no shared contact. A private nonshared root-contact has an actual
boundary neighbor by original complete degree four. The proof uses this
fact only under the adopted full-source leaf-contact theorem.

For t=0, all four root colors are admissible. A shared-contact piece accepts
every diagonal; the other piece either has shared contact too, or its
boundary-bearing contact supplies an accepting diagonal at the very same
literal boundary color. If neither piece has shared contact, choose one
boundary-bearing contact in each. Opposite owners give Theorem S. Equal
owners give Theorem C for at least one piece because the other root's two
incidence counts sum to five. Thus every fixed designated row has a common
joint. This proves the t=0 source exclusion without any size bound and
without joining witnesses from different rows.

The subsequently completed structure proof, Sections 5-7, has also been
independently checked here. In its common-boundary-contact minor, the bags
`{h}`, `H-C`, `{p}`, `{z}`, `(C-{p,z}) union (B-{h})` are disjoint and
connected. Deleting two adjacent private cycle vertices leaves C connected;
its outside-h attachment remains because p,z each attach only at h. The
other long piece supplies the remaining second-fifth adjacency, and the
root spoke supplies first-second. This verifies every original adjacency.

For the hidden-contact lemma HD, an ordinary private cycle vertex's list
contains D and a private contact's list excludes D. They cannot both equal
the same rejecting block palette. Thus a failed diagonal forces adjacent
private contacts at h, to which the minor applies. The single-block bridge
and cycle cases and the multiblock leaf cases are all covered; arbitrary
cycle length or block-chain length does not leave an omitted case.

For t=1, the signature consequences and shared-contact argument use all
three rows only to constrain original attachments; every final lift stays
in one selected row. The r-incidence splits `(2,2)` and `(1,3)` exhaust the
sum four. Each low-contact existence row is paired with HD acceptance in
all three designated rows. In the remaining `(1,3)` case the forbidden
cell union has size at most `4+3*2=10<12`, so its same-row joint follows
directly. This independently verifies T1 as an arbitrary-size source
exclusion, in addition to T0.

The original two-long geometry together with T0/T1 now leaves only support
sizes {3,3}, with `2<=t<=3`, or {3,4}, with `t=2`. At least one long still
has four or more original root incidences. These remaining cases and
LL-CUT are not proved here. The old four-contact all-diagonal-failure path
blocks a local diagonal-only extension; it does not refute the joint
theorems, which use the other original piece and simultaneous capacities.

The evidence level is paper proof using already adopted source inputs.
Finite controls can check the literal matrix, capacity arithmetic and full
joins; they do not discharge arbitrary-size source qualification. This
paper does not introduce a Lean theorem, new source enumeration, a source
counterexample, commit, or push. The full N2 original55 double-long branch
and E-ARC2 remain OPEN beyond the scoped t=0 and t=1 exclusions.

## 7. Independent matrix implementation review

The separate `../joint/matrix.py` implementation was read against Sections
3-4. Its safe-Q cells are correctly forced to one, safe-P cells to zero;
row bounds use s incidences and column bounds use r incidences. It enumerates
every assignment to the remaining cells without dropping forced cells.
Residual lower and upper counts subtract the actual forced-one counts.
Both cut formulas have the correct complement direction. A negative upper
bound is reported as an immediate obstruction, and the implementation
asserts that a found cut cannot coexist with an explicitly feasible matrix.
No mathematical implementation defect was found in this review. Runtime
calibration and source-qualified target coverage remain separate evidence
recorded by the parent checker, not claims supplied by this read-through.
