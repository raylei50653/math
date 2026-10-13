# N2-BRIDGE: excluding the missing all-five-rejection source

BASE `243a125a80e4d8de40957f59d8da0bdbc974cf69`. This is an arbitrary-size
paper synthesis, with an explicitly retained finite-terminal U4 dependency.
The new steps concern mask 932. They do not redo the old original55 grid.

## 1. Statement and the exact missing bridge

Let G satisfy the original E4 §1 contract: a finite simple disk with ordered
induced B=C5, all T4 rows accepted, every non-B edge critical for the **complete**
boundary relation, effective excess two, two nonadjacent complete-degree-five
roots r,s and all other effective interior vertices of complete degree four.
Assume H−{r,s} has exactly two original mixed components, all remaining
components unary, and G rejects q0=01212, q1=01202, q3=01021 in one frame.
All original attachments, contact identities, ownership, rotation, bridges,
branches, empty fibres and full lifts are retained. Free isolated vertices
are omitted only from the effective count, retaining their four-colour factors.

**Theorem NB. No such G exists.**

T4 and the three rejections give exactly four possible complete masks:
941 (q2,q4 accepted), 933 (q2 rejected, q4 accepted), 940 (q2 accepted,
q4 rejected), 932 (both rejected). The first three are the already excluded
complete-Sigma N2 domain, with 940 transported **as a whole source** by
b_i ↦ b_(1−i) to 933. This neither guesses the missing bits nor identifies
independently transformed components. It remains to exclude 932.

The exact missing source fact useful to the old local proofs is weaker than
all-edge, all-ten-row minimality:

> **CW:** every original component C of H−{r,s} can be deleted while retaining
> a complete exterior lift of each designated rejected row. In addition,
> the original interior boundary neighbours are at most an adjacent pair.

CW is not asserted to be a logically necessary minimal axiom among all possible
proofs. It is the explicit sufficient missing witness interface found by
tracing the existing proofs. The 932 bridge below proves the stronger
Sigma(G−C)=Omega and the attachment bound, without a generalized N45 theorem.

## 2. Established bridge inputs, without circular N45 use

[U4_TRANSFER](U4_TRANSFER.md) audits the mask-free content of U4. Its
necessary-domain reduction and 828-core finite terminal imply that a N2
source under the original three-row premise has no two-root44 minimal
core. This includes 932. The general root-omission lemma excludes every
single-root core here: each root has at least two mixed incidences. Thus
Z(G)=empty. The general theorem P in frozen arc-pair-critical §3 gives
at most one rejected singleton row in **any** B-preserving proper subgraph.

[BRIDGE_LEMMAS](BRIDGE_LEMMAS.md) proves, for 932 using this P:

1. Every interior vertex, including roots, has at most two boundary
   neighbours, adjacent if two. Each nonedge pair of B is equal in two of
   the five rejected rows; deleting one of its spokes would retain both.
2. For every original C, at least four singleton rows have complete exterior
   lifts in G−C and are rejected in G. Their lists give the original Gallai
   block structure, consistent actual attachments, at most one ordinary
   private point per odd-cycle block, and private root-contacts in all leaves.
3. No unit unary exists. With U4 and no root omission, every remaining C
   has Sigma(G−C)=Omega. Component-edge deletion has the same **complete
   exterior projection**, by degree-four slack.
4. The original H consists of its central r,s block and at most one root
   leaf block at each root; H has no bridges. Original H-degree-two vertices
   have injective actual boundary-edge attachments. Every C is a bridge /
   odd-cycle cactus. These facts come from the original minors, not from
   minimal near-triangulations or a W5 degree theorem.

Only these facts and the original shields are used below. In particular we
do not first assume every root-spoke deletion accepts every row, nor assume
each selected row has G itself as its minimal core.

## 3. Exclude all original unary components

All original pieces are one-sided; their shield edges are disjoint. Unary
support has at least three points and costs at least two shield edges.
If a mixed P had singleton support {h} in the presence of a unary U, choose
the whole-source root order so that U is r-owned. The original bags
R={r}∪U, S={s}∪Q, T=B are disjoint connected and pairwise adjacent, where Q
is the other mixed. Their intersections with N(P) are respectively r,s,h.
Take a complete exterior lift of G−P in a rejected row, supplied by §2.
If P does not extend, merging only equal-colour hub bags and using the
degree-four hub lemma gives an original K5 minor. Thus P cannot have
singleton support. Empty support was already excluded in general E4 §2.1.
The same argument applies to Q. This rechecks the only exterior-witness
premise of frozen residual-unification §3.

Consequently, if u≥2, the two mixed cost at least one edge each and the
two unary cost at least two each, giving 1+1+2+2>5. Thus u≤1.
If u=1 and both mixed are long, the three pieces each cost at least two,
also impossible. Only the following cases remain.

**One unary, two short mixed.** Its owner has k_U=2 or 3: one is excluded
by §2 and the two mixed each consume a root incidence. All explicitly
listed *local* hypotheses of frozen unary-three-row-escape §§1–4 now hold:
degree four, cactus, private leaf contacts, at most one ordinary private
point per odd cycle, adjacent boundary attachments, support at least three,
and the original H-degree-two attachment injection. That proof reads no
other acceptance bit or critical witness. It gives one i in {0,1,3} where
U accepts owner D=3. Both short mixed accept (D,D) in this exact row by
E4 N-diagonal. D avoids every original spoke and rs is absent. The three
full original lifts join to colour G, a contradiction.

