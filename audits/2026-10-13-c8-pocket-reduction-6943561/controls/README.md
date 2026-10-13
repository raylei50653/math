# Finite pocket controls

Run from the repository root:

```sh
python3 audits/2026-10-13-c8-pocket-reduction-6943561/controls/produce.py --check
python3 audits/2026-10-13-c8-pocket-reduction-6943561/controls/independent_check.py --negative
```

`produce.py --write` exclusively creates `CERTIFICATE.json.gz` and
`RESULTS.json`; it refuses to replace an existing output. All inputs come from
the enclosing frozen snapshot and are checked against `INPUTS.json` hashes.
`independent_check.py --write` exclusively creates `INDEPENDENT_CHECK.json`;
`--write-v2` creates `INDEPENDENT_CHECK.v2.json`, preserving the first receipt.
Neither script imports previous audit code; the independent checker also does
not import the producer.

The certificate includes every one of the 91 legal noncrossing C8 boundary
partitions among all 4,140 restricted growth strings, including the identity.
Here legal means no boundary-adjacent vertices in one block and no alternating
distinct blocks. Extra edges of a particular source can further restrict legal
identifications; this boundary-only enumeration makes no source-realizability
claim. Digons retain their two boundary edge occurrences. Every canonical fan
forest has `d+1` disk pockets, simple contracted pocket cycles, and total pocket
boundary length eight. An independent rotation-system face walk checks the
producer's polygon splitting.

All seven frozen ordered C4 representatives retain their complete 84 literal
fibres. Each allowed mask contains mask 7 (one private vertex), mask 10, or mask
12 (zero private vertices). This is relation inclusion, not a claim of equal
fibres. The certificate records every available contained cheap mask and a
chosen representative of minimum private size.

The opposite-pair control retains all 274 original C8 rows for each of four
identifications and all 49 ordered representative pairs: 53,704 complete
fibres, including 45,896 empty fibres and 19,592 full private tuples. Private
tuple order is explicit in each graph. The whole-graph DFS and Cartesian join
of the two pockets agree on the same literal row. The independent checker uses
whole-graph direct products, with seed 17 row and edge shuffles. All 1,568
intersections with the eight original U bounds are nonempty. This includes the
four `(14,14)` pairs with six private vertices. These representative checks do
not by themselves prove anything about all arbitrary C4 gadgets.

For each of the eight short chords `b_i=b_(i+2)`, the long C6 pocket order is
`(b_i,b_(i+3),...,b_(i+7))`. Every chord retains all 92 original canonical Eq
rows and all 2,196 literal Eq rows, with original row indices, the projected
literal row, the inverse normalization colour frame, and the omitted original
vertex colour. All 31 normalized C6 preimage fibres are explicit, including
empty preimages in an individual U bound. Thirty C6 rows have three canonical
C8 preimages and the alternating two-colour row has two. The eight projected
supports are exactly the images of original `U intersect Eq`; they remain
necessary bounds rather than actual source relations.

Producer replay, four mutation-difference comparisons, seed 17 full-row replay,
and the independent checker passed. The strengthened independent checker also
requires the exact key sets: all seven C4 masks and all 84 literal rows, all
196 opposite-pair ordered mask combinations, all eight short chords, and all
31 proper C6 rows. Its `--negative` mode passes five actual corrupted deep
copies into the same `check()` validator and requires rejection: a dropped
partition, a dropped joint combination, a fabricated empty-fibre tuple, the
false selected reduction 7 inside mask 14, and a dropped C6 preimage. All five
were rejected with `AssertionError`; the v2 receipt records these rejections.
The eight original residuals remain; the general
theorem is OPEN, no four-colour theorem is assumed, and no new Lean theorem is
asserted.
