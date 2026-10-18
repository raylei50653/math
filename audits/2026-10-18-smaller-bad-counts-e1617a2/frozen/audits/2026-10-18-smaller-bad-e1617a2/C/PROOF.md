# C. A common-exterior catalogue control for all six fixed candidates

Frozen BASE `e1617a2756813327d7ad333cfdd0fd92fa9efc38`.

The catalogue and local lift identities do **not**, by themselves, force one
of the six proposed smaller graphs outside K132. The explicit common
relations below satisfy all those identities while putting every candidate
mask in the catalogue. They are abstract exterior relations, not realized
plane exteriors, and do not refute an argument using additional source
geometry or actual Kempe components. No actual smaller bad graph is claimed.

## One exterior relation for every candidate

Retain the ordered eight contacts

```
(x,y,a,c,q,L,R,n),
```

whose exterior boundary is the actual cycle
`(a,n,R,L,q,c,x,y)`. The original b has exactly the three surviving
neighbours `{a,c,q}` after deleting p,h. An abstract exterior state assigns
one literal colour to each of these eight contacts. A chosen relation R
contains all S4 relabellings of each selected state, with the same relabelling
applied simultaneously to all contacts. For each state the checker retains
**every** legal b colour and **every** original `(p,h)` lift, including empty
lift sets. Thus none of the projected masks can use an independently chosen
exterior relation.

The exact local projections are:

| Projection | Constraint on the same exterior state and legal b |
| --- | --- |
| Original G | a full proper `(p,h)` lift exists |
| G_a | the three fan-a chords are proper |
| G_b | the three fan-b chords are proper |
| H | delete b from G_a; boundary becomes `(x,y,a,q,c)` |
| S | `q=n`; all surviving original edges remain |
| H1 | `n=b` and `q=R`; all surviving original edges remain |
| H2 | `n=b` and `b=L`; all surviving original edges remain |

The actual constructions and completed costs belong to A and B's proofs.
Here the equalities are evaluated on the full common exterior state; no
path is added and no crossing identification is assumed. A surviving edge
whose endpoints become equal automatically rejects that state. Duplicate
quotient coordinates remain in the encoding to bind the witness to its
original contacts; they are not additional private vertices.

The control scans only the existing C8 interface: 274 colour orbits,
including one two-colour orbit and 273 using three or four colours. This is
finite relation algebra, not a search over larger patches or completed
graphs. The two-colour orbit is automatically forbidden by each of the
three original target masks because one of its original lifts has row01021.

## Exact ear insertion from H to G_a

For each full H colouring, inserting b permits exactly the colours outside
`{a,q,c}`. Therefore Sigma(G_a) is the union of the following row images,
with no dependence on unspecified local or exterior choices:

| H row | G_a image mask |
| --- | --- |
| 01012 | 4 |
| 01021 | 2 |
| 01023 | 1 |
| 01201 | 256 |
| 01202 | 576 |
| 01203 | 128 |
| 01212 | 528 |
| 01213 | 32 |
| 01231 | 8 |
| 01232 | 80 |

This support map is exact for the actual ear operation. Applying it to all
132 frozen catalogue masks gives 132 catalogue outputs, counting repeated
images. In particular H mask91 maps to G_a mask854. Thus catalogue
membership of H is compatible with the already established fan-A transport.

## Explicit coherent controls

[certificate.json](certificate.json) and the compact
[relation-models-v2.json](relation-models-v2.json) give the selected orbit
generators. Their full S4 closures use 480, 456, 456 literal exterior states
respectively. The resulting joint masks are:

| Original G | G_a | G_b | H | S | H1 | H2 |
| --- | --- | --- | --- | --- | --- | --- |
| 932 | 854 | 91 | 91 | 165 | 91 | 935 |
| 933 | 854 | 91 | 91 | 165 | 91 | 935 |
| 941 | 854 | 91 | 91 | 165 | 91 | 935 |

Each of the six candidate masks is an actual key of the frozen K132
catalogue. The original mask is not. H rejects its new-boundary01232;
G_a accepts its original-boundary01232 and both paired negative rows;
H2 retains original-boundary01232. The original accepted fibre has two
full local lifts in each model. Both are covered by H1 or H2 when they
belong to the old fan-A branch, as required by B's acceptance-cover theorem.
The checker also verifies that old fan-B accepted lifts belong to S when
present; that branch is empty in these particular controls.

The certificate saves all ten full abstract fibres for each projection,
including empties. A record names its exact exterior-state index and then
its b colour and, for G, its p,h colours. The full state itself is saved.
These are complete assignments in the **abstract relation**. They are not
colourings of a claimed plane exterior with hidden vertices.

The earlier [relation-models.json](relation-models.json) is retained as the
initial nine-orbit control for G,G_a,G_b,H only. It is not the all-six
certificate. The current full certificate uses 20,19,19 orbit generators;
no claim of a minimum number of generators is needed.

## Independent projection review of the stronger Kempe consistency control

[review_kempe.py](review_kempe.py) independently evaluates every one of root's
274 C8 tuples using C's full local edge-and-lift checker. All original local
projection masks agree. The surviving sets supplied by the root certificate
give the following exact joint projections:

| Original G | Surviving states | G_a | G_b | H | S | H1 | H2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 932 | 154 | 1021 | 1023 | 509 | 1021 | 1021 | 1021 |
| 933 | 191 | 1021 | 1023 | 509 | 1021 | 1021 | 1021 |
| 941 | 225 | 1023 | 1023 | 511 | 1023 | 1023 | 1023 |

Again all six candidate masks lie in K132, and the old projection is exactly
the prescribed target. [REVIEW-KEMPE.json](REVIEW-KEMPE.json) binds the review
to the exact root checker and certificate hashes. This C review checks the
joint projections, not the noncrossing fixed-point algorithm itself. Even
that stronger necessary boundary-component closure does not supply a plane
exterior realization or an actual-source exclusion.

## Replay and limits

```
python3 -B audits/2026-10-18-smaller-bad-e1617a2/C/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-18-smaller-bad-e1617a2/C/check.py --check
python3 -B audits/2026-10-18-smaller-bad-e1617a2/C/review_kempe.py --check
```

The checker rejects a deleted full lift, a lift attached to a different
exterior state, and a false graph-realization flag. A separately corrupted
certificate is also rejected; [validation.json](validation.json) records
normal and seed17 replay and the corruption check.

The useful conclusion is a precise limitation: the shared local relation,
complete b recolouring, exact ear map, the old full lift gate, and membership
of all six smaller candidates in K132 can coexist algebraically. Obtaining
an actual smaller bad graph requires a further implication from the actual
exterior or a different construction. Smaller badness remains OPEN.
