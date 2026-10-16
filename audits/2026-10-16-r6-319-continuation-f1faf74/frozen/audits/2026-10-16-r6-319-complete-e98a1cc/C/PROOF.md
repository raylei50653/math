# A planar countercontrol to the proposed ordinary-to-even bridge

BASE `e98a1cc1afd9a428600dcf4027d8138078c01650`, 2026-10-16.
This is an independent algebra/counting audit of the remaining complete-319
obligation. It proves a useful negative result about a proposed bridge;
it does **not** exclude or realize the original minimum source.

## 1. The precise source obligation retained

Keep the same original G, ordered contacts and rotations, the original
seven pins `(z,s,v,w,t,p,q)`, the legal quotient `J=U/(s=t)`, and its actual
embedded cubic dual D. The marked edges remain

`e=(vw)*, f=(pq)*, g=(mz)*, m=[s=t]`.

The frozen full-J bridge proves, on complete colourings in one colour frame,

`|E1(J)|=12 W110`, `|E2(J)|=12 W101`,

where E1 is `d_e=d_f!=d_g` and E2 is `d_e=d_g!=d_f`. Each W is a sum
of `2^c(D-M)` over the indicated perfect matchings whose complements are
all even. Every other perfect matching has an empty complete Tait fibre.
Thus the exact target is the combined inequality `W110+W101>0`.

The frozen seven-disk proof supplies an ordinary 101 matching. The source
ABCDB row supplies an even 111 matching. It is tempting to bridge these
two facts using planarity and connectivity of the joint matching family.
The following proposition shows that such a bridge needs additional
original source information.

**Proposition C1.** There is a simple sphere triangulation J with no
separating triangle, six distinct marked primal endpoints, marked faces
mvw and zpq, an even 111 matching, and a nonempty ordinary 101 family,
but `W110=W101=0`.

Consequently the implication

`planar cubic + even111 + ordinary101 nonempty => W110+W101>0`

is false, even when the primal is four-connected. This is a finite
countercontrol to that implication, not a counterexample to the source
claim: its explicit source failures are given in section 5.

## 2. The complete embedded graph

Use vertices 0 through 9 and the following cyclic rotations:

```text
0: 1 2 3 4 5
1: 0 5 6 7 2
2: 0 1 7 3
3: 0 2 7 8 9 4
4: 0 3 9 5
5: 0 4 9 6 1
6: 1 5 9 8 7
7: 1 6 8 3 2
8: 3 7 6 9
9: 3 8 6 5 4
```

The rotation has 10 vertices, 24 edges and 16 triangular faces. Traversing
each dart exactly once gives an orientable connected cellular embedding
with Euler characteristic two, hence this is an explicit sphere embedding.
The complete facial triples, in the fixed order used for dual vertices, are

```text
012 015 023 034 045 127 156 167
237 349 378 389 459 569 678 689
```

Every triangle is in this list. Deleting any three vertices leaves a
connected graph, checked directly, so J is four-connected. These finite
checks are independently reconstructed from the rotation by `verify.py`.

Fix the literal pins

`m=1, z=5, v=0, w=2, p=6, q=9`.

The marked original edges are `02,69,15`; their duals have indices
`e=1, f=21, g=6` in the lexicographically ordered original-edge list.
The faces mvw=012 and zpq=569 occur in the above embedding, and the three
marked dual edges have six distinct dual endpoints. No pin is selected
afresh for different colourings.

## 3. Complete colourings and exact perfect-matching weights

Normalize the actual facial triangle 012 to colours 0,1,2. There are
exactly six normalized complete colourings; the entries below are for
vertices 0 through 9, with colours viewed as elements of F2 squared.

| Complete colouring | `(d_e,d_f,d_g)` |
| --- | --- |
| `0121323020` | `(2,3,3)` |
| `0121232030` | `(2,2,2)` |
| `0123123010` | `(2,3,3)` |
| `0123123020` | `(2,3,3)` |
| `0123132010` | `(2,2,2)` |
| `0123232010` | `(2,2,2)` |

Every one uses all four colours. Applying all 24 global colour
permutations gives every complete labelled colouring exactly once:
there are 144 in total. Every colouring satisfies `d_f=d_g`, so E1 and
E2 are both empty. The certificate stores all 144 full assignments;
the checker searches the graph directly instead of assuming this table.

The actual dual has exactly 18 perfect matchings. Only two have the 111
pattern. Written as original-edge/dual-edge indices they are

```text
M111a = [1,3,6,10,13,16,19,21]       complement lengths 8,8
M111b = [1,6,10,11,13,15,19,21]      complement length 16
```

There is no ordinary 110 matching. There is exactly one ordinary 101
matching:

```text
M101 = [1,3,6,8,12,14,18,20]         complement lengths 9,7.
```

Therefore

`W111=2^2+2^1=6`, `W110=W101=0`, `omega_e=2`.

In particular, the joint exchange graph is connected: it consists of a
single vertex, and that vertex has positive oddness. Unlike a Petersen
control, this obstruction occurs in an actual planar cubic graph with a
known even111 endpoint. The 111a-to-101 symmetric difference is the one
alternating cycle

`[8,10,12,13,14,16,18,19,20,21]`.

It avoids e and g, changes f, and changes the even 8+8 complement into
the odd 9+7 complement. Thus a first step from even111 into the ordinary
joint family need not preserve an even endpoint.

Independently applying B's transition definition to the full complete
colourings gives four root-zero, alpha-one choices for M111a, all with
two transitions separated between the two odd cycles. M111b has two
such choices. Its difference with M101 is a single twelve-edge
alternating cycle with four transitions: three on the nine-cycle and
one on the seven-cycle. The six choices are not all choices on M111a.

## 4. All complete fibres, including the empty ones

