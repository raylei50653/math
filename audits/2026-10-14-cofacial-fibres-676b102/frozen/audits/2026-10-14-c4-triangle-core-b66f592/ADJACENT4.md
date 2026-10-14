# Adjacent degree-four outer vertices: a single C4 mask and joint residual

Conditional paper lemma for the degree-three-b branch of [PROOF](PROOF.md).
No Four Colour Theorem is used. This does not close the remaining joint residual.

## Preconditions

Use B=(x,y,a,b,c) and original inner count k. Suppose d_G(b)=4, so the preceding reduction gives a simple 4-connected sphere triangulation T0 with designated facial triangles zxy and zpq. Its vertex count is k+3. Vertices p,q are distinct from x,y,z, adjacent to z and each other, and neither is adjacent to x or y. Its degrees satisfy z>=6, x,y,p,q>=4, all others>=5.

Assume additionally d_G(x)=d_G(y)=4. This is exactly d_T0(x)=d_T0(y)=4. Failure of the original target would mean that every complete T0 colouring has the same unordered colour pair on xy and pq.

## 1. The smaller C4 disk

Let xyr be the second face at edge xy. In cyclic order, the neighbourhoods are

`N(x)=(z,y,r,s)`, `N(y)=(z,x,r,t)`.

The vertices z,s,r,t are distinct. In particular, if s=t then sxy is a third triangle at edge xy, besides its two incident faces zxy and rxy, contradicting the absence of nonfacial triangles. Edge zr is absent: otherwise zxr would be nonfacial. Delete x,y and take

`Q=(z,s,r,t)`

as the outer boundary. This gives a C4 disk R. Vertices p,q remain strictly internal, because neither is adjacent to x or y. Edge st is absent as well: if present it would divide the Q disk into triangles zst,rst, at least one containing p or q, contrary to 4-connectivity of T0. Hence Q is induced.

R has k+1 vertices, four boundary vertices, and exactly k-3 inner vertices. It is therefore within the strict s<k contract of the source-relative C4 representative lemma. Its complete C4 support lies in

`{7,10,11,12,13,14,15}`,

with bit order **ABAB, ABAC, ABCB, ABCD**, exactly as in [the frozen degree report](frozen/audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md) section 3.

All R inner degrees are unchanged from T0. Only p,q may have degree four; every other R inner vertex has degree at least five. The boundary degree changes are z minus two, r minus two, s/t minus one.

## 2. Exact six-vertex cap table

For each fixed colouring of Q, reinsert x,y with exactly the original edges

`zx,sx,rx,xy,zy,ry,ty`.

The complete local extension table is:

| Q=(z,s,r,t) | all possible ordered (x,y) | unordered xy palettes |
|---|---|---|
| ABAB | (C,D), (D,C) | {C,D} |
| ABAC | (C,B), (C,D), (D,B) | {B,C}, {C,D}, {B,D} |
| ABCB | none | none |
| ABCD | (D,B) | {B,D} |

These are literal disjoint complete lifts of each same R colouring. No p,q recolouring is involved.

Because zpq is a triangle, in an ABAC row its pq palette is one of the three two-element subsets of {B,C,D}. Exactly one of the three cap extensions matches it, and the other two differ. Thus **any ABAC colouring of R immediately supplies two T0 lifts solving the original target**.

Therefore target failure requires the ABAC bit of R to be absent. Within the source-relative seven-mask list this leaves only masks 12 and 13.

## 3. Excluding mask 12 without 4CT

Since zr is absent, identify z and r across the exterior of R and suppress parallel edges, producing a loopless planar graph J with k vertices. This graph is colourable using only original source minimality:

Choose an outer edge vw of J. Add three new vertices along an exterior path of length four from v to w, retaining vw as the fifth edge of a new outer C5. The thin newly drawn face can be designated the outer face on the sphere, so all of J lies in the resulting disk. The new graph has k+3 total vertices and five boundary vertices, hence k-2<k inner vertices. By the global minimality of the original source, its relation belongs to K. The finite K catalogue contains no empty relation, so it has a complete colouring. Its restriction colours J.

Lift this J colouring to R, giving z=r. Thus R has ABAB or ABAC. Under target failure ABAC is absent, so ABAB must be present. Mask 12 has neither ABAB nor ABAC and is excluded.

We have proved the following exact conditional conclusion:

> If the original target fails and d_G(x)=d_G(y)=d_G(b)=4, the smaller induced C4 disk R has **exactly mask 13**, namely ABAB, ABCB, ABCD and no ABAC.

This uses source-relative colourability of one graph with k vertices. It makes no universal planar colourability assertion.

## 4. The retained joint obligation

Mask 13 alone does not retain p,q colours. Target failure adds the following two same-colouring conditions:

- For every complete R colouring with Q=(A,B,A,B), `{f(p),f(q)}={C,D}`.
- For every complete R colouring with Q=(A,B,C,D), `{f(p),f(q)}={B,D}`.

The ABCB fibres are nonempty because the mask is 13, but none lift through this cap, so they impose no immediate palette condition.

Conversely, mask 13 together with these two universal joint conditions makes every complete cap lift preserve equality of the xy and pq palettes. Thus the conjunction is the **exact residual**, not merely a necessary numerical test.

The seven ordinary C4 masks cannot by themselves test this residual. The finite checker includes an abstract relation with outer support 13, proper triangle zpq, and exactly the two prescribed bad palettes; all cap lifts then fail to change the palette. This is an information-loss negative control only. It is not asserted to be realizable by a planar graph or by the required degree profile.

The required interface is the joint colouring relation on `(z,s,r,t,p,q)`, or an equivalent record preserving the actual p,q colours in each full R fibre. Replacing R by a representative that preserves only its four outer pins does not justify either existence or absence of the original target.

## 5. Finite control and bounds

Run:

`python3 -B audits/2026-10-14-c4-triangle-core-b66f592/controls/check_cap.py --check`

The checker directly tests the eleven edges of the six-vertex C4 cap against all sixteen x,y assignments for each of the four fixed outer assignments. It independently compares the resulting ordered lifts with the table, checks all six ordered p,q choices forming a triangle with z, confirms exactly two successful cap lifts for each ABAC choice, filters the seven masks to 12/13 and then 13, and retains the abstract-joint negative control.

Certificate: [cap.json](controls/cap.json).

Status: finite controls PASS; actual target source controls 0. No source realizability, arbitrary joint-interface representative theorem, Lean theorem, or unbounded extension is claimed.
