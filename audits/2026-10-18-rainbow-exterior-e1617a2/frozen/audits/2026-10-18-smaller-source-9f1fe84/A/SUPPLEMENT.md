# The two fans partition the retained original full colourings

2026-10-18. This short supplement uses only A/PROOF sections 1–2 and the same
literal six-contact disk `(A,B,Q,L,R,N)`. No further enumeration is used.

Let F_A and F_B be the proper rim relations of the zero-centre fans at A and B,
and R_P the original two-centre relation. Then

`F_A intersect F_B subseteq { A,B,Q,N are four different colours }`,

so in particular `F_A intersect F_B intersect R_P = empty`.

Indeed A and B differ on the rim. If both fans are proper, L,R avoid both A,B
and differ from each other. Thus they are the remaining two colours. Q avoids
A,B,L (the fan-A chord AQ, original BQ, and original QL), hence Q=R. Similarly
N avoids A,B,R, hence N=L. The quartet A,B,Q,N is therefore rainbow. The old
vertex p cannot be coloured against this quartet.

The intersection contains exactly 24 literal rim tuples: choose the ordered
different colours A,B in 12 ways and order the two remaining colours as L,R
in 2 ways; Q=R and N=L are forced. This is a direct count, not evidence that
any such tuple has the actual source's full exterior extension.

For an original full colouring with A,B,Q all different, the pair cover is
therefore an **exact partition**: it restricts to precisely one fan, with the
branch selected by h=A or h=B. The deleted p is forced to the fourth colour.
Moreover the original (p,h) lift is unique for any liftable tuple on either
fan in this domain. The explicit inverse from A section 2 is consequently
bijective, giving the full-colouring identity

```
Colourings(G; row, A/B/Q all different)
  ≅ { chi in Colourings(G_A; row): A/B/Q all different, quartet not rainbow }
    disjoint-union
    { chi in Colourings(G_B; row): A/B/Q all different, quartet not rainbow }.
```

All other original vertices, including the whole exterior and the original
ordered boundary, are fixed by this bijection. For original 01232 the A/B/Q
condition holds in each of the four mapped source positions, so the identity
applies to its entire full fibre. It sharpens the existence cover without
excluding any of the candidates' additional rainbow colourings.

This does **not** imply `Sigma(G_A) intersect Sigma(G_B)=empty`. The same outer
row can be accepted by both graphs via different full rim tuples. In particular
the separate K132 supports still cannot be intersected as a substitute for
the common full-colouring relation. No smaller bad source follows from the
partition alone.

Independent root review: the integrated REPORT.md and check.py were read after
the active-f B source was added to root INPUTS.json. No substantive finding was
found. In particular, the two-row Kempe connection refinement uses the original
edge xy together with b's complete three-neighbour list in fan-A; it does not
join paths from different queried colourings.
