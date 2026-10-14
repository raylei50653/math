# General opposite-contact crosscut: source coverage review

BASE: `77fbd5da7ba273f0af7c75175dc08376d2282f46`.
Reviewed submission: `../frozen/T1_generalization_notes.md`, especially lines
80–110, and the subsequently supplied candidate ZIP, SHA256
`06c570b699817883ae6d444b33198a02693422c573bc8a7254e04c3aea457e4b`.
This is an independent paper review of the source-to-shell reduction, source
inspection of both candidate constructors, and a read-only comparison of all
64 saved named shell records with the original-face specification. No candidate
producer or verifier script was executed by this reviewer; numerical replay
belongs to the parent audit. This is a separate agent-assisted review, not a
third-party human review or Lean verification.

**Verdict: the arbitrary-source geometric reduction is sound under the adopted
BASE no4ct source contract.** The full graph admits the exact two-C6 decomposition
below for every original opposite double contact, without an upper bound on
either side's size or number of single contacts. This includes original BRIDGE
sources. The 32 named collar-target-position queries cover the required source
domain. Both inspected candidate implementations and all 32 saved main-case
shells match the specification below; the 32 supplemental BRIDGE shells were
also compared. The finite exclusion is a separate obligation; this review
alone does not establish `h=3 => p=0`.

## 1. Exact imported source contract

All repository paths and line references in this report refer to BASE.

* `audits/2026-10-13-c5-no4ct-c8-6cafdfb/REPORT.md:17–25` fixes a globally
  minimum interior-vertex count over **all** catalogue-external finite simple
  disk-C5 sources, followed by maximum edge count. It does not minimize one
  target mask separately. One common D5 alignment fixes the original ordered
  B and the complete relation in `{932,933,941}`. G is a simple plane
  near-triangulation with chordless outer B and the actual inner cycle
  C_(5+h). For h=3, H contains all k original interior vertices.
* That report, lines 38–45 and 96–107, supplies induced C8 and the exact eight
  remaining collar-target contracts; lines 118–125 connect the original
  contact and peeling structure to the no4ct contract. In particular, the
  h=3 target 932 is already excluded (lines 76–85).
* `docs/c5_c8_peeling.md:43–59` fixes C=(c0,...,c7), the original inner disk H,
  I=V(H)\C and Q=H[I]. Every I vertex has at most two C contacts; a double
  contact is adjacent or opposite. The counter p counts precisely the
  opposite double contacts (lines 50–59).
* `audits/2026-10-13-c8-peeling-6cafdfb/structure/PROOF.md:83–90` already uses
  c_i–x–c_(i+4) as a simple disk crosscut. Its arbitrary-size classification is
  stated and proved in lines 94–115. No finite-size calibration is used in
  the proof below.

The new geometric step needs less than the whole inherited source contract:
a simple embedded disk with the stated actual C8 boundary and an interior
vertex with the two original opposite spokes suffices for the two-disk cut.
The stronger adopted hypotheses fix the outer annulus and ensure that x has
no other B or C contacts. The no4ct dependency repair is retained; no universal
four-colourability assertion is imported here.

## 2. Source-to-annulus map, with all original B contacts

For a fixed source query, write e_j=d_G(b_j)−4. The actual interior link of
b_j is

`(a_(j−1), y_(j,1), ..., y_(j,e_j), a_j)`.

Here a_j is the third vertex of the original face b_j b_(j+1) a_j. The five
a_j and the three y vertices are pairwise distinct. Each a_j is adjacent
to exactly b_j and b_(j+1) among B; each y_(j,t) is adjacent to exactly b_j.
These are **all** B-to-interior neighbours. In the original orientation C is

`(a0, y_(1,*), a1, y_(2,*), a2, y_(3,*), a3, y_(4,*), a4, y_(0,*))`.

