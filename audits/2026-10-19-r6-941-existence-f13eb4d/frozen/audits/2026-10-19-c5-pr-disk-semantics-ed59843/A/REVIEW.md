# A: arbitrary-disk paper audit of reconstructed P/R semantics

Frozen BASE: `ed59843ff8aad66cf3dd895da101787b3daec7a0`. Input authority is
the parent `BASE.json` and its frozen copies, especially the source model,
source `RESULTS.md`, import README and observation-depth report. This audit
writes only `A/`. No source attachment or older evidence is modified.

**Verdict.** There are explicit, everywhere legal operations on embedded C5
disks whose full literal-colour fibre transformations are exactly the supplied
P/R integer matrices. The proof holds for arbitrary finite size, with chords
allowed. It establishes a reconstructed realization of the supplied operators;
it cannot recover the identity of the missing historical README or program.

## 1. Exact source and embedding contract

Let `G` be a finite simple graph embedded in a closed topological disk `D`.
Its distinguished ordered boundary is the simple cycle
`B=(b0,b1,b2,b3,b4)`; every boundary edge is present and follows the boundary of
`D`, and all other edges and vertices lie in `D` except their boundary
endpoints. Retain the entire embedded graph, including all boundary chords,
all interior components and every old edge and incidence sector. Connectivity
may be imposed without changing the argument. No assumption on graph size,
triangular inner faces, degree, colourability or membership in the 132-state
grammar is used. In particular the F seed's chords are permitted.

The palette is the fixed literal set `U={0,1,2,3}`. For every literal tuple
`beta in U^5`, let `Fib(G,B;beta)` be the **entire set** of proper colourings
`c:V(G)->U` whose restriction to the ordered B is beta. This includes empty
sets, and beta need not be proper. No colour permutation, existential choice,
or independent marginal is built into this literal fibre definition.

The ten normalized proper C5 boundary rows, in source order, are

```text
0 01012   1 01021   2 01023   3 01201   4 01202
5 01203   6 01212   7 01213   8 01231   9 01232
```

Every proper four-colour tuple on C5 uses three or four colours, and normalizing
colours by first occurrence gives exactly one row in this list. There are 240
proper literal tuples, partitioned into ten colour-permutation orbits of size
24. Let `n_i=|Fib(G,B;row_i)|`; its positivity is support bit `x_i`.

## 2. Explicit operations and their legality at every size

Define R to leave every vertex, edge and embedding incidence unchanged and
change the distinguished boundary order to

```text
R(B)=(b4,b0,b1,b2,b3).
```

This rotates the starting point while preserving the existing cyclic
orientation. Its direction matters: `(b1,b2,b3,b4,b0)` induces the inverse
matrix, which is different from the supplied R. R has interior cost zero.

Define P using a fresh vertex z. Glue a second disk Q to D precisely along
the boundary arc `(b4,b0,b1)`. Give Q boundary `(b4,b0,b1,z)`, add the diagonal
`b0-z`, and retain the whole old embedded graph. Equivalently add exactly

```text
V(PG)=V(G) disjoint-union {z},
E(PG)=E(G) disjoint-union {z-b4,z-b0,z-b1},
P(B)=(z,b1,b2,b3,b4).
```

Gluing two closed disks along a proper boundary arc produces a disk. Its
boundary is precisely the displayed five-cycle. The point b0 now lies in its
interior; z is on its boundary. The fresh vertex prevents loops or parallel
edges. The new patch meets the old graph only along the named old arc, so
there are no crossings, no lost chords and no changed interior incidence
orders. The dart toward z is inserted in the old exterior sector at b0;
the old interior sectors stay intact. Q adds precisely the triangles
`(z,b4,b0)` and `(z,b0,b1)`. Hence inner triangulation, when present in G, is
preserved. The vertex count rises by one, the boundary count remains five,
and the interior count rises by one, agreeing with `cost(P)=1`.

Both constructions are total on this disk class and can be repeated using
the **current** ordered boundary. P changes boundary identity; b0 is retained,
with all its original attachments, as an interior vertex. It is not a deletion,
contraction, or recolouring of the original graph, and it does not preserve a
fixed original boundary B.

## 3. Full literal fibre bijections, including empty cases

For any literal beta, put

```text
rho(beta)=(beta1,beta2,beta3,beta4,beta0),
T(beta)=U \ {beta0,beta1,beta4},
alpha_t(beta)=(t,beta1,beta2,beta3,beta4).
```

The identity on all vertices is an explicit bijection

```text
Fib(RG,RB;beta) <-> Fib(G,B;rho(beta)).                 (R-fibre)
```

For P there is an explicit **disjoint-union bijection**

```text
Fib(PG,PB;beta) <-> coproduct[t in T(beta)]
                         Fib(G,B;alpha_t(beta)).     (P-fibre)
```

The forward map restricts a whole colouring to the old vertex set and records
the actual old colour `t=c(b0)`. The old edge constraints give
`t != beta1,beta4`; the new spoke gives `t != beta0`. Thus the image lies in the
displayed tagged summand. The inverse retains that entire old colouring and
sets `c(z)=beta0`. The edges `zb1,zb4` are proper because beta is proper on the
new boundary, and `zb0` is proper by `t in T(beta)`; every old edge is already
proper. The maps are inverse and preserve every old vertex colour and edge.

The displayed P formula is asserted for **proper** beta. For arbitrary beta,
the universally valid form puts the boundary gate
`beta0 != beta1 and beta0 != beta4` in front of the coproduct. If the gate fails,
the target fibre is empty. If a different boundary edge fails, that identical
old edge makes every source summand empty. This distinction prevents an
improper new beta from acquiring a false source extension. Consequently all
1024 literal beta cases, including the 784 improper ones, are accounted for.

