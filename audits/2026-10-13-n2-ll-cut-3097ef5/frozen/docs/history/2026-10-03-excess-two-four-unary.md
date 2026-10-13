# 2026-10-03：t=2 四原 unary 的固定支援排除

接手基準 `main@bbd900a`，保留前輪全部未提交成果；未要求或執行
commit／push。先讀 HANDOFF、STATUS、Kempe 導覽及原 binary 省略報告，
接續明列的 t=2、(1,1,1,1) 四原 unary 問題。

成果見 [專題報告](../c5_excess_two_four_unary.md)，目前停止點見
[Kempe 導覽](../c5_kempe_guide.md)。研究線與進行中 tag 未改，依文件
治理保留 HANDOFF 薄索引；更新 README、STATUS、導覽、研究綜述及
前序 binary 省略報告的後續連結。

## 結果與證據

933／941 固定完整 Σ、edge-minimal C₅ disk 來源，在 ε=2、唯一
degree-6 root、t=2 前提下，整份四原 unary 型不可能。

每條原 unary root 邊由 edge-minimality 取得私有禁色見證，四因子
子覆蓋保留該完整原分量。全 degree-4 分類遂給 K₄-free Gallai
前提，排除零點／單點框支援。四份固定原支援各至少跨一段，D 身份
另需一段；共同五段預算迫唯一 D 分量及其固定三點支援。每個拒絕列
都須由它禁 D，故拒絕 singleton 位置全在同一連續三點。933 有四點，
941 的三點不連續，兩者均排除。

沒有新增原圖枚舉或省略 pair 的跨列動態規劃；本輪紙面不依賴前輪
binary 或 spoke＋unary 有限接回表。完整 (r,x₀,x₁,x₂,x₃) 接合、
原分量、全部附件與單一色框保持；跨列只沿用同一原支援及 D 身份。

- 16 份具名 D 身份，恰四份通過「至少一 D＋五段跨度」必要限制。
- 25 次原框弧／singleton 位置等價控制。
- 50 次目標／固定弧比較全部排除，保留全部阻斷列。
- 五份連續三點正控制保留，未聲稱 disk 可實現。
- 3,360 份六-unit 覆蓋的完整四因子子覆蓋／私有色控制。
- 15⁴ 份非空 unary domains、16 個 spoke 色集，810,000 次完整
  五接點接合與 root 投影控制；artifact 為 46,639 bytes，低於大型
  artifact 門檻，保留為一般可追蹤檔案，未加入 MANIFEST／ignore。

這是任意大小紙面化約＋Python 固定域控制，未新增 Lean theorem。
沿用全 degree-4 分類、外部 degree-list、D 守恆與共同支援 lifts；
本輪未重跑全部歷史 topology 模板。其餘 ε=2、兩個 degree-5 roots
（含 mixed）、一般出口與 K∞=K≤5 保留，共同下界仍 ε≥2。

## 實際驗證

```bash
python3 scripts/c5_excess_two_four_unary.py
python3 scripts/c5_excess_two_four_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_unary.py --check
python3 scripts/c5_single_spoke_root_conservation.py --check
lake build
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新證書在預設及 `PYTHONHASHSEED=17` 下逐位元組重播通過，既有 D
守恆 checker 通過。`lake build` 成功（8,831 jobs、既有 linter
warnings），只確認既有 Lean 專案，不表示新紙面證明形式化。

文件檢查通過：440 份 Markdown、4,517 個本地連結；DocGraph 為
62 文件／213 關係、零錯誤。既有大型 artifact status 為 `ok=111`；
本輪小型 artifact 由上述新 checker 直接重播。`git diff --check`
通過，前輪未提交成果保留，未 commit／push。

## 當輪停止點與可貼接手摘要

四原 unary 整型排除完成。下一窄題選 t=1、(2,1,1,1) 的兩份原
unary 省略條件分支；只記錄方向，未啟動計算。其他 ε=2 分支保留。

> 在 `/home/ray/developer/ai/math` 先讀 HANDOFF、STATUS、Kempe 導覽及
> git status。基準仍 `main@bbd900a`，前輪未提交成果保留。新結果：
> 933／941 固定完整 Σ、edge-minimal disk、ε=2、唯一 degree-6 root
> 下，t=2、(1,1,1,1) 四原 unary 整型排除。固定支援五段預算迫唯一
> D 分量及連續三點拒絕位置，兩候選均不符；50 比較全排除，810,000
> 完整五接點控制通過。重播
> `python3 scripts/c5_excess_two_four_unary.py --check`。
> 新證據為紙面＋Python，未 Lean 化，共同下界仍 ε≥2。下一題為
> t=1、(2,1,1,1) 的兩原 unary 省略，保留同一原 binary 的有序接點、
> 三份原 unary、附件、ownership、環序與共用色框。未 commit／push。
