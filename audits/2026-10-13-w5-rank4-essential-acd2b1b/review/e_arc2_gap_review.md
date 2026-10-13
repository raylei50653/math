# Independent review of the essential rank-four classification

2026-10-13; reviewer task `/root/e_arc2_gap`; BASE `acd2b1beea6c909edade565a00eeeeac05d2b3a7`.
Scope: independent paper scrutiny and small combinatorial corroboration. This review
does not claim a fresh replay of the complete coloring certificate or the separate
contractible rank-four audit.

**Verdict: PASS for the proposed essential rank-four classification and complete
attachment parameter domain**, conditional on the stated global minimum-source
premises and the adopted annulus/collar inputs. No blocker was found involving
disconnected private graphs, shared PPP vertices, branches, subdivisions or the
two possible positions of the inner boundary.

## Paper checks

The general identities in the frozen rank-three proof, Sections 2–3, apply to
arbitrary private cycle rank. For essential rank four they give
`h=3`, `p=a=M=0`, `c=1`, `delta(F)>=2`, and
`sum_x (d_F(x)-2)=6`. Every vertex of a PPP face has private degree at least
three: otherwise all its terminal neighbours occupy one remaining link interval,
and complete degree at least five forces a B/U switch and hence an M face.
The original complete-degree sum is `4r+13`; consequently `r<=13`, while
the adopted K<=13 result gives `r>=8`.

The union S of the three PPP triangles therefore has at most six vertices.
The following cluster cases are necessary, including vertex-only overlaps:

1. An edge-connected three-face cluster is a triangulated pentagon or K4.
   The K4 case has a vertex surrounded by three PPP faces, so its complete
   degree is three and contradicts the source degree condition.
2. For a diamond and a separate triangle, disjoint supports have seven vertices.
   One shared vertex has degree at least four, causing more than six excess.
   Two shared vertices without a shared edge can only be the diamond's two
   nonadjacent tips. The union then has five vertices and eight edges, already
   contributing six excess; the new triangle vertex still has private degree
   two and requires an additional edge. This also exceeds the budget.
3. Three clusters sharing no edges use at least six vertices. Equality requires
   shared vertices of degree at least four, again exceeding six excess.

The remaining pentagon fan has degrees `4,3,3,2,2`. Its two degree-two ears
must each acquire another private edge; this exhausts the total excess six.
All other private vertices consequently have degree two, and the fan's other
vertices have no unused private incidence. Connectedness therefore forces all
remaining private edges to form a single simple external ear-to-ear path.
A disjoint cycle, attached tree, extra branch or omitted subdivision cannot fit.

The two non-PPP faces are the B face and the U face. The fan's short-side apex
has private degree four and one or two consecutive terminal neighbours on that
side. The two long-side vertices each have private degree three and exactly two
consecutive terminal neighbours on their side. Both assignments of B/U to these
two sides are retained. The ears meet both terminal faces; ordinary path vertices
do too. Their permitted letters are respectively `O/B/U/D` and `B/U/D`.
With apex increment d in {0,1}, the word length is `r-3`, and the increments sum
to `(5-d,3)` before the patch contributes `(d,2)`.

All original edges are represented by private path/fan edges, terminal cycle
edges and these consecutive attachment intervals. The direction on both pin
cycles must be transported together. Independent choices of starting pins are
allowed; independently reversing one pin cycle is not an additional equivalence.
Inspection of the proposed producer's oriented faces and independent interval
construction found both B/U orientations present and no discrepancy in this rule.

## Independent finite corroboration

[triangle_and_count_check.py](triangle_and_count_check.py) imports no producer,
graph library or coloring routine. Its stored [results](triangle_and_count_results.json)
perform two small checks:

* All triples of distinct triangles on four through six used vertices, with at
  most two selected faces on each edge and
  `sum(max(d_S(v),3)-2)<=6`, give only K4 on four vertices or the fan degree
  sequence on five vertices. There are no candidates on six vertices.
  These labeled counts are corroboration of the paper cases, not source counts.
* The coefficients of `(1+x+y+xy)^2 (x+y+xy)^(r-5)` at
  `x^(5-d)y^3`, doubled for the two orientations, give
  `96,408,840,912,504,112` for r from eight to thirteen, totaling 2,872.

Both normal and `PYTHONHASHSEED=17` checks pass. The script does not establish
planar realizability or any full fiber identity; those belong to the audit's
oriented-face and complete-coloring validators.

## Adoption boundary

This essential theorem by itself gives
`F contains an essential cycle => rho(F)>=5` under the complete minimum-source
contract. General `rho(F)>=5` additionally requires the separate
`2026-10-13-w5-rank4-contractible-acd2b1b` audit. Its inputs are explicitly frozen
as untracked working-tree evidence in this audit's BASE, not treated as HEAD
authority. Parent replay and adoption of that audit are a separate necessary
step before combining the two exhaustive topological branches.

No E-ARC2 exclusion, general small representative, equality of R3/full fibers
between different graphs, or Lean theorem follows from this review. The complete
minimum-source hypotheses cannot be replaced by N2 or low-excess hypotheses.
