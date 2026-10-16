# Final same-colouring attempt from A's new all-distinct source sector

BASE f1faf743833c51ddc5efbe9e0f390b87b9f2311d.
Only this new file is written; the existing B proof/checker/certificate remain
unchanged. This attempt proves the two literal forced primal linkages below,
but obtains no W110/W101 endpoint or full319 exclusion.

Fix one actual complete colouring supplied by A with

`z=v=A, m=s=t=C, w=B, {p,q}={B,C}`.

Let `u_B` be the actual one of p,q coloured B and `u_C` the other one,
coloured C. This notation preserves their original individual attachments;
it does not exchange p,q. Give A,B,C,D the Klein values0,1,2,3. The marked
edge differences are `e=1, f=3, g=2`. Full FJ requires e,f on the same
actual {1,3} dual cycle and e,g on the same actual {1,2} dual cycle.

## Exact linkages in this one full colouring

For a fixed dual two-colour family, its disjoint cycles bound the components
of the primal graph consisting of the third-difference edges. Those
components are the two complementary primal Kempe palettes. The adjacency
graph of the resulting Jordan regions is a tree: each new disjoint Jordan
cycle adds one region. Consequently two edges on the same dual cycle have
their respective primal endpoints in the same two palette components.
This is the frozen joint-zero B3 region argument applied to the third
Tait-colour matching, with every whole complementary cycle retained.

Apply it to e,g on the {1,2} cycle. The third difference3 joins A-D and
B-C. The A endpoints are v,z, so the actual same colouring has an AD
z-v path. The other endpoints w,m are already joined by the original BC
edge wm, inherited from the original U edge wt.

Apply it to e,f on the {1,3} cycle. The third difference2 joins A-C and
B-D. Thus this same colouring has a BD path from w to u_B. The other
required AC connection is already the actual path

`v-s-z-u_C`

in split U, corresponding to v-m-z-u_C in J. Its four vertices and every
edge are literal; colours along it are A,C,A,C.

Both nontrivial paths survive *unchanged* in U. The identified vertex m
has colour C, and its split copies s,t also have colour C, so none occurs
in either the AD or the BD subgraph. The split does not invent a path or
require independently chosen colourings. The source nonedges zv,zw and
pv,pw,qv,qw prevent short terminal edges, but do not prevent these longer
paths through actual private vertices.

## Why the proposed Jordan contradiction does not follow

AD and BD are not complementary palettes: **they share D**. The two actual
paths can meet at a D vertex, including with their incident rays alternating
in its original rotation. Thus their endpoints cannot be treated as two
vertex-disjoint paths, and a Jordan noncrossing assertion is unavailable.
There is a concrete locally allowed crossing shape: a retained degree-five
W5 centre of colour D with cyclic rim colours

`A,B,A,B,C`.

The two AD rays and the two BD rays alternate around this centre. All wheel
faces are properly coloured. Its induced C5 rim is precisely the permitted
remote W5 cap, rather than a forbidden small separator. This is a local
calibration of the missing exclusion, not a claim that this wheel extends
to a whole FJ source. Larger-degree D intersections also remain possible.
No current source lemma eliminates these intersections or supplies a
complete-colouring Kempe change that resolves them while retaining a
forbidden marked sector.

There is one valid disjoint-palette conclusion: the AD z-v path separates
the original outer s and w, so s,w cannot be BC-connected in U; the actual
edge wt keeps w,t together. This is exactly A's full-component bijection
argument. The new BD w-u_B path does not make u_B BC-connected to w,
because it may pass through D. Replacing BD by BC would create the desired
contradiction but changes the actual component and is unjustified. Likewise
the BC component containing w,m in J can split into different s/t components
in U; the original split rotation must not be silently identified again.

A also guarantees another full colouring in the reflected z=w sector.
It is a separately quantified witness. Its paths cannot be overlaid with
this colouring's paths, and no proved map identifies their private colours.
The new positive counts W010,W001 belong to allowed all-distinct sectors;
changing the distinguished Tait colour does not convert them into W110 or
W101.

## Exact residual obligation

A closing topological proof would have to control the actual intersections
of these AD and BD paths (including the legal W5 crossing above), or prove
a complete-colouring switch which changes one forced dual cycle coincidence
on the same original graph. Merely asserting disjointness, exchanging the
palette BD for BC, gluing the two guaranteed sectors, or forgetting the
original s/t split would lose the source contract.

No such repair or exclusion was obtained in this attempt. The sufficient
contradiction `W110+W101>0`, full319 exclusion, and strict completed-source
descent remain OPEN. All operations analyzed stay on the same graph; the
full original-source reconstruction still costs k+5. No broad enumeration,
external theorem, new Lean claim, commit, push, or sealed-file change occurs.
