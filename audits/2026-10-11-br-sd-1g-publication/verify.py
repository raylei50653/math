#!/usr/bin/env python3
"""Read-only publication custody for the unchanged BR-SD-1g research audit.

The original fresh-BASE verifier and all frozen bytes remain untouched.
This entry checks actual descendant HEAD/index independently of working files.
"""
import argparse
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
from urllib.parse import unquote, urlsplit

PUB = Path(__file__).resolve().parent
ROOT = PUB.parents[1]
AUDIT = ROOT / "audits/2026-10-11-br-sd-1g-dbdc4c35"
BASE = "dbdc4c35f785519c8e3cb0260807f0d2feb82469"
ORIGINAL_SEAL_SHA = "d3952f60eaba362762d3555b800ba9a03eeaf5171c0404fbea70cfc330ec8edc"
PREFIXES = tuple(p.relative_to(ROOT).as_posix() + "/" for p in (AUDIT, PUB))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def git(*args):
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True)
    if result.returncode:
        raise ValueError(f"git {args!r} failed with exit {result.returncode}")
    return result.stdout


def inventory(directory, exclude=()):
    rows = []
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"unexpected symlink: {path}")
        if path.is_file():
            name = path.relative_to(directory).as_posix()
            if name not in exclude:
                data = path.read_bytes()
                rows.append({"path": name, "sha256": sha(data), "size": len(data),
                             "mode": path.stat().st_mode & 0o777, "symlink": False})
    return rows


def tracked_content(records, prefix, reference, required):
    if reference == "HEAD":
        listing = git("ls-tree", "-r", "-z", "HEAD", "--", prefix)
    else:
        listing = git("ls-files", "--stage", "-z", "--", prefix)
    modes = {}
    for item in listing.split(b"\0"):
        if item:
            metadata, path = item.split(b"\t", 1)
            fields = metadata.decode().split()
            if reference == "index" and fields[2] != "0":
                raise ValueError("unmerged index entry")
            modes[path.decode()] = fields[0]
    names = set(modes)
    expected = {prefix + "/" + x["path"] for x in records}
    if required or names:
        if names != expected:
            raise ValueError(f"incomplete or extra {reference} files: {prefix}")
        for row in records:
            path = prefix + "/" + row["path"]
            blob = git("show", ("HEAD:" if reference == "HEAD" else ":") + path)
            expected_mode = "100755" if row["mode"] & 0o111 else "100644"
            if sha(blob) != row["sha256"] or len(blob) != row["size"] or modes[path] != expected_mode:
                raise ValueError(f"{reference} byte drift: {path}")
    return len(names)


def allowed_diff(*args):
    for row in git("diff", "--name-status", "--no-renames", *args).decode().splitlines():
        status, path = row.split("\t", 1)
        if status != "A" or not path.startswith(PREFIXES):
            raise ValueError(f"outside publication additions: {row}")


def validate_manifest(manifest, payloads):
    keys = {"schema", "base", "original_seal_sha256", "parent_status",
            "new_unconditional_closures", "payload_manifest_sha256", "payloads"}
    if (set(manifest) != keys or manifest["schema"] != "br-sd-1g-publication-v1"
            or manifest["base"] != BASE or manifest["original_seal_sha256"] != ORIGINAL_SEAL_SHA
            or manifest["parent_status"] != "OPEN" or manifest["new_unconditional_closures"] != 0
            or manifest["payload_manifest_sha256"] != sha(canonical(manifest["payloads"]))
            or manifest["payloads"] != payloads):
        raise ValueError("publication manifest corruption or inventory drift")


