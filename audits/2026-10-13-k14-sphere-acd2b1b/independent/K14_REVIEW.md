# Independent read-only review of the K14 sphere audit

Reviewer: delegated research agent `/root/c8_gap`.
Review date: 2026-10-13. This is a mathematical and implementation review, not a
cryptographic signature or an independent proof of plantri's generation theorem.

## Verdict and scope

**PASS within the explicitly inherited generation-completeness boundary.**
The cone/root coverage argument and the two colouring implementations justify
K<=14=K<=5 when combined with the already established K<=13 bound and source
normal form. This review found no source-pruning, changed-boundary, or marginal
relation substitution in the new primary or independent checker.

The separate C8 paper note proves the conditional strengthening h=3 => k>=16.
It retains the original eight unbounded source residuals. That proof is not
needed for K14's unpruned sphere coverage.

## Cone and complete source coverage

If any catalogue-outside source has k<=14, global minimality and the prior K13
result force k=14. The existing edge-maximal normal form gives the same simple
triangulated disk G with original ordered C5 boundary, boundary degrees >=4,
and internal degrees >=5. It has 19 vertices and 49 edges.

Adding one new vertex z in the original outside disk and joining it to all five
original B vertices gives a simple spherical triangulation T with 20 vertices,
54 edges, and minimum degree at least five. Its specified z has degree five.
Conversely, deleting any degree-five vertex from such a T, retaining the original
rotation and the vacated star as the specified outside face, gives a 19-vertex,
49-edge disk with the desired degree bounds. Allowing boundary chords and other
nonminimal sources in this converse only enlarges the finite domain.

Every simple spherical triangulation is three-connected, so the inherited
plantri `-m5` domain covers T without requiring a new five-connectivity premise.
Both programs inspect every degree-five vertex of every generated T. They retain
one literal ordered B, all ten proper normalized B words, and all ten D5 frames.
Whole-embedding isomorphism can move the distinguished root, but every degree-five
root is explicitly retained; boundary start/orientation is covered by the frames.
Hence no minimum source is lost. Neither program uses h, C8, a cap, or a proposed
mask as a pre-colouring pruning condition.

## Primary implementation inspected

`check.py` independently checks reciprocal simple rotations, connectedness,
face-dart traversal, genus zero, triangular sphere faces, the literal ordered
outside C5 after deleting z, exact degree lists, and curvature. Its exhaustive
fixed-order colour search branches over every available one of four colours;
a branch is rejected only by an actual same-source edge conflict. It records
entire vertex-colour strings for every lift, and explicit lists for all ten
boundary fibres. The full payload is compared byte-for-byte on `--check`.

The source-generation comparison invokes the frozen whole-embedding canonicalizer
only on the two generated sphere collections. It does not participate in the
colour search or remove a root. The two generated collections each contain 73
distinct embeddings and their canonical embedding sets agree.

## Independent implementation inspected

`independent/compare.py` calls only dimension-neutral routines from the frozen
independent K13 implementation. The old K13 dimension-specific `calculate`,
`verify_disk`, and `collar` entrypoints are not invoked. The independent parser,
original-label face traversal, and propagated-domain exhaustive CSP are distinct
from the new primary fixed-order backtracking.

Every independently reconstructed original-label lift is converted with the
record's actual vertex map and compared to the exact full-lift list. The recorded
original rotation, edges, faces, degree list, h, boundary mapping, and all ten D5
counts are also checked. Visited-root equality prevents omitted or spurious root
records. This compares the same complete graph and same boundary assignment,
not two independently feasible projections.

## Replays personally executed

Both commands completed with exit status zero during this review:

```
python3 -B audits/2026-10-13-k14-sphere-acd2b1b/check.py --check
python3 -B audits/2026-10-13-k14-sphere-acd2b1b/independent/compare.py
```

Both obtained 73 spheres, 1,001 root-deleted disks, 10,010 literal boundary rows,
and 180,228 complete lifts. Every root relation was 1023, a member of K132.
The primary payload SHA256 at review was:

```
01c6ef3c978868479c7a292f5575a803f7e27d4de8275b43084a477bc0d97d7e
```

The generation replay script and saved replay log were inspected. The log records
byte equality for the minimum-five run and the minimum-four run with a terminal
minimum-five filter; the latter inspected 64,719,885 outputs and retained 73.
This reviewer did not personally rerun compilation/generation. Its completeness
continues to depend on the frozen published plantri theorem and implementation;
two generation entrances are not two unrelated software implementations.

## C8 paper lemma review and preservation boundary

`C8_PROOF.md` explicitly establishes connectedness of Q=H[I], absence of Q leaves,
and the outer-face incidence used in its outerplanar step. For m=6 the fixed
original C-edge faces pair C-I incidences and force odd Q-degrees and a forbidden
leaf. For m=7, curvature permits only two stated degree multisets. Their parity
and Euler counts either contradict the no-leaf lower bound directly or force an
outerplane graph with just one vertex of degree <=2. A maximal outerplanar
augmentation has at least two ears, proving the required contradiction even
when Q originally has cut vertices.

This is an argument on the same original H and its actual faces. It does not
combine counts from different sources, promote a necessary support to an actual
relation, or claim that the eight C8 residuals are entirely excluded.

A packaging follow-up was communicated to the parent: the C8 apex theorem and
its source/geometry dependencies must be frozen alongside the K14 inputs before
sealing the final manifest. The unpruned K14 argument itself is independent of
that supplemental C8 theorem. All 1,001 actual finite-domain relations are full,
so their zero rejected fibres do not by themselves exercise an empty-fibre branch;
any dedicated negative/calibration controls must be reported separately.

The result is paper reasoning plus complete finite generation and exact exhaustive
colouring, with no newly formalized Lean theorem. Actual 933/941 source occurrence
remains `not triggered`; source exclusion follows from complete coverage and
complete relations, not from that phrase.
