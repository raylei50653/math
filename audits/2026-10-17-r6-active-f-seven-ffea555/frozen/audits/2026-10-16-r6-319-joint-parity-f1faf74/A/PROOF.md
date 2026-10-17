# A: complete Kempe rectangles and an exact link-locking residual

BASE `f1faf743833c51ddc5efbe9e0f390b87b9f2311d`, including the
uncommitted continuation frozen by the root manifest. Only this audit's
`A/` directory is written. The assertions below are conditional on the
same complete 319 source as the frozen continuation. They do **not** prove
`W110+W101>0` or exclude that source.

The new point is that a separated component condition gives a literal
complete-colouring transport into the allowed `f=g!=e` sector, commuting
with the preceding outer-orientation transport. A second result converts
the remaining single-colour extension obstruction into an exact condition
on actual components meeting the complete original z-link. Both results
keep all private colours and both ordered p/q attachments.

## 1. Contract and the four literal fibres

Use the original `U=R-r`, its induced ordered boundary `(z,s,v,w,t)`,
and the actual plane triangulation `J=U/(s=t)` with `m=[s=t]`.
The retained faces are `mvw,zpq` and the retained edge is `mz`.
Every complete J colouring obeys

`(d(vw)=d(pq)) iff (d(vw)=d(mz))`.                     (FJ)

All source hypotheses and every U fibre, including empty fibres and all
legal r lifts, remain in force. In particular the frozen continuation
supplies actual full all-distinct colourings in both outer orientations.
The witnesses need not have the same p/q direction or private colours.

Fix literal distinct colours A,B,C,D. Choose an original vertex
`u in {p,q}` and write d for the other original vertex. The notation
does not permute their attachments. Define four sets of full J colourings:

| Fibre | m | z | v | w | u | d |
| --- | --- | --- | --- | --- | --- | --- |
| E_v(u) | C | A | A | B | C | B |
| E_w(u) | C | A | B | A | C | B |
| F_v(u) | C | A | A | B | D | B |
| F_w(u) | C | A | B | A | D | B |

Every E row has e,f,g all distinct. Every F row has `f=g!=e`, so FJ
allows it. There is no claim that an arbitrary one of these four full
fibres is nonempty. In every row the original split s,t are both C,
and the entire r fibre is exactly `{D}`. That lift is retained even
when an original p/q vertex also has colour D.

Write X for the condition that the **actual maximal AB components**
containing the edges vw and zd are distinct. Write Y for the condition
that the actual maximal CD components containing m and u are distinct.
These definitions apply literally to all four fibres. All components
are components of the complete graph J, not a visible-pin skeleton.

## 2. Two commuting full-colouring involutions

On any row satisfying X, let S interchange A,B on the entire maximal
AB component containing vw. The original edge zd puts z,d together
in a different component. Hence S fixes z,d,m,u and exchanges the
colours of v,w. It gives bijections

`E_v(u)^X <--> E_w(u)^X`,
`F_v(u)^X <--> F_w(u)^X`.                             (1)

The first is the preceding continuation's map; the second is included
to identify the same complete transport after the new CD switch.

On any row satisfying Y, let T interchange C,D on the entire maximal
CD component containing u. It leaves m fixed and changes u between C
and D. All other displayed vertices have colours A or B and stay fixed.
Thus the new literal bijections are

`E_v(u)^Y <--> F_v(u)^Y`,
`E_w(u)^Y <--> F_w(u)^Y`.                             (2)

Each operation swaps a whole actual component, so it preserves every
edge and moves each private vertex according to that same colouring.
Its component vertex set does not change under its own two-colour
swap. Moreover AB and CD are disjoint palettes: S does not change the
CD-induced graph and T does not change the AB-induced graph. Therefore
X and Y are preserved by both maps, and S,T commute exactly on full
colourings. It follows that

`|E_v(u)^(X,Y)|=|E_w(u)^(X,Y)|`
`             =|F_v(u)^(X,Y)|=|F_w(u)^(X,Y)|`.          (3)

Equation (3) holds also when all four fibres are empty. If one has a
complete colouring, it constructs all four colourings on that same
original graph; it does not assemble witnesses from their marginals.
The private colours in the square are explicitly related by S and T.

If X fails, the entire AB exchange cube preserves which rim endpoint
has z's colour. If Y fails, every CD exchange changes m and u together
or fixes both, and hence preserves their equality. These are exact
obstructions to these two specified transports, not assertions that
no other sequence can work.

## 3. Every complete CD cube has the same singleton z fibre

Start with any one actual E_v(u) colouring chi; the E_w proof is its
literal v/w reflection. Put `B0=J-z` and retain its entire full colouring.
Since z=A and all its neighbours avoid A, arbitrary independent swaps
of full CD components in B0 extend with z=A to proper complete J
colourings. The CD components are identical in B0 and J.

For every resulting full B0 colouring psi,

`psi(v)=A`, `psi(w)=psi(d)=B`,
`psi(m),psi(u) in {C,D}`.

Let `L_z=N_J(z)` be the complete original link, and let

`A_z(psi)={A,B,C,D} minus psi(L_z)`.

