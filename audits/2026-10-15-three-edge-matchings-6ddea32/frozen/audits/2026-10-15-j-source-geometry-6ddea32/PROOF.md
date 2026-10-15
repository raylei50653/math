# Original source geometry of J and its exact two-star interface

BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`.
[INPUTS.json](INPUTS.json) freezes the original source proofs, the round-three
return criterion, and the round-four custody manifest. All preceding audits
are read-only. The main results below are arbitrary-size consequences of the
original source, not inferences from finite patch controls.

## 1. Contract and new conclusions

Let G be the same globally minimum noncatalogue C5 source with original boundary
`(x,y,a,b,c)`, secondary maximum-edge choice, and

`d_G(x)=d_G(y)=d_G(b)=4`, `d_G(r)=6`.

The original edge apexes are `(r,t,p,q,s)`, in that order. Write
`a0=d_G(a)`, `c0=d_G(c)`, and `h=a0+c0-8>=3`. The frozen transfer proves
`d_G(s),d_G(t)>=6`. The original r rotation is `(x,y,t,w,v,s)`.
Use the already constructed `U=R-r`, with induced boundary `(z,s,v,w,t)`,
and the legal sphere triangulation `J=U/(s=t)`, with `m=[s=t]`.
Its two marked faces are `mvw` and `zpq`; the edge `mz` is retained.

The new source consequences are:

1. J has **no separating triangle**, hence is a four-connected sphere
   triangulation. This improves the previously known simple-triangulation
   identity without assuming general planar colourability.
2. Every induced C4 of J meets `{m,z}`; every induced C5 avoiding these
   two vertices has a side consisting of one complete degree-five W5 centre.
3. The original rotations give two induced link cycles with exact arc lengths.
   Their two-star union is a disk. Deleting m,z leaves an actual triangulated
   disk W with a simple boundary of length at least nine.
4. Every complete W colouring has an explicit **complete** J-lift set.
   The original all-r condition is imposed on every member of that set,
   including the obligation to retain empty lift fibres.

These statements do not prove that a source colouring violates the return
criterion. The all-size319 exclusion remains OPEN.

## 2. Exact degrees and the two original fan arcs

No extra common neighbour is silently suppressed. The frozen common-neighbour
formula is `N_U(s) intersect N_U(t)={z}`. The sole duplicate pair in forming
J is `sz,tz`; all other incidences survive separately. Thus:

| Vertex in J | Exact original degree expression | Lower bound |
| --- | --- | ---: |
| m | `d_G(s)+d_G(t)-5` | 7 |
| z | `a0+c0-5=h+3` | 6 |
| v,w | `d_G(v)-1`, `d_G(w)-1` | 4 |
| p,q | `d_G(p)-1`, `d_G(q)-1` | 4 |
| every other vertex | its original G degree | 5 |

In particular only `v,w,p,q` can have J degree four. The formulas for v,w use
the original collar fact that neither contacts B; the formulas for p,q retain
their distinct original a/b and b/c contacts. There is no assumption that all
four of these degrees are five.

Let alpha be the first original inner neighbour after t in a's fan toward p;
let beta be the first original inner neighbour after s in c's fan toward q.
The endpoint identifications are literal:

`alpha=p iff a0=4`, `beta=q iff c0=4`.

Otherwise alpha/beta are the actual original intermediate fan vertices, not
fresh arbitrary vertices. All a-fan and c-fan vertices are distinct: an original
inner vertex cannot contact nonadjacent original boundary vertices a,c.

The original faces `a t alpha` and `c s beta` become exactly the two faces
`mz alpha` and `mz beta` on edge mz. The path in `link_J(z)` from m to p
along the a fan has length `a0-3`; the path from q to m along the c fan has
length `c0-3`. Together with the edge pq these give total length `h+3`.

Similarly, `link_J(m)` consists of the original s-neighbour path from z to v,
the edge vw, and the original t-neighbour path from w to z. The two path
lengths are respectively `d_G(s)-3>=3` and `d_G(t)-3>=3`. They have no
common internal vertex because s,t have only the one common U neighbour z.
These exact arc lengths are source information absent from the preceding
twelve-vertex plane control.

## 3. Every triangle of J is a face

Every triangle of U is a triangle of the four-connected original T0, and
therefore is an actual face. The s=t quotient preserves each of those
triangular faces, including the two distinct faces just identified at mz.

A triangle of J avoiding m is one of these old faces. A triangle `m z j`
also comes from an old `s z j` or `t z j` triangle: j is adjacent to at
least one of s,t, and z is adjacent to both. It too is an old face. A
triangle `m A B` with A,B different from z is an old face if A,B were
both adjacent to s, or both adjacent to t. Because s,t have no common
neighbour other than z, the only remaining possibility is a crossed edge

`sA, AB, Bt in E(G)`, with `A,B != z`.

All five vertices `(r,s,A,B,t)` are distinct original G inner vertices.
In particular A cannot be w and B cannot be v, since sw and tv are
forbidden original edges; neither is r since U deleted r.

Consider the actual original proper C5

`C=(r,s,A,B,t)`.

At r, its rs/rt rays separate the rotation into the sector containing x,y
and the sector containing v,w. The x,y sector is outside the bounded disk
of C: x and y lie on the original outer boundary, are not on C, and their
incident edges cannot enter that disk without crossing C. Consequently
every one of v,w not on C lies strictly in its bounded disk. This is the
actual source rotation, not a free choice of which side is bounded.

The frozen small-cap theorem says that the bounded disk of every original
proper C5 is empty or consists of one W5 centre, adjacent to all five
boundary vertices. There are four cases:

| A=v | B=w | Consequence |
| --- | --- | --- |
| no | no | v,w are both strictly inside C, impossible |
| yes | no | w is inside; the W5 conclusion forces ws, an original nonedge |
| no | yes | v is inside; the W5 conclusion forces vt, an original nonedge |
| yes | yes | the crossed edge is exactly vw |

The last case gives the already specified face mvw. Thus no other crossed
edge can create a new triangle. Every J triangle is facial. For a simple
sphere triangulation of order at least five, a three-vertex separator
must bound a triangle (the incident triangular faces around any separated
component close its three-vertex boundary). Conversely a nonfacial
triangle separates. J is already three-connected as a simple sphere
triangulation, so the absence of such a triangle proves four-connectivity.

One exact new original-edge identity is therefore

`E_U(N_U(s)\{z}, N_U(t)\{z}) = {vw}`.

The two sets are disjoint by the old common-neighbour formula. The identity
counts the single undirected edge vw once; no independent fan relabelling
or chosen colouring is involved.

## 4. Short separators are confined to the two distinguished vertices

Let C be a J cycle of length four or five avoiding m,z. Its vertices and
edges lift literally to original G inner vertices and edges. The original
bounded cap is therefore empty for a C4, and empty or one W5 centre for a
C5. No removed vertex can be that centre: r,s,t have complete original
degree at least six, whereas a W5 centre has complete degree five. The
other removed/split vertices belong to the original boundary and cannot
be strictly inside a cycle all of whose vertices are original inner
vertices. Thus this entire bounded cap is unchanged by the construction
of J.

An empty triangulated C4 has a diagonal. Consequently every induced C4 in
J must meet m or z. If it meets both but omits mz, that edge is a chord;
an induced C4 containing both therefore uses mz. An empty triangulated
C5 also has diagonals, so every induced C5 avoiding m,z has a retained
single degree-five centre, with exactly its five cycle neighbours in J.

This does **not** say that all J C4s are empty, that every J C5 is small,
or that J is internally-six-connected. Cycles through m or z are precisely
the still-uncontrolled exceptions.

For the actual embedded cubic dual `D=J*`, these facts imply:

- Every three-edge cut is the star of one dual vertex. Indeed membership
  changes an even number of times around each primal vertex, so the
  primal image of a three-edge cut is an even subgraph with three edges.
  Simplicity forces a triangle, and the triangle is facial. The same
  parity argument rules out cuts of size one or two.
- The marked edges `e=vw*`, `f=pq*`, `g=mz*` are pairwise vertex-disjoint:
  no triangular primal face can contain two original edges with disjoint
  endpoint sets. Therefore each three-edge cut contains at most one of
  e,f,g.
- Every cyclic four-edge cut has at least two cut edges on the boundary
  of the dual face m or z. Its primal image is a C4. If that C4 has a
  chord, the facial-triangle result makes one side a two-triangle disk;
  that dual side has no cycle. Thus a cyclic cut gives an induced C4,
  which meets m or z by the preceding paragraph.

These are restrictions on the common original dual graph. They are useful
for the parallel prescribed-matching audit, but do not by themselves
assert that a matching has an even complement.

## 5. An exact disk after deleting the two stars

Since all J triangles are facial, the two common neighbours of m,z are
exactly alpha,beta. Any other common neighbour would give another triangle
through mz, while an embedded edge has only its two actual incident
faces. The edge alpha-beta is absent: it would make the two extra
triangles of a K4 through m,z, impossible in this source order. Each link
cycle is induced, since a chord would likewise give a nonfacial triangle.

Delete z from `link_J(m)`, obtaining the simple path P_m from alpha to
beta through w,v, in that order. Delete m from `link_J(z)`, obtaining the
simple path P_z from alpha to beta through p,q, in that order. The paths
have just their two endpoints in common. Here alpha may literally equal
p and beta may literally equal q; no endpoint is duplicated to make the
displayed order look strict.

The union of the closed stars of m,z is a triangulated disk with boundary

`C_star = P_m followed by reverse(P_z)`.

Its only strictly internal vertices are m,z, joined by their original
edge. The complementary closed disk is precisely

`W=J-{m,z}`,

with actual simple outer cycle C_star, and all its bounded faces are
triangles. No boundary edge or additional chord of W is deleted. Put
`M=d_J(m)`, `Z=d_J(z)`. Then

`|C_star|=(M-2)+(Z-2)=M+Z-4=d_G(s)+d_G(t)+h-6>=9`,

`|V(W)|=k-3`,

`number of W interior vertices = k+3-d_G(s)-d_G(t)-h`.

The dual patch has inherited face lengths M and Z, rather than two
unconstrained new terminals. The construction is a retained-edge
interface, not a smaller bad-source theorem.

## 6. Complete W fibres and the strengthened source obligation

Fix one **complete** W colouring chi, including every private vertex.
Define its two missing-colour sets from the actual paths:

`A_m(chi)={0,1,2,3} \ chi(V(P_m))`,
`A_z(chi)={0,1,2,3} \ chi(V(P_z))`.

Both sets have size at most two because P_m contains edge vw and P_z
contains edge pq. The full J fibre over this very colouring is exactly

`K(chi)={(a,b): a in A_m(chi), b in A_z(chi), a!=b}`.

The pair gives m=a,z=b and leaves every W vertex unchanged. Conversely
every J colouring restricts to exactly this W colouring and one such
pair. This proves a literal full-colouring bijection, including empty
K(chi). Nothing requires every W colouring to extend; discarding empty
fibres would change the object being compared.

The original all-r transfer is stronger than the previous E-free screen.
For a J colouring write its three edge differences as

`d_e=chi(v) XOR chi(w)`, `d_f=chi(p) XOR chi(q)`, `d_g=a XOR b`.

The unique legal r colour is the fourth colour omitted by `(a,chi(v),chi(w))`.
If z has that colour, the original R frame is ABAB and its pq palette
must be the two remaining colours, namely `{chi(v),chi(w)}`. If z instead
equals one of v,w, the R frame is ABCB; its original allowed pq palettes
are exactly the two that avoid the forbidden complementary-vw event.
Consequently, for every complete J colouring, the entire original all-r
condition is precisely

`(d_e=d_f) iff (d_e=d_g)`.                         (FJ)

Equivalently, the forbidden triples are `d_e=d_f!=d_g` and
`d_e=d_g!=d_f`. This uses the frozen R palette table in one literal frame;
it does not assume separate p/q witnesses. The432 proper local rows
contain240 allowed rows and96 rows of each forbidden kind.

The exact W obligation is therefore:

> For every complete chi in Col_4(W), and **every** pair `(a,b)` in
> K(chi), condition (FJ) holds.

If `chi(alpha)!=chi(beta)`, both missing-colour sets are contained in the
same complementary two-colour pair. Any legal distinct pair must use that
whole pair, so

`a XOR b = chi(alpha) XOR chi(beta)`.

Thus on every nonempty fibre with differently coloured alpha,beta, (FJ)
reduces further to the same-row boundary condition

`(chi(v) XOR chi(w) = chi(p) XOR chi(q))`
` iff (chi(v) XOR chi(w) = chi(alpha) XOR chi(beta))`.

This is a genuine reduction of the return obligation on this exact
geometric interface. It does not assert that such a nonempty fibre
exists with the condition false. If alpha,beta have equal colours,
the complete set K(chi), possibly with several different differences,
must still be retained.

### 6.1 A new excluded complete W fibre

**Theorem (two-palette equality).** In the original source, every complete
W colouring satisfies

`|A_m(chi)|=|A_z(chi)|=2 => A_m(chi)=A_z(chi)`.

Proof. Suppose the two size-two sets are different. Both paths use
exactly two colours. They share alpha,beta, so their used-colour pairs
intersect. If alpha,beta had different colours, both paths would use
that same pair, contrary to the assumption. Thus alpha,beta have one
common colour, and the two paths have different other colours. The two
missing-colour sets consequently have one common member; their
Cartesian product minus its one diagonal contains exactly three pairs.
Their XOR differences are exactly the three nonzero elements of F_2^2.

Because vw and pq are edges on their respective two-coloured paths,
`d_e=XOR(A_m)` and `d_f=XOR(A_z)` are distinct. Condition (FJ) therefore
requires `d_g!=d_e` in **every** legal hub lift. Exactly one of the three
actual lifts has `d_g=d_e`; it is a forbidden complete colouring of the
same J and gives the source contradiction. No choice between independently
constructed path colourings occurs. QED.

Both path endpoints now have the same colour, so both path lengths are
even. Hence this excluded fibre could only occur when M and Z are even,
equivalently `d_G(s)+d_G(t)` is odd and h is odd. This is a condition on
when the fibre can occur, not exclusion of the entire even/even degree
branch: existence of the offending complete W colouring is still
unproved. Empty hub fibres remain allowed and are not involved in this
argument. The theorem is one concrete, arbitrary-size source exclusion
at the level of complete fibres, beyond a mere rephrasing of the old
six-terminal event.

## 7. Relation to safe cycles and the remaining gap

The round-three proof translates any actual dual alternating-cycle switch
to a full primal colouring by a Klein translation on its side. Requiring
both forbidden events above to stay absent gives the stronger table:

| Allowed difference type | Pair that must be checked | Necessary and sufficient cycle condition |
| --- | --- | --- |
| all three equal a | each `{a,b}`, b different | f and g are on one cycle |
| `d_f=d_g!=d_e` | `{d_e,d_f}` | f and g are on one cycle |
| all three distinct | `{d_e,d_f}` | e and f are on one cycle |
| all three distinct | `{d_e,d_g}` | e and g are on one cycle |

Other pairs add no condition. The table follows by intersecting the
round-three one-event table with its version swapping f and g. For
example, when all three agree, avoiding the first event requires
`g~e or g~f`; avoiding the second requires `f~e or f~g`. By transitivity
their conjunction is exactly `f~g`. When a required coincidence fails,
the same one-cycle switch creates one of the two forbidden events.

The new geometry constrains the graph in which those actual cycles live:
it is the same four-connected J, with the exact two link lengths,
localised short separators, and full W fibres above. We have **not**
shown that this geometry forces any row of the table to fail. A precise
remaining obligation is to produce, from this original source, either
(i) a complete W colouring and one of its genuine hub pairs violating
(FJ), or (ii) a complete J colouring and an actual two-colour dual cycle
violating a required coincidence. Both are full-colouring statements;
neither can be replaced by an independently feasible boundary palette.

The numerical size decrease in W is not completed-source descent:

`(k-3) + 2 [restore m,z] + 1 [split m] + 5 [restore G from U] = k+5`.

A thin C5 cap on W would have k-5 interior vertices and supply some W
colouring by source minimality. It does not guarantee a nonempty K(chi),
let alone a violating hub pair. Thus this cap is not offered as a
circular proof of the remaining obligation.

## 8. Finite calibration and authority boundary

[check.py](check.py) independently reconstructs the432 local all-r rows.
It also builds three explicitly labelled two-star **patches**, not new
weak sphere counterexamples. They calibrate the generic fan case and the
literal endpoint identities alpha=p and beta=q. Each has boundary nine,
two interior hubs,2760 full colourings,19680 proper boundary rows, and
17040 empty hub fibres. It checks the Cartesian fibre formula against a
direct enumeration on the whole patch graph, retaining all full lifts
and all r colours. The remaining improper boundary assignments are
explicitly empty by their retained boundary edge. Parameters of these
local patches are not asserted to satisfy every global source collar
restriction, nor to be completed to a source.

These calculations validate the finite interface algebra and endpoint
bookkeeping. The arbitrary-size Jordan-side, source small-cycle, and
four-connectivity arguments are the paper proof, not a finite certificate
of hypothetical sources. An additional even/even patch, with M=8,Z=6,
has5688 complete colourings and59052 proper boundary rows;53712 fibres
are empty. Its24 differently two-coloured path rows each have all three
hub lifts, exactly one of which violates (FJ), as section6.1 predicts.
[check_two_palette.py](check_two_palette.py) retains the whole patch
relation and every empty fibre in [two-palette.json.gz](two-palette.json.gz),
not just the24 selected rows. This is a positive local calibration of
the excluded fibre; it does not supply a source W with that boundary row.
Normal/seed17 replay, corrupted fibre/source-
palette certificates, exclusive-create rejection, and the388-file prior
seal are recorded in [VERIFICATION.json](VERIFICATION.json).

Actual minimum sources supplied: zero, **not triggered**. Complete319
exclusion, omega=0, strict bad-source descent, and the general main claim
remain OPEN. There is no new external theorem, 4CT invocation, Lean
result, shared-document mutation, commit, or push.
