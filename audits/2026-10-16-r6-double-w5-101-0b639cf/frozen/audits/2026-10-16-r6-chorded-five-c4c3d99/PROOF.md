# R6-CHORDED-FIVE: every 101 five-cut component is a retained W5

2026-10-16; Git BASE `c4c3d99c59cfe4f85b3e33f6831da955a8efcbc7`.
Retain the complete original globally minimum noncatalogue C5 source,
secondary maximum-edge choice, ordered boundary `(x,y,a,b,c)`,
`d_G(x)=d_G(y)=d_G(b)=4`, `d_G(r)=6`, and the actual legal
`J=U/(s=t)`, `m=[s=t]`, with spherical dual D. No graph is replaced.
The literal marks are `e=(vw)*`, `f=(pq)*`, `g=(mz)*`.

## 1. Frozen inputs and statement

The [source geometry](frozen/audits/2026-10-15-j-source-geometry-6ddea32/PROOF.md)
supplies faciality of every J triangle, the faces `mvw,zpq,mz alpha,mz beta`,
the nonedges `zv,zw`, and the literal sectors. The
[sector theorem](frozen/audits/2026-10-16-r6-joint-zero-c4c3d99/C/PROOF.md)
states that every induced C4 meets m or z and crosses its original sectors;
with order `m,z,u,v,m`, only `(u in L_a,v in L_s)` or
`(u in L_c,v in L_t)` is possible. In particular
`alpha in L_a intersect L_t`, `beta in L_c intersect L_s`.

Work in direction 101: `X=V(e) union V(g)`, `H=D-X-f`, and choose a
maximum-cardinality Tutte-violating set S. The
[barrier theorem](frozen/audits/2026-10-15-three-edge-matchings-6ddea32/PROOF.md)
gives odd factor-critical components. The
[common-111 saturation theorem](frozen/audits/2026-10-16-r6-cap-barriers-c4c3d99/B/PROOF.md)
gives `tau=1`: both endpoints of f belong to different components of H-S.
Thus neither endpoint is in S or X, and f is internal to no component.

**Theorem.** Every five-cut component C of this maximum 101 barrier
has an induced primal boundary. Consequently it is a retained original
W5 component. A 101 maximum barrier with exactly one non-singleton
five-cut component is impossible. If it has two five-cut components,
both are W5 and satisfy the previous exact two-wheel rigidity.

The last assertions use the frozen
[induced-five theorem](frozen/audits/2026-10-16-r6-cap-barriers-c4c3d99/C/PROOF.md)
and [weighted curvature theorem](frozen/audits/2026-10-16-r6-cap-barriers-c4c3d99/A/PROOF.md).
It remains to prove inducedness, without assuming it at any intermediate
five-cycle step.

## 2. A chord gives an exterior facial ear

The actual cut of C is a bond: its complement is connected, since two
complementary components would each require at least three cut edges.
Its primal image is therefore a simple five-cycle Q, with exactly the
faces of C on one side. Since tau=1, `H[C]=D[C]`.

A non-singleton factor-critical graph has minimum degree at least two:
if u had unique neighbour v, deleting v would leave u isolated in a
nonempty even graph. Connectivity excludes degree zero.

Suppose Q has a chord xy. The shorter Q path is `x,t,y`; the triangle
`x,t,y` is an actual face F, because every J triangle is facial and the
other two Q vertices lie on its other side. If xy lies on the C side,
F belongs to C and has only one neighbour inside C, across xy. This
contradicts the preceding minimum-degree observation. Hence xy lies on
the exterior side, F is outside C, and F has two distinct neighbours in
C across xt and ty.

F cannot be in another component of H-S: the only D edge between
distinct such components is f, whereas there are two F-to-C edges.
Thus **F is in S or X**. Adding the face F to the disk C gives a disk
R with four-cycle boundary Q', obtained by replacing `x,t,y` with xy.
Its face set is exactly `C union {F}`.

**Q' is induced.** A chord of a four-cycle in this triangulation makes
one side the disk of two facial triangles. The R side has at least four
faces, because a non-singleton odd C has at least three. Its other side
contains at least three faces from `X minus {F}`. Neither side can be
the two-face disk, a contradiction. This argument also excludes further
chords of Q' and does not require any source-order bound.

