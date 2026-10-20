# C. Two explicit smaller original disks and the exact remaining lift gate

Frozen BASE `9f1fe84f73aabfa87a33d28754633bae6bf0b707`.
This exclusive C audit freezes its additional original-source authorities in
[INPUTS.json](INPUTS.json). It constructs actual `k-2` disks conditionally on
an adjacent original degree-five pair at one of the four specified sites. It does **not**
prove that one of them remains outside K132. Neither the site nor the final
gate below has been established for every remaining source.

## 1. Work in the original disk, with no hub reconstruction cost

Retain the original ordered C5 `(x,y,a,b,c)` and all actual original edges.
Suppose the original vertex p has facial rotation `(a,b,q,ell,n)` and both
p and ell have original degree five. These are precisely the `h=ell`
possibilities in the frozen active-f-seven authority, but the argument here
only needs this actual local configuration, not any perfect matching or
odd-cycle premise. The source has every triangle facial.

The two common neighbours of p,ell are exactly q,n: any further common
neighbour would create a third triangle on edge p ell, whereas every
triangle is a face and that edge has only two incident faces. Therefore
the union of their closed stars is a genuine disk with simple boundary

`C=(a,b,q,L,R,n)`.

The actual neighbours are

`N(p)={a,b,q,n,ell}`, `N(ell)={p,q,L,R,n}`.

The six rim vertices are distinct. There are exactly two private vertices,
p and ell, and no unrecorded incident edges. The common edge ab is the
original outer edge; all five original outer vertices are retained.

Construct two graphs on `V(G) minus {p,ell}`:

* `G_a`: replace this disk by the zero-interior fan at a, adding
  `aq,aL,aR`.
* `G_b`: replace it by the zero-interior fan at b, adding
  `bn,bL,bR`.

These are actual fixed graphs, not a different patch for each queried row.
The new edges can be drawn in the evacuated disk. If an endpoint pair
already has an exterior edge, suppress one of the parallel copies; this
preserves its proper-colouring constraint and produces a simple plane
graph. The original outer C5 remains simple with its original ordered
vertices. The resulting disk need not retain minimum degree or the r6
subclass; neither is required of a competitor to global minimum badness.

Both completed graphs have exactly

`|V(G_a)|=|V(G_b)|=k+3`, hence `k(G_a)=k(G_b)=k-2`.

There is no hidden cost for restoring z, m, r, x, y or b. The entire
operation was performed directly on G. In particular it is different
from deleting two vertices of J and then paying the old reconstruction
cost.

## 2. One of the two graphs really retains the accepted row

Fix any complete original colouring of row `01232`, so

`(x,y,a,b,c)=(0,1,2,3,2)`.

The original edges imply `{p,q}={0,1}`. Since ell is adjacent to both p,q,
its colour is either 2=a or 3=b.

If `ell=a`, all three added edges of G_a are proper: ell's edges to q,L,R
already certify that their colours differ from a. Restricting this very
same full original colouring therefore gives a complete G_a colouring.
If `ell=b`, ell's edges to n,L,R certify the G_b additions. Thus

`01232 in Sigma(G) => 01232 in Sigma(G_a) union Sigma(G_b)`.

The graph chosen by an accepted witness is fixed for all subsequent
queries. This is a constructive two-branch acceptance cover, at actual
completed cost k-2. It does not say that both branches accept the row.

### 2.1 All four original source positions

The construction is not limited to `h=ell`. Its generic form has rim
`(A,B,Q,L,R,N)` and centres

`p~A,B,Q,N,h`, `h~p,Q,L,R,N`.

Whenever one complete old colouring has A,B,Q all different, p is their
missing fourth colour and h belongs to `{A,B}`. Hence the two fans at
A and B cover every such full colouring. The common lift gate for both
fans is exactly `A,B,Q,N not all different`, proved just as in §3.

For the four possible original sites, the literal identifications are:

| Actual original pair | Generic `(A,B,Q,N)` | Two fan roots |
| --- | --- | --- |
| p,ell | `(a,b,q,n_a)` | a,b |
| p,n_a | `(q,b,a,ell)` | q,b |
| q,ell_c | `(c,b,p,n_c)` | c,b |
| q,n_c | `(p,b,c,ell_c)` | p,b |

