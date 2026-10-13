# Two private vertices are sometimes necessary and sufficient

2026-10-13. This subpackage uses the parent's frozen BASE
`19209f4cf68261fdce5e84a7804cfe04ae0957bf`.
It gives a synthetic annulus relation with an exact minimum of **two** private
vertices. It does not give a globally minimum catalogue-outside source.

The result rules out a general replacement theorem with `r <= 1`, including
arbitrary new private vertices and arbitrary changes throughout the annulus.
It does not rule out `2 <= r <= 6`. This is different from the previous
zero-new-vertex, U-only local positive-union obstruction.

## 1. Fixed slots and relation

The ten distinct original pins are
`B = (b0,b1,b2,b3,b4)` and `U = (u0,u1,u2,u3,u4)`, each inducing its stated
C5. The two cycles keep their order and form the outer face and inner empty
face. On the common named palette `C={0,1,2,3}`, let

\[
 R_=^{(3)}=\{(\beta,\tau):\beta\text{ proper on }B,
       \tau\text{ proper on }U,\ |\tau(U)|=3,
       \ \beta(b_0)=\tau(u_0)\}.
\]

No other relation between boundary colours is imposed. This is a named
support relation; U is never normalized independently of B.

## 2. A legal annulus with r=2

Introduce two private vertices `x,y`. In addition to the two original C5
cycles, add exactly

```
b1-x, x-y, y-b1,
b0-x, b0-y,
u0-b1, u0-x, u0-y.
```

Thus `b1,x,y` form a triangle and `b0,u0` are both adjacent to all its
vertices (the edge `b0-b1` was already on B). The induced subgraph is
`K5` minus the edge `b0-u0`.

A literal consistently oriented sphere map is below; the first and last
faces are distinguished as the outer face and the empty U face.
Repeated `u0` in an annular facial walk is intentional and is not a second
pin. No embedding or attachment is silently inferred from abstract planarity.

```
(b0,b4,b3,b2,b1)                     outer
(b0,y,b1,b2,b3,b4)
(b0,b1,x)
(b0,x,y)
(u0,x,b1,u0,u4,u3,u2,u1)
(u0,y,x)
(u0,b1,y)
(u0,u1,u2,u3,u4)                     empty inner face
```

Every directed edge occurs once. Every vertex link is a single cycle and
`V-E+F=12-18+8=2`. The graph is connected. These data certify the plane
annulus slot; the certificate records its derived literal rotation and
all edge/vertex ownership.

In every four-colouring, the triangle `b1,x,y` uses three different colours.
Both `b0` and `u0` must receive its missing colour, hence they are equal.
Conversely, for any proper `(beta,tau)` with `b0=u0`, `b1` differs from that
common colour, and the two other colours can be put on `x,y` in either order.
Both choices extend all original edges. Therefore the full, unrestricted
B/U support is exactly equality of `b0,u0`; in particular its three-colour-U
support is `R_=^(3)`. Every supported cell has exactly two full lifts.

The proof gives full lifts in both directions: restrict to the ten pins,
or choose either ordering of the two remaining colours for `x,y`. After
adding a new centre `v` inside the *same* empty U face, every supported
three-colour-U lift has exactly one extension, at the unique missing colour.
The resulting wheel graph has `5+2+1=8` internal vertices.

## 3. Exact lower bound: r<=1 cannot represent this support

**Theorem.** A loopless ordinary graph with these ten distinct fixed pins and
at most one further vertex cannot have three-colour-U named support
`R_=^(3)`. This remains true without any planarity assumption. The statement is
for one representative graph, with every pin distinct and literal.

**Proof.** If a graph accepts every member of `R_=^(3)`, each of its pin-pin
edges must join pins which always differ on that relation. The complete list
of such pairs consists of the ten original cycle edges and

\[
 b_0u_1,\ b_0u_4,\ u_0b_1,\ u_0b_4.                 \tag{1}
\]

Here is a direct verification that the list is exhaustive. Nonadjacent pins
on either C5 can be equal in a proper three-colouring. For a cross pair with
neither pin distinguished (`bi,uj`, with `i,j != 0`), each cycle independently
has a proper three-colouring with its distinguished pin coloured 0 and the
specified pin coloured 1, so these two pins can be equal. A cross pair
`b0,uj` with `j=2 or 3` can be equal in a proper three-colouring of U, and the
same argument applies to `u0,bi`, `i=2 or 3`. Finally `b0,u0` are always equal.
These constructions use one common palette and preserve `b0=u0`.

Now set, in the original ordered slots,

\[
 \beta_*=(1,2,1,0,2),\qquad
 \tau_*=(0,2,0,1,2).
\]

Both C5 colourings are proper; U uses three colours. The pair satisfies all
four edges in (1) and all original cycle edges, but `b0=1 != 0=u0`.
All ten pins use only colours 0,1,2. If there is one private vertex, colour
it 3; this works for *every* subset of its possible neighbours. If there
is no private vertex, the pin assignment itself is already a full lift.
Thus every candidate graph accepting all target cells also accepts this
forbidden cell. This proves the lower bound for a single representative.

This proves the theorem. QED.

The finite certificate independently stores, for each of the other 31 pin
pairs, a target assignment with equal endpoints, and checks all 1024 possible
neighbour sets for the optional private vertex. This is a calibration of the
explicit universal proof, not a finite search promoted to an unbounded claim.

## 4. Arbitrarily large graphs in this representable class

Starting with the r=2 annulus, repeatedly insert a new private vertex into
one of its triangular annular faces and join it to the three face vertices.
This preserves both named cycles, the empty inner face, and all outside
attachments and rotations. Each proper colouring of that face uses three
colours, so the inserted vertex has exactly one possible colour. Restriction
and reverse insertion give complete lifts between the decorated graph and
the r=2 representative, preserving all named cells (including four-colour U
cells and empty cells).

The construction works for any number of insertions; it is not inferred from
a bounded enumeration. The finite control makes five insertions, so the
original annulus has r=7 and its restored wheel has thirteen internal
vertices. Removing the five explicitly owned insertions gives the r=2
annulus and an eight-internal-vertex restored wheel. This example is therefore
a literal `13 -> 8` compression, with all lifts recorded in both directions.

**This class cannot witness the assumed globally minimum catalogue-outside
source:** the insertion has a removable degree-three vertex, and the equality
gadget contains an occupied separating triangle. The frozen source assumptions
exclude both. The control's source-minimality status is `not triggered`.

## 5. Replay, scope, and remaining methods

```
python3 -B audits/2026-10-13-w5-three-support-19209f4c/representatives/check.py --check
```

Only Python's standard library is used. `--check` regenerates the full
certificate without writing; `--write` creates both artifacts exclusively
and refuses overwrites. The certificate has all 10 x 1024 named cells per
graph, including 9640 empty cells; each graph has 1200 H full lifts and 600
restored-G full lifts. Its 1200 three-colour-U cells include 300 nonempty
cells. All rotations, edges, oriented faces, insertions, pin names and
ownership are explicit. Centre extensions are the explicit unique missing
colour rule; the checker verifies the complete source/representative lifts.

The proven result is exact for this relation: `r_min=2`. It rules out a
universal single-representative theorem at `r=0` or `r=1`; arbitrary ordinary
annulus graphs with `2 <= r <= 6`, weaker outer-Sigma-only replacement,
positive unions, source-dependent reductions, and the actual 933/941 minimum
source remain unexcluded. There is no new Lean theorem and no claim that
this construction supplies the requested general or source-conditional
r<=6 theorem.
