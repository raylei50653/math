# Arbitrary-k run-template rank theorem

Audit BASE `30f2d19275657393b7354ed75eca31439d8ee12b`; mathematical
BASE `d5b8a8605bcbcef7aebbcf1934dad7ba255ccf02`.

The six previously measured ranks are instances of the following all-k
theorem. This is a self-contained paper proof about the **unpruned universal
local templates**, with an independent finite compatibility check against
the frozen W7 columns. It is not a nonnegative-cone theorem or a source
exclusion. No large LP was run.

## Statement and exact definitions

Fix an integer `k >= 1`. Place contacts `0,...,2k-1` in their given cyclic
order. The two palettes are the even and odd indices. Let `P_k` be all
noncrossing set partitions of these contacts into exactly `k+1` nonempty
blocks, each contained in one palette. Here noncrossing means there are no
`a<b<c<d` with `a,c` in one block and `b,d` in a distinct block.

Let `V_k = F_2^{2k-2}`. Its coordinates are the phases at contacts
`2,...,2k-1`; contacts 0 and 1 have phase zero. For `p in P_k`, exclude the
two distinct blocks containing contacts 0 and 1. For each of the remaining
`k-1` blocks, take its indicator vector on the phase coordinates. Their
span is `H_p <= V_k`. These vectors are nonzero and disjointly supported,
so `dim H_p=k-1`.

Define `B_k` to have one row for each `x in V_k` and, for every `p in P_k`,
one column `1_(v+H_p)` for **every coset** of `H_p`. Repetitions, if any,
do not affect the theorem. This is the local definition used by the frozen
[template report](../../2026-10-21-w7-reuse-d5b8a86/templates/REPORT.md)
and [Fourier probe](../../2026-10-21-w7-reuse-d5b8a86/fourier/probe.py).

**Theorem.** For every `k >= 1`,

```
rank_Q B_k = binom(2k-1,k-1).
```

There is also an exact description of its Walsh support. For a frequency
`a=(a_2,...,a_(2k-1))`, put

```
A_i = a_i                           (i >= 2),
A_0 = sum of a_i over even i >= 2    (mod 2),
A_1 = sum of a_i over odd  i >= 3    (mod 2).
```

Thus each palette contains an even number of selected contacts `A_i=1`.
Read the selected contacts in order, writing `E` or `O` for their palette.
Then the Walsh character at `a` belongs to `colspan_Q B_k` if and only if
this word reduces to the empty word by deleting adjacent `EE` and `OO`.
Equivalently, the selected contacts have a noncrossing perfect matching in
which both endpoints of each pair have the same palette. The original cyclic
order is retained.

## 1. Fourier support and the anchor completion

For a subspace `H <= V_k`, the rational span of the indicator columns of
all its cosets is exactly the span of the Walsh characters

```
chi_a(x) = (-1)^(a dot x),       a in H^perp.
```

Indeed, a character in `H^perp` is constant on every coset, and is the
signed sum of their indicators. Conversely, the indicator of a coset has
the Fourier expansion

```
1_(v+H)(x) = |H|/|V_k| * sum_(a in H^perp) chi_a(v) chi_a(x).
```

The Walsh characters are independent over the rationals. Consequently
`rank_Q B_k` is the size of the union of all `H_p^perp`.

The condition `a in H_p^perp` says that the selected contacts in every
nonanchor block of `p` have even cardinality. The completed bits `A` give
even total cardinality in each palette. Since all blocks have one palette,
the anchor block of each palette then has even cardinality as well.
Conversely, even cardinality in every block implies orthogonality to the
nonanchor block indicators. We have therefore proved

```
a in union_p H_p^perp
iff some p in P_k has an even number of selected contacts in every block.
```

This is why the two anchor bits must be completed by palette parity;
setting them to zero would be a different criterion.

## 2. Noncrossing matching equivalence, including completion

Suppose such a partition `p` exists. In each block, list its selected
contacts in cyclic order and pair successive selected contacts. The pairs
within a block do not cross. Pairs in distinct blocks cannot cross by the
definition of a noncrossing partition. This gives a noncrossing
monochromatic perfect matching of all selected contacts.

For the converse, take any such matching. Draw only its pairs of even
contacts as straight chords of a circle. Let there be `r` of them. Their
endpoints are distinct and their interiors are disjoint, so these chords
divide the disk into exactly `r+1` regions. Every region contains an odd
contact on its boundary: a region has a nonempty arc of the original
circle between even contacts, and such an arc contains an odd contact.
There is no region enclosed solely by chords, since the disjoint chords
have no cycle. Assign each odd contact to its unique incident region;
an odd contact is never a chord endpoint.

Make one even block for each drawn pair, and make every remaining even
contact a singleton. There are `k-r` even blocks. Within each of the
`r+1` regions, put **all** its odd contacts into one odd block. The regions
are convex intersections of the disk with chord half-planes, so the odd
blocks can be joined inside their own regions without crossing each
other or any even chord. Hence the resulting partition is noncrossing
and has

```
(k-r)+(r+1)=k+1
```

monochromatic nonempty blocks. Every even block has zero or two selected
contacts. Each selected odd pair of the given matching lies in one
region, because its chord crosses no even chord. Thus every odd block
also has an even number of selected contacts. The constructed partition
belongs to `P_k` and meets the condition of Section 1.

