# A: original boundary caps force two-step degree bounds

Frozen BASE: `6c420f3ca77d60952ed76f93dff7449c522715ca`.
The parent [INPUTS.json](../INPUTS.json) supplies the authority and immutable
copies under `../frozen/`. This worker writes only `A/`. This is an independent
arbitrary-size paper audit of the two-step lemmas; no original `v=5` premise
is imposed.

## A1. Contract and conclusion

Fix the same globally minimum-inner-vertex noncatalogue plane C5 disk G,
with the secondary maximum-edge choice, original ordered boundary
`B=(x,y,a,b,c)`, and the adopted no4ct source hypotheses

```
d_G(x)=d_G(y)=d_G(b)=4,    d_G(r)=6.
```

The original edge apexes of `(xy,ya,ab,bc,cx)` are `(r,t,p,q,s)`.
Keep the actual source constructions `U=R-r`, `J=U/(s=t)`, and `m=[s=t]`.
Write `a0=d_G(a)`, `c0=d_G(c)`; all degrees in the conclusions are original
G degrees. The [frozen geometry](../frozen/audits/2026-10-15-j-source-geometry-6ddea32/PROOF.md)
§§1–2 establishes this contract, `a0+c0>=11`, the original rotation
`(x,y,t,w,v,s)` at r, and the fact that neither v nor w contacts B.

**Theorem A.** For every two-edge path in the actual J,

```
p-h-w  => a0<=5,                 q-h-v => c0<=5.
```

The two statements are proved directly in the two original boundary sectors
of this one G. They do not require reflecting its support mask, choosing a
different original frame, or assuming a degree for v or w.

## A2. Original vertex identities and the two exceptional hubs

The geometry §2 records that the J construction changes only the two
original boundary vertices a,c into z and the original s,t into m; all
other retained J vertices are literal original inner vertices. No deleted
collar vertex can be a J path midpoint. A midpoint h is distinct from its
two path endpoints by the definition of a path.

If `h=z`, the first path would require zw and the second would require zv.
Both are absent because w,v have no original B contact and identifying a,c
adds no other incidences. Thus neither path can use z.

If `h=m`, the first path has mp and the second has mq. The original
geometric identities are

```
mp iff a0=4,                    mq iff c0=4.
```

For completeness, these identities follow without the v5 calculation.
The geometry §5 shows that m,z have exactly two common neighbours,
`alpha,beta`; §2 identifies `alpha=p iff a0=4` and
`beta=q iff c0=4`. Both p and q are adjacent to z. The a-fan and c-fan
are disjoint, so p cannot be beta and q cannot be alpha. Hence mp forces
p=alpha, and mq forces q=beta; the reverse implications follow from the
two actual faces on mz. This proves both stated identities and handles
all paths through m.

It remains to consider a midpoint h which is a retained original inner
vertex, distinct from s,t,r and every point of B. Every incidence of h to
p,w or q,v lifts to the corresponding literal original edge.

## A3. The bounded side at a is forced by the exterior boundary

Suppose `p-h-w` has such an original midpoint. Consider the actual original
cycle

```
Q_a=(a,p,h,w,t).
```

Its edges ap and at come from the original apex faces abp and yat; ph and
hw are retained original path edges; wt is an edge of the original r
link. Its five original vertices are distinct. In particular h cannot be
t, which was absorbed into m, and w has no original B contact. Q_a meets
the original exterior boundary only at a, so it is a proper C5 distinct
from B.

The two actual faces yat and abp fix the complete inner fan at a in the
order

```
y, t, ..., p, b.
```

The sector between ap and at containing the rays ay and ab is on the
unbounded side of Q_a: y,b are distinct original exterior-boundary
vertices, and the original external wedge at a lies in that same sector.
Therefore the bounded Q_a sector is precisely the other one, from t to p
through the interior a fan. This is determined in G, not by choosing a
favourable side of a cycle in J.

Every a neighbour except y,b,t,p is consequently on Q_a or strictly inside
its bounded disk. An edge from a beginning in that bounded sector cannot
end outside the disk without crossing Q_a. Among the other Q_a vertices,
w is excluded by the original collar nonedge aw; only h can supply an
additional boundary neighbour. No omitted outside a neighbour is possible:
the facial wedges ayt and apb and the exterior wedge between ab and ay
already occupy the entire complementary rotation sector.

