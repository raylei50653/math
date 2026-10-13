# Independent topology and no-spoke joint proof

Frozen source: `HEAD 19209f4cf68261fdce5e84a7804cfe04ae0957bf`; inputs are
the copies in `../frozen/docs/`. This note uses the full original55 N2 contract,
including complete Sigma, all nonboundary edges critical, the original two
nonadjacent degree-five roots, and the adopted original cactus/leaf facts.
Nothing here enumerates sources or replaces a piece by another graph.

## 1. Shield geometry in the double-long case

Both original mixed pieces are one-sided and long. Their shield arcs are
edge-disjoint and each has at least two edges. Thus their arc-length multiset is
`{2,2}` or `{2,3}`; the corresponding actual support sizes are `{3,3}` or `{3,4}`.
The exact support equality uses full B-touch and the adopted shield interval
lemma, not just the lower bound on support.

For lengths `{2,3}`, the arcs exhaust the boundary edges. Every root spoke must
avoid each shield's interior, so its endpoint is one of the two common arc
endpoints. These two endpoints are nonadjacent on the original C5. Since one
root's boundary neighbors lie in one boundary edge, each root has at most one
spoke. Hence `t <= 2`.

For lengths `{2,2}`, the spokes can end only at the three shield endpoints.
Exactly one pair among them is adjacent: the endpoints of the single unused
boundary edge. If both roots had two spokes, both would use that same pair.
The adopted same-boundary-edge root-spoke K5 lemma applies: either long has an
actual boundary attachment outside the pair, and the other mixed piece supplies
the disjoint root-to-root path. Therefore `t <= 3`.

These are arbitrary-size source restrictions. They do not by themselves force
a joint or classify the full relations.

## 2. Every non-shared mixed piece has a boundary-bearing contact

For an original mixed piece C, define

`W_C^z = {b in B: some original v in C is adjacent to both z and b}`

for `z in {r,s}`. These are actual original attachments, not counts or abstract
support assignments.

**Lemma L.** If C has no shared contact, then `W_C^r union W_C^s` is nonempty.

**Proof.** A singleton mixed piece necessarily has its only vertex adjacent to
both roots, and hence is excluded by the no-shared hypothesis. The adopted
original-block theorem leaves only bridges and odd cycles. If C has multiple
blocks, choose a private root-contact in a leaf block, whose existence is an
adopted full-source fact. Its degree inside C is one for a bridge and two for an
odd cycle. With no shared contact it has exactly one root edge. Since its
original full degree is four, it has respectively two or one original boundary
neighbors. If C has a single bridge/odd-cycle block, take any root-contact
(there is one since C is mixed); its degree inside C is again at most two, and
the same degree argument applies. Thus an actual contact-boundary edge exists.
No statement is made about arbitrary local gadgets without the adopted
leaf-contact theorem. QED.

## 3. A fixed-row capacity consequence

Here is the precise existing capacity input used below. For either root order,
every fixed admissible color `a` at r, and either mixed piece Q,

`#{b: F_Q(q_i; a,b) is empty} <= k_Q^s`.

It is the individual conditional-color bound used in B-C2, with actual s
incidences, not the number of distinct contacts. It applies to the complete
original fibre and includes empty cells. In the no-spoke case all four root
colors are admissible and `k_P^s + k_Q^s = 5`.

If `W_P^r` is nonempty, choose `a = q_i(b0)` for an original
`b0 in W_P^r`. At the contact adjacent to r and b0 those two external neighbors
have the same color. Strict degree-list slack therefore gives a complete
original P lift for **every** s pin b. If `k_P^s >= 2`, then `k_Q^s <= 3` and the
capacity bound leaves at least one b for which Q also has a complete lift.
The same `q_i,a,b` then gives a full original joint. Consequently, a rejected
row in the no-spoke case must satisfy

`W_C^r != empty => k_C^s = 1`,

and the exchanged-root version. This uses only one fixed row at a time.

## 4. No-spoke common joint theorem

**Theorem T0.** Under the full original55 N2 contract with exactly two mixed
pieces and no unary pieces, `t=0` is impossible. More concretely, at every
designated row q_i, the existing structural/capacity hypotheses give common
ordered pins and complete lifts of both original mixed pieces.

