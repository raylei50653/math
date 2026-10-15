# C4 source: exact reduction to a triangulation with a forced fourth colour

This is a conditional paper lemma. It uses the strengthened source hypotheses proved in [SMALL_CYCLES](SMALL_CYCLES.md); it does not assume the general diagonal conjecture, the Four Colour Theorem, or colourability of arbitrary planar graphs.

## 1. Names and hypotheses

Write the original C5 boundary in cyclic order as

`B=(x,y,a,b,c)`.

Add a new vertex `u` outside it, adjacent to all five B vertices, obtaining the sphere triangulation `S`. Let `H=S-ub`, with outer boundary `(u,a,b,c)`. Assume:

1. `S` is simple, every face is triangular, and every vertex has degree at least five.
2. `B` is induced and `N_S(u)={x,y,a,b,c}` in that cyclic order.
3. No 3- or 4-cycle of S has vertices on both sides.
4. Every 5-cycle has a side containing at most one vertex.

The intended source has `d_S(u)=5`, `d_S(v)=d_G(v)+1` on B, and unchanged degrees at original inner vertices. The target is a complete H colouring with `a=c` and `u!=b`.

First observe that `N_S(a) intersect N_S(c)={u,b}`. Any further common neighbour w is outside B, since B is induced. The 4-cycle `u-a-w-c-u` has b on one side and x,y on the other: at u its two sectors are distinguished by the neighbour order. This contradicts hypothesis 3.

## 2. Construction and degrees

Draw edge ac in the outer quadrangle of H, contract it to z, and suppress the two resulting facial parallel-edge pairs at u and b. There are no other parallel edges, by the preceding common-neighbour observation. The resulting J is a simple sphere triangulation. Vertex u has exactly the neighbours z,x,y and degree three. Delete u and designate `zxy` as the outer face. The result T is again a simple sphere triangulation.

This construction keeps every other original vertex and edge, except that a,c are explicitly identified and their two edges to b become one. In particular it is not being presented as a literal same-boundary transformation without identification.

The exact degrees are

- `d_T(z)=d_S(a)+d_S(c)-3 >= 7`;
- `d_T(x)=d_S(x)-1=d_G(x) >= 4`, and likewise for y;
- `d_T(b)=d_S(b)-2=d_G(b)-1 >= 3`;
- every other vertex has its original S degree, at least five.

All vertices of T other than z,x,y are internal in the chosen plane drawing. The only possibly low-degree internal vertex is b.

## 3. Complete colouring bijection and exact obstruction

For each proper T colouring f in the same fixed four-colour frame, the facial triangle zxy has three distinct colours. Let `mu_f(zxy)` denote its unique missing colour. Split z back into a,c with the same colour, and set `u=mu_f(zxy)`. This gives a unique proper H colouring with a=c. Restriction and identification give the inverse. Thus this is a bijection on complete colourings, including empty fibres; no independent witnesses are combined.

Consequently

`H has a=c and u!=b  iff  T has f with f(b)!=mu_f(zxy)`.

Because bz is an edge, the latter condition is equivalently

`f(b) is in {f(x),f(y)}`.

Failure of the target says exactly that every complete T colouring gives b the missing colour of its designated outer triangle. This universal statement is valid even if the fibre is empty. For the actual 932/933/941 source the known `x24>0` and the C4 ABAB transfer separately certify nonemptiness.

For the fixed frame `z=B,x=C,y=D`, the T fibre with `b=C` restricts to the original fixed C5 assignment `(C,D,B,C,B)`, hence is exactly its singleton-1 fibre. The T fibre with `b=D` restricts to `(C,D,B,D,B)`, hence is exactly its singleton-0 fibre. To recover the single fixed H target `(u,a,b,c)=(A,B,C,B)`, keep the first branch unchanged and apply the same global swap `C<->D` to every vertex in the second branch. The two branches then have `(x,y)=(C,D)` and `(D,C)` respectively and form a disjoint union of full lifts. This supplies the fixed-frame identity `n_H(ABCB)=y1+y0` with the colour transport explicit.

More completely, with `(z,x,y)=(B,C,D)`, the full T fibre counts indexed by the b colour `(A,B,C,D)` are exactly `(x24,0,y1,y0)`. The A branch restricts to `(C,D,B,A,B)`, whose sole repeated pair is 24. Thus an actual target source with `y0=y1=0,x24>0` gives exactly `x24` colourings per fixed outer-triangle frame, all forcing b to its missing colour.

## 4. Classification of all nonfacial triangles of T

Every nonfacial triangle of T, if there is one, is precisely the neighbour triangle of b, and then `d_T(b)=3`. In particular:

