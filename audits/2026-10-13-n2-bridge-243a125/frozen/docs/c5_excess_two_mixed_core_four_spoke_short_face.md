# ε=2 四-spoke (2,2)：原 unary 的短 face 與非 critical 接線

**後續（2026-10-03；2026-10-04 整理）**：本頁短 face 當輪排8／16份，
unequal框架由40／66降至32／50；同日[長 face 次序排除](c5_excess_two_mixed_core_four_spoke_long_face.md)
排原01／04、root交換與同機制10／10份，中間殘留為22／40。其後
crosscut、短框弧及[不相交pairs總報告](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md)
完成四-spoke (2,2)、mixed-(1,1) 加各側一原 unary 子型，最後殘留0／0。
以下保留原正文、輪次數字、停止點及證書；其他 incidence 與 ε≥3 仍未證。
最新停止點與排程由 [Kempe 導覽](c5_kempe_guide.md)維護。

2026-10-03，接手基準 `0e38127`。接續
[共用原 pair 的 sealed mixed 排除](c5_excess_two_mixed_core_four_spoke_equal_pair.md)
所留原 `a=5、b=6、spokes=01／02`，source indices=97／133，
root 交換=111／153。現況由 [Kempe 導覽](c5_kempe_guide.md)維護；
實際驗證與貼用摘要見 [本輪紀錄](history/2026-10-03-excess-two-four-spoke-short-face.md)。

**上述具名入口與 root 交換均作任意大小來源排除。** 原 a-side unary
U 無論位於哪個可用原 face，都只有相鄰兩點以內的實際支援。
既有短支援引理逐列使 U 能避開任何 root 色，所以原 au 的省略
不改變完整 Σ，與 Σ edge-minimality 矛盾。此證明不需將 C 化約成
有限圖，也不需先證其所有合法 root pair 都能延拓。

同一機制排除 933／941 的 **8／16 份** unequal-pair 具名框架，
殘留從 **40／66 縮到 32／50**。其中共用一框點者剩 **18／32**，
不相交者仍 **14／18**；整份 (2,2)、mixed-(1,1) 加各側一 unary
尚未完成。證據為任意大小紙面合成及 Python 固定域證書；
**共同 ε≥2 不變，ε≥3 未證，沒有新增 Lean theorem。**

## 1. 原來源、分量身份與完整 joint

沿用前序來源前提：G 有限簡單，B=(b₀,…,b₄) 為指定有序
induced-C₅ disk 外框，完整 Σ=933／941 或整圖 D₅ 像，每條非框邊
刪除均嚴格擴大 Σ。有效內部 H 連通，ε=2，恰兩個相鄰完整
degree-5 roots a,b，其餘有效內點完整 degree 四。

H−{a,b} 恰為原 mixed C 及原 unary U、V；C contacts=(x,y)、
owners=(a,b)、incidence=(1,1)，允許 x=y 但不複製原頂點。
原 unary 接線為 au、bv，各側各兩條 spokes，原 ab 存在。
保存原 C／U／V 的全部內邊、actual attachments／supports、bridges、
旁支、ownership、原嵌入環序與同一字面四色框。

令原完整 relations 為 R_C(β;x,y)、R_U(β;u)、R_V(β;v)，
A_r(β)={0,1,2,3}−β(S_r)。六角色 joint 是

\[
J_G(β)=\{(A,D,X,Y,T,W): (X,Y)\in R_C(β),\ T\in R_U(β),\ W\in R_V(β),
\ A\in A_a(β),\ D\in A_b(β),\ A\ne D,X,T,\ D\ne Y,W\}. \tag{1}
\]

每個 tuple 都附原分量的完整染色存在量詞；固定原 B、roots 後
才接合，不將 C 的 marginals 相乘。固定字面 (A,D) 後保留完整
(X,Y,T,W) 纖維，含空纖維。省略 au 只去掉式 (1) 的 A≠T，
其餘原邊、contacts、root guards 及兩份其他分量均保留。

## 2. 任意原嵌入的四個 faces 與實際支援包絡

先固定原 spokes=01／02。原 crosscut b₀–a–b₁ 分開 disk。
原 b 接 b₂，故 b 及原 ab、bb₀、bb₂ 在含 b₂ 的那側；
再用該側的原 crosscut b₀–b–b₂。只有剩餘區域的 closure 同時
含 a、b，故原 ab 位於其中，將它切成原三角形 b₀ab 與
原四邊形 a b₁ b₂ b。整份骨架的四個內側 open faces 因此為

