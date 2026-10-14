# T1 crosscut: independent support and Kempe logic review

Date: 2026-10-14. Baseline: `77fbd5da7ba273f0af7c75175dc08376d2282f46`.

**Verdict: PASS for the mathematical support-exclusion criterion, conditional on
the stated literal graph decomposition and an exact, complete finite replay.**
No counterexample to the support, Cartesian-product, Kempe-pruning, or maximal
rectangle argument was found. This review alone does not establish the
source-to-shell coverage or adopt `h=3 => p=0` into the repository.

The reviewed manuscript is `frozen/T1_generalization_notes.md`, especially
lines 112–165. The candidate archive arrived during this review; its producer
and verifier were then inspected. A new independent rule/control module was
written and executed before inspecting those candidate implementations.

## 1. Exact literal gluing, including full fibres

The sufficient decomposition hypotheses are

\[
G=P\cup L_+\cup L_-,\quad
V(P)\cap V(L_\pm)=D_\pm,\quad
V(L_+)\cap V(L_-)=D_+\cap D_-\subseteq V(P),
\]

with all original edges contained in the displayed pieces and all identifications
literal. In the proposed crosscut, the last intersection is the same original
path `c_i-x-c_(i+4)`. These are hypotheses for this support review; their universal
source coverage belongs to the separate geometry review.

Fix a literal boundary row `beta` on the named original B. If `F_L(gamma)` is
the complete set of proper colourings of L restricting to literal `gamma`, then
restriction and union give the exact fibre identity

\[
F_G(\beta)\cong
\bigsqcup_{\substack{p\in\operatorname{Col}_4(P)\\p|_B=\beta}}
F_{L_+}(p|_{D_+})\times F_{L_-}(p|_{D_-}).
\]

Every factor, including empty factors, remains present. Given the full triple
`(p,f_+,f_-)`, union is unique and all original edges have been checked in a
piece. Conversely every full G colouring has exactly that restriction triple.
This does **not** make the full G colouring unique for fixed `p,q,r`.

The wording “能唯一黏合” at manuscript line 120 should therefore be read, or
made explicit, as “after choosing the two full lifts, their common literal
union is unique.” Support membership guarantees existence, not a singleton
fibre. The saved exterior lifts are full colourings of P, not a listing or
count of the unknown original G's full colourings. This is a clarification of
the claimed identity, not a counterexample to it.

Let `R_+` and `R_-` be the complete **unconstrained** boundary-orbit supports of
the same two fixed original disks. An orbit belongs to such a support exactly
when every literal representative of that orbit has a full lift: a single
witness transports by a global palette permutation on that disk. No boundary
vertex permutation is used. For any actual shell colouring p, these transports
can make each side equal to `p|D_+` and `p|D_-` at every boundary vertex. They
therefore agree on the shared path. The exterior p remains fixed throughout.

Define `M(q,r)` by simultaneous restriction of one shell colouring, then take
the two orbit indices. The fibre identity proves exactly

\[
\Sigma_B(G)=\bigcup_{q\in R_+,\ r\in R_-}M(q,r).
\]

This operation preserves support and the existential content of the full
literal fibres. It does not reconstruct fibre multiplicities from supports.

## 2. Safety and the quantifier order

If `Sigma_B(G)=tau`, every pair from the **one fixed** product `R_+ x R_-`
satisfies `M(q,r) subseteq tau`. Otherwise a forbidden B row has a shell witness
and both full side lifts, producing a forbidden colouring of that same G.
Consequently

\[
R_+\times R_-\subseteq E_\tau,
\qquad E_\tau=\{(q,r):M(q,r)\subseteq\tau\}.
\]

Different accepted rows may use different shell colourings and different full
lifts, but the two complete disk supports remain fixed. A per-row choice of
supports, or an arbitrary set of independently selectable safe pairs, is a
larger relaxation and does not replace this necessary product condition.

Pairs with `M(q,r)=empty` must be retained as safe. In particular, some pairs
cannot align on the shared path; the common literal shell enumeration gives
exactly zero output for these pairs. Removing them from `E_tau` would impose a
false requirement that every abstract product pair have a shell witness.

An empty disk support gives empty global support by the exact identity. Since
933 and 941 are nonempty, this case is already contradictory. Nothing here
assumes that every planar disk is four-colourable.

## 3. Necessary Kempe alternatives and deletion

For a fixed literal C6 row and one of the three complementary palette splits,
take all connected components in the two corresponding bichromatic induced
subgraphs of an actual disk colouring. Their nonempty intersections with C6
partition its six vertices. A block uses only one palette pair; boundary
neighbours in the same pair are in the same block. Distinct components are
vertex-disjoint embedded connected subgraphs, so two blocks cannot alternate
around the simple disk boundary. Thus the actual partition occurs among the
candidate noncrossing partitions used here.

Each boundary-meeting component can be switched independently. Edges between
different palette groups remain properly coloured, and distinct components
of one group have no edge between them. Components missing the boundary can
be left fixed. Hence the entire boundary orbit `O(r,split,partition)` of all
subsets of these switches belongs to that **same disk's complete support**.

For every real support R, the necessary statement is

\[
\forall r\in R\ \forall s\in\{0,1,2\}\ \exists\pi:
O(r,s,\pi)\subseteq R.
\]

Allowing the witnessing partition to vary with the row or split is a valid
relaxation. Neither a common witness across different colourings nor
realizability of an arbitrary accepted support is asserted. Crucially, R is
not a support already filtered by one shell colouring or fixed shared-path
pins; such filtering need not be Kempe-closed.

