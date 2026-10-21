# The 103-column residual: four full stars and a nonnegative source chain

2026-10-21. Audit BASE `30f2d19275657393b7354ed75eca31439d8ee12b`;
mathematical BASE `d5b8a8605bcbcef7aebbcf1934dad7ba255ccf02`.
All authority input hashes are recorded in [BASE.json](../BASE.json).
This work runs no LP and changes no frozen input.

## Source and exact scope

Assume the entire frozen [strict only-R/W7 source contract](../../2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)
and [complete count model](../../2026-10-20-w7-count-cone-d5b8a86/MODEL.md).
In particular, one actual arbitrary-size core `F13` supplies every `Z` and
every complete Kempe orbit, with all private component multiplicities.
The ordered rim is `(a,n,u4,u3,u2,u1,L,q,c,s,v,w,t)`.
The symbols `Z_i` refer to the fixed canonical literal states of the frozen
model; no source is selected separately for different palette words.

The existing integer potential gives

```
2 Z44459 = sum_(103 columns) X - sum_(95 columns) X - 2 sum_(8 columns) X.
```

The desired reverse inequality on the two sides of this difference is
**equivalent to `Z44459=0`** under this identity and nonnegativity. It is a
valid theorem target, but naming it compensation does not establish a new
mechanism. The following decomposition locates the missing mechanism.

## Exact palette-block decomposition

Every exchange column has a fixed literal binary palette-membership word.
Regroup the 13 original half-row weights by this word. The same original
equations `2Z_i=sum X` then give seven separate exact laws. All 307,197
columns, including the zeros in each displayed block, are checked.

| Literal palette word | Half-row state expression on the left | Nonzero prices on the right |
| --- | --- | --- |
| `0010101101001` | `2(Z44459-Z44480)` | none; all 288 block columns have price zero |
| `0111111010010` | `2(Z44480-Z44541)` | two columns of price -1 |
| `0101010101011` | `2(Z44541-Z784-Z37416-Z46468-Z66394)` | 93 columns of price -1, eight of price -2 |
| `0101011011001` | `2Z784` | 42 columns of price +1 |
| `0110101011001` | `2Z66394` | 42 columns of price +1 |
| `0111010011001` | `2Z37416` | 14 columns of price +1 |
| `0111101111001` | `2Z46468` | five columns of price +1 |

Consequently every common feasible count vector, and hence every original
source under the stated contract, satisfies

```
Z44459 = Z44480 <= Z44541 <= Z784+Z37416+Z46468+Z66394.
```

This is an exact source-valid chain, not a claim that these counts are
positive or that the necessary cone has a common feasible point.

The four positive families are **complete marked-phase stars** of the
unpruned universal templates with half-run counts `5,5,4,3`. For each
marked phase, every universal template column containing that phase
survives the frozen zero closure: respectively `42,42,14,5` columns.
The checker compares the actual original column IDs, local template IDs,
and the entire universal marked-phase support. These are not estimates
or counts inferred from a sample.

This explains what a source theorem must add: the existing necessary
closure has not removed any possible partition choice at these four
marked phases. A true source can still be much more constrained than
the universal phase stars.

## Two precise limits on naive repairs

**Same-palette orbit flips.** All positive-priced columns occur in the
four positive words in the table. All negative-priced columns occur in
the other two nonzero-price words. No price block has both signs.
A component flip within a fixed palette preserves the binary membership
word (indeed, it stays within that actual Kempe orbit). Thus no composition
of only those flips can map a positive-priced orbit to a negative-priced
orbit. A proof by weighted injection must add a cross-palette operation
or a new source restriction; it cannot be obtained by that within-orbit
action alone. This does not rule out a more general injection.

**Direct chord-zero forcing.** The optional original C13 chords that make
target state `44459` improper are exactly

```
s-u2, s-u4, w-u1, w-u3.
```

For auxiliary state `66394`, the corresponding list is only

```
w-u1, w-u3.
```

Therefore any optional chord set compatible with target `44459` is also
proper on auxiliary state `66394`. Direct same-colour chord tests alone
cannot kill all four auxiliary states in the chain while preserving
this target. This is **not** a proof of common feasibility and does not
exclude further orbit closure, topology, or minimality arguments.
[result.json](result.json) records the full direct chord check for all
112 original complete profiles; each profile retains its original ID.
The later geometric exclusions are owned by [geometry](../geometry/PROOF.md).

## Verification and current boundary

[check.py](check.py) uses the standard library and independently recomputes
all state coefficients, all column prices, seven block laws and four full
stars from the pinned original files. It does not import the numerical
solver. It rejects a lost positive column, changed target coefficient,
and corrupted palette map by exact certificate comparison. No claim here
depends on floating-point residuals.

```
python3 -B audits/2026-10-21-w7-structural-30f2d19/compensation/check.py
python3 -B audits/2026-10-21-w7-structural-30f2d19/compensation/check.py --seed 17
```

Default execution is read-only; `--build` exclusively creates a new local
result file. The seed changes traversal order while the complete result
must remain identical. Evidence is a finite exact decomposition plus the
existing paper source-to-orbit counting theorem, not a new Lean theorem.
Neither target emptiness, strict W7 exclusion, the general J1/J2 branches,
a smaller bad source nor a source realization has been established.
The current stopping point is summarized in the [parent report](../REPORT.md).
