# Generic used-equal-pin fixed calibration

The generic local bound passes on **89 of 228 saved pieces**, with **445
triggered proper three-colour rows**. The checker records the complete
forbidden equal-pin set F and its intersection with the used global boundary
colours on every one of the 2,280 saved rows. Among the triggered rows the
intersection is empty 341 times and a singleton 104 times; there are no
violations of `|F(q) intersect q(B)| <= 1`.

This is fixed calibration of the generic paper theorem. It does not establish
a source exclusion by observing zero complete target sources. N2-55 and
E-ARC2 remain OPEN; complete target source status is `not triggered`.

## Exact trigger predicate

`paper_controls.py` reads the twelve BASE-hashed snapshots and the same 228
saved pieces as `checker.py`. It does not modify that earlier checker or its
outputs. It computes the following local hypotheses from literal edges and
actual attachments, rather than trusting a saved `cactus` or `leaf` label:

1. C is connected and every vertex has total original degree four.
2. The total original root incidence count is at most three, with no shared
   contact vertex between distinct roots.
3. Actual boundary support has at least three points, and each vertex's actual
   boundary attachments are at most two points; a pair must be a literal C5 edge.
4. Tarjan blocks are bridges or odd cycles. Each leaf block has a private
   contact vertex, and each odd-cycle block has at most one ordinary private
   vertex. Here private means non-cutpoint of the original C, and ordinary
   means not incident with any actual root.

All these local conditions plus a proper row using exactly three global
boundary colours trigger the bound. Root labels and ownership remain literal.
The equal-pin query fixes every actual root to the same colour, so a no-shared
mixed piece has the same lists as the corresponding single-owner query; this
is a local equality-pin calculation, not a source-ownership replacement.

| Denominator or check | Count |
| --- | ---: |
| All saved local pieces | 228 |
| Local hypotheses `triggered and holds` | 89 |
| Local hypotheses `not triggered` | 139 |
| Triggered pieces with k=2 / k=3 | 47 / 42 |
| Triggered actual unary / mixed equal-pin pieces | 42 / 47 |
| All saved rows, including four-colour rows | 2,280 |
| Saved proper three-colour / four-colour rows | 1,140 / 1,140 |
| Generic bound `triggered and holds` rows | 445 |
| Generic bound `not triggered` rows | 1,835 |
| Triggered rows with zero / one forbidden used colours | 341 / 104 |
| Independently recalculated complete equal-pin cells | 9,120 |
| Complete equal-pin ordered tuples checked | 28,225 |
| Original component-slack row custody checks | 1,790 |

The 89 triggered pieces are 42 original components, all 45 saved motif
exemplars, and two saved named joint pieces. The two high-contact controls
are outside the k bound. The forty-two actual unary triggers all have k=2;
this observation is not a proof excluding any unrepresented unary k=3 source.
Failure counts for every individual hypothesis are retained; failures overlap.

The artifact preserves Tarjan blocks, literal internal edges, cutpoints,
private contacts, ordinary private vertices, actual attachment maps, and all
original coordinates. For each of the ten original rows it stores the exact
F set, F intersect q(B), all four complete equal-pin fibre sizes and hashes,
and the trigger status. Complete tuples remain in the frozen full-fibre source
at its SHA256 and JSON pointer. Empty fibres are included when forming F.

## Stronger empty-row claim: retained counterexamples

The already completed `../review/equal_pin_full_probe.json` re-queries exactly
800 frozen attachment controls. It finds ten controls where F is nonempty
on all three target rows. The generic artifact references that probe by SHA256
and independently recalculates their 120 complete equal-pin cells, preserving
their literal source pointers and attachments. All ten satisfy the local
hypotheses and all obey the weaker used-colour bound.

For the named tail-triangle entry34, the actual C is triangle `7,8,9` with
bridges `7-10,10-11`, contacts `8,9,11`, and attachments
`7->{0}, 8->{2}, 9->{2}, 10->{0,1}, 11->{1,2}`. Its target-row forbidden sets are
`q0:{0}`, `q1:{0}`, and `q3:{2,3}`. Their used-colour intersections are respectively
`{0}`, `{0}`, and empty. Thus F need not be empty on any target row, and a
forbidden colour need not be unused. The generic `at most one used colour`
statement survives exactly. These are local controls and not complete target
sources; no rotation, criticality, or source capacity is supplied by them.

## Replay and artifact corruption

```sh
python audits/2026-10-12-n2-boundary-partition-law/controls/paper_controls.py --check
PYTHONHASHSEED=17 python audits/2026-10-12-n2-boundary-partition-law/controls/paper_controls.py --check
```

Both replays pass. The separate artifact negative control substitutes two
incorrect forbidden used colours while keeping the underlying complete tuple
hashes unchanged; the verifier rejects the inconsistency. An independently
invoked `--artifact PATH` CLI check also returns nonzero for that corruption.

The receipt records the new checker and artifact hashes and the unchanged
earlier checker hash. No original checker output, BASE input, or shared
document is changed by this supplementary calibration.
