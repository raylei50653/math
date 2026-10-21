# Independent same-source exclusion check for the original edge u3v

The independent reconstruction proves the requested two columns vanish:

```
X66582 = X67755 = 0,
Z44459 = Z44466 = 0.
```

This excludes the eight fixed u3v profiles under the complete strict-W7
source contract, since that contract supplies `Z44459+Z44466>0` on the
same original core. The argument already follows from the one original
edge u3v; all seven other profiles add edges to that minimal case.
Consequently u3v is necessarily absent in this strict original-source
branch. The prior 40 necessary target-compatible profiles reduce to 32;
the parent strict-W7 problem remains OPEN.

The frozen authorities are this audit's [BASE.json](../BASE.json), the
[complete-source contract](../../2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md),
[source geometry](../../2026-10-20-r6-941-j1-five-edge-417732f/geometry/PROOF.md),
and [complete orbit-count proof](../../2026-10-20-r6-941-j1-five-edge-417732f/counting/PROOF.md).

## Independent compact source-exchange review

After the synchronous check below, the transport work found a much shorter
proof. I independently re-read the pinned literal states and scanned the
complete frozen column family for all their half-row incidences. The
following exact facts hold before imposing the new edge zero:

```
A = 44459 = (0,1,2,1,2,1,2,3,1,2,0,1,2),
g = 44111 = (0,1,2,1,2,1,2,0,2,1,3,1,2),
l = 44127 = (0,1,2,1,2,1,2,0,2,3,1,3,2).

A, 03|12 half-row 12302027: support {306985};
g, 03|12 half-row 12301211: support
    {306972,306983,306985,307044,307049};
g, 13|02 half-row 10064313: support
    J={147448,147449,167802,226130,231666};
l, 13|02 half-row 10064365: support exactly J.
```

Nonnegativity and these complete incidence sets give the sharper chain

```
Z_A <= Z_g = Z_l.
```

The last state has `l[u3]=l[v]=1`, so the actual original edge u3v
forces `Z_l=0`. This already proves the exclusion and vanishing of the
two requested X values. Unlike the long residual, this proof only needs
three named states and the displayed complete incidence comparisons.

The source maps also check independently. Recovering components by
same-palette XOR variation profiles of all rows of column 306985 gives

```
{a}, {q,v}, {c,s}, {n,u4,u3,u2,u1,L,w,t}.
```

Consequently every complete D-colouring with rim A has
`K03(q) intersect rim={q,v}` and `K12(c) intersect rim={c,s}`.
Flip both **whole actual components**, including all their private
vertices. The resulting rim is exactly g. Each flip preserves its
induced palette graph, and the other flip uses the complementary
palette, so they commute and their composition is an involution on
complete D-colourings with q in 03 and c in 12. Its restriction gives an injection from the
full A fibre into the full g fibre.

Independently recovered profiles for all five columns in J have
`K13(v) intersect rim={s,v,w}`. Flipping that whole actual component
changes the rim from g to l. This is an involution on complete
D-colourings with v in 13. The identical complete support on the l side also shows
that its inverse applies to every complete l-colouring. Thus these two
full fibres are in bijection, consistent with `Z_g=Z_l`.

Equivalently, on an actual source containing u3v, any g-colouring would
have u3 in `K13(v)` directly from the original edge, contradicting the
forced boundary contact set. The flip-to-l description expresses that
same contradiction as a proper-colouring-preserving operation whose
claimed image would be improper on an original edge.

The operations act on the same full original **core D**. They need not
keep one previously chosen extension assignment on the deleted cap
vertices. The Z authority counts every complete D-colouring, with all
original cap lifts re-quantified as in the source counting proof. No
history or particular cap extension is assumed invariant.

**Review verdict.** The direct `A -> M -> F` complete-core injections
are sound, including their component coverage and all private vertices.
The distinction between a complete D-colouring and a fixed original-G
cap assignment is essential and is stated correctly in the transport
proof. I independently ran its read-only checker and the compact numeric
checker with malformed-proof controls; both passed. The latter establishes
the sufficient inequality chain, and does not need the stronger middle
equality observed above. No mathematical bug was found. This closes the
eight user-named profiles while leaving the remaining parent branch OPEN.

## Why the finite zero rules are valid on the original source

Fix the same arbitrary-size original core D, including every original
attachment and private vertex. `Z_s` counts all complete colourings with
the fixed literal boundary colours of canonical state s. The original
edge u3v gives

