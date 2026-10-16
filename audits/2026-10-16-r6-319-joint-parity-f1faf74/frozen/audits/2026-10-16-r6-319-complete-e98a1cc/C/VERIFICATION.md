# Verification of C's complete planar countercontrol

Run from the repository root:

```sh
python3 -B audits/2026-10-16-r6-319-complete-e98a1cc/C/verify.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-16-r6-319-complete-e98a1cc/C/verify.py --check
```

The checker imports no earlier checker and has no third-party dependency.
It reconstructs the sphere embedding from its complete cyclic rotations,
all complete labelled J, W and U colourings, all perfect matchings, all
empty matching and hub fibres, and every legal r lift. Both reflected
seven-pin universes have all 16,384 counts, with full private-colouring
record indices. The J six-pin universe has all 4,096 counts.

`INPUTS.json` seals the frozen source proofs used for the mathematical
contract. Every run verifies those hashes. `VERIFICATION.json` records
the final checker and certificate hashes, normal and seed-17 replay,
four intentionally corrupt certificate rejections, and the expected
exclusive-create rejection. The controls falsely replace the joint
minimum by zero, drop one explicit empty seven-pin cell, drop a legal
r lift, and drop one complete private J colouring. All must be rejected.

`source-failures.json` extracts the exact source diagnostics from the
active certificate and names every source condition tested here.
`certificate-before-*` are preserved earlier certificates; the active
file is exclusively `certificate.json`. Their replacement was explicit
and preserved the preceding bytes, as requested.

The discovery used the already present plantri binary only to locate
the graph. `planar-search-with-101.json` is a discovery receipt; it is
not the proof of planarity, complete colour coverage, or absence of
source graphs. The independent final checker needs no plantri executable.

No actual minimum source is supplied. Source coverage is **not triggered**.
The positive mathematical result is the finite refutation of the broad
ordinary-to-even bridge, with exact preservation of every retained fibre.
