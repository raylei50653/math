# R6-CAP-BARRIERS A: weighted curvature excludes wheel barriers

BASE `c4c3d99`; this extends the frozen same-source result
[JOINT-ZERO A](../../2026-10-16-r6-joint-zero-c4c3d99/A/PROOF.md).
The source and maximum-barrier inputs are
[the J geometry proof](../../2026-10-15-j-source-geometry-6ddea32/PROOF.md)
and [the three-edge proof](../../2026-10-15-three-edge-matchings-6ddea32/PROOF.md).
All assertions below have the complete original globally minimum noncatalogue
C5 source premises, with the original degree-four x,y,b, degree-six r,
legal retained-edge J, literal six pins, and actual spherical dual D=J*.
There is no new external theorem. In particular a wheel below is an actual
subgraph of this J, not an abstract replacement graph.

## A1. Exact parity-sensitive Euler identity

Write `P={v,w,p,q}`, `T=P union {m,z}`, and `o_u=d_J(u) mod 2`.
The source bounds are `d(m)>=7`, `d(z)>=6`, `d(P)>=4`, and
`d(u)>=5` for every u outside T. Their parity-sensitive minima are

| Vertex class | Minimum degree with parity o |
| --- | --- |
| m | `8-o_m` |
| z | `6+o_z` |
| u in P | `4+o_u` |
| u outside T | `6-o_u` |

Let `s_u=d_J(u)-d_min(u)` and `L=sum_u s_u`. Each s_u is a nonnegative
even integer. Define

`Q(o)=6+o_m-o_z-sum_{u in P}o_u+sum_{u outside T}o_u`.

Euler's identity is exactly

`12 = Q(o)-L`.                                                   (A1)

Thus `Q(o)>=12`, and not merely the existence of five unmarked odd
vertices, is a necessary source condition. Flipping one parity changes
Q by exactly one in absolute value; flipping both ends of an edge raises
it by at most two. The all-even parity vector has Q=6.

For any bit assignment on V(D), let F be its monochromatic dual edges.
Around every actual dual face the number of bit changes is even. Therefore

`o_u = d_{F*}(u) mod 2`                                          (A2)

at every original primal vertex, with the literal primal edges retained.
This is the earlier face-parity lemma, used here with its full weighted
Euler consequence. No edge colouring or even-complement assumption occurs.

## A2. The exact barrier parity vector

For either ordinary family, let a,b be its forced edges, h its forbidden
edge, `X=V(a) union V(b)`, and `H=D-X-h`. Choose a maximum-cardinality
Tutte-violating S. The frozen proof gives only odd factor-critical
components of H-S and

`sum_C mu(C)+|B|=1+tau`,

where `B=E_D(S) union E_D(S,X)`, `mu(C)=(|delta_D(C)|-3)/2`, and tau
records whether h joins two different components of H-S.

Give bit zero to S union X and bit one to every component of H-S. If
`I_C=E_D(C)` denotes the actual dual edges internal to a non-singleton
component, its complete monochromatic set is

`F={a,b} union B union (union_C I_C) union ({h} if tau=1)` .        (A3)

All these displayed parts are disjoint. In particular h inside S is in B,
h inside one component is in I_C, and h between S and a component is
bichromatic. There is no omission of a forbidden-edge placement.

For one five-cut component `|B|=tau`. For two five-cut components or one
seven-cut component, `tau=1` and B is empty.

The parity supplied by only a,b has Q=2 for 110 and Q=4 for 101:
`vw,pq` each flip two negative-weight pins, whereas `mz` flips one
positive-weight and one negative-weight pin. With all three marked edges
present every vertex of T is odd, every other vertex even, and Q=2.

## A3. No single wheel barrier

Call a component C a **wheel component of length l** only when there is
an actual degree-l vertex c of J whose l incident faces are exactly C,
and whose complete link is the simple l-cycle forming the cap boundary.
Then D[C] is the l-cycle, and `I_C*` is exactly the l spokes of this
same primal wheel. For odd l its odd-incidence support is the l+1-element
set `K={c} union N_J(c)`.

This definition does not identify an arbitrary dual cycle component with
a wheel: a dual cycle can surround an omitted dual region. Nor does it
assert that an arbitrary seven-cut component has a disk boundary.

The center c is outside T. If c is an endpoint of a forced primal edge,
its complete face set meets X, which is impossible. If it is an endpoint
of the forbidden primal edge, h is internal to D[C]; deleting h leaves
a path of odd order in H[C], which is not factor-critical. For example,
deleting the neighbor of an endpoint isolates that endpoint and prevents
a perfect matching. These alternatives cover every vertex of T.

**Theorem A3.** Neither ordinary residual admits a maximum barrier whose
only non-singleton component is a five-wheel component. Neither residual
admits a maximum barrier whose only non-singleton component is a
seven-wheel component.

