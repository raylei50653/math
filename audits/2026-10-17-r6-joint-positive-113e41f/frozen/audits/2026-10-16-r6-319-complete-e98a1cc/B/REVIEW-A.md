# Independent B review of A's paper proof

Reviewed `../A/PROOF.md` at frozen BASE e98a1cc. Paper result: **PASS**,
with exactly the OPEN boundary stated there. This review covers the
paper arguments and the final checker replay recorded below.

* The `mp iff a0=4` and reflected `mq iff c0=4` use the literal original
  nonedges and fan endpoints, so cofacial contraction in J minus z
  introduces no loop. The exposed link face, rather than a claimed
  face of J itself, is the correct domain.
* The order calculation is consistent: J has k-1 vertices, the deletion
  and contraction give k-3, and the three-vertex thin cap gives k-5
  interior vertices. Its relative-minimality invocation is confined to
  this source's smaller legitimate C5 disk. It is not general planar
  colourability.
* For m=p of colour c and q of colour d, a J lift is FJ-legal exactly
  when its z colour and d are the two colours of v,w. This follows
  separately for z equal to the fourth triangle colour and z equal to
  a v/w colour. Hence all complete z fibres, including empty ones,
  satisfy the stated empty-or-singleton restriction.
* I checked all edges of the displayed local empty-fibre witness.
  Its old entire z link uses all four colours. It demonstrates why
  nonempty quotient colourings do not prove any nonempty J lift.
* In the complete-U Kempe bijection, the AD z-v path separates the
  boundary endpoints s,w in BC. The s-component switch fixes every
  other boundary position, changes ABACD to ACACD, and preserves its
  own vertex set for the inverse. The forbidden reverse v-switch is
  the ABCBC boundary class. The pq conclusion keeps the same actual
  colouring and follows because the switch never creates colour D.

No path here supplies the remaining nonempty violating hub fibre or
the joint even-complement endpoint. A correctly leaves full 319 OPEN.

After A corrected the tuple/list serialization mismatch and generated
`final-certificate.json`, I independently replayed
`python -B ../A/check.py --check`: PASS, with 2688 complete quotient
colourings, all 1296 empty z fibres, 360 compatible nonempty fibres,
1032 incompatible nonempty fibres, and 16384 seven-pin assignments.
The initial serialization failure was not treated as a passing check.
