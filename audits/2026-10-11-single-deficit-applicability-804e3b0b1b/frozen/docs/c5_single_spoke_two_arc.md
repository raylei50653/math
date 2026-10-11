---
docgraph:
  id: c5.single-spoke-two-arc
  family:
    - c5
    - c5.single-spoke
  requires:
    - c5.single-spoke-cross-row
    - c5.single-spoke-frame-arc
    - c5.single-spoke-two-two
---
# Single-spoke (2,2)：兩框弧 K5、record 17 雙列延拓與分開套表

後續（2026-09-28）：[局部 residual 相同列引理](c5_single_spoke_residual_locality.md)
已完成 record 90／282 的 p₂；來源排除仍 278，保留 102 筆／51 型全部雙列
已證、0 查詢未決，指定 (2,2) 分離已接回條件式出口。下文及原 artifact
保留當輪數字與停止點；新結果未證可實現性或完整 Σ。

後續（2026-09-28）：[singleton-source 首橋相容性](c5_single_spoke_first_bridge.md)
已證 record 87 的 p₂，套表共新增 16 個指定列延拓；來源排除仍 278 筆，保留
102 筆／51 型、100 筆雙列已證，僅 record 90／282 的 p₂ 未決。下文與舊
artifact 保留當輪語境；新層保留首橋共用 β，未放寬舊 pair 引理的 singleton 限制。

2026-09-28，基準 `123a4bc`。本輪獨立審核使用者貼出的兩框弧推導，確認
把整個另一原分量納入 Z 的構造成立，並重建 checker 後套全表。使用者連結的
`/mnt/data/math_record17_two_arc_review/` 與 ZIP 在本環境不存在；本輪沒有重播
附件所述 1,040／4,480／13 個控制，下列數字全部來自 repo 內新建控制。
研究優先序見 [HANDOFF](HANDOFF.md)。

**record 17 的 p₁=01021、p₂=01212 均必延拓。** 不限制原 bridge 路徑長度，
也不要求兩個路徑塊接到相同的兩個具名框點。所需的是同一份連通兩框弧分割，
每塊都實際碰兩側，而原 spoke 加另一分量的實際支援也碰兩側。

完成引理審核及全表重算後，新增 **6 筆來源排除、20 個指定列延拓**。
來源累計排除 **278 筆**，保留 **102 筆／51 型**；其中 **84 筆雙列已證**，
**18 筆各剩一列未決**。原 50 個未決查詢中，12 個隨來源排除移出，20 個
另有延拓證明，留下 18 個；沒有把移出的 12 個算成延拓。

任意大小結論是紙面證明＋外部 degree-list 定理。Python 核對支援代數、
具名 branch sets、反射及完整拒絕候選；**未新增 Lean theorem**，未證保留型
可實現性、完整 Σ、所有來源共用同一 z 色或一般 (2,2) 出口分離。

## 1. 來源前提、任意拒絕列與支援族

沿用 [(2,2) 必要分類](c5_single_spoke_two_two.md) §1–3 的完整前提：
G 有限簡單，B=(b0,…,b4) 是 induced-C5 disk 外框，有效 H 連通；G 是
edge-minimal q=01012 obstruction。唯一完整 degree-5 點 z 只有 spoke zb_s，
其餘內點完整 degree=4。H−z 恰有 C0、C1，各有兩個不同原有序接點
(u_k,v_k)，S_k 是全部實際 boundary 支援。套既有保留表時另沿用 T4 篩選。
U={0,1,2,3}，p₁=01021，p₂=01212。

對任意 proper row t，保留同一 C_k coloring 的完整有序關係 R_k(t)。
忽略 z 時的 lists 至少為內部 degree，在接點嚴格多一色，所以 R_k(t) 非空，
|F_k(t)|≤2，且精確接合式是

\[
F_k(t)=\bigcap_{a\in R_k(t)}\operatorname{set}(a),\qquad
Z_G(t)=(U\setminus\{t_s\})\setminus(F_0(t)\cup F_1(t)).
\]

