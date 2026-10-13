#!/usr/bin/env python3
"""Verify preservation of the two original deliveries and a publication seal.

The original seals are immutable. Their shared-document entries resolve to
source-docs snapshots; audit entries and archive blobs retain repository paths.
This verifier does not recompute mathematical certificates or inspect Git index
state. --check is read-only; --seal creates MANIFEST.json exclusively once.
"""

import argparse
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zlib


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BASE = "50d5474f2446403f3b3001d5943571184c8c9936"
IMPORT_HEAD = "5211a92178dffd9d7cd3f883a19d8a3f03932d07"
SOURCES = {
    "k13": ("audits/2026-10-13-k13-collar-50d5474", "SEAL.json"),
    "rank3": ("audits/2026-10-13-w5-rank3-contractible-50d5474", "DELIVERY.json"),
}
EXCLUDED_EXECUTABLES = {"plantri", "plantri_min4_filter"}
CHUNK = 1 << 20


class VerificationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def decode_json(data):
    return json.loads(data, object_pairs_hook=unique_object)


def relative(value):
    require(isinstance(value, str) and value, "empty or non-string path")
    path = PurePosixPath(value)
    require(not path.is_absolute() and ".." not in path.parts,
            f"unsafe repository path: {value}")
    require(str(path) == value and value != ".", f"noncanonical path: {value}")
    return value


def physical(rel):
    path = REPO / relative(rel)
    require(path.resolve().is_relative_to(REPO.resolve()), f"path escapes repository: {rel}")
    require(not path.is_symlink(), f"symlink is not sealed evidence: {rel}")
    return path


def excluded(rel):
    path = PurePosixPath(rel)
    return ("__pycache__" in path.parts or path.suffix == ".pyc"
            or path.name in EXCLUDED_EXECUTABLES)


def below(rel, prefix):
    return rel.startswith(prefix + "/")


def git_bytes(commit, rel):
    return subprocess.check_output(["git", "show", commit + ":" + relative(rel)], cwd=REPO)


class Evidence:
    def __init__(self):
        self.archive = decode_json((REPO / "audits/ARCHIVE.json").read_bytes())
        self.cache = {}
        self.gzip_count = 0
        self.snapshot_prefix = str(HERE.relative_to(REPO)) + "/source-docs/"

    def snapshot_gzip(self, rel):
        if rel.startswith(self.snapshot_prefix):
            compressed = physical(rel + ".gz")
            if compressed.is_file():
                return compressed
        return None

    def bytes(self, rel):
        path = physical(rel)
        if path.is_file():
            return path.read_bytes()
        compressed = self.snapshot_gzip(rel)
        if compressed is not None:
            self.fingerprint(rel + ".gz")
            return gzip.decompress(compressed.read_bytes())
        record = self.archive["files"].get(rel)
        require(record is not None, f"missing evidence: {rel}")
        blob = self.archive["blobs"].get(record["sha256"])
        require(blob is not None, f"missing archive blob record: {rel}")
        return gzip.decompress(physical(blob["path"]).read_bytes())

    def json(self, rel):
        return decode_json(self.bytes(rel))

    def fingerprint(self, rel):
        relative(rel)
        if rel in self.cache:
            return self.cache[rel]
        path = physical(rel)
        archived = not path.is_file()
        compressed = self.snapshot_gzip(rel) if archived else None
        if compressed is not None:
            self.fingerprint(rel + ".gz")
            stream = gzip.open(compressed, "rb")
        elif archived:
            record = self.archive["files"].get(rel)
            require(record is not None, f"missing evidence: {rel}")
            blob = self.archive["blobs"].get(record["sha256"])
            require(blob is not None, f"missing archive blob record: {rel}")
            self.check(blob["path"], blob)
            stream = gzip.open(physical(blob["path"]), "rb")
        else:
            stream = path.open("rb")
        digest, size = hashlib.sha256(), 0
        with stream:
            for chunk in iter(lambda: stream.read(CHUNK), b""):
                digest.update(chunk)
                size += len(chunk)
        result = {"sha256": digest.hexdigest(), "bytes": size}
        self.cache[rel] = result
        if archived and compressed is None:
            self.check(rel, record)
        if not archived and path.suffix == ".gz":
            with gzip.open(path, "rb") as stream:
                for _ in iter(lambda: stream.read(CHUNK), b""):
                    pass
            self.gzip_count += 1
        return result

    def check(self, rel, record):
        require(isinstance(record, dict), f"invalid hash record: {rel}")
        expected = {"sha256": record.get("sha256"), "bytes": record.get("bytes")}
        require(isinstance(expected["bytes"], int) and expected["bytes"] >= 0,
                f"invalid byte count: {rel}")
        require(isinstance(expected["sha256"], str) and len(expected["sha256"]) == 64
                and all(c in "0123456789abcdef" for c in expected["sha256"]),
                f"invalid SHA-256: {rel}")
        require(self.fingerprint(rel) == expected, f"sealed bytes differ: {rel}")


