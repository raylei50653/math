# Nonadjacent two-spoke exit-separation certificate

See the [paper reduction and scope](../../docs/c5_two_spoke_nonadjacent.md)
and [actual verification record](../../docs/history/2026-09-27-nonadjacent-two-spoke.md).

`observations.json` records:

- 74 inherited degree-four normal graphs with a retained hub and an added
  spoke, full ordered component tuples at q/pA/pB, exact hub joins, explicit
  q-colorings, and all pA edge-deletion colorings of the base.
- 3,492 degree-complete attachments for the two pB completion structures,
  full two-contact tuples at q/pB, and all edge-deletion colorings for the
  528 pB-rejecting completions.
- The four representative entries and their reflected images, plus source hashes.

```bash
python3 scripts/c5_two_spoke_nonadjacent.py --check
```

Replay uses only the Python standard library and saved rotations. Running
without `--check` regenerates this artifact. The finite certificate relies on
the report's arbitrary-size coverage; it is not a bounded source-graph census,
a disk-realizability classification, or a fully formalized graph theorem.
