# B. Two complete complement cycles: universal reference obstruction and primal form

Frozen BASE: `3d325d7197aa05815c71bedc52c1b253d736c7bb`.
Independent write scope: this audit's `B/` directory. This paper audit
accepts the user's sections 1, 2 and the precise repair obligation in
section 5. It constructs no repair and no original minimum source.

## 1. Source contract and evidence used

Keep the same original minimum completed no4ct C5 source G, ordered
outer frame `(x,y,a,b,c)`, original apexes `(r,t,p,q,s)`, original
supports, attachments, rotation and private vertices. Keep the complete
U319 relation on `(z,s,v,w,t,p,q)`, every empty complete fibre and every
legal original r lift. The actual graphs and literal marks remain

`J=U/(s=t)`, `m=[s=t]`, `D=J*`,
`e=(vw)*`, `f=(pq)*`, `g=(mz)*`.

There is no added original v-degree-five premise. Fix an actual ordinary
perfect matching `M in P101`, so `e,g in M` and `f notin M`, and put
`F=D-M`. Suppose F has a complete nonfacial seven-cycle C containing f.
The frozen [active-f B proof](../frozen/audits/2026-10-17-r6-active-f-seven-ffea555/B/PROOF.md),
sections 1--3, supplies the actual two-star disk K, its centres u,h
with `u in {p,q}`, the unique matching chord `(uh)*`, the five matching
spokes, and the simple boundary Q5. In particular

`V(Q5) intersect {m,z,v,w}={z}`.

All seven primal triangular faces in K are exactly the dual vertices
of C. The literal primal face `mvw` is retained from the sealed prior
[J geometry proof](../../2026-10-17-r6-active-f-seven-ffea555/frozen/audits/2026-10-15-j-source-geometry-6ddea32/PROOF.md),
section 1. This additional cited file is in the root
[INPUTS.json](../INPUTS.json) `previous_audit_inventory`, with SHA256
`ea1b16704a689dcf14e80ea232be2bfed114c5d5535b783d4d55b297cc576093`.

Sections 2--3 below need only a finite cubic graph, one perfect matching
M, and any actual perfect matching R whose **entire** complement is
even. Planarity, source minimality, FJ and cap geometry are unnecessary
there. The exact primal structure in sections 4--6 uses the embedded
spherical triangulation J and the full actual cap just specified.

## 2. Every full reference region contains an even number of old odd cycles

Let R be **any** actual perfect matching of D with even complement and
define the spanning exchange graph

`L_R=D-(M intersect R)=(D-M) union (D-R)`.

For every full connected component W of L_R, every cycle of D-R that
meets W is entirely contained in W. These cycles partition W and all
have even length; hence `|W|=0 mod 2`. Every F cycle that meets W is
likewise entirely contained in W. Counting the vertices of this second
partition modulo two gives

`odd(F[W]) = |W| = 0 mod 2`.                         (B1)

The quantifier is over all actual even-complement R and all full L_R
components. Neither partition may be replaced by a local cap piece or
an incomplete exterior path. This is the parity fact in the frozen
[C proof, section 2](../frozen/audits/2026-10-17-r6-active-f-seven-ffea555/C/PROOF.md),
with its universal quantifier retained.

If F has exactly two odd cycles C,C', they therefore lie in the same
L_R component for every such R. Additional even F cycles are allowed
in this statement; they need not lie in that same component.

If a literal edge g has an endpoint on C' and `g notin R`, its whole
edge lies in L_R. Thus in that case `W_C(R)=W_g(R)`. For every actual
all-distinct R100 reference, `g notin R100`, so the assertion applies
without independently changing any part of the reference colouring.

## 3. Exactly two full complement cycles force universal connectedness

Now assume the stronger hypothesis

`F=C7 disjoint-union O`,                            (B2)

with exactly these two full components. D has even order because it has
a perfect matching. Since C7 has odd order, O also has odd order. By
(B1) the two cycles lie in the same L_R component for every actual
even-complement R. They span all vertices, so

`L_R is connected for every actual even-complement R`. (B3)

The actual source has complete all-distinct colourings. For every one
of them, its simultaneously selected class R100 is an even-complement
reference with `e in R100`, `f,g notin R100`. Therefore

`W_C(R100)=W_g(R100)=V(D)`,
`|W_g(R100)|=|V(D)|`.                               (B4)

