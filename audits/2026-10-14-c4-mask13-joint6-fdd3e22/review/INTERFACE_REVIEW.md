# Independent review of complete fibres and paper transport

Reviewed `JOINT_FIBRES.md`, `controls/check_fibres.py`, the resulting
`controls/fibres.json`, and the mathematical matching in `SOURCE_GEOMETRY.md`.
The reviewer authored `controls/check_interface.py`, so the observations below
about that control are a soundness audit, not an independent code review of it.

## Result and exact scope

No blocking mathematical error was found in the reviewed claims. The
complete-colouring maps in JOINT_FIBRES use actual maximal Kempe components,
retain the literal six pins, and give inverse maps on full colourings. The
ABAB map fixes p and q individually. The ABCD map can reverse their order;
the document explicitly states the condition for this reversal and does not
infer both orientations from nonemptiness of that sector.

The exclusion of pq={B,C} in ABCB correctly requires both universal failure
conditions. The C-coloured pq endpoint belongs to the AC component of z by
the literal z-p or z-q edge; this is the reason the r-switch retains its
colour. The t-switch retains the C endpoint because it only uses B,D. The
two resulting forced paths have alternating endpoints on the original C4
and disjoint colour sets. The proof never places p,q on an invented Jordan
boundary or combines separate colourings.

The two unconditional mask13 maps to the AC-connected and AC-disconnected
ABCB sectors are checked on seven explicit disk graphs. Their 42 complete
fixed-Q colourings were independently enumerated by the Cartesian product
of all assignments to all remaining vertices, without importing producer
code or using its branching heuristic. The independent checker also
recomputes the component maps and both inverses as set equalities: all 14
complete-set bijections pass. It checks connectedness, the induced original
C4, and the named triangle in each marked example.

Replay:

```sh
python3 -B audits/2026-10-14-c4-mask13-joint6-fdd3e22/controls/check_fibres.py --check
python3 -B audits/2026-10-14-c4-mask13-joint6-fdd3e22/review/check_fibres_independent.py
```

These examples have low degrees and fail the joint obstruction hypotheses.
They test the underlying full-fibre involutions and provide negative controls
for dropping hypotheses; they are not examples satisfying the new conditional
palette theorem. Actual target source controls remain zero. The base embedded
disk and successive facial stellar insertions give the stated plane disks;
the producer additionally checks oriented darts, Euler characteristic and
vertex links. An optional independent NetworkX check was unavailable in the
current interpreter; its failed import is retained in
`initial_environment_failure.log`. No independent NetworkX planarity check
is reported as passing.

## Necessary abstract control

The seven-orbit control is sound as a relaxation. For any actual colouring,
its terminal intersections with maximal Kempe components respect all seven
mandatory edges and the original C4 noncrossing condition. Each subset switch
of complementary-pair components is another full colouring of the same graph.
Therefore every genuine supported row survives every fixed-point iteration,
by induction. Global canonicalization is legitimate because it applies one
S4 permutation to the entire six-pin tuple and the entire underlying colouring.

The surviving abstract choices can depend on both the row and the colour
split; the control does not establish a common graph realizing all choices.
It also does not preserve full-fibre multiplicities. INTERFACE_CONTROL states
these quantifiers and limits accurately. Its seven surviving orbits establish
only that the listed necessary conditions cannot by themselves empty the
joint relation. The rejected repeated-z model is clearly excluded.

## Source geometry and local r table

The five-apex contact exclusions, optional-edge criteria, degree accounting,
and the relative point counts in SOURCE_GEOMETRY were checked against the
stated original-source geometry. In particular, deleting an original
degree-five r changes only s,v,t after the existing x,y deletion, and those
three vertices lie on the new boundary. The literal local r table was
independently recomputed using raw colour values, without the producer's
normalization code: its allowed pq pairs are CD/DC, BC/CB, CD/DC, and empty
in the four fixed-Q' rows.

The use of the external 4-candidate bound was reviewed against the already
adopted `2026-10-14-c5-c4-boundary-pivot-77fbd5d/EXTERNAL.md`, not a fresh
download or rerun of the external enumeration. With original p,q degrees at
least six, all R internal degrees are at least five and |R|=k+1, giving the
stated conditional k>=28. Under the additional original r-degree-five
hypothesis, R' has k vertices and no rainbow row, giving conditional k>=29.
The cited h=3 and 932/h=4 apex results force r>=6, so the document correctly
keeps the latter 29 bound separate from those two subdomains. The read
upstream reports support the stated two h=3 vectors and the 932/h=4 apex
degree transfer. This review did not reverify their full historical certificates
or the external generation software.

## Resolved minor control concern

At initial review, the producer's missing-full-lift negative control merely
deleted one element and asserted the set changed. That demonstrates the
mutation but does not itself exercise the set-equality validator. The root
agent strengthened it by checking a freshly recomputed switch image against
the deliberately damaged target set with the same `need` equality validator.
The expected `ValueError('ABAB full-set bijection')` is now required and
recorded in the certificate. The reviewer inspected that change and reran
both the producer replay and the independent full-set checker successfully.
The initial certificate remains retained as historical evidence. This issue
is resolved; it did not affect the positive comparisons or the paper proof.

The general six-pin exclusion, source realization, arbitrary-size diagonal
extension, and new Lean formalization remain outside these PASS statements.
