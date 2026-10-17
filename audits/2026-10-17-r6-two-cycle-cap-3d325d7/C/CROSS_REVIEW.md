# C cross-review of A: original cap–m contact exclusion

Frozen BASE: `3d325d7197aa05815c71bedc52c1b253d736c7bb`.
This is a separate review by the SEP-cycle worker of
[A/PROOF](../A/PROOF.md), checked against the frozen old cap, compatible
five-cycle and original degree authorities.

**Verdict: ACCEPT**, with the original-source and paper-only boundary
stated in A. No missing chord exclusion or endpoint exception was found.

## Independent checks

1. In the p,ell case, each u_i is a retained original vertex distinct
   from the original s,t and from boundary a,c: its actual Q5 rim avoids
   m,z except for the displayed z. Thus all asserted original C4/C5
   cycles have their displayed distinct vertices. The same observation
   handles the p,n case. Every claimed proper C5 contains original inner
   vertices and differs from the original boundary.
2. For the hypothetical mu1 contact in the p,ell case, the original
   s-side C4 has exactly the absent diagonals sq and cu1. The t-side C5
   has exactly the five absent chords tn,tell,aell,au1,nu1. The last
   three follow from the induced J p-link or induced Q5; original edges
   between these retained vertices would survive the quotient. Hence
   the use of the original induced-cap theorem is valid.
3. The other p,ell contact has C4 diagonals tn,au2. Its s-side C5 has
   exactly the absent chords sq,sell,cell,cu2,qu2. The p,n case likewise
   has t-side C4 diagonals tn,au1, and s-side C5 chords
   sq,sell,cell,cu1,qu1. These exhaust the possible chords rather than
   only selected sector incidences.
4. Each forced-star case is a **compatible** original ta or sc lift.
   The frozen C1.4 identifies the cap centre with literal alpha0 or
   beta0, respectively, and excludes alpha0=p or beta0=q in that
   compatible case. The crossed endpoint exceptions of C1.5 are never
   used. The stars are therefore distinct from all boundary vertices
   whose links are being closed.
5. In the first forced-star case the four actual n faces close the
   simple interior link circle `a-p-ell-alpha0-a`. They give the
   **complete** original degree four, which is contradictory. In the
   beta0 cases the actual faces close q's entire circle and c's entire
   interior boundary path, giving original q=c=5. This contradicts the
   precise adopted q=5 => c>=6 theorem. It does not rely on a stronger
   generic adjacent-degree prohibition.
6. The ordinary original n in the p,n case really has a, not z, as
   its last original neighbour. The proof keeps that distinction and
   only passes to nz after the original edge na is quotiented. The
   collision between this n and the present hub m is resolved explicitly.
7. The q-side table is the full literal image of every p-side case
   under `(x,y),(a,c),(p,q),(s,t),(v,w),(alpha0,beta0)`. Its four-degree
   private-link case and its p=a=5 cases use the correct reflected
   contradictions. This is a theorem under relabelled data of the same
   G, with the whole source relation transported; it assumes no graph
   automorphism and joins no independent complete-colouring witnesses.
8. Once (G) is established, a dual vertex on the m-face is a triangle
   containing m and hence is outside X. Adjacency to X must cross a rim
   edge uv and would make m adjacent to the two distinct endpoints u,v.
   The singleton intersection in (G) excludes this, proving the full
   m-face distance >=2. It does not establish component separation.

## Scope

No original v=5, matching oddness minimum, two-complete-cycle, or
reference-colouring premise entered these checks. The no4ct original
small-cap and full-source nonedge contracts are retained. Source
realization remains **not triggered**; the proof adds no finite source
coverage or Lean theorem. Matching repair and SEP existence remain
open where specified by the parent.
