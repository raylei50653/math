# B cross-review of the degree exclusion and R100 integration

BASE `ffea555fc2a896d8166ce198ca28ed9262912f25`, 2026-10-17.
Reviewed [A/PROOF.md](../A/PROOF.md), [C/PROOF.md](../C/PROOF.md) and
the root [PROOF.md](../PROOF.md) against the frozen direct authorities
listed in [INPUTS.json](../INPUTS.json). The B localization argument was
written independently before reviewing these new notes.

## 1. Degree exclusions: accepted

A correctly uses the literal endpoint equalities beta=q and alpha=p,
and uses the same selected g at the actual dual vertices of mzq/mzp.
The matching implication through zpq has no colouring-lift premise and
therefore applies even to an ordinary P101 matching with an odd
complement. The subsequent p/q-centre split is exhaustive under the
frozen A2--A3 classification. It excludes only nonfacial active-f seven
components, at arbitrary size.

For the adjacent-sector centre, the original degree-six a rotation
contains distinct alpha,n_a,p. The actual faces mzalpha and zalpha n_a
have their asserted inside/outside statuses because X consists of
exactly the primal triangles incident with a centre. Their shared
spoke collides with g at the former face. The argument would fail for
a degree-five rotation, and A explicitly avoids that mistake using
the adopted a0>=6 bound. The reflected c argument and all four rows
of the residual table follow. In B's notation, `n=n_a` and
`ell_q=ell_c`; these are harmless names for the same transported pins.

## 2. Root localization: accepted

The conjunction of the ell-s,ell-t and n_a-s,n_a-t nonedges is valid:
each separately nonempty full fibre forbids an actual retained edge
of the same original G. Neither the root nor B combines its two
complete-colouring witnesses. The five-degree ell link gives the
claimed conditional ell-v/ell-w exclusion from qv/qw and n_av/n_aw.
The older later-source proof independently gives an even stronger
version of these latter nonedges.

B reconstructs both complete-star boundary orders and their reflected
q counterparts. Thus the induced five-cycle really is the spoke dual
of this same cap, contains z, and avoids m,v,w. Both marks e and g are
wholly outside X; selected spokes cannot meet one of their already
matched endpoints. This proves graph distance at least two. The root
correctly does not infer complete exchange-region separation.

## 3. R100 conditional theorem: accepted

C takes all three reference matchings from one complete all-distinct
Tait colouring of the same D. Each has an even complement. For any
such R, `L_R=(D-M) union (D-R)` contains every entire old and reference
complement cycle. Flipping all difference cycles in one full component
replaces its whole complement by the even reference and preserves all
old complement cycles outside it. Since its vertex count is even, an
included seven-cycle is accompanied by a positive even total of old
odd cycles; strict descent is at least two.

For R100, e is common, f is absent from both, and g is the only marked
difference. Avoiding the complete g region is exactly the condition
for a batch of whole regions containing C to remain P101. C correctly
leaves existence of such an actual reference OPEN. The forced e/f
alpha-beta circle obstructs R001; the forced e/g alpha-gamma circle
obstructs R010. These are claims about the specified whole-region
strategy, and do not rule out every other alternating repair.

The spoke counts are odd and cannot be five for an even reference,
giving simultaneous counts `(3,1,1)` with no designated three-spoke
class. The alpha-beta and alpha-gamma safe full-circle switches can
alter R100; beta-gamma switches cannot. The exact update

`E(L_R')=E(L_R) triangle (M intersect E(K))`

has the correct addition/deletion directions. In particular a move
which only adds L edges cannot strictly shrink the g component.
Minimizing that component is a well-defined finite choice over actual
complete source colourings, and C correctly requires an additional
improving-move argument before deducing separation.

## 4. Editorial check and authority boundary

The initially reviewed root text pointed to C section 5 for the
move/update rules; they are in C section 6. This correction was sent
to the integrator. No mathematical objection or missing premise was
found in the reviewed claims.

All 17 frozen inputs were checked against their manifest byte counts
and SHA256 values with zero drift. B supplies no new finite source
enumeration or certificate. This cross-review is a paper proof audit;
it does not formalize the geometry in Lean or construct a genuine
minimum source. The complete source relation, empty fibres and full
lifts are retained. Remaining seven-caps, reference-region separation,
other odd components, joint even-complement positivity and complete319
remain OPEN.
