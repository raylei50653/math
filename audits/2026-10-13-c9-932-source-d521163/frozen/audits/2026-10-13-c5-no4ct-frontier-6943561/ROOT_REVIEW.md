# Independent review: W5 prerequisites, terminal closure and C9 budget

2026-10-13. Reviewed the current [W5 proof](w5/PROOF.md),
[terminal proof](terminals/PROOF.md), [terminal checker](terminals/check.py),
and [C9 geometry §6](c9/geometry/PROOF.md). No producer, certificate, old
evidence or shared documentation was edited by this review.

**Paper review PASS.** The new claims below retain the globally smallest
catalogue-outside source contract and the exact no4ct size restrictions.
The review does not certify any surviving C9 necessary support as a source.

## W5 prerequisite integration

A proper original C4 or C5 cycle uses an original inner vertex, since B
is induced and the only cycle on its five vertices is B itself. Original
B vertices cannot lie strictly inside a proper cycle: they remain on the
outer face of the original plane disk. Thus its cap has s<=k-i(C)<k.
The restricted C4 and smaller C5 representatives are legitimately applied.
Replacing the cap at the same named cycle preserves all literal extension
truth values; its new inner count is exactly k-s+s'. This gives s<=3 or
s<=5 without assuming universal C4 representability.

For 2<=s<=5 every private cap vertex must touch its rim, or its degree
would be at most s-1<=4. Hence the private induced graph is outerplane,
including the disconnected case; its edge bound 2s-3 contradicts Euler's
required 2s-b+3+q for b<=5. The single-vertex C5 case is exactly W5; the
C4 case is impossible. No colorability theorem enters this step.

The five double attachments to B are exactly the five actual facial
apices: short C4 exclusion forbids nonadjacent attachments, and an extra
point on an original B edge creates an occupied triangle. Therefore
|L1|=D_B-15. Subtracting the first-layer five-degree count from
n5=D_B-14+X yields precisely 1+X+h1 deep five-degree vertices. The proof
distinguishes h1 from original boundary excess h_B.

A chosen deep vertex has exactly five original inner neighbors. Its
incident triangular faces form its actual star disk. A neighbor chord
would form a triangle through the center whose bounded side contains a
nonempty open neighbor arc, contrary to occupied-triangle exclusion.
This verifies the induced W5 and all ten distinct original B/U pins.
The integration includes 932 and assumes no nonempty singleton support.

## Arbitrary-size terminal T0 and exact 64-shape coverage

In one zero-single-attachment side, the original structural theorem gives
the actual rim (endpoint,four named t vertices), all original inner
vertices. It has s_cap<=k-5<k. Terminal ear counting gives a nonempty
interior, so the proper C5 cap theorem forces the literal W5. This works
when the other side has arbitrary size and arbitrary single attachments.
It is a paper closure of that side, not an inference from bounded data.

When both sides have zero single attachments, all private vertices are
the two actual centers. PINCH has eight t, one shared endpoint and two
centers (m=11); BRIDGE has eight t, two endpoints and two centers (m=12).
The classified Q outer walk leaves no other region in which private
vertices could occur. There are exactly four opposite C pairs, two
shapes, and eight original collars. Private BRIDGE endpoint names may
be fixed once by clockwise side ownership; their opposite naming is
not an additional original shape. This verifies exhaustive 64-shape
coverage rather than merely 64 successful finite controls.

The original six-point J is induced and its terminal patch has five
private vertices, 24 edges and 14 triangular faces. Its center-color
formula retains every spoke, rim edge and endpoint inequality. The
full separator join fixes the same J colors in the original graph.
The skeleton stores one shared PINCH endpoint and the actual BRIDGE
edge, so separately feasible endpoint copies cannot be combined.

The complete 64-graph replay gives Sigma=1023 for all ten original B
rows in every graph. Together with the exact shape coverage this
excludes s=0 for PINCH/BRIDGE, and yields their respective bounds
m>=12 and m>=13. It does not exclude a single zero-side terminal
attached to an arbitrary larger other side.

## Narrow RING R0 and C9 Euler boundary

For RING p=s=0, Q has the actual simple outer T8 and boundary Q-degree
at least three. A short T chord cuts off an empty C3/C4 cap and a
nonendpoint degree-two ear. An opposite chord cuts Q into two actual
proper C5 caps; each must be W5. Then all private vertices are the two
centers and m=10. Consequently m>=11 excludes every T chord. This
argument gives induced T8 only in this precise zero-single-attachment
RING subdomain, and transmits neither degree four nor a repeated C8
collar contract.

C9 §6 uses E(H)=3m+2n-3 and the exact decomposition into n cycle
edges, c chords, j private edges and s attachments. Consequently
sum_C(d_H-3)=3m-3-j+c is correct. In the induced-boundary branch each
original boundary edge has its third point in I. The consecutive
neighbor paths in I meet through these third points, and all other
I components would have to attach to this union. Thus I is connected
and j>=m-1. In the one-ear branch the isolated ear center is separated
by its original chord; the chordless residual C6 has a connected
private graph, and its sole-center case violates long-arc Y-degree.
The optional m>=3 bound is sound and explicitly weaker than k>=16.

## Executed finite evidence and trust boundary

Executed `python3 -B terminals/check.py --check --negative` from the
parent audit directory. Result PASS: 64 graphs, 640 complete original
B fibers, 61,752 full lifts; 4,096 terminal fibers, 744 terminal lifts;
three semantic negative controls and two archive corruptions rejected.
This is a replay of the producer's complete graph/direct/join comparison.

Separately rebuilt the terminal's 24 edges directly from its rim,
spokes and C-half-arc attachment description; did not import the
producer. A fixed-order global DFS over all eleven named vertices
rebuilt all 4,096 literal J fibers, including empties, and compared
each complete private lift list with the v2 archive. Result PASS:
3,652 empty literal fibers, 732 proper J rows with histogram
288 empty / 144 single-lift / 300 double-lift, and 744 full lifts.
The proper literal row 010102 was independently empty.

These checks support the new finite atom and its complete joins.
The arbitrary-size premises are established by the paper proofs above.
Inherited source classification and earlier bounds retain the parent's
existing external trust dependencies; this review adds no new external
paper theorem and no Four Colour Theorem premise. No Lean theorem or
general source exclusion is claimed. Independent C9 finite rechecking
is recorded separately by the parent audit.
