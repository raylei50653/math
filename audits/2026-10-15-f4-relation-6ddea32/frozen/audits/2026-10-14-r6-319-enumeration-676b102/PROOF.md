# Complete bounded coverage of the named degree-six branch

The machine outcome and completed sizes are recorded in REPORT.md, separately
from the coverage argument below. This is not an arbitrary-size theorem.

## 1. Frozen source contract

Use the actual current-worktree inputs sealed in INPUTS.json at Git BASE
676b1024715f24a0d969fba90baab21b756406e2, including the uncommitted cofacial
supplement. G is a finite simple disk with ordered original induced boundary
B=(x,y,a,b,c), globally minimum interior order k among complete C5 relations
outside K132, and then maximum edge count. The inherited normal form gives
triangular inner faces, boundary degree at least four, interior degree at
least five, and the source small-cycle restrictions. Assume

    d_G(x)=d_G(y)=d_G(b)=4,  d_G(r)=6.

The original boundary-edge apices, in boundary order, are (r,t,p,q,s).
The frozen degree-six transfer proves d_G(s),d_G(t)>=6, the original r link
(x,y,t,w,v,s), and the induced C5 C=(z,s,v,w,t) after the prescribed quotient
and deletions. The original z-p-q triangle is retained, and p,q are interior.
The seven pins are literal, distinct original vertices except that z is the
single identified class {a,c}. The complete all-r-lifts table has upper
outer mask319; the cofacial supplement strengthens the outer relation to
exactly319. In particular, the outer row ABCBC (bit6) has an empty fibre.

This audit uses the source theorem that h=sum_B(d_G-4)>=3. It does not use
the stronger external high-p,q bound to prune candidates, and does not
filter on a selected global G coloring, arbitrary Kempe connectivity, or a
representative graph with the same boundary projection.

## 2. Spheres, roots and frames

Add a new vertex u in the actual exterior of G, adjacent to all five
original boundary vertices. The result S is a simple sphere triangulation
of order n=k+6 with minimum degree at least five; d_S(u)=5. Original interior
degrees are unchanged, and d_S(v)=d_G(v)+1 on B.

The frozen plantri 5.8 minimum-five construction supplies all embedded
isomorphism classes at order n. Only its FILTER output hook is changed:
the generation recursion is unmodified. In every supplied sphere, inspect
every degree-five vertex u and all five starts in both directions of its
actual cyclic neighbor list. Every source embedding therefore maps to an
inspected sphere, root and entire ordered frame. A whole-graph reflection is
covered by the opposite direction; named pieces are never normalized
independently. Automorphism-equivalent frames are deliberately retained.

The imported construction/completeness trust is the same as the frozen
K15 PROOF.md: Brinkmann--McKay's minimum-five generation theorem and the
local C implementation. No new independent generator or Lean proof is claimed.
Split runs use every residue 0,...,m-1 for the same denominator. Their summed
unfiltered FILTER invocation count must equal the documented full sphere
count; incomplete or failed partitions do not produce a complete summary.

## 3. Output-only necessary filters

Each counter below records survivors of the preceding stage. The root count
counts all five-degree roots; frame counters begin with all ten directions
per root and retain their literal identities.

| Counter | Predicate | Frozen authority / reason |
| --- | --- | --- |
| frames_degree444 | S-degrees of x,y,b all five | Exact branch hypothesis |
| induced_boundary | B has exactly its cycle edges | Source normal form |
| unique_apices | Each boundary edge has one common interior neighbor, the five apices are distinct and each meets precisely its two named boundary endpoints | Original facial apices and absence of nonfacial source triangles; SOURCE_GEOMETRY §§1-2 |
| apex_degrees | d_S(r)=6 and d_S(s),d_S(t)>=6 | Original interior degrees and R6_TRANSFER §§1,4 |
| boundary_excess | sum_B(d_S-5)>=3 | Inherited h>=3 |
| apex_skeleton | Exact induced apex edges rs,rt,pq, plus tp iff d_G(a)=4 and sq iff d_G(c)=4; not both optional edges | SOURCE_GEOMETRY §2 |
| r_fan | Original r rotation is (x,y,t,w,v,s) up to reversal; v,w are different from B,p,q | R6_TRANSFER §1 |
| seven_pin_edges | Induced C5 and triangle zpq, with only optional tp,sq among the seven pins | SOURCE_GEOMETRY §2 and R6_TRANSFER §§1,3-4; pv,pw,qv,qw absent |

These are necessary predicates, not a characterization of genuine minimum
sources. Retaining a larger class is safe for exclusion. Other original
small-cycle/degree restrictions are intentionally not used as extra pruning.

## 4. Exact original-edge quotient and coloring obligations

For each retained frame delete {u,x,y,b,r} from S and identify a,c as z,
suppressing parallel edges. This is exactly U: it has n-6=k vertices and
k-5 interior vertices. Every remaining original edge is retained. Save the
entire original rotation and all names, and order U as

    (a,s,v,w,t,p,q, remaining original labels in increasing order), a representing z.

A saved full coloring has one color for every vertex in this list. The
independent verifier reconstructs the quotient from the original edge set,
checks its exact vertex set and named order, and checks every original edge
after identification. Thus it does not rely on the search solver or on
matching only a color-count marginal.

An extension of any of the forbidden boundary words ABCBC, ABCBD, ABCDC
contradicts Sigma(U) subset319. A single complete witness suffices to reject
that particular graph/frame. It is unnecessary to enumerate its other
colorings to establish this contradiction. An ABCBC coloring may give more
than one r lift; no choice of r is made to erase the violation of the required
complete outer relation.

If all forbidden outer rows have empty fibres, search every forbidden
seven-pin row. A witness there is checked by independently inspecting all
legal r colors and deriving a violation of the R full-lift condition. U
colorings with no r lift are allowed and are not rejected for nonextension.
Only candidates without either kind of witness enter exhaustive collection
of all allowed seven-pin fibres, including empty fibres. The exact outer
mask then distinguishes a genuine necessary 319 residual from a missing
required outer row. Such a residual still does not prove source realization.

## 5. Exact conclusion rule and limits

For any order for which the full sphere generation, all roots and frames,
necessary-filter coverage, and per-frame contradictory-coloring checks have
completed, there is no minimum source of that order in this named branch.
The conclusion follows from coverage plus witnessed contradiction for every
retained frame, not from a zero target-trigger count.

Original r>=7, different original boundary degrees, unbounded r6, general
T/T0 extension, and the general catalogue equality are not covered. Finite
absence for this branch does not raise the general K bound. Upstream paper
and external-computation dependencies remain explicit; there is no new Lean
theorem or proof of all-size source realizability/exclusion.
