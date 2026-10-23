# 933: six fibres of one original C10, and the private 13 bridge

Fix the **same complete original globally minimum r6/933 source G** used in the
three frozen predecessor rounds. All original boundary names, rotation,
attachments, small-cap hypotheses and full support assumptions remain. This is
not a minimum taken only among mask-933 graphs. No original source is supplied.
The mathematical authorities, including the actual r rotation and the low-p
nonedges, are frozen byte-for-byte in [INPUTS.json](INPUTS.json).

## 1. Removing a genuine original cap

Retain the exact original data

```
B=(x,y,a,b,c), E=(a,n,R,L,q,c,x,y),
N(p)=(a,b,q,h,n), N(h)=(p,q,L,R,n), N(b)={a,c,p,q},
N(x)={y,c,r,s}, N(y)={x,a,r,t}, N(r)=(x,y,t,w,v,s).
```

Here p,h have original degree five, r has original degree six, and s,t have
original degree at least six. E is the genuine disk from the frozen
[two-star source proof](frozen/audits/2026-10-18-smaller-bad-e1617a2/B/PROOF.md).
The stronger disjointness needed here follows from the **full source geometry**,
not from the fact that E alone is a C8:

1. The frozen [active-f source, section 2](frozen/audits/2026-10-17-r6-active-f-seven-ffea555/B/PROOF.md)
   proves h=ell has no original edge to s,t. It also gives
   pv,pw,qv,qw,nv,nw absent. The complete original degree-five h link
   `(p,q,L,R,n)` then proves hv,hw absent: an h neighbour at L next to q
   would force qv/qw, and one at R next to n would force nv/nw.
2. Since ph is an original edge whereas pv,pw are absent, h is **distinct**
   from v,w. Its degree five makes h distinct from r of degree six,
   s,t of degree at least six, and x,y of degree four. Thus h is none of
   the six vertices in the exact original r neighbourhood
   `(x,y,t,w,v,s)` from [J-source geometry, section 1](frozen/audits/2026-10-15-j-source-geometry-6ddea32/PROOF.md).
   Therefore hr is an original nonedge as well.
3. The four vertices n,R,L,q are all original h neighbours. Consequently
   none can equal **any** of r,s,t,v,w. For example n=t would contradict
   ht absent, L=s would contradict hs absent, and R=r would contradict
   hr absent. This uses actual edges and original names, not independently
   normalized interfaces.
4. The original C8 already makes a,n,R,L,q,c distinct. The four vertices
   s,v,w,t are distinct in r's original link and are all interior original
   vertices, hence distinct from original outer vertices a,c. Combining
   these facts gives all ten distinct vertices of D.

No original coincidence is silently resolved by creating a new point.

The following **eight original facial triangles** are in E:

```
xyr, ytr, twr, wvr, vsr, sxr, xsc, yat.
```

They form one disk cap with simple boundary `(a,y,x,c,s,v,w,t)`, containing
exactly the original r in its interior and having original x,y on its boundary.
Its intersection with the boundary of E is exactly the connected arc a-y-x-c;
s,t,v,w are not other E-boundary contacts. Removing r,x,y and those facial
sectors therefore leaves the genuine closed disk

```
D=(a,n,R,L,q,c,s,v,w,t).                               (1)
```

This is a **simple original boundary**, and is not asserted induced. Any
original chords, private vertices and attachments remain in D. In particular
we do not fill its cells or bound its number of interior vertices. The original
s,t degree assumptions remain part of the source; their D degrees are exactly
d_G(s)−2 and d_G(t)−2, respectively, hence at least four. The original v,w each
lose only r. No extra neighbours of any of these vertices are suppressed.

For a fixed literal proper D word d, let F_D(d) be **all complete colourings of
this same actual D** with that word, including an empty set. Let d(d)=|F_D(d)|.
Canonical indexing of proper C10 words uses one common S4 action on a complete
colouring. There are 2461 such words; a word violating an original D chord has
an empty actual fibre automatically.

The complete rxy cap relation, for d=(a,n,R,L,q,c,s,v,w,t), is

```
x != y,c,s,r; y != a,t,r;
r outside {x,y,s,v,w,t};
c-s-v-w-t-a is proper.
```

The cap contains no other vertex. Consequently, for every literal E word e,
restriction and union give a true complete-fibre disjoint union over all literal
s,v,w,t and **every** legal r lift. No r completion is selected or discarded.
All original private colouring in D is shared by every cap lift in that fibre.

