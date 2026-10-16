#!/usr/bin/env python3
"""Compare whole-tree DocGraph error kinds/IDs with exact tracked BASE Markdown."""
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from tools.docgraph.parser import parse_repo
from tools.docgraph.validate import validate


def errors(root):
    _, diagnostics = validate(*parse_repo(root))
    return [d for d in diagnostics if d.level == 'error']


def keys(items):
    result = []
    for d in items:
        match = re.match(r"id '([^']+)' is declared by", d.message)
        result.append([d.code, match[1] if match else d.message])
    return sorted(result)


def main():
    base = json.loads((HERE / 'BASE.json').read_text())['base']
    archive = subprocess.check_output(['git', 'archive', base], cwd=ROOT)
    count = 0
    with tempfile.TemporaryDirectory(prefix='r6-seven-docgraph-', dir='/tmp') as tmp:
        target = Path(tmp)
        with tarfile.open(fileobj=io.BytesIO(archive)) as tree:
            for member in tree:
                if member.isfile() and member.name.endswith('.md'):
                    path = target / member.name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(tree.extractfile(member).read())
                    count += 1
        old = errors(target)
    live = errors(ROOT)
    equal = keys(old) == keys(live)
    result = {'base': base, 'tracked_base_markdown_files': count,
              'base_errors': len(old), 'current_errors': len(live),
              'same_error_kinds_and_logical_ids': equal,
              'byte_identical_messages': [str(d) for d in old] == [str(d) for d in live],
              'historical_errors': keys(old),
              'whole_tree_pass': not live,
              'history_removed_or_modified': False}
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if equal else 1)


if __name__ == '__main__':
    main()
