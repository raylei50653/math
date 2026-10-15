# Cross-review: oddness descent

Reviewed the sibling
[PROOF](../2026-10-15-oddness-descent-6ddea32/PROOF.md),
[REPORT](../2026-10-15-oddness-descent-6ddea32/REPORT.md),
the complete named edge/face inputs and checker. No sibling file was edited.
No substantive mathematical gap was found in the stated scope.

1. In a fixed separation direction, every symmetric-difference component
   of two perfect matchings avoids both designated edges. Flipping those
   disjoint cycles sequentially gives the claimed connected exchange space.
   This does not assume an even-complement target exists.
2. Cutting all old complement edges used by one alternating cycle leaves
   disjoint paths and untouched cycles. Both reconnection systems are
   2-regular on the same endpoints. Summed path/connector parity exactly
   computes the odd-cycle difference; multiple cuts on one old cycle are
   handled rather than discarded.
3. If exactly one edge is cut from each touched old complement cycle,
   replacing the alternating cycle's old edges with the remaining old
   paths produces one new cycle. Its parity is the number of touched odd
   cycles modulo two, proving the stated strict decrease when that number
   is at least two. The missing general existence premise remains explicit.
4. For the 36-vertex control, independently reconstructed primal edges
   confirm `zb=[9,8]`, `xy=[3,10]`, facial zxy, by present and bx absent.
   Thus the specified named position is meaningful, and the retained by
   edge explicitly prevents this control from being the original T source.
   All twelve fixed-direction first moves have measure `(2,36)` from
   `(2,10)`. Exactly eleven direction-reversing moves reach oddness zero.
   The counterexample therefore has precisely the reported fixed-direction
   scope; it does not refute the source XOR descent obligation.
5. The 46-vertex control has three nontrivial 3-edge cuts and its primal
   designated edges share an endpoint. Its weaker scope is correctly
   separated from the source theorem. The 20-vertex control's six matchings
   with nonzero oddness have no once-per-old-cycle exchange, but this does
   not exclude exchanges revisiting an old cycle.

The sibling formal checker was replayed successfully with input drift zero.
An additional [independent script](checks/review_oddness.py), importing no
sibling checker, re-enumerates every matching using a different branching
order, reconstructs complement components, and compares the entire allowed
single-cycle exchange graph. It also independently checks the 36-vertex
named source gap and eleven opposite-direction descents, and checks absence
of the restricted exchange from every bad 20-vertex state. Its
[result](logs/oddness-independent.json) is PASS:

| Control | All matchings | Allowed states | Complete exchange edges |
| --- | ---: | ---: | ---: |
| 36 vertices | 365 | 60 | 390 |
| 46 vertices | 960 | 322 | 8864 |
| 20 vertices | 36 | 10 | 35 |

Reviewed graph SHA256:
`7ab93b52f2562313bd63a62ec044ca8154bd32f4c89cd3fafc1f1e62fc40a73c`.
Reviewed certificate SHA256:
`40c4830f66ea4b9eeaa64fac735a35954420d205bfc610fa42b4d81cc47d98a8`.

The wording “positive odd-number matching” was clarified by the owning
agent to “matching with nonzero odd-cycle count”; the count is even.
This was a prose correction and did not alter the certificate.
Source realizability is still **not triggered** and source omega=0 is OPEN.
