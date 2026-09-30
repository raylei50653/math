# C₅ 反向接合的混合外框：完整 R255 與單內點代表

2026-09-30。接續[反向私有內點拓撲](c5_two_vertex_private_reverse_topology.md)，
只核對 `private_interiors_reverse` 原十五點三十五邊圖的已保存外面
`(a0,a4,a3,a2,b2)`。**該具名順序的完整 relation 恰為 R255：
8 個全域 S₄ 軌道、192 份具名賦色；等於既有單內點 disk 代表。**
本輪完成指定框的核對，證據為紙面推導＋Python 固定圖證書，未新增
Lean theorem。目前停止點與下一題由[兩點重疊導覽](c5_two_vertex_overlap_guide.md)維護。

2026-09-30 後續：[第二五邊形面](c5_two_vertex_second_mixed_frame.md)
`(a0,b4,b0,a2,a1)` 已完成完整 R1022／9 軌道／216 賦色及雙內點
disk 代表核對，與本框非 D₅ 等價。下文保留第一框輪的當時停止點；
本輪原證書及原 J 不變。

2026-09-30 後續：[兩混合框共同拉回](c5_two_vertex_mixed_pullback.md)
有 114 軌道，較原 J 多 54；補回原邊 b2–b4 及兩條四點跨框條件
後精確還原 J。完整差集與原圖拒絕已保存；本框的單框 relation 與
密封替換範圍不變。

## 1. 同圖、同外面及存在量化的範圍

來源仍為 R127 `(0,2)` 接 R167 `(3,1)`，識別 a0=b3、a2=b1；
全部原邊、七個私有內點及具名映射不變。原八點介面、新框與隱藏點為

```text
U = (a0, a1, a2, a3, a4, b0, b2, b4)
C = (a0, a4, a3, a2, b2)       在 U 的索引為 (0,4,3,2,6)
H = (a1, b0, b4)
```

相對於 C，內部有十點：H 加上
`A_inner5,…,A_inner9,B_inner5,B_inner6`。它們在本次 relation
查詢中全部存在量化；沒有刪原邊、額外識別或替換來源圖。

[證書](../artifacts/c5_two_vertex_overlap/mixed_frame_relation.json)重新核對
反向見證的 70 條有向邊、22 面及 Euler=2，保留原面 19 作外面。
切開 C 的面對偶後，外側只有面 19，內側有其餘 21 面；五條框邊、
30 條內側邊、零條外側邊，十個內點的 incident edges 全在內側。
按 C 的具名方向，有界側為左側。球面補面與 simple 外面給出整圖的
C-disk 實現；此拓撲推論仍屬紙面層。

在同一色框下，完整關係是

\[
R_C(q)=\exists c_{a1},c_{b0},c_{b4}\;
 R_{127}(c_{a0},c_{a1},c_{a2},c_{a3},c_{a4})
 \land R_{167}(c_{b0},c_{a2},c_{b2},c_{a0},c_{b4}),
\]

其中 $q=(c_{a0},c_{a4},c_{a3},c_{a2},c_{b2})$，兩來源 relation
已各自量化原私有內點。這正是完整 J 的 C 投影，不是兩點摘要接合。

## 2. 完整表與原八點纖維

