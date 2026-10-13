# Independent review: original C9/932 identities and apex degree-three exclusion

Scope is the single frozen global-minimal-source contract in
[SOURCE_CONTRACT](../SOURCE_CONTRACT.md), with complete relation 932 and
h=4. The checked conclusion excludes all 100 named degree-three apex
hypotheses and gives original apex H-degree at least four. The geometric
consequence m>=9 and k>=18 is valid in this same scope. Neither statement
excludes the 20 full sources with larger apex degree, or any h>=5 branch.

## Original identities and joint transports

The frozen independent checker was rerun read-only with its eight negative
controls. Its complete reconstruction of all 70 annuli, 435 queries and
574,000 fibres passed; see [frozen run](frozen-independent-check.json).
The twenty target-932 residuals are precisely the identities in the root
contract. Their three D5 orbits have sizes 5, 5 and 10:

| Source geometry | Named queries | Original support size |
| --- | ---: | ---: |
| Two nonadjacent gaps equal two | 5 | 376 |
| Three consecutive positive gaps, 1,2,1 | 5 | 352 |
| Three consecutive positive gaps, 2,1,1 or its reflection | 10 | 356 |

The target-932 bits are exactly the five four-color C5 rows, so its
stabilizer is all of D5. This fact was checked from the actual ten outer
rows, not inferred from the mask's decimal name.

For every one of the 20 cases and every `(s,t)` with s in {1,-1} and
t modulo five, the original vertex transport is

* `b_i -> b_(s*i+t)`;
* `a_i -> a_(i+t)` if s=1, and `a_i -> a_(t-i-1)` if s=-1;
* `y_i_j -> y_(s*i+t)_j` if s=1, and
  `y_i_j -> y_(t-i)_(e_i+1-j)` if s=-1.

The reflected face orientation and each original annulus rotation path
are reversed together. The independently computed destination C9 position
map acts on all 820 rows. One common color permutation normalizes the
transported inner row and acts on the entire corresponding literal lift,
including its outer B colors. We check every full fibre, including empties,
against the destination fibre; we also check all columns and the complete
necessary support mask. Thus all 200 transports preserve the same original
attachments and color frame. [identities.json](identities.json) retains all
20 original identities and all 200 complete vertex and row maps.

## Independent finite derivation

[check.py](check.py) imports no producer code. It reconstructs proper rows
by literal enumeration and canonicalization. It enumerates all 21,147 Bell
partitions of nine positions and rejects crossings, obtaining 4,862
noncrossing partitions. For each row and complementary color-pair split,
it checks monochromatic-side blocks and the forced connections along
original C9 edges. It then enumerates every simultaneous set of component
flips. The resulting complete table is checked equal to the frozen generic
C9 Kempe table, entry by entry.

At each of the nine positions the checker independently changes only the
apex color while holding the other eight literal colors fixed. It retains
three occurrences when constructing each recoloring triple. This gives
91 triples per position. For C9 these three indices are in fact distinct:
the remaining eight vertices form a proper path of odd edge length with
equal endpoint colors, so those eight fixed colors cannot use only two
colors. At least three fixed colors prevent a nontrivial color permutation
from identifying different apex choices while fixing the entire remainder.

Starting from each original frozen support, the checker alternates its own
D3 singleton deletions and generic Kempe deletions. All 100 original
collar/apex hypotheses finish empty. The destructive-round histogram is
30 in 3 rounds, 50 in 4, 10 in 5 and 10 in 6. The main certificate also
counts the final stationary check, so its 4--7 rounds describe the same
process. This is a counting convention, not a mathematical discrepancy.

The independent trace is preserved in
[independent-certificate.json.gz](independent-certificate.json.gz). A normal
read-only run regenerates and compares its complete content, and similarly
checks all of identities.json, rather than accepting their final counts.

The checker additionally reads the main
[counts certificate](../counts/certificate.json.gz). Every recorded D3
literal witness is checked against independently reconstructed rows. Every
removal must be live in the stated before-mask and justified by its stated
triple or by a genuinely absent row in **every** independently reconstructed
Kempe orbit of the specified split. The exact before/after chain must lead
from the original frozen support to zero. All 100 named apex labels must
occur exactly once. The full 20 by 10 by 820 annulus transfer coefficients
are checked against the independently verified literal fibres; both row
domains have S4 orbit size 24, so no orbit-size multiplier is missing.
The main 232 quotient constraints retain the frozen exact masks.

Six additional corruptions must be rejected: a changed recoloring triple,
a wrong original apex position, a changed annulus count, a broken deletion
chain, a false omitted Kempe row and an overclaim that the 20 whole sources
were excluded. See [final run](independent-final-run.json). The root
verification also reruns this checker with hash seed 17.

## Paper review and exact stopping boundary

The original degree-three local faces in [geometry/PROOF](../geometry/PROOF.md)
are forced: the induced C9 neighbors u,v and unique strict inner neighbor t
give exactly the inner faces uat and avt. Original t is adjacent to both
u and v. Deleting a is planar and loopless, removes one vertex, and replaces
u,a,v by u,t,v on a length-nine boundary. It does not produce an old C8
source. The separately described addition of uv produces a legitimate C8
disk but fails the old five-apex/three-Y and strict-inner degree contracts.

For a fixed literal assignment to C minus a with u=v colored c, the three
counts z_d on this one H-a give exactly x_i=z_j+z_l and its cyclic versions.
This retains complete full lifts, not marginal data. Its triangle
inequalities and the actual-component Kempe condition apply to the same
820-coordinate count vector as annulus transfer and source-relative
quotient positivity. A support deletion preserves containment of the real
support; the empty terminal support contradicts an accepted original B
row. Thus the certificate proves the apex-degree theorem for arbitrary
finite inner size under the fixed source contract. The signed partition
expansion in [counts/PAPER](../counts/PAPER.md) is also a valid same-H
identity, but is not needed for this contradiction.

The k>=18 corollary is independently valid. After all original C vertices
have H-degree at least four, a strict inner vertex touching C positions at
circular distance two would bound an empty original C4 cap. Inducedness
forces its middle C vertex to have full H-degree three. Circular distance
three similarly gives an original C5 cap: its empty triangulation is the
fan from the inner vertex, or its only nonempty possibility is literal W5.
Both force a short-arc middle C vertex to have H-degree three. These cap
arguments use the inherited original-cap contract; their boundary already
contains original inner vertices, giving the required strict size budget.

Therefore one inner vertex cannot touch C positions at distances two or
three. Any two distinct C9 boundary edges have such a pair among their
endpoints. Their inner triangular faces cannot have the same third vertex.
All nine third vertices are strictly inside the induced C9, proving m>=9
and k=9+m>=18. Distance-four contacts, including permitted three-contact
sets, remain available under these necessary restrictions; no C8
two-contact conclusion is imported.

No source realization, stronger n5 bound, general 932 exclusion, h>=5
closure, universal planar colorability or Lean formalization is asserted.
