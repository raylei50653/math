# A. Original hexagon construction: exact gate and local obstruction

BASE `9f1fe84f73aabfa87a33d28754633bae6bf0b707`; 2026-10-18.
This is independent work on the actual original two-star patch, not on its
five-contact quotient. The source authority is
`audits/2026-10-17-r6-active-f-seven-ffea555/B/PROOF.md`, sections 1–3;
the root INPUTS records the frozen inputs. No claim is made that every remaining
source has this patch, or that the constructed smaller graph retains badness.

## 1. The original patch and two completed smaller graphs

In the p-centred, h=ell case the original facial links are

```
N_G(p) = (a,b,q,h,n),       N_G(h) = (p,q,u1,u2,n).
```

Their two closed stars form the original disk with ordered boundary
`L=(a,b,q,u1,u2,n)` and exactly two interior vertices p,h. Its boundary cycle
and all exterior attachments are retained. The original C5 boundary remains
`B=(x,y,a,b,c)`. In particular qb and qc are actual retained edges.

The two explicit candidates are:

* H_a: remove p,h and their incident edges; add aq, au1, au2 in the vacated disk.
* H_b: remove p,h and their incident edges; add bu1, bu2, bn in that same disk.

Each added set is a hexagon fan, so it has a fixed planar realization. Existing
copies of an added edge may be simplified; no boundary pin is identified and
no hidden exterior edge is removed. The completion ledger is exactly
`k(H_a)=k(H_b)=k(G)-2`: no quotient hubs need reconstructing and no new vertex
is inserted. This is a literal operation on G, not a cost claim about J.

**Accepted-witness pair cover (independent review of C).** Every complete
original 01232 colouring is retained by at least one of these two graphs.
Indeed a=c=2, b=3. The edges bq,cq force q in {0,1}; the original p is the
other colour in {0,1}. Since h is adjacent to p,q, h is either 2 or 3.
If h=2=a, its original neighbours q,u1,u2,n all differ from a, so the added
edges of H_a are proper in the same original colouring after deleting p,h.
If h=3=b, its neighbours give all added edges of H_b. This uses one full
original colouring and never combines two unrelated lifts.

Thus at least one actual legal completed smaller disk accepts 01232.
This constructive conclusion does not yet say it is outside K132.

## 2. The exact inverse gate

For a proper colouring t of either candidate, define

`D(t) = { colour(a), colour(b), colour(q), colour(n) }`.

Then t extends, with its entire exterior and all six contacts fixed, to the
original p,h patch if and only if `|D(t)| <= 3`.

Necessity follows from the four actual neighbours a,b,q,n of p. For sufficiency
choose a missing colour for p. In H_a put h=colour(a); the fan and rim make
h different from q,u1,u2,n, and the chosen p differs from a. In H_b instead
put h=colour(b); its fan and qb give all required inequalities. These are
explicit complete lifts, with no exterior recolouring.

Consequently, for a row rejected by original G, every full colouring of either
candidate must make the quartet a,b,q,n rainbow. This is the precise remaining
condition: acceptance of a candidate and absence of all such rainbow full
lifts must hold on that same candidate.

A tempting repair is to add a single gate vertex adjacent to a,b,q,n. It would
test the condition and still save one vertex. It cannot be placed across the
fan sectors while retaining all the fan edges. The finite family below includes
every one-centre triangulated hexagon and finds no nonempty locally sound repair.

## 3. Literal forbidden-row controls

Keep only the exact boundary row, the complete rim, and the retained exterior
edge qc. These conditions do not rule out rainbow leaks. For H_a:

| original B row | original extendable rim tuples | fan tuples | retained | leaks |
| --- | ---: | ---: | ---: | ---: |
| 01232 | 14 | 16 | 10 | 6 |
| 01021 | 18 | 8 | 5 | 3 |
| 01202 | 14 | 16 | 10 | 6 |
| 01212 | 14 | 16 | 10 | 6 |

Concrete leaks in rim order (a,b,q,u1,u2,n) are respectively
`(0,2,3,1,2,1)`, `(2,0,1,0,1,3)`, `(2,1,0,1,0,3)` for the three
rejected rows. They satisfy every displayed edge, but p sees all four colours.
These are **partial-interface controls**, not claimed full exterior lifts of
the hypothetical minimum source. The exact complete exterior could forbid
them; its excluding all such tuples is still to be proved.