```
Z_s = 0 whenever s[u3] = s[v].
```

Endpoint equality is invariant under a global colour permutation, so it
is sufficient to check the canonical tuple; no choice of colour gauge
changes this zero. This supplies 15,382 additional zero states among
the 61,308 previously live frozen states.

For each normalized half-row h, the complete actual component-orbit
construction gives the shared-source equation

```
2 Z_(i(h)) = sum_(j: h in C_j) X_j,      Z >= 0, X >= 0.
```

The frozen family contains every possible actual complete orbit column;
the original source's X values include the positive multiplicities of
all private components. Extra necessary columns in that family merely
relax the model. The following two implications are therefore valid:

1. If any state represented in a complete column is zero, its X value
   is zero. This follows from that half-row equation and nonnegativity.
2. If every column supporting one half-row h has X zero, then
   `Z_(i(h))=0`. This is the original equation itself. The resulting Z
   zero applies to **all three** half-rows of that canonical state,
   which use the same complete-source count.

Starting from the inherited frozen zeros and the actual-edge zeros,
induction makes every subsequent zero a consequence on the same D.
There is no invariance assumption for a selected type-III history or a
selected five-edge-path subfamily: the exchanged orbits are those of
all complete colourings of D. No private colouring multiplicity is
discarded, and no independent profile or palette witness is substituted.

## Independent algorithm and result

[independent.py](independent.py) does not import the root closure
implementation. It uses a different algorithm and representation:
each synchronous round rebuilds the complete set of eligible columns
from the current live-state set, takes their full half-row support,
and retains only states whose three original half-rows all remain
supported. It uses no queue or degree-decrement counters.

Only the pinned caps and complete original orbit family are used in
this derivation. Their byte SHA256 values are checked against BASE.
The root residual is read **after** the independent fixed point has
been computed, solely to compare every final live state and column.

The independent fixed point has 35,132 live states and 70,343 live
columns, exactly matching the root's profile-10 residual. It adds
10,794 propagated state zeros beyond the 15,382 original-edge zeros.
Fifteen synchronous rounds include the final no-change round.

The target is eliminated much earlier:

| Synchronous stage | Z44459 | Z44466 | X66582, X67755 |
| --- | --- | --- | --- |
| Original-edge initialization | not yet forced zero | zero | not yet forced zero |
| Round 1 | not yet forced zero | zero | both still supported |
| Round 2 | zero | zero | both still temporarily present in the previous-state column filter |
| Round 3 | zero | zero | both zero |

In particular, neither requested column is directly improper on u3v:
its entire normalized orbit support is proper on that edge. The new
exclusion uses a different palette half-row and the shared canonical
Z count. Once `Z44459=0` is proved there, its 01|23 equation gives

```
0 = 2 Z44459 = X66582 + X67755,
```

so nonnegativity forces both requested X values to zero. Since B is
already improper on u3v, both possible witness fibres vanish. This is
a source exclusion, not an inference from residual support survival
to common-count feasibility.

## Controls and replay

[independent.json](independent.json) saves the full round trace, hashes,
fixed-point counts, and comparison result. Four controls exercise real
proof gates:

- With no new edge zeros, the original complete family is already a
  fixed point and loses no live state or column.
- State 44459 is proper on u3v and is rejected as a purported direct
  original-edge zero leaf.
- Both requested columns survive the initial complete-column edge
  filter; the later elimination requires propagation through shared Z.
- Reinserting 44459 into the final live-state residual is rejected by
  exact comparison with the independently derived set.

Normal and reordered seed-17 optimized read-only replays pass. The
seed changes column-processing order; synchronous sets and the trace
are unchanged. Explicit checks remain active under `python -O`.
Logs: [normal.log](normal.log),
[seed17-optimized.log](seed17-optimized.log).

```sh
python3 -B audits/2026-10-21-w7-u3v-30f2d19/review/independent.py
python3 -B -O audits/2026-10-21-w7-u3v-30f2d19/review/independent.py --seed 17
```

## Boundary of the conclusion

The new exclusion is conditional on the fixed original-source
contract and the actual original edge u3v. It covers all eight named
profiles by the minimal one-edge case and monotonicity of added edge
zeros. It does not supply a corridor contraction, a smaller bad graph,
or a theorem for the remaining strict-W7 profiles, a general C7
pocket, general J1/J2, or Lean. No LP or new original-graph enumeration
was used.
