# C₅ 兩混合框共同拉回：54 個假接受軌道與精確修復

**2026-10-02 形式化後續：** [NamedRepair](lean_named_repair.md) 已補兩個核心的
具名原圖 J、指定兩框 P、完整 W／C 及 repair 分類。指定框 P 內的精確 repair 等式已由 NamedRepair 形式化；軌道數、完整差集與拓撲證書仍為 Python／紙面。
下文保留原輪次的計算與證據界線；disk 框完備性仍未 Lean 化。


2026-09-30。接續[第一混合框 R255](c5_two_vertex_mixed_frame.md)與
[第二混合框 R1022](c5_two_vertex_second_mixed_frame.md)，只處理原
`private_interiors_reverse` 十五點三十五邊圖。**兩框的完整 relation
共同拉回不等於原 J：拉回有 114 軌道／2,736 份賦色，原 J 有
60 軌道／1,440 份，差集為 54 軌道／1,296 份。**
補回一條原邊仍剩 16 個假接受軌道；再加入兩條四點跨框條件後
恰好還原 J。證據為紙面關係推導、原邊拒絕證明及 Python 固定圖
完整證書，未新增 Lean theorem。目前停止點由
[兩點重疊導覽](c5_two_vertex_overlap_guide.md)維護。

2026-09-30 後續：[全部三點投影](c5_two_vertex_ternary_projections.md)仍只
得到補回 b2–b4 的 76 軌道，保留全部 16 個原邊相容的假接受軌道。
對原 U 上無輔助變數的局部條件合取，新增條件的最小最大 arity
恰為四；兩個指定四點投影已足夠。以下保留本輪語境。

## 1. 具名共同拉回與完整差集

來源仍為 R127 `(0,2)` 接 R167 `(3,1)`，識別 a0=b3、a2=b1。
保留原圖、全部附件、七個私有內點及同一顏色集合 `{0,1,2,3}`。

```text
U  = (a0, a1, a2, a3, a4, b0, b2, b4)
C₁ = (a0, a4, a3, a2, b2)    U 索引 (0,4,3,2,6)
C₂ = (a0, b4, b0, a2, a1)    U 索引 (0,7,5,2,1)
C₁ ∩ C₂ = {a0,a2}           C₁ ∪ C₂ = U
```

定義

\[
P(u)=R_{255}(u_0,u_4,u_3,u_2,u_6)
     \land R_{1022}(u_0,u_7,u_5,u_2,u_1).
\]

這是沿具名框映射的共同拉回；只在兩點的**實際顏色相同**時接合，
不把兩框的標準 patterns 直接配對，也不獨立換色後忽略共享點。
由兩份 relation 都是 J 的投影，必有 $J\subseteq P$，但逆包含失敗。
每份 P 賦色至少在 C₁ 用三色，故其全域 S₄ 軌道大小皆為 24。

| 關係 | S₄ 軌道 | 具名賦色 |
| --- | ---: | ---: |
| P | 114 | 2,736 |
| 原 J | 60 | 1,440 |
| P∖J | 54 | 1,296 |
| J∖P | 0 | 0 |

[完整證書](../artifacts/c5_two_vertex_overlap/mixed_frame_pullback.json)
保存 P 的全部賦色、P∖J 的全部賦色與 54 份軌道記錄、原 J 與原圖。
每份差集軌道另有兩個十五點原圖正常染色：分別保持該列的 C₁、C₂
顏色；並列出各延拓改動了哪些其他 U 點。兩份全圖染色用同一具名
色框核對，每份拒絕列另有原邊矛盾。因此「分別能延拓」與「同時
能實現這份 U」的差別有直接見證，不只依集合大小判斷。

例如 `u=01012122` 的兩框分別是 `02102`、`02101`，都被接受。
保持 C₁ 時有原 J 列 `01012123`，保持 C₂ 時有原 J 列 `01012112`；
但 u 本身令 b2=b4=2，違反原邊 b2–b4。這兩個延拓不能合成 u。

## 2. 遺失的跨框條件

以下條件均在同一 U 顏色框中解讀：

\[
\begin{aligned}
G_E(u)&:\quad c_{b2}\ne c_{b4},\\
G_A(u)&:\quad |\{c_{a0},c_{a1},c_{a2},c_{a3}\}|\le3,\\
G_B(u)&:\quad c_{a2}\ne c_{b4}\ \lor\ c_{b0}=c_{b2}.
\end{aligned}
\]

**精確修復式為 $J=P\land G_E\land G_A\land G_B$。**
P 已保留十條混合框邊；原圖在 U 上有十一條邊，唯一遺失的是
b2–b4。四點條件則各含兩框無法共同看到的接點，不能由某一框
的完整 relation 單獨保留。

差集按失敗條件分成下列互斥組，完整 tuples 均在 artifact：

| 恰好失敗的條件 | 軌道 | 具名賦色 |
| --- | ---: | ---: |
| G_E | 34 | 816 |
| G_A | 6 | 144 |
| G_B | 8 | 192 |
| G_E、G_A | 4 | 96 |
| G_A、G_B | 2 | 48 |

因此 38 軌道違反原邊；補回該邊後，餘下 16 軌道分為 A-only 6、
B-only 8、A/B 同拒絕 2。這與原來源 R127、R167 的逐列拒絕完全一致。

