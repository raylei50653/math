# A. Two safe interval switches and an exact same-O interface

Frozen BASE `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`.
Independent write scope: `A/` only. This proof uses the frozen
two-cycle-cap proof and its B proof, and the frozen seven-five-repair A
proof. It invokes no external theorem. Its principal result is the
arbitrary-size conditional interval repair in sections 3--5; it does
not prove that one of the two required intervals succeeds.

## 1. The literal source and complete complement

Retain the original globally minimum completed no4ct C5 source G,
ordered boundary `(x,y,a,b,c)`, original x,y,b degree four and r degree
six, support in `{932,933,941}`, rotation, private vertices and actual
attachments. Retain the complete U319 relation, including every empty
fibre, the complete `(v,r,x,y,b)` reconstruction and every original r
lift in the same colour frame. The graphs remain the literal
`J=U/(s=t)`, `m=[s=t]`, `D=J*`, with
`e=(vw)*`, `f=(pq)*`, `g=(mz)*`. There is no added original v-degree-five
assumption, new source, quotient, or smaller bad source.

Fix an actual ordinary `M in P101` with

`F=D-M=C disjoint-union O`,

where C is the complete active-f nonfacial seven-cycle. These are the
only two complete components. Consequently O is odd. The established
two-star cap has its four-degree centre `u in {p,q}`, ordinary
five-degree centre h, one internal matching chord, and five matching
spokes. Label this actual cap

`C=(0,1,2,3,4,5,6)`, chord `03`, ports `1,2,4,5,6`,

with the four-degree centre on the `0,1,2,3` side of chord03. For each
port i let `t_i` be the actual outer end of its matching spoke. All
`t_i` are distinct and lie on O. The literal e and g are matching
chords of O, since both endpoints of both marks are outside C.

This labeling names actual vertices and edges in one source. It is
not permission to choose a new embedding or independently replace
the exterior matching, its cyclic order, or its parities.

## 2. The f/z incidence fixes which intervals are safe

The actual two-star links, not an arbitrary placement of three dual
marks, give the following useful normalization.

* If `u=p,h=ell`, the seven faces may be ordered
  `pqell, pzq, pzn, pnell, ell n u2, ell u2 u1, ell u1 q`.
  Thus `f=01`. The ports in order are dual to
  `zq,zn,n u2,u2 u1,u1 q`. In particular the rim vertex z is between
  ports1 and2.
* If `u=p,h=n`, order the faces
  `pnz,pzq,pqell,pell n,n ell u1,n u1 u2,n u2 z`.
  Thus `f=12`. The ports are dual to
  `zq,qell,ell u1,u1u2,u2z`. Here z is between ports6 and1.

The q-centred cases are the literal reflection of these same lists.
Reversing the indexing can place the second z sector between ports2
and4; it does not move z to sector45 or56.

Take the disk bounded by O which contains C. The five disjoint spokes
occur in cyclic order `1,2,4,5,6` on both boundaries of the intervening
annulus. A chord of O drawn on this side is confined to a single
interport interval: otherwise it crosses a spoke. Interior matching
chords are noncrossing within each such interval. The primal edge mz
lies on the cap side of O, in the sector corresponding to the actual
rim vertex z. The edge vw is on the other side of O. These side
assertions also follow directly from the established primal matching
graph: its rim component is the unicyclic zero component containing
Q5,mz; its other exterior component is the value-one tree containing
vw; the cap's centre K2 is on the cap side. Equivalently, the embedded
cycle O separates the two components obtained by omitting it from the
dual adjacency of primal faces. The root of the branch containing mz
is z, so mz belongs specifically to the z sector.

It follows that each of the two actual O intervals

`I45=t_4 O t_5`, `I56=t_5 O t_6`

has all the following properties:

1. its cap-side matching chords avoid e and g;
2. its corresponding cap edge, respectively45 or56, avoids f;
3. its interior contains no other spoke endpoint.

These are the **two safe intervals** used below. The interval
notation means the subarc between consecutive ports which contains
no other port, not an independently chosen route around O.

The f/z incidence is necessary when using abstract controls. For
example, a graph with `f=12` and g in sector56 does not satisfy this
literal normalization even if it has the same cap, five spokes,
planarity, an even111 reference, and an all-distinct reference.

## 3. The actual monotone chain on a safe interval

Write either safe interval in its actual O order as

`I=(v_0=t_a,v_1,...,v_L=t_b)`,

