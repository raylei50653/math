# D₄：B₃ 固定快照獨立稽核

結論：固定快照中的 B₃ payload 與五型原 K₅ 紙面論證通過本次獨立覆核。
可與既有 B₂ 的短 face 結論合用，**只登記 W933-101、W941-139 兩份具名骨架已封閉**。
原 B 的 20／20 literal 必要列完整保留；各移除一個 primary key 後，其餘 **19／19** 本輪未新判。
W933-171、W941-279 的 root-swap 對應已核對為 transport 證據，沒有另登記來源閉合。
不推 mixed22 整型、ε≥3、來源實現、一般出口、K∞=K≤5，沒有新增 Lean theorem。

本層只讀 [D₄ 固定 production 快照](../snapshot/README.md)，只寫 `b3/`。
採用 D₂ audit-local [independent_core.py](independent_core.py) 的新 MRV 枚舉器、原邊 BFS、
本輪 Tarjan block 分解及 literal join 重算；沒有 import production producer/helper/validator。
來源、完整 relations、空 fibres、witnesses 與歷史 artifacts 沒有改寫。

## 任意大小紙面覆核

覆核使用有限簡單原 G、固定 induced C₅ disk 外框、完整 Σ-critical 與原 (5,5) q-core 等
既有 B 前提。C 是 H−{a,b} 的同一份原連通分量；全部原邊、ownership、附件、bridges、
旁支與有序 contacts 保持。任意大小结論不是對 16 份 fixed controls 作外推。

1. 對每個被拒絕 q 的每個合法原 G−C root pair，由完整 C-degree 四可得 exact lists
   至少 internal degree。若存在 strict slack，沿距該點遞減的順序貪婪著色原 C，矛盾。
   因此所有實際外鄰顏色必須互異。跨全部拒絕列求交得到四 owner 的必要表。
   每種 owner 的最低 C-degree 都是二；所有 terminal bridges 均排除。
   shared 點若內度一，額外框鄰只能是 0／3／4；0 必須用 row 6，而 3／4 用 row 1。
   row 1 單獨容許 shared 接 0，不能丟掉跨列求交。內度二的 shared 點可以處於內部橋鏈。
2. 拒絕 degree assignment 使 C 為 Gallai tree。terminal odd cycle 的 private 路徑上，
   每個相鄰點都不是 C 的 cutvertex，故 exact lists 相同；兩個合法 pairs (3,1)、(2,3)
   在同一 row 01021 的五個有序 list signatures 互異，連同實際附件識別五 leaf 型。
   nonowner 04 和 nonowner 34 雖有相同 missing-color membership，完整 signatures 不同。
3. K₄ block 每點除三條 clique 邊外只剩一條 incidence。若不直達 X=B∪{a,b}，該邊是原
   block-tree 的 bridge；沿其有限側取 terminal private 點，planarity 排掉 K₅ clique，
   此 private 點的 C-degree≤3，由完整 degree 四得到實際 X 邊。四個側在原 C 中互斥；
   否則原 block/bridge 身份失效。連通 X 與四條實際 tethers 形成第五袋，提取 K₅。
   這不需要固定 root pair 後逐邊 minimality，也不補未用 degree 邊。
4. 排掉 K₄ 與 terminal bridges 後，terminal blocks 是 odd cycles。若只有一個 block，
   private vertices 全部同一 owner/附件；nonowner 違反 contacts 存在，其餘 owner 每類
   原頂點最多二，小於 odd cycle 長度。因此至少兩個 terminal odd cycles。
   帶 owner 的 leaf 必為 triangle；nonowner leaf 長度仍無上界。
5. 在任一 leaf 選相鄰 private u,w。刪兩點後，原 cycle 餘段包含 cutvertex；其他 blocks
   原樣附著，故 C′ 連通。共同 hubs h,k 相鄰且各接 u,w。E′=X−{h,k} 的表列路徑確為
   同一原骨架的全部餘點。nonowner／a-only／b-only 分別由剩餘原 contacts 接 C′ 到 E′。
   shared leaf 的兩 private 點耗盡四角色，另一 terminal leaf 因而是 nonowner，實際
   04／34 附件將 C′ 接到 B。O=C′∪E′ 連通，並有到 h,k,u,w 的四條原邊。
   {h},{k},{u},{w},O 互斥、連通，十對鄰接都是原邊，給原 K₅ minor，與 disk 矛盾。

