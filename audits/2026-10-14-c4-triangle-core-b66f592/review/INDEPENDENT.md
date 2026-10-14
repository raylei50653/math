# Independent paper review: opposite identification and the remaining marked vertex

2026-10-14. Reviewer c4_theory. This review rederived the assertions from the original G contract independently; it did not infer them from finite examples. Status: PASS for the precise statements below; no source exclusion is claimed.

## Exact names

Original B=(x,y,a,b,c)=(b0,b1,b2,b3,b4). H adds u adjacent to x,y,a,c and has outer Q=(u,a,b,c). Identify a=c=z in that outer face, simplify duplicate edges, and delete u. Call the result T and choose facial zxy as its outer triangle. Original source hypotheses are the full no4ct global-minimum contract, including the proved proper-C5 empty/W5 theorem and the fact that every original interior vertex has at most two B neighbours, which must be consecutive.

## 1. Topology and degrees

The only common neighbours of a and c in H are u and b: any original interior common neighbour violates the nonadjacent B contact theorem; x,y cannot be common neighbours because B is induced. Thus the quotient introduces no loops and exactly two duplicate edge pairs, zu and zb. They bound the two empty digons obtained by pinching the original outer Q along a=c, so simplification creates a sphere triangulation J. In J, u has precisely the three neighbours z,x,y, which already span a triangle. Removing u leaves the simple sphere triangulation T. All original triangular faces not incident to a or c remain facial; those incident to a or c retain their local sectors under identification.

Degrees are exact:

- d_T(b)=d_G(b)-1≥3.
- d_T(x)=d_G(x)≥4 and d_T(y)=d_G(y)≥4.
- d_T(z)=d_G(a)+d_G(c)-1≥7.
- Every other vertex is an original interior vertex and has unchanged degree≥5.

T has |V(T)|=k+4, outer triangle zxy and k+1 vertices inside it. It is not a smaller-k C5 source and has no automatic K132 replacement.

## 2. All separating triangles are classified

A T triangle avoiding z comes from an original G triangle, hence stays facial. A triangle zrs whose two z-edges both come from the same endpoint a or c comes from an original G facial triangle and stays facial. If r or s equals b, select its preimage endpoint to match the other edge; it is again such an inherited facial triangle.

The only remaining type has r,s distinct from b, with ar and cs original edges and rs an original edge. If r=y,s=x, it is the designated outer facial triangle zxy. Otherwise r,s are original interior vertices: y is adjacent to a but cannot meet an interior neighbour of c because that neighbour would then meet nonadjacent B points y,c; similarly x cannot meet an interior neighbour of a. These prohibitions also follow by the original C4 cap lemma. Therefore

D=a-r-s-c-b-a

is a proper original C5. Its cap along the original boundary arc a-b-c contains the whole G-interior sector at b. The proper-C5 theorem says the cap is empty or a five-wheel. A five-wheel gives d_G(b)=3 (neighbours a,c and its centre), impossible. In the empty cap, d_G(b)≥4 forces both br and bs, so d_G(b)=4 and {a,c,r,s}=N_G(b).

Consequently the only possible separating triangle of T is zrs=N_T(b), it exists precisely when d_T(b)=3, and its small side consists exactly of b. If d_T(b)≥4, no separating triangle exists and T is 4-connected. If d_T(b)=3, deleting b makes zrs facial and creates no edges or new triangles, leaving a 4-connected sphere triangulation T0. The order is far above four under the actual source bounds, so the usual small-order exception in the equivalence is absent.

The proof must explicitly exempt outer zxy. A generic statement that every mixed zrs comes from a *proper* C5 would incorrectly apply the s<k rule to B itself.

## 3. The two marked facial triangles in the degree-three branch

Write N_T(b)={z,p,q}. Then T0 has two facial triangles zxy and zpq. Their four non-z vertices are pairwise distinct: x,y are original B points and p,q original interior points.

There are no cross edges xp,xq,yp,yq. Indeed p and q are precisely the two original interior neighbours in the four-vertex link of b; after orientation, p meets a,b and q meets b,c. Each already has two consecutive original B contacts, so any contact to x or y violates the at-most-two-consecutive-contact theorem.