where `(a,b)` is `(4,5)` or `(5,6)`. Run the following deterministic
construction, always on this one actual interval.

Start at `v_0`. Take its next O edge to `v_1`. More generally, after
arriving at an index j from the preceding O edge:

* if `j=L`, stop successfully;
* otherwise inspect the original M chord at `v_j`;
* if it is on the side of O opposite C, stop with that actual chord
  as an exterior-side blocker;
* if it is on the cap side, follow it to its other end `v_k`, and
  continue with the next O edge `v_k v_{k+1}`.

Every followed cap-side chord has `j<k`. Here is a direct proof,
including why the construction cannot silently cycle or leave I.
The first chord cannot end left of `v_1`, because the only earlier
vertex is the spoke endpoint `v_0`, already matched by its spoke.
Inductively, the earlier used chords skip disjoint intervals
`[j_r,k_r]`, in increasing order. An endpoint of a later backward
chord cannot be an earlier chain vertex, since that vertex is already
matched. All remaining earlier vertices are strictly inside one of
the skipped intervals. A chord from such an interior point to a point
past `k_r` interlaces the endpoints of the used cap-side chord
`v_{j_r}v_{k_r}`, hence crosses it in the disk. This is impossible.
The sector property keeps both endpoints in I. Thus each step
strictly increases the index, and exactly one of the two stated
terminations occurs.

If it succeeds, let its used matching chords be

`d_r=v_{j_r}v_{k_r}`, `r=1,...,s`,

and let `ell_r=k_r-j_r` be the length of the **entire actual O subarc**
skipped by d_r. The resulting outside path P starts and ends with an
O edge and alternates O edges and M chords. It contains `s+1` O edges
and s matching chords.

Close P with the two actual matching spokes and the actual cap edge
ab. This yields one actual simple M-alternating cycle Q. Its vertices
are distinct: P is monotone and outside C, and its only spoke
endpoints are its two ends. By section2, Q avoids all three literal
marks. Consequently

`N=M triangle E(Q) in P101`.

No independent exterior witness is needed: Q is constructed from M
on the same graph. It is already a valid batch consisting of one
vertex-disjoint alternating cycle.

## 4. Every complete new complement cycle is explicit

For a successful chain, the complete new complement `D-N` consists
of exactly the following cycles:

* for each r, the cycle made of d_r and the complete skipped O
  subarc `v_{j_r} O v_{k_r}`, of length `ell_r+1`;
* one remaining cycle, containing `C-ab`, the two spokes, and all
  O vertices outside the union of the closed skipped subarcs.
  The endpoints of each skipped subarc belong to its separate
  pocket cycle.

To check this statement edge by edge, the switch deletes from the
old complement precisely ab and the `s+1` used O edges, and adds
precisely the two spokes and the s used chords. Between successive
deleted O edges lies exactly one skipped subarc. Adding its chord
closes it; neither the chain nor another added chord meets its
interior. The rest of O is one path from `t_b` back to `t_a`.
Joining that path to `C-ab` through the two spokes produces the
remaining cycle. Original matching chords not used by Q stay out of
the complement. Thus hidden chords inside a skipped subarc cannot
alter its complete complementary cycle. All vertices of the old two
cycles have been accounted for exactly once.

Let

`j = number of r for which ell_r is even`.

Exactly j of the skipped-subarc cycles are odd. Since `|V(D)|` is
even, the parity of the remaining cycle is `j mod 2`. Hence the exact
full oddness, not just local cap oddness, is

`odd(D-N)=j+(j mod 2)`.                              (A1)

In particular:

**Theorem A1 (safe odd-arc chain repair).** If either safe interval's
monotone chain reaches its other port and every skipped O subarc has
odd length, the actual Q above gives an even-complement matching
`N in P101`. It repairs both original odd cycles simultaneously.

Conversely, for this constructed Q, even complement holds only if
every skipped subarc has odd length. A successful path alone is
insufficient: one or two even-length skipped subarcs leave complete
oddness two; three or four give complete oddness four.

The case s=0 is the adjacent-spokes four-cycle switch. The theorem
extends it to arbitrarily many actual internal matching chords and
arbitrarily long skipped O subarcs. It has no size bound and uses
neither a reference colouring nor the unavailable fixed-M SEP
condition.

## 5. An exact necessary blocker statement for a putative failure

Suppose the same literal two-cycle source has no even-complement
matching in `P101 union P110`. For **each** of I45 and I56, its
deterministic chain must then exhibit at least one of:

