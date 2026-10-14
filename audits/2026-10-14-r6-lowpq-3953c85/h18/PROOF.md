# The induced original collar excludes h=18 and sharpens the active budget

BASE `3953c85e334b96533e44652df065640f5463715a`. This audit uses the same
globally minimum noncatalogue no4ct source G, with literal outer cycle
`B=(x,y,a,b,c)`, `Sigma(G) in {932,933,941}`, and
`d_G(x)=d_G(y)=d_G(b)=4`. Every degree below is an original G degree.
The input authority is the parent input seal; this file does not alter
old reports, certificates, or their historical claim boundaries.

**New source conclusion:** in this fixed branch, `k<=27` forces `h<=12`.
In particular the proposed `h=18` extreme is excluded. This is an
arbitrary-size geometric and degree argument before the final numerical
specialization. It uses neither a new graph enumeration nor an
intersection of colour supports from different deletion graphs.

## 1. Authority and the original collar

Use the [simple original collar](../../2026-10-13-c5-no4ct-collar-6cafdfb/REPORT.md),
the [four-connected T0 and exact original geometry](../../2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md),
the [double-low ell bound](../../2026-10-14-c4-return-branches-a11d4bb/pq/PROOF.md),
the [zero-side s/t bounds](../../2026-10-14-c4-return-branches-a11d4bb/r_high/PROOF.md),
and the accepted [source table](../../2026-10-14-lowpq-source-676b102/classification/SOURCE_TABLE.md).
Write `alpha=d_G(a)-4`, `gamma=d_G(c)-4`, `h=alpha+gamma`.
The inner neighbours of a in original rotation are
`t,A1,...,A_alpha,p`; those of c are `q,C1,...,C_gamma,s`.
The known simple original collar is therefore

`C=(r,t,A1,...,A_alpha,p,q,C1,...,C_gamma,s)`, `|C|=h+5`.

Its five apex vertices r,t,p,q,s each have exactly two original B
neighbours. Every one of the other h collar vertices has exactly one.
All these vertices are distinct. Let H be the original disk inside C
and `P=V(H) minus V(C)`. This P denotes private vertices, not a degree
variable and not the p-deletion face.

Set `E=sum_{v notin B}(d_G(v)-5)`. The accepted original Euler identity
is `k=h+6+E`; therefore `|P|=k-h-5=E+1`. Every summand is nonnegative.

## 2. C is induced at every h in this branch

The authority constructs the simple four-connected sphere triangulation
T0 by identifying a,c to z and deleting u,b. Its z-link in the actual
embedding is

`(x,y,t,A1,...,A_alpha,p,q,C1,...,C_gamma,s)`.

The link of a vertex in a four-connected sphere triangulation is
induced: an edge between nonconsecutive neighbours would form a
nonfacial triangle through that vertex, contradicting the absence of
separating triangles. Thus after removing x,y, the retained path
`t,A*,p,q,C*,s` has no extra edges between its vertices.

The remaining collar vertex r is not adjacent to z. The source geometry
proves the exact whole-graph equality

`N_R(z) intersect N_R(r) = {s,t}`.

Every vertex of the preceding path is a z-neighbour in R. Hence r has
no extra edge to that path either. The two retained edges rt,rs close
exactly the cycle C. All edges under discussion are original edges
between retained vertices, so this proves that the **original collar C
is induced**, without an assumption on h, p, q, or r beyond the fixed
source contract.

## 3. The private graph is connected

H is a connected triangulated disk with simple induced boundary C,
and `|C|>=8` since the accepted collar theorem gives h>=3. Every inner
triangle contains at least one P vertex: three C vertices could only
form a triangle if C had a chord. Every edge shared by two inner
triangles also has a P endpoint: an edge with both ends in C would be
a boundary edge or a forbidden chord, and boundary edges are incident
with only one inner triangle.

The adjacency graph of the inner triangular faces across inner edges
is connected. Within a triangle all its P vertices are connected by
edges; across consecutive triangles the shared edge supplies a common
P endpoint. Consequently all P vertices belong to one component of
H[P]. Also P is nonempty, since a chordless cycle of length at least
four cannot be triangulated using its boundary vertices alone.
Therefore, writing `e_P=|E(H[P])|`,

`e_P >= |P|-1`.

This proves the needed connectivity from the actual original disk. It
does not posit a connected private representative for an arbitrary
boundary colour relation.

### The private graph has no leaf and has at least two independent cycles

First `E>=3`, so `|P|=E+1>=4`. If r=6, the already proved s,t>=6
provides three units of excess at r,s,t. If r>=7, r provides two;
if either p or q is at least six that vertex provides another. In the
remaining p=q=5 case the accepted ell>=6 theorem provides another, at
a vertex distinct from r. This argument does not use k<=27 or G28.

Suppose u is a degree-one vertex of H[P]. In its full original cyclic
link, its unique private neighbour is followed by the other
`d_G(u)-1>=4` neighbours, all in C. Consecutive members of this latter
list are adjacent by the original triangular faces. C is induced, so
they form one consecutive C arc. Each middle vertex of this arc has
its whole inner sector filled by the two triangles incident with u;
its only H neighbours are its two C neighbours and u. Thus its H
degree is three. It cannot be a one-contact collar vertex, which would
have original degree four. It must be an original degree-five apex.
There are at least two such consecutive middle vertices.

The only possible consecutive pair of degree-five apexes on C is pq.
The pairs rs,rt are impossible because r>=6. A pair tp is consecutive
only when alpha=0, but the accepted a=4=>t>=6 excludes two degree-five
endpoints. Similarly qs is excluded by c=4=>s>=6. These exhaust the
adjacent apex pairs in the stated collar order. Consequently the arc
has exactly two middle vertices, p and q, and `d_G(u)=5`. Its triangle
upq is the actual inner face at pq, so u is the other pq-face vertex
ell. But the two middle vertices satisfy p=q=5, and the accepted
double-low theorem says ell>=6. This is a contradiction.

