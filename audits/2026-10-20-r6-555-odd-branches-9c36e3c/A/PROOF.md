# A. A ten-edge repair for the coupled 5/5/5 configuration

Frozen Git BASE: `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`.
Independent write scope: this audit's `A/` directory. The argument uses
only the frozen previous batch proof, its B proof, and the frozen
literal-source geometry. It proves an arbitrary-size conditional
theorem. It does not construct or certify a new original source.

## 1. Authority and exact hypothesis

Retain the same globally minimum completed no4ct C5 source G, its
secondary maximum-edge choice, ordered frame `(x,y,a,b,c)`, actual
attachments and rotations, complete U319 fibres including empty fibres,
every full original lift, and all original r lifts. Work in the same
literal graphs

`J=U/(s=t)`, `m=[s=t]`, `D=J*`,

with the same named marks `e=(vw)*`, `f=(pq)*`, `g=(mz)*`.

**Local notation.** In the local rotations and exchange below,
`t=τ` denotes the actual outer third vertex of AB. It is not the
original split apex t appearing in `J=U/(s=t)`, whose quotient image
is m. Likewise the local neighbours `a=α`, `b=β`, `c=ξ` below are
labels for actual J vertices; they do not reassign the ordered
original source contacts a,b,c. This convention applies to every
local face label, set X, and component formula below.

Fix the same actual `M in P101` with full complement `C7 disjoint-union O`,
where both cycles are odd and C7 is the active-f nonfacial seven-cycle.
No source relation, quotient, attachment, rotation, or matching is
replaced by a control graph.

The frozen previous proofs give

`P=(V(J),M*) = K2 disjoint-union T disjoint-union U0`.

Here `K2={u,h}`, u is p or q and has J degree four, h is the ordinary
centre of J degree exactly five, T is the tree containing vw, and U0
is unicyclic with unique rim Q5 and mz in the branch at z. The fixed
weak binary colouring takes value one on K2 and T, zero on U0; P is
exactly its set of equal-value edges. Every actual triangular face has
exactly one P edge. J is simple and every triangle is facial.

Let A and B be the two safe consecutive rim vertices r45 and r56.
Write L for the other rim neighbour of A and R for the other rim
neighbour of B. The actual rim order has the segment `L,A,B,R`.
The centre star is exactly

`N_J(h)={u,L,A,B,R}`,

with cyclic order `u,L,A,B,R` or its whole-source reversal. This is the
five-degree centre star of the literal C7 cap, not an added degree
assumption. Its five triangles are `huL`, `hLA`, `hAB`, `hBR`, `hRu`.

Assume the conditional degree pattern

`d_J(A)=d_J(B)=d_J(t)=5`, `t notin {v,w}`,

where t is the actual outer third vertex of the rim edge AB.
The previous B proof establishes t in T and the actual local rotations
below. For completeness, the needed derivation is repeated in section 2.
The two branches of T-t may have odd degree parity as in the requested
subcase. The construction will also work if both are even.

For each vertex set S put

`q(S)=sum_{x in S} d_J(x) mod 2`,

always using full degrees in the original J. The frozen full-component
calculation gives `q(K2)=q(T)=1` and `q(U0)=0`.

## 2. All four rotations are actual and complete

For any original vertex x the number of triangular faces at which x
is the minority binary value is

`k(x)=d_J(x)-2 d_P(x)`.

The two Q5 neighbours of either safe rim vertex are P neighbours.
Since its degree is five, the inequality `2 d_P(x)<=d_J(x)` forces
`d_P(A)=d_P(B)=2`. Thus neither A nor B has an attached U0 tree.
The complete stars of A and B have the forms

`A: h,L,a,t,B`,

`B: h,A,t,b,R`,

up to reversing the entire source. Here a,b lie in T and the actual
faces include `Aat`, `Btb`. Consequently ta and tb are P edges.
The vertices a,b are distinct: otherwise A and B would have a common
neighbour other than their two facial third vertices h,t, contradicting
the frozen facial-triangle property.

At t there are already the consecutive neighbours a,A,B,b. Since t
has degree five, its remaining neighbour is a vertex c, with rotation

`t: a,A,B,b,c`.

The vertex c lies in U0: ta and tb are already two P edges at a
degree-five vertex, so no further P edge is possible. No centre vertex
can be adjacent to T. In particular `d_T(t)=2`, and the remaining two
faces are `tbc` and `tca`. The vertex c is distinct from A,B, hence
belongs to `U0-{A,B}`. It is also distinct from L,R: for example c=L
would make L a third common neighbour of A,t in addition to a,B.

