# B: the exact pentagon repair interface and its protected outside arc

Frozen BASE `f1faf743833c51ddc5efbe9e0f390b87b9f2311d`.
This is an arbitrary-size same-graph lemma, followed by finite calibration.
It does **not** complete Sigma319 exclusion or prove `W110+W101>0`.

## 1. Source and the shortest ordinary switch

Keep the original globally minimum no4ct source G, its ordered contacts,
rotation, every complete fibre including empty ones, and every original r
lift. The graph remains the literal `J=U/(s=t)` and its actual dual D, with
`e=(vw)*`, `f=(pq)*`, `g=(mz)*`. The frozen complete proof supplies an even
111 matching M0 from one actual complete J colouring and an ordinary101
matching. These are distinct witnesses.

Fix this M0. Its symmetric difference with an ordinary101 matching has a
unique f-containing component Q, which avoids e,g. Flipping just Q gives
an ordinary101 matching `N=M0 xor Q`. Consequently the family of actual
M0-alternating cycles containing f and avoiding e,g is nonempty. Choose a
member Q of minimum edge count. This choice does not minimize oddness.

The frozen joint-zero B proof identifies a remote W5 defect as follows.
An induced original monochromatic rim C5 avoiding m,z has a retained
original degree-five centre u away from both closed hub stars. The five
faces around u are the entire odd pentagon P of `D-N`; every edge of its
five-edge cut lies in N. Its internal dual spoke edges avoid all of e,f,g.
This proof analyzes that same literal pentagon. No cap or graph is replaced.
The rim/cut can contain e; because e lies in both M0,N it never belongs to Q.

## 2. All 32 pentagon port fibres

Let `x0,...,x4` be the cyclic vertices of a facial pentagon in any cubic
plane graph, and let `hi` be the unique edge leaving it at xi. A matching's
selected ports are those hi which it contains. Once all five port statuses
are fixed, the entire internal matching fibre is:

| Selected ports | Nonempty fibres | Internal matching | Complement inside the pentagon |
| --- | ---: | --- | --- |
| all five | 1 | empty | one closed odd pentagon |
| three, with the two unselected vertices adjacent | 5 | their connecting edge | one path of length four |
| one | 5 | the unique matching of the other four-vertex path | two paths, of lengths two and one |
| every other footprint | 21 empty | none | no matching filling |

**Proof.** Internal matching edges cover precisely the vertices whose ports
are unselected. Their number is even. With three selected ports the two
remaining vertices must be adjacent. With one selected port deletion of
that vertex leaves the path on four vertices, whose perfect matching is
unique. Five selected ports leave none. This also proves the empty rows,
not merely the existence of the eleven displayed fillings. Removing the
internal matching edges from the pentagon gives the stated whole strands.
QED.

For any complete Tait colouring of the whole graph, each colour appears an
odd number of times among the five ports: count that colour's incidences
on the five vertices, with each internal edge counted twice. Hence their
colour multiplicities are exactly `3,1,1`. There are exactly thirty complete
local Tait colourings with the three colours labelled. The checker records
all of them and all thirty-two port fibres, including the twenty-one empty
ones. A local open-port row is not represented as a complete source.

## 3. Two exhaustive forms of a new remote pentagon

Suppose the shortest Q above produces a remote odd pentagon P. Since N
selects all five ports, M0 selects exactly one or three of them.
Indeed the port count must be odd by Section 2; selecting all five would
already leave an odd pentagon in the even complement of M0.

If M0 selects three ports, Q crosses exactly the other two ports and uses
the sole internal M0 edge between their adjacent pentagon vertices. This
internal edge is the pentagon's unique transition in the frozen transition
formula. The three-port case supplies no local f-preserving shortcut.

If M0 selects one port, rename its vertex x0. The internal M0 matching is
then exactly `x1x2,x3x4`. Q contains those two internal edges and crosses
all four other ports. It avoids x0 because its M0 edge h0 is common to
M0 and N. The new pentagon again contains exactly one transition: its
at most two internal M0 edges have an odd transition count by the frozen
whole-component parity identity.

This is an exhaustive classification of each such actual defect. In
particular it is incorrect to assume that M0 always meets the defect's
cut in three ports, or that every pentagon defect admits an internal
matching change with its external footprint fixed. The five-port fibre
contains exactly one filling, which leaves the odd pentagon in place.

## 4. A new protected-arc theorem for the one-port case

**Theorem.** In the one-port case of Section 3, Q has two exterior arcs,
`P14` joining x1 to x4 and `P23` joining x2 to x3. The latter arc contains
f. Replacing P23 by the literal pentagon edge x2x3 gives a strictly shorter
M0-alternating cycle Q', avoiding e,g, which loses f.

