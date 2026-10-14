# Independent review: the original r-degree-six frontier

2026-10-14. Source authority is the frozen no4ct minimum-source contract in
[INPUTS](../INPUTS.json). This review checks the first r-deletion transfer,
its empty-fibre semantics, the additional source geometry, and the
subsequent t-degree-five exclusion. Reflection supplies the s case.

## 1. First transfer and zero r lifts

Suppose the original r has degree six, with original cyclic neighbour order
`(x,y,t,w,v,s)`. Deleting r from R exposes the C5 boundary
`(z,s,v,w,t)`. The original p,q remain internal and retain triangle zpq.
For every complete colouring of this disk, **every** colour outside
`{f(s),f(v),f(w),f(t)}` must restore an admissible R colouring. If these
four neighbours use all four colours, there are zero r lifts; the
universal requirement is then true. Such a colouring of the smaller disk
must not be discarded.

I independently enumerated the actual old x,y cap edges, rather than
copying the degree4 checker's old joint-relation predicate. The only extra
input is the frozen actual-source ABCB missing-colour theorem. This gives
exactly the same 624 labelled joint assignments, 26 global-colour orbits,
upper outer mask 319, and catalogue submasks `271,314,319`.
Precisely 288 accepted labelled rows have zero r lifts. They occur over
the canonical outer words ABACD and ABCAD. All are retained.

The first-stage checker is a necessary joint-relation screen. It does not
establish that a mask-271/314/319 source exists, that all compatible
abstract rows occur in one graph, or that their full-fibre counts agree.
The ordinary smaller C5 relation is in K by original global minimality;
this does not license replacing its internally marked p,q by a witness
which only preserves the five outer pins.

The complementary-pair closure in `degree4/check_transfer.py` also has a
valid necessary interpretation: mandatory two-colour edges force their
endpoints into the same terminal component; distinct components on the
actual outer C5 cannot interlace; independently switching any subset of
components in two complementary colour pairs gives actual proper
colourings. Choosing a separate compatible partition for each pairing is
an overapproximation, which is safe for exclusions. Fixed-point survival
does not prove joint source realizability. The initial transfer certificate
passed its own `--check` replay in this review.

## 2. Four further original-edge facts

Vertices v,w have no original B contacts. They are distinct from p,q by
the already proved absence of rp,rq. Their contacts with x,y,b are
excluded by those vertices' exact degree-four neighbourhoods. A contact
with a would give the original chordless C4 `(a,y,r,v)` or `(a,y,r,w)`;
both diagonals are absent. A contact with c is excluded by the reflected
C4 through x. Such a C4 cannot bound an empty triangulated quadrangle,
contrary to the frozen original-C4 theorem.

The link of r has no nonconsecutive chord, because such a chord and r
would give a nonfacial original triangle. In particular sw and tv are
absent. The following sharpen the p,q attachment information:

`pv, qw are absent;`

`pw exists iff d_G(a)=4 and d_G(t)=5;`

`qv exists iff d_G(c)=4 and d_G(s)=5.`

For pv, the proper original C5 `(a,y,r,v,p)` would have both t,w in its
bounded side. The direction of that side is fixed at the original edge
ay, and the r rotation places both t,w in that sector. This contradicts
the original proper-C5 theorem (at most one private vertex). For qw use
the reflected proper C5 `(c,x,r,w,q)`, which contains s,v.

If pw exists, `(a,y,r,w,p)` has t in its bounded side. That proper C5 is
therefore exactly the link of a singleton W5 centre t. Consequently
`N_G(t)={a,y,r,w,p}` and `d_G(t)=5`, while its edge tp forces `d_G(a)=4`
by the frozen source geometry. Conversely a-degree-four supplies tp;
t-degree-five then makes those five displayed vertices its exact
neighbourhood. Their facial cyclic order forces wp. Reflection proves
the qv equivalence.

These arguments concern original G cycles and their original bounded
sides, avoiding the exceptional large C5s that can arise in transformed H.

## 3. General original t-degree-five deletion is legal

Assume now `d_G(t)=5`, without assuming the degree of a. Besides y,a,r,w,
let h be the fifth original neighbour of t. In the first smaller C5 disk
U, the exact neighbourhood of t is `{z,w,h}`. Here h is distinct from
z,w by simplicity, from s by the absence of st, from v because tv is a
nonconsecutive r-link chord, and from q by the frozen absence of tq.
The one genuine identification is `h=p`, equivalent to the edge tp and
therefore to `d_G(a)=4`.