## 4. Two rejected contexts already require full local containment

Let Q be any ordinary colour-symmetric replacement touching the exterior only
at the six named L contacts. Suppose one tries to establish rejection safety
using only the row on B, the rim edges, and qc. Then soundness for 01021 and
01202 alone implies the stronger local condition `R_Q subseteq R_P`.

To prove this, take any proper rim tuple t of Q. If q=a, globally rename colours
so a=0,b=2, and assign c=1. Then t lies in the 01021 partial context and qc is
proper. If q differs from a (and also from b by qb), globally rename a=2,b=0,
q=1 and set c=a=2. Then it lies in the 01202 partial context. An original patch
lift after this renaming pulls back to a lift of t. This is a single common
S4 renaming of all contacts; no independent normalization of different fibres
is used. Since every proper rim tuple is in one case, local containment follows.

Therefore the four-row abstraction cannot weaken local containment when the
only available exterior information is B and qc. An actual improvement has to
use more of the **same** exterior relation. This does not say that the complete
exterior fails to provide such information.

## 5. Replayed finite operation families

[check_hexagon_obstruction.py](check_hexagon_obstruction.py) enumerates all 732
literal proper C6 tuples and retains every complete (p,h) fibre, including
empties. Original P accepts 300 of these tuples.

The named replacement family starts with a triangulated disk having either
zero or one private centre, and assigns every boundary diagonal either equality
(contract its noncrossing chord) or inequality (retain the edge). Nonempty
support automatically excludes loop-producing identifications. The centre,
when present, must avoid all colours at its actual spokes. Both relations are
evaluated on the same six original contacts before any quotient.

| shape type | triangulations | equality/inequality assignments | nonempty | sound nonempty |
| --- | ---: | ---: | ---: | ---: |
| zero centre | 14 | 112 | 70 | 0 |
| one centre | 84 | 545 | 365 | 0 |

The one-centre enumeration chooses its cyclic neighbour set S, then all
`6-|S|` noncrossing boundary diagonals that do not separate S. The counts by
`|S|=3,4,5,6` are 56,21,6,1. The zero-centre enumeration chooses three
noncrossing diagonals. Every nonempty candidate has a stored literal leak
witness. This includes contractions not tested in the simpler fan proposal.
The claim is exact for this finite described operation family, not a universal
impossibility theorem for arbitrary gadgets or source-dependent replacements.

Two focused larger-patch attempts are also completely replayable in the same
certificate. All internal vertices in each patch have degree five:

* Three centres x,y,z form a triangle, with rim neighbours `(0,1,2)`,
  `(2,3,4)`, `(4,5,0)` respectively. Its support has 336 literal tuples.
* Four centres form the cycle 0–1–2–3–0 plus diagonal 0–2, with rim neighbour
  lists `(0,1)`, `(1,2,3)`, `(3,4)`, `(4,5,0)`. Its support has 384 tuples.

Neither patch admits a nonempty sound candidate from the preceding 657-member
family or from the 1,983-member adjacent-two-centre family recorded in the
certificate. That family uses the same core polygon S, splits it at two actual
contacts into the neighbour arcs of adjacent centres, and applies the same
noncrossing diagonal choices. Complete original fibres and one leak per
nonempty candidate are saved. These are named finite attempts; no claim is
made that every original source contains either larger patch.

## 6. Verification and stopping boundary

```
python3 -B audits/2026-10-18-smaller-source-9f1fe84/A/check_hexagon_obstruction.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-18-smaller-source-9f1fe84/A/check_hexagon_obstruction.py --negative-control
```

Both normal and seed17 replay reproduce `hexagon_obstruction.json`. The negative
control rejects the fan's false soundness claim and a certificate with the
01202 leaks erased. The certificate SHA-256 is
`f2cad7410cc0a7a444838613847c839bd631f12d92bfedbccf235823bb2a226d`.
No external theorem, 4CT invocation or Lean proof is added. Exact matching
positivity and complete319 are unchanged. The concrete construction saves two
vertices and preserves an accepted full witness in a pair; preventing all
three rejected-row rainbow fibres in one accepted candidate remains OPEN.