This is the paper construction in
`audits/2026-10-13-c5-no4ct-collar-6cafdfb/REPORT.md:87–104`, and is exactly
the naming map implemented by the adopted T1 independent constructor in
`audits/2026-10-13-c8-terminal-s1-d521163/review/independent_transfer.py:38–51`.
Define c_j to be entry j of this ordered list, once for the entire source;
neither a colouring nor a choice of cut changes this map.

The exact six geometric lists for the eight source queries are:

| Query or queries | e | c0,...,c7 in original names |
| --- | --- | --- |
| c15-933, c15-941 | (0,1,2,0,0) | a0,y1_1,a1,y2_1,y2_2,a2,a3,a4 |
| c18-933, c18-941 | (0,2,1,0,0) | a0,y1_1,y1_2,a1,y2_1,a2,a3,a4 |
| c04-941 | (0,0,1,0,2) | a0,a1,y2_1,a2,a3,y4_1,y4_2,a4 |
| c07-941 | (0,0,2,0,1) | a0,a1,y2_1,y2_2,a2,a3,y4_1,a4 |
| c20-941 | (1,0,0,0,2) | a0,a1,a2,a3,y4_1,y4_2,a4,y0_1 |
| c30-941 | (2,0,0,0,1) | a0,a1,a2,a3,y4_1,a4,y0_1,y0_2 |

The eight query identities and e values agree between the adopted no4ct
report (lines 98–107), the T1 independent constructor (lines 16–21), and the
submission (lines 39–53). Thus "eight collars" is best read as **eight named
collar-target contracts**; there are six distinct geometric annuli.

Let A be the graph consisting of the two original boundary cycles B and C,
the ten edges b_j a_j and b_(j+1) a_j, and the three edges b_j y_(j,t).
There are no omitted B edges, because B is chordless and its complete links
have just been listed. There are no annulus-private vertices: the original
faces b_j b_(j+1) a_j together with b_j u v for consecutive vertices u,v of
its interior link fill the annulus. All other original vertices lie in H.
The source's induced-C8 conclusion forbids extra C-to-C chords. Consequently
A is the whole original outer patch on B∪C, with its original face sectors.

## 3. The actual two closed disks and exact intersections

Assume p>0 and choose one **original** vertex x counted by p. Choose the
unique i∈{0,1,2,3} with N_C(x)={c_i,c_(i+4)}. Put

`K = c_i–x–c_(i+4)`.

The two spokes are original embedded edges. They have no crossing, their
open interiors contain no graph vertex, x lies strictly inside C, and their
only common point is x. Thus K is a properly embedded simple arc in the
closed disk bounded by C, meeting its boundary only at its two endpoints.
The disk crosscut theorem separates that closed disk into two closed disks
Δ+ and Δ−, with simple boundary cycles

`D+ = (x,c_i,c_(i+1),c_(i+2),c_(i+3),c_(i+4))`,

`D− = (x,c_(i+4),c_(i+5),c_(i+6),c_(i+7),c_i)`.

Both have exactly six distinct original vertices. Define L± to contain every
original vertex and edge of H drawn in Δ±, including the whole boundary.
This is a restriction of the original embedding, not a graph replacement.
Every original edge not on K has its open interior on just one side of K:
otherwise its embedding would meet K away from an allowed common endpoint.
No original edge can join the two open disks. At c_i, c_(i+4), and x, the
original rotation assigns every incident edge sector to its actual side.

The resulting exact vertex and edge identities are

```
V(L+) ∩ V(L−) = {x,c_i,c_(i+4)},
E(L+) ∩ E(L−) = {x c_i, x c_(i+4)},
V(H) = V(L+) ∪ V(L−),
E(H) = E(L+) ∪ E(L−).
```

The vertex intersection has no hidden vertices because original edges have
no vertex in their open interiors. The edge intersection contains no
c_i c_(i+4), since C is induced. Equivalently it follows directly from the
closed-disk intersection Δ+∩Δ−=K. A triangle of H lies on one side unless
its boundary contains a crosscut edge; in the latter case its interior
still lies on exactly one side. Hence each L± inherits all original faces
inside its disk, in particular a near-triangulation, with no edge or face
sector dropped at the three shared vertices.