For a candidate S containing R, a deletion of r because one split has no
alternative wholly in S cannot delete an element of R: its actual colouring
provides an alternative wholly in R and therefore in S. Induction preserves R
through all deletions. The deletion operator is monotone and deflationary, so
iteration reaches the greatest fixed point contained in S, denoted `kappa(S)`.
Sequential fair deletion and simultaneous deletion reach the same result.
In particular `kappa(empty)=empty`.

Only necessary planar conditions are used. Chords, extra internal edges and
arbitrarily many internal vertices can restrict true supports further; omitting
those restrictions enlarges the relaxation and does not invalidate exclusion.

## 4. Maximal safe rectangles, including empty sides

Use coordinatewise inclusion of ordered support pairs `(A,B)` when speaking of
a maximal rectangle. Let `Q` be the 31 orbit indices and `N(q)` the safe right
neighbours of q. Take every intersection

\[
B=\bigcap_{q\in X}N(q)\quad(X\subseteq Q),\qquad
A=\{q:B\subseteq N(q)\}.
\]

The empty-family intersection is Q. For every displayed B, `X subseteq A`
and `B subseteq N(q)` for all `q in A`, so
`intersection_{q in A} N(q)=B`. These are exactly the coordinatewise maximal
safe pairs. Conversely, any safe pair `(R_+,R_-)` extends to one of them:
first take `B=intersection_{q in R_+}N(q)`, then take the corresponding A.
This also proves coverage for empty sides with the stated convention.

Enumerating only nonempty matrix entries, omitting the empty-family
intersection, or enumerating only inclusion-maximal sets of product pairs
without defining empty-side handling would not be the stated proof. The
candidate implementations do not make these substitutions.

For a containing safe rectangle, true supports survive independently:

\[
R_+\subseteq\kappa(A),\quad R_-\subseteq\kappa(B),\qquad
\tau=\Sigma_B(G)\subseteq
\bigcup_{q\in\kappa(A),r\in\kappa(B)}M(q,r)\subseteq\tau.
\]

Thus an exactly computed missing target row for every maximal safe rectangle
excludes all such pairs of actual disks, without an internal-size bound. The
same missing row for all rectangles is stronger evidence than required; a
different missing row for each rectangle would also suffice.

## 5. Candidate code inspection and new independent controls

The following code implements the reviewed logic:

- `candidate-original/t1_broad_probe/kempe_probe.py:11` enumerates all set
  partitions and uses the alternating-four-indices test; lines 22–38 generate
  full independent-switch alternatives. Lines 40–51 implement sound deletion.
- `twohole_fast.py:19` builds all 31-by-31 safe pairs, including zero outputs.
  Its `domains={ALL}` and repeated intersections enumerate the full closed
  rectangle family, including the empty-family intersection. Lines 11–17 use
  sequential deletion, and lines 26–38 test the pruned rectangle union.
- `independent_verify.py:90` uses set blocks and a circular-gap test; lines
  112–138 generate alternatives by repeated switches. Lines 140–146 use
  simultaneous deletion. Lines 164–185 enumerate the transpose closure family
  and compare each complete rectangle, both pruned supports and missing mask.
  A record marked incomplete cannot pass these checks.
- `twohole_probe.py:38` and `independent_verify.py:68` derive both interface
  orbit indices from one literal shell colouring. They do not independently
  align the two interfaces. The latter retains each complete shell colouring.

The newly written `review/kempe_controls.py` imports neither candidate
implementation nor the new reconstruction producer. It generates the 31
canonical rows from all literal C6 colourings and the 132 noncrossing set
partitions from restricted-growth words, computes switch-orbit masks and a
simultaneous `kappa`, and enumerates actual graph colourings for seven disks.
After writing it, its 31 row identities and all 93 sets of Kempe alternatives
were compared to **both** candidate implementations: all agree exactly.
Its partition representation happens to coincide with the candidate producer's
representation; the candidate verifier supplies the separate set-block/gap/BFS
path. Independent authorship is not claimed to make these mathematical
representations different.

The independent positive controls executed successfully:

| Disk construction | Support size | Full literal colourings | `kappa(R)=R` |
|---|---:|---:|---|
| C6 cycle | 31 | 732 | PASS |
| C6 wheel | 11 | 264 | PASS |
| Fan triangulation | 8 | 192 | PASS |
| Zigzag triangulation | 8 | 192 | PASS |
| One short chord | 20 | 480 | PASS |
| One opposite chord | 25 | 588 | PASS |
| One vertex stacked in a fan face | 8 | 192 | PASS |

The independent empty-support and universe fixed-point checks also pass.
Compact JSON serialization of the independent `rules` table has SHA256
`de135931433b350bfffb5dc1e72dd74e93c9fafff0998f05b6ac9770671d8c2e`.

The independent row enumeration has 1 two-class, 10 three-class and 20
four-class partitions. For a fixed four-colour palette, a partition with k
classes has `4!/(4-k)!` literal representatives. Thus the full C6 literal
count is `1*12 + 10*24 + 20*24 = 732`. Review self-check corrected an earlier
factorial formula here; the row enumeration and executed control count were
already 31 and 732 respectively.

This subreview did **not** independently rerun all 64 outer kernels, 701,020
rectangles, the 59,156 exterior lifts, the negative controls or determinism
runs. Those manuscript figures are not promoted to locally verified facts
by this file. The complete replay is recorded separately by the coordinating
review. The support criterion, candidate implementation inspection, exact
rule-table agreement, and the seven new actual-disk controls are the evidence
established here. No new Lean theorem or universal source realization claim
is made.
