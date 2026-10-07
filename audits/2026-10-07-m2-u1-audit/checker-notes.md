# M2 independent finite checker

Frozen candidate: `ba0b447f09617591d9f2ba81c988f537af771791`.

`verify.py` uses only Python's standard library. It imports neither the U1
producer/checker nor an inherited producer/checker. Its independent solver pins
the five boundary colors and each of all sixteen ordered root-color pairs,
then searches the complete literal graph by minimum-remaining-values forward
checking. This differs from enumerating all colorings first and projecting the
roots. Each restored graph is solved afresh; filtering the core certificate is
only a subsequent comparison.

The checker independently generates all ten canonical proper C5 rows and the
whole-boundary D5 action on ten-bit signatures. The target signatures are the
given full signatures 933 and 941. One boundary permutation acts on the entire
signature; no side, piece or marginal is separately transformed. Canonical
color renaming chooses representatives of global S4 classes.

The inherited and U1 certificates are joined by exact form ID, literal edges,
named coloring order, ordered roots, family and original unary vertex groups.
The actual no-mixed component partition, ownership, ordered contacts, support,
per-vertex boundary attachments and incident edges are reconstructed from
those same edges. The original zw remains an internal bridge, every complete
core inner degree is four, and only the two ordered roots gain degree five on
literal restoration. Every inherited nonframe q-critical deletion witness is
checked on its full edge-deleted graph; rejection of q is independently solved.

For every one of the 344 cores and 3,498 restorations, the checker solves all
ten rows and compares complete ordered pairs, including empty fibres. It
checks every certificate core witness and every indexed restored witness on
the actual full edge set and common boundary color frame. Fresh solver
witnesses are independently checked too. Every Cartesian product of absent
named root spokes is compared against the stored restoration list. It
recomputes the aggregate family counts, full histogram, target intersection,
and 64 double-triangle / 1,024 restoration histogram.

Corruption controls alter only in-memory copies: drop a genuine core pair;
corrupt an unpinned interior witness while preserving the row/root pins;
invent a pair in an empty core fibre; omit a surviving restored pair index;
invent an index in an empty restored fibre; omit a literal restoration;
remove an original graph edge; and omit a target orbit member. Each must fail
its corresponding check. Explicit small positive and contradictory negative
graphs exercise the fresh solver independently of the repository inputs.

These are finite necessary-domain controls. They do not trigger the complete
source premise: no tested restoration has a target signature, and the
relaxed restoration list has no disk/criticality source-positive control.
Arbitrary-size normalization and upstream topology/NetworkX completeness are
paper dependencies and are classified as `not triggered` by this program.
No new Lean theorem, source realizability result, U2-U4 result or general
theorem is claimed.

The result contains SHA256 and byte sizes of both immutable JSON inputs and
the U1 producer file, whose bytes are read solely to verify the certificate's
declared hash. It also contains the independent checker's SHA256, deterministic
counts, per-form relation digests, the controls and a zero-byte-drift check.
The parent audit runner records command, exit code and logs separately.

```sh
python3 audits/2026-10-07-m2-u1-audit/verify.py \
  --root /tmp/math-m2-ba0b447-audit \
  --output audits/2026-10-07-m2-u1-audit/results.json
```

Changing output locations or `PYTHONHASHSEED` does not change mathematical
result bytes. Timestamps, runtimes and output paths are omitted deliberately.

Development record: the first complete development execution passed without
an error. Before formal executions, the witness corruption control was
strengthened to change an unpinned interior color while preserving the
boundary and root pins, ensuring detection by the literal-edge check. The
pre-final development result was removed; it is not delivery evidence. The
checker was frozen before the parent runner's formal default/seed17 runs.
