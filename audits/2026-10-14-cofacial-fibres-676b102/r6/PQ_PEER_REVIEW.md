# Independent review: the low-p branch when original a has degree four

This review checks the proposed new source exclusion against the frozen
BASE `676b1024715f24a0d969fba90baab21b756406e2` source geometry,
JOINT_FIBRES, and low-p proof. It concerns the same original
`d_G(x)=d_G(y)=d_G(b)=4` contract. The conclusion is

`d_G(p)=5 => d_G(a)>=5`, and by reflection `d_G(q)=5 => d_G(c)>=5`.

The proposed proof passes the following critical checks.

1. The frozen p link is `(z,q,ell,m)` in T0, all four vertices distinct,
   with nonedges zell and qm. If a has original degree four, the source
   geometry gives tp and the facial triangle zpt. Thus t is the p-link
   neighbour immediately beside z opposite q, namely m. In particular
   ell cannot be t, since zt is an edge but zell is not.
2. In `D=R-p`, the original exterior face `Q=(z,s,r,t)` and the newly
   exposed face `P=(z,q,ell,t)` are actual simple faces. They share exactly
   edge zt. The apexes s,r,t,p,q are distinct; ell cannot equal s or r
   because ps and pr are forbidden. Deleting p does not erase Q or fuse
   these faces across zt, whose edge remains present.
3. Draw zr inside Q and qt inside P **before** doing either contraction.
   The arcs have disjoint interiors and distinct endpoints, even though
   the faces share zt. Contracting these two added edges preserves
   planarity. Both original pairs zr and qt are nonedges. Hence neither
   quotient class `{z,r}` or `{q,t}` contains an original edge; no loop
   arises, including after both contractions. Suppress parallel edges.
4. D has k vertices, the quotient has k-2, and zq survives as an edge
   between the two distinct classes. The face-side length-four path cap
   therefore has k+1 total vertices and k-4 interior vertices, strictly
   fewer than the original k. Original global minimum-source comparison
   gives a complete quotient colouring without 4CT. Pulling back yields
   one complete colouring of this same D satisfying both z=r and q=t.
5. Restore p with its exact four neighbours z,q,ell,t. Because q=t,
   those neighbours use at most three colours. Therefore at least one
   complete R lift exists. Its outer z=r relation is ABAB or ABAC;
   the latter is forbidden by the original mask13. Thus s=t=q. After
   one common global renaming the R boundary is ABAB with q=B. The
   universal ABAB condition says the pq palette is CD. This contradicts
   the actual q colour in that same complete R colouring.

This proves that `p=5,a=4` is impossible. The original boundary degree
lower bound is four, so p=5 forces a>=5. Reflecting all original names
`x<->y, a<->c, p<->q, s<->t` proves the stated q-side conclusion.

This is a joint quotient on a real common deletion graph. Its two arcs
occupy two actual distinct faces. It does not turn D into a single C4
disk or combine independent witnesses. The surviving cases p=5,a>=5
and q=5,c>=5 remain open, as do the desired full p,q>=6 theorem and any
general improvement of `K<=22`.
