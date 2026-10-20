# A. Two completed k-3 constructions and the remaining badness gap

Date: 2026-10-18. BASE `e1617a2756813327d7ad333cfdd0fd92fa9efc38`.
The prior turn's uncommitted rainbow audit is a separately identified
frozen input in the parent INPUTS; it is not silently attributed to BASE.
This paper uses that frozen A/B proof and the frozen smaller-source C
proof. No prior audit is modified.

The user requests a smaller **bad** source, not merely another candidate.
The constructions below are actual smaller plane graphs with exact
full-colouring maps. Neither construction is proved outside K132. H
rejects its own accepted query `01232` by the exact ear-insertion map;
S has a complete degree-three boundary neighbourhood that prevents the
previous four-query certificate. Their purpose here is to
make the attempted reduction concrete and isolate the still missing
implication, including a planar alternative to the crossing double
identification. This paper does not report the user goal as completed.

## 1. Fixed original source and every vertex cost

Use the original `(p,h)=(p,ell)` site and ordered boundary
`B=(x,y,a,b,c)`. The actual complete links are

```
N_G(p)=(a,b,q,h,n),
N_G(h)=(p,q,L,R,n),
N_G(b)={a,c,p,q},
```

with original qc present. The two-star disk has actual simple rim
`(a,b,q,L,R,n)`. The original graph has `k+5` vertices, with p,h interior.
All original triangles are facial, as in the frozen construction. The
two fixed fans delete p,h and add respectively `aq,aL,aR` or `bn,bL,bR`.

The original full fibres for `rho_0=01202`, `rho_1=01212`, and
`tau=01021` are empty, and `alpha=01232` is nonempty. All assignments
below use the literal palette `{0,1,2,3}`. No colour quotient replaces
a complete fibre.

## 2. A smaller disk obtained by changing the boundary vertex

Let

```
H = G_A - b,
B_H = (x,y,a,q,c).
```

This is a plane C5 disk, with its displayed boundary explicitly changed
from the original one. In the actual fan-A embedding, triangles abq and
bqc are the two faces incident with boundary b. Its complete neighbour
set is `{a,q,c}`. Deleting b replaces the boundary segment a-b-c by
a-q-c, with q an original interior vertex distinct from x,y,a,c. Thus
the new boundary is simple and bounds the remaining graph. No interior
exterior edge is dropped beyond the three edges incident with b.

The final graph has `k+2` vertices and five boundary vertices, hence

```
k(H)=k-3.
```

Global minimum badness ranges over all plane C5 sources, so a proof
that this graph lies outside K132 would be a valid completed decrease.
It would not be a proof preserving the original ordered boundary B;
the changed boundary is part of the construction, not a hidden relabel.

### Exact full-colouring insertion map

For each full colouring eta of H, the possible b-colours in G_A are
exactly

```
{0,1,2,3} minus {eta(a),eta(q),eta(c)}.                 (A1)
```

Each choice extends eta on the same entire exterior and gives one full
G_A colouring. This includes every extension and every possible empty
fibre; no other vertex is recoloured. For each such extension, the old
G lift is still the frozen full two-centre lift, nonempty exactly when
`(a,b,q,n)` is not rainbow.

In particular, H cannot accept its own row `01232`. In that row
`(x,y,a,q,c)=(0,1,2,3,2)`, (A1) permits b=0 and b=1. If n belongs to
`{0,2,3}`, choose b=0; the old gate is nonrainbow. If n=1 choose b=1,
again making it nonrainbow. Each choice yields the corresponding
original rejected row rho_0 or rho_1 and an old full lift. Thus

```
F_01232(H)=empty.                                     (A2)
```

If G_A accepts alpha, deleting b gives an H colouring in row `01202`
when q=0 or row `01212` when q=1. The preceding audit further forces
n=3 in either case. But accepting one of these rows while rejecting
`01232` is not itself an outside-K132 certificate.

### The complete support-level ear map

For reproducibility, use the frozen ten-row order

```
01012,01021,01023,01201,01202,01203,01212,01213,01231,01232.
```

One present H row contributes the following bitmask to the support of
G_A through all choices (A1), with one common global palette renaming
only when reading the canonical catalogue row:

```
4, 2, 1, 256, 576, 128, 528, 32, 8, 80.              (A3)
```

This map is a consequence of actual vertex insertion, not an abstract
independently selectable extension. It determines the entire support of
G_A as the bitwise union over the present H rows. It does not determine
the full joint n-fibres or the original G support. The C audit separately
checks its catalogue consequences; they must not be promoted to a
realization theorem for an arbitrary exterior relation.

## 3. A planar q=n quotient retaining the original outer boundary

There is a different actual candidate that enforces q=n without also
identifying h with b. Define

```
T = (G-p)/(q=n),
S = T-h.
```

Write Q for the merged q,n vertex. Both are original interior vertices
at this source site. Thus this operation does not identify any original
outer vertex, and the five named original vertices x,y,a,b,c remain
distinct in their original cyclic order.

