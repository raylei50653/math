# ε=2：t=1、(3,2) 的原 binary 路徑與同框排除

2026-10-03。接續 [三接點加兩 unary 排除](c5_excess_two_ternary_two_unary.md)
及 [短支援引理](c5_short_support_singleton.md)。目前總入口見
[Kempe 導覽](c5_kempe_guide.md)。

**933／941 固定完整 Σ、edge-minimal C₅ disk 來源，在 ε=2、唯一
degree-6 root、t=1 下，不可能有原分拆 `(3,2)`。** 三接點分量
的 singleton 禁色具有跨列 D 身份守恆；兩份原分量的共同支援弧
跨度均至少二。五個 slit 區間對、十份具名位置乘十個目標，共
100 queries，在同一原 binary 路徑塊的支援限制下全部排除。

只有局部 S4 profiles 與 D 守恆時仍有八份抽象殘留，不能省略
binary 路徑這一步。結論排除整型來源，不只排除 degree-4 子核心；
任意大小紙面論證與 Python 必要域證書均未新增 Lean theorem。

## 1. 原來源與完整六接點

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框。
有效內部 H 連通，唯一 root r 完整 degree 六，其餘內點完整
degree 四。唯一 spoke 是 rb_s；H−r 為原 binary A 與原 ternary C，
接點依序為 (x,y)、(u,v,w)。保留全部原邊、附件、ownership、
環序、嵌入及同一字面色框。

任一 proper b 下，兩份完整有序 relations R_A(b;x,y)、R_C(b;u,v,w)
均由接點 slack 貪婪引理非空。原圖完整接合為

\[
J_b=\{(a,c,d,e,f,g):(c,d)\in R_A(b),\ (e,f,g)\in R_C(b),
\quad a\notin\{b_s,c,d,e,f,g\}\}. \tag{1}
\]

