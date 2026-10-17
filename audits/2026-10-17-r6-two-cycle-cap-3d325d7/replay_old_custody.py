#!/usr/bin/env python3
"""Replay the old publication checker against its exact published BASE bytes."""

import io
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile


REPO = Path(__file__).resolve().parents[2]
BASE = "3d325d7197aa05815c71bedc52c1b253d736c7bb"
PUBLICATION = "docs/history/2026-10-17-r6-active-f-seven-publication"
PATHS = ["audits/2026-10-17-r6-active-f-seven-ffea555", PUBLICATION,
         "docs/STATUS.md", "docs/c5_kempe_guide.md"]


def main():
    archive = subprocess.check_output(["git", "archive", BASE, *PATHS], cwd=REPO)
    git_dir = subprocess.check_output(["git", "rev-parse", "--absolute-git-dir"],
                                      cwd=REPO, text=True).strip()
    with tempfile.TemporaryDirectory(prefix="r6-old-custody-") as temporary:
        with tarfile.open(fileobj=io.BytesIO(archive)) as snapshot:
            snapshot.extractall(temporary, filter="data")
        # git merge-base is read-only; all inspected files are archived BASE bytes.
        env = {**os.environ, "GIT_DIR": git_dir, "GIT_WORK_TREE": temporary}
        subprocess.run(["python3", "-B", PUBLICATION + "/check_custody.py"],
                       cwd=temporary, env=env, check=True)


if __name__ == "__main__":
    main()
