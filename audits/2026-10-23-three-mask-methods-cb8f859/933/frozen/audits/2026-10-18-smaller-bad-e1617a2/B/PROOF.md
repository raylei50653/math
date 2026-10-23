# B. Two actual k-4 quotients, complete old lifts, and the verified exterior

BASE `e1617a2756813327d7ad333cfdd0fd92fa9efc38`. The parent freezes the
preceding uncommitted audit separately. Four additional source authorities
are copied byte-for-byte from BASE under B/frozen and listed in
[INPUTS.json](INPUTS.json). No earlier audit is edited.

The constructions below are genuine completed smaller graphs. Their
badness is not established. The paper identifies the exact remaining
same-source equality fibres, rather than treating a local replacement
or a necessary Kempe connection as a completed reduction.

## 1. Full original source

Fix the original no4ct globally minimum C5 source G, with ordered boundary
`B=(x,y,a,b,c)`, original apexes `(r,t,p,q,s)`, all actual edges and their
rotation. Retain the original branch

```
d_G(x)=d_G(y)=d_G(b)=4, d_G(r)=6, d_G(s),d_G(t)>=6,
N_G(p)=(a,b,q,h,n), N_G(h)=(p,q,L,R,n), d_G(p)=d_G(h)=5.
```

Here h=ell is the actual other pq-face vertex. All original triangles
are facial and every original interior vertex has degree at least five.
The ordered two-star rim is `(a,b,q,L,R,n)` and its two interior vertices
are exactly p,h. The original complete fibres `01021,01202,01212` are
empty; `01232` is nonempty. Every colour equation below uses this same
literal original frame.

The fixed source authorities are:

- SOURCE_GEOMETRY sections 1–2: apexes, exact boundary contacts and the
  original small-cycle restrictions;
- low-p PROOF section 1: the original full no4ct source and original
  degree lower bounds;
- J-source geometry sections 1–2: r=6, s,t degree bounds, exact source
  degrees and original fan identities;
- active-f B sections 1–3: the actual two-star position and rotations.

No finite representative is used as a substitute for this hypothetical
source. In particular, control graphs below need not satisfy these source
assumptions.

## 2. The exterior eight-gon is genuine in this source

The exact x,y boundary stars are

```
N_G(x)={y,c,r,s}, N_G(y)={x,a,r,t}.
```

The ordinary five-degree h differs from r,s,t, whose original degrees
are at least six. Thus hx,hy are absent. Edges ha or hb would make a
third triangle on ph in addition to its actual incident faces pqh and
phn. Since every triangle is facial, they are absent as well.

Finally suppose hc existed. Triangle qhc would be facial. At q the four
actual triangular faces would then give the closed link cycle

```
b-p-h-c-b
```

through faces bpq,pqh,qhc,bcq. The four vertices are distinct. These
facial sectors exhaust the rotation at the interior vertex q, forcing
`d_G(q)=4`. This contradicts the original interior degree lower bound.
Hence hc is also absent.

It follows that h has no original outer neighbour. The original p apex
has exactly the boundary contacts a,b, so its neighbour n is interior.
The other apex q is interior, and L,R are interior because they are h
neighbours. They are already distinct by the actual two-star rim. Thus
the two-star disk meets B exactly in the original edge ab.

The actual triangle bcq lies outside that disk and meets it along bq.
Adjoining the triangle gives a disk whose outer boundary is
`(a,b,c,q,L,R,n)`. Its intersection with the original outer disk boundary
is precisely the connected arc a-b-c. Consequently the complementary
closed disk E is genuine and has simple boundary

```
E: (a,n,R,L,q,c,x,y).                                  (B1)
```

This verifies the previous audit's extra eight-gon hypothesis for this
full original source. It does not assert (B1) for arbitrary plane two-star
patches, for a different original r branch, or for an unverified different
centre position. The full reflected `(q,ell_c)` source has the reflected
statement. The `(p,n_a)` position must retain its different literal map.

## 3. The accepted-colouring crosscut is therefore source-applicable

In an old-liftable accepted colouring of the fixed fan H_b, write

```
a=c=2, b=3, q=n=t in {0,1}, s=1-t, {L,R}={2,s}.
```

Let Z be the one of L,R of colour s. The preceding frozen proof establishes
that the actual `{s,3}` component from b reaches x when s=0, or y when
s=1: otherwise its switch gives a nonrainbow original rejected row.
Its unique first neighbour of colour s is Z. Deleting bZ from a simple
such path gives an original-edge path from Z to that anchor in E.

Only Z and the anchor on the boundary (B1) have colours in `{s,3}`.
Thus the path is a crosscut of E. It separates q and n on the actual
boundary order. Its palette is disjoint from `{2,t}`, so q and n are
in distinct actual `{2,t}` components of E. The rim edges give

```
{a,n} in one {2,t} component, {q,c} in another.          (B2)
```

This is a simultaneous one-colouring source conclusion. It does not
contradict the rejected-row q-to-n connections, which belong to different
colourings and palettes. No transport retaining these paths across a
change of row has been established.

