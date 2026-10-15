task_source=/home/ray/developer/ai/math
task_replay="$(mktemp -d /tmp/math-route-baseline-replay.XXXXXX)"
git -C "$task_source" worktree add --detach "$task_replay" 6ddea32a81349821ad3724ae1652bddb9c6a7b04
python3 -B - "$task_source" "$task_replay" <<'PY_COPY'
import hashlib, json, pathlib, shutil, sys
source, replay = map(pathlib.Path, sys.argv[1:])
base = json.loads((source / 'audits/2026-10-15-route-round4-6ddea32/BASE.json').read_text())
names = base['prior_audits'] + base['write_scope']
assert len(names) == len(set(names)) == 16
for name in names:
    shutil.copytree(source / name, replay / name)
    for path in (source / name).rglob('*'):
        if path.is_file():
            target = replay / path.relative_to(source)
            assert hashlib.sha256(path.read_bytes()).digest() == hashlib.sha256(target.read_bytes()).digest()
PY_COPY
python3 -B "$task_replay/audits/2026-10-15-route-round4-6ddea32/check_bundle.py" --write "$task_replay.bundle.json"
