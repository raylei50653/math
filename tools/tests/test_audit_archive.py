"""Exercise selective archive publication in isolated, gitless repositories."""
from contextlib import redirect_stderr, redirect_stdout
import gzip
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SPEC = importlib.util.spec_from_file_location(
    'audit_archive', Path(__file__).resolve().parents[1] / 'audit_archive.py')
archive = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(archive)


class SelectiveAppendTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / 'audits').mkdir()
        (self.root / '.gitignore').write_text('# local ignores\n')
        (self.root / archive.INDEX).write_text(json.dumps(
            dict(schema=1, description='fixture', files={}, blobs={})) + '\n')

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def data(self):
        return json.loads((self.root / archive.INDEX).read_text())

    def append(self, **kwargs):
        with redirect_stdout(io.StringIO()):
            archive.append(self.root, **kwargs)

    def published_bytes(self):
        paths = [self.root / archive.INDEX, self.root / '.gitignore']
        blob_dir = self.root / archive.BLOBS
        if blob_dir.exists():
            paths.extend(blob_dir.iterdir())
        return {path.relative_to(self.root).as_posix(): path.read_bytes()
                for path in paths}

    def test_selection_deduplicates_and_restores_exact_bytes(self):
        payload = b'{"selected": true}\r\n\x00'
        first = self.write('audits/chosen/first.json', payload)
        first.chmod(0o640)
        self.write('audits/chosen/duplicate.json', payload)
        self.write('audits/unrelated/large.json', b'x' * 1_000_000)
        self.write('audits/unrelated/.snapshot/small.txt', b'snapshot')
        with mock.patch.object(archive, 'scan', side_effect=AssertionError('whole audit scan')):
            self.append(paths=['audits/chosen/first.json',
                               'audits/chosen/first.json',
                               'audits/chosen/duplicate.json'])

        data = self.data()
        self.assertEqual(set(data['files']), {'audits/chosen/first.json',
                                             'audits/chosen/duplicate.json'})
        self.assertEqual(len(data['blobs']), 1)
        sha = hashlib.sha256(payload).hexdigest()
        self.assertEqual(data['files']['audits/chosen/first.json']['sha256'], sha)
        self.assertEqual(data['files']['audits/chosen/first.json']['mode'], 0o640)
        self.assertEqual(data['files']['audits/chosen/first.json']['reason'], 'explicit')
        compressed = (self.root / data['blobs'][sha]['path']).read_bytes()
        self.assertEqual(gzip.decompress(compressed), payload)
        self.assertEqual(compressed[:8], b'\x1f\x8b\x08\x00\x00\x00\x00\x00')
        self.assertIn('/audits/chosen/first.json\n', (self.root / '.gitignore').read_text())
        self.assertNotIn('unrelated', (self.root / '.gitignore').read_text())

        destination = self.root / 'restored'
        with redirect_stdout(io.StringIO()):
            archive.replay(self.root, 'restore', destination)
            archive.replay(self.root, 'verify', destination)
        restored = destination / 'audits/chosen/first.json'
        self.assertEqual(restored.read_bytes(), payload)
        self.assertEqual(restored.stat().st_mode & 0o777, 0o640)

    def test_existing_records_and_gzip_blobs_remain_unchanged(self):
        self.write('audits/old.json', b'{"old": true}\n')
        self.append(paths=['audits/old.json'])
        old_data = self.data()
        old_blobs = {sha: (self.root / record['path']).read_bytes()
                     for sha, record in old_data['blobs'].items()}
        self.write('audits/new.json', b'{"new": true}\n')
        self.append(paths=['audits/old.json', 'audits/new.json'])
        data = self.data()
        self.assertEqual(data['files']['audits/old.json'], old_data['files']['audits/old.json'])
        for sha, content in old_blobs.items():
            self.assertEqual(data['blobs'][sha], old_data['blobs'][sha])
            self.assertEqual((self.root / data['blobs'][sha]['path']).read_bytes(), content)

    def test_changed_selected_archive_rejected_before_publication(self):
        self.write('audits/old.json', b'old')
        self.append(paths=['audits/old.json'])
        self.write('audits/old.json', b'changed')
        self.write('audits/new.json', b'new')
        before = self.published_bytes()
        with self.assertRaisesRegex(ValueError, 'Archived path changed'):
            self.append(paths=['audits/new.json', 'audits/old.json'])
        self.assertEqual(self.published_bytes(), before)

    def test_unselected_archive_is_not_scanned(self):
        self.write('audits/old.json', b'old')
        self.append(paths=['audits/old.json'])
        old_record = self.data()['files']['audits/old.json']
        self.write('audits/old.json', b'changed')
        self.write('audits/new.json', b'new')
        self.append(paths=['audits/new.json'])
        self.assertEqual(self.data()['files']['audits/old.json'], old_record)

    def test_invalid_paths_are_rejected_without_publication(self):
        self.write('audits/valid.json', b'valid')
        self.write('outside.json', b'outside')
        (self.root / 'audits/directory').mkdir()
        (self.root / 'audits/file-link.json').symlink_to(self.root / 'audits/valid.json')
        (self.root / 'audits/dir-link').symlink_to(self.root / 'audits/directory', target_is_directory=True)
        self.write('audits/.archive/blobs/forbidden.gz', b'blob')
        invalid = ['outside.json', str(self.root / 'audits/valid.json'),
                   '../audits/valid.json', 'audits/../outside.json', 'audits',
                   'audits/missing.json', 'audits/directory', archive.INDEX,
                   'audits/.archive/blobs/forbidden.gz', 'audits/file-link.json',
                   'audits/dir-link/missing.json']
        before = self.published_bytes()
        for relative in invalid:
            with self.subTest(relative=relative):
                with self.assertRaises(ValueError):
                    self.append(paths=['audits/valid.json', relative])
                self.assertEqual(self.published_bytes(), before)

    def test_default_append_preserves_scan_selection(self):
        self.write('audits/large.json', b'x' * 1_000_000)
        self.write('audits/.snapshot/small.json', b'{}\n')
        self.write('audits/whitespace.txt', b'trailing space \n')
        self.write('audits/small.json', b'{}\n')
        self.append()
        self.assertEqual({path: record['reason'] for path, record in self.data()['files'].items()},
                         {'audits/large.json': 'large',
                          'audits/.snapshot/small.json': 'snapshot',
                          'audits/whitespace.txt': 'historical-whitespace'})
        before = self.published_bytes()
        self.write('audits/large.json', b'y' * 1_000_000)
        with self.assertRaisesRegex(ValueError, 'Archived path changed'):
            self.append()
        self.assertEqual(self.published_bytes(), before)

    def test_selection_can_include_manifest_artifact_blobs(self):
        self.write('audits/chosen.json', b'{}\n')
        payload = b'manifest artifact bytes\n'
        self.write('artifacts/generated.json', payload)
        sha = hashlib.sha256(payload).hexdigest()
        self.write('artifacts/MANIFEST.json', json.dumps(dict(files={
            'artifacts/generated.json': dict(sha256=sha, bytes=len(payload))})).encode())
        self.append(paths=['audits/chosen.json'], include_artifacts=True)
        data = self.data()
        self.assertEqual(set(data['files']), {'audits/chosen.json'})
        self.assertIn(sha, data['blobs'])
        self.assertEqual(gzip.decompress((self.root / data['blobs'][sha]['path']).read_bytes()), payload)

    def test_cli_accepts_paths_for_append_and_rejects_other_actions(self):
        argv = ['audit_archive.py', 'append', '--repo', str(self.root),
                '--artifacts', '--paths', 'audits/chosen.json', 'audits/another.json']
        with mock.patch('sys.argv', argv), mock.patch.object(archive, 'append') as append:
            archive.main()
        append.assert_called_once_with(self.root, True, ['audits/chosen.json', 'audits/another.json'])
        for action in ('pack', 'restore', 'verify'):
            with self.subTest(action=action):
                with mock.patch('sys.argv', ['audit_archive.py', action, '--paths', 'audits/file.json']):
                    with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                        archive.main()
                    self.assertEqual(error.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
