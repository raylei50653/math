# The legal J fibre: a three-original-edge return criterion

BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`. Authority and live/frozen
hashes are in [INPUTS.json](INPUTS.json). The eight previous audits are
read-only; only this audit directory is written. This is an exact return
criterion and a new finite obstruction to a weaker Kempe argument. It is
not a source exclusion.

## 1. The complete source fibre, with no choice of separate witnesses

Use exactly the original minimum-source contract of the frozen six-pin
forcing proof: `d_G(x)=d_G(y)=d_G(b)=4`, `d_G(r)=6`,
`U=R-r`, outer order `(z,s,v,w,t)`, internal facial triangle `zpq`, and
all seven distinct pins. Put `m=[s=t]`. The previous proof establishes
that `J=U/(s=t)` is a simple sphere triangulation with `k-1` vertices.
Its specified facial triangles are `(m,v,w)` and `(z,p,q)`; `mz` is an
original edge constraint, representing the two original edges `sz,tz`.
Every other original U edge has its literal image in J. Suppressing this
one duplicate constraint loses no colouring or vertex identity in U.

There is a literal bijection

`Col_4(J) <-> {f in Col_4(U): f(s)=f(t)}`.

It copies the one m value to both s and t and retains every other vertex
value. The existing thin cap at interior cost `k-3<k` supplies at least
one complete J colouring. No marked pq palette is prescribed. The source
forbids, in **every** such full colouring, the event

`E: {f(v),f(w)} intersect {f(p),f(q)} = empty`.

The six names in this displayed event belong to the same J colouring.
In U one additionally writes `s=t`; that equality is already built into
J. No J colouring is discarded on account of its r-lift set. For E the
r colour is unique, so obtaining E would indeed contradict the inherited
all-r source condition.

## 2. Three retained edge constraints, rather than six marginal colours

Identify the four literal colours with `F_2^2={0,1,2,3}`, and for each
original J edge `ab` write `d(ab)=f(a) XOR f(b)` in `{1,2,3}`. Set

`e=vw`, `f_edge=pq`, `g=mz`.

**Lemma 1 (exact bridge).** For every complete proper J colouring,

`E <=> d(e)=d(f_edge) != d(g)`.

Proof. Two unordered distinct-colour pairs have the same XOR exactly
when they are identical or complementary: for each nonzero difference,
the four colours split into its two disjoint pairs. Complementarity is
exactly E. If the pairs are identical, each triangle forces its third
vertex m or z into the complementary pair; `mz` then forces them to be
its two distinct colours. Hence `d(g)=d(e)=d(f_edge)`. If the pairs are
complementary, m belongs to the pq pair and z belongs to the vw pair, so
their difference cannot be the within-pair difference. Conversely, equal
edge differences with `d(g)` different cannot be the identical-pair case.
All implications are literal at this one full colouring. QED.

The edge `mz` is essential: equal differences alone do not distinguish
identical palettes from complementary palettes. The 432 proper labelled
assignments of the two triangles plus `mz` include exactly 96 E rows.
This finite count is an identity, not a realizability assertion.

## 3. A dual cycle switch returns an entire colouring

The sphere dual `J*` is cubic. In every triangular face the three nonzero
edge differences are distinct, so they give a proper three-edge-colouring
of `J*`. Fix two nonzero differences `a,b`. Their dual edges form disjoint
cycles; record a cycle by its crossed **original J edges**, not by a
terminal partition inferred from separate witnesses.

**Lemma 2 (full lift of a cycle switch).** For any such cycle C, put
`c=a XOR b`, and add c to every primal vertex on one of its two sides.
This produces a complete proper J colouring, interchanges labels a,b
exactly on the crossed edges, and leaves all other edge differences
unchanged. This operation is an involution.

Proof. A simple dual cycle separates the sphere; original edges cross it
at most once, and exactly the edges recorded in C cross it. Edges with
both endpoints on the same side retain their differences. A crossed
edge has difference a or b, so adding c to one endpoint changes it to b
or a and never to zero. Thus every original edge remains proper. Applying
the same vertex translation twice is the identity. Copying m back to s,t
then gives a full original U colouring, still with `s=t`, on the same
vertices and in the same literal colour frame. QED.

The operation may translate both complementary colour pairs on the
chosen side. It is not being mislabeled as one ordinary vertex Kempe
component swap. It is a simultaneous switch of actual components: an
edge of difference c does not cross C, so each component in either of
the two vertex-colour pairs paired by translation c lies entirely on
one side. Those ordinary switches commute and give the displayed full
translation. Conversely, an ordinary vertex Kempe component swap has a
cut consisting of dual cycles of the other two differences; taking the
corresponding sides gives that swap, up to a global translation. Hence
allowing products of these cycles and global colour permutations also
allows the ordinary Kempe operations relevant here.

## 4. Exact safe-cycle table, including simultaneous cycle switches

Let a state be a complete J colouring that does not satisfy E. For a
fixed difference pair write `u~v` when the dual copies of the two marked
original edges u,v lie on the same cycle of that pair. An edge whose
difference is absent from the pair lies on no such cycle. The following
table is necessary and sufficient for **every** independent subset of
the cycles in that pair to remain E-free.

| Initial `(d(e),d(f_edge),d(g))` | Relevant pair | Exact condition |
| --- | --- | --- |
| `(a,a,a)` | `{a,b}`, for each `b!=a` | `g~e or g~f_edge` |
| `(a,b,a)`, `a!=b` | `{a,b}` | `e~f_edge or e~g` |
| `(a,b,b)`, `a!=b` | `{a,b}` | `f_edge~e or f_edge~g` |
| `(a,b,c)`, all distinct | `{a,b}` | `e~f_edge` |

Pairs not indicated cannot change the inequality between the e and
f_edge differences, or change neither of them. They cannot create E.

**Theorem 3 (one-cycle return alternative).** For any failed full state
and fixed difference pair, either the corresponding row in this table
holds and the entire commuting cycle cube is E-free, or one single
cycle already returns a complete E colouring. Thus a search over many
cycles of one pair cannot improve on a one-cycle return at that state.

Proof. Give each actual cycle an independent bit recording whether it
is switched. The label at each marked edge is toggled by its cycle bit.
For `(a,a,a)`, if g shares a cycle with e or f_edge, equality of the final
first two labels forces the third to agree. Otherwise switching only
the g cycle makes E. For `(a,b,a)`, e and f_edge on one cycle stay
different, while e and g on one cycle stay equal; either prevents E.
If neither coincidence holds, switch the e cycle: f_edge stays b and
g stays a, so the new triple is `(b,b,a)`. The `(a,b,b)` case is reflected.
For three distinct labels, g is outside the `{a,b}` cycles; e,f_edge on
one cycle stay different, and otherwise switching the e cycle gives
`(b,b,c)`. These arguments prove both the safe cube and the one-cycle
return assertions. QED.

Consequently a genuine source must obey this table at **every full J
colouring**, with cycles obtained from its actual retained edges. A
violation is a checkable return certificate consisting of that complete
colouring, the two differences, one dual cycle as original edges, its
primal side, and the translated full colouring. The checker verifies all
these objects in the positive control. This is a precise new source
necessity, not a proof that any source violates it.

## 5. A planar control rules out an unconditional Kempe return claim

The first control has vertices `0,...,11`. Set `A_i=2+(i mod 5)` and
`B_i=7+(i mod 5)`. Its twenty triangular faces are, for `i=0,...,4`,

`(0,A_i,A_(i+1)), (1,B_i,B_(i+1)),`
`(A_i,A_(i+1),B_i), (A_i,B_(i-1),B_i)`.

These are two pentagonal caps and a triangulated connecting annulus.
Name `(m,v,w,z,p,q)=(0,2,3,4,5,9)`. Both designated triangles are actual
faces, `mz` is an edge, and none of `pv,pw,qv,qw` is an edge. Every vertex
has degree five and every triangle is facial (the latter also follows
directly by enumerating all vertex triples in this explicit graph).

Its 240 complete labelled colourings contain 24 E colourings and 216
E-free colourings. The exact table in section 4 holds at **all** 216
E-free colourings for all three pairs. The checker reconstructs every
dual cycle and translates every side, so this is not a check on just
the marked partitions. The set of those 216 full colourings is therefore
closed under every dual cycle switch. Induction gives closure under
every finite sequence; global colour permutations preserve E as well.
By the component description in section 3, ordinary vertex Kempe
sequences cannot leave this E-free set either.

Thus the weaker statement “from an arbitrary complete J colouring one
can Kempe-return to E using only the two marked facial triangles, mz,
planarity, the four cross nonedges, minimum degree five, and absence of
nonfacial triangles” is false. This does not rule out choosing a
different Kempe class using some source theorem, or an operation outside
the stated class.

The complete source is crucial. Splitting m along its actual link at z
and between v,w gives an actual triangulated U with outer
`(z,s,v,w,t)`. It has 864 full colourings, of which exactly 240 have s=t
and match the J full lifts. Its degrees `(d_U(z),d_U(s),d_U(t))=(6,4,2)`
violate the source requirements `d_U(z)>=7` and `d_U(s),d_U(t)>=4`.
This is not a minimum-source realization, an r6 exclusion, or a
counterexample to the true source claim.

## 6. Positive returns, empty fibres, and verification scope

The second control flips original edge `0--5` of the displayed sphere
to its opposite nonedge `4--6`, retaining the six named vertices and
both designated faces. Its 288 full J colourings include 96 E states.
There are 96 failed-state/difference-pair cases violating the table;
each stores its complete one-cycle returns. Its split U has 960 full
colourings. It is a plane control, not an asserted source transformation
or smaller bad graph: the deleted edge is explicit, and no use of this
flip is made on the hypothetical source.

The third control starts with tetrahedron `0,1,2,3`, inserts vertices
4,5,6,7 in faces `(1,2,3)`, `(1,4,3)`, `(1,4,5)`, `(1,5,6)`, and uses
`(m,v,w,z,p,q)=(0,2,3,1,6,7)`. Each insertion has a unique fourth colour,
so its 24 full colourings are one global colour orbit; every one fails
E. It has the two designated faces, mz, and all four cross nonedges.
It has separating triangles and low degrees. It confirms that these
marked edges and face identities by themselves do not force E even
when every complete colouring is considered. Its split U has 96 full
colourings.

For all three controls the certificate stores all `4^6` J pin fibres,
all `4^7` split-U pin fibres including empties, all private-vertex lifts,
and all original r lifts, including empty r-lift sets. The J-to-U
bijection is compared with an independent enumeration of the complete
U colourings. Closed-surface checks verify edge incidence, orientability,
all vertex links, connectedness, and Euler characteristic two. The
165 abstract marked cycle cubes are also exhausted; they are finite
algebraic validation, not source realizability. The checker imports no
previous certificate or checker.

Normal replay, `PYTHONHASHSEED=17`, damaged complete-lift/empty-fibre/
return certificates, exclusive-create rejection, and frozen-input drift
are recorded in [VERIFICATION.json](VERIFICATION.json). Genuine original
sources supplied: zero, **not triggered**. What remains is to prove that
the original source geometry forces a failure of the table in some
full J state, or to supply a different source-preserving construction
that forces E. All-size 319 exclusion, a strict completed-source descent,
and the general theorem remain OPEN. Splitting m and restoring r,x,y,b
and the a/c split restores the original order; the reversible switches
here do not lower completed-source size. No 4CT, external enumeration,
Lean theorem, shared-document update, commit, or push is used.
