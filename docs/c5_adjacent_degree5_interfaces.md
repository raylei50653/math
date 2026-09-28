---
docgraph:
  id: c5.adjacent-degree5-interfaces
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.degree5-interfaces
---
# 相鄰雙 degree-5：完整有序色對介面與逐類刪邊

後續整理（2026-09-28）：[唯一共鄰單點化約](c5_adjacent_degree5_shared_singleton.md)
與 [同側限制](c5_adjacent_degree5_singleton_sectors.md) 已接上
[01／23](c5_adjacent_degree5_singleton_long_arc.md)、[12](c5_adjacent_degree5_singleton_middle_arc.md)
雙列分離及 [34／40 排除](c5_adjacent_degree5_singleton_end_arc.md)，
唯一 mixed singleton 的全部支援已接回條件式出口。
[唯一 mixed K2 各一接點型](c5_adjacent_degree5_mixed_edge.md) 則由
[原四環次序](c5_adjacent_degree5_mixed_edge_order.md) 全部作 disk 來源排除。
[共鄰端點型](c5_adjacent_degree5_mixed_edge_shared.md) 的原 288 筆必要資料保持，
其中 [w 側 t=2、(1)](c5_adjacent_degree5_mixed_edge_shared_t2.md) 已證雙列、
加入出口第八類，不需 T4。其餘 w 分拆及一般雙 root 仍保留，必要表未證
實現性，未 Lean 化。下文保留第一輪語境；目前停止點見 [HANDOFF](HANDOFF.md)。

2026-09-28。接續 [list-critical 基礎](c5_weak_list_cores.md) 與
[單 root 完整介面](c5_degree5_interfaces.md)。本輪完成任意大小的精確接合、
root-edge 對角強迫、degree-4 分量解除，以及逐類 edge-minimality 條件。
這些是紙面證明；[Python 控制](../scripts/c5_adjacent_degree5_interfaces.py)
只核對指定有限圖／關係。未新增 Lean theorem，未作雙 root 分離或平面分類。
目前優先序見 [HANDOFF](HANDOFF.md)。

## 1. 同一來源、兩個有序 root 與完整接點

G 是有限簡單圖，B=(b₀,…,b₄) 誘導 C5，H 是有效內點誘導圖。
研究對象是保留 B 的 minimal q-core：q=01012 不延拓，而刪除任一非外圈邊
後 q 都延拓。令 U={0,1,2,3}，D=3。指定有序相鄰內點 (z,w)，
完整 degree 都為 5，其餘有效內點完整 degree 都為 4。
H 連通、每個內點的 q-boundary 鄰色互異，沿用 list-critical 的初等證明。
若來源另有 disk embedding／T4，始終保留，但以下接合與刪邊引理不需要它們。

令 C 遍歷 **原圖** H−{z,w} 的連通分量，定義

\[
 S_z=N_B(z),\quad S_w=N_B(w),\qquad
 P_C^z=N(z)\cap C,\quad P_C^w=N(w)\cap C.
\]

保存各 root 的原鄰接次序（有 embedding 時為其 rotation 中的次序），
以及各接點的原頂點身份。接點集合 P_C=P_C^z∪P_C^w 取固定次序；
共鄰點在 P_C 中只佔一個座標，同時帶有 z、w 兩個 incidence。
等價地可用兩份有序接點序列，但必加上兩序列同一頂點的座標相等約束。
不把共鄰點拆成兩個頂點，不補邊，不改接線，也不把兩 root 交換當作相同資料。

對任意 proper boundary row β（不只 q），設

\[
 L_\beta(v)=U\setminus\{\beta(x):x\in N_B(v)\},\qquad
 A_z(\beta)=L_\beta(z),\quad A_w(\beta)=L_\beta(w),
\]
\[
 \mathcal T_C(\beta)=
 \{(f(p))_{p\in P_C}: f\text{ 是 }C\text{ 的 proper }L_\beta\text{-coloring}\}.
\]

這是完整有序接點關係。供兩 root 接合的精確投影是