### 三種原邊拒絕證明

G_E 失敗即由原邊 b2–b4 直接拒絕。

G_A 失敗時，共同換色可設 `(a0,a1,a2,a3)=(0,1,2,3)`。
原鄰點 `(a0,a1,a2)` 迫 `A_inner9=3`；原鄰點
`(a0,a2,A_inner9)` 迫 `A_inner5=1`；原鄰點 `(a0,a2,a3)`
迫 `A_inner7=1`。這違反原邊 `A_inner5–A_inner7`。
證明保留所有具名附件，與 a4 或 B 的其他選色無關。

G_B 失敗時，a2=b4 且 b0≠b2。由 P 已保留的 b0–a2、b2–a2，
`{b0,b2,a2}` 恰含三色。`B_inner5` 的原鄰點 `(b0,b4,b2)`
與 `B_inner6` 的原鄰點 `(b0,a2,b2)` 因而用相同三色，迫兩個
內點同取第四色，違反原邊 `B_inner5–B_inner6`。

Checker 對每一份差集軌道的每一個失敗條件保存上述強迫步驟，
逐步驗實際原邊、已知鄰色、唯一可用色及最後的同色衝突原邊。
共同 S₄ 換色給出全部 1,296 份具名拒絕。

## 3. 為何三條件已足夠

原來源框分別為

```text
A = (a0,a1,a2,a3,a4)
B = (b0,a2,b2,a0,b4)
```

完整來源 masks 在十個 proper C₅ 軌道上的精確公式是

\[
\begin{aligned}
R_{127}(q)\iff{}&\operatorname{Proper}_{C_5}(q)
 \land |\{q_0,q_1,q_2,q_3\}|\le3
 \land |\{q_0,q_4,q_3,q_2\}|\le3,\\
R_{167}(r)\iff{}&\operatorname{Proper}_{C_5}(r)
 \land r_2\ne r_4
 \land (r_1\ne r_4\ \lor\ r_0=r_2).
\end{aligned}
\]

第一式恰接受原目錄 bits 0–6；第二式恰接受 bits 0、1、2、5、7。
Checker 在全部 `4^5` 賦色逐份比對兩式與完整來源 masks；既有
八點 checker 另重播來源代表及完整 J，不依賴新的修復公式。

P 已給出 A 的所有框邊及第一混合框的四點至多三色條件；加入
G_A 就滿足第一式。P 已給出 B 的所有框邊，G_E 是 B 的原弦
b2–b4，G_B 正是第二式最後的條件。因此三條件成立就有
`R127(A)∧R167(B)`；兩來源私有內部互斥，只在 a0、a2 共享，
所以同一 U 賦色的兩來源延拓可接合，得到原 J。
反向包含由原 J 投影及兩來源公式成立，也由上述原邊矛盾直接支持。

這個充分性論證沿用完整來源關係的固定代表證據；沒有使用四色定理，
也沒有對任意來源圖或新幾何接法作推廣。

三條件在這份修復中均不可省略：

| 從完整修復省略 | 殘留軌道 | 假接受軌道 | 只違反該條件的 U 例 |
| --- | ---: | ---: | --- |
| G_E | 94 | 34 | `01012122` |
| G_A | 66 | 6 | `01232013` |
| G_B | 68 | 8 | `01201132` |

Artifact 保存三條件所有八個子集合的完整假接受 patterns；上述
「不可省略」只指這三條具體條件，不宣稱是所有可能摘要中的最小表示。

## 4. 重播、證據層與停止點

[Checker](../scripts/c5_two_vertex_mixed_pullback.py)使用標準函式庫，
SHA-256 綁定兩個混合框 artifact、原圖資料、既有 verifier 鏈及自身。
原 J 由七內點回溯重建；共同拉回由共享具名顏色的 natural join 與
全部 `4^8` 查詢兩條路徑比較。所有集合比較均含實際內容。

```bash
python3 scripts/c5_two_vertex_mixed_pullback.py
python3 scripts/c5_two_vertex_mixed_pullback.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_mixed_pullback.py --check
python3 scripts/c5_two_vertex_mixed_frame.py --check
python3 scripts/c5_two_vertex_second_mixed_frame.py --check
python3 scripts/c5_two_vertex_join.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

每次重播還核對五項 verifier 負控制：刪掉 b2–b4 後仍宣稱原邊
拒絕、填入錯誤強迫色、刪掉 B 的衝突原邊、擅改共享點顏色、將
單框延拓當成完整 U 延拓；五者均須被拒絕。
實際驗證與未重跑範圍見[本輪紀錄](history/2026-09-30-c5-two-vertex-mixed-pullback.md)。

本輪完成指定兩框的共同拉回、完整差集及精確修復，不搜尋新來源圖、
環序或其他外框。兩份五點投影不能無條件替代原八點 J；這也不否定
各自密封其他十點後的單框替換。是否可用更低 arity 的跨框資料取代
上述四點條件，留給導覽的下一窄題。一般多步同餘、幾何政策、
完整後繼表及 `K∞=K≤5` 仍保留。未新增 Lean 或 `native_decide`
證明；`lake build` 只驗既有 Lean。
