# 933: three candidate 01231 lower bounds, fan-B full-support no-go, and two quotient targets

BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`; 2026-10-23. Output boundary: this `933/` directory only. No shared docs, commits, or pushes.

**New conditional source results.** In the original complete r6 source contract with full support 933, each of the same literal candidates Q1, Q2, GB has a nonempty complete `01231` fibre. More precisely,

\[
4N_{01231}(H)\ge N_{01232}(G)>0\quad(H=Q1,Q2,GB).
\]

Thus the proposed alternative certificate `01232 positive; 01202 and 01231 zero` is impossible for all three. Together with the earlier `01212` leakage identity, this closes all three minimal K132-outside certificates whose sole positive row is `01232`.

The bounded exact screen goes further: **the full support of this fixed GB is always in K132.** On each Q1 and Q2, only two of the 56 minimal signed support certificates survive the specified propagation. They are not asserted feasible, and no source is realized. These results exclude methods on the same fixed family; they do not exclude a 933 original source or construct a smaller bad graph.

## Frozen authority and complete source identity

[INPUTS.json](INPUTS.json) freezes ten authority inputs byte-for-byte at BASE, including the old count-space certificate/checker, original three-candidate proof, complete Kempe live sets, K132 catalogue, and all 56 support rules. Each replay checks both frozen hashes and zero drift against the current authority paths. Routing documentation hashes are recorded separately and permitted to drift; no mathematical input is taken from those routing files.

Use the same original ordered boundary and actual exterior:

```
B = (x,y,a,b,c)
E = (a,n,R,L,q,c,x,y)
N(p) = (a,b,q,h,n)
N(h) = (p,q,L,R,n)
N(b) = {a,c,p,q}
Q1 = (G-{p,h})/(n=b,R=q)
Q2 = (G-{p,h})/(n=L=b)
GB = G-{p,h}+{bn,bL,bR}
```

The original complete r6 contract, original rotation, original attachments and face identities, literal color frame, and strict completion costs k-4/k-4/k-2 are inherited unchanged from the frozen source proof. E is the actual C8 disk interface, not an abstract polygon independently recolored per row. Original `x,y,b` are degree four, `p,h` degree five, original r degree six, and original s,t at least six, with the other original minimal-source hypotheses retained. The present proof needs their established consequence that the same actual exterior count vector lies in the frozen 933 necessary space.

`z_j` counts **all complete exterior extensions** of the fixed canonical representative of E tuple j. Its value applies to another tuple only through a single common S4 action; individual contacts or rows are not normalized independently. Every z is nonnegative. The checker reconstructs all 274 proper C8 representatives and 2560 literal local rows; it retains every p,h lift, including all 2392 empty local fibres. There are 175 local lifts in total. It checks the full local relation directly against all original named edges and separately against the local extension formula before constructing the four full ten-row projection matrices.

For any actual E disk, the vector z belongs to the signed span A of the noncrossing equality indicators (1430 partitions, 91 nonzero columns, rank 91). The frozen actual-source Kempe zero coordinates intersect this span in dimension 18 for 933; coordinates 176 and 192 are additionally forced zero. The checker reconstructs this space exactly with rational arithmetic. The signed coefficients of the span are never assumed nonnegative: only the actual complete counts z are.

## Exact small proof of the new 01231 lower bound

The following are identities on that same 18-dimensional source space:

\[
N_{01232}(G)=4z_{20}=4z_{30}=4z_{131}.
\]

The distinguished literal E words, in the fixed order above, are

```
20  = 01012121
30  = 01012323
131 = 01202323
```

Direct complete projections, modulo the already forced-zero exterior coordinates, give

\[
\begin{aligned}
N_{01231}(Q1)&=z_{131}+z_{51}+z_{273},\\
N_{01231}(Q2)&=z_{30}+z_{172}+z_{212},\\
N_{01231}(GB)&=z_{20}+z_{34}+z_{61}+z_{101}+z_{121}+z_{155}+z_{182}.
\end{aligned}
\]

All residual terms are nonnegative complete fibres of the same actual exterior, giving the displayed factor-four lower bound separately for each literal candidate. This proof does not add independently feasible vectors or swap candidate witnesses. The checker verifies each equality by multiplying its complete 274-coordinate residual through the reconstructed 18-column basis.

The earlier identities, independently rechecked here, are

\[
4N_{01212}(H)-N_{01232}(H)=c_Hz_{17},
\quad c_{Q1}=c_{Q2}=2,\quad c_{GB}=4.
\]

The three alpha-single-positive minimal rules are exactly:

| positive | zero rows | reason impossible here |
| --- | --- | --- |
| 01232 | 01023,01212 | old 01212 leakage |
| 01232 | 01202,01231 | new strict 01231 positivity |
| 01232 | 01021,01202,01212 | old 01212 leakage |

## Exact screen of all 56 signed support certificates

The checker regenerates all minimal Boolean signed rules over the complete ten-row support, checks equality with the frozen 56, and checks the equivalence for all 1024 support masks. A full support is outside K132 iff it satisfies at least one rule. Each rule is applied to one fixed candidate H, with the same exterior vector z.

For each candidate/rule pair, the zero projected counts first force zero all exterior coordinates appearing with positive coefficient in the corresponding complete count rows. In the remaining rational subspace, choose independent coordinates that are themselves actual nonnegative z entries. Exact row reduction writes every other z as a linear combination of these coordinates. An identity

\[
z_j=\sum_i c_i z_{q_i},\qquad c_i\le0
\]

forces every term with c_i<0 to zero, since all the actual counts on both sides are nonnegative. Iterate this rule, retaining the complete literal vector and all zero coordinates. Each recorded step stores the row, actual pivot-coordinate IDs, exact signed coefficients, and newly forced zeros. The checker independently recomputes the relation and signs. A case is ruled out only when a strictly positive original 933 row or required positive candidate row is identically zero. All six accepted original rows, `01012,01023,01203,01213,01231,01232`, remain required positive throughout.

No LP, large graph enumeration, or per-row choice of component witnesses is used. The 168 cases have 81 nonempty propagation rounds and 633 explicit zero-relation witnesses.

| candidate | original positive killed | candidate positive killed | survived this propagation |
| --- | ---: | ---: | ---: |
| Q1 | 54 | 0 | 2 |
| Q2 | 49 | 5 | 2 |
| GB | 55 | 1 | 0 |

Because all 56 rules are impossible on GB, its full ten-row support belongs to K132. This is a full-support no-go for this fixed fan-B family on original support 933, extending the earlier impossibility of the designated four-row certificate. It does not say which K132 cell occurs, and does not exclude another legal reduction.

The only residual rules for either quotient are these zero-based rule IDs in the frozen order:

| ID | positive | zero rows |
| --- | --- | --- |
| 49 | 01203 | 01012,01201,01202 |
| 55 | 01023 | 01012,01021,01202 |

For Q1/Q2 the complete 01021 projection is already identically zero on this same source space. Thus rule 55 reduces to `N01023>0; N01012=N01202=0`. Rule 49 keeps its three zero obligations. **Consequently, under the original source contract, a quotient is outside K132 iff it satisfies one of these two remaining signed conditions.** Both require `N01012=N01202=0`; their positive row is no longer alpha. The proof is conditional and exact; it does not establish that either condition can occur in a nonnegative necessary vector or an actual original graph.

This is the next concrete method choice: analyze the complete 01012/01202 fibres of the actual Q1/Q2 and seek a source-geometric contradiction or a true same-candidate positive witness for rule 49 or 55. New reduced constructions remain a separate option. Further widening of the necessary cone or original graph enumeration was deliberately not performed.

## Validation and boundaries

Replay commands:

```
python3 audits/2026-10-23-three-mask-methods-cb8f859/933/check.py
PYTHONHASHSEED=17 python3 audits/2026-10-23-three-mask-methods-cb8f859/933/check.py
python3 audits/2026-10-23-three-mask-methods-cb8f859/933/check.py --negative
```

`--build` exclusively creates a new certificate and is not used by a read-only replay. [certificate.json](certificate.json) contains the complete full-lift records, matrices, new decompositions, all 56 rules, all 168 traces, and summaries. Normal, seed-17 and negative replay outputs and exit records are saved alongside this report. Corruptions cover changing the factor four, changing contact order, omitting a full lift or an empty fibre, dropping a rule or candidate/rule case, reversing a propagation coefficient sign, omitting one strict original positive row or its killed-positive witness, and falsely claiming source realization/general exclusion.

| authority | status |
| --- | --- |
| exact count identities and fixed full local relations | triggered and holds |
| sound 56-rule propagation on the frozen necessary space | triggered and holds |
| actual complete original 933 source control | not triggered; no original source graph supplied |
| feasibility of the surviving two quotient rules | OPEN; not asserted |
| source realization of surviving rules | OPEN; not asserted |
| GB support in K132, conditional on the original source contract | paper consequence with exact finite certificate |
| a new strictly smaller bad graph | not constructed |
| general 933/932/941 exclusion or K-infinity closure | OPEN |
| new Lean theorem | none |

The absence of a realized source control is not used to prove the conditional results. Their source applicability is the actual-source-to-necessary-space implication inherited from the frozen authority; all new exclusions hold on the entire stated necessary domain. No statement of source realizability follows from a surviving propagation case, and the result does not close general 933.
