# Independent review of the small-cap and induced-C8 proof

Reviewer scope: read-only review by the classification worker, independent
of the geometry author. Reviewed `../geometry/PROOF.md` against frozen
`docs/c5_saturation_degree_bound.md` §§1–4 and frozen old
`COVERAGE.md` §§1–2. This is a paper-argument review, not a Lean proof or
replay of the inherited external computation.

Reviewed geometry proof SHA256:
`ca4f8d8a07bdc9ee2906568a9028ac11d83bbf11e9e8173f8d0c94cef34dfdaa`.

Verdict: **accepted with the explicitly stated inherited source and
catalogue hypotheses**. No mathematical issue requiring a change was found.
It proves a universal exclusion of the subdomain with a C8 chord for each
of the ten residual queries; it does not exclude any complete query.

## Cap replacement and the quantifier on minimality

The source minimizes original-B interior vertices over *all* relations
outside K, not just over a fixed target or saturated graphs. The frozen
source explicitly supplies this global quantifier. Replacing a disk bounded
by Q with a representative having the same complete Q relation preserves
the existence of each full coloring in the original common literal frame.
This remains true when Q shares some named vertices with B. The condition
that no B vertex lies strictly inside the replaced disk ensures no B label
is deleted. Other replacement vertices receive fresh identities.

The replacement need not preserve extension multiplicities, degree bounds,
or maximal edge count. Strictly reducing the primary minimum is sufficient.
Removing a duplicate boundary chord preserves proper-coloring existence
and planarity. The old general C4 representative bound applies even with
boundary chords; it is not restricted to induced C4 sources.

For an entirely internal C5, the cap has fewer strict interior vertices
than the original G: the five Q vertices already count as original interior
vertices but not as cap interior vertices. Thus the cap relation belongs
to K before its at-most-five representative is used. This avoids assuming
that an arbitrary C5 source already has a small representative.

## Euler and the outerplane argument

For a triangulated disk with b boundary vertices, k strict interior
vertices, q boundary chords, and m edges induced by the strict interior,
Euler gives `E=3k+2b-3`. Counting edges incident to the strict interior gives
`sum deg = E-b-q+m = 3k+b-3+m-q`. Every such vertex has its complete
original-G neighborhood in the cap, so its degree is at least five.

The C4 inequalities for k=1,2,3 are strict. For a C5 with 2≤k≤5, the step
asserting that the induced interior embedding is outerplane is sound:
Q is outside every bounded face of that induced embedding. A vertex not
incident to its global unbounded face cannot have a Q neighbor without
crossing the induced embedding. It would then have degree at most k−1≤4.
This reasoning also handles disconnected induced subgraphs and one
component lying inside a bounded face of another. Consequently all
vertices are on the global unbounded face, and the standard simple
outerplanar bound `m≤2k−3` applies for k≥2. Its contradiction with
`m≥2k−2+q` is exact. The cases k=0,1 are separately correct; k=1 requires
all five spokes and leaves no room for a boundary chord.

## Chords, sectors, and ears

Each C8 chord has shorter cyclic distance 2, 3, or 4. Its short-side cap
contains no original B vertex. Every non-endpoint vertex of that short
arc has its *entire* H-interior sector on that side of the chord. Thus the
degree calculated within the cap is its actual H degree; the proof does
not accidentally ignore neighbors on the other side of the chord.

Distance two is excluded by the empty separating-triangle side and H
boundary minimum degree three. Distance three gives an empty triangulated
quadrilateral, whose single diagonal can meet at most one of the two
short-arc middle vertices. Distance four yields two pentagonal caps. An
empty triangulated pentagon has two nonadjacent ears. The chord endpoints
are adjacent along that pentagon, so at least one ear is a middle vertex.
The resulting degree two is impossible. Both sides must therefore be W5.
All six non-endpoint C8 vertices then have H degree three, while at least
one of the three distinct private y vertices is not a chord endpoint.
Its required degree four gives the contradiction.

The ear argument only uses polygons of length at least four, so the
three-vertex exception to a generic nonadjacent-ear formulation is absent.
No count vector, Kempe support, or finite search is needed for this proof.

## Boundary face rotation and curvature

After chordlessness, each boundary edge's inner triangular-face third
vertex lies strictly inside C8. If the two third vertices at a boundary
vertex v agree, the two original facial triangles on its boundary edges
meet along the same v-to-interior edge. Their being actual faces leaves
no extra neighbor in v's interior rotation sector. Hence deg_H(v)=3.
Conversely, degree three gives one interior neighbor, used by both faces.
The private vertices, having H degree at least four, must therefore have
distinct neighboring third vertices. This is a statement about one fixed
embedding, with no selection of separate rotations across colorings.

The Euler curvature formula and its split into five apex degree-three
baselines and three private degree-four baselines are correct. Strictly
interior degrees are at least five, so the formula proves at least one
strictly interior degree-five vertex. It does not imply a coloring escape.

## Accepted boundary of the result

The representative and minimum-degree statements retain the frozen
universal screen, catalogue and external-theorem dependencies. They are
not re-proved by this review. The new paper argument is otherwise valid
for arbitrary finite source size. It excludes the chorded subdomain,
including the conditional `a1-a4` chord option observed by the saved
c16/c32 positive supports. The degree and cap argument alone does not
exclude a complete query. The subsequent
[cofacial quotient proof](QUOTIENT_PROOF.md) adds the four-color existence
requirement and excludes c16-941 and c32-941.

The exact unproved next implication is that a chordless triangulated H
with these complete degrees, boundary face identifications, attachments,
and all-source minimality cannot realize the required complete ten-row
outer relation. The accepted theorem alone does not supply that implication.
