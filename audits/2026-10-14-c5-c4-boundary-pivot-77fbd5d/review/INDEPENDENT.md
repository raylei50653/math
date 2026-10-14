# Independent review: C5 to C4 boundary pivot

This review independently derives the four-coordinate transfer and checks the
candidate contract. It does not import the primary checker or infer source
exclusion from a zero-target search. The direct C4 route covers all three
no4ct minimum-source branches, including 932.

## 1. Literal transfer and full fibres

Write the fixed original boundary as `B=(b0,b1,b2,b3,b4)`. Add a fresh vertex
`u` outside B, adjacent to all five boundary vertices, obtaining S. Delete
only `ub3`, obtaining H, and choose the merged quadrilateral
`Q=(u,b2,b3,b4)` as the outer face. The graph G, every original edge and
every original vertex remain present in H. The full H fibres are exactly
the original G colourings compatible with the chosen cap assignment.

Fix one literal Q assignment. All lifts through the added cap are obtained
by choosing the actual colours of b0 and b1; neither original side is
normalised independently. For colours A,B,C,D, the complete possibilities
are:

| Fixed Q | Possible `(b0,b1)` | Original complete-row counts |
| --- | --- | --- |
| ABAB | `(C,D),(D,C)` | `2 x24` |
| ABAC | `(B,C),(B,D),(D,C)` | `y3 + x02 + x14` |
| ABCB | `(C,D),(D,C)` | `y1 + y0` |
| ABCD | `(B,C),(B,D),(C,D)` | `y4 + y3 + y2` |

For example ABCB fixes `u=A,b2=B,b3=C,b4=B`. Both b0 and b1 avoid A
because they are adjacent to u, and both avoid B because of their original
boundary neighbours. Their original edge b0b1 then forces `(C,D)` or
`(D,C)`. The two original B assignments are `(C,D,B,C,B)` and
`(D,C,B,C,B)`, whose singleton positions are 1 and 0 respectively.

For each such literal cap lift, join **all** original G colourings with
that exact B assignment. These disjoint joins are precisely the complete H
fibre. This proves the count formula and the support formula, including
empty fibres, for an arbitrary G. The coefficient 2 in ABAB is necessary:
its two unused colours yield two distinct literal assignments on b0,b1.
Global S4 transport identifies their counts, not their full lifts.

The aligned three branches have singleton supports empty, `{4}`, and
`{2,4}`. Thus each rejects both `y0,y1`. H forbids ABCB for all three;
its exact four-bit mask in the displayed Q order is 3 for 932 and 11 for
933/941. This is a diagonal-forbidding condition, not merely a statement
that some unspecified boundary colouring fails.

## 2. Candidate contract

Use the already established no4ct global minimum contract: G is a simple
chordless-C5 near-triangulation, has no occupied triangle, has interior
minimum degree five and boundary minimum degree four. These are hypotheses
on the global minimum source, not on an arbitrary graph with the same mask.

Every triangle of S avoiding u is a facial triangle inherited from G.
Every triangle through u uses an adjacent pair on B, because B has no
chord, and is one of the five new faces. Hence all triangles of S bound
faces. Removing ub3 merges exactly the faces `ub2b3` and `ub3b4`.
All other faces remain triangular. Every triangle of H was a triangle of S
and still bounds its original face. The outer quadrilateral is simple and
induced: its diagonals are the removed ub3 and the absent boundary chord
b2b4.

H has `k+6` vertices. Its internal vertices are precisely the k original
interior vertices and b0,b1. The former keep their original degrees; the
latter have degrees `d_G(bi)+1 >= 5`. The only endpoints that lose an edge
are u and b3, which are external in H. Therefore H is a 4-candidate in the
exact definition at the beginning of Section 2 of the external paper.
Neither this construction nor this argument assumes S is 4-colourable.
The 932 branch is consequently included.

## 3. External statement and the size quantifier

