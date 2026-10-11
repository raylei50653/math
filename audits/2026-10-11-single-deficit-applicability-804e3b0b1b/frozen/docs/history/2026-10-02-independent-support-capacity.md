# 2026-10-02：933／941 的第一個 excess／容量／跨度下界

基準 `1274894`，開始時工作區乾淨。使用者要求推進兩候選的 edge-minimal
disk sources，建立 degree-excess → forbidden-colour capacity → boundary-support
span 的第一個可證下界，優先尋找 ≥6 障礙，不做新大枚舉。
本輪採固定完整 Σ 的逐邊極小性；與固定拒絕列 q 的 minimal core 分開。

成果見 [專題報告](../c5_independent_support_capacity.md)，目前停止點由
[Kempe 導覽](../c5_kempe_guide.md)維護；HANDOFF 將本線加上進行中標記。

## 成果與界線

- 兩候選都必有效內部連通、碰全部五框點、ε≥1；任意兩份 minimal cores
  兩兩共用原 degree≥5 root。ε≥1 沿用既有全 degree-4 合成。
- 固定刪 root 後的完整染色，對原 degree-4 分量保留完整條件 tuples，
  得 D+O=degree−4；包含 mixed，O 也包含重色 spokes／其他 root 邊色。
- Unary 未用色 carrier 有 ℓ≥max(0,3−|F|)，同一 root 相容 lifts 總長≤5。
  三份 singleton D-carriers 迫 ≥6，故此配置不能為 disk。
- 尚未證 933／941 必含上述禁形，未證 ε≥2，沒有新的候選排除。
  ε=1 的 core 只可能整圖或恰省一條 spoke／一份單 incidence 分量，
  留下同源十列的四容量子覆蓋比較；不得把跨列支援不扣重複地相加。

## 實際驗證

下列命令已通過：

```bash
python3 scripts/c5_independent_support_capacity.py --check
PYTHONHASHSEED=17 python3 scripts/c5_independent_support_capacity.py --check
python3 scripts/c5_unattached_boundary.py --check
python3 scripts/c5_kempe_screen.py --check
lake build
```

新 checker：36 個有序支援交錯控制、147 個色穩定子控制、三張固定具名圖的
46 份條件介面。保存完整原邊集、contacts、tuples、刪 root 與 tuple witnesses、
逐邊新增列見證；artifact 約 180 KB。沒有產生新圖 catalogue。
既有未接內點 checker 重播 480 份改色、5,120 份 signature 控制及原應用。
Kempe screen 仍為 153／142／132，額外十個 masks 未變。
Lean build 完成 8,831 jobs，只有既有 AttachmentOrder／SymRelabel lint。

文件及 whitespace 檢查亦通過：

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

文件檢查：410 份 Markdown、4,179 個本地連結，anchors／索引／HANDOFF
均通過。DocGraph：62 documents、213 relations、5 families，零 errors／notes。

本輪未重跑 degree-4 整套分類、degree-5／mixed 系列、no-mixed 大表、
cell graph enumeration、943 的原 rotation、Lean axiom audit。
ε 下界的既有分類依賴與任意大小拓撲仍屬紙面／外部定理；本輪未新增 Lean。
未開子代理、未 commit／push；即時狀態以 Git 為準。

## 接手摘要

> 讀 `docs/c5_independent_support_capacity.md`。933／941 採完整 Σ 極小：
> 已證 ε≥1、內部連通及 cores 兩兩共用高 degree root。條件容量對 mixed
> 有效，但需同一份刪 root 見證；三份同 root、同 q 的 unary F={D} 迫
> 六跨度，尚未證候選必含此型。下一步處理 ε=1 單 root 的同源四容量
> 子覆蓋及跨列共享，不開新大枚舉。重播新 checker `--check`。