**Proof.** Fix a single designated original row q_i. There are no root spokes,
no root-root edge, and no unary factor, so every ordered pair in `[4]^2` meets
all external constraints.

First suppose P has a shared contact. P then accepts every diagonal `(a,a)` by
strict slack. If Q also has a shared contact, any such pair works. Otherwise
Lemma L provides a boundary-bearing contact of Q. Take a to be the q_i color
of its actual boundary neighbor. Equal root pins `(a,a)` make that Q contact
have repeated external color too; thus both full original fibres are nonempty
at exactly the same row and pins. This proves a common joint in this case.

It remains that neither piece has a shared contact. Choose, for each C, one
root z_C for which `W_C^{z_C}` is nonempty, using Lemma L. If `z_P != z_Q`,
choose each root pin to equal the boundary color of the chosen actual contact
in its own piece. Each original piece then has strict slack; both full lifts
exist at these same ordered pins. If instead `z_P = z_Q = r`, either
`k_P^s >= 2` or `k_Q^s >= 2`, since their sum is five. The fixed-row consequence
in Section 3 supplies a common joint. The case `z_P = z_Q = s` is symmetric.

Each resulting joint fixes the original full boundary q_i and the same ordered
root pins for both pieces. Their remaining original vertex sets are disjoint;
their complete lifts, together with those pins and q_i, cover every original
edge. Thus q_i extends to G, contrary to its designated rejection. QED.

This theorem does not use the long support sizes and thus is valid for the
larger adopted two-mixed, no-unary, no-spoke original55 contract. The present
task needs only its double-long subcase. It does not use a different row's
coloring, an independently normalized frame, or any marginal relation.

## 5. A common-boundary-contact K5 minor

**Lemma H.** Suppose C and C' are the two original long mixed pieces, some
root has an original spoke to h in B, and p,z are adjacent private vertices
of a leaf odd-cycle block of C (or adjacent vertices of its only cycle block).
Suppose p,z have no shared contact and each is a root-contact with its actual
boundary neighbor h. Then the original graph has a K5 minor.

The five branch sets, with all names referring to original vertices, are

1. `{h}`;
2. `H - C`;
3. `{p}`;
4. `{z}`;
5. `(C - {p,z}) union (B - {h})`.

They are disjoint. The second is connected because it consists of r,s and the
other original mixed piece C'. The fifth is connected: deleting two adjacent
private cycle vertices leaves C connected, and C long has a boundary attachment
outside h; p,z have only h as boundary neighbor, so such an attachment remains.
The spoke gives the first-second adjacency. The contacts and h attachments
give every adjacency from p,z to the first two sets; pz is an original edge.
Their other cycle edges give their adjacencies to the fifth set. Boundary edges
at h give first-fifth adjacency. Finally C' is long and hence touches B-h,
giving second-fifth adjacency. All ten pair adjacencies are witnessed by
original edges. The owners of p,z may be the same or different roots.

This is a minor obstruction only; no Sigma claim is made for the minor.

## 6. Hidden contacts force full diagonal acceptance

**Lemma HD.** In the same double-long source with a root spoke at h, let C have
no shared contact and `W_C^r union W_C^s` be contained in `{h}`. For every
designated row q_i, C accepts `(D,D)` with a complete original lift.

**Proof.** Suppose the full diagonal fibre is empty. All degree lists are
tight and have the adopted incident block-palette representation. C cannot be
a singleton because it is mixed without shared contact. A leaf bridge contact
would have two distinct boundary neighbors, contrary to the W restriction.
For a leaf odd-cycle block, there is a private root-contact. Its private list
excludes D, whereas an ordinary private vertex has only boundary external
neighbors and hence its list contains D. Every private vertex's list equals
the same odd-cycle palette, so no ordinary private vertex is possible. Thus
all private vertices are root-contacts. There are at least two, adjacent along
the private part of the cycle, and each has its one actual boundary neighbor h.
Lemma H gives a K5 minor, a contradiction. The same list comparison applies to
a single cycle block, where every vertex is private; a single bridge was already
excluded, and other single blocks are excluded by the adopted cactus theorem.
Thus the original full fibre is nonempty. QED.

