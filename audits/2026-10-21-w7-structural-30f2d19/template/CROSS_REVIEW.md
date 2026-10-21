# Independent review of the source-level structural claims

This review was written by the template-proof author after independently
reading the compensation and geometry implementations and certificates,
the target-exchange paper proof and implementation, and the frozen counting
and geometry authorities. It is a review of those other claims, not an
independent review of the all-k theorem in this directory.

No mathematical bug was found in the claims below, with their stated scopes.

## Compensation and the source-valid chain

The exact block coefficients and column-price signs give:

- `0010101101001`: all prices vanish, so `Z44459=Z44480`.
- `0111111010010`: only two negative prices, so `Z44480<=Z44541`.
- `0101010101011`: all prices are nonpositive, so
  `Z44541<=Z784+Z37416+Z46468+Z66394`.

These follow by multiplying the original shared-Z half-row equations by
their displayed integer weights. No independent source is selected in any
block. The four positive marked-phase families contain `42+42+14+5=103`
columns; the negative families contain 95 price-minus-one and eight
price-minus-two columns. The global conservation law is exactly
`2Z44459=P-N`. Therefore `P<=N` is equivalent to target emptiness under
the existing equations; merely rewriting it supplies no new exclusion.

The palette obstruction is valid for compensation preserving that fixed
palette-membership word. It does not prohibit a mechanism changing the
palette split or coupling distinct words through the same source.
The optional-chord zero-set inclusion for state 66394 is a direct
chord-properness observation; it does not establish a feasible fibre or
survival under further orbit closure.

The final semantic summary validator checks histogram completeness,
the global conservation coefficient, and the marked-phase star mapping.
Its three negative controls violate those invariants. Independent normal
and seed-17 read-only replays of compensation/check.py passed.

## Conditional target exchange and the five joined types

For either named target, the other 01 rim vertices are exactly
`{a,n,u3,u1,c}`. If the actual 01-component containing the original edge
`vw` avoids this set, swapping the whole component preserves every other
rim colour and exchanges the two target tuples. The induced 01 graph is
unchanged, so this is an involution of complete original colourings,
including all private vertices. No automorphism or invariance of a
selected path-witness subfamily is needed.

Restricting XOR variation profiles to one palette distinguishes actual
boundary components after normalization: among any two distinct same-
palette components, at least one has an independent flip. The recovered
blocks regenerate all sixteen rows of each complete normalized coset.
I checked the fifteen recorded partitions against the five-type paper
table; they agree. The shared five columns have separated `vw`, and the
exclusive five on each side have `vw` joined to `a,n,c`.

The exact difference of the two original incidence rows yields the
displayed ten-term identity. If a separate argument proves `Z44459=0`,
nonnegativity eliminates its shared and exclusive contributions, leaving
only the five B-exclusive terms. This does not prove target equality or
emptiness of those joined types. In the model's normalization the shared
sum is `U=2N_A^sep=2N_B^sep`, since each half-row equation has left side
`2Z`. The paper's description of U as the common contribution is
consistent with that scale.

Independent normal and `PYTHONHASHSEED=17` optimized read-only replays
of review/target_exchange.py passed, including its support-corruption
control.

## Geometry and the 69/40 necessary profiles

I read geometry/PROOF.md against geometry/check.py and certificate.json.
The external-neighbor lemma has a source-level Jordan proof: the two
nonempty wheel arcs lie on opposite sides of the original four-cycle,
so its bounded side contains a named original point regardless of which
side is bounded. The three five-cycle arguments correctly retain a
legal W5 center when all required spokes exist and impose a **complete**
degree-five star rather than only extra edges.

The placeholder cells do not assert empty original regions. Cutting
their dual along an actual short cycle locates named original points
without discarding unknown private vertices. Thus the computed interior
sets are conservative lower bounds. The complete old-rim contact
profiles justify the absent-spoke exclusions.

The certificate records 43 excluded and 69 surviving profiles; the
direct witness-proper subsets have sizes 28 and 24, overlap 12, and
union 40. These are necessary geometric/profile constraints for the
fixed source contract, not source realizations or joint-cone feasibility
certificates. The original chord-free profile remains in that union.

The five exterior face centers on the path edges are pairwise distinct
by the external-neighbor lemma. They are actual face vertices on the
F13 side of its rim, so they are retained F13 vertices, not deleted cap
vertices. With no C13 chord, a third face vertex cannot be another rim
point, giving five distinct private F13 vertices. This is a lower bound
on source structure and does not justify a source reduction by itself.

An independent `geometry/check.py --controls` replay passed. No LP,
new original-disk enumeration, shared documentation edit, or source
realization was performed in this review.
