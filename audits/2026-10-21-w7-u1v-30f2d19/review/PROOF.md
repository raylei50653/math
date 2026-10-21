# Independent original-u1v source-exchange review

**Verdict:** the same literal `A -> M -> F` source maps prove this u1v
branch empty. Their component classification has no original-u3v
prerequisite. No reflection, u1/u3 renaming, or independent marginal
witness is used. In particular,

```
Z44459 = Z44466 = X48617 = X67755 = 0.
```

This closes the eight named profiles `68,69,78,79,88,89,92,93` under the
fixed strict original-source contract. The parent W7/J1/J2 questions
remain OPEN.

## Fresh inputs and the hidden-prerequisite check

[check.py](check.py) independently reads the original pinned
[source contract](../../2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md),
[complete orbit-count proof](../../2026-10-20-r6-941-j1-five-edge-417732f/counting/PROOF.md),
caps and full orbit family. It compares their bytes and SHA256 values
with this audit's [BASE.json](../BASE.json). It also reads the frozen
pre-u3v profile certificate to verify the exact eight-profile coverage.
It does not read any u3v-audit result, transport checker, or closure.

All 307,197 original surviving columns are scanned. This family is the
original common necessary family, with inherited cap/C10 zeros and
shared-state closure, before adding a specific optional chord such as
u1v or u3v. Its coverage allows original rim chords without assuming
either chord present.

Every one of the eight profiles has actual original edge u1v, and none
has u3v. Thus a supposed u3v prerequisite would not cover these source
profiles. The fresh checker explicitly verifies this and rejects a
certificate that adds u3v as a required extra edge.

## Exact literal maps and six-column coverage

The ordered original rim remains
`(a,n,u4,u3,u2,u1,L,q,c,s,v,w,t)` throughout:

```
A = 44459 = (0,1,2,1,2,1,2,3,1,2,0,1,2),
M = 44111 = (0,1,2,1,2,1,2,0,2,1,3,1,2),
F = 44127 = (0,1,2,1,2,1,2,0,2,3,1,3,2).
```

A's `03|12` half-row 12302027 has exactly one incident original column,
306985. Its complete boundary components are

```
03: {a}, {q,v};
12: {n,u4,u3,u2,u1,L,w,t}, {c,s}.
```

For every complete colouring of the same D with rim A, flip the whole
actual component `K03(q)` and the whole actual component `K12(c)`.
Their rim changes are respectively `q:3->0,v:0->3` and `c:1->2,s:2->1`;
the image is M. In particular, u1 and u3 both remain 1. These disjoint
palette operations preserve their induced graphs and commute. Each
whole-component flip is an involution, giving an injection of full
fibres `Col_D(A) -> Col_D(M)`.

M's `02|13` half-row 10064313 has exactly five incident original columns:

```
147448, 147449, 167802, 226130, 231666.
```

Each independently recovered partition has the **same** complete
boundary block `K13(v) intersect rim={s,v,w}`. It excludes both named
vertices u1 and u3. Flipping that whole actual component changes
`s:1->3,v:3->1,w:1->3`, and gives F, still with u1=u3=1. This is another
involution on its natural complete-colouring domain, hence an injection
`Col_D(M) -> Col_D(F)`.

The fresh checker recovers the partitions by testing whether the
low-colour-bit difference of two same-palette rim positions is constant
over the full column. Distinct components have independent flips, so
their relative bit varies, even with one normalization anchor fixed.
The checker then regenerates each complete normalized coset from the
recovered blocks and requires equality with every original row. All six
columns' full row supports and partitions are saved in
[result.json](result.json).

The numerical source-count version uses the original nonnegative
shared-source equations `2Z_i=sum X_j`: column 306985 contains M's
half-row 12301211, and all five middle columns contain the same F
half-row 10064365. These **complete** incidence comparisons give

```
0 <= Z44459 <= Z44111 <= Z44127.
```

They do not combine separately chosen witnesses or source graphs.

## Original-u1v contradiction and the requested two X values

F has `u1=v=1`. The actual original edge u1v therefore makes its whole
complete D fibre empty. Equivalently, if an M colouring existed, its
original edge u1v would put u1 in `K13(v)`, contradicting the forced
boundary block `{s,v,w}`. Thus the full-fibre injections imply
`Z44459=0`.

The other witness 44466 also has `u1=v=1`, so `Z44466=0` directly on
that same original edge. The original actual path witness requires
`Z44459+Z44466>0`, a contradiction in the same source.

Both requested columns 48617 and 67755 contain A's `01|23` half-row
6712710. Once A's complete count is zero, that row's nonnegative
equation forces both X values to zero. This conclusion is about the
original X coordinates with all private-component multiplicities.

## Complete core and cap-lift scope

Every operation acts on the same complete actual core
`D=G-{b,p,h,R,x,y,r}` and carries **all** private vertices of its actual
component. It is not a boundary-only recolouring and does not delete,
identify, or replace any attachment.

The operations need not preserve one chosen extension assignment on
the deleted original cap vertices. The Z authority counts all complete
D colourings, including those without a G extension; the same original
G/Q1/J1 caps retain all original stars and re-quantify every lift on
the current D colouring. Thus the source zero and coverage authorities
remain applicable after the first operation. No invariance of a
selected type-III history or path-witness subfamily is assumed.

The proof uses the literal fact that u1 stays 1 and F has v=1. It does
not transfer an u3v statement by symmetry or alter the original rotation.
The inherited source contract and zero fibres are essential; this is
not a claim about an arbitrary C13 disk with a chord u1v.

## Controls and replay

Normal and seed-17 optimized read-only replays pass:

```sh
python3 -B audits/2026-10-21-w7-u1v-30f2d19/review/check.py
python3 -B -O audits/2026-10-21-w7-u1v-30f2d19/review/check.py --seed 17
```

The six rejected corruptions are: omitting a complete middle partition,
flipping only v, substituting a proper middle state as the terminal
edge-zero state, adding a hidden u3v prerequisite, restricting the full
fibres to an unproved history subfamily, and substituting the old u3v
requested column ID. Flipping only v also fails properness on the
ordinary C13 rim itself, confirming why the whole actual component
matters. Logs: [normal.log](normal.log),
[seed17-optimized.log](seed17-optimized.log).

No LP, new original-graph enumeration, source contraction, smaller-bad
construction, or Lean modification is part of this review.
