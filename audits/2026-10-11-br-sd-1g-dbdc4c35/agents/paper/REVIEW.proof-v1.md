# BR-SD-1g independent review of first complete proof

2026-10-11. Reviewer: `/root/paper`. BASE:
`dbdc4c35f785519c8e3cb0260807f0d2feb82469`.

Reviewed root `PROOF.md` SHA256:
`cc5c078361ca3a93ce5e990acdb356073e6fbb5d8996c967c3cd899be0629c1a`.
This review precedes final `MAPPING.md`/`REPORT.md` and does not accept later bytes.

## Mathematical verdict

No mathematical blocker found. The exact two-branch candidate scoped exclusion
follows from the proof's complete original source contract and the externally
frozen degree-list characterization. It does not infer an actual source from
degree capacity, a synthetic list assignment, or failure of the old routes.

| Proof obligation | Independent check |
| --- | --- |
| Source identity | §1 retains same G, exact sole deleted spoke, X=M, M's own rejection/minimality, full source witnesses, degree4/5, literal β/Col and original lifts. |
| W1 private witness | The connected W1 is separated by x1. x1 is a cutpoint, and neither r nor a1 supplies a replacement noncontact private J1 witness. J2's old private point remains available. |
| Terminal applicability | §2 separates direct applicability at v/a3 from violated location or arm-degree premises elsewhere. It does not apply a one-W theorem wholesale to the two-W source. |
| Original complete lists | All original neighbors are accounted for by C, B and s. The degree assignment has ≥, and slack is allowed before non-colorability. |
| Complete extension | The restriction/join argument covers every original edge, including both branch interiors and attachments; ignored-node factors are explicitly retained. |
| Gallai premise | The frozen PDF defines degree assignment with ≥ on p.5, and Theorem10 supplies exact blockwise unions/disjoint palettes on p.6 for connected non-colorable C. No initial tightness or H_M biconnectivity is assumed. |
| J2 exact palette | Preserved J2 witness belongs to original S and has degree2 in C. Its two distinct B neighbors must be the exact actual support pair; proper β on that edge yields `P_J2={T,D}`. |
| Barrier | S meets the L-side only through r. Its only block at r is preserved J2; branches have no second exit. A palette containing exactly one of T,D cannot meet J2 anywhere. |
| Incidence graph | Maximal blocks include bridge K2 blocks. The graph with every original vertex-node is the standard block-cut tree with noncutpoints added as leaves, hence finite and acyclic. |
| Chase start | T in q's list produces an incident T palette; D excluded at q excludes D from that palette. It cannot be J2 or meet it. |
| Chase step | Every chosen different vertex lies in S away from q/r, needs the other literal color, and forces a different incident block. Disjointness forbids the preceding color in the new palette. A noncutpoint gives immediate contradiction. |
| Finiteness | A nonbacktracking walk in a tree is a simple path. Its forced indefinite extension contradicts finite C, independently of arm length, W2 position or either branch size. |
| W1 palette routing | Its unique first block follows from connected C[W1] after deleting x1; degree1 at x1 yields bridge, degree2 under Gallai yields odd cycle/triangle. D can lie there while excluded from J1; no false universal incident-palette inference is used. |
| Scope | §7 states only candidate scoped exclusion of the requested exact two-branch family and leaves all parent/general identities OPEN, with unconditional closure count 0. |

## Precision note

The phrase “C 的完整 L-coloring 恰對應 … M 的完整延拓” in §3 is valid as
an existence equivalence and as a restriction/join relation with the original
ignored-node factors. After those coordinates are forgotten, it is generally not
a one-to-one map: one C-coloring can have multiple legitimate full M lifts at the
ignored B-only points. The following sentences retain those coordinates/factors,
so this does not invalidate the contradiction. A final wording that explicitly
says “連同被忽略原點的合法因子” would remove ambiguity.

## Remaining review boundary

Final independent acceptance still requires checking final root PROOF/MAPPING/
REPORT and controls classifications, followed by hash readback. No actual target
source was reviewed; that test remains `not triggered`. This paper review does not
serve as custody verification, canonical adoption, a Lean theorem, or a general
multi-branch Gallai-tree closure.
