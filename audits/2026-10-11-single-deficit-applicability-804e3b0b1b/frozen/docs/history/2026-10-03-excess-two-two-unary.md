# 2026-10-03：t=2、(2,1,1) 兩份原 unary 省略排除

接手基準 `bbd900a`，分支 `main`。使用者要求確認接手狀態、選方向並
開始推進，未要求 commit／push。接手時已有三原 unary、t=3 binary
省略及 t=2 雙 binary 省略等未提交成果與連動文件修改；全部保留。
記憶中的 ε=1 停止點已過時，以即時 HANDOFF、STATUS、Kempe 導覽及
工作樹為準。本輪先重播最新雙 binary checker，再接續其指定窄題。

成果見 [專題報告](../c5_excess_two_two_unary.md)，現況與下一入口見
[Kempe 導覽](../c5_kempe_guide.md)。研究線未增減，依文件治理維持
HANDOFF 薄索引；README、STATUS、導覽及前序報告補上後續關係。

## 本輪結果

933／941 固定完整 Σ、edge-minimal C₅ disk 來源若 ε=2、唯一 degree-6
root、t=2、原接點分拆 (2,1,1)，則同時省略兩份原 unary 必全收十列。
全 degree-4 分類及原接點 tail transfer 給任意大小涵蓋，保留原
(r,x,y,u,v)、三份原分量與共同色框。

- 118 bases／398 marked roots，兩候選各五像共 3,980 比較。
- 1,194 個在原核心拒絕列已不符目標，841 個有空必要列，1,945 個迫
  同一 binary 省略圖拒絕至少兩列；剩餘零。
- 111 份字面接合輸入保存全部 3,980 個原核心列引用；全部 15×15 對
  非空 unary domains 的 24,975 次完整五接點控制通過。
- 正式必要域容許各列獨立選 unary 禁色，無需 D 身份守恆或新增幾何。

因此該型的全 degree-4 拒絕核心只剩省略原 binary 的身份。
不是整份 (2,1,1) 或全部 ε=2 來源排除；共同下界仍 ε≥2，無新 Lean
theorem，一般出口與 K∞=K≤5 仍未證。

## 實際驗證

```bash
python3 scripts/c5_excess_two_two_binary.py --check
python3 scripts/c5_excess_two_two_unary.py
python3 scripts/c5_excess_two_two_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_two_unary.py --check
python3 scripts/c5_excess_two_spoke_unary.py --check
python3 scripts/c5_excess_two_double_spoke.py --check
lake build
uv run --with-requirements requirements.txt python tools/artifacts.py record artifacts/c5_excess_two_two_unary/observations.json
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 兩種 hash seed 均逐位元組重播通過。前序的雙 binary、
t=2 spoke＋unary、雙 spoke checker 通過；新 checker 亦重算原 398
位置的完整 relations、核心染色與原 rotations。`lake build` 成功
（8,831 jobs，既有 linter warnings），不代表本輪紙面論證已形式化。
任意大小分類、tail transfer 及外部 degree-list 定理沿用原報告，未重跑
其全部歷史模板或其他研究線；未使用新來源圖枚舉或 planarity oracle。

新證書為 2,086,800 bytes，依既有大檔制度登錄 MANIFEST／producer，
以 `.gitignore` 排除產生檔本體。未 commit／push。

文件檢查通過：436 份 Markdown、4,474 個本地連結；DocGraph 為
62 文件／213 關係、零錯誤。Artifact status 為 `ok=110`，
`git diff --check` 通過。另核對新 producer 的重建依賴包含原
`c5_941_three_spoke.py`，避免新 clone 在輸入尚未重建時先執行本輪 checker。

## 當輪停止點與可貼接手摘要

指定兩-unary 省略分支完成。下一窄題是同一 t=2、(2,1,1) 型的 binary
省略：剩下 r、U、V 的全 degree-4 核心中，r 有兩條內部 bridges，
先從既有 path／tail 的原 degree-2 root 分類接上任意原 binary A。
沿用本輪及前序全部 unit-pair 省略全收；保留完整有序 (x,y)、原接點、
實際附件、ownership 及共同色框。

> 在 `/home/ray/developer/ai/math` 先讀 HANDOFF、STATUS、Kempe 導覽及
> git status。基準仍為 bbd900a，工作樹有多輪未提交成果。新結果：
> ε=2、唯一 degree-6 root、t=2、(2,1,1) 的兩 unary 省略必全收；
> 3,980 必要比較全排除，24,975 完整五接點控制通過。重播
> `python3 scripts/c5_excess_two_two_unary.py --check`。
> 下一題為同型 binary 省略分支；未排除整型，未提高 ε≥2，未 Lean 化。
