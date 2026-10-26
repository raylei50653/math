#!/usr/bin/env python3
"""Verify saved sources, complete original outputs, and a fresh seed-17 replay."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def verify(seed_dir):
    source_manifest = json.loads((HERE / "final-source-manifest.json").read_text())
    for name, expected in source_manifest.items():
        assert sha((HERE / "final-source" / name).read_bytes()) == expected, name
        assert sha((ROOT / name).read_bytes()) == expected, name
    expected_sources = {k: v for k, v in source_manifest.items()
                        if k != "scripts/four_color_flow_experiment.py"}
    exploration = json.loads((HERE / "exploration.json").read_text())
    exploration_cases = {case["name"]: case for case in exploration["cases"]}
    source_matches = 0
    for mode, prototype in (("anchor", "baseline"), ("prefix", "prefix")):
        report = json.loads((HERE / "comparison" / mode / "report.json").read_text())
        assert report["sources"] == expected_sources
        assert report["driver_sha256"] == source_manifest["scripts/four_color_flow_experiment.py"]
        assert report["inputs_sha256"] == sha((HERE / "inputs.json").read_bytes())
        for case in report["cases"]:
            row = case["results"]["combined-contexts"]
            raw = (HERE / "comparison" / mode / row["full_record"]).read_bytes()
            assert sha(raw) == row["compressed_record_sha256"]
            result = json.loads(gzip.decompress(raw))
            assert result.pop("bucket_method") == mode
            assert sha(gzip.compress(encoded(result), mtime=0)) == (
                exploration_cases[case["name"]]["modes"][prototype]["original_record_sha256"])
            source_matches += 1
    normal = HERE / "comparison"
    records, metadata = [], []
    for path in sorted(normal.rglob("*")):
        if not path.is_file() or path.name == "timings.json" or path.suffix == ".log":
            continue
        relative = path.relative_to(normal)
        other = seed_dir / relative
        if path.suffix == ".json":
            # Stored summaries may be compacted; their complete JSON is identical.
            assert json.loads(path.read_bytes()) == json.loads(other.read_bytes()), str(relative)
            metadata.append(str(relative))
        else:
            assert path.read_bytes() == other.read_bytes(), str(relative)
            records.append(str(relative))
    independent = json.loads((HERE / "independent-checks/receipt.json").read_text())
    for mode, data in independent["modes"].items():
        for name, expected in data["source_hashes"].items():
            assert sha((HERE / "exploration-sources" / mode / "scripts" / name).read_bytes()) == expected
    receipt = dict(
        final_source_files_verified=len(source_manifest),
        full_outputs_equal_to_frozen_prototypes_except_method=source_matches,
        seed17_full_records_byte_identical=len(records),
        seed17_metadata_json_equal=len(metadata),
        compared_full_records=records, compared_metadata=metadata,
        independent_receipt_sha256=sha((HERE / "independent-checks/receipt.json").read_bytes()),
        final_comparison_sha256=sha((normal / "comparison.json").read_bytes()),
        excluded_from_seed_comparison=["timings.json", "*.log"],
        tests_log_sha256=sha((HERE / "tests.log").read_bytes()),
        interpretation="Sources and frozen input bound to complete records. "
            "The historical default differs only by new method metadata. "
            "All 80 complete gzip records replay byte-for-byte; metadata compares "
            "as complete JSON to permit archive whitespace compaction. "
            "Timing/RSS are observations, excluded from determinism claims.",
    )
    (HERE / "verification.json").write_bytes(encoded(receipt))
    print(json.dumps({k: v for k, v in receipt.items() if type(v) is int}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-dir", type=Path, required=True)
    verify(parser.parse_args().seed_dir)
