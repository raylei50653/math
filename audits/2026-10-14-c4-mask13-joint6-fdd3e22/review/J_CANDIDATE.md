# Unadopted direction: a second quotient

Status: **UNADOPTED; pending a complete independent endpoint and embedding
review.** This note records a possible next direction. It is not an input
to the adopted conclusions of this audit.

The common-neighbour equality and the identity of J as a triangulation
have since received their own adopted proof in
[SOURCE_GEOMETRY section 2](../SOURCE_GEOMETRY.md). That document is the
authority for those two facts. The separating-triangle classification and
subsequent deletions below remain unadopted.

Use all original source hypotheses and names from the frozen triangle-core
audit: S has no separating 3/4-cycle, every 5-cycle has a side with at most
one vertex, and minimum degree at least five. The original boundary is
(x,y,a,b,c); u is its cap vertex. Here x,y,b have S-degree exactly five.
R is the smaller C4 disk with boundary (z,s,r,t), where z identifies a,c.

## Candidate common-neighbour lemma

One expects N_R(z) intersect N_R(r)={s,t}. For an additional common
neighbour w adjacent to original a, consider the S-cycle

    (u,a,w,r,x).

At u its sectors contain y on one side and b,c on the other. These
vertices are absent from the cycle, since w and r are original inner
vertices. The five-cycle rule forces the y side to be the singleton y.
Then degree at least five forces N_S(y)={u,a,w,r,x}, so w=t by the known
degree-five link of y. A common neighbour attached to original c gives
w=s using (u,c,w,r,y). Each original neighbour of z comes from a or c.

This would show that identifying z,r across the exterior and suppressing
parallel edges removes exactly the two facial pairs at s,t. Let the merged
vertex be h. The resulting graph J would be a simple sphere triangulation
on k vertices. Its degree formulas would be

    d_J(h)=d_S(a)+d_S(c)+d_S(r)-10 >= 5,
    d_J(s)=d_S(s)-2 >= 3,    d_J(t)=d_S(t)-2 >= 3,
    d_J(p)=d_S(p)-1 >= 4,    d_J(q)=d_S(q)-1 >= 4,

with all other degrees unchanged from S and at least five. As always,
parallel-edge suppression cannot be restricted to the displayed two
pairs without first proving the common-neighbour lemma.

Every J colouring lifts to an R colouring with z=r. Since ABAC is absent,
it must have s=t, and the joint failure condition says that this common
colour is the colour missing from the facial triangle hpq. Source
minimality gives nonemptiness, but does not immediately give a colouring
breaking this constraint.

## Candidate separating-triangle classification

The tentative claim is that every nonfacial triangle of J is the neighbour
triangle of s or t, and occurs only when that vertex has J-degree three.

A triangle avoiding h comes from S. For hvw, if v,w share a preimage
among a,c,r, the original triangle is facial. A genuinely mixed a/c
triangle is controlled by the old triangle-core classification: after
removing b,x,y its only retained exceptional image is the now facial hpq.

For a genuinely mixed a/r triangle, choose v adjacent to a and w adjacent
to r with no shared preimage. The cycle

    (a,v,w,r,y)

has, at y, a sector containing t and the other sector containing u,x.
The genuinely mixed condition excludes t from v,w, while the R vertex
set excludes u,x,y. The small-cycle rule would therefore isolate t as
the singleton side. It would force

    N_S(t)={a,v,w,r,y},    N_J(t)={h,v,w},    d_J(t)=3.

The c/r case is symmetric, using (c,v,w,r,x) and isolating s. Cases where
one endpoint is the other common neighbour need to be checked explicitly;
some would force the already forbidden edge st and hence cannot occur.
The reverse direction also needs its size and nonfaciality checked.

If this classification is confirmed, deleting whichever of s,t have
degree three should remove all separating triangles. This would produce
a still smaller four-connected triangulation with one or two forced
vertex/face-colour obligations, depending on the degree branch. It is not
yet an exclusion: the relative source hypothesis only supplies the
particular colourability statements already justified by smaller C5
constructions, not a universal vertex/face extension theorem.

The full case audit, original rotations, exceptional endpoints, the
degrees after any subsequent deletions, and exact complete-colouring
maps remain obligations. None is discharged by this note's plausibility.
