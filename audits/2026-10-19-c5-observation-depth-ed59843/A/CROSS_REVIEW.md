# A cross-review of B and integration checker

Outcome: PASS for the finite mathematical claims and their stated scope.

Reviewed integration checker SHA-256:
`0e16e25e4c8a22347cc8d9e5e9f7da5a08bfbaa8f344920cfc1ff8b2b04bed61`.
Reviewed B checker SHA-256:
`65fb8678596a07da2b12899aeae38e261be31a776a5ac91038cfa3109b64a1c2`.
Reviewed B README SHA-256:
`db47d01821c326c906ff15df42ad41fb46c3e325efd6181d8f22152c362697ce`.
These hashes identify the reviewed versions; subsequent edits require their
own consideration.

The observation order `(01232,01021,01202,01212)` and the destination-row,
source-column matrix action agree across implementations. Left-to-right word
execution makes the three experiment outputs

```text
RR  : (x2,x4,x0,x1)
PRR : (x5,x9,x7,x3 OR x8)
RRR : (x8,x6,x1,x3).
```

B's one-based inverse and the integration checker's zero-based inverse
both select the correct ten coordinates. The omitted two outputs satisfy
`c3=a4` and `b4=c4 OR c1` in one-based indexing. The integration checker's
complete image equality check also verifies that these are sufficient
constraints on the twelve output bits.

The unique minimum `{RR,PRR,RRR}` is correctly restricted to fixed subsets of
the 15 words of length at most three for the 132-state domain. Every experiment
starts independently from the same state. No claim is made here that this
exhaustion proves optimality for arbitrarily long words or for adaptive
observations on the 132 states. On all 1,024 formal masks, the separate
two-query information bound is valid regardless of word length, and the
three-probe decoder achieves it. The formal-mask algebra is not a graph
realizability theorem or a reconstruction of literal fibre counts.

Cross-checks performed:

- A, B, and integration `--check` each passed.
- All 59 depth-three pair witnesses from the independent A BFS exactly match
  the integration certificate, including their shortest suffixes.
- All 132 entries of B's three-probe codebook match the integration
  certificate's independently evaluated output vectors.
- The 8,646-pair histogram and all four complete partitions agree.

A's CLI now supports nonmutating `--check`. Its `--output` path uses exclusive
creation. A deliberate attempt to write to the already archived JSON raised
`FileExistsError`, and the archived bytes were verified unchanged. The result
SHA-256 remains
`d9c442559764d180ed13d515ac78ad326c60cfa3ae518d04448e7e31cbc26abe`.
B's reviewed version still overwrote its output in the generating mode; this
custody issue was reported to the integrating agent for B's owner to address.
No B or integration files were edited by A.