Define the fixed shell P=A∪K. Then, writing D± for its boundary-cycle graph,

```
V(P) = B ∪ C ∪ {x},
E(P) = E(A) ∪ {x c_i, x c_(i+4)},
V(P) ∩ V(L±) = V(D±),
E(P) ∩ E(L±) = E(D±),
G = P ∪ L+ ∪ L−.
```

Each boundary cycle edge is retained in P and its side. The two spokes
belong to all three graphs; this repetition records the same original
edge and same original x. Every B vertex is outside both L±. Every vertex
strictly inside L± has no neighbour outside L±: crossing C would first
meet C, and crossing K would first meet K. All original C-to-interior edges
lie in their assigned L±; all original B-to-C edges lie in P.

As an exact shell check, P has 14 vertices and 28 edges: five B edges,
eight C edges, thirteen B-to-C edges and two spokes. Its annulus has the
thirteen original triangular faces just described; its two remaining inner
faces are the two C6 holes. Both source inspection and the saved-record
comparison in §6 agree with this exact shell signature.

## 4. Why all p>0 sources, including BRIDGE, are covered

The four unordered opposite pairs are `{c0,c4}`, `{c1,c5}`, `{c2,c6}` and
`{c3,c7}`. Using i+4 instead of i only interchanges the two stated disk
orders; fixing i in 0,...,3 therefore loses no source. No rotation of B or
C is used when selecting i. Every one of the eight named source queries
has precisely these four choices, giving 32 named obligations. There are
24 distinct geometric shells, with c15 and c18 each tested against both
targets; this duplication is intentional.

For an original BRIDGE source, choose either endpoint as x. The other
endpoint y is not on K, so it belongs strictly to one of Δ±. Its two
spokes to C and its original bridge xy belong to that same L±. This is
also visible in the original empty-C4 proof: the faces c_i x y and
c_(i+4) x y are on the side of K containing y
(`structure/PROOF.md:88–90`). The bridge is therefore neither deleted
nor treated as an independent external constraint. Its endpoint x is
the very same x in P and both interfaces. Nothing in the decomposition
requires p=1, a terminal of size W5, or a prescribed terminal link order.

Every single contact, all original terminal interior vertices, and all
their edges remain in L+ or L− according to the original embedding.
The location and number of these vertices affect the two unknown complete
relations, but do not alter P or D±. Thus the reduction is uniform over
all nonnegative s+,s− and all finite side sizes allowed by the original
contract. It also avoids assuming that the next peeled boundary inherits
degree, chord or contact restrictions: it does not peel to that boundary.

## 5. Exact full-lift consequence and adoption boundary

For each original B row β and complete literal colouring f of P extending
β, put γ±=f restricted to D±. There is an exact bijection

```
F_G(β) ≅ disjoint_union over f∈F_P(β)
             {f} × F_L+(γ+) × F_L−(γ−).
```

The product is valid because both side lifts agree with f at every shared
original vertex and their private vertices are disjoint. Union is unique
**for a chosen triple of lifts**. All original edges occur in the union
of the three pieces; restriction is the inverse map. Empty side fibres
give empty product cells. This preserves full lifts, not just their
existence or separate side marginals. The complete support/orbit formula
in the submission follows by S4-equivariance of each fixed side graph,
with the same literal P colouring determining both orbit indices.

The submission's geometry has no uncovered arbitrary-size PINCH/BRIDGE
case under these premises. Two wording improvements make the exact
contract explicit:

1. Submission line 101 should say: "All B-to-C edges already belong to
   the fixed P; the original C-to-inner edges, and all remaining inner
   edges, are retained in their actual L±." B is not a vertex of L±.
2. Submission line 120 should specify that **each chosen pair of complete
   lifts**, together with the chosen shell lift, has a unique union.
   Membership in the two orbit supports does not assert unique side lifts.

