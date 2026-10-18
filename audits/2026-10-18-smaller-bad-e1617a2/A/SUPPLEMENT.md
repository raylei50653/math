# A supplement: a three-candidate cover retaining an actual accepted witness

BASE `e1617a2756813327d7ad333cfdd0fd92fa9efc38`, with the preceding
uncommitted audit frozen separately in the parent INPUTS. This uses the
full original `(p,h)=(p,ell)` source verified in [B/PROOF](../B/PROOF.md),
including its complete original links, original degree-four b, facial
triangles, and the actual interior rim vertices. It does not assert that
every remaining source has this site or transport that geometry to an
unverified different centre position.

Fix the following three completed graphs once and for all:

```
Q_1 = (G-{p,h})/(n=b, R=q),
Q_2 = (G-{p,h})/(n=b, L=b),
G_B = G-{p,h} with fan edges bn,bL,bR.
```

The Q_i constructions are the two successive cofacial operations proved
in B Sections 4–5: first delete p and identify n with b; then delete h
and identify one opposite pair in the actual quadrilateral face qLRb.
The two second choices are separate graphs. The indicated equality
classes are independent, so simplification removes parallel copies only,
not loops. The original ordered outer cycle `(x,y,a,b,c)` is retained in
all three graphs. Every exterior edge and attachment is carried by its
literal quotient map or retained by the fan constructor.

Their final completed interior counts are respectively

```
k(Q_1)=k-4,  k(Q_2)=k-4,  k(G_B)=k-2.                 (S1)
```

There is no later hub, boundary, or private-vertex restoration cost.

## Full-colouring acceptance cover

Take **any one full original** `01232` colouring psi. The preceding
paired-rejection proof partitions its actual values into

```
(h,n)=(a,b)  or  (h,n)=(b,q).
```

This is a partition of complete original assignments; it is not a choice
of separate marginal pin values. In the literal frame put `q=t` and
`p=s=1-t`, where t is 0 or 1.

If `(h,n)=(a,b)`, then `a=c=h=2` and `b=n=3`. The original edges force

```
(L,R)=(3,s), (3,t), or (s,t).
```

In the first case L=b, so the unchanged full assignment descends to
Q_2. In the last case R=q, so it descends to Q_1. In the middle case
both equalities hold, and it descends to both. All quotient classes have
equal values in this same psi, so every retained edge remains proper;
all original outer colours are unchanged.

If `(h,n)=(b,q)`, the same psi restricts to G_B. Its original h-edges
certify the new edges bL,bR, its h-n edge certifies bn, and all other
candidate edges already belonged to G. Again the whole exterior and all
original outer colours are retained.

Therefore

```
F_01232(G) nonempty
  => F_01232(Q_1) nonempty
     or F_01232(Q_2) nonempty
     or F_01232(G_B) nonempty.                         (S2)
```

More strongly, every original accepted full assignment has the explicitly
given image in at least one of these fixed graphs. This is a cover, not
a bijection or disjoint union: the h=a middle case has two images, and
a candidate may have additional accepted colourings with no old lift.

Using G_B as the third member matters. The diagnostic k-3 graph S from
A/PROOF also covers the old h=b sector, but its complete degree-three
b-neighbourhood directly prevents the stated four-query certificate.
The three-member family here avoids that particular immediate no-go;
it does not assert that any member is bad.

## What is still required on the accepting member

The accepted witness and its candidate are now supplied by (S2), without
assuming fan-B alone accepts. A successful smaller-bad proof must show
that **one of the accepting members** also rejects all three queried
rows. For Q_1,Q_2, B Sections 7–8 give every old lift and the exact
remaining equality fibres. For G_B, the frozen preceding audit gives
every old lift and the three remaining rainbow fibres. These are
different candidate relations and cannot be joined as if they were one.

No such simultaneous three-row exclusion is established here. Nor does
the cover show that an accepting member has a different outside-K132
certificate. The output is a concrete fixed finite family of actual
smaller original-boundary graphs with a proved full-witness acceptance
cover, together with an explicit unresolved badness obligation.
