# Independent review of the fixed exterior and full matching lifts

BASE `120aae90cab8bc4881916adc598cf344f2f20f4b`.
Reviewed [MATCHING](MATCHING.md), [matching_check.py](matching_check.py),
its final v3 certificate, the complete frozen matching contract, and the
independent replay recorded in
[rigidity_matching_review.json](rigidity_matching_review.json).

**Verdict: PASS for the exact arbitrary-size statements M1--M5.**
They retain the same actual exterior and complete fibres, including empty
ones. They do not prove ordinary 101 existence or source exclusion.

## 1. Paper reconstruction

There are s+1 singleton residual components A and s+4 vertices in
`B=S union X`. After removing C the only B-B edges are the forced e,g;
the only possible A-A edge is external f. A singleton cannot meet C
except across crossing f. These facts follow from the exact residual
component definition and the already saturated zero S budget, rather
than a newly selected matching witness.

Requiring e,g occupies all X. In a 101 exterior fibre, crossing f is
unavailable and every allowable selected cut end lies in S. All s+1
singleton A vertices remain and need distinct available S mates, of
which there are at most s. Therefore every one of the 128 exterior
cells is empty. This is a conditional localization of the existing
fixed 101 barrier. A new interior patch by itself cannot remove that
exterior deficit, but no claim about every other exterior follows.

For 111, crossing f forces its unique selected port and leaves exactly
the balanced graph `D[S,A-{a}]`. External f leaves one fixed graph
`K=D[S,A-{a,a'}]`, with each labelled port fibre equal to the full
matching fibre `PM(K-v_j)`, supplied with the same marked edges and
that literal cut edge. Repeated endpoint labels retain different cut
edges. The alternating directed-path criterion is correct: flipping
an alternating path from the unique exposed root exposes its other
S endpoint; the symmetric difference proves the converse.

For every complete 111 exterior witness, removing its matching removes
all same-part edges e,g,f. The remaining exterior is bipartite in the
same A,B partition. Every unselected cut incidence ends in B, including
the case of crossing f because its A incidence was selected. Exterior
cycles and every B-to-B path therefore have even internal length.
Repeated end vertices give literal length-zero paths, also even.

The specialized join criterion consequently has only the internal
path parities on each component of the union of the two actual
pairings. Internal odd cycles are forbidden. For eta zero the prior
edge-count parity forces an even total internal parity vector, yielding
the eligible upper bound `7*5*4=140`. The componentwise join equations
and actual exterior support are still necessary. The 280 eta-one
ordinary signatures remain present with empty even111 fibres; they
have not been deleted from the ordinary matching relation.

The statement that the actual source has an even111 member uses the
separate guaranteed complete all-equal colouring in the original-sector
[C5 theorem](../2026-10-16-r6-joint-zero-c4c3d99/C/PROOF.md#c5-a-guaranteed-complete-all-equal-starting-state).
Nonempty ordinary P111 alone would not imply this statement. The
guaranteed colouring has e=f=g as differences, whose common Tait
colour class is the required even111 matching on the same D.

## 2. Finite implementation review and independent replay

The checker enumerates complete internal and external matchings, forms
their literal unions, and compares them with direct complete global
matching enumeration. Its state registry retains all 1206 ordinary
cells and all 128 selected-port cells, including empties. Marker leaves
separate repeated external incidences, so the two triggered zero-length
paths are actual recorded walks. Complete global cycles and every
labelled Tait lift with the fixed matching colour are retained.

The four controls cover crossing and external f, each with a C7 patch
and a larger factor-critical patch. The first has ordinary111 members
with no even111 lift; the second has a positive even111 witness. Thus
ordinary existence was not silently substituted for even positivity.
The separate alternating-support control has three supported S vertices
and one empty support fibre. Spherical rotations are verified, while
the minimum-source contract is explicitly `not triggered`.

Independent default and seed17 runs both pass. The latter sets both
`PYTHONHASHSEED=17` and the checker's `--seed 17`; complete replay output
agrees. Four independently corrupted certificates are rejected: a
missing empty state, altered exterior path parity, altered zero path
length, and a missing complete Tait lift. These are calibration of the
finite algebra and fail-closed certificate replay, not an enumeration
of genuine sources or proof of the paper geometry.

## 3. Exact boundary

The 140 bound applies to eligible internal signatures for the even111
subfamily on the actual barrier. The ordinary bound remains 420 and
the complete registry remains 560 tight cells. No source replacement,
completed-source descent, general colourability, Lean theorem,
ordinary101 positivity, `W110+W101>0`, complete319 exclusion, commit,
or push is established by this matching route.
