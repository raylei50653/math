# ε=2 四-spoke (2,2)：共用原 spoke-pair 的 sealed mixed 排除

**後續（2026-10-03；2026-10-04 整理）**：本頁當輪排除共用 pair
7／9 份，留下 unequal 40／66；後續[短 face](c5_excess_two_mixed_core_four_spoke_short_face.md)
排8／16份至32／50、[同一長 face](c5_excess_two_mixed_core_four_spoke_long_face.md)
再排10／10份至22／40，其後 crosscut、短框弧及[不相交pairs總報告](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md)
完成四-spoke (2,2)、mixed-(1,1) 加各側一原 unary 子型，最後殘留0／0。
以下保留原輪次數字、停止點與證書；其他 incidence 及 ε≥3 仍未證。
現況與排程由 [Kempe 導覽](c5_kempe_guide.md)維護。

2026-10-03，接手基準 `b63a096`，保留前序未提交工作樹。接續
[原四接點 leaf-slack](c5_excess_two_mixed_core_four_spoke_quaternary.md)之後的
(2,2)、mixed-(1,1) 加各側一原單接點 unary。研究現況由
[Kempe 導覽](c5_kempe_guide.md)維護；實際驗證與貼用摘要見
[本輪紀錄](history/2026-10-03-excess-two-four-spoke-equal-pair.md)。

**新窄結論：固定完整 Σ=933／941 的下列原來源，若兩側兩條 spokes
接到同一對原框點，則來源不存在，含 root 交換。** 使用者指定的
原 a=5、b=6、兩側 spokes=01 入口已排除；同一論證亦覆蓋原框點
不相鄰的共用 pair。原 mixed 必封在同一原三角區域，固定三角形
的合法染色可延拓整份原 C；原 G−C 已全收，所以 G 也必全收，矛盾。

933／941 的原 (2,2) 必要框架分別有 47／75 份，本頁排除共用
pair 的 **7／9 份，仍保留 unequal pair 的 40／66 份**。這是原
子型的必要化約，未完成整份 (2,2)、mixed-(1,1) 加各側一 unary。
任意大小結論是紙面 Jordan／degree-list／既有三-hub 引理的合成，
Python 核對固定框架、完整 relations 及 witnesses；**ε≥3 未證，
沒有新增 Lean theorem。**

## 1. 同一原來源、原身份與完整六點 joint

G 有限簡單，B=(b₀,…,b₄) 為指定有序 induced-C₅ disk 外框；完整
Σ 是 933、941 或其整圖 D₅ 像，每條非框邊刪除均嚴格擴大 Σ。
有效內部 H 連通，ε=2，恰兩個完整 degree-5 roots a,b，其餘有效
內點完整 degree 四。原 ab 存在；H−{a,b} 恰有原 mixed C 及
原 unary U、V。C 的有序 contacts=(x,y)，owners=(a,b)，
incidence=(1,1)；U 只以原 au 接 a，V 只以原 bv 接 b。
兩側各兩條 spokes，故 ab、各一 mixed incidence、各一 unary
incidence 與兩條 spokes 正好耗盡兩側完整 degree 五。

x=y 時仍是同一原頂點，不複製 contact。保存原 C／U／V 的全部
內邊、實際 attachments／supports、bridges、旁支、ownership、
原嵌入環序及同一字面四色框。令 Sₐ、Sᵦ 是原 spoke 支援，
Aᵣ(β)=U₄−β(Sᵣ)，原完整 relations 記 R_C(β;x,y)、
R_U(β;u)、R_V(β;v)。精確 joint 為

\[
\begin{split}
J_G(β)=\{(A,D,X,Y,T,W):\;&(X,Y)\in R_C(β),\ T\in R_U(β),\ W\in R_V(β),\\
&A\in A_a(β),\ D\in A_b(β),\\
&A\ne D,X,T,\quad D\ne Y,W\}. \tag{1}
\end{split}
\]

每份 tuple 的存在量詞由原 C、U、V 各自的整份 coloring 承擔；
固定 B 與 roots 後才能接合。不能將 R_C 的兩個 marginals 相乘。
固定每個字面 (A,D) 後保留整個 (X,Y,T,W) 纖維，含空纖維。
省略 ab 只去掉同一 joint 的 A≠D；省略一條原 spoke只放寬其
原 root 的 boundary guard，接回時在同一 tuple 上恢復該色限制。

## 2. 共用 pair 的原 diamond 把 C 封入一個三角形

本節假設 Sₐ=Sᵦ={h,k}，h≠k，不要求 h,k 相鄰。只取同一原圖
的五條邊 ab、ab_h、bb_h、ab_k、bb_k。兩條原 h–k 簡單弧

\[
b_h-a-b_k,\qquad b_h-b-b_k
\]

