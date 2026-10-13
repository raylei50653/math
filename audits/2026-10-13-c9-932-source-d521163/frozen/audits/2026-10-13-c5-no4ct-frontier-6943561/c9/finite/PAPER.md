# h=4 的完整 C9 介面：三支必要條件與 W5 弦側排除

2026-10-13；BASE `6943561e644e7598342d1ccd7df44dac0ebcd5cf`。
本文件接 [原圖幾何證明](../geometry/PROOF.md)，來源為所有目錄外 disk-C5
圖中全域最小內點、再最大邊數者；不使用四色定理、不改用固定 mask 最小性。
以下有限計算只遍歷完整邊界介面，不搜尋任意大小來源圖。

## 1. 有限介面覆蓋任意大小原內側

原 B 邊界超額 h=4 時，e=(e0,…,e4) 有 70 份有序分配；內圈 C9 的名字、
全部原 collar 邊及 14 份有向 annulus 三角面由原 rotation 固定；保存每點的
原 annulus rotation path，B 的外側正向與 C 的內側反向一併核對。各原 e 同時處理
932、933、941 三個完整 Σ 目標，不分別旋轉 pieces 或單獨重命名顏色。

每份原 collar 的幾何只可能是 induced C9 或一條短側 W5 的弦；完整候選
包括 70 份 induced 情形與 75 份具名弦位置，共 145 份幾何、435 個查詢。
75 份是來源必要條件的覆蓋，有些還可能被其他原外側拓撲排除；沒有宣稱
每份都可實現。弦側 mask 同時檢查原弦兩端異色和短 C5 恰用三色。

C9 有 19,680 份 proper literal 指派及 820 個共同 S4 色名軌道；其中三色
85 個、四色 735 個。每份軌道代表固定 literal 色名，enumerate 全部 compatible
原 B literal 指派，按共同 B 十列保存完整 annulus lifts，包含所有空 fibres。
總計 574,000 個具名 fibres，其中 530,845 個空；完整 annulus lifts 共 48,450 份。
任意實際 H 的完整染色必沿相同 literal C9 指派接到其中一份，反向亦成立。
本輪沒有捏造未知 H 的 full lifts。

## 2. 同一實際來源的必要支援縮減

設 S 是實際 H 的完整 C9 軌道支援，column(p) 是固定內列 p 所能接出的
全部 B 軌道。若完整 Σ(G)=t，必有

\[
p\in S\Longrightarrow column(p)\subseteq t,
\qquad \bigcup_{p\in S}column(p)=t.
\]

因此從所有 column(p)⊆t 的列開始；弦側先再交原 W5 mask。對每個支援列 p
與三份互補色對 split，實際 H 中 boundary 觸及的 Kempe components 在 C9
形成 noncrossing partition。相鄰且同一色對的原圈點必在同一 component。
獨立 flip 這些原 components 產生整份 orbit，全部仍在 S。

`check.py` 使用 frozen 的一般 Cn 規則 enumerate 全部相容 partitions／orbits。
即使有原弦，僅使用圈邊的規則也是安全上界：實際弦所迫的 component
連通性只會減少選項。若某列某 split 沒有整份 orbit 包含於目前上界 U，
刪掉該列。每步仍有 S⊆U；終止時若原 columns 的聯集不等於 t，則實際
來源不存在。這個論證不將不同色列或 pieces 的可行性合成共同染色。

在同一來源 k 下，no4ct 下降引理保證至多 k+5 點的 loopless planar graph
可染。C9 的 independent noncrossing partition 有 232 份；其 q-block 外側
樹收縮商圖有 k−9+q≤k 點。故每份 partition 必由同一 H 的某份完整染色
滿足，不同 blocks 可同色。若支援 U 連這項必要要求都無法滿足，排除該查詢。
弦側額外排除同一 block 包含原弦兩端的 partitions，以免商圖產生 loop。
此正性只在來源相對大小界內成立，不是普遍 4CT 前提。

## 3. 完整結果與來源結論

| 目標／induced C9 | transfer＋Kempe 排除 | 相對 quotient 排除 | 必要條件殘留 |
| --- | ---: | ---: | ---: |
| 932 | 50 | 0 | 20 |
| 933 | 44 | 0 | 26 |
| 941 | 28 | 4 | 38 |
| 合計 | 122 | 4 | 84 |

全部 75×3=225 份 W5 弦側查詢均由 transfer＋Kempe 排除。不是全部 fixed
points 都空：75 份最後仍有非空支援，卻無法接出目標的全部接受列；其餘
150 份支援為空。故不能把「非空支援」當成來源或完整目標實現。

由幾何覆蓋及此必要 screen，得到新來源定理：

\[
\boxed{h=4\Longrightarrow\text{原內圈 C9 induced}.}
\]

在原共同對齊下，932 的 20 份 e 僅有兩種完整家族：兩個不相鄰的 2
（5 份），或三個連續正項為 {2,1,1}、兩個零相鄰（15 份）。因此

\[
\boxed{\Sigma(G)=932,\ h=4\Longrightarrow4\le d_G(b_i)\le6
\quad\text{for every original }b_i.}
\]

三支共同有 e_i≤3，故在 h=4 下原 B 度数≤7。以上上界沒有推广到 h≥5。
完整 435 項 ledger 見 [RESULTS](../RESULTS.json)，原具名關係／full lifts
見 [certificate](certificate.v2.json.gz)，來源採納界線見 [ADOPTION](../geometry/ADOPTION.md)。

## 4. 驗證及下一個精確義務

```bash
python3 -B audits/2026-10-13-c5-no4ct-frontier-6943561/c9/finite/check.py --check --negative
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c5-no4ct-frontier-6943561/c9/finite/check.py --check --negative
```

producer 從 frozen 一般 Cn 規則重播，並以完整 certificate 比對全部輸出；
另由 [獨立覆核](../review/REVIEW.md)重建所有具名 annulus fibres、非交叉
partitions、Kempe obligations 和全部查詢，不能只比對總數。

84 項是各具名 e／目標的必要條件殘留；仍未證實任一項有同圖來源。
下一義務是用同一 H 的實際 extension counts／Kempe orbit weights，排除這些
支援的共同實現，或先修復 A 點 H-degree≥4 的 C9 版本。現有幾何只给
A degree≥3、Y degree≥4，不能沿用 C8 apex 引理的數字或 274 維計數式。
h≥5 是另外保留的 OPEN 範圍；一般 k≥16／h≥3／n5≥9、932 的 h≥4／n5≥10
及一般主命題均不因本輪提高。沒有新增 Lean theorem 或四色定理的新證明。

初始 `certificate.json.gz` 保留，作非權威 prototype；最終 checker 僅讀 v2。
v2 補齊有向原面與 rotation paths，所有數學支援／排除結果與 prototype 相同。
輸出均採 exclusive-create，已有檔案時拒絕覆寫。
