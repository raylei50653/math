# A. Same-graph full-fibre transport rules out the accepting fan-A route

Date: 2026-10-18. Exclusive audit BASE
`e1617a2756813327d7ad333cfdd0fd92fa9efc38`.

This paper argument uses the frozen previous smaller-source REPORT,
C/PROOF and A/SUPPLEMENT, and the frozen active-f B/PROOF. The original
ordered boundary remains `(x,y,a,b,c)` throughout. Every colouring below
assigns every vertex of one fixed completed graph, in the literal palette
`{0,1,2,3}`. Empty fibres are retained. There is no bounded-exterior or
small-patch enumeration hypothesis.

The main conclusion changes the proposed proof target: **an accepting
fan-A can never reject both `01202` and `01212`**, regardless of its
exterior. Under the original two empty fibres, there is an exact
full-colouring bijection identifying its accepted fibre with the disjoint
union of these two leaked fibres. Thus exterior connectivity cannot
complete the three-rejection proof on an accepting fan-A. Fan-B still has
a separate unresolved acceptance and rejection obligation.

## 1. The same actual candidate at each of the four sites

Use the original two-centre disk with ordered rim
`(A,B,Q,L,R,N)`, original centres `u,h`, and complete centre neighbourhoods

```
N_G(u) = {A,B,Q,N,h},
N_G(h) = {u,Q,L,R,N}.
```

The actual rim cycle and unchanged exterior are retained. Here `B=b` is
the original boundary vertex, not the name of the ordered outer cycle.
The fixed zero-centre fan-A is rooted at A and the fixed fan-B at B.
They are the completed `k-2` candidates of the frozen construction.
The no-go below is restricted to the four original sites in the table,
where the original b has degree four. The previous generic adjacent-five
construction can also be valid at sites without this b-neighbourhood;
no no-go for those more general sites is claimed here.
For a full candidate colouring, the exact old lift gate is

```
{chi(A),chi(B),chi(Q),chi(N)} is not rainbow.
```

It is equivalent to the existence of at least one complete old `(u,h)`
lift with every other original vertex fixed. The entire lift set remains
the one recorded in frozen C/PROOF; no selected witness replaces that
set in this argument.

Write `s` for the original apex surviving the deletion. The literal maps
are:

| Deleted original pair | `(A,B,Q,N)` | `s` | fan-A root |
| --- | --- | --- | --- |
| `p,ell` | `(a,b,q,n_a)` | `q` | `a` |
| `p,n_a` | `(q,b,a,ell)` | `q` | `q` |
| `q,ell_c` | `(c,b,p,n_c)` | `p` | `c` |
| `q,n_c` | `(p,b,c,ell_c)` | `p` | `p` |

At every site, fan-A has the complete neighbourhood

```
N_{G_A}(b) = {a,c,s},
```

and `s` is adjacent to all three of `a,b,c`: the original surviving-apex
edges supply two incidences, and the fan supplies the third. This is a
claim about actual retained or added edges. The original degree-four
neighbourhood of b and the fact that the fan at A adds no b-edge prove
the complete-neighbourhood assertion. In every row with `a=c`, the
generic gate has the same four values as `(a,b,s,N)`.

For a graph H with this original ordered boundary, denote its complete
proper-colouring fibre by `F_z(H)`, with no quotient by colour permutation.
Put

```
alpha = 01232,
rho_0 = 01202,
rho_1 = 01212,
tau   = 01021.
```

The source assumptions used in Sections 3--6 are exactly
`F_rho_0(G)=F_rho_1(G)=empty`, in addition to the actual local geometry.
The main no-go in Section 2 does not even require these original
rejections. No use of the original tau rejection is hidden in it.

## 2. Accepting fan-A already forces a leaked rejected row

Take any `psi in F_alpha(G_A)`. Its original boundary is

```
(x,y,a,b,c) = (0,1,2,3,2).
```

Because s is adjacent to a,b,c, `psi(s)` is either 0 or 1. Let
`t=1-psi(s)`. Recolour only b from 3 to t. This is a proper full
colouring because b's complete neighbours have colours 2 and `1-t`.
Every exterior vertex, every other original vertex, and every graph edge
is unchanged. The resulting outer row is exactly `rho_t`.

Consequently

```
F_alpha(G_A) nonempty
  => F_rho_0(G_A) nonempty or F_rho_1(G_A) nonempty.       (A1)
```

Equivalently, on this fixed candidate,

```
F_rho_0(G_A)=F_rho_1(G_A)=empty => F_alpha(G_A)=empty.
```

