# Independent C review of A and B

Reviewed the current A and B paper arguments against the frozen source
degree, induced-forced-pair, all-singleton and 111-colouring inputs.

* A1's parity-sensitive degree minima give exactly `12=Q-L`, with even,
  nonnegative L. A2's bit partition includes h in the correct case,
  including h internal to a component or inside S.
* A3's bounds are at most ten for a sole five- or seven-wheel, below
  Euler's twelve. The wheel centre is outside T: a forced-edge endpoint
  meets X, while a forbidden-edge endpoint leaves a non-factor-critical
  odd path when h is deleted.
* A4's common-wheel support is the symmetric difference of the two
  closed wheel neighbourhoods. The all-three-marked vector has Q=2;
  only flipping m has the negative sign. This gives exactly
  `L=2(1-r_cap-epsilon)` and the stated overlap/degree restrictions.
  An h edge joining the two wheels supplies two shared rim vertices,
  contradicting the overlap bound.
* B1's saturation uses one common M in P111, with X already matched by
  the forced edges. Every odd component needs an odd positive crossing
  count, while S and h supply at most `|S|+2` incidences in total.
  Equality yields tau=1 and the simultaneous tight cuts for every M.
  It does not require maximum S until factor-criticality is used.
* B2's two uncrossing formulas are exact matching-edge identities; odd
  set parity forces equality and the stated avoided cross edges.

The hub-crossing W5 side issue is not automatic from a small-cap theorem.
C1.2 resolves it for an actual induced five-cut boundary using the four
forced vertices: the opposite choice would place an induced two-edge
X inside four vertices of a dual pentagon, which necessarily induce
three edges. Noninduced boundaries require their separate argument.

No reviewed statement supplies an even-complement joint matching. The
same-source positive-oddness case and the positive-weight target remain
OPEN, even if a subsequent ordinary-matching obstruction is excluded.
