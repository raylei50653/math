#!/usr/bin/env python3
"""Validate fresh audit authoring, links, structured data and recorded raw logs."""
import ast
import gzip
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit

sys.path.insert(0, '/tmp/math-m3-ba0b447/scripts')
from check_docs import anchors, links


def main():
    root = Path(__file__).resolve().parent
    counts = {'python': 0, 'json': 0, 'markdown': 0, 'local_links': 0, 'recorded_logs': 0}
    for path in sorted(root.rglob('*')):
        if not path.is_file() or '__pycache__' in path.parts:
            continue
        assert path.stat().st_size < 1000000, str(path)
        if path.name.endswith('.json.gz'):
            json.loads(gzip.decompress(path.read_bytes()))
            counts['json'] += 1
        if path.suffix not in {'.py', '.md', '.json'}:
            continue
        text = path.read_text()
        assert text.endswith('\n'), str(path)
        assert all(line == line.rstrip() for line in text.splitlines()), str(path)
        if path.suffix == '.py':
            ast.parse(text, filename=str(path))
            counts['python'] += 1
        elif path.suffix == '.json':
            json.loads(text)
            counts['json'] += 1
        else:
            counts['markdown'] += 1
            for line, destination in links(text):
                url = urlsplit(destination)
                if url.scheme or url.netloc:
                    continue
                target = (path.parent / unquote(url.path)).resolve() if url.path else path
                assert target.exists(), (path, line, destination)
                if url.fragment and target.suffix == '.md':
                    assert unquote(url.fragment) in anchors(target.read_text()), (path, line, destination)
                counts['local_links'] += 1
    records = list((root / 'commands').glob('*.json'))
    for path in records:
        record = json.loads(path.read_text())
        for entry in record['logs']:
            log = root / entry['path']
            raw = log.read_bytes()
            assert len(raw) == entry['bytes'] and hashlib.sha256(raw).hexdigest() == entry['sha256'], entry
            counts['recorded_logs'] += 1
    setup = json.loads((root / 'setup.json').read_text())
    for record in setup['commands']:
        assert hashlib.sha256((root / record['log']).read_bytes()).hexdigest() == record['sha256']
    print(json.dumps({'status': 'PASS', 'counts': counts, 'setup_commands': len(setup['commands'])}, sort_keys=True))


if __name__ == '__main__':
    main()
