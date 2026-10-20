#!/usr/bin/env python3
"""Exclusive receipts and negative controls for the fixed C certificate."""
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
CHECK = HERE / "check.py"
CERT = HERE / "certificate.json.gz"


def create(path, payload):
    with path.open("xb") as stream:
        stream.write(payload)


def packed(value):
    return gzip.compress((json.dumps(value, indent=2, sort_keys=True) + "\n").encode(), mtime=0)


def main():
    cert_bytes = CERT.read_bytes()
    cert = json.loads(gzip.decompress(cert_bytes))
    receipts = []
    storage = []
    initial = HERE / "certificate.json"
    if initial.exists():
        data = initial.read_bytes()
        archived = HERE / "certificate-initial.json.gz"
        create(archived, gzip.compress(data, mtime=0))
        assert gzip.decompress(archived.read_bytes()) == data
        storage.append({
            "file": archived.name, "compressed_bytes": archived.stat().st_size,
            "compressed_sha256": hashlib.sha256(archived.read_bytes()).hexdigest(),
            "uncompressed_bytes": len(data), "uncompressed_sha256": hashlib.sha256(data).hexdigest(),
            "status": "initial certificate before pair-audit enrichment; exact bytes archived",
        })
        initial.unlink()
    data = gzip.decompress(cert_bytes)
    storage.append({
        "file": CERT.name, "compressed_bytes": len(cert_bytes),
        "compressed_sha256": hashlib.sha256(cert_bytes).hexdigest(),
        "uncompressed_bytes": len(data), "uncompressed_sha256": hashlib.sha256(data).hexdigest(),
        "status": "current authoritative replay certificate",
    })

    def run(label, args, expect, seed=None):
        env = dict(os.environ)
        if seed is not None:
            env["PYTHONHASHSEED"] = str(seed)
        command = [sys.executable, "-B", str(CHECK), *map(str, args)]
        result = subprocess.run(command, capture_output=True, env=env)
        create(HERE / (label + ".stdout.log"), result.stdout)
        create(HERE / (label + ".stderr.log"), result.stderr)
        assert (result.returncode == 0) == expect, (label, result.stderr.decode())
        receipts.append({
            "label": label, "returncode": result.returncode, "expected_success": expect,
            "hash_seed": seed, "stdout": label + ".stdout.log", "stderr": label + ".stderr.log",
        })

    run("replay-normal", [], True)
    run("replay-seed17", [], True, seed=17)

    def negative(label, mutate):
        altered = copy.deepcopy(cert)
        mutate(altered)
        destination = HERE / (label + ".json.gz")
        create(destination, packed(altered))
        run(label, [destination], False)

    def omit_empty(c):
        fibres = c["controls"][4]["complete_spoke_mask_fibres"]
        del fibres[next(key for key, values in fibres.items() if not values)]

    def omit_outer_odd_circle(c):
        control = c["controls"][4]
        index = control["degree555_double_pair_obstruction"]["pair_matching_rows"][0]
        row = control["matching_rows"][index]
        row["complement_cycles"].remove(max(row["complement_cycles"], key=len))

    def omit_odd_component(c):
        control = c["controls"][4]
        pair = next(r for r in control["safe_pair_audit"] if r["rho"] == 5 and r["tau"] == 8)
        pair["residual_components"] = [
            r for r in pair["residual_components"] if r["touched"] or not r["charge"]]
        pair["all_untouched_even"] = True

    def wrong_component_charge(c):
        c["controls"][4]["matching_rows"][40]["primal_components"]["components"][0]["charge"] ^= 1

    def wrong_shore_charge(c):
        c["controls"][4]["matching_rows"][40]["primal_components"]["region_tree"][0]["side_degree_charge"] ^= 1

    def invent_cut(c):
        fibres = c["controls"][4]["all_anchored_cut_masks_to_matching_rows"]
        fibres[fibres.index(None)] = 0

    negative("negative-missing-empty-spoke-fibre", omit_empty)
    negative("negative-omitted-outer-odd-cycle", omit_outer_odd_circle)
    negative("negative-omitted-untouched-odd-component", omit_odd_component)
    negative("negative-changed-component-charge", wrong_component_charge)
    negative("negative-changed-shore-charge", wrong_shore_charge)
    negative("negative-invented-cut-fibre", invent_cut)
    negative("negative-changed-literal-mark",
             lambda c: c["controls"][4]["marks"].__setitem__(2, [17, 19]))
    negative("negative-source-authority",
             lambda c: c.__setitem__("source_realizability", "triggered"))
    run("negative-exclusive-create", ["--write", CERT], False)
    assert CERT.read_bytes() == cert_bytes
    result = {
        "status": "PASS", "check_sha256": hashlib.sha256(CHECK.read_bytes()).hexdigest(),
        "certificate_sha256": hashlib.sha256(cert_bytes).hexdigest(),
        "storage": storage, "receipts": receipts,
        "source_realizability": "not triggered",
    }
    create(HERE / "VERIFICATION.json", (json.dumps(result, indent=2, sort_keys=True) + "\n").encode())
    print(json.dumps({"status": "PASS", "normal_and_seed17": 2, "rejected_negative_controls": 9,
                      "largest_compressed_certificate_bytes": max(r["compressed_bytes"] for r in storage)}))


if __name__ == "__main__":
    main()