Since P is connected and has at least four vertices, it has no
degree-zero vertex either. Hence its minimum degree is at least two
and `e_P>=|P|`. If equality held, the connected graph H[P] would be a
simple cycle of length at least four. Its bounded side contains no C
vertices, which lie on the outer boundary of H, and no other private
vertices, since all P vertices belong to this cycle. Triangulation of
that empty polygon requires a chord, contrary to every P vertex having
P degree two. Therefore

**`e_P>=|P|+1=E+2`.**

Equivalently the connected private graph has cycle rank
`rho=e_P-|P|+1>=2`. This does not assert a particular private graph or
its colour relation.

## 4. An exact excess identity on one original graph

Define the nonnegative original degree excesses

`E_C=sum_{v in C}(d_G(v)-5)`,
`E_P=sum_{v in P}(d_G(v)-5)`, and `E=E_C+E_P`.

The accepted Euler identity is `k=h+6+E`, hence

`|P|=k-(h+5)=E+1`.

Let `A=|E_G(C,P)|`. Since C is induced, an apex contributes
`d_G(v)-4=1+(d_G(v)-5)` edges to P: two edges go to B and two to C.
A one-contact collar vertex contributes
`d_G(v)-3=2+(d_G(v)-5)`. Therefore

`A=5+2h+E_C`.

Private vertices have no B contacts by the original collar theorem.
Counting their degrees in the same original graph gives

`A+2e_P=5|P|+E_P=5(E+1)+(E-E_C)`.

Eliminating A yields the exact identity and its private-graph consequence

**`h=3E-E_C-e_P=2E-E_C-rho`, and `h<=2E-E_C-2`.**

Equivalently, at every size in this branch,

**`2k=3h+12+E_C+rho >= 3h+14+E_C`.**

These formulas count actual edges of one original G; they retain all
private-private edges. They do not replace any complete-colouring
fibre or infer a source from an arithmetically feasible allocation.

## 5. The proposed h=18 extreme is impossible

The accepted source table gives, when `h=18` and `k<=27`,
`k=27`, `r=7`, `s=t=5`, and `E=3`. Thus `|P|=4`.
For LH or HL, the single high p/q vertex has degree six; all excess
lies on C, so `(E_C,E_P)=(3,0)`. The actual C-to-P edge count would be
44, but the four private degrees sum to 20.
For LL, the other pq-face vertex ell is private and has degree six;
the r excess lies on C, so `(E_C,E_P)=(2,1)`. The C-to-P edge count
would be 43, but the private degrees sum to 21.

Both violate `A<=sum_{v in P}d_G(v)` even before private connectivity is
used. Equivalently the exact identity would demand respectively
`e_P=-12` or `e_P=-11`. These are contradictions for a real graph.

Here ell is private: its original triangle pqell puts it on the inner
side of collar edge pq, and an induced collar has no third collar
vertex adjacent to both p and q. In the accepted source table it was
already proved distinct from the five apexes; the induced-collar result
also excludes all one-contact collar vertices.

## 6. The resulting k<=27 active domain

At every size r>=6. If r=6, the adopted theorem forces s,t>=6, so
`E_C>=3`. If r>=7, r alone supplies `E_C>=2`. Thus universally in this
fixed branch `E_C>=2`. Combining this with the exact identity gives

**`k>=ceil((3h+16)/2)`, and `k<=27 => h<=12`.**

This improves the proposed h<=17 stopping point directly, without
having to combine the two s/t deletion masks. The bound is conditional
on the fixed x,y,b-four-degree source, and does not change the general
catalogue equality `K_{<=22}=K_{<=5}=K_132` or its k>=23 minimum-source
bound.

For comparison with the existing source table, retain its notation
`beta=Q-5` in LH, `beta=P-5` in HL, and `beta=d_G(ell)-5` in LL;
all beta>=1. Write `R=d_G(r)` and
`chi=1_{alpha=0}+1_{gamma=0}`. The following are additional necessary
conditions, to be intersected with all previous source conditions:

| Low p/q type | Original r branch | Lower bound on E_C | Necessary condition if k<=27 |
| --- | --- | --- | --- |
| LH or HL | R=6 | `3+beta` | `3h+beta<=37`, hence `h<=12` |
| LL | R=6 | `3` | `3h<=37`, hence `h<=12` |
| LH or HL | R>=7 | `R-5+beta+chi` | `3h+R+beta+chi<=45`, hence `h<=12` |
| LL | R>=7 | `R-5` | `3h+R<=45`, hence `h<=12` |

The LL excess at ell is private; it is still present in E, and was not
discarded or counted as a collar excess. These inequalities do not
prove that any remaining integer allocation is realized by a graph.

## 7. Scope and replay

The direct-deletion supports 956/1012/1020 and their reflection remain
valid on their own literal deletion graphs, but are not used in this
proof. No intersection of supports on different graphs is taken. The
suggested joint s/t fibre search stops because the exact original
geometry already excludes h=18 and supplies the stronger h<=12 bound.

`check.py --check` checks the incidence arithmetic independently through
the two degree sums and replays all bounded nonnegative integer degree
allocations admitted by these necessary constraints. It is a small
arithmetic audit, not graph enumeration, a realization test, or a
substitute for the topological proof above. Its certificate and logs
retain the exact h=18 contradictions and the raw, connected, and cycle-rank bounds.
General low p/q source exclusion, r=6 as a whole, and the unbounded
catalogue equality remain OPEN. No new external theorem, Lean theorem,
commit, or push is used.
