# 2026-10-03：t=2、(2,1,1) 原 binary 省略排除

接手基準 `main@bbd900a`，保留兩 unary 省略及其他前輪全部未提交成果。
未要求 commit／push，本輪亦未執行。先核對 HANDOFF、STATUS、Kempe
導覽與工作樹，重播兩 unary 證書後，接續其明列的 binary 省略分支。

成果見 [專題報告](../c5_excess_two_binary_two_unary.md)，目前接手入口見
[Kempe 導覽](../c5_kempe_guide.md)。研究線及進行中狀態未改，依文件治理
保留 HANDOFF 薄索引；更新 README、STATUS、導覽與前序的後續關係。

## 結果與證據

933／941 固定完整 Σ、edge-minimal C₅ disk 來源，在 ε=2、唯一 degree-6
root、t=2、(2,1,1) 前提下，省略整份原 binary A 必全收十列。
連同前序，該型所有容量二省略均全收，已無全 degree-4 minimal
rejected-row core；沒有排除整份 (2,1,1)，共同下界仍 ε≥2。

原接點 (r,x,y,u,v)、原三分量及完整 relations 保持。省略核心只缺
q₀，迫兩份原 unary 恰有一份 D carrier；兩份都完整保留在同一
K₄-free Gallai 核心中，故共同支援跨度至少 2 與 1。A 不加正跨度。
不需要 path／tail 正常形枚舉或原 binary 圖生成器。

- 700 份代數比較；933／941 分別保留 320／240 份。
- 2,340 份共同原支援包絡；上述殘留的 37,200／27,900 次比較全排除。
- 全部 65,535 份非空有序 binary relation 的投影核對。
- 13 份完整 binary relation 的全部 unary domains／spoke 色集，合計
  46,800 次完整五接點接合；另有 176 次穩定子控制。
- 證書保留全部代數 row options、具名 arcs、原 case／geometry 引用及
  逐比較空列；保留同 marginals 不同禁色的反例。

任意大小涵蓋由紙面 slack、飽和／全 degree-4 分類、同圖 D 守恆及
共同支援 lifts 負責。Python 只排除固定放寬必要域，不證來源實現性；
未新增 Lean theorem，一般出口與 K∞=K≤5 仍未證。

## 實際驗證

```bash
python3 scripts/c5_excess_two_two_unary.py --check
python3 scripts/c5_excess_two_binary_two_unary.py
python3 scripts/c5_excess_two_binary_two_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_binary_two_unary.py --check
python3 scripts/c5_excess_two_spoke_unary.py --check
python3 scripts/c5_excess_two_double_spoke.py --check
python3 scripts/c5_single_spoke_root_conservation.py --check
lake build
uv run --with-requirements requirements.txt python tools/artifacts.py record artifacts/c5_excess_two_binary_two_unary/observations.json
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 在預設及 `PYTHONHASHSEED=17` 下逐位元組重播通過。
上述四份前序 checker 通過。`lake build` 成功（8,831 jobs、既有
linter warnings）；不表示新紙面證明 Lean 化。沿用全 degree-4 分類及
外部 degree-list 的歷史證據，未重跑全部歷史模板或其他研究線。
新 artifact 為 10,750,259 bytes，已登錄 MANIFEST／producer 及產生檔
ignore 規則。新 checker 不讀舊 artifacts，不需另加產生器輸入順序。

文件檢查通過：438 份 Markdown、4,497 個本地連結；DocGraph 為
62 文件／213 關係、零錯誤。Artifact status 為 `ok=111`；
`git diff --check` 通過。全部前輪未提交成果保留，未 commit／push。

## 當輪停止點與可貼接手摘要

完成指定 binary 省略分支。下一窄題為唯一 degree-6 root、t=2、
(1,1,1,1) 的四原 unary：先用四因子子覆蓋、具名兩-unary 省略身份、
D 守恆與同一兩-spoke 支援。其他 ε=2 分支保留。

> 在 `/home/ray/developer/ai/math` 先讀 HANDOFF、STATUS、Kempe 導覽及
> git status。基準仍 `main@bbd900a`，多輪未提交成果保留。新結果：
> ε=2、唯一 degree-6 root、t=2、(2,1,1) 的原 binary 省略必全收十列；
> 560 個代數殘留的 65,100 次共同支援弧比較全排除，46,800 完整五接點
> 控制通過。重播 `python3 scripts/c5_excess_two_binary_two_unary.py --check`。
> 該型已無全 degree-4 minimal rejected-row core，但未排除整型，未提高
> ε≥2，未 Lean 化。下一題為 t=2、(1,1,1,1) 四原 unary。
