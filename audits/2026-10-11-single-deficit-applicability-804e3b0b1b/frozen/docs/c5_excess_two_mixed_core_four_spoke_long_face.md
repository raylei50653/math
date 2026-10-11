# ε=2 四-spoke (2,2)：同一長 face 的兩原 unary 次序排除

**後續（2026-10-03；2026-10-04 整理）**：本頁長 face 當輪排10／10份，
unequal殘留為22／40；同日[原 crosscut](c5_excess_two_mixed_core_four_spoke_crosscut.md)
排941原01／03、933原01／13、root交換及同機制8／16份，中間殘留為14／24。
再經短框弧及[不相交pairs總報告](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md)
完成四-spoke (2,2)、mixed-(1,1) 加各側一原 unary 子型，最後殘留0／0。
以下保留原正文、輪次數字、停止點及證書；其他 incidence 與 ε≥3 仍未證。
最新停止點與排程由 [Kempe 導覽](c5_kempe_guide.md)維護。

2026-10-03，接手基準 `0e38127`，保留既有未提交的
[短 face 成果](c5_excess_two_mixed_core_four_spoke_short_face.md)。
本輪接續原 a=5、b=6、spokes=01／04，source indices=98／135、
root 交換=126／195。現況見 [Kempe 導覽](c5_kempe_guide.md)，
驗證及貼用摘要见 [本輪紀錄](history/2026-10-03-excess-two-four-spoke-long-face.md)。

**選定 01／04 及同機制具名來源均排除。** 若兩份原 unary 都在
唯一共同長 face，實際支援沿它的三段框弧必須依序排列；每份
Σ-critical unary 又不能有短支援，所需至少四段，與三段矛盾。
因此有一條固定原 unary 接線的省略不改變完整 Σ。
933／941 各新排 **10 份**，unequal-pair 必要框架由 **32／50
降至 22／40**；整份 (2,2) 子型尚未完成。
這是任意大小紙面合成與 Python 固定域證書，**共同 ε≥2 不變，
ε≥3 未證，未新增 Lean theorem**。

## 1. 原來源與完整六角色 joint

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框，
固定完整 Σ=933／941 或整圖 D₅ 像；每條非框邊刪除均嚴格擴大
Σ。有效 H 連通，ε=2，恰兩個相鄰完整 degree-5 roots a,b，
其餘有效內點完整 degree 四。原 H−{a,b} 恰有 mixed C 與兩份
unary U、V，C incidence=(1,1)、contacts=(x,y)、owners=(a,b)，
U、V 分別以原 au、bv 接線。容許 x=y，仍是同一原頂點。
各側兩條原 spokes，原 ab 存在；所有原分量、內邊、attachments、
actual supports、bridges、旁支、ownership、嵌入與色框保持。

固定 proper β，令 R_C(β;x,y)、R_U(β;u)、R_V(β;v) 為原完整
分量關係，A_r(β)=U₄∖β(S_r)。原 joint 為

\[
J_G(β)=\{(A,D,X,Y,T,W):(X,Y)\in R_C(β),\ T\in R_U(β),\ W\in R_V(β),
\ A\in A_a(β),\ D\in A_b(β),\ A\ne D,X,T,\ D\ne Y,W\}. \tag{1}
\]

每份 tuple 的存在量詞是各原分量的完整 coloring witness。
先固定同一字面 β、原 root colors 才接合；C 的 marginals 不能
相乘。固定 (A,D) 後保留全部 (X,Y,T,W) 纖維，包含空纖維。
省略 au 或 bv 只移去各自的 A≠T 或 D≠W guard。

## 2. 原短 faces 與唯一共同長 face

01／04 的原 crosscuts 與原 ab 給四個 disk 內側 faces：

| 原 face 邊界 | 原框包絡 | 可接入原分量 |
| --- | --- | --- |
| b₀–a–b₁–b₀ | {0,1} | U |
| b₀–a–b–b₀ | {0} | C、U、V |
| b–b₄–b₀–b | {0,4} | V |
| a–b₁–b₂–b₃–b₄–b–a | {1,2,3,4} | C、U、V |

前輪的 crosscut 論證同樣適用：原連通分量避開 skeleton，整份
位於某個固定 open face，所有原接線與框附件在其 closure。
Python 另窮盡每份原骨架的全部 rotations，並非選一份 apex
rotation 當作所有來源的嵌入。

