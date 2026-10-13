# Independent review: exact edge quantifiers and one-swap synchronization

2026-10-13. Scope: the frozen original-source documents in this audit only.
This review introduces no actual minimum outside-catalogue source.

## 1. Audit of the inherited single-edge statement

Let G be a global interior-vertex minimum among all disk C5 sources whose
complete ordered relation is outside K132. After one common D5 transport,
assume R=Sigma(G) is 933 or 941. Put p*=01232. The inherited finite premise is
that no S in K132 satisfies p* in S subset R. For 933, 01231 has the same
finite property; it is a separate application.

Fix a nonboundary edge e=st incident with triangular faces stu and stv.
Require u and v distinct and at least one of u,v interior. The latter refers
to the vertices being identified, not merely to an endpoint of e. If a
complete G colouring c with boundary p* has c(u)=c(v), then u,v are
nonadjacent. Deleting e makes them cofacial. Identification gives the legal
disk source Q=(G-e)/(u=v), retains the original five boundary vertices, and
has fewer interior vertices. Thus Sigma(Q) is in K132 and contains p*.
The finite premise supplies p in Sigma(Q) minus R. Every lift f of such p
back to G-e satisfies f(u)=f(v), and must also satisfy f(s)=f(t): otherwise
f would restore e and extend p to G. Its four surviving side edges make
the two equal-colour pairs use distinct colours.

In precise form, with J retaining literal colours and full lifts,

    for every eligible e,
      J_e(p*;1,0) nonempty implies
        there exists p outside R with J_e(p;0,0) nonempty.

For every p outside R, both J_e(p;1,0) and J_e(p;1,1) are empty.
The antecedent is edgewise existential in the original p* colouring. A
fixed original c can supply many antecedents, but the conclusion is only
for all e exists p_e exists f_e. Neither a common p nor a common f follows.
The proof does not assert Kempe reachability from c to f_e: their boundary
rows differ, and Q minimality supplies an extension existentially.

The edge-maximal secondary normalization is not used by this isolated
implication once the two triangular faces and the legal quotient are
supplied. It is used upstream to supply the required plane configuration.
The requirement that an opposite vertex is interior is indispensable to
this proof: identifying two original boundary vertices does not retain
the original C5 source contract.

## 2. Universal obstruction to literal cross-edge witness intersections

For an edge e of any simple graph G and a fixed boundary row p, let

    D_e(p) = {f proper on G-e, f|B=p, f identifies the endpoints of e}.

If e and d are distinct original edges, then D_e(p) intersect D_d(p) is
empty. Indeed, f in D_e is proper on d, whereas f in D_d is monochromatic
on d. This proof is independent of planarity, minimality, or catalogue
assumptions. In particular, literal intersection of two J_e(p;0,0)
full-lift sets is always empty. The useful common object for spokes at a
single vertex is their restriction to G-v, with an explicitly different
colour assigned to v in each extension. This is stronger than merely
warning that arbitrary witnesses might fail to coincide.

## 3. Exact boundary-fixed one-swap escape theorem

Let G be any finite graph with an interior degree-five vertex v whose
five distinct neighbours, in cyclic order U=(u0,...,u4), contain the five
rim edges. Set H=G-v, and let B be the boundary whose literal colours must
remain fixed. Assume B and {v} are disjoint; U may meet B. Fix a proper H
colouring h with

    h(U)=(a,b,a,c,d), with a,b,c,d pairwise distinct.

For a colour pair x,y, write K_xy(w) for the connected component of w
in the subgraph of H induced by colours x and y. A one-component Kempe
swap is boundary-fixed exactly when its component misses B.

**Theorem.** A boundary-fixed one-component Kempe swap reduces the number
of colours used on U from four to three if and only if it swaps one of
the pairs {b,c}, {b,d}, the two corresponding singleton rim vertices lie
in distinct bichromatic components, and the swapped component contains
one of those vertices and misses B.

