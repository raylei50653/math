# Extension: the entire curvature equality I+B=12 is impossible

Independent extension of the reviewed three-ear argument, on the same
G,J,D,S,C and actual seven-disk R. This uses only the already adopted
identities and the all-ear four-cycle contradiction proved in
[RIGIDITY sections 3--4](RIGIDITY.md). No new source premise, graph,
matching witness or theorem is introduced.

## 1. Parity and equality

Let E_ii count interior-interior edges and E_ib count interior-boundary
edges. Handshaking in the actual disk gives

`I = sum_interior d_J(u) = E_ib = sum_Q t_u = B (mod 2)`.

Thus I+B is even. The inherited theorem gives I+B>=12. Suppose equality
holds. The exact excess identity becomes

`Delta=2(1-epsilon)`.

If epsilon=0, the m-sector argument accounts for at least two units at
m alone, hence exactly two and zero elsewhere. If epsilon=1, Delta=0.
All non-m vertices attain their exact parity-dependent minima. Every
odd interior vertex has degree five and every even interior vertex
degree six. Hence disk curvature gives

`sum_Q t_u=I+8`.                                           (E1)

As in RIGIDITY, zpq is outside R: all its three vertices avoid the
strict interior, and a C face with all three on Q would force a
triangle inside the chordless-on-the-R-side simple seven-cycle.

## 2. Complete classification of boundary t at equality

For an ordinary boundary vertex, the baseline parity is even. Thus

* odd t: complete degree five, so t is one or three;
* even t: complete degree six, so t is two or four.

The larger option in either row satisfies d_R=2+t=d_J. It leaves
exactly one actual exterior triangular face, centred at this ordinary
vertex. Call this an ear centre.

For v,w,p,q, odd t gives complete degree four and t=1; even t gives
complete degree five and t=2.

For z, odd t gives complete degree six and t=1 or three; even t gives
complete degree seven and t=2 or four. The larger option would leave
exactly two exterior faces at z. But mz alpha, mz beta, and zpq are
three distinct exterior faces. Therefore z always has the smaller
option: t=1 when odd and t=2 when even.

For m with odd t, epsilon=1, complete degree eight and the original
sector degrees are six and seven. Its C-sector degree is even by
`d_G(u)-3=2k+t_m+2`, so it is six and t_m=1.

For m with even t, epsilon=0, complete parity is odd, minimum degree
seven and its exact excess is two, giving complete degree nine. The
original sector degrees are both odd and at least seven, and sum to
fourteen, hence both seven. In the C-sector equation

`7-3=2k+t_m+2`,

positive even t_m forces t_m=2. Thus every named boundary vertex also
has the smaller option and is not an ear centre.

## 3. Exactly three ordinary ears, for every I at equality

Let h be the number of ordinary ear centres. Each odd t contributes
baseline one, and each even t contributes baseline two. The preceding
classification is exhaustive, and each ear centre contributes exactly
two additional units. Therefore

`sum_Q t_u = B+2(7-B)+2h = 14-B+2h`.                        (E2)

Equality I+B=12 and (E1) give

`I+8=I+2+2h`, so `h=3`.

The centres are ordinary even when their complete degree is six, so
neither old boundary edge at a centre can be pq. The exact face-bit
identity therefore again makes all three exterior ears zero faces.
They are pairwise nonadjacent by the same unique exterior-face argument,
form the same disk R4 and simple four-cycle Q4, and leave all six T0
vertices on or outside it. The inducedness and four forced-ear cases
of RIGIDITY sections 3--4 apply verbatim: they depend only on three
ordinary actual zero ears, not on whether a centre has degree five
or six. They contradict the source-sector theorem.

This excludes every equality I+B=12 case, including I=5,B=7 and
I=6,B=6, while allowing arbitrarily many even interior vertices.
Since I+B is even and was at least twelve, the new exact necessary
condition is

`I+B>=14`, hence `I>=7` and `|C|=2i+5>=19`.

There is no assertion that the remaining I>=7 disks are impossible.
Ordinary101 matching existence, even-complement positivity, complete
source exclusion and source-preserving descent remain OPEN.
