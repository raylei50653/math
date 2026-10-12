# Independent proof review

Reviewed `paper/cofacial_normal_form.md` as read and rechecked on 2026-10-12,
current SHA-256 `579054e712697c353834ea351e40df5b4b516310265148816ae5d8ad3179f08c`.
The recorded hash is unchanged: the initial review captured it after the
Section 1 correction had landed, while its scope comment still referred to
the earlier displayed draft. The follow-up verified the Section 1 scope correction and explicit exception
for original C5 frame edges in the embedding contract. Re-reading Sections
2-8 confirmed that the proof argument and conclusions remain unchanged.
The paper and external-theorem file were read only. The external theorem is
accepted here at the exact statement and applicability boundary documented in
`EXTERNAL.md`; this review does not independently replay its computer proof.

**Verdict:** no fatal mathematical gap found in the current normal-form proof
or its conditional transfer of Corollary 20 to general simple disk cells with
at most twelve internal vertices. The argument does **not** need completeness
of the old graph enumeration at five internal vertices. It needs soundness of
the necessary screens, the concrete witnesses, the finite relation
calculations, the stated topological arguments, and the cited external result.
The initial scope-wording concern is resolved in the current paper, as
recorded below.

## Exact dependency chain; no enumeration completeness assumption

Let K be the explicitly listed 132 relation masks. Independently recolouring
and checking disk planarity of each witness proves K is contained in K_{<=5}.
It does not presume the reverse inclusion.

The universal Kempe and exterior soundness arguments, followed by the finite
1023 -> 153 -> 142 calculation, put every disk relation in K or in the ten
remaining masks. The exterior argument uses only concrete disk witnesses for
K, plus 4CT after gluing; it does not require K to contain every small graph
relation. The ten outside masks all contain T4 and have independent singleton
support. The two orbit representatives are 933 and 941.

Independently, the 8,778 unions establish binary union closure of the abstract
finite set K. There is no claim that unions are represented by taking planar
unions of particular witness graphs. This distinction is sufficient for the
extremal argument.

If an outside source with n <= 12 existed, choose globally minimum n among
all sources with relation outside K, then maximize the number of edges. The
normal form supplies a triangulated outside source with that same minimum n.
The stated Corollary 20 then contradicts n <= 12. Thus K_{<=12} is contained
in K, and the inclusions

    K subseteq K_{<=5} subseteq K_{<=12} subseteq K

prove equality. No invocation of exhaustive enumeration appears in this
chain. In particular, one must not insert K = K_{<=5} as a premise of the
minimum-source selection; the current paper correctly defines outside using
the concrete finite set K.

## Identification and extremality

The temporary uv arc is inside a face and has distinct nonadjacent endpoints,
at least one of which is internal. Its contraction cannot identify two
boundary vertices or create a loop from an existing uv edge. Parallel edges
can be suppressed while retaining each original C5 edge. Interior-boundary
identification may produce chords, which the stated graph class permits.
The outer cycle and its vertex labels therefore survive. This is precisely
the closure needed for the extremal argument; a class that forbade all
boundary chords at the outset would require a different proof.

For each fixed labelled boundary assignment, the quotient colouring pulls
back to exactly the colourings with equal endpoints, and colourings of G+uv
are exactly those with unequal endpoints. The existential supports can
overlap, but their union is the entire source relation. Consequently, minimum
n puts the quotient relation in K. Union closure then forces the added-edge
relation outside K. It has the same n and more simple edges, contradicting
maximality. There is no use of jointly realizable witnesses for different
states or point pairs.

The maximum-edge choice exists even though embeddings are not enumerated:
for the fixed number of vertices the simple edge count is a bounded integer.
The selection must range over all outside relations. Choosing a minimum
representative for a fixed mask alone would be insufficient. The optional
minimum-|Sigma| intermediate choice is consistent and is not used by the
subsequent normal-form proof.

## Connectivity and repeated face walks