This establishes all incident faces of h,A,B,t in the original rotation.
There is no appeal to a redrawable abstract planar control.

## 3. The actual alternating ten-cycle

Take the actual vertex set

`X={h,A,B,t}`,

and let `Q=(delta_J(X))*` in the fixed dual D. Its five internal primal
edges are exactly `hA,hB,AB,tA,tB`; its two internal primal faces are
`hAB` and `tAB`. Its boundary in the dual is the following actual cycle
of ten distinct dual vertices, written by their original primal faces:

`huL, hLA, ALa, Aat, atc, tcb, tbB, BbR, BRh, hRu, huL`.

The ten primal edges crossed by this boundary, in the same cyclic
order, are

`hL, LA, Aa, at, tc, tb, bB, BR, Rh, hu`.

Their P membership alternates exactly as follows:

`not-P, P, not-P, P, not-P, P, not-P, P, not-P, P`.

Therefore Q is a simple ten-edge M-alternating cycle, in the original
rotation. One can also verify its length directly:

`|delta_J(X)|=5+5+5+5-2*5=10`.

The displayed face list proves simplicity as well as the local
alternation. All boundary triangles have the cut sides prescribed by
their actual stars; the internal faces `hAB` and `tAB` are not cut.

The matching

`N=M symmetric-difference E(Q)`

is consequently an actual perfect matching of the same D. Equivalently,
flip the binary value on exactly X. Its full equal-value graph is
`P_N=(V(J),N*)=P symmetric-difference delta_J(X)`.

All four selected vertices avoid the endpoints of e,f,g. The safe
rims A,B avoid all six named endpoints. The ordinary centre h is
neither centre u nor any named rim/branch endpoint. The vertex t lies
in T and is explicitly different from v,w; the other marked endpoints
lie in the centre or U0. Hence the cut crosses none of vw,pq,mz.
The same marks are retained, and `N in P101`.

## 4. Every full new component and its parity

Since A,B have no attached U0 trees, deleting them leaves the one
connected U0 component containing the remaining rim path from L to R.
Since `d_T(t)=2`, deleting t leaves exactly the two complete branches
T_a and T_b containing a,b. The full components after the switch are
exactly

1. `H0={u}`;
2. `H1={A,B} union (T-{t})`;
3. `H2={h,t} union (U0-{A,B})`.

This list follows from all changed equal-value edges. The centre
edge hu is removed. The old rim edges LA,BR are removed, while AB
remains and joins A and B. The old tree edges ta,tb are removed;
the new equal-value edges Aa,Bb join the two complete T branches
through the retained edge AB. Finally hL,hR and tc become equal-value
edges, joining h,t to the full remaining U0 component. All other
equal-value edges are unchanged. No vertex or residual attachment
is omitted.

Their full original degree parities are

`q(H0)=d_J(u)=0 mod 2`,

`q(H1)=q(A)+q(B)+q(T)+q(t)=1+1+1+1=0`,

`q(H2)=q(h)+q(t)+q(U0)+q(A)+q(B)=1+1+0+1+1=0`.

In particular the two odd branches do not remain separate: the
actual unchanged edge AB joins both to the same new component.
Their parities must be added only after that actual join.

The frozen full-component criterion states that a perfect matching
of this same plane cubic D has an entirely even complete complement
if and only if every full component of its primal matching graph
has even q. Applying it to the complete component list proves that
every complete cycle of `D-N` is even.

There is also a direct exact count. Three complete primal components
give two complete complement cycles. Since H0 is the degree-four
vertex u alone, one is its full facial four-cycle. The other therefore
has length

`|V(D)|-4=7+|O|-4=|O|+3`,

which is even because O is odd. Thus the construction supplies exactly
`C4 disjoint-union C_(|O|+3)`, with all of e,f,g retaining their original
matching status.

## 5. Conditional conclusion and limits

Under the original same-source two-complete-cycle contract, the
5/5/5 hypothesis alone forces an actual even-complement matching in
P101, by the explicit ten-cycle above. This resolves the conditional
same-tree two-odd-branch subcase. The four-point switch also works
when the two branches are even; their individual parities are not
needed.

If the current contradiction argument assumes there is no even
matching in P101, the full 5/5/5 configuration is therefore impossible
in that assumed source. This is a conditional source contradiction,
not a claim that every source has the 5/5/5 pattern.

No proof is supplied that both safe rim vertices and their actual
outer third vertex must have degree five. The general two-cycle
repair, other conditional degree patterns, full joint positivity,
omega_e=0, complete319 and smaller-bad-source realization remain
outside this theorem. There is no new Lean theorem or external
colourability invocation; all existing source-size and reconstruction
cost boundaries remain unchanged.
