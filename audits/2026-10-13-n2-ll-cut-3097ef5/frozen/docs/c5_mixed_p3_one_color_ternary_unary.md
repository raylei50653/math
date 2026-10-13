# 共鄰 P₃ 的一色支援飽和三接點 unary：原 triangle 與 K₅ 來源排除

**獨立驗收（2026-10-04，D₅）**：[最終成果固定快照與稽核](../audits/2026-10-04-task-d5/REPORT.md)
只新增關閉(CPP-134-1,34,60)、side IDs=(27,1)；九份自身支援配置、
27份完整relation組合、contacts次序／原bridges及逐份2↔3 lift雙射均核對。
未知w完整relation保持符號纖維；不以整側禁色聯集代替逐分量檢查。
連同C₂／C₃合用恰三keys，3500key ledger及原36／140／900表不刪，
其餘3497keys未關閉。以下各輪正文／artifacts保持，現行入口由weak-deletion導覽維護。

**獨立驗收（2026-10-04，D₄）**：[正式返回工作區稽核](../audits/2026-10-04-task-d4/REPORT.md)
C₃雙框strict-list、T／N葉及原K₅已独立核對；合用本頁
只登記geometry30／join20與geometry34／join20兩keys。
其他geometry／w角色未驗收，原C／C₂ artifact不改寫。

後續（2026-10-04，C₃）：[雙框點三接點 unary](c5_mixed_p3_two_frame_ternary_unary.md)
已重新證明 geometry 34／side_join_id 20 的原葉限制：先排接點碰 b₂，
再以原外路 K₅ 排雙框點非接點葉，完成這份任意大小來源排除。
本文單框點論證與當輪停止點保留；目前入口由 weak-deletion 導覽維護。

