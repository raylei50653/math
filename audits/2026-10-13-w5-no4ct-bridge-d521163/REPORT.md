# T3｜W5-NO4CT-BRIDGE：私人圈秩排除鏈的三支接入

2026-10-13。**完整成功：932／933／941 三支共同的 no4ct 私人 ρ≥5 定理已接通。**
本輪 BASE 為 `d5211633ba80c2b10cb12eaa8189421e35a31cc3`，研究在專屬 detached
worktree 進行；本包為新證明接入，舊報告、BASE、seal、manifest、證書與
成功／失敗 receipts 全部保留。沒有 commit／push。

## 1. 精確交付

K 為固定 K132。G 在**所有**完整 Σ(G)∉K 的有限簡單 plane disk-C5 圖中
先最小化內點數 k，再最大化邊數，採用既有 no4ct 三支來源定理鏈。
對 G 的**任意**合法全內部 induced W5，保留原框 B、中心 v、原鄰環 U，令

\[
P=V(G)\setminus(B\cup U\cup\{v\}),\qquad F=G[P].
\]

則在 932、933、941 三支皆有

\[
\boxed{\rho(F)=|E(F)|-|V(F)|+c(F)\ge5.}
\]

完整定理與來源到模板的證明在 [PROOF](PROOF.md)，逐項前提、三支與各圈秩
的接入矩陣在 [DEPENDENCIES](DEPENDENCIES.md)。不是固定 mask 最小性、普通
annulus、N2／ε／edge-critical 或 Gallai 結論。完整 degree 下界始終屬 G。

新增接點是：

1. 原 C4／proper C5（含接觸 B 者）皆有 `s≤k−i(C)<k`，可接已證受限
   cap 引理；由此取得原 B 附件界，另以原 `x-ui-v-uj-x` C4 證 U 附件界。
2. 抽出 mask 無關的局部前提 L，重新接回所有原面、分量、bridges、
   subdivisions、essential／contractible 分支與來源到模板的完整嵌入同構。
3. 新 k≥16 給 r≥10，落入舊完整必要域。森林直接由 r≤8 排除；其他圈秩
   以原全模板完整 Σ∈K 矛盾，不需一般 annulus 代表。

三份獨立分支審閱分別是 [森林至圈秩二](review/LOWRANK.md)、
[圈秩三](review/RANK3.md)、[圈秩四](review/RANK4.md)；
[最終獨立審閱](review/FINAL_REVIEW.md)再核對合併定理、量詞與證據界線。
**本輪没有剩餘低圈秩具名引理缺口。**

## 2. 沿用與本輪重播的分界

七份原 seal／manifest 共 407 筆記錄按原 SHA 接入，包括原證明、完整染色
證書、模板、摘要及 receipts。42 份本輪權威輸入以固定 BASE bytes 凍結。
完整清單、每個原 BASE、證書 SHA 及歷史共享文件的 publication 快照對應
均見 [INPUTS](INPUTS.json)；八個 archived 路徑直接校驗封存 blob 與原 bytes。
原 rank3-contractible seal 的八份共享文件使用已發布的歷史 gzip 快照，
不要求今日共享文件等於當時文件，也不改原 seal。

| 圈秩／分支 | 原完整必要模板數 | 新 r≥10 的 metadata 子域 |
|---|---:|---:|
| 森林 | 70 | 0，紙面大小矛盾 |
| 單環 essential | 1,652 | 252 |
| 雙環 contractible | 974 | 70 |
| 三 essential | 1,283 | 790 |
| 三 contractible | 2,270 | 484 |
| 四 contractible | 6,389 | 2,955 |
| 四 essential | 2,872 | 2,368 |
| 合計 | 15,510 | 6,919 |

子域數目只是從舊 summary／template index 過濾的必要超集，不是新生成圖數、
新的完整 fibre receipt 或真正最小來源數量。新 checker 另核對固定 K132 的
全部 D5 搬運封閉，以及原摘要全部 masks 的 membership。**本輪沒有重播
完整染色枚舉**；原完整 DFS／獨立 DFS／seed17／負控制沿用凍結 receipts。

本輪驗證與命令見 [VERIFICATION](VERIFICATION.json)。重播證據接點：

```bash
python3 -B audits/2026-10-13-w5-no4ct-bridge-d521163/evidence.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-no4ct-bridge-d521163/evidence.py
python3 -B audits/2026-10-13-w5-no4ct-bridge-d521163/verify_delivery.py
```

本輪正常與 seed17 輸出逐 byte 一致；損壞 proof hash、漏掉一筆 sealed record
兩項負控制均被拒絕。Checker 的 PASS 只指證據完整性、membership 及接點
計帳；任意來源覆蓋由紙面證明與獨立審閱承擔。

## 3. 檢查、文件路由與停止點

主工作樹 `scripts/check_docs.py` 通過：674 Markdown／8,720 本地連結。
正式 docs DocGraph 通過：95 documents／352 relations。
隔離 checkout 文件檢查保留失敗紀錄：部分歷史路徑並未在 BASE Git／archive
中交付；已能按 archive 還原者只還原原 bytes，未把本輪成果誤報成修復這些
歷史問題。全樹 DocGraph 仍有 63 個既有重複 ID 錯誤，未刪任何凍結證據。
本包自身的連結、anchors、文字空白及交付 seal 另作完整核對。

本次只交付專屬 audit；共享入口的原證明鏈仍是歷史契約，沒有被本輪直接
改寫。已核對直接父入口與 consumers，具體接入位置及 reviewed-unchanged
理由見 [ROUTING](ROUTING.md)。這是證明交付，未執行提交或發布。

真正全域最小目錄外來源仍為 `not triggered`；零觸發不證排除。本定理是
**no4ct 上游紙面／外部有限計算＋本輪紙面橋接＋原有限完整證書**的條件結論，
沒有新增 Lean theorem，也沒有重算上游外部計數或 plantri 完整域。
一般 ρ≥5 來源縮減、無界 932／933／941 排除及 K∞=K≤5 仍 **OPEN**。
普遍九點 W5 代表不屬本任務；沒有展開圈秩五／六枚舉。
