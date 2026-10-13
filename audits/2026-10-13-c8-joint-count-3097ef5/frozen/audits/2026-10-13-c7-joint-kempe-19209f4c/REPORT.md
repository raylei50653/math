# C₇ 共同計數恆等式排除 941 的最後 h=2 外圈

2026-10-13。BASE `19209f4cf68261fdce5e84a7804cfe04ae0957bf`。
接續 [完整外圈權威入口](../../docs/c5_neartri_boundary_collar.md)。
原始輸入見 [BASE.json](BASE.json) 與 `frozen/`；既有證書不修改。
本報告處理具名 C₇ 的 55 列上界，與舊 N2 original-55 無關。

## 1. 已證結論與量詞

固定內圈順序

```
(v0,v1,v2,v3,v4,v5,v6) = (a0,a1,y2,a2,a3,y4,a4)
```

固定四色 `0,1,2,3` 及原外圈 `(b0,b1,b2,b3,b4)`；內點對外圈的實際附件依序為

```
({b0,b1}, {b1,b2}, {b2}, {b2,b3}, {b3,b4}, {b4}, {b4,b0}).
```

令 U 為原證書 pattern order 下的 mask
`755425272170557940120206052`，含 91 個 proper 色軌道中的 55 列。
對**任意有限簡單、嵌於此具名 C₇ 內側的平面圖 H**，允許 chords、任意內點數，
保留完整關係 S=Σ₇(H)，本輪證明：

1. 若 S⊆U，既定外圈 transfer 不可能接受 `01232`，因此不可能等於 941。
2. 進一步沿用 4CT 與既有外側 fan cap，可排除 **S⊆U 本身**：不存在這種 H。

第一項只需一般計數引理、有限整數恆等式及原完整 transfer；第二項另用 4CT。
兩項都不是有限來源圖搜尋的外推。由原 h≤2 的另外 41 項排除，對原本「在所有
目錄外來源中最小化內點，再最大化邊數」的正規形，得到

\[
\boxed{\Sigma(G)\in\{933,941\}\quad\Longrightarrow\quad h\ge3,\quad n_5\ge9.}
\]

只關閉 h=2 這一葉；一般 h≥3、十三內點以上來源、K∞=K≤5 仍 OPEN。
舊 ε／N2／E-ARC2 的量詞與前提不同，沒有由此更新那些結論。
沒有新增 Lean theorem；實際目標來源控制為 `not triggered`，普遍排除來自下述證明。

## 2. 同一圖全部邊界列的普遍計數引理

令 x_p 是 H 在**固定字面邊界指派 p** 下的完整四色延伸數。不是色軌道的
總數；色名置換給各代表之間的雙射。對邊集 F⊆E(H)，令 k₀(F) 為
`(V(H),F)` 中不碰 C₇ 的連通分量數，π(F) 為其在七個具名邊界點誘導的 partition。
逐邊展開 properness 的乘積，得到

\[
x_p=\sum_{F\subseteq E(H)}(-1)^{|F|}4^{k_0(F)}
  E_{\pi(F)}(p),\qquad
E_\pi(p)=\mathbf1[p\text{ 在每個 }\pi\text{ block 上為常數}]. \tag{1}
\]

固定 H 後，右側係數對**全部 p 相同**。不同分量是 disk 中互不相交的連通
子圖，不能連接交錯邊界端點，故 π(F) 必 noncrossing。這是唯一平面拓撲步驟。
F 可以不含框邊；若某 block 迫 proper 邊界列相鄰點同色，該項自動為零。
不假設 H 二連通、近三角化、minimal、Kempe connected，亦不限制 |V(H)|。

七點共有 429 個 noncrossing partitions；在完整 91 列上僅 36 個 equality
vectors 非零，rank=36。拒絕列對應的 36 rows 有 rank=31。rank 用來發現
恆等式，**證明驗收只需對全部 429 partitions 逐項檢查整數等式**，不信任
浮點 LP、符號解算器或來源枚舉。

## 3. 可直接引用的共同矛盾

[count_identity_certificate.json](joint/count_identity_certificate.json) 保存完整
pattern order、429 partitions、36 active columns、全部 7 份整數恆等式及逐项零殘差。
每份恆等式的右側只使用 U 外的拒絕列。當 S⊆U，右側全部等於零，特別得到

\[
\begin{aligned}
x_{0101212}+x_{0120131}&=0,\\
x_{0121202}&=x_{0101212},\\
x_{0123231}&=x_{0101212}.
\end{aligned} \tag{2}
\]

所有 x 非負，故 (2) 中三列 `0101212,0121202,0123231` 的計數全為零。
原完整外圈表中，U 內能接到外列 `01232` 的內列**恰為這三列**，
全局 index 分別為 6、58、89。因此每份 `01232` 全圖 lift 都不可能存在。
941 卻接受 `01232`，矛盾。

這裡沒有拼接不同列的染色；(1) 對同一 H 的全部完整延伸數同步成立。
完整外圈的每一個接受、拒絕、空 fibre 及帶色名 lift 仍使用原凍結證書。

### 單一拒絕列與 Kempe 的第二條重播路徑

另一份較短的恆等式為

\[
\begin{aligned}
x_{0120231}={}&x_{0101231}-x_{0102012}+x_{0102031}+x_{0102101}\\
&-x_{0102131}-x_{0102301}-x_{0120101}+x_{0120121}\\
&+x_{0120301}+x_{0121012}-x_{0121021}-x_{0121312}+x_{0123213}.
\end{aligned} \tag{3}
\]

