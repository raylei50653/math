# K13 finite generation completeness

Fixed repository BASE: `50d5474f2446403f3b3001d5943571184c8c9936`.
This note proves coverage of the finite source domain; it does not itself
certify a colour relation. The main and independent colour checkers supply
that distinct obligation. All identifiers below are zero based.

## 1. Cone the original ordered outer face

Let G be any source satisfying the normal form used in the audit proof:
the outer face is the specified chordless cycle B of length five, every
other face is a triangle, G is finite and simple, its five B vertices have
degree at least four, and its thirteen other vertices have degree at least
five. Draw a new vertex z in the original outer face and join z to all five
B vertices inside that face. No original edge is changed. The resulting
embedded sphere S is simple, all its faces are triangles, it has nineteen
vertices and fifty-one edges, and its minimum degree is five. In particular,
z has degree five. A simple sphere triangulation on at least four vertices
is 3-connected: a cut vertex or a separating pair would force a repeated
vertex or a missing edge on a facial triangle. This fact imposes no extra
connectivity assumption on G.

Conversely deleting any degree-five vertex from such an S leaves an embedded
disk with its five distinct neighbors as the specified outer facial cycle.
The five neighbors have degree at least four after deletion; all other
vertices retain degree at least five. The converse disk might, in general,
have a chord of that outer face, but the universal source stream keeps it
anyway. Thus no source can be lost by a chord or collar test.

Enumerate every embedded isomorphism class of simple sphere triangulations
of order nineteen and minimum degree five, then every degree-five vertex
in every representative. For an isomorphism from the cone of an original
source to a representative, the original z maps to one of those retained
vertices. The image of the original ordered B is one of the ten cyclic
frames of that vertex's neighbor cycle. Consequently these roots and frames
cover every original source with its complete ordered B, original edges,
rotation, and faces. An isomorphism reverses either all rotations or none;
the frame operation is a whole-graph D5 transport, never an independent
rotation of pieces. Full colouring extension is unchanged under this
bijection, including an empty fibre.

## 2. External complete sphere generation and implementation boundary

The frozen vendor source and guide in
`artifacts/c5_excess_two_independent_search/vendor/` specify plantri
**5.8, March 4, 2026**. The replay checks their bytes against BASE.
No external binary is trusted: both executables are compiled locally from
that source. `-m5 19` requests all simple 3-connected plane triangulations
with minimum degree five, with reflectional isomorphism allowed. It does
not request 4- or 5-connectivity and does not exclude separating cycles.
No plug-in, pre-filter, edge filter, degree maximum, or split is used on this
primary route.

