# 2026-10-02：四容量子覆蓋共享、933 的 ε≥2 與 941 殘餘

發布整理（2026-10-02）：使用者後續要求 commit＋push，將本輪與前輪
容量下界的兩份 checker、兩份 artifact、報告及導覽／索引一起發布。
程式及證書沿用本對話已通過的重播與 Lean build；發布整理只補本段說明，
另核對證書記錄的來源 SHA，並重跑文件、DocGraph 及 staged whitespace 檢查。
下文「未要求／未 commit／push」保留研究完成時的語境；發布狀態以 Git 為準。

基準 `1274894`。接手時前輪容量下界的 script／artifact／report／索引尚未提交；
本輪在該工作區繼續，保留全部既有變更。使用者要求沿 ε=1、同源十列的
四容量子覆蓋與共享限制推進，未要求 commit／push。

成果見 [專題報告](../c5_excess_one_subcovers.md)，目前停止點由
[Kempe 導覽](../c5_kempe_guide.md)維護。HANDOFF 的 Kempe 進行中標記已符合
目前狀態，沿用前輪修改，沒有加入詳細研究結果。

## 成果與證據界線

- 省略一條 root-spoke 或一份單接點原分量後，若仍拒絕 q，完整 Σ 恰缺 q。
  因此不同列不能共用省略身份；每列至多兩個身份，缺額／重疊分類精確給出。
- 從既有來源引理抽出只需 T4 的 minimal degree-5 相鄰列分離。三-spoke
  使用 3703 的三拒絕排除與雙拒絕分類，不借用來源恰雙缺失的前提。
- 單接點分量跨三色列的 D／非 D 身份守恆，配合省略身份，證五單容量
  因子至多拒絕兩個 singleton 列。t=2 的核心矛盾是三個二元身份之
  兩兩和都等於一，迫偶數等於三。
- **933：ε≥2。** 四個拒絕列都需不同單容量省略身份，容量五迫全單容量，
  與上述限制矛盾。這排除 ε=1 分支，沒有排除 933 的一般來源。
- **941：ε=1 只餘單 binary 原分量 C₂，t=1、2、3。** q₀、q₁ 各有不同
  省略身份，C₂ 在兩列禁包含 D 的二色集；q₃ 全圖 minimal 時恰禁 {D}。
  t=1 的兩個 unary 身份已由 q₀、q₁ 用盡，故 q₃ 必為全圖 minimal。

任意大小結論沿用全 degree-4 分類、degree-5 指定雙列分離、sector 分類
及外部 degree-list／既有有限拓撲證據。Python 控制不代替那些紙面依賴；
本輪無新 Lean theorem、無新圖枚舉，也沒有把同一 binary 拆成獨立 unary。
941 的 ε≥2、一般 adjacent-singleton lemma、共同出口及 K∞=K≤5 仍未證。

## 實際驗證

已通過：

```bash
python3 scripts/c5_excess_one_subcovers.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_one_subcovers.py --check
python3 scripts/c5_independent_support_capacity.py --check
python3 scripts/c5_single_spoke_root_conservation.py --check
lake build
```

新 checker 核對七種容量分拆的 686 份四色覆蓋、120 組 Boolean 共享模型、
256 份三-spoke 接合控制，以及一張固定 943 圖的 16 個因子子集／160 次
完整十列檢查。保存原邊、全部接點 tuples、tuple witnesses、各 root 色的
完整 coloring；artifact 為 1,032,611 bytes。另保存移除 D 守恆後可三拒絕
的抽象控制，未聲稱它是圖 relation 或可實現來源。

前輪下界 checker 的 36 支援對／147 穩定子／46 條件介面控制重播通過。
單接點守恆 checker 的 2,632 份非 root 與 1,340 份 root palette 局部控制
通過，其既有 114 筆支援結論仍為 66 雙列、18 僅 p₁、30 僅 p₂；後續完成
狀態由原系列維護，不把這份歷史 artifact 改成最新累計。
Lean build 完成 8,831 jobs，只有既有 AttachmentOrder／SymRelabel lint。

文件及 whitespace 檢查亦通過：

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

文件檢查覆蓋 412 份 Markdown、4,207 個本地連結，anchors／索引／HANDOFF
皆通過。DocGraph 為 62 documents、213 relations、5 families，零 errors／notes。

本輪沒有重跑全 degree-4 模板分類、degree-5 全系列、sector 拓撲全表、
cell enumeration、Kempe screen、943 的原 rotation 或 Lean axiom audit。
既有定理前提經文件核對；有限資料未重播者沒有標成重新驗證。
未開子代理、未 commit／push；即時提交狀態以 Git 為準。

## 接手摘要

> 先讀 `docs/c5_excess_one_subcovers.md`。固定完整 Σ 的 edge-minimal 下，
> 933 已證 ε≥2；941 的 ε=1 只餘同一份二接點 C₂ 加三個單容量因子，
> root-spokes t=1、2、3。不同拒絕列不能共用四容量子覆蓋的省略身份，
> 單接點 C 的 D／非 D 身份在非空禁色列間守恆。q₀、q₁ 的 C₂ 都是含 D
> 的二色集；q₃ 若全圖 minimal，C₂ 恰禁 {D}。優先 t=1：(2,1,1) 兩 unary
> 分別提供 q₀、q₁ 的省略見證，q₃ 必全圖 minimal。保留同一 C₂ 的有序
> 兩接點、實際附件、完整十列，檢查兩份飽和列到 singleton-D 列的轉換，
> 不開新大圖枚舉。重播 `python3 scripts/c5_excess_one_subcovers.py --check`。
