# Independent B audit: minimum terminal FOUR probes

The unique smallest subset of the 15 words of length at most three that
distinguishes the supplied 132 states is

\[
\{RR,\;PRR,\;RRR\}.
\]

Each word is executed independently from the same starting state, left to
right, and only its terminal FOUR output is observed. These are three probes,
not one trajectory containing three observations. Epsilon is unnecessary.

The frozen source is `../frozen/certificate_v02.json`, SHA-256
`55109b2872294bb43dcd161635a65dff6ed3453d5c870a05ef0f3a9248e0d933`.
The audit reconstructs the 264 transitions from the supplied Boolean matrices
and checks them against the transition table before computing observations.
It also checks all four supplied refinement partitions, obtaining
`15 → 66 → 97 → 132`.

## Exhaustive minimum

Words use shortlex order, with `P < R`, and the empty string denotes epsilon.
For each subset of size at most three, the checker computes its union of
separated unordered state pairs. All 8,646 pairs must be covered.

| Number of probes | Subsets checked | Injective subsets |
| --- | ---: | ---: |
| 0 | 1 | 0 |
| 1 | 15 | 0 |
| 2 | 105 | 0 |
| 3 | 455 | 1 |

`minimum_observations.json` contains a concrete colliding state pair for each
of the 121 subsets of size below three, and the complete 132-state codebook
for the unique minimum. Among all pairs of probes, `{RR, PRR}` attains the
unique maximum of 68 output classes.

Deleting each probe gives the following independent negative controls.

| Removed probe | Remaining probes | Classes | Colliding states | Common remaining outputs |
| --- | --- | ---: | --- | --- |
| `RR` | `PRR`, `RRR` | 59 | 91, 95 | `0001`, `0111` |
| `PRR` | `RR`, `RRR` | 61 | 91, 123 | `0111`, `0111` |
| `RRR` | `RR`, `PRR` | 68 | 91, 347 | `0111`, `0001` |

## Direct reconstruction

Write the ten source support bits in certificate row order as

\[
(x_0,\ldots,x_9)
= (01012,01021,01023,01201,01202,01203,01212,01213,01231,01232)
\]

where a row label on the right denotes its support indicator. The FOUR
output order is `(01232, 01021, 01202, 01212)`. Boolean multiplication of the
supplied operators gives

\[
\begin{aligned}
a=O(\delta(q,RR))&=(x_2,x_4,x_0,x_1),\\
b=O(\delta(q,PRR))&=(x_5,x_9,x_7,x_3\lor x_8),\\
c=O(\delta(q,RRR))&=(x_8,x_6,x_1,x_3).
\end{aligned}
\]

For component indices `1,…,4`, the inverse is

\[
(x_0,\ldots,x_9)
=(a_3,a_4,a_1,c_4,a_2,b_1,c_2,b_3,c_1,b_2).
\]

The two redundant output relations are `c₃ = a₄` and `b₄ = c₄ ∨ c₁`.
The formulas are obtained by applying the Boolean operators to each of the
ten singleton masks. A separate check reconstructs all 1,024 formal masks
and obtains 1,024 distinct probe signatures. Three probes are also optimal
for that algebraic domain: two four-bit outputs admit at most 256 values.
The unique minimum within the 15-word pool remains the same, since a set
injective on all formal masks must be injective on its 132-state subset.

The formal-mask extension is an identity of the supplied Boolean operators.
It does not assert that all 1,024 masks arise from planar graphs. The audit
does not reconstruct literal fibre counts, identify source graphs, preserve
an original fixed boundary through `P`, or establish a global colouring
theorem.

## Reproduction

From the repository root:

```sh
python3 -B audits/2026-10-19-c5-observation-depth-ed59843/B/replay_minimum_observations.py --check
```

This command compares the archived result byte for byte against a fresh
independent replay and passed. To regenerate into a new path, omit `--check`
and pass `--output /tmp/c5-minimum-observations-new.json`. Writing uses
exclusive creation and refuses to overwrite an existing result. The script
uses only the Python standard library and reads no main checker or other
agent implementation.
