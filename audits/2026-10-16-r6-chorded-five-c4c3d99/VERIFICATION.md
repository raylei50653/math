# Verification and custody

The arbitrary-size authority is [PROOF](PROOF.md), with the same-agent
second-pass [review](REVIEW.md). No independent agent, external theorem,
source census or Lean build was used this round.

## Finite calibration

Normal and `PYTHONHASHSEED=17` read-only certificate checks exit zero
and have identical output. Removing a recorded deletion matching and
promoting source coverage to triggered are both rejected. Attempting to
overwrite the certificate with `--write` is rejected by exclusive creation.
Commands, exits and logs are recorded in [verification-runs](verification-runs.json).

The controls reuse the exact three planar graphs in the earlier
three-edge audit; their original labels, full face lists and all five-cycles
are retained. The two controls with all triangles facial give:

| Control | Simple five-cycles | Odd nontrivial face sides | Factor-critical sides | Interior-ear rejections | Induced-four expansions with both sides large |
| --- | ---: | ---: | ---: | ---: | ---: |
| icosahedral | 72 | 144 | 72 | 120 | 0 |
| flipped_icosahedral_return | 82 | 164 | 82 | 136 | 16 |

Ear counts are chord/side incidences, so multiple chords of a side count
separately. There are respectively 120 and 106 exterior chord/FC-side
incidences. These explicitly show that factor-critical plus facial
triangles does not itself force inducedness. Their deletion-matching
witnesses are recorded in the certificate. The third control has
nonfacial triangles, so the facial-ear implication is not applied to it.
It supplies 49 cycles and 98 odd sides as a premise-coverage control;
it is not claimed to refute the theorem without faciality.

The 16 induced-four expansions are checks of the general geometric
step; their additional 101 forced-face/source-sector hypotheses are not
claimed. Actual minimum-source coverage is **not triggered**. There is
no finite calibration of arbitrary original-sector topology; that part
is the paper argument. The perfect-matching deletion fibres include null
failures and are not substituted for original four-colouring fibres.

Replay from the repository root:

```sh
python3 -B audits/2026-10-16-r6-chorded-five-c4c3d99/check.py --check audits/2026-10-16-r6-chorded-five-c4c3d99/certificate.json
PYTHONHASHSEED=17 python3 -B audits/2026-10-16-r6-chorded-five-c4c3d99/check.py --check audits/2026-10-16-r6-chorded-five-c4c3d99/certificate.json
python3 -B audits/2026-10-16-r6-chorded-five-c4c3d99/check_bundle.py
```

## Documents and historical boundary

Formal documentation passed: 687 Markdown files, 9021 local links.
Scoped DocGraph passed: 97 documents, 383 relations, zero errors.
Tracked whitespace passed. [Documentation receipts](documentation-checks.json)
record the actual outputs. Whole-tree DocGraph was not run; no global
DocGraph PASS is claimed.

The current bundle checker retains the preceding cap audit's custody
implementation, with this round's BASE and manifest. It checks all 383
pre-existing audit files unchanged, 13 frozen authority/routing copies,
new Python syntax, local report links and final sealed membership.
Its PASS is not a mathematical proof check. The control graph bytes are
also hashed in BASE and checked by the finite checker.

The preceding CAP-BARRIERS bundle checker still passes. The older
JOINT-ZERO checker was also attempted and **fails at its historical live
routing hash for docs/STATUS.md** after this authorized research update.
Its preceding audit-membership comparison passed; no old audit bytes
were changed. Its original failure output is retained, not converted to
PASS. This round separately verifies every old audit byte against BASE;
the old routing snapshot is preserved and is not current routing authority.

All new research evidence was developed in this exclusive directory.
After the paper review, the documentation-maintenance phase updated the
four existing routing files, preserving their prior uncommitted changes.
The sealed [MANIFEST](MANIFEST.json) excludes only itself; the final
read-only bundle result is reported outside the sealed directory.

## Propagation

- Updated: Kempe current card, milestone, result row and exact stop;
  STATUS direct index; C4 direct parent; State active-route pointer.
- Reviewed unchanged: HANDOFF line selection; general and fixed-branch
  numerical bounds; earlier proof/certificate files; full colour relations.
- Remaining OPEN: 101 paired W5 and nonwheel seven-cut; 110 remaining
  five/seven-cut barriers; joint ordinary existence and even-complement
  positivity; full319 and the general claim.
- Propagation stops at L2: this narrows a named source obstruction and
  does not change the general bound, global research lines or README.

No commit or push. Reconstruction cost remains k+5.
