# B. A four-vertex legal exchange repairs the 5/5/5 configuration

Frozen BASE: `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`.
Independent write scope: this audit's `B/` directory. The proof is for
arbitrary source size. It repairs the stated conditional configuration;
it does not show that every source has this configuration.

## 1. Same-source hypotheses

Retain the original globally minimum completed no4ct C5 source, its
secondary maximum-edge choice, ordered contacts and original rotation,
actual attachments, private vertices, complete U319 fibres including
empty fibres, all full lifts and all original r lifts. Work in the same
literal `J=U/(s=t)`, `D=J*`, with

`e=(vw)*`, `f=(pq)*`, `g=(mz)*`.

**Local notation.** Below `t=τ` is the actual exterior third vertex of
AB; it is distinct from the original split apex t whose image is m in
`J=U/(s=t)`. Likewise the local labels `a=α,b=β,c=ξ` denote actual J
neighbours without renaming the original ordered source contacts a,b,c.
Every local rotation, face and component formula uses this convention.

Fix the same actual `M in P101`, with full complement `C7 disjoint-union O`.
Use the complete primal monochromatic subgraph of the actual weak binary
colouring supplied by this M:

`P=(V(J),M*) = K2 disjoint-union T disjoint-union U0`.

The centre K2 has vertices u,h of degrees four and five, both of value
one; T is the value-one tree containing vw; U0 is the value-zero
unicyclic component with unique rim Q5 and mz in its z-rooted tree.
These are exactly the same components and values as in the frozen
[batch B proof](../frozen/audits/2026-10-20-r6-two-cycle-batch-9c36e3c/B/PROOF.md),
sections 1–3 and 7. The original-source geometry proves that every J
triangle is a face.

Use the fixed literal rim order

`R=r61, C=r12, L=r24, A=r45, B=r56`.

The actual centre rotations give

`N_J(u)={R,C,L,h}`, `N_J(h)={u,R,L,A,B}`.

The two safe vertices A,B have h as their sole centre neighbour.
Assume exactly the conditional 5/5/5 hypotheses

`d_J(A)=d_J(B)=d_J(t)=5`, `t notin {v,w}`,

where t is the actual outer third vertex of the rim edge AB. No
assumption on the parity of the two branches will be needed.

For any vertex set S write

`q(S)=sum_{x in S} d_J(x) mod 2`.

All these degrees remain the original fixed J degrees throughout the
exchange. The frozen complete-component parity theorem gives

`q(K2)=1`, `q(T)=1`, `q(U0)=0`,

and says that a perfect matching N has entirely even full complement
exactly when every complete component of `(V(J),N*)` has q-value zero.
Its proof uses the full region tree of every complete complementary
cycle, so it includes all outer cycles.

## 2. The exact local stars are forced by the original rotation

The frozen degree-five argument shows that A,B have no attached U0-tree
children. Their neighbours outside the rim and h are T vertices. Write
these actual neighbours as a,t at A and t,b at B. In a simultaneous
orientation of the original disk the rotations are

`A: (h,L,a,t,B)`, `B: (h,A,t,b,R)`.

In particular the faces `Aat` and `Btb` force the actual P edges at and
bt in T. The vertices a,b are distinct: equality would give A and B a
third common neighbour in addition to the two facial third vertices h,t.
Since t has degree five, its rotation contains the consecutive segment

`a,A,B,b`.

The fifth neighbour c is distinct from these four. The value-one
neighbours a,b are P neighbours of t. No two P neighbours can be
consecutive in its rotation, as that would make a monochromatic
triangle. Thus the degree-five bound forces exactly two P neighbours
at t, and its fifth neighbour c has value zero. It lies in U0, and

`t: (a,A,B,b,c)`.

Therefore `deg_T(t)=2`, with exactly the two complete components T_a,T_b
of T-t, containing a,b respectively. Since A,B have no U0-tree children,

`U'=U0-{A,B}`

is connected: its remaining rim is the path R-C-L, with every original
attached tree retained. The vertex c is an actual member of U'. No
replacement embedding or relabelling of the original marked vertices
is used here.

## 3. The exchange X={h,A,B,t} is legal at every actual triangle

Set

`X={h,A,B,t}`,

and flip the binary value precisely on this one actual vertex set.
The old and new values on the patch are

| vertex | u | h | A | B | t |
| --- | ---: | ---: | ---: | ---: | ---: |
| old | 1 | 1 | 0 | 0 | 1 |
| new | 1 | 0 | 1 | 1 | 0 |

The exterior vertices R,C,L,c retain value zero; a,b retain value one.
By the complete stars in section 2 and the actual degree-five star at
h, every triangle meeting X is one of the following twelve faces:

