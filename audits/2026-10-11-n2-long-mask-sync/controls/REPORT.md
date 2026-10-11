# Complete original fibres and bounded long-mask synchrony controls

This audit reads the exact component-slack snapshot declared in the parent
`BASE.json` and writes only this new `controls/` directory. No source graph
generation, modification of shared evidence, independent frame normalization,
commit, push, or Graphify was performed. The fixed local motif controls below
are explicitly bounded calibration; arbitrary block-tree coverage belongs to
the separate paper analysis.

The frame is literal throughout:
`I={0,1,3}`, `q0=01212`, `q1=01202`, `q3=01021`, `D=3`.
The source table indices are respectively `6,4,1`; the checker selects beta
tuples rather than confusing source row indices with these named labels.
Every recorded full-fibre exemplar retains all ten literal boundary rows and
all sixteen ambient ordered root-pin cells, including empty cells.

## 1. Independent original-graph replay

`checker.py` verifies the source byte count and SHA256 against frozen `BASE`,
then independently enumerates numeric-order full vertex assignments. It reads
the frozen component tuple arrays for equality comparisons; it neither imports
the old checker nor treats old counts as sufficient evidence.

All 179 original components of all 63 fixed graphs were recomputed:

| Obligation | Result |
| --- | --- |
| All original local fibres | 1,790 rows, 28,640 cells, 3,372 empty cells; exact full tuple equality |
| Original exterior fibres after deleting each component | 1,790 full tuple comparisons; exact equality |
| Same-graph, same-row, same-ordered-pin component joins | 10,080 complete cells; equal independent direct graph DFS |
| Complete original global tuples | Independent direct DFS equals recombined full tuples and frozen SHA256 in every row |
| Frozen long mixed pieces | 37, all three named diagonal cells nonempty |
| Shared-contact long controls | 34 `triggered and holds` |
| Long support at least three and at most three root incidences | 0, `not triggered` |
| Two long mixed pieces in the same frozen graph | 0, `not triggered` |
| Complete target N2 sources | 0, `not triggered` |

The 37 long mixed pieces split into four shared-contact pieces with total
incidence three, thirty shared-contact pieces with total incidence four, and
three pieces without shared contacts with total incidence four. The last
three have literal support `{1,2,4}`. Most shared-contact examples have
nonconsecutive two-point support. These calibration graphs do not justify
the target one-sided long-support theorem, target shield packing, or new
target exclusions. All original geometry and ordered contacts are retained.

The snapshot supplies no rotation or actual shield certificate. Accordingly
the checker records actual attachments and support, and identifies an exact
two-edge support arc only when the actual support is precisely the three
vertices of that literal arc. It does not invent shield ownership for the
frozen examples. The component lifts preserve original region edges; the
same-graph join separately preserves root spokes, any root-root edge, boundary
edges, all other components, and every exterior coordinate.

## 2. Exhaustive literal tables for seven fixed motifs

For each named internal motif, the checker exhausts every degree-four
attachment choice using zero, one, or two adjacent boundary neighbors as
required by its literal internal degree and contacts. It retains exactly
those choices having an exact three-point consecutive support and injective
boundary-edge attachments at H-degree-two vertices. Contacts are distinct;
one fixed mixed ownership split is retained. Splitting owners does not change
the `(D,D)` lists, while all off-diagonal fibres of the selected exemplars
remain explicit.

| Fixed original local shape | Attachment candidates | Retained exact-arc controls | Observed masks |
| --- | ---: | ---: | --- |
| Two-contact bridge | 25 | 10 | `Eq(A)` |
| Three-contact three-vertex path | 125 | 30 | empty or `Diff(A)` |
| Three-contact triangle | 125 | 30 | empty |
| Contact leaf triangle with one bridge | 625 | 190 | empty |
| Contact leaf triangle with two-bridge tail | 3,125 | 270 | empty or `Eq(A)` |
| Two triangles sharing one cutpoint, with one leaf bridge | 3,125 | 270 | empty or `Diff(A)` |
| Three contact leaves at a bridge star | 625 | 0 | `not triggered` under exact two-edge support and attachment injectivity |

This is 800 retained controls. Each table entry stores its actual attachments,
every complete local diagonal lift in each named row, and its rejection mask.
Forty-five canonical motif/arc/mask exemplars additionally store all ten by
sixteen full local cells. Their original vertex coordinates, original region
edges and contact ownership are explicit. No criticality, full target Sigma,
or target disk realization is asserted for these fixed motifs.

