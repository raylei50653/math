# Independent universal count certificate

The named inner boundary is
`(a0,a1,y2,a2,a3,y4,a4)`, with literal colors `0,1,2,3`.
The 91 pattern order and the outer transfer are read from the frozen
`collar_certificate.json`. No ring relabelling or separate row relabelling
is performed. The old universally sound bound is
`U = 755425272170557940120206052`, containing 55 rows.

## Universal identity proof

Let H be any finite graph embedded in the closed disk, with the seven named
boundary vertices in this cyclic order. For a fixed proper named boundary
assignment p, let N(p) be the number of proper four-color extensions to H.
This is a nonnegative integer; it is positive exactly when p is in the full
relation of this one H. The same H defines every coordinate of N.

Expand the product of edge inequality indicators by inclusion-exclusion.
For F a subset of E(H), let pi(F) be the partition of the boundary vertices
induced by connected components of (V(H),F), and let k0(F) be the number of
components containing no boundary vertex. Let E_pi(p) be 1 when p is
constant on each block of pi, and 0 otherwise. Then

```
N(p) = sum_{F subset E(H)} (-1)^|F| 4^k0(F) E_pi(F)(p).
```

Every pi(F) is noncrossing: two vertex-disjoint connected components joining
alternating boundary pairs would contradict planarity in the disk. Thus N
is in the linear span of the equality vectors of the 429 noncrossing
partitions. On the 91 proper C7 assignments, only 36 of these equality
vectors are nonzero. No positivity is asserted for their expansion
coefficients. Only the actual extension counts N(p) are nonnegative.

The checker independently enumerates all set partitions as restricted
growth words, checks crossing quadruples, and computes the equality matrix.
It uses exact Python Fraction arithmetic to derive identities. Every
resulting identity is then separately checked pointwise on all 429
noncrossing partitions, including the 393 zero columns. Consequently the
identity holds for every such H, without an interior-vertex bound, a
triangulation assumption, or a conjectural count cone.

## Contradiction from the complete relation

Write x_i=N(p_i). Since the old screen proves the full relation is contained
in U, every rejected coordinate is zero. The independently certified
identities then imply

```
x_6 + x_35 = 0,
x_58 - x_6 = 0,
x_89 - x_6 = 0.
```

The first identity and nonnegativity force x_6=x_35=0. The other two force
x_58=x_89=0. The exact named patterns are

| Index | Pattern |
| --- | --- |
| 6 | 0101212 |
| 35 | 0120131 |
| 58 | 0121202 |
| 89 | 0123231 |

The frozen complete outer transfer gives **exactly** indices `[6,58,89]`
as the U-accepted inner preimages of the required outer row `01232`.
All of them have zero extension count, so the complete outer relation
cannot contain `01232`; 941 does contain it. This excludes every disk inner
source contained in U that would transfer to 941. It does not claim U itself
is realizable or that each coordinate has an independent source.

An alternative certified consequence is x_42=0 (`0120231`), from the short
identity

```
x_42 = x_8 - x_10 + x_14 + x_16 - x_21 - x_23 - x_30
       + x_33 + x_44 + x_51 - x_53 - x_67 + x_88.
```

Every term on its right is outside U. The certificate additionally verifies
x_49=x_73=x_75=0. These alternatives are not needed for the direct transfer
contradiction.

## Replay and negative controls

```
python3 audits/2026-10-13-c7-joint-kempe-19209f4c/joint/count_identity.py --check
```

`count_identity_certificate.json` records all 91 rows, all 429 partitions,
the full 91 by 36 equality matrix, seven exact signed identities, and all
429 zero residuals for each identity. Full rank is 36; rejected-row rank is
31. Rank is diagnostic: the proof is the pointwise identity verification.

Changing the coefficient of rejected index 8 in the x_42 identity is
detected by a nonzero equality-vector residual. Substituting the Boolean
membership vector of U as an alleged count vector gives identity residuals
`[1,1,1,1,2,0,0]`, so the checker rejects the tempting identification of a
support upper bound with actual extension counts. Actual graph controls are
kept separately in the parent audit's `counts` directory.

`maximal_screen.py` and its certificate are a separate, prior diagnostic:
using only maximal complementary partitions leaves the same 55-row bound.
They record 1,785 checks that each original orbit contains a maximal
partition's orbit, and 189 viable triples summed across the 55 rows. These
figures do not assert simultaneous realization of the 55-row relation.