| 原 face 邊界 | 原框點包絡 | 能接入的原分量 |
| --- | --- | --- |
| b₀–a–b₁–b₀ | {0,1} | U |
| b₀–a–b–b₀ | {0} | C、U、V |
| a–b₁–b₂–b–a | {1,2} | C、U、V |
| b–b₂–b₃–b₄–b₀–b | {0,2,3,4} | V |

表中的可接入只表示 closure 含所需 roots，不宣稱存在實際附件。
原連通分量避開 skeleton，故整份位於一個固定 open face；其
原 contact edges 與框附件只能落在該 face 的 closure。尤其

\[
N_B(U)\subseteq\{b_0,b_1\},\quad\{b_0\},\quad\text{或}\quad\{b_1,b_2\}, \tag{2}
\]

三者取決於原嵌入中的同一個固定 face，不能逐列換 face，也不
將包絡當成全部實際支援。C 可以是共鄰或不同 contacts、任意
bridges／旁支；它的 face 包絡仍保留為 {0} 或 {1,2}，本輪不需要
單獨判定 C 的 pair relation。

一般共用單框點 h 的兩份 pair，寫成 S_a={h,p}、S_b={h,q}。
選沿 B 的方向使 h,p,q 依序出現，三條原框弧 I_hp、I_pq、I_qh
各有正長度，總和五。上述同一 crosscut 證明給出四 faces：
a 外側 I_hp、兩-root face I_pq、b 外側 I_qh 及原三角形 hab_h。
因此若 a 所接的三個 faces 的框包絡都包含於某條原框邊，原 U
必短；b 側同理。直接機制恰適用於三弧長度 (1,1,3) 或 (3,1,1)。
Python 對原七點骨架的全部 rotations 核對這些包絡；任意大小
soundness 由本節紙面證明承擔，不由一份 apex rotation 推定。

## 3. 原短支援引理使 au 非 critical

使用 [短支援引理](c5_short_support_singleton.md)：原連通 unary
W 的每點完整 degree 四、只接 root r；若實際框支援包含於原
相鄰框點對 {h,k}，r 有原 spoke，且有一條原 r→ℓ 的外部路徑
避開整份 W、ℓ∉{h,k}，則對每列 β，

\[
F_W(β)=\bigcap_{t\in R_W(β)}\operatorname{set}(t)=\varnothing. \tag{3}
\]

這個引理不限制原分量大小、接點數、odd cycles 或 bridges，
不要求整份 G 是該列的 minimal q-core。U 只有原 au 接 roots，
所以也是 H−a 的原分量；a 另接 b、C，b 保持 degree 五不影響
引理。式 (2) 的全部前提逐面由同一原 skeleton 提供：

| U 的原 face 包絡 | 使用的原相鄰 pair | 原外部路徑 L |
| --- | --- | --- |
| {0,1} | {0,1} | a–b–b₂ |
| {0} | {0,1} | a–b–b₂ |
| {1,2} | {1,2} | a–b₀ |

每條 L 的內點只可能是另一 root，避開原 C、U、V，終點在 pair
之外；全部邊均是原邊。故每列 F_U(β)=∅。R_U 本身非空：
忽略 au 時，u 的 boundary-only lists 有至少一色 slack，而所有
其他 U 點至少是 degree lists；連通生成樹逆序貪婪可染整份 U。
對單接點更可寫成 |R_U(β;u)|≥2。

取任意原 G−au 的完整 coloring f，令 A=f(a)。式 (3) 選一份
原 U 的完整 witness，contact 色 T≠A。只替換原 U，保存 β、
roots、整份原 C／V witnesses，即可接回原 au。精確 relation 等式是

\[
\pi_{a,b,x,y,v}J_G(β)=\pi_{a,b,x,y,v}J_{G-au}(β),\qquad
\boxed{\Sigma(G-au)=\Sigma(G).} \tag{4}
\]

這是五角色投影相等，**不宣稱完整六角色 joints 相等**：原 u 的
允許 tuples 會受 au guard 篩選。共鄰 x=y 仍保留同一原 contact。
式 (4) 與完整 Σ edge-minimality 矛盾；亦可直接取 au 的新接受
列及其整圖 witness，見其必能延拓。沒有將逐列 q-minimality
代入，沒有用 Σ(G−C)=Ω，沒有從邊刪除推定其他子圖的 minimality。

