#!/usr/bin/env python3
"""Independent finite replay of the minimum depth-three FOUR probe family.

Only the standard library and the frozen certificate are read. Matrices act
as Boolean destination-row/source-column maps; words are executed left to
right. Empty string denotes epsilon. This proves properties of the supplied
finite automaton and of its Boolean matrix maps, not graph realizability.
"""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROWS = ["01012", "01021", "01023", "01201", "01202", "01203", "01212", "01213", "01231", "01232"]
FOUR = ["01232", "01021", "01202", "01212"]


def build_result(certificate_path):
    raw = certificate_path.read_bytes()
    certificate = json.loads(raw)
    model = certificate["model"]
    assert model["rows"] == ROWS
    assert model["alphabet"] == ["P", "R"]
    states = sorted(model["states"])
    assert len(states) == len(set(states)) == 132
    matrices = model["operators"]
    output_indices = [ROWS.index(row) for row in FOUR]

    def step(mask, letter):
        matrix = matrices[letter]
        return sum(
            1 << destination
            for destination in range(10)
            if any(
                matrix[destination][source] and mask & (1 << source)
                for source in range(10)
            )
        )

    def execute(mask, word):
        for letter in word:
            mask = step(mask, letter)
        return mask

    def observation(mask):
        return "".join(str((mask >> bit) & 1) for bit in output_indices)

    # Rebuild all transitions from the matrices before trusting the table.
    for mask in states:
        for letter in model["alphabet"]:
            actual = step(mask, letter)
            assert actual == model["transitions"][str(mask)][letter]
            assert actual in states

    words = ["".join(chars) for depth in range(4) for chars in product("PR", repeat=depth)]
    values = {
        mask: [observation(execute(mask, word)) for word in words]
        for mask in states
    }

    def partition(indices):
        groups = {}
        for mask in states:
            key = tuple(values[mask][index] for index in indices)
            groups.setdefault(key, []).append(mask)
        return sorted(groups.values())

    depth_counts = []
    for depth in range(4):
        actual = partition([index for index, word in enumerate(words) if len(word) <= depth])
        depth_counts.append(len(actual))
        assert actual == sorted(certificate["refinement"]["four_fibres"]["rounds"][depth])
    assert depth_counts == [15, 66, 97, 132]

    # One integer represents the set of pairs separated by a probe. This
    # exhaustive search is independent of any partition-refinement code.
    pairs = list(combinations(states, 2))
    covers = []
    for index in range(len(words)):
        cover = 0
        for bit, (left, right) in enumerate(pairs):
            if values[left][index] != values[right][index]:
                cover |= 1 << bit
        covers.append(cover)
    complete_cover = (1 << len(pairs)) - 1
    lower_bound_collisions = []
    subset_counts = []
    minimum_indices = []
    for size in range(len(words) + 1):
        checked = 0
        solutions = []
        for indices in combinations(range(len(words)), size):
            cover = 0
            for index in indices:
                cover |= covers[index]
            checked += 1
            if cover == complete_cover:
                solutions.append(indices)
            else:
                missing = complete_cover ^ cover
                first_missing_bit = (missing & -missing).bit_length() - 1
                left, right = pairs[first_missing_bit]
                if size < 3:
                    left_output = [values[left][index] for index in indices]
                    right_output = [values[right][index] for index in indices]
                    assert left_output == right_output
                    lower_bound_collisions.append({
                        "words": [words[index] for index in indices],
                        "collision": [left, right],
                        "common_outputs": left_output,
                    })
        subset_counts.append({"size": size, "checked": checked, "injective_subsets": len(solutions)})
        if solutions:
            minimum_indices = solutions
            break
    assert [[words[index] for index in indices] for indices in minimum_indices] == [["RR", "PRR", "RRR"]]
    chosen = minimum_indices[0]
    assert len(lower_bound_collisions) == 1 + 15 + 105

    # Boolean maps preserve unions, so their action on singleton supports
    # gives exact source-bit OR formulas, beyond the 132-state restriction.
    formulas = []
    for index in chosen:
        word = words[index]
        equations = []
        for row, output_bit in zip(FOUR, output_indices):
            source_bits = [source for source in range(10) if execute(1 << source, word) & (1 << output_bit)]
            equations.append({
                "output_row": row,
                "source_bit_indices": source_bits,
                "source_rows": [ROWS[source] for source in source_bits],
            })
        formulas.append({"word": word, "outputs": equations})
    expected_sources = [[[2], [4], [0], [1]], [[5], [9], [7], [3, 8]], [[8], [6], [1], [3]]]
    assert [[item["source_bit_indices"] for item in formula["outputs"]] for formula in formulas] == expected_sources

    # a=O(RR q), b=O(PRR q), c=O(RRR q), component positions start at 1.
    reconstruction = [["a", 3], ["a", 4], ["a", 1], ["c", 4], ["a", 2], ["b", 1], ["c", 2], ["b", 3], ["c", 1], ["b", 2]]
    formal_signatures = set()
    for mask in range(1024):
        outputs = [observation(execute(mask, words[index])) for index in chosen]
        named = dict(zip("abc", outputs))
        recovered = sum(int(named[name][position - 1]) << bit for bit, (name, position) in enumerate(reconstruction))
        assert recovered == mask
        assert outputs[2][2] == outputs[0][3]
        assert int(outputs[1][3]) == (int(outputs[2][3]) | int(outputs[2][0]))
        formal_signatures.add(tuple(outputs))
    assert len(formal_signatures) == 1024

    pair_class_counts = []
    for indices in combinations(range(len(words)), 2):
        pair_class_counts.append((len(partition(indices)), indices))
    max_pair_classes = max(count for count, _ in pair_class_counts)
    deletion_witnesses = []
    for removed in chosen:
        remaining = tuple(index for index in chosen if index != removed)
        collision = next(group[:2] for group in partition(remaining) if len(group) > 1)
        deletion_witnesses.append({
            "removed_word": words[removed],
            "remaining_words": [words[index] for index in remaining],
            "class_count": len(partition(remaining)),
            "collision": collision,
            "common_outputs": [values[collision[0]][index] for index in remaining],
            "removed_word_outputs": [values[mask][removed] for mask in collision],
        })

    return {
        "schema": "c5-minimum-observation-audit-B-v1",
        "source": {
            "path": "../frozen/certificate_v02.json",
            "sha256": sha256(raw).hexdigest(),
            "rows": ROWS,
            "four_output_rows": FOUR,
            "matrix_orientation": "destination_row_source_column",
            "word_execution_order": "left_to_right",
        },
        "scope": {
            "state_set": "exact_132_states_from_supplied_certificate",
            "probe_set": "all_15_words_over_P_R_of_length_at_most_3",
            "probe_execution": "each_word_runs_from_the_same_start_state_independently",
            "formal_extension": "supplied_Boolean_matrices_on_all_1024_formal_10_bit_masks",
            "graph_realizability_claim": False,
            "fixed_original_boundary_claim": False,
            "literal_count_reconstruction_claim": False,
        },
        "word_order": words,
        "depth_partition_counts": depth_counts,
        "minimum_cardinality": len(chosen),
        "all_minimum_subsets": [[words[index] for index in indices] for indices in minimum_indices],
        "epsilon_required": False,
        "exhaustive_subset_counts": subset_counts,
        "lower_bound_collision_witnesses": lower_bound_collisions,
        "pair_class_count_histogram": {str(count): frequency for count, frequency in sorted(Counter(count for count, _ in pair_class_counts).items())},
        "maximum_classes_from_two_probes": max_pair_classes,
        "all_two_probe_subsets_attaining_maximum": [[words[index] for index in indices] for count, indices in pair_class_counts if count == max_pair_classes],
        "selected_probe_deletion_witnesses": deletion_witnesses,
        "boolean_probe_formulas": formulas,
        "reconstruction": {
            "probe_names": {"a": "RR", "b": "PRR", "c": "RRR"},
            "component_positions": "one_based",
            "source_bit_reconstruction": reconstruction,
            "redundancy_identities": ["c3=a4", "b4=c4 OR c1"],
            "formal_masks_checked": 1024,
            "formal_masks_reconstructed": 1024,
            "formal_signature_count": len(formal_signatures),
            "formal_minimum_probe_count": 3,
            "formal_lower_bound": "two_four_bit_outputs_have_at_most_256_values_for_1024_masks",
        },
        "canonical_codebook": [
            {"state_mask": mask, "source_bits_in_row_order": "".join(str((mask >> bit) & 1) for bit in range(10)), "outputs": [values[mask][index] for index in chosen]}
            for mask in states
        ],
        "status": "PASS",
    }


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=here.parent / "frozen" / "certificate_v02.json")
    parser.add_argument("--output", type=Path, default=here / "minimum_observations.json", help="result path; writing requires a new path")
    parser.add_argument("--check", action="store_true", help="compare with the existing deterministic result instead of writing")
    args = parser.parse_args()
    rendered = json.dumps(build_result(args.certificate), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        assert args.output.read_text() == rendered, "stored result differs from independent replay"
    else:
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(rendered)
    print("PASS: unique minimum {RR, PRR, RRR}; 121 smaller-subset collisions; 132-state codebook; 1024 formal masks reconstructed")


if __name__ == "__main__":
    main()
