#!/usr/bin/env python3
"""Read-only pin/domain checks, with a separate exclusive-create seal action."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def pin(raw):
    return {'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}


def check_inputs():
    data = json.loads((HERE / 'input-pins.json').read_bytes())
    need(data['base'] == BASE, 'BASE changed')
    paths = set()
    counts = {'BASE Git blob': 0, 'sealed audit physical SHA256': 0}
    for item in data['inputs']:
        name, frozen = item['path'], HERE / item['frozen_path']
        need(name not in paths, 'duplicate input pin')
        paths.add(name)
        raw = frozen.read_bytes()
        need(pin(raw) == {k: item[k] for k in ('bytes', 'sha256')}, 'frozen input changed: ' + name)
        need((REPO / name).read_bytes() == raw, 'live authority changed: ' + name)
        counts[item['authority']] += 1
        if item['authority'] == 'BASE Git blob':
            blob = subprocess.check_output(['git', 'rev-parse', BASE + ':' + name], cwd=REPO, text=True).strip()
            need(blob == item['git_blob'], 'BASE blob pin changed: ' + name)
            need(subprocess.check_output(['git', 'cat-file', 'blob', blob], cwd=REPO) == raw,
                 'BASE bytes differ: ' + name)
        else:
            need(item['git_blob'] is None and item['included_in_BASE_claimed'] is False,
                 'audit physical input incorrectly claimed as BASE')
    for name, digest in data['sealed_deliveries'].items():
        need(sha256((REPO / name).read_bytes()).hexdigest() == digest, 'reviewed delivery changed')
    need(counts == {'BASE Git blob': 12, 'sealed audit physical SHA256': 11}, 'input counts changed')
    return counts


def check_tasks():
    tasks = json.loads((HERE / 'tasks.json').read_bytes())
    need(tasks['base'] == BASE and len(tasks['tasks']) == 4, 'task count or BASE changed')
    original = json.loads((HERE / 'authority/sealed/audits/2026-10-11-n45-s-long-s-review/remaining-schedules.json').read_bytes())
    remaining = original['remaining_schedules']
    expected = [
        [s for s in remaining if s['t_s'] == 1],
        [s for s in remaining if s['t_s'] == 2 and s['beta_q'] == 0],
        [s for s in remaining if s['t_s'] == 2 and s['beta_q'] == 2],
        [],
    ]
    labels, ids, outputs, keys = set(), set(), set(), []
    for index, task in enumerate(tasks['tasks']):
        labels.add(task['label']); ids.add(task['task_id']); outputs.add(task['output_directory'])
        need(task['assigned_schedules'] == expected[index], 'assigned schedule records changed')
        need(task['assigned_schedule_count'] == len(expected[index]), 'task count differs')
        need(task['depends_on_same_round_results'] is False and task['research_started_by_dispatch'] is False,
             'dispatch scope changed')
        text = (HERE / task['task_file']).read_text()
        need(task['task_id'] in text and task['output_directory'] in text, 'task routing text differs')
        need(all(term in text for term in ['K1–K12', '同一原圖', 'inclusion-minimal', '待獨立驗收']),
             'task contract missing')
        for s in task['assigned_schedules']:
            keys.append((s['t_s'], s['beta_q'], s['SigmaG_orbit'], tuple(s['QG'])))
        if task['label'] == 'A':
            need(task['s_spoke_variants'] == [[0], [2]] and task['schedule_spoke_queries'] == 28,
                 'T1 spoke variants changed')
        if task['label'] == 'D':
            need(task['finite_caps'] == {'named_cases': 8, 'C_vertices_per_case': 11}, 'transfer caps changed')
    need(len(labels) == len(ids) == len(outputs) == 4, 'duplicate task identity/output')
    need(len(keys) == len(set(keys)) == 24, 'paper partition not disjoint/complete')
    need([len(x) for x in expected] == [14, 3, 7, 0], 'paper partition changed')
    for link in re.findall(r'\]\(([^)]+)\)', (HERE / 'TASKS.md').read_text()):
        need((HERE / link).exists(), 'dispatch index link missing: ' + link)
    return [14, 3, 7]


def inventory():
    files, directories = [], []
    for path in sorted(HERE.rglob('*')):
        name = path.relative_to(HERE).as_posix()
        need(not path.is_symlink(), 'unexpected symlink')
        if path.is_dir():
            directories.append(name)
        elif path.is_file():
            if name != 'delivery.json':
                files.append({'path': name, **pin(path.read_bytes())})
        else:
            raise ValueError('unexpected special file: ' + name)
    return files, directories


def main():
    parser = argparse.ArgumentParser()
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument('--seal', action='store_true')
    choice.add_argument('--check', action='store_true')
    args = parser.parse_args()
    counts, partition = check_inputs(), check_tasks()
    files, directories = inventory()
    expected = {'base': BASE, 'batch_id': 'N45-S-LONG-S-RFIBRE-WAVE',
                'scope': 'four independently publishable tasks; research not started',
                'files': files, 'directories': directories, 'payload_files': len(files),
                'payload_bytes': sum(item['bytes'] for item in files),
                'metadata_exclusions': [{'path': 'delivery.json', 'reason': 'self-hash recursion'}]}
    manifest = HERE / 'delivery.json'
    if args.seal:
        with manifest.open('xb') as stream:
            stream.write((json.dumps(expected, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode())
    need(json.loads(manifest.read_bytes()) == expected, 'sealed dispatch inventory differs')
    print(json.dumps({'status': 'passes', 'base': BASE, 'inputs': counts, 'paper_partition': partition,
                      'task_count': 4, 'payload_files': len(files),
                      'delivery_sha256': sha256(manifest.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    main()