This is the exact full J-lift set over psi, with every missing colour
included. Colour A remains available and B is excluded by d. If m,u
are differently coloured, both C,D occur on L_z, so A_z is `{A}`.
If both are C, a z=D lift would have

`d(vw)=d(mz) != d(pq)`,

violating FJ. Thus D is unavailable and again `A_z={A}`. The case
`m=u=D` is the same calculation with C,D exchanged. Hence

**every full colouring in this actual CD cube has exactly one z lift,
namely A.**                                                     (4)

In particular T can reach the F sector without producing a second z
lift. This explains why the same-source square alone does not close
the original obstruction. It is stronger than saying that each base
has some unspecified nonempty fibre: the entire actual cube has the
same literal singleton.

There is a corresponding BD statement from the same E_v colouring.
First, w and d must belong to the same actual BD component. Otherwise
swapping the full BD component of d fixes w,m,u,z,v and gives
`m=u=C,z=v=A,w=B,d=D`. Then `e=f!=g`, violating FJ. Thus they are
connected in the original full colouring. Arbitrary BD component
swaps preserve `w=d in {B,D}`, while m=u=C,z=v=A remain fixed.
The only colour not already excluded by m,d, besides A, is the
fourth colour of triangle mvw. Giving z that colour again violates
FJ. Consequently every full base colouring in this actual BD cube
also has exactly the z fibre `{A}`.                         (5)

## 4. Exact mixed-link component criterion and constructive exit

For a full two-colour induced subgraph and a prescribed set L of
vertices, the following elementary equivalence holds:

* every independent component swap leaves both palette colours on L;
* some one actual component meets L in vertices of both colours.    (6)

For the forward implication, if each component's L-intersection were
monochromatic or empty, orient every nonempty intersection to the same
one colour. These choices are independent because they are different
actual components. The reverse implication follows because a mixed
intersection stays mixed under either orientation of its component.
This argument includes components missing L and all empty intersections.

Apply (6) to the same original E_v colouring, with `L=L_z`:

* some CD component of J-z contains both a C-coloured and a
  D-coloured original neighbour of z;
* some BD component of J-z contains both a B-coloured and a
  D-coloured original neighbour of z.                           (7)

The CD conclusion follows from (4), since otherwise a full cube
orientation would omit one of C,D from L_z. The BD conclusion follows
from (5). This is a statement about actual components of the same
complete colouring, not separate paths from separate witnesses.
The two required mixed components need not coincide, and their paths
may meet at D vertices. No disjointness is asserted.

The proof supplies a constructive sufficient exit. If an actual E
colouring fails either condition in (7), orient each touching component
to one colour, keep every private vertex transported by that operation,
and recolour z to the newly missing colour. The resulting complete J
colouring violates FJ and its full r lift violates the original return
rule. In matching language this produces one member of the union
counted by `W110+W101`; it does not need both families separately.

There is a useful exact localisation. If the mixed component has a
path along L_z of length one, it is an actual edge of the link. If no
such edge exists, select a shortest path joining two oppositely
coloured z-neighbours within that palette. Choose it shortest among
all such endpoint pairs. No internal vertex of the path belongs to
L_z, for it would shorten the connection to one of the opposite-colour
endpoints. The path is chordless. Together with its two edges to z,
it is therefore an induced odd cycle of length at least five through
z. (Its odd path length is at least three.) Such a cycle can cross the
original z sectors or bound one of the allowed W5 caps; the present
argument excludes neither possibility.

## 5. The precise remaining case

The frozen source theorem guarantees
`E_v(p) union E_v(q)` nonempty and independently
`E_w(p) union E_w(q)` nonempty in the corresponding literal frame.
It does not force X or Y in either witness. The four visible
component possibilities `(X,Y)=(0,0),(0,1),(1,0),(1,1)` all preserve
FJ under the entire complementary AB/CD cube in the independent finite
calibration. Those component models are necessary local data, not
planar source realizations.

The new mixed-link tests also do not exclude the remaining case.
Actual BD or CD edges in the three-coloured z link already satisfy
them, and induced odd connectors may satisfy them when those edges
are absent. Excluding short cyclic cuts containing e or f does not
directly eliminate these connectors: the constructed odd cycles go
through z and need not contain either marked edge.

Accordingly there is no proof here that X, Y, or a failure of (7) must
occur in a genuine source. There is no construction of a violating
complete colouring, no source realization of the finite component
models, and no completed-source descent. Every operation stays on J;
splitting m and restoring the original source still returns total
`k+5`. Complete 319, the joint even-complement positivity, and the
general main theorem remain OPEN.

## 6. Verification scope

`check.py` independently reconstructs all 16,384 seven-pin colour
assignments, their complete r-colour lists, the direct original return
test, and the FJ comparison on every proper `s=t` row. Improper and
empty rows are retained. It checks both directions of both maps in
the four actual-visible component patterns and all 36 labelled cube
members, and verifies the mixed-link equivalence for every four-component
intersection pattern (including empty intersections).

These finite tests calibrate the algebra and the exact component
quantifiers. The arbitrary-size component maps and shortest-path proof
above are the authority for the source-conditional statements. Actual
minimum-source instances supplied: zero, **not triggered**. No external
theorem, 4CT, new Lean theorem, commit, or push is used.