Primary source: Dvorak, Lidicky and Mohar, *On a conjecture concerning
4-coloring of graphs with one crossing*, arXiv:2504.08327v2 (14 April 2025),
[Section 2 and Table 1](https://arxiv.org/html/2504.08327v2#S2).

The required external fact is the **direct** exhaustive 4-candidate result:
through 28 vertices, no diagonal-forbidding candidate occurs except the
four-vertex diamond. We use this direct result rather than deriving a
27-vertex diagonal bound from the rainbow bound via Theorem 11. The paper
reports an independent implementation cross-check only through 25 vertices;
the larger range remains the reported main computational result.

The local bridge does not invoke 4CT, the general one-crossing conjecture,
Lemma 7, Theorem 10's equivalences, or the paper's general Corollary 17.
External completeness of candidate generation and the reported colouring
computation are separate trusted inputs. This review did not rerun the
external billion-graph enumeration.

If any source with at most 22 internal vertices lay outside K, choose a
source with globally least internal count, then greatest edge count. Its
count k is at most 22, and the no4ct classification supplies one of the
three aligned branches. The construction above gives a diagonal-forbidding
4-candidate on `k+6 <= 28` vertices. It is not the four-vertex diamond
(already `k >= 16`), a contradiction to the external finite result.
Therefore the new conclusion is `K_{<=22}=K_{<=5}`, subject to the stated
external trust. It is not a claim that arbitrary 933/941 sources satisfy
the minimum-source degree contract, nor an exclusion of all sizes.
General 932/933/941 and `K_infinity=K_{<=5}` remain OPEN.

## 4. Independent finite checks

`check_independent.py` uses only Python's standard library and fixed
literal edge sets. It does not import any repository checker. It stores
all cap assignments and complete positive-control fibres in [`result.json.gz`](result.json.gz), using deterministic gzip (`mtime=0`).
The checker decompresses and compares the complete content and also checks
the deterministic compressed bytes; all full lifts remain present.

- Four count rows independently recomputed from all 4^6 literal cap
  assignments; five boundary rotations checked with simultaneous column
  transport. Each rotation has 84 complete Q fibres and 216 literal cap
  lifts, for 1,080 stored lifts.
- Every one of the 1,024 possible complete B masks is checked against all
  84 literal Q assignments in each rotation: 430,080 support checks.
- The five-wheel is a scope and empty-fibre control, whose new internal
  vertices b0,b1 have degree four, too low for the candidate theorem.
  Its G mask is 91 (all T3 and no T4), and H counts are `[0,1,2,3]`.
  All 144 full H lifts are retained, as are the 120 empty original T4
  assignment fibres and the 12 empty ABAB assignment fibres of H.
- An independently constructed icosahedron with one degree-five root
  deleted is a positive source control. Its ten G counts are all two.
  Its H is the 12-vertex 4-candidate obtained by deleting an icosahedron
  edge; the internal minimum degree is five and H counts are `[4,6,4,6]`.
  All 432 full H lifts equal the literal cap joins of the complete G fibres.
- A negative control deletes the original added spoke ub0 as well. An
  actual cap lift from an accepted 941 row then reaches ABCB, detecting
  that the specified four-spoke cap is essential.

The actual positive sources have complete masks 91 and 1023; the three
target sources are **not triggered** in these controls. The general exclusion
comes from the paper argument plus the external exhaustive domain, not
from this zero count. No new Lean theorem is claimed.

Replay without overwriting the stored result:

```sh
python3 -B audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/review/check_independent.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/review/check_independent.py --check
```

## 5. Additional review of the initial one-crossing idea

For the 933-only initial construction, S plus the edge b1b3 has a drawing
with just one crossing, with ub2. Its new common-neighbour triangles are
exactly `u b1 b3` and `b1 b2 b3`: another original interior common neighbour
would be a forbidden two-edge crosscut between nonadjacent B vertices.
The external paper defines a separating triangle graph-theoretically by
vertex deletion. Since S is a sphere triangulation with no separating
triangle, it is 4-connected, and adding an edge preserves that property.
Thus crossing an edge of a triangle is not itself a separating-triangle
objection. Nevertheless the direct diagonal-forbidding C4 construction in
Sections 1–3 is the useful final route: it covers all three branches with
one formula and avoids importing the one-crossing equivalence machinery.