def seal_records(obj):
    records = obj["files"]
    if isinstance(records, dict):
        return {relative(rel): record for rel, record in records.items()}
    require(isinstance(records, list), "seal files must be a map or list")
    result = {}
    for record in records:
        rel = relative(record["path"])
        require(rel not in result, f"duplicate seal path: {rel}")
        result[rel] = record
    return result


def frozen_input(evidence, prefix, record, base):
    rel = relative(record["path"])
    frozen_rel = prefix + "/frozen/" + rel
    original = git_bytes(base, rel)
    require(evidence.bytes(frozen_rel) == original, f"frozen BASE bytes differ: {rel}")
    evidence.check(frozen_rel, record)


def verify_preservation(evidence):
    publication = str(HERE.relative_to(REPO))
    origins = evidence.json(publication + "/ORIGINS.json")
    require(origins["base"] == BASE, "unexpected frozen BASE")
    require(origins["import_head"] == IMPORT_HEAD, "unexpected publication import head")
    configured = {}
    for source in origins["sources"]:
        label = source.get("label", source.get("id"))
        require(label in SOURCES and label not in configured, "unexpected or duplicate source")
        configured[label] = (source["prefix"], source["seal"])
    require(configured == SOURCES, "origin source paths differ")

    expected_imported = set()
    sealed_count = 0
    for label, (prefix, seal_name) in SOURCES.items():
        seal_rel = prefix + "/" + seal_name
        seal = evidence.json(seal_rel)
        require(seal["base"] == BASE, f"original seal BASE differs: {label}")
        expected_imported.add(seal_rel)
        for rel, record in seal_records(seal).items():
            if below(rel, prefix) or below(rel, "audits/.archive/blobs"):
                destination = rel
                expected_imported.add(rel)
            else:
                destination = publication + "/source-docs/" + label + "/" + rel
            evidence.check(destination, record)
            sealed_count += 1

    imported = evidence.json(publication + "/IMPORTED.json")["files"]
    require(isinstance(imported, dict), "IMPORTED files must be a map")
    require(set(imported) == expected_imported, "IMPORTED inventory differs from original seals")
    for rel, record in imported.items():
        require(not excluded(rel), f"excluded executable/cache in import inventory: {rel}")
        evidence.check(rel, record)
    # Detect undeclared audit files, including files later packed into archive blobs.
    for prefix, _ in SOURCES.values():
        found = {str(path.relative_to(REPO)) for path in physical(prefix).rglob("*")
                 if path.is_file() and not excluded(str(path.relative_to(REPO)))}
        found.update(rel for rel in evidence.archive["files"]
                     if below(rel, prefix) and not excluded(rel))
        expected = {rel for rel in imported if below(rel, prefix)}
        require(found == expected, f"undeclared or missing files in {prefix}")

    kprefix = SOURCES["k13"][0]
    inputs = evidence.json(kprefix + "/INPUTS.json")
    require(inputs["base"] == BASE, "K13 input BASE differs")
    for rel, digest in inputs["sha256"].items():
        original = git_bytes(BASE, rel)
        frozen_input(evidence, kprefix,
                     {"path": rel, "sha256": digest, "bytes": len(original)}, BASE)
    rprefix = SOURCES["rank3"][0]
    base = evidence.json(rprefix + "/BASE.json")
    catalogue = evidence.json(rprefix + "/CATALOGUE_INPUT.json")
    require(base["base"] == catalogue["base"] == BASE, "rank3 input BASE differs")
    for record in base["inputs"] + [catalogue]:
        frozen_input(evidence, rprefix, record, BASE)

    baseline = decode_json(git_bytes(IMPORT_HEAD, "audits/ARCHIVE.json"))
    for group in ("files", "blobs"):
        for key, record in baseline[group].items():
            require(evidence.archive[group].get(key) == record,
                    f"pre-import archive record differs: {group}/{key}")
    additions = evidence.json(kprefix + "/ARCHIVE_ADDITIONS.json")
    snapshot = evidence.json(publication + "/source-docs/k13/audits/ARCHIVE.json")
    for rel, record in additions.items():
        require(evidence.archive["files"].get(rel) == record,
                f"K13 archive addition differs: {rel}")
        require(snapshot["files"].get(rel) == record,
                f"K13 source archive addition differs: {rel}")
        digest = record["sha256"]
        require(evidence.archive["blobs"].get(digest) == snapshot["blobs"].get(digest),
                f"K13 archive blob record differs: {digest}")
        evidence.check(rel, record)
        blob = evidence.archive["blobs"][digest]
        evidence.check(blob["path"], blob)
        data = gzip.decompress(physical(blob["path"]).read_bytes())
        require(len(data) == record["bytes"] and hashlib.sha256(data).hexdigest() == digest,
                f"K13 archived content differs: {rel}")
    return {"imported_files": len(imported), "original_sealed_files": sealed_count,
            "frozen_inputs": len(inputs["sha256"]) + len(base["inputs"]) + 1,
            "archive_additions": len(additions), "old_archive_records_unchanged": True}