For this fixed M, the reference minimization objective is constant.
Switching actual complete colourings, mixing palette moves, or even
allowing every actual even-complement matching cannot yield SEP.
There is no contradiction with the correct conditional descent theorem:
its SEP hypothesis is simply unavailable under (B2). This does not
prove that an original minimum source realizes (B2), and does not
exclude that source subcase either. It proves that its next obligation
must modify M or exclude the subcase by another argument.

The distinctions matter: with merely two odd cycles and additional
even cycles, (B1) forces the odd pair together but does not force all
of L_R to be connected. An R with odd complement has no such parity
authority. The small controls in section 8 check both boundaries.

## 4. The spanning primal matching graph has three components and one cycle

Continue under (B2) and define the embedded spanning graph

`P=(V(J),M*)`, `n=|V(J)|`.

The spherical triangulation J has `2n-4` triangular faces, so D has
`2n-4` vertices and `|M|=n-2`. Thus `|E(P)|=n-2`.

For any embedded spanning primal subgraph, its faces correspond to
connected components of the dual graph on the omitted primal edges.
Here those dual edges are precisely `D-M=F`. One can see this directly:
two triangular face interiors of J are in the same face of P exactly
when one can pass between them across edges absent from P. The dual
path witnessing that passage lies in F, and conversely every F path
gives such a passage. This argument includes isolated primal vertices.
Consequently P has exactly two faces. The disconnected plane Euler
formula gives

`n-(n-2)+2 = 1+kappa(P)`,
`kappa(P)=3`,
`beta1(P)=|E(P)|-|V(P)|+kappa(P)=1`.               (B5)

The five actual matching spokes give all five actual rim edges of
`Q5 subseteq P`. This is a simple cycle, so the total cycle rank one
in (B5) proves it is P's unique simple cycle. In particular P has one
unicyclic component and two tree components; any other P edge is a
bridge. A different cycle hidden in a remote tree would contradict
the total cycle rank, independently of its length or location.

## 5. Integrating the binary assignment on the same primal graph

Every triangular face of J has exactly one edge in P, since its dual
vertex is incident with exactly one edge of M. Label each primal edge
by `d(uv)=0` on P and `d(uv)=1` outside P. The sum of d on every
triangular facial boundary is `0+1+1=0` in F2. Every closed walk in a
spherical triangulation is generated modulo two by its facial
boundaries. Thus path integration defines a consistent assignment
`sigma:V(J)->F2`, unique up to global interchange, with

`d(uv)=sigma(u)+sigma(v)`,
`uv in P iff sigma(u)=sigma(v)`.                   (B6)

Equivalently one may integrate along any spanning tree and use the
facial equations to check all remaining edges. Only this one actual
P is used; sigma is not a claimed full U319 colouring or a new legal
lift. It is a binary assignment on J defined by this M.

Normalize Q5 to value zero. The facts needed to locate the components
are all literal edges and faces:

* `z in Q5` gives `sigma(z)=0`; `mz in P` gives `sigma(m)=0`.
* Every centre-to-rim edge has dual on C and is outside M. The centres
  therefore have value one. The common edge `uh in P` is consistent
  with this assignment.
* In the actual face mvw the selected edge is `vw in P`. Hence the
  other two edges mv,mw are outside P, giving
  `sigma(v)=sigma(w)=1`.

The centre component is exactly the actual `K2` on u,h. Indeed all
primal faces incident with either centre are among the seven faces
of K. The only M edge dual to a centre-incident primal edge is the
unique internal chord `(uh)*`; all other centre-incident primal edges
dualize to C edges. Thus `deg_P(u)=deg_P(h)=1` and no exterior P edge
can leave this K2.

The connected Q5 component has value zero. The connected subgraph
`vw` has value one and is outside the complete centre K2; hence it is
in a third component. These three components already exhaust (B5).
Every value-zero vertex, and in particular both m and z, must therefore
belong to the Q5 component. There is no possible additional value-zero
component, since that would give at least four components. The direct
edge mz also forbids separating m from z in P.

We have proved the exact structural description:

| Full P component | Required actual vertices/edges | Full structure |
| --- | --- | --- |
| Centre | `u,h,uh` | Exactly `K2` |
| Outer value-one | `v,w,vw` | A tree |
| Rim value-zero | `Q5,m,z,mz` | Unicyclic, unique cycle Q5 |

