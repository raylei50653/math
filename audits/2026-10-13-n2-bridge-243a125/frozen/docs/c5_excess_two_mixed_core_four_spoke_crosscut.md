# ε=2 四-spoke (2,2)：原 unary crosscut 封住 mixed 與二／三 hub 排除

**後續（2026-10-03）**：[共用短框弧原拒絕列延拓](c5_excess_two_mixed_core_four_spoke_short_arc.md)
已排本頁下一入口941原02／03與全部六份共用點殘留；
[不相交pairs完成報告](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md)
再排最後14／18，完成同一mixed11+各側unary子型。下文保留
當輪14／24數字及原證書；其他incidence與ε≥3仍保留。

2026-10-03，接手 HEAD=`0e38127`，沿用未提交的
[短 face](c5_excess_two_mixed_core_four_spoke_short_face.md)與
[同一長 face](c5_excess_two_mixed_core_four_spoke_long_face.md)成果。
接續 941 原 a=5、b=6、spokes=01／03，source indices=134／174；
933 的原 01／13、indices=100／156 使用同一幾何機制。
現況由 [Kempe 導覽](c5_kempe_guide.md)維護，實際驗證與貼用摘要見
[本輪紀錄](history/2026-10-03-excess-two-four-spoke-crosscut.md)。

**指定入口、root 交換及同機制 `(1,2,2)` 框架均作任意大小來源排除。**
Critical unary 的原 owner-to-support crosscut 把 C 限制到一個框點；
同一原路徑提供二／三 hub Gallai K₅ 反證，使 C 能延拓每份合法原
外部染色。只替換完整 C witness，原 mixed contact 邊 ax 因而非 critical。
933／941 新排 **8／16** 份，unequal-pair 必要框架從 **22／40
降至 14／24**；共用一框點者剩 **0／6**，不相交者仍 **14／18**。
整份 `(2,2)` 尚未完成，**共同 ε≥2 不變，ε≥3 未證，未新增 Lean theorem**。

## 1. 原來源與完整六角色關係

G 有限簡單，B=(b₀,…,b₄) 為指定有序 induced-C₅ disk 外框，
固定完整 Σ=933／941 或整圖 D₅ 像，每条非框邊 Σ-critical。
有效內部 H 連通，ε=2，恰兩個相鄰完整 degree-5 roots a,b，
其餘有效內點完整 degree 四。H−{a,b} 恰有原 mixed C 及 unary U、V；
C incidence=(1,1)、ordered contacts=(x,y)、owners=(a,b)，容許 x=y，
仍是同一原頂點。U、V 分別以原 au、bv 接線；兩側各兩條原 spokes，
原 ab 存在。所有原內邊、actual attachments／supports、bridges、
旁支、ownership、嵌入環序及共同字面四色框保持。

記原完整關係 R_C(β;x,y)、R_U(β;u)、R_V(β;v)，以及
A_r(β)=U₄∖β(S_r)。完整 joint 為

\[
J_G(β)=\{(A,D,X,Y,T,W):(X,Y)\in R_C(β),\ T\in R_U(β),\ W\in R_V(β),
\ A\in A_a(β),\ D\in A_b(β),\ A\ne D,X,T,\ D\ne Y,W\}. \tag{1}
\]

每個 tuple 的存在量詞由各原分量的完整 coloring witness 承擔。
先固定同一 β 及原 roots，才接合完整 tuples；不相乘 C marginals。
固定每個字面 (A,D) 後保存全部 (X,Y,T,W) 纖維，含空纖維。
省略原 ax 只去掉 A≠X，其他原 guards 不動。

## 2. Critical U 的實際附件與原 crosscut

先以 941 原 01／03 為具名座標。原 crosscuts 與 ab 給四個 faces：

| 原 face 邊界 | 原框包絡 | 能接入原分量 |
| --- | --- | --- |
| b₀–a–b₁–b₀ | {0,1} | U |
| b₀–a–b–b₀ | {0} | C、U、V |
| a–b₁–b₂–b₃–b–a | {1,2,3} | C、U、V |
| b–b₃–b₄–b₀–b | {0,3,4} | V |

原連通分量避開骨架，整份位於一個固定 open face，全部附件在其
closure。對 U 的兩個短 incident faces，actual support 分別包含於
{0,1} 或 {0}；原 a–b–b₃ 外路徑避開 C／U／V，終點在 {0,1} 外。
[短支援引理](c5_short_support_singleton.md)使 U 在每列能避開任何
a 色，原 au 非 critical。因此原 au critical 迫 U 在共同 face
F=(a,b₁,b₂,b₃,b)。若 F 中的 actual support 包含於 {1,2} 或 {2,3}，
原 spoke a–b₀ 提供 pair 外的外路徑，同一引理仍使 au 非 critical；
空／單點支援也包含於這些 pairs。因此其固定 actual support 必非短。

{1,2,3} 的非短子集恰為 {1,3} 與 {1,2,3}，故 **原 U 實際碰 b₁、b₃**。
不能只用 face 包絡推定這兩條附件存在。U 的連通性與原 au 給簡單路徑

