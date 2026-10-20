# A return injection excludes the original degree-five r branch

This is an arbitrary-size paper argument on actual complete colourings of
the same plane disk. It uses neither the Four Colour Theorem nor graph
enumeration. Its source scope is the fixed original branch
`d_G(x)=d_G(y)=d_G(b)=4` of
[SOURCE_GEOMETRY](../../2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md).

## 1. The local return lemma

Let H be a finite plane disk with the four distinct outer vertices
`(z,s,v,t)` in that Jordan order, and let pq be an edge of H. Retain one
common colour frame `(A,B,C,D)`. Suppose H has no complete proper colouring
whose four outer vertices all have different colours.

Write `E` for the set of **all complete H colourings** with outer word
`ABAC` and unordered pq palette `{B,C}`. Write `T` for the set of all
complete H colourings with outer word `ABAB` and the same palette `{B,C}`.
There is an injection

`E -> T,    f |-> switch K_f(t;BC)`.

Here K is the actual maximal two-colour component in the original H.

**Proof.** In each f in E, z and v belong to the same AD component.
Otherwise switching the AD component of v fixes z,s,t and produces the
rainbow outer word ABDC, contrary to the hypothesis. An AD path from z to v
and a BC path from s to t would be vertex-disjoint paths with alternating
endpoints on the disk boundary. Hence s and t lie in different BC
components. Switching the BC component containing t therefore changes
exactly t among the four outer vertices, yielding ABAB. Because pq is a BC
edge, p and q belong to the same BC component: the switch either fixes both
or interchanges their two colours. Their unordered palette stays `{B,C}`.
Finally, switching a maximal BC component preserves its vertex set, so
switching the target's BC component of t again recovers the full original
colouring. This proves injectivity on complete colourings, including all
interior vertices. No fibres from different graphs have been combined.

Its exact image is `T0={g in T : s,t lie in different BC components}`.
Indeed the switch preserves the two distinct component vertex sets, so its
image is contained in T0. Conversely the same t-component switch sends
every g in T0 back into E, again preserving the pq palette. Thus this is
the complete-fibre bijection `E <-> T0`, with an explicit common inverse.
It need not be a surjection onto all of T: a general member of T could
have s,t in one BC component. No assertion of general Kempe connectivity
is used.

## 2. Apply it to the original r deletion

Assume for contradiction that `d_G(r)=5` in the fixed source branch. The
already established literal deletion produces `R'=R-r`, a triangulated
disk with induced outer cycle `(z,s,v,t)`, with its original internal edge
pq. Its total vertex count is k and its interior count is `k-4<k`.
The relative C4 classification forces its outer relation to be mask7, and
the same-source joint-fibre lemma gives the following **universal** table:

| R' outer word | pq palette in every complete colouring |
| --- | --- |
| ABAB | `{C,D}` |
| ABAC | `{B,C}` |
| ABCB | `{C,D}` |

These are the statements of
[SOURCE_GEOMETRY §5](../../2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md).
In particular, mask7 supplies a nonempty ABAC fibre and forbids the rainbow
fibre. The return lemma maps that nonempty ABAC fibre into T, but the ABAB
row of the table says T is empty. This is a contradiction.

In fact this final step needs no fresh invocation of the relative C4
classification. The literal r-lift table directly gives both facts:

- A rainbow R' colouring `ABCD` has the unique r-colour A, producing an R
  colouring `ABAD`, a forbidden ABAC type.
- A complete R colouring with outer word `ABCD` has v forced to A, since
  v is adjacent to s=B, r=C and t=D. Delete r and globally interchange C,D
  to obtain a complete R' colouring `ABAC` with pq palette `{B,C}`.

The ABAB row above also follows directly from its two r-lifts C and D:
the original R ABCB missing-colour theorem requires pq to contain D for
the first lift and C for the second lift, while both use the same p,q
colours. Hence pq is `{C,D}`. The contradiction therefore requires only
the original R full-fibre hypotheses, the original degree-three r
deletion geometry, and the return lemma, without reclassifying R'.

Thus the stronger source conclusion is

`d_G(x)=d_G(y)=d_G(b)=4  ==>  d_G(r)>=6`.

The preexisting original interior degree bound is `d_G(r)>=5`, so excluding
equality gives the displayed bound. No assumptions on `d_G(p)` or `d_G(q)`
were added. The attempted subsequent degree-three deletion at s or t is
unnecessary in this branch, because its degree-five r premise is now
excluded. This does not provide lower bounds on s,t in the surviving
`d_G(r)>=6` branch.

## 3. Where the new return comes from

The earlier maps on R transported ABAB and ABCD into disjoint sectors of
ABCB. Deleting the original degree-five r yields the smaller R' and, crucially,
forbids its rainbow outer fibre. This forces an AD connection in every
ABAC lift. The **same colouring's** complementary BC disconnection then
allows the return switch to ABAB while the actual edge pq protects its
unordered palette.

All connectivity assertions here are within one complete colouring. The
AD connection and BC disconnection are used together before the switch;
the switch component has an exact inverse afterward. This supplies the
missing local injection without a count-only argument or separately
chosen path witnesses.

## 4. Finite replay and limits

[check_return.py](check_return.py) independently enumerates every six-pin
assignment and every terminal component partition for each complementary
colour-pair split, with the honest outer C4 and mandatory edges of the
original six-pin skeleton. Its certificate records that the two ordered
ABAC rows fail immediately, leaving only the ABAB and ABCB outer types.
It also explicitly checks all three BC terminal partitions possible for
each ABAC pq orientation once the forced AD connection is imposed. Each
produces the forbidden ABAB pq palette by the stated return switch.

Three explicit small triangulated C4 disks supply nonvacuous controls.
The checker enumerates and saves their entire complete fibres under each
fixed outer word. One shows that removing the no-rainbow hypothesis allows
a nonempty E with empty T; one has no rainbow and verifies the bijection
on actual nonempty E and T0; the third has no rainbow and forces pq=CD in
ABAB but retains ABAC with a different pq palette, showing why the source's
universal ABAC row is essential to the contradiction.

The finite replay checks the complete local partition model; it does not
construct an actual target graph or identify complete fibres across
different graphs. The arbitrary-size result is proved in §§1–2, not inferred
from bounded graph search.

Run:

```sh
python3 -B audits/2026-10-14-c4-c5-recursion-fdd3e22/fibre/check_return.py --check
```

The general mask13 six-pin branch, the possibility of p or q having original
degree five, and the unbounded C5 catalogue equality remain OPEN. No new
source realization or Lean theorem is asserted. The previous conditional
`r=5, p,q>=6 => k>=29` subdomain is now empty, and is retained only as
historical evidence; it must not be presented as a remaining live branch.