Here ell_c,n_c are the reflected actual neighbours of q. In the second
row the original rim is `(a,b,q,ell,U,V)` and the generic rim is
`(q,b,a,V,U,ell)`, the literal reverse order; no new attachment is
introduced. The other two rows use the reflected original embedding.
In every row, original boundary `01232` makes generic A,B,Q pairwise
different, so the acceptance cover applies without any extra colour
premise. Every candidate retains the original ordered boundary, with no
row relabelling required to use the four-query certificate.

## 3. Exact extension criterion for either candidate

Let chi be **one complete colouring** of G_a or G_b, including the entire
unchanged exterior, in the original colour frame. Write

`T(chi)={chi(a),chi(b),chi(q),chi(n)}`.

Then chi extends across the two deleted original vertices iff

`|T(chi)| <= 3`.                                             (C1)

Necessity is immediate: p is adjacent to all four vertices in T. For
sufficiency in G_a, put `ell=chi(a)` and choose p to be any colour outside
T. The old edges of ell to q,L,R are protected by the three added fan
edges, its edge to n by original rim edge an, and its edge to p because
p differs from a. All original p edges are proper by its choice. In
G_b, instead put `ell=chi(b)`; the added fan edges protect n,L,R, the
original edge bq protects q, and p again differs from ell. This preserves
every exterior vertex and every original ordered boundary colour.

The **complete** lift set, including empty sets, is explicitly

`{(P,H): P outside {a,b,q,n}, H outside {q,n,L,R,P}}`,            (C2)

where the symbols on the right are the actual values in chi. Equation
(C1) is a theorem about all lifts (C2), not a claim that the chosen lift
is the only one. The checker saves and verifies every such finite local
fibre.

Consequently, for each rejected original row

`z in {01021,01202,01212}`,

every complete G_a or G_b colouring with row z necessarily has

`a,b,q,n all four different`.                                 (C3)

Otherwise the explicit lift would contradict the original empty z fibre.
The missing badness proof is now precise: on whichever one of G_a,G_b
retains `01232`, exclude its three complete fibres satisfying (C3).
This cannot be replaced by excluding the corresponding marginal pin
values independently.

## 4. The gate is not automatic, even with the actual q attachments

The three negative controls below use the original rim, the fan at a,
and the exterior edges qb,qc. They satisfy the indicated complete original
outer row but have no original cap lift because p would see all four
colours. Values are ordered `(q,b,a,n,R,L)`.

| Original row | Fan-a interface colouring | Missing p colour after a,b,q |
| --- | --- | --- |
| 01021 | `(3,2,0,1,3,1)` | 1, already on n |
| 01202 | `(1,0,2,3,1,3)` | 3, already on n |
| 01212 | `(0,1,2,3,0,3)` | 3, already on n |

Thus `a=c` in the last two rows and the real q-b/q-c attachments do not
alone prove the fan sound. The fan at b has analogous controls, checked
exhaustively. These are explicit local plane-patch controls, **not**
realizations of a hypothetical globally minimum original source. They
disprove the proposed local implication, not an implication that uses
additional complete exterior geometry or Kempe constraints.

The small J two-star cap with degree pattern (4,5) is not this original
cap: its p-link is `(z,q,ell,n)`, while original p has the extra neighbour
b and uses a in place of z. Its sound pentagon fan therefore does not
license the original hexagon fan. Equation (C3) records exactly the
lost original-neighbour obstruction.

## 5. Forced Kempe contacts in any leaked full colouring

There is a useful general implication in each candidate, with no graph
size or cycle-length assumption. Let a complete rejected-row colouring
have the rainbow gate `(A,B,Q,N)`. Choose T among A,B,Q, and let K be the
actual maximal two-colour component of N using colours chi(N),chi(T).
Then K must contain either T itself or an original outer vertex of one
of those two colours. Otherwise switching **that same component** fixes
the entire original outer row and fixes T, but makes N equal to T.
It creates a candidate colouring with nonrainbow gate, and the explicit
lift from §3 would give an original colouring in the rejected row.

