# C: marked cyclic four-cuts and the original degree-five v branch

BASE `f1faf743833c51ddc5efbe9e0f390b87b9f2311d`; immutable inputs are under
`../frozen/` and are individually hashed by `../BASE.json`. All names refer to
the same original minimum no4ct source G and its actual quotient J and dual D.
The complete seven-pin U relation, every private colouring, empty fibres and
all original r lifts remain in force. Nothing below supplies a new source.

## 1. Every cyclic four-cut avoids e and f

**Theorem C4.** Every actual cyclic four-edge cut of D avoids both
`e=(vw)*` and `f=(pq)*`. It may contain `g=(mz)*`.

Proof. The frozen source geometry proves that the primal image of a cyclic
four-cut is an induced four-cycle Q meeting m or z. If Q contains vw,
it cannot contain m, since m is adjacent to both v and w and supplies a
chord. It must therefore contain z. But a four-cycle containing the edge
vw and vertex z has z adjacent on that cycle to v or w; both edges zv,zw
are forbidden. Thus Q cannot contain e.

If Q contains pq, it cannot contain z, because zp,zq supply a chord.
Thus Q contains m. Write its cyclic order `(p,q,A,m)`, allowing reflection
p/q. This order requires mp and mA,qA. The actual source identity mp iff
`d_G(a)=4`, together with `d_G(a)+d_G(c)>=11`, gives `d_G(c)>=7` and mq
absent. The frozen exact common-neighbour identity now gives

`N_J(m) intersect N_J(q) = {z,p}`.

A cannot equal p because cycle vertices are distinct; A cannot equal z
because zp is a forbidden chord of Q. There is no A. The reflected order
uses mq iff `d_G(c)=4`, `d_G(a)>=7`, and
`N_J(m) intersect N_J(p)={z,q}`. Therefore Q also avoids f. QED.

This improves the old short-cut information on the same arbitrary-size
graph: each cyclic four-cut avoids e,f, while every cyclic five-cut contains
at most one of e,f,g. It does not imply that an alternating exchange has no
odd complementary cycle: a complementary cycle is not an edge cut.

## 2. A legal C5 completion when the original v has degree five

Assume temporarily `d_G(v)=5`. Its literal original rotation is
`(r,w,i,j,s)` up to reversal; all five vertices are distinct. In U, v has
neighbours `(w,i,j,s)`. The vertices i,j differ from p,q, because all four
original edges pv,pw,qv,qw are absent. The original no-separating-triangle
property implies si and jw are absent: either would chord the link of v.
The six vertices `(z,s,j,i,w,t)` are distinct. In particular z is not a
neighbour of v, and t is not a neighbour of v. Deleting v from U gives the
literal triangulated hexagonal disk H with that ordered outer boundary.

Draw si through the outer face, close to the outer arc s-j-i. The resulting
triangle s-j-i is a new face, j becomes interior, and the remaining outer
boundary is `(z,s,i,w,t)`. Thus

`V_i=(U-v)+si`

is an actual legal C5 disk with k-1 total vertices and k-6 interior vertices.
Every old vertex and edge of H remains; only the displayed edge is added.
It is therefore within the original smaller-source K132 authority. The
reflected completion `V_j=(U-v)+jw` has boundary `(z,s,j,w,t)` and keeps i
interior. These are two actual graphs, not a claim of a common colouring.

For one complete colouring of V_i, keep the actual private colour of j.
Its entire U lift fibre consists of all colours

`L_v = {A,B,C,D} minus {colour(s),colour(j),colour(i),colour(w)}`.

For each v in that exact set, the complete r lift set is
`L_r(v)={A,B,C,D} minus {colour(s),v,colour(w),colour(t)}`.
The frozen original R rule must hold for every pair `(v,r)` in these sets.
Empty L_v and L_r fibres are retained. In particular adding si does not
supply an arbitrary v lift or permit choosing j independently of the full
V_i colouring.

Every original U colouring with literal frame ABABC restricts to a complete
V_i colouring: s=w=B, while i,j are the two other colours C,D, since they
are adjacent to each other, to v=A, and respectively to w,s. The resulting
V_i frame is ABCBC or ABCBD after one common colour permutation. Therefore
excluding both of these V_i rows by legitimate same-colouring arguments
would exclude `d_G(v)=5`; no such exclusion is asserted here.

## 3. Same-H dual completion theorem

**Theorem C5 (paper reduction plus finite necessary exhaustion).** If the
same source has `d_G(v)=5`, then both actual graphs above have exact complete
ordinary boundary support

`Sigma(V_i)=Sigma(V_j)=1022`.

This does not claim that the two complete private-colouring relations are
equal. It says that each graph, in its own displayed ordered frame, rejects
ABABC and realizes each of the other nine rows. The finite computation
supplies the last exhaustion step of the theorem, so this is not advertised
as a table-free paper proof.

Here is the precise necessary reduction. Use H pins `(z,s,j,i,w,t,p,q)`.
The H edge set on these pins contains its actual ordered outer C6 and the
actual triangle zpq. Enumerate all local assignments and impose the universal
v/r rule from section 2, including empty v and r fibres. Modulo one common
colour permutation this gives 99 proper rows. For each of the three
complementary palette pairings, the actual maximal components induce a
partition of the pins. It must respect every retained edge, and complementary
components cannot cross on the six genuine outer pins. Switching any subset
of these full components gives another full H colouring and therefore another
allowed row. All partitions with these necessary properties are retained;
there is no claim that any retained abstract partition is realized.

