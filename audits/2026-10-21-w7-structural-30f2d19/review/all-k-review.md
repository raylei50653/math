# Independent adversarial review: arbitrary-k template theorem

Reviewed [template/REPORT.md](../template/REPORT.md), SHA256
`f65654068741a186daefb338e2f29921c0d96fda5b948089abc0b8ae589fb8bf`,
against the frozen local template definition and [template/check.py](../template/check.py).
No external result, original-graph enumeration, or LP was used.

**Verdict: the all-k paper proof is sound as stated.** It proves the rational
column-space rank and the stated Walsh support. I found no missing
nonemptiness, completion, parity, or normalization hypothesis. It does not
prove a nonnegative-cone or original-source statement.

The potentially delicate points survive the following checks.

1. **Completion gives exactly k+1 nonempty blocks.** The r even matching
   chords have distinct endpoints and disjoint interiors. Every chord splits
   one existing cell, giving r+1 cells. A cell cannot be enclosed entirely
   by chord segments: disjoint matching chords cannot form such a cycle.
   Thus it has a positive-length original-circle arc between distinct even
   chord endpoints; that arc contains an odd contact. When r=0 the sole
   disk contains all k odd contacts, including k=1. Hence every odd cell
   block is nonempty. The cells are intersections of the disk with chosen
   closed chord half-planes and are convex. An odd contact is never a chord
   endpoint, so it belongs to a unique cell. Any selected odd matching pair
   stays in one cell because its chord crosses no even matching chord.
   Consequently every odd cell block has an even selected cardinality.
   There are r even pairs plus k−2r even singletons, hence k−r even blocks,
   and r+1 odd blocks. The resulting k+1-block partition is noncrossing.
   This construction need not preserve the odd pairs as separate blocks;
   even selected cardinality is precisely the required condition.

2. **The pair-count recurrence has the correct shift.** After n contacts,
   the last edge matching pairs consecutive vertices starting at −(n−1).
   Counts on its j-th pair are `binom(n−1,j)`. The next matching shifts
   by one vertex, so its j-th pair receives the old pair counts with
   indices j−1 and j, with out-of-range counts zero. Pascal's identity
   gives `binom(n,j)`, including both boundary pairs. At n=2k, zero is
   the second vertex of pair j=k−1, giving `binom(2k−1,k−1)`.
   An additional independent direct count checked the full asserted
   distribution, not only its return entry, for n=1,...,24; it agreed.
   The induction above, rather than these finite checks, is the all-k
   justification.

3. **Returning subsets and frequencies are in bijection.** Empty-word
   reduction deletes equal-letter pairs, so every returning subset has
   even selected cardinality in each palette. Given its nonanchor bits,
   the even-palette parity uniquely determines contact 0, and the
   odd-palette parity uniquely determines contact 1. Conversely the
   completed bits of every accepted frequency are a returning subset.
   Thus there is neither an uncounted anchor condition nor a factor of
   four from anchor choices. At k=1 there is one frequency and one
   returning subset, the empty subset.

4. **The Fourier argument uses the actual normalized subgroups.** Each
   nonanchor block has a nonzero indicator with disjoint support, giving
   dimension k−1. Omitting both anchor blocks is correct after fixing the
   two palette phases. Orthogonality tests even selected cardinality on
   nonanchor blocks; palette-parity completion supplies precisely the
   missing two anchor-block conditions. Keeping every coset makes the
   span exactly the Walsh characters in the annihilator. Summing these
   character spans over all partitions gives their union, with no possible
   extra characters. The frozen run-contact convention alternates the two
   palettes, so its bipartite/transition conditions reduce exactly to
   monochromatic noncrossing partitions with k+1 blocks. Constant entry
   multiplicity before normalization does not change rank.

These checks support adoption of the theorem without changing its scope.
The proof's explicit warnings about signed reconstructions, pruned templates,
shared Z, nonnegative weights, source realization, and W7 exclusion are
necessary and should remain.
