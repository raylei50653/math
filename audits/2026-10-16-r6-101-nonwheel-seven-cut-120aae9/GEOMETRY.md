# R6-101-NONWHEEL-SEVEN-CUT: disk geometry and localized odd curvature

Research BASE `120aae90cab8bc4881916adc598cf344f2f20f4b`.
This is the independent geometry route for the same original minimum,
secondary maximum-edge, noncatalogue C5 source G. Its ordered boundary,
original degrees, actual legal `J=U/(s=t)`, actual spherical dual `D=J*`,
and literal marks `e=(vw)*`, `f=(pq)*`, `g=(mz)*` are retained throughout.
No graph or barrier is replaced. This route proves new necessary conditions
for arbitrary source size; it does not exclude every remaining component.

## G1. Adopted inputs and the new theorem

The [frozen source geometry](frozen/audits/2026-10-15-j-source-geometry-6ddea32/PROOF.md)
supplies all facial triangles, the exact m and z sectors, the marked
faces `mvw,zpq,mz alpha,mz beta`, the original degree identities, and the
absence of dual cuts of size one or two. Every dual three-edge cut is
trivial. The [original-sector theorem](../2026-10-16-r6-joint-zero-c4c3d99/C/PROOF.md)
says every induced J C4 meets m or z, and its two rays cross their original
sectors; with both hubs, their edge mz must be a cycle edge. The
[weighted curvature identity](../2026-10-16-r6-cap-barriers-c4c3d99/A/PROOF.md)
and [common-111 saturation](../2026-10-16-r6-cap-barriers-c4c3d99/B/PROOF.md)
are inherited. The latter is one simultaneous statement about the whole
nonempty `P111`, not separate matching witnesses.

Fix any maximum-cardinality violating set S for `H=D-X-f`,
`X=V(e) union V(g)`. In the remaining seven-cut case, the inherited budget
and barrier results give:

* C is the unique nonsingleton component of H-S and is factor-critical;
* `|delta_D(C)|=7`, and every other component is a singleton;
* f joins two different components of H-S (`tau=1`);
* `B=E_D(S) union E_D(S,X)` is empty, and `D[X]={e,g}`.

**New theorem.** The actual faces C form a triangulated closed disk R
whose boundary Q is a simple seven-cycle. No Q chord lies on the R side.
No vertex in `T={m,z,v,w,p,q}` is strictly interior to R. Let

`i_odd = number of strictly interior R vertices of odd complete J degree`,

`t_u = number of neighbours of a boundary vertex u strictly interior to R`,

`b_odd = number of u in V(Q) with t_u odd`,

`epsilon = 1 if m lies on Q and t_m is odd; otherwise 0`.

Then, for the same global parity excess Delta used in the adopted
weighted curvature theorem,

`Delta = i_odd + b_odd - 2 epsilon - 10`,                      (G1)

`Delta >= 2(1-epsilon)`,                                    (G2)

and therefore

`i_odd + b_odd >= 12`, `i_odd >= 5`.                          (G3)

In particular R has at least five strictly interior vertices and C has
at least fifteen dual vertices. This excludes the whole arbitrary-size
subclass with at most four odd-degree vertices strictly inside R, even
if arbitrarily many even-degree interior vertices are allowed.

## G2. Factor-critical consequences used here

The induced subgraphs `H[C]` and `D[C]` coincide, because f is between
different residual components. The connected nonsingleton graph `D[C]`
has minimum degree at least two. A degree-one vertex u with neighbour v
would remain isolated after deleting v; the resulting nonempty even
vertex set could not have a perfect matching.

It is also bridgeless. If ab were a bridge, one component after its
removal would have even order and the other odd order, since C has odd
order. Delete the endpoint of ab on the even side. The odd side is now
a disconnected odd component of the remaining graph, preventing a
perfect matching. This contradicts factor-criticality.

Here `D[C]` has maximum degree three. It is consequently two-connected:
if a vertex separated two or more components, bridgelessness would
require at least two incident edges from that vertex into every such
component, requiring degree at least four. This last implication uses
the actual subcubic hypothesis; factor-criticality alone does not imply
two-connectivity.

## G3. The complement is connected: the possible triangular hole is excluded

Assume `D-C` is disconnected. Each of its components requires at least
three cut edges. Their total is seven, so there are exactly two, with
cut sizes three and four. The three-edge-cut component must be a single
dual vertex t. Indeed all dual three-cuts are vertex stars, and the
alternative side of such a star contains all vertices except t, which
cannot be this component because C has at least three vertices.