This proves the equivalence without assuming a partition-completion
theorem or changing the cyclic order. Notice that the completion need
not retain the individual odd pairs as blocks; merging whole selected
pairs preserves precisely the even-cardinality condition needed here.

## 3. Matching and word reduction

A nonempty noncrossing perfect matching in a linearly ordered list has
an adjacent matched pair: take an innermost pair. Here its two letters
are equal. Delete them and continue. This reduces the selected `E/O`
word to the empty word by the rules `EE -> empty`, `OO -> empty`.

Conversely, record the pairs removed in any such reduction. At the time
of removal their endpoints are adjacent among the remaining letters.
Restoring removals in reverse order gives a noncrossing matching of
equal letters. This supplies the matching equivalence in the statement.

For an entirely explicit reduction test, scan the word with a stack:
pop when its top equals the next letter, and push otherwise. The stack
is always an alternating word. Inserting or deleting an adjacent equal
pair leaves the final stack unchanged (the two identical stack updates
compose to the identity). Therefore the word reduces to empty exactly
when this deterministic stack ends empty. No choice of reduction order
enters the criterion.

## 4. Counting the support by a path recurrence

Consider the infinite path with vertices `Z`. Label the edge
`{2j,2j+1}` by `E`, and the edge `{2j-1,2j}` by `O`. Let an `E` or `O`
letter move across the unique incident edge of that label. These moves
are involutions. A nonempty alternating word starting at vertex 0 moves
strictly along the path, reaching distance equal to its length. Adjacent
equal letters undo one another. It follows from the stack criterion
that a word ends at 0 exactly when it reduces to empty.

Now at contacts `0,...,2k-1`, independently omit or take the prescribed
letter of `(EO)^k`. Let `f_n(x)` count histories reaching `x` after the
first `n` contacts. Each step adds the current count to itself and to
its partner across the next edge matching. After `n >= 1` contacts,

```
f_n(-(n-1)+2j) = f_n(-(n-1)+2j+1) = binom(n-1,j),
                                      j=0,...,n-1,
```

and all other values vanish. For `n=1` the two counts at 0 and 1 are
both 1. In the next step the edge matching shifts by one vertex, so each
new adjacent pair receives the sum of two consecutive old pair counts.
This is exactly Pascal's recurrence, proving the formula by induction.
For `n=2k`, vertex 0 is in the pair with `j=k-1`. Thus the number of
selected subsets whose word reduces to empty is `binom(2k-1,k-1)`.

Every word reducing to empty has an even number of each letter, since
each deletion removes two equal letters. Consequently its selected
subset is uniquely the anchor completion of its bits at contacts
`2,...,2k-1`. Conversely every accepted frequency gives exactly one
such subset. The return count therefore counts frequencies, not extra
anchor choices. Together with Sections 1–3 this proves the theorem.

## Finite compatibility and negative controls

[check.py](check.py) uses only the Python standard library. It checks the
two consumed frozen files against this audit's [BASE.json](../BASE.json),
reconstructs the templates by enumerating noncrossing partitions of at
most six even contacts, and compares **every literal column support**
with the frozen templates. Its complementary-face construction keeps
all cosets and both anchors.

Independently, it extracts subgroups directly from the frozen column
supports, verifies their complete coset families, and computes the exact
union of their annihilators. At every frequency it compares that union
with the completed-word criterion, then compares it with the earlier
frozen Fourier support. No floating-point rank decision is used.

The finite ranks are `1,3,10,35,126,462`; all 5,033 template columns are
reconstructed. Three negative controls pass:

1. At `k=2`, frequency `a=3` completes to selected word `EOEO`. Both
   palettes have even total cardinality, but the only monochromatic
   pairs cross. The frozen template excludes this frequency.
2. Keeping the complete cosets of just one of the `k=2` subgroups gives
   rank 2, rather than the full-template rank 3. The theorem depends on
   the complete partition family, as well as complete cosets.
3. Replacing a legitimate `k=2` column by a diagonal support of the same
   size is rejected by literal reconstruction.

[result.json](result.json) records the exact results. Normal and seed-17
read-only replays pass; the seed changes the order of partition and
column processing, not the mathematical input. Logs are
[check-normal.log](check-normal.log) and
[check-seed17.log](check-seed17.log). From the repository root:

```sh
python3 -B audits/2026-10-21-w7-structural-30f2d19/template/check.py
python3 -B audits/2026-10-21-w7-structural-30f2d19/template/check.py --seed 17
```

## Scope and the remaining positivity gap

The theorem describes the **signed rational span** of unpruned local
columns for arbitrary `k`. In Section 1, a character is a sum of coset
columns with coefficients `+1` and `-1`. Such a reconstruction need not
give nonnegative column weights. The word criterion characterizes
linear equalities, not the facets or membership of the nonnegative cone.

The theorem neither computes exact ranks for pruned live-row shapes nor
selects an independent global equation set. In the W7 model, zero
Fourier modes on the `X` side still impose the corresponding linear
conditions on the **same shared `Z`**. They must not be discarded.
The theorem provides no new nonnegative `X`, no common positive forms,
no source gluing or realization, no original-source exclusion, and no
Lean theorem. The 112 contact types and their source-geometric
constraints remain separate from this template statement.
