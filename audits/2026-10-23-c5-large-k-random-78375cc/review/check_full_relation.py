#!/usr/bin/env python3
"""Exact independent verifier for graphs claiming the full ten-row relation.

One proper complete coloring for each fixed row proves Sigma=1023.  There are
no absent rows to refute and no need to rediscover these witnesses by search.
"""
from hashlib import sha256
import json
from pathlib import Path
import sys

import independent_check as checker


def main():
    sample_path, output_path = map(Path, sys.argv[1:])
    data = sample_path.read_bytes()
    catalogue_path = Path(__file__).resolve().parent.parent / "frozen/artifacts/c5_cells/cells.json"
    catalogue_bytes = catalogue_path.read_bytes()
    catalogue = json.loads(catalogue_bytes)
    assert len(catalogue["cells"]) == 132 and "1023" in catalogue["cells"]
    assert catalogue["pattern_order"] == [list(map(int, w)) for w in checker.PATTERNS]
    graphs = witnesses = 0
    for line in data.splitlines():
        if not line:
            continue
        sample = json.loads(line)
        checker.check_disk(sample)
        assert sample["sigma"] == 1023
        assert sample["rows"] == list(checker.PATTERNS)
        assert len(sample["witnesses"]) == 10
        for word, colors in zip(checker.PATTERNS, sample["witnesses"]):
            checker.check_witness(colors, sample["n"], sample["boundary"], word, sample["edges"])
            witnesses += 1
        graphs += 1
    result = dict(schema="c5-independent-full-relation-review-v1",
                  complete_source_sigma_verifications=graphs,
                  independently_verified_literal_full_witnesses=witnesses,
                  exact_sigma_histogram={"1023": graphs},
                  no_rejected_rows_to_refute=True, unresolved_decisions=0,
                  catalogue_outside_verified=[],
                  samples_sha256=sha256(data).hexdigest(),
                  catalogue_sha256=sha256(catalogue_bytes).hexdigest(),
                  checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  topology_and_witness_dependency_sha256=sha256(Path(checker.__file__).read_bytes()).hexdigest())
    with output_path.open("x") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