Iterating this necessary condition removes 14, then 2, then 2 rows, leaving
81. Every true H row survives by induction: its actual partition provides an
option whose entire switch orbit consists of true rows. No private vertex is
recoloured independently of its actual maximal component.

For each true full H colouring, its membership in Col(V_i) is exactly
`s!=i`, and its membership in Col(V_j) is exactly `j!=w`. The edge added to
each cap is the only extra condition; every private vertex is unchanged.
Thus these two relations are restrictions of the **same** full H relation.
The ordinary boundary masks must belong to the original K132, because both
caps have k-6 interior vertices. Each cap's upper mask is 1022; the frozen
K132 supplies 39 candidates for each cap. For each of the 1,521 pairs, retain
only H rows whose existing cap projections belong to the chosen masks,
repeat the H necessary component closure, and require both cap supports to
be exactly their chosen masks and the union of **all** v lifts to have the
known complete U support 319. Only `(1022,1022)` survives. This proves C5 by
exhaustion of necessary alternatives. The surviving 81-row relation itself
is not asserted to be the relation of an actual graph.

The independent local table for V_i has 70 normalized rows, and its
five-boundary component screen leaves 66 while retaining all 39 catalogue
candidates. The joint same-H restriction is essential to this narrowing.
The frozen catalogue is additionally sealed by `../ADDITIONAL_INPUTS.json`;
no new catalogue enumeration or completeness claim is introduced.

## 4. Using every original a/c split colouring strengthens the relation

There is a still stronger actual helper graph

`F=G-{x,y,b,r,v}`,

whose ordered outer boundary is `(c,s,j,i,w,t,a,p,q)`. It is obtained
by deleting the original collar vertices and v, rather than by pretending
p,q were boundary vertices of H. Its nine boundary vertices are distinct,
and every old edge and private vertex survives. The two separate boundary
vertices a,c retain their original attachment sectors. Its equal-colour
slice a=c is exactly the full H relation, through the literal quotient that
identifies a,c as z.

For each complete F colouring, restore exactly the original vertices
`(v,r,x,y,b)` with exactly their original attachments:

* v joins s,j,i,w,r;
* r joins s,v,w,t,x,y;
* x joins c,s,r,y;
* y joins x,r,t,a;
* b joins a,c,p,q.

Every proper five-vertex completion is retained, including the case of zero
completions. Fix the source mask S once for the whole graph: the frozen
source theorem states `S in {932,933,941}` in frame `(x,y,a,b,c)`. Each
restored boundary row must belong to that same S. S is never selected anew
for an individual F colouring.

There are 820 normalized proper nine-boundary rows, each with 24 distinct
global colour permutations; they represent all 19,680 proper labelled rows.
The remaining 242,464 labelled assignments are explicitly improper and
have empty proper fibres. The retained local file lists all 820 proper
fibres: 475 are empty and the others have a total of 648 normalized full
five-vertex completions. An independent direct 14-vertex edge check verifies
every listed completion and every empty fibre.

Running the same necessary maximal-component closure, now on the **actual
nine-point outer Jordan cycle**, gives:

| Fixed original S | Initial necessary F rows | Stable F rows | Full original lift support | a=c slice rows |
| --- | ---: | ---: | ---: | ---: |
| 932 | 607 | 362 | 932 | 58 |
| 933 | 659 | 536 | 933 | 58 |
| 941 | 716 | 662 | 941 | 58 |

The three equal-colour slices are literally the same 58 normalized H rows.
All three preserve U lift support319. The 58-row H relation remains stable
under the earlier six-boundary necessary screen, and the simultaneous K132
cap test again leaves only `(1022,1022)`. This is a genuine additional
necessary restriction: 23 of the old 81 H rows cannot occur in a source,
using full switches through a!=c and all original reconstruction lifts.
It does not force any private colouring into those 23 rows, so it does not
exclude v5.

The auxiliary nine-boundary calculation which merely required a=c and
merged the split a/c components before switching gave no further deletion
beyond 81. It correctly allowed the two split copies to be disconnected;
forcing them to stay connected would wrongly delete legitimate partitions.
The separate six-ear-cap exploration is likewise only an exploratory
necessary control and is not used in Theorem C5.

## 5. Remaining obligation and reconstruction cost

The legal C5 completions force the two complete supports1022, and the
full original reconstruction restricts the joint H relation to58 necessary
rows. Their surviving target rows have not been excluded. In particular any retained option does not prove source
realizability. The all-distinct AD/BD linkages may still meet at a D vertex;
the locally valid W5 rim ABABC remains an allowed crossing.

C4 does not yet produce `W110+W101>0`. No same-source odd-cycle repair or
completed-source strict decrease is proved. Starting from V_i, removing the
one added edge si and restoring v recovers U, then the original restoration
cost is five vertices, so `(k-1)+1+5=k+5`. Numerical helper size is not a
bad-source decrease. Complete319, the v/w degree-five exclusions, and the
joint even-complement endpoint remain OPEN. No external theorem, 4CT,
new Lean claim, commit, or push occurs.


## 6. Evidence and authority

`check.py` verifies the frozen paper and catalogue input hashes, the worker
seal, all820 original five-vertex fibres by a separate edge test, and replays
four screens from their exact inputs. `VERIFICATION.json` records default,
PYTHONHASHSEED=17, corrupted-fibre rejection and exclusive-create rejection.
The finite screen retains all abstract component choices and switches every
subset; it is a sound necessary relaxation, not a complete source model.
Actual minimum source instances supplied: zero, **not triggered**. Paper
C4, paper geometry and finite C5 exhaustion remain distinct authorities.
