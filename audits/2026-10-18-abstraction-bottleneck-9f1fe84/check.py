#!/usr/bin/env python3
"""Read-only replay of the abstraction audit; no source enumeration."""
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def frozen_inputs():
    count = 0
    for folder in (HERE, HERE / "A", HERE / "B"):
        manifest = json.loads((folder / "INPUTS.json").read_text())
        for item in manifest.get("inputs", manifest.get("additional_inputs", [])):
            frozen = folder / item.get("frozen", "frozen/" + item["path"])
            data = frozen.read_bytes()
            assert hashlib.sha256(data).hexdigest() == item["sha256"]
            original = subprocess.check_output(
                ["git", "show", manifest["base"] + ":" + item["path"]], cwd=ROOT
            )
            assert data == original
            count += 1
    return count


def independent_four_queries():
    data = json.loads((HERE / "A/frozen/artifacts/c5_cells/cells.json").read_text())
    known = {int(key) for key in data["cells"]}
    assert len(known) == 132
    results = {}
    for target, expected in ((932, 5), (933, 2), (941, 1)):
        for size in range(5):
            certificates = []
            for coordinates in itertools.combinations(range(10), size):
                observation = tuple(bool(target & (1 << i)) for i in coordinates)
                projections = {
                    tuple(bool(mask & (1 << i)) for i in coordinates) for mask in known
                }
                if observation not in projections:
                    certificates.append(coordinates)
            if certificates:
                assert size == 4 and len(certificates) == expected
                assert (1, 4, 6, 9) in certificates
                results[str(target)] = {"minimum": size, "number": len(certificates)}
                break
        else:
            raise AssertionError("missing four-query certificate")
    cylinder = {mask for mask in range(1024) if mask & 594 == 512}
    assert len(cylinder) == 64 and not cylinder & known
    for removed, witness in ((1, 774), (4, 564), (6, 960), (9, 165)):
        scope = 594 ^ (1 << removed)
        assert witness in known and witness & scope == 512 & scope
    return results


def replay(relative_script, certificate=None):
    run = subprocess.run(
        [sys.executable, "-B", str(HERE / relative_script)],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    assert not run.stderr
    if certificate:
        assert json.loads(run.stdout) == json.loads((HERE / certificate).read_text())
    return "PASS"


def corrupted_certificate_control():
    with tempfile.TemporaryDirectory(prefix="math-four-query-negative-") as tmp:
        folder = Path(tmp)
        for filename in ("check_signed_interface.py", "INPUTS.json"):
            shutil.copyfile(HERE / "A" / filename, folder / filename)
        (folder / "frozen").symlink_to(HERE / "A/frozen", target_is_directory=True)
        cert = json.loads((HERE / "A/signed_interface_certificate.json").read_text())
        cert["common_interface"]["accepted_query_mask"] = 0
        (folder / "signed_interface_certificate.json").write_text(json.dumps(cert))
        run = subprocess.run(
            [sys.executable, "-B", str(folder / "check_signed_interface.py")],
            capture_output=True, text=True,
        )
        assert run.returncode != 0 and "AssertionError" in run.stderr
    return "rejected"


def main():
    result = {
        "scope": "paper abstraction controls; source realization and closure not established",
        "frozen_inputs_equal_base": frozen_inputs(),
        "independent_four_queries": independent_four_queries(),
        "A": replay("A/check_signed_interface.py"),
        "B": replay("B/check_interface.py", "B/controls.json"),
        "C": replay("C/check.py", "C/controls.json"),
        "corrupted_A_certificate": corrupted_certificate_control(),
    }
    inventory = HERE / "OUTPUTS.sha256"
    if inventory.exists():
        for line in inventory.read_text().splitlines():
            digest, relative = line.split("  ", 1)
            assert hashlib.sha256((HERE / relative).read_bytes()).hexdigest() == digest
        result["sealed_outputs"] = "PASS"
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
