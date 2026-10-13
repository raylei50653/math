# Independent review: conditional arithmetic and forest preclassification

Reviewed the final `../conditional/REPORT.md`, `forest_review.md`,
`check.py` and `certificate.json`. The main report is sound with the
conditional logical status detailed below.

## Forest preclassification

The arguments in `../conditional/forest_review.md` are correct under its
frozen source hypotheses. In particular the U-neighbour argument uses the
four-cycle through the original centre v; this is essential. A private vertex
has at most two adjacent B neighbours and two adjacent U neighbours, so a
private-forest isolated vertex would violate original degree at least five.

For a private forest with r vertices and c components, annular Euler and
triangle counts give `e=3r+20`, `t=2r+10`. Let f=r-c. Each forest edge is in two
triangles with exactly two private vertices, and such a triangle contains
only one forest edge; therefore their count is exactly `2f`. The terminal-only
triangles each have exactly one boundary edge and two cross edges. The report's
identities `x-M+a=10`, `M+2a=2p` are consequently exact. They imply `M=2c` and
`p=c+a`; the private degree sum is `4r+10-c-p`, hence `r<=10-c-p`.

Every forest leaf has four terminal neighbours and degree exactly five. Its
cyclic link must contain at least one B–U edge because deleting its sole
private neighbour leaves a path containing both B and U labels. Distinct
leaves give distinct mixed faces. The `2c` lower bound for the number of leaves
saturates the `M=2c` upper bound, so each component is a path and all mixed
faces belong to endpoints. With `r>=7` this yields one path and precisely the
three reported numerical slots `(r,p,a)=(7,1,0),(8,1,0),(7,2,1)`.

No slot is excluded by this preclassification alone. This note does not claim
that a degree sequence has a planar realization or that a remaining slot is
a true catalogue-outside source.

## Exact finite relation arithmetic

`../conditional/check.py` reads the frozen 132-mask catalogue and recomputes
all proper five-cycle tuples and the displayed subset/superset leakage sets.
Its two controls are formal named relations; no graph, rotation or full graph
lift is claimed for them. Their exact Q and fan projections, multiplicities,
and leakage counts are verified. Such formal controls refute deductions from
those projection/multiplicity facts alone; they cannot refute additional
plane-source constraints. The script labels this boundary explicitly.

`PYTHONHASHSEED=17 --check` passed. A temporary copy with the recorded count of
proper rim assignments changed from 240 to 239 was rejected. Original source
and frozen-catalogue hashes were unchanged; see `review_checks.json` and its
replay script. This review does not rerun the upstream graph catalogue search.

## Final main report: exact conditional status

The source-specific positive-union no-go is valid. Under the *hypothesis* that
G is globally minimum outside K, every smaller legal branch has its relation
in K. The exact catalogue subsets of 933 and 941 show that every sound branch
misses the original accepted row `01232`; a union of sound branches therefore
misses it as well. Adding edges to a quotient does not escape the argument
as long as the resulting graph remains legal, preserves B and has fewer than
k internal vertices. This implication does not assert that the hypothetical
minimum source exists. It is a direct consequence of the global-minimality
premise and catalogue membership; it does not constitute a new geometric
nonrealizability theorem for arbitrary annuli or prevent proving the source
premise contradictory by constructing a representative.

The stronger named-lift consequence is also valid. Every original accepted
`01232` colouring has a three-colour rim and belongs to two adjacent quotient
pullbacks. Each such quotient must leak to one of the named rejected rows.
Any leaked colouring uses four rim colours, so it belongs to exactly one
quotient pullback. Thus the two leakage witnesses are necessarily different
full H colourings, even if their B row is equal. This avoids joining unrelated
existence witnesses. The special R=933, Sigma(H)=957 argument similarly forces
at least two lifts in each of two distinct rejected B fibres, hence at least
four total.

The formal support examples show consistency only of their listed relation
projections, not realization by a graph. The report states this explicitly.
The final link to the parent's forest report properly defers the later forest
exclusion to that report; this review does not duplicate its enumeration.

No requested correction remains. The no-go's true minimum-source status is
conditional `triggered and holds` as a theorem; actual source realization
remains `not triggered`, exactly as the report states.
