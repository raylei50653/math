"""Exercise real no-clobber producers and rebuild restoration in temporary repositories."""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SPEC = importlib.util.spec_from_file_location(
    'artifacts_rebuild', Path(__file__).resolve().parents[1] / 'artifacts.py')
artifacts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(artifacts)


class ArtifactRebuildTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.root_patch = mock.patch.object(artifacts, 'ROOT', self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def write(self, relative, payload):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload.encode() if isinstance(payload, str) else payload)
        return path

    def producer(self, *, main=b'main', companion=b'companion', exit_code=0,
                 arguments=False, name='generate.py', write_companion=True):
        relative = 'scripts/' + name if '/' not in name else name
        expected_arguments = ('--size', '5') if arguments is True else arguments or ()
        self.write(relative, '\n'.join([
            'from pathlib import Path',
            'import sys',
            f'root = Path({str(self.root)!r})',
            "target = root / 'artifacts/main.json'",
            'target.parent.mkdir(parents=True, exist_ok=True)',
            f"with target.open('xb') as output: output.write({main!r})",
            "target = root / 'artifacts/sidecar.json'",
            f"with target.open('xb') as output: output.write({companion!r})"
            if write_companion else '# companion intentionally missing',
            f'assert sys.argv[1:] == {list(expected_arguments)!r}',
            f'raise SystemExit({exit_code})',
            '',
        ]))
        return name

    def manifest(self, producer, payload=b'main'):
        return {'files': {'artifacts/main.json': {
            'script': producer, 'bytes': len(payload),
            'sha256': hashlib.sha256(payload).hexdigest(),
        }}, 'producers': {producer: []}}

    def rebuild(self, producer, *, keep_going=False, manifest=None):
        with mock.patch.object(artifacts, 'ADDITIONAL_OUTPUTS', {
                producer: ('artifacts/sidecar.json',)}):
            return artifacts.run_producer(
                producer, ['artifacts/main.json'], manifest or self.manifest(producer),
                keep_going)

    def test_exclusive_producer_rebuilds_main_and_saved_companion(self):
        producer = self.producer()
        self.write('artifacts/main.json', b'main')
        self.write('artifacts/sidecar.json', b'companion')
        unrelated = self.write('artifacts/unrelated.json', b'leave untouched')
        result, _, bad = self.rebuild(producer)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(bad, [])
        self.assertEqual((self.root / 'artifacts/main.json').read_bytes(), b'main')
        self.assertEqual((self.root / 'artifacts/sidecar.json').read_bytes(), b'companion')
        self.assertEqual(unrelated.read_bytes(), b'leave untouched')
        self.assertEqual(list(self.root.rglob('*.pre-rebuild')), [])
        self.assertEqual(list(self.root.rglob('*.rebuilt')), [])

    def test_failed_producer_restores_original_bytes_and_modes(self):
        producer = self.producer(main=b'new main', companion=b'new companion', exit_code=7)
        main = self.write('artifacts/main.json', b'original main')
        main.chmod(0o640)
        sidecar = self.write('artifacts/sidecar.json', b'original companion')
        sidecar.chmod(0o600)
        result, _, bad = self.rebuild(producer, keep_going=True)
        self.assertEqual(result.returncode, 7)
        self.assertEqual(set(bad), {'artifacts/main.json', 'artifacts/sidecar.json'})
        self.assertEqual(main.read_bytes(), b'original main')
        self.assertEqual(main.stat().st_mode & 0o777, 0o640)
        self.assertEqual(sidecar.read_bytes(), b'original companion')
        self.assertEqual(sidecar.stat().st_mode & 0o777, 0o600)
        self.assertEqual(main.with_name('main.json.rebuilt').read_bytes(), b'new main')
        self.assertEqual(sidecar.with_name('sidecar.json.rebuilt').read_bytes(), b'new companion')

    def test_companion_byte_mismatch_is_reported_and_original_restored(self):
        producer = self.producer(companion=b'changed companion')
        self.write('artifacts/main.json', b'main')
        sidecar = self.write('artifacts/sidecar.json', b'saved companion')
        result, _, bad = self.rebuild(producer)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(bad, ['artifacts/sidecar.json'])
        self.assertEqual(sidecar.read_bytes(), b'saved companion')
        self.assertEqual(sidecar.with_name('sidecar.json.rebuilt').read_bytes(), b'changed companion')

    def test_subprocess_launch_failure_restores_saved_outputs(self):
        producer = self.producer()
        main = self.write('artifacts/main.json', b'main')
        sidecar = self.write('artifacts/sidecar.json', b'companion')
        with mock.patch.object(artifacts.subprocess, 'run', side_effect=OSError('cannot launch')):
            with self.assertRaisesRegex(OSError, 'cannot launch'):
                self.rebuild(producer)
        self.assertEqual(main.read_bytes(), b'main')
        self.assertEqual(sidecar.read_bytes(), b'companion')
        self.assertEqual(list(self.root.rglob('*.pre-rebuild')), [])

    def test_keep_going_preserves_saved_companion_as_recorded(self):
        producer = self.producer(companion=b'changed companion')
        self.write('artifacts/main.json', b'main')
        sidecar = self.write('artifacts/sidecar.json', b'saved companion')
        result, _, bad = self.rebuild(producer, keep_going=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(bad, ['artifacts/sidecar.json'])
        self.assertEqual(sidecar.read_bytes(), b'changed companion')
        self.assertEqual(sidecar.with_name('sidecar.json.recorded').read_bytes(), b'saved companion')

    def test_missing_saved_companion_must_still_be_generated(self):
        producer = self.producer(write_companion=False)
        result, _, bad = self.rebuild(producer)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(bad, ['artifacts/sidecar.json'])

    def test_existing_rebuild_backup_is_preserved_before_any_output_move(self):
        producer = self.producer()
        main = self.write('artifacts/main.json', b'main')
        backup = self.write('artifacts/sidecar.json.pre-rebuild', b'earlier saved bytes')
        with self.assertRaisesRegex(ValueError, 'backup already exists'):
            self.rebuild(producer)
        self.assertEqual(main.read_bytes(), b'main')
        self.assertEqual(backup.read_bytes(), b'earlier saved bytes')

    def test_canonical_repository_producer_generates_and_uses_correct_label(self):
        producer = self.producer(name='artifacts/probe/generate.py')
        result, _, bad = self.rebuild(producer)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(bad, [])
        self.assertEqual(artifacts.script_label(producer), producer)
        self.assertEqual(artifacts.script_path(producer), self.root / producer)
        self.assertIn('from pathlib', artifacts.script_text(producer))
        expected = hashlib.sha256(
            (producer + '\0').encode() + (self.root / producer).read_bytes() + b'\0')
        self.assertEqual(artifacts.fingerprint(producer, self.manifest(producer)), expected.hexdigest())

    def test_producer_path_rejects_noncanonical_or_escaping_paths(self):
        for producer in ('/tmp/generate.py', '../generate.py', 'scripts/../generate.py',
                         'scripts\\generate.py', './generate.py', 'scripts//generate.py',
                         'generate.txt', '', None):
            with self.subTest(producer=producer), self.assertRaises(ValueError):
                artifacts.script_path(producer)

    def test_adjacent_probe_override_names_only_the_exact_output(self):
        output = 'artifacts/c5_excess_two_e4/control_probe/split_hub_probe.json'
        self.assertEqual(artifacts.infer_producer(output), output.removesuffix('.json') + '.py')
        with self.assertRaises(SystemExit):
            artifacts.infer_producer(output + '.rebuilt')

    def test_producer_symlink_cannot_escape_repository(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / 'generate.py'
            target.write_text('raise SystemExit(0)\n')
            (self.root / 'scripts').mkdir()
            (self.root / 'scripts/generate.py').symlink_to(target)
            with self.assertRaisesRegex(ValueError, 'escapes repository'):
                artifacts.script_path('generate.py')
            (self.root / 'external').symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'escapes repository'):
                artifacts.script_path('external/generate.py')

    def test_legacy_basename_fingerprint_preserves_labels_and_dependency_encoding(self):
        self.write('scripts/generate.py', 'import helper\n')
        self.write('scripts/helper.py', '# helper bytes\n')
        manifest = {'files': {'artifacts/input.json': {
            'script': 'upstream.py', 'sha256': 'a' * 64}},
            'producers': {'generate.py': ['upstream.py']}}
        expected = hashlib.sha256()
        for name in ('generate.py', 'helper.py'):
            expected.update(f'scripts/{name}\0'.encode()
                            + (self.root / 'scripts' / name).read_bytes() + b'\0')
        expected.update(('artifacts/input.json\0' + 'a' * 64 + '\0').encode())
        self.assertEqual(artifacts.fingerprint('generate.py', manifest), expected.hexdigest())
        self.assertEqual(artifacts.script_label('generate.py'), 'scripts/generate.py')

    def test_generation_arguments_are_used_and_change_fingerprint(self):
        producer = self.producer(arguments=True)
        manifest = self.manifest(producer)
        original = artifacts.fingerprint(producer, manifest)
        with mock.patch.object(artifacts, 'PRODUCER_ARGS', {producer: ('--size', '5')}):
            changed = artifacts.fingerprint(producer, manifest)
            self.assertNotEqual(changed, original)
            result, _, bad = self.rebuild(producer)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(bad, [])

    def test_readonly_default_producers_receive_explicit_write_mode(self):
        for name in ('c5_qcore_shield_screen.py', 'c5_open_leaf_ledger.py'):
            with self.subTest(producer=name):
                self.assertEqual(artifacts.PRODUCER_ARGS[name], ('--write',))
                producer = self.producer(name=name, arguments=('--write',))
                result, _, bad = self.rebuild(producer)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(bad, [])


if __name__ == '__main__':
    unittest.main()
