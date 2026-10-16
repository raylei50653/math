# The seven-cut exterior is a fixed bipartite matching interface

Task `R6-SEVEN-DISK-RIGIDITY`, BASE
`120aae90cab8bc4881916adc598cf344f2f20f4b`. This note uses the frozen
[seven-disk proof](../2026-10-16-r6-101-nonwheel-seven-cut-120aae9/PROOF.md)
and [complete matching contract](../2026-10-16-r6-101-nonwheel-seven-cut-120aae9/MATCHING.md).
It introduces no external theorem and uses no four-colour theorem. Every
statement concerns the original minimum C5 source, its ordered pins and
rotation, the same legal J, its actual spherical dual D, the literal
marks e=(vw)*, f=(pq)*, g=(mz)*, and one hypothetical fixed maximum-cardinality
101 barrier S. There is no replacement source or independently chosen exterior.
The [general geometry proof](PROOF.md) in this audit now excludes this entire
seven-barrier case and proves ordinary101 nonemptiness. The conditional
exterior lemmas below remain valid; by themselves they establish neither
that exclusion nor even-complement positivity.

## M1. Exact exterior structure

Write s=|S|, X=V(e) union V(g), and H=D-X-f. The adopted seven-cut
case has s+2 odd components of H-S: the unique nonsingleton
factor-critical disk C and a set A of exactly s+1 singleton components.
Put B=S union X. All these sets are literal vertex sets of D. The
adopted cut budget gives

`E_D(S)=E_D(S,X)=empty`, `D[X]={e,g}`.                 (M1)

The adopted common-111 saturation gives f between two different odd
components, with neither endpoint in S or X. Since all other components
are singleton, f either joins C to one vertex a of A, or joins two
distinct vertices a,a' of A. There is no other edge between different
components of H-S. Consequently:

* In the actual exterior L=D-C, the only B-B edges are e and g.
* The only possible A-A edge is f; it occurs exactly when f is external.
* Every cut edge from C ends in B, apart from f when f crosses C.
* Each vertex of A has no edge to C except that possible f.

This is an exhaustive list, including possible repeated external cut
endpoints. Contraction of C therefore gives the exact skeleton with
parts {C} union A and B, of sizes s+2 and s+4, and only three same-part
edges f and e,g. Contraction here is a description; it is not a change
to the source used in any colouring or matching argument.

## M2. All 101 exterior fibres are empty before inspecting C

Let b_i=u_i v_i, i=0,...,6, be the seven actual cut edges in their
source cyclic order. For EVERY subset T of these labels, define the
complete exterior fibre E_T^101 as in the frozen matching contract:
selected b_i are retained literally, their outside endpoints are
removed from L, all remaining exterior vertices must be perfectly
matched, e and g are required, and f is forbidden. Repeated selected
outside endpoints make the fibre empty.

**Theorem M2.** `E_T^101=empty` for all 128 subsets T.

**Proof.** Edges e,g match every vertex of X. A selected edge ending
in X is therefore disallowed; a selected f is also disallowed. M1
then says that every allowable selected cut edge ends in S. All s+1
vertices of A remain in the exterior. Since f is forbidden, and their
edges to X cannot be used, each must be matched to a different remaining
vertex of S. There are at most s such vertices, and fewer if a cut edge
was selected. This is impossible. The argument also covers T=empty
and subsets of either parity. QED.

This is an exact localization of the obstruction, not a new proof of
101 existence or a source exclusion. In particular, changing only the
interior of C while retaining the same seven cut incidences and literal
exterior cannot create an ordinary101 matching, regardless of the
interior order, complete matching fibres, or complement parities. Any
source-preserving reduction must also address this exterior obstruction,
or prove that this whole exterior/patch pair cannot occur. The statement
is unconditional about this fixed exterior and does not assume that a
proposed replacement is source-realizable.

## M3. Complete 111 support reduces to one fixed bipartite graph

The same nonempty P111 family is tight on C. Its decomposition remains

`P111 = disjoint union_j PM(C-u_j) times E_{ {j} }^111`.    (M2)