Deleting t exposes the simple C5 `(z,s,v,w,h)` of V. Its total size is
`k-1` and its private interior size is `k-6<k`, so the complete outer
relation belongs to K. When h=p, p is promoted to the boundary and q
stays internal. When h differs from p, both p and q stay internal.
The original triangle zpq is retained in both cases. Possible boundary
chords would be allowed in the legal-source contract; no inducedness
assumption is needed to apply minimality or the Jordan arguments below.

For completeness hv is absent: h is not one of the six r neighbours,
so rh is absent; the original C4 `(r,t,h,v)` also lacks diagonal tv,
contradicting the original empty-C4 theorem if hv existed. This extra
absence is not used in the colouring screen.

Restore t in **all** colours outside `{z,w,h}`, then restore r in **all**
colours outside `{s,v,w,t}`. Empty second-stage lift sets remain admitted.
The direct cap-edge implementation in [check_r6_review.py](check_r6_review.py)
independently gives:

| Case | Upper outer mask | Catalogue submasks |
| --- | ---: | --- |
| h=p, retain q | 542 | none |
| h distinct from p,q, retain both | 575 | 564,567,572,575 |

Thus the h=p case is excluded already by its complete outer support.

## 4. Two same-colouring Kempe steps exclude the general case

For h distinct from p,q, the independent all-lift table is:

| V boundary `(z,s,v,w,h)` | Allowed unordered pq palettes |
| --- | --- |
| ABABC | BD |
| ABACB | BC,BD,CD |
| ABACD | BC,CD |
| ABCAB | BC |
| ABCAC | BC,CD |
| ABCAD | BC |
| ABCBC, ABCBD, ABCDB | none |
| ABCDC | CD |

**First eliminate ABCAC/CD.** Suppose a complete V colouring has boundary
`(A,B,C,A,C)` and pq palette CD. Vertices v,h must be connected in CD:
otherwise switching the CD component of v changes the boundary to
`(A,B,D,A,C)` and preserves the unordered pq palette (pq is an actual
CD edge). Under the common C/D interchange this is an ABCAD/CD row,
forbidden by the table. Also z,w must be connected in AB: otherwise
switching the AB component of w gives the forbidden boundary ABCBC.
An AB z-w path and a CD v-h path have alternating endpoints on the
actual C5 boundary, a contradiction.

**Then eliminate ABCDC/CD.** Suppose the boundary is `(A,B,C,D,C)` with
pq palette CD. The edge sv connects s,v in BC. Vertex h must be in that
same BC component; otherwise switching its BC component gives forbidden
ABCDB. Jordan separation consequently disconnects z,w in AD. Switch
the AD component of w, producing boundary ABCAC. The D-coloured endpoint
of pq is adjacent to z=A and so lies in z's AD component, outside the
switch; the C-coloured endpoint is unaffected. The resulting palette
is still CD, contradicting the preceding paragraph.

Both arguments switch actual maximal components of one actual full
colouring and preserve a single colour frame. They do not rely on the
abstract terminal-partition fixed point, counts, or Kempe graph
connectivity. The independently replayed fixed point gives the same
exclusion, but is not needed in this paper proof.

Deleting the ABCDC bit from outer mask 575 leaves mask 63. The 132-item
catalogue contains **no** submask of 63. This contradicts minimality for
V and finishes the general h case. Therefore the live source implication
is

`d_G(r)=6 => d_G(s),d_G(t)>=6`

under the original x,y,b-degree-four branch. In particular the pw and
qv edge cases of section 2 are now impossible in the surviving r6 branch.
The result does not exclude r6 itself or any higher-r branch.

## 5. Sharper review of the r5 return proof

The updated [fibre proof](../fibre/PROOF.md) correctly removes any need
for a second use of the relative C4 catalogue in the r5 argument. A
rainbow R' row would restore the unique r=A and yield forbidden R ABAC.
An existing R ABCD full colouring forces v=A; restriction and a common
C/D swap give the required nonempty R' ABAC/BC fibre. Finally its ABAB
fibre has two r lifts whose compulsory missing colours force the same
unchanged pq palette CD. These are sufficient for the stated return
injection contradiction. The earlier independent review's route through
mask7 remains valid but has an unnecessary classification dependency.

## 6. Validation boundary

Run `python3 -B audits/2026-10-14-c4-c5-recursion-fdd3e22/degree3/check_r6_review.py --check`.
The [certificate](r6-certificate.json) records all three independent
screens, the retained zero-r-lift count, and the catalogue submask checks.
The two Kempe contradictions and original graph surgery are proved above;
the checker does not claim to verify embeddings or enumerate target
sources. No new source realization or Lean theorem is claimed.
