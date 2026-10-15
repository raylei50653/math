# Verification

The [input seal](INPUTS.json) freezes nine files at BASE and two explicit
uncommitted first-round reports. Every replay compares both frozen and
original live bytes; all eleven inputs have zero drift.

From the repository root:

```sh
python3 -B audits/2026-10-15-six-pin-forcing-6ddea32/checks/check_forcing.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-15-six-pin-forcing-6ddea32/checks/check_forcing.py --check
```

Both read-only replays pass. The certificate preserves all 1440 local
proper assignments and all their r lifts, including empty lift sets.
The event has 96 assignments, split into four disjoint sets of 24.

Three whole-graph controls have an additional private vertex h adjacent
to v,w. They carry no optional pin edge, tp, and sq respectively. All
complete colourings are independently enumerated before quotienting.
All proper pin fibres, including empty ones, are saved. Improper pin
assignments are explicitly empty because they violate a retained edge.
The exact full pullbacks of two H and four K colourability obligations
are compared to the complete event fibres, with no normalization.

| Control | Complete colourings | Complete event colourings |
| --- | ---: | ---: |
| No optional edge | 2880 | 192 |
| Original tp | 1920 | 96 |
| Original sq | 1920 | 96 |

The five degree indicator classes are exhaustive for a0,c0>=4,
a0+c0>=11. They check exact loop and duplicate-edge arithmetic in
small incidence models. These models are not triangulated sources;
`|E(U)|=3k-8` and the exact common-neighbour sets are paper premises.

[receipts.json](logs/receipts.json) records six runs, complete stdout and
stderr, and the certificate hash before and after. Expected rejections:

- A complete H_p pullback is removed.
- An I planar excess is changed to zero.
- An actually empty seven-pin fibre is deleted from a control.
- A second generation attempts to overwrite the exclusive certificate.

All four attempts fail, and the original certificate remains byte-identical.
Its SHA256 is
`489d86dccb7f72ca0a46624a59633924109df4234aaa642cb30f2841b973a08b`.
The three damaged certificates are retained as negative evidence only.

Finite verification does not certify the arbitrary-size embedding arguments,
generate a genuine minimum source, or establish the missing event. Source
coverage remains **not triggered**; the original all-size conclusions remain
OPEN. No shared document or historical artifact is changed.
