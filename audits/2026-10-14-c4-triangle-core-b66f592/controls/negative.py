#!/usr/bin/env python3
"""Reject damaged inputs/certificates without modifying any archived bytes."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    protected = [HERE / 'certificate.json', HERE / 'structure-v2.json',
                 PACKAGE / 'frozen/artifacts/c5_cells/cells.json']
    before = {str(p.relative_to(PACKAGE)): sha(p) for p in protected}
    result = []

    def rejected(name, command, reason):
        proc = subprocess.run([sys.executable, '-B', *map(str, command)],
                              capture_output=True, text=True)
        if proc.returncode == 0 or reason not in proc.stderr:
            raise AssertionError((name, proc.returncode, proc.stdout, proc.stderr))
        result.append({'name': name, 'rejected': True, 'reason': reason})

    with tempfile.TemporaryDirectory(prefix='c4-core-negative-') as folder:
        tmp = Path(folder)
        damaged = json.loads(protected[0].read_text())
        damaged['records'].pop()
        bad_certificate = tmp / 'bad-certificate.json'
        bad_certificate.write_text(json.dumps(damaged))
        rejected('missing fibre record', [HERE / 'check_quotient.py', '--check',
                 '--output', bad_certificate], 'Certificate differs')
        bad_source = tmp / 'bad-source.json'
        bad_source.write_bytes(protected[2].read_bytes() + b'\n')
        rejected('source drift', [HERE / 'check_quotient.py', '--check',
                 '--input', bad_source], 'Frozen source hash differs')
        rejected('exclusive create', [HERE / 'check_quotient.py'], 'FileExistsError')
        damaged = json.loads(protected[1].read_text())
        damaged['cores'].pop()
        bad_structure = tmp / 'bad-structure.json'
        bad_structure.write_text(json.dumps(damaged))
        rejected('missing rooted opening', [HERE / 'check_structure.py', '--check',
                 '--certificate', bad_structure], 'certificate differs')
    after = {str(p.relative_to(PACKAGE)): sha(p) for p in protected}
    if before != after:
        raise AssertionError('protected bytes changed')
    def module(name):
        spec = importlib.util.spec_from_file_location(name, HERE / (name + '.py'))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    old, current = module('check_structure_v1'), module('check_structure')
    pinched = json.loads((HERE / 'pinched_surface.json').read_text())
    adj = current.adj_from_edges(pinched['vertices'], pinched['edges'])
    old.sphere_faces(adj, pinched['faces'])
    try:
        current.sphere_faces(adj, pinched['faces'])
    except ValueError as error:
        if str(error) != 'vertex link is one cycle':
            raise
        result.append({'name': 'pinched two icosahedra', 'v1_accepted': True,
                       'v2_rejected': True, 'reason': str(error)})
    else:
        raise AssertionError('accepted non-surface face system')
    print(json.dumps({'ok': True, 'negative_controls': result,
                      'protected_sha256_before_and_after': before}, indent=2))


if __name__ == '__main__':
    main()
