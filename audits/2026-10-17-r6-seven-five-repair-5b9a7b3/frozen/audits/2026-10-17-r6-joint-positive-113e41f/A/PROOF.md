# A: every nonfacial seven-defect exposes an actual crossed five-cut

BASE `113e41f7023aa00c8257b815ce8727035b648f26`, 2026-10-17.
This is an arbitrary-size paper lemma about the same source, followed by
finite geometric calibration. It does **not** prove joint positivity.

## 1. Fixed source and exact scope

Keep the original minimum no4ct completed C5 source G, its ordered contacts,
rotation, attachments and private vertices. Keep the whole U319 relation in
`(z,s,v,w,t,p,q)`, including all empty fibres and all legal original r lifts.
The graphs are the actual `J=U/(s=t)` and sphere dual `D=J*`; `m=[s=t]`.
The literal marks are `e=(vw)*`, `f=(pq)*`, `g=(mz)*`, with the same faces
`mvw,zpq`, actual hub edge mz and original link sectors. No projection below
replaces the complete U relation or independently chooses witnesses.

Use these frozen source facts: J is a simple sphere triangulation, every
triangle is facial; `d_J(m)>=7`, `d_J(z)>=6`; every vertex outside
`{m,z,v,w,p,q}` has degree at least five, and v,w,p,q have degree at least
four. The original nonedges include `zv,zw,pv,pw,qv,qw`.
The four link sectors and their endpoint conventions are exactly those in
frozen `continuation-f1faf74/C/PROOF.md` section 1. Its Theorem C1 classifies
every induced C5: every case without a star side crosses its original single
hub sectors or uses crossed incidences at both hubs. The additional original
geometry inputs are sealed in `../ADDITIONAL_GEOMETRY_INPUTS.json`.

For every ordinary PM M, set `F=D-M`. This is a collection of complete
cycles, whether or not its colouring fibre is empty. The target is a PM
in the **union** of 110 and 101 with no odd F component. No separate
positivity of the two directions is required. All results below apply to
arbitrary M, and hence to every positive-oddness joint minimizer.

## 2. A general seven-cycle lemma

**Lemma A1.** Let D be a simple cubic plane graph with no triangle, at least
three-edge-connected, and with every three-edge cut trivial. If C is a
seven-cycle that is a component of `D-M` for some PM M, precisely one of the
following holds:

1. C is facial, with no chord;
2. C is nonfacial, has exactly one chord, that chord belongs to M, and on
   one side C bounds exactly the union of an adjacent four-face and five-face.
   The five other edges incident with C are five distinct M spokes. They
   form an actual cyclic five-cut between `V(C)` and its complement.

Here a trivial three-cut isolates one vertex. “Facial” refers to the fixed
sphere embedding, rather than to an abstract drawing selected for C.

**Proof.** A four- or five-cycle has no chord, since a chord would give a
triangle. If both sides contained vertices, their outgoing edge counts
would each be at least three. There are at most five outgoing edges in
total. Thus every such cycle is facial.

Suppose first that C has no chord and is nonfacial. Each of its seven
vertices has exactly one edge leaving C, and that edge is in M. Both open
sides contain vertices. The edges from either open side to C form an actual
cut: there is no edge crossing C, and there is no other contact between the
sides. Both counts are at least three. Since the counts sum to seven, one
side has exactly three such edges. Its three-cut must be trivial. That side
cannot be the complement of a singleton, since its complement contains the
seven distinct vertices of C. Hence the open side itself consists of a
single vertex. Its three incident edges would all belong to M, contradicting
that M is a matching. The chordless nonfacial case is impossible.

Every chord belongs to M, because the two C edges already occupy the two
complement incidences at each endpoint. A chord splits C into cycles whose
lengths sum to nine. Triangle exclusion leaves only lengths four and five.
Both are facial by the preceding paragraph. For each small cycle, the
other arc of C contains vertices outside that cycle, so its empty facial
side must be the region between the chord and its own C arc. Consequently
the entire chord side of C consists of those two faces. There is no second
chord on that side. A chord on the other side would give the same two-face
argument there, leaving D with exactly seven vertices. A cubic graph has an
even number of vertices, so this too is impossible. Thus there is exactly
one chord. A facial C with any chord is also impossible: the two-face
chord side and the empty facial side would again leave exactly seven
vertices.

There are consequently five remaining incidences from C to its complement,
all in M, and they have distinct outer endpoints because M is a matching.
The complement of V(C) is nonempty (again D cannot have seven vertices).
Every vertex there lies on a whole F cycle different from C. It therefore
contains a cycle, while D[V(C)] contains C. The literal five-edge boundary
is thus cyclic. QED.

The source D satisfies the hypotheses: a simple sphere triangulation has
three-edge-connected cubic dual; a three-cut is a bond and is dual to a
primal triangle. Every primal triangle is facial, so every three-cut is
trivial. A dual triangle would bound a degree-three primal vertex: a
chordless three-cycle cannot have vertices on both sides by three-edge
connectivity. The source has primal minimum degree at least four, so D
has no triangle. These statements use no planar colourability theorem.

## 3. Translation into the actual source and its sectors

**Theorem A2.** Every seven-cycle component C of `D-M` is either the entire
face of a degree-seven primal vertex, or the boundary of the two adjacent
primal vertex stars of degrees four and five. In the second case:

* its unique internal M chord is the actual primal edge between those two
  vertices, and the degree-four vertex is one of v,w,p,q;
