# B final mathematical review of the root integration

BASE `e98a1cc1afd9a428600dcf4027d8138078c01650`.
Reviewed the complete `../REPORT.md`, especially sections 4 and 7,
and the updated current-status and section-3 passages of
`../../../docs/c5_kempe_guide.md`.

**Result: PASS. No mathematical correction is required.**

## 1. Scope, sufficient contradictions, and OPEN boundary

The report identifies `W110+W101>0` as a sufficient same-source
contradiction for this route. It does not require both weights positive,
does not claim this is necessary for every possible source-exclusion
proof, and explicitly distinguishes ordinary P101 nonemptiness from
even-complement positivity. The known even 111 endpoint is outside the
joint family. The source-exclusion and omega-zero obligations remain
OPEN in the opening paragraph, proof-chain table, section 7, and guide.

The source quotient result is stated with its correct quantifiers:
every defined quotient has a complete colouring, at least one quotient
is defined, and the witnesses of different quotients are not joined.
Every base colouring can have an empty z-lift fibre. The singleton
restriction on a nonempty fibre is necessary under the source FJ
obligation; it is not asserted to produce a violating lift.

## 2. Transition identity and the exact two-transition criterion

Section 4 correctly fixes the complete labelled Tait colouring before
using its alpha matching M0. The f-containing component of a symmetric
difference with an ordinary 101 endpoint is a genuine alternating cycle
avoiding e,g, and flipping it alone still gives ordinary 101.

The transition definition agrees with B2: an original alpha edge newly
put in the complement is a transition when its two incident removed
non-alpha edges have different original beta/gamma colours. The entire
new component has length parity equal to its own transition count.
This is an equality for the complete surgery; the integration never
adds independent local changes that share an old complementary cycle.

The conclusions `t` even and `odd(D-N)<=t` are correct. For exactly two
transitions, placing both on the same entire component is necessary and
sufficient for the complement to be all-even; placing them on different
components gives exactly two odd components. Thus merely proving
`t<=2` would not establish positivity. Both the report and guide retain
this distinction and state that even this transition bound is unproved.

The pentagon statement is correct because a matching contributes at
most two old alpha edges to a five-cycle, whereas its transition count
must be odd. The f-containing short-defect conclusion keeps the source
minimum-degree premise: a length-five odd component is the actual D
face of p or q, whose J degree is five and whose original G degree is
six. Its centre must have the 101 bit opposite to z. Otherwise that
marked odd component has length at least seven. Neither alternative is
claimed excluded.

## 3. The corrected t=2 and t=4 calibration

I checked the root's corrected counts against B's complete certificate:

* `M111a={1,3,6,10,13,16,19,21}` has complement lengths eight and eight.
  Its four fixed-root, fixed-alpha complete beta/gamma choices have
  exactly two transitions, split one each between the new nine- and
  seven-cycle after its single ten-edge difference-cycle flip.
* `M111b={1,6,10,11,13,15,19,21}` has one sixteen-cycle in its complement.
  Its two corresponding choices have four transitions on the single
  twelve-edge difference cycle; three lie on the new nine-cycle and one
  on the new seven-cycle.

Section 5 correctly distinguishes these four and two choices rather
than attributing six two-transition choices to one starting matching.
The control's weights are correspondingly `W111=4+2=6` and
`W110=W101=0`. Its unique ordinary joint matching has oddness two.
It disproves the stated general planar implication but violates actual
source hypotheses. The integration does not promote it to a source.

## 4. Reconstruction cost and the sufficient next obligation

Section 7 correctly asks for a batch entering a joint direction with
even transition count on **every whole new complementary component**.
By the identity this supplies an all-even complement and hence positive
weight. It neither guarantees such a batch nor treats a computable
upper bound or an allowed local constraint as an existence theorem.

All same-graph operations leave source size unchanged. The smaller
quotient used for relative minimality does not reconstruct a smaller
bad completed source. The retained `k+5` completed-source return cost
and the explicit absence of strict bad-source descent are correct.
No new K bound, r>=7 result, full 319 exclusion, or Lean authority is
asserted. Guide propagation matches the root report.

## 5. Final replay

During this integration review I independently replayed:

* A's current default `sealed-certificate.json` with
  `python -B A/check.py --check`: PASS, retaining 2688 complete quotient
  colourings, 1296 empty z fibres, and all 16384 seven-pin assignments.
* B's complete certificate with `--seed 17`: PASS, including the explicit
  four-choice t=2 and two-choice t=4 assertions and all whole-component
  transition identities.

This review writes only `B/REVIEW-INTEGRATION.md`. It makes no mutation
to the root report, shared guide, frozen authority, or other audits.
