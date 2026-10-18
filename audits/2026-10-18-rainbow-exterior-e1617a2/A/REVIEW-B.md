# A independent review of B

Reviewed B/PROOF.md against the frozen smaller-source C proof,
A supplement, and active-f B proof at BASE
`e1617a2756813327d7ad333cfdd0fd92fa9efc38`.

## Mathematical findings

No substantive mathematical defect found in the paper implications.

* The boundary-anchored gate-pair lemma uses one actual full colouring,
  its actual maximal component, and the same original rejected row.
  Four gate pairs have actual candidate edges, and the two remaining
  pairs are exactly `(a,q)` and `(q,n)` for the stated `(p,ell)` site.
* All five rainbow sectors are retained. For `01202` the q/n palette
  has only boundary vertex y; for `01212` it has only x. Thus distinct
  q/n components leave one unanchored and give the forbidden old lift.
  For `01021`, original qc correctly anchors q's 13 component at c,
  while a distinct n component must reach y. The 03 contact uses the
  literal two boundary vertices a,x. The palettes of these nonautomatic
  components exclude b, so all their edges are original surviving edges.
* An old-liftable accepted fan-B colouring has `q=n=t` and
  `{L,R}={2,1-t}`. Its complete b-neighbour set has exactly one vertex
  of colour `1-t`, namely Z. This remains a statement about a set if
  an added edge duplicates an exterior edge; suppressing the parallel
  copy does not remove its adjacency. The forced b-to-anchor component
  therefore yields the stated original-edge path after deleting b.
* The additional genuine-eight-gon hypothesis in Section 6 is stated
  explicitly. Under that hypothesis the Z-to-anchor path has no other
  boundary vertex in its palette, so it is a proper crosscut. Inspecting
  the given cyclic order places q,n on opposite arcs for all four
  endpoint choices. The complementary `{2,t}` palette is vertex-disjoint
  from the crosscut, proving the conditional separation. This argument
  does not establish the eight-gon hypothesis for the actual source.
* Section 7 retains fan-B acceptance, all three full-fibre exclusions,
  and applicability of the conditional geometry as unresolved. The
  accepted path is not combined with a path from a rejected colouring.

## Scope correction resolved

The first draft's Section 2 heading and Section 7 opening could be read
as excluding every possible smaller-bad use of fan-A. The proved result
excludes the **specified four-query certificate**, which is sufficient
for being outside K132 but has not been shown necessary for arbitrary
candidate supports. I requested that those phrases, including the claim
that all work producing a smaller bad graph must use fan-B, explicitly
refer to this four-query route. This does not change the mathematical
proof or the remaining three-fibre target.

The revised B proof was reread at those passages. Its Section 2 now
explicitly leaves a different outside-K132 certificate possible, and
Section 7 limits the fan-A obstruction to the specified four-query
certificate. The scope correction is resolved.

No source example, finite-table check, independent realization assertion,
four-colour theorem, or new Lean authority is supplied by this review.