- if `d_G(b)>=5`, then T has no separating triangle and is 4-connected;
- if `d_G(b)=4`, then T has exactly one separating triangle, namely `N_T(b)`, with b as the sole vertex on one side.

Here is a complete proof, including the exceptional endpoints.

A triangle avoiding z is an original S triangle and remains facial. For a triangle zvw, if both v,w are neighbours of a in S, or both are neighbours of c, it too is the image of a facial S triangle and remains facial. If v or w is b, it necessarily belongs to this case, because b is adjacent to both a and c.

Thus a nonfacial triangle must have, after interchanging v,w if needed,

`v in N_S(a) minus N_S(c),  w in N_S(c) minus N_S(a)`,

with neither vertex b or u. We have v=y as the only possible B endpoint on the a side, and w=x as the only possible B endpoint on the c side. The case `(v,w)=(y,x)` is exactly the designated facial triangle zxy and is excluded.

Consider the simple 5-cycle

`C=(u,a,v,w,c)`

in S. At u, one side contains b; call it the b side. The other contains every one of x,y that is not on C; call it the xy side.

**Case A: v!=y and w!=x.** Both x,y lie strictly on the xy side, so that side contains at least two vertices. Hypothesis 4 forces the b side to have exactly the one vertex b. No vertex strictly inside a Jordan cycle has neighbours strictly outside it. Since d_S(b)>=5 and C has five vertices, b must be adjacent to all five vertices of C and has degree exactly five. Hence `N_S(b)={u,a,v,w,c}`. After identification and deletion, `N_T(b)={z,v,w}` and `d_T(b)=3`. The triangle zvw has exactly b on one side.

**Case B: v=y and w!=x.** The xy side contains x. If it contained only x, all neighbours of x would lie on C. But ax is absent because B is induced, so x could have at most four neighbours, contradicting d_S(x)>=5. Thus this side has at least two vertices. Hypothesis 4 again forces the b side to be the singleton b. But by is absent because B is induced, so the same argument gives d_S(b)<=4, another contradiction. Thus this case cannot produce a nonfacial triangle.

**Case C: v!=y and w=x.** This is symmetric. The xy side contains y, and if it were a singleton, the missing edge cy would give degree at most four. If the b side were a singleton, the missing edge bx would give degree at most four. Hence this case is impossible as well.

There are no remaining cases. A degree-three vertex in a triangulation has its neighbours forming a triangle. Here b is not adjacent to x or y, so when d_T(b)=3 its neighbour triangle has b on one side and x,y on the other, and is indeed separating. The above classification shows it is the only one.

A simple sphere triangulation with at least five vertices and no separating triangle is 4-connected: maximal planar graphs are 3-connected, and any 3-vertex separator in a triangulation induces a separating triangle. The graphs here comfortably exceed this size; minimum degree five in S gives |S|>=12 by Euler, so |T|>=10.

## 5. The degree-three branch: two faces of one 4-connected triangulation

Assume `d_G(b)=4`. Write `N_T(b)={z,p,q}`. The two vertices p,q are original inner vertices, distinct from x,y, and pq is an edge. Remove b and designate zxy as the outer face, obtaining T0. The triangle zpq becomes a face.

No new edges are added. Every triangle of T0 was a triangle of T; the unique former separating triangle zpq is now facial. Hence T0 has no separating triangle. Its degrees are

- `d_T0(z)=d_S(a)+d_S(c)-4 >=6`;
- x,y have degree at least four;
- p,q have degree at least four;
- every other vertex has degree at least five.

Thus T0 is a simple 4-connected sphere triangulation with two distinguished faces `zxy` and `zpq`, sharing exactly z. As an additional source consequence, the original interior vertices p,q can contact at most two B vertices, and those contacts must be adjacent: otherwise a common-neighbour C4 through u separates B vertices. Since p contacts a,b and q contacts b,c, neither p nor q is adjacent to x or y.

Every complete T0 colouring lifts uniquely to an a=c colouring of H: restore b with the missing colour of zpq and restore u with the missing colour of zxy. This is another complete-colouring bijection. Therefore the original target is present precisely when some same complete T0 colouring has

`mu_f(zxy) != mu_f(zpq)`.

Since the triangles share z, this is equivalent to

`{f(x),f(y)} != {f(p),f(q)}`.

Thus the unresolved degree-three branch is an exact assertion about the two fixed facial triangles in one 4-connected triangulation: do they admit a colouring with different colour sets? Their full colourings must be compared in the same row. Two separately feasible face colourings do not suffice.

## 6. Scope

This is a structural reduction and exact residual. Neither residual extension theorem is proved. Complete finite controls and the next obligation are in [REPORT](REPORT.md). No new Lean theorem is claimed.
