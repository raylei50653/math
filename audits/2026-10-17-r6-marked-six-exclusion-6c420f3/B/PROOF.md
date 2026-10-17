# B: full-source marked six-cycle exclusion and cyclic-cut corollary

Frozen BASE `6c420f3ca77d60952ed76f93dff7449c522715ca`.
The exclusive source manifest is [../INPUTS.json](../INPUTS.json); all source
references below point into its frozen copies. This worker writes only `B/`.

**Conclusion.** Under the original full `r=6` source contract, every simple
cycle of J containing both `vw,pq` has length at least seven. Every cyclic
edge cut of the actual dual D containing `e=vw*` and `f=pq*` likewise has
size at least seven. Neither conclusion assumes `d_G(v)=5`.

## 1. The one original source and the exact inputs

G is the globally minimum noncatalogue plane C5 disk, secondarily chosen
with maximum edges, with original induced boundary `(x,y,a,b,c)`, one
fixed original support in `{932,933,941}`, and

`d_G(x)=d_G(y)=d_G(b)=4`, `d_G(r)=6`.

Keep its original edge apexes `(r,t,p,q,s)` for `(xy,ya,ab,bc,cx)` and
its original r rotation `(x,y,t,w,v,s)`. Use the already constructed same
graphs `U=R-r`, `J=U/(s=t)`, `m=[s=t]`, and actual embedded dual `D=J*`.
The other distinguished vertex is `z=[a=c]`; the marked primal edges
`vw,pq,mz` and their original embeddings are retained. All degrees denoted
`a0,c0` are the original `d_G(a),d_G(c)`. In particular

`a0+c0>=11`, `d_G(s),d_G(t)>=6`.

The [frozen source-geometry proof, §§2–5](../frozen/audits/2026-10-15-j-source-geometry-6ddea32/PROOF.md)
supplies the following exact, arbitrary-size facts:

1. J is a simple sphere triangulation with every triangle facial.
2. Its faces on `mz` are exactly `mz alpha` and `mz beta`, with alpha
   from the original a fan and beta from the original c fan. The two
   fan vertex sets are disjoint; `alpha=p iff a0=4` and
   `beta=q iff c0=4`. Thus
   `N_J(m) intersect N_J(z)={alpha,beta}`.
3. `W=J-{m,z}` is the actual complementary closed disk. Its boundary is
   the original m-link path from alpha through `w,v` to beta, followed
   by the reverse of the original z-link path from alpha through `p,q`
   to beta. Its four distinct terminals therefore occur in cyclic order
   `(w,v,q,p)`. Literal `alpha=p` or `beta=q` does not duplicate a vertex
   and does not change this four-terminal cyclic order.
4. Every three-edge cut of D isolates a single vertex on one side.
   There is no cut of size one or two.

The [frozen marked-cut addendum, §§1–2](../frozen/audits/2026-10-16-r6-319-continuation-f1faf74/C/MARKED_CUTS.md)
retains the old cross nonedges `vp,vq,wp,wq` and the original nonedges
`zv,zw`. These nonedges hold in the full source; no v5 compulsory-colouring
calculation is used here. In particular, a cycle through `vw,pq` has
length at least six: both connecting portions have length at least two.

We use the [proper-C5 small-cap theorem, §§2–3](../frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md):
the original bounded cap of any simple C5 other than the original outer
boundary is empty, or exactly one W5 centre with all five spokes and no
additional boundary chord in that cap. It applies also when a proper
cycle meets the original boundary. Original inner degrees are at least
five, original triangles have empty bounded interiors, and G is internally
triangulated. We use the separately adopted
[low-p/q theorem](../frozen/audits/2026-10-14-lowpq-source-676b102/pq/PROOF.md):

`d_G(p)=5 => a0>=6`, `d_G(q)=5 => c0>=6`.

Finally the new two-step lemmas, independently proved in
[A/PROOF.md](../A/PROOF.md), are used in exactly this form:

`p-h-w in J => a0<=5`, `q-h-v in J => c0<=5`.

These include the `h=m` cases, where the relevant degree is four, and
exclude `h=z` by `zw,zv` absent. For other h their witnesses are the
proper original cycles `(a,p,h,w,t)` and `(c,q,h,v,s)`. Their proof
uses the original bounded side and complete small-cap structure.

No additional source or colouring is selected below. Every ordered pin,
attachment, fixed support, private-colouring fibre, empty fibre, and full
original lift remains that of this one source. The proof only restricts
its actual edges and disks.

## 2. A complete six-cycle split

Suppose C is a simple six-cycle of J containing the two disjoint edges
`vw,pq`. Removing these edges leaves two vertex-disjoint connecting paths.
The four cross nonedges force each path to have at least two edges;
since there are four edges left, both have exactly two. Consequently,
up to reversing the cyclic orientation, there are exactly two pairings:

