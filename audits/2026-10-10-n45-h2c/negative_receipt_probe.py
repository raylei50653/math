#!/usr/bin/env python3
"""Exercise actual worker delivery validation with one in-memory wrong receipt binding."""
import importlib.util
import json
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent.parent
WORKER = ROOT / 'audits/2026-10-10-n45-s-high2'
spec = importlib.util.spec_from_file_location('actual_high2_seal', WORKER / 'seal.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
target = WORKER / 'receipt.json'
wrong = json.loads(target.read_text())
wrong['manifest.json_sha256'] = '0' * 64
original = Path.read_text


def replacement(path, *args, **kwargs):
    return json.dumps(wrong) if path == target else original(path, *args, **kwargs)


with patch.object(Path, 'read_text', replacement):
    sys.argv = [str(WORKER / 'seal.py'), '--check-delivery']
    raise SystemExit(module.main())
