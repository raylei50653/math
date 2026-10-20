# C. Independent exact replay of the four-vertex switch

Frozen BASE: `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`.
Write scope: this audit's `C/` only. No prior checker was imported.

The four-vertex set `X={h,A,B,t}` passes all three acceptance conditions
in the fixed local 5/5/5 odd-branches control: the actual original rotation,
the three literal marked edges, and every complete component of `N*`.
Its dual cut is one alternating decagon. This finite result agrees with
the arbitrary-size conditional paper proof supplied separately by A and B.
It does not establish that an original source realizes this control or
that every source belongs to the 5/5/5 configuration.

## Independent reconstruction

[check.py](check.py) hash-verifies the frozen previous `C/check.py`,
`C/certificate.json.gz`, and `B/PROOF.md` against this audit's `INPUTS.json`.
It reads the frozen data and independently reconstructs:

- Every directed face walk from the original cubic rotation, retaining the
  literal frozen primal-face numbering and checking the sphere Euler identity.
- Every primal edge, triangular face, original primal degree and rotation.
- All perfect matchings by an independent backtracking enumeration.
- All complete complement cycles and all alternating difference cycles.
- All complete primal components, their original-degree sums, and the complete
  region tree; every cycle parity is checked against its entire tree shore.
- All primal cuts modulo complementation, checking the actual two-sided
  triangle law at every original facial triangle.
- Every pair of actual primal vertices, plus explicit named proposed sets.

The seven frozen controls are classified from their actual degrees and
original matching components. Exactly one has the local 5/5/5 configuration
with two odd branches: `literal_both_outside_blocked`.

The resulting [certificate](certificate.json.gz) contains all 56 matchings,
all 4,096 anchored cuts, all 78 vertex pairs, and all eight literal mark
fibres and eight even-complement mark fibres. No fibre key is omitted.
Every mark fibre happens to be nonempty on this particular control.
All 56 matchings appear exactly once among the valid anchored cuts.

## One simultaneous witness

The actual labels are

`(u,h,A,B,t,a,b)=(1,2,5,6,8,7,9)`.

The fixed `T-t` branches are `{7,12}` and `{9}`. Their original-degree
sums are 13 and 3, respectively, so both have odd parity. The two central
pair switches `{A,t}` and `{B,t}` are legal and preserve the literal marks,
but each retains two odd complete complement cycles.

The diamond `X={2,5,6,8}` is matching row 55. All four selected vertices
have original degree five. Its original-rotation dual cut is the decagon

`[0,3,4,9,10,15,14,12,13,6]`.

The removed matching edges are

`03, 49, 6-13, 10-15, 12-14`;

the added edges are

`06, 34, 9-10, 12-13, 14-15`.

The three original dual marks `18-20`, `1-2`, `16-21` are all unchanged,
with retained mark type `101`. Every original triangular constraint passes.
The full new primal components are exactly:

| Component formula | Actual vertices | Original-degree sum |
| --- | --- | --- |
| `{u}` | `{1}` | 4 |
| `(T-t) union {A,B}` | `{5,6,7,9,12}` | 26 |
| `(U0-{A,B}) union {h,t}` | `{0,2,3,4,8,10,11}` | 36 |

These components cover every primal vertex. Each sum is even. The entire
new complement has precisely two cycles:

`[0,1,2,3]`,

`[4,5,6,13,14,12,11,10,15,16,17,18,19,20,21,7,8,9]`.

Their lengths are 4 and 18, agreeing with `4` and `|O|+3` for the original
outer cycle length 15. The certificate retains both full cycles and every
full component in the same row; it does not combine separate witnesses.

There are six joint even rows on this control. The sole minimum-size pair
repair is `{B,b}={6,9}`, row 40, but its vertex `b` has original degree
three. Consequently this pair supplies no R6 source repair. The diamond
uses four vertices whose original degrees are all five.

## Replay and negative controls

Both ordinary replay and `PYTHONHASHSEED=17` pass with byte-identical
standard output. SHA256 checks before and after show that replay leaves
the checker and certificate bytes unchanged. See
[VERIFICATION.json](VERIFICATION.json).

Eleven negative controls are rejected:

- Omitted complete primal component.
- Altered component charge.
- Omitted complete outer complement cycle.
- Changed literal mark.
- Changed original rotation.
- Missing mark fibre.
- Omitted anchored cut.
- Invented repairing pair.
- Changed diamond cut set.
- Invented source authority.
- Attempted overwrite through the exclusive-create option.

Replay command:

```sh
python3 -B audits/2026-10-20-r6-555-odd-branches-9c36e3c/C/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-20-r6-555-odd-branches-9c36e3c/C/check.py
```

## Authority boundary

This fixed plane control has degree-three primal vertices 9, 11 and 12,
and parallel primal edge pairs. It is not an original R6 source. Original
source realization is **not triggered**; no source contradiction is inferred
from these local computations. The arbitrary-size conditional theorem has
its paper proof in the separate A/B outputs. The coverage statement that
all original sources fall into this degree pattern remains **OPEN**.
This artifact supplies no Lean theorem, no new source-fibre enumeration,
and no smaller-source reconstruction claim.