以下採用 [catalogue 的固定十列順序](c5_cell_enumerator.md#02-一個-bit-的精確語義)。
每個 proper C₅ pattern 至少用三色，其 S₄ 軌道恰有 24 份賦色。
「纖維」是**固定表中 q 顏色後**可行的 H 賦色數，亦等於投到該 q
軌道的原 J 軌道數；不是十內點全圖延拓的總數。

| bit | C 的 pattern | 可延拓 | 完整 J 纖維大小 |
| ---: | --- | --- | ---: |
| 0 | `01012` | 是 | 6 |
| 1 | `01021` | 是 | 6 |
| 2 | `01023` | 是 | 6 |
| 3 | `01201` | 是 | 12 |
| 4 | `01202` | 是 | 12 |
| 5 | `01203` | 是 | 12 |
| 6 | `01212` | 是 | 3 |
| 7 | `01213` | 是 | 3 |
| 8 | `01231` | 否 | 0 |
| 9 | `01232` | 否 | 0 |

因此 mask 是 $\sum_{i=0}^{7}2^i=255$，完整接受集合有 $8\cdot24=192$
份，proper C₅ 的其餘 48 份全部拒絕。纖維合計 60，展開共同 S₄
後精確還原原 J 的 1,440 份八點賦色。

Artifact 保存全部 192 份具名 q、十列（含兩個空纖維）、每個纖維的
完整 U tuple／H tuple／十五點染色 witness，以及直接五點查詢得到的
八份全圖 witnesses。先按新框正規化，再對整份 U 與全圖使用**同一**
顏色置換；不把投影與被隱藏點分別正規化。每份纖維再與原 J 展開後
固定該 q 的完整集合相等比較，沒有只比數量。

## 3. 四點限制與原邊拒絕證明

完整結果可寫成

\[
\boxed{R_C(q)\iff\operatorname{Proper}_{C_5}(q)
       \land |\{q_0,q_1,q_2,q_3\}|\le3.}
\]

一個可重播的來源分解是：R127 投影到 `(a0,a4,a3,a2)` 得到
`0101,0102,0120,0121` 四個 patterns／84 份賦色，恰為 proper
三邊路徑且四點未用滿四色；R167 投影到 `(a2,b2,a0)` 得到
`010,012`／36 份賦色，恰為任意 proper 二邊路徑。
兩來源只共用 a0、a2，隱藏變數各自私有，因此共同對齊這兩點後的
兩份完整部分關係合取，正好給出上式。這兩份部分關係由完整來源表
計算並逐份比較，來源代表的染色正確性另由八點接合 checker 重播。

兩個零 bit 還有不依賴查表的原邊拒絕見證。若前四點用滿四色，
共同換色為 `(a0,a4,a3,a2)=(0,1,2,3)`：

| 原內點 | 已知原鄰點 | 被迫顏色 |
| --- | --- | ---: |
| A_inner7 | a0、a3、a2 | 1 |
| A_inner6 | a0、a3、A_inner7 | 3 |
| A_inner8 | a0、a3、a4 | 3 |

但 `A_inner6–A_inner8` 是原邊，故矛盾。Proper C₅ 要求 b2 異於
a0、a2，僅剩 1 或 2，正是 `01231`、`01232`。Checker 核對
每一步具名原邊、禁色集合與最後衝突；其餘八列各有原十五點全圖
正見證，配合全域 S₄ 換色給出充分性。

**全部點對投影仍不足。** 對 R255 的全部十組點對取完整具名投影，
再求同時滿足這十份投影的五點賦色，結果仍是 C₅ 的全部 240 份。
即五條對角點對全自由；此四點限制不能從二元投影恢復。
兩個拒絕 patterns 是保存的負控制，誤收共 48 份賦色。

## 4. 既有 R255 單內點 disk 代表及替換界線

[既有目錄](../artifacts/c5_cells/cells.json)的 `cells["255"]` 恰為
C₅ 加一個私有點 h，額外邊為 `h–0,h–1,h–2,h–3`。
具名對應直接是

```text
(0,1,2,3,4) ↦ (a0,a4,a3,a2,b2)
```

不需再作 D₅ 旋轉或反射。h 能選到顏色 iff 四個鄰點未用滿四色，
所以其完整 relation 正是 §3。Checker 對這個六點九邊原目錄代表
另跑全部 `4^5` 份框賦色，與原十五點圖的完整接受集合比較。
另保存其 rotation、五面與 C 作外面的 disk 證書；這個小代表是獨立
驗證的同 relation 圖，不宣稱是原十五點圖的 minor。

若未來 context 只在 C 共享頂點，不接觸 H 或七個原私有內點，
完整 relation 相等給出染色可行性的 context 替換，符合
[密封與替換](local_closure.md#1-可以安全消去的是未來不會再接觸的內部)
的適用範圍。原 J 及全部纖維仍保留；本輪**未指定**未來可接觸政策，
也未證八點摘要可無條件縮成五點。原圖的內面、舊接點及全圖染色
延拓數並非此替換宣稱保持的資料。

## 5. 重播與信任界線

[Checker](../scripts/c5_two_vertex_mixed_frame.py)只用標準函式庫，
綁定原來源目錄、八點 artifact、反向拓撲 companion、自身及全部匯入
verifiers 的 SHA-256。舊 artifacts 不改寫。

```bash
python3 scripts/c5_two_vertex_mixed_frame.py
python3 scripts/c5_two_vertex_mixed_frame.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_mixed_frame.py --check
python3 scripts/c5_two_vertex_private_reverse_topology.py --check
python3 scripts/c5_two_vertex_join.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 窮查原八點 `4^8` 賦色及七內點延拓，重建完整 J；再以
C 為五點介面窮查 `4^5` 賦色及十內點延拓。完整 J 投影、直接原圖、
來源部分關係合取、四點公式及單內點代表五路結果相同。這些回溯
共用既有 graph solver，不宣稱為不同實作；原邊拒絕與全部接受 witnesses
提供另外的可讀證據。實際驗證及未重跑範圍見
[本輪紀錄](history/2026-09-30-c5-two-vertex-mixed-frame.md)。

此結果限於指定來源代表與指定外框，未遍歷其他外框／環序或同 Σ
的其他實現。另一個五邊形面的 relation、一般接合政策、完整後繼表、
多步幾何充分性與 `K∞=K≤5` 保留。未新增 Lean 或 `native_decide`
證明；`lake build` 只驗既有 Lean。
