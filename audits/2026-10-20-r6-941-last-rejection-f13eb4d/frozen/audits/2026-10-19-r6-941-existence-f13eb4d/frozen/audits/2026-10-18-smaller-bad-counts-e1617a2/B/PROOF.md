# B. Full-colouring injections from the quotient leaks

2026-10-18. BASE `e1617a2756813327d7ad333cfdd0fd92fa9efc38`.
The parent [INPUTS](../INPUTS.json) freezes the preceding uncommitted audit.
All mathematical inputs below are the frozen copies of the preceding
[geometry and quotient proof](../frozen/audits/2026-10-18-smaller-bad-e1617a2/B/PROOF.md)
and [acceptance supplement](../frozen/audits/2026-10-18-smaller-bad-e1617a2/A/SUPPLEMENT.md).
No preceding evidence is edited.

This proves two injections of **complete colourings of the same actual
exterior**, not an implication between independently chosen boundary
relations. They exclude the `01021` quotient fibres for original masks
932/933 and remove the q=3 parts of both other negative fibres for all
three source masks. They do not empty the remaining negative fibres.

## 1. Source, maps, and counts

Keep the original ordered frame `(x,y,a,b,c)`, literal colours 0,1,2,3,
complete source and the verified exterior disk

```
E = G-{b,p,h},  boundary (a,n,R,L,q,c,x,y).
```

All its original edges and all its private vertices are retained. In
particular the original complete b-star is `{a,c,p,q}`. The original
p/h links and the two actual quotient maps are

```
N(p)=(a,b,q,h,n), N(h)=(p,q,L,R,n),
Q1=(G-{p,h})/(n=b,R=q),
Q2=(G-{p,h})/(n=L=b).
```

A quotient colouring pulls back uniquely to its complete E colouring;
b has the colour of n, and every identified vertex has its literal
pulled-back colour. Conversely an E colouring satisfying the appropriate
equalities and the b-neighbour inequalities gives one quotient colouring.
This retains complete fibres including empties.

Write `tau=01021`, `beta=01201`, `rho_i=012i2` for i=0,1, and
`alpha=01232`. Let `N_w(X)` count complete colourings with the **literal**
row w; let `A_b` count original alpha colourings with h=b=3. The subscript
on `A_b` names the original vertex b, not a variable colour.

The main inequalities are

```
N_tau(Q1)+N_tau(Q2) <= N_beta(G),                       (T)
sum over i=0,1 and j=1,2 of N_rho_i(Qj) <= A_b.         (R)
```

(T) requires the original tau fibre empty. (R) requires both original
rho fibres empty. Neither inequality counts colour orbits or forgets
private exterior vertices. The joint inequality (R) uses a recoverable
component-contact bit to distinguish the two original row domains.

The only topological fact used below is the usual disk separation fact:
boundary components of two disjoint colour palettes cannot alternate.
For example a path of one palette joining R to q separates L from a in
the other palette. This is applied within one full colouring at a time.
A Kempe switch means switching the **whole actual E component**, including
all its private vertices. The palette-induced graph and its components
are unchanged by switching one of them, so that switch is an involution.

## 2. Transport of the tau fibre

Assume `F_tau(G)=empty`. The complete old-lift tests force every quotient
tau colouring to have q=3 and exactly the following E boundary:

| candidate | E boundary `(a,n,R,L,q,c,x,y)` |
| --- | --- |
| Q1 | `(0,2,3,0,3,1,0,1)` |
| Q2 | `(0,2,0,2,3,1,0,1)` |

The case q=a=0 has an old lift and hence cannot occur. These are all
possible quotient tau colourings, not a selected subfibre.

### 2.1 First forced switch

The outer arc c-x-y-a is a single `{0,1}` component. In Q1, n and R
are in one `{2,3}` component; in Q2, L and q are in one such component.
If n and q were in the same `{2,3}` component, noncrossing separates
L (Q1) or R (Q2) from the outer `{0,1}` component. Switch that separated
component from 0 to 1 at the indicated pin. The same exterior now admits

```
(b,p,h)=(2,1,0),
```

which is an original complete tau colouring. This is impossible.
Therefore n and q lie in distinct `{2,3}` components.

Switch the actual q-component in `{2,3}`. It touches no other displayed
boundary pin except q for Q1, or L,q for Q2. The result is

| candidate | intermediate E boundary | distinguished Z |
| --- | --- | --- |
| Q1 | `(0,2,3,0,2,1,0,1)` | R |
| Q2 | `(0,2,0,3,2,1,0,1)` | L |