The checker retains all 274×256=70,144 E-word/tail fibres, including 67,593
empty ones, and reconstructs a sparse nonnegative integer kernel K with

```
z_E=K d_D.                                            (2)
```

The predecessor's full 10-row matrices are retained unchanged, so simultaneously

```
N(G)=M_G K d_D, N(T0)=M_T0 K d_D, N(T1)=M_T1 K d_D.      (3)
```

All three complete ten-row products are saved, together with the complete old
p,h lift relation, including its empty fibres. Equations (2)–(3) concern one
actual D, E and G; they do not glue independently feasible exterior pieces.

## 2. All r,x,y lifts reduce the two leaks to six D fibres

Recall the fixed literal E assignments

```
U=z73=z(01023013), V=z76=z(01023031).
```

They have common prefix `(a,n,R,L,q,c)=(0,1,0,2,3,0)`, with `(x,y)=(1,3)` or
`(3,1)` respectively. The inherited actual-source zero set includes

```
z72=z(01023012)=0, z74=z(01023021)=0.                  (4)
```

For the common D prefix enumerate the 256 literal tails s,v,w,t and the complete
64 r,x,y assignments. Exactly 24 tails have any U or V lift. For **18** of them,
the same D colouring has another proper cap lift to one of the zero E words in
(4). Thus the **whole D fibre** must be empty. This argument crucially uses all
rxy lifts: one permitted U/V lift cannot hide a second forbidden lift of the
same complete D colouring.

The remaining six words and their entire cap-lift sets are:

| Name | s,v,w,t | All r,x,y lifts | Contribution |
| --- | --- | --- | --- |
| A1 | 2,1,3,2 | (0,1,3), (0,3,1) | U and V |
| A2 | 2,3,1,2 | (0,1,3), (0,3,1) | U and V |
| CU1 | 3,0,3,1 | (2,1,3) | U |
| CU2 | 3,1,0,1 | (2,1,3) | U |
| CV1 | 1,0,1,3 | (2,3,1) | V |
| CV2 | 1,3,0,3 | (2,3,1) | V |

Use these names also for their actual complete D counts. The exact consequence is

```
U=A1+A2+CU1+CU2,
V=A1+A2+CV1+CV2.                                      (5)
```

Every summand is a count of a fixed full literal D fibre of the same original
D. The six rows are not six graphs or six asserted realizations. Nothing in
(5) asserts a simultaneous solution of any necessary support model.

The predecessor gives U+V>0 for the original globally minimum source. Hence

```
2(A1+A2)+CU1+CU2+CV1+CV2>0.                           (6)
```

This is a concrete source positive branch. If all six actual D fibres were
proved empty, U=V=0 would follow, and the predecessor's two fixed legal k−2
completions would both be smaller bad graphs. Those zero statements are not
proved here. Minimality, a conditional smaller-bad statement, and the unresolved
fibre emptiness remain separate authorities.

## 3. Actual D components and a finite all-subset lemma

Fix one complete D colouring in any of the six rows. Its actual 02 and 13
components induce a noncrossing partition of the **ordered** D contacts.
Each block is monochromatic in its palette; consecutive boundary contacts in
one palette are in the same component by their original rim edge. Different
component blocks cannot alternate around a disk. Components not meeting D's
boundary remain in the graph and may be left fixed.

Keep this one actual partition and switch any subset of its complete actual
components. Every resulting literal boundary word has a positive complete D
fibre. If any proper rxy cap lift of that resulting word reaches an inherited
zero E fibre, the starting complete D colouring cannot exist. This is a
universal statement about one colouring's whole orbit, rather than selecting
a different component witness at successive steps.

The bounded finite lemma checks precisely these six rows, at the **single
complementary split 02|13**. It includes all compatible partitions and all
literal subset outputs. Each rejected partition has a recorded full D subset
switch followed by a complete rxy lift to an inherited zero E word. Only the
original 83 inherited Kempe-zero E coordinates are used; there is no new planar
count cone, LP, full support search, or source graph enumeration.

| D row | Compatible NC partitions | Not rejected by this test |
| --- | ---: | ---: |
| A1,A2 | 12 each | 3 each |
| CU1,CU2 | 55 each | 5 each |
| CV1,CV2 | 55 each | 6 each |