右側 13 列全在 U 外，因此 x₄₂=x₀₁₂₀₂₃₁=0。另一方面，在 U 內的完整
Kempe 軌道要求下，外列 `01232` 的三個前像分別沿下列接受蘊涵迫 row42 接受：

```
6 → 19 → 12 → 89 → 42
58 → 57 → 37 → 42
89 → 42
```

[caps/certificate.json](caps/certificate.json) 的 `row42_forcing` 保存七項所用
split、唯一完整交換軌道及全部列；[獨立 checker](caps/independent_verify.py)
從 noncrossing partitions 重建它們。亦可刪 row42 後重做 sound prune：
依次刪 5、5、3、1 列，最終外聯集 429，恰缺 941 的 bit9=`01232`。
兩條論證共用紙面計數引理，但完整關係矛盾的驗證路徑不同。

## 4. 55 列上界本身不可由 disk 圖實現

沿用既有 3,383 caps 中的外平面 fan：C₇ 加四條 chords
`(0,2),(0,3),(0,4),(0,5)`。其五個面依序為
`012,023,034,045,056`，可嵌在 C₇ 外側。
完整關係 mask 為 `2339273691857418867305349120`，與 U 的交集恰為
`{0123231}`，即 row89。
其 91 列完整接受／拒絕與全部字面 lifts 見 [singleton_cap.json](caps/singleton_cap.json)。

若實際 H 滿足 S⊆U，將此 fan 黏在另一側，得到合法平面圖。4CT 給一份
整圖染色，其具名 C₇ 列必在 S∩Σ(fan)；故 x₈₉>0。但 (2) 已證 x₈₉=0，矛盾。
這證明 U **不包含任何合法 disk C₇ 圖的完整關係**；不是只說 U 恰好 55 列
不能實現，也不是由 cap 與 U 不相交得出。原 cap 確實與 U 相交，新的矛盾
來自同一 H 必須滿足的共同計數限制。

## 5. 完整關係控制與限制

沿用原 3,383 caps，沒有增長 cap 搜尋範圍。僅使用原 Kempe 閉包、完整
transfer=941 及共同 cap-hitting 條件，得到 45 個必收列、10 個可選列，
全部 2¹⁰ 完成中有 72 個抽象關係通過；最小有 47 列，四個 inclusion-minimal
關係大小為 47、48、48、49，全部 72 個仍通過全部 caps。
完整 accepts/rejects 與 cap hit witnesses 見 [caps 證書](caps/certificate.json)。
這是**舊必要條件不足的反控制**；72 個都由本輪計數矛盾排除可實現性。

[counts/controls.json](counts/controls.json) 保留四張字面圖、全部 364 個固定
邊界查詢及 492 個 full lifts。三張合法 disk 圖滿足 (3)，其中一張既有 cap
確實接受 row42，說明不是無條件排除此列。另一張用交錯 equality gadgets
構成的圖違反 (3)，展示不能刪掉「同一具名 disk」前提；不把它當作平面
disk 反例。將 U 的 Boolean membership 當延伸數也違反恆等式。
破壞一個恆等式係數或刪除一個 full lift 的證書均應被拒。

本輪另保存 [topology 證書](topology/certificate.json)：原最小来源中 C₇
必 induced，且無內部長二 crosscut 連接非相鄰 C₇ 點。它們是獨立必要
收窄，**本輪最終排除不依賴這些額外拓撲計算**。

## 6. 獨立驗證、重播與信任界線

[計數證明與覆核](joint/COUNT_PROOF.md)、
[独立計數覆核程式](topology/count_review.py) 分別重建 noncrossing partitions，
核對恆等式及原字面 transfer；主發現曾用另一套 exact rational 線性代數
核對 (3)，最終計數與 cap checkers 僅依賴 Python 標準庫；額外 topology
literal controls 使用既有 NetworkX 環境，不在最終排除的依賴鏈。

```bash
python3 audits/2026-10-13-c7-joint-kempe-19209f4c/joint/count_identity.py --check
python3 audits/2026-10-13-c7-joint-kempe-19209f4c/topology/count_review.py
python3 audits/2026-10-13-c7-joint-kempe-19209f4c/caps/checker.py --check
python3 audits/2026-10-13-c7-joint-kempe-19209f4c/caps/independent_verify.py
python3 audits/2026-10-13-c7-joint-kempe-19209f4c/counts/controls.py --check
python3 audits/2026-10-13-c7-joint-kempe-19209f4c/verify.py --check
```

normal／seed17、破損證書測試與凍結輸入 hash 的實際結果記於
[verification.json](verification.json)，文件檢查另見 [documentation_checks.json](documentation_checks.json)。
正式文件連結、正式 docs DocGraph 及 `git diff --check` 通過；全工作樹 DocGraph
仍因既有 audit／scratch 快照的 62 個 duplicate IDs 失敗，未刪歷史來消除此結果。
舊 21 份外圈全部表與 3,383 caps 保留，
沒有重跑大型來源圖枚舉或外部 count-cone 證书。
沒有使用未證的通用 count-cone 猜想；(1) 是本報告給出的有限圖直接證明。
既有 Lean 未新增此拓撲／計數引理的形式化，本轮 Python 通過不代表 Lean 證成。

紙面結論／有限證書／實際圖控制分開：普遍目標為 `excluded`；合法控制上的
恆等式為 `triggered and holds`；不滿足 disk 前提的控制為 `counterexample`；
真正 941 目標圖為 `not triggered`，沒有構造該圖。
目前一般停止點見 [Kempe 導覽](../../docs/c5_kempe_guide.md)。