## 3. The ear cannot be in S

Suppose F belongs to S. The R disk avoids every face of X. Both mz faces
are in X, so mz is not a boundary edge of R. Inducedness then prevents
Q' from containing both m and z. It cannot avoid both by the induced-C4
source theorem.

If Q' contains m alone, the incident R faces occupy one nonempty link
interval avoiding `mvw,mz alpha,mz beta`. Deleting these three link edges
leaves the singleton z and the two original sector paths L_s,L_t.
The two Q' neighbours of m are therefore in the same sector, contradicting
the induced-C4 sector theorem.

If Q' contains z alone, that theorem requires its two neighbours to lie
in opposite a/c fans. Its R interval avoids both mz faces, so it runs
through pq and includes the entire face zpq. F is not an endpoint of f
because F is in S. Consequently zpq is in C, and the other endpoint of
f is in a different component. That endpoint is neither in C nor F,
so f crosses R. Thus pq is an edge of Q'. The vertices z,p,q form a
triangle, impossible in an induced four-cycle. This excludes F in S.

## 4. The ear cannot be in X

Suppose F belongs to X. Its two edges to C are not its forced matching
edge, whose other endpoint also belongs to X. Its remaining third edge,
dual to xy, must therefore be e or g. There are exactly two cases.

### 4.1. The chord is vw

Q' contains the edge vw. It cannot contain m, which is adjacent to both
v and w and would create a triangle in an induced C4. It cannot contain
z: each of the other two positions of a C4 with edge vw is adjacent to
v or w, and both zv,zw are nonedges. Hence Q' avoids both hubs,
contradicting the induced-C4 source theorem.

### 4.2. The chord is mz

Write the order of Q' as `m,z,u,v,m`. The ear F is either `mz alpha`
or `mz beta`. First take F=`mz alpha`, so the original five-cycle order
is `m,alpha,z,u,v,m`.

The C interval at m avoids all of X, including `mvw` and both mz faces.
Its two neighbours alpha,v must be in the same original sector. Since
alpha is in L_t, v is in L_t. The induced-C4 sector theorem for Q'
then forces u into L_c. At z, the C interval between alpha in L_a and
u in L_c avoids the two mz faces. It therefore contains zpq. Saturation
again forces pq to be an edge of the ORIGINAL Q.

That is impossible. Both p,q are neighbours of z. The only Q edge not
incident with m or z is uv; inducedness of Q' says zv is a nonedge,
so uv cannot be pq. All other Q edges have an endpoint m or z, neither
of which is p or q. For F=`mz beta`, the same literal argument puts
v in L_s and u in L_a; the C interval crosses the fans in the opposite
direction and yields the identical contradiction. Endpoint coincidences
alpha=p or beta=q do not change this edge list or the nonedge zv.

Both X cases are excluded. Every possible chord has now been excluded,
which proves the theorem.

## 5. Exact consequence and retained boundary

By the previous induced-five theorem, every 101 five-cut component is
an actual retained W5. The previous curvature bound excludes the single
W5 row. Together with the earlier all-singleton exclusion, **ordinary
101 failure now has only two maximum-barrier types**:

1. Two W5 components, with `r_cap+epsilon<=1`,
   `Delta=2(1-r_cap-epsilon)`, original `s,t<=8`, and `h<=6`.
2. One seven-cut component that is not a complete W7.

This does not exclude either remaining type or prove an ordinary 101
matching. It does not sharpen the 110 five-cut classification. Even an
ordinary matching would still need an even complement; `W110+W101>0`,
complete319 exclusion and the general unbounded claim remain OPEN.
No colouring is patched or projected, and all original full fibres,
including empties and all r lifts, remain part of the source contract.
No reconstruction is performed; its existing completed-source cost is
still k+5. General K<=22 and fixed-branch k>=25 are unchanged.

This is an arbitrary-size paper proof using frozen source theorems.
Finite controls separately calibrate the facial-ear step and expose
its failure without the source sector premises. No new external theorem,
source realization, finite census, Lean theorem or strict descent is claimed.