## 4. First actual cofacial operation: identify n with original b

Delete p. Its actual pentagonal hole has cyclic boundary
`(a,b,q,h,n)`. The vertices b,n are nonadjacent: the complete original
boundary star is `N_G(b)={a,c,p,q}`, and n is a distinct interior vertex.
Draw a b-to-n arc in this hole and contract it, retaining b as the
original boundary name. Suppress parallel edges only. Put

```
D=(G-p)/(n=b).
```

This is one cofacial identification of an interior vertex with one
original boundary vertex. No two outer vertices are identified, the
ordered outer C5 remains, and no hidden completion vertices are inserted.
The completed size is `k(D)=k-2`.

In D the complete h-neighbourhood is now `(q,L,R,b)`. Its four facial
triangles form the actual closed star of h with boundary

```
q-L-R-b-q.                                            (B3)
```

Here bq is original, while Rb is the image of Rn. The triangle bqh is
the result of contracting the b-to-n arc in the p hole. The other three
triangles are the retained original h faces. Thus deleting h next really
exposes this one quadrilateral face; it is not an arbitrary abstract
four-contact relation.

## 5. Two explicit completed k-4 graphs

In the hole (B3), identify either opposite pair q=R or opposite pair L=b.
These are separate graphs, not two simultaneous crossing diagonals:

```
Q_1 = (G-{p,h})/(n=b, R=q),
Q_2 = (G-{p,h})/(n=b, L=b).                            (B4)
```

Their legal embedding is the sequential construction in sections 4–5.
For Q_1, qR is absent in G: otherwise triangle hqR would be a third
facial triangle on hq, besides hpq and hqL. The first n=b quotient does
not create qR, so its second contraction creates no loop.

For Q_2, bL is absent by the complete original b star, and nL is absent
because triangle hnL would be a third facial triangle on hn, besides
hpn and hnR. Consequently bL is still absent after n=b. Equivalently,
the full final class `{b,n,L}` is independent in G. Again there is no
loop. All distinct final classes and every exterior attachment are
retained; only duplicate copies of the same inequality are simplified.
If a parallel class contains an original outer C5 edge, keep that copy.
Thus suppressing copies never deletes the designated embedded outer cycle.

The vertex ledger for either operation is

```
G: k+5;
delete p: k+4;
identify n=b: k+3;
delete h: k+2;
identify one opposite pair: k+1.
```

Both graphs retain the five original ordered boundary vertices, so

```
k(Q_1)=k(Q_2)=k-4.                                    (B5)
```

Their boundary degrees and connectivity need not satisfy the original
minimum source's restrictions. Competitors in global minimum badness
only need to be legal finite simple plane disk-C5 graphs. No claim of
badness follows merely from the strictly smaller size.

## 6. Acceptance cover of the original h=a sector

Fix one original complete accepted colouring with h=a. The preceding
source two-rejection argument forces

```
a=c=h=2, b=n=3, q=t in {0,1}, p=s=1-t.
```

The original h and rim edges give precisely the following possibilities:

```
(L,R)=(3,s), (3,t), or (s,t).                          (B6)
```

Thus either R=q, giving a proper restriction/quotient to Q_1, or L=b,
giving one to Q_2. Every other original vertex retains its actual colour;
the equality classes are imposed on this same complete witness.

The overlap `(L,R)=(b,q)` goes to both candidates, so this is a cover,
not an asserted disjoint partition. If this original accepted h=a sector
is nonempty, at least one of the **fixed** graphs Q_1,Q_2 accepts `01232`.
The graph selected by such a witness must then be used for every further
row query.

This does not cover the old h=b accepted sector, where n=q instead.
The companion A construction gives its different k-3 quotient and exact
acceptance relation; one cannot select a different quotient independently
for each rejected row.

## 7. All old fibres of Q_1 and Q_2

Take one complete Q_i colouring and pull it back to the same original
`G-{p,h}` using its actual quotient map. This fixes every retained
exterior vertex, including all original boundary colours. The complete
old `(p,h)` lift sets, including empties, are exactly

```
Q_1: {(P,H): P outside {a,b,q}, H outside {b,q,L,P}},
Q_2: {(P,H): P outside {a,b,q}, H outside {b,q,R,P}}.    (B7)
```

For Q_1 the pullback has n=b,R=q; for Q_2 it has n=L=b.
No further original edge is missing from this description. All edges
not incident with p,h have already been checked by properness of the
quotient colouring.

The resulting exact empty-fibre tests are

```
Q_1 has an old lift iff L != a;
Q_2 has an old lift iff a=q or R != a.                 (B8)
```

Proof: a,b differ and b,q differ by retained edges. If a differs from q,
the three colours a,b,q force P to their missing fourth colour. Then H
can only be a, so (B7) is nonempty exactly when the remaining pin L or R
differs from a.

