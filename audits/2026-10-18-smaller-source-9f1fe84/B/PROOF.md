# B: an explicit smaller cap, and the exact limits of fixed-rim replacement

BASE `9f1fe84f73aabfa87a33d28754633bae6bf0b707`; 2026-10-18.
Authority inputs are frozen in [INPUTS.json](INPUTS.json). This worker writes
only B/. The objects below are actual small plane patches, not hypothetical
full minimum sources. In particular, the positive result is a smaller
**cap**, and its use in a smaller completed original source is conditional.

## 1. The literal five-rim cap and its smaller representative

Use ordered rim `Q=(0,1,2,3,4)`. Its five edges are present. The two inner
vertices are `u=5,h=6`, with additional edges

```
u0,u1,u2,uh, h0,h2,h3,h4.
```

The oriented inner faces are
`(u,0,1),(u,1,2),(u,2,h),(u,h,0),(h,2,3),(h,3,4),(h,4,0)`.
Thus this is an actual triangulated disk with induced rim, degrees
`d(u)=4,d(h)=5`, seven inner triangles and two inner vertices.
The reversed rim is the outer face. The certificate checks all dart
incidences, cyclic vertex rotations and Euler's identity.

Delete u,h and add the two chords `13,14`. The resulting fan T has no
inner vertices and oriented inner faces `(0,1,4),(1,2,3),(1,3,4)`.
It saves exactly two vertices on this same fixed rim. Its added chords
are drawn in the emptied disk and cross neither each other nor any
outside edge. These chords are new in K. In the actual J application
the complete rim is induced. For an arbitrary outside E that already
contains either endpoint pair, draw the new copy in the disk and then
suppress one parallel copy; this preserves every colouring constraint
and leaves a simple plane graph.

The complete canonical boundary fibres, in one common colour frame, are:

| Rim row | K centre assignments `(u,h)` | T inner assignment |
| --- | --- | --- |
| 01012 | (2,3) | empty fibre |
| 01021 | (2,3) | empty fibre |
| 01023 | (2,1),(3,1) | () |
| 01201 | empty fibre | empty fibre |
| 01202 | (3,1) | () |
| 01203 | (3,1) | () |
| 01212 | empty fibre | empty fibre |
| 01213 | empty fibre | empty fibre |
| 01231 | empty fibre | empty fibre |
| 01232 | (3,1) | () |

Consequently `Sigma(K)=567` and `Sigma(T)=564` in this **local rim**
ordering. The latter 01232 is a row on Q; it must not be confused with
01232 on the original external frame `(x,y,a,b,c)`.

There is a particularly simple total lift from T to K. For any literal
proper colouring beta of T set

```
h = beta(1),
u = any colour outside {beta(0),beta(1),beta(2)}.
```

Such a colour exists. The two fan chords and the two rim neighbours of
1 make h different from every rim neighbour of h; u is then different
from all its neighbours. All five rim colours remain literally fixed.
This proves `Sigma(T) subset Sigma(K)` without an enumeration argument.
The certificate records one full lift for every literal T rim colouring.

Let E be any outside graph attached exactly along this rim, retaining
its actual ordered attachments. Every full colouring of `E union T`
lifts to a full colouring of `E union K` by the displayed map. Thus
every rejected external query remains rejected. An accepted external
query survives precisely when it has an original full colouring whose
Q restriction satisfies

```
beta(1) != beta(3) and beta(1) != beta(4).
```

This is a complete one-sided replacement theorem for arbitrary outside
size. It uses an actual common full colouring, not two marginal rows.
No count or bijection of private fibres is claimed.

## 2. This fan is the entire sound zero/one-vertex operation family

**Theorem.** Let H be any finite simple plane patch with the same fixed
ordered C5 rim, at most one inner vertex and no hidden outside attachment.
Then

```
Sigma(H) subset Sigma(K)
```

holds if and only if H contains both chords 13 and 14. In that case
`Sigma(H)=564`. Thus no such sound smaller patch retains either lost row
01012 or 01021, even if it is not triangulated.

**Proof.** A three-coloured rim always extends to the single inner vertex
if present, because a fourth colour is available. To reject K's missing
three-colour row 01201, H therefore needs the chord 03 or 14. To reject
the missing three-colour row 01212, it needs the chord 13 or 24.
The chords 03 and 24 cross in the disk, so they cannot coexist.

If both 13 and 14 are present, they triangulate the rim. Any one inner
vertex lies in one of these three triangular regions and can be adjacent
only to that region's three vertices. Every fan colouring therefore
extends to it. The complete support is exactly 564, and section 1 gives
soundness.

Suppose 14 is absent. The forced chords are then 03 and 13. Consider
K's missing row 01231. No chord other than 14 can reject this row, since
its only nonadjacent equal-colour pair is 1,4. To reject it via the sole
inner vertex, that vertex must see all four colours, in particular the
unique colours at vertices 0 and 2. But chord 13 separates 0 and 2 into
opposite open sides, so one inner vertex cannot be adjacent to both.
Thus 01231 leaks.

