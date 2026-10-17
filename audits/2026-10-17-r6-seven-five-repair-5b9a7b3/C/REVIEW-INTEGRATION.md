# C independent review of the integrated paper

Reviewed `../PROOF.md` at BASE
`5b9a7b3190c84bc10ff99608e372a9b4be57a0f6`, 2026-10-17.
Scope: complete source mark trichotomy, the explicit six-cut, whole-region
descent, and the stated OPEN endpoint. No blocking mathematical issue found.

1. The trichotomy in section 3 is exhaustive. A chosen mark incident with
   the degree-four centre cannot lie on C, so it must be the shared chord;
   the omitted f in 101 instead lies on the four-face arc. Its other cap
   centre is ordinary by A3 and the cross nonedges. The first two cap types
   retain the chord in M0 and therefore only have the three common-chord
   rows of the local table.
2. The statement that all other marks are exterior in the first two types
   is correct. For chord e, f or g as a spoke would require respectively
   one of pv,pw,qv,qw or zv,zw. Neither can be a cap edge since its primal
   endpoints are not cap centres. For chord f, the e-spoke is excluded by
   the same cross nonedges. The omitted g cannot be a spoke since all five
   spokes are in M; it cannot be a cap edge by the hub degree bounds.
3. In section 5 the four-face placement guarantees a nonchord endpoint
   a of f. Literal primal endpoint disjointness ensures e is not incident
   with a. The set Y=X minus {a} has precisely six boundary edges, includes
   both marks, retains the entire other five-face, and has an exterior
   whole F cycle on its complementary side. Thus every hypothesis of the
   adopted marked-six theorem is verified for an explicit vertex set.
4. The section 4 equality is exact. The connected components of
   `D minus (M intersect M0)` are closed under complete F, F0 and
   difference cycles. Their boundaries consist only of common matching
   edges. Flipping all difference cycles in a component therefore replaces
   the whole complement inside by even F0 while retaining every outside
   complement cycle. Avoiding the sole h-containing difference cycle H
   preserves the exact joint identity. The resulting strict descent proves
   that every odd F circle of a joint oddness-minimizer is in W_H.
5. The OPEN boundary in section 6 is necessary and accurate. No marked
   cyclic cut follows from H-connectedness as presently proved. Every cap
   type has e or f internal to X, so a region containing X cannot have both
   marks on its boundary. A new cut argument must split X and re-establish
   cyclicity and its size bound. Neither `Q != H` nor a single local safe
   flip gives an unconditional full-complement descent.

The local calibration independently checks all 25 nonincident
spoke / C-edge placements, including both four-face and five-face arcs.
Normal and seed17 replays pass; corrupted-certificate and exclusive-create
controls reject as intended. Frozen proof inputs equal BASE bytes. This is
finite calibration and not named-source realization or a source exclusion.
