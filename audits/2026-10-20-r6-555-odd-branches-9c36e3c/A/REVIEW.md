# A cross-review of B's conditional repair

Reviewed after independently writing [A/PROOF.md](PROOF.md).
The reviewed file is [B/PROOF.md](../B/PROOF.md).

Verdict: PASS for the arbitrary-size conditional 5/5/5 theorem.

1. The four vertices `h,A,B,t` are fixed original-source vertices.
   In particular h is the already established degree-five centre,
   not an additional freely chosen partner. The complete rotations
   in B agree with the frozen literal cap and 5/5/5 stars.
2. B checks all twelve actual triangles meeting the selected set.
   Its ten boundary faces occur in the same cyclic order as the
   independently derived alternating decagon in A. Thus the exchange
   is legal against the same original M, including both sides of
   the triangle-cut condition.
3. The selected set avoids all six original mark endpoints, using
   the stated `t notin {v,w}` assumption. It therefore preserves the
   three named matching bits individually, which is stronger than
   preserving only their required logical relation.
4. The full new components are exactly `{u}`, `T-t+A+B`,
   `U0-A-B+h+t`. In particular the actual path `a-A-B-b` joins both
   old T branches; it would be incorrect to continue checking their
   parities as if they remained separate full components.
5. Their degree parities all vanish. The region-tree criterion
   therefore checks every complete complementary cycle, including
   the outer cycle. The independent explicit cycle count agrees:
   the new complete complement is `C4 disjoint-union C_(|O|+3)`.
6. B correctly states that this also repairs the even/even branch
   and does not prove that every original source has the 5/5/5
   pattern. No control graph is used as source-realization authority.

The independent checker agent additionally reported that the same
four-point set is the frozen weak control's row 55 and yields full
cycles of lengths four and eighteen with marked status 101. This
is consistent finite calibration only; it is not a premise of the
paper proof or an original-source instance.

No mathematical correction was required.
