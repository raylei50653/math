# C. Affine marked repair and the rank of the obstruction

Frozen BASE: `9f1fe84f73aabfa87a33d28754633bae6bf0b707`.
Exclusive output scope: this audit's `C/` directory.
This is a paper theorem about arbitrary finite loopless cubic graphs, followed
by its same-source specialization and separate finite controls.

## 1. What is retained, and what is abstracted

The source specialization retains the original minimum completed no4ct C5
source, its ordered contacts, rotation, attachments, complete U319 relation
including empty fibres and every legal original r lift. It retains the actual
`J=U/(s=t)`, `D=J*`, and literal marks `e=(vw)*`, `f=(pq)*`, `g=(mz)*`.
No matching from another source, independently selected exterior, or partial
colouring is substituted. The actual objective is the joint family
`P101 union P110`; no separate positivity of its two summands is requested.

The frozen seven-five A proof, sections 3--4, already proves exact whole-cycle
surgery and full-reference-component repair. The frozen two-cycle B proof,
sections 2--3, already proves even parity of the old odd-cycle count in every
full region and universal connectedness when the old complement consists of
two odd cycles. This note abstracts **marked constraints**, independently of
cap shape, defect size, graph order, and number of complementary components.
It does not claim the existing repair lemma or ordinary matching reachability
as a new result.

## 2. General affine marked family

Let D be a finite loopless cubic graph and E its actual edge set. Parallel
edges, if present, are retained as different edge identities. For a matching
M, write chi(M) in F2^E for its edge-incidence vector. Fix a linear map

`A : F2^E -> F2^d`

and a vector b. Its columns can be zero on all unmarked edges. The family is

`F_b = {perfect matchings M of D : A chi(M)=b}`.

Fix `M in F_b`. Write `F=D-M` and let R be an actual perfect matching of the
same D whose **entire complement** `F_R=D-R` is even. No condition
`R in F_b` is imposed. Define the complete exchange graph

`L_R=D-(M intersect R)`.

For every full connected component W of L_R define

`T_W=(M triangle R) intersect E(D[W])`,
`q_W=number of odd complete F cycles contained in W`,
`s_W=A chi(T_W)`.

Every F or F_R component meeting W is entirely contained in W. Since the
F_R cycles are even and partition W, `|W|` is even and `q_W` is a
nonnegative even integer. Every boundary edge of W is in `M intersect R`.
Thus T_W is a union of full actual alternating difference cycles, with no
unfinished outside path.

## 3. Exact safe-batch criterion and rank theorem

**Theorem C1 (affine complete-region repair).** For any subset S of the full
components of L_R, set

`N_S=M triangle (union_{W in S} T_W)`.

Then N_S is an actual perfect matching of D and

`odd(D-N_S)=odd(F)-sum_{W in S} q_W`,
`A chi(N_S)=b+sum_{W in S} s_W`.

Consequently this batch is a strict repair inside F_b exactly when

`sum_{W in S} s_W=0` and `sum_{W in S} q_W>0`.       (C1)

**Proof.** All difference cycles are vertex-disjoint. Flipping a selected
union preserves the matching condition. On a selected W the new complement
is exactly F_R restricted to W; on every unselected component it remains F.
Common boundary matching edges stay selected. Hence the whole-complement
oddness changes by exactly the indicated sum. Symmetric difference is vector
addition over F2, so the marked equation follows from linearity. QED.

Let Z be the linear span of all s_W with q_W=0, and let I be the set of
components with q_W>0.

**Theorem C2 (exact obstruction rank).** There is no batch satisfying (C1)
if and only if the images of `(s_W)_{W in I}` are linearly independent in
`F2^d/Z`. In particular, if M globally minimizes oddness over F_b, then

`|I| <= rank(A)-dim(Z) <= rank(A)`.                (C2)

More precisely, replace rank(A) in the first inequality by the dimension of
the span of all available s_W if that span is smaller.

**Proof.** A dependence of the positive-region images means that a nonempty
subset I' of I has syndrome sum in Z. By the definition of span over F2,
this syndrome equals a sum of a subset of zero-gain region syndromes. Select
I' and that subset. Their total syndrome is zero, while their gain is
positive. Conversely any positive-gain zero-syndrome batch selects a
nonempty positive-region subset whose syndrome sum belongs to Z. This is a
linear dependence in the quotient. Independence gives the dimension bound.
A global minimizer admits no strict family repair, so it satisfies that
bound. QED.

This is an exact criterion for the specified full-region operations. It is
not a completeness theorem for all alternating-cycle repairs. The quantity
bounded is the **number of odd-containing regions**, not their orders, their
boundary sizes, or the number of odd cycles inside one region.

## 4. The literal joint family has two equations

For the actual three marks define

`A chi(N)=(chi_e(N), chi_f(N)+chi_g(N))`, `b=(1,1)`.

The allowed mark patterns are exactly 101 and 110. Thus the ordinary joint
family is affine of rank two, and its objective is one minimization over the
union. For any actual even-complement R, an oddness minimizer M in this family
has at most two full L_R components containing old odd cycles, subject to the
stronger quotient condition in C2.

If R retains e, every available component syndrome has first coordinate
zero. The effective rank is at most one. If M is odd, exactly one full region
contains **all** its odd complement cycles. For M101:

