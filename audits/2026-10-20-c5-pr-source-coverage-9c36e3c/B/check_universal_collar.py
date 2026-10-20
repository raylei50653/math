#!/usr/bin/env python3
"""Check a fixed 17-push collar sending every nonempty support to 1023.

No shortest-word claim. --check is read only; generation is exclusive.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import random
from check_transition_obstruction import compile_local

HERE = Path(__file__).resolve().parent
DEFAULT = HERE / "universal_collar.json"
WORD = "RRR" + "PPR" * 4 + "P" + "PRP" * 4


def build(seed):
    rows, matrices, _ = compile_local()

    def step(mask, op):
        return sum(int(any(c and mask >> j & 1 for j, c in enumerate(row))) << i
                   for i, row in enumerate(matrices[op]))

    def word_image(mask, word):
        for op in word:
            mask = step(mask, op)
        return mask

    states = [1 << i for i in range(10)]
    trace = [states]
    for op in WORD:
        states = [step(s, op) for s in states]
        trace.append(states)
    assert len(WORD) == 28 and WORD.count("P") == 17
    assert states == [1023] * 10
    assert word_image(0, WORD) == 0
    domain = list(range(1, 1024))
    if seed is not None:
        random.Random(seed).shuffle(domain)
    assert all(word_image(s, WORD) == 1023 for s in domain)
    # Each Boolean matrix preserves joins: independently check this on all
    # masks by reconstructing from their singleton contributions.
    for op in ("P", "R"):
        singleton_images = [step(1 << i, op) for i in range(10)]
        for s in range(1024):
            reconstructed = 0
            for i in range(10):
                if s >> i & 1:
                    reconstructed |= singleton_images[i]
            assert step(s, op) == reconstructed
    # A failed tempting simpler word is retained as an exact finite cycle,
    # not represented as evidence that no other fixed word exists.
    pr = [1 << i for i in range(10)]
    pr_trace = [pr]
    for _ in range(14):
        pr = [word_image(s, "PR") for s in pr]
        pr_trace.append(pr)
    assert pr_trace[10] == pr_trace[14]
    assert all(any(s != 1023 for s in state) for state in pr_trace[:14])
    assert all(step(1023, op) == 1023 for op in ("P", "R"))
    return {
        "schema": "c5-pr-fixed-universal-collar/v1",
        "authority": "Formal support identity; disk interpretation uses frozen P/R semantics.",
        "word": WORD,
        "word_factored": "RRR (PPR)^4 P (PRP)^4",
        "letter_count": len(WORD),
        "push_count": WORD.count("P"),
        "domain_nonempty_masks": 1023,
        "common_image": 1023,
        "empty_mask_image": 0,
        "singleton_images_by_prefix": trace,
        "join_preservation_checked_on_all_masks": True,
        "direct_check_on_all_nonempty_masks": True,
        "PR_power_negative_control": {
            "singleton_images_n0_through_n14": pr_trace,
            "cycle_start_n": 10,
            "cycle_period": 4,
            "all_n_non_synchronizing": True,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path, default=DEFAULT)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    result = build(args.seed)
    encoded = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.check:
        assert args.certificate.read_text() == encoded, "Certificate mismatch."
    else:
        with args.certificate.open("x") as handle:
            handle.write(encoded)
    print(json.dumps({
        "check": args.check, "seed": args.seed, "push_count": 17,
        "all_nonempty_masks_to_1023": True, "PR_power_synchronizes": False,
        "certificate_sha256": sha256(encoded.encode()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