2026-10-04。接續[共鄰端點報告](c5_mixed_p3_common_endpoint.md#6-停止點與下一個具名入口)
的 **CPP-134-1／geometry 30／side_join_id 20**。
**z 側原三接點 unary 自身支援恰為 {b₁}、禁色 {0,2,3} 時，
完整 degree=4 迫其原圖就是三接點 triangle；原 z–x₂–b₄ 外路再給
K₅ subdivision。因此這份窄支沒有 disk source。**

這是任意有限 unary 大小的來源排除。完整三點 P₃、w 側、全部附件、
共同色框及原 bridges／旁支均保留。證明沒有先假設飽和 unary 是小圖，
也沒有做 target 查詢、T4 查詢或新增 Lean theorem。

[Checker](../scripts/c5_mixed_p3_one_color_ternary_unary.py)、
[證書](../artifacts/c5_mixed_p3_one_color_ternary_unary/observations.json)及
[本輪紀錄](history/2026-10-04-mixed-p3-one-color-ternary-unary.md)保存
原入口身份、完整關係與原邊 minor witnesses；驗證結果見歷史。

## 1. 固定同一來源與原 unary 身份

M 有限簡單，B=(b₀,…,b₄) 是 induced C5 disk 外框，q=01012，
U={0,1,2,3}；H=M−B 非空連通。M 拒絕 q，刪任一非框邊後接受 q。
相鄰 roots z,w 完整 degree=5，其餘內點完整 degree=4。
唯一 mixed 原分量是 C*=x₀x₁x₂，P*ᶻ=P*ʷ={x₂}。

固定原附件與完整三座標關係為

\[
S_0=\{b_0,b_1,b_4\},\quad S_1=\{b_1,b_4\},\quad S_2=\{b_4\},
\]
\[
\mathcal T_* =\{(3,0,1),(3,0,3)\},\qquad
F_* =\{(1,3),(3,1)\}.
\tag{1}
\]

本份必要 residual 是 E_z={1}、E_w={1,3}，A_z={b₁}、
A_w={b₂,b₄}，J=b₁b₂b₃b₄，色字串 1–0–1–2。
side roles 為 (8,1)：兩 root 均無 spoke，z 側一份原 unary 有三接點、
禁色 {0,2,3}；w 側一份原 unary 也有三接點、禁色 {0,2}。
後者仍是原必要角色，這裡沒有宣稱其實現。

記 z 側這份原分量為 D，其三個互異原接點為
P_D=(u₀,u₁,u₂)。這些符號標記原頂點，並非新增接點或替換 gadget。
因原 A_z={b₁} 且 z 無 spoke，D 的自身實際支援恰為 {b₁}。
D 外部只有 z 與 b₁；沒有 D–w 邊或 D–C* 邊。
令 \(\mathcal T_D(q)\) 是 D 所有完整染色的有序三接點 tuples，
\(f_D(q)=\bigcap_{t\in\mathcal T_D(q)}\{t_0,t_1,t_2\}=\{0,2,3\}\)。
所有染色及 lists 始終使用同一 q，未獨立正規化兩側。

## 2. 完整 degree 給最小內度與一份不可染 degree assignment

令 p(v)=1 當 v∈P_D，否則為 0；s(v)=1 當 vb₁ 是原邊，否則為 0。
簡單性與單一原框點支援使每點最多一條 vb₁；故完整 degree=4 給

\[
d_D(v)=4-p(v)-s(v)\ge2,
\qquad d_D(v)=2\Longleftrightarrow p(v)=s(v)=1.
\tag{2}
\]

固定 z=0 即足夠。這不要求 (0,w) 是整圖可用 root pair：僅查詢原 D。
因 0∈f_D(q)，原 D 在 lists

\[
M_0(v)=U\setminus\bigl(\{1:s(v)=1\}\cup\{0:p(v)=1\}\bigr)
\tag{3}
\]

下不可著色。外部色 0、1 互異，所以 |M₀(v)|=4−p(v)−s(v)=d_D(v)。
這是連通 D 的不可染 degree assignment。使用
[Dvořák，Lemma 7／Theorem 10，第 5–6 頁](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)：
D 是 Gallai tree，blocks 為 clique 或 odd cycle；M₀ 是 blockwise-uniform
assignment，incident palettes 在 shared cut vertex 互不相交並聯集為 list。
此定理只需 connected degree assignment，不需一般 critical-graph 前提。
本輪已直接讀取原文，沒有把後面的 critical-graph corollary 當作前提。

後續論證實際只需一個禁色 0≠q(b₁)。完整三禁色仍保存於原入口；
不另外假設每條 unary 邊的刪除見證，因以下 slack 論證已能提供所需染色。

## 3. 原外路使 D 的 K₄ block 不可能

原邊 zx₂ 與 x₂b₄ 仍存在，故
X=B∪{z,x₂} 在原圖中連通，且與 D 不交。
這補足[連通外框 K₄ 引理](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
所需的 exterior connectivity；這裡不用 root spoke，也不合併 w 側。

若 D 有 K₄ block K，每個 v∈K 已用三條 clique 邊，完整 degree=4
恰留一個原方向。該方向可直達 z 或 b₁；若進入 D−K，必是一條 bridge，
因剩餘 degree 只有一且 K 是原 block。四個外側分量互不相交：
若有外側路徑接回 K 的兩點，K 就不會是 block。

對這條 bridge vv′，D−vv′ 的兩個連通側都沿用同一 M₀。
各側的 bridge 端點少一條內邊，lists 比其新 degree 多一，故生成樹
slack 貪婪法各給至少一份完整染色。若兩端可取不同色便能拼回 D，
與 (3) 拒絕矛盾；因此兩側端點可取色集必是同一個 singleton。
若外側沒有實際 z／b₁ 附件，其全部 lists 為 U，可對完整染色作任意
S₄ 置換，端點就不可能只取一色。故外側必碰 z 或 b₁。

於是 K 的四點各有一條原 tether 抵達 X，四條路徑在 X 之前互不相交。
把 X 及各 tether 去掉 K 端點後的尾段合成一個 connected hub，
K 四點各為 singleton，十對鄰接均由原邊見證，得到 K₅ minor。
這與 disk planarity 矛盾，故 D 沒有 K₄ block。
K₅ block 的五點各已用完整 degree 四，不能再接原三接點或其他 D 頂點；
連通 D 會等於該 K₅ 且無接點，矛盾。更大 clique 直接違反 degree 四。
因此 D 的所有 blocks 只剩 bridges 與 odd cycles。

## 4. 葉 block 計數迫原圖恰是三接點 triangle

若有限 block-cut tree 有多於一個 block，至少有兩個 leaf blocks。
它們的 private vertices 屬不同原頂點集合；cut-vertex nodes 的 degree
至少二，故不能把第二個 leaf 偷換成一個沒有 private vertices 的 cut node。

leaf bridge 的 private endpoint 在 D 內 degree 一，違反 (2)。
每個 leaf odd cycle 至少有兩個 private vertices，這些點在 D 內 degree 二；
依 (2)，它們都必是原 z 接點且都有原 b₁ 附件。
兩個 leaf odd cycles 至少需要四個互異原接點，與 |P_D|=3 矛盾。

故 D 只有一個 block。bridge 已由 (2) 排除，cliques K₄ 以上由 §3 排除，
所以 D 是一個 odd cycle。其所有頂點 degree 二，依 (2) 全部都屬 P_D
且鄰接 b₁；原接點恰有三個，遂得到原圖等式

\[
V(D)=\{u_0,u_1,u_2\},\qquad
E(D)=\{u_0u_1,u_1u_2,u_2u_0\},
\tag{4}
\]

以及三條原 zuᵢ、三條原 b₁uᵢ。沒有消掉任何可能的 bridge 或旁支再猜
triangle；(4) 是對原 D 的結論，額外 vertices／blocks 已由葉數排除。

在同一 q 下完整有序關係因此恰為六份 tuples

\[
\mathcal T_D(q)=\{(0,2,3),(0,3,2),(2,0,3),
(2,3,0),(3,0,2),(3,2,0)\}.
\tag{5}
\]

三份拒絕 lists 的共同 triangle palettes 分別為
z=0：{2,3}；z=2：{0,3}；z=3：{0,2}。
z=1 時各點 list={0,2,3}，大小三大於內度二，接受。
這核對原完整禁色恰 {0,2,3}，未以三個獨立 marginals 取代 (5)。

## 5. 原外路補上第十條 K₅ 鄰接

在原 M 中取 branch vertices u₀,u₁,u₂,z,b₁。
三條 triangle 邊、三條 zuᵢ、三條 b₁uᵢ 已給九條 K₅ edges；
剩下 z–b₁ 用原路徑

\[
Q=z-x_2-b_4-b_3-b_2-b_1.
\tag{6}
\]

Q 的內點 x₂,b₄,b₃,b₂ 互異，與 D、z、b₁ 不交，所有邊均是已固定原邊。
故這十四條原邊構成 K₅ subdivision。等價的五個 minor branch sets 為
{u₀}、{u₁}、{u₂}、Z={z,x₂,b₄,b₃,b₂}、{b₁}。
Z 由 Q 的前四條邊連通，Z–{b₁} 的 witness 是原 b₂b₁。
十對鄰接與 disjointness 都可直接核對，無需 planarity oracle。

P₃ 的 x₀x₁、x₁x₂ 及全部六條附件、原 zw／wx₂、w 側原分量與附件
一直保留於 M；證書僅選取 witness 子圖，未把這些邊刪出原 source。
外路也沒有被當作可指定顏色的替代 boundary vertex。
因此 CPP-134-1／geometry 30／side_join_id 20 這份必要側接合
不能實現為具有原 degree／minimality 的 disk source。

## 6. 證書、範圍與停止點

Checker 核對固定入口與 predecessor payload 的連結、(1) 的兩份完整
P₃ triples、(5) 的六份完整 unary triples、三拒絕 palettes、color-1 slack、
四種原點身份的 16 個 pinned-list 核對、32 份 K₄ tether minor 控制、
兩條原框外路的 K₅ subdivisions 和五組 minor witnesses。
九條 unary 相關邊逐條刪除後，各四個 z 色均有局部染色，共 36 份；
其中三個原拒絕色的 27 份 witnesses 都使刪邊兩端同色。
另有九份保留 B、P₃、zw／wx₂ 的 partial colorings，固定 z=0、w=1，
完整 P₃ tuple=(3,0,3)。原 D_w 在 w=1 的完整避色 fibre 由禁色 {0,2}
保證非空；其內點染色未枚舉，這些 partial witnesses 不稱為全 source
colorings。它們表明局部 degree／刪邊解除可成立，失敗在原外路的平面性。
這些是固定域控制；任意 block 數、bridge 長度
及 unary 大小的排除由 §§2–5 紙面證明與外部 Gallai 定理承擔。

```bash
python3 scripts/c5_mixed_p3_one_color_ternary_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_one_color_ternary_unary.py --check
python3 scripts/c5_mixed_p3_common_endpoint.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

驗證結果見[本輪歷史](history/2026-10-04-mixed-p3-one-color-ternary-unary.md)。
Python 不重證外部 degree-choosability 定理，也不把 Jordan／Gallai 紙面
論證變成 Lean theorem；本輪沒有新增形式化宣稱。

前層的 36 個 retained cases、140 份必要幾何及 900 組 retained 側角色
仍是原控制的歷史計數。本輪只關閉固定這份側接合，沒有把整份 case、
全部 side joins、所有一色支援或 singleton 側首邊型一起計為已排除。
下一個具名入口是 **CPP-134-1／geometry 34／side_join_id 20**：
原 P₃、兩側三接點身份與禁色不變，自身支援改為
A_z={b₁,b₂}、A_w={b₂,b₄}。非接點可同時碰 b₁、b₂ 而內度二，
因此本頁單框點的葉數證明不能直接套用；本輪未研究此型。
目前停止點以[weak-deletion 導覽](c5_weak_deletion_guide.md#3-精確停止點與下一個窄問題)為準。
其他共鄰 P₃ 接合、triangle、更大／多 mixed、指定 target 出口、完整 Σ、
一般／共同出口及 `K∞=K≤5` 仍保留。
