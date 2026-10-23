# Two new same-source k−2 completions, with one exact common obligation

Fix the complete original r6 two-star minimum source G with full labelled support
933. The authority is the frozen source proof and the two predecessor audits in
[INPUTS.json](INPUTS.json). This is a conditional paper argument about that one
hypothetical G, its original rotation and its actual exterior E. No such source
is supplied or realized here.

Retain

```
B=(x,y,a,b,c), E=(a,n,R,L,q,c,x,y),
N(p)=(a,b,q,h,n), N(h)=(p,q,L,R,n), N(b)={a,c,p,q}.
```

All original attachments, small-cycle hypotheses, facial triangles, interior
minimum degree five, x/y/b degree four, p/h degree five, r degree six and s/t
at least six remain in force. The frozen source proof establishes that E is a
**genuine complementary disk**. We do not assume an abstract polygon can replace
this original geometry.

## The new legal graphs

Delete the two original interior vertices p,h. Their actual two-star disk has
simple boundary, in original cyclic order,

```
H=(a,n,R,L,q,b).
```

The original triangle bqc remains outside this hole. All of E remains unchanged.
Draw these respective noncrossing sets of diagonals *inside that actual hole*:

```
T0=(G−{p,h})+{aL,bL,nL},
T1=(G−{p,h})+{aL,bL,aR}.
```

For T0 the four new triangular regions are anL, nRL, Lqb, Lba. For T1 they are
anR, aRL, aLb, bLq. Thus the drawing respects the original rotation and all
original retained attachments. Each diagonal joins two distinct original hole
vertices. If a diagonal's endpoint pair already has an original edge drawn in
E, first draw the new parallel copy in the hole and then delete **that new
copy**, keeping the original edge. This yields a simple plane disk-C5 graph
with the same vertex set and exactly the same colouring inequalities. No
original E edge, outer edge or vertex is deleted. The resulting faces need not
all be triangles; the globally minimum bad source's competitors are simple
plane disk-C5 graphs. No triangulation hypothesis is needed on a competitor.

Both original boundary names and the ordered C5 survive. No vertex is added or
identified, so both completed graphs have k−2 interior vertices. These graphs
are different from Q1, Q2 and the old fan-B. This round also checks the fourteen
possible noncrossing triangulations of this **one** hole; it does not enumerate
exterior graphs.

## The same actual complete exterior counts

For each proper C8 representative t_j in the fixed E order let z_j be the number
of **all complete extensions to this same E** of its fixed literal assignment.
These are nonnegative integers. Canonical indexing uses only a single common
S4 permutation of a complete colouring and every named contact. Nothing is
normalized separately by factor, row, candidate, palette or component.

The frozen planar indicator-span argument and original source Kempe zeros imply
z lies in the reconstructed 18-dimensional rational space B. The coefficients
of the planar span can be signed. Only the actual z entries are nonnegative;
there is no converse from the span, nonnegativity or necessary Kempe conditions
to an original source.

The checker rebuilds all 2560 literal assignments consisting of ten fixed outer
rows and all four-colour assignments to n,R,L,q. For every one it retains **all
16 tested original (p,h) assignments**, via the complete lift set including
empties. There are 175 lifts and 2392 empty old fibres. It simultaneously tests
the edges of all fourteen actual replacement patches. This gives nonnegative
integer matrices M_G and M_i, each 10×274, and the exact whole-graph identities

```
N(G)=M_G z, N(T_i)=M_i z.
```

The complete matrices and all literal local fibres are in
[certificate.json](certificate.json). To check them independently,
[independent.py](independent.py) starts with canonical E words and b, applies one
common colour permutation to the outer frame and every contact, and reconstructs
all matrices. It also compares M_i z with direct complete colourings of fourteen
actual graphs built on one genuine cone-over-C8 exterior. That cone control
**does not satisfy the full original r6/933 source contract**.

Here is the full ten-row projection for the two new candidates on B. Write
S(I)=sum_{j in I} z_j. A listed sum uses only actual complete E fibres; omitted
raw projection terms are coordinates identically zero on B. The certificate
retains those raw terms as well.

| Outer literal row | T0 | T1 |
| --- | --- | --- |
| 01012 | S(33,38,40,45,60,85,214,220,227,228,248,267) | S(153,154,161,167,181,200,214,220,227,228,248,267) |
| 01021 | 0 | 0 |
| 01023 | S(32,38,40,46,58,87,215,222,227,228,247,268) | S(153,154,159,166,180,201,215,222,227,228,247,268) |
| 01201 | S(88,216,233) | S(155,172,202,216,233) |
| 01202 | z73 | z196=z73 |
| 01203 | S(37,42,43,48,63,89,217,224,230,232,252,270) | S(156,158,164,171,185,203,217,224,230,232,252,270) |
| 01212 | z76 | z198=z76 |
| 01213 | S(35,42,43,50,62,90,219,225,230,232,250,272) | S(156,158,163,169,183,205,219,225,230,232,250,272) |
| 01231 | S(34,51,61,91,218,226,233,273) | S(155,182,204,218,226,233,273) |
| 01232 | S(52,54,75,77,257,259) | z257+z259 |

