# Replay and custody

All replay commands ran from `/home/ray/developer/ai/math` on 2026-10-15.
[INPUTS.json](INPUTS.json) hashes 12 direct authorities; tracked inputs were
compared byte-for-byte with BASE at freeze time. First-round uncommitted
reports/checker are explicitly labelled working-tree inputs. Every checker
run rechecks both the frozen copies and the original paths.

```sh
python3 -B audits/2026-10-15-kempe-compatibility-6ddea32/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-15-kempe-compatibility-6ddea32/check.py --check
```

Both pass with 720 states, 22 canonical rows and exact outer mask 319. The
checker reconstructs the system using a deterministic exact-cover search,
then independently replays the saved state transition tables. No solver,
network, SciPy or NumPy is needed for the certificate or ordinary replay.

[Receipts](logs/receipts.json) retain commands, environments, exit statuses
and certificate SHA256 before/after. Full stdout and stderr are adjacent.

| Run | Exit | Result |
| --- | ---: | --- |
| Normal | 0 | PASS |
| PYTHONHASHSEED=17 | 0 | PASS, identical certificate bytes |
| Wrong switch target | 1 | Rejected by wrong literal switch target check |
| Missing final state | 1 | Rejected by missing cube target check |
| Attempted second --write | 1 | Rejected by exclusive-create |

The two intentionally damaged JSON files are retained in `logs/`. They
are negative controls and are not alternative certificates. The positive
certificate SHA256 before and after all checks is
`149383e607f1b9c90c85592115b941600fa8ce2d54e8073b76c9f86bcd63d9ab`.
Input drift is zero. No old certificate or shared source document was
modified. The work did not commit or push.

Finite-state validation is triggered and passes. Genuine minimum-source
validation is `not triggered`: no source graph was supplied or produced.
No arbitrary-size graph-realizability or source-exclusion theorem is
certified by these finite checks.
