# B: independent audit of the original nine-boundary full lifts

The original source geometry is separately bound by
`../SOURCE_G_INPUT.json`; the checker verifies its frozen byte size and SHA.
Reviewed C's `explore_full_source.py` (the script actually present), not a
nonexistent `explore_original_full.py`.

The nine retained boundary vertices are exactly
`(c,s,j,i,w,t,a,p,q)`. Restoring the deleted vertices has the full named
neighbour sets

| Restored vertex | Full original neighbours |
| --- | --- |
| v | r,w,i,j,s |
| r | x,y,t,w,v,s |
| x | y,c,r,s |
| y | x,a,r,t |
| b | a,c,p,q |

The original degree assumptions make these lists complete. The edges among
restored vertices are rv,rx,ry,xy and all four are present in the model.
The boundary edges of the actual nine-disk are retained, including cs,ta,
ap,pq,qc. Additional edges or private vertices of the retained disk are not
invented or deleted: the local table applies to each actual full colouring
of that entire disk. An abstract nine-row allowed by the table need not
have such a full colouring.

The independent `check_source_lifts.py` uses these explicit graph edges and
brute-forces **all 4^5 assignments** of v,r,x,y,b over each of the 820 proper
nine-boundary colour orbits. It does not import C's code or reproduce its
nested palette-exclusion traversal. The resulting complete lifts retain
the actual original boundary `(x,y,a,b,c)` and its mask bit. Each of the
three cases fixes one whole-source SigmaG in {932,933,941} throughout: every
lift of every actual retained full colouring must belong to that same SigmaG.

All 475 empty reconstruction fibres remain in each universal upper table.
They cannot be excluded merely because they have no original G lift.
The independently generated upper rows are exactly C's 607,659,716 rows,
respectively, with equality of the complete row lists, not just counts.
Over C's supplied final sets of 362,536,662 rows, the independent full-lift
unions give the original SigmaG and the quotient U support319 as reported.
For the U projection, a=c is imposed on the same retained colouring and
every legal v colour is used; original r/x/y/b existence is not falsely
required for an already valid U colouring.

Normal and seed17 checks pass. Removing an empty fibre, deleting one of a
row's original full five-vertex lifts, and deleting the original rv edge
are separately rejected; see `SOURCE_LIFTS_VERIFICATION.json`.

This review certifies the full local reconstruction, universal upper rows,
and the stated support calculations on the supplied survivors. It does
not independently certify C's Kempe fixed-point elimination algorithm,
nor does it treat any surviving abstract row as an actual source. No v5
exclusion follows from this review alone; complete source coverage remains
not triggered and full319 remains OPEN.
