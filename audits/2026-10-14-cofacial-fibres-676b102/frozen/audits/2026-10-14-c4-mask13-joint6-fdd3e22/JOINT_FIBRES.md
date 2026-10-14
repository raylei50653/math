# C4-MASK13-JOINT6: the previously free ABCB fibres

This is a conditional paper lemma, proved by switches of actual maximal
two-colour components in one complete colouring and the Jordan separation
property of a disk. It uses no Four Colour Theorem, enumeration assumption,
or general assertion that a Kempe graph is connected. The final exclusion of
the source remains OPEN.

## 1. Literal input and the failure hypothesis

Use the graph R and the six original vertices from
[the frozen adjacent-four reduction](frozen/audits/2026-10-14-c4-triangle-core-b66f592/ADJACENT4.md).
R is a plane disk with induced outer cycle Q=(z,s,r,t); p and q are distinct
strictly internal vertices, and zpq is a facial triangle. All six vertices,
all their original attachments, and the actual embedding remain fixed.

The lemma below only needs the disk embedding, the four boundary edges,
and the edges zp,zq,pq. Faciality, triangulation, degree bounds, and source
minimality justify the input R but are not extra steps in this lemma.

Write F(W) for **all complete proper R colourings** with the literal fixed
boundary word W in the common colour frame (A,B,C,D). Assume the retained
failure hypothesis:

1. R has exactly outer mask 13: F(ABAB), F(ABCB), and F(ABCD) are nonempty,
   while F(ABAC) is empty.
2. Every f in F(ABAB) has the unordered pq palette {C,D}.
3. Every f in F(ABCD) has the unordered pq palette {B,D}.

For a colouring f, let K_f(v;ij) be the **maximal** component containing v
in the subgraph induced by the two colours i,j. Switching that component
means interchanging i,j at every one of its vertices. This is an involution
on complete proper colourings. The component has the same vertex set after
its switch, which is what will prove the exact inverse statements below.

The planar fact used throughout is the following. An AC path from z to r
and a BD path from s to t cannot both occur: their endpoints alternate on
the outer Jordan cycle, whereas their colour sets make the paths
vertex-disjoint. We only use paths on the **original four-point outer
boundary**. In particular we do not replace the internal triangle by a
fictitious six-point Jordan boundary.

## 2. Component constraints in ABAB and ABCD

Fix f in F(ABAB). The vertices s,t belong to one BC component: otherwise
switching K_f(t;BC) would give the forbidden boundary ABAC. The same
argument with BD, followed by the single common colour renaming D to C
and C to D, puts s,t in one BD component. Consequently z,r are disconnected
in AC and also in AD, by the complementary-path planar fact.

If p=C and q=D, the BC component containing s,t also contains p. Otherwise
switching the BC component of p would fix all four boundary vertices and
give pq palette {B,D} in ABAB, contradicting hypothesis 2. Similarly the
BD component containing s,t also contains q. For the opposite pq
orientation interchange p and q in these statements. Thus the following
are same-colouring conditions, not separate existential paths:

    s ~BC t ~BC (the C-coloured endpoint of pq),
    s ~BD t ~BD (the D-coloured endpoint of pq),
    z !~AC r,   z !~AD r.

Fix instead f in F(ABCD). The vertices z,r are in one AC component:
otherwise switching K_f(r;AC) would give the forbidden boundary ABAD,
which is the ABAC state under the common C,D interchange. Hence s,t are
disconnected in BD. These statements hold for each full lift separately.

## 3. The missing colour is compulsory in ABCB

Fix f in F(ABCB). Since zpq is a triangle and z=A, the three possible pq
palettes are {B,C}, {B,D}, {C,D}.

Suppose first that pq has palette {B,C}. If z,r were disconnected in AC,
switch K_f(r;AC). The C-coloured endpoint of pq is adjacent to z, and
therefore belongs to the AC component of z; it is not switched. The
B-coloured endpoint is not switched either. The result would be an ABAB
full lift retaining pq={B,C}, contrary to hypothesis 2. Thus z and r are
connected in AC.

