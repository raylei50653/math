# Independent review of outer-star bound and B14 attachment count

Reviewed `workers/geometry/PROOF.md` against the frozen Γ8 two-interior-point
proof and the complete original component/rootless-star contract.

**Verdict: the at-least-four outer F-private vertex bound is valid.**

The interior-common-neighbor barrier is sound. An interior t and exterior v
cannot be adjacent across Γ. For nonadjacent Γ endpoints p,q, the simple
original C4 p–t–q–v therefore has both diagonals absent, contrary to the
original empty-C4/triangulation authority. The claimed r/s and x/d barriers,
and the L-specific T/x and R-specific T/d barriers, use actual τ/ζ edges.

All four exterior-face third points u,a,b,c are actual original F vertices:
each defining edge has a private endpoint whose entire original star is in
F. The complete induced Γ graph disallows another Γ point as that face's
third vertex. Their K2/M2/N3 memberships force private status. The r/s
barrier permits only u=a and b=c among the six pairs, and either permitted
equality has color 3 in N. In L, b=c seals s's entire exterior link to a
single point and gives degree four; in R, u=a similarly gives degree four
at r. O excludes both, already yielding four distinct outer private points.

The L/R three-point argument also closes every loophole needed for its
complete-link inference:

- T's entire original star is rootless and private, so there are no boundary
  neighbors missing from its exterior link. The L/R barrier disallows the
  third of u,a,b,c as an additional T-neighbor. The forced link edge gives
  b∈M2 in L and a∈M2 in R.
- In L, all s-neighbors are private. A non-K 02 neighbor lies in the same
  rootless J−K branch; a boundary K neighbor could only be U, and the
  original ψ12 C/E separation excludes sU. Thus the three-point assumption
  really forces the exterior link T–b–c–x and c∈N3.
- In either L or R, the next x-link point after exterior c cannot be h:
  that would join N to B. This next point w has color 1 or 2, hence belongs
  to private N or private K2. The listed common-neighbor barriers or the
  M/K anticompleteness exclude each previous private point as w. The
  complete induced Γ graph also prevents w from lying elsewhere on Γ.

Thus w is a fourth *different* exterior F-private vertex. Counting τ,ζ and
the four already private Γ points r,T,s,x gives ten distinct private points
on this same skeleton. This is a local necessary lower bound; it neither
raises the inherited global k≥23 nor establishes a collar/source realization.

## Independent endpoint count

Recomputed from the Cartesian set
`d∈{private,U}`, `e∈{private,V,Y}`, `h∈{private,c}`,
`W*∈{private,q}`, without reading the parent's attachment enumeration.

The uniform Γ8 filters are:

1. h=c implies d,e private (complete M02 flip, then same K flip);
2. e=V,W*=q is impossible (the exact original Y/V common-neighbor theorem);
3. d=U,W*=q implies both original ear edges absent (complete rootless N13
   flip plus the initial03 4/9 U/q separation; the dW edge is directly Uq).

They retain exactly 12 of the 24 endpoint-presence patterns. Exactly two
patterns have d=U,W*=q, and each retains the three zero-ear L/R/O types.
The other ten retain all eleven at this filter level. Counts are therefore
`10×11+2×3=116` rows per complete contract, or 464 across four contracts,
from 1056 initial attachment/type/contract rows. All eleven unlabelled local
types survive with private endpoints. This agrees with the parent's
independent 1056→464 finite check and carries no full-collar realizability
claim.

## Wording corrections incorporated in FINDINGS

The rooted ψ12 block at c is D, with contacts `{c,s}` or `{c,s,v}`. The Γ
component E may be rootless; if E meets B14 then E=D. The earlier wording
that assigned those contacts unconditionally to E has been corrected.

The full-component flips produce a new witness on the same original source
and preserve the fixed cap/fibre/lift relations. The wording now explicitly
does not claim that the fixed M vertex set acts properly or bijectively on
every other coloring in those full relations.