Suppose 13 is absent. The forced chords are 14 and 24. Use missing row
01213: its only equal-colour nonadjacent pair is 1,3, so no present
chord rejects it. The sole inner vertex would need to see both unique
colours at 0 and 2, which lie on opposite sides of chord 14. Again the
row leaks. These cases exhaust the forced chord disjunctions. QED.

This is a paper classification for the whole stated operation family,
not a claim about all possible larger regions or outside-conditioned
replacements.

## 3. Why this does not yet produce the requested original source

The frozen active-f geometry identifies this cap in J, whose degree-four
centre is p or q. For p, the original G link is `(a,b,q,ell,n_a)` and
the J link is `(z,q,ell,n_a)`. There are two possible second centres.

* For `h=ell`, write its ordinary link as `(p,q,L,R,n_a)`. One compatible
  standard J rim is `(q,z,n_a,R,L)`; the fan adds `zR,zL`. The original
  patch has rim `(q,b,a,n_a,R,L)`, with **two degree-five centres**.
* For `h=n_a`, one compatible J rim is `(z,q,ell,R,L)`; the fan adds
  `qR,qL`. The original patch again has a six-vertex rim: the J vertex z
  represents the a/c identification, and the adjacent original boundary
  vertex b was deleted in forming the intermediate triangle core.

All names in a reflected q case must be reflected together. These maps
identify where the local replacement is drawn; they do not identify
original full colourings with J colourings. In original G the boundary
edge ab forces different colours; J instead identifies a,c into z and
has no b, as recorded in the parent audit's
[frozen triangle-core construction](../frozen/docs/c5_c4_triangle_core.md).
Splitting z back into a,c, restoring b, and restoring the other
original attachments is therefore a genuine
lift obligation. A two-vertex saving inside J alone does not discharge
the completed-source size or the original four-query obligations.

There is also a concrete obstruction to applying an unconditional
fixed-rim patch rule directly in G. Consider the generic original
adjacent-degree-five cap with ordered rim `(0,1,2,3,4,5)` and centres
`u=6,h=7`, with u adjacent to `0,1,2,3,h` and h adjacent to `0,3,4,5,u`.
It has eight inner triangles and two inner vertices. Its complete
canonical support consists of these 13 rows:

```
010101 010102 010121 010202 010203 010232
012013 012023 012031 012032 012101 012103 012131
```

**Finite family theorem.** No simple plane patch on that same six-rim
with zero or one inner vertex has support contained in this cap support.
This is stronger than failure of a particular fan, but its scope remains
fixed pins, no identifications, at most one inner vertex, and soundness
against every outside colouring. It does not rule out a replacement
whose soundness is proved only after using the actual original outside
relation and the four external queries.

The independent finite proof enumerates every such graph by completion
to a triangulated disk on the same vertices. With no inner vertex there
are 14 hexagon triangulations. With one inner vertex, choose its cyclic
neighbour set S, of size at least three, draw its wheel on S, and
triangulate each intervening boundary sector. This gives all 84 maximal
patches. Every smaller edge set occurs as a subgraph of a maximal patch
in its actual embedding. Deduplicating by labelled edges gives 45 and
1,148 graphs, respectively. Every graph has a concrete leaking full
colouring recorded in the certificate. Distinct embeddings with the
same edges have the same colouring relation; a containing triangulation
provides one actual rotation for each recorded edge set.

For comparison the C5 family gives 5 and 21 maximal patches, 11 and 212
edge sets, and respectively 1 and 16 sound graphs. All 17 have support
564, independently confirming section 2's paper classification.

## 4. Certificate and authority boundaries

[check_patches.py](check_patches.py) and [patches.json](patches.json) retain
the ordered rims, all maximal oriented faces and rotations, every tested
edge set, every canonical proper boundary row, every private assignment
in each fibre, including empty fibres, and a leakage witness for every
failed candidate. Improper rim rows are explicitly empty. A **single
common S4 permutation of the entire lift** expands the canonical data
to all literal 4^5 or 4^6 boundary tuples. No piece is independently
normalized. The K-to-T accepted-colouring criterion and T-to-K full lift
are checked on all literal fan colourings.

The checker regenerates the entire certificate and compares exact
objects. Generation uses exclusive creation; ordinary and seed17 replay,
a deleted-row negative control, and input custody checks are reported
in [VERIFICATION.json](VERIFICATION.json).

The cap replacement is **triggered and holds** for the named finite K,T.
The C5/C6 fixed-rim family classifications are complete in their stated
finite domains. A true minimum 932/933/941 original source was not supplied:
source realization and a qualifying original accepted witness are
**not triggered**. No smaller completed bad source, full319 exclusion,
joint even-complement positivity, general closure, or new Lean theorem
is claimed here. The source-conditioned reconstruction is left to the
separate A/C work; nothing in this report replaces its full-lift check.