All three neighbours of t are in C. The vertex t cannot be in X, because
its forced matching mate is also in X and therefore outside C. It
cannot be in a different component of H-S: between that component and
C there is at most the one edge f. Thus `t in S`.

Put `R_4=C union {t}` as a face region and let K be the other component
of `D-C`. Both `D[R_4]` and `D[K]` are connected, and their cut has size
four. K contains all four faces X. The primal cut is a simple C4, Q4.
It is induced: any chord would divide one side into two actual facial
triangles, while the two sides have respectively at least four faces
(`|C|+1>=4`) and at least four faces (X). This is impossible.

All faces of R4 avoid X. The following exhaustive source argument
excludes its induced four-cycle:

* If Q4 avoids both hubs, it violates the adopted induced-C4 theorem.
* If Q4 contains both hubs, inducedness makes mz a boundary edge, but
  both faces on mz are in X, so neither is in R4.
* If Q4 contains m alone, its nonempty R4 face interval at m avoids
  `mvw,mz alpha,mz beta`. Removing these three edges from `link_J(m)`
  leaves the singleton z and the two original sector paths. Both Q4
  rays at m therefore lie in the same original sector, contradicting
  the induced-C4 crossing theorem.
* If Q4 contains z alone, that theorem requires its two rays in opposite
  a/c fans. Its R4 interval avoids the two mz faces and therefore
  contains the actual face zpq. The vertex t belongs to S, while neither
  endpoint of f belongs to S. Thus `zpq in C`. The other f endpoint is
  in a different residual component and is neither in C nor t. Hence f
  crosses R4 and `pq in E(Q4)`. This puts the facial triangle z,p,q in
  an induced four-cycle, a contradiction.

This proves that `D-C` is connected. In particular no triangular hole
is silently ignored before treating the seven-cut as a disk boundary.

## G4. The seven-cycle disk and its complete internal incidence

The cut `delta_D(C)` is now a bond. Its primal image is a simple cycle
Q with seven edges, with exactly the faces C on one side. Equivalently,
connectedness on both dual sides rules out more than one boundary
component or a self-touching boundary. Thus those actual faces form the
closed triangulated disk R.

Suppose a Q chord lay inside R. It would split R into two nonempty face
disks whose only dual adjacency is the edge dual to that chord. This is
a bridge of `D[C]`, contrary to G2. All possible chords of Q therefore
lie on its exterior side. Inducedness of Q itself is not claimed.

Each face in C has at most one Q edge, by its internal dual degree at
least two. Consequently the seven Q edges have seven distinct incident
C faces. These are exactly the seven degree-two vertices of `D[C]`;
every other C vertex has degree three. Their order is the actual cyclic
order on Q, rather than a freely permutable terminal list.

No T vertex is strictly inside R. Interior m, z, v or w would place an
incident forced face in C. Interior p or q would place both endpoints
of f in C, contrary to tau=1. Every strictly interior vertex therefore
has its unchanged complete J degree at least five. All its incident
faces and all its incident edges are present in R.

For u on Q, the absence of inside chords gives the exact disk degree
`d_R(u)=2+t_u`. At least one interior neighbour occurs at each u:
otherwise its R face interval would be the single facial triangle on
its two Q neighbours, with an inside Q chord. Thus `t_u>=1`.

Let i be the number of strictly interior vertices. Disk Euler and
triangle incidence give

`|C|=2i+5`,                                                   (G4)

`E_ii+E_ib=3i+4`,

where `E_ii` joins two interior vertices and `E_ib` joins an interior
vertex to Q. Also `E_ib=sum_{u in Q}t_u` and
`sum_{a interior}d_J(a)=2E_ii+E_ib`.
These are identities for the actual disk; they are not a finite census.

## G5. Exact weighted curvature localized to this disk

Give the faces `S union X` bit zero and every residual component bit one.
The complete set of monochromatic primal edges is exactly

`F*={vw,pq,mz} union I_R`,                                   (G5)

where `I_R` consists of all R edges except its boundary edges. The
pieces are disjoint. This uses B empty and tau=1: vw,mz join zero
faces, pq joins two different one components, and every remaining
one-one adjacency is internal to C.

For completeness, write `o_u=d_J(u) mod 2`. The parity-sensitive minima
from the adopted theorem are

| Vertex class | Minimum complete degree for parity o |
| --- | --- |
| m | `8-o` |
| z | `6+o` |
| v,w,p,q | `4+o` |
| all other vertices | `6-o` |