Since neither vw nor mz lies on Q5, both are bridges. Deleting the
cycle edges from the unicyclic component leaves trees, each containing
exactly one Q5 vertex. The tree containing mz has root z because mz is
incident with z. Thus mz lies on the branch attached at z, with its m
endpoint away from Q5. All other vertices of that component likewise
belong to trees attached to its unique Q5.

The proof is unchanged for the q-centred cap: use its literal centre
u=q and its actual ordinary centre h on this same source.

## 6. The primal explanation applies to every actual even reference

For any actual even-complement R, alternately colour every even cycle
of D-R with two Tait colours and give R the third Tait colour. At each
dual vertex the three colours are distinct. Interpret the three
colours as the three nonzero elements of `F2^2`; the triangle equation
is their zero sum. Spherical integration gives a primal four-colouring
in which every R* edge has the same nonzero difference alpha. This
integration concerns R on this same J and asserts no new original
source lift.

Set `S_R=(V(J),(M intersect R)*)`, a spanning subgraph of P. Every
cycle in S_R must be even: along a cycle of length k its integrated
difference is `k alpha=0`, and alpha is nonzero. But P's only simple
cycle is the odd Q5. Consequently S_R has no cycle and is a forest.
A spanning forest embedded on the sphere has one face, including when
it has several components or isolated vertices. The omitted-edge dual
of S_R is L_R, so L_R is connected. This independently recovers (B3)
from the precise primal form and uses all actual common edges at once.

## 7. Exact next matching-repair obligation

Under (B2), the presently unproved task is to construct a collection
`A` of actual pairwise vertex-disjoint M-alternating simple cycles,
write `T=E(A)`, and require

`e notin T`,
`f in T iff g in T`,
`all full cycles of D-(M triangle T) are even`.    (B7)

Alternating means that on each cycle membership in M alternates;
simultaneously flipping these disjoint cycles therefore gives an
actual perfect matching `N=M triangle T` of the same D. The first
two conditions in (B7) are exactly equivalent to
`N in P101 union P110`: e stays selected; with f initially absent and
g initially present, either neither is toggled, giving 101, or both
are toggled, giving 110. Toggling just one gives 100 or 111. Conversely,
any perfect matching N in the joint family has symmetric difference
with M consisting of precisely such vertex-disjoint alternating
cycles and obeys these mark conditions.

Initially the complete oddness is exactly two. Any strict decrease of
the **full** odd-cycle count is therefore zero, because every spanning
2-factor on the even-order D has an even number of odd cycles. Thus
a genuine strict joint-family descent suffices in this branch, and
produces an even-complement matching. It is insufficient to repair only
the local C7 or to ignore the remote O cycle.

The three-component P form and the all-reference obstruction define a
precise next target. They do not construct A, prove any strict descent,
or provide positive `W110+W101`.

## 8. Small controls and evidence boundary

[check_controls.py](check_controls.py) has two explicitly supplied,
connected simple cubic graph controls. It enumerates all their perfect
matchings, checks (B1) for every even-complement reference, and records:

* On the triangular prism with M equal to its three rungs, F consists
  of exactly two triangles. All three even-complement references give
  connected L_R. The non-even reference R=M gives disconnected L_R,
  showing why the even-complement premise cannot be removed.
* On an explicitly supplied ten-vertex graph, F consists of two
  triangles and a square. An explicit even-complement R gives L_R
  components of orders six and four: the two odd cycles are together,
  but the extra even cycle is separate. Thus the two-odd-cycle lemma
  must not be strengthened to universal connectedness.

These are graph-theoretic scope controls, with **no** U319 relation,
actual source frame, source colouring/lifts, seven-cap or minimality
claim. They are not original-source controls or counterexamples. The
paper statements are proved above without any finite-search premise.
Normal and `PYTHONHASHSEED=17` read-only outputs are recorded in
[controls.log](controls.log) and [controls-seed17.log](controls-seed17.log).
The malformed-reference negative check is part of that same replay.

All source realizability remains `not triggered`: no actual minimum
source is supplied. There is no new external theorem, 4CT invocation,
Lean theorem, or general even-complement conclusion. The active-f
seven-cap, its two-cycle matching repair, other odd complements,
H-connected case, `W110+W101>0`, `omega_e=0`, and full319 remain OPEN.
The original completed-source reconstruction cost remains `k+5`.