\[
 R_C(\beta)=\{(a,b)\in U^2:\exists t\in\mathcal T_C(\beta),\quad
   (\forall p\in P_C^z,\ t_p\ne a)\land
   (\forall p\in P_C^w,\ t_p\ne b)\}.
 \tag{1}
\]

兩組避色條件使用**同一個 t、同一份 f**。R_C 不含 zw 的異色條件，
也不預先限制 a∈A_z、b∈A_w；對角 (a,a) 必須保留，以處理刪 zw。
R_C 是此種雙 root 接合的完整 16 格允許關係，並非 \(\mathcal T_C\) 的可逆表示。

等價的 residual lists 為

\[
 M_{\beta,a,b}(v)=L_\beta(v)\setminus
   \bigl(\{a:v\in P_C^z\}\cup\{b:v\in P_C^w\}\bigr).
 \tag{2}
\]

共鄰點在 a=b 時只扣一個**色**，但有兩條原 root 邊；這個差異不可抹除。
不同 C 或不同 root 不可各自重命名顏色。全域 σ∈S₄ 的搬運恰為
\(R_C(\sigma\beta)=(\sigma\times\sigma)R_C(\beta)\)，
接點 tuples 亦須一起搬運。boundary 反射／旋轉另須同步搬運實際接線與次序。

## 2. 精確接合式

寫 Δ={(c,c):c∈U}、F_C(β)=U²∖R_C(β)，以及

\[
 K_\beta=(A_z(\beta)\times A_w(\beta))\cap\bigcap_C R_C(\beta),\qquad
 Z_G(\beta)=K_\beta\setminus\Delta.
 \tag{3}
\]

**精確接合定理。** Z_G(β) 恰為 G 的 β-延拓在有序 (z,w) 上的所有色對；
G−zw 的相應關係恰為 K_β。因此 β 延拓到 G iff Z_G(β)≠∅。

證明：限制一份全圖染色到各 C，直接得到 (1) 及兩 root lists、zw 異色。
反向固定同一個 (a,b) 後，對每個 C 選一份 (1) 的完整見證。各 C 內點
互不相交且無跨 C 邊，共用的 B、z、w 已固定同一色框，故可直接合併。
每條邊恰屬外圈、root-spoke、zw、C 內部、C-boundary 或 C-root 之一；
全部條件都已核對。去掉 zw 時只去掉 a≠b。證畢。

R_C 可由 unary lists、原內部邊的異色 factors、兩 root 的 incidence factors
natural join，再存在量化 C 變數得到。若先用 block-cut tree 分解，shared cut
vertex 的同一變數須留到兩側接合；不能先取端點 marginals。

## 3. Root-edge 對角強迫

**引理。** 若 q 不延拓到 G，但延拓到 G−zw，則

\[
 \varnothing\ne K_q\subseteq\Delta.
 \tag{4}
\]

反之 (4) 亦精確表示 q 拒絕 G 而接受 G−zw。因此 minimal q-core 必滿足 (4)。
證明由 (3)：刪 zw 給 K_q 非空；若其中有 a≠b，該染色可加回 zw，矛盾。
特別是 **G−zw 的每份 q-染色都使 z、w 同色**，不是只存在一份同色染色。

令 E={c:(c,c)∈K_q}，則
\(\varnothing\ne E\subseteq A_z(q)\cap A_w(q)\)。這不表示 E 是 singleton、
不表示 E={D}、不表示所有共同可用色都在 E。刪 zw 只釋放非空的對角色對，
不能宣稱整個 U² 或 off-diagonal 關係全開。§8 有 |E|=2 的固定圖控制。

## 4. Degree-4 的 tightness、共鄰點與分量解除

以下只要求 C 連通，且每個 v∈C 在原 G 的完整 degree 為 4；
β、a、b 任意，a=b 亦可，不要求 root lists 或 root-edge 合法。
因 C 的外部只有 B、z、w，