An actual source partition must be among those not rejected. The converse is
not asserted. The checker and independent reconstruction derive the following
structural consequences from **every** partition left in the stated row.

For any private C row, s and t are in **different complete D13 components**.
Let these be S and T. In a CU row, n,q are in one D13 component N, which is
either S, T, or disjoint from both. In a CV row the same three possibilities
exist, together with exactly one additional attachment type:

```
n in T, q in S, with their D13 components distinct.    (7)
```

The reversed crossed assignment n in S, q in T is excluded by the same finite
lemma. These statements preserve arbitrary private vertices and rootless
components. They do not say the actual components are just their boundary
contacts.

## 4. The original s–x–y–t path is three bridges

In every C row, r=2, a=c=0, and s,t have opposite colours 1,3. The original
complete x,y neighbourhoods imply

```
N_E13(x)={s,y}, N_E13(y)={x,t}.
```

Since S and T are distinct in D13, the complete E13 component through x,y is
exactly

```
S — x — y — T,                                       (8)
```

where each of S,T includes all of its actual private attachments. Each of the
three original edges sx,xy,yt is therefore a bridge of this complete E13
component. No alternative D13 s–t path exists. Internal cycles inside S or T
and arbitrary other rootless components are retained.

This is a source consequence, not a property of an abstract boundary partition
being called realized. It isolates the only way the private leakage can use the
original r6 boundary cap.

## 5. Two genuine complete-colouring bijections

**The common A subfibres.** In either A row r=0 and s=t=2. The complete original
x,y neighbourhoods show that the actual E13 component through x,y is exactly
`{x,y}`. Its switch exchanges `(x,y)=(1,3)` with `(3,1)`, while fixing **every
vertex of D and its complete private colouring**. This is an involutive
bijection between the U and V subfibres indexed by that same A word.

**The free private C subfibres.** Call a C colouring free if neither n nor q
belongs to S or T. Switch the one complete E13 component (8), including every
private vertex of S,T. The fixed D prefix remains `(0,1,0,2,3,0)`, because n,q
are outside the switched component. The literal tails transform as

```
CU1 <-> CV1, CU2 <-> CV2.
```

The actual D graph is unchanged; its colouring is changed exactly on the two
complete components S,T. All other D components, including rootless ones, stay
fixed. Palette-induced edges and components are unchanged by a complete Kempe
switch, so the free premise is preserved and the reverse is the same switch.
This is a full-colouring bijection, not equality of separately feasible local
counts. It proves equality of the free CU_i and CV_i counts.

In particular either a positive A fibre or a positive free private C subfibre
forces **both U and V positive**. Thus unilateral leakage is restricted further:

- If U>0 and V=0, some private CU row is positive, r=2, exactly one of v,w is
  zero, and the common n,q D13 component attaches to S or to T.
- If V>0 and U=0, some private CV row is positive with the same r/zero condition;
  n,q either attach together to S or T, or have the crossed attachment (7).

Together with (6), the next actual source question is restricted to paired
positive A/free-C subfibres or this attached private bridge. A boundary-only
switch, a separate palette witness, or an independently feasible D row cannot
supply the missing source proof.

## 6. Checks and authority boundaries

[check.py](check.py) reconstructs the generic full cap kernel, every relevant
empty/full fibre, the six exact count terms, all 244 compatible NC partitions
and their full subset outputs, and the complete ten-row projections (3).
Certificate generation is exclusive create; ordinary replay is read-only.

[independent.py](independent.py) does not import the producer. It uses the
missing-neighbour-colour formula for r and separately enumerates partitions of
the 02 and 13 contact sets before checking noncrossing. Its entire generic
kernel and all component-survivor lists agree. Six actual disk controls add
private pendant trees at s,t and a rootless 13 component. Their full vertex
assignments and actual whole-component switches verify both bijections;
private vertices move where required and the rootless component remains fixed.
Those controls are **not complete original minimum r6/933 sources**; that source
control is `not triggered`.

All results are conditional source structure with exact finite evidence. Neither
the six fibres nor the surviving partition data are asserted realizable. Their
emptiness, general 933 exclusion, an actual smaller bad graph, K-infinity and
Lean remain OPEN. The old Q1/Q2/fan-B method remains closed; this round does not
reopen it or upgrade the other twelve completions to full-support no-gos.