Every internal member extends with EVERY exterior witness in its same
cell. No matching or empty fibre is removed.

If f crosses C at port j_f, its requirement and tightness imply that
j_f is the ONLY supported port. Write a in A for its exterior endpoint.
After removing X and a, E_{ {j_f} }^111 is in literal bijection with

`PM(D[S,A-{a}])`,                                         (M3)

a balanced bipartite graph on s+s vertices. The selected cut edge is
f, and e,g are supplied unchanged. All other E_{ {j} }^111 are empty.
Nonemptiness follows here from the existing same-source P111 member;
(M3) is not an independent existence theorem.

If f is external between a,a' in A, supported ports must end in S.
Put A'=A-{a,a'} and fix the ONE bipartite graph

`K=D[S,A']`, `|S|=s`, `|A'|=s-1`.                         (M4)

For every port j with v_j in S,

`E_{ {j} }^111 <-> PM(K-v_j)`,                            (M5)

by supplying the same e,g,f and b_j. For v_j in X the exterior cell is
empty. Thus the supported external endpoints are precisely those S
vertices exposable by a matching of K saturating A'. Different port
labels with the same endpoint have the same underlying bipartite
matching fibre, but retain their different selected cut edge. The
hypothesis s>=1 in this case follows from |A|=s+1>=2.

For completeness, this support can be tested without selecting a new
exterior for each port. Fix ANY matching Q of K saturating A', and let
r be its unique exposed S vertex. Direct each non-Q edge from S to A'
and each Q edge from A' to S. Then v in S is exposable iff v is reachable
from r by a directed alternating path (the zero-length path includes
r). Flipping such a path exposes v. Conversely compare Q with any
matching exposing v: their symmetric difference has an alternating
path from r to v, along with cycles, and yields the directed path.
This is an exact all-lifts support description on one unchanged K.

## M4. Every actual 111 exterior path and cycle is even

**Theorem M4.** For every exterior witness in (M2), its internal
complement cycles are even, and EVERY complement path between unselected
cut incidences has even internal edge length.

**Proof.** Remove its matching edges from L, retaining the vertices
whose matching edge crosses the cut. The only possible same-part edges
of L are e,g,f by M1. All present ones belong to the 111 matching and
have been removed. The exterior complement is therefore bipartite
with the fixed parts A and B. Its cycles are even.

Every unselected cut incidence ends in B. Indeed the only possible
exception is the A endpoint of a crossing f; that f must be selected.
The exterior complement paths consequently have both endpoints in B,
so have even length. Two cut incidences may meet the SAME exterior
vertex; their connecting path then has length zero and is still even.
Cubic degree and the matching condition give exactly two incidences
at every complement vertex, so these paths and cycles exhaust the
exterior complement. QED.

This removes the previously unrestricted exterior parity vectors on
THE ACTUAL barrier, simultaneously for every complete 111 exterior
matching. It does not assert that all combinatorial pairings are
realizable, nor identify exterior matchings merely because they have
the same pairing. All their edge lists, paths, cycles and lifts remain
in their fibres. Since the actual exterior lies on the complementary
side of the same disk, its pairing is also noncrossing in the reversed
boundary order. The order-reversal leaves the set of noncrossing
pairings unchanged.

## M5. Exact even111 join and the 140 eligible internal signatures

Retain the frozen internal signature (j,pi,alpha,eta), its complete
PM(C-u_j) fibre, all paths and cycles, and all empty cells. There are
560 registered tight signatures, of which 140 are universally empty
by the adopted complement edge-count parity; at most 420 ordinary
signatures remain possible. Those statements are unchanged.

For any fixed literal internal/exterior pair in (M2), M4 specializes
the adopted parity join to

`M is even <=> eta=0 and xor_{p in Z} alpha_p=0`
`for every connected component Z of pi union pi_ext`.      (M6)

There is no exterior odd-cycle bit or nonzero exterior path parity to
choose. A component of the union of the two pairings represents one
actual global complement cycle; its cut-edge count is even. Its parity
is exactly the sum of the internal path parities. The other global
cycles are the recorded internal and exterior cycles, establishing both
directions of (M6).

