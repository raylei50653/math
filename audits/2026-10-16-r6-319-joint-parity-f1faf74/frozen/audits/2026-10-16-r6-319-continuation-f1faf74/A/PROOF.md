# A: complete 319 forces two genuine all-distinct J sectors

BASE `f1faf743833c51ddc5efbe9e0f390b87b9f2311d`; this audit writes
only `A/`. The authority inputs are the root frozen files. No actual
minimum source has been supplied.

**New arbitrary-size source theorem.** The same J has complete colourings
with `e,f,g` pairwise different, both with `z=v` and with `z=w`. More
precisely, two specified complete-U Kempe maps below are bijections.
This supplies a genuinely different starting sector from the known111
sector. It does not prove `W110+W101>0` or exclude complete319.

## 1. Same-source contract and literal full fibres

Fix the same globally minimum-interior, then maximum-edge no4ct source G,
with original boundary `(x,y,a,b,c)`, original four-degree x,y,b,
original r rotation `(x,y,t,w,v,s)` and `d_G(r)=6`. Use its actual
`U=R-r`, ordered induced boundary `(z,s,v,w,t)`, and
`J=U/(s=t)`, with `m=[s=t]`. All original p,q attachments, private
vertices, literal colours, and all legal r lifts are retained.

The frozen full transfer gives `Sigma(U)=319`. In one fixed colour frame
with distinct colours A,B,C,D its complete-U fibres obey:

* `(A,B,A,B,C)` has pq palette `{B,C}`;
* `(A,B,C,A,C)` has pq palette `{B,C}`;
* the boundary pattern ABCBD is absent;
* for boundary `(A,C,D,B,C)`, triangle `(m,v,w)=(C,D,B)`
  has unique r lift A, so the whole all-r condition requires
  pq palette `{D,B}`.

These are statements about every full colouring, not independent
boundary witnesses. In particular the first two full fibres are nonempty
because their boundary bits belong to the exact support319. Write
`F(X;P)` for the complete U colourings with literal boundary X and,
when specified, literal unordered pq palette P. An omitted P retains
every allowed ordered p/q assignment. The set may be empty.

## 2. A complete-colouring involution between two actual fibres

Define

`X=(A,B,A,B,C)`, `Y=(A,C,A,B,C)`, `P={B,C}`.

There is a bijection

`T_s: F(X) <--> F(Y;P)`,

given in both directions by interchanging B,C on the entire maximal
BC component containing the original vertex s.

**Forward proof.** Fix any full colouring chi in F(X). If z and v were
in different AD components, swapping the full AD component of v would
give literal boundary `(A,B,D,B,C)`, whose one common normalization is
ABCBD, absent from319. Thus there is an actual AD path from z to v.
The four actual outer vertices occur in cyclic order `(z,s,v,w)`.
An AD z-v path and a BC s-w path would be vertex-disjoint paths with
alternating outer endpoints in a disk, impossible by Jordan separation.
Hence s and w belong to different BC components. The retained boundary
edge wt puts w and t in one BC component, so the s component contains
neither w nor t. Its full swap gives exactly Y. Every pq endpoint is
B or C and pq is a retained edge; therefore either both endpoints lie
in the swapped component or neither does. Their unordered palette
remains P, while their original individual assignments are carried
along, possibly interchanged. This is a full colouring in F(Y;P).

**Reverse proof.** Fix any full colouring psi in F(Y;P). If z,v were
in different AD components, the full AD component swap at v would give
boundary `(A,C,D,B,C)` with the unchanged pq palette `{B,C}`. Its
unique legal r colour is A. Since z=A, the frozen full all-r rule
requires pq palette `{D,B}`, a contradiction. Therefore z,v are again
in one AD component. The same Jordan argument disconnects s from w,t
in BC, and the complete BC component swap at s returns exactly X.

The vertex set of a maximal BC component is unchanged by interchanging
its two colours. Consequently these forward and reverse maps are
literal inverses on full colourings, including every private vertex.
The argument neither merges distinct witnesses nor discards an empty
fibre. It proves equality of the two full-colouring counts, with no
claim that the ordered pq subfibres are separately equal.

## 3. An actual all-distinct J colouring in each outer orientation

The source has F(X) nonempty, hence F(Y;P) nonempty. In every image
colouring `s=t=C`, so the colouring descends bijectively to the original
J. Its full original r lift is the unique colour D. In that same
literal colouring,

`e=A XOR B`, `f=B XOR C`, `g=C XOR A`.

For three distinct elements of `F_2^2`, these are exactly the three
distinct nonzero elements. Thus the source has a full all-distinct
J colouring with `z=v`, not merely a feasible local pin assignment.

