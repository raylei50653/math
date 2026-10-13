# Publication preservation verifier

Run the read-only preservation check from the repository root:

```sh
python3 -B audits/2026-10-13-k13-rank3-publication/verify.py --check
```

This checks the immutable K13 `SEAL.json` and rank3 `DELIVERY.json`. Their audit
files and archive blobs retain their repository paths; their shared-document
entries resolve to exact `source-docs/k13/` and `source-docs/rank3/` snapshots,
stored as gzip files with `.gz` appended to the original path. Hashes and byte
counts are checked after decompression; the publication seal covers the gzip bytes.
`IMPORTED.json` covers every imported audit file, including the original seals,
and the imported compressed blobs. Frozen inputs must equal their recorded
hashes and `git show` bytes at the original BASE. K13 archive additions must
match current records and the original archive snapshot; records present at the
publication import head must remain unchanged. Gzip streams are read to completion.

The original verifiers retain their original isolated-worktree meaning. This
publication verifier permits the repository HEAD and Git index to advance; it
does not rewrite an original seal or rerun mathematical enumeration.

After the connected publication file selection is final, create its separate
seal once:

```sh
python3 -B audits/2026-10-13-k13-rank3-publication/verify.py --seal
```

`WHITELIST.json` has the form `{"paths": ["repository-relative/path", ...]}`.
Paths can name files or directories; directories include their current files
and archived logical files, excluding caches and reproducible plantri binaries.
The selection must include its own whitelist, `ORIGINS.json`, `IMPORTED.json`,
and every imported original evidence file. `MANIFEST.json` is excluded from
itself. Creation uses exclusive mode and fails if the manifest already exists.

Once `MANIFEST.json` exists, `--check` also verifies the exact final whitelist
and all its hashes. Before creation, `--check` verifies preservation alone.
