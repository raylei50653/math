# ε=2：t=1、(4,1) 的共同 active forest 與兩份固定原末端袋

2026-10-03。**933／941 固定完整 Σ、edge-minimal C₅ disk 來源，在
ε=2、唯一 degree-6 root、t=1 下，不可能有原接點分拆 (4,1)。**
此處排除整型來源；不把四接點分量當成 binary，不以「沒有全
degree-4 真子核心」代替整型反證。全部 t=1 接合見
[整批報告](c5_excess_two_single_spoke_complete.md)。

證明先以固定原支援及完整十列 profiles 得到 216 份放寬必要資料，
再以同一未用色 D 決定原 active forest。連通雙 triangle 型有原圖
K₅；兩原 bridge paths 型給两份固定、互不交且各只含一個原 contact
的末端袋，其實際支援不能在同一原 spoke 切口內並排。Python 核對
100 份來源必要查詢、8 份末端袋證書、1,280 份原圖 minors 及
134,400 份完整六接點接合；無新 Lean theorem。

## 1. 同一原圖與完整六接點

G 有限簡單，B=(b₀,…,b₄) 為指定有序 induced-C₅ disk 外框；
Σ(G) 為 933、941 或整圖 D₅ 像，接受全部 T4。每條非框邊 e 皆有
Σ(G−e)⊋Σ(G)。有效內部 H 連通，唯一 root r 完整 degree 六，其餘
內點完整 degree 四；r 有唯一原 spoke。H−r 的原分量 C、W 分別有
四個有序原接點 (x₀,x₁,x₂,x₃) 及原單接點 w。全部原分量、附件、
ownership、環序、嵌入及同一色框保持。

固定 proper boundary coloring b，原完整 relations 記為 R_C(b) 及
S_W(b)，接點 slack 保證皆非空。精確完整關係是

\[
\mathcal R_G(b)=\{(a,c_0,c_1,c_2,c_3,d):
 (c_0,c_1,c_2,c_3)\in R_C(b),\ d\in S_W(b),
 a\notin\{b_s,c_0,c_1,c_2,c_3,d\}\}.\tag{1}
\]

令 F_C=∩_{t∈R_C}set(t)，F_W=S_W 當 |S_W|=1，否則 F_W=∅。
式 (1) 的 root 投影恰為 U₄∖({b_s}∪F_C∪F_W)。這是原接合的
精確投影，未拆四個接點的 marginals。

