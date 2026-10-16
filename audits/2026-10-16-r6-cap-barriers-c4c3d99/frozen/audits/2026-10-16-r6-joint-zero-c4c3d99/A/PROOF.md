# R6-JOINT-ZERO A: curvature excludes the singleton barrier class

Frozen BASE: `c4c3d99`. This is an arbitrary-size theorem for the same
original globally minimum noncatalogue C5 source, with
`d_G(x)=d_G(y)=d_G(b)=4`, `d_G(r)=6`, the legal retained-edge
`J=U/(s=t)`, and its actual spherical dual `D=J*`.

The input geometry and matching budget are frozen at
[the source proof](../frozen/audits/2026-10-15-j-source-geometry-6ddea32/PROOF.md)
and [the three-edge proof](../frozen/audits/2026-10-15-three-edge-matchings-6ddea32/PROOF.md).
No new external theorem is used. The previously verified Tutte theorem is
used only through the frozen maximum-barrier conclusion. The root audit
reverified the author text, p.348 Theorem A, in the
[1954 Cambridge PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/3785657C35F370E32E5AEAFC3D1B84CE/S0008414X00023774a.pdf/short_proof_of_the_factor_theorem_for_finite_graphs.pdf).

## A1. Source curvature supplies five unmarked odd vertices

Let `T={m,z,v,w,p,q}`, retaining the original six distinct vertices. In J,

* `d(m)>=7`, `d(z)>=6`;
* `d(v),d(w),d(p),d(q)>=4`;
* every vertex outside T has degree at least five;
* J is a simple sphere triangulation.

Let `t4,t5` count degree-four and degree-five vertices among `v,w,p,q`.
Let `n5` count degree-five vertices outside T, and put

`E=sum_{u:d_J(u)>=7}(d_J(u)-6)`.

Euler's identity for this very J gives exactly

`2 t4 + t5 + n5 - E = 12`.

Here `E>=1` because `d(m)>=7`, and `t4+t5<=4`. Therefore

`n5 = 12+E-2t4-t5 >= 8+E-t4 >= 5`.                 (A1)

This is a complete-source identity: it neither chooses arbitrary new
terminals nor suppresses high-degree vertices. In particular the set
`O={u outside T: d_J(u) is odd}` has at least five members.

## A2. Monochromatic dual edges record odd primal degrees

Assign either bit to each vertex of the actual dual D. Let F be the set
of dual edges whose ends have the same bit, and retain their literal
primal edges `F*` in J. Around the dual face corresponding to a primal
vertex u, the number of bit changes is even. Consequently

`d_{F*}(u) = d_J(u) (mod 2)`.                     (A2)

Thus every odd-degree primal vertex is incident to a primal edge of F*.
This uses the actual face walk in the spherical embedding. It is valid
for every bit assignment, not merely one induced by a matching. It has
no Tait-colouring or four-colour premise.

## A3. No singleton Tutte obstruction in either prescribed family

The actual marked dual edges are
`e=(vw)*`, `f=(pq)*`, `g=(mz)*`. The two ordinary families are

`P110={M PM of D: e,f in M, g notin M}`,
`P101={M PM of D: e,g in M, f notin M}`.

For either family write `a,b` for its forced edges, `h` for its forbidden
edge, `X=V(a) union V(b)`, and `H=D-X-h`. The source proves
`D[X]={a,b}` and all three marked edges are vertex-disjoint in D.

**Theorem A.** There is no Tutte-violating set S in H for which every
component of `H-S` is a singleton. In particular no maximum-cardinality
Tutte barrier of either empty family belongs to the all-singleton row of
the frozen four-row barrier table.

**Proof.** Suppose such a set S exists. Put `I=V(H)-S`, `q=|I|`.
The frozen deficiency bound gives `q=|S|+2`. Alternatively, counting
D-edges from I gives `3q<=3|S|+10`, and q-|S| is a positive even integer,
so this same conclusion follows without the maximum-barrier theorem.
Let `tau=1` if h has both ends in I and zero otherwise. (Since I consists
of singleton components, these are different components.) Let

`B=E_D(S) union E_D(S,X)`.

The exact degree count, using `|X|=4` and `D[X]={a,b}`, is

`|B|=1+tau<=2`.                                  (A3)

For clarity, with `s=|S|`, the sum of the q singleton degrees is

`3q=(3s-2|E_D(S)|-|E_D(S,X)|)`
`    +(8-|E_D(S,X)|)+2tau`.

Substitute `q=s+2` to obtain (A3).

Give bit zero to `S union X` and bit one to I. Its monochromatic edge
set is exactly

`F={a,b} union B union ({h} if tau=1 else empty)`.

There is no other I-I edge: every such edge except possibly h would be
an edge of H-S, contradicting its singleton components. Edges h inside
S are already counted in B; h from S to I is bichromatic. Thus no
forbidden-edge placement has been omitted.

All primal endpoints of a,b,h belong to the original set T. By (A2),
every odd-degree primal vertex outside T must therefore be an endpoint
of an edge in `B*`. But (A3) bounds the number of such endpoints by
`2|B|<=4`, contradicting (A1). QED.

The proof actually applies to any embedded cubic dual satisfying the
induced forced-edge and five-unmarked-odd-vertices hypotheses. Its
application here has full original-source premises, supplied by A1.

## A4. Consequence for joint ordinary failure

If `F_e=P110 union P101` is empty, choose a maximum-cardinality Tutte
barrier in each of the two residuals in the **same** D. Every one of
these maximum barriers contains a non-singleton factor-critical
component. Thus both sides of a simultaneous ordinary obstruction must
use one of precisely these three surviving types:

| Non-singleton components | Sum of cut excesses mu | `|E_D(S)|+|E_D(S,X)|` | Extra condition |
| --- | ---: | ---: | --- |
| one five-edge-cut component | 1 | tau | none |
| two five-edge-cut components | 2 | 0 | tau=1 |
| one seven-edge-cut component | 2 | 0 | tau=1 |

Here `mu(C)=(|delta_D(C)|-3)/2`. Each five-edge component whose literal
primal boundary avoids m,z is the retained degree-five W5 cap, by the
frozen source theorem. All other surviving five-edge boundaries pass
through m or z. Seven-edge components remain unrestricted by that
short-cycle theorem.

This excludes an entire arbitrary-size common-barrier class: a joint
ordinary obstruction cannot have an all-singleton maximum barrier on
either side. It is a strict strengthening of the old table; no additional
finite census or new ordinary-matching existence claim is being used.

## A5. Boundaries and completion cost

The theorem does not prove either ordinary family nonempty, does not
exclude coexistence of the three remaining barrier types, and says
nothing by itself about odd complements when an ordinary family is
nonempty. In particular `W110+W101>0`, the full fixed-degree r=6 branch
exclusion, and the joint-zero main objective remain OPEN.

There is no graph deletion/reconnection proposed as a source reduction;
H is only the exact ordinary-matching residual. Reconstructing the same
source through W/J still costs `k+5`. The general `K<=22=K<=5` statement
and this branch's old conditional `k>=25` remain unchanged. No theorem
about `r>=7`, unrestricted T/T0, full 720-state covers, or Lean is claimed.

The control checker retains original pins and reconstructs each dual
from all original faces. It independently enumerates residual Tutte
sets, verifies actual singleton-bit parity in the embedded control, and
records which source-degree premises fail. In particular the old
stacked example has a real singleton barrier but fails the source
geometry, while Petersen has joint ordinary failure but no spherical
source embedding. They are calibration controls only. No hypothetical
minimum source is supplied: source-level numerical tests are `not triggered`.