所用主來源為 [Dvořák 的原始講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本輪 live 核對 Lemma 7、Corollary 8、Theorem 10 的連通性、degree-assignment、
noncutvertex 前提。原 PDF 保存在 [gallai-primary.pdf](gallai-primary.pdf)，
來源日期、hash、逐項適用條件見 [primary_source_review.json](primary_source_review.json)。
此紙面審查仍未 Lean 化；固定 Python controls 本身不證 disk topology 或任意大小 leaf 定理。

## 獨立重算覆蓋

| 項目 | cycle 14 圖 | internal shared bridge 2 圖 | 合計 |
| --- | ---: | ---: | ---: |
| 完整有序 R_C | 140 | 20 | 160 |
| 完整原圖／spoke omission／G−C joints | 840 | 120 | 960 |
| pinned literal root-pair fibres | 13,440 | 1,920 | 15,360 |
| 明列空 fibres | 10,024 | 1,432 | 11,456 |
| spoke 接回 | 560 | 80 | 640 |
| root-swap variants | 420 | 60 | 480 |
| 共同 global S₄ R_C | 3,360 | 480 | 3,840 |
| 額外直接重算 S₄ whole-graph joints | 20,160 | 2,880 | 23,040 |
| S₄ 原 joint witness 搬運 | 257,280 | 16,656 | 273,936 |

逐份重算原 degree、attachments、supports、contacts 別名與共享相等座標，並核對全部
2,646 份 R_C witnesses、11,414 份 joint witnesses、11,414 份 fibre witnesses。
所有 fibre witnesses 必須是同一原圖、同一 literal β、同一 root pair 的完整 coloring；
沒有用 marginals 或獨立 normalization 替代 joint。

其他完整覆蓋為 52 份實際 attachment 候選、546 份拒絕 row/pair 精確 lists，
5 種原 leaf signatures，6 份按 mask 分列的 shared degree-one strict-slack 控制及
3 份共通 ledger witnesses。兩份 degree-two shared internal bridge 正控制各直接
刪去兩條 incident 原 C 邊，4 次均斷開；原 bridges 与空附件∅保留。

30 份原 leaf K₅ 分別為 nonowner04／34 各 6、a0／b3 各 3、sharedab 12；
逐袋 BFS 驗原連通與互斥，逐對核對 300 條原鄰接、42 份原外部路徑。
long nonowner private points 分成兩個連通袋，與任意大小紙面選兩個相鄰點的五袋
是不同但各自有效的固定證書。另覆核既有 2 份 K₄ tether controls 的 20 原鄰接、
8 原路徑；它們沒有補齊所有 degree，與 16 份完整 degree controls 分開標示。

## 重播、版本保存與停止點

```bash
python3 audits/2026-10-04-task-d4/b3/audit_b3.py
```

每次執行在 `attempts/0001` 起建立新資料夾，保存当次 audit/solver 版本、log、
results 和 exception；成功輸出再同步 [results.json](results.json)，失敗紀錄不覆寫。
本輪第一次執行通過；第二次增加 producer summary 與獨立 counters 的逐欄核對後也通過。
沒有本輪失敗嘗試；舊 D／D₂／D₃ 與 B₃ 原工作所記失敗保持原樣。
Production 重播与全輪 docs／DocGraph／artifact／diff 驗證由 D₄ root 統一保存。

最新停止點為兩份具名長 face 七身份零殘留，與 B₂ 合用僅登記兩 primary W 全部 faces
封閉。原 B 20／20 必要表與其他 19／19 literal keys 保留；本輪沒有擴張到其他骨架、
933 原 04／12 shared 附件{4}分支，亦不登記 root-swap counterpart 的新增閉合。
未 commit／push。
