#!/usr/bin/env python3
"""Run a read-only checker and record actual file/import dependencies."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import sys


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--script', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root, output = args.repo.resolve(), args.output.resolve()
    assert not output.exists(), 'Preserve earlier runtime traces'
    observed, writes = set(), set()

    def hook(event, fields):
        if event != 'open' or not isinstance(fields[0], (str, bytes, os.PathLike)):
            return
        path = Path(os.fsdecode(fields[0])).absolute()
        try:
            relative = str(path.relative_to(root))
        except ValueError:
            return
        flags = fields[2] if len(fields) > 2 and isinstance(fields[2], int) else 0
        if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC):
            writes.add(relative)
        else:
            observed.add(relative)

    sys.dont_write_bytecode = True
    sys.path.insert(0, str(root / 'scripts'))
    sys.argv = [str(root / 'scripts' / args.script), '--check']
    sys.addaudithook(hook)
    code, exception = 0, None
    try:
        runpy.run_path(sys.argv[0], run_name='__main__')
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
    except BaseException as exc:
        import traceback
        traceback.print_exc()
        code, exception = 1, repr(exc)
    paths = sorted(p for p in observed if (root / p).is_file())
    repository_reads = {p: {'sha256': digest(root / p), 'size': (root / p).stat().st_size}
                        for p in paths}
    external = {}
    for name, module in sorted(sys.modules.items()):
        file = getattr(module, '__file__', None)
        if file and Path(file).is_file() and not Path(file).resolve().is_relative_to(root):
            external[name] = {'path': str(Path(file).resolve()), 'sha256': digest(Path(file))}
    data = {'script': args.script, 'hashseed': os.environ.get('PYTHONHASHSEED', 'default'),
            'exit_code': code, 'exception': exception, 'repository_read_dependencies': repository_reads,
            'repository_writes': sorted(writes), 'imported_external_modules': external,
            'python_executable': {'path': sys.executable, 'sha256': digest(Path(sys.executable))},
            'scope': 'Observed open events and imported module files for this --check execution'}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    assert not writes, f'Checker wrote into snapshot: {writes}'
    raise SystemExit(code)


if __name__ == '__main__':
    main()
