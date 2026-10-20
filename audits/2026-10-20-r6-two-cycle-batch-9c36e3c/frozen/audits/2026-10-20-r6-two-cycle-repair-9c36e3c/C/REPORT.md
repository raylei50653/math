# C. Complete fixed controls for two-cycle matching repair

BASE `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`, 2026-10-20.
This independent finite audit uses four explicit plane cubic graphs. None is an
R6 source, and none is used to infer source realizability or exclusion.
The active certificate is [certificate-v2.json](certificate-v2.json), reconstructed
by the read-only stdlib [checker](check.py). The first three-control development
seal and its logs are retained unchanged as `certificate.json` and
`VERIFICATION.json`; current evidence is [VERIFICATION-v2.json](VERIFICATION-v2.json).

## 1. Full interface and audit authority

Every graph has the literal old complement
`C=(0,1,2,3,4,5,6)` and `O=(7,...,6+n)`, with odd n. The initial perfect
matching M consists of chord03, the five spokes at cap ports `(1,2,4,5,6)`,
and the listed O chords. There are no omitted vertices or old complement
components. The cap chord is on the C-disk side; the five spokes and all
O chords marked `cap` lie on the same side of O. Chords marked `outside`
are on its other side. Every graph has `e,g in M`, `f=12 not in M`, e outside,
g on the cap side, and both marked edges at distance at least two from C.

The certificate retains a full oriented sphere rotation and all faces; the
checker verifies both dart occurrences, simple face boundaries, connectedness,
and Euler characteristic 2. It enumerates **every** perfect matching by
branching on the least unmatched vertex and retaining every possible matched
neighbor. For each PM it records the actual edge set, every complete complement
cycle, the 3-bit mark pattern, and every actual alternating cycle in `M xor N`.
All eight PM fibres and all eight even-complement fibres, including empty fibres,
are retained. Every batch of vertex-disjoint M-alternating cycles corresponds to
one enumerated PM, and every enumerated PM supplies such a batch. Thus a zero
joint fibre in a control excludes *all* admissible batches in that fixed graph.

The checker also reconstructs every labelled Tait colouring with e colour 0:
choose its complete even-complement colour-0 matching, then independently choose
the two alternating 1/2 orientations on every whole complementary cycle. It
retains full edge-colour rows. Its all-distinct counts are genuine same-row
witness counts, not separate edge marginals.

The words `p,q,z,m,v,w` below are roles in the dual of the fixed plane control.
A successful literal-incidence check requires six different primal vertices,
`f=pq`, `g=mz`, `e=vw`, an actual primal triangle `p q z` at an endpoint of f,
and an actual triangle `m v w` at an endpoint of e. The primal p face is the
four-face `(0,3,2,1)`; m has no incidence with C. This check does not reconstruct
the original G, its ordered contacts, complete U319 fibres, or any source lift.

## 2. Weak geometry does not force any repair

Take n=11, outer spoke endpoints `(7,8,9,12,17)`, and

- O chords `10-15` outside, `11-14` outside, `13-16` cap side;
- `e=10-15`, `f=12`, `g=13-16`.

There are 36 PMs and 24 even-complement PMs. The complete even fibres are
`|P101|=0`, `|P110|=0`, `|P111|=2`; six complete e-zero Tait rows have the marks
all distinct. Consequently even the existence of actual 111 and all-distinct
references, two old odd cycles, five spokes, opposite e/g sides, and mark
separation does not force an admissible repair in an arbitrary plane control.

The decisive source-contract failure is precise: g is in the annular sector
between cap ports5 and6. For f12, an actual z completing p q z must instead be
in sector6-to1 or sector2-to4. Rebuilding primal faces finds no legal assignment
of all six literal roles. Hence this is **not** a counterexample to the R6
claim or to a repair theorem that retains the literal z sector.

The 56 monotone interval actually gives an even-complement switch: its O path
is `12,13,16,17` and the skipped O arc `13,14,15,16` has odd length3. But the
switch uses g and avoids f, so it is forbidden. This exposes exactly where
replacing the literal sector by a generic cap-side chord loses safety.

## 3. A safe cap-removing switch can retain two odd cycles

Take n=13, outer endpoints `(7,8,9,11,12)`, and

- O chords `10-13` outside, `14-19` cap side, `15-17` cap side, `16-18` outside;
- `e=16-18`, `f=12`, `g=14-19`.

