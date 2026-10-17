# C: the split-source pivotal-component theorem

BASE `113e41f7023aa00c8257b815ce8727035b648f26`. Only this audit's
exclusive C directory is written. The frozen complete, continuation and
joint-parity A proofs supply the original graph contract and genuine
nonempty all-distinct sectors. No actual minimum source is supplied.

The new conclusion is an arbitrary-size constraint on the *same original
split graph U*. A permitted CD exchange from an all-distinct row into
`f=g!=e` must destroy one complementary connection and create another.
This holds throughout the entire actual CD cube. It is stronger than the
previous rectangle, which kept the AB component data but did not constrain
the new AD/BC components. It does not yet prove `W110+W101>0`.

## 1. Literal source and complete fibres

Retain the globally minimum-interior then maximum-edge no4ct C5 source G,
its induced disk `U=R-r` with ordered outer vertices `(z,s,v,w,t)`, and the
actual triangulation `J=U/(s=t)`, with `m=[s=t]`. Retain the actual distinct
p,q and their ordered original attachments, both original hubs, all fan
vertices and original nonedges. The retained U edges are the outer C5 and
`zp,pq,qz`; the two J faces are `mvw,zpq`, with retained edge `mz`.
Every source hypothesis, all of U319, every empty complete fibre and every
legal r lift remain in force. No new edge is inserted. Statements below
are consequences of that whole contract and do not replace it.

Use four literal distinct colours A,B,C,D. Choose one original endpoint
`u in {p,q}` and call the other original endpoint d. They are labels for
the proof, without changing their original attachments. Consider complete
U colourings, with all private colours retained, in the following fibres:

| Fibre | z | s | v | w | t | u | d |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E_v(u) | A | C | A | B | C | C | B |
| F_v(u) | A | C | A | B | C | D | B |
| H_v(u) | A | C | D | B | C | D | B |

They descend to the same J. E is all-distinct in `(e,f,g)`; F has
`f=g!=e`; H has `e=f=g`, where `e=d(vw), f=d(pq), g=d(mz)`.
The full r lift is `{D}` in E and F, and `{A}` in H. In particular
u=D in F does not remove the legal r=D lift: u is not an r-neighbour.

Two frozen source rules, applied to entire colourings, will be used:

* boundary X=`(A,B,A,B,C)` forces the entire pq palette `{B,C}`;
* boundary `(A,C,D,B,C)` has legal r=A=z and forces pq palette `{D,B}`.

They also follow directly from the original all-r return rule. In every
J colouring the full rule implies
`(d(vw)=d(pq)) iff (d(vw)=d(mz))` (FJ). The first X fibre is genuinely
nonempty; the earlier complete-colouring map supplies a genuine E_v
colouring for at least one original u. No F_v fibre is asserted nonempty
without an actual CD separation in an E colouring.

## 2. A source-forced change in the complementary connections

**E lock.** In every full E_v colouring, z and v belong to the same actual
maximal AD component of U. If not, swap the whole AD component of v. The
boundary becomes `(A,C,D,B,C)`, while pq stays `{C,B}`. Its complete legal
r=A lift contradicts the second source rule. Thus the AD connection is
an actual same-colouring path.

By Jordan separation in the actual disk, an AD z-v path prevents a
vertex-disjoint BC s-t path: their endpoints alternate on the original
boundary as `(z,s,v,t)`. Consequently s and t lie in different actual BC
components in every E_v colouring. The retained edge wt puts w with t.
This uses distinct original s,t. Identification into m would erase the
separation information.

**F lock.** In every full F_v colouring, s and t belong to the same actual
maximal BC component of U. Otherwise the whole BC component of s contains
neither t nor w. Swap it. The boundary is X=`(A,B,A,B,C)`, whereas the same
original u still has D, since a BC exchange cannot change it. The source
requires pq palette `{B,C}`, a contradiction. The entire r=D lift is
retained in this contradiction.

Jordan separation now implies that z and v lie in different actual AD
components. Both assertions apply to *every* full F colouring, regardless
of all private colours and regardless of its CD component partition.
They are not inferred by splicing paths from different witnesses.

The new exact distinction is therefore

`E_v: AD(z,v) connected; BC(s,t) disconnected`,
`F_v: AD(z,v) disconnected; BC(s,t) connected`.       (1)

The reflected statement exchanges `(s,v)` with `(t,w)` and carries every
original p/q attachment along; equivalently one can repeat these two
proofs on the reversed actual outer order. It gives the corresponding
E_w/F_w connection change. No graph automorphism is assumed.

## 3. An actual CD component is pivotal throughout the full cube

Fix one *actual* full E_v colouring chi. Suppose the actual maximal CD
components of J containing m and u are distinct. Let K be the component
containing u. In U this is the same actual CD component, excludes both
original s,t, and has no new attachment created by identifying them.
Switch the whole component K. This gives the previous rectangle's exact
bijection `T:E_v^Y <-> F_v^Y`, where Y is that CD separation. Its private
colours, all original edges and unique r=D lift are carried along.

The new assertion is that K necessarily changes both connections in (1).
Put `K_D={x in K : chi(x)=D}`. Then:

1. K_D meets *every* original AD path from z to v.
2. K_D meets *every* BC path from s to t in T(chi).

For 1, an AD path avoiding K_D also avoids K (its colours are only A,D),
so it survives the switch as an AD path in F, contradicting (1).
For 2, the only vertices newly entering the BC-induced subgraph are the
old D vertices K_D, now C. A new BC s-t path avoiding them would already
have existed in E, again contradicting (1). Hence K_D is nonempty and
simultaneously blocks the old connection and supports every new one.
This is an actual vertex separator/mandatory-intersection statement;
no planar graph is manufactured from abstract component partitions.

This is uniform over all other actual CD components. Allow arbitrary
independent whole-component switches except the m component, keeping
s=t=C. For each such *complete colouring*, u is C when K is unswitched
and D when it is switched. The source rules give exactly

`AD(z,v) connected <=> K unswitched`,
`BC(s,t) connected <=> K switched`.                    (2)

Components missing all displayed pins remain in this cube and may switch
independently. They are not discarded. Equation (2) says K is pivotal
for every background orientation of those components, including empty
intersections with the displayed pins.

**Constructive sufficient exit.** If an actual E_v colouring has Y and
an AD z-v path avoiding K_D, switch K. The surviving path in the resulting
F colouring forces BC(s) away from t,w. Switch that entire BC component.
The result is a proper complete U colouring with boundary X and u=D,
whose explicit legal r=D lift violates the original all-r rule. This
would contradict complete U319 by two actual whole-component operations.
The complete-lift bridge then excludes a source having
`W110+W101=0`; positivity of the union is the only requested target.
This is a sufficient exit, not a proof that an actual source must supply
such an avoiding path. Under the hypothesized source, (1) proves it does
not supply one. Notice that the last violating row has s!=t; we do not
claim that the final colouring itself is one of the forbidden J sectors.

## 4. A second forced bridge into the 111 sector

Every complete F_v colouring has z and v in different actual AD
components by (1). The retained edge zu puts z,u together. Switch the
entire AD component L of v. It fixes z,u,d,s,t,w and changes v from A to
D, giving an actual full H_v colouring. Its inverse is the same whole
component exchange on H_v whenever v is AD-separated from z,u. Thus

`F_v(u) <-> H_v(u)^{AD(v) != AD(z)}`                    (3)

is a literal full-colouring bijection, with empty fibres retained. This
strengthens a merely conditional local F-to-H transport: in the source
every F row satisfies its separation premise.

In every such H row, m and u must be connected in CD in J. Otherwise
switch the CD component of u, fixing m,v,w,z,d. This yields
`m=C,z=A,v=D,w=B,u=C,d=B`, with `e=g!=f`, contradicting FJ through its
actual legal r=A lift. The same applies to every H row, not just images.

In particular start with E^Y, switch K, then switch L as in (3). In the
intermediate F row m and u are still CD-separated, since a CD exchange
preserves its component sets. They are CD-connected in the H image.
Every resulting CD m-u path must therefore contain an old A vertex of
L that becomes D at the second exchange. This second mandatory bridge
uses vertices outside K_D (those became C before the second exchange).
The ordered two-exchange process is a new exact constraint on component
updates, rather than independent feasibility of an E and an H witness.

## 5. A third literal equality transport

There is also a useful complete-colouring transport in the remaining
complementary pairing AD/BC. In a full E_v(u) row, suppose the actual BC
component containing the retained edge pq is different from the one
containing mw in J. Switch the entire pq component. It fixes m,z,v,w,
exchanges the original individual p/q colours B,C, and gives E_v(d).
The actual component vertex set is unchanged, so this is a bijection
between the two separated ordered-equality subfibres. The same argument
applies to E_w. It is not a global p/q relabelling. If the original
mp or mq edge is present, its corresponding separation is impossible
because that original edge connects the two actual BC components.
No positivity of this subfibre is asserted.

## 6. Exact status and validation boundary

The frozen full source supplies an E colouring. It does not force Y,
and when Y occurs the new theorem forces the pivotal separator rather
than refuting it. Equations (1)-(3) give arbitrary-size same-source
structure and a fully specified exit test, but do not produce a source
violating the exit test. The old AB/CD square alone did not impose these
AD/BC updates, so this is an additional component-consistency obligation.
An abstract finite component cube is still not an actual planar source.

All operations keep the same underlying U and J. Splitting m and restoring
the original source still has completed total k+5. There is no smaller bad
source descent, no even-complement existence proof, no external theorem,
no new Lean theorem, no commit and no push. Full319 and
`W110+W101>0` remain OPEN. Actual minimum sources: zero, not triggered.

The checker retains all 16,384 seven-pin assignments, all legal r fibres
including empty and improper slots, and independently checks original
all-r/FJ. It exhausts the visible AD and BC partitions in E and F, rejects
exactly the component separations used in the proof by their concrete
full-component image rows, checks the reflected rows and inverse maps,
and checks the relevant whole CD cube row types. These are finite
algebra/component calibrations. The arbitrary-size path, Jordan and
pivotal-set assertions are proved above and are not inferred from that
finite enumeration. Normal, hash-seed17 and corrupted-certificate replay
receipts are retained separately.
