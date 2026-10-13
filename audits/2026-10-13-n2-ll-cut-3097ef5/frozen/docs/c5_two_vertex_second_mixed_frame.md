# C₅ 反向接合的第二混合外框：完整 R1022 與雙內點代表

2026-09-30。接續[第一混合外框](c5_two_vertex_mixed_frame.md)，只核對
同一 `private_interiors_reverse` 見證的另一五邊形面
`(a0,b4,b0,a2,a1)`。**此具名順序的完整 relation 恰為 R1022：
9 個全域 S₄ 軌道、216 份具名賦色，只拒絕 proper pattern `01012`。**
完整 J 投影、原圖十內點延拓、來源部分關係及既有雙內點 disk 代表
全部一致。證據為紙面推導＋Python 固定圖證書，未新增 Lean theorem。
本輪完成指定框；目前停止點見[兩點重疊導覽](c5_two_vertex_overlap_guide.md)。

2026-09-30 後續：[兩框共同拉回](c5_two_vertex_mixed_pullback.md)已完成，
有 114 軌道，較原 J 多 54；補回 b2–b4 仍多 16，另加兩條四點
跨框條件後精確還原 J。完整差集、分別延拓及原邊拒絕全保存；
下文保留第二框輪的當時停止點，原證書不變。

## 1. 同圖換外面與量化範圍

來源仍是 R127 `(0,2)` 接 R167 `(3,1)`，識別 a0=b3、a2=b1。
十五點、三十五條原邊、七個來源私有內點及全部具名映射均保留。

```text
U  = (a0, a1, a2, a3, a4, b0, b2, b4)
C₂ = (a0, b4, b0, a2, a1)       在 U 的索引為 (0,7,5,2,1)
H₂ = (a3, a4, b2)
```

對 C₂ 的 relation 查詢存在量化 H₂ 及
`A_inner5,…,A_inner9,B_inner5,B_inner6`，共十個內點。
沒有刪邊、額外識別或更換來源代表。

[證書](../artifacts/c5_two_vertex_overlap/second_mixed_frame_relation.json)
重播[反向拓撲](c5_two_vertex_private_reverse_topology.md)相同的 rotation、
70 條有向邊及 22 面，只將外面由 19 改為 21。原面 21 正是 C₂；
切開框的面對偶後，外側只有面 21，內側有其餘 21 面。
五條框邊、30 條內側邊、零條外側邊；十內點的 incident edges
全在內側。按指定框方向，有界側為左側。

連通 rotation 的 Euler 值為 2；球面嵌入中選此 simple 面作無界面，
給出整圖的 C₂-disk 實現。這個拓撲推論屬紙面層；沒有分類其他環序。
同一 rotation 恰有兩個五邊形面，本輪連同前輪完成這兩面的 relation，
不等於枚舉原圖所有五環或所有可能外框。

同一色框中的定義為

\[
R_{C_2}(q)=\exists c_{a3},c_{a4},c_{b2}\;
 R_{127}(c_{a0},c_{a1},c_{a2},c_{a3},c_{a4})
 \land R_{167}(c_{b0},c_{a2},c_{b2},c_{a0},c_{b4}),
\]

其中 $q=(c_{a0},c_{b4},c_{b0},c_{a2},c_{a1})$；來源 relation 已量化
各自私有內點。這是原完整八點 J 的投影。

## 2. 完整 relation 與原 J 纖維

