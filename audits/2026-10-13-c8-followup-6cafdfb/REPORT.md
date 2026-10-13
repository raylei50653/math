# C8 original short crosscuts: h=3 forces at least eighteen inner vertices

2026-10-13. BASE `6cafdfb02fe5892a49eee21f92aea2369a25c022`.

**Proved under the existing globally minimal, edge-maximal source contract:**

    h=3 ==> k(G)>=18.

The BASE bound for this branch was k>=16. All eight unbounded 933/941 C8
contracts remain OPEN; this result excludes their sixteen- and seventeen-inner-
vertex domains in addition to the previously excluded smaller domains.

The new arbitrary-size paper lemma says that no strict inner H vertex can join
two original C8 vertices at cyclic distance two or three. Such attachments cut
off original C4/C5 caps and force a C8 vertex to have H-degree three. Therefore
every inner vertex meets C8 at most twice, and the eight original C-edge face
third vertices are all distinct. Outerplanarity then forces at least one more
vertex. Equality gives a unique original inner graph: a second C8 surrounded
by the original triangular annulus and capped with an eight-spoke wheel.

For that unique equality graph, all eight original outer collars have complete
Sigma=1023. The 80 fixed literal outer-row fibres contain **3,272 complete full
lifts**, all saved in [certificate.json.gz](certificate.json.gz). This excludes
the equality case as a 933/941 source. See [the full proof](PROOF.md).

The graph reduction is paper-only and does not use graph generation. The only
new finite computation exhausts complete colorings of these eight forced named
graphs, preserving all labels, attachments, edges, oriented faces, rotations,
the common literal color frame, and all ten fibres. Each graph has 22 vertices,
58 edges, and 37 inner triangular faces. The certificate includes empty-fibre
positions in its complete ten-row map; all happen to be nonempty here.

[Independent review](independent/REVIEW.md) accepts the paper argument and
independently reconstructs the graphs from the prior literal collar edge lists,
then compares every complete full lift using a fixed-order search, distinct
from the primary checker's extras-based reconstruction and minimum-domain
search. Normal and seed-17 runs agree. Negative controls reject a deleted full
lift, a deleted original edge, and a missing query.

Read-only replay from the repository root:

```sh
python3 -B audits/2026-10-13-c8-followup-6cafdfb/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c8-followup-6cafdfb/check.py --check --negative
python3 -B audits/2026-10-13-c8-followup-6cafdfb/independent/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c8-followup-6cafdfb/independent/check.py
python3 -B audits/2026-10-13-c8-followup-6cafdfb/independent/check.py --negative
```

Seven BASE documents are frozen and hashed in [INPUTS.json](INPUTS.json).
The independent checker separately hashes and freezes the prior literal source
results. Primary verification is recorded in [VERIFICATION.json](VERIFICATION.json),
and the independent directory contains its normal, seed-17, and negative receipts.
[MANIFEST.json](MANIFEST.json) seals all audit files except itself.

The source quantifier is the existing minimal graph among **all** disk-C5 graphs
outside K132, with its entire Sigma transported at once to 933 or 941. No N2,
epsilon, edge-critical, Gallai, or extra color-count assumption was added. The
cap replacement and degree theorems retain their upstream K132 and coloring
dependencies. No new external theorem, Lean formalization, or graph generator
was introduced.

This audit alone does not change the general bound K<=14 available at BASE,
prove h>=4 or n5>=10, or close K-infinity=K<=5. The actual target-source status
is `not triggered`: exclusion follows from paper completeness and full-fibre
enumeration, not from zero target sightings. Concurrent general-bound work has
its own evidence and is not a premise here. Only this exclusive audit directory
was changed by this worker; no shared document or prior certificate was edited,
and no commit or push was performed.
