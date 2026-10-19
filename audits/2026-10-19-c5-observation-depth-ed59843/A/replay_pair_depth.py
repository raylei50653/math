#!/usr/bin/env python3
"""Independent finite Moore-machine audit by BFS on unordered state pairs.

No package dependencies. Reconstruct support transitions from the matrices;
do not use the submitted refinement algorithm or trust its state list.
All P/R letters count as one observation step, despite R's zero vertex cost.
"""

import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


OBSERVATION_ROWS = ("01232", "01021", "01202", "01212")


def replay(certificate_path):
    raw = certificate_path.read_bytes()
    certificate = json.loads(raw)
    model = certificate["model"]
    rows = model["rows"]
    alphabet = tuple(model["alphabet"])
    assert alphabet == ("P", "R")
    observed_indices = tuple(rows.index(row) for row in OBSERVATION_ROWS)
    matrices = model["operators"]
    width = len(rows)
    assert width == 10
    assert all(len(matrix) == width for matrix in matrices.values())
    assert all(len(row) == width for matrix in matrices.values() for row in matrix)
    assert all(entry >= 0 for matrix in matrices.values() for row in matrix for entry in row)

    def transition(state, letter):
        return sum(
            1 << i
            for i, row in enumerate(matrices[letter])
            if any(row[j] and (state & (1 << j)) for j in range(width))
        )

    def observe(state):
        return tuple((state >> i) & 1 for i in observed_indices)

    def after(state, word):
        for letter in word:
            state = transition(state, letter)
        return state

    seed = model["seeds"]["F"]["mask"]
    construction = {seed: "F"}
    queue = deque([seed])
    while queue:
        state = queue.popleft()
        for letter in alphabet:
            successor = transition(state, letter)
            if successor not in construction:
                construction[successor] = construction[state] + letter
                queue.append(successor)
    states = sorted(construction)
    assert states == model["states"]
    assert len(states) == 132
    transition_checks = 0
    for state in states:
        for letter in alphabet:
            assert transition(state, letter) == model["transitions"][str(state)][letter]
            transition_checks += 1
        word = model["reachable_words_F"][str(state)]
        assert word[0] == "F" and after(seed, word[1:]) == state

    def shortest_distinguishing_word(left, right):
        # Search all words in breadth-first order; pair deduplication is exact
        # because all future outputs depend only on the current pair.
        start = tuple(sorted((left, right)))
        queue = deque([(start, "")])
        seen = {start}
        while queue:
            (a, b), word = queue.popleft()
            if observe(a) != observe(b):
                return word
            for letter in alphabet:
                nxt = tuple(sorted((transition(a, letter), transition(b, letter))))
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, word + letter))
        return None

    pairs = []
    histogram = Counter()
    pair_depth = {}
    for left, right in combinations(states, 2):
        suffix = shortest_distinguishing_word(left, right)
        assert suffix is not None
        depth = len(suffix)
        histogram[depth] += 1
        pair_depth[left, right] = depth
        pairs.append({"left": left, "right": right, "depth": depth, "suffix": suffix})
    max_depth = max(histogram)
    assert max_depth == 3
    assert sum(histogram.values()) == 132 * 131 // 2

    # Recover classes from the pair-BFS distances, without successor refinement.
    # Check every pair within/between the resulting equivalence classes.
    partitions = []
    for depth in range(max_depth + 1):
        remaining = set(states)
        blocks = []
        while remaining:
            representative = min(remaining)
            block = sorted(
                state for state in remaining
                if state == representative
                or pair_depth[tuple(sorted((state, representative)))] > depth
            )
            remaining.difference_update(block)
            blocks.append(block)
        block_index = {state: i for i, block in enumerate(blocks) for state in block}
        for (left, right), distance in pair_depth.items():
            assert (block_index[left] == block_index[right]) == (distance > depth)
        partitions.append(blocks)
    block_counts = [len(blocks) for blocks in partitions]
    submitted = certificate["refinement"]["four_fibres"]
    assert block_counts == submitted["round_block_counts"] == [15, 66, 97, 132]
    assert partitions == submitted["rounds"]
    submitted_example = certificate["distinguishing_example"]
    example_states = [submitted_example["left"], submitted_example["right"]]
    assert [list(observe(state)) for state in example_states] == submitted_example["before_output"]
    assert [list(observe(after(state, submitted_example["suffix"]))) for state in example_states] == submitted_example["after_output"]

    deepest = [pair for pair in pairs if pair["depth"] == max_depth]
    witness = min(
        deepest,
        key=lambda pair: (
            len(construction[pair["left"]]) + len(construction[pair["right"]]),
            max(len(construction[pair["left"]]), len(construction[pair["right"]])),
            pair["left"], pair["right"],
        ),
    ).copy()
    left, right = witness["left"], witness["right"]
    witness["construction_words"] = [construction[left], construction[right]]
    witness["common_outputs_through_depth_2"] = []
    for depth in range(max_depth):
        for letters in product(alphabet, repeat=depth):
            word = "".join(letters)
            output = observe(after(left, word))
            assert output == observe(after(right, word))
            witness["common_outputs_through_depth_2"].append({"suffix": word, "output": output})
    witness["after_masks"] = [after(left, witness["suffix"]), after(right, witness["suffix"])]
    witness["after_outputs"] = [observe(state) for state in witness["after_masks"]]
    assert witness["after_outputs"][0] != witness["after_outputs"][1]

    # Deliberate negative controls: the two overclaims are numerically false.
    # Depth 2 fails to identify all states; one final-output suffix cannot
    # identify 132 states because four Boolean observations have only 16 values.
    negative_controls = {
        "depth_2_is_sufficient_rejected": block_counts[2] < len(states),
        "one_final_four_bit_output_identifies_132_rejected": 2 ** len(observed_indices) < len(states),
    }
    assert all(negative_controls.values())
    return {
        "schema": "c5-independent-pair-depth-audit/v1",
        "scope": "reachable support-mask Moore automaton from supplied nonnegative matrices, seed F only",
        "certificate_sha256": sha256(raw).hexdigest(),
        "observation_rows": OBSERVATION_ROWS,
        "observation_indices_zero_based": observed_indices,
        "observation_type": "ordered Boolean nonempty-support bits, not literal fibre counts",
        "depth_cost": {letter: 1 for letter in alphabet},
        "state_count": len(states),
        "matrix_transition_checks": transition_checks,
        "all_submitted_reachability_words_replayed": True,
        "pair_count": len(pairs),
        "shortest_distinguishing_depth_histogram": dict(sorted(histogram.items())),
        "max_shortest_distinguishing_depth": max_depth,
        "partition_block_counts_from_pair_BFS": block_counts,
        "all_four_partitions_match_certificate": True,
        "observation_order_matches_supplied_example": True,
        "depth_3_necessity_witness": witness,
        "negative_controls": negative_controls,
        "construction_words_from_unweighted_BFS": {str(state): construction[state] for state in states},
        "pair_witnesses": pairs,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path,
                        default=Path(__file__).resolve().parent.parent / "frozen" / "certificate_v02.json")
    parser.add_argument("--output", type=Path, help="exclusive-create a new result; with --check, select the stored result")
    parser.add_argument("--check", action="store_true", help="recompute and byte-compare the stored result without writing")
    args = parser.parse_args()
    result = replay(args.certificate)
    rendered = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if args.check:
        stored = args.output or Path(__file__).resolve().parent / "pair_depth_results.json"
        if stored.read_bytes() != rendered:
            raise ValueError("stored pair-depth result differs from independent replay")
    elif args.output:
        with args.output.open("xb") as handle:
            handle.write(rendered)
    summary = {key: value for key, value in result.items()
               if key not in ("pair_witnesses", "construction_words_from_unweighted_BFS")}
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
