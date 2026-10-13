# Independent C8 attachment and equality review

BASE `6cafdfb02fe5892a49eee21f92aea2369a25c022`; source contract is the original
globally vertex-minimal, edge-maximal disk-C5 source with h=3 and one of the eight
accepted C8 residuals. This review adds no edge-critical, Gallai, or N2 premise.

## Paper argument checked

Let C be the original induced C8 collar and H its inner disk. Every C vertex has
H-degree at least four, and every strict inner vertex has degree at least five.
The already accepted original-cap statements say that a simple C4 encloses no
vertices and a simple C5 other than B encloses no vertices or precisely one wheel
center with its five incident faces.

If x strictly inside C is adjacent to C vertices at cyclic distance two, x and
the short C arc form an original C4. Its empty triangulated cap cannot have a
C-C diagonal, so it contains the diagonal from x to the middle C vertex. The two
resulting original triangular faces fill that middle vertex's entire inner
sector, giving H-degree three, a contradiction.

For cyclic distance three the analogous original C5 cap is either empty or the
single wheel. In the empty case the only permitted triangulation is the fan from
x; either middle C vertex has H-degree three. In the wheel case the two middle C
vertices have only their two C neighbors and the wheel center in H, again degree
three. The caps lie inside H, and their arc-middle vertices have no further inner
sector outside the cap. Thus each x has at most two C neighbors: the graph on C8
whose allowed pairs have distance one or four is triangle-free.

The eight original C-edge third vertices t_i are distinct. Equality of third
vertices from different edges would give at least three distinct C neighbors.
For Q=H[I], every Q vertex has degree at least three because it has at most two C
neighbors. If all Q vertices met C, all would be on Q's common outer face, making
Q outerplane of minimum degree at least three, impossible. Hence |I|>=9.

When |I|=9, exactly the eight t_i meet C, each precisely twice. There are sixteen
C-I edges; therefore every C vertex has H-degree four and the t_i form a simple
cycle T in their original cyclic order. Its annulus to C is completely determined
by the original C vertex links. The sole remaining vertex r lies inside T.

Suppose T has a chord. The chord side not containing r is an empty triangulated
polygon. It has an ear away from the chord endpoints: for a triangle this is its
middle arc vertex; for a larger polygon two adjacent vertices cannot be the only
ears. That ear's entire inner Q sector is in this polygon, so its Q-degree is two,
contrary to the minimum-three bound. There are no T chords. Triangulation now
forces all eight r-t_i edges, so Q is precisely W8. No subdivisions, extra bridges,
private components, or attachments remain unaccounted for.

## Independent finite check

`INPUT.json` hashes the prior `RESULTS.json` bytes, saved as
`RESULTS.frozen.json`. The independent checker constructs all eight graphs from
the prior *literal collar edges and named cyclic order*, rather than the primary
checker's extras formula. It adds exactly the forced sixteen C-T edges, eight T
cycle edges, and eight center spokes. It checks the primary vertices, named pins,
edges, oriented faces and induced rotations. Its coloring search has a fixed
order r,t0,c0,t1,c1,...,t7,c7, separate from the primary minimum-domain search.

Every full lift on all 22 original named vertices is compared literally for each
of the ten fixed outer rows. All eight full relations are 1023. The source target
remains `not triggered`; exclusion follows from the complete paper uniqueness
reduction plus complete finite relations, not zero target sightings.

Normal and seed-17 independent runs agree. Independent negative checks reject a
deleted full lift, a deleted original edge, and a missing query. This establishes
the conditional h=3 bound k>=18 when joined to the eight accepted source
contracts. It does not exclude those eight unbounded contracts, change h>=3,
prove general K bounds, or add a Lean theorem.
