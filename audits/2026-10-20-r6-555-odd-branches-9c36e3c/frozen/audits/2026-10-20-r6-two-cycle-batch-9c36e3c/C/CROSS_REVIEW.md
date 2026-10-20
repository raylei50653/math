# C cross-review

BASE `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`.
The complete fixed-control computation was performed before reading
the new A/B proofs. The independent results were then compared with
[A](../A/PROOF.md) and [B](../B/PROOF.md).

**A: PASS within its stated conditional source contract.** The triangle
admissibility criterion and region-tree parity criterion agree with all
16,384 fixed cut subsets and 275 complete perfect matchings. The exact
bad-corner test and untouched-component parity test agree with all nine
eligible literal fixed-control pairs. The three new repairing pairs
demonstrate the intended algebra, but their partner degrees 3/3/4 do not
satisfy the source lower bound. Their source applicability is explicitly
untriggered; the simple-source two-face disk argument is not inferred
from controls having primal parallel edges.

**B: PASS after one exposition correction.** The local 5/5/5 control
has two odd T branches and two legal nonrepairing pairs, precisely as
the coupled criterion predicts. Charges `(1,1,0)` on an arbitrary
three-vertex tree do not alone imply two odd edges. C requested that
the proof also invoke the even order of D: exactly two complete circles
and failure of all-even imply exactly two odd circles. B incorporated
this explicit step. The finite control neither establishes that the
5/5/5 pattern occurs in a source nor excludes its odd/odd branch.

The full-scope obstruction is unchanged: the criteria do not prove
that either safe rim has an admissible pair with all untouched
components even. Larger cuts and multi-cycle batches remain possible.
