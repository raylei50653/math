# Independent structural reuse review

BASE: `d5b8a8605bcbcef7aebbcf1934dad7ba255ccf02`. This review changes no prior
evidence or solver model. It establishes finite representation and rank facts,
without deciding the necessary cone or any source-realizability question.

## Reviewed result

`check_fourier.py` independently decoded all **199,290** literal half-rows and
reconstructed all **307,197** frozen columns through the extracted run templates.
It imports neither extraction nor Fourier discovery code. Input SHA256 values
and the PASS record are in `fourier-review.json`.

The six universal templates have respectively:

| Number of transitions / 2 | Rows | Columns | Exact rational row rank |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 4 | 4 | 3 |
| 3 | 16 | 20 | 10 |
| 4 | 64 | 112 | 35 |
| 5 | 256 | 672 | 126 |
| 6 | 1,024 | 4,224 | 462 |

The rank proof is exact. The row phases form a binary vector space. Each column
is an affine-subspace indicator. Grouping columns by their difference subgroup,
the review checks that **every coset** occurs for each subgroup. Such a complete
coset family spans precisely the Walsh characters trivial on that subgroup.
The union of these character supports therefore gives both an upper and a lower
bound for the rational rank. The Walsh matrix is invertible over the rationals;
no floating-point rank tolerance, modular-rank assumption, or general binomial
identity is used. This confirms the proof in `fourier/probe.py` independently
from the extracted column supports.

## Exact reduction contract

For a palette-membership word `q`, let `T` be its full universal template and let
`J` be its surviving columns. Extend the shared state values to a full template
row vector `u_q`: a live half-row carries its original `Z_i`, while a removed
half-row carries zero. The original block equations are exactly

```
T[:, J] X_q = 2 u_q,     X_q >= 0.
```

Every surviving column is zero on removed rows. The original column ID and
original state ID maps reconstruct the full frozen system.

Applying the full Walsh transform preserves these equations. Frequencies absent
from the template span give equations **on Z**:

```
Walsh_forbidden(u_q) = 0.
```

They cannot be discarded because the X side vanishes. Allowed-frequency
equations plus these Z identities are equivalent to the original block.
Deleting columns or rows can create further dependencies, so universal ranks
are upper bounds for pruned blocks; they need not remain equalities.

A rank basis for `T` alone does not justify deleting the corresponding full
equations `2Z_i - (TX)_h = 0`. The Z coefficients also have to obey every removed
row relation. Further global compression must keep a checked basis of the
shared-Z identities, with an exact reconstruction map.

Linear span also does not replace cone membership. In a factorization
`X_q = particular(u_q) + N_q w_q`, the inequalities `X_q >= 0` remain essential.
An exact final point must reconstruct every original X and Z and pass the
existing independent checker.

## Computation that can be reused now

All six templates together have only **5,033** distinct columns and **146,905**
incidences. Cache these operators and the checked maps. A matrix-free multiply
can bucket original X by membership word and template column, apply the local
template, and scatter to original half-rows. Its transpose reverses these steps.
The X-only operator then takes the same two half-row differences per state;
positivity rows are evaluated from the same reference sums. This avoids storing
repeated template coefficients and preserves all coordinate identities.

Cache local Walsh transforms, exact row dependencies, and symbolic elimination
orders by template and by pruned live-row mask. Numerical factors can be reused
only when their actual coefficients match; changing IPM weights generally
changes them. Batch equal local shapes where useful, and benchmark actual
operator time and memory before claiming a solver speedup.

For static condensation, the local nullspaces constrain a global Z master while
local nonnegative X feasibility remains per block. This is a valid decomposition
or oracle formulation. It does not imply a small global interface: every state's
three palette rows share one Z. Schur complements may fill in, and singular
local blocks require rank-aware elimination. The rank and size of the global
master must be measured separately.

## Limits and further reusable certificates

The earlier discrete equitable partition rules out that specific averaging
reduction, but is compatible with the template reuse verified here. Conversely,
slow crossover and one greedy triangular probe do not prove that every possible
basis has a dense core of the observed size. Those are measurements of particular
supports and elimination choices.

Exact cone points form a reusable witness library. Since all ten positivity
forms are nonnegative, independently exact homogeneous points covering the ten
requirements can be added and scaled to satisfy them jointly. Each library item
must use the same frozen model and full coordinate maps; approximate points
cannot be substituted. The target sum may be covered by either target state.
This cone-point addition does not glue independently chosen source colourings
or prove one original graph exists.

The next substantive computation is global compression of the shared-Z linear
identities, followed by a measured local/global formulation. No renewed large
solver run is required to establish the reusable structures above.