The mathematical coverage authority is Brinkmann--McKay,
[Construction of planar triangulations with minimum degree 5](https://users.cecs.anu.edu.au/~bdm/plantri/min5paper_sc.pdf),
Theorems 1 and 3 (pp. 2--4) and the corrected Theorem 2 proof (p. 8).
The icosahedral expansions first cover 5-connected triangulations.
Theorem 3 supplies smaller parents, measured by order and separating
cycles, for the remaining connectivity classes. Reversing these reductions
covers all simple minimum-five sphere triangulations. The implementation
section (p. 8) uses canonical construction paths to retain one member per
embedded isomorphism class. We rely on this published construction theorem,
including its displayed local operations; we do not re-prove those external
reductions here. This is not an appeal to a numerical count table.

The corresponding frozen C functions are `initialize_min5`, `scanmin5`,
`scanmin5c`, `scanmin5c4_0`, `scanmin5c4_1`, `scanmin5c3_0`,
`scanmin5c3_1`, and `min5_dispatch`. Their correctness is computational
trusted code, not a Lean theorem. The independent checks below exercise
different construction paths and independently parse/solve outputs; none
is described as a formal verification of all C instructions or the compiler.
The external PDF bytes and hashes are retained in this directory.

## 3. Second complete construction: cone the inner boundary

Assume the original collar theorem supplies a simple C of length 5+h.
Its five original apices have H-degree at least three, its h other collar
vertices have H-degree at least four, and every strictly interior vertex
has degree at least five. H has thirteen vertices. Cone its actual outer
face C to a new q. The resulting simple sphere T has fourteen vertices,
minimum degree at least four, and q has degree 5+h. This works with every
possible C chord: the cone lies outside C and never intersects an edge of H.

Therefore enumerate every sphere14 minimum-four triangulation and every q
of degree nine, ten, eleven, or twelve. Deleting q gives H with its specified
outer face C; q's neighbor order gives that face. Let I be the other vertices.
Only the following two necessary degree tests are used:

1. If some vertex of I has degree below five, discard the root.
2. A vertex of C with degree four in T has degree three in H and must be
   one of the original five apices. If there are more than five, discard.

No other pruning is used. For every surviving root, choose every five-element
subset of C containing all forced apices. All other C vertices are y's.
Every choice meets precisely the required degree inequalities, so there is
no omitted alternative type of apex assignment. All inner edges, including
all C chords and all C--I attachments, remain exactly those of T-q.

The minimum-four generator is distinct from the primary minimum-five
construction. Its mathematical authority is Brinkmann--McKay,
[Fast generation of planar graphs](https://users.cecs.anu.edu.au/~bdm/papers/plantri-full.pdf),
Section 2, Figure 6 (pp. 9--10), using the octahedron and three expansions.
Section 1.2 explains canonical rejection. Frozen functions `initialize_min4`,
`scanmin4`, `find_extensions_min4`, and `min4_dispatch` implement this
family. `-m4 14` uses no custom filter.

This alternative construction is run through a separate collar-gluing
algorithm, rather than by feeding the primary list to another checker.
It covers precisely the h=4--7 degree-compatible inner domains before any
colour exclusion and independently recovers the entire relevant rooted
embedded graph set from the primary route.

## 4. Every named excess vector and the forced annulus

For a named vector e=(e0,...,e4), ei>=0 and sum(e)=h, introduce distinct
named vertices a0,...,a4 and y(i,1),...,y(i,ei). The cycle C follows the
paths

`a(i-1), y(i,1), ..., y(i,ei), ai`

in cyclic i order. Attach bi to every vertex of this path and retain each
original boundary edge bi b(i+1). The annular triangular faces are exactly
the original-edge face bi b(i+1) ai and the fan triangles at bi along
successive vertices of its path. Thus an apex ai has precisely its two
original attachments bi,b(i+1), and each y(i,j) has precisely bi. This gives
the actual original rotation at every B vertex and the exterior sector of
every C vertex. The remainder of the rotation belongs to H and is kept by
its embedding.

Under the existing simple-collar theorem there is no additional geometric
freedom in the annulus: its consecutive neighbor lists, boundary-edge
apices, and triangular faces force exactly these fans. The names and order
of y(i,j) fix all attachments. All remaining choices are in the embedded
H already enumerated. Choosing an apex subset on C, then a cyclic starting
apex and orientation, recovers every named e vector and every annular
placement. `inner_cover.py` retains one base labeling for each subset and
all ten B frames. Under reflection the whole embedding is reversed.

`named_configurations.json` enumerates every weak composition of h into
five parts. Each record includes its D5 representative, the actual
representative-to-original B permutation, and every inner-core/frame pair
realizing that named vector; empty lists are retained. Its B permutation
extends as the identity on the original H vertex IDs and transports the
entire glued graph. Original apices in a reversed frame are determined by
the transported original B edges, not by independently reversing an apex
list. `inner_cores.json` contains each H's exact edges, directed faces,
rotation, C, I, chosen apices, C chords, completed sphere rotation, and the
complete map to its primary sphere/root and ordered B frame.

## 5. Exact finite coverage results

The primary route yields **23** sphere classes and retains **306** roots.
Every root in this run has a simple collar. The h distribution is
0:5, 1:24, 2:98, 3:134, 4:41, 5:4, 6:0, 7:0. All roots, including h<4,
are passed to universal complete-relation checking before any use of the
933/941 screen. No source is discarded solely for having the wrong mask.

The independent inner route starts with all **2,472** min4 sphere14 classes:

| h | named vectors | D5 vector orbits | all rooted H | degree-eligible H | apex cores | nonempty named vectors |
|---|---:|---:|---:|---:|---:|---:|
| 4 | 70 | 10 | 629 | 19 | 27 | 55 |
| 5 | 126 | 16 | 214 | 1 | 1 | 10 |
| 6 | 210 | 26 | 41 | 0 | 0 | 0 |
| 7 | 330 | 38 | 2 | 0 | 0 | 0 |

`inner_filters.json` retains all **886** q roots, complete original sphere
rotations/degrees, every rejected interior vertex, every forced apex, and
the rejection reason. `inner_cores.json` retains all **28** cores. These
are enumeration records with possible isomorphic repetitions, not a claim
that all twenty-eight are nonisomorphic.

The forty-five primary roots with h=4 or5 and the twenty-eight alternate
cores give exactly the same **26 rooted embedded isomorphism classes**.
`primary_to_inner.json` supplies each primary root's alternate-core matches.
Isomorphism equality is checked by a complete rotation encoding over every
initial dart and both whole orientations, with z fixed for rooted equality.
It is an exact encoding from which every rotation can be recovered, not an
incomplete graph fingerprint. Every alternate core additionally has an
explicit vertex isomorphism to a primary sphere and root.

Chords are material: among the forty-one h4 primary roots, thirty-nine
have no C chord and two have one; all four h5 primary roots have two.
Any blanket chordless assumption would omit the complete h5 domain.

## 6. Additional independent coverage checks and replay

As a second full-order construction test, run all **11,284,042** min4
sphere19 classes and apply `min5_filter.c` only when an output would be
written. The filter accepts exactly **23**. It has no pre-filter hook and
cannot prune any recursion subtree. Their complete embedded-isomorphism
set equals the primary set; `min4_to_min5.json` records correspondence.
This is a different generation recursion but shares plantri's storage and
canonical machinery, so it is not represented as a separate implementation.
The independent checker also exhaustively generates smaller abstract graph
domains without plantri; see that checker's report for its actual execution.

Replay from this fixed worktree:

```
python audits/2026-10-13-k13-collar-50d5474/generation/replay.py --output /tmp/k13-generation-normal --seed 0
python audits/2026-10-13-k13-collar-50d5474/generation/replay.py --output /tmp/k13-generation-seed17 --seed 17
```

Each target must be fresh; replay refuses to overwrite existing mathematical
products. Replays record commands, return codes, stdout, stderr, compiler and
Python versions, BASE input hashes, and all twelve mathematical product
hashes. The generator itself is deterministic; PYTHONHASHSEED=17 tests that
the postprocessors do not depend on unordered iteration. Retained initial
compile failure is a quoting error on the plug-in macro, not a source
generation run; the successful invocation passes the unquoted pathname to
plantri's own stringification macro.

This completeness proof uses neither the Dvorak--Lidicky fewer-than-thirty
bound nor any extension to thirty dual vertices. No original source edge
is removed for a colouring test. No C8-only apex-degree or no-chord fact is
used for C9--C12. There is no new Lean theorem in this generation work.