令 F_W(b)=∩_{t∈R_W(b)}set(t)。式 (1) 的精確 root 投影為
\(U\setminus(\{b_s\}\cup F_A(b)\cup F_C(b))\)。二接點容量給
|F_A|≤2，而 [三接點兩禁色 K5](c5_excess_two_ternary_two_unary.md#2-三接點在所有列都至多禁一色)
給所有 proper b 都有 |F_C|≤1。F 只用於這個接合查詢；兩個原
relations 的有序 tuples 並未拆成 marginals。

## 2. 三接點的跨列 D 身份守恆

五個 singleton boundary rows 共用未用色 D=3。反設同一原 C 在
兩列 q,p 分別有 F_C(q)={D}、F_C(p)={a}，a≠D。固定 r=D 與
r=a 取得兩份不可著色 degree lists M_q、M_p，均處處 tight。
兩份 Gallai block palettes 記 S_K^q、S_K^p。原 spoke 使 C
K4-free，blocks 只有 bridges 及 odd cycles。

因 q、p 都不使用 D，在非接點兩份 lists 都含 D；在原接點，
M_q 不含 D 而 M_p 含 D。因此同一 vertex–block incidence
matrix I 與係數

\[
\delta_K=\mathbf1_{D\in S_K^p}-\mathbf1_{D\in S_K^q}\in\{-1,0,1\}
\]

滿足 **Iδ=1_P**，P={u,v,w} 是同一原三接點集合。每份 palettes
在每個頂點互斥，故同頂點至多一個正 active block、一個負 active
block。接點恰接一個正 block；非接點恰接零個，或一正一負。

active incidence forest 的葉恰為三個原接點；每個非空分量至少
兩葉，所以它連通。葉數公式迫恰有一個 triangle block，餘下
active blocks 都是 bridges：一個原 triangle 加三條原 bridge
arms，終點恰為 u,v,w。

每個 triangle 頂點已有兩條 triangle 邊及一條 arm／root-contact
邊，degree 四留下恰一條其他原邊。它若不直達 B，便進入不含
接點的 inactive 旁支。該旁支必有實際 boundary 附件，否則刪下
它後以 slack 染色，再把其全 U coloring 整體換色拼回，違反
M_q 不可著色。三條實際 tethers 因而存在，彼此內部不交。

取三個 triangle-arm branch sets、{r} 及 B 加三條 tethers；
原 triangle 邊、三條原 root-contact 邊、三份真實附件及唯一
spoke 給 K5，與 planarity 矛盾。這是
[原三接點 minor](c5_single_spoke_three_one.md#4-只有一條-spoke-的五個原圖-branch-sets)
的同一構造；此處只比較 D 的 membership，沒有假設其他色的
兩列 palettes 相同。因此

\[
\boxed{F_C(q),F_C(p)\ne\varnothing\ \Longrightarrow\
 (D\in F_C(q)\iff D\in F_C(p)).} \tag{2}
\]

這不要求整份 G 在 q 或 p 下 minimal，亦不要求 F_C 每列都非空。
非 D 色名可以變動；不能把式 (2) 加強為全部色名守恆。

## 3. 兩份原支援的跨度下界與真實端點

每份原分量有完整 Σ edge-minimality 提供的私有色見證，故其
F 至少在一列非空。原支援至少兩點的 tight-Gallai 證明沿用
[固定支援下界](c5_excess_two_ternary_two_unary.md#3-每份固定原支援至少兩點)：
ternary 有容量一；binary 若只碰一框點，任何非空禁色集在該
點色的 stabilizer 下不變且大小≤2，也只能是該已見色 singleton，
同一 tightness 及 K4-free Gallai 末端矛盾適用。

現在排除跨度一，即實際支援恰為某條框邊的兩端 {a,b}。來源
完整 Σ 為 933／941，使 G 碰齊全部五個框點。因此在 C 或 A
之外必有原 r–h 路徑，h∉{a,b}，其內點避開該短支援分量。

對 ternary，[短支援引理](c5_short_support_singleton.md)排除任何
已見色禁色。未見的兩色由 stabilizer 互換，容量一亦不能只禁
其中一色，故 F 全列皆空，與私有色見證矛盾。

對 binary，同引理排除已見色；唯一仍可能的非空 F 是未見二色
pair。既有 [雙禁色原 bridge 路徑](c5_single_spoke_frame_arc.md#1-來源前提與任意列的拒絕證書)
給至少兩個原路徑塊，每塊 residual 恰為這個 pair。其局部
stabilizer 迫每塊都實際接 a、b，否則固定只見一色的置換會
破壞二色 residual。避開 binary 的原 r–h 路徑與 a,b,h 三段
連通框弧，給 [frame-arc K5](c5_single_spoke_frame_arc.md#3-三段框弧與任意兩塊的-k5-引理)。
故 binary 亦不可能有非空 F，矛盾。

於是兩份原支援的共同相容 lifts 均有跨度至少二。共同 D₅ 搬運
使 spoke 為 rb₀，沿它切開 disk，框位置為 0,1,2,3,4,5，其中
0、5 同為原 b₀。**在同一 lift 內取每份實際支援的第一與最後
附件作端點**，得到最小 envelope；故 envelope 的兩端點確是
原附件，其內部點只作容許範圍，並非新增附件。

兩段按切口次序排列，全部區間對只有

\[
([0,2],[2,4]),\ ([0,2],[2,5]),\ ([0,2],[3,5]),\
([0,3],[3,5]),\ ([1,3],[3,5]). \tag{3}
\]

A、C 的兩種具名位置均保留，共十份幾何必要配置。

## 4. 同一原 binary 路徑塊的跨列支援

對所有 |F_A(b)|=2 的列，兩份拒絕 lists 迫同一原 x–y 奇數
bridge 路徑 P。它是原圖唯一 x–y 路徑，故不同列不能改選 P。
刪 P 邊後的原路徑塊 W_j 亦相同；T_j 是 W_j 的全部實際框支援，
包含路徑點自己的附件，且 T_j 包含於 A 的 envelope I_A。

[逐塊 residual](c5_single_spoke_frame_arc.md#2-任意列的逐塊-residual-穩定子)
及 [跨列搬運](c5_single_spoke_cross_row.md#2-跨列-residual-換色引理)給：

1. 固定 b(T_j) 的每個色置換都保持 F_A(b)；
2. 若 b′|_{T_j}=π∘b|_{T_j}，則 F_A(b′)=πF_A(b)。

只在兩列 F 都是 pair 時加入第二式。沒有對齊置換時不產生
限制；singleton 列不套此 residual 公式。

Checker 在 T⊆I_A 的全部子集上核對所有 24 色置換，建立同時
適用於已選雙禁色列的容許族 𝒯。這包含每個真實 T_j。另一
ternary 可能稀疏；外部 anchors **只使用原 spoke 及它的兩個
真實 envelope 端點**，記 O₀={b₀}∪{C 的兩端点}。

若存在同一份連通兩框弧分割 B=X⊔Y，使 O₀ 碰兩側且每個
T∈𝒯 都碰兩側，[兩框弧 K5](c5_single_spoke_two_arc.md#2-兩框弧與另一原分量納入-z)
適用。其 Z branch set 包含 r、除選定相鄰兩塊外的原 P，以及
整份原 ternary C。此構造只要求另一分量連通且由原邊接 r，
不要求它是 binary 或 r degree 五，故本題仍成立。

空 𝒯 直接矛盾；若所有 T 共有兩個框點且 O₀ 有第三點，也可
用原三框弧引理。實際本輪搜尋的全部拓撲刪除都是兩框弧型，
沒有以 envelope 內部虛構 Z 的外部附件。

## 5. 十列共同 CSP 與有限結果

每份原分量在同一 envelope 上的局部 equality pattern 決定
其 F 的 S4 搬運；空／至多二色或空／singleton 選項必對該列
局部 stabilizer 不變。這是 [同框 profile 放寬](c5_excess_two_ternary_two_unary.md#5-同一原分量跨列的-s4-profile)，
允許依賴整條 envelope，只會擴大真正稀疏支援的必要域。

對式 (3) 的十份具名配置及兩候選十個 D₅ 像，逐列加入：
完整 root 接合式 (1)、共同局部 profile、式 (2) 的 ternary D
身份，以及 §4 的同一原 binary 路徑支援。DFS 保留所有尚未
排除的選項，不只檢查第一份 profile witness。

**100 queries 全部無解。** 搜尋共 174 個節點，核出 38 次
共同局部 profile 衝突、8 次 ternary D 身份衝突及 90 次共同
兩框弧 K5。這些是搜尋次數，不是來源圖數。

若停用 binary 路徑條件，仍有八份 941 軌道抽象 profiles；證書
完整保存它們作界線控制。它們符合前述必要色集合條件，並沒有
聲稱可由同一 disk 圖實現。這也避免把 D 守恆誤報為獨自完成排除。

## 6. 完整關係控制與重播

[Checker](../scripts/c5_excess_two_ternary_binary.py)及
[artifact](../artifacts/c5_excess_two_ternary_binary/observations.json)保存
100 queries 的具名 envelope、原分量次序、各 equality class 的
literal 色集選項、逐列候選數、搜尋次序，以及每個使用的實際
路徑塊支援族／共同框弧 witness。原路徑支援 helpers 的結果另用
直接 24 置換核對；輸入程式 SHA256 綁定所沿用的有限運算。

完整六接點代數另保存 972-tuple star 算子，核對所有 16 個
binary ordered tuples、64 個 ternary ordered tuples及四個
spoke 色，共 4,096 次 singleton-pair 接合。另測全部 120×2,016
對二元素完整 relations，共 241,920 次接合及 967,680 次 spoke
限制。每次都與獨立 Cartesian-product 定義比對，包含非 Cartesian
relations；一般原 R_A、R_C 的涵蓋由逐 ordered-tuple 的 union
恆等式負責。抽象 tuples 不是來源 realizability witnesses。

```bash
python3 scripts/c5_excess_two_ternary_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_ternary_binary.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_cross_row.py --check
python3 scripts/c5_single_spoke_two_arc.py --check
```

本頁只排除 `(3,2)` 整型。四接點分量的二禁色不等於原 binary，
因此不得把本頁路徑塊論證直接套到 `(4,1)`；其他來源分支依各自
報告判定。共同 ε≥2、一般來源／出口及 K∞=K≤5 的界線不變。
