# Seven-port matching interface on the same original source

Task `R6-101-NONWHEEL-SEVEN-CUT`, BASE
`120aae90cab8bc4881916adc598cf344f2f20f4b`. This note retains the original
minimum, secondary-edge-maximum C5 source, its ordered contacts, the legal
`J=U/(s=t)`, its actual spherical dual D, the literal marks e,f,g, and ONE
chosen maximum-cardinality violating S of `H=D-X-f`,
`X=V(e) union V(g)`. C is its unique nonsingleton component. No graph is
replaced below. The previously proved common-111 saturation applies to ALL
members of the same nonempty P111 simultaneously.

## M1. Seven distinct ports and no articulation

The graph `H[C]=D[C]` is connected and factor-critical; equality holds
because f joins two different odd components. Its minimum internal degree
is at least two: if u had sole neighbour v, deleting v would leave u
isolated in a nonempty even graph. Connectivity excludes degree zero.
As D is cubic and `|delta_D(C)|=7`, there are exactly seven distinct
vertices `u_0,...,u_6` of internal degree two, each incident with exactly
one actual cut edge `b_i=u_i v_i`. Every other C vertex has internal
degree three. The exterior endpoints v_i are not asserted distinct.

C has no bridge. A bridge divides its odd order into an odd side A and
an even side B. Delete the endpoint of the bridge in B. Then the odd
set A is an isolated component of the remaining graph and cannot be
perfectly matched, contradicting factor-criticality. If C had an
articulation v, every component of C-v would require at least two edges
to v, because a unique edge would be a bridge. Two such components
would require degree at least four at v. Hence C is 2-connected.

The actual disk/bond theorem in PROOF.md supplies the cyclic order of the
seven cut edges on its simple primal C7 boundary. It is this source disk
that is used in M3, rather than a freely chosen planar embedding. The
matching conclusions in M1--M2 do not require a disk assumption.

## M2. Full singleton fibres and one unchanged exterior

For an odd subset `T subset {0,...,6}`, define the COMPLETE fibre

`F_T = PM(C - {u_i:i in T})`.

All seven singleton fibres are nonempty by factor-criticality. Even T
have empty fibres by parity. No claim is made that every larger odd
fibre is nonempty. In particular retaining a support set without its
empty cells and all its internal matchings would lose information.

Define E_T on the SAME actual exterior `D-C`: its elements are all PMs
after deleting the outside endpoints v_i of selected b_i, together with
the selected original cut edges, subject to any specified original
marks. Declare E_T empty if two selected edges share an exterior
endpoint or violate a specified mark. Then ordinary matchings of the
original D satisfying those marks have the exact disjoint decomposition

`disjoint union_T (F_T times E_T)`.

The bijection simply restricts a matching to the two sides of the actual
cut and records its actual crossing edges. Conversely, take the literal
union of a compatible pair and those cut edges. Every vertex is covered
once, and there is neither a witness change nor an alteration of J.
The fibres retain literal matching edges, not merely their counts.

For P111 the established tight cut condition restricts T to a singleton:

`P111 = disjoint union_{j=0}^6 (F_{ {j} } times E_{ {j} }).`       (M1)

Consequently if one exterior matching supports port j, EVERY member of
`PM(C-u_j)` extends using that very same exterior matching. The entire
internal fibre, including its possibly odd-complement choices, is
present in P111. If f crosses C, only its literal port can be supported:
f is required in every member and tightness forbids any second crossing.
If f does not cross C, any port ending in X is unsupported, since e,g
already match all of X. These are necessary restrictions; they are not
a proof of 101 matching existence.

## M3. At most 560 tight states, with every full lift retained

Take `N in F_T`. In the internal complement `D[C]-N`, vertices u_i for
`i not in T` have degree one; all other vertices have degree two.
Thus it is a disjoint union of cycles and paths, with the paths pairing
exactly the unselected cut ports. All these components and their actual
edge sequences are determined by N. The paths are vertex-disjoint in
the same disk. Two alternating endpoint pairs on its boundary cannot
be joined by disjoint paths: a simple path together with a boundary arc
separates the disk, forcing an intersection for the alternating pair.
The pairing is therefore noncrossing in the actual cyclic order.

Record the state

`(T, pi, epsilon, eta)`,

where pi is this pairing, epsilon records each paired path's internal
edge-length parity, and eta is one iff an internal complement cycle is
odd. Keep in EACH state fibre every literal N, all path edge sequences,
and the full internal cycle list; empty states remain explicit. eta is
a finite compatibility bit, not permission to discard the odd records.
For tight T={j}, there are five noncrossing pairings of six boundary
points, eight path-parity vectors, and two eta values: at most

`7 * 5 * 8 * 2 = 560` states.                               (M2)

For all ordinary crossing patterns the corresponding complete registry
has at most

`2 * (7*5*8 + 35*2*4 + 21*1*2 + 1) = 1206` states.          (M3)

The terms correspond to |T|=1,3,5,7. The elementary pairing counts for
0,2,4,6 points are 1,1,2,5: pair the first point and split the remaining
points into the two even intervals. If the disk theorem were unavailable,
arbitrary pairings instead give 1680 tight states and 2606 full ordinary
states; the stronger numbers (M2)--(M3) use the actual disk conclusion.

