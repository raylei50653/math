# Independent review of the rotated and p/q returns

Reviewed `rotation/PROOF.md`, `rotation/check_rotation.py`, `pq/PROOF.md`
and `pq/check.py` against the frozen original triangle reduction,
SOURCE_GEOMETRY, JOINT_FIBRES and R6_TRANSFER. Both final replay commands
passed in this isolated worktree. No mathematical correction is requested.

## Whole-source rotation

The exact necessary failure hypothesis is `y_i=y_(i+1)=0` for the two
endpoints of the oriented boundary edge. The fixed zxy triangle has two
disjoint target branches, with the opposite third boundary vertex coloured
as x or y. Each branch is exactly its corresponding singleton fibre after
the stated common colour renaming. Positivity in either branch defeats
the failure hypothesis; it cannot be ignored merely because three degrees
are four.

With boundary indices `(x,y,a,b,c)=(0,1,2,3,4)`, the extra usable cuts are:

| Cut | Required additional degree | Failure masks | Apex conclusion |
| --- | --- | --- | --- |
| ab, indices 2/3 | a=4 | 932,933 | p>=6; p=6 forces t,q>=6 |
| bc, indices 3/4 | c=4 | 932 | q>=6; q=6 forces p,s>=6 |

The 941 singleton at index 2 blocks ab; the 933 singleton at index 4
blocks bc. The ya and cx degree premises require a=c=4, contradicting
h>=3 in this fixed branch. Thus the published side scopes
`932/933 a4` and `932 c4` are exact. The current-head checker tests these
obstructions directly through the fixed triangle target.

For k<=27, G28 then forces q=5 in the ab case and p=5 in the bc case.
The transported degree-six frontier excludes p=6 or q=6 respectively,
giving p>=7 or q>=7. These are conditional restrictions and do not improve
the common k>=23 bound or prove low-degree exclusion.

## Original p/q degree-five branch

The single deletion takes an actual degree-four T0 vertex to an induced
link C4. ABAB has two p lifts with different pq palettes and unchanged
xy, so its entire fibre is empty. Both diagonal fibres have xy=BD and
become nonempty from two separately constructed source-colourable quotients.
The resulting exact support is mask14; the rainbow fibre has no p lift.

The stated rainbow full-fibre split is consistent. In the ABAC map, the
ell AD component avoids z and both xy endpoints, then one global C/D
permutation gives the xy=BC rainbow sector. Its inverse uses the ell AC
component and the same global permutation. In the ABCB map, the m BD
component preserves the edge xy's unordered palette and returns exactly
from the xy=BD rainbow sector. The exclusions of xy=CD and the forced
complementary connections use paths from the same complete colouring.
The maps are bijections on all vertices, not deductions from their counts.

For p=q=5, their common second-face vertex ell is an original inner vertex:
the only original B possibilities are removed b, identified a/c, or x/y,
and the last pair is adjacent to neither p nor q. It is none of r,s,t
by the original forbidden p/q edges. Hence its degree is unchanged on
passing to T0, and the double deletion loses exactly its two p/q edges.
The degree-three ell deletion is therefore legitimate when d_G(ell)=5.

Its last C4 is induced: a putative z-w edge divides it into two triangles,
at least one containing the retained internal x/y triangle vertices, which
contradicts T0 triangle faciality. The same-row two ell lifts in ABAB
force the missing colours C and D simultaneously, so xy=CD. A retained
rainbow K colouring forces w=A; deleting ell and using the common C/D
renaming gives a nonempty L ABAC/BC fibre. The original no-rainbow return
lemma then supplies the contradiction. The claimed conclusion
`p=q=5 ==> ell>=6` is supported; it does not exclude p=5, q=5 separately
or the double-low branch with ell>=6.

## Verification boundary

The rotation checker verifies colour transport and target positivity. The
p/q checker verifies all local lifts and one explicit full-colouring disk
control. The geometry, smaller-source colourability and arbitrary-size
Kempe proofs remain paper arguments. Their abstract controls are explicitly
not source realizations, and no Four Colour Theorem or universal planar
colourability is imported.