\[
 |M_{\beta,a,b}(v)|\ge 4-|N_G(v)\setminus C|=\deg_C(v).
 \tag{5}
\]

**Slack 引理。** 連通有限圖的 lists 若逐點至少等於 degree，且某點嚴格大於
degree，則可著色。以該點為根取生成樹，子點先於 parent 著色；非根尚有
未著色 parent，最後根使用多出的一色。單點圖也包含在內。

因此若 (a,b)∉R_C(β)，(5) 每點皆等號；每個點的所有**實際外部鄰居**
使用的色全互異。這同時給出：

- 若 C 有共鄰點，則 Δ⊆R_C(β)：a=b 會在該點造成 slack。
- 若 C 某點的兩個 boundary 鄰居在 β 下同色，則 R_C(β)=U²。
- 在拒絕列中，z 接點的 a、w 接點的 b 必各自避開該點 boundary 顏色；
  共鄰點另要求 a≠b。這些只是必要局部條件，非 R_C 的充分描述。

記 E_C 為所有至少一端在原 C 的邊，含內部邊、C-root 邊及 C-boundary
spokes；E_C 不含 zw 或 root-boundary 邊。對 e∈E_C，以 R_C^−e(β)
表示刪 e 後**整個原 C 區域**的允許關係，仍保存原接點變數，僅移除該邊條件。
若 C−e 分裂，兩側仍屬同一原區域。

**分量解除定理。** 對所有 β、e∈E_C，

\[
 R_C^{-e}(\beta)=U^2.\tag{6}
\]

證明：固定任意 (a,b)。若原本可著色，沿用原染色；否則上述 tightness 成立。

| e 的種類 | 刪除後為何可著色 |
| --- | --- |
| C-boundary spoke | 該外部色在其 C 端點只出現一次，刪邊新增一色；C 連通，使用 slack 引理 |
| zC 或 wC 邊 | 同理。若另一 root 也接該點，拒絕列已強迫兩 root 色不同，故確實新增一色 |
| C 內部非 bridge | lists 不變，C−e 連通，兩端 degree 各少一，出現 slack |
| C 內部 bridge | C−e 的兩個連通分量各有一端 degree 少一，分別使用 slack 引理 |

每個 (a,b) 都成功，得到 (6)。再刪其他邊只會放寬限制。此證明不用
Gallai、planarity、minimality 或兩 root 的 degree=5；只用 C 的完整 degree=4。
**全開的是被碰到的原分量關係**；其他分量、root lists 與 zw 條件仍在。