局部非 critical 結論本身不依賴 Σ 恰為 933／941；本輪具名必要域
及剩餘計數只限前述固定候選，不能外推其他原 incidence 型。
外部依賴仍是既有連通外框 K₄、Gallai／二三-hub minor 與 degree-list
刻畫。[Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
本輪核對 degree assignment、tightness 與 blockwise palettes 前提；
沒有用四色定理作 oracle，未新增任意大小外部定理假設。

## 4. 固定證書、重播與停止點

[Checker](../scripts/c5_excess_two_mixed_core_four_spoke_short_face.py)／
[joint helper](../scripts/c5_excess_two_four_spoke_short_face_joint_controls.py)／
[artifact](../artifacts/c5_excess_two_mixed_core_four_spoke_short_face/observations.json)
唯讀前序具名 skeletons，逐份比對原 index、root order、spokes、
全部原骨架邊及 apex rotation。74 份共用一點 frames 各窮盡
96 份 rotation assignments，恰兩份以原 B 作一個 face 的 spherical
rotations；**7,104 assignments／148 disk rotations** 全保留。
所排每份原 unary 的三個 face 包絡、相鄰 pair 與原外部 L 明存。

| 原候選具名域 | 933 | 941 |
| --- | ---: | ---: |
| 前序 unequal pairs | 40 | 66 |
| 本輪短 face 排除 | **8** | **16** |
| 剩餘共用一點 | 18 | 32 |
| 剩餘不相交 | 14 | 18 |
| 剩餘合計 | **32** | **50** |

另有 24 份原 root 交換身份及 7,200 次整體 D₅／列／原 L 搬運，
沿用短支援 local／three-hub 數學 payload 唯讀重算相同。具名
候選框架只是必要域，不宣稱實現、候選完整 Σ 或 Σ-criticality。
另有 **24 張完整 degree 圖**，C 取共鄰 singleton／不同接點 edge／
triangle，U／V 取四份形狀配對，含 root 交換。保存全部實際附件、
contacts、原 root 邊、十列完整 tuples 及染色 witnesses。
G、G−au、G−bv、G−ab、四條原單 spoke 省略及 G−C 共九種圖，
**2,160 joints／34,560 pinned fibres／1,680 原邊接回／1,080 root
交換**與獨立全圖回溯相同，纖維包含空集。

其中 108 份 |R_U|≥2 的原圖列逐份核對式 (4) 的五角色投影，
**3,736 份原 U 替換 witnesses**保存替換前後整圖 coloring，逐原邊
核對，原 U 之外的所有頂點保持。另保留 58 份 singleton U 投影
失敗列、具體 au 接回阻塞、C marginals 假允許及 spoke 接回阻塞。
一份實際支援 01 的原 U triangle 每列只取 β₁，保存原 K₅ branch
sets；說明短支援排除需要 planarity，不能當成任意圖代數限制。
這些圖沒有 disk、候選 Σ 或 criticality 主張；它們核對有限接合
及帶明列 relation 前提的 witness 替換，沒有以任意附件圖核對
式 (2) 的 disk 幾何或普遍式 (4)。

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_short_face.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_short_face.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_equal_pair.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

無參數只生成本輪新 artifact；`--check` 重算逐 byte 比對。
本輪未重跑整倉歷史來源 catalogue、R 系列或全 degree-6 分拆，
原證書未覆寫。`lake build` 不形式化本頁 crosscut／短支援合成。

**停止於選定 01／02 與同機制 8／16 份來源排除，unequal pairs
剩 32／50。** 下一具名入口為原 spokes=01／04，indices=98／135，
root 交換=126／195。其兩份 unary 各有長 face 可用，不能套本輪
「所有 incident faces 都短」前提。保留原 C／U／V、actual supports、
共同 lifts、原嵌入與完整六點 joint，再分析同一長 face 的分量位置。
其他 (2,2) incidence、較少 spokes、單省略、原 (5,5) q-core、
多 mixed／no-mixed／非相鄰 roots 及 unary 側例外均保留；
ε≥3、來源實現、一般出口及 K∞=K≤5 未證。本輪未 commit／push。
