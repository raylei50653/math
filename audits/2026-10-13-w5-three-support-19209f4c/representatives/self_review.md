# Equality gadget audit and provenance

This is a second paper/code audit by the construction author, **not** an
independent-authorship review. The independent reviews in this directory are
those of the other authors' W3 and conditional reports.

The exact lower bound survives the following checks:

- The graph uses all ten original distinct pins and exactly two private
  vertices. Its B and U induced cycles are unchanged. The given eight facial
  walks certify the annulus directly; a repeated u0 in one annular face is a
  facial walk through a cutvertex, not an identification or missing pin.
- The triangle b1,x,y has two hubs b0,u0. Both hubs must take its fourth colour;
  every proper pin assignment with b0=u0 has exactly two private extensions.
  This proves full support, including the restricted three-colour support.
- The r<=1 obstruction uses only edges which hold on **all** target cells.
  The fourteen permitted pin edges are exhaustive. The stated false-positive
  assignment satisfies all fourteen and uses only three colours across all
  ten pins. Every optional private vertex can therefore take the fourth
  colour regardless of its neighbour set. No topological assumption is used
  in this lower bound.
- Both directions refer to one representative graph. No lower bound is
  claimed for a union of branches accepting separate portions of the target.
- The five face insertions preserve all pin assignments and give unique
  reverse extensions. In the control, r=7 compresses to r=2 and the restored
  wheel's internal count decreases from thirteen to eight. Complete H and G
  lifts and literal maps are stored, not inferred from outer Sigma bits.

There is no provenance upgrade: the construction is synthetic, is not from
933/941, has occupied separating triangles and low-degree vertices, and cannot
be the stipulated minimum source. The paper labels this throughout. Its exact
minimum r=2 is a restriction on a universal class of annulus representatives,
not a proof that all minimum sources have a representative or need at least
two private vertices. It leaves r=2 through r=6 open in the general problem.

The final checker passes normally and at PYTHONHASHSEED=17. A corrupted copy
is rejected and all original evidence hashes are unchanged; the reproducible
record is `review_checks.json`.
