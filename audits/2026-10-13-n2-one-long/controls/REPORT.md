# One-long named full-fibre and boundary controls

2026-10-13. All files in this directory are newly created audit products. The
four frozen inputs and their exact bytes/SHA are in [BASE](BASE.json). The
main artifact is [observations.json](observations.json); its SHA256 is
`516c44fc1480002c4fe358ea5ce0cc69349d55ed463427c685db42ec887ec2a7`.

These are fixed local/full-graph controls and exhaustive arithmetic on five
named boundary points. **No original N2 source search was performed. Complete
target source status is `not triggered`; the controls do not assert source
exclusion.** Arbitrary-size mathematical exclusion belongs to the accompanying
paper argument, not these finite controls.

## 1. Literal original controls

Boundary order is `0,1,2,3,4`, roots are `r=9,s=10`. Every path is the same
literal four-vertex path `5–6–7–8`; original r-contacts are `5,6`, original
s-contacts are `7,8`. The three fixed attachment schedules are:

| Control | Attachments at `5,6,7,8` | Actual support | Rejection mask on `I={0,1,3}` |
| --- | --- | --- | --- |
| Original four-contact countercontrol | `01;0;2;12` | `012` | `I` |
| Four-support path | `01;0;3;23` | `0123` | empty |
| Five-support path | `01;2;3;34` | `01234` | `{3}` |

The first control's complete ten-row/16-pin fibres agree exactly with the
frozen 2026-10-11 certificate. It has original degree four, distinct root
contacts, and distinct endpoint boundary-edge attachments. Its three empty
diagonal fibres include literal bridge-palette witnesses. It remains a
`counterexample` only to a proposed escape based on these local conditions;
it is not an N2/E-ARC2 counterexample.

The fixed short is original vertex `11`, joined to `r,s,3,4`. It accepts every
diagonal cell. For each long, four fixed external spoke schedules are used:
`r0,r4,s1,s2`; no spokes; `r0`; `r0,s1`. The first schedule gives both roots
complete degree five; all schedules are calibration graphs. Disk rotation and
Σ-criticality are not supplied/claimed.

## 2. Complete named partitions and same-row joins

All ten proper C5 boundary-color partitions, all 16 **ordered** literal root
pins, every complete original tuple, and all empty cells are retained. The
ten boundary rows are also independently regenerated as restricted-growth
proper C5 colorings with at most four colors.

For each piece, the interface order is its actual named boundary support,
followed by `r,s`. Each cell records its full named equality partition,
representative, and one common S4 permutation acting on **every coordinate**
of the representative's original tuple. Exact transported tuple sets must
equal independent Cartesian-product enumeration.

The catalogue includes every named support of sizes three, four, five:

| Actual support type | Full named partition cells |
| --- | ---: |
| Consecutive three-point arc | 26 |
| Nonconsecutive three-point support | 36 |
| Any four of the five boundary vertices | 74 |
| All five boundary vertices | 160 |

The four-point count retains the five proper path patterns: one two-color
pattern with ten pin orbits and four patterns with sixteen, giving
`10+4×16=74`. All ten five-point patterns use at least three colors, so their
color stabilizer is trivial and the full count is `10×16=160`. No Eq/Diff
two-bit representation is applied to four/five-point support.

The local enumerator is exhaustive Cartesian product. A separate MRV DFS
enumerates the whole literal graph. Every same-row/same-pin Cartesian join,
including its original external factor, must equal direct whole-graph fibres.
Unpinned global DFS independently checks the union over all sixteen root pins.

The main certificate stores 640 local cells (64 empty; 1,688 full local tuples),
1,920 same-row join cells (981 empty), 120 unpinned global DFS comparisons, and
2,560 cells in sixteen named-support catalogues.

## 3. Common-color and boundary signature witnesses

For each fixed graph let `T` be the original root-spoke support and `W` the
boundary-neighbor union of original long contacts. For **each** row and each
`a∈q(W)\q(T)`, the certificate saves a complete original coloring with
`r=s=a`, the actual long collision contact(s), and the same-pin fibre size.
There are 197 such full witnesses. The statement that arbitrary source graphs
have these lifts is a paper lemma; these fixed controls calibrate its join.

