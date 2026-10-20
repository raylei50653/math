# Same-coloring joint Kempe boundary state: fixed-catalogue experiment

## Result and exact scope

The state consisting of the literal boundary colors and the six boundary
partitions induced by the actual maximal bicolour components of **one full
proper coloring** does not determine its own successor under a rooted Kempe
swap. This already fails on the fixed 8-vertex catalogue cell `95`, on one and
the same source graph and ordered boundary `B=(0,1,2,3,4)`.

The experiment enumerates exactly the 132 saved graph representatives in the
frozen `cells.json`. For each graph, all ten prescribed literal boundary
fibres are retained, including empty fibres, and every full extension is
saved in `certificate.json`. The source words use the ten canonical boundary
patterns, but **no target word or individual component system is normalized**.
All colors, vertices, and source/target comparisons use a single literal frame.
This is a finite certificate, not a general coverage or source-realizability
result. The fixed catalogue graph is not claimed to be a realization of the
live `941 / J1 / 01021` source contract.

## Definition

For a full coloring `c` and unordered pair `ab`, let `C_ab(c)` be the full
maximal components of the subgraph induced by colors `a,b`. Let `pi_ab(c)` be
the nonempty intersections of these components with the ordered boundary.
The state is

`S_B(c) = (c|B, pi_01(c), pi_02(c), pi_03(c), pi_12(c), pi_13(c), pi_23(c))`.

An action is `(unordered color pair, boundary root)`. It is enabled exactly
when the root has a color in that pair, and swaps the **entire actual maximal
component containing that root**. Each full lift has 15 enabled rooted
actions. Components without boundary contacts are retained in the witness's
full component systems, although they do not define rooted actions here.

The full source graph is fixed externally; this experiment does not compare
independently feasible graphs, rotated frames, or six independently chosen
colorings.

## Explicit counterexample

The source graph has vertices `0,...,7`, boundary cycle `0-1-2-3-4-0`, and
non-boundary edges

```
05 06 07 17 25 26 27 36 46 56 57
```

The complete edge list and an oriented combinatorial disk certificate are in
the certificate. The nine oriented faces are

```
(0,1,7) (1,2,7) (2,3,6) (3,4,6) (4,0,6)
(0,5,6) (2,6,5) (0,7,5) (2,5,7)
```

The checker verifies opposite interior edge incidences, precisely the ordered
outer cycle, Euler characteristic 1, and a connected path/cycle link at every
boundary/interior vertex.

Take full literal source colorings

```
c = 01012132
d = 01012233
```

Both have boundary `01012`. Their six boundary partitions are identical:

| Pair | Both source partitions |
|---|---|
| 01 | `{0,1,2,3}` |
| 02 | `{0,2,4}` |
| 03 | `{0,2}` |
| 12 | `{1} / {3,4}` |
| 13 | `{1} / {3}` |
| 23 | `{4}` |

Use the same rooted action `((1,2), root=1)`. In `c`, its full component is
`{1,5,7}`; in `d`, its full component is `{1}`. The targets are

```
c' = 02012231
d' = 02012233
```

Both target boundaries are `02012`, but two target partitions differ:

| Pair | At c' | At d' |
|---|---|---|
| 01 | `{0,2,3}` | `{0} / {2,3}` |
| 23 | `{1} / {4}` | `{1,4}` |

Thus no deterministic update function `F_G(S_B, pair, root)` can produce the
next `S_B` even on this fixed graph. The literal next boundary word *is*
determined by `S_B`: swap precisely the boundary block containing the root.
The failed claim concerns closure of the six-partition summary under update.
It does not rule out nondeterministic transitions, retained private contacts,
or a further refined state.

The discrepancy becomes a boundary observation after the same second action
`((0,1), root=0)`. Its full component is `{0,2,3,7}` at `c'` and `{0}` at `d'`.
The resulting full words are `12102230` and `12012233`, whose literal
boundaries are `12102` and `12012`. Thus the initial joint summary does not
determine the two-step boundary observation either. This is a direct
derivation from the recorded full first-step targets; the stable v1 checker
does not separately include a second-step certificate.

For this graph, the complete ten-fibre cardinalities, in the frozen pattern
order, are `3,3,2,1,1,0,1,0,0,0`. In particular, the `01012` fibre is exactly

```
01012132
01012133
01012233
```

The witness keeps both full source and target colorings, the selected full
components, and all six full component systems before and after each swap.

## Exhaustive finite counts

| Quantity | Count |
|---|---:|
| Fixed graphs | 132 |
| Boundary fibres, including empty | 1,320 |
| Empty fibres | 405 |
| Full literal lifts | 1,810 |
| Joint states, summed separately per graph | 1,280 |
| Boundary fibres distinguished further by joint state | 310 |
| Graphs with such a distinction | 120 |
| Enabled rooted actions on full lifts | 27,150 |
| Distinct joint-state/action pairs | 19,200 |
| Joint-state/action pairs with multiple target joint states | 1,229 |
| Joint states with at least one such ambiguous action | 290 |
| Graphs with a collision | 90 |

The joint state therefore does retain information absent from boundary colors,
but equality of joint states does not define a deterministic rooted-action
quotient. Counts of states and ambiguities are scoped to the ten canonical
literal source fibres; no independent palette quotient is applied to targets.

## Reproduction and negative controls

From the repository root:

```
python3 -B audits/2026-10-20-joint-kempe-state-1148ce0/experiment/check.py --check
```

The standard-library checker regenerates the entire result in memory and
requires byte equality with the saved certificate. `--check` writes nothing;
`--generate` opens its output with exclusive creation and cannot overwrite an
existing certificate. The certificate records hashes of the frozen catalogue
and checker. It is 78,897 bytes.

The checker rejects four deliberately corrupted witnesses: a deleted source
edge, an improper full coloring, an incomplete selected component, and a
forged target signature. These rejection checks are included in every run.

`--generate` and `--check` both passed. No broad graph search, `811`
enumeration, Lean proof, source-941 exclusion, or smaller-bad construction was
performed.

See `CUSTODY.md` for a transient post-pass v2 edit and restoration. Only the
restored v1 names `check.py` and `certificate.json` are the stable experiment
evidence. The separate reconstructed transient-v2 files are historical
reconstructions, not additional frozen evidence.