若 U 在前兩個短 faces，其 actual support 包含於 {0,1}，
原外路徑 a–b–b₄ 避開 C／U／V、終點在此 pair 外。
若 V 在短 faces，使用 pair {0,4} 與原路徑 b–a–b₁。
[短支援引理](c5_short_support_singleton.md)遂使對應 unary 在每列
都能避開任何 root 色，原接線非 critical，詳見 §4。

因此仍可能 Σ-critical 的兩份 unary 必須同時位於同一原長 face
F，其原 actual supports S_U、S_V 均包含於 {1,2,3,4}。
這只是同一固定 face 的包絡，沒有把包絡當作全部實際支援，
也沒有逐列重新挑選 face。C 位於哪個 face 不影響下面的論證。

## 3. 原交錯路徑與三段框弧

沿 F 的原邊界次序 a,b₁,b₂,b₃,b₄,b，使用位置 1,…,4。
若 j∈S_U、k∈S_V 且 j>k，原 U 的連通性及實際附件給簡單路徑

\[
P_U:a-u\leadsto z-b_j,\qquad P_V:b-v\leadsto w-b_k,
\]

其內部頂點分別全部位於原 U、V。兩份原分量互斥，所以路徑
內部互斥、也不碰 F 邊界的其他點；四個端點 a,b_k,b_j,b 沿 F
交錯。Disk 中的簡單 crosscut 分隔兩個邊界弧，另一條路徑無法
連接兩側，矛盾。因此對非空支援必有

\[
\boxed{\max S_U\le\min S_V.} \tag{2}
\]

共用原框端點允許等號；只有 j>k 時才使用四個不同端點。
空支援與單點支援已是短支援，不假造缺失的 max／min。
兩份非空 actual supports 的區間跨度 d_U、d_V 滿足

\[
d_U+d_V=(\max S_U-\min S_U)+(\max S_V-\min S_V)\le4-1=3. \tag{3}
\]

所以至少一份 d≤1，其 actual support 包含於原框邊 12、23 或
34。這份 unary 的 owner 有原 spoke 到 b₀，故原外路徑
owner–b₀ 避開整份 unary，終點在 pair 外。空支援也可用任一
具名框邊及原外路徑。短支援引理遂適用。

等價地，Σ-criticality 的原 au／bv witnesses 各迫非空 unary
禁色見證；短支援引理使每份固定原支援跨度至少二，式 (3) 卻
要求 4≤3。兩個 critical witnesses 可以在不同列，相加的是
**同一原來源的固定幾何支援跨度**，沒有跨列相加容量或禁色。

一般共同框點 h、外侧 spokes 到 p、q 的同機制要求三弧長度
(1,3,1)：兩側外 face 都短、唯一共同長 face 的框弧恰三段。
全局 D₅ 搬運與 root 交換保留原圖，給本輪所有 10／10 份。
其他 arc types 不由式 (3) 自動排除。

## 4. 固定一份原 unary 的 witness 替換

按原嵌入及 actual supports，選定 §2 或 §3 證成短的那份 W。
這個選擇在 β 之前固定。W 是 H−owner 的原 unary 分量，
每點完整 degree 四、唯一原 contact 邊、原 spoke 及外路徑皆
保持，故短支援引理給 F_W(β)=∅ 對所有 proper β 成立。
原 contact slack 的生成樹貪婪保證 R_W 非空；單接點時因此有
至少兩個 contact colors。

取任意 G−e 的完整 coloring，其中 W=U 時 e=au、W=V 時 e=bv。
若 W=U，就只替換同一原 U 的
完整 witness，使 u 避開固定 a 色；B、roots、完整 C 的同一
(x,y) witness 及整份 V 都逐點保留。W=V 時同理。精確等式是

\[
\begin{aligned}
W=U &: \ \pi_{a,b,x,y,v}J_G(β)=\pi_{a,b,x,y,v}J_{G-au}(β),\\
W=V &: \ \pi_{a,b,x,y,u}J_G(β)=\pi_{a,b,x,y,u}J_{G-bv}(β).
\end{aligned} \tag{4}
\]

所以固定原邊 e=au 或 bv 滿足 Σ(G−e)=Σ(G)，與完整 Σ
edge-minimality 矛盾。**不宣稱完整六角色 joints 相等**，因為
恢復原邊仍會篩選被忘記的 contact 色。此證明不需要 Σ(G−C)=Ω，
不固定一列的 q-minimal core，也不要求 C 的每個合法 root pair
延拓。

