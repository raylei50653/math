# B: a global joint-oddness obstruction after both marked-cut restrictions

Frozen BASE `f1faf743833c51ddc5efbe9e0f390b87b9f2311d` and the continuation
bytes frozen by this audit's `BASE.json`.

**Full Sigma319 exclusion remains OPEN.** The result below rules out an
abstract finishing argument that uses only planarity, full FJ, the known
even 111/all-distinct endpoints, ordinary101 existence, and the new marked
four-/five-cut restrictions. Those hypotheses can hold simultaneously while
the **global minimum over the whole joint family is two**. This is stronger
than a failure of one shortest exchange cycle. It is a finite countermodel
to the weakened implication, not a source counterexample or a source-size
bound. The literal source layout is explicitly absent.

## 1. Exact target and the source contract retained

For the actual source, retain the original completed G, its ordered contacts,
rotation, all attachments and private vertices, all complete fibres including
empty ones, and all legal original r lifts. The graphs stay `J=U/(s=t)`,
`D=J*`, with `e=vw*`, `f=pq*`, `g=mz*`. Set

`F_e = { M a PM of D : e in M, exactly one of f,g in M }`,

`omega_e = min { odd(D-M) : M in F_e }`.

The old proof gives ordinary101, so the actual family's minimum is defined.
The desired sufficient conclusion is `omega_e=0`, equivalently
`W110+W101>0`; neither direction separately has to be positive. The complete
even 111 witness and the new two complete all-distinct source sectors are
separate full witnesses. The latter give even010/001 endpoints on the same
D, but their private colours cannot be superposed with the former witness.

The continuation proves every actual cyclic five-cut meets at most one mark.
The new C proof in this audit additionally proves every cyclic four-cut avoids
e and f. Section 2 keeps both restrictions in its weakened premise set.
It does **not** keep the source's two triangular faces and hub edge: Section
4 identifies this missing literal condition, rather than claiming it follows
from the cuts.

## 2. A complete global countermodel to the weakened implication

Take exactly the frozen `flipped_icosahedral_return` graph, retaining its
twelve primal vertices, thirty actual edges, twenty triangular faces, and
their original edge order. The present input is [input_graph.json](input_graph.json).
Only the three selected edge indices differ from that old control's marking:

`(e,f,g)=(0,29,6)`, with primal endpoints
`((0,2),(10,11),(1,9))` and dual endpoints
`((0,14),(11,17),(5,8))`.

Thus the three marks are pairwise disjoint in both primal and dual. No old
named pins are assigned to this new marking. The checker requires the
declared marked endpoints to equal these indexed edges and rejects an
inherited pins field, preventing mixed markings of the same underlying graph.

The independent exhaustive reconstruction finds exactly 288 complete labelled
J colourings and 38 perfect matchings of its actual dual. Every colouring obeys

`(d_e=d_f) iff (d_e=d_g)`.

There are even111 matchings, for example

`{0,2,4,6,12,14,16,18,22,29}`

whose whole complement has lengths 14 and 6. There is also a complete
all-distinct colouring, in vertex order 0,...,11:

`(0,1,2,1,3,2,1,3,2,0,3,0)`.

Its actual marked differences are `(2,3,1)`. Its three colour matchings are
therefore the simultaneous even001, even100, even010 witnesses supplied by
**one** complete colouring. No private vertices are omitted.

All ordinary counts and even-complement weights, in this one marking, are:

| Mark status | Ordinary PM count | W |
| --- | ---: | ---: |
| 000 | 13 | 28 |
| 001 | 3 | 2 |
| 010 | 1 | 2 |
| 011 | 6 | 16 |
| 100 | 9 | 18 |
| 101 | 3 | 0 |
| 110 | 0 | 0 |
| 111 | 3 | 6 |

Here W is exactly `sum 2^cycles(D-M)` over the even complements. Thus
`W010=W001>0`, `W111>0`, ordinary101 is nonempty, and the whole joint family
is precisely the following three matchings:

| Matching | Entire complement cycle lengths |
| --- | --- |
| `{0,2,6,8,11,16,18,22,24,25}` | 5, 15 |
| `{0,2,6,8,11,18,20,21,24,25}` | 5, 10, 5 |
| `{0,6,8,11,13,17,19,22,24,25}` | 13, 7 |

Every one has oddness two and an **empty complete fixed-alpha colouring
fibre**. Consequently `omega_e=2`. Allowing arbitrary batches, changing the
even starting colouring, or optimizing over both joint directions cannot
produce an even endpoint in this graph: all final matchings in the entire
joint family are in the table. This is not merely a one-step local minimum.

The graph has exactly two actual cyclic four-edge cuts,

`{9,10,13,17}` and `{17,19,23,28}`,

