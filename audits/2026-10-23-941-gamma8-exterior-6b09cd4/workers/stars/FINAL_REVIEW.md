# Final independent main audit

Result: **PASS within the stated necessary-condition scope. No material flaw found.**

Reviewed the main `PROOF.md`, `produce.py`, `exploration/join.py`, `check.py`,
and `certificate-v2.json`. Also compared the main complete local orbits to
this worker's separately written `orbit.py` / `orbit.json`.

## Same-source proof and open boundaries

- Full original M02 and N13 are rootless. Each entire swap preserves the
  literal B14 word, the complete original02/13 induced graphs, every complete
  original02/13 component and the SAME K. The unique successor calculation
  is indexed by target/original02 type, with original03=4/9 retained jointly.
  Applying the same K after any M/N choice is therefore authorized by the
  actual frozen quantifiers. No independent palette witnesses are stitched.
- The actual M/K-transformed 12 path e-d-r-T-sΓ-x-h uses only known surviving
  original edges and fixed local colors. Its endpoint exclusions do not
  presume survival of whole original C/E paths.
- E is explicitly allowed to be rootless. The exact M2 separator statements
  distinguish the vacuous rootless-E case from rooted D. h=c really anchors
  E0 and forces a nonempty M2∩C separator. d=U/e=V/Y only forces a nonempty
  M2∩E separator when E has boundary contacts. For j=2 all M2 are strictly
  Γ-exterior. The proof does not replace this set by one T-neighbor.
- The N-flip U/q ear lemma correctly uses both original03 choices, each of
  which separates U from q, and does not assume the original03 type remains
  unchanged after the rootless flip. It applies for arbitrary j and either
  ear side, as stated.

## Four/five private exterior vertices

The C4 interior/exterior common-neighbor barrier and the four outside facial
third vertices are valid with complete original stars. The L/R three-point
contradictions use only full private T/sΓ/x stars. The O exact-four argument
correctly retains the possible nonprivate neighbor U0 at r; this cannot join
K2 to M2. Its last step uses the actual edge d-u and u's full private star,
so the second face duw lies in F even when d=U. No F-boundary link is treated
as a complete cyclic link. The other face has a different third vertex from
r; the fixed induced Γ graph/component nonedges exclude other Γ vertices as
w. Thus w is a new strictly exterior private point.

The resulting paper bounds L/R≥4 and O≥5 are necessary burdens, with no
sharpness, local-type exclusion, source-realization or global-k improvement
claim. The arbitrary-j scope of the endpoint/whole-component lemmas is kept
separate from the j=2 star bounds.

## Independent finite replay

The producer uses graph walks; the main checker independently uses union-find
for local/attached palette components. Original full gates are read from the
frozen authorities. On the incomplete known-edge graph, the checker asks only
that observed boundary contacts refine one complete necessary gate, rather
than inventing missing global paths. It compares every stored certificate
row, not merely aggregate counts.

The exact dimensions are four contracts = two targets × initial02 13/36,
each retaining both original03 choices as a gate. Therefore:

- 11 local graphs × 24 endpoint patterns × 4 contracts = 1056 rows.
- Each contract retains 116 and excludes 148.
- Total retained 464; total excluded 592.
- The 12 surviving identity patterns comprise ten with all 11 types and two
  U/q patterns with only three zero-ear types: 10×11+2×3=116.

The main checker explicitly checks equivalence to the paper's endpoint/ear
conditions for every finite row. All 11 unlabelled types retain private
endpoint cases. This is an endpoint filter, not full-exterior enumeration.

The independent stars orbit comparison matched all 88 local coloring states
and all 528 complete local palette partitions exactly, including singleton
and rootless local components.

Read-only commands executed:

```sh
python3 -B audits/2026-10-23-941-gamma8-exterior-6b09cd4/check.py --negative
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-gamma8-exterior-6b09cd4/check.py --seed 17 --negative
```

Both returned PASS with 14/14 semantic negatives rejected, 65 frozen inputs,
219 preserved prior outputs and immutable drift zero. The inherited checker
also passed, retaining all prior full local fibres/lifts and eleven-type
classification. Explicit require checks remain active under `-O`.

No new source, full collar, smaller bad, general wrong-side exclusion, Lean
or matching result is inferred from these finite checks. The main proof and
certificate maintain those OPEN boundaries.