外部依賴只沿用既有短支援的連通外框 K₄、兩／三-hub Gallai
minor 及 degree-list 刻畫。重新取得的
[Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
確認 connected degree assignment 的 slack／tightness 及 blockwise
uniform 前提；本輪没有以四色定理為 oracle，也未新增外部定理。

## 5. 固定域證書及具名殘留

[Checker](../scripts/c5_excess_two_mixed_core_four_spoke_long_face.py)、
[完整圖 helper](../scripts/c5_excess_two_four_spoke_long_face_joint_controls.py)、
[artifact](../artifacts/c5_excess_two_mixed_core_four_spoke_long_face/observations.json)
唯讀前序來源 identity、原骨架邊、root order、spokes、apex rotation。
50 份剩餘共用單點骨架各核對 96 rotations，**4,800 assignments／
100 disk rotations**；所排各份明存全部 incident faces、短 face
原外路徑及共同長 face 的原框弧。

每份所排框架保存 16×16 份 actual support 子集，包括空支援。
其中 80 份與原次序相容（49 份兩邊非空）；64 份兩支援都非短
者全部交錯。合共 **5,120 支援對／1,280 雙非短 pair**，無相容
雙非短 pair。每份六種交錯端點保存兩條原路徑的身份及其收縮後
apex 圖的九條互斥 K₃,₃ subdivision paths，合共 **120 份**。
Apex 位於原 C₅ disk 外側，與 boundary 相接；收縮只用於拓撲
反證，不用於染色關係或 degree／Σ 保持。固定 skeleton 不補滿
來源 degree；任意大小 crosscut 定理由 §3 承擔。

另有 20 原 root 交換、51,200 全局 D₅ 支援對、2,000 同框列
搬運及 1,200 搬運後 subdivision path checks。短支援 local／
three-hub 數學 payload 與原 artifact 唯讀重算相同。

| 原候選必要域 | 933 | 941 |
| --- | ---: | ---: |
| 前序 unequal-pair frames | 32 | 50 |
| 本輪同一長 face 排除 | **10** | **10** |
| 剩餘共用一框點 | 8 | 22 |
| 剩餘不相交 pairs | 14 | 18 |
| 剩餘合計 | **22** | **40** |

原 source indices 全保留：933 新排 98、99、126、132、141、146、
174、177、188、191；941 新排 135、136、195、203、216、223、283、
287、303、307。具名框架只是前序必要域，不提供 disk 實現、候選
完整 Σ 或 criticality。

18 張完整 degree 控制圖含 C 共鄰 singleton／不同接點 edge／
triangle、三種 unary 配對與 root 交換。所有实际附件在長包絡
1234，保存完整 C／U／V witnesses 與字面 frame；九份圖變體有
**1,620 完整 joints／25,920 pinned fibres／1,260 原邊接回／810
root 交換**，與獨立整圖回溯相同。U／V 的 66／90 份多色 contact
列分別核對式 (4)，保存 **680／1,012** 份逐原邊驗證的完整
替換 witness，unary 外所有原頂點保持；72／52 份 singleton
投影失敗列、C marginals 假允許及原邊接回阻塞保留。
這些圖不是 disk／候選／critical 來源，不以任意附件圖推定紙面
幾何。它們的原交錯路径只核對「同在此原長 face」的負控制。

## 6. 重播、停止點與下一窄入口

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_long_face.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_long_face.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_short_face.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

無參數只生成本輪新 artifact；`--check` 重算逐 byte 比對。
實際驗證範圍見本輪紀錄；沒有重跑舊全倉來源 catalogue、degree-6
全分拆、R 系列或 Lean axiom audit，沒有覆寫前序 artifacts。
`lake build` 不形式化本輪 crosscut／短支援合成。

**停止於同一長 face 的 (1,3,1) 窄排除，unequal pairs 剩22／40。**
下一具名入口為 941 原 spokes=01／03、indices=134／174；933 同
arc type 的原 spokes=01／13、indices=100／156，需對整圖做一次
共同 D₅ 搬運。01／03 的 critical U 必在共同 face、支援包含1、3；
V 必在原外 face、支援包含3、0。保留原 C／U／V、所有 actual
supports、共同色框、環序與完整六角色 joint，再研究原 C 的
位置及可否用同一原外路徑封成少數 hubs。這些位置限制只是下一
題入口，本輪不據此新增來源排除。

其他 (2,2) incidence、較少 spokes、單省略、原 (5,5) q-core、
多 mixed／no-mixed／非相鄰 roots 與 unary 側例外保留；ε≥3、
來源實現、一般出口及 K∞=K≤5 未證。本輪未 commit／push。