An outside relation is nonempty by the necessary-screen/4CT premise. A
boundary-free connected component can therefore be deleted and restored
with a colouring independent of the boundary. At a cut vertex z, every other
boundary vertex is in one component of G-z because the surviving part of C5
is connected. Any other component W contains only internal vertices.
Its existing colouring can be recoloured by one global colour permutation
to match any chosen colour at z. Deleting W preserves the entire relation
and decreases n, which is impossible.

This argument applies to the selected edge-maximal graph because it retains
the globally minimum n property. It establishes 2-connectivity before the
proof treats face boundaries as simple cycles. Thus bridges, repeated face
walks, and branches have not been silently excluded.

## Face triangulation and the apex separation step

For a bounded facial cycle F of length at least four containing internal x,
choose a nonconsecutive y. Cofacial completeness implies xy already exists;
since it is not a side of F it lies in the complementary closed disk on the
sphere. Choose u and v on opposite x-y arcs. The four vertices are distinct
and alternate x,u,y,v on F.

If either u or v is internal, cofacial completeness provides an edge uv.
It is not a side of F and is vertex-disjoint from xy. If both are boundary
vertices, the external apex supplies the vertex-disjoint path u-a-v. Its
interior is outside the original C5 disk and hence outside the bounded face
F. Both cases yield disjoint arcs joining alternating boundary points in
the same complementary closed disk, contradicting Jordan separation.
This successfully addresses the existing-diagonal-outside-the-face issue;
one is not simply adding a second copy of an existing edge.

If all vertices of a bounded facial cycle belong to the outer boundary, the
absence of boundary chords forces that cycle to be C5 itself. Its disk side
being a face leaves no internal graph, and connectedness gives G=C5, whose
relation is in K. The absence of chords follows for every outside mask from
T4 containment, since each C5 chord forbids the four-colour state whose only
repeated pair is that chord. Thus all bounded faces are triangles.

The apex is solely a separation argument, not a vertex added to the source
used in the size bound. The proof does not claim arbitrary graphs can be
triangulated on their existing vertices while preserving their full relation.

## The twelve-vertex consequence

For the resulting near-triangulation, V=n+5 and 2E=3(F-1)+5 yield E=3n+7
and F=2n+4. The dual therefore has 2n+4 vertices, one of degree five and all
others of degree three. Parallel dual edges are permitted by the stated
external theorem. The primal has no bridges, so dual loops from bridges do
not arise.

After a whole-graph D5 alignment to 933 or 941, singleton support is contained
in {2,4}. The state 01232 repeats exactly the pair {2,4} and is accepted, so
x_24>0. The fixed-boundary-assignment count identity gives x_24=m because
all singleton counts outside {2,4} vanish. The cited inequality and
sum(x)=5m+3sum(y) give m<=0. This is a contradiction, with no factor 4 or 24
introduced into fixed-assignment counts.

The external strict threshold 2n+4<30 is exactly n<=12 for integral n.
It does not cover n=13. Thus the general <=12 conclusion follows, while the
unbounded compression statement remains open.

## Scope wording: resolved

The original Section 1 sentence grouped the universal applicability of the
screen together with the finite mask computations. The current paper now
explicitly distinguishes:

- finite classification of the 1,023 nonempty ten-bit masks;
- the universal Kempe/exterior necessity arguments and their dependence on
  planar separation and 4CT;
- the finite relation calculations in items 2-4;
- the later topological and minimality proofs, which finite tests do not
  replace.

This fully resolves the trust-boundary concern from the initial review.
The embedding contract also now explicitly exempts the original C5 frame
edges from the requirement that edge interiors lie inside the disk; this is
the intended disk convention used throughout the proof.

For maximal explicitness Section 7 could apply the whole-graph D5 alignment
anew before using x_24. D5 closure of K and the explicit alignment convention
in Section 1 already justify that step. This remains an optional exposition
suggestion, not an unresolved proof obligation.

## Review boundary

This review checks the paper argument against the finite evidence and the
stated external theorem. It does not provide Lean formalization of arc
contraction, Jordan separation, duality, or external theorem correctness.
No outside source is supplied, and no finite control is treated as a
realization or as a proof of the unbounded theorem.