若 c∈F_k(t)，從原兩接點 lists 去掉 c，得到連通 C_k 上被拒絕的 degree lists。
[Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
分別給 tightness 與 blockwise-uniform palettes；本輪重新讀取原 PDF 核對。
兩條結論只要求連通、degree assignment 及拒絕，**不另要求 target minimality**。
K4-free、任意列雙禁色 bridge 化約與每塊 residual 的存在性沿用
[frame-arc §1–2](c5_single_spoke_frame_arc.md) 及
[cross-row §1–2](c5_single_spoke_cross_row.md)。

若 F_k(t) 為 pair，原接點間有奇數長 bridge 路徑 P=(x0=u,…,xℓ=v)，ℓ≥1。
刪去全部 P 邊所得 W_j 連通、兩兩不交，只含一個 x_j 及其全部旁支。
T_j 是 W_j 的實際 boundary 支援，包含 root 自己的附件。逐塊 residual
引理給一族必包含每個 T_j 的容許支援：

- 只用 t：取全部 T⊆S_k，使逐點固定 t(T) 的每個 π∈S₄ 都保持 F_k(t)。
- q、t 均為 pair：可取已證 `joint_supports`，再合用 q 的穩定子及
  `t|T=π∘q|T ⇒ F_k(t)=π(F_k(q))`。兩列保留同一 P、W_j 及 component identity。
- q 為 singleton、t 為 pair：只用 t 自己的支援族；t 為 singleton 時跳過
  這個路徑塊引理。沒有對齊置換時，不以跨列條件刪掉 T。

下節的拓撲引理只要求實際 T_j 碰兩弧，本身不需要跨列 palettes。

## 2. 兩框弧與另一原分量納入 Z

固定 k，令 C=C_k、D=C_(1−k)，P 是 C 的原 bridge 路徑，
J=P∪{zu,zv}。假設存在同一份分割 B=X⊔Y，其中 X、Y 非空且各沿原框邊連通，
並且

\[
O=\{b_s\}\cup S_D,\qquad O\cap X\ne\varnothing,\quad O\cap Y\ne\varnothing,
\]
\[
\forall j,\quad T_j\cap X\ne\varnothing,\quad T_j\cap Y\ne\varnothing.
\]

任取一條原 bridge xy=x_ix_(i+1)，取五個 branch sets

\[
A=W_i,\quad A'=W_{i+1},\quad
Z=(V(J)\setminus\{x_i,x_{i+1}\})\cup V(D),\quad X,\quad Y.
\]

A、A' 連通；原 bridges 保證它們與其餘路徑點不交。J 是經 z 的 simple cycle；
刪掉相鄰兩點後，剩餘部分仍經 z 連通，ℓ=1 時就是 {z}。D 是另一原連通分量，
由原接點邊與 z 相接，所以 **整個 D 放入 Z 後仍連通**。X、Y 的連通性來自
原框路徑。C、D、{z}、B 的身份與 W 分割保證五組兩兩不交。

| pair | 原邊來源 |
| --- | --- |
| A–A' | 原 bridge xy |
| A–Z、A'–Z | J 上兩塊朝外的 cycle 邊；端點時使用原 z 接點邊 |
| A–X、A–Y、A'–X、A'–Y | 各 W 的實際 boundary 附件，四個落點可不同 |
| Z–X、Z–Y | O 的實際附件：原 spoke 或 D 到該弧的原邊 |
| X–Y | 原 C5 分割的切口邊 |

十對皆相鄰，給同一來源 G 的 K5 minor。此處沒有把 C、D 的著色關係合併，
只是把 D 的原頂點放在同一拓撲 branch set。Z–X、Z–Y 所用的 D 內路徑可以
共用內點、原接點或整段路徑，因為它們全部在同一個 Z 中。Z 本身不含框點。
不需第三個外部落點，不需先界定 bridge 長度，也不需要旁支大小上界。

若選不相鄰的 W_i、W_j，可令 A 吸收 x_(i+1),…,x_(j−1)，Z 改用 J 上經 z
的另一弧及 D；相同十對仍成立。套表只需相鄰特例；有限控制也核對這個變體。

對容許族 𝒯 的安全套用條件是

\[
\exists\,X/Y\quad O\text{ 碰兩側}\quad\land\quad
\forall T\in\mathcal T,\ T\text{ 碰同一份 }X/Y\text{ 的兩側}.
\]

先選固定分割、再驗全部 T。不能對每個 T 重選分割，也不能將 T 的選言資訊
先壓成共同必接點。空支援族另證不可能有 W，不用 vacuous 全稱構造 minor。

## 3. record 17 的兩列

s=0，S0={0,1}、S1={0,1,2,3,4}，F0(q)={1}、F1(q)={2,3}。
兩個 p 在 S0 都與 q 逐點相同，故同一 C0 的完整 R0 不變，F0(p)={1}。
兩列在 b0 都用 0；反設任一 p 拒絕，接合式迫使 {2,3}⊆F1(p)，
由非空 R1 與二接點容量，得 **F1(p)={2,3}**。

對 p₁，q 的逐塊穩定子迫使每塊看見 q 色 0、1，因而碰 b0/b2 至少一者。
若 T 不含 b1，則 T⊆{0,2,3,4}；這些點上 p₁=(1 2)∘q，跨列 residual
引理迫使 F1(p₁)=(1 2){2,3}={1,3}，矛盾。因此

\[
b1\in T,\qquad T\cap\{b0,b2\}\ne\varnothing.
\]

取 X={b0,b2,b3,b4}、Y={b1}；X 沿 b0–b4–b3–b2 連通。

對 p₂，只用該列穩定子：每塊必看見色 0、1，故

\[
b0\in T,\qquad T\cap\{b1,b3\}\ne\varnothing.
\]

取 X={b0}、Y={b1,b2,b3,b4}；Y 沿 b1–b2–b3–b4 連通。
兩列的 O 都是 {b0,b1}，原 spoke 與 C0 到 b1 的實際附件提供 Z 的兩側鄰接。
§2 於是給 K5 矛盾，**兩個 p 均延拓**。每列 32 個 T、全部 24 色置換的
獨立核對各留下 12 個 T，恰為上述條件；共同必接集合分別僅有 {b1}、{b0}。
這正是原來只搜尋兩個共同具名框點的 checker 無法捕捉的情形。

## 4. 全表重算：來源排除與延拓分開

[Checker](../scripts/c5_single_spoke_two_arc.py) 只讀原必要表與 cross-row artifact，
核對前層輸入 SHA256；原記錄、完整 relation schema IDs、ordered contacts、
slit lifts、contact words、反射及全部既有 target 證據逐筆保留。

先在 q 下只用單列支援族掃 108 筆來源。新排除的六筆為
**174、231、965、1233、1332、1417**，即三個交換分量型；六筆原先皆為 ?/?。
它們都有雙禁色分量 S_C=01234，並可用 X=B\{b4}、Y={b4}：

| 來源 IDs | s | F_C(q) | S_D | 每個 W 除 b4 外的強迫選言 |
| --- | ---: | --- | --- | --- |
| 174、231 | 0 | {1,3} | 04 | b0/b2 |
| 965、1417 | 4 | {1,3} | 04 | b0/b2 |
| 1233、1332 | 4 | {0,3} | 34 | b1/b3 |

逐塊 q 穩定子給表中的兩側附件，O 分別為 04、04、34，均碰兩側，故直接
排除來源。這六筆的 12 個未決查詢跟著來源移出，**不記為 target 延拓**。

對其餘 102 筆，逐一處理 38 個未知 target。從兩份完整 F 候選族重算覆蓋
z 可用色的所有整組拒絕候選，逐項核對原 `rejection_options`，並重算前層
`candidate_evidence` 確认繼承 witness。每個新 witness 保存採用的支援族、
同一份框弧、原分量與原接點、O 的兩個實際附件來源及符號 branch sets。
只有全部完整拒絕候選被消去，才接受 target。

| 階段 | 來源 | A/A | A/? | ?/A | ?/? | 未決查詢 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| cross-row 輸入 | 108 | 74 | 8 | 10 | 16 | 50 |
| 六筆來源排除後 | 102 | 74 | 8 | 10 | 10 | 38 |
| 二十個延拓後 | 102 | 84 | 8 | 10 | 0 | 18 |

新增延拓的十筆來源為 **17、73、82、316、317、338、433、451、828、829**，
各新增 p₁、p₂，共 20 個。38 查詢有 166 組拒絕候選：前層已排除 124 組，
本輪再排除 24 組，剩 18 組各屬一個未決查詢。前輪六個「六消五」查詢
493/p₁、827/p₁、1111/p₂、1115/p₁、1515/p₁、1527/p₂ 仍未決。

所有數字包含交換 C0、C1 的具名記錄。checker 核對交換後逐候選狀態相同，
也核對 ρ=(3,2,1,0,4)、π=(0 1) 的**字面 target**、禁色、全部支援及同一份
框弧與附件來源的搬運；反射側不另計數。完整資料見
[JSON](../artifacts/c5_single_spoke_two_arc/observations.json) 與
[套用表](../artifacts/c5_single_spoke_two_arc/support_table.md)。

## 5. 控制、重播與下一個窄入口

- record 17 兩列各 32 個 T，逐一以全部 24 置換獨立核對，各留下 12 個。
- 10 種不分左右的連通兩框弧分割，另以刪兩條框邊獨立枚舉核對完整性。
  31 種非空 O × 496 種一個或兩個非空支援的族，共 **15,376 個量詞控制**，
  用直接逐族檢查與分割 mask 交集獨立比較；JSON 保存結果摘要 SHA256。
- **3,150 個一般 minor 控制**：全部分割、兩塊各自的供應點、spoke 與另一
  分量的落點；另含長度 1–5 全部 35 個兩塊位置及共用 tether／外部路徑。
- **2,560 個 record 17 控制**：兩列各兩種供應點任意組合、長度 1/3/5
  全部相鄰位置及一個非相鄰位置、16 種兩塊 tether 形狀、兩種另一分量接線。
- **18 個負控制**：缺 spoke、另一分量與 z 斷開、缺外部附件／tether／bridge／
  cycle 邊、框弧斷裂、缺框切口邊、branch sets 重疊、O 只碰一側、未吸收
  中間路徑、分割不連通／重疊／空、量詞顛倒、空支援族、singleton 適用範圍、
  只排除部分候選。每份正控制保存實際原邊、五集合、附件路徑及十條鄰接。

```bash
python3 scripts/c5_single_spoke_two_arc.py --check
python3 scripts/c5_single_spoke_cross_row.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_two_two_external.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_two_two.py --check
python3 scripts/c5_single_spoke_bridge_path.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 無參數時生成本輪 JSON／套表，有 `--check` 時重算逐 byte 比對。
當輪實際驗證及未重跑範圍見 [研究紀錄](history/2026-09-28-two-arc.md)。
有限 minor skeletons 不是滿足 degree/list 條件的來源圖、圖枚舉或可實現性
證書；任意大小由來源到 palettes 的既有論證、§2 的原圖五集合承擔。
`lake build` 不使本輪紙面引理成為 Lean 證明。

下一個具名入口是 **record 87 的 p₂**：s=0，S0=234、S1=012，
F0(q)={1}、F1(q)={2,3}；p₁ 已證。剩下唯一完整拒絕候選為
F0(p₂)={1,2}、F1(p₂)={3}。C0 的 target 支援族是 {23,34,234}；
每塊碰 b3 及 b2/b4 至少一者，O=012。連通兩弧若同時切開 23 和 34，
必有一側恰為 {b3}，但 O 不碰它，故本輪條件無法消除此候選。
q 在 C0 為 singleton，不能套雙列 pair residual 引理；需保留同一 C0 的
完整關係、旁支及實際附件，取得新的 singleton/pair 相容性或拓撲限制。
不因此聲稱 record 87 可實現或不可延拓。

一般 (2,2) 分離、其餘 t=1 分拆、t=0、更高 degree、多 degree-5、核心存在／
分離、共同出口及 `K∞=K≤5` 仍未證。