Here Z has colour 3. Let A be the `{0,2}` component containing a,n;
for Q2 it also contains R. The component containing q also contains L
for Q1. The only remaining possible `{0,2}` boundary contact is x.

### 2.2 Second forced switch

Inspect the actual `{1,3}` component of Z.

* If it reaches neither c nor y, switch it. Only Z changes on the
  boundary, from 3 to 1. Restore `(b,p,h)=(3,1,3)`; the original boundary
  is `(0,1,0,3,1)`, globally equal to tau by swapping 2 and 3. This
  contradicts the empty literal tau fibre by colour symmetry.
* If it reaches c but not y, its Z-to-c path separates the q-side
  `{0,2}` component from A and x. Switch that q-component and restore
  `(b,p,h)=(2,3,1)`. This is an original complete literal tau colouring.
* Consequently it must reach y. Its Z-to-y path separates A from q and
  x. Switch A; its boundary contacts are exactly a,n for Q1, or a,n,R
  for Q2. Restore `(b,p,h)=(0,3,1)`.

The final case gives an original complete **literal beta** colouring,
with boundary on E respectively

```
Q1 image: (2,0,3,0,2,1,0,1),
Q2 image: (2,0,2,3,2,1,0,1).                          (I_tau)
```

There is no choice of a path or a component in this map: it first
switches the q-component in `{2,3}`, then the a-component in `{0,2}`.
Paths establish why the required boundary contacts are the only ones;
the map itself uses the entire uniquely named component.

### 2.3 Injectivity, including private vertices

Given a target colouring in the image, delete b,p,h and use its actual
E colouring. Switch its a-component in `{0,2}` and then its q-component
in `{2,3}`. These are the inverses of the two complete switches in reverse
order. The full initial E colouring, including every private vertex,
is recovered, and hence its original quotient colouring is recovered.
The two patterns (I_tau) are disjoint; they also distinguish which
quotient the input came from. Thus this is an injection

```
F_tau(Q1) disjoint-union F_tau(Q2) -> F_beta(G),
```

proving (T). It needs no count normalization and no assertion that every
beta colouring has such an inverse image.

For masks 932 and 933, beta is absent, so **both quotient tau fibres
are empty**. For mask 941, beta is present; (T) bounds a still-possible
leak and does not exclude it.

## 3. Transport of the two rho fibres

Assume the original rho_0 and rho_1 fibres are empty. Fix i in `{0,1}`.
The complete old-lift tests force every quotient rho_i colouring to be

```
Q1 E=(2,i,q,2,q,2,0,1),
Q2 E=(2,i,2,i,q,2,0,1),   q in {1-i,3}.
```

Let delta be the fourth colour outside `{2,i,q}`. Consider the two
palettes `{i,q}` and `{2,delta}`. If n and q belong to the same first
component, its path separates the middle pin L (Q1) or R (Q2) from
both a and c in the second palette. It also separates that pin from
any outer boundary anchor having colour delta. Switch this component,
changing the middle pin from 2 to delta. Restoring

```
(b,p,h)=(i,delta,2)
```

gives a full original rho_i colouring. Thus n and q must be in distinct
`{i,q}` components.

Switch the q-component in `{i,q}`. At the local pins this changes only
q for Q1, or L,q for Q2. It may also change outer anchors in the same
component. The resulting full E colouring always admits

```
(b,p,h)=(delta,q,delta).                              (J)
```

These p,h values are checked against every original local edge, not
just their boundary projection.

### 3.1 The q=3 sector is impossible

If q=3, then delta=1-i. The anchor with colour 1-i is unchanged by the
switch. The anchor with colour i either stays i or becomes 3. In both
cases the restored original b has exactly the unchanged other anchor's
colour, and a=c=2. Therefore (J), after one global palette renaming if
needed, gives original rho_{1-i}, which is forbidden.

Consequently **q=1-i in every surviving rho_i quotient colouring**.
The preceding full-lift table's q=3 possibilities have been removed
using the actual source exterior, not by deleting rows of an abstract
relation.

### 3.2 Complete injection into the accepted h=b sector

Now q=1-i and delta=3. The switch uses `{0,1}`. Since xy is an edge,
x and y lie in the same `{0,1}` component, so either both anchors are
switched or neither is. After the switch and restoration (J), globally
swap 0 and 1 if necessary to return x=0,y=1. This gives a literal
original alpha colouring with h=b=3. Write its q=n colour as t; its
p colour is 1-t, and its E boundary has one of the forms

