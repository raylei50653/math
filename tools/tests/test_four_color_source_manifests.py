"""Current source manifests must suffice to replay the new solver dependencies."""

from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import four_color_combined_experiment as combined
import four_color_cycle_context_experiment as contexts
import four_color_guarantee_audit as guarantee
import four_color_joint_propagation_experiment as joint


class SourceManifestTests(unittest.TestCase):
    def test_current_snapshots_replay_without_workspace_import_fallback(self):
        for experiment in (combined, contexts, guarantee, joint):
            with self.subTest(experiment=experiment.__name__), TemporaryDirectory() as directory:
                snapshot = Path(directory)
                manifest = experiment.source_hashes()
                for name in manifest:
                    if name.startswith("scripts/") and name.endswith(".py"):
                        target = snapshot / name
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes((ROOT / name).read_bytes())
                # Isolated Python ignores PYTHONPATH; only declared snapshot files
                # can supply project modules. Both new helpers are exercised.
                program = "\n".join((
                    "import sys",
                    "sys.path.insert(0, sys.argv[1])",
                    "from four_color_constraints import solve_constraints",
                    "from four_color_serialization import json_dumps, json_loads",
                    "g = {'vertices': [10**4300, -3, 7], 'edges': [[10**4300, -3], [-3, 7]]}",
                    "result = solve_constraints(g, use_joint_consistency=True, trace_limit=0)",
                    "assert result['status'] == 'colored'",
                    "assert result['colors'][0] != result['colors'][1]",
                    "assert result['colors'][1] != result['colors'][2]",
                    "assert json_loads(json_dumps(result))['graph']['vertices'] == g['vertices']",
                    "assert result['stats']['joint_consistency_queries'] > 0",
                ))
                completed = subprocess.run(
                    [sys.executable, "-I", "-c", program, str(snapshot / "scripts")],
                    cwd=snapshot, capture_output=True, text=True, timeout=30)
                self.assertEqual(completed.returncode, 0, completed.stderr)


if __name__ == "__main__":
    unittest.main()