Reflect the whole argument by
`s<->t, v<->w, p<->q, a<->c, x<->y`, followed by one common
colour interchange B,C. This proves the second full-colouring bijection

`T_t: F(A,B,C,A,C) <--> F(A,B,C,A,B; {B,C})`,

where the map swaps the full maximal BC component of t. The two sets
retain the same original graph and the same literal vertex names.
The right side descends to a full all-distinct J colouring with `z=w`.
The two J sectors are disjoint because vw is an edge, so z cannot
equal v and w in one colouring.

In particular a complete source cannot have `d_f=d_g` in every J
colouring. The old planar control with144 J colourings and no
all-distinct state is therefore excluded by the **full-U source
support and all-r condition**, independently of its other geometric
failures. It remains a valid control against the weaker bridge.

## 4. Exact narrowing and remaining obligation

In an all-distinct J colouring, z equals exactly one of v,w and m
equals exactly one of p,q. To see this, z cannot be the fourth colour
omitted by `(m,v,w)`, since then `e=g`; if z=v, the only pq palette
with the third edge difference is `{m,w}`; if z=w it is `{m,v}`.
The original edge identities consequently give:

* if `d_G(a)=4`, so mp is an edge, both guaranteed sectors have `m=q`;
* if `d_G(c)=4`, so mq is an edge, both guaranteed sectors have `m=p`.

These are actual same-source nonempty equal-colour fibres, although
the whole additional quotient `J/(m=p)` or `J/(m=q)` need not be planar.
Consequently **at least one defined** quotient `H_p=(J-z)/(m=p)` or
`H_q=(J-z)/(m=q)` from the frozen previous round has a complete colouring
whose actual `A_z` is nonempty. If `a0=4`, it is H_q and both guaranteed
z=v/z=w sectors occur in that direction; if `c0=4`, it is H_p and both
sectors occur in that direction. If both degrees exceed four, each
guaranteed sector extends one of the two quotients, possibly different
ones. The theorem does not claim both quotients extend. This strictly
improves the previous nonemptiness obligation, which did not establish
even one nonempty actual z fibre, while still providing an allowed lift.

There is also an exact positive count. Let `n0=|F(A,B,A,B,C)|` and
`n4=|F(A,B,C,A,C)|` in the one literal frame used above. Both are
positive. Every all-distinct J colouring has exactly one of z=v,z=w;
in either case its three distinct colours uniquely specify the literal
frame `(A,B,C)`, with24 choices. The two bijections give

`N_all-distinct(J)=24(n0+n4)>0`.

For the actual dual D, define W010 and W001 by the same even-complement
matching weights `2^c(D-M)` as in the frozen bridge, in marked-edge
order `(e,f,g)`. Under the complete source equivalence FJ, a Tait lift
in either pattern010 or001 has all three differences distinct: the
other possible two-equal case would violate FJ. Conversely, every
all-distinct colouring appears in the corresponding fixed Tait-colour
count. The same four root colours and three common edge-colour choices
as in the frozen factor12 count therefore give

`N_all-distinct(J)=12 W010=12 W001`,
`W010=W001=2(n0+n4)>0`.

These positive families omit e. They are different from the sufficient
contradiction families W110/W101, which contain e.

All three differences are different, so this new starting state is
allowed by the full return equivalence `(e=f) iff (e=g)`. To finish
the three-edge route one must still obtain a full colouring in one
of the forbidden sectors, equivalently `W110+W101>0`. The two forced
cycle coincidences in the frozen all-distinct row remain possible;
we have not proved one fails. Ordinary matching existence still
does not imply an even complement.

All swaps leave the same graph and its number of vertices unchanged.
Completing J by splitting m and restoring the five original vertices
returns the original total `k+5`; there is no strict bad-source descent.

## 5. Verification scope

`check.py` independently reconstructs all16384 seven-pin assignments,
including every improper/empty position, the entire legal r fibre,
the direct original all-r palette test, and its separately written
case table. It enumerates every possible visible component partition
compatible with the retained skeleton and the actual outer Jordan
condition; for each literal X and Y colouring row it verifies the
forced links and every permitted full-component image. The target
fibre's reverse obstruction is checked through its actual r=A lift.

It also reconstructs the all-distinct-free necessary Kempe fixed point:
only six s=t canonical rows survive, with outer support266, incompatible
with source support319. This finite auxiliary check agrees with the
short paper proof but is not its arbitrary-size authority.

The certificate retains all16384 local positions and every r lift,
including zero slots, and all component options. These are local
assignment slots and necessary component models, not actual full
source-colouring counts. The paper proof transports actual complete
colourings and is the authority for the unbounded source theorem.
Actual minimum sources supplied: zero, **not triggered**. No new
external theorem, Lean theorem, shared-doc edit, commit, or push.
