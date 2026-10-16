# Independent preliminary mathematical review

Research BASE: `120aae90cab8bc4881916adc598cf344f2f20f4b`.
The reviewer read the original J geometry, original-sector C4 theorem,
CAP A/B/C proofs, chorded-five proof, and the current double-W5 report.
This document preserves historical exploratory work; REVIEW.md records
the final accepted draft review. Its preliminary i>=4 calculation is
superseded by the accepted source-sector theorem i_odd>=5 and |C|>=15
in GEOMETRY.md and PROOF.md. No weaker number here is a current stopping
point or an alternative formulation of the final theorem.
No frozen input was edited and no external theorem was adopted.

## 1. Independent subcubic factor-critical lemma

Let K be a connected factor-critical graph of maximum degree at most
three and order greater than one. Then K has minimum degree at least
two and has no cut vertex. Indeed a degree-one vertex becomes isolated
when its neighbour is deleted. If v is a cut vertex, each component A
of K-v has even order, because K-v has a perfect matching. Each such A
requires at least two neighbours of v: if its unique neighbour were w,
deleting w would leave the odd nonempty set A-w with no edge to its
complement. Two components of K-v would therefore force degree at least
four at v. Consequently K is 2-connected.

Applied to the actual seven-cut component C, every cut endpoint in C
has internal degree two, and each other vertex has internal degree
three. There are exactly seven distinct such boundary endpoints.
The identity is about the same D[C]; tau=1 ensures that deleting f
has not deleted an internal edge. It must not be applied to arbitrary
replacement dual graphs as a source-realizability statement.

## 2. Disk and chord obligations

Diskhood is not automatic from cut size seven. If D-C is disconnected,
3-edge-connectivity and the singleton nature of every 3-cut allow only
two complementary components; at least one is a singleton with three
neighbours in C. That singleton is neither in X (its forced mate is
also outside C) nor a second H-S component (only f can join components),
so it is a vertex s of S. The set C union {s} then has a 4-bond boundary.
The original-sector argument excluding an X-avoiding induced C4 disk
can exclude this configuration. The final proof must state the interval
and f-placement arguments, rather than cite diskhood by cut size alone.

After diskhood, an internal chord of the simple heptagonal primal
boundary would give a bridge of D[C], because its two sides contain
nonempty sets of faces. The preceding 2-connectivity lemma excludes
all such chords, including the longer chords that do not form ears.
Exterior chords remain a separate issue and are not excluded by this
argument.

## 3. Historical small-case exploration, superseded by the sector proof

Let i be the number of primal vertices strictly inside the disk,
Iodd the number having odd complete J degree, and Bodd the number of
seven boundary vertices whose inward degree t=d_R-2 is odd. Let eps
record that m is a boundary vertex with odd t. Interior vertices avoid
all six pins: a forced-edge endpoint would contain a face of X, and
an endpoint of pq would put both endpoints of f in C, contrary to
common-111 saturation. Their complete degrees are at least five.

The complete monochromatic edge set is the three literal marked
edges together with every dual edge internal to C. Starting from the
three-marked parity vector Q=2, the weighted Euler formula therefore is

`Q=2+Iodd+Bodd-2eps`,

`L=Iodd+Bodd-2eps-10 >= 0`.

This is an arbitrary-size identity. It immediately gives i>=3. If
i=3, equality forces Iodd=3, Bodd=7, eps=0, L=0, so all three interior
vertices have degree five. The disk edge count is

`Eii+Eib=3i+7-3`, `sum d_J(interior)=2Eii+Eib`.

Hence Eii=2 and Eib=11, not Eii=3 and Eib=9. The interior graph is a
three-vertex path A-B-C. Each positive inward degree is odd and at
most three, so exactly two boundary vertices u,v have inward degree
three and the other five have inward degree one. Both u and v are
adjacent to A,B,C. Faciality of the four triangles uAB,vAB,uBC,vBC
closes the complete link of B as A,u,C,v,A. Thus d_J(B)=4, contrary
to degree five. This excludes i=3, and the valid resulting bound is

`i>=4`, `|V(C)|=2i+5>=13`.

The final source-sector argument strengthens this independently checked
preliminary bound. The face interval at m can meet only one original
sector. Its C block has length t_m+1, and each other one-block is a
singleton. The endpoint zero faces consequently give
`d_G(u)-3=2k_u+t_m+2` in the affected sector and `2k_u` in the other.
If t_m is even, both source degrees are odd and at least seven, so
`d_J(m)>=9`; m has odd parity, whose minimum is seven, and L>=2.
If t_m is odd, eps=1. When m is outside the disk, both sectors again
give odd source degrees at least seven and L>=2. Therefore
`L+2eps>=2`, so `Iodd+Bodd>=12`, `Iodd>=5`, and
`i>=5`, `|V(C)|>=15`. This uses the original source sectors, not an
extra condition on arbitrary synthetic disks.

## 4. Synthetic lower-bound calibration

The following is a local calibration, carrying no original-source claim.
Take boundary `(u,d1,d2,v,c1,b2,b1)` and the thirteen disk faces

`ABC, ACv, AvD, ADu, AuB, Du d1, Dd1 d2, Dd2 v,`
`Bu b1, Bb1 b2, Bb2 C, Cb2 c1, Cc1 v`.

The four interior vertices A,B,C,D have complete disk degree five.
Their induced graph is triangle ABC with pendant edge AD. The inward
degrees on the boundary are `(3,1,1,3,1,2,1)`. The face-adjacency dual
has 13 vertices, 16 edges, seven degree-two vertices and six degree-three
vertices. A direct recursive perfect-matching calculation verified all
13 single-vertex deletions. Thus the bound i>=4 is sharp under these
local disk, factor-critical and weighted-curvature conditions alone.
This patch has no declared six-pin geometry or source completion.
Its presence only prevents an unsupported stronger local exclusion.

## 5. Matching-interface review obligations

The family in each claim must remain all of the same nonempty P111.
Tightness of the C cut for all those matchings does not quantify over
all perfect matchings of D. Factor-criticality supplies a near-perfect
matching after every vertex deletion, but does not by itself supply
an even complement or a particular globally compatible entry edge.

A finite interface recording pairings must retain each actual complete
matching lift and empty interface fibre. Pairing topology, parity and
one odd-cycle indicator can be a finite key for an existence question;
they are not a bijection with complete colour fibres or full matchings.
Any claimed interface count must specify which keys are syntactically
possible, which are geometrically feasible, and which actually occur
on the original C. A bound on keys does not bound |C| or prove a source
reduction. The remaining geometry and complete-319 claims stay OPEN.