1. an actual exterior-side M chord at which the construction stops;
2. a used cap-side M chord whose entire skipped O subarc has even
   length.

If neither occurs, Theorem A1 constructs a forbidden even101
witness. The assertion is a necessary obstruction on each of two
specified intervals, with actual endpoints and actual O lengths.
It is not a sufficient obstruction to every possible repair: a
different alternating cycle or batch, or a switch to direction110,
can still exist. Nor does it prove that either blocker is impossible
in a minimum source.

One can stop the search early on the first even-length jump and
already have a blocker for this criterion. For a complete certificate
of the deterministic chain, continue until the successful endpoint or
the first exterior-side chord and retain the whole ordered list.

## 6. A finite cap interface retaining the entire same O

For completeness there is an exact finite interface for **all**
possible repairs, including batches beyond section3. Let S be the
ports whose spokes are selected by a prospective new matching N,
and let L be its internal cap matching. The cap has seven vertices,
so `|S|` is odd. There are thirteen local states whose cap complement
contains no complete odd cycle:

| S | L | Complement paths, with exact lengths |
| --- | --- | --- |
| 124 | 03,56 | 5--6:6 |
| 125 | 06,34 | 4--6:2; one even4-cycle |
| 126 | 03,45 | 4--5:6 |
| 145 | 06,23 | 2--6:6 |
| 256 | 01,34 | 1--4:6 |
| 456 | 03,12 | 1--2:6 |
| 1 | 23,45,06 | 2--4:4; 5--6:1 |
| 2 | 01,34,56 | 1--6:4; 4--5:1 |
| 4 | 01,23,56 | 5--6:4; 1--2:1 |
| 4 | 03,12,56 | 1--6:2; 2--5:3 |
| 5 | 12,34,06 | 1--2:3; 4--6:2 |
| 6 | 01,23,45 | 4--5:4; 1--2:1 |
| 6 | 03,12,45 | 1--5:3; 2--4:2 |

Completeness is elementary. Choose odd S from the five ports and
match all remaining vertices using the eight internal edges
`01,12,23,34,45,56,60,03`. There are seven states with one selected
spoke, seven with three, and one with five. The omitted three-spoke
state `S=456,L={01,23}` leaves the internal odd5-cycle
`0,3,4,5,6`; the five-spoke state leaves C itself. Both are impossible
in any full even complement. The other thirteen states are listed.

For one listed state, take one actual exterior matching of all O
vertices except the `t_i` with i in S; those exceptional vertices
are matched by the selected spokes. In the exterior complement,
`T={1,2,4,5,6}-S` are precisely the degree-one endpoints. Retain all
its complete closed cycles and all its paths.

* If `|S|=3`, there is one exterior path. If all exterior closed
  cycles are even, this path automatically has even length:
  the exterior has `|O|` vertices and `|O|-1` complement edges,
  and `|O|` is odd. Its cap path has even length, so their union
  with the two spokes is even.
* If `|S|=1`, there are two exterior paths. If all exterior closed
  cycles are even, their length sum is odd, since the exterior has
  `|O|-2` complement edges. Exactly one path is odd. The two cap
  paths likewise have opposite parity. If the exterior endpoint
  pairing differs from the cap pairing, their union is one cycle
  and is automatically even. If the pairings agree, there are two
  cycles, and each exterior path must have the same parity as its
  paired cap path. The two matching spokes on each resulting
  cycle contribute even length.

In the differing-pairing case the single complete cycle contains
four spokes, also an even contribution. No path or complete exterior
cycle may be omitted. Planarity restricts both endpoint pairings to
the noncrossing pairings on these four ordered ports, but the stated
parity calculation itself does not require that restriction.

The mark test is imposed on this same exterior witness:

`e in N`, `g in N iff f notin L`.                     (A2)

Together, the thirteen states, (A2), and the complete exterior
cycle/path condition are necessary and sufficient for an actual
even-complement N in `P101 union P110`. Sufficiency assembles an
actual perfect matching on the same D. Necessity is its restriction
to the cap and exterior. Its symmetric difference with M then is
the required actual batch of vertex-disjoint alternating cycles.

## 7. The exterior test uses only the actual ordered O and its chords

The interface can be represented without inventing any exterior graph
or using independently feasible marginal pairings. List every O
vertex in order, every original M chord with its two actual indices,
and the five actual spoke indices. For one S, choose a set
`B subseteq E(O)` and require:

