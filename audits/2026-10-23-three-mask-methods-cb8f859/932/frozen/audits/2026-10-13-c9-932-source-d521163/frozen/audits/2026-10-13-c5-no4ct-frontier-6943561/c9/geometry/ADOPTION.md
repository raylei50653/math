# C9 source consequence of the complete necessary interface

Scope: the same globally inner-vertex-minimal, then edge-maximal source
outside the fixed catalogue K as in [PROOF](PROOF.md). This does not use
the Four Colour Theorem and does not apply fixed-mask minimality.

The paper dichotomy gives two exhaustive possibilities when h=4: an
induced actual C9, or one original W5 ear. For the latter, its precise
named position is among the 75 eligible (e,chord) pairs. The literal
short-C5 condition is an actual necessary relation, with one center
lift per permitted row. Consequently a real source in an ear branch
must pass that branch's complete annulus transfer and Kempe tests.

The [finite producer](../finite/check.py) retains all 70 original
collars, all 820 C9 S4 row orbits, all ten original C5 columns, empty
annulus fibers and full literal annulus lifts. The query starting
support consists exactly of columns contained in the target relation,
intersected with the full ear mask when present. True inner rows all
belong to this initial support. At each Kempe deletion a real full
inner lift supplies its actual boundary component partition. This is
one of the noncrossing options in the generic table; an additional
original chord can remove options but cannot remove the actual one.
All component swaps of that lift stay in the same real complete inner
relation. By induction no real inner row is deleted.

Thus if the final support's complete outer union omits any accepted
target row, that named query has no source. It is safe to use equality
of this union with the target as the acceptance requirement: every
initial column, and hence every surviving column, is already contained
in the target. Zero source triggers do not participate in this proof.

The produced complete certificate records all 75x3 ear queries as
excluded by transfer/Kempe. Every ear query's final outer union is
zero; some still have 100 or 200 inner rows, all with empty original
annulus columns. Therefore the paper dichotomy and verified interface
give the conditional source theorem

\[
\boxed{h=4\ \Longrightarrow\ \text{the original C9 is induced}.}
\]

This adoption requires the full producer/checker replay and the parent
audit's independent finite review. Their actual run outcomes are
recorded in the parent verification ledger, not assumed by this
document. The proof does not need universal C9 disk colorability or
an unrestricted planar quotient theorem.

For induced C9 the same certificate gives the following necessary
query boundary:

| Complete original target | Transfer/Kempe excluded | Source-relative quotient excluded | Necessary residuals |
| --- | ---: | ---: | ---: |
| 932 | 50 | 0 | 20 |
| 933 | 44 | 0 | 26 |
| 941 | 28 | 4 | 38 |
| Total | 122 | 4 | 84 |

The four quotient exclusions use the actual independent noncrossing
blocks and N=k-9+q<=k. The remaining 84 query supports only pass these
necessary conditions. They are not 84 realized sources, and their
different rows or splits have not been proved jointly realizable.

The full residual list also yields narrow boundary restrictions. For
all three targets at h=4, every residual e has maximum at most three,
so every original B vertex has degree at most seven. For 932 the
twenty residual named collars all have maximum exactly two and are
precisely the following necessary families:

- Two nonadjacent gaps equal two; the other three gaps are zero
  (five ordered choices).
- Three consecutive gaps are positive with entries 2,1,1 in any
  order; the other two consecutive gaps are zero
  (fifteen ordered choices).

Here "consecutive" always means the original cyclic B order, not an
independent normalization of pieces. These families account for all
twenty original named 932 queries. In particular the verified interface
implies the branch-specific conditional source bound

\[
\boxed{\Sigma(G)=932\text{ and }h=4
\ \Longrightarrow\ 4\le d_G(b_i)\le6\ \text{for every original }b_i.}
\]

The corresponding boundary degree multisets are {6,6,4,4,4} or
{6,5,5,4,4}, with the positions restricted as above. This is not a
general boundary degree upper bound for h>=5 or for arbitrary disks.

This theorem preserves the inherited k>=16 and the branch-specific
932 bounds h>=4,n5>=10. It does not exclude h=4, force h>=5, improve the
common five-degree count, imply the h=3 bound k>=19 at h=4, or close
any arbitrary-size 932/933/941 branch. The next C9 task must retain all
five A and four Y vertices, the original e and original accepted
outer rows, and the full literal support of each residual query.
No new Lean theorem is asserted.
