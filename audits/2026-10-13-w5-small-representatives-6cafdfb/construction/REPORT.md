# Free-W5 insertion and actual small annulus representatives

This is an elementary construction on the frozen catalogue, not a claim that
an unknown catalogue-outside minimum source has already been replaced.
All pins have fixed literal names `B=(0,1,2,3,4)` and `U=(5,6,7,8,9)`.
The private vertices in a target are `10,...,9+k`, and its restored center is
`10+k`. Every face, edge, rotation and complete colouring assignment is kept
in `certificate.json.gz`; all 1,024 U cells, including empty fibres, occur in
every one of the ten ordered B rows.

## 1. Plane construction

Let H be a finite simple connected plane disk graph with the indicated outer
face B, and assume B is induced. Let p be its number of private interior
vertices. Choose any bounded face F incident with b0 and its occurrence of b0.
Put a disjoint ordered five-cycle U in the interior of F and add a bridge
b0u0 entirely inside F. There is no other connection between H and U.
Call the resulting annulus A(H). Its private vertices are exactly H's p
interior vertices. Both B and U are induced, and U is an empty inner face.
Restore v in that face with exactly the five spokes vu_i to obtain G(H).

For a directed boundary walk F=(...,b0,x,...), the insertion replaces that
occurrence by

    (...,b0,u0,u4,u3,u2,u1,u0,b0,x,...)

and adds the new inner face `(u0,u1,u2,u3,u4)`. Thus both directions of the
bridge occur on the same remaining face; this is an ordinary legitimate
plane bridge, not a crossing or an unidentified attachment. Capping removes
the U face and inserts the five directed triangular faces `(v,u_i,u_{i+1})`.
The outer face and all original H darts are unchanged. The certificate checks
each dart exactly once, one cyclic rotation at each vertex, connectedness and
Euler characteristic two. Repeated vertices on the bridge face are allowed;
2-connectedness and triangular annular faces are not part of this target
contract. If a stronger target class disallows bridges, this construction
does not establish membership in that class.

The constructed ring has the same orientation and named cyclic order as the
specified empty U interface. It may be placed in the given annular region
by deforming its embedding while keeping the two ordered boundary components
aligned. No original U labels are identified with H vertices.

## 2. Exact complete relation proof

Fix a literal boundary assignment beta. Restriction from a complete G(H)
colouring to H proves `Sigma(G(H)) subset Sigma(H)`. Conversely let eta be
any complete H colouring. Choose a proper three-colouring tau of U with
`tau_0 != eta(b0)`, and colour v with the unique fourth colour. Such a tau
always exists: for example start with the proper three-colour tuple
`(0,1,0,1,2)` and apply one common permutation of the four colours so that
the colour of u0 differs from eta(b0). This extends eta across the only
attachment edge and every W5 edge. Consequently

    Sigma(G(H)) = Sigma(H),       private(A(H)) = p.

This equality is the whole ordered B relation, not a cardinality statement.
For each fixed beta and tau the complete annulus fibre is exactly

    J_A(H)(beta,tau)
       = { eta union tau : eta in C_H(beta) }

when tau is proper and `tau_0 != beta_0`, and is empty otherwise. The capped
fibre appends the unique missing centre colour exactly when tau uses three
colours. The original full H lift, rather than separately chosen marginals,
is used in each union. Thus the certificate includes every complete assignment
and supplies explicit restriction and extension maps. It does not infer
equality of numbers of colourings between H and G(H): each complete H lift
has 90 capped extensions, and 180 uncapped extensions.

For an original annulus A whose capped outer relation equals Sigma(H), the
construction A(H) is a legal target for preservation of complete capped
Sigma. A two-way total relation on full capped colourings can match each
beta-fibre with itself: take the Cartesian product of its complete source
and target fibres, or select a deterministic full target lift in that fibre.
It preserves B, not necessarily U, centre colour or private assignments.
Those stronger conditions are deliberately not part of this theorem.

## 3. The 102 actual catalogue targets

The frozen `cells.json` has 132 masks with at-most-five-interior-vertex disk
witnesses. Of the stored witnesses, 102 have no edge between nonadjacent B
vertices; 30 have one or two B chords. For every one of the 102 chordless
witnesses the checker constructs the entire actual A(H) and G(H) above,
including a plane embedding. It obtains the stored complete mask again by
independent direct full-graph DFS, and compares every complete fibre with
the explicit H-times-U formula. The distribution of target private counts is

| p | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| target masks | 1 | 6 | 20 | 30 | 25 | 20 |

Hence every recognized induced-B catalogue relation has an actual target
with `r'=p<=5`, and its capped graph has at most `6+p<=11` interior vertices.
In particular these targets meet the weaker requested `r'<=9` bound. No
source degree, near-triangulation or edge-minimality condition is imposed on
these derived targets.