[四接點三禁色 K₅](c5_no_spoke_exterior.md#5-多分量的三四接點分量也排除)
只需同一 C 的三份拒絕 palettes、內点完整 degree 四及 C 外連通 hub；
原 spoke 已提供 hub。因此任一 proper b 都有 **|F_C(b)|≤2**。
此局部引用不要求全圖在 b 是 minimal，也不用 no-spoke 圖的完整覆蓋。
拒絕列於是必滿足 |F_C|=2、|F_W|=1，且兩者與 spoke 色兩兩不交。

## 2. 同一 spoke 切口的十份支援包絡

每個原因子的 Σ-minimality 見證迫它在某 singleton 列有非空禁色。
來源碰齊五個框點，[短支援引理](c5_short_support_singleton.md) 的
外部原路徑因而存在；每份原分量的實際支援均不能包含於一條框邊。
沿[原 spoke 切口次序](c5_single_spoke_cores.md#3-任意大小的支援與嵌入限制)
共同搬運整圖，使 spoke 為 rb₀，切口上的原框次序為

\[
b_0,b_1,b_2,b_3,b_4,b_0.
\]

C、W 的全部接點各成一個原區塊，實際支援有同序最小包絡 I_C、I_W，
各跨度至少二、內部不交、總跨度至多五。兩份已排序整數區間只能為

\[
(02,24),\ (02,25),\ (02,35),\ (03,35),\ (13,35).\tag{2}
\]

其中例如 25 表示切口位置 [2,5]，其字面框點為 2,3,4,0。C、W
可按兩種次序擁有這兩份区間，共十份具名包絡。端點共用允許，
沒有把包絡內的稀疏位置新增為附件；每份跨度至多三，不會同時含
同一 b₀ 的兩個副本。

若兩列在一份包絡上的色列只差一個 S₄ 置換，沿該原分量完整染色
搬運就得到同一 F 的相應置換。Checker 為每個局部相等型只選一次
穩定子不變禁色集，C 容量至多二、W 容量至多一，全部十列共用它。
另外保留[同一原 unary 的 D 身份守恆](c5_excess_one_subcovers.md#4-單接點分量的跨列-d-身份不能互換)：
在各三色列 F_W 非空時，是否等於共同未用色 D=3 不能互換。

十份具名包絡乘候選十個 D₅ 像，共 100 份必要查詢。只用上述同源
限制及完整 Σ，92 份沒有完整 profiles；其餘 8 份共 216 份完整
profiles。在每份保留資料的**每個原拒絕列**，都有

\[
F_C(q)=\{D,a_q\},\qquad F_W(q)\ne\{D\}.\tag{3}
\]

這是有限必要域的輸出，不提前當作一般四接點定理。Checker 明留
non-D-pair guard：若某拒絕 pair 不含 D，就不適用後面的共同 D 論證；
216 份資料皆實際通過此 guard。

## 3. 全部拒絕列共用同一原 active forest

對同一 q 的 root=D、root=a_q 取兩份拒絕 degree lists 及 Gallai
block palettes。C 是 K₄-free，因原 spoke 使 B∪{r} 連通；外部
degree-list 及 palette 存在性沿用 [完整介面](c5_degree5_interfaces.md)。

只看 palette 中 D 的 membership。所有三色 q 的框點都不用 D，
所以在非接點，兩份 lists 對 D membership 相同；在每個原接點，
root=D 刪 D，root=a_q 留 D。[原 vertex–block incidence 矩陣 I 的
欄獨立性](c5_single_spoke_four.md#2-三組差異共用一個係數向量) 迫
唯一同一係數 τ，滿足

\[
I\tau=\mathbf1_P,\qquad
\mathbf1_{S_K^D}-\mathbf1_{S_K^{a_q}}
=\tau_K(\mathbf e_{a_q}-\mathbf e_D),\quad
\tau_K\in\{-1,0,1\}.\tag{4}
\]

I、P 不隨 q 改變，所以 τ、全部 active 原 blocks 及原 bridge paths
亦不隨 q 改變。不能只在每列各挑一份同構 active tree。

同頂點 active 正、負 palettes 各至多一份；active incidence forest
的葉點恰為四個原 contacts。若有 h 個非空分量，葉數公式為

\[
4=2h+\sum_{\text{active odd cycles }K}(|V(K)|-2).
\]

因此只有兩型：一棵連通樹含兩個 triangles、其餘皆原 bridges；或
兩條互不交的原 bridge paths，各有兩個原 contacts 作端點。第一型
包括兩 triangles 共一 cut vertex；不能漏掉此零長 connector。

## 4. 連通雙 triangle 型的原圖 K₅

連通型由兩 triangles、它們間的原 bridge path（可長度零）及四條
通往原 contacts 的原 bridge arms 組成；arm 可長度零，此時 triangle
頂點本身就是原 contact。

每個非 shared-cut 的 triangle 頂點都有兩條 cycle 邊及一條 arm、
connector 或 root-contact 邊，已用完整 degree 三。第四條原邊直達
B，或進入 inactive bridge 支路。所有 contacts 已在 active tree，
該支路無其他 contact，也不能返回另一 active 頂點，否則破壞原
block 結構。其原 tether 必碰 B：若不碰，刪其 bridge 後兩側 slack
可染，無 boundary／root 附件的支路可任意置換四色，便能拼回被
拒絕的原 lists。不同頂點的 tethers 內部互不相交，亦避開 active tree。
這使用 [既有實際 tether 論證](c5_single_spoke_three_one.md#3-每個-triangle-頂點的實際-boundary-tether)。

**兩 triangles 不交。** 取第一份 T={a,b,x}，a、b 通往兩個原
contacts，x 通過 connector 到第二 triangle。令 A、A′ 為 a、b
的完整原 arms；X={x}；Z 包含 r、connector 除 x 外的原部分、第二
triangle 及另外兩條 arms。O 包含 B 及 a、b、x 三條 tethers 除其
起點以外的原頂點。五組 A、A′、X、Z、O 非空、連通、兩兩不交：
前三組的 triangle 邊、它們各到 Z 的原 contact／connector 邊、
三份真實 tethers 及原 spoke r–O，給十對鄰接。

**兩 triangles 共 cut x。** 寫 T={a,b,x}、T′={c,d,x}。取 a、b
完整 arms 為 A、A′；X={x,c}；Z={r}∪d 的完整原 arm；O 包含 B
及 a、b、c 三條 tethers 除起點外的原頂點。c 的 arm 保留在來源，
此 minor 不使用它。A、A′、X 用 T 的三邊，A、A′ 各以原 contact
接 Z，X–Z 可用原 cd，A／A′／X 各有 tether 到 O，Z–O 是原 spoke。
再得 K₅。Gallai blocks 不能共邊，兩種情形已窮盡。

兩個構造都只反證平面性，不宣稱合併 boundary 後仍保持完整 Σ。
所以實際來源只可能落在兩原 bridge paths 型。

## 5. 兩份固定原末端袋與完整 rooted residual

兩條 active paths 各有兩個原 contacts。因其所有邊都是 C 的原
bridges，兩條 paths 在 C 內的唯一連接段各只碰一個路徑頂點；
若返回同一路徑另一點，就使某原 bridge 落在 cycle 上。

在每條 path 選遠離此 connector 的一個 contact 端點 x，切掉其
第一條 active bridge，令 V_x 為含 x 的原連通分量。所得兩份
V₀、V₁ 固定、互不交，各恰含一個原 contact；其餘原 contacts
都在被切邊的另一側。全部 inactive 旁支及實際 boundary 附件保留。
特別是**不使用含另一條 active path 的中央袋**。

固定 q，令 E_x(q) 是在 V_x 中、尚未扣 root 色及被切 active bridge
鄰色之前，x 的完整可延拓色集。V_x 只有 x 一個 r-contact，故固定
r=D 或 r=a_q，x 的色集分別正好是 E_x∖{D}、E_x∖{a_q}。

x 是 active leaf，式 (4) 使它的第一條原 bridge 為正，兩份 bridge
palettes 分別為 {a_q}、{D}。切橋兩側各有 slack、都可染；原 C
不可染迫兩端在兩份 lists 中各強迫同一 bridge 色。因此

\[
E_x(q)\setminus\{D\}=\{a_q\},\qquad
E_x(q)\setminus\{a_q\}=\{D\},\qquad
\boxed{E_x(q)=F_C(q)=\{D,a_q\}.}\tag{5}
\]

這是每份固定 V_x 的完整 rooted relation；没有把一般四接點 pair
當作 binary pair，也沒有忽略另一原 contact 對中央袋的影響。

令 T_x=N_B(V_x) 為實際支援。若 π 固定 q(T_x)，原完整 coloring
置換迫 πE_x(q)=E_x(q)；若 p|T_x=πq|T_x，则同一原 V_x 的完整
relation 迫 E_x(p)=πE_x(q)。每份候選支援因而須同時通過全部拒絕
列的穩定子及跨列換色，不逐列更换 T_x。

V₀、V₁ 各經自己的原 contact 邊接 r，且內部互不交。沿**原 spoke
切口**的 crosscut 次序，其支援在同一 I_C 內必有不交內部的原 lifts：
前一份 max≤後一份 min，或相反。I_C 長度至多三，位置由式 (2)
固定，不能改用繞過 spoke 的補弧來縮短某份支援。

## 6. 八份必要資料的固定支援族皆不能並排

下表用原框點列出 C 包絡及兩份 V_x 都必屬於的同一支援族。
同一列的支援族內任兩份（可相同）在該固定包絡中皆有重疊的開
框邊段，不能滿足 §5 的次序。每族非空，且包含整份 C 包絡；
排除來自兩份實際原袋同時存在，並非誤報空 relation。

| C 包絡 | W 包絡 | 完整目標 mask | 完整 profiles | 共同末端袋支援族 |
| --- | --- | ---: | ---: | --- |
| 012 | 2340 | 949 | 9 | 01、012 |
| 012 | 2340 | 950 | 9 | 01、012 |
| 2340 | 012 | 949 | 45 | 0234 |
| 2340 | 012 | 950 | 45 | 034、0234 |
| 0123 | 340 | 941 | 45 | 012、0123 |
| 0123 | 340 | 949 | 45 | 0123 |
| 340 | 0123 | 941 | 9 | 04、034 |
| 340 | 0123 | 949 | 9 | 04、034 |

支援集合例如 0234 在包絡 2340 中仍按 2,3,4,0 的**原線性次序**
取 hull，不把集合排序後的數字當成新嵌入。216 份完整 profiles
全部被這八份同源證書涵蓋，完成 (4,1) 整型來源排除。

## 7. 證書、重播與信任界線

[Checker](../scripts/c5_excess_two_four_one.py) 及
[artifact](../artifacts/c5_excess_two_four_one/observations.json) 保存全部
100 份支援／目標查詢、原 C／W ownership、局部 profile domains、
216 份完整十列資料 digest、8 份逐步支援族及其固定包絡位置。
支援集合統一使用 frozenset；另以全部 24 色置換的獨立定義重算
穩定子與跨列族，並強制整份 C 包絡留在每個最終族。正控制在
0123 包絡、q=01012、E={2,3} 下確實容許 01、23 兩份並排支援；
non-D-pair guard 則拒絕把不適用的資料送進共同 τ 論證。

1,280 份雙 triangle minor 控制涵蓋 shared cut、connector 長度
1／2／3、四條 arms 各長度 0／1、五個原 spoke 位置、直接／細分
tethers、共同／不同框末端。80 份代表保存全部原邊及五組十鄰接，
其餘由具名參數域及 digest 綁定；三個負控制拒絕缺 spoke、缺一組
必要鄰接及 branch-set 重疊。

完整六接點控制對全部 256 份 singleton 四接點 tuples 與 15 份
非空 unary domains，以及全部 32,640 份二 tuple 四接點 relations
與四種 unary singleton 色，逐 tuple 核對式 (1)、聯集恆等式、
root 投影及四種 spoke 色限制，共 134,400 次完整接合。這些抽象
relations 不宣稱 disk 實現；一般完整 R_C 的涵蓋由式 (1) 承擔。

```bash
python3 scripts/c5_excess_two_four_one.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_one.py --check
python3 scripts/c5_short_support_singleton.py --check
python3 scripts/c5_single_spoke_cross_row.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

任意大小、原 active forest、tethers 與平面 crosscut 由紙面論證承擔，
外部 degree-list 及前序無界引理沿用指定依賴。Python 不形式化拓撲，
`lake build` 亦不把本頁新論證升為 Lean theorem。本頁不處理其他
ε=2 root 型或一般來源；共同 ε 下界及全 t=1 範圍以整批報告為準。
