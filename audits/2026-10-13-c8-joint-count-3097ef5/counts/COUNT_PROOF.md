# C8 common extension counts: exact exclusions and residuals

The final artifact is `certificate.v2.json`. The initial
`certificate.json` is retained as discovery evidence; its residual vectors
are not asserted to satisfy Kempe closure on their own supports. The final
artifact certifies 57 transfer/Kempe exclusions, three additional universal
count exclusions, and ten necessary-condition residuals. Every final
residual has a complete rational count vector whose own support satisfies
all recorded Kempe obligations.

## The common count space

Fix one finite graph H embedded in a closed disk, with the named boundary
cycle C8 in the collar's recorded cyclic order. For each canonical proper
boundary word p, define x_p to be the number of proper four-color extensions
of that fixed literal word to this same H. Each x_p is a nonnegative
integer. A common permutation of all four color names gives bijections
between extension sets, so choosing one representative of each S4 orbit is
valid. No orbit size is multiplied into x_p.

Expand the product of edge inequality indicators by inclusion-exclusion.
For F contained in E(H), let pi(F) be the partition of boundary vertices
induced by components of (V(H),F), and k0(F) the number of components meeting
no boundary vertex. For a partition pi, let E_pi(p) equal one when p is
constant on every block of pi, and zero otherwise. Then

```
x_p = sum_{F subset E(H)} (-1)^|F| 4^k0(F) E_pi(F)(p).
```

The boundary partition pi(F) is noncrossing: two disjoint components
connecting alternating pairs of boundary vertices cannot be embedded in
the disk. Thus x belongs to the span of all noncrossing equality vectors.
This assertion holds for arbitrary interior size. The signs of the
inclusion-exclusion coefficients are unrestricted.

`checker.py` independently enumerates restricted growth words for all set
partitions of eight named positions, rejects crossing quadruples, and
constructs the equality columns on all 274 proper C8 color orbits. It finds
1,430 noncrossing partitions. Exactly 91 columns are nonzero, and exact
Fraction elimination gives rank 91. The other 1,339 columns are identically
zero because their equalities conflict with proper cycle coloring. The
certificate stores all 1,430 partitions, the indices of the 91 nonzero
columns, and the full 274 by 91 nonzero-column matrix; the full 274 by 1,430
matrix is specified by inserting zero columns at the other indices.
Consequently this space has codimension 183 in the 274 count coordinates.

There is no assumption that the coefficients in this column expansion are
nonnegative. The only imposed nonnegativity concerns actual x_p. In
particular, neither a Boolean support indicator nor a vector of
independently selected extension counts is substituted for x.

## Transfer and universal certificates

The independently checked parent `interface.json` defines T[b,p] as the
number of distinct literal inner words q in orbit p that are compatible
with the fixed literal outer representative b on every actual collar edge.
For every H, the outer count is exactly

```
y_b = sum_p T[b,p] x_p.
```

This formula includes the two-color orbit with its 12 literal words and
the other orbits with their 24 words. It uses the same color frame on both
boundaries and requires no division by an assumed common orbit size.

The parent Kempe screen proves that the complete relation of any eligible
H is contained in its recorded upper U. Thus x_p=0 outside U. Each new
exclusion identity has a positive integer left side supported inside U and
a signed integer right side supported outside U. The checker checks its
residual separately on **every one of the 1,430 equality vectors**, checks
every zero coordinate, and recomputes all preimages of the required outer
row from the complete transfer. The identity and nonnegativity force every
left-side count to zero.

For the three count exclusions, the required outer row is index 9, literal
word `01232`. All its allowed preimages occur on the following left sides;
the complete signed right sides are in the certificate and vanish.

| Case | Named extras (a0,a1,a2,a3,a4) | Target | Positive left side | Required preimages |
| --- | --- | --- | --- | --- |
| c05 | (0,0,1,1,1) | 941 | x28 + 4x123 + x207 + 2x225 | 28,207,225 |
| c13 | (0,1,1,0,1) | 941 | x18+x59+x87+2x94+x131+x205+4x223+x250+x269+x272 | 18,59,87,131,205,250,269,272 |
| c23 | (1,0,1,0,1) | 941 | x18+x21+x59+x60+2x94+4x108+x176+x270+x271+x272 | 18,21,59,60,176,270,271,272 |

The right sides have respectively 46, 64, and 71 nonzero integer terms.
Each term stores both index and literal named word, preventing accidental
mixing of pattern orders. Every required preimage has count zero, whereas
941 requires that outer count to be positive. These are exclusions for all
finite inner disk graphs, independent of their size.

## Combining zero-count deductions with Kempe support closure

