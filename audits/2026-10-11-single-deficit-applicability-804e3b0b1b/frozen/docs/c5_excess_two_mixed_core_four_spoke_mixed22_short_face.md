# B₂：mixed-(2,2) 原短 face 的 Gallai leaf 與原 K₅

**獨立驗收（2026-10-04，D₅）**：[最終成果固定快照與稽核](../audits/2026-10-04-task-d5/REPORT.md)
只接受W933-129／04–12／長face{2,3,4}的指定shared原附件{4}支：
六shared身份／八選擇、11tight pairs、連通K=C−v與完整degree握手式，
五袋非空／互斥／連通及十對原邊均獨立核對。整份W933-129、整個長face、
其他附件及原20／20表保留；B₂／B₃的兩primary閉合仍依前輪證據。
以下正文／前綴保持各輪截點，現行具名入口由Kempe導覽維護。

**獨立驗收（2026-10-04，D₄）**：[正式返回工作區稽核](../audits/2026-10-04-task-d4/REPORT.md)
已獨立核對B₃跨拒絕列slack、五leaf型與原K₅。
合用本頁短face只登記W933-101／W941-139兩primary骨架封閉；
原B表及其他19／19原列保持，原93304／12共享附件{4}未驗收。

2026-10-04。接續 [B 報告 §7](c5_excess_two_mixed_core_four_spoke_mixed22.md#7-重播停止點與下一窄入口)，
固定 **W933-101／W941-139、原 a=5、b=6、spokes 01／23、短 face {1,2}**。
本輪取得任意大小窄引理：**完整原 C 若在此短 face，原 G 含 K₅ minor；
因此兩個具名短-face 分支全部來源排除，七種 contacts 身份均無殘留。**
其他原 faces、mixed-(2,2) 整型、ε≥3、一般出口及 K∞=K≤5 仍保留。
目前接續由 [Kempe 導覽](c5_kempe_guide.md)維護；實際驗證及貼用摘要見
[B₂ 紀錄](history/2026-10-04-excess-two-four-spoke-mixed22-short-face.md)。

**後續（2026-10-04，B₃）**：[同一原骨架長 face 的 leaf bridge／原 K₅](c5_excess_two_mixed_core_four_spoke_mixed22_long_face.md)
已獨立排除 W933-101／W941-139 的 {0,4,3}，七身份零長-face 殘留。
下文「長 face 保留」是 B₂ 當輪停止點；本層 checker／artifact 未改寫，
不能以本頁短 face 結論單獨刪整個骨架。其他骨架及整型仍保留。

證據是任意大小紙面證明、外部 degree-list 定理及 Python 固定圖證書；
未新增 Lean theorem，`lake build` 不形式化以下 topology。

## 1. 固定原圖、原身份及完整 fibre

沿用 B 的全部前提：有限簡單 G、有序 induced-C₅ B=(b₀,…,b₄) 為
disk 外框、完整 Σ=933／941、每條非框邊 Σ-critical；有效 H 連通、
ε=2、a,b 相鄰且完整 degree 五，其餘有效內點完整 degree 四。
H−{a,b} 恰為唯一原連通 C，沒有 unary，原 mixed incidence=(2,2)。
原 spokes 為 ab₀、ab₁、bb₂、bb₃，原 ab 存在；原 contacts 是
ax₀、ax₁、by₀、by₁，x₀≠x₁、y₀≠y₁。

七份身份全部保持：D4、S00、S01、S10、S11、Pstraight、Pcross。
共享角色始終是同一原頂點，不複製 contacts；C 的所有原邊、bridges、
旁支、ownership、實際附件、環序及整份染色 witnesses 保持。
B 已證四原 spoke 省略各自 Ω，每個拒絕 q 的 minimal q-core 正是
原 G (5,5)。這裡不把它替換為唯一 degree-5 圖，也不從 q-minimality
推論「固定每個 root pair 後 C 仍逐邊 minimal」。

短 face 的原圈是 a–b₁–b₂–b–a，故所有原 C–B 邊只能到 b₁、b₂。
原長 face a–b₀–b₄–b₃–b–a 的 envelope {0,4,3} 本輪保留。

對同一字面 boundary 染色 β，原完整四接點 relation R_C(β) 與六角色
joint 為

\[
J_G(β)=\{(A,D,X_0,X_1,Y_0,Y_1):
(X_0,X_1,Y_0,Y_1)\in R_C(β),\ A\ne D,\
A\notin β(\{0,1\})\cup\{X_0,X_1\},\
D\notin β(\{2,3\})\cup\{Y_0,Y_1\}\}.
\]

對每個合法 (A,D)，其完整 pinned fibre 保留全部四座標 tuples 與
同一原 C witness，空 fibre 亦保存。以下只在原圖提取反證 minor，
不宣稱收縮保存 R_C、完整 joint、Σ 或接點 state。

## 2. 全部拒絕列的 tightness 與原 leaf-owner 邊

對每個原拒絕 q 及每個原 G−C 合法 root pair，C 的 exact lists 為

\[
L_{A,D}(v)=\{0,1,2,3\}\setminus
\bigl(q(N_B(v))\cup\{A:a\in N_G(v)\}\cup\{D:b\in N_G(v)\}\bigr).
\]

原 degree 四給 |L(v)|≥deg_C(v)，原 C 連通且不能延拓此 pair；
connected-slack 貪婪引理迫每點 tight。沿用 B 跨**全部拒絕列及全部
合法 pairs**的同一實際附件交集，短 face 內精確必要表如下。

| 原 owner | 容許實際 N_B(v) | 必要 min deg_C | leaf private 點的實際全部外鄰 |
| --- | --- | ---: | --- |
| 無 root owner | ∅、{1}、{2}、{1,2} | 2 | {b₁,b₂} |
| 僅 a | ∅、{1} | 2 | {a,b₁} |
| 僅 b | ∅、{2} | 2 | {b,b₂} |
| 共享 a,b | ∅ | 2 | {a,b} |

最後一欄使用 leaf odd-cycle private 點原內度二與完整 degree 四。
四個外鄰 pair 都是原圈 a–b₁–b₂–b–a 的**實際邊**。
此欄不能只從 q=01021 推出：該列單獨仍可能容許 a-only 接 b₂；
原 row 6 的 q=01212 同時拒絕，才排除該實際接線。

兩 masks 共同拒絕 q=01021；E_a={2,3}、E_b={1,3}，原完整合法
root pairs 恰為 (2,1)、(2,3)、(3,1)。缺色 d=3。比較 (d,1) 與
(2,d) 時，exact lists 的 d-membership 分別為
無 owner (1,1)、a-only (0,1)、b-only (1,0)、shared (0,0)。
對每個 pair，Gallai blockwise-uniform lists 迫同一 leaf 的 private
vertices 有相同 lists，故其原 owner 全同。這同時比較同一原圖上的
兩份 lists，沒有獨立重命名兩份色框。

外部依賴是 [Dvořák 的 Lemma 7、Corollary 8、Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)：
connected degree assignment 的 slack、private 點 list 相同，以及拒絕
當且僅當 Gallai tree／blockwise-uniform。前提已逐項核對；不要求
此 pinned pair 的逐邊 minimality，也不使用四色定理 oracle。

## 3. 補強的原 K₄-block 排除及 leaf 存在

此處直接證明實際 tethers，避免沿用 fixed-pair 刪邊 minimality。
令 X=B∪{a,b}，它由原 C₅、四 spokes 及 ab 原樣連通。
若原 C 有 K₄ block Q，每個 Q 點已用三條 clique 邊，完整 degree 四
只餘一條原 incidence。若不是直接接 X，該邊必為 bridge：另一
非 bridge block 至少耗兩條 incidence，已超出 degree。

每條 bridge 的外側 F 與其他三側互斥，也不會返回另一 Q 點，否則
Q 不是 block。若 F 僅一點 w，其原 C-degree 為一；否則在 F 的有限
block-cut tree 中取遠離 Q 的末端 block，其 private 點 w 的原 C-degree
至多三。這裡 clique 至多 K₄，由
假設 G 平面；其餘為 odd cycles／bridges。完整 degree 四迫 w 有
一條**實際 X 邊**。因而從 Q 的每個點得到一條原路徑到 X，四條
路徑的內點互斥。把 X 與四條路徑除 Q 端點之外的部分合成第五袋，
Q 的四點各一袋，即為原 K₅，矛盾。故 C 沒有 K₄ block。

Gallai leaves 不可能是 bridges，因 private 點內度一違反 §2；
因此每個 leaf 是 odd cycle。若 private 點帶 owner，其 owner 類最多
兩個原頂點，故該 leaf 必為 triangle。若 C 只有一個 odd-cycle block，
所有點均 private，§2 迫所有點有同一 owner；無 owner 違反原四個
contacts 存在，非空 owner 又最多兩點，小於 odd cycle 的三點。
故 C 至少兩個 blocks，至少兩個 terminal odd cycles。

身份限制亦保留具名 provenance：D4 可有 nonowner、a-only 或 b-only
leaf；S00／S01／S10／S11 的每個非空 owner 類只有一點，故只能有
nonowner leaf；Pstraight／Pcross 可有 nonowner 或 shared leaf。
這些是必要 leaf 身份，沒有獨立生成一份新的來源 catalogue。

## 4. 四種 leaf 的五個原 branch sets

取任一 terminal odd cycle 的兩個相鄰 private vertices u,w。
刪去它們後，原 C′=C−{u,w} 仍連通：剩餘 cycle 是含原 cutvertex
的一條非空路徑，其餘 blocks 原樣接於該 cutvertex。
u、w 各有一條原 cycle 邊進入 C′。由 §2，u,w 有相同兩個實際外部
hubs h,k，且原 hk、hu、hw、ku、kw、uw 都存在，形成原 K₄。

令 E′=X−{h,k}；以下表保存原 E′ 的連通路徑及第五袋 O=C′∪E′。

| leaf owner | 四 singleton bags | 原 E′ 中的連通路徑 | C′ 與 E′ 的實際連接 |
| --- | --- | --- | --- |
| 無 | {b₁},{b₂},{u},{w} | a–b₀–b₄–b₃–b | 四個原 contacts 全在 C′，接 a 或 b |
| 僅 a | {a},{b₁},{u},{w} | b–b₂–b₃–b₄–b₀ | 兩個原 b-contacts 全在 C′ |
| 僅 b | {b},{b₂},{u},{w} | a–b₁–b₀–b₄–b₃ | 兩個原 a-contacts 全在 C′ |
| 共享 | {a},{b},{u},{w} | 原 C₅：b₀–b₁–b₂–b₃–b₄ | 另一原 leaf 的實際 boundary 邊 |

前三列的 contacts 都用原 incidence 接入上述路徑；不需要添加邊。
共享型的 u,w 用盡兩側四個 contact 角色，所以身份必為 Pstraight
或 Pcross。由 §3 存在另一 terminal odd cycle；其 private vertices
都無 owner，原內度二，完整 degree 四迫實際附件恰為 {1,2}。
此另一 leaf 不含 u,w，故它的一條實際 boundary 邊將 C′ 接到原 B。
這證明共享型 O 連通，不要求把 C′ 另行換色，也不更改任何原 fibre。

四型的 O 都鄰接 h,k：nonowner 用原 ab₁、bb₂；a-only 用 ab、b₀b₁
（或 b₁b₂）；b-only 用 ab、b₁b₂；shared 用原 spokes。
O 亦經剩餘 cycle 的原端邊鄰接 u,w。故

\[
\boxed{\{h\},\{k\},\{u\},\{w\},\ C′\cup E′}
\]

是五個互斥、連通、兩兩有**原邊**的 branch sets，提取原 K₅ minor。
全部七種 contacts 身份均被上述四種 leaf owner 覆蓋，與 disk 平面性矛盾。
所以 W933-101／W941-139 的原短 face **零殘留**。
minor 最後一袋可包含原框點，只用於非平面反證；不作 Σ-preserving
boundary 操作，不宣稱獨立 root marginals 等於原完整 joint。

## 5. 固定證書、重播與停止點

[Checker](../scripts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face.py)、
[完整 relation／原路徑 helper](../scripts/c5_excess_two_four_spoke_mixed22_short_face_controls.py)、
[observations](../artifacts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face/observations.json)
另存本層。它以 SHA256 綁定 B 的原 artifact，保存兩份原 frame／rotations、
全拒絕列與完整 root pairs、原 actual 附件交集、七身份、四種 leaf-owner
路徑 ledger；原長 face 與其完整 provenance 保留，未覆寫 B 的 observations。

固定完整 degree 圖逐份保留同一原 C 的四角色 R_C、六角色 joints、
所有 pinned root-pair fibres（含空）與整份 witnesses；獨立從原邊求解
核對 join、原 spoke 省略／接回、root swap 與共同全域 S₄。
另有四種 leaf-owner 的原 K₅ branch sets／十條原鄰接證書，以及兩份
K₄ 直達／長 tethers 的條件式原 K₅ 控制。固定圖及 tethers 是提取／
介面控制，不宣稱 disk、目標 Σ、criticality 或來源實現；任意大小
結論由 §2–4 的紙面證明承擔，具體控制數字見本輪紀錄。
較長 nonowner leaf 控制把兩段相鄰 private 路徑各留為 connected bag，
同樣逐條核對原邊；不把路徑內部改成 relation 中的虛構頂點。

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

無參數只生成 B₂ 自己的 observations；`--check` 重算逐 byte 比對。
本輪實際執行與未重跑範圍見 [B₂ 紀錄](history/2026-10-04-excess-two-four-spoke-mixed22-short-face.md)。

**停止於固定兩份短 face 的任意大小原 K₅ 排除，零具名短-face 殘留。**
同一 W933-101／W941-139 的原長 face {0,4,3} 未排；若接續，可固定
該原長 face 的 full C、七身份及完整四接點 fibre，研究共享 contact
有實際框附件時的 leaf bridge。B 的其他 20／20 必要骨架不由此改為
來源 catalogue，沒有套用本輪短 face 引理刪除長 face。
本輪未 commit／push，未重開其他 incidence／較少 spokes／多 mixed／
no-mixed／非相鄰 roots 或任務 A。