If s,t were disconnected in BD, switch K_f(t;BD). This would give ABCD.
The C-coloured endpoint of pq is unaffected, so its palette could not be
{B,D}, contrary to hypothesis 3. Thus s,t are connected in BD as well.
The two complementary paths contradict the alternating-endpoint planar
fact. Therefore pq={B,C} is impossible.

We have proved the new six-point constraint:

> In every ABCB complete lift, one of p,q has the missing colour D.

There is a further exact split.

- If pq={C,D}, then s,t must be connected in BD: otherwise the same
  t-component switch would give ABCD still using C on pq. Hence z,r are
  disconnected in AC.
- If pq={B,D}, then z,r must be connected in AC: otherwise an r-component
  switch would give ABAB with its unchanged palette {B,D}. Hence s,t are
  disconnected in BD.

Thus the two palette sectors of ABCB have opposite, forced complementary
connection patterns. No internal triangle was moved, and no two different
colourings were combined.

## 4. Exact complete-fibre bijections

Define the disjoint subsets

    X = {f in F(ABCB) : pq has palette {C,D}},
    Y = {f in F(ABCB) : pq has palette {B,D}}.

Section 3 proves F(ABCB)=X disjoint-union Y.

### ABAB to the CD sector

For each f in F(ABAB), switch K_f(r;AC). Section 2 puts z outside this
component; s,t have colour B and are outside as well. The new boundary is
exactly ABCB. The C-coloured endpoint of pq is in the AC component of z,
and the D-coloured endpoint is outside the two-colour subgraph. Both p
and q therefore keep their **individual** colours. The image lies in X.

For any g in X, Section 3 disconnects z,r in AC. Switching K_g(r;AC)
gives ABAB and again fixes p and q individually. The component vertex set
is unchanged by its own switch, so these constructions are exact inverses:

    F(ABAB) <--> X,        f |-> switch K_f(r;AC).

This also restricts to a bijection for each ordered pq assignment (C,D)
or (D,C). Moreover both ordered assignments occur in F(ABAB): switch its
CD component containing the edge pq, which avoids the A/B boundary.
Therefore both ordered assignments occur in X too.

### ABCD to the BD sector

For each f in F(ABCD), switch K_f(t;BD). Section 2 puts s outside the
component, and z,r have colours A,C. The new boundary is exactly ABCB.
The edge pq puts p and q in one BD component. Consequently this switch
either fixes both or interchanges both their colours; in either case
the unordered palette remains {B,D}. The image lies in Y.

For any g in Y, Section 3 disconnects s,t in BD. Switching K_g(t;BD)
gives ABCD, retains the unordered pq palette, and is the exact inverse:

    F(ABCD) <--> Y,        f |-> switch K_f(t;BD).

There is no claim that this second bijection preserves the ordered pq
assignment. Its actual rule is precise: the order is reversed exactly
when the BD component of t contains the edge pq. We also do not infer
that both pq orders occur in F(ABCD) or in Y.

Since mask 13 supplies nonempty F(ABAB) and F(ABCD), both X and Y are
nonempty. For finite R this yields the count identity

    |F(ABCB)| = |F(ABAB)| + |F(ABCD)|.

The count identity is weaker than the displayed disjoint complete-fibre
bijections. No equality of fibres across different graphs is asserted.

## 5. What the refinement does and does not exclude

The earlier abstract six-pin negative control selected the palette {B,C}
for its ABCB row (its three selected rows were ABAB/CD, ABCB/BC, and
ABCD/BD). Such an abstract relation cannot be the complete joint relation
of a plane R satisfying the failure hypothesis: its ABCB row violates
Section 3. The old control still correctly demonstrated
that the **outer support mask alone** loses internal p,q information.

A refined abstract relation can retain only {C,D} in ABAB, {B,D} in ABCD,
and the two palettes {C,D}/{B,D} in ABCB. This paper lemma does not prove
that this refined relation is realizable, and does not exclude all such
relations. Necessary terminal component partitions are not a construction
of one graph, its maximal Kempe components, or its complete colouring set.

The proof adds a compulsory missing colour, a per-colouring connection
split, and explicit full-fibre transport. It does **not** establish the
desired palette-changing cap lift, exclude mask 13, improve the original
size bound, or finish C4-MASK13-JOINT6. The additional source degree and
small-cycle hypotheses remain available for a later step.
