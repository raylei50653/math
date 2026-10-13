# B₃：mixed-(2,2) 原長 face 的 leaf bridge 與原 K₅

**獨立驗收（2026-10-04，D₅）**：[最終成果固定快照與稽核](../audits/2026-10-04-task-d5/REPORT.md)
只接受W933-129／04–12／長face{2,3,4}的指定shared原附件{4}支：
六shared身份／八選擇、11tight pairs、連通K=C−v與完整degree握手式，
五袋非空／互斥／連通及十對原邊均獨立核對。整份W933-129、整個長face、
其他附件及原20／20表保留；B₂／B₃的兩primary閉合仍依前輪證據。
以下正文／前綴保持各輪截點，現行具名入口由Kempe導覽維護。

**後續（2026-10-04，B₄）**：[原933 04／12的shared框附件{4}](c5_excess_two_mixed_core_four_spoke_mixed22_shared4.md)
已在精確W933-129完成此窄支。它容許真正deg_C=1，11原pairs全tight，
由原cut parity／K₅獨立排除，沒有借本頁min-degree二分類。
W933-129其他附件及整份骨架保留；本頁原兩W結論／artifact不變。

**獨立驗收（2026-10-04，D₄）**：[正式返回工作區稽核](../audits/2026-10-04-task-d4/REPORT.md)
完整重建14＋2圖relations／joints／空fibres並核對五leaf型及原K₅。
原degree二shared internal bridges保留；合用B₂只登記兩primary骨架
封閉，不擴到root-swap對應或其他19／19原列。

2026-10-04。接續 [B₂](c5_excess_two_mixed_core_four_spoke_mixed22_short_face.md)，
固定 **W933-101／W941-139、原 a=5、b=6、spokes 01／23、原長 face {0,4,3}**。
取得任意大小窄引理：**完整原 C 若在此長 face，原 G 含 K₅ minor；
兩份具名長-face 分支的七種 contacts 身份全部來源排除，零殘留。**
本輪先獨立證明長 face，再與 B₂ 的短 face 結論合用；沒有從短 face
全排直接刪整個骨架。B／B₂ 原證書及其當輪必要骨架保持。
其他骨架、mixed22 整型、ε≥3、來源實現、一般出口與 K∞=K≤5 保留。
目前入口見 [Kempe 導覽](c5_kempe_guide.md)，實際驗證與貼用摘要見
[B₃ 紀錄](history/2026-10-04-excess-two-four-spoke-mixed22-long-face.md)。

證據為任意大小紙面引理、外部 degree-list 定理與 Python 固定圖證書。
未新增 Lean theorem；`lake build` 不形式化以下 topology。

## 1. 原圖與完整四接點 fibre

沿用 [B 的全部前提及原身份](c5_excess_two_mixed_core_four_spoke_mixed22.md)：
有限簡單 G，指定有序 induced-C₅ B=(b₀,…,b₄) 為 disk 外框，完整
Σ=933／941，每條非框邊 Σ-critical；有效 H 連通、ε=2、a,b 相鄰，
原完整 degrees=(5,5)，其餘有效內點完整 degree 四。
H−{a,b} 恰為一份原連通 C，沒有 unary；原 ab 與四 spokes
ab₀、ab₁、bb₂、bb₃ 保持，原 contacts 為 ax₀、ax₁、by₀、by₁，
x₀≠x₁、y₀≠y₁。B 已證四條原 spoke 省略各自全收 Ω，且每個
原拒絕 q 的 minimal q-core 就是原 G (5,5)。

七身份 D4、S00、S01、S10、S11、Pstraight、Pcross 全部保持，
共享角色仍是同一原頂點。C 的全部原邊、bridges、旁支、ownership、
實際 attachments／supports、環序及完整 witnesses 亦保持。
原長圈是 a–b₀–b₄–b₃–b–a，故 C 的原框附件只能落在 {0,4,3}。
這個 envelope 不是要求每個 C 點都接三點，也不是一份新來源圖。

同一字面 boundary β 的完整 R_C(β) 保留所有有序
(X₀,X₁,Y₀,Y₁) tuples 與整個原 C 的 witness。完整六角色 joint 是

\[
J_G(β)=\{(A,D,X_0,X_1,Y_0,Y_1):
(X_0,X_1,Y_0,Y_1)\in R_C(β),\ A\ne D,\
A\notin β(\{0,1\})\cup\{X_0,X_1\},\
D\notin β(\{2,3\})\cup\{Y_0,Y_1\}\}.
\]

所有 pinned (A,D) 四接點 fibres（含空）保持；下文從原圖提取
非平面反證，不主張 minor 保存 R_C、joint、Σ 或 boundary state。
也不要求固定某個 root pair 後 C 仍逐邊 minimal。

## 2. 全部拒絕列的 actual 附件與 shared leaf bridge