* An R111 reference changes f and keeps e,g, so the only nonzero component
  syndrome belongs to the region containing the actual f edge.
* An R100 reference changes g and keeps e,f, so the only nonzero component
  syndrome belongs to the region containing the actual g edge.

For M110, interchange f and g in the corresponding statements. These recover
the previous one-blocker result while making its source-independent reason
explicit. Any actual even reference already in the joint family would make
the minimum zero; that case needs no repair theorem.

A zero-gain component can matter: its syndrome can cancel the marked cost of
a positive-gain component. C2 therefore quotients by their span instead of
checking only positive regions or requiring each region to be safe separately.

## 5. Compatible repairs from different references

**Theorem C3 (disjoint full-region gluing).** Let W_1,...,W_t be pairwise
vertex-disjoint full regions, where W_i may come from a different actual
even reference R_i. Compute T_i,q_i,s_i against the same original M and
same A. Then flipping the union of T_i is a perfect matching, its total
oddness gain is `sum q_i`, and its syndrome is `sum s_i`.

**Proof.** Every T_i is contained in W_i, and every boundary edge of W_i
is an unchanged M edge. Disjoint supports therefore allow the same matching
and complement gluing argument as C1. Every old F cycle meeting W_i lies
wholly there, so no complete old cycle or gained odd component is counted
twice. QED.

At a minimizer the syndromes of any pairwise disjoint positive-gain full
regions are independent, after accounting for any disjoint zero-gain regions.
This permits cross-reference batches when their actual supports are disjoint;
abstract syndromes alone do not authorize overlapping flips.

There is a stronger limitation in the present joint problem. For every
actual e-preserving even reference, its unique positive region at an odd
joint minimizer contains **all the same old odd F cycles**. Consequently
positive regions from any two such references automatically overlap on every
old odd F cycle. Mixing disjoint whole regions from these references cannot
produce a new descent at that minimizer. In particular, a proposed 111-region
plus 100-region direction-changing repair is valid when disjoint, but
minimality already forces its disjointness premise to fail.

The exactly-two-odd-cycle obstruction is a special case: the parity of each
q_W puts that pair together for every even reference, with or without an
e-preserving premise. If those two cycles span D, every L_R is connected.
Changing the reference does not then produce a smaller full region.

## 6. What this abstraction changes about the bottleneck

The theorem no longer depends on C7, five ports, a local wheel, a fixed
number of exterior cycles, or a bounded graph. Its hypotheses are a cubic
matching/complement pair, actual even references, and affine marked equations.
It separates two obligations:

1. **Repair verification** is exact and generic: zero total syndrome plus
   positive complete oddness gain.
2. **Repair existence** remains a source-specific problem. At a joint
   minimizer every e-preserving full reference repair is already concentrated
   in its unique blocked region. There is no additional separation lemma
   available merely by restating whole-region exchange.

A new argument must supply an actual partial-region surgery with complete
outside parity data, a different completed-source reduction, or another
source structural obstruction. Ordinary joint-family connectivity supplies
no monotone oddness path; a connected state graph can have local minima.
Neither a rank bound nor reachability makes `W110+W101` positive.

## 7. Finite scope controls

The stdlib-only [check.py](check.py) generates explicit cubic graphs and
writes [controls.json](controls.json). These controls have no U319 relation,
original attachments, minimum source, or source-realizability authority.

* All old perfect matchings and all even references on a 12-vertex expanded
  K4 are checked. Every subset of full regions is replayed, and both the exact
  oddness/syndrome identities and the quotient independence equivalence are
  verified.
* A connected 24-vertex simple cubic graph gives sharp rank two. The checker
  enumerates every perfect matching and an affine family with two equations.
  Its global minimum is four odd cycles. For an explicit even reference,
  a minimizing matching has two positive regions, each of gain two, with
  independent syndromes `(1,0)` and `(0,1)`. The equations differ from the
  literal source joint equations; this is sharpness of C2 in its general
  affine scope, not a claim of sharpness for the source specialization.
* An arbitrary-size construction concentrates arbitrarily many old odd
  cycles in one region: expand every vertex of an even Hamiltonian cubic
  base into a triangle, take M to be all external edges, and take R from
  the complementary base matching together with the appropriate internal
  triangle edges. The old complement consists of all `2k` triangles;
  the reference complement is one even `6k`-cycle and L_R is connected.
  Replays use `2k=4,6,8,16,32`. These M are not asserted to minimize a
  specific affine family. This control proves that the region count and
  component parity alone do not bound its internal odd-cycle count.
* Substituting the odd-complement reference R=M makes the even-region parity
  check fail, confirming that arbitrary ordinary references lack that
  premise.

The infinite concentration construction is immediate from its edges: the
reference omits each base-cycle external edge and retains the other external
edge at each triangle; its complement follows the base Hamiltonian cycle,
using two internal edges per triangle and one external edge per base step.
Its length is therefore `3*(2k)`. In L_R all triangles remain connected
along the same base cycle.

No external theorem, 4CT, Lean result, global closure, smaller bad source,
full319 exclusion, or positive joint even-complement count is claimed.
Original completed-source reconstruction cost remains `k+5`.