In particular eta=0 is necessary. For tight internal complements the
adopted edge-count identity already gives sum alpha=0 mod 2 when eta=0.
The number of ELIGIBLE internal signatures for an even111 lift is thus

`7 selected ports * 5 pairings * 4 even-total vectors = 140`. (M7)

This is an upper bound on eligibility before imposing the componentwise
join equations, source geometry and actual exterior support. It does
not claim that these 140 cells are nonempty, that they all have an
exterior realization, or that every eligible pair is compatible. The
other 280 potentially ordinary signatures with eta=1 keep their full
ordinary matching lifts and EMPTY even111 fibres. The [source C5 complete-row proof](../2026-10-16-r6-joint-zero-c4c3d99/C/PROOF.md#c5-a-guaranteed-complete-all-equal-starting-state)
supplies a complete J colouring whose three literal differences coincide.
Its corresponding common-colour matching is an even111 member. This uses
the adopted complete Sigma319 row and all-r transfer, not a general
colourability assertion. Thus at least one of the 140
eligible cells really has a compatible full internal/exterior pair.

For each compatible pair, retain both alternating assignments of the
other two named colours on EACH actual even global complement cycle.
Taking their Cartesian product supplies every full labelled Tait lift;
an incompatible pair has an empty Tait fibre. This preserves complete
colour lifts and never combines marginal witnesses. The 140-signature
bound concerns this even111 subfamily and does not strengthen ordinary
matching existence, positive W110+W101, source realization, or Lean.

## M6. Exact finite calibration and scope

[matching_check.py](matching_check.py) uses only the Python standard
library. Its controls glue two declared factor-critical seven-port
patches (C7, and C9 plus chord 0-4) to two fixed exteriors. One has f
crossing C; the other has f external. The external vertices on two
pairs of ports are deliberately repeated, so the zero-length convention
is tested on actual full matching records. Every one of the 128
boundary cells and 1206 ordinary state cells is retained, including
empties; every global PM, complete complement cycle and full labelled
Tait assignment is retained. The checker compares literal restriction/
union lifts to direct whole-graph enumeration, tests (M3)--(M6), and
checks all 101 exterior cells empty. Its final replay certificate is
[matching_certificate-v3.json](matching_certificate-v3.json). The initial and v2
certificates are retained as earlier finite calibrations; v3 adds positive
and empty even111 witnesses, spherical rotations, and a nontrivial alternating
support control. Normal/seed17 replay and deliberate missing-empty, path-parity,
zero-length and Tait-lift corruptions are recorded in
[matching_verification.json](matching_verification.json).

The complete global PM counts for C7/crossing-f, C7/external-f,
rotated-theta/crossing-f and rotated-theta/external-f are respectively
10, 11, 15 and 16. Their P111 counts are 1, 1, 2 and 2; their even111
counts are 0, 0, 1 and 1. Thus both the positive and empty sides of
(M6) are exercised, with odd-complement ordinary111 records retained.
The fixed-K support control has three exposable S vertices reached by
alternating paths and one unexposable vertex, with its empty fibre explicit.

These small controls calibrate the algebra only. They do not satisfy
the original source contract: their patches have fewer than five odd
primal interior vertices; in particular no source or globally minimum
source is claimed. No finite zero count is used as an arbitrary-size
source exclusion. The paper proofs M1--M5, the finite certificate and
the existing Lean build are separate evidence layers. No Lean theorem,
source replacement, smaller completed source or new reconstruction cost
is asserted. The general geometry proof in this audit excludes the hypothetical
seven-barrier and, with the adopted earlier barrier exclusions, proves
ordinary101 nonemptiness. That conclusion uses the geometry paper, rather
than the finite controls or these exterior lemmas alone. An ordinary101
matching may still have odd complement: W101 positivity, positive joint
W110+W101, omega=0, complete319 exclusion and the general source theorem
remain OPEN.