* the five M spokes form an induced primal C5 Q;
* Q has no single-vertex star side. Therefore Q necessarily crosses the
  original sectors in exactly the sense of frozen Theorem C1.

**Proof.** Dual four- and five-faces correspond to primal vertices of those
exact degrees. Their shared edge is the chord in A1. Every degree-four
vertex is one of the four stated terminals by the source bounds.

The five-cut is a bond: if either side had two components, each would
require at least three boundary edges. Its primal image is therefore a
simple C5 Q. This Q is induced. Indeed a chord of a C5 produces a triangle,
which is facial in J. The two Q edges of that triangle correspond to two
of the five M spokes, incident with the same dual triangle vertex. That
contradicts matching. This argument does not assume that an ordinary PM
has any full Tait colouring.

On its two-face side Q contains exactly the two adjacent primal vertices
of degrees four and five, so this side is not a single-vertex star. The
other side cannot be such a star either: otherwise J would have exactly
`5+2+1=8` vertices. But z has at least six neighbours and the two distinct
nonneighbours v,w; hence `|V(J)|>=9`. Apply the frozen induced-C5 theorem
C1 to this same Q: every noncrossed case has a star side, so the remaining
case has the stated original-sector crossing. QED.

The inducedness argument is stronger than saying the five spokes happen
to avoid short marked cuts: it uses the actual PM incidences. The crossed
Q is a necessary feature of this same complete matching, not a separately
feasible separator imported from another witness.

## 4. Exact marked defect alternatives in the joint family

**Corollary A3.** In a joint matching the following alternatives hold.

* In direction 110 the active omitted mark is g. Any seven-defect containing
  g must be a facial seven-cycle centred at m or z, with that hub of degree
  exactly seven. It cannot be a nonfacial seven-defect. There is no five-
  defect containing g, since its only incident primal centres m,z have
  degrees at least seven and six.
* In direction 101 the active omitted mark is f. A seven-defect containing
  f is either the face of a degree-seven terminal p or q, or the boundary
  of the star of a degree-four terminal p or q together with an adjacent
  degree-five vertex h outside `{m,z,v,w,p,q}`. Thus that terminal has
  original degree five, and h has unchanged original degree five.
  The separating Q5 in this second alternative crosses the original sectors.
* A five-defect containing f is a facial pentagon centred at a degree-five
  J terminal p or q, hence at an original degree-six terminal. This is
  distinct from the new two-vertex seven-defect case.

**Proof.** Every five-cycle in D is facial by A1's first paragraph. A marked
primal edge can lie on a dual face only when that face is centred at one
of its actual endpoints. A nonfacial seven-defect has the two primal
centres from A2. If its boundary contains g, one of those centres would
be m or z, which violates their degree bounds. If its boundary contains
f, exactly one centre is p or q. The degree-four centre cannot instead
be the other p/q (then f would be their shared chord), or v/w (all four
cross edges are absent). It must be the incident terminal itself. The
other degree-five centre is neither a hub nor another terminal: hubs
are too large, the other p/q would make f the chord, and v/w are forbidden
neighbours. The original degree formulas at the terminals give the stated
original degrees. QED.

The frozen original degree identity is
`d_J(m)=d_G(s)+d_G(t)-5`, with both original degrees at least six.
Thus the m-centred seven-defect requires exactly `d_G(s)=d_G(t)=6`.

Thus, if a 110 matching has a g-containing odd component and both hubs
have degree other than seven, that component has length at least nine.
If a 101 matching has an f-containing odd component, it is either one of
the explicit five-/seven-defect alternatives or has length at least nine.
The active mark need not lie on an odd component at all: none of these
statements asserts that it does. Remote odd components are also retained.

## 5. Calibration, authority and remaining obligation

`check.py` reconstructs the cubic dual directly from the frozen complete
flipped-icosahedral sphere input and from a new seven-bipyramid control.
It independently checks the sphere links, all primal triangles, absence
of dual triangles, every edge deletion of size at most three, and every
PM with every complete complement cycle. It verifies A1/A2's geometric
statements on every odd cycle of length at most seven, retaining actual
faces, chords, five-cut spokes, two centres and the induced Q5. The first
control positively exercises nonfacial seven-defects; the second positively
exercises facial seven-defects. Neither satisfies the original source
contract, and neither supplies source-realizability or source enumeration.
No finite zero is used to prove the arbitrary-size paper lemma.

The active certificate is `certificate-v3.json`; `certificate.json` and
`certificate-v2.json` are initial development seals, retained without overwrite.
The v2 seed17 replay exposed a tuple-versus-JSON-list comparison error; the
final checker canonicalizes its entire reconstruction to JSON types before
comparison. No geometric record was deleted or weakened. The certificate includes every PM and every complement cycle, not only
successful cases. This checker is geometric: it does not replace any
source colouring relation or declare a nonempty colouring fibre for an odd
complement. Normal and seed17 replay, corrupted-shape rejection and exclusive
create rejection are recorded in `VERIFICATION.json`.

A1--A3 give a new arbitrary-size necessary localization of seven-defects,
including their actual crossed five-cut. They do not exclude the crossed
case, a facial seven-defect at a hub/terminal, or longer odd components.
There is still no proof of a zero-oddness joint PM, no strict oddness
decrease and no smaller completed bad source. All operations use the same
J,D and have zero reconstruction cost; restoring from U still costs five
vertices and gives completed size k+5. `W110+W101>0`, complete319 exclusion,
the general theorem and any new Lean theorem remain **OPEN**. Source input:
**not triggered**. No 4CT, external theorem, old-evidence mutation, shared
routing edit, commit or push is used.