def publication_manifest(evidence):
    publication = str(HERE.relative_to(REPO))
    whitelist_rel = publication + "/WHITELIST.json"
    paths = evidence.json(whitelist_rel)["paths"]
    require(isinstance(paths, list) and len(paths) == len(set(paths)), "invalid or duplicate whitelist")
    selected = set()
    manifest_rel = publication + "/MANIFEST.json"
    for rel in paths:
        path = physical(rel)
        require(rel != manifest_rel, "MANIFEST must not include itself")
        if path.is_dir():
            selected.update(str(p.relative_to(REPO)) for p in path.rglob("*")
                            if p.is_file() and not excluded(str(p.relative_to(REPO))))
            selected.update(r for r in evidence.archive["files"]
                            if below(r, rel) and not excluded(r))
        else:
            require(not excluded(rel), f"excluded executable/cache in whitelist: {rel}")
            selected.add(rel)
    selected.discard(manifest_rel)
    require(whitelist_rel in selected, "WHITELIST must seal its own selection")
    imported_rel = publication + "/IMPORTED.json"
    require(imported_rel in selected and publication + "/ORIGINS.json" in selected,
            "publication metadata missing from whitelist")
    require(set(evidence.json(imported_rel)["files"]).issubset(selected),
            "imported original evidence missing from publication whitelist")
    return {"schema": 1, "base": BASE, "import_head": IMPORT_HEAD,
            "scope": "publication whitelist; original source seals preserved separately",
            "files": {rel: evidence.fingerprint(rel) for rel in sorted(selected)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="read-only verification (default)")
    mode.add_argument("--seal", action="store_true", help="create final MANIFEST.json once")
    args = parser.parse_args()
    evidence = Evidence()
    summary = verify_preservation(evidence)
    manifest_path = HERE / "MANIFEST.json"
    if args.seal or manifest_path.exists():
        manifest = publication_manifest(evidence)
        data = (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode()
        if args.seal:
            with manifest_path.open("xb") as stream:
                stream.write(data)
            summary["manifest"] = "created"
        else:
            require(manifest_path.read_bytes() == data, "publication MANIFEST differs")
            summary["manifest"] = "verified"
        summary["publication_files"] = len(manifest["files"])
    else:
        summary["manifest"] = "not yet sealed"
    summary.update(status="PASS", mode="seal" if args.seal else "check",
                   gzip_integrity=True, gzip_files=evidence.gzip_count,
                   mathematical_recomputation=False)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (VerificationError, OSError, EOFError, ValueError, KeyError, TypeError, zlib.error,
            subprocess.CalledProcessError) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, sort_keys=True), file=sys.stderr)
        sys.exit(1)