After deleting b, degrees satisfy d_T0(z)≥6, d_T0(x),d_T0(y),d_T0(p),d_T0(q)≥4, and all remaining vertices have degree≥5. The no-cross-edge conclusion is an additional valid structural constraint for the reduced target.

## 4. Full fibre mapping and palette interpretation

Use the fixed literal frame A,B,C,D and colour outer zxy=(B,C,D). Every T colouring has a unique lift to J, since u is forced to A, then a=c=z lifts uniquely to H. In T the marked b cannot be B. A target H colouring with Q=(A,B,C,B) has (x,y)=(C,D) or (D,C). The first corresponds to T with b=C; the second is converted to zxy=(B,C,D), b=D by one global swap C↔D on the whole colouring. This is a disjoint-union bijection on complete lifts, including empty fibres.

In original G notation the individual fixed fibres are:

- b=A: original boundary (C,D,B,A,B), i.e. x24, count c.
- b=C: original boundary (C,D,B,C,B), singleton y=b1, count y1.
- b=D: original boundary (C,D,B,D,B), singleton x=b0, count y0.

Thus n_H(ABCB)=|F_T(zxy=(B,C,D),b=C)|+|F_T(zxy=(B,C,D),b=D)|=y1+y0. This preserves all named vertices of T and the explicit global colour action; it is not a marginal statement.

When d_T(b)=3, every T0 colouring extends uniquely over b, because z,p,q form a rainbow triangle. For fixed zxy=(B,C,D), b=A exactly when triangle zpq uses palette {B,C,D}; b=C or D exactly when its palette differs. Hence the source target y0=y1=0 is equivalent to every complete T0 colouring having the same palette on its two marked triangles (provided the full literal fixed-outer-triangle frame is used). A target extension is exactly one actual full colouring with different palettes.

Nonemptiness in the source is supplied by c=x24>0, not by invoking 4CT. In arbitrary T/T0 graphs, a universal palette equality without this existence premise could be vacuous.

## 5. Limits

The reduction is an exact reformulation with stronger proven topology, not an unconditional recolouring theorem. The two cases, b degree≥4 in 4-connected T and palette locking in 4-connected T0, remain OPEN. Generic 4-connectedness cannot be silently substituted for the full degree/contact contract. The structural lemmas did not rely on the external one-crossing conjecture, its 4CT-dependent equivalences, or any finite no-hit evidence.

## 6. Review of the delivered broader S6 proof

I subsequently read [PROOF](../PROOF.md) in full. Its §4 proves the same separating-triangle classification directly from the stronger sphere hypotheses rather than using the source proper-C5/contact lemmas. The three endpoint cases are complete. In the one-endpoint cases, the alleged singleton x/y or b has a forbidden original B chord among its five possible neighbours, so minimum degree five gives the stated contradiction. The distinction between (v,w)=(y,x) and a proper mixed path is handled explicitly. I found no gap in §§1–5.


## 7. Final checker review and repair

The initial structure checker omitted the T0 no-cross-edge assertion and did not require a single oriented link at each vertex. Both were added in v2. The retained pinched-two-icosahedra control passes the old face/dart/Euler checks but is rejected by v2 with `vertex link is one cycle`. This repairs validation scope; it does not change the paper theorem. The final full v2 normal and seed17 replays both confirm 10,895 rooted openings, including the no-cross-edge statement.

## 8. Adjacent degree-four refinement

Independent review PASS for [ADJACENT4](../ADJACENT4.md). The cap counts in the literal ABAB/ABAC/ABCB/ABCD order are (2,3,0,1). The ABAC lifts have three palettes while p,q stay fixed in one full R colouring. The proof explicitly establishes s!=t, absent zr, and p,q strictly inside R. The source-relative sizes k-3 and k-2 are strictly below the original k; the planar quotient is coloured via K nonemptiness, without 4CT. The result is R=13 plus the retained joint conditions, not an exclusion of mask13 or a representative preserving only the four outer pins.
