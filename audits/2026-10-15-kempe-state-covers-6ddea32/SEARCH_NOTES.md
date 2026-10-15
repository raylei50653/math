# Exploratory discovery provenance

The formal positive witness is replayed directly from original graph files by
`check.py`; it does not require these discovery scripts or assert an exhaustive
source exclusion from this search.

`probe_voltage.py` / per-layer JSON first computed the binary cover space.
`probe_covers.py` built necessary weak colour functions on the864-state
Layer0 two-sheet cover. `probe_all_covers.py` examined all512 representatives of
the zero-visible-product-voltage quotient, completing in about83 seconds.
`probe-all-covers.json` retains every voltage, complete finite-domain search
node count, weak function/edge count and first t/q reachability result.

The search found458 first-test failures and54 weak survivors. The largest search
tree had1197 nodes. `probe_strict.py` / `probe-strict.json` impose actual cube
one-bit colour functions and all pin-block connectivity, leaving10 candidates.
`probe_prune.py` / `probe-pruned.json` repeatedly remove colour types having a
bichromatic component with no designated visible pin. Eight then split a required
pin block; two retain common-graph witnesses. Their exploration indices are5
and101, but the formal files bind their voltage vectors explicitly.

A printing-only KeyError and its immediate syntax correction occurred while
writing the first pruning probe; the complete saved final run contains all ten
candidates. Neither error affected the final graph files or graph verification.
`probe_graph.py` and `probe_graph101.py` first established the complete colouring
counts; `check.py` reimplements that enumeration and all original-edge checks.

These files preserve how the witnesses were found. The authoritative theorem is
the direct graph/complete-colouring/cover certificate, normal and seed17 replay,
and independent original-edge verifications, rather than the exclusion status
of the other510 exploration classes. The zero-product restriction is an explicit
subdomain and does not represent arbitrary covers with hidden components.
