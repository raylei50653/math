# 3903：空交集分支的框鄰點身份與內部葉點排除

發布紀錄：本報告與相關證書合併於 [STATUS §70](STATUS.md#70-3903-空分支後繼與-331-四輪成果發布)；
以下「未提交」及停止點描述本研究輪當時狀態，目前入口見 [HANDOFF](HANDOFF.md)。

後續：[空分支末端 block 排除](c5_sector_empty_terminal.md) 已完成空交集分支；
合併非空分支，只排除具指定 sector 前提與兩拒絕列的 397→330 交換。
一般 3903 仍開放；以下保留本報告研究輪的狀態。

2026-09-22，從乾淨 `56faeb4` 接手。接續
[非空分支排除](c5_sector_terminal_blocks.md)，本輪只處理
**N_G(0)∩B₃=∅**。得到兩項任意大小必要條件：
**C 沒有葉點；0 至少有一個舊色 1 鄰點，且每個此類鄰點的框鄰集
恰為 {0}，內部度數恰為 3。** 未排除空交集分支或一般 3903。

## 1. 同一圖、同一交換的前提

Γ=(0,1,2,3,4) 是 K 的指定 induced disk 外框；G=K−{01,04}。
C 是非空連通內部，內點完整 degree≤4，deg_G(0)=2。
固定 proper c，舊框列 01021；S 是 maximal 0/1 分量，
S∩Γ={0,1,2}。c′ 僅在此 S 交換，原始新框列為 **10121**。
來源 profile 397、正規化候選 profile 330 都取這同一次交換。
B₃ 始終是 G[c′∈{0,2}]−{1} 中包含 3 的分量。

3903 的拒絕列 α=01212，配合連通 C，依
[緊 list 論證](c5_sector_rejection_lists.md#1-拒絕列強迫每點都緊)，
迫使每內點完整 degree=4，且 α 在 A(v)=N_G(v)∩Γ 上單射。
本輪只用此一拒絕列，不需另用 δ=01213。

從完整 profiles 讀出的必要分離為：舊 02、03 中 0 與 2 分離；
新原始 12、13 中 0 與 4 分離。來源／候選另給舊 13 的 1–4 路徑
與新原始 02 的 1–3 路徑，故既有兩種飽和 star 分離定理適用。
不能把正規化的新 02 與原始的新 02 混為一談。

## 2. 不借用非空分支的 b 身份

S 連通且包含 0、1，從 0 出發的 S 路徑第一點必是內點，舊色 1。
任取一個這樣的鄰點 b；它因鄰接 0 而自動屬於同一 maximal S。
不宣稱另一個 0 鄰點的顏色，也不命名 w,p,q,r。

properness 排除 b1、b4。若有 b3，交換後 c′(b)=0，而 c′(3)=2；
邊 b3 在新 02 刪 1 後仍存在，故 b∈N(0)∩B₃，違反空交集。

若有 b2，則 0–b–2 是 S−{1} 中的 Γ-path。
[雙 star 分離定理](c5_sector_saturated_cuts.md#2-兩種分離集定理)
迫使此路徑分別碰 T₂、T₃；唯一內點 b 必同時屬於兩者。
但其完整鄰色不可能既為 0,0,2,2 又為 0,0,3,3，矛盾。
即使原先考慮「刪 1 切斷」情形，假設的 b2 邊本身也提供了這條路徑，
所以沒有漏掉切斷分支。

因此 **A(b)={0}、deg_C(b)=3**，而且對每個舊色 1 的 0 鄰點都成立。
這不代表 N(0) 的兩點都是色 1，也不代表涉及 0 的混合分離自動成立。

## 3. 七種葉點身份全部排除

若 v 是 C 葉點，degree 緊性迫使 |A(v)|=3。
α 單射性只允許下表四個框鄰集；舊 properness 給七個色別。

| A(v) | c(v) | 同一圖上的矛盾 |
| --- | --- | --- |
| {0,1,2} | 2 | 舊 02 路徑 0–v–2 |
| {0,1,2} | 3 | 舊 03 路徑 0–v–2 |
| {0,1,4} | 2 | 新原始 12 路徑 0–v–4 |
| {0,1,4} | 3 | 新原始 13 路徑 0–v–4 |
| {0,2,3} | 1 | v∈S、c′(v)=0，邊 v3 迫使 v∈B₃ |
| {0,2,3} | 3 | 舊 03 路徑 0–v–2 |
| {0,3,4} | 3 | 新原始 13 路徑 0–v–4 |

色 2、3 不受交換影響；色 1 的情形由 v0 強迫 v∈S。
前六項分離矛盾（表中除 B₃ 那項）不需 disk，最後一類由空交集排除。
沒有替 v 指定圈外鄰點、沒有使用 degree≤4 的框點假設。

C 若僅一點，其 degree=4 要求四個框鄰居，亦不可能對只有三色的 α
單射。由連通、非單點且無葉點得到 **δ(C)≥2**。

## 4. 停止點與下一個窄問題

空交集分支現在具備 δ(C)≥2，且有一個 A(b)={0}、deg_C(b)=3 的
實際點。可接續核對末端奇圈／K4 的兩列完整 root 介面：
先檢查含框點 0 的 private attachment 類能否容納 b 與 deg_G(0)=2，
再處理 b 到 root 的真實接回路徑、單一 block 與共用 root 情形。
這些是待證項目；不直接搬用非空分支的 w 度數或 corner 次序。
中間 bridges 保留，兩個拒絕列必共用實際 attachments。

本輪沒有完成末端 block 拓撲合成，沒有使用 Gallai 結構來聲稱分支已排除。
一般總體 ≥6 下界、603 profiles 與固定點不變；一般 3903、R31、共同出口
及 K∞=K≤5 仍未證。

## 5. 證書與驗證界線

[checker](../scripts/c5_sector_empty_branch.py) 與
[JSON](../artifacts/c5_sector_empty_branch/observations.json) 直接讀取既有
397／330 的完整框分割，核對色正規化、七種局部葉點的路徑與分離、
四種舊色 1 鄰點框鄰集及兩個互斥 star 鄰色型，保存依賴 hashes。
這是必要局部配置的完整小表，不是候選圖或染色搜尋，不是空分支實現。
任意大小的結論由 §1–3 紙面證明與既有 disk 分離引理承擔；未新增 Lean theorem。

```bash
uv run python scripts/c5_sector_empty_branch.py --check
uv run python scripts/c5_sector_rejection_lists.py --check
uv run --with networkx==3.5 python scripts/c5_sector_saturated_cuts.py --check
lake build
git diff --check
```

本輪上述三份 checker、Lean build、變更文件本地連結與 whitespace 通過。
terminal-blocks、transition-control、其他 standalone、minimality 及 R 系列
未重跑；前輪非空排除沿用既有成果。未 commit／push。
