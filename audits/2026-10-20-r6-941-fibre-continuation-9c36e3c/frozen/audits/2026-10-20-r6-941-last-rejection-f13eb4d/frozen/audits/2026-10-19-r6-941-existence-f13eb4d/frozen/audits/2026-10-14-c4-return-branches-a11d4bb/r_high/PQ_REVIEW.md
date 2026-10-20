# Independent review of the p/q paper argument

Reviewed [pq/PROOF](../pq/PROOF.md) at frozen BASE a11d4bb. This review
does not edit that proof. The mathematical steps reviewed below hold
under its stated global minimum-source no4ct contract; no whole-source
realization or general p/q exclusion follows.

1. **Single-p deletion and exact support14.** Original p degree5 becomes
   degree4 in T0 because b is deleted; x,y are not neighbours and merging
   a,c does not duplicate a p edge. Its link C4 is induced by T0 triangle
   faciality. The double p lift in ABAB requires the same unchanged xy
   palette to equal BC and BD, so ABAB is genuinely empty. The two
   opposite exterior quotients are loopless simple planar graphs after
   parallel suppression. H has k+2 vertices, quotient k+1, and attaching
   a length-four path adds exactly three vertices. The resulting C5 has
   k+4 total vertices and k-1 interiors, so original minimality applies.
   The retained triangle zxy ensures an edge exists. For precision,
   select an edge incident with a chosen exterior face and draw the new
   path in that face; then choose the empty side of the new cycle as
   exterior. No theorem about arbitrary planar graph colourability is
   used. The quotient existence arguments independently supply the two
   diagonal fibres; their fibres are not multiplied or identified.

2. **The two full-fibre maps.** The AD ell switch in ABAC fixes the
   D-coloured xy endpoint because it is adjacent to z, and the following
   global C/D interchange is necessary. Its inverse uses the AC ell
   switch and the same global permutation. The BD m switch from ABCB
   protects the unordered xy palette because xy is an actual edge.
   The rainbow CD exclusion and the BC/BD connectivity split use only
   alternating endpoints on the literal C4 boundary, within one full
   colouring. The displayed bijections and rainbow disjoint split are
   sound; they do not supply an exclusion of mask14.

3. **Double-low p=q=5 and ell>=6.** The common second pq-face vertex ell
   is a literal original inner vertex. It differs from r,s,t: r has no
   p or q edge, s has no p edge, and t has no q edge. It differs from all
   original B vertices: x,y are not adjacent to p,q; b is deleted before
   naming this face; original a does not contact q and c does not contact
   p. More strongly ell has no B contact. Original b's complete degree4
   list excludes it; the complete x,y lists exclude it because it is
   not r,s,t; and the absent opposite p-link edge z-ell rules out both
   original a-ell and c-ell. Consequently it loses no edge in passing
   G to T0, and loses exactly p-ell,q-ell in K:
   `d_K(ell)=d_G(ell)-2`. This verifies the degree premise needed for the
   swapped return, independently of a count-only cap argument.

4. **Swapped return geometry.** Deleting p,q keeps both x,y strictly
   internal because neither is adjacent to either deleted vertex. A
   putative m-n chord of the exposed C4 leaves one of its two triangle
   sides containing x or y, contradicting T0 triangle faciality. If
   ell has original degree5 its K degree is3; deleting ell exposes the
   actual C4 L, with x,y still internal. The z-w diagonal is ruled out
   by the same triangle-side argument. The full all-ell-lifts table is
   exactly the original degree-three return configuration with xy as
   the protected edge. A complete K rainbow colouring forces w=A and
   supplies the nonempty L ABAC/BC fibre after one common colour
   permutation. L has no rainbow by the forbidden K diagonal lift.
   The return injection then contradicts its universal L ABAB/CD row.

Accepted paper conclusion: original p=q=5 forces original ell>=6.
The double-low branch with ell>=6, and each isolated p=5 or q=5 branch,
remain OPEN. This review is independent mathematical review; finite
certificate replay and source realizability are separate claims.