For each of the 18 actual perfect matchings, integrate the edge bit zero
on M and one off M over this sphere embedding, fixing vertex 0's bit
to zero. The checker retains its entire induced vertex partition,
every complement cycle, and every complete labelled J colouring with
that first coordinate. Its fibre has size

`0` for positive oddness, and `2^(c(D-M)+1)` for an even complement.

Exactly six of these complete colouring fibres are empty; the unique
joint matching is one of them. Deleting those rows would manufacture an
incorrect positive-endpoint argument, so all six are retained.

For the actual `W=J-{1,5}`, the checker enumerates all 408 complete W
colourings. For each it retains the actual missing-colour sets on the
two original neighbor paths and **all** legal distinct hub pairs.
Exactly 288 W fibres are empty. The 120 other fibres, with all lifts,
give precisely the 144 complete J colourings. This uses the same
Cartesian fibre formula as the source geometry audit, without assuming
that an arbitrary W colouring extends.

The only legal cellular split of m with the fixed z and the fixed
boundary gap vw, together with its reflected naming, is checked in the
next section. Both full seven-pin tables and every legal r lift are
retained, including colourings with no r lift. No U colouring is removed
because it fails a source condition.

## 5. Exact failures of the original source contract

The graph is deliberately **not** assigned original source authority.
The failures are explicit and prevent any inference that 319 is realized.

| Original source requirement | This control |
| --- | --- |
| `d_J(m)>=7` | `d_J(1)=5` |
| `d_J(z)>=6`, equivalently `h>=3` | `d_J(5)=5`, so `h=2` |
| Every unmarked vertex has degree at least five | vertices 4 and 8 have degree four |
| Every induced C4 meets m or z | induced cycle `3,7,6,9,3` avoids both |
| Original nonedge zv and induced U boundary | edge `zv=5-0` is present |
| Both original m-fan arc lengths at least three | the two lengths are 1 and 3 |
| Original `d_G(s),d_G(t)>=6` | the unique split implies 4 and 6 |
| Full seven-pin all-r transfer | 192 of 432 complete U colourings fail |
| Complete U support 319 | support 1016, or 967 after the original reflection |

The four forbidden source cross edges `pv,pw,qv,qw` are all absent in
this control. The separate original nonedge zw is also absent; zv is
the unique chord of the split U boundary. In particular `beta=v=0`
also fails the original fact that v,w have no boundary contacts.
All induced C5s meet m or z, so the no-hub C5 cap condition
has no instance here. Those facts do not repair the listed violations.

To check all legal splits for these fixed pins, note that a cellular
split must cut the cyclic neighbor order of m at z and at the gap vw.
Every other incidence belongs to exactly one resulting arc; moving an
incidence between arcs changes the sphere rotation. Thus, up to the
source reflection, the only split has

`N_U(s)=[5,0]`, `N_U(t)=[5,6,7,2]`, with `s=10,t=1`.

It gives the specified simple boundary `(z,s,v,w,t)=(5,10,0,2,1)`,
with its retained zv chord.
The endpoint identities are `alpha=p=6`, `beta=v=0`. The z-link arc
lengths give original `a0=4,c0=6`, so `h=a0+c0-8=2`. The m-link
lengths give original `d_G(s)=4,d_G(t)=6`. Reflecting exchanges these
two expressions; it does not improve them.

The 432 complete U colourings have the following full boundary counts:

| Original boundary row | Count | Count after reflection |
| --- | ---: | ---: |
| ABABC | 0 | 48 |
| ABACB | 0 | 72 |
| ABACD | 0 | 72 |
| ABCAB | 72 | 0 |
| ABCAC | 48 | 0 |
| ABCAD | 72 | 0 |
| ABCBC | 48 | 48 |
| ABCBD | 72 | 48 |
| ABCDB | 72 | 72 |
| ABCDC | 48 | 72 |

The resulting support masks are 1016 and 967. Each orientation has
exactly 192 full-colouring violations of the frozen all-r transfer.
In the displayed orientation, the forbidden `(C5 row,pq)` counts are

```text
(ABCBC,BD):24   (ABCBC,DC):24   (ABCBD,BC):72
(ABCDC,DB):24   (ABCDC,BC):24   (ABCAC,DC):24.
```

The checker also reconstructs these decisions directly from **every**
legal r colour and the original R table; no-r-lift fibres remain present
and pass that universal test vacuously. The source-failure summary and
the complete fibres are in the sealed certificate.

The certificate additionally retains the **entire** pin-assignment
universes. The J six-pin order is `(z,m,v,w,p,q)` with all `4^6=4096`
counts, including 4048 zero fibres. Each split's original seven-pin
order is `(z,s,v,w,t,p,q)` with all `4^7=16384` counts, including 16144
zero fibres. Every nonempty cell indexes all of its complete private
colouring records. The arrays use the declared lexicographic base-four
index, so improper and absent pin rows are present as explicit zeros.

## 6. Scope and remaining obligation

Proposition C1 rules out obtaining a complete proof merely by combining
ordinary101 nonemptiness, a known even111 matching, planarity, and joint
exchange connectivity. An external theorem purporting to provide that
implication would contradict the explicit graph above.

The complete original source has stronger degree, fan-sector, induced
short-cycle and full seven-pin obligations. The countercontrol fails
several of them, particularly the s!=t fibres which are invisible in J.
The complete-319 proof must use those retained source constraints to
obtain an actual even joint matching, or give a valid completed-source
descent preserving all full fibres and lifts. Neither step is proved
here. `W110+W101>0` for the original source and the complete319 exclusion
remain **OPEN**. The restoration cost remains k+5.

There is no appeal to general planar colourability, no external theorem,
no finite-to-source inference, and no new Lean or publication authority.
The certificate is a complete finite countercontrol to one bridge only.