| Pairing | Connecting paths | Representative C |
| --- | --- | --- |
| I | `v-h1-q`, `w-h2-p` | `(v,h1,q,p,h2,w)` |
| II | `v-h1-p`, `w-h2-q` | `(v,h1,p,q,h2,w)` |

Here `v,w,p,q,h1,h2` are six distinct vertices. Neither midpoint can be z,
because either midpoint has an edge to v or w, whereas `zv,zw` are
absent. The vertex m occurs at most once. Every other midpoint is a
retained original inner vertex, not one of the original deleted/split
collar vertices.

For pairing I, A's two-step lemmas give respectively `c0<=5` and `a0<=5`,
contrary to `a0+c0>=11`. This also disposes of all its m cases; no separate
same-sector lifting premise is silently imposed.

It remains to exclude pairing II.

## 3. Alternating terminals in the actual disk

First suppose both connecting paths of pairing II avoid m. They already
avoid z, so both lie entirely in the actual disk W. Its boundary has
cyclic order `(w,v,q,p)`, and the two paths join alternating terminal
pairs `v--p` and `w--q`.

For completeness the familiar disk obstruction also covers paths with
boundary midpoints. An embedded simple path with distinct boundary
endpoints can be moved, fixing those endpoints, slightly into the disk
at every other boundary contact. If two embedded paths are disjoint,
take disjoint sufficiently small neighbourhoods of them and perform
these moves in their respective neighbourhoods; they stay disjoint.
Each path is now a proper arc of the disk. A proper `v--p` arc separates
the disk into two sides, with w and q on opposite boundary arcs. Every
`w--q` path must meet the first arc, contradicting disjointness.

The six-cycle gives vertex-disjoint embedded paths, so this obstruction
applies. It does not assume that h1,h2 were disk-interior vertices or
that alpha,beta were distinct from p,q. Thus pairing II must use m.
Its two paths are disjoint, so exactly one uses m. There are precisely
two remaining cases:

`v-m-p` with `w-h-q`, or `v-h-p` with `w-m-q`.

We treat these in the original G separately. No whole-source reflection
and no changed support mask is used.

## 4. The `v-m-p` exception forces `p=5,a0=4`

The edge mp and the retained edge zp form the triangle `mzp`. It must
be one of the two actual faces at mz. Its third vertex p is on the a
fan, and cannot be beta on the disjoint c fan. Hence `p=alpha`, so
`a0=4`. In particular `(a,t,p)` is an actual original face. The degree
sum gives `c0>=7`, whence `q!=beta`, so mq is absent. In particular,
the original edge tq is absent. This derives the necessary mp/mq
identities from full-source facial geometry without the old v5 lemma.

The other connector is `w-h-q`; its h is different from m,z and the
four terminals. Its edges are retained original edges. Consequently

`Qp=(t,p,q,h,w)`

is a genuine simple proper C5 in G: `tp` was just established, `pq,qh,hw`
are original edges, and `wt` is in the original r-neighbour ring. Its
five vertices are distinct original inner vertices. No identified vertex
is substituted for t, and this is not the crossed pentagon
`(m,q,p,h,w)` left open by the previous v5 audit.

At p the following three actual original faces lie outside the bounded
cap of Qp:

`(t,p,a)`, `(a,p,b)`, `(b,p,q)`.

The first comes from `a0=4`; the other two come from the original ab
apex and the degree-four b fan. Original boundary vertices a,b lie
outside Qp. These three faces therefore fix the entire exterior link
segment at p to be `t,a,b,q`. There is no position for an extra exterior
neighbour: consecutive entries of that segment are actual facial wedges,
and its complementary segment from q back to t is precisely the bounded
side of the Qp disk.

If the cap is empty, it is a triangulated pentagon. Its five potential
diagonals are `tq,th,ph,pw,qw`. The nonedges `tq,pw,qw` leave only `th,ph`,
and both must occur, since an empty pentagon triangulation uses two
diagonals. Thus the cap link at p is `t,h,q`. Combined with the fixed
exterior segment, its complete original neighbourhood is

`N_G(p)={t,a,b,q,h}`.

If the cap contains one centre u, the full W5 conclusion gives cap link
`t,u,q`, with no boundary chord in the cap. The complete original
neighbourhood is then

`N_G(p)={t,a,b,q,u}`.

Both are five-element sets. Thus `d_G(p)=5` while `a0=4`, contrary to the
adopted low-p implication `p=5 => a0>=6`. This excludes the first m case.

## 5. The `w-m-q` exception forces `q=5,c0=4`

