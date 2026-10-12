# Final independent proof review

**Final current verdict: conditional PASS**, including the stronger exclusion
of both nonadjacent two-contact types. The only remaining types are M0, M1,
and M2E. The final paper hash and stable v1/v2 replays are recorded in the
addendum below. The earlier checker-version drift is resolved; the first
review below is retained as review history and its five-residual stopping
point is superseded by the addendum.

2026-10-12. Review of `paper/classification.md` against the frozen Task A and
degree-bound premises, followed by read-only replay of both finite controls.

**Initial mathematical verdict: conditional PASS.** No substantive gap or overclaim
was found in the source-conditional classification, complete-interface
replacement, or the new conclusion `m<=2`. One verification-metadata drift
was noticed below; it does not invalidate the successful replay and was
subsequently reconciled in the final addendum before sealing.

Reviewed paper SHA-256:
`e08d8f3675915b65da1855c1815010b5eeb6a5b31d4874754e59936060d98493`.
The line references below refer to that exact version.

## Paper checks

- Lines 15-21: clearing the bounded interior of an occupied triangle preserves
  all named `B` vertices. The original accepting coloring supplies one interior
  lift, and the single proper triangle color orbit supplies the extension for
  every outside coloring. This uses global minimum interior order and no
  edge-critical premise. The proof also applies when triangle vertices lie
  on `B`.
- Lines 23-29: the degree-5 rotation gives five distinct neighbors and the
  five actual incident faces, hence an embedded star disk with only `v`
  inside. A nonconsecutive link chord leaves another spoke/neighbor in each
  sector at `v`; the bounded side of the resulting triangle therefore has
  a vertex. Such a vertex cannot be an outer-boundary point. The occupied
  triangle contradiction is valid, and does not assume an entirely interior
  link. No finite skeleton test is being substituted for this paper argument.
- Lines 33-57 and 74-84: the common-order and shared-edge rules correctly
  distinguish relative orientation from independent relabeling. In
  particular the `pi=1 iff qi=1` rule uses geometric common-edge direction
  as well as the induced cycles. The resulting positive gap decompositions
  exhaust all contact sizes. An adjacent contact pair leaves a C8 cap;
  it cannot be treated as the nonadjacent C4+C6 or C5+C5 case.
- Lines 64-72: all nine cap boundaries checked edge by edge against their
  listed `B` and `L`. The M2E sequence has eight distinct vertices; M2-46 has
  lengths four and six; M2-55 has lengths five and five; M3S has two genuine
  quadrilateral caps. The one-contact boundary walk has one repeated vertex
  before closure, and the no-contact row has two distinct boundary cycles.
- Lines 75-77: when a boundary vertex is internal to a shared path, its two
  original inner face sectors are occupied by the wheel faces, forcing
  degree exactly three. This is stronger than merely observing degree three
  in an unfilled diagnostic skeleton and properly excludes M3P, M4, and M5.
- Lines 81-84: Task C's specified cap boundaries use the opposite relative
  cycle orientation and select M2-55. Its apparent tuple similarity to M2-46
  is therefore harmless. The paper does not import Task C's closure result.
- Lines 88-107: region ownership follows from the embedded skeleton. In
  particular the M2E edge `ab` is retained outside the cap even though both
  endpoints are its boundary pins. The only possible new boundary chord in
  an original cap joins a `B`-exclusive to an `L`-exclusive pin. For a C4 cap,
  its sole candidate diagonal would leave two empty triangles and a link
  private vertex of total degree four, which is indeed impossible under
  the inherited degree bound.
- Lines 109-118: the annular cut retains both path copies and equality of
  their original pins. The M1 closure has two sectors at its repeated pin;
  cutting it normalizes to a ten-sided disk only if the equality and sector
  restoration constraints remain. Neither is treated as an ordinary C5
  patch with only five interface pins.
- Lines 122-165: all shared pins and identities are fixed in one color set.
  Equality of the full named extension relation supplies lifts for the
  *same* interface assignment in both directions. The proof correctly does
  not promise a coloring bijection or matching fibre cardinalities. The
  explicit joint records all ten outer rows and their empty possibilities;
  additional pins are added to the common assignment. The separate embedding
  premise and harmless simplification of duplicate edges are necessary and
  present.
