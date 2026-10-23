# Independent review of the B14 join argument

Reviewed `../b14/FINDINGS.md` against:

- `audits/2026-10-23-three-mask-methods-cb8f859/941/PROOF.md`, sections 1 and 4,
  and all four `component_interface_rows` of its certificate;
- `audits/2026-10-21-w7-I-joint-2c38d1d/geometry/PROOF.md`, section 2;
- the original Γ8 and complete-rootless-component proofs.

The complete M and N flips are valid same-original-graph operations. A complete
02 flip on M preserves the entire 02-induced graph, its components, and the
unchanged 13-induced graph. A complete 13 flip on N likewise preserves both
induced vertex sets and component graphs for the split 02|13. Rootlessness
preserves the literal B14 word. Therefore each new pre-K coloring still has
the same necessary original 02 type 13/36; the existing original-03 gate and
the unique necessary post-K successor apply anew. No independent palette
partition is being selected.

The N-flipped actual path U–r–T–sΓ–x–q is indeed 03 whenever d=U,
W*=q and xW* is an original edge. Both allowed original-03 types separate U
and q. The direct dW* edge excludes the other ear. This proof does not use
`j=2`, the side of either ear, or the number of global true crossings.

The M-then-K coloring has the stated actual χ12 path
e–d–r–T–sΓ–x–h. The unique post-K successor separates c from every one of
U,V,Y in both targets and both original 02 types. Thus h=c really forces
d and e private, uniformly in Γ8 interior size and ear status. The exact
boundary identity alternatives and the q/V prohibition follow from complete
contacts and the independent original z5-ear common-neighbor theorem.

The separator statement is also valid. In the original ψ12 graph, deleting
M2 preserves both named paths. M0 was absent from that graph; inserting its
χ12 vertices joins their surviving components by T. All original C and E
boundary contacts retain their colors because M is rootless. The necessary
χ successor then forbids simultaneous surviving C-boundary and E-boundary
reachability. In the stated endpoint cases the opposite surviving path has a
literal boundary contact, which yields the claimed M2 vertex separator.

For `j=2`, no M2 point is on or inside Γ: its only interior points are N3 τ
and K2 ζ, and its only M point on Γ is T0. Therefore every separator point
in M2 lies strictly outside Γ. A demanded separator is nonempty only when
the actual complete component under discussion meets B14. C always does;
Γ's E can be rootless. Thus h=c demands a nonempty exterior M2∩C separator,
whereas d=U or e∈{V,Y} demands a nonempty exterior M2∩E separator only if
Γ's E itself meets B14. For larger j one must not move all M2 separator
points outside Γ without another argument.

This caveat also affects the phrase “complete E12 contacts are {c,s} / ...”
in FINDINGS: those are the contacts of the boundary component D containing
c. Γ's complete E is either D or rootless. Its h contact is still either c
or private, so the exact endpoint identity alternatives and all endpoint
contradictions above remain valid. The universal separator implication also
remains valid when E is rootless, but is then vacuous on its E side.

The 12 surviving endpoint patterns and 116 endpoint/type rows are correct
as a finite necessary filter. The 116 rows do not imply source realization,
and none of the eleven unlabeled local types is excluded.

Wording detail: saying all boundary-indexed fibres/full lifts “remain the
same” should mean that the original graph, literal boundary-indexed extension
problem, and frozen complete records are unchanged. It should not assert that
an individual private vertex coloring or its component membership in the
other palettes is unchanged by a flip. The proof itself respects this
distinction; no mathematical correction is required.
