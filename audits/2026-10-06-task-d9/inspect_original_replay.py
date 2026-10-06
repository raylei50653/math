#!/usr/bin/env python3
"""Diagnose historical byte FAILs without replacing artifacts.

This tool intentionally calls the ORIGINAL build functions solely to compare
their replay payloads and provenance. It is not an independent lemma checker.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get('D9_REPO', str(HERE.parents[1])))


def differences(old, new, path=''):
    if type(old) is not type(new):
        return [{'path': path, 'historical': old, 'current': new}]
    if isinstance(old, dict):
        answer = []
        for key in sorted(old.keys() | new.keys()):
            if key not in old or key not in new:
                answer.append(dict(path=path + '/' + key,
                                   historical=old.get(key), current=new.get(key)))
            else:
                answer.extend(differences(old[key], new[key], path + '/' + key))
        return answer
    if isinstance(old, list):
        if len(old) != len(new):
            return [dict(path=path, historical_length=len(old), current_length=len(new))]
        return [item for i, (a, b) in enumerate(zip(old, new))
                for item in differences(a, b, path + '/' + str(i))]
    return [] if old == new else [dict(path=path, historical=old, current=new)]


def main():
    results = []
    for name, relative, kwargs, provenance in [
        ('e4_reductions', 'artifacts/c5_excess_two_e4/reductions.json', {}, 'sources'),
        ('e5_controls', 'artifacts/c5_excess_two_e5/controls.json', {'root': ROOT}, 'source_sha256'),
    ]:
        source = ROOT / f'scripts/c5_excess_two_{name}.py'
        spec = importlib.util.spec_from_file_location(name, source)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        historical_raw = (ROOT / relative).read_bytes()
        historical = json.loads(historical_raw)
        current = module.build(**kwargs)
        current_raw = (json.dumps(current, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()
        current = json.loads(current_raw)
        (HERE / f'{name}_current_replay.json').write_bytes(current_raw)
        delta = differences(historical, current)
        old_payload = {k: v for k, v in historical.items() if k != provenance}
        new_payload = {k: v for k, v in current.items() if k != provenance}
        result = dict(checker=name, artifact=relative,
                      historical_sha256=hashlib.sha256(historical_raw).hexdigest(),
                      recomputed_sha256=hashlib.sha256(current_raw).hexdigest(),
                      strict_bytes_match=historical_raw == current_raw,
                      payload_without_provenance_matches=old_payload == new_payload,
                      differences=delta,
                      original_build_reused=True, independent_lemma_checker=False)
        results.append(result)
        print(json.dumps(dict(checker=name, difference_count=len(delta),
                             payload_without_provenance_matches=old_payload == new_payload)))
    (HERE / 'historical_replay_differences.json').write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
