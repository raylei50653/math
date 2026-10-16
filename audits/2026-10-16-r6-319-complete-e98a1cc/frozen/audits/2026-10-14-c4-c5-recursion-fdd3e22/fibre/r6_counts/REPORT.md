# The next seven-pin control also survives exact count conservation

This is a necessary finite count model for the original degree-six r
deletion of [the degree-four transfer control](../../degree4/check_transfer.py).
It is not an enumeration or realization of source graphs. All three
retained outer C5 masks, `271,314,319`, admit an **exact integer** solution
to the common-count constraints below.

| Outer C5 mask | Permitted canonical joint rows | Positive canonical rows in witness | Total labelled abstract mass |
| --- | ---: | ---: | ---: |
| 271 | 18 | 12 | 288 |
| 314 | 18 | 12 | 288 |
| 319 | 26 | 18 | 432 |

Every positive canonical row has count one in these witnesses. Each of its
24 global S4 renamings has the same count. Counts are zero on the other
permitted rows. Each required outer C5 fibre is positive. These counts
are abstract witnesses for the stated linear constraints, not the counts
of a constructed graph.

## Why the count equations are necessary

Fix one actual full colouring f of a finite graph H and one complementary
pairing of the four colours, for example `AB | CD`. All maximal AB and CD
components together partition V(H). Switching any subset of these
components gives an action on complete H colourings. The components keep
their vertex sets under all these switches, so the action partitions all
complete colourings into finite simultaneous-switch orbits.

If there are b components meeting the seven named pins and h components
meeting no pin, each orbit has `2^(b+h)` complete colourings. Its projection
to **labelled** pin rows has `2^b` distinct rows, each occurring exactly
`2^h` times. Distinct choices of visible component switches give distinct
labelled rows because each visible component contains at least one pin.

Consequently, for a fixed pairing, the complete fibre count n(r) of each
labelled pin row r is a nonnegative integer sum of uniform masses on
projected simultaneous-switch orbits. Different full orbits with the same
projection may be pooled into a single integer mass. Terminal partitions
must respect mandatory edges and the honest outer C5 noncrossing condition,
and every projected successor must pass the previously proved all-r-lifts
screen.

The model imposes this decomposition for **all three** complementary
pairings, using one common n(r), with `n(sigma r)=n(r)` for every global
colour renaming sigma. It requires a positive total in every prescribed
outer C5 fibre. Thus the separate pairings cannot be supplied with
inconsistent row multiplicities.

Only the **labelled** switch orbit is assigned uniform mass. Assigning a
uniform mass directly to canonical S4 row orbits would not be justified:
different labelled switch rows can normalize to the same canonical row.
The checker first preserves every labelled row, then imposes the common
S4 equalities separately.

## Exact evidence and limits

[counts.json](counts.json) records all nonzero masses, a valid terminal
partition witnessing every used projected orbit, every labelled successor
in that orbit, and the common count of every canonical joint row. The
model has 106 available projected orbits per pairing for each of masks271
and314, and 204 per pairing for mask319. All marginal equalities are
verified with Python integers.

The solver was used only to find a proposal. Its floating-point output
was rationalized, scaled to integers, and checked exactly before saving.
The ordinary replay needs no solver, NumPy, SciPy, or network:

```sh
python3 -B audits/2026-10-14-c4-c5-recursion-fdd3e22/fibre/r6_counts/check_counts.py --check
```

The optional generation command was:

```sh
uv run --with scipy python -B audits/2026-10-14-c4-c5-recursion-fdd3e22/fibre/r6_counts/check_counts.py --solve
```

The certificate is written exclusively; generation will not overwrite an
existing file. Normal and `PYTHONHASHSEED=17` exact replays pass. Internal
negative controls reject a changed row count and an all-zero witness; a
deliberately changed certificate is retained with its rejection log.

[input_transfer.py](input_transfer.py) is a frozen copy of the contemporaneous
degree-four transfer helper. Only its pure partition/all-lift functions are
imported; its own command-line main is not used. The certificate binds
both that source and the count checker by SHA256. This avoids changing
the model if the independent degree-four investigation subsequently adds
geometric constraints.

Feasibility proves only that these specified support and count equations
do not contradict one another. It does not supply one plane graph, one
system of actual maximal Kempe components across different pairings, or
complete fibres of a source. In particular it does not prove the residual
realizable, rule out a stronger geometric return injection, or close the
degree-six branch. The next information must go beyond these equations,
for example by constraining how the same colouring's components for
different colour pairings change after a switch.
