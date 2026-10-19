# Independent audit A: pair BFS and exact observation depth

Input: `../frozen/certificate_v02.json`, SHA-256
`55109b2872294bb43dcd161635a65dff6ed3453d5c870a05ef0f3a9248e0d933`.
This audit uses only the supplied finite support-mask machine. It does not replay
the construction of actual graphs or the original whole-graph counting verifier.

Replay, from the repository root:

```sh
python3 -B audits/2026-10-19-c5-observation-depth-ed59843/A/replay_pair_depth.py --check
```

This recomputes the result and compares its bytes without modifying the archived
JSON. `--output NEW_PATH` exclusively creates a fresh artifact and refuses to
overwrite an existing file. With no arguments the script only prints a summary.

The script reconstructs Boolean support transitions from the nonnegative 10 by 10
matrices, closes seed F under both operations, and checks all 264 supplied
transitions and every supplied F construction word. It then performs BFS on each
unordered pair of distinct reachable masks. The first unequal-output pair gives
an independently shortest distinguishing suffix. It does not run successor
partition refinement. Classes recovered from these pair distances match every
block in each of the certificate's four partitions.

The explicit ordered observation is
`(01232,01021,01202,01212)`, corresponding to zero-based matrix-row indices
`(9,1,4,6)`. Its entries are nonempty-support bits, not literal fibre counts. This
order reproduces the certificate's example tuples; the named `four_fibres`
certificate field itself does not separately serialize the four row names.
Both P and R cost one observation step here. The certificate's distinct
interior-vertex cost assigns R cost zero and is not the depth used below.

| Minimum distinguishing depth | Unordered pairs |
|---|---:|
| 0 | 7,661 |
| 1 | 820 |
| 2 | 106 |
| 3 | 59 |
| Total | 8,646 |

The recovered class counts are exactly `15 -> 66 -> 97 -> 132`. Thus all 132
support states are distinguished by depth three, and depth two is insufficient.

## Tight witness

`FP` has mask 91; `FPPP` has mask 347. These independently replayed constructions
agree at every suffix of length at most two:

| Suffix | Common ordered output |
|---|---|
| empty | 0111 |
| P | 1101 |
| R | 0111 |
| PP | 0111 |
| PR | 1110 |
| RP | 1101 |
| RR | 0111 |

For suffix `RRR`, mask 91 stays 91, whereas mask 347 goes to 603. The outputs are
respectively `0111` and `1111`. This gives a concrete lower bound of three.
The JSON records shortest suffixes for all 8,646 pairs, including all 59 pairs
that require depth three.

## Lemma and minimality consequence

For a deterministic machine with state set Q, alphabet {P,R}, total transition
function delta, and observation O, define `q ~0 r` by `O(q)=O(r)`. Standard
successor refinement defines `q ~(k+1) r` when `q ~k r` and
`delta(q,a) ~k delta(r,a)` for both letters a. Then

```text
q ~k r  iff  O(delta(q,w)) = O(delta(r,w)) for every word w with |w| <= k.
```

Proof: the k=0 case is the definition. At the next round, the retained relation
handles the empty word (and all old words); the successor conditions handle
every nonempty word `a v` with `|v| <= k`. Conversely, equality for all words of
length at most k+1 includes equality for old words and, for each initial letter,
all required suffixes v. This proves the induction in both directions.

Every equivalence relation that preserves O and is a right congruence for both
transitions is contained in every ~k, by the same induction. Since ~3 is the
identity on the 132 reachable masks, the only such quotient identifies no
distinct states.

More generally, any deterministic Moore machine reproducing all four ordered
Boolean outputs after every word in the entire language `F(P|R)*` needs at least
132 reachable states. This quantifies over all common P/R continuations, not
only the selected finite construction witnesses. Choose one F construction
word for each of the 132 masks. If two words
reached the same state in another machine, deterministic continuation would
force equal outputs after every common suffix, contradicting the distinguishing
suffix found here. The supplied 132-state machine attains the lower bound.

This is minimality for this exact four-output behavior over this declared
alphabet. It is not minimality for the single predicate `mask=319`, for counts,
or for arbitrary planar disks. It gives no full-r6 exclusion, fixed-original-B
invariance, even-complement result, or new Lean theorem.

Finally, depth three means that the collection of outputs for suffixes of
length at most three identifies the state. It does not mean one common suffix
whose final four-bit output alone identifies 132 states: such a final output
has at most 16 possible values.
