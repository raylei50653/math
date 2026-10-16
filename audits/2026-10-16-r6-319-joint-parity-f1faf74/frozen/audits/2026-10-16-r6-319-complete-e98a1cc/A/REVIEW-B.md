# A independent review of B

Read B/PROOF.md and independently replayed

`python3 -B audits/2026-10-16-r6-319-complete-e98a1cc/B/verify.py --check audits/2026-10-16-r6-319-complete-e98a1cc/B/certificate.json`.

Exit status 0. The replay covers all four controls, each complete
root-normalized beta/gamma choice, the complete endpoint PM batches and
their individual alternating components. Source coverage remains
`not triggered`.

* B1 is valid: taking the f component of `M0 xor N` preserves e and g
  because those marked edges are common to both matchings. The resulting
  ordinary 101 need not be even and is not asserted to minimize oddness.
* B2's path decomposition uses the same complete labelled old F0.
  B is a matching, so a touched old cycle produces nondegenerate paths;
  each has parity `1+b(x)+b(y)`. Every assembled new cycle uses equally
  many paths and A edges, so its parity is exactly its transition parity.
  The total transition count is even by a cyclic binary word on each
  original alternating cycle. Empty Tait fibres are explicitly retained.
* B3 correctly separates t=2 from positivity. Two transitions on separate
  new cycles give exactly two odd cycles. Its sufficient condition is
  joint and does not demand both W110 and W101 positive.
* B4's short-cycle proof is valid for the actual simple cubic dual:
  3-edge-connectivity makes each nonempty side of a chordless cycle
  require at least three external incident edges. A cycle of length at
  most five cannot support two such sides. A dual triangle would therefore
  be facial, contradicting primal minimum degree four; this also removes
  any chord of a four- or five-cycle. A marked pentagon is one of the two
  faces incident with f, hence has primal centre p or q. The frozen 101
  bit row singles out the endpoint opposite z. A remote retained W5
  pentagon avoids f, so the two cases are correctly distinguished.
* The control provides a limitation of generic planar reasoning, not a
  source counterexample. Its degree-premise failures and complete-U gap
  are material and remain explicit. B's source-specific transition
  placement and long-odd-cycle obligations remain OPEN.

Paper proof and independent finite replay: PASS at the inspected version.
The B5 count prose was being corrected from six choices on one M0 to four
choices on the displayed M0 and two on the second M0; this correction
does not change B1--B4 or the independently verified certificate.