Deleting the interior degree-five p creates the actual pentagonal face
`(a,b,q,h,n)`. The vertices q,n are cofacial. They are not adjacent in
G: an edge qn would make triangle pqn, but edge pq already has its two
facial triangles pbq and pqh, and n differs from b,h. It would therefore
contradict the original facial-triangle condition. Draw a q-to-n arc
through that evacuated face and contract that arc. This is one
cofacial identification, so it has a plane embedding; parallel edges
can be simplified without changing their inequality constraints. There
is no loop from a pre-existing qn edge. The original outer cycle is
retained. No second identification arc is being assumed compatible.

After the quotient, h has complete neighbour set `{Q,L,R}`. Original
edges qL, LR, Rn give the triangle QLR. Hence `{Q,L,R,h}` is a K4 with
h of degree three. Deleting h preserves exactly the proper-colouring
relation on every retained vertex: a proper triangle QLR always has
one missing fourth colour, which is the unique h-colour. This is a
total and unique lift, not an invocation of a four-colour theorem.

The vertex ledger is exact:

```
G:       k+5 vertices;
G-p:     k+4;
T:       k+3 after q=n;
S=T-h:   k+2.
```

The original five boundary vertices remain, so

```
k(S)=k-3.                                             (A4)
```

This gives a legal plane graph at the claimed completed size while
avoiding the crossing pair of identifications `h=b` and `q=n`.
It does not enforce h=b on arbitrary rows.

## 4. All old lifts of S, including every empty fibre

Take one full S colouring chi. The triangle QLR has three distinct
colours; let

```
H(chi) = the unique colour outside {chi(Q),chi(L),chi(R)}.
```

Restore h with this colour, and split Q back to q,n with their common
colour chi(Q). Every edge not incident with p is now proper, with every
retained vertex and every original outer colour fixed. The complete old
lift set at p is exactly

```
{P: P outside {chi(a),chi(b),chi(Q),H(chi)}}.            (A5)
```

The candidate S retains triangle abQ: ab is original, bQ comes from bq,
and aQ comes from an. Thus a,b,Q have three distinct colours. Since
h is adjacent to Q, (A5) has exactly one element when

```
H(chi) in {chi(a),chi(b)},
```

and is empty otherwise. These are all lifts. No restriction to a
chosen accepted sector appears in this statement.

For every source-rejected original row, an S colouring must therefore
have the fourth gate colour at h. The quotient itself has not excluded
that obstruction; it has moved it from n to the uniquely restored h.

## 5. Exact acceptance test for S and why the same certificate still fails

In S the complete neighbourhood of original b is again `{a,c,Q}`.
Take an S colouring of alpha. Then `a=c=2`, `b=3`, and `Q=t` for
some t in `{0,1}`. Recolour b only to `s=1-t`. This is proper and
produces rho_s. The restoration value H(chi) is unchanged, since it
depends only on Q,L,R. The original rho_s fibre is empty, so (A5)
must be empty. Its other three colours are exactly `2,s,t`, forcing

```
H(chi)=3.                                             (A6)
```

Consequently every accepted S colouring actually lifts to an original
accepted colouring with h=b=3, p=s, and q=n=t. Conversely, every
original accepted colouring with h=b has q=n, by the original edges
at p,h,n; its restriction and quotient give an S colouring. The maps
are inverse on all full assignments:

```
F_alpha(S) ~= {psi in F_alpha(G): psi(h)=psi(b)=3}.     (A7)
```

This is also the old-liftable accepted sector of fan-B. It proves an
exact acceptance test for the new plane k-3 candidate. It does not
prove that the right side is nonempty: the previous accepted-source
partition still permits all accepted original witnesses to have
`(h,n)=(a,b)` instead.

Even when (A7) is nonempty, the b-only recolouring just used constructs
an S colouring of rho_0 or rho_1. Therefore

```
F_alpha(S) nonempty
  => F_rho_0(S) nonempty or F_rho_1(S) nonempty.         (A8)
```

Thus this planar quotient cannot meet the specified accepted-plus-three-
empty certificate either. Its leaked colouring has no old p-lift,
precisely as (A5) records. Identifying h=b as a second operation would
remove that freedom, but the planar proof of Section 3 does not permit
that additional crossing identification. No exterior Kempe path has
been proved to make the double identification planar.

## 6. Exact stopping point

Both H and S are fully specified completed plane C5 graphs, with exact
colouring/lift maps and final size k-3. S retains the original ordered
boundary; H has the displayed new one. Neither has been proved bad.
The full-colouring statements do not supply any of the following:

* an outside-K132 support for H or S;
* an accepted old h=b witness, hence unconditional acceptance of S;
* a planar way to impose both h=b and q=n while retaining the actual
  exterior and all original boundary vertices;
* a transport that empties all three rainbow fibres of one accepting
  fan-B.

The first construction demonstrates why boundary replacement must be
tested with its exact ten-row transfer; the second demonstrates why a
single legal cofacial identification does not authorize the crossing
double identification. H's empty accepted query and S's degree-three
boundary b give explicit failures of the previous four-query target,
rather than an unsupported claim that a convenient quotient is a smaller
bad source. The separate [supplement](SUPPLEMENT.md) proves the accepted
full-witness cover by the fixed family `Q_1,Q_2,G_B`, saving four, four,
and two interior vertices respectively; its badness obligation remains.

The requested `bad -> success or smaller bad` construction remains OPEN.
No local patch family was enlarged, no abstract relation was called a
realizable source, and no matching, even-complement, full319, or Lean
closure is claimed.
