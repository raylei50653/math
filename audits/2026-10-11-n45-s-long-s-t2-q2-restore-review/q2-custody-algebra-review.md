# Independent q2 custody and algebra review

Date: 2026-10-11. Target: `../2026-10-11-n45-s-long-s-t2-q2-restore/`.
BASE: `f2692089ad4259808e27d9b7e882ac09505b180a`.
The target, shared files, dispatch authority, and prior audit artifacts were
read only. No other current worker's new outcomes were examined or used.

## Judgment and required coverage correction

Delivery custody and the bounded literal/pin calibration pass. The new claimed
restoration coordinates are consistent with all literal support maps, complete
ordered pin transport, and the seven assigned schedules. Paper validity is
judged separately by the independent paper reviewer. The original coverage
must be adopted with an overlay for 112 omitted known-empty cells; original
bytes remain immutable. These omissions do not affect the selected q3/q4
restoration fibres or their seven-schedule coverage.

The original U012 query is identically 012 on β=01201, q1=01202, q0=01212,
and the four T4 literals 01203, 01213, 01231, 01232. Thus inherited
`F_U(β)={1}` forces every full X pin with s=1 empty on all seven rows. Across
seven schedules these are 196 positions. The original coverage already marks
84 positions empty on β/q0/q1; the other 112 positions, on the four T4 rows,
are marked `source-specific; not supplied`, with no existing emptiness reason.
Neither retained s-spoke forbids s=1 there, and those G rows are accepted.
Consequently all 112 are newly classified known-empty cells, rather than
positions that merely need another reason. They are exactly the Cartesian
product of seven schedules, those four literals, r=0/1/2/3, and s=1.

## Exact custody

Current delivery SHA256:
`79dc6912fbd13f863986d1d85e6f4b9490920711e023d8c2ab33feb8cd454605`.
The delivery has exactly 90 payload files and 5,015,240 payload bytes.
The actual target tree has 92 regular files and 14 directories, no symlinks
or special files. The precise exclusions are only root `delivery.json` and
root `seal-receipt.json`. Both frozen authority copies named `delivery.json`
are included and match their hashes. There are no missing, extra, duplicate,
or mismatched payload entries. The receipt binds this current manifest.

All 23 authority inputs match their live originals, local frozen copies,
dispatch records, and dispatch frozen copies. The twelve BASE inputs also
match exact BASE Git blob identities and bytes. The eleven sealed audit
inputs have null Git blob identity and explicitly do not claim BASE inclusion.
The separate 164,927-byte external Gallai PDF matches its inherited SHA256
`50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`;
it remains an external primary source pin, neither a BASE blob nor a new theorem
dependency in the restoration proof.

Before/after custody snapshots are identical and contain 1,037 records for
1,036 distinct files. `audits/2026-10-11-n45-s-long-s-fibre/external/gallai.pdf`
appears twice with the same hash. All 1,036 live files were independently
rehashed without drift. Hence “1,037 monitored records” is correct; “1,037
distinct inputs/files” would need correction. Current HEAD is BASE and the
tracked diff is empty, matching both recorded snapshots.

Independent native `git show BASE:path` queries return exit128 for both
`artifacts/c5_no_spoke_exterior/observations.json` and
`artifacts/c5_single_spoke_residual_locality/observations.json`. Their inputs
are not admitted and dependent replay is unexecuted. No physical or quarantine
copy substitutes for BASE. The earlier manifest-validator failure is retained
as a failed generation and native exit1 log; its two differing paths are
exactly the frozen authority delivery copies. The current exact-root exclusion
fix handles both copies correctly.

## Independent bounded arithmetic

The standalone `independent-check.py` imports no delivered worker code and
only reads files, runs read-only Git queries, and prints JSON. It independently
enumerates all ten normalized proper boundary rows and all S4 permutations.
Thirty piece/row queries produce 720 permutation comparisons and 34 matching
maps: six queries have no map, fourteen have one, and ten have two. In
particular U012=012 cannot be mapped by a colour permutation to target 010;
the delivery correctly uses a separate arbitrary-size U slack argument.

All six β two-colour partitions are checked. The unique partition compatible
with the proved S r=0/r=1 nonempty fibres is S={2,3}, L={0,1}. Independently
deriving the target support maps gives:

| Target | L map | S map | Seeds → common pins | Original b4 colour |
| --- | --- | --- | --- | --- |
| q3=01021 | [2,1,0,3] | identity | L(2,3), S(0,3) → (0,3) | 1 |
| q4=01012 | [1,2,0,3] | [0,2,1,3] | L(2,3), S(0,3) → (0,3) | 2 |

All four maps are bijections of the complete ordered 16-pin domain, giving
64 pin maps including diagonal and empty positions. Both target U queries
are 010, and both retained original s-spokes have colour 0. At s=3 the q3
L/S forbidden r sets are {1,2}/{2,3}; q4 sets are {1,2}/{1,3}. In both rows
the only nonempty r pin is 0. This is symbolic full-fibre metadata and its
paper transport, without actual assignments, tuple counts, or preimage counts.

Exact schedule coverage is seven schedules, 70 rows, 1,120 ordered symbolic
pin cells, and 280 diagonal cells. The two target rows provide fourteen
symbolic nonempty cells and 42 empty cells in their s=3 slices. Nine of those
nonempty cells occur in the respective original Δ sets and give claimed
contradictions. Selecting q4 where available covers five schedules; q3 covers
the remaining two. The original e and its literal b4 colour are checked on
every row, including T4 rows, and each claimed restored fibre has pins (0,3).

The preserved corrupted calibration certificates have exactly these mutations:

1. q4's L map changes [1,2,0,3] to [0,2,1,3], with no other mutation.
2. The (3,3) diagonal pin is removed only from calibration schedule 933/0123,
   literal 01012, with no other mutation.

## Safe native replays

The following worker commands are read only. Root supervision captures fresh
native command, stdout, stderr, and exit records separately:

```sh
python3 -B audits/2026-10-11-n45-s-long-s-t2-q2-restore/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n45-s-long-s-t2-q2-restore/checker.py --check
python3 -B audits/2026-10-11-n45-s-long-s-t2-q2-restore/checker.py --check --certificate audits/2026-10-11-n45-s-long-s-t2-q2-restore/negative-controls/wrong-L-map.json
python3 -B audits/2026-10-11-n45-s-long-s-t2-q2-restore/checker.py --check --certificate audits/2026-10-11-n45-s-long-s-t2-q2-restore/negative-controls/missing-diagonal.json
python3 -B audits/2026-10-11-n45-s-long-s-t2-q2-restore/validate_delivery.py --manifest
python3 -B audits/2026-10-11-n45-s-long-s-t2-q2-restore-review/independent-check.py
```

`checker.py --print-certificate` also only prints but is unnecessary for
acceptance. `run_checks.py` is a mutating exclusive-generation/log wrapper
and must not be replayed. Both negative commands reject at the exact
calibration certificate equality after frozen input verification. Such
rejection verifies bounded metadata, not source realizability. The validator
checks the delivered original coverage structure; it does not detect the
112-cell missing known-empty classification and therefore cannot replace
the independent overlay.

Target source remains unexecuted with null trigger count and `not triggered`.
No source graph enumeration, historical 19-control replay, new Lean theorem,
or general N45/N2/E conclusion is claimed. Full-assignment product semantics
and arbitrary-size existence are paper obligations assessed separately from
these finite metadata checks.