If some or all source fibres are empty the same restriction/extension maps
still apply; an empty summand contributes no colouring. Different summands
are disjoint because they have different colours at the same original b0.
Thus the formula cannot assemble pieces from different source graphs or
different partial colourings. It keeps the entire original graph and every
literal colour throughout. No nonzero-fibre assumption is used.

## 4. Exact matrix rows and colour transport

For canonical target beta the following table lists every admissible old
literal boundary tuple. Parentheses give its normalized source row index.
R's literal source tuple is also shown. All nonlisted coefficients are zero.

| i | target beta | P: old literal tuples | R: old literal tuple |
|---|---|---|---|
|0|01012|31012 (7)|10120 (1)|
|1|01021|21021 (3), 31021 (8)|10210 (3)|
|2|01023|21023 (5)|10230 (8)|
|3|01201|21201 (1), 31201 (8)|12010 (4)|
|4|01202|31202 (9)|12020 (6)|
|5|01203|21203 (2)|12030 (9)|
|6|01212|31212 (6)|12120 (0)|
|7|01213|21213 (0)|12130 (2)|
|8|01231|21231 (1), 31231 (3)|12310 (5)|
|9|01232|31232 (4)|12320 (7)|

For any literal proper source tuple alpha, the normalization map on its used
colours extends uniquely to a permutation of U: at least three colours occur,
so there is at most one unused colour. Apply that **single global palette
permutation to the complete old colouring**. It gives a bijection between the
literal alpha fibre and its normalized-row fibre, including empties. This is
only a subsequent coordinate identification; the fibre restriction formula
itself does not change the original literal palette.

The table has 13 P terms and 10 R terms. Every normalized source row occurs
at most once in each target row, so each displayed matrix coefficient is
exactly one, not an orbit multiplicity. Taking cardinalities gives, in the
ordinary nonnegative integers,

```text
n(PG)=M_P n(G),       n(RG)=M_R n(G).
```

Their positive support gives, in the Boolean semiring,

```text
x(PG)_i=OR_{j : (M_P)ij=1} x(G)_j,
x(RG)_i=OR_{j : (M_R)ij=1} x(G)_j.
```

These are entry for entry the frozen source matrices. Their validity is a
consequence of the arbitrary-size fibre bijections, rather than a claim
inferred from checking finitely many small graphs.

## 5. Seeds and arbitrary words

The frozen F seed is the five-cycle with diagonals `b0-b2` and `b0-b3`, embedded
as a triangulated pentagon. There are no interior vertices. A canonical row
extends precisely when its b0 colour differs from both b2 and b3, which holds
exactly for rows 6,7,8,9. Each successful fibre is a singleton, giving the
source count vector `(0,0,0,0,0,0,1,1,1,1)` and mask 960.

The C seed is the unchorded five-cycle. Every proper boundary tuple has its
single boundary colouring as the full colouring; its canonical count vector
is all ones and support is 1023. Its sole bounded face is a pentagon.

By induction on any finite P/R word, the graph operations remain legal and
their complete-fibre formula composes. Hence the supplied matrix transition
semantics are realized by this explicit family at arbitrary word length and
arbitrary resulting size. From a certified closure of the F seed one may
transfer conclusions to this reconstructed F grammar; adding C has the exact
source-described extra seed. This does not classify arbitrary disk sources.

## 6. Stronger scoped consequence: every disk admits the three probes

Since P/R are total on **every** disk under this contract, the earlier
matrix identities for `RR,PRR,RRR` apply to any such disk, regardless of whether
its support belongs to K132. From three independently transformed copies of
the same source disk, the four observed support bits reconstruct all ten
source support bits by the earlier inverse formula. The same pure-coordinate
decoder recovers the ten **canonical fibre cardinalities** if the probe
observations are counts. The two redundant count coordinates obey
`c3=a4` and `b4=c4+c1`; for support the latter is OR. Count recovery does not
recover the actual full sets of colourings.

This consequence is independent of general grammar coverage. It also does
not make the 132-state minimal machine universal for arbitrary disks: the
132-state claim applies to the 132 realized grammar states. The full formal
1024-mask transition model is injectively decoded by the same probes, so its
states are pairwise distinguishable; actual arbitrary-disk support coverage
remains a separate question.

## 7. Corroboration and unresolved identity boundary

The already existing repository file `docs/c5_kempe_screen.md`, section 5,
describes exactly this boundary replacement by a new vertex adjacent to the
old boundary neighbours, retaining the old C5 edges, with optional spoke to
the old vertex. `scripts/c5_kempe_screen.py:111` implements that support
calculation as `push(mask,v,spoke)`. The reconstructed P is its `v=0,
spoke=True` case. Copies in `A/frozen/` and hashes in
`A/additional-inputs.json` preserve these corroborating bytes. They are older
project evidence, not the missing attachment implementation.

The matrices alone do not identify a unique historical graph operation.
For example one may compose this P with an interior triangular-face insertion
where legal; the latter preserves all literal four-colouring fibre counts by
the unique fourth-colour extension, so the matrix need not distinguish those
different graphs. That alternative changes the interior cost, and is not the
P used here. Even a matching cost does not constitute custody of historical
code. No claim of original-program recovery or replay is warranted.

The spoke is essential: dropping `z-b0` adds source row 0 to target row 0
(`01012` admits old tuple `01012` as well as `31012`), contradicting the supplied
P row. The R direction and retained original boundary edges are likewise part
of the exact contract, not conventions that may be omitted from an exported
graph construction.

General disk source coverage, correspondence to every remaining r6 source,
`K_infinity=K_<=5`, historical test/UI reproduction and Lean formalization
remain outside this result.