對每個原拒絕 q、每個原 G−C 合法 root pair (A,D)，C 的 exact lists 為

\[
L_{A,D}(v)=\{0,1,2,3\}\setminus
\bigl(q(N_B(v))\cup\{A:a\in N_G(v)\}\cup\{D:b\in N_G(v)\}\bigr).
\]

完整 degree 四給 |L(v)|≥deg_C(v)。因原 q 拒絕所有合法 pairs，
原連通 C 不可延拓；connected-slack 引理迫每點 tight，所有實際
外鄰的顏色在每個 pair 都互異。對同一原頂點跨全部拒絕列求交，
兩 masks 的原長 face 得到同一必要表：

| 原 owner | 容許的實際 N_B(v) | 必要 min deg_C | private odd-cycle 點的實際全部外鄰 |
| --- | --- | ---: | --- |
| 無 | ∅、{0}、{3}、{4}、{0,4}、{3,4} | 2 | {b₀,b₄} 或 {b₃,b₄} |
| 僅 a | ∅、{0} | 2 | {a,b₀} |
| 僅 b | ∅、{3} | 2 | {b,b₃} |
| 共享 a,b | ∅ | 2 | {a,b} |

因此 **shared contact 不能是 terminal bridge 的 private 點**：那會有
原 C-degree 一，完整 degree 四迫它另接某個 bⱼ，j∈{0,3,4}。
以下保留每個候選實際邊的同框 slack 反證：

| 假設原 shared 點的額外框鄰 | 原共同拒絕 q | 合法 (A,D) | 實際外鄰重色 |
| --- | --- | --- | --- |
| b₀ | 01212（row 6） | (2,0) | D=q₀=0 |
| b₃ | 01021（row 1） | (2,1) | A=q₃=2 |
| b₄ | 01021（row 1） | (2,1) | D=q₄=1 |

三者均有 |L|=2>deg_C=1，原連通 C 可貪婪延拓，與拒絕矛盾。
單列 01021 尚容許 shared 點接 b₀；row 6 必須保留。
這只排除 shared **leaf** bridge；原 C 內 degree 二的 shared 點仍可
位於兩條內部 bridges 之間，本輪沒有刪去這些原路徑。
933 的另一原 04／12 骨架容許 shared 附件 {4}，與本骨架身份不同，
不能搬入此表或直接套本引理。