- Lines 175-211: the retained original interior set is exactly the center
  plus the `5-m` link-exclusive pins. The formula adds any further retained
  contacts by a set union, avoiding duplicate counts. Each actual C5 cap
  has smaller interior order, so global minimality permits its five-interior
  representative with all five boundary labels fixed. The numerical bounds
  are correct: M3S at most `3+3+3=9`, M2-55 at most `4+5+5=14`, and M2-46
  at most `7+r6`. The five residual rows remain explicitly open.
- Lines 208-222: deleting `v` gives a smaller ordinary C5 source, but an
  unmarked representative does not retain the five original link pins or
  their sectors. The distinction is correct. The conclusion is conditional
  on the adopted upstream screen, small representatives, and twelve bound;
  it is not existence of a source, finite proof of arbitrary-size behavior,
  or a new Lean theorem.

## Independent finite replays and semantics

The following read-only commands exited 0 in this review:

```text
.venv/bin/python audits/2026-10-12-degree5-link-a-e293fc11/controls/check.py --check audits/2026-10-12-degree5-link-a-e293fc11/controls/certificate.json --seed 29
.venv/bin/python audits/2026-10-12-degree5-link-a-e293fc11/review/projection/check.py --check audits/2026-10-12-degree5-link-a-e293fc11/review/projection/certificate.json
```

Topology replay output: nine literal skeletons, 362 legal oriented contact
records, all ten-row fibres. Certificate SHA-256:
`131faafb5961b31fd4eefe13d03b9aab05d92f7298ef80ede1bdd542879b8acd`.
Checker SHA-256 observed after that run, during the concurrent version change:
`7b0019f19d996cebe2737f8d0a5a2d5b67db4cb799b2338765379ee2bd81e0d4`.
This after-run reading does not bind the preceding v1 certificate replay to
that newer checker. The stable, matched version pairs are verified below.

I also inspected the relevant checker paths. Its interface encoding iterates
every assignment to all original link-exclusive vertices, distinguishes
improper assignments from proper zero-center fibres, stores every center
color, and compares the joined full lifts both with full product enumeration
and a separately ordered recursive search. Its D5 transport is one global
vertex map on both cycles, with the same orientation sign. The contact
enumeration is explicitly a finite incidence domain whose exhaustiveness
for actual sources depends on the paper Jordan argument. The finite graphs
are not assumed triangulated or minimum-degree sources. All these scope
boundaries match the paper.

Projection replay output: `P0=P1=1023`, but `P0_Q=255` and `P1_Q=987`; the
complete ten-row comparison and the witness `012310` passed. The two edges
`za` and `ze` can be inserted into the same named exterior face
`(z,d,e,a,b)`. This is a valid planar countercontrol to forgetting the extra
pin, not a change of embedding admissibility. Its checker and certificate
hashes were respectively
`b68ee6a068815c323de82c4bf580ae59c51c0f6889f7886250faddac201c2f18` and
`ca067783c057ffcff5bd0406ece2a606aa775096527906834e162184130cbef4`.

The ordinary complete-interface premise is `triggered and holds` in the
finite joins. The weaker outer-projection replacement premise is
`counterexample`. A genuine globally minimal 933/941 source is
`not triggered`. No new Lean execution was performed by this reviewer.

## Verification metadata finding

At review time `controls/verification.json` recorded checker hash
`b0610d3a7c68a2bc9635f6e4819cbb8b951f0e6629af03b565654d1d81821a4f`,
whereas the currently replayed checker hash is `7b0019f...` above. The root
agent was notified. The earlier recorded seed runs cannot silently be cited
as exact-current-checker runs until this record is refreshed or its historical
checker version is explicitly retained. The original seed-29 run passed,
but its post-run checker hash was observed during that concurrent edit; the
matched runs in the final addendum replace that ambiguous version attribution.