**Proof.** All four colours occur on U. A swap can remove a colour from U
only by moving every occurrence of that colour into the other colour
without simultaneously moving an occurrence of the latter back. For a
pair containing the repeated colour a and any singleton colour, the rim
has an edge with those two colours: b is adjacent to both a occurrences,
c is adjacent to u2, and d is adjacent to u0. The edge's two endpoints
belong to one component. Swapping that component leaves both colours on
the edge; swapping a different component leaves the edge unchanged.
Thus both colours remain on U. The singleton pair {c,d} likewise has
rim edge u3u4 and cannot remove a colour. For {b,c} or {b,d}, each colour
occurs once on U. If the two occurrences lie in the same component,
swapping it interchanges them and leaves both colours; swapping another
component changes neither. If they lie in different components, swapping
exactly one component containing an occurrence removes its colour from
U and leaves the other three colours. Such a swap fixes B precisely when
that component misses B. These cases exhaust all six colour pairs. QED.

Equivalently, at least one boundary-fixed one-swap escape exists precisely
when, for one of the two nonadjacent singleton pairs, the corresponding
components are distinct and at least one misses B. This condition is
necessary and sufficient within the one-component, one-swap mechanism;
it is not claimed to be necessary for longer Kempe sequences or arbitrary
recolouring.

## 4. Same-lift tether consequence and conditional exclusion

Suppose p does not extend to G but h extends p to H. The rim must use all
four colours, since any missing colour could be assigned to v. Rotate
the rim and use notation as above. Applying the theorem yields, in this
same h, both constraints

    K_bc(u1)=K_bc(u3), OR both distinct components meet B;
    K_bd(u1)=K_bd(u4), OR both distinct components meet B.

These are statements about actual bichromatic components of one original
H colouring, with its fixed boundary colour frame. They are not existence
claims assembled from different edge witnesses. When the components are
distinct, the conclusion supplies actual paths from each singleton to B,
in the same induced bichromatic graph. The two obligations are compatible
with sharing vertices of colour b and must not be treated as disjoint
paths unless a separate argument proves disjointness.

The same conditions hold at every H colouring reachable from h by a
finite sequence of boundary-fixed Kempe swaps. Otherwise the final
escape would give a three-colour rim and hence an extension to G. This
orbit obstruction is a necessary condition, not a proof that the orbit
is all of the p fibre.

There is a useful sharper special case. If a colour pair x,y occurs on
at most one vertex of B, two distinct x/y components cannot both meet B.
For either nonadjacent singleton pair, rejection then forces an actual
bichromatic path between its two rim vertices. All rejected rows of 933
and 941 use three boundary colours with multiplicities (2,2,1). Hence,
when a relevant inner singleton pair consists of the absent boundary
colour and the unique boundary singleton colour, it must have an actual
path. This does not prove that either of the two relevant pairs always
has those colours; that placement remains an additional hypothesis.

For a hypothetical globally minimum 933/941 source, deleting an interior
degree-five vertex gives a smaller disk source H with Sigma(H) in K132.
Since R is not in K132 and R subset Sigma(H), some rejected p extends to
H. Consequently, the following **conditional exclusion criterion** is
sufficient: for at least one such v and at least one p in Sigma(H) minus
R, an H colouring has a nonadjacent singleton pair in different
bichromatic components with one component disjoint from B. The theorem
then constructs, by one swap and assigning v the missing colour, a
literal full G extension of p, a contradiction.

This criterion asks for only one pair in one actual lift. It does not ask
all five spokes to have identical full lifts, or all rejected rows to
escape. Within a single-component one-swap mechanism it is exact. No
argument here proves that the established nine/eight degree-five
vertices, or the entirely internal W5, force this condition. Such a
topological forcing result remains the missing universal step.

## 5. What catalogue information alone does and does not synchronize

The frozen certificate gives precisely these K132 supersets of R:

    R=933: 935,943,951,957,959,997,999,1005,1007,1013,1015,1021,1023;
    R=941: 943,957,959,1005,1007,1021,1023.

Their respective new-row masks are

    R=933: 2,10,18,24,26,64,66,72,74,80,82,88,90;
    R=941: 2,16,18,64,66,80,82.

