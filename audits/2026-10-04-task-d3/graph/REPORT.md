# D₃：C₂ 原邊、刪邊 witness 與 K₅ 獨立稽核

2026-10-04。稽核 **D₂ 整合基準的 CPP-134-1／geometry 30／side_join_id 20**。
輸入使用 D₃ 凍結快照；C₂ artifact、script、report 三份 hashes 與 D₂
successor baseline 一致。獨立程式沒有 import 原 checker 或其 helpers。

**結果：2,513 項檢查，0 項失敗。** 四份人工破壞的 K₅ 路徑 negative
controls 均被捕獲。一次建立稽核程式時的 functions.exec JavaScript parse
failure 保存於 [attempts.json](attempts.json)；當次未写檔案，屬工具輸入失敗。
negative controls 的詳細失敗檢查保存在 [results.json](results.json)，没有改动
原 artifacts。

## 可重播證據

- [獨立程式](audit_c2_graph.py)：重建具名原邊、枚舉固定四色情況、驗證儲存 witnesses。
- [結果](results.json)：完整同色框 root-pair fibres、所有枚舉數、原邊分組、path/minor 檢查及 negative controls。
- [執行紀錄](run.log)與 [嘗試紀錄](attempts.json)。

```bash
python3 audits/2026-10-04-task-d3/graph/audit_c2_graph.py
```

預設輸入是
`audits/2026-10-04-task-d3/snapshot/`，只寫 graph/results.json。
原 artifacts、scripts、docs、歷史紀錄未由本分工修改；未 commit／push。

## 完整 tuples、actual attachments 與空 fibres

同一色框 q=01012，沒有 component-wise 正規化。獨立從原附件重建
P₃ lists 與完整 tuples：

- S₀={b₀,b₁,b₄}、S₁={b₁,b₄}、S₂={b₄}。
- 完整 tuples 恰 (3,0,1)、(3,0,3)。
- 16 個 root-pair fibres 全部具名保存；空 fibres 恰 (1,3)、(3,1)。
- side roles (8,1)，實際側支援 A_z={b₁}、A_w={b₂,b₄}，兩 root 原 spoke 均空。
- E_z={1}、E_w={1,3} 接 P₃ 後只有 (1,1)；保留原 zw 後 joint fibre 為空。

迫出的原 D_z contacts 是 (u₀,u₁,u₂)=(10,11,12)。每個 uᵢ 的實際外附件
恰 {b₁,z}，三條原 triangle 邊及六條原外附件共九邊。原 D_z=triangle
是紙面任意大小論證的結論；本固定域機械稽核不枚舉任意大小 D_z。
獨立關係枚舉得到：

```text
(0,2,3), (0,3,2), (2,0,3),
(2,3,0), (3,0,2), (3,2,0)
```

完整禁色恰 {0,2,3}；16 個 D_z root-pair fibres 中恰12個空，
僅 z=1 的四個 fibres 各有六 tuples。完整 intact pins 的染色數按
z=0,1,2,3 為 0,6,0,0。三份拒絕 palettes、四種原頂點身份與16個
pinned-list checks 均一致。

## 九條原邊的局部與投影刪邊 witnesses

獨立原圖投影保留：

| 原邊身份 | 條數 |
|---|---:|
| induced C5 frame | 5 |
| P₃ internal edges | 2 |
| P₃ actual boundary attachments | 6 |
| zw、zx₂、wx₂ | 3 |
| 迫出的原 unary triangle及附件 | 9 |
| 合計 | 25 |

九條 unary 相關邊逐條刪除，36份儲存的局部染色全部合法。獨立枚舉所有
三個 contact 顏色，任何被刪 unary 邊的16個局部 root-pair fibres 均非空。
每條 attachment 刪除的染色數按 z=0,1,2,3 為 2,6,2,2；每條 triangle
內邊刪除為 2,12,2,2。三個原拒絕色的27份 witnesses，刪邊兩端皆同色。

這36份 local witnesses 的邊約束是原 unary 局部九邊減一條；
z=1,w=1 的局部 witness 沒有加入原 zw 約束。它們只提供局部刪邊解除證據。

九份儲存的 partial witnesses 全部覆蓋13個具名原頂點，固定 q、z=0、
w=1，逐條符合其餘24條原投影邊。P₃ tuple 均為 (3,0,3)，刪邊兩端同色；
每條刪邊的完整投影枚舉恰有兩份染色。

原 D_w 的 actual support={b₂,b₄}、三個原 w contacts 與 forbidden={0,2}
保持原身份，其完整 tuples 未知。若同一原 D_w 的完整 relation 存在，
f_Dw={0,2} 使它必有一份避免 w=1 的 full tuple；這項邏輯存在性不枚舉
D_w，九份 partial witnesses 不稱為全 source colorings。

## 兩份 K₅ subdivision 的原邊與互斥性

兩份 subdivision 的 branch vertices 均為 b₁,z,u₀,u₁,u₂。
每份恰十個不同 unordered branch pairs，九條直接原邊由 unary triangle
及其附件提供；第十條是原外路 z 到 b₁：

| 外路 | 內點 | subdivision原邊 | 頂點 |
|---|---|---:|---:|
| z–x₂–b₄–b₃–b₂–b₁ | x₂,b₄,b₃,b₂ | 14 | 9 |
| z–x₂–b₄–b₀–b₁ | x₂,b₄,b₀ | 13 | 8 |

20份 paths 逐條驗證方向、指定端點、simple path、原邊 provenance、
內點不含任何 branch vertex。每份的45對 paths 全部檢查 interior disjoint、
edge disjoint，以及相交頂點恰為共同 branch endpoints。兩份共90對
edge-disjointness checks，全部通過；branch degree=4、internal degree=2。

兩份的五個 minor branch sets 逐組驗證非空、相互不交及原邊連通，
20份跨集合 adjacency witnesses 全部是原投影的實際原邊。長支的
Z={z,x₂,b₄,b₃,b₂}，短支的 Z={z,x₂,b₄,b₀}；外部 b₁ singleton 以
原 b₂b₁ 或 b₀b₁ 見證第十對 adjacency。兩組 Z 均不借用 w 或 D_w。

## K₄ tether controls 與紙面證據邊界

獨立核對全部 2⁴×2=32份控制：四个 K₄ singleton、端點為原 b₁ 或 z
的四條 tethers、可選的互異 subdivision vertices、hub 原連通性及
每份十對 adjacency。320份 adjacency witnesses 全部合法。

這32份 records 是固定 route controls；其新内部標號40–43是控制圖的
subdivision vertices，未當作原 source 已存在的頂點。任意原 K₄ block
的四條 tether 存在性、Gallai theorem 應用及 leaf-block counting 由紙面
獨立稽核承擔。

C₂ 的機械結果只核對指定 side_join_id 20；不能把整个 CPP-134-1 case、
其他 side joins 或 geometry 34 計為關閉。父層另外稽核 predecessor
保留 ledger，這份 graph 報告不修改該 ledger，也不推進 C₃。
沒有 target、Lean、完整 Σ、一般／共同出口或 K∞=K≤5 的新增宣稱。