## Final addendum: stronger source conclusion and resolved evidence custody

The final reviewed `paper/classification.md` has SHA-256
`92df030ab8cfdf3211f1304e288ef12948ad7cd1069d6d3fd2aee4f54d9fafcc`.
I reread this complete version, including its new Section 5.1 and the updated
classification/count tables. **Conditional PASS** applies to this exact
paper and its stronger conclusion: only M0, M1, and M2E remain possible.

The new proof is independently reproduced in
`review/small-cap-refinement.md`. Its critical steps were checked as follows:

1. Replacing one actual cap by its complete-boundary representative would
   change the whole interior order by `r'-r` while preserving the whole
   relation. Global minimum interior order therefore bounds each original
   cap's private order, not just its representative's order: at most 3 for
   C4, at most 5 for C5. The C5 representative is available because that
   actual cap has fewer private interior vertices than the source.
2. Every original cap private vertex retains its full original degree in
   the cap. The cap is triangulated, so its exact Euler count and private
   degree sum are `E=3r+2p-3` and `D=3r+p-3-d+e`, with `d` boundary chords
   and `e` induced private edges. Both signs and constants in the final
   paper are correct.
3. For `2<=r<=5`, every private vertex has a cap-boundary neighbor. The
   corresponding original edge lies in the unbounded face of the induced
   private graph, proving outerplanarity in the actual embedding. The
   argument also handles disconnected private graphs. After connecting
   components through the unbounded face, the outer boundary walk has
   length at least `r`, and every inner face length is at least three.
   The paper's inequalities `2e>=3(f-1)+r` and `r-e+f=2` indeed give
   `e<=2r-3`; the original graph has no more edges than that augmentation.
4. Thus `D<=5r+p-6<5r` for `p=4,5`, contrary to the original degree bound.
   At `r=1`, only the C5 wheel is possible. Hence original C4 caps have
   no private vertices and original C5 caps have at most one.
5. The M2-46 zero-private C4 requires a diagonal. The contact-contact
   diagonal is forbidden; the other diagonal gives exactly boundary degree
   three at `b` and interior degree four at `x`, both genuine full-source
   degrees by the original region ownership. M2-55 instead has original
   `k(G)=4+rP+rQ<=6`, contrary to `k(G)>=13`. These exclusions do not
   depend on Task C's separate all-catalogue-pairs finite closure claim.

No remaining paper gap or mathematical overclaim was found. The earlier
five-residual review and fourteen-vertex representative estimate remain
historically correct but no longer describe the final stopping point.

The metadata issue is now **resolved**. The original v1 checker is retained
as `controls/check.v1.py`, matching the original `verification.json`.
The current `controls/check.py`, `certificate.v2.json`, and
`verification.v2.json` form a second consistent version. The v2 change gives
invalid contact-premise encodings status `not triggered` with a rejection
reason instead of calling them mathematical counterexamples; the literal
graphs, complete relations, and legal-contact counts are unchanged.

I independently replayed both matched versions with seed 29, measuring each
checker and certificate hash immediately before and after its subprocess.
Both runs exited 0, and both before/after hash pairs were identical:

| Checker | Checker SHA-256 | Certificate | Certificate SHA-256 |
|---|---|---|---|
| `check.v1.py` | `b0610d3a7c68a2bc9635f6e4819cbb8b951f0e6629af03b565654d1d81821a4f` | `certificate.json` | `131faafb5961b31fd4eefe13d03b9aab05d92f7298ef80ede1bdd542879b8acd` |
| `check.py` | `7b0019f19d996cebe2737f8d0a5a2d5b67db4cb799b2338765379ee2bd81e0d4` | `certificate.v2.json` | `cb1f620e663e955b813b250e1360e9e49b8931568e65cf852ea861aa76ea20b6` |

Each output again reports nine literal skeletons, 362 legal oriented records,
and complete ten-row fibres. `verification.v2.json` records this same current
checker and certificate pair for its normal and corruption checks. There is
no unresolved checker/certificate custody finding in the reviewed package.
All general-source and external-theorem limitations stated earlier remain.