For each initial residual, `strengthen.py` computes the maximal possible
support of the rational nonnegative count cone with the prescribed outer
zeros and positive accepted counts. It starts with a feasible vector. For
every coordinate still zero, it either finds another feasible vector where
that coordinate is positive and adds the vectors, or produces an exact
nonnegative identity forcing that coordinate (and possibly others) to
zero. It then reruns the complete Kempe pruning on the reduced support.
Any resulting deletion becomes another necessary zero for the next count
problem. There are 22 additional exact forced-zero identities across the
ten cases. Every step is recorded under `refinement_stages`.

This iteration remains universally sound. An identity with positive left
side and already-zero right side cannot delete an actual positive count.
Kempe pruning cannot delete a member of the complete relation of one
actual inner graph. These facts are preserved inductively. A final
residual vector is positive at every coordinate of the final upper and
zero elsewhere; its support itself passes every complementary-pair Kempe
obligation. It therefore supplies a simultaneous witness to this precise
combination of necessary conditions, including all common linear count
identities, rather than separate witnesses for individual coordinates.

## Exact remaining cases

All ten vectors, all 91 signed partition-expansion coefficients, all ten
outer counts, and the complete preimage lists are saved in
`certificate.v2.json`. The checker uses Fraction arithmetic to verify
x=E c, x>=0, required zeros, and the exact positive/zero outer pattern.
The denominator column below is the least common denominator of all 274
counts; multiplying by it gives an integral vector satisfying the same
homogeneous necessary conditions.

| Case | Named extras | Target | Initial upper size | Final support | Count denominator |
| --- | --- | --- | --- | --- | --- |
| c04 | (0,0,1,0,2) | 941 | 201 | 193 | 192 |
| c07 | (0,0,2,0,1) | 941 | 201 | 193 | 36960 |
| c15 | (0,1,2,0,0) | 933 | 144 | 134 | 4 |
| c15 | (0,1,2,0,0) | 941 | 175 | 173 | 48 |
| c16 | (0,2,0,0,1) | 941 | 102 | 102 | 4 |
| c18 | (0,2,1,0,0) | 933 | 144 | 134 | 8 |
| c18 | (0,2,1,0,0) | 941 | 175 | 175 | 48 |
| c20 | (1,0,0,0,2) | 941 | 175 | 173 | 96 |
| c30 | (2,0,0,0,1) | 941 | 175 | 175 | 10 |
| c32 | (2,0,1,0,0) | 941 | 102 | 102 | 4 |

These are **necessary-condition residuals**. They are not actual inner
graphs, counterexamples, or realizable relations. Fractionality by itself
is not the missing obstruction, since all vectors can be scaled to
integers. What remains unproved is realization by one disk graph with the
required collar, full-source minimality, degree and triangular-face
conditions. The Boolean Kempe obligations require an allowable component
partition for each row and split, but do not construct one graph realizing
all such partitions and all these extension multiplicities together.
Any exclusion of these residuals must use additional restrictions on
same-graph Kempe-component/count compatibility or the specific minimal
triangulated source structure, beyond the identities and obligations
certified here. No proposed extra restriction is assumed in this audit.

There is therefore no adoption of h>=4 or n5>=10, and no conclusion about
K<=13=K<=5 or K_infinity=K<=5.

## Reproduction and controls

Final exact verification uses only the Python standard library:

```
python3 audits/2026-10-13-c8-joint-count-3097ef5/counts/checker.py --check
python3 audits/2026-10-13-c8-joint-count-3097ef5/counts/negative_controls.py
```

Discovery uses scipy `linprog` only to find candidate primal and dual
vectors. `generate.py` and `strengthen.py` reconstruct them by exact
Fraction elimination, and run the independent solver-free checker before
exclusive creation of a certificate. Reproduction order is `generate.py`
with a fresh `--output`, then `strengthen.py --initial <that-output>` with
another fresh `--output`.

The controls alter one identity coefficient, alter its named pattern,
remove a necessary accepted-row preimage, and remove the final support
verification field. All are rejected. The coefficient and preimage
corruptions are also passed to the actual checker CLI and must exit
nonzero. For case c05, substituting the Boolean indicator of its upper
into the certified identity gives residual 8, so that support vector
cannot be an actual common count vector. Orbit-size corruption and
literal finite-graph transfer controls are checked by the parent audit.

`verification.json` records the successful runs and normal/seed-17 byte
comparisons. `discovery_failure_01.txt` preserves an initial serialization
type mismatch caught before any v2 certificate was written. It was fixed
by normalizing in-memory tuples to JSON arrays before verification; no
mathematical condition was weakened.
