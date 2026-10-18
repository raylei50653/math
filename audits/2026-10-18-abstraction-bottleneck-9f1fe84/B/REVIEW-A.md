# Independent review of A and the integrated response statement

Reviewer: B; frozen research BASE
`9f1fe84f73aabfa87a33d28754633bae6bf0b707`.

Read A/ANALYSIS.md, A/check_signed_interface.py, the actual frozen catalogue,
and the frozen no4ct handoff section 2. No A implementation was imported for
the independent calculation. Instead, enumerate combinations of boundary-row
indices in increasing cardinality, comparing their separate Boolean values
against every catalogue mask. The results are:

| Target | Minimum observations | Number of minimum scopes |
| --- | --- | --- |
| 932 | 4 | 5 |
| 933 | 4 | 2 |
| 941 | 4 | 1 |

The unique 941 scope is the proposed common four-query scope. Directly
checking the four claimed deletion controls confirms catalogue masks
774, 564, 960 and 165 respectively satisfy the other three conditions.
There are 132 distinct catalogue masks and 64 raw masks satisfying all
four conditions. This independently confirms the reported numbers, within
the frozen catalogue only; no catalogue enumeration completeness was rerun.

The signed contextual replacement theorem is sound: acceptance uses one
actual common tuple and fresh disjoint private vertices, while each rejection
uses emptiness of the complete actual exterior intersection. Full relation
equality is stronger than required. The same P' must satisfy all queries;
different complete colourings at different boundary rows are legitimate.

The smaller-bad-source corollary is licensed by the frozen no4ct handoff:
the minimum is over all disk sources outside K, rather than one mask or
the r=6 branch. The new graph must remain in the original finite simple
ordered disk class and be smaller after completion. A correctly retains
these obligations and does not claim to construct that graph.

One correction was requested and accepted in A section 1: replace "exactly two complete
odd complement cycles" by "exactly two complete complement cycles, both
odd". The former can be read as allowing extra even components, in which
case full reference connectedness is false. Frozen two-cycle B sections
2--3 and its explicit negative control draw precisely this distinction.

Root REPORT section 3 agrees with B's dominance direction: old P must
have response no larger than smaller Q, so Q success transfers to P and
P badness implies Q badness. Its compatibility relation should include
the literal joint target `e=1, f xor g=1`. Response equality is not
full-source fibre equality, and the report correctly preserves that limit.
