# Independent checker scope and reconstruction

`checker.py` checks the fixed-`01232` finite necessary envelope in
`EXPLORATION-literal-strong-four.json`. It does not import `explore.py`, and it
does not check the separate seven-row experiment in `multirow/`.

The frozen round-7 certificate is pinned to SHA256
`0d53cda484f624966dcf5e46cef6933ccc4af2e542d27250258640b7906be6c8`.
This seals its original-source contract, cap edge lists, ordered attachments,
complete fibre records and prior residual sets. This checker does not replace
the prior proof of the safe replacement library.

## Independent reconstruction

1. Generate all 274 proper canonical K8 boundary words independently. For each
   of all 21 cap edge lists, enumerate every inner colouring by direct DFS;
   compare full lifts and every empty fibre against the frozen records.
2. Expand each residual to every literal S4 image while keeping the outer C5
   literally `01232`. Re-enumerate lifts directly on each literal boundary,
   rather than normalizing the two boundary components independently.
3. Enumerate exterior partitions by restricted-growth strings after union-find
   imposes the original edges of both rings. Check each rim's interlacing by
   counting cyclic changes between each pair of blocks.
4. Reconstruct each cap's bichromatic components from its full edges and every
   full lift. Join one fixed exterior partition with each lift's components.
   Enumerate every subset of the resulting components. Reject a partition if
   any lift and subset reaches a forbidden C5 row; otherwise retain every
   `01232` successor using the single palette determined by C5.
5. Independently test complementary pairs for rim interlacing, the common-gap
   condition and through-block cyclic order. Compare every per-state option
   count, every complementary-pair count, each removal set, the terminal fixed
   point and every reported survivor control.
6. For `EXCLUDED-24.json`, compare the entire six-palette option lists and both
   weak and strong pair counts, including their completeness, against the
   independent reconstruction.
7. Give an explicit vertex map from a representative to each of all 21 caps.
   Verify complete edge sets, oriented faces, the ordered K8 cycle, all full
   fibres including empties and the residual sets. The original outer C5 and
   the literal palette stay fixed. Transport every excluded literal word
   through that verified ordered boundary map.

All 21 maps use rotations; none requires a reflection. This transports the
finite interface computation to every literal cap. It makes no symmetry
assumption about the original B14 attachments or about an actual exterior.

## Target-only result

| Representative distribution | Literal states before | Literal states after | Canonical residual before | Canonical residual after |
|---|---:|---:|---:|---:|
| 200000 | 720 | 720 | 30 | 30 |
| 110000 | 2040 | 2040 | 85 | 85 |
| 101000 | 2784 | 2760 | 116 | 115 |
| 100100 | 2592 | 2592 | 108 | 108 |

The only representative removal is the entire 24-image orbit of `01023213`
for `101000`. Eight literal images already fail the two-rim condition; the
other sixteen require the stronger annular conditions. After this removal,
the next round removes no further state.

The verified cap maps give these six canonical row removals in their own
ordered K8 frames:

| Source cap index | Distribution | Removed canonical row |
|---:|---|---|
| 2 | 101000 | 01023213 |
| 4 | 100010 | 01021323 |
| 8 | 010100 | 01213032 |
| 10 | 010001 | 01213203 |
| 13 | 001010 | 01202313 |
| 17 | 000101 | 01231302 |

Thus the target-only envelope reduces the sum of the 21 canonical residual
counts from 1710 to 1704. Counts here describe necessary states, not actual
source graphs. In particular, every cap still has surviving states, and this
calculation does not construct a common exterior or exclude the whole branch.

## Scope, replays and controls

The default check requires exactly the four distinct representative cap
records, the literal-state v2 schema and `strong: true`. A full `PASS` also
requires all four envelope replays and all 21 transports. Explicit subset
checks report `PARTIAL_PASS`; `--transport-only` reports
`TRANSPORT_ONLY_PASS`. Output records the frozen source, checker and result
SHA256 values, the verified scope and the exact transport maps.

Normal and seed-17 replay commands are:

```sh
python3 -B audits/2026-10-23-941-k8-exterior-78375cc/checker.py
python3 -B audits/2026-10-23-941-k8-exterior-78375cc/checker.py --seed 17
```

The seed changes the order of literal states during the independent
reconstruction; comparison of the mathematical outputs is insensitive to this
order. Final receipts are `runs/independent-normal.jsonl` and
`runs/independent-seed17.jsonl`. The explicitly named
`*-preseal.partial.jsonl` files are interrupted development runs, not passing
replay receipts.

Both final replays returned full `PASS` and identical mathematical outputs
after removing seed and elapsed-time fields. The comparison and compact
four-representative/all-21-cap data, including the full vertex maps, are in
`runs/independent-comparison.json`. Both receipts match the final checker SHA256
`456abe2ee1ad5a0af3b00bc834c6d7163e3f6dcb45c53cbbd06eeabce9da16f4`
and the result bytes present at replay time.

Each replay exercises thirteen semantic controls: crossing/nesting,
annular pockets, four through-block orders, a forbidden-row subset swap, six
global palette checks, and a real cap-1 fibre where a fixed exterior partition
works for one lift but fails another. It also rejects ten mutations: deleting
an empty fibre, a full lift or an original ring edge; corrupting a transported
residual, oriented face or lift; omitting or duplicating a representative;
downgrading annular mode; or changing the relative-palette schema.

The finite necessity argument itself is reviewed in `REVIEW-theory.md` and
`PROOF.md`. The executable validates the finite computation under that
argument. It does not prove annular realizability, common-source realizability,
the full original branch, a new Lean theorem, or a matching theorem.
