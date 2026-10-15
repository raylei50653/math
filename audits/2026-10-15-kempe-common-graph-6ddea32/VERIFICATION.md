# Replay and negative controls

From the repository root:

```sh
python audits/2026-10-15-kempe-common-graph-6ddea32/check.py
PYTHONHASHSEED=17 python audits/2026-10-15-kempe-common-graph-6ddea32/check.py
python audits/2026-10-15-kempe-common-graph-6ddea32/verify.py
PYTHONHASHSEED=17 python audits/2026-10-15-kempe-common-graph-6ddea32/verify.py
```

All four pass. The generator recomputes all data and compares the whole JSON
certificate. The independent verifier reconstructs literal binary constraints,
checks every deletion and complete branch in the47-node search proof, and
reconstructs all weak/strict type graphs and all failed blocks. It does not
import `check.py` or use its search.

Three saved corruptions are each rejected by both programs:

- `logs/missing-type.json`: delete one admissible function;
- `logs/false-edge.json`: add the impossible edge18-19;
- `logs/missing-branch.json`: omit one branch of the exhaustive tree.

`check.py --write` also rejects the existing certificate using exclusive create.
The11 run receipts, arguments, exit codes, stdout and stderr are in
[logs/receipts.json](logs/receipts.json). Every replay checks the SHA256 hashes of
both frozen and live authority inputs. The original states are not regenerated
or modified. A K3 control confirms that the necessary test accepts a known
realization; failure here is specific to the supplied table.

The exhaustive domain is all covariant vertex-colour functions on the supplied
finite state set, not all graphs below a chosen vertex cutoff. The path-image
lemma turns its certified missing path into an obstruction for every finite
graph size satisfying the stated lift contract.