The conclusion uses the entire original C and is independent of its size or
root-incidence count. It is not a claim that every row or every pin is accepted.

## 7. Exactly one spoke is impossible for two long pieces

**Theorem T1.** The complete original55 double-long source cannot have `t=1`.

Name the root with the unique spoke r and its boundary neighbor h; s has no
spokes. Their mixed incidence totals are respectively four and five. In every
designated row, the admissible root sets have sizes `|E_r|=3`, `|E_s|=4`.

The elementary conditional capacity/slack consequence used below is:

`k_C^s >= 2 => W_C^r subset {h}` and
`k_C^r >= 2 => W_C^s = empty`

under the assumed rejection of all three designated rows. For the second
implication, any boundary-bearing s contact produces strict slack at an
admissible s color; the other piece then forbids fewer r colors than are
available. For the first implication, any boundary-bearing r contact whose
boundary color differs from q_i(h) similarly yields a joint by capacity in the
s direction. Therefore every b in W_C^r satisfies `q_i(b)=q_i(h)` in all three
rows. The actual three-row signatures at boundary positions 0,1,2,3,4 are
`000,111,220,102,221`, respectively, and are pairwise distinct. Hence b=h.
This is a comparison on the same original boundary, with no rowwise relabeling.

First suppose one piece P has a shared contact. If Q also does, `(D,D)` works
immediately. Otherwise, any b in `W_Q^r union W_Q^s` whose color differs from
q_i(h) provides a legal diagonal pin `a=q_i(b)`: P accepts it by shared slack,
and Q accepts it by contact-boundary slack. Therefore rejection in all three
rows forces `W_Q^r union W_Q^s subset {h}`, by the distinct signatures above.
Lemma HD makes Q accept `(D,D)` in every designated row, and P does too. The
same-row full join contradicts rejection.

Now suppose neither piece has a shared contact. If a piece has at least two
incidences at each root, the two capacity consequences put all its
boundary-bearing contacts at h. Lemma HD therefore makes that piece accept
`(D,D)` in every designated row.

The possible r-incidence splits, up to exchanging P,Q, are `(2,2)` and `(1,3)`.

- For `(2,2)`, if both s counts are at least two, both pieces satisfy Lemma HD
  and there is an immediate diagonal joint. If one s count is one, that piece
  has total incidence three, and the other has at least two incidences at each
  root. The already adopted arbitrary-size low-contact long escape gives one
  designated row where the first piece accepts `(D,D)`; the second accepts
  this same row by HD.
- For `(1,3)`, name the pieces P,Q accordingly. If `k_Q^s >= 3`, then Q has at
  least two incidences at each root and accepts all three designated diagonal
  cells; `k_P^s <= 2`, so P has total incidence at most three and the same
  adopted low-contact escape supplies a common row. If `k_Q^s <= 2`, use the
  complete forbidden pin cells inside the same `E_r x E_s`. P has at most one
  forbidden r color for each fixed s, so it has at most four forbidden cells.
  Q has at most `k_Q^s` forbidden s colors for each fixed r, so it has at most
  `3 k_Q^s <= 6` forbidden cells. Their union has at most ten cells, less than
  the twelve admissible ordered pin cells. A surviving same-row pair has both
  complete original fibres nonempty and hence gives a full joint.

All cases keep the original row, ordered pins, complete piece tuples, and
external spoke. The low-contact existence row is used only against another
piece known to accept every designated diagonal row. No two independent
existence rows are combined. QED.

## 8. Residual boundary

Sections 1, 4, and 7 leave the double-long source only with

- support sizes `{3,3}` and `2 <= t <= 3`; or
- support sizes `{3,4}` and `t = 2`.

The other adopted restriction, at least one original long with four or more
root incidences, remains in force. A full arbitrary-size joint theorem for
these remaining positive-spoke cases has not been proved in this note. Existing local
four-contact diagonal failures are not counterexamples to Theorem T0: it uses
the second original piece and the simultaneous degree-five capacities.

This is a paper argument using adopted external degree-list/capacity results.
It is separate from finite calibration and is not a Lean theorem. A full target
source has not been exhibited or searched for here; target controls remain
`not triggered`.
