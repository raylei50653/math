# Independent source-geometry and full-fibre-control review

2026-10-14. Review scope: [SOURCE_GEOMETRY](../SOURCE_GEOMETRY.md),
[check_fibres.py](../controls/check_fibres.py), its local r table, the
source/bound statements in [REPORT](../REPORT.md), and the cited existing
C8/C9 reports. This reviewer authored [JOINT_FIBRES](../JOINT_FIBRES.md);
the present note is therefore **not** an independent review of that
reviewer's own paper proof. Its independent paper review is recorded
separately in INTERFACE_REVIEW.

## Adopted source statements

PASS for the five-apex induced skeleton. Each prohibited edge in the
table creates an original C4 whose two diagonals are absent by the
literal original-boundary contact restriction. The empty-C4 and
triangulated-interior hypotheses then give the stated contradiction.
The tp/qs equivalences use the actual sector at a/c and the absence of
nonfacial triangles. The excess h>=3 excludes both optional edges at once.

PASS for N_R(z) intersect N_R(r)={s,t}. An additional common neighbour
comes from a or c; its original five-cycle separates the indicated one
boundary vertex from the other two. All listed endpoints are distinct
and the extra neighbour is an original inner vertex. S6 and the known
five-degree link force it to be t or s. Thus the exterior identification
has exactly two parallel-edge pairs to suppress, and the resulting k-point
graph J is a simple sphere triangulation. The report correctly adopts
neither a general colouring extension on J nor the tentative further
triangle classification in J_CANDIDATE.

PASS for the degree table and G28. The losses at p,q are exactly the
deletion of original b; the losses at s,t and r are exactly the indicated
deletions of x,y. All other internal degrees are unchanged. Under original
d(p),d(q)>=6, R meets every listed 4-candidate hypothesis and its induced
outer C4 rules out the diamond. The bound uses k+1>28, hence k>=28.

The reviewer checked the existing EXTERNAL.md custody record for the
precise candidate definition, total-vertex bound, and the separation of
the C++ 28-point result from the independent Python/Sage 25-point result.
This review does not claim an independent rerun of either external
enumeration. The current audit's live primary-source check is documented
by its separate EXTERNAL.json record.

The C8 report's eight residual rows, filtered by e_x=e_y=e_b=0, leave
exactly c04-941 and c07-941. Its apex theorem gives original degree at
least six at all five apex vertices. The C9-932 report explicitly gives
that apex bound for all twenty h=4 residuals, and its source-contract
table identifies c09-induced-932 with extras (0,0,2,0,2). These are
exactly the two source subdomains claimed in SOURCE_GEOMETRY. No bound
has been moved to the other h=3 rows or arbitrary h>=4 sources.

PASS for the r-five-degree reduction. Its fifth neighbour v is distinct
from p,q by the prohibited rp,rq edges. Its contacts with all original B
vertices are excluded by the known links and the two displayed C4
arguments. Deleting r exposes exactly (z,s,v,t), with no diagonal. The
strict inner count is k-4<k. The local extension table produces mask13
from exactly mask7 within the permitted seven masks. Its per-row pq
intersection retains all full r lifts and gives exactly
ABAB/CD, ABAC/BC, ABCB/CD. The first row needs the new Kempe lemma, as
the text explicitly states.

PASS for the narrower G29 application. Under original d(p),d(q)>=6,
all remaining low-degree vertices affected by deleting r are on the
new outer boundary. The internal minimum degree and facial-triangle
requirements persist. The candidate has k total vertices, so the
rainbow-forbidding finite exclusion gives k>28, hence k>=29. The report
correctly excludes the already high-r C8/C9 subdomains from this r=5
intersection.

## Full-fibre control

The seven models are explicit oriented sphere-face lists with a selected
C4 outer face. Incidence, Euler characteristic, and cyclic vertex links
are checked before enumerating their full proper colourings. For these
fixed models all pinned boundary assignments are proper, and the
backtracking enumeration retains each entire colouring tuple.

The checked bijections are the ordinary C4 Kempe split by AC connectivity,
which does not require these samples to meet the joint failure hypothesis.
The script expressly verifies that its marked-triangle samples violate
at least one bad-palette condition, and retains actual ABCB/BC negative
controls. Thus the 14 full-set checks must not be described as 14 actual
target-source checks.

The local r table independently enumerates all 16 assignments, normalizes
the entire old boundary in one colour frame, and intersects allowed pq
palettes across all lifts of each same R' row. The fixed missing-colour
completion in the normalization is correct, including the r=D lift.

The first missing-lift negative control only tested set inequality. This
review requested validation rejection instead. The corrected version
passes the altered set through the named full-set equality validator and
records its caught error; the initial certificate is retained separately.

Actual post-correction replay:

    python3 -B audits/2026-10-14-c4-mask13-joint6-fdd3e22/controls/check_fibres.py --check

Result: PASS; 7 graphs, 42 complete fixed-Q colourings, 14 full-set
bijections, and 0 actual target sources. No new implementation defect or
mathematical scope error was found in this review. The source itself,
unbounded mask13 exclusion, K-infinity conclusion, and Lean formalization
remain outside these checks.