1. B is a matching along O;
2. `t_i` is covered by B exactly when `i notin S`;
3. for each original M chord xy of O, either both x,y are covered
   by B or neither is;
4. neither endpoint of e is covered, and the endpoints of g are
   covered exactly when `f in L`.

Define A to be the original M chords whose endpoints are covered by
B. The exterior matching is exactly

`N_out=(M_chords-A) union B`,

and its complete exterior complement is exactly

`H_out=(O-B) union A`.                               (A3)

These formulas prove a bijection: every exterior matching uses only
O edges and original M chords, and the matching constraint at a
chord endpoint forces its mate to have the same covered status.
At the five ports, the prescribed spoke status forces condition2.
Thus (1)--(4) are an exact finite Boolean condition on one ordered O.

For component parity, cut the actual O at every B edge and retain
each resulting subarc with its actual endpoints and integer length.
Add the actual chords in A, each of length one. The assembled
components are exactly (A3). The XOR of the retained arc lengths
and added chord lengths gives each complete component parity.
This is an arbitrary-size reduction to ordered endpoints, chord
pairs, arc lengths and the literal marks. It does not replace these
data by a free planar matching or independently realizable states.

Sections6--7 are an exact test, not an existence theorem. They retain
the full O, including complete odd cycles created far from the cap.
The new local theorem isolates two explicit sufficient states and
their complete necessary blockers without requiring a search over
this entire interface.

## 8. Independent finite replay and cross-review

[check_interface.py](check_interface.py) retains all thirty-two
selected-spoke masks, including every empty local matching fibre,
in [interface-certificate.json](interface-certificate.json). There
are fifteen actual cap matching states, thirteen without a complete
internal odd cycle. Independent whole-graph recursive perfect
matching enumeration is compared with the ordered-O Boolean
assembly, and every reconstructed matching's complete complement
is compared with the interface parity test. Two corruption checks
reject deletion of an empty mask and alteration of an actual path
length.

The finite controls are explicit small cubic graphs only. The
weak no-repair control with f12 and g in sector56 fails the literal
f/z incidence and is recorded as such. A second control respects
the literal sector positioning and has a safe interval56 switch
to one complete even20-cycle. In that same graph a different safe
nonmonotone switch replaces complete lengths7,13 by9,11; the full
oddness is still two. This independently verifies why safety and
removing C do not replace the full-cycle calculation.
Two further controls exercise an actual jump: an odd skipped
subarc of length3 gives complete lengths4,16, while an even skipped
subarc of length2 gives complete lengths3,15. The latter control
has a triangular complementary pocket and lacks an all-distinct
reference; it tests the parity identity only. Even the controls
which respect the named sectors do not have the original source's
degree bounds or complete fibres.

Across these four controls, whole-graph recursion and the same-O
interface agree on all160 perfect matchings and all their complete
parity tests. Normal and `PYTHONHASHSEED=17` replay produce identical
certificate bytes; hashes and negative-check results are retained
in [VERIFICATION.json](VERIFICATION.json).

The independent B review checked the literal f/z sectors and
the monotone Jordan argument and corrected the description of
the main circle's vertex set: skipped-subarc endpoints belong
to the separate pocket cycles, not to the main circle.
The stronger primal interpretation in
[B, section6](../B/PROOF.md) identifies a successful chain with
the complete dual facial cycle of its named rim vertex. This
further gives `d_J(root)=2s+4` and identifies each skipped cycle
with the cut around one actual child subtree; its parity is the
sum of the original J degrees in that entire subtree modulo two.
Neither condition may be replaced by the root's degree alone.

All finite controls have `source_realizability=not triggered`.
Their graph matchings do not supply the original C5 source,
complete U319 fibres, reconstruction or original r lifts.

## 9. Scope

Proved here: the literal f/z sector normalization; the monotone safe
interval construction; its exact list of all complete new cycles;
formula(A1); the arbitrary-size sufficient repair and the two
necessary blocker alternatives; and the exact thirteen-state
same-O criterion with explicit marked Boolean realization.

Unproved: that either safe chain has no blocker in every original
minimum source; that another thirteen-state witness must exist
when both chains fail; source realization or exclusion of the
two-cycle class; joint positivity `W110+W101>0`; `omega_e=0`;
complete319; the general main theorem. The original completed-source
reconstruction cost remains `k+5`. No new Lean theorem or finite
source certificate is claimed.
