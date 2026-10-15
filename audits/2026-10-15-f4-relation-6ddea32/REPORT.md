# F4 relation audit at 6ddea32

The [proof and report](proof/REPORT.md) establishes that the frozen seven-pin
necessary allowance relation (26 S4 orbits / 624 literal rows) has exact
projection arity six. All five-pin projections admit 96 false positives;
a single explicit six-pin polynomial together with all four-pin projections
recovers the exact allowance relation. This is not a planar-source exclusion.

[Certificate](certificate.json) · [checker](checks/check_relation.py) ·
[validation receipts](logs/receipts.json) · [frozen input seal](INPUTS.json)

Normal and seed17 replays pass, corrupted-certificate and exclusive-create
controls are rejected, and frozen/live authority input drift is zero.
No shared documentation, previous audit, commit or remote state was modified.
