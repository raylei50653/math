#!/usr/bin/env python3
"""Export the fan 4 / fan 5 residual-class data to closed Lean inputs.

Reads artifacts/stepwise/fan4_signatures.json and fan5_signatures.json and writes
Math/StepwiseGenerated.lean: shortest representatives, pairwise separators, and the
minimised transition tables.  Math/StepwiseReplay.lean then re-decides every separator
endpoint with the verified strip checker (Math/StripGraph.lean), so the JSON is untrusted
input and the Lean statements do not depend on the Python DFA construction.

python scripts/export_stepwise.py           # rewrite Math/StepwiseGenerated.lean
python scripts/export_stepwise.py --check   # regenerate in memory and compare byte for byte
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    4: (ROOT / 'artifacts/stepwise/fan4_signatures.json', ('fan4',)),
    5: (ROOT / 'artifacts/stepwise/fan5_signatures.json', ()),
}
OUT = ROOT / 'Math/StepwiseGenerated.lean'
EXPECTED_CLASSES = {4: 55, 5: 97}


def load(fan):
    path, keys = SOURCES[fan]
    raw = path.read_bytes()
    data = json.loads(raw)
    for k in keys:
        data = data[k]
    classes = data['classes']
    n = len(classes)
    assert n == EXPECTED_CLASSES[fan]
    assert [c['id'] for c in classes] == list(range(n))
    assert classes[0]['representative'] == []
    for c in classes:
        assert all(type(x) is int and 0 <= x < 4 for x in c['representative'])
        assert len(c['delta']) == 4 and all(type(t) is int and 0 <= t < n for t in c['delta'])
        assert type(c['live']) is bool
    seps = data['separators']
    assert len(seps) == n * (n - 1) // 2
    assert sorted((q, r) for q, r, _ in seps) == [(q, r) for q in range(n) for r in range(q + 1, n)]
    assert all(all(type(x) is int and 0 <= x < 4 for x in s) for _, _, s in seps)
    return dict(sha256=hashlib.sha256(raw).hexdigest(), path=path.relative_to(ROOT),
                reps=[c['representative'] for c in classes],
                delta=[c['delta'] for c in classes],
                live=[c['live'] for c in classes], seps=seps)


def lean_list(items, per_line, indent='  '):
    lines = [', '.join(items[j:j + per_line]) for j in range(0, len(items), per_line)]
    return '[\n' + ''.join(f'{indent}{line},\n' for line in lines[:-1]) + f'{indent}{lines[-1]}\n]'


CHUNK = 250  # keep every list literal small: fast elaboration, no deep recursion


def chunked_def(name, ty, items, per_line):
    """One def per chunk of `items`, then `name` as their concatenation."""
    parts = [items[j:j + CHUNK] for j in range(0, len(items), CHUNK)]
    if len(parts) == 1:
        return [f'def {name} : {ty} := ' + lean_list(items, per_line)]
    out = [f'def {name}_{k} : {ty} := ' + lean_list(part, per_line) for k, part in enumerate(parts)]
    names = [f'{name}_{k}' for k in range(len(parts))]
    joined = ' ++\n    '.join(' ++ '.join(names[j:j + 6]) for j in range(0, len(names), 6))
    out.append(f'def {name} : {ty} :=\n  {joined}')
    return out


def render(fan, d):
    """Words are exported over ℕ; StepwiseReplay maps them to Fin 4."""
    word = lambda w: '[' + ','.join(map(str, w)) + ']'
    lines = [f'/-! Fan {fan}: {d["path"]}', f'SHA-256 {d["sha256"]}. -/']
    lines += chunked_def(f'fan{fan}Reps', 'List (List ℕ)', [word(w) for w in d['reps']], 8)
    lines += chunked_def(f'fan{fan}Live', 'List Bool',
                         ['true' if b else 'false' for b in d['live']], 12)
    lines += chunked_def(f'fan{fan}Delta', 'List (List ℕ)', [word(r) for r in d['delta']], 6)
    lines += chunked_def(f'fan{fan}Seps', 'List (ℕ × ℕ × List ℕ)',
                         [f'({q}, {r}, {word(s)})' for q, r, s in d['seps']], 5)
    return '\n'.join(lines) + '\n'


def generate():
    header = [
        '/-', 'Copyright (c) 2026 raylei50653. All rights reserved.',
        'Released under Apache 2.0 license as described in the file LICENSE.',
        'Authors: raylei50653', '-/', 'import Mathlib', '',
        '/-! Generated data. Run scripts/export_stepwise.py to regenerate.',
        'Shortest representatives, pairwise separators and minimised transition tables of the',
        'fan 4 / fan 5 residual classes.  Untrusted input: Math/StepwiseReplay.lean re-decides',
        'every separator endpoint against the strip graph semantics of Math/StripGraph.lean. -/',
        'namespace StepwiseData', '',
    ]
    body = [render(fan, load(fan)) for fan in (4, 5)]
    return '\n'.join(header) + '\n'.join(body) + '\nend StepwiseData\n'


if __name__ == '__main__':
    content = generate()
    if '--check' in sys.argv:
        assert OUT.read_text() == content
        print('stepwise export: JSON validated and Math/StepwiseGenerated.lean matches')
    else:
        OUT.write_text(content)
        print(f'wrote {OUT.relative_to(ROOT)}')