For `A=(a,a+1,a+2)` define `Eq(A)` by equality of the two endpoint colors and
`Diff(A)=I\Eq(A)`. The literal table is:

| Arc start a | Exact original arc vertices | Eq(A) | Diff(A) |
| ---: | --- | --- | --- |
| 0 | 0,1,2 | `{3}` | `{0,1}` |
| 1 | 1,2,3 | `{0}` | `{1,3}` |
| 2 | 2,3,4 | `{0,1}` | `{3}` |
| 3 | 3,4,0 | `{1}` | `{0,3}` |
| 4 | 4,0,1 | `{3}` | `{0,1}` |

The tail-triangle enumeration includes every literal boundary-point
attachment, including repeated middle-point attachments. No stronger
same-row endpoint characterization is inferred from the masks.

## 3. Synchrony controls retain the failures

The checker compares 810 ordered pairs of the retained distinct
motif/arc/mask signatures whose two literal support-arc edge sets are
disjoint. Empty masks and full original exemplar references remain recorded.
Fifty-six pairs have mask union `I`; these are retained as
`counterexample` controls against inferring a common diagonal escape merely
from separate proper masks or disjoint two-edge supports.

For disjoint literal two-edge arcs, an `Eq(A)` mask and a `Diff(A')` mask
always leave a common row in this bounded table. An empty mask also causes
no obstruction. Two `Eq` masks or two `Diff` masks can cover all three rows.
For example, arc starts 0 and 2 give `Eq` masks `{3}` and `{0,1}`. Two path
controls on those same arcs give `Diff` masks `{0,1}` and `{3}`. These are
signature controls, not independently realizable target sources, and their
mask union cannot replace complete relations in an actual joint proof.

The named two-path negative control goes further: it retains two distinct
original vertex sets with the same literal roots and boundary, all local
full tuples, and their complete same-pin full graph joins. Its masks are
`{0,1}` and `{3}`. Both roots have three local incidences. It is a
`counterexample` to separate escapes implying a common diagonal row; it
does not have target degree-five roots or target Sigma.

## 4. Uncontracted common-spoke K5 calibration

Starting with the same two-path negative graph, add the four original spokes
from both roots to boundary edge `{0,4}`. Both root degrees become exactly
five; all local component tuples and the common frame stay fixed. The
checker retains all full graph fibres and verifies the five original bags

`[5,11,12,13]`, `[6]`, `[0]`, `[4]`, `[1,2,3,7,8,9]`.

They are pairwise vertex-disjoint, each is connected using literal original
edges, and every one of the ten bag pairs has an explicitly retained
original cross-edge witness. This control is `triggered and holds` for a
K5 minor certificate, hence demonstrates a planarity obstruction in the
named graph. It does not contract any graph during enumeration, prove the
arbitrary source premises forcing common spokes, or claim a target source
realization. The full target status remains `not triggered`.

## 5. Replays, corruption control and evidence boundaries

The exclusive-created `observations.json` has 23,818,946 bytes and SHA256
`da41436e3441d705dd41d0363be996d9834124cf71c3f5792f635119d4f23468`.
Normal and hash-seed-17 read-only replays both pass with identical bytes and
SHA. Exact tool outputs are retained in `verification.json`.

One generation attempt failed before artifact creation because the frozen
global tuple digest uses compact JSON plus a newline, while the initial
checker used its pretty-printed artifact encoding for that digest comparison.
The local tuples and exterior tuples already matched. The digest comparison
was corrected without modifying evidence; the failed attempt and correction
are retained in `generation_failures.json`.

The complete corrupted copy `observations.corrupt.json` changes only the
reported frozen graph count from 63 to 64. The checker recomputes the entire
artifact and rejects that copy with `artifact mismatch`, exit 1. Exact
negative output is retained in `negative_verification.json`.

```bash
python3 -B audits/2026-10-11-n2-long-mask-sync/controls/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n2-long-mask-sync/controls/checker.py --check
python3 -B audits/2026-10-11-n2-long-mask-sync/controls/checker.py --check --artifact audits/2026-10-11-n2-long-mask-sync/controls/observations.corrupt.json
```

The last command is expected to fail. Finite motif calibration, arbitrary
paper shape coverage, same-source target planarity, target exclusions and
Lean formalization remain separate obligations. No new Lean theorem is
asserted by these controls. In particular the zero original low-contact
long and zero two-long co-occurrence counts do not prove exclusions.