def check(preseal=False, require_tracked=False):
    head = git("rev-parse", "HEAD").decode().strip()
    git("merge-base", "--is-ancestor", BASE, head)
    # Committed, staged and working states are distinct checks: a local undo
    # cannot conceal an out-of-scope change already present in HEAD.
    allowed_diff(BASE, "HEAD")
    allowed_diff("--cached")
    for record in git("status", "--porcelain=v1", "-z", "--untracked-files=all").split(b"\0"):
        if record:
            if record[:2] not in (b"??", b"A ") or not record[3:].decode().startswith(PREFIXES):
                raise ValueError(f"unexpected working/index state: {record!r}")
    original_bytes = (AUDIT / "SEAL.json").read_bytes()
    if sha(original_bytes) != ORIGINAL_SEAL_SHA:
        raise ValueError("original research seal drift")
    seal = json.loads(original_bytes)
    if (seal["base"] != BASE or seal["parent_status"] != "OPEN"
            or seal["new_unconditional_closures"] != 0 or len(seal["payloads"]) != 159
            or seal["payload_manifest_sha256"] != sha(canonical(seal["payloads"]))
            or inventory(AUDIT, {"SEAL.json"}) != seal["payloads"]):
        raise ValueError("original 159-payload custody drift")
    original_files = inventory(AUDIT)
    if len(original_files) != 160:
        raise ValueError("original research file coverage drift")
    inputs = json.loads((AUDIT / "authority/INPUTS.json").read_text())
    if inputs["base"] != BASE or len(inputs["inputs"]) != 31:
        raise ValueError("authority identity drift")
    for row in inputs["inputs"]:
        blob = git("show", BASE + ":" + row["path"])
        if (sha(blob) != row["sha256"] or len(blob) != row["size"]
                or (AUDIT / row["frozen"]).read_bytes() != blob
                or (ROOT / row["path"]).read_bytes() != blob):
            raise ValueError(f"frozen/BASE/live authority drift: {row['path']}")
    old = json.loads((AUDIT / "authority/OLD-CUSTODY.json").read_text())
    directories = {"audits/2026-10-11-br-sd-1a-0f181045", "audits/2026-10-11-br-sd-1c-fd6e1112",
                   "audits/2026-10-11-br-sd-1e-337d018b"}
    observed = []
    for directory in sorted(directories):
        observed.extend({**row, "path": directory + "/" + row["path"]} for row in inventory(ROOT / directory))
    if len(old) != 313 or sorted(observed, key=lambda r: r["path"]) != sorted(old, key=lambda r: r["path"]):
        raise ValueError("old three-audit custody drift")
    paper = json.loads((AUDIT / "agents/paper/ACCEPTANCE.json").read_text())
    if (paper["verdict"] != "accepted scoped paper exclusion" or paper["base"] != BASE
            or paper["parent_status"] != "OPEN" or paper["new_unconditional_closures"] != 0
            or paper["canonical_adoption_authorized"] is not False
            or paper["actual_target_source_status"] != "not triggered"
            or set(paper["accepted_hashes"]) != {"PROOF.md", "MAPPING.md", "REPORT.md"}):
        raise ValueError("paper acceptance scope drift")
    for name, expected in paper["accepted_hashes"].items():
        if sha((AUDIT / name).read_bytes()) != expected:
            raise ValueError(f"reviewed paper bytes drift: {name}")
    recorded = json.loads((AUDIT / "logs/CHECKS.json").read_text())
    if len(recorded) != 22 or any(r["exit_code"] != r["expected_exit_code"] for r in recorded):
        raise ValueError("recorded research check drift")
    for row in recorded:
        for field in ("stdout", "stderr"):
            if sha((AUDIT / row[field + "_path"]).read_bytes()) != row[field + "_sha256"]:
                raise ValueError("recorded output digest mismatch")
    manifest_path = PUB / "MANIFEST.json"
    if preseal:
        if manifest_path.exists() or require_tracked:
            raise ValueError("preseal mode only allowed before publication manifest creation")
        publication_files = inventory(PUB)
    else:
        validate_manifest(json.loads(manifest_path.read_text()), inventory(PUB, {"MANIFEST.json"}))
        accepted = json.loads((PUB / "agents/ACCEPTANCE.json").read_text())
        if accepted["verdict"] != "accepted publication custody" or accepted["blocking_findings"] != 0:
            raise ValueError("publication independent acceptance missing")
        if set(accepted["accepted_hashes"]) != {"verify.py", "PUBLICATION.md"}:
            raise ValueError("publication acceptance hash coverage incomplete")
        for name, expected in accepted["accepted_hashes"].items():
            if sha((PUB / name).read_bytes()) != expected:
                raise ValueError(f"publication reviewed bytes drift: {name}")
        publication_files = inventory(PUB)
    helper = runpy.run_path(str(ROOT / "scripts/check_docs.py"), run_name="publication_link_helper")
    links = 0
    for directory in (AUDIT, PUB):
        for path in directory.rglob("*.md"):
            if "authority" in path.relative_to(directory).parts:
                continue
            for line, destination in helper["links"](path.read_text()):
                url = urlsplit(destination)
                if url.scheme or url.netloc:
                    continue
                target = (path.parent / unquote(url.path)).resolve() if url.path else path
                if not target.exists():
                    if preseal and target == manifest_path and not url.fragment:
                        continue
                    raise ValueError(f"missing local link: {path}:{line}: {destination}")
                if url.fragment and target.suffix == ".md" and unquote(url.fragment) not in helper["anchors"](target.read_text()):
                    raise ValueError(f"missing anchor: {path}:{line}: {destination}")
                links += 1
    index_counts, head_counts = [], []
    for directory, rows in ((AUDIT, original_files), (PUB, publication_files)):
        prefix = directory.relative_to(ROOT).as_posix()
        index_counts.append(tracked_content(rows, prefix, "index", require_tracked))
        head_counts.append(tracked_content(rows, prefix, "HEAD", require_tracked))
    return {"status": "publication custody verified", "base": BASE, "actual_head": head,
            "preseal": preseal, "original_files": 160, "original_payloads": 159,
            "authority_inputs": 31, "old_custody_files": 313, "recorded_research_checks": 22,
            "publication_files": len(publication_files), "index_file_counts": index_counts,
            "HEAD_file_counts": head_counts, "local_links_checked": links,
            "original_seal_sha256": ORIGINAL_SEAL_SHA, "parent_status": "OPEN",
            "new_unconditional_closures": 0, "source_status": "not triggered",
            "claim": "publication custody only; no mathematical adoption"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.add_argument("--preseal", action="store_true")
    parser.add_argument("--require-tracked", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.preseal, args.require_tracked), sort_keys=True))
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