The [frozen no4ct small-cap theorem](../frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md)
§§2–3 applies to every original proper C5, including one touching B.
Its strict comparison is especially transparent here: four vertices of
Q_a are original inner vertices, so the number of strictly enclosed
original vertices is at most `k-4<k`. Its conclusion is that the cap is
empty, or is exactly one W5 centre with all five spokes and no boundary
chord.

There are therefore precisely two cap types to consider.

* **Empty cap.** All additional a neighbours lie among the other Q_a
  vertices. Only h is possible; hence
  `N_G(a) subseteq {y,b,t,p,h}` and `a0<=5`.
* **One W5 centre u.** The no-extra-boundary-chord part of the theorem
  excludes ah. The only a neighbour strictly inside the cap is u. The
  complete original neighbour set is then exactly
  `{y,b,t,p,u}`, so `a0=5`.

This proves the first implication, including all empty-cap triangulations,
possible chord ah, and the single-centre case. Merely using the weaker
statement “at most one interior vertex” would allow an unjustified sixth
neighbour ah together with u; the chord-free W5 conclusion removes it.

## A4. The c proof in the original source

Suppose instead `q-h-v`, with h an original midpoint as in A2. Use

```
Q_c=(c,q,h,v,s).
```

The edges cq,cs come from the original faces bcq,cxs; qh,hv lift literally;
vs lies in the original r link. These are five distinct original vertices,
and Q_c meets B only at c. At c the original inner fan is

```
x, s, ..., q, b.
```

The arc containing x,b and the external wedge is outside Q_c, so its
bounded sector contains the entire original fan from s to q. Every c
neighbour except x,b,s,q is on or strictly inside this cap. Since cv is
an original nonedge, only h can be one further boundary neighbour.

For an empty cap, `N_G(c) subseteq {x,b,s,q,h}`, giving `c0<=5`.
For a nonempty cap the small-cap theorem supplies the unique W5 centre u
and forbids the boundary chord ch, giving exactly
`N_G(c)={x,b,s,q,u}` and `c0=5`.

Together with the exceptional cases in A2, this proves the second
implication in the same original G. No reflected-source admission or
transport of a colouring theorem is involved.

## A5. Immediate arbitrary-size uses and limits

If a simple marked six-cycle has the connector pairing

```
v-h1-q,   w-h2-p,
```

the two paths give `c0<=5` and `a0<=5`, contradicting the frozen
`a0+c0>=11`. This works with either original midpoint and with a midpoint
m; simplicity already prevents two occurrences of m. In particular, the
formerly retained `v-m-q-p-h-w` case has c0=4, a0>=7 and contains p-h-w,
contradicting Theorem A.

This worker does not by itself exclude the other connector pairing
`v-h1-p, w-h2-q`: that requires the actual disk argument and the further
p/q cap analysis. The low-p/q theorem is not needed anywhere in A1–A4;
its authority is read only for the separate full-six-cycle integration.
The [frozen low-p/q proof](../frozen/audits/2026-10-14-lowpq-source-676b102/pq/PROOF.md)
establishes the original implications `p=5=>a>=6`, `q=5=>c>=6` but is
not silently used to infer a0 or c0 here.

This is a paper consequence of the existing complete original source
contract. No finite target source is supplied, no complete colouring is
assembled from separate witnesses, and no fibre or source mask is
altered. A finite calibration is provided solely for the empty/W5 local
cap arithmetic and the need for the W5 no-chord conclusion. It does not
prove the arbitrary-size sector location or source coverage. No new Lean
theorem, external enumeration, commit, or push is claimed.

## A6. Calibration and custody receipt

`python3 -B A/check.py` from the audit root verifies all 21 frozen input
hashes and independently enumerates all five triangulations of the empty
pentagon. With the sole calibration restriction aw absent (respectively
cv absent), three remain and the boundary degree after adding the two
fixed outside neighbours is at most five. This deliberately allows some
diagonals forbidden elsewhere in the full source: it calibrates a larger
family and uses no extra hypothesis to obtain the bound. The W5 case
has exactly ten edges by the disk Euler formula and gives full boundary
degree five.

Normal and `PYTHONHASHSEED=17` outputs are byte-identical. Two deliberately
invalid controls are rejected: dropping aw/cv allows degree six, and
adding ah/ch to W5 violates the exact cap Euler count. Commands, exit codes
and log hashes are recorded in [VERIFICATION.json](VERIFICATION.json).
Frozen-input drift is zero. No code for arbitrary-size source geometry is
claimed; the bounded-side and complete-neighbour arguments are A3–A4.