If a=q, choose P among the two colours outside `{b,q}`. If the remaining
pin is one of those two colours, choose P equal to it; otherwise either
choice leaves an H. Hence a=q always admits an old lift. In Q_1 the
retained edge qL already forces L!=a in this case. In Q_2 there is no
qR edge, so a=q=R is a valid liftable case and must not be erased.

For accepted `01232`, the nonempty old lift is unique: p is the missing
colour of a,b,q and h=a. Thus the liftable accepted parts of Q_1,Q_2
give precisely their original accepted h=a sectors satisfying the
respective extra equality. Additional accepted colourings without an
old lift are not silently removed.

## 8. Exact remaining rejected equality fibres

Because every nonempty (B7) would contradict the corresponding original
rejected fibre, the only possible complete candidate colourings in the
three rejected rows have these simultaneous values:

| Row | q | Q_1 pullback | Q_2 pullback |
| --- | --- | --- | --- |
| 01021 | 3 | n=b=2, R=q=3, L=a=0 | n=L=b=2, R=a=0 |
| 01202 | 1 or 3 | n=b=0, R=q, L=a=2 | n=L=b=0, R=a=2 |
| 01212 | 0 or 3 | n=b=1, R=q, L=a=2 | n=L=b=1, R=a=2 |

The q=a=0 sector of `01021` is excluded by its old lift, for both
candidates. This includes Q_2's possible R=a=q case; forgetting that
case would incorrectly narrow the full lift theorem.

These are conditions on the same complete quotient/exterior colouring.
They do not follow from independent feasibility of the displayed pin
values. To certify one accepting Q_i as a smaller bad graph through the
specified four-query certificate, all three of its complete equality
fibres in this table must still be proved empty.

## 9. A completed negative control for unconditional lifting

The already frozen twelve-vertex control consists of the original two-star
cap, triangle bcq, and the cone at r over the eight-gon (B1). Use precisely
that one graph, not an enlarged family of patches. Its seven interior
vertices are `p,h,q,L,R,n,r`, and the two quotients (B4) have three interior
vertices each, agreeing with `7-4=3`.

In both quotients fix the complete original outer row `01202` and set
q=1,r=3. For Q_1 use the full pullback

```
(a,b,q,L,R,n)=(2,0,1,2,1,0).
```

For Q_2 use

```
(a,b,q,L,R,n)=(2,0,1,0,2,0).
```

Every surviving rim and exterior edge is proper: the exterior eight-gon
uses only colours 0,1,2 and its cone r has colour 3. All quotient equality
classes have the stated same colour. In both cases old p is forced to 3,
while old h sees all four colours and has no lift. These are complete
colourings of actual smaller plane graphs, not merely partial interfaces.

The control original graph does **not** have the source's three empty
fibres and does not satisfy its minimum-source geometry. Therefore this
is an explicit countercontrol to unconditional quotient lifting, not a
counterexample to a theorem using the full source assumptions. It shows
exactly why the empty-fibre obligation in section 8 cannot be dropped.

The independent stdlib [checker](check.py) rebuilds this one original graph
from its oriented triangular faces, forms both actual quotient edge sets,
and enumerates their complete fibres in all ten frozen original rows. For
each full assignment it pulls back through the literal quotient map and
checks all 16 original (p,h) assignments against the entire original edge
set. The full fibres and every old lift, including empty sets, are saved
in [certificate.json](certificate.json). The original source exclusion
hypotheses are explicitly `not-triggered` on this control.

Both actual quotient controls have three interior vertices and mask 91,
which belongs to the frozen K132 catalogue. In the ten-row order used by
that catalogue, each has counts

```
(2,2,0,2,2,0,2,0,0,0).
```

They are not smaller bad examples. A separate saved Q_2 control has
`a=q=R` and a nonempty old lift, rejecting the tempting incorrect rule
that every `R=a` assignment must be unliftable.

Replay from the repository root:

```
python3 -B audits/2026-10-18-smaller-bad-e1617a2/B/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-18-smaller-bad-e1617a2/B/check.py --negative-control
```

Embedding legality is supplied by the actual facial operations in sections
4–5, separately from the checker's edge/fibre verification. The certificate
SHA256 is `ee86623807e402011b0f361a56c5c6dc832fd4aa8f17b4e0e318a12e2b5e1342`.

## 10. Remaining barrier

The genuine source exterior and its accepted crosscut are now verified.
Two further actual quotients save four original interior vertices and
cover every accepted original h=a witness. Their complete old fibres
are explicit and isolate equality leaks rather than rainbow leaks.

No argument yet turns (B2), which lives in an old h=b accepted colouring,
into the exclusion of any row in section 8, which belongs to another
candidate and another full colouring. Likewise it does not prove that
the original h=a accepted sector is nonempty. These distinctions prevent
a cross-row or cross-candidate path substitution.

Accordingly no smaller **bad** source has been constructed. An actual
outside-K132 certificate for one fixed completed graph remains required.
The paper adds neither a universal reduction nor matching/even-complement,
full319, or Lean closure.