This argument uses all vertices of one actual complete colouring. The
contact alternatives are not independently chosen path witnesses.

For either p-centred site, the original degree-four condition at b gives
an additional exact simplification in the fan-A candidate: after removing
p, the complete neighbour set of b is `{a,c,q}`. The fan at a or q adds
no edge at b. In the rows with a=c, b is therefore
isolated in the chi(b)/chi(n) subgraph. The following table records all
colour sectors, including q taking the fourth colour missing on the
outer boundary. `n -> S` means that the same actual two-colour component
of n contains at least one vertex of S. For the p,n_a site, replace n
in this table by its literal gate vertex ell.

| Rejected row | q,n values | Colours | Forced contact in G_a |
| --- | --- | --- | --- |
| 01021 | 3,1 | 1,2 | `n -> {y,c}` |
| 01202 | 1,3 | 0,3 | `n -> {x}` |
| 01202 | 3,1 | 0,1 | `n -> {x}` |
| 01212 | 0,3 | 1,3 | `n -> {y}` |
| 01212 | 3,0 | 0,1 | `n -> {y}` |

In the first line, an n-component meeting b also meets c by original
edge bc. In the other lines the isolated b cannot belong to n's
component. When the pair is 0,1, original edge xy makes reaching either
x or y reach both. Thus the two precise fixed anchors are x for 01202
and y for 01212 in every palette sector. No `q=1` or `q=0` assumption
is silently made in the last four lines. The two q-centred sites have
the same fixed anchors in the same original row order, by the identical
isolated-b and xy argument. Their 01021 alternative is `{x,a}` by literal
reflection.

For **either** G_a or G_b at the p,ell site, the chi(n)/chi(q) component
of n must meet `{q,y,c}` in row 01021, `{q,y}` in row 01202, and `{q,x}`
in row 01212. These are the general lemma with T=q and the full original
outer row. They do not by themselves give disjoint alternating-endpoint
paths: every constraint starts at the same n, and the alternatives and
the maximal components must remain in this single colouring.

## 6. Completed graph control and limits

The checker executes the actual constructors on an explicit twelve-vertex
plane C5 disk. Its outer cycle is `(x,y,a,b,c)`, and its seven interior
vertices are `q,L,R,n,p,ell,r`. Start with the complete two-centre cap,
add original edge qc and triangle bcq, then fill the remaining eight-cycle
`(a,n,R,L,q,c,x,y)` by its cone r. The 17 oriented triangular faces are
given in the certificate; all inner edges have opposite face incidences,
all boundary edges occur once, and the original C5 has no chord.

Direct enumeration of all complete original and candidate colourings gives:

| Graph | Interior vertices | Mask | Counts on the four queries `(01232,01021,01202,01212)` |
| --- | --- | --- | --- |
| control G | 7 | 863 | `(4,13,1,1)` |
| control G_a | 5 | 854 | `(2,1,1,1)` |
| control G_b | 5 | 783 | `(10,12,0,0)` |

This is a real plane graph and a real completed decrease by two. Its
original three rejected fibres are not empty, so it is explicitly **not**
the hypothetical minimum source. The G_b control also shows why accepting
01232 and rejecting only 01202,01212 does not certify badness: its 01021
fibre is nonempty. Every candidate's full fibres and every old lift are
checked by independent edge enumeration, with hashes of the complete
full-colouring sets retained in the certificate.

This supplies a real smaller-source **candidate** family and an exact,
one-bit local obstruction to lifting its complete exterior colourings.
Adding a single new private vertex adjacent to all four gate vertices
would enforce nonrainbow, but cannot simply be drawn alongside either
complete fan: the fixed outer-six graph would have seven vertices and
thirteen edges, whereas a simple plane disk with that six-cycle as its
outer boundary has at most `3*7-6-3=12` edges. This rules out that specific
one-vertex repair of the complete fan; it does not rule out changing
edges, using more vertices or exploiting the actual exterior relation.
The conditional site existence and three global empty fibres remain
unproved. It does not give `bad -> success or smaller bad`, ordinary or
even-complement positivity, full319, or a new Lean theorem.

Replay `python3 -B C/check_bridge.py --check` from the audit root.
