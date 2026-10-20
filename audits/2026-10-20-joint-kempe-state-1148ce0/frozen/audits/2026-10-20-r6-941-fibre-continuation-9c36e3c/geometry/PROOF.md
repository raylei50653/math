# J1 residual fibres: same-colouring separators and a W5 exception

This audit uses the parent frozen BASE `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`.
It inherits the complete [source contract](../frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d/SOURCE_CONTRACT.md)
and all its original graph, embedding, full-star, private-point, pocket, and global
minimality hypotheses. Fix **one** complete colouring of the same actual core F
in either residual literal fibre

```
(a,n,R,L,q,c,s,v,w,t) = (0,1,3,2,3,1,2,e0,e1,2),
(e0,e1) = (0,1) or (1,0).
```

Write z0,z1 for the original v,w having colours 0,1. No graph, colouring,
frame, or candidate is changed below. Every component includes all private
vertices. The source remains unexcluded.

## Exact component trichotomy

The frozen J1 certificate gives the following exhaustive necessary 03|12
boundary partitions for this one colouring (each brace is one actual boundary
component; there can also be components not meeting the rim):

| type | 03 components | 12 components |
| --- | --- | --- |
| I | {a}, {R,q,z0} | {n,t}, {L}, {c,s} |
| II | {a}, {R,z0}, {q} | {n,t}, {L,c,s} |
| III | {a}, {R}, {q,z0} | {n,L,t}, {c,s} |

In the 12 columns, additionally insert z1 into the block containing t if
z1=w, and into the block containing s if z1=v. This includes that vertex in
all cases and preserves the original distinction between v and w.

Thus the uncovered transport part q~z0 consists exactly of I and III.
In type III there is a real 12 n–L connection; in type I there is a real
03 R–q connection. Type II is precisely the covered q-singleton part.
These are necessary alternatives for the same colouring, not a declaration
that arbitrary choices at different colour pairs can be realized together.
The checker retains all three complete partitions for each literal fibre.

## Short-path pocket consequences

The original induced C10 and the original full h,r stars are retained.
All statements below concern paths in the actual F.

1. In type I every simple 03 R–q path has at least four edges. Its length is
   even. A two-edge path, together with original R–h–q, would make an original
   C4. Original L lies strictly inside: the h-side sector is the fixed two-face
   fan h–R–L–q, while L has colour 2 and cannot lie on the 03 path. This violates
   the original C4 empty-interior theorem.
2. If s and t are in the same 23 component, every simple 23 s–t path has at
   least four edges. Its length is even. A two-edge path, together with
   original s–r–t, would make an original C4 enclosing both original v,w in
   the fixed r-side sector s–v–w–t. Neither v nor w can lie on a 23 path.
3. In type III, a simple 12 n–L path has odd length at least three. If it has
   length three, write it `n–u2–u1–L`, with colours u2=2,u1=1. Both u2,u1
   are private core vertices. Indeed u2 cannot be s or t because original
   ns,nt are nonedges; u1 cannot be c because n,c lie in different 12
   components, and cannot be z1 because Lz1 is an absent C10 chord. The other
   rim identities are ruled out by colours or simplicity.

   The original C5 `n–h–L–u1–u2–n` encloses R: its fixed h-side sector is
   n–R–L, and R has colour 3 so is not on the path. The original C5 pocket
   theorem therefore forces exactly one interior point, namely R, and forces

   ```
   d_G(R)=5,
   N_G(R)=(n,h,L,u1,u2),
   ```

   up to simultaneous reversal of the embedding. In particular the full star
   is exact; there are no additional neighbours or private points in this
   pocket. Otherwise every 12 n–L path has length at least five. This is a
   W5 exception, not an unconditional five-edge lower bound.

The same source already supplies a simple 01 a–c path, every such path having
at least five edges; this is inherited from the frozen J1 proof, not claimed
as new here. None of the lower bounds supplies an upper bound.

In the exceptional case the three original degree-five stars p,h,R form an
actual disk with boundary

```
(a,b,q,L,u1,u2,n)
```

and interior exactly p,h,R. Its eleven faces are
`abp,bpq,pqh,phn,pna,hqL,hLR,hRn,Rnu2,Ru2u1,Ru1L`.
The original p,h patch has eight faces, and the R-centred W5 pocket has
five. They overlap in precisely the two triangles hRn and hLR, so their
union has 8+5−2=11 faces and the displayed seven-vertex boundary.
All remaining attachments are retained outside this disk. No smaller
C5 candidate has been constructed, so this normal form carries no completed
reduction or reconstruction-cost claim.

## Compatible separator ladder in the uncovered part

Assume type I or III, so fix any actual simple 03 path Q from q to z0.
Choose an actual simple 01 a–c path P in the **same complete colouring**.
The rim order a,q,c,z0 is alternating. Planar separation therefore forces
P and Q to meet, and every intersection has colour 0. No intersection is a
(the 03 boundary component of a is separate), c (colour 1), or q (colour 3).
An intersection can equal z0 if z0 belongs to the a–c component.
Boundary contacts of P can be handled by its proper subarcs, or by a small
perturbation in the disk; no new graph edge is inserted.

If additionally s~t in 23, choose any actual simple 23 s–t path S. The frozen
01|23 partition then puts v,w in a different 01 component from a,n,c.
Consequently P avoids v,w, and P and S are vertex-disjoint because their
palettes are disjoint. S has no other rim contacts: its boundary block is
exactly {s,t}. The s–t crosscut separates z0 from q, so Q meets S at colour 3.
Moreover S lies in the c–s–v–w–t–a side of P. Traverse Q from q, take its
first S-contact y3, and take its last P-contact x0 before y3. Such x0 exists
by separation. These are distinct private vertices, occur in the order

```
q ... x0(0) ... y3(3) ... z0,
x0 in P, y3 in S,
```

and the open x0–y3 subpath avoids both P and S. The privacy assertion follows
because the only rim zeroes are a,z0 and the only rim threes are R,q; the
first pair are excluded as above and S meets the rim only at its colour-2
endpoints s,t. All three paths are thus simultaneously present in one actual
colouring. This is a structural necessary condition, not a contradiction.

## Verification and limit

[check.py](check.py) verifies frozen input SHA256 values, independently reads
the two residual records, checks every allowed partition against the exact
trichotomy and separator implications, and checks the fixed cap face lists
and seven-rim patch boundary. Its negative certificate control rejects an
unconditional n–L >=5 claim. It does not reconstruct an actual source or
mechanically prove the Jordan/pocket arguments above.

Normal and seed17 replay and a tampered-certificate control are recorded in
[checks.json](checks.json). J1's two fibres, the W5 exception and all remaining
long-path cases remain OPEN. No source contradiction, smaller bad, new Lean
result, commit, or push is claimed.