The common intersection is empty in each case. Thus membership in K132
and containing R, alone, do not force a preselected rejected row to occur
in every vertex-deletion source. This is a finite relation-level
non-implication; it does not assert that these supersets are jointly
realizable by deletions of one target source.

The established n5>=9 for 933 and n5>=8 for 941 do force at least three
degree-five vertices whose deletion sources accept one common rejected
row, by pigeonhole over respectively four and three rejected rows.
Their H graphs differ and no common full colouring follows. The exact
new-row counts and empty intersection are reproduced by catalogue_check.py.

A slightly stronger incidence count starts with one fixed original
accepted colouring alpha=01232. The inherited collar proof supplies two
adjacent eligible opposite-equal spokes at each degree-five interior
vertex. Label every such (vertex, spoke) incidence with a rejected row
given by the original single-edge lemma. There are at least 2n5 flags,
so one rejected row labels at least ceiling(2n5/4)>=5 flags for 933, or
ceiling(2n5/3)>=6 flags for 941. Any one edge is counted at most twice,
and any one centre contributes exactly two flags. Thus one rejected row
has such 00 witnesses at at least three distinct original edges and at
least three distinct degree-five centres. This counting conclusion still
does not identify full colourings at different centres.

At one centre, a rejected-row 00 witness for spoke i restricts to a
four-colour rim with repeated pair (i-1,i+1). Assigning the centre each
singleton rim colour gives defect witnesses at i, i+2, i+3. If both
adjacent original trigger spokes i and i+1 have 00 witnesses in the same
rejected row p, their respective triples cover all five spokes. This
gives five p single-defect witnesses, not one simultaneous colouring.
The two original 00 witnesses even have necessarily different H
restrictions: their four-colour rims have different unique repeated
pairs. This is a conditional support-level sharpening, not an exclusion.

## 6. Trust boundary

Sections 2--4 are elementary full-colouring arguments. Section 1 inherits
the upstream legal plane quotient and K132 subrelation calculation.
Section 5 is a bounded replay of the frozen 132 relation keys, not a
re-enumeration of disk graphs. The nine/eight degree bound and existence
of an entirely internal induced W5 are inherited paper results. No
actual 933/941 minimum source was provided or constructed, so that source
domain is `not triggered`. No new Lean theorem is claimed. A counterexample
outside the minimum-source contract would refute only a broader proposed
inference, not the source-conditioned theorem above.

The independent script also checks all 120 literal proper four-colour
rim assignments against all partitions of the selected two-colour rim
vertices consistent with rim edges, all component boundary-hit flags,
and each selected component swap: 5,280 cases, including 960 escapes.
This verifies the local iff combinatorics. It does not assert plane
realizability of arbitrary abstract component partitions. Reproduce with:

    python3 -B audits/2026-10-13-cross-edge-kempe-19209f4c/review/catalogue_check.py

The same script independently checks the four identities (W) directly
by assigning each of the four possible centre colours for each of the
240 proper literal rim colourings, each of five spokes, and each of four
cells. All 4,800 cells agree with the stated A/T classification; exactly
1,080 cells are nonempty, and every such cell has a unique centre colour.
Normal and PYTHONHASHSEED=17 output are byte-identical in catalogue_check.json
and catalogue_check.seed17.json.

## 7. Independent review of the root REPORT

Reviewed the full draft REPORT.md, including every displayed identity.
The following are accepted mathematically under the stated source and
pin conventions:

- (W): the four complete restriction bijections. The two three-colour
  opposite-equal positions are i+2 and i+3 relative to the unique
  singleton; the other three positions give the 11 cell. The 01 cell
  consists of A_(i+2), A_(i+3), and T_i, with unique centre restoration.
- (C): exact nonnegative residuals t_i and the full G-extension count.
  No quotient by colour permutations or independent rim normalization
  is used in these counts.
- (A): composing through the same literal J_vw(p;0,1) colouring yields
  the claimed bijection between two disjoint unions, preserving all
  colours outside {v,w}. The rejected-row premise removes T summands.
  Independent middle witnesses would not establish this map.