`huL, huR, hLA, hAB, hBR, ALa, Aat, AtB, Btb, BbR, tac, tcb`.

Each listed triple has both values after the flip. This verifies the
full original-triangle condition, including its complementary closure;
triangles disjoint from X retain their original valid values.
Equivalently, each triangle still has precisely one monochromatic
edge. Hence

`N* = M* symmetric-difference delta_J(X)`

is dual to a perfect matching N. At each crossed triangle the cut
contains one original M edge and one original non-M edge, so
`delta_J(X)*` is an actual vertex-disjoint batch of M-alternating
cycles. In fact it is one simple alternating decagon. Its ten actual
dual vertices, in order, are the triangles

`(u,h,L), (h,L,A), (L,A,a), (A,a,t), (a,t,c),`

`(t,c,b), (t,b,B), (b,B,R), (B,R,h), (R,h,u)`.

Its primal crossed edges alternate as

`hL, LA, Aa, at, tc, tb, bB, BR, Rh, hu`,

where `LA,at,tb,BR,hu` are original P edges and the other five are
original non-P edges. The two remaining faces `hAB,tAB` are wholly
inside X and contribute no crossed edge. This explicit decagon uses
all ten edges of `delta_J(X)` and verifies the rotation directly.
Thus this is a legal simultaneous exchange with respect to the fixed
original M itself.

All four selected vertices h,A,B,t avoid `{m,z,v,w,p,q}`. The original
centres and literal sectors already give this for h,A,B, and t is in T
and is excluded from v,w by hypothesis. Thus the cut crosses none of
the three marked primal edges vw,pq,mz. In particular it preserves the
original membership of e,f,g individually:

`e in N`, `f notin N`, `g in N`,

so `N in P101`. This checks the stronger form of the required
`e in N` and `f xor g` conditions, on the same named edges.

## 4. All complete new components are even

The list of all full components of `(V(J),N*)` is exactly

1. `I={u}`;
2. `Y=(T-{t}) union {A,B}`;
3. `Z=(U0-{A,B}) union {h,t}`.

To verify exhaustiveness, all old P edges outside the four selected
stars are unchanged. The centre edge uh is deleted. The old rim edges
LA and BR are deleted, while AB remains. The edges at and bt are
deleted. The newly monochromatic edges are precisely

`hR, hL, Aa, Bb, tc`.

The first pair attaches h to the connected U'; tc attaches t to it.
The unchanged edge AB and the new edges Aa,Bb join the two complete
branches T_a,T_b into one connected Y. Every other unchanged old edge
lies within one of these three sets; there is no remaining edge
between them. This proves the full component list rather than only
selected component marginals.

Their original degree parities are

`q(I)=d_J(u)=4=0 mod 2`,

`q(Y)=q(T)+q({t})+q({A})+q({B})=1+1+1+1=0 mod 2`,

`q(Z)=q(U0)+q({A})+q({B})+q({h})+q({t})`

`    =0+1+1+1+1=0 mod 2`.

Thus the complete-component parity theorem proves that **every complete
cycle of D-N is even**. There are exactly two such complete cycles,
because the new primal spanning graph has exactly three components.
The cycle bounding I is the unchanged degree-four dual face of u;
its other complete cycle has length `|V(D)|-4=|O|+3`, hence is even.
This also follows directly because Y is a tree, Z is unicyclic, and
the unique Z cycle is the new rim `h-R-C-L-h=link_J(u)`. The two
complete-cycle lengths are therefore exactly `4` and `|O|+3`.

In the user's specified same-tree two-odd-branches subcase,
`q(T_a)=q(T_b)=1`, these odd branches are joined in Y by the actual
path `a-A-B-b`. They are no longer left as separate odd full
components. Their branch parity does not have to change individually.
The proof also works when both branches are even.

## 5. Result and boundary

**Conditional repair theorem.** For the same actual source and fixed
matching M in the two-complete-cycle branch, if the two literal safe
rim vertices A,B and the actual exterior third vertex t of AB all
have degree five, with t outside {v,w}, then flipping exactly
`X={h,A,B,t}` gives an actual `N in P101` whose full complement is
entirely even. In particular this closes the stated same-tree
odd/odd branch subcase.

This theorem constructs the required larger legal alternating batch;
no smaller bad source, source contradiction, or source realization is
needed to certify this conditional repair. It proves neither that
all sources satisfy 5/5/5 nor that all two-cycle sources lie in this
conditional branch. Those coverage statements, joint positivity,
complete319 and the general same-source repair remain OPEN. There is
no 4CT oracle, new external theorem or Lean claim; the original
completed-source reconstruction cost k+5 is unchanged.