\[
P:a-u\leadsto z-b_3,\qquad V(P)\setminus\{a,b_3\}\subseteq U. \tag{2}
\]

P 是 F 的原 crosscut，與 C、V 及其他骨架頂點互斥；它的兩側邊界弧為
a,b₁,b₂,b₃ 及 a,b,b₃。若 C 在 F，原 by 接線迫 C 位於 P 的 b-side，
否則由 C 內的原路徑與 b-contact 穿越 P。故

\[
\boxed{N_B(C)\subseteq\{b_3\}.} \tag{3}
\]

也可直接取 C 到 b₁ 或 b₂ 的原附件路徑，它與 P 的四個端點在 F
邊界交錯，得到矛盾。C 在另一個共同 face 時，該 face 是原 b₀ab
三角形，故 N_B(C)⊆{b₀}。整份 C 的實際 face 與原 P 在 β 之前固定。

一般取共同框點 h、另兩 spoke 點 p,q，三條框弧的長度為 `(1,2,2)`，
owner a 的 h–p 外 face 短、共同 p–q face 有兩段。完全相同的原
crosscut 把 C 支援封至 q；root 交換及一次整圖 D₅ 搬運均保持論證。

## 3. 同一原外路徑保 degree 的二／三 hubs

固定任一原 G−C 的完整 coloring，a=A、b=D；原 U、V witnesses 及所有
外部頂點逐點保留。若 C 在 b₀ab 三角形，A,D,β₀ 互異且原三 hubs
兩兩相鄰，直接使用既有三-hub 延拓。以下處理式 (3) 的 common-face C，
令 t=β₃。原 ab、bb₃ 給 A≠D、D≠t，允許 A=t。

若 C 不可延拓，原 exact lists 為

\[
L(w)=U_4\setminus\bigl(β(N_B(w))
\cup(\{A\}\text{ if }w=x\text{ else }\varnothing)
\cup(\{D\}\text{ if }w=y\text{ else }\varnothing)\bigr). \tag{4}
\]