對 minimal q-core，每個 C 的 F_C(q) 必非空（§5），故 C 是 Gallai tree：
取任一拒絕色對，(5) 是不可著色 degree assignment，再用標準
[degree-choosability 定理，Dvořák Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
這項結構推論依賴外部定理；(1)–(6) 的證明均不依賴它。未在此排除 K4
或把 Gallai 型提升為 disk 可實現性。

## 5. 各類非外圈邊的 minimality 條件

本節全部在 q 下，同一份實際圖。簡寫 A=A_z(q)、B'=A_w(q)，
R=⋂_C R_C(q)，以及

\[
 O=(A\times B')\setminus\Delta,\qquad
 \Pi_C=O\cap\bigcap_{D'\ne C}R_{D'}(q).
 \tag{7}
\]

q 拒絕 G 等價於 O⊆⋃_C F_C(q)。在此前提下，
\(\Pi_C=O\cap(F_C(q)\setminus\bigcup_{D'\ne C}F_{D'}(q))\)，
所以 Π_C 是 C 的**私有有序色對**，不同 C 的 Π_C 互斥。

| 刪除 e | G−e 在 (z,w) 的精確 q 關係 | minimality 必要條件 |
| --- | --- | --- |
| zw | K_q | ∅≠K_q⊆Δ |
| zbᵢ | ((A_z^−e(q)×B')∩R)∖Δ | 此集合非空 |
| wbᵢ | ((A×A_w^−e(q))∩R)∖Δ | 此集合非空 |
| C-root 或 C-boundary 邊 | Π_C，由 (6) | Π_C≠∅ |
| C 內部非 bridge 或 bridge | Π_C，由 (6)，保留原 C 區域 | Π_C≠∅ |

這裡 A_z^−e 按**刪後實際鄰居**定義，不能在重複鄰色時假定新增一色。
minimality 強迫各 root 的 q-spokes 顏色互異。若 c=q(bᵢ)，root-spoke
條件於是可精確寫成

\[
 e=zb_i:\quad\exists b\in B'\setminus\{c\},\ (c,b)\in R;\qquad
 e=wb_i:\quad\exists a\in A\setminus\{c\},\ (a,c)\in R.
 \tag{8}
\]

證明：若刪 root-spoke 的染色仍用原 root list，就已能延拓 G，矛盾。
因此 root 必取新色 c，另一 root 須不同色，且所有原分量同時接受。
不能只找每個 C 各自接受的不同 b 或不同 a。

**完整逐邊等價式。** 對 §1 的 degree 規格（先不假定 minimality），
G 是 minimal q-core iff 以下四條同時成立：

1. O⊆⋃_C F_C(q)；
2. K_q≠∅（由 1 它自動包含於 Δ）；
3. 每個實際 root-boundary 邊的表中集合非空；
4. 每個原 C 有 Π_C≠∅。

必要性由表及 (6)。充分性：1 拒絕 q，2–4 逐類給每一非外圈刪邊的延拓。
因染色對刪邊單調，逐邊 critical 等價於非外圈邊集的 inclusion-minimality。
若已知 root-spokes 在 q 下互異，3 可直接換成 (8)；其餘內點的 spokes
互異亦被此等價式迫出，因重色會令該 C 的 F_C(q)=∅，違反 4。

這不是單 root 的 \(\bigcup F_C=A\) 等式。雙 root 的覆蓋域是 O；
O 以外只受 (4)、(8) 等條件限制，不能要求其全部不被任何 C 阻擋。
不同刪邊可有不同見證染色；每一份見證內的各 C 必共用同一有序色對。

**刪邊端點強迫。** 更一般地，q 拒絕 G 時，任何 G−uv 的 q-染色都滿足
f(u)=f(v)，否則可加回 uv。因此對 e∈E_C、(a,b)∈Π_C，每一份刪後 C
見證都使被刪邊兩端同色：刪 zv 時 f(v)=a、刪 wv 時 f(v)=b、刪 vbᵢ
時 f(v)=q(bᵢ)，刪 C 內部邊 uv 時 f(u)=f(v)。其餘原邊仍須全部 proper。
特別是 v 為共鄰點、只刪 zv 時，仍有 f(v)≠b，故 a≠b；不能連同 wv
一起忘掉。這也可直接由 Π_C⊆F_C(q) 及加回 e 反證，不需要選擇特定見證。

## 6. 接點計數與固定來源多步刪邊

設 t_z=|S_z|、t_w=|S_w|。因 q 只有三色且 spokes 互異，t_z,t_w≤3，
且由 zw 已佔各 root 一條邊，

\[
 \sum_C|P_C^z|=4-t_z,\quad\sum_C|P_C^w|=4-t_w,\quad
 |A|=4-t_z,\quad |B'|=4-t_w.
 \tag{9}
\]

共鄰點對兩個和各貢獻一次；不能以 |P_C^z∪P_C^w| 替代 incidence 總數。
每個 C 至少接一個 root，由 H 連通性得之。若有 r 個 C，私有色對互斥給

\[
 r\le |O|=|A||B'|-|A\cap B'|,
 \qquad r\le 8-t_z-t_w.
 \tag{10}
\]

因此 O=∅ 不可能是此規格的 minimal core：每個 root 至少另有一個 C 接點，
卻沒有私有非對角色對。這些只是必要計數，沒有列舉或認證平面來源。

更一般地，任取已刪非外圈邊集 J。令 I_J={C:J∩E_C=∅}，
A_z^J、A_w^J 按剩餘 root-boundary spokes 計算，並令
D_J=U²∖Δ（zw∉J）或 U²（zw∈J）。則

\[
 Z_{G-J}(\beta)=
 (A_z^J(\beta)\times A_w^J(\beta))\cap D_J\cap
 \bigcap_{C\in I_J}R_C(\beta).
 \tag{11}
\]

證明由 (6) 與 (3)，保留原分量身份即可，即使刪邊後分裂或出現孤立點亦然。
原 E_C 彼此互斥，與 zw、root-boundary edges 正好劃分全部非外圈邊。
這是固定來源精確公式；最多 r+t_z+t_w+1≤9 個二元開關，至多 512 個
配置（可重複），並非跨來源狀態分類、小 disk 代表或 weak-congruence 定理。

## 7. 共同色框下的跨列問題仍保留

對每個 proper β，接受條件仍是 (3) 非空。因此「minimal q、另拒絕相鄰
p、接受全部 T4」可精確表為：§5 的 q 條件、Z_G(p)=∅，及每個 T4 row
的 Z_G(β)≠∅。所有 R_C(β) 必由**同一張原圖與同一份實際接線**產生。
q 下的私有對可隨刪邊改變，跨 boundary rows 也不能獨立配製關係。

下一個窄問題是利用 (4)、(8) 與各 C 的原接線，限制同一來源在另一個
指定 p 下的完整 R_C(p)，尤其共鄰點分量與只接單 root 分量的互動。
本輪沒有完成全部相鄰雙 root 分離，沒有重跑唯一 degree-5 枚舉，
沒有把抽象 16 格關係候選當作平面可實現性證書。非相鄰雙 root、degree≥6、
更多高 degree 點、一般單側／共同出口與 K∞=K≤5 都仍保留。

## 8. 有限控制、重播與證據層

[checker](../scripts/c5_adjacent_degree5_interfaces.py) 與
[certificate](../artifacts/c5_adjacent_degree5_interfaces/observations.json)
只使用標準 Python。控制保留具名 boundary、z、w、原頂點與邊，包含
共鄰 singleton、edge、path、triangle、odd/even cycle、triangle 加 bridge、K4。
對全部 240 proper boundary rows，完整接點 tuples 的存在投影與獨立 pinned
list-coloring 回溯比較全部 16 格，並逐 E_C 邊核對 (6)。

另固定一張完整 degree 序列 (5,5,4,4) 的圖：z,w,x,y 誘導 K4，
z,w 各接 b₁,b₄，x,y 各接 b₄。q 下 A=B'={0,3}，
L_q(x)=L_q(y)={0,1,3}，故 K_q={(0,0),(3,3)}。
它拒絕 q 且 zw critical，但刪 zb₁ 或 wb₁ 仍拒絕 q，**不是 minimal core**。
這個控制區分對角強迫與完整 minimality，未宣稱它是 disk／T4 來源。
對其單邊及指定多邊刪除，(11) 與獨立全圖回溯逐列核對。

負控制另有共鄰 singleton：同一 x 接 z,w,b₁,b₄，L_q(x)={0,3}，
完整 R_C 恰拒絕 (0,3),(3,0)，但兩個 root 邊際投影都是 U。
將其拆成兩份各自可著色的 singleton，或把一維投影相乘，都會誤接受這兩格。
全域 S₄ 搬運另外核對，並保存不同分量獨立換色可誤接合的抽象負控制；
該抽象控制只說明量詞／色框錯誤，不提供來源圖。
另以單點完整 degree=5 的反例核對：刪一條重複外部色的邊仍可拒絕某色對，
故 (6) 的完整 degree=4 假設不可省略。

```bash
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

紙面一般證明不依靠有限圖窮盡；Gallai 推論單獨依賴外部定理。
`lake build` 只確認既有 Lean 專案仍可建置，不表示本報告已形式化。
本輪實際驗證與未重跑範圍見 [研究紀錄](history/2026-09-28-adjacent-degree5-interfaces.md)。