**One unary, one long and one short.** The preceding non-singleton argument
makes the short support a true boundary pair. Shield costs are exactly
(2,2,1), so U and the long have actual consecutive three-point supports.
Again k_U is 2 or 3. The following capacity repair is the additional local
bridge; it does not borrow the old original55 factor-disjointness claim.

If k_U=3 and U is r-owned, complete degree five forces t_r=0 and
k_P^r=k_Q^r=1. There is no other unary. Fix any designated row q and any
legal colour b at s (the attachment bound ensures such a colour). Define
F_U(q) from the complete U fibres and G_C(q,b) as the r-colours forbidden
by the complete C fibre with s=b. Degree-four slack with r left free gives
|G_C(q,b)|≤k_C^r=1. Since G rejects q,

    [4] minus F_U(q) ⊆ G_P(q,b) union G_Q(q,b),
    hence |F_U(q)| ≥ 2.                                      (UC3)

The unary three-row escape supplies one q_i with D not in F_U(q_i).
Frozen partition-rule §6's local used-colour theorem, whose complete
hypotheses are exactly the cactus/leaf/degree/support facts already proved,
gives |F_U(q_i) intersect q_i(B)|≤1. As D is the only unused colour,
|F_U(q_i)|≤1, contradicting UC3 in that **same** row.

Thus k_U=2. Frozen unary-diff-closure §2 is explicitly a local theorem
U2-DIFF-ALL: with the derived cactus, leaf, private-point and injection
hypotheses and actual support A=(a,b,c), a proper row taking three distinct
colours on A has F_U(q)=empty. Its original five-shape classification and
barbell K5 proof use no complete-Sigma assumption. Each A has a Diff row
in {q0,q1,q3}. In that row §2 gives a complete lift of G−U; U accepts its
**actual** owner colour, so the full original assignments join. Contradiction.

This exhausts all unary cases and proves u=0 for the hypothetical 932 source,
without transplanting a single exact-S or exact-U N45 certificate.

## 4. No unary: the local long proofs have their real premises

The original H is now biconnected by §2. The remaining two mixed have
nonempty supports, each a short or a long. The following is a premise
audit of existing proof bodies, not a repetition of their nine-grid labels.

| Local result and frozen sections | Actual inputs, supplied here | Extra Sigma/core input in that proof body |
| --- | --- | --- |
| E4 §4.1–4.2, two short | one-sided short original pieces, degree four, full B-touch, no rs, same (D,D) | none |
| diagonal-three-row §3, low-contact long | leaf contacts, odd-cycle private-point bound, attachment injection, degree four; same three rows | none; replaces no topology hypothesis |
| one-long-closure §§2–5, OL | original long and short, all above, adjacent root spokes, full B-touch; complete exterior lift for singleton-support restriction | none; its capacities and OL-F follow directly from degree five and a spanning-tree slack colouring |
| double-long-joint §§2–4, t=0/1 and residual table | same graph, full fibres, cactus/leaf facts, degree-five incidence equations, original shields and root-spoke bound | none; no q2/q4 lookup |
| LL-CUT TOPOLOGY §§2–8 | original two longs and their other-piece minors, all above, low-contact escape; literal q0/q1/q3 | none after these structural inputs have been supplied |

There is no unary factor, so for each root v and proper row q,
|E_v(q)|=4−t_v=k_P^v+k_Q^v−1. The equality needs only that two spokes
are adjacent, so they have different colours. It does not use critical
witnesses from deleting spokes. B-C2 is a full-fibre capacity, not a claim
about marginal colours.

Two short give an immediate diagonal lift. With one long the OL proof
produces a same-row complete lift. With two longs, the t=0/1 proof, shield
residual table and LL-CUT+diag proof together produce a same-row joint in
every possible incidence/spoke domain. Their extra diagonal cells are
justified by the original Gallai/minor argument, not arbitrary safe bits.
In each case this contradicts one of the three rejected rows of G.

Thus 932 is impossible. The exact four-mask partition in §1 completes
Theorem NB. The former complete-mask N2 exclusion remains an explicit
input for the other three masks; no old certificate or historical claim
has been rewritten.

## 5. What has and has not been proved

General N2 **in the original E4 contract** is excluded, including all choices
of q2/q4. This is a paper theorem with inherited external Gallai/hub inputs
and the separately checked U4 finite terminal. It is not a new Lean theorem.
The actual fixed graphs are controls of local assertions, with the full
N2 source premise `not triggered`; this non-trigger is never the proof.

E-ARC2 still has N1 and adjacent-root sources. A single-root *core* may
remain there, whereas the whole source with its sole excess-two degree-six
root was already excluded by E3+D8. Excess≥3 and mask932 are not additional
obligations of E-ARC2's original domain. See [PARENT_COVERAGE](PARENT_COVERAGE.md)
for the exact current cover, core identities and named residual ledger.
