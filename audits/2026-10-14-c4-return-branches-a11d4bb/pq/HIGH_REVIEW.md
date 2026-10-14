# Independent review of the high-r exterior quotient step

Decision: **PASS for the new arbitrary-size source argument.** This review
reads the direct t-deletion setup and local tables in
[r_high/PROOF](../r_high/PROOF.md), its checker, and the frozen original
SOURCE_GEOMETRY nonedge statement. No source search or broad replay was
performed. Only this file in the pq-owned directory was written.

## 1. Source geometry and exact size

In the fixed original `d_G(x)=d_G(y)=d_G(b)=4` failure branch, R has
induced outer C4 `(z,s,r,t)`. Thus zr is absent as an actual graph edge,
not merely rejected in an abstract colouring relation. Under t=5 the
literal deletion V=R-t has outer `(z,s,r,w,h)` and k total vertices.
The retained z and r are distinct and still nonadjacent.

Identify z,r along an arc in V's exterior, then suppress every parallel
edge pair. This is a loopless planar graph J with exactly k-1 vertices.
No loop arises because the identified endpoints were nonadjacent. Parallel
suppression is harmless for proper colourings: all suppressed copies have
the same endpoint pair, so a colouring of J lifts to a proper V colouring
with z=r. Extra original common neighbours, if any, do not invalidate this
statement and do not need the stronger original common-neighbour theorem.

Choose an edge of J, add three new vertices forming an exterior path of
length four between its endpoints, and retain the edge as the fifth side
of a new outer C5. Designate the thin new face as exterior. The resulting
graph has k+2 total vertices and k-3<k interiors. This is precisely the
source-minimality colourability construction already used in ADJACENT4.
Its catalogue relation is nonempty, so restriction colours J and the
quotient lift gives a complete colouring of the same V with z=r.

This establishes one full-colouring witness from a smaller legal source
comparison. It does not assert fibre equality with J, any catalogue
representative, or an independently coloured second graph.

## 2. Exact row consequence

Normalize that whole V colouring in one common colour frame. Its proper
outer C5 has z=r=A and s=B. The only three restricted-growth words are

`ABABC`, `ABACB`, `ABACD`.

The direct all-t-lifts table makes the first two complete marked fibres
empty. Therefore the third row must occur:

`F_V(ABACD) is nonempty`.

Its actual pq palette must be CD (both orders are allowed by the local
screen), and its unique t lift has t=B. The conclusion refers to the
complete original V colouring, with the original p,q colours untouched.

Among the ten generic masks after the necessary Kempe closure,

`424,440,632,956,960,976,1000,1012,1016,1020`,

exactly `956,1012,1020` contain the ABACD bit (bit2). This is an arithmetic
screen, not a representative substitution. Thus the quotient argument
reduces the live generic frontier to those three masks.

## 3. The alias is genuinely excluded

When h=p, equivalently original a=4, the previous direct screen leaves
only exact support424. That mask has none of ABABC,ABACB,ABACD. It therefore
contradicts the quotient colouring above. The calibration graph carrying
the six-pin support424 has a zr edge, so it cannot supply the legal z=r
quotient. This explains exactly why it was only a non-source control.

The source consequence is

`a=4 ==> d_G(t)>=6`,

and the literal reflection exchanging `(x,y),(a,c),(p,q),(s,t)` gives

`c=4 ==> d_G(s)>=6`.

Both use the same original target-failure hypothesis and fixed branch.
They apply to all three retained Sigma cases932,933,941; no rotation of
the original singleton-fibre conditions is involved. There is no general
claim that p,q have high degrees or that every high-r source is excluded.

## 4. Publication consistency

The ten-mask generic screen and the mask424 alias should remain described
as intermediate finite controls. The final live generic frontier is the
three-mask set; the alias424 source subdomain is empty. Retain its full
finite calibration fibres as historical non-source evidence, and distinguish
the paper quotient-colourability step from the bounded terminal calculation.
The r=7 C6 support calculation and its OPEN source realizability boundary
are unaffected by this additional lemma.

The updated r_high/PROOF was subsequently read. It now states the three
live generic masks, labels the mask424 statement as pre-quotient, and
records the genuine alias exclusion. These final prose claims agree with
the argument reviewed here.