**Proof.** Delete `x1x2,x3x4` from the single simple cycle Q. The two
remaining paths are exterior to the facial pentagon except for their
endpoints. Pairing (x1,x2),(x3,x4) would give two Q components. Pairing
(x1,x3),(x2,x4) would cross in the complementary disk of the pentagonal
face, contrary to planarity. The pairing is therefore exactly (x1,x4),
(x2,x3).

The first and last edges of P23 are the non-M0 ports h2,h3. Every interior
step of P23 alternates. The missing pentagon edge x2x3 is also outside
M0, while the Q edges at x2 and x3 retained on the other side are the M0
edges x1x2,x3x4. Consequently

`Q'=(Q minus E(P23)) union {x2x3}`

is one simple M0-alternating cycle. It uses existing vertices and edges
only. The path P23 uses its two different ports and at least one intervening
M0 edge, so has length at least three. Thus Q' is strictly shorter.
The new edge is one original dual spoke of the remote W5 centre, hence
is none of e,f,g. All other Q' edges already lie in Q, so Q' avoids e,g.
If P23 avoided f, Q' would still contain f and contradict the chosen
minimum length of Q. Therefore P23 contains f. QED.

The result locates the exact obstruction to this actual local shortcut.
It does not prove an oddness decrease: the only short replacement has
removed the required root mark. Nor does it exclude two such defects.
For disjoint defects on one Jordan side of Q, their literal shortcut
chords do not cross. After cutting Q at f, the *f-avoiding complementary*
intervals are therefore nested or disjoint. Their f-containing discarded
arcs need not form a chain; they can overlap and cover Q. This topological
observation imposes no bound on the number of defects.

## 5. A shortest-cycle negative calibration

The frozen flipped-icosahedral control, with its original thirty-edge
indexing, has the pairwise primal-disjoint marks `(e,f,g)=(2,20,5)` and
an even starting matching

`M0={2,5,9,10,15,19,20,26,28,29}`.

A shortest M0-alternating cycle containing f and avoiding e,g is

`Q={0,7,9,10,14,15,16,18,19,20,22,24,28,29}`.

Its length is fourteen. The checker lists **every** eligible single Q
and independently confirms the minimum. Its endpoint matching is

`N={0,2,5,7,14,16,18,22,24,26}`,

whose complete complement consists of cycles of lengths fifteen and five.
The complete fixed-alpha colouring fibre is empty. The pentagon is the
face of original primal vertex 9; its one-port shortcut removes exterior
arc `{16,20,22}` and inserts actual edge 21. The shortened Q' has length
twelve and loses f=20, exactly as Section 4 requires.

There is also an even endpoint at length fourteen in this control. Thus
the negative result is precise: **an arbitrarily chosen shortest eligible
single Q need not have even complement**. It does not say every shortest
Q fails or that the marked family's global minimum oddness is positive.
This new marking is not asserted to have FJ or the original source's
local faces, fan sectors, degrees, induced boundary, or complete Sigma319
support. It is a calibration of the exact local obstruction, not a source
counterexample or a further failure of the source theorem.

## 6. Replay and authority

[verify.py](verify.py) independently reconstructs each dual from all faces
of the four frozen controls in [input_controls.json](input_controls.json).
It enumerates every full labelled J colouring and every actual PM, storing
all complete fixed-alpha fibres including empty ones. The equality checked
at each PM is `fibre_size=4*2^cycles` for an even complement, and zero
otherwise. This keeps every primal root colour and complete choice of
beta/gamma alternation. It makes no claim that the controls are complete
original r sources, and supplies no actual minimum source: **not triggered**.

For every even M0 and every endpoint whose symmetric difference is a single
cycle, it checks every literal newly odd facial pentagon. It finds 186
one-port cases and 193 three-port cases across the controls, checks every
one-port exterior pairing and the actual shorter matching, and records
each whole trace. It also replays the fixed shortest-Q negative calibration.
Normal and seed17 runs compare the whole canonical certificate, rather
than selected marginals. Corrupted empty-fibre, shortcut-edge, and
protected-arc records are separately rejected; see [VERIFICATION.json](VERIFICATION.json).

The new arbitrary-size result is the exact local port interface plus the
protected-arc theorem for a source-supplied shortest ordinary switch.
It narrows why a remote W5 defect can resist a local change. Neither the
three-port case nor the f-containing discarded arc is excluded, and no
long odd component is repaired. The known full111 and newly supplied
all-distinct source sectors are distinct complete witnesses; this proof
does not combine their private colours.

All changes and shortcuts remain on the same original J,D and have zero
reconstruction cost, but supply no smaller completed source. Restoring
W/J to the original G still costs k+5. The joint positive weight,
Sigma319 exclusion, the general main claim, and new Lean authority remain
OPEN. No shared documentation, prior audit, commit, or push is changed.