只有原端點相交，其餘都在 disk 內。由 Jordan crosscut 性質，
這兩條弧將原 disk 分為 a 外側、兩弧之間及 b 外側三個區域。
兩個外側區域各只在 closure 中含一個 root；中間區域邊界是
原四環 b_h–a–b_k–b–b_h，其內沒有其他原框點。
原 ab 的內部避開其他原邊，只能位於中間區域，將其切成

\[
T_h=(a,b,b_h),\qquad T_k=(a,b,b_k). \tag{2}
\]

原 C 非空連通、避開 roots 與 B，且原 ax、by 同時存在。因此
C 及兩條 contact edges 的內部位於 skeleton 的同一 face；這份
face 的 closure 必同時含 a,b，只可能是式 (2) 的其中一個。
對某個**固定原** t∈{h,k}，整份 C 便封在原 T_t 中，故

\[
N_B(C)\subseteq\{b_t\},\qquad N_G(C)\setminus C\subseteq\{a,b,b_t\}. \tag{3}
\]

這裡不能把兩份三角形的支援合併成 {h,k}，也不能每列另選 t。
原 U、V 可在其他區域，無須改動或縮成 boundary spokes。
本節同時涵蓋共鄰 x=y 與不同接點 x≠y；所有原路徑與附件保持。

固定控制另窮盡 diamond 的 cyclic rotations：十份具名 pair、
root 交換共 80 份 rotation assignments，恰 40 份 spherical rotations，
每份均有兩個原三角 face 及一個四環 face。原 B 的兩段框弧在
disk 外框條件下位於兩個外側區域；不能因 diamond 的四環 face
也含兩 roots，就把 C 放到外框之外。前序 apex skeleton 的實際
rotation 亦逐份核對，兩-root faces 正好為式 (2)。這些是有限
rotation 控制；任意原嵌入 soundness 由上述 crosscut 證明承擔。

## 3. 原三-hub 延拓：完整 C 不阻斷任何合法原三角染色

固定任一 β 及原 T_t 的合法三色染色 a=A、b=D、b_t=β_t；三色
互異。C 的 exact lists 是

\[
L(v)=U_4\setminus\bigl(β(N_B(v))
\cup(\{A\}\text{ if }v=x\text{ else }\varnothing)
\cup(\{D\}\text{ if }v=y\text{ else }\varnothing)\bigr). \tag{4}
\]