採用[目錄的固定十列順序](c5_cell_enumerator.md#02-一個-bit-的精確語義)。
每個 proper C₅ pattern 的全域 S₄ 軌道大小為 24。「纖維」是固定
表中 q 的具名顏色後，全部可行 H₂ tuples 的數量；不是原圖十內點
延拓總數。Proper C₅ 至少用三色，因此其 S₄ stabilizer 為平凡群，
此數也等於投到該 q 軌道的原 J 軌道數。

| bit | C₂ 的 pattern | 可延拓 | 完整 J 纖維大小 |
| ---: | --- | --- | ---: |
| 0 | `01012` | 否 | 0 |
| 1 | `01021` | 是 | 4 |
| 2 | `01023` | 是 | 4 |
| 3 | `01201` | 是 | 12 |
| 4 | `01202` | 是 | 12 |
| 5 | `01203` | 是 | 12 |
| 6 | `01212` | 是 | 4 |
| 7 | `01213` | 是 | 4 |
| 8 | `01231` | 是 | 4 |
| 9 | `01232` | 是 | 4 |

Mask 是 $\sum_{i=1}^9 2^i=1022$，接受 $9\cdot24=216$ 份具名賦色。
纖維合計仍為 60，共同 S₄ 展開後還原原 J 的 1,440 份八點賦色。

Artifact 保存全部 216 份 q、十列完整纖維（含空纖維）、每筆完整
U tuple／H₂ tuple／十五點染色 witness，另有直接五點查詢所得的
九份原圖 witnesses。先按 C₂ 正規化，再將同一換色作用於整份 U
與全圖；不獨立正規化隱藏點。每份纖維都與原 J 展開後固定 q 的
完整集合比較，不只比較數量。

## 3. 精確條件與原邊拒絕證明

\[
\boxed{R_{C_2}(q)\iff\operatorname{Proper}_{C_5}(q)
       \land (q_0\ne q_2\ \lor\ q_1\ne q_3).}
\]

在 proper C₅ 下，後一條件等價於 $|\{q_0,q_1,q_2,q_3\}|\ge3$：
前四點形成三邊路徑，恰用兩色 iff 交替為 `0101`。
第五點需異於首、末兩色，因此全部失敗賦色共同換色後恰為 `01012`。

### 來源部分關係的完整合取

R127 投影到 `(a2,a1,a0)` 得 `010,012`／36 份賦色，恰為任意
proper 二邊路徑。R167 投影到 `(a0,b4,b0,a2)` 得
`0102,0120,0121,0123`／96 份賦色，恰為 proper 三邊路徑且至少用三色。
兩來源只共享 a0、a2，分別隱藏 `(a3,a4)` 與 b2；隱藏變數互斥，
故共同對齊具名顏色後，兩份完整部分關係的合取正好給出上述公式。
Checker 從完整來源 masks 計算兩份投影，與公式逐份集合比較。
來源代表的完整染色另由八點 checker 重播。

### 拒絕列的原三角形

對 `01012`，有 `(a0,b4,b0,a2,a1)=(0,1,0,1,2)`。
保留原圖三角形 `(b2,B_inner5,B_inner6)` 及下列具名原附件：

| 三角形點 | 已固定的原鄰點 | 可用色的上界 |
| --- | --- | --- |
| b2 | a0、a2 | `{2,3}` |
| B_inner5 | b0、b4 | `{2,3}` |
| B_inner6 | b0、a2 | `{2,3}` |

三角形不可能只用兩色。更明確地，若 b2=2，兩內點皆被迫為 3；
若 b2=3，兩內點皆被迫為 2；皆違反原邊 `B_inner5–B_inner6`。
證書保存並核對全部原附件、三角形三邊、兩個完整分支及衝突原邊。
其餘九列各有原十五點正常染色 witness，配合全域 S₄ 換色給出充分性。

**全部十組點對投影仍不足。** 合取 R1022 的所有具名點對投影，仍得到
proper C₅ 的全部 240 份賦色；五條對角點對皆自由。因此會誤收
`01012` 的整個 24 份軌道。此負控制由 checker 重算。

## 4. 既有雙內點 disk 代表與 D₅

[目錄](../artifacts/c5_cells/cells.json)的 `cells["1022"]` 是 C₅ 加
內點 h5、h6，原額外邊為

```text
h5–2, h5–3, h5–4, h6–0, h6–1, h6–4, h5–h6
(0,1,2,3,4) ↦ (a0,b4,b0,a2,a1)
```

此具名順序直接相等，不需 D₅ 再對齊。給定 proper q，兩內點的可用
色集分別為四色補去 `{q2,q3,q4}`、`{q0,q1,q4}`，均非空；原內邊
可染 iff 兩集不是相同 singleton。兩者同為相同 singleton iff
兩個鄰色三元集合相等且各含三色。由框邊 q1≠q2，可知這恰要求
q0=q2、q1=q3，亦即上述唯一拒絕軌道。

Checker 另窮查此七點十二邊圖的全部 `4^5` 框賦色，並保存 rotation、
七面及 C₂ 作外面的 disk 證書；其有界側亦為左側。這是獨立核對的
同 relation 代表，不宣稱是原圖 minor，也不宣稱內點數最小。

十個 D₅ 位置作用全部保存，約定 `new_q[i]=old_q[permutation[i]]`
後再共同換色正規化。其軌道 masks 為
`959,1007,1015,1021,1022`，stabilizer 大小為 2（identity 與
`(3,2,1,0,4)`）。第一外框 R255 只有 8 個 S₄ 軌道，本框有 9 個，
所以二者不可能 D₅ 等價。

若未來染色 context 只在 C₂ 共享頂點、其餘十點全部密封，完整
relation 相等給出上述雙內點代表的染色替換，見
[密封與替換](local_closure.md#1-可以安全消去的是未來不會再接觸的內部)。
這不保持原八點介面、舊接點、內面或全圖延拓數；未指定的一般幾何
接合政策仍為 unknown。原 J 及其完整纖維均保留。

## 5. 重播、限制與停止點

[Checker](../scripts/c5_two_vertex_second_mixed_frame.py)只用標準函式庫。
SHA-256 綁定原目錄、八點 artifact、反向拓撲 companion、匯入 verifier
鏈及自身；舊 scripts／artifacts 不改寫。

```bash
python3 scripts/c5_two_vertex_second_mixed_frame.py
python3 scripts/c5_two_vertex_second_mixed_frame.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_second_mixed_frame.py --check
python3 scripts/c5_two_vertex_mixed_frame.py --check
python3 scripts/c5_two_vertex_private_reverse_topology.py --check
python3 scripts/c5_two_vertex_join.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

原 J 由 `4^8` 份賦色及七內點回溯重建；新框與小代表各窮查 `4^5`
份賦色。完整 J 投影、原圖十內點延拓、來源部分關係、精確公式及
小代表接受集全部一致。這些染色回溯共用既有 solver，不宣稱為不同
實作；原邊拒絕與全部接受 witnesses 提供可讀證據。每次重播另要求
三項擾動均被拒絕：把面 19 誤作本框外面、把接受列 `01021` 誤作
三角形拒絕、刪掉衝突原邊後仍宣稱相同拒絕證明。
實際驗證與未重跑範圍見[本輪紀錄](history/2026-09-30-c5-two-vertex-second-mixed-frame.md)。

本輪停止於同一 rotation 的第二五邊形面完整 relation；不遍歷其他
來源圖、環序或所有可能外框。尚未檢查兩個完整外框 relation 的共同
拉回能否還原原 J；此為[導覽](c5_two_vertex_overlap_guide.md)所列下一窄題。
完整後繼表、一般多步摘要充分性與 `K∞=K≤5` 保留。
未新增 Lean／`native_decide` 證明；`lake build` 只驗既有 Lean。