Set Delta to the sum of the complete degree excesses over these minima.
Every summand is a nonnegative even integer. With

`Qcharge(o)=6+o_m-o_z-sum_{u in {v,w,p,q}}o_u+sum_{u outside T}o_u`,

the adopted Euler identity is `12=Qcharge(o)-Delta`.

For any face-bit assignment, face transitions around a primal vertex
are even in number. Its complete degree parity is therefore its
monochromatic-edge incidence parity. The three disjoint marked edges
alone give parity one at exactly T and have `Qcharge=2`.

The I_R incidence is the complete degree at an interior vertex, t_u at
a boundary vertex, and zero elsewhere. Each odd incidence flips the
marked-edge baseline. Every flip raises Qcharge by one, except the
flip at m, which lowers it by one. Hence

`Qcharge=2+i_odd+b_odd-2epsilon`.

Substituting Euler proves (G1). This argument uses all incidences and
the actual degrees; it does not project to a boundary marginal.

## G6. An original-sector cost at m supplies the extra two units

The source has `d_G(s),d_G(t)>=6` and
`d_J(m)=d_G(s)+d_G(t)-5`. The two original m sector paths have exact
lengths `d_G(s)-3` and `d_G(t)-3`, with endpoints the zero faces on mz
and the zero face mvw.

If C has a face at m, then m is on Q and its C faces form one interval.
That interval avoids all three displayed zero faces and lies in exactly
one original sector. Its length in faces is

`L=d_R(m)-1=t_m+1`.

Every other one-face interval in either m sector is a singleton residual
component. There are no other consecutive one faces: their shared
primal edge is incident with m, so its dual is not f, and hence they
could only be in the same residual component C. There are no consecutive
zero faces inside a sector: B is empty and neither marked zero-zero edge
vw or mz is an internal sector edge.

If a sector contains k singleton one-blocks and no C block, its exact
zero-to-zero face word gives

`d_G(u)-3=2k` for `u=s or t`.                                 (G6)

If it contains the unique C block, its exact word instead gives

`d_G(u)-3=2k+(L+1)=2k+t_m+2`.                                (G7)

These count actual face transitions. They include empty singleton lists
and do not assume any original fan endpoints to be distinct beyond the
frozen source contract.

If epsilon is zero, either m is absent from Q, or t_m is even. Equations
(G6)--(G7) then make BOTH original degrees d_G(s),d_G(t) odd and hence
at least seven. Consequently `d_J(m)>=9`. Its parity is odd: the baseline
at m is odd and no odd I_R incidence flips it. The odd parity minimum
at m is seven, so its degree excess alone is at least two.

If epsilon is one, the nonnegative excess identity is all that is needed.
Thus in all cases

`Delta>=2(1-epsilon)`.

Combining this with (G1) yields

`i_odd+b_odd>=12`.

Since Q has seven vertices, `b_odd<=7`, proving `i_odd>=5` and therefore
`i>=5`, `|C|=2i+5>=15`. No bounded-size or small-i enumeration enters
this proof.

## G7. The exact remaining interface and OPEN

The remaining candidate is an actual two-connected, factor-critical,
subcubic plane dual patch with seven distinct degree-two ports, all
other vertices of degree three, at least fifteen vertices, and at least
five odd-length bounded faces corresponding to complete odd-degree
interior primal vertices. Its internal primal vertices avoid all T.
Every boundary chord is exterior. Its actual ordered seven-port matching
fibres must still be retained, including every empty fibre; no such
fibre has been discarded or identified by this geometry proof.

The exterior must still be glued on the same J,D,S: it contains the
four fixed forced faces, all singleton residual components, the actual
f edge, and the source m and z sectors with B empty. Seven ports are a
finite boundary size, not a finite family of private interiors. A proof
that no such patch and exterior satisfy every source premise is OPEN.

The theorem excludes every candidate with at most four odd interior
vertices, including arbitrarily large private disks with many even
interior vertices. It also excludes every candidate with fewer than
fifteen dual faces. It does not prove ordinary 101 matching existence,
even complement positivity, `W110+W101>0`, complete 319 exclusion,
source reconstruction descent, or a general `K_infinity=K_<=5` statement.
Original complete colouring fibres, all r lifts, the existing `k+5`
reconstruction cost, general `K_<=22=K_<=5`, and fixed-r6 `k>=25` remain
unchanged.

No external theorem, synthetic source realization, Lean theorem, commit
or push is introduced by this route. Independent calculation may
calibrate the finite parity and sector-word identities; its domain
cannot establish arbitrary-source nonexistence.