This is not a finite zero-hit observation or a claim about independently
chosen rows. It is an explicit map from each entire accepted colouring
to an entire leaked colouring on the same graph. Its only mutation is
at the named original vertex b. Arbitrary exterior Kempe conditions
cannot invalidate this proper recolouring. Therefore **none of the four
fan-A candidates can satisfy the four-query smaller-bad certificate**.

The map is injective into the disjoint union of the two negative fibres:
the target row records t, and restoring b to 3 recovers psi. Thus even
without original rejections,

```
|F_alpha(G_A)| <= |F_rho_0(G_A)| + |F_rho_1(G_A)|.         (A2)
```

## 3. Both original rejections give an exact bijection, not only an injection

Now use the two original empty fibres. The fixed-exterior lift theorem
says every full `rho_t` colouring of G_A has rainbow gate `(a,b,s,N)`.

### 3.1 The fourth-colour apex sectors disappear

In row rho_t, `a=c=2`, `b=t`, and therefore

```
s in {1-t,3}.
```

If `s=3`, the rainbow gate forces `N=1-t`. Recolour b alone from t to
`1-t`. Its neighbours are coloured 2 and 3, so this is proper. The new
row is `rho_(1-t)`, but its gate has `b=N`; hence it has a complete old
lift, contradicting the other original empty fibre. Thus for every full
colouring of either negative row,

```
rho_0:  s=1, N=3;
rho_1:  s=0, N=3.                                      (A3)
```

This checks both palette sectors before eliminating one. In particular
the old possible sectors `(s,N)=(3,1)` and `(3,0)` are now excluded by
actual full-colouring transport, not omitted by palette normalization.

### 3.2 All accepted fan-A colourings have N=3

For any accepted psi, apply Section 2's b-only recolouring with
`t=1-psi(s)`. Its target is in `F_rho_t(G_A)`, and the original rho_t
rejection forces the target gate rainbow. The three gate values at
`a,b,s` are exactly `2,t,1-t`. Hence the fourth is

```
psi(N)=3.                                             (A4)
```

This proves (A4) even for a candidate accepted colouring not initially
known to lift to G. In fact all such colourings now do lift, because
in the accepted row `N=b=3` makes the gate nonrainbow.

### 3.3 The maps and their inverses

Partition the accepted full fibre by its actual s-value. For `t=0,1`,
define

```
Phi_t : {psi in F_alpha(G_A): psi(s)=1-t} -> F_rho_t(G_A)
         by changing b: 3 -> t and nothing else.
```

Section 2 proves this map is proper. By (A3), every target colouring has
neighbour colours `{2,1-t}` at b, so changing b back from t to 3 is
proper and returns a member of the displayed domain. These are literal
inverse maps on the full vertex assignments. Therefore

```
F_alpha(G_A)
  ~= F_rho_0(G_A) disjoint-union F_rho_1(G_A),           (A5)

|F_alpha(G_A)| = |F_rho_0(G_A)| + |F_rho_1(G_A)|.        (A6)
```

All fibres in (A5) include their possible empty case. Every assignment
in all three fibres has `N=3`. The identification fixes every exterior
vertex. This exact same-graph relation is stronger than separate
necessary Kempe contacts, and shows why trying to empty the two negative
fibres while retaining alpha on this candidate cannot succeed.

## 4. Consequence for the original accepted full fibre

In an original alpha colouring, `A,B,Q` are pairwise different, u is
their missing fourth colour, and h belongs to `{A,B}`. The frozen
full-fibre partition identifies its restriction with precisely one
nonrainbow fan colouring, with branch selected by h.

If `h=A`, its restriction is in `F_alpha(G_A)`, so Section 3 forces
`N=B=3`. If `h=B`, the original edges `AN`, `uN`, `hN` forbid A, the
missing fourth colour, and B at N. Thus `N=Q`. Every original accepted
colouring consequently lies in exactly one of the two sectors

```
(h,N) = (A,B)  or  (B,Q).                              (A7)
```

The equality is in colours at the actual labelled vertices; A or Q can
be the surviving apex in the second and fourth sites. It is not an
identification of vertices. For example at `(p,ell)`, the two sectors
are exactly `(ell,n_a)=(2,3)` or `(3,chi(q))`.

For every accepted fan-A colouring, the unique old lift is
`h=chi(A)` and u equal to the fourth colour missing on A,B,Q. For
fan-B, its accepted nonrainbow sector has `N=Q` and unique old lift
`h=3`, with the same missing colour at u. The previous full partition
therefore sharpens to