All 32 named `T` subsets are listed with
`cl(T)={b: q_i(b)∈q_i(T) for every i∈I}`. The checker tests the equivalence
`q_i(W)⊆q_i(T)` for all three rows iff `W⊆cl(T)` for every one of the 32 named
`W` subsets, totaling 1,024 equivalences.

[boundary_observations.json](boundary_observations.json) separately applies the
necessary leaf-edge rule `e⊆cl(T), e⊄T` to all five original boundary edges for
all 32 `T`. Exactly six `T` have a candidate; exactly two have two distinct
candidate leaf edges:

| Named `T` | All candidate original leaf edges |
| --- | --- |
| `012` | `40` |
| `123` | `34` |
| `0123` | `34,40` (`h=4`) |
| `014` | `12` |
| `034` | `23` |
| `0134` | `12,23` (`h=2`) |

The source obligations that original leaf attachments satisfy this rule, that
there are at least two leaves, and that their attachment edges are distinct
are explicitly external to this finite boundary calculation.

## 4. Sidewise outside-slack controls

[side_observations.json](side_observations.json) retains both residual boundary
types, both root orientations, both original leaf edges, and every leaf owner.
For each of sixteen named leaf/owner cases it saves all target-row/color pairs
with `a∈q(leafedge)\q(T_owner)`: 32 explicit witnesses. Root/leaf labels, actual
root-contact edges, original spoke edges, and collision boundary vertices are
retained. The root-spoke matching is `01|34` at `h=2`, and `01|23` at `h=4`.

For each of the three fixed degree-five-root graphs, every boundary row, each
owner, and each of its four colors, a Cartesian-product enumerator stores the
**complete exterior `G−L` fibre**. This includes all illegal/empty cells.
Every legal owner pin has an exterior lift. Whenever that pin collides with
an actual long-contact boundary neighbor, **every** exterior tuple has a
same-pin long lift, and the complete joined set equals independent whole-graph
root-fixed DFS.

This retains 240 exterior cells (120 empty), 246 complete exterior tuples,
240 whole-graph DFS comparisons, and 43 triggered sidewise escape cells.
Different rows, owners, or root pins are never combined into one coloring.

## 5. Replay and qualification

[minor_observations.json](minor_observations.json) adds an independent replay
of the topology author's three fixed original-edge K5 constructions: direct
leaf-cycle attachment, leaf-cycle boundary-arc attachment, and a leaf bridge
whose boundary endpoints are both root spokes. The exact input is copied at
[frozen/topology/minor_controls.json](frozen/topology/minor_controls.json), SHA
`7cc4567aba9e24d65611bf2c53786f5ad4d89d6bd00525c643ba4ec577022435`.
The independent checker rebuilds connectivity for all fifteen disjoint bags,
checks the supplied original spanning trees, and verifies all thirty bag-pair
adjacencies against original edges. Removing the original `p–q` edge is
rejected before certificate comparison. These are branch-set construction
controls; complete degree/source conditions remain `not triggered`.

```bash
python3 -B audits/2026-10-13-n2-one-long/controls/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-n2-one-long/controls/checker.py --check
python3 -B audits/2026-10-13-n2-one-long/controls/boundary_checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-n2-one-long/controls/boundary_checker.py --check
python3 -B audits/2026-10-13-n2-one-long/controls/boundary_side_checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-n2-one-long/controls/boundary_side_checker.py --check
python3 -B audits/2026-10-13-n2-one-long/controls/minor_checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-n2-one-long/controls/minor_checker.py --check
```

All generation uses exclusive-create. All `--check` modes only read. Normal
and seed-17 stdout SHA agree; recorded replay payload mutations are zero.
Each checker rejected its separately retained corrupted certificate with exit
1. See [main verification](verification.json),
[supplemental verification](supplemental_verification.json), and literal logs.
The independent minor replay has its own [verification](minor_verification.json).

The positive classifications are `triggered and holds` for partition
transport, complete joins, collision controls, boundary arithmetic and the
stated fixed outside-slack controls. An absent escape antecedent is
`not triggered`. Complete original N2 sources are `not triggered` throughout;
no source count, topology classification, arbitrary-size theorem, or Lean
result is inferred from these finite controls.
