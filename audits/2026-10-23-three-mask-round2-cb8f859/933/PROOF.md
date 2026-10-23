# 933: the two remaining quotient support certificates are impossible

The domain is the **complete original r6 two-star source contract** frozen in
[INPUTS.json](INPUTS.json), with original full ten-row support 933. This proves a
no-go for the three fixed reductions. It does not exclude an original 933 source.

Fix one such hypothetical original graph G and its actual exterior disk E.
Retain all original edges, rotation, boundary attachments and ordered contacts:

```
B=(x,y,a,b,c), E=(a,n,R,L,q,c,x,y),
N(p)=(a,b,q,h,n), N(h)=(p,q,L,R,n), N(b)={a,c,p,q}.
Q1=(G-{p,h})/(n=b,R=q), Q2=(G-{p,h})/(n=L=b),
GB=G-{p,h}+{bn,bL,bR}.
```

The inherited original hypotheses include global minimum badness, original
facial triangles, original interior minimum degree five, original x,y,b degree
four, p,h degree five, r degree six, s,t at least six, and the original fan and
two-star face identities. The inherited source proof verifies that E really is
the complementary disk. The reductions have the same original outer C5, with
strict completion costs k-4, k-4, k-2. None of these hypotheses or operations is
replaced by a newly invented graph.

For each of the 274 canonical proper C8 words t, let z(t) count every complete
extension to **this same actual E** of the fixed literal boundary assignment t.
These are nonnegative integers. A common S4 permutation acts on the complete
colouring and all contacts, giving canonical-word indexing. The argument never
normalizes separate contacts, factors, components, or rows independently.

The inherited planar equality-indicator span and original source Kempe zeros
give z in a fixed 18-dimensional rational subspace B of Q^274. The checker
reconstructs this from all 1430 noncrossing partitions, 91 nonzero independent
indicator columns, and the frozen original-mask-933 support bound. Coefficients
in the indicator span can have either sign; only the actual counts z are
nonnegative. Complete matrices M_G,M_Q1,M_Q2,M_GB are reconstructed from all
2560 literal cap assignments and every p,h lift, including all 2392 empty
fibres. Hence N(H)=M_H z is the full ten-row count vector of one fixed H.

The predecessor already proved that GB has full support in K132 and that each
quotient can be outside K132 only by one of these exact signed conditions:

| inherited rule | positive row | empty complete fibres |
| --- | --- | --- |
| 49 | 01203 | 01012,01201,01202 |
| 55 | 01023 | 01012,01021,01202 |

For both quotients the entire 01021 count is already zero. We only examine these
four residual candidate/rule pairs. No new 56-rule screen is used.

The following exact identities hold throughout B:

\[
N_{01232}(G)=4z_{30}=4z_{131}>0,
\]
\[
z_0=z_5=z_{26}=z_{47}=z_{127}=z_{152}=z_{168}=0,
\]
\[
z_{130}=z_{112}+z_{125}+z_{129}
        =z_{11}+z_{112}+z_{125},\qquad
z_{29}=z_{11}+z_{24}+z_{28}.
\]

The relevant fixed E words are:

| ID | word | ID | word |
| --- | --- | --- | --- |
| 0 | 01010101 | 5 | 01010202 |
| 17 | 01012101 | 24 | 01012301 |
| 26 | 01012303 | 29 | 01012321 |
| 30 | 01012323 | 47 | 01020303 |
| 127 | 01202303 | 130 | 01202321 |
| 131 | 01202323 | 152 | 01210101 |
| 168 | 01210303 | | |

Every count identity is checked by exact multiplication against a reconstructed
basis, rather than a comparison on selected feasible controls.

Fix the palette split 02|13. In one complete colouring of E, the connected
components induced by these two complementary pairs define one partition pi of
the ordered eight boundary contacts. Each block has only one palette. Any two
adjacent boundary contacts in the same palette are in one component because
their original rim edge is present. Distinct component blocks cannot have
alternating boundary contacts: their disjoint connected subgraphs would give
crossing paths in a disk. Thus pi is among the compatible noncrossing partitions.

Keep this **one actual partition** and switch any subset of its actual complete
components. Components meeting no boundary can be left unchanged. Switches
within either complementary pair preserve properness, and their boundary words
are the orbit of pi. Every member of that orbit therefore has a positive
complete E fibre. Consequently, if every compatible pi has an orbit member
whose complete fibre is forced empty, the starting fibre must also be empty.
This is a universal exclusion of every actual component choice, with no choice
of an unrelated witness at successive switches.

The following small finite lemma is reconstructed exhaustively and independently
of graph realization. It includes every compatible partition and every subset
switch, retaining the complete literal outputs in the certificate:

| starting ID | compatible 02|13 NC partitions | set hit by every orbit |
| --- | ---: | --- |
| 131 | 12 | {47,127,130} |
| 30 | 55 | {5,26,29,168} |
| 17 | 55 | {0,24,26,152} |

This is a finite interface lemma for arbitrary-size actual E. It is not
enumeration of exterior graphs and does not assert that any admissible
partition, support, or count vector is realized by an original source.

**Q1.** In fact the two complete fibres 01012 and 01202 cannot both be empty.
Their nonnegative complete projections force z112=z125=0. Restricting B by all
coordinates in these projections gives the exact identity z132=-z11. Since both
are nonnegative actual complete E counts, z11=0. The displayed identity then
gives z130=0, while z47=z127=0 is already inherited. The 12-partition lemma
forces z131=0, contradicting N01232(G)=4z131>0. Both residual rules require the
two empty fibres, so neither is possible. The separate rule49 certificate also
checks the direct alternative z129=0 and z130=z112+z125+z129=0.

**Q2, rule49.** Its complete empty projections force z11=z24=z28=0. Thus z29=0;
the other three blockers z5,z26,z168 are inherited zeros. The 55-partition lemma
at 30 forces z30=0, contradicting N01232(G)=4z30>0.

**Q2, rule55.** Its complete empty projections force z24=0. The other blockers
z0,z26,z152 are inherited zeros. The 55-partition lemma at 17 forces z17=0.
On this same restricted count space, direct complete projection gives

\[
N_{01023}(Q2)=z_{17}.
\]

This contradicts the required positive **candidate** row. This last argument
does not kill a required original-source row and does not exclude the original
source itself.

All four quotient residuals are therefore impossible under the complete
original source contract. By the inherited complete-support classification,
both Q1 and Q2 have full ten-row support in K132. Together with the inherited
GB result, **every member of this fixed three-candidate family has support in
K132**. None can supply a smaller bad graph by any alternate K132-outside
support certificate. Another legal construction or a direct source argument
is still required; general 933, source realizability, smaller badness and Lean
formalization remain open.