x=y 時兩份 guards 同時作用於同一原點。完整 degree 四給
|L(w)|≥deg_C(w)。Connected slack-list 貪婪與
[Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
使拒絕時所有 lists tight，C 是 blockwise-uniform Gallai tree。
這是 degree assignment 定理，不需 G 在 β 是 minimal q-core。

先核對 K₄-free。原外部 B∪{a,b} 連通。若 C 有 K₄ block，每個 clique
點因完整 degree 四恰有一個外方向；若此方向是 bridge，刪橋後兩側
endpoint 都有 slack，兩側皆可染。拒絕迫兩個完整 endpoint domains
是同一 singleton；不碰原外部的那側可任意 S₄ 換色，不能是 singleton。
所以每個方向都有抵達原外部的路徑。四個方向在 Gallai block tree
中互斥，與連通原外部合成第五 branch set，給原 K₅ minor，矛盾。
此處沿用[連通外部 K₄ 引理](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
的局部證明；不假設新的 q-minimality。

**A≠t。** 取原外部 bags

\[
X=\{a\}\cup(V(P)\setminus\{a,b_3\}),\quad Y=\{b\},\quad Z=\{b_3\}.
\tag{5}
\]

三組互斥且連通，原 ab、bb₃、P 給三條 hub 鄰接。P 的內部全部在
U，沒有 C–U 邊，因此收縮沒有合併任何兩個 C 外鄰；C degree 四及
式 (4) 的 lists 都保持。給三 hubs 輔助色 A,D,t，三色互異。
既有[三-hub Gallai 引理](c5_short_support_singleton.md#4-三-hub-引理排除未見色接點數不設上限)
的末端 odd-cycle／bridge 論證给 K₅，與原 planarity 矛盾。

**A=t。** Tightness 禁止 C 的同一頂點同接 a、b₃；否則兩條原外邊
重複禁 A，該點有 list slack。取 X=V(P)、Y={b}，將整條原 P 兩端
合併，唯一可能的 C 鄰居碰撞已被排除，所以 C degree 仍四；auxiliary
lists 亦保持。兩 hubs 相鄰，C 為 K₄-free Gallai tree，既有
[兩-hub引理](c5_short_support_singleton.md#3-兩-hub-gallai-引理五個-branch-sets)
給 K₅。不能在未證 tightness 時合併 a、b₃，也不能在 A≠t 時作此合併。

以上收縮只作 topology 反證。P 內部 U 點的原色不必等於 A，沒有宣稱
保存原 U 路徑染色或把收縮圖當作 relation factor；原 R_C、R_U、R_V
與式 (1) 始終不動。兩個 Gallai 引理覆蓋任意 cycle 長度、bridges 與
旁支，Python 有限控制不承擔無界覆蓋。

## 4. 完整 C witness 替換與原 ax 非 critical

兩個位置都證成：**每份合法原 G−C coloring 能延拓整份原 C，並逐點
保留 C 外的全部頂點。** 因而

\[
\pi_{a,b,u,v}J_G(β)=J_{G-C}(β). \tag{6}
\]

取任一 G−ax coloring，限制至 C 外後是原 G−C coloring；用上述
完整 C witness 替換它原有的 C coloring，恢復 ax 與所有原 C 邊，
原 roots、U、V、β 逐點不變。因此

\[
\pi_{a,b,u,v}J_G(β)=\pi_{a,b,u,v}J_{G-ax}(β),\qquad
\boxed{\Sigma(G-ax)=\Sigma(G).} \tag{7}
\]

ax 是 β 之前固定的一條原 mixed contact 邊，與 Σ-criticality 矛盾。
本證明不需前序 Σ(G−C)=Ω，也不跨列相加禁色容量。
**完整六角色 joints 不必相等**，因為 (x,y) 的 witness 可能改變。

## 5. 固定域、完整 degree 圖與證書

[Checker](../scripts/c5_excess_two_mixed_core_four_spoke_crosscut.py)、
[joint helper](../scripts/c5_excess_two_four_spoke_crosscut_joint_controls.py)、
[artifact](../artifacts/c5_excess_two_mixed_core_four_spoke_crosscut/observations.json)
只讀前序原身份、骨架邊、spokes、root order 與 apex rotation。
30 份殘留共用單點骨架核對全部 **2,880 rotations／60 disk rotations**；
24 所排框架各保存 8 份 actual U 支援與 8 份 actual C 支援，含空支援。
U 的 192 子集中 48 份可 critical；C 的 192 子集中 48 份與 crosscut 相容。
48 份明示 apex K₃,₃ subdivisions 核對九條互斥 paths，apex 只在原 disk 外側。

保存全部 720 份合法原列／root-color cases，其中 **192 份同色二-hub、
528 份異色三-hub**；5,760 局部外鄰子集核對 exact lists、tightness、
合併碰撞及 degree 保持。另核對 24 原 root swaps、3,840 共同 D₅ 支援
子集、7,200 列／root-color 搬運及 480 搬運後 subdivision 檢查。
短支援 local／three-hub 數學 payload 與原 artifact 唯讀重算相同。

| 原候選必要域 | 933 | 941 |
| --- | ---: | ---: |
| 前序 unequal-pair 框架 | 22 | 40 |
| 本輪原 crosscut 排除 | **8** | **16** |
| 剩餘共用一框點 | 0 | 6 |
| 剩餘不相交 pairs | 14 | 18 |
| 剩餘合計 | **14** | **24** |

新排原 indices：933=100,113,116,127,156,162,172,190；
941=134,137,156,160,174,181,196,222,237,245,262,266,280,281,305,306。
固定必要框架不提供來源實現或 Σ-critical witnesses。

原 933 01／13 用 g(i)=1−i mod5 送到 canonical 01／03，所有 β、
attachments／supports、嵌入與 contacts 同時搬運。**此映射把 Σ933
送到 940，並非 941**；證書保存完整列與色置換，僅對照幾何，沒有
識別兩候選來源的完整 relations。

18 張手建完整 degree 圖含 C 的 W₄ 相鄰／相對 contacts 及原共鄰
subdivided-K₄ contact、三種 unary 配對與 root 交換；C 實際支援為 {3}。
G／G−ax／G−by／G−C 的 **720 完整 joints、11,520 pinned fibres**
與獨立整圖回溯相同，540 四角色投影核對保存 **7,752 整份 C 替換
witnesses**，逐原邊驗證且 C 外逐點不變。另有 360 原 mixed 邊接回、
360 swaps 及完整六角色 joint 不相等的負控制。這些圖不宣稱 disk、
候選 Σ 或 criticality；拓撲骨架亦不補滿來源 degree。

## 6. 重播與精確停止點

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_crosscut.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_crosscut.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_long_face.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

無參數只生成本輪新 artifact，`--check` 唯讀逐 byte 比對。實際驗證及
未重跑範圍見本輪紀錄；`lake build` 不形式化本輪 crosscut／Gallai 合成。

**停止於 `(1,2,2)` 原框架排除；unequal 剩 14／24，整個子型未完成。**
下一窄入口為 941 原 spokes=02／03、source index=155、root swap=175；
六份共用框點殘留為 155,175,179,239,243,263。Critical U、V 在兩個不同
原外 faces，actual supports 分別必含 {0,2}、{0,3}；C 在原 0ab 三角形
或共同四邊形 (a,b₂,b₃,b)，後者支援包含於 {2,3}。這裡沒有本輪的
owner-to-far-end crosscut，不自動套用封單框點或三異色 hub 引理。
保留同一原圖、原環序及完整六角色 joint，再研究此短框弧上的 mixed
relation 與兩份 critical unary 的共同限制，不重開來源 catalogue。

其他 `(2,2)` incidence、較少 spokes、單省略、原 `(5,5)` q-core、
多 mixed／no-mixed／非相鄰 roots 與 unary 側例外保留；ε≥3、來源實現、
一般出口及 K∞=K≤5 未證。本輪未 commit／push。
