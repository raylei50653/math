# B cross-review of the integrated proof and A cap lemma

Frozen source BASE `6c420f3ca77d60952ed76f93dff7449c522715ca`.
This review is independent of the root's derivation and edits only `B/`.

Reviewed bytes:

| File | SHA256 |
| --- | --- |
| `../PROOF.md` | `463cb574f3d8bf4b7abd1de668ae1f67d31f07b42838406c621cc04de73aef10` |
| `../A/PROOF.md` | `7d50f8e0d9ade8a91ab1872d49681b31c72c9151e92e3395f60b10e1a0c2e401` |
| `PROOF.md` | `a977f4033d38e635539960c83b1133dc9c59f878fd6c60c9b7968a6dc11e679c` |

**Verdict: PASS for the full-source marked-six theorem and its stated
cyclic-cut corollary. No missing case or additional v5 premise found.**

## 1. Independent A cap audit

The complete original fan, not just two incident edges, determines the
bounded sector at a in `Q_a=(a,p,h,w,t)`. The opposite sector contains
the outside boundary wedge and is exhausted by the two original faces
`yat,abp` and that wedge. Thus an original neighbour outside
`{y,b,t,p,h}` would have to lie strictly inside the bounded cap. The
cap's four original inner boundary vertices make the strict source
comparison `s<=k-4<k` valid, even though a is on the original exterior
boundary. Original aw is absent because w has no original boundary
contact.

In an empty cap only ah can add a boundary neighbour. In a one-centre
cap the full W5 theorem excludes ah as an interior cap chord. The fixed
exterior link sector also rules out drawing an additional ah edge on
the exterior side. Consequently a has at most five neighbours in either
case. The c argument uses its actual original fan and cv absent, with
the same bounded-side check; it does not transport a support mask.

The hub identities mp iff a0=4 and mq iff c0=4 follow from the two
actual facial triangles on mz and disjoint original a/c fans. They do
not depend on the previous v5 proof. A includes both hubs, and a z
midpoint is impossible. The two-step lemmas are therefore proved in
their full stated quantifier range.

## 2. Root §§3–4: all six-cycle cases

Deleting the two marked edges leaves two disjoint paths. Cross nonedges
force each to have length at least two, and a six-cycle forces equality.
The two listed endpoint pairings exhaust the cases; a z midpoint is
impossible and the simple cycle cannot have two m occurrences.

For pairing I the simultaneous bounds a0,c0<=5 contradict the same
original degree sum. For pairing II the actual complementary disk has
the four-terminal order `(w,v,q,p)`, including the literal alpha=p and
beta=q endpoint cases. The perturbation into disjoint small path
neighbourhoods justifies use of the disk crosscut separation theorem
even when a midpoint lies on the boundary. No interior-vertex premise
is needed.

Both m exceptions in root §4 were checked separately in the original
graph:

| Path through m | Original cap | Complete fixed exterior link | Forced degree and contradiction |
| --- | --- | --- | --- |
| `v-m-p` | `(t,p,q,h,w)` | `t,a,b,q` at p | `p=5,a0=4`, contradicting `p=5=>a0>=6` |
| `w-m-q` | `(s,q,p,h,v)` | `s,c,b,p` at q | `q=5,c0=4`, contradicting `q=5=>c0>=6` |

For each empty cap the three forbidden diagonals leave exactly the two
diagonals stated by the root. For each nonempty cap the W5 conclusion
fixes the entire remaining link. The complete-link calculation in
B/check.py independently checks both labelled original cases. Neither
case uses v5, w5, the H compulsory-colouring rows, or a support reflection.

## 3. Root §5: arbitrary cyclic cuts

The conclusion quantifies over cuts whose two induced sides each contain
a cycle; it does not assume the sides connected. If one side is
disconnected, one of its components K has a cycle and its complement
contains the other side's cycle. A three-edge cut therefore cannot be
delta(K), since neither side is a single vertex. At least four edges
leave K; every further component costs at least three. These sets of
exiting edges are disjoint because they are distinct components of the
same induced cut side. Thus a disconnected side costs at least seven
edges, and both sides of a cyclic cut of size at most six are connected.

The resulting bond corresponds to a single simple primal circuit in
the actual planar duality. Marked dual edges retain their primal names.
The five-or-fewer exclusion and full six-cycle exclusion then prove
the stated size-at-least-seven bound for every marked cyclic cut. No
assumption that every primal six-cycle is cyclic on the dual side is
introduced.

## 4. Root §6: exact exchange identity and stopping boundary

A direct enumeration of the eight possible toggle masks on `(e,f,g)`
gives precisely:

| Starting membership | Toggle masks entering `110/101` | Result |
| --- | --- | --- |
| `110` | `000`, `011` | `110`, `101` |
| `101` | `000`, `011` | `101`, `110` |
| `111` | `001`, `010` | `110`, `101` |

For a vertex-disjoint family of actual alternating cycles, the edge-set
membership is exactly this toggle indicator, and symmetric difference
is a perfect matching of the same D. Therefore the root's iff condition
from the joint family is correct: e does not flip and f,g flip equally.
The separate 111-start requirement is that e does not flip and exactly
one of f,g flips. Preserving these identities alone does not establish
strict odd-cycle descent; the root correctly leaves that obligation
open. The theorem constrains primal marked cycles/dual marked cuts and
does not bound odd-complement cycle lengths.

The adoption does not prove `omega_e=0`, `W110+W101>0`, or source
realizability. Actual source instances remain zero, **not triggered**.
No root/shared file was edited during this review.