Now the edge mq and the retained edge zq form facial triangle `mzq`.
The vertex q is on the original c fan, so `q=beta` and `c0=4`. The
original face `(c,s,q)` is present. Since `a0+c0>=11`, we have `a0>=7`,
so mp is absent and in particular the original edge sp is absent.

The other path is `v-h-p`, with h an actual retained original inner
vertex. The literal original five-cycle is

`Qq=(s,q,p,h,v)`.

Its edges `sq,qp,ph,hv,vs` are original edges; `vs` belongs to the
original r-neighbour ring. These are five distinct original inner
vertices. Its bounded cap again falls under the proper-C5 theorem.

At q the exact exterior facial segment is now

`(s,q,c)`, `(c,q,b)`, `(b,q,p)`.

The first comes from `c0=4`, the second is the bc apex face, and the
third comes from the same original degree-four b fan. Boundary vertices
c,b lie outside Qq. Hence the complete exterior q-link is `s,c,b,p`,
with its other segment entirely in the cap.

For an empty cap the potential diagonals are `sp,sh,qh,qv,pv`. The
nonedges `sp,qv,pv` leave exactly `sh,qh`; both must occur. The cap q-link
is `s,h,p`, giving

`N_G(q)={s,c,b,p,h}`.

For a one-centre W5 cap the cap q-link is `s,u,p`, giving

`N_G(q)={s,c,b,p,u}`.

Thus `d_G(q)=5,c0=4`, contrary to the adopted original implication
`q=5 => c0>=6`. This excludes the second m case directly in the same G.
Sections 2–5 exhaust every simple six-cycle through `vw,pq`.

## 6. Small cyclic cuts are bonds

Let `delta_D(X)` be a cyclic edge cut of size at most six: both induced
cut sides have a cycle. D is cubic and connected, has no one/two-edge
cut, and every three-edge cut isolates one vertex on one side.

Suppose `D[X]` is disconnected. Choose a component K containing a cycle.
Its complement also contains a cycle, because it contains `D[V(D)\X]`.
It therefore cannot have exactly three outgoing edges: a three-edge cut
would isolate a vertex on one of those two cycle-bearing sides. Its
number of outgoing edges is at least four. Every additional component
has at least three outgoing edges. Since distinct components of `D[X]`
have no edges to one another, these outgoing edge sets are disjoint and
their sizes sum to `|delta_D(X)|`. Two components would thus cost at
least `4+3=7` edges, a contradiction. Applying the same argument to the
other cut side proves both sides connected.

The cut is consequently a bond. In the fixed planar duality its primal
edge set is one circuit, hence a simple J cycle. This is the standard
bond/circuit duality for the actual embedding: deleting the bond splits
D into exactly its two connected sides, and its dual edges give their
single minimal separating boundary. J is simple, so it has no one/two-edge
circuits. If the cut contains e and f, that primal simple cycle contains
`vw,pq`. The cross nonedges already exclude lengths at most five, and
Sections 2–5 exclude length six. Therefore

`e,f in delta_D(X)` and `delta_D(X) cyclic => |delta_D(X)|>=7`.

The cut need not be chosen by a particular matching or Tutte barrier.
Conversely this argument does not claim every six-cycle gives a cyclic
cut: one side of a simple primal cycle can have an acyclic dual side.

## 7. Calibration, scope, and the remaining positive endpoint

[check.py](check.py) verifies every frozen manifest hash, independently
enumerates all connector pairings on six labelled vertices, enumerates
all five pentagon triangulations on each original cap, and glues each
retained empty/W5 cap to its three original exterior faces. The resulting
complete p/q links have exactly five vertices in all four cases. It also
checks the four literal endpoint variants of the disk's terminal order
and the small-cut component arithmetic. Its finite output is
[certificate.json](certificate.json); replay and rejection receipts are
in [VERIFICATION.json](VERIFICATION.json).

These checks calibrate the finite local combinatorics. The original
bounded sides, full-source two-step lemma, actual complementary disk,
arbitrary-size Jordan separation, and cut duality are paper arguments.
There is no finite enumeration of arbitrary sources here. Genuine
minimum-source instances supplied: zero, **not triggered**.

The theorem excludes the old `v5,c0=4` marked-six residual and additionally
excludes every such marked six-cycle without v5. It does not establish
`W110+W101>0`, `omega_e=0`, a shorter-source reconstruction, or the
all-size 319 exclusion. In particular it gives no lower bound on lengths
of odd cycles of `D-M`: in the intended joint family e is a matching
edge and therefore absent from that complement. No external theorem,
4CT invocation, new Lean theorem, shared-document edit, commit, or push
is part of this worker's contribution.