外部依賴是 [Dvořák 的 Lemma 7、Corollary 8、Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
它們給 connected-slack、相鄰非 cutvertex 的 list 相同，以及
degree assignment 拒絕時的 Gallai block 結構。本輪 live 核對這些
前提；不用四色定理 oracle，也不用 pinned-pair 逐邊 minimality。

## 3. 同一 leaf 的五種精確型

共同拒絕 q=01021 的合法 root pairs 是 (2,1)、(2,3)、(3,1)。
取同一原 C 的兩份 lists，按順序 (3,1)、(2,3) 比較。
Terminal odd cycle 的 private 點原內度二、非 cutvertices，沿 private
路徑相鄰，故對每個 pair 其 exact lists 全相同。§2 給全部可能如下：

| 原 private 型 | L_(3,1) | L_(2,3) | 共同實際 hubs h,k |
| --- | --- | --- | --- |
| nonowner 04 | {2,3} | {2,3} | b₀,b₄ |
| nonowner 34 | {0,3} | {0,3} | b₃,b₄ |
| a-only | {1,2} | {1,3} | a,b₀ |
| b-only | {0,3} | {0,1} | b,b₃ |
| shared | {0,2} | {0,1} | a,b |

五個有序 list signatures 互異，所以同一 leaf 的全部 private 點
有同一 owner **及同一實際附件 pair**。特別是 nonowner 的兩種
附件不能在一個 leaf 內混用；只看缺色 membership 尚不足以區分它們。
這是同一字面框上的比較，沒有獨立換色或只保留 marginals。

## 4. 原 K₄ blocks、terminal cycles 與原外部路徑

令 X=B∪{a,b}，其原 FRAME、四 spokes 與 ab 保持連通。
拒絕的 exact degree lists 迫 C 為 Gallai tree。若 C 有 K₄ block Q，
每個 Q 點三條 clique 邊以外只有一條原 incidence；若不直達 X，
該邊必為 bridge，其他非 bridge block 至少需要兩條邊，超出 degree。
每條 outward bridge 的有限 Gallai 側取遠離 Q 的 terminal private 點，
其 deg_C≤3（planarity 排 K₅ clique），完整 degree 四迫一條實際 X 邊。
四側互斥、不能重回 Q 或互接，否則 Q／bridge 的原 block 身份不成立。
四條原 tethers 與連通 X 合成第五袋，Q 四點各自一袋，給原 K₅。
故 C 無 K₄ block；這沿用 B₂ 的實際 tether 論證，與本 face 的表相容。

§2 的 min deg_C≥2 排掉 terminal bridges，所以 terminal blocks 都是
odd cycles。C 不可能只有一個 block：若是 odd cycle，全體 vertices
均 private，§3 迫同一 owner；nonowner 違反原 contacts 存在，而
每個非空 owner 類最多兩個原頂點，小於 odd cycle 的三點。
因此至少兩個 terminal odd cycles。

帶 owner 的 leaf 必是 triangle，其兩個 private 點耗用至少兩個
同 owner 原頂點。D4 可有 a-only／b-only leaf；四種 Sij 只有
nonowner leaf；Pstraight／Pcross 可有 shared leaf。
nonowner leaves 可有任意奇長度，不據此限制原 C 大小。

取任一 terminal odd cycle 的相鄰 private u,w，令 C′=C−{u,w}。
剩餘 cycle 是包含其原 cutvertex 的非空路徑，其餘 blocks 原樣接入，
故 C′ 連通。u,w 各有一條原 cycle 邊到 C′。
由 §3，它們共享實際 hubs h,k，且 hk、hu、hw、ku、kw、uw 都是原邊。

以下逐型保存 E′=X−{h,k} 的實際連通路徑與 C′ 接入理由：

| 原 leaf 型 | h,k | 原 E′ 路徑 | C′ 到 E′ 的原連接 |
| --- | --- | --- | --- |
| nonowner 04 | b₀,b₄ | a–b₁–b₂–b–b₃ | 四個原 root contacts 均在 C′ |
| nonowner 34 | b₃,b₄ | b–b₂–b₁–a–b₀ | 四個原 root contacts 均在 C′ |
| a-only | a,b₀ | b₁–b₂–b–b₃–b₄ | 兩個原 b-contacts 均在 C′ |
| b-only | b,b₃ | b₂–b₁–a–b₀–b₄ | 兩個原 a-contacts 均在 C′ |
| shared | a,b | 原 C₅ | 另一 terminal leaf 的實際 04／34 框附件 |

shared 型只可能是 Pstraight／Pcross；u,w 用盡全部原四個 contact
角色。另一 terminal odd cycle 的 private 點因而都無 owner，原 degree
四迫實際附件是 04 或 34，至少一條原框邊接 C′ 到 B。
這條路徑經同一原 C 的 cutvertex、bridges 與另一 leaf，無須添加邊。

令 O=C′∪E′，各型 O 均連通。其到 h,k 的原邊可分別選
ab₀／b₃b₄、bb₃／b₀b₄、ab／b₀b₁、ab／b₂b₃、ab₀／bb₃；
另有兩條原剩餘 cycle 邊接到 u,w。因此

\[
\boxed{\{h\},\{k\},\{u\},\{w\},\ O}
\]

是五個互斥連通 branch sets，十對鄰接全由原邊見證，提取原 K₅ minor。
與 disk 平面性矛盾，故固定 W933-101／W941-139 長 face **七身份零殘留**。
minor 的 O 可含原框點，只用於非平面反證，不作 Σ-preserving 操作。

## 5. 證書、重播與停止點

[Checker](../scripts/c5_excess_two_mixed_core_four_spoke_mixed22_long_face.py)、
[literal controls](../scripts/c5_excess_two_four_spoke_mixed22_long_face_controls.py)、
[observations](../artifacts/c5_excess_two_mixed_core_four_spoke_mixed22_long_face/observations.json)
構成獨立 B₃ 層。SHA256 綁定原 B／B₂ 證書；保存原 frames／rotations、
完整拒絕 rows／root pairs、actual 附件交集、七身份、三份 shared leaf-bridge
slack、五 leaf 型及其原外部路徑。B／B₂ observations 不覆寫。

完整 degree 固定圖逐份保存同一原 C 的 R_C、six-role joints、全部
四座標 fibres（含空）及整份 witnesses；直接從原邊重算 join，核對
spoke 省略／接回、root swap 與共同 global S₄。條件式 minors 逐袋
檢查原連通性、十條原鄰接及 actual paths；長 nonowner leaf 用兩段
connected private bags，與 §4 相鄰兩點提取同樣有效。
固定圖不宣稱 disk、目標 Σ、criticality 或來源實現；任意大小結論
由 §2–4 的紙面引理承擔。完整數字與實際驗證見 B₃ 紀錄。

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_long_face.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_long_face.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

無參數只生成本層 observations；`--check` 重算逐 byte 比對。
**停止於固定兩份原長 face 的任意大小原 K₅ 窄引理，零具名長-face 殘留。**
B₂ 已獨立排相同 W 的短 face，兩份原 mixed-capable faces 至此各自
有證明；原 B 的 20／20 必要骨架是保存的歷史層，不由短 face 單獨
改寫。其他原骨架與 933 原 04／12 的 shared 框附件分支保留。
本輪未繼續其他 face／incidence，未證 ε≥3 或 mixed22 整型，未 commit／push。