This is a bounded interface, not a bounded list of patches. A fibre may
have arbitrarily many internal matching records and arbitrarily long
paths or cycles. Their full data are retained; no source-order bound,
replacement gadget, colouring-fibre reduction or descent follows.

There is a further necessary parity restriction within this registry.
Put `n=|C|` and `r=(7-|T|)/2`. Cubic degree counting gives
`|E(D[C])|=(3n-7)/2`, whereas `|N|=(n-|T|)/2`. Thus the internal
complement has exactly `n-r` edges. Since n is odd,

`sum epsilon + (number of odd internal cycles) = 1-r (mod 2)`. (M4)

In particular eta=0 forces `sum epsilon=1-r (mod 2)`. For tight r=3,
140 of the 560 registered states are universally empty; at most 420
signatures can occur. Across the full ordinary registry the numbers of
universally empty eta=0 states for |T|=1,3,5,7 are respectively
140,140,21,1, leaving at most 904 effective signatures. The r=0 case
has an odd total number of internal cycle edges, so eta=1 is compulsory.
The checker retains the complete original 560/1206 registries including
these impossible cells; this refinement never drops an empty fibre.

## M4. Exact parity join and complete colour lifts

Join one recorded internal matching to one compatible matching of the
unchanged actual exterior. In the complement, the unselected cut edges
join the two path systems. Exterior cut ends are separately labelled even
when their actual endpoints v_i coincide. Two unselected cut edges
meeting one exterior vertex are connected there by a path of length
zero; cubic degree and the matching condition leave at most two such
ends at that vertex. All other exterior paths are the ordinary chains
between cut ends. Thus repeated exterior endpoints do not require a
new assumption or invalidate the parity test.

The union of the two port pairings is a 2-regular multigraph on the
unselected port labels (a shared paired edge gives a two-edge cycle).
Each such alternating cycle corresponds to exactly one actual global
complement cycle. Its length is the sum of the recorded internal and
external path lengths plus its cut-edge count. That count is even,
because internal and external paths alternate. Its parity is therefore
the xor of the recorded path parities around that alternating cycle.

The original matching has even complement iff BOTH sides have eta=0
and every joined alternating cycle has xor zero. This is an iff on
literal full matching lifts. In particular a nonempty ordinary fibre
with eta=1 remains present but supplies an EMPTY even-colour fibre.

For an even complement the already adopted Tait correspondence gives
two alternating assignments of the other two named edge colours per
actual global complement cycle. Retain every assignment on every
internal cycle and joined path cycle, independently; an odd cycle has
zero assignments. Together with the fixed matching colour, this
recovers every complete labelled Tait lift, and the adopted same-J
integration recovers its complete vertex-colouring lift. Actual cycle
counts and edge sequences are kept inside the state fibre precisely
because the finite signature alone does not determine the number or
identity of these lifts. No marginal colour witnesses are combined.

## M5. Same-family crossing restrictions

For any component K of a maximum 110 barrier on the same D, both K and C
are odd and their cuts are tight for EVERY member M of P111. If they
cross, the already proved matching cut identities give the following.
For odd `|C intersect K|`, both intersection and union are tight and
`M(E(C-K,K-C))=0`. For even intersection, both differences are tight and
`M(E(C intersect K,V(D)-(C union K)))=0`. The identities are applied to
each literal M from the common family, never to separately selected
witnesses. A forced e,f,g in the excluded edge class gives a contradiction.
Without such an edge, tightness alone supplies no contradiction.

One must also not silently assume a 110 barrier exists: an ordinary
110 matching with odd complement is logically possible at this stage.

## M6. Calibration scope and remaining obligation

`matching_check.py` enumerates ALL matching fibres, including all even
and odd empty cells, on three fixed local seven-port graphs: the seven
cycle, a nine-cycle with a chord whose two bounded faces have lengths
five and six, and the dual of the thirteen-face triangle-and-pendant
disk recorded in PROOF.md. The second is the factor-critical theta
graph with path lengths (1,5,4), a nonwheel local calibration. All have
seven degree-two ports on one face. The third has four complete primal
interior vertices of degree five; it is factor-critical, with 64 local
matching lifts, and so prevents inferring a larger order exclusion
from factor-criticality alone. It does not meet the additional original
m-sector condition used to obtain the source lower bound in PROOF.md.

The checker preserves all PM lifts, full complement cycles, and all
Tait assignments in the glued controls and independently checks the
join against direct whole-graph enumeration. Their complete global PM
counts are respectively 29,44,104; odd-complement matching fibres remain
explicit and have empty Tait fibres. This finite domain is declared in
`matching_certificate-v2.json`, the final three-control certificate.
`matching_certificate.json` is the retained initial two-control artifact,
not the final replay target. Neither certificate verifies a source or
proves the arbitrary-size disk or matching lemmas by enumeration.
The three doubled controls have distinct exterior cut endpoints; the
repeated-endpoint, zero-length-path convention in M4 is proved on paper.

The remaining source problem is to exclude the actual disk patches
allowed by the source face/sector/degree restrictions, or to obtain a
genuine source-preserving reduction. The finite interface permits exact
tests of proposed new restrictions while preserving every old lift and
empty fibre. It does not itself show the interface empty. No genuine
globally minimum source is produced; source realization is `not
triggered`. No ordinary matching is equated with an even-complement
matching; W110+W101, full 319 and general K-infinity claims remain OPEN.
The existing k+5 reconstruction cost is unchanged.