both avoiding all three marks. Its twenty-two actual cyclic five-edge cuts
each meet at most one of e,f,g. The checker exhausts all `2^19-1` nontrivial
unordered bipartitions of the twenty dual vertices. It computes each literal
boundary and checks a cycle on each side. These are genuine cuts, not sets
obtained by adding redundant deleted edges to a smaller cut. All sides and
boundary edge indices are retained in the certificate.

This establishes the stated finite countermodel to the weakened implication.
In particular, no proof of a strict descent at every positive joint minimum
can follow from that premise set alone.

## 3. Why joint shortest-cycle selection does not repair the old shortcut

One attempted finishing argument strengthens the old choice of Q: minimize
its length over all M0-alternating cycles avoiding e and containing **exactly
one** of f,g, rather than fixing the 111-to101 direction. The family is nonempty
because ordinary101 exists.

For a new remote W5 pentagon in the one-port case, the old literal shortcut
deletes the outside arc P23 and inserts one original dual spoke. The inserted
spoke avoids **all three** marks. Thus its exact marked characteristic vector
is obtained only by deleting the marks lying on P23. The shortcut cannot
insert the opposite mark. If P23 avoids the active mark, the shortcut
contradicts joint minimality just as before; otherwise it loses the sole
active mark and exits the joint family. Joint minimality therefore still
only proves that P23 contains the active mark.

The five-cut theorem restricts the pentagon's five ports. It does not restrict
the entire exterior arc P23, which can contain the active mark far from all
five ports. No inference from one to the other is available. This calculation
neither excludes three-port defects nor repairs long odd components. It is
an exact accounting of the proposed stronger selection, not a new claim
that a single shortcut yields descent.

## 4. The absent literal source geometry and the whole fixed-graph census

The fixed marking in Section 2 cannot have the actual source layout
`mvw`, `zpq` as triangular faces and `mz` as g. Its candidate m must be one
of g's endpoints 1 or 9, while v,w must be 0,2. Neither 1 nor 9 is adjacent
to either 0 or 2. Hence the first triangle already fails. No relabelling of
unmarked vertices repairs that incidence. This graph is not asserted to arise
from any original G,U,r, to realize complete Sigma319, or to supply the two
source all-distinct z=v and z=w sectors.

To distinguish this from a choice of an unfortunate marking, the checker
also examines **all 24,360 ordered triples of distinct actual edge indices
on this one graph**. The cumulative layers are:

| Exact fixed-graph condition | Ordered markings |
| --- | ---: |
| Full FJ, an even111 colouring, and an all-distinct colouring | 224 |
| Also ordinary joint nonempty | 144 |
| Also each cyclic four-cut avoids e,f | 52 |
| Also each cyclic five-cut meets at most one mark | 12 |
| Also literal same-pin faces mvw,zpq and actual edge mz | 0 |

The finite zero in the last row is **not** a theorem for arbitrary graphs
and does not exclude a source. Independently of the small-cut conditions,
there are four literal same-pin layouts satisfying the first two rows.
All four violate both small-cut conditions, at least one original cross
nonedge, and the source's exact common-neighbour identity:

| Marks (e,f,g) | (m,z; v,w; p,q) | A forbidden actual cross edge |
| --- | --- | --- |
| (17,6,22) | (5,10; 4,6; 1,9) | 4--9 |
| (17,7,21) | (5,9; 4,6; 1,10) | 6--10 |
| (17,11,1) | (0,3; 4,6; 2,7) | 2--6 |
| (17,14,0) | (0,2; 4,6; 3,7) | 3--4 |

The certificate also lists both actual sets `N(z) intersect N(v/w)` for
every row. No candidate secretly satisfies the full source common-neighbour
rule `{m}`. The small-cut restrictions and the actual source layout must
therefore be used together in any subsequent attempted closing theorem;
they cannot be replaced by separately witnessed properties of markings.

## 5. Verification and stopping point

[verify.py](verify.py) imports no old checker. It reconstructs the dual from
every original triangular face, checks all vertex links and Euler data,
enumerates every full labelled colouring and PM, and retains every complete
fixed-alpha fibre including the empty ones. For each PM it independently
checks `fibre_size=4*2^cycles` for an even complement and zero otherwise.
It enumerates all small cuts and all ordered marked triples of this fixed
graph, retaining literal same-pin layouts. Normal, seed17, and corrupted
fibre/cut/layout/marking controls are recorded in [VERIFICATION.json](VERIFICATION.json).

No actual minimum source was supplied: **not triggered**. The positive
arbitrary-size source result in this audit belongs to C's marked four-cut
proof, not to this finite B control. A complete proof still needs a strict
joint oddness descent or an incompatible complete colouring using the actual
two-face layout, fan sectors, original nonedges, and full fibres together.
No such descent was proved here. Same-graph exchanges have zero reconstruction
cost but supply no smaller completed bad source; the original reconstruction
cost remains k+5. Full319, the general claim, and any new Lean theorem remain
OPEN. No 4CT or external theorem, source replacement, commit, or push is used.