The source map is proved here by original faces, rotation and disk
separation. Seven small positive controls, or any larger finite source
search, would not prove this coverage. Conversely the coverage proof
does not verify the alleged 512,568 rectangles or their missing target
row. The source-to-shell comparison is complete in §6; theorem adoption
still requires validation of the complete finite exclusion certificate.
No Lean theorem, general RING
exclusion, h≥4 exclusion or general catalogue closure follows from this
source-coverage review.

## 6. Candidate code and all saved shell identities

All candidate paths in this section are relative to
`../candidate-original/t1_broad_probe/`.

The active constructor is `twohole_probe.py:13–36`, imported by
`twohole_fast.py:7`. For `kind='PINCH'` it creates exactly the original B
and C cycles, the thirteen original B contacts under the source map, one
vertex x, the two original opposite spokes, and the two C6 orders used
above. The loop at lines 33–35 uses the **same** string x in both interfaces.
It has no t vertices, fixed W5 end, other terminal, or single-contact
parameter. The eight queries are imported from `probe.py:9–14`, exactly
matching BASE's T1 query table. The old `probe.outer()` at lines 23–60 is
the separately retained one-W5 exploratory cut; the active broad producer
does not call it. `probe.colouring()` is used only for literal enumeration.

`independent_verify.py:28–46` gives the same map by rebuilding the actual
outer triangular faces rather than importing the producer: five B-edge
triangles and all consecutive interior-link fan triangles. Their undirected
edge union, plus both original C6 boundary cycles, is precisely P. For
the supplemental BRIDGE shell it additionally inserts both original
triangles c_i x y and c_(i+4) y x; x and y are different vertices, and
xy is retained. The two endpoint names are attached to opposite half-arcs
once globally. The filled-hole tests at lines 47–65 check edge incidences,
Euler characteristic and vertex links. The stored triples are face vertex
sets, not a certificate of a globally coherent directed orientation; the
paper fan order above supplies the inherited embedding. This distinction
does not alter their correct undirected shell or ordered interfaces.

The literal synchronisation also matches the paper map:
`twohole_probe.py:38–47` enumerates one entire shell colouring before deriving
both canonical C6 indices; `independent_verify.py:68–88` does the same with
its own fixed vertex order and saves every full shell lift. Neither obtains
a purported joint state by independently picking the two boundary colours.

A separate inline Python check was run read-only against all eight saved
`twohole_{kind}_{pair}.json` files. It parsed only the upstream BASE
`BROWS` and `QUERIES` literals via `ast.literal_eval`, reconstructed the
thirteen annulus triangle faces from the paper's link formula, took their
edge union and added the prescribed original spokes (and xy for the
supplemental BRIDGE case). It compared every complete ordered vertex list,
sorted edge list, both ordered interfaces, query, target and e tuple.
It also required each record's kind/pair to equal its filename slot and
checked the exact eight-query sequence in each file and 64 unique case keys.
The observed result was:

```json
{"named_shells_compared":{"BRIDGE":32,"PINCH":32},"scope":"read-only original-face edge reconstruction and exact named-file coverage; no candidate script import or execution","status":"PASS","unique_case_keys":64}
```

The exact graph signatures were `(14 vertices,28 edges)` for every PINCH
shell and `(15 vertices,31 edges)` for every supplemental BRIDGE shell.
This is a full finite **shell-identity** comparison, not a reconstruction
of arbitrary original interior graphs and not a rectangle/Kempe replay.

One validator coverage issue should remain explicit. In the submitted
`independent_verify.py`, `check_record()` reads kind/pair from the record
itself (lines 148–153), while `run(kind,pair)` checks only the query sequence
(lines 217–224). The verifier by itself does not check that each record
belongs to its requested filename slot. Thus an otherwise internally valid
replacement with a duplicate kind/pair file could pass that per-file path.
The separate 64-key check just performed closes this potential omission
for the **supplied bytes**. A durable adoption wrapper should enforce those
same slot and uniqueness conditions whenever it validates a package.