There are 47 PMs, 35 even PMs, and complete even fibres of sizes
`P101=5`, `P110=1`, `P111=4`. Ten e-zero Tait rows have all three marks distinct.
The exact primal labels, as indices into the complete face list, are
`p=1, q=3, z=0, m=9, v=7, w=11`. Thus both required primal triangles and all
three literal marked edges hold in this fixed embedding.

The actual 111 reference

`M0={03,12,4-9,56,7-8,10-11,12-13,14-19,15-17,16-18}`

has a single even20-cycle complement. Its difference from M contains the
alternating cycle

`Q=(5,6,12,13,10,11)`.

Q avoids all three marked edges. Its switch removes the old seven-cycle but
produces the two **complete** complement cycles

`(0,1,2,3,4,5,11,12,6)` and
`(7,8,9,10,13,14,15,16,17,18,19)`.

Their lengths are9 and11. Full oddness remains2. Thus safe marks and cap
removal do not imply strict descent even when the old complement had only two
complete cycles and the local literal incidences are retained.

This graph is still not an R6 source. Its sphere faces `(15,17,16)` and
`(16,17,18)` give primal vertices of degree3, forbidden in the source geometry.
Its literal m face has length5 as well, below the source bound `d_J(m)>=7` proved in B. It refutes only the indicated weaker inference.

The same graph supplies a positive direct-interval control: interval56 has
outside path `(11,12)`. The actual safe alternating4-cycle `(5,6,12,11)` gives
one complete even20-cycle. Interval45 reaches outside chord10-13 and is
correctly reported as blocked by the monotone cap-side procedure.

## 4. Jump-arc parity is a necessary condition

For a genuine even-jump control take n=11, endpoints `(7,8,9,13,14)`, chords
`10-12` cap side, `11-16` outside, `15-17` cap side, and marks
`e=11-16`, `f=12`, `g=15-17`. The full literal roles again exist. The 45
monotone walk follows `(9,10,12,13)` and jumps across O arc `(10,11,12)`,
whose length is2. The actual safe cycle

`Q_even=(4,5,13,12,10,9)`

produces a complete triangle `(10,11,12)` and a complete15-cycle. Thus the
parity obstruction is a real complete odd component, not a marginal port
parity. There are22 PMs and13 even PMs; 111 references exist, but no complete
all-distinct Tait row exists. Its facial triangles are an additional explicit
source-contract failure. The 56 direct interval still provides a separate safe
even18-cycle repair, so this is not a control against every possible repair.

For a nonvacuous positive odd-jump control take n=13, endpoints
`(7,8,9,14,15)`, chords `10-13` cap side, `11-18` outside, `12-17` outside,
`16-19` cap side, and `e=11-18`, `f=12`, `g=16-19`. Literal roles and both
reference kinds exist. The 45 path `(9,10,13,14)` jumps across the odd-length
arc `(10,11,12,13)`. The actual safe cycle

`Q_odd=(4,5,14,13,10,9)`

produces complete complement cycles of lengths16 and4, namely
`(0,1,2,3,4,9,8,7,19,18,17,16,15,14,5,6)` and `(10,11,12,13)`.
There are55 PMs and34 even PMs; the complete joint even fibres have sizes5
and1, and six e-zero Tait rows have all marks distinct. This control validates
the nonempty-jump positive branch on one full fixed graph. It does not supply
the original source, arbitrary-size coverage, or the missing universal
existence of a suitable monotone interval. In this control m has degree4,
violating the source bound `d_J(m)>=7`; the skipped4-cycle surrounds a degree4
child, violating B's ordinary-child degree lower bound. Thus even this
nonempty-jump positive is a fixed-graph trigger only.

## 5. Results and evidence boundary

| Fixed control | All PMs | Even PMs | Even101 | Even110 | Even111 | e-zero Tait | All-distinct rows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Weak geometry, no joint repair |36|24|0|0|2|24|6|
| Literal safe cap disappearance |47|35|5|1|4|48|10|
| Literal even skip |22|13|3|0|2|12|0|
| Literal odd skip |55|34|5|1|1|38|6|

Normal and `PYTHONHASHSEED=17` replay pass. Four separate contaminations are
rejected: deleting an empty complete fibre, dropping one complete post-switch
cycle, changing the literal z sector, and changing a jump-arc parity. A second
exclusive-create attempt fails and leaves the active certificate bytes
unchanged. These results are in `VERIFICATION-v2.json` and the corresponding
`*-v2` logs. No worktree-level or remote checks are claimed by this child audit.

The general source repair remains OPEN. The controls justify retaining the
literal z sector, the exact marks of the actual switch, and every complete
post-switch cycle; they do not supply any of the omitted source assumptions.