```
F_alpha(G)
  ~= F_rho_0(G_A)
       disjoint-union F_rho_1(G_A)
       disjoint-union {eta in F_alpha(G_B): eta(N)=eta(Q)}.   (A8)
```

Every arrow means the stated b recolouring plus the unique old-centre
lift or its inverse; all other original vertices are fixed. This is a
single-source full-colouring count identity, not a relation formed by
intersecting two candidate supports.

In particular the old assertion that at least one fan accepts alpha
does not prove that fan-B accepts it: all old witnesses could occupy
the `(h,N)=(A,B)` sector. Conversely, a fan-B accepted witness with
rainbow gate would not come from the old partition. Neither possibility
is silently discarded.

## 5. The exterior Kempe contacts survive the exact transport

Fix one accepted `psi in F_alpha(G_A)` with `psi(s)=1-t`. Put
`chi=Phi_t(psi)`, a specific full rho_t colouring. In both assignments,
b is an isolated vertex of the subgraph induced by colours `{t,3}`:
its complete neighbours have colours 2 and `1-t`. Recolouring b alone
does not change any other component of this induced subgraph.

The frozen forced-contact lemma applied to this very chi therefore
transfers directly to psi:

| Fixed accepted sector | Actual component in that same accepted colouring |
| --- | --- |
| `s=1, N=3` | `C_{03}(N)` contains the original x |
| `s=0, N=3` | `C_{13}(N)` contains the original y |

Here each C is the maximal component in the complete candidate graph,
including its actual exterior. To prove the first line directly,
if `C_{03}(N)` missed x then it would miss every original boundary
vertex of colours 0,3 except isolated b, which is in a different
component. Switching it in chi would preserve rho_0, change N to
b's colour 0, and produce an old lift. The second line is identical
with colours 1,3 and boundary anchor y. Thus these are verified
necessary conditions on whole accepted fibres as well as leaked fibres.

There is also a limited exact cross-sector transport. In psi let K be
the maximal 0/1 component containing s. Since original xy is an edge,
K either contains both x,y or contains neither. If it contains neither,
switching K gives a new full accepted colouring psi' on the same G_A,
with s changed from `1-t` to t and N,b still 3. Applying
`Phi_(1-t)` then gives the other rejected-row fibre. The inverse uses
the same set K (its induced component is unchanged by its switch).
Explicitly the path on full assignments is

```
rho_t --[b:t->3]--> alpha
      --[switch actual C_01(s), disjoint from {x,y}]--> alpha
      --[b:3->1-t]--> rho_(1-t).                        (A9)
```

This gives a bijection between the two negative-fibre subsets for
which the specified intermediate accepted component avoids x,y.
Equivalently, in the leaked colouring chi, b is a leaf of the induced
0/1 graph, with sole neighbour s; its actual maximal component is
exactly `K union {b}`. Switching that single component directly
performs the same rho_t-to-rho_(1-t) transport. This formulation also
retains the entire component, rather than an independently selected path.
It does not cover the boundary-pinned component case. After the
switch, the opposite forced N-anchor condition belongs to psi',
not automatically to psi. No two paths from different colourings
are combined into a planar crossing argument. The actual transported
assignment and its actual component remain part of the statement.

## 6. Sharp residual for the same k-2 candidate program

The fan-A branch is now an arbitrary-exterior no-go for the proposed
four-row certificate. It is not merely still missing a Kempe argument.
Its three rejection fibres cannot all be empty whenever its accepted
fibre is nonempty; rho_0 and rho_1 alone already obstruct that goal.
The original tau fibre and its exterior contacts remain relevant to
fan-B, but cannot repair fan-A's direct b recolouring.

For one fixed fan-B, the unresolved sufficient target is still:

1. produce an actual full alpha colouring of that same fan-B;
2. exclude each complete rainbow fibre for tau, rho_0, rho_1 there,
   using its actual exterior and its actual maximal Kempe components.

The old source gives item 1 if some accepted original witness has
`h=B`; (A7)--(A8) do not establish such a witness. The fan-B adds
incidences at b, so the b-only recolouring used here is unavailable
there. No assertion of all three fan-B exclusions is proved.

These paper results preserve the actual graph, attachments, original
row labels, all palette sectors, and every full-colouring quantifier.
They require no new local patch search, four-colour theorem, matching
assumption, source realizability claim, or Lean theorem. A smaller
bad source, unconditional fan-B acceptance, all three fan-B exclusions,
and the general closure remain OPEN.
