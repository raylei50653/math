# Independent audit of the small-cap refinement

2026-10-12. This is an additional conditional paper result within Task A,
reviewed independently after `final-proof-review.md`. It strengthens the
earlier stopping point without using Task B, Task C's finite cap-pair closure,
or a new source enumeration.

**Verdict: PASS under the same frozen source premises.** Both M2-46 and
M2-55 can be excluded. The remaining possible contact types are M0, M1,
and M2E. This is a source-conditional conclusion; it does not establish the
separate `132^2` finite closure assertion requested by Task C.

## 1. Global minimality controls the size of each original cap

Let `P` be an actual simple C4 or C5 cap in the classification. Write `r` for
the number of its private vertices. Its full interface is exactly its named
boundary, since all of its private vertices and incident edges lie in its
original cap region. The fixed rest of the original source includes `v`.

For C4, the inherited theorem supplies a disk representative `P'` with the
same complete named boundary relation and at most three private vertices.
For C5, `P` has fewer interior vertices than the whole `G`, so global
minimality puts its relation in `K`; the inherited catalogue then supplies
such a representative with at most five private vertices.

The complete-interface replacement lemma embeds `P'` in the original cap and
preserves `Sigma(G)` after gluing to the unchanged exterior. Any parallel edge
copies can be simplified while keeping the original outer boundary. If `r'`
is the representative's private order, then the resulting source has

`k(H)=k(G)-r+r'`.

Because the resulting relation remains outside `K`, global minimum interior
order forbids `r'<r`. Therefore each **original** C4 cap has `r<=3`, and each
**original** C5 cap has `r<=5`. This is stronger than merely asserting the
existence of small representatives to use in a later twelve-bound estimate.
It does not require minimum edge order or edge-criticality.

## 2. A small triangulated cap with private degrees at least five

Let `P` be a triangulated disk with simple boundary length `p`, where
`p` is 4 or 5. Let `r<=5` be its private order. Every private vertex of `P`
has the same incident edges in `P` as it has in `G`, hence degree at least 5.
All cap regions in the classification satisfy this triangulation premise:
their boundaries consist of original edges, and all of the original faces
on the cap side are triangles.

Let `H` be the induced embedded graph on the `r` private vertices; let `h`
be its edge count; let `d` count chords with both endpoints on the cap
boundary. Euler's formula and triangular face counting give

`|E(P)|=3r+2p-3`.

Subtract the `p` boundary edges and the `d` boundary chords, and count each
private-private edge a second time, to obtain the exact identity

`sum_(u private) deg_P(u) = 3r+p-3+h-d`.             (1)

Assume now `2<=r<=5`. Every private vertex has at most `r-1<=4` private
neighbors, so it has at least one original cap-boundary neighbor. The open
drawing of an edge to such a neighbor avoids `H` and connects to a boundary
point in the unbounded component of the complement of `H`. Thus that open
edge lies in the unbounded face of `H`, and its private endpoint is incident
to that face. This holds for every private vertex, proving that `H` in its
actual embedding is outerplane.

This inference does not require `H` to be connected. The familiar simple
outerplanar bound `h<=2r-3` holds for a disconnected graph as well when
`r>=2`: connect its components by noncrossing edges in the outer face and
apply the connected bound (or apply the component bounds and count isolated
vertices separately). No embedding is being rearranged to avoid a hidden
interior vertex; the original boundary-neighbor edges prove that none is
hidden from the outer face in the first place.

Since `d>=0`, (1) now yields

`sum deg_P(u) <= 3r+p-3+(2r-3) = 5r+p-6 < 5r`,

because `p<=5`. This contradicts all `r` private degrees being at least 5.
Consequently `r>=2` is impossible.

For `r=1`, its unique private vertex can only have the `p` boundary neighbors.
It cannot have degree at least 5 when `p=4`. When `p=5`, it must be adjacent
to all five boundary pins, so the cap is the five-wheel; the edge count
leaves no additional boundary chord. Thus the precise conclusion is:

- C4, `r<=5`, private degrees at least 5: necessarily `r=0`.
- C5, `r<=5`, private degrees at least 5: necessarily `r=0` or `r=1`;
  the one-private-vertex case is the five-wheel.

The proof does not require a new separating-triangle argument and avoids
case classification of private K4 or W4 graphs.

## 3. Consequences for the original link classification

For M2-46, the original C4 cap has `r<=3` by Section 1, hence `r=0` by
Section 2. Its boundary is `(a,b,c,x)`, with `a,c` the two contacts,
`b` the original B-exclusive pin, and `x` the original L-exclusive pin.
The two possible quadrilateral diagonals are `ac` and `bx`. The former
is forbidden by inducedness of both original cycles. Triangulation therefore
requires `bx`. With no private cap vertex and with the wheel filling the
other side of the link, `x` then has exactly neighbors `a,c,b,v`, of degree
4, contrary to the frozen interior degree bound. Equivalently `b` would
have exactly neighbors `a,c,x`, of boundary degree 3. This excludes M2-46.
The same argument excludes an original C4 cap in M3S; that row was already
excluded in the earlier proof.

For M2-55, each original C5 cap has at most five private vertices by
Section 1, hence at most one by Section 2. The two caps partition all original
private vertices outside the fixed wheel skeleton. The retained original
interior vertices are exactly the three link-exclusive pins and `v`, so

`k(G)=4+r_P+r_Q<=4+1+1=6`.

This contradicts the frozen `k(G)>=13`. It is a bound on the **original**
conditional source, not the earlier `4+5+5=14` bound on a constructed source.
No finite claim about all ordered catalogue cap pairs has been assumed or
proved in this argument.

Combining these exclusions with the earlier M3P/M3S/M4/M5 exclusions gives:

**In the globally minimum-interior outside-K source, a degree-5 interior
vertex has zero, one, or two outer neighbors; in the two-neighbor case they
are adjacent on both original cycles and form the same original edge.**

The remaining geometries are the genuine annulus, the one-pin pinched
region, and the shared-edge C8 cap. Their marked relation/embedding bounds
remain open, as does the general catalogue conjecture. No actual 933/941
source was supplied or tested; that source predicate is `not triggered`.
