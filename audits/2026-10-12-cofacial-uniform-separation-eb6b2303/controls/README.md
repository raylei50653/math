# Cofacial control certificate

The current certificate is `certificate.v2.json`, checked by `checker.py`.
The checker requires NetworkX 3.5, reads frozen inputs, and does not enumerate
large graphs. Run from the repository root:

```sh
uv run --with networkx==3.5 python audits/2026-10-12-cofacial-uniform-separation-eb6b2303/controls/checker.py --check audits/2026-10-12-cofacial-uniform-separation-eb6b2303/controls/certificate.v2.json
```

This run used an existing cached installation, without an install or network
request:

```sh
PYTHONPATH=/home/ray/.cache/uv/archive-v0/VGgqpOS0eMjyutRd/lib/python3.13/site-packages python audits/2026-10-12-cofacial-uniform-separation-eb6b2303/controls/checker.py --check audits/2026-10-12-cofacial-uniform-separation-eb6b2303/controls/certificate.v2.json
```

For a new certificate use `--write controls/NEW_NAME.json` with the full audit
path; output must be directly inside this controls directory and must not
already exist. `--seed 17` changes only the order of visiting catalogue rows.
Both `--check` and the frozen screen import avoid writes, including bytecode.

## Checks and scope

- Independently enumerate the ten canonical proper C5 boundary patterns.
- Independently recolour all 132 stored witnesses and check each apex graph
  for planarity. This validates witnesses; catalogue exhaustiveness is an
  input boundary, not a conclusion of this checker.
- Check all 8,778 unordered catalogue unions including diagonals.
- Check the complete catalogue subrelation lists for 933 and 941 and all
  twenty D5 transports, which produce ten distinct target masks. Record all
  missing target patterns and the transported `01232` state.
- Import the frozen screen definitions without calling main. Recompute the
  complete Kempe obligations, rejection witnesses, all disjoint exterior
  catalogue witnesses, and the 153 / 142 / 10 counts. All ten outside
  candidates contain the five four-colour states (mask 932), and their
  three-colour singleton supports have one point or two nonadjacent points.
- Check three explicit small source graphs (the third with two pairs), with
  all ten complete boundary fibres, including empty fibres. Quotient lifts
  pull back exactly to equality lifts; adding the pair edge gives exactly
  the inequality lifts. Eq and Diff relation masks overlap.
- The specified graph C5 + b0a + b0b + b0c + ac has independently safe
  identifications a=b and b=c, but no joint lift. It is a counterexample to
  combining independent witnesses. After the first identification the
  second pair is adjacent; simultaneous identification would create a loop.
- All small source G+uv embeddings are also checked using explicit integer
  coordinates. Twelve source/quotient/added-edge apex tests pass.

`validation.v2.json` records that the seed-17 certificate is byte-identical,
read-only checks preserve hashes, frozen files remain unchanged, attempted
rewrite is rejected, and an impossible lift inserted in an empty Eq row is
rejected. `certificate.corrupted.v2.json` is intentionally invalid.

The outside-source, globally minimum outside-source, and lexicographic
maximum-edge premises are **not triggered**: no such source is supplied or
inferred. The universal adjacent-singleton statement remains unproved here;
its finite candidate filter is explicitly conditional. No source realizability,
general compression theorem, or Lean proof is claimed by these controls.

## Earlier optional-dependency pass

`checker.v1.py`, `certificate.json`, `certificate.seed17.json`,
`certificate.corrupted.json`, and `validation.json` preserve the initial
stdlib-only pass. V1 marked NetworkX unavailable and used exact coordinates
for small controls. V2 supersedes it by also checking all 132 witness apex
graphs and the frozen necessary screen. To replay V1 with its original
missing-NetworkX environment use system Python with PYTHONPATH unset.
The V1 validation recorded the original checker digest under its then-current
name `checker.py`; that identical code is now preserved as `checker.v1.py`.
