# C independent review of integration proof

Reviewed BASE: `6c420f3ca77d60952ed76f93dff7449c522715ca`.
Reviewed root `PROOF.md` SHA256:
`463cb574f3d8bf4b7abd1de668ae1f67d31f07b42838406c621cc04de73aef10`.

**Assessment: PASS; no blocking issue found.** This review read the root proof
and checked its finite-control and exchange boundaries against C's independent
reconstruction. It also checked the cited frozen proper-C5 theorem §§2–3,
original two-star geometry, and the stated low-p/q conclusion. It does not
substitute finite computation for A/B's arbitrary-source topology audits.

## Theorem versus finite control

The root theorem retains the original completed G and fixed support, the
same U,J,D, literal marked edges, original sectors, and the complete-fibre
contract. It does not retain the old extra original-v5 or c>=5 premises.
The two-step argument uses a different true original C5 touching the
outer frame, a case included in the frozen proper-C5 theorem. In its
nonempty case the no-extra-boundary-chord conclusion is essential and is
explicitly used; using only a bound of one interior vertex would not prove
the displayed degree bound.

The simple six-cycle pairing classification is exhaustive: the four original
cross nonedges force both remaining connection paths to have length two.
Pairing I uses both original fan sectors in the same G. Pairing II uses the
actual complementary disk, whose terminal order makes the two avoiding-m
paths cross. Each remaining m path is treated by its own original p or q
cap. The root does not reflect support933 into an unadopted support.
The small cyclic-cut argument handles disconnected sides before invoking
bond/cycle duality; a cyclic component needs at least four boundary edges
and any extra component at least three, contradicting size at most six.

C's five marked primal six-cycles, including the two cyclic cuts, violate the
new source restriction. C still has exactly 38 PMs, three joint101 PMs, and
joint oddness minimum two. These are consistent facts because C is only a
weak-premise control with no literal source layout. Its computed rejection
does not prove that every positive joint minimum forces a forbidden cut.
The root proof keeps the latter implication OPEN. It makes no claim that
the new restriction alone implies joint positivity or source realizability.

## Exchange contract in §6

For M in F_e, let t_e,t_f,t_g indicate membership in the union of actual
vertex-disjoint M-alternating cycles. Symmetric difference produces a PM
on the same D. Its marked bits are `(1 XOR t_e, f XOR t_f, g XOR t_g)`.
Since initially f XOR g=1, final membership in F_e is equivalent to
`t_e=0` and `t_f=t_g`. Thus the displayed iff condition is correct and allows
110<->101. From a111 PM the corresponding condition is instead `t_e=0`
and `t_f XOR t_g=1`. The proof states this difference explicitly.

The root also correctly requires recalculation of the entire complement:
marked-family preservation alone gives no strict oddness decrease.
Its marked cyclic-cut lower bound does not impose a length bound on odd
cycles of D-M, because e belongs to M for every target matching. The listed
remaining seven-defect repair and failed-repair-to-cut implication are open
rather than silently supplied by the C census.

## Evidence checked

`C/check.py --check`, the seed17 replay, all seven corruption controls, and
the exclusive-create preservation check passed. The full record is
`C/VERIFICATION.json`; the proof and certificate retain actual IDs for every
matching, complement cycle, primal six-cycle, and both cut sides. No
commit, push, or new Lean authority is inferred.
