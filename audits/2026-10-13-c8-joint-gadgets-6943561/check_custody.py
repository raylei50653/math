"""Read-only input/artifact custody, local Markdown links and whitespace."""
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    inputs = json.loads((HERE/'INPUTS.json').read_text())
    for item in inputs['files']:
        assert sha(ROOT/item['path']) == item['sha256'], ('live input drift',item['path'])
        assert sha(HERE/'frozen'/item['path']) == item['sha256'], ('frozen input drift',item['path'])
    manifest = json.loads((HERE/'MANIFEST.json').read_text())
    for path, item in manifest['files'].items():
        p = HERE/path
        assert p.stat().st_size == item['bytes'] and sha(p) == item['sha256'], ('artifact drift',path)
    linked = 0
    authored = []
    for path in HERE.rglob('*'):
        if not path.is_file() or 'frozen' in path.parts or 'vendor' in path.parts:
            continue
        if path.suffix in ('.py','.cpp','.md'):
            authored.append(path)
            text = path.read_text()
            assert all(line.rstrip() == line for line in text.splitlines()), ('trailing whitespace',str(path))
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                if re.match(r'[a-zA-Z]+:', target) or target.startswith('#'):
                    continue
                target = unquote(target.split('#')[0].strip('<>'))
                assert (path.parent/target).exists(), ('broken local link',str(path),target)
                linked += 1
    print(json.dumps(dict(status='PASS',direct_inputs=len(inputs['files']),
                          artifact_files=len(manifest['files']),local_links=linked,
                          authored_text_files=len(authored),input_drift=0),sort_keys=True))


if __name__=='__main__':main()