x=y 時兩份 root guards 同時作用在同一原點。因每點完整 degree
四，|L(v)|≥deg_C(v)。若原 C 不可著色，連通 slack-list 貪婪法
迫全部 lists tight；degree-list 刻畫使 C 為 Gallai tree。
外部依賴為 [Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本輪已核對 degree assignment、tightness 與 blockwise-uniform 前提。

先核對原 C 的 K₄-free 前提，而非假設整份 G 是 q-minimal。
若有原 K₄ block，每個 clique 點恰有一個外接方向，直達原
連通 hub X={a,b,b_t}，或經一條原 bridge 離開該 block。
刪 bridge 後兩側 endpoint 均有 list slack，故兩側都能染色。
原拒絕迫兩側 root domains 是同一 singleton；外側若不碰 X，
可任意置換四色，無法只有一色。因此每個 clique 點都有一條
內部互斥、抵達 X 的原路徑。合併 X 與這四條路徑的外部部分，
加四個原 clique singletons，得到 K₅ minor，與 planarity 矛盾。
這正是 [連通外框 K₄ 引理](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
的局部證明；這裡 X 是原三角形，不需唯一 degree-5 root 或
全圖 q-minimality。

現已逐項滿足 [三-hub Gallai 引理](c5_short_support_singleton.md#4-三-hub-引理排除未見色接點數不設上限)：
C 非空連通、K₄-free Gallai、每點完整 degree 四，外鄰只在三個
兩兩相鄰且固定異色的原 hubs a,b,b_t。若拒絕，該紙面引理的
末端 odd-cycle／bridge 分支給原 K₅ minor；原 G planar，矛盾。
因此對每個符合原三角 guards 的 (A,D)，必有

\[
\exists(X,Y)\in R_C(β):\quad X\ne A,\ Y\ne D. \tag{5}
\]

式 (5) 保留同一完整 R_C 的整份 witness；不是兩個接點各自有
可用色，也不把無界 C 換成有限 skeleton。沒有使用四色定理 oracle。

## 4. 接回同一原 U／V：G 必全收，排除具名來源

沿用 [省略原 mixed 必全收](c5_excess_two_mixed_omission.md)，其全部
前提正是 §1，故 Σ(G−C)=Ω。固定任一原 G−C 的完整 coloring，
保存它的原 (a,b,u,v) tuple 及 U／V witnesses。原 ab 使 A≠D，
兩側共用 spokes 使 A,D≠β_t；原 T_t 已是合法三色三角形。
式 (5) 選到原 C 的一份完整 coloring，與該 tuple 在同一 B 色框
接合，滿足原 ax、by，得到原 G 的完整 coloring。

對每列其實得到忘 C contacts 後的四角色完整 relation 等式

\[
\pi_{a,b,u,v}J_G(β)=J_{G-C}(β),\qquad
\boxed{\Sigma(G)=\Sigma(G-C)=\Omega.} \tag{6}
\]

右至左由原 C 的整份 witness 承擔，左至右是原圖限制。原 G 的
Σ=933／941 與式 (6) 矛盾，完成共用 pair 子框架的任意大小來源排除。
整份 (2,2) 不因此完成；unequal pairs 的 C 可碰較大的原框弧，
式 (3) 的單框點前提尚未取得。

## 5. 固定必要域、完整 degree 圖與證書

[Checker](../scripts/c5_excess_two_mixed_core_four_spoke_equal_pair.py)／
[joint helper](../scripts/c5_excess_two_four_spoke_equal_pair_joint_controls.py)／
[artifact](../artifacts/c5_excess_two_mixed_core_four_spoke_equal_pair/observations.json)
只沿用原 single-spoke 證書的具名 skeletons，沒有重開來源圖枚舉：

| 固定 (2,2) necessary skeletons | 933 | 941 |
| --- | ---: | ---: |
| 原具名框架 | 47 | 75 |
| 共用 pair 排除 | **7** | **9** |
| unequal pair 仍保留 | **40** | **66** |

被排者是兩側相同的 01、02、04、12、13、23、34；941 另有 03、14。
兩候選原 01／01 的 source indices 是 96／132。保存原 root order、
retained edges、apex rotations 及未排框架，另有 16 次原骨架 root
交換與 1,600 次整體 D₅／列搬運；不為各分量獨立正規化。

三-hub 既有數學 payload 原樣唯讀重算相等：1,201 份接線、28 份
拒絕及其 K₅ bags／十條鄰接。另將這 28 份接線按原 sealing t=0／1
及 root 交換展開為 112 份原 C₅ minor 控制，逐邊核對。
它們核對一般三-hub 拒絕機制，**不是 incidence-(1,1) 完整 degree-5
來源**，沒有以這些 skeletons 代替任意大小證明或判定來源實現。

另有 **36 張完整 degree 圖**：六份手列 C（shared singleton／triangle、
不同接點 edge／triangle／square、path 中點 contact）×三份原 U／V
形狀配對×root 交換。a,b degree 五，全部原 C／U／V 點 degree 四；
每張保存實際全部附件、全部十列原 relations 與整份 witnesses。
G、G−ab、四份原單 spoke 省略及 G−C 共七種原圖各自直接回溯：
**2,520** 完整 joints、**40,320** pinned fibres（含空纖維）、
**1,800** 原邊接回等式及 **1,260** 完整 root 交換核對通過。
G−C 的 ports 是 (a,b,u,v)；其餘保存完整 (a,b,x,y,u,v) 六角色，
共享 contact 仍只用一個原頂點。另保留 marginals 假允許／完整 C
guard 空的反例，以及原省略 spoke joint 非空、接回原圖全濾空的見證。

這些完整 degree 圖只核對式 (1) 與原邊恢復，**沒有宣稱 disk、
候選 Σ、Σ-critical 或式 (3) 的封閉幾何**；因此不以它們核對式 (6)
的任意大小結論。固定 degree 圖與未補齊 root degree 的 minor 控制
分開記錄。前序 artifact 保留，新層明存原 single-spoke 文件 hash 漂移。

## 6. 重播與停止點

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_equal_pair.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_equal_pair.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

無參數只寫新層；`--check` 重算逐 byte 比對。實際執行及未重播範圍
見本輪紀錄。原 G−C 全收與舊 K₄ 任意大小引理沿用既有紙面成果，
本輪沒有重新跑其全部歷史證書；外部 degree-list 文獻已重新核對。
`lake build` 不形式化本頁 Jordan／Gallai／minor 合成，沒有新 Lean theorem。

**停止於選定 (2,2)、mixed-(1,1) 加各側一 unary 的共用 pair 窄排除，
含原 01／01 與 root 交換。** 仍有 40／66 份 unequal-pair 必要框架。
下一具名入口為原 a=5、b=6、spokes=01／02，原 source indices=97／133；
root 交換為 111／153。保持原 C／U／V、actual supports、所有原邊、
環序及同一六點 joint，先分析原 C 所在 face 的實際支援包絡。
本輪不分析這個新入口、不 commit／push。

其他 (2,2) incidence、較少 spokes、原 unary 單省略、原 (5,5) q-core、
多 mixed／no-mixed／非相鄰 roots 及 unary 側例外仍保留。
共同 ε≥2 不變；ε≥3、來源實現、一般出口與 K∞=K≤5 均未證。
