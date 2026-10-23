# Independent review: exterior stars and fixed B14 join

Reviewed source files:

- `workers/geometry/PROOF.md` (four private exterior vertices and final O ≥5 refinement).
- `workers/b14/FINDINGS.md` (endpoint, full M/N swaps and separator; wording
  corrections communicated to author).
- Existing authorities named in both files, especially predecessor cells,
  P/B13, methods `boundary_restrictions` and original full B14 component tables.

## Four exterior-private theorem: PASS

The inner/exterior common-neighbor barrier is sound: for nonedge pq and
strictly interior common neighbor t, any strictly exterior common neighbor v
would give an original C4 with both diagonals absent. The tv nonedge is a
consequence of the actual Jordan circle, not a new combinatorial assumption.

The dr,rT,Ts,sx outer third vertices u,a,b,c lie in F because each of those
edges has a known F-private endpoint with complete original star. Their
membership in K2/M2/N3 proves they are F-private, even where d might equal U.
The only equality possibilities u=a or b=c follow from the r/s barrier.
The low-degree exclusion of one equality in each L/R (both in O) uses complete
cyclic links of r/s, which are private. In the remaining L/R three-point
case, both T and s have only private original neighbors; the source-J proof
of that fact in the geometry note is valid. The subsequent x-link step uses
x's full private star, so it avoids all d/U frame issues. Fourth-private
conclusion passes for all 11 types and arbitrary outside size.

## O refinement: at least five exterior-private points: PASS

Independently checked the proposed exact-four contradiction. With only
u,a,b,c private exterior vertices, O barriers force T's exterior neighbors
exactly a,b. The full T5 star gives (a,b)=(M2,N3) or (N3,M2).

s has no boundary neighbors and no exterior u/a neighbor by the r/s barrier;
its full exterior link is T-b-c-x. Thus c=K2 in the first orientation and
c=N3 in the second.

In the second orientation, the original x-c edge beyond its face with s
forces another exterior private point exactly as in the earlier geometry
argument. The first orientation has a=M2,b=N3,c=K2. At r, only u,a and possibly
the fixed boundary U0 can occur in the exterior link: every other r-neighbor
is private, while b,c are forbidden by the r/s barrier. If u=K2, no proper
link from u to a can use only U0, since a∈M2 cannot neighbor U∈K0. Therefore
u=N3.

Use the **actual original edge d-u**, rather than treating d as F-private.
Its known exterior face is d-r-u. The other actual face has third point w;
u's full private original star guarantees w∈F even if d=U. Its colors are
1 or 2. Color1 gives w∈N (private); color2 gives w∈K2 (private). This face
and w lie strictly outside Γ. w cannot be a (M2/K0 forbidden edge), b (color3),
or c (d/x exterior-common-neighbor barrier), and differs from u. Thus it is
a fifth private exterior vertex. No F-boundary cyclic-link claim is needed.

This proves the O ≥5 refinement; it does not exclude O outright or assert
sharpness. The final geometry separator addendum initially inferred
M2∩E nonempty from d=U/e∈{V,Y} without requiring E to touch B14. This
would be false for rootless E; the author was asked to add E=D. The uniform
five-point proof above does not use that optional corollary.

## Fixed B14 join: PASS after wording corrections

All endpoint alternatives follow from full original K/B contacts and
rootless M/N, plus exact successor C contacts. The e=V,W=q prohibition uses
the stronger upstream full-star common-neighbor theorem, not ordinary
coloring alone. The rootless full N swap leaves the complete original02/13
induced graphs and literal B14 fixed; the known d-r-T-sΓ-x path becomes03.
Both allowed original03 rows separate U and q, so U/q attachments prohibit
either ear even for arbitrary Γ8 interior size.

The rootless full M swap, followed by the SAME complete K, still uses the
same unique necessary successor. The actual local12 path e-d-r-T-sΓ-x-h
therefore rules out h=c with d=U or e∈{V,Y}. These are conditional endpoint
exclusions, not exclusions of unlabelled eleven types. The stable graph
`ψ12 − M2` gives the stated separator; it does not assume that original
whole C/E paths survive the exchange. For j=2 all M2 are Γ-exterior.

Two wording corrections were identified and accepted by the B14 author:

1. The complete rooted D contacts are fixed; E may be rootless. Only when E
   meets B14 must E=D. The original early sentence giving D contacts to E
   was too strong and is now corrected.
2. Same F, literal boundary and cap relation are unchanged, and the full M
   exchange supplies a new proper complete witness. No claim is made that
   swapping a fixed reference M vertex set gives a bijection on every other
   complete coloring in a fibre.

## Finite dimensions and remaining scope

The parent checker dimensions are four tables `(target,original02 type)`;
original03=4/9 are both retained as a two-way gate within each table, not an
independent row factor. Thus 11×24×4=1056 raw local attachment rows and
116×4=464 rows after these necessary endpoint/ear filters are consistent.
If original03 were separately labelled there would instead be eight tables,
but that is not the parent's chosen certificate schema.

The independent `stars/orbit.py` writes 11×8=88 same-local-graph restrictions
for complete rootless M/N and SAME K exchanges and retains all six local
palette components. All are proper; every M/K row has the actual e/h12 path,
and the N/K e/h12 path exists exactly for O. This is an independent local
calibration, not a source realization, full-exterior enumeration or a new
source exclusion. All 11 all-private endpoint types still pass the fixed
B14 filter. General wrong-side and the eventual full 941 source exclusion
remain OPEN.