## A four-variable exact statement

Define actual complete counts

```
U=z73  =z196,     V=z76  =z198,
W=z257,          W'=z259.
```

Their fixed representative E words are

| Name/ID | Word |
| --- | --- |
| U / 73 | 01023013 |
| V / 76 | 01023031 |
| U alias / 196 | 01213023 |
| V alias / 198 | 01213032 |
| W / 257 | 01232023 |
| W' / 259 | 01232032 |

Exact multiplication against a reconstructed basis of B proves

```
U+W=V+W'=z30,
N01232(G)=4(U+W)>0,
N01021(T0)=N01021(T1)=0,
N01202(T0)=N01202(T1)=U,
N01212(T0)=N01212(T1)=V,
N01232(T0)=4(U+W)=N01232(G),
N01232(T1)=W+W'.
```

These statements are stronger than merely selecting an accepting witness. T0
has the same complete accepting count as G, for every actual exterior satisfying
the source contract. They do not claim a bijection of individual original and
replacement witnesses; the equality follows from complete count identities.

Consequently the original four-query bad certificate on either fixed new graph
has the **same exact remaining obligation**:

```
U=V=0.                                                (O)
```

Necessity follows from its two complete rejected counts. For sufficiency, (O)
gives W=W'>0, so T0 accepts with the original accepting count and T1 accepts
with half that count. Both reject all three rows 01021,01202,01212. The checker
independently checks all 64 ten-row masks satisfying these four requirements
against the complete K132 catalogue; all are outside K132. Thus **if (O) is
proved for the original source, both legal graphs are genuine k−2 smaller bad
competitors**. No independently feasible external assignments or per-row graph
choice enter this implication.

In particular, for the **globally minimum original source** its smaller-graph
minimality gives the new geometric necessary condition

```
U+V>0.                                                (M)
```

This use of minimality is explicit. It is not claimed on an arbitrary exterior
count vector, an arbitrary r6 two-star graph, or the 18-dimensional necessary
space alone. The next source contradiction can therefore be stated narrowly:
prove the complete actual fibres 01023013 and 01023031 are both empty using
original geometry. At least one must be positive by (M).

## The other twelve patches

For each T_i, i=2,...,13 in the certificate's lexicographic diagonal-set order,
the hypothesis N01212(T_i)=0 already contradicts N01232(G)>0. This includes the
old fan-B as T6; there are eleven other new no-go completions. These twelve
cannot provide the designated original four-query certificate. This does **not**
classify their complete supports as K132.

Each nonnegative complete projection first forces every contributing z entry
to zero. The checker restricts B by these coordinates. When a relation
z_j=sum c_i z_i with c_i≤0 holds in that restricted space, all strictly negative
terms must vanish, since every actual count on both sides is nonnegative.
The certificate records the exact rational identities, signs and newly forced
coordinates until the whole original accepting functional vanishes. Each case
ends in a 15-dimensional linear restriction with original 01232 identically
zero. This is an exact necessary-domain no-go; no LP, full 56-rule screen or
exterior graph enumeration is used.

## The remaining diagnostic is not feasibility

For T0/T1, (O) restricts B to dimension 16. Sign propagation adds no zeros.
Every one of the original six strict positive row functionals
01012,01023,01203,01213,01231,01232 remains nonzero. This is a statement about
functionals, **not** a simultaneous nonnegative solution with all six positive.

The resulting possible support has 156 coordinates. For every such coordinate
and each of the three complementary palette splits, the checker finds at least
one compatible noncrossing boundary-component partition whose entire subset
switch orbit stays in that possible support. For W and W', in each of 02|13 and
03|12, exactly one of twelve partitions survives. All twelve partitions and all
literal subset-switch outputs are retained for these four narrow controls.
These partitions can have different witnesses for different palettes; no common
source colouring is asserted. An actual complete E colouring must use its own
one component partition, with complete components and all rootless attachments.
The diagnostic merely says that this particular support elimination adds no
new zero. Necessary-system feasibility and original-source realizability both
remain OPEN.

The complete original r6/933 source, a smaller bad graph, general 933 exclusion,
K-infinity and Lean are not produced. The concrete new result is a pair of
legal same-E k−2 competitors with exact full projections, a common two-fibre
obligation, and the minimum-source consequence (M).