- (G): summing (C) counts each original edge once for each of its
  degree-five interior endpoints. Its right-hand side is n5 times the
  same original G p-extension count. For a rejected row it is zero,
  without implying that either summand separately vanishes.
- The >=5/>=6 flag count, its >=3 distinct edges and >=3 centres
  consequence, and the conditional five-spoke support consequence.
- The exact one-component escape theorem and the explicit lack of a
  proof that the source structure forces its hypothesis.

Two definition clarifications were requested from the parent: the
algebraic wheel formula must explicitly use designated opposite pins
u_(i-1),u_(i+1) if triangular faces are not assumed; and (G)'s edge sum
must range only over edges for which the two-face J_e is defined (all
contributing edges are nonboundary). These do not change the source
theorems or proofs. Both clarifications are now present in the root
REPORT: actual triangular faces are required for its original-face
semantics, and the weighted sum ranges over edges incident with a
degree-five interior vertex. No substantive mathematical correction was found.
This review accepts the paper derivations, not upstream finite graph
enumeration, source realizability, or a universal 933/941 exclusion.

The added same-row six-edge bound is also accepted. Select the three
centres already forced by the flag pigeonhole argument. Each supplies
three distinct spokes with a p single-defect witness, giving nine
incidences. A duplicated edge must join two of these three centres, so
there are at most three duplicate pairs; no simple edge belongs to all
three stars. Their union therefore has at least 9-3=6 distinct original
edges. The conclusion is about 00-or-01 support in one rejected row,
not six equal complete colourings, nor necessarily six 00 cells.

## 8. Independent full-lift and actual-component replay

`independent_full_lifts.py` imports no project checker. It enumerates the
Cartesian product of all free vertex colours directly from literal
edges for each G, each vertex deletion H, and each G-e. It compares
complete sets including duplicate rejection and every empty cell.
It separately rebuilds actual bichromatic components by a graph search,
then checks all boundary-fixed component swaps and all rim4-to-rim3
single moves. The original certificate is read-only and its bytes are
checked unchanged at exit.

On certificate SHA-256
`200109de855e537cbcd5871015873528afb0d2be7c3e8dcd493d34fd05750960`:

- Five literal graphs: 50 G rows and 403 complete G lifts.
- Sixteen original degree-five centres: 160 H rows and 1,253 complete H
  lifts, including every `other_degree5_wheels` deletion.
- Sixty-one original edge tables: all 2,440 cells, of which 1,063 are
  empty, with all 4,894 complete J lifts matching.
- All 7,518 bichromatic component partitions and 4,870 boundary-fixed
  component swaps match the stored complete data.

The same independent checker explicitly reconstructs (A), rather than
inferring it from counts. For every rejected row at an adjacent pair
v,w, it recolours v to obtain the exact middle G-vw lift, identifies the
unique repeated rim pair at w, then recolours w into its right-hand 00
branch. The map is checked bijective and preserves every literal colour
outside {v,w}. Fourteen rejected adjacent-edge rows are checked; eight
have nonempty transport, totalling ten transported full lifts. Thus
this test is not vacuous despite `triangulated_00` accepting every row.

Normal and seed17 results are byte-identical in `independent_full_lifts.json`
and `independent_full_lifts.seed17.json`. Explicit negative mode checks
deleting a nonempty J lift, populating an empty J cell, and deleting an
H lift. All three corrupted temporary copies are rejected, while the
original bytes remain unchanged; diagnostics are saved in
`independent_full_lifts.negative_controls.json`.

    python3 -B audits/2026-10-13-cross-edge-kempe-19209f4c/review/independent_full_lifts.py
    PYTHONHASHSEED=17 python3 -B audits/2026-10-13-cross-edge-kempe-19209f4c/review/independent_full_lifts.py
    python3 -B audits/2026-10-13-cross-edge-kempe-19209f4c/review/independent_full_lifts.py --negative-controls

The default command writes only stdout. Explicit negative mode creates
and removes temporary damaged copies within this review directory; it
does not overwrite the certificate. These five finite graph controls
are `triggered and holds`; an actual minimum outside-catalogue source
with relation 933 or 941 remains `not triggered`.
