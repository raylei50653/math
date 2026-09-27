"""Run as `python3 tools/docgraph <command>` or `python3 -m docgraph <command>`."""
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "docgraph"

from docgraph.cli import main  # noqa: E402

sys.exit(main())