```
Q1 image: (2,t,1-t,2,t,2,0,1),
Q2 image: (2,t,2,1-t,t,2,0,1),   t in {0,1}.           (I_rho)
```

The complete target also determines the source row i. Let H be 1 if
its actual E q-component in `{0,1}` reaches x (equivalently y), and 0
otherwise. The palette-induced graph is unchanged by the switch and by
the global 0/1 swap, so this component-contact bit has the same value
before and after both operations. Forward normalization swaps 0 and 1
exactly when H=1. Since n is not in the switched q-component, the output
has `t=i XOR H`, hence the source row is recovered as `i=t XOR H`.

From the full original image, restrict to E and compute H. Undo the
global 0/1 swap if H=1, then switch the q-component in `{0,1}`. This
reverses the entire actual switch and recovers all original E colours,
including every private vertex. Restore the quotient b-colour i and
its equality classes. The two image patterns (I_rho) distinguish the
candidate, while the actual component-contact bit distinguishes the
source row. Thus the disjoint union of **all four** negative quotient
fibres injects into the original alpha h=b sector, proving (R).

## 4. A source-level consequence of minimum badness

For original masks 932/933, the accepted h=b sector is nonempty.
Indeed suppose `A_b=0`. By (R), both quotients reject both rho rows;
by (T), both reject tau. Since original alpha is nonempty, its original
witness partition then places every witness in h=a. The previously
proved same-witness Q1/Q2 cover makes at least one fixed quotient accept
alpha. That same quotient rejects all three specified rows, hence has
an outside-K132 certificate and completed size k-4. This contradicts
the source's global minimum badness.

Thus `A_b>0` for these two source masks. This yields actual acceptance
of the fixed fan-B (and of the earlier S quotient) through their exact
same-source accepted-sector maps. It does not establish badness of
fan-B or S, and does not make any negative fibre of them empty. The
argument does not cover mask 941 because its beta fibre is nonempty.

## 5. Exact degree-four count identity

For completeness use the legal intermediate

```
D=(G-p)/(n=b),  k(D)=k-2.
```

Its complete h-link is the four-cycle `(q,L,R,b)`. For any one complete
colouring of D-h, the number of h lifts is

```
4 - |{q,L,R,b}| = 1[q=R] + 1[L=b].                   (D4)
```

A proper C4 uses two, three, or four colours; the right side is respectively
two, one, or zero. Equality q=R gives exactly the corresponding Q1
colouring, while equality L=b gives exactly the Q2 colouring. Counting
over complete D-h colourings with a fixed literal original outer row gives

```
N_w(D)=N_w(Q1)+N_w(Q2)  for every proper outer row w.
```

Both-colour equalities contribute twice, precisely because h then has
two colours. The identity retains all hidden exterior multiplicities;
it is not an inclusion-exclusion identity for supports. It also gives
`support(D)=support(Q1) union support(Q2)`.

## 6. Verification and limit

The independent stdlib [checker](check.py) enumerates **boundary component
partitions**, not local graphs. It checks all 1,430 noncrossing partitions
of eight ordered contacts, retains every compatible actual-edge-forced
partition for each palette split, and checks every old b,p,h lift after
each branch. It finds 3 first-stage and 12 second-stage partitions for
each tau case; each of the eight rho cases has 12 partitions. All 84
proper literal C4 rows satisfy (D4). All local lift sets, including the
initial empty ones, are saved in [certificate.json](certificate.json).

The inverse claim is a paper theorem about complete-component involutions.
Its boundary equalities and inverse palette decisions are replayed by
the checker. The checker does not independently prove the existence of
a source, or assert that every allowed partition has a planar realization.

Negative controls retain crossing-component examples where the transport
fails if planarity is discarded, and the legal old-tau branch which
prevents forcing the beta target if original tau emptiness is omitted.
These are component-algebra controls, not claimed source counterexamples.

```
python3 -B audits/2026-10-18-smaller-bad-counts-e1617a2/B/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-18-smaller-bad-counts-e1617a2/B/check.py
```

No external theorem beyond the already used elementary disk separation
is introduced. No Lean theorem is claimed. The resulting restrictions
and injections apply to arbitrary-size genuine E, but the requested
smaller bad source and general bad-to-success-or-smaller-bad implication
remain OPEN.
