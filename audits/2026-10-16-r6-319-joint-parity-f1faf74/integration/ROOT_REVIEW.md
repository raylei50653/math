# Root independent review

The initial HEAD is f1faf743833c51ddc5efbe9e0f390b87b9f2311d. The working
tree already contained the previous continuation and three documentation
edits; their bytes were frozen before delegation, not reset or overwritten.

## Geometry and source reductions

I independently reconstructed C4's proof: an induced quadrilateral through
vw cannot contain m (a chord) or z (a forbidden incident edge). Through pq
it cannot contain z; containing m requires mp or mq. For mp, a=4 and the
source degree sum force c>=7, reducing the exact common-neighbour set of
m,q to {z,p}; neither supplies the fourth vertex of an induced cycle.
Reflection gives the other orientation. This establishes the claimed
arbitrary-size cyclic-four-cut restriction and no oddness conclusion.

For v5, the original link (r,w,i,j,s) and the proved original nonedges give
the six distinct boundary vertices (z,s,j,i,w,t) after deleting v.
The additions si and jw are separately legal exterior triangle caps.
Their entire colouring sets are literally the s!=i and j!=w subsets of
the same H colouring set. They may therefore be constrained together
without merging independently chosen witnesses. I directly enumerated
all 65536 eight-pin assignments of one cap and all nested v/r lifts:
70 canonical allowed rows, upper mask1022, and39 K132 candidates. In
particular the two target rows have exactly j,p,q=DBC/DCB and DBD/DDB.
A's independent reconstruction reviews the subsequent shared-H fixed point
and the complete1521 mask-pair comparison; see A/REVIEW-C.md.

The stronger source-F step retains a!=c colourings as well. Deleting the
literal vertices x,y,b,r,v exposes the nine-cycle c,s,j,i,w,t,a,p,q.
Each original source mask is fixed throughout its own calculation. Every
proper F colouring, including one with no G lift, must remain in its own
actual Kempe cubes; hence each elimination round gives a valid inductive
upper bound on the true full-colouring projection. Restricting the final
upper bound to a=c yields a necessary bound on every H colouring. B's
separate explicit-edge enumeration confirms all820 local fibres,475 empty
ones,648 lifts, and the three607/659/716 initial tables. I reviewed this
inductive necessity argument and replayed the full C screen, which leaves
the common58-row upper bound. This is a finite-assisted necessary source
theorem, not proof that its remaining rows are realizable.

The last count-cone check expands all58 rows into1392 literal assignments
and enforces one shared count vector across all three palette pairings.
The exact Fraction replay checks the saved weights and25 positive support
conditions. Its feasibility does not establish the actual component
identities across palette changes or a source graph. The original
unbounded geometric problem remains outside that relaxation.

For C's final addendum, I reran all58 single-row absence tests using A's
independent component engine instead of C's implementation. Exactly the
claimed six rows force the stable support triple(1022,1022,63), with40
remaining rows. Each therefore contradicts the required U bit8 if absent.
The12 literal fixed-A/B fibre existence conclusions are accepted, including
their empty v lifts. The actual K=J-v quotient uses the entire s=t slice,
not only those six rows. Its34→34 result was independently reconstructed
by A and replayed from C's saved certificate. This gives no source exclusion.

## Complete-colouring transports

I reviewed A's two component involutions and the singleton argument. The
AB/CD swaps operate on disjoint induced vertex sets, so their full maps
commute, not just their six visible values. In a CD cube, differing m,u
already exclude both C,D from the z fibre; equal m,u exclude the other
colour by the forbidden e=g!=f event. The BD statement first requires the
actual w,d component coincidence, correctly proved by a forbidden e=f!=g
swap. This does not force any separated subfibre to be nonempty.

## Independent finite global-oddness countercontrol

independent_control.py imports no worker checker. It fixes an actual
facial triangle, enumerates all 4^9 remaining assignments, then restores
all24 common colour permutations. It enumerates every dual PM with an
independent bit-mask recursion, retains every empty colouring fibre, and
derives small cuts by enumerating primal simple four-/five-cycles. This
differs from B's enumeration of all dual vertex bipartitions.

The complete results agree:288 labelled colourings,38 PMs, the joint
family consists of three101 matchings each of oddness2, and W111=6,
W010=W001=2,W110=W101=0. There are2 cyclic four-cuts and22 cyclic
five-cuts. Neither orientation of the marked g endpoints permits the
literal source face layout. Thus the control refutes only the weakened
implication explicitly stated in B.

During review I found that the copied input initially retained old
marked endpoints/pins while its edge-index marks had been changed. The
worker corrected these before producing its active certificate and added
negative controls rejecting both kinds of stale marking. I also required
A's writer to use exclusive creation; its original script/certificate
were retained and active certificate-v2 was generated after that change.
These corrections are custody safeguards, not proof advances.

## Scope

No statement here converts an ordinary matching into an even-complement
one, combines independent private colourings, supplies a minimum source,
or claims strict completed-source descent. The restoration remains k+5.
The original complete319 exclusion and the joint positivity are open.