For a five-wheel, its spokes flip exactly six primal parities. If tau=0,
B is empty, so Q is at most 2+6=8 for 110 or 4+6=10 for 101. If tau=1,
the three marked edges supply Q=2, the sole B edge can raise Q by at most
two, and the wheel by at most six. Again Q<=10. Every case contradicts
(A1).

For a seven-wheel the barrier table gives tau=1 and B empty. Its spokes
flip eight parities, so Q<=2+8=10, already a contradiction. In fact the
unmarked center has degree seven, odd parity, and minimum degree five,
so `L>=2` and the stronger upper bound is `Q-L<=8`. QED.

The five-wheel result applies whether or not its rim contains m or z.
In particular the frozen source theorem makes every hub-avoiding five-cut
component a retained W5, so **a one-five-cut barrier must have its boundary
through at least one hub and must fail to be a complete five-wheel cap**.
Any additional source argument identifying a hub-crossing boundary with
such a wheel may now exclude that case directly.

**Side-assignment lemma.** If the actual simple five-cut boundary has a
five-wheel on either side, then its Tutte component C is that wheel side.
Otherwise all four forced dual vertices X would lie in the opposite
five-wheel's five-face cycle. Any four vertices of C5 induce exactly
three edges, contrary to the source identity `D[X]={a,b}`, which has only
two. Thus a theorem identifying merely one side of the boundary as W5
is sufficient; it need not separately orient that side toward C.

## A4. Exact rigidity for a pair of five-wheels

Suppose a maximum barrier has exactly two five-cut non-singleton
components, both actual five-wheels, with centers c1,c2 and
`K_i={c_i} union N_J(c_i)`. The two centers are distinct and nonadjacent:
an edge between them would have incident faces belonging to both
components. Thus neither center belongs to the other K_i, and
`K_1 intersect K_2` consists only of common rim vertices.

Put

`r_cap=|K_1 intersect K_2|`,
`epsilon=1 if m belongs to K_1 symmetric_difference K_2, else 0`.

Here r_cap is a new intersection count, not the original named vertex r.
The barrier table gives tau=1 and B empty. Start with the all-three-marked
parity vector of Q=2. Exactly the symmetric difference of K1,K2 is
flipped. Its size is `12-2r_cap`. Every one of these flips raises Q by
one, except a flip at m lowers Q by one: unmarked vertices start even,
the four negative pins and z start odd, and m starts odd. Consequently

`Q=14-2r_cap-2epsilon`,
`L=2(1-r_cap-epsilon)`.                                         (A4)

This is an equality, not a union bound. It proves:

1. `r_cap+epsilon<=1`. In particular two common rim vertices are
   impossible; one common rim vertex together with m on exactly one
   wheel is also impossible.
2. If `r_cap+epsilon=1`, every vertex attains its parity-sensitive
   minimum in A1. If `r_cap=epsilon=0`, precisely one vertex has degree
   two above its parity minimum; every other vertex attains its minimum.
   The exceptional vertex cannot be either wheel center.
3. `7<=d_J(m)<=9` and `6<=d_J(z)<=9`. The source degree identities give
   `d_G(s)+d_G(t)<=14`, hence `6<=d_G(s),d_G(t)<=8`, and
   `3<=h=d_J(z)-3<=6`. This does not bound the source order k.
4. The forbidden edge h cannot join the two wheel components. If it did,
   its literal primal edge would lie on both wheel rims, placing its two
   distinct primal endpoints in `K_1 intersect K_2`, contrary to item 1.

The last item preserves the actual identity of the forbidden edge. It is
stronger than choosing independent cap witnesses, and does not assert
that h must meet either cap: a singleton-to-singleton h remains possible.

## A5. What the result closes and what remains

Combined with the preceding all-singleton exclusion, an ordinary failure
now has only the following possibilities:

* one five-cut component which is not a five-wheel, necessarily crossing
  at least one hub;
* two five-cut components, with any two-wheel instance satisfying the
  exact global degree restrictions (A4) and the forbidden-edge exclusion;
* one seven-cut component which is not a seven-wheel.

Theorem A3 excludes an arbitrary-size barrier subclass by a complete
source Euler contradiction. A4 is an arbitrary-size necessary condition,
not a construction, finite catalogue exclusion, or a proof that either
ordinary family is nonempty. Caps through hubs are not automatically
wheels; seven-cut components are not automatically disks. No such
identification is used silently.

Even existence of an ordinary matching would still leave its complement
parities to be proved. `W110+W101>0`, complete Sigma-319 exclusion, and
completed-source descent all remain OPEN. There is no source replacement
or changed reconstruction cost: the existing k+5 cost, general
`K<=22=K<=5`, and this branch's conditional k>=25 remain unchanged.
There is no new Lean claim, commit, or push.

[check.py](check.py) exhausts the six-pin membership quotient of the
weighted-parity identities, directly checks a literal wheel's spoke
incidences, and rejects deliberately corrupted charge formulas. These
are algebraic calibration controls, not hypothetical original sources;
source-level numerical tests are `not triggered`. The arbitrary-size
conclusions are the paper proofs above.
