#!/usr/bin/env python3
"""Readable discussion examples using the existing same-C5 relation API.
No new graph grammar or geometry checker. Replays relations on all labelled colours.
"""
import argparse
from itertools import permutations
from pathlib import Path

from boundary_relations import Literal, c5_universe
from pp_relations import load_language

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/state_views/examples.md'


def expanded(relation):
    return {tuple(p[c] for c in row) for row in relation.patterns
            for p in permutations(range(4))}


def status(rows, i, j):
    if not rows:
        return 'infeasible'
    values = {row[i] == row[j] for row in rows}
    return 'free' if len(values) == 2 else 'forced_equal' if True in values else 'forced_different'


def build():
    language = load_language()
    left, right, fan = [language[key].relation for key in ('R91','R935','R767')]
    universe = c5_universe()
    eq, neq = Literal('b0','b2'), Literal('b0','b2',False)
    guard = [Literal('b1','b4'), Literal('b0','b2',False)]
    lr, rr, fr, ur = map(expanded,(left,right,fan,universe))
    cases = [
        ('L',left,lr,'b0','b2'),
        ('R',right,rr,'b0','b2'),
        ('join(L,R)',left.meet(right),lr & rr,'b0','b2'),
        ('condition(join(L,R), b0!=b2)',left.meet(right).condition([neq]),
         {b for b in lr & rr if b[0]!=b[2]},'b0','b2'),
        ('F',fan,fr,'b0','b3'),
        ('condition(F, Γ)',fan.condition(guard),
         {b for b in fr if b[1]==b[4] and b[0]!=b[2]},'b0','b3'),
        ('condition(U, Γ)',universe.condition(guard),
         {b for b in ur if b[1]==b[4] and b[0]!=b[2]},'b0','b3'),
    ]
    lines = ['# 狀態觀察表：同一有序 C5', '',
             '由 `python scripts/state_views.py` 生成；`--check` 完整重算並逐 byte 比對。',
             'L=R91，R=R935，F=R767，U=全部 proper C5；Γ=(b1=b4 ∧ b0!=b2)。',
             '以下是 computationally observed 的染色關係重驗，沒有重新驗證圖幾何。',
             '載入既有 catalog 時由原 loader 核對來源 hash 與 witness 對應。', '',
             '| 表達式 | 色型數 | 完整賦色數 | 查詢 | 結果 | 同色／異色 witness |',
             '| --- | ---: | ---: | --- | --- | --- |']
    labels = {'free':'未強迫','forced_equal':'強迫同色','forced_different':'強迫異色','infeasible':'無解'}
    for name,rel,expected,a,b in cases:
        actual = expanded(rel)
        assert actual == expected
        i,j = rel.ports.index(a),rel.ports.index(b)
        query = rel.query(a,b)
        assert query['status'] == status(expected,i,j)
        witnesses = []
        for key in ('equal_witness','different_witness'):
            witness = query[key]
            if witness is not None:
                assert tuple(witness) in actual
            witnesses.append('—' if witness is None else ''.join(map(str,witness)))
        lines.append(f"| `{name}` | {len(rel.patterns)} | {len(actual)} | {a},{b} | "
                     f"{labels[query['status']]} | {' / '.join(witnesses)} |")
    lines += ['', '## 分支相容表', '',
              '兩側各自 split(b0=b2)：`=` 與 `≠` 都是非空分支。表格數字是接合後的完整賦色數。',
              '0 可按染色衝突剪枝；非零只表示染色相容，幾何另判。', '',
              '| 左分支 \\ 右分支 | R：b0=b2 | R：b0!=b2 |', '| --- | ---: | ---: |']
    for guard_l in (eq,neq):
        l = left.condition([guard_l])
        assert l.patterns
        counts = []
        for guard_r in (eq,neq):
            r = right.condition([guard_r])
            assert r.patterns
            joined = l.meet(r)
            assert expanded(joined) == expanded(l) & expanded(r)
            counts.append(len(expanded(joined)))
        lines.append(f'| L：{guard_l.text()} | {counts[0]} | {counts[1]} |')
    lines += ['', '## 完整色型觀察', '',
              '每列展開同一個全域 S4 換色 orbit；位置 b0…b4 保持固定。這不是五點獨立換色。', '',
              '| 色型 | L | R | join(L,R) |', '| --- | --- | --- | --- |']
    for pattern in sorted(universe.patterns):
        flags = ['✓' if pattern in s.patterns else '—' for s in (left,right,left.meet(right))]
        lines.append(f"| `{''.join(map(str,pattern))}` | {' | '.join(flags)} |")
    lines += ['', '## 幾何與證明狀態', '',
              '本觀察表的 join 統一標示 geometry=unknown。既有特定一內一外 witness 的幾何結果見',
              '[boundary_relations.md](../../docs/boundary_relations.md)；不能轉用到任意同側接線。',
              'Γ 對 R767 的 conditional forcing 另有既有 Lean native finite 證明，',
              '見 `Math/C5PairForcing.lean`；這次只重驗 Python 關係與觀察輸出。', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    result = build()
    if args.check:
        if OUT.read_text() != result:
            raise SystemExit('observation sheet mismatch')
    else:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(result)
    print(f'{"checked" if args.check else "wrote"}: {OUT}')


if __name__ == '__main__':
    main()