Here is the precise justification for the word “every recognized”. It uses
the Four Colour Theorem, in addition to the finite catalogue control. If a
finite plane disk source D has induced outer B, any nonadjacent pair a,b in
B can be identified by an arc in the exterior face. The quotient is planar
and loopless (parallel edges may be suppressed), since ab was not an edge.
A four-colouring of the quotient lifts to a complete D colouring with a=b.
Thus Sigma(D) contains a colouring equating every prescribed nonadjacent
pair in turn. A witness H with a B chord ab rejects every colouring with
a=b, so it cannot have `Sigma(H)=Sigma(D)`. Therefore when `Sigma(D)` is in
K132, its stored witness must be one of these 102 chordless witnesses.
This argument does not delete a chord or replace it by an illegal equality
gadget; a chorded witness simply cannot be equivalent to an induced-B source.
The imported Four Colour Theorem retains its own existing trust boundary;
this audit adds no proof or formalization of it.

## 4. A new strictly shrinking family that preserves only Sigma

Instead of the bridge b0u0, place a simple path of any length L>=2 between
b0 and u0 inside the same face, with L-1 new private vertices. The wheel is
otherwise as above. Denote its annulus by A_L(H). Its restored graph has

    r = p+(L-1),           k = 6+p+(L-1).

Restriction again gives `Sigma(G_L(H)) subset Sigma(H)`. Every complete H
colouring extends to a three-coloured U and its center, and a path with
four available colours can be coloured between any prescribed endpoint
colours. For length two choose the middle colour outside the two endpoint
colours; for larger lengths colour all but the last private point in order,
then choose its colour outside the preceding and final endpoint colours.
So `Sigma(G_L(H))=Sigma(H)=Sigma(G(H))`. Replacing the path with the direct
bridge strictly reduces r to p. The path lies wholly on the outer side of U,
so the named U face and its empty cap slot remain legitimate.

This operation need not preserve R3. For L=2, every proper three-colour U
tuple is feasible over every nonempty complete H beta-fibre, including
tau_0=beta_0; the bridge target rejects all such equal-endpoint tuples.
Thus this is a concrete class where the weakest Sigma contract permits
strict shortening that the R3 contract would forbid.

Two complete finite controls use L=2:

| complete mask | source r | target r' | source capped interior k | target k' | R3 cells changed |
|---|---|---|---|---|---|
| 1023 | 1 | 0 | 7 | 6 | 300 |
| 127 | 6 | 5 | 12 | 11 | 210 |

The arbitrary-length paper construction also provides sources exceeding the
K15 threshold: for example the actual k_eff=5 mask-127 witness with L=6
gives `r=10,k=16`, and its bridge target gives `r'=5,k'=11`. This particular
long-path example is justified by the path extension proof, not claimed as
an additional exhaustively enumerated full-fibre control. All these sources
contain degree-two path vertices and fail the true minimum-source hypotheses.
For those hypotheses the result is `not triggered`.

## 5. Exact residual and conditional equivalence

For the class of connected induced-B plane disk graphs and induced-B/U plane
annuli allowing the legitimate bridge faces above, assume the accepted
`K_{<=15}=K132` theorem. Then the following are equivalent:

1. Every such annulus has a legal same-named-boundary replacement with
   `r'<=9` preserving the full capped outer Sigma.
2. Every such annulus's capped relation belongs to K132.
3. Every connected induced-B plane disk graph's full relation belongs to
   K132.
4. Every such annulus has a legal replacement with `r'<=5` preserving the
   full capped outer Sigma.

Indeed 1=>2 follows by adding the five U vertices and centre to the target:
`6+r'<=15`. Each capped annulus is itself an induced-B disk, giving 3=>2.
Conversely the free-W5 construction embeds any connected induced-B disk H
in this annulus class without changing its full outer relation, so 2=>3.
For 2=>4, apply the catalogue recognition lemma in section 3 and the actual
at-most-five-private-vertex construction. Finally 4=>1 is immediate.

This is a reduction of the remaining universal existence obligation, not a
proof of any of the four statements. An unknown catalogue-outside source
still has no recognized witness to feed into the construction. In particular
no replacement for an actual globally minimum 933/941 source has been
constructed. The universal nine-point representative claim and the induced-B
catalogue completeness claim remain OPEN. No assertion is made here about
other boundary classes or stronger targets forbidding bridge faces.

## 6. Finite evidence

The primary checker retains 1,044,480 target annulus cells, 1,545 complete
H lifts, 278,100 complete annulus lifts and 139,050 complete capped lifts.
The two strict-shrink controls additionally retain their full annulus and
capped fibres. All exact comparisons use the same literal colour names;
the same global S4 permutation transports a complete row to any literal
proper B tuple. U is never normalized independently.

Run the primary read-only replay with:

```bash
uv run --with networkx==3.5 python -B audits/2026-10-13-w5-small-representatives-6cafdfb/construction/check.py --check
```

`--write` opens certificate outputs exclusively and was used only for initial
creation. NetworkX 3.5 supplies a candidate embedding of the coned witness;
the produced directed faces and rotations are then explicitly checked. These
finite controls do not verify NetworkX universally, do not prove the Four
Colour Theorem, do not establish a truly minimal source exists, and add no
Lean theorem. The all-size insertion/path proofs are elementary paper
arguments separate from the finite catalogue controls.
