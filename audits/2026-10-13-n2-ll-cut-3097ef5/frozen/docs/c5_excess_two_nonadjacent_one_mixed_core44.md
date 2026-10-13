# ε=2 非相鄰唯一 mixed：U3 的 incidence11 兩-root (4,4) 身份排除

**後續（2026-10-08，U4完成）。** [非相鄰兩mixed的U4](c5_excess_two_nonadjacent_two_mixed_core44.md)
現亦全排，固定完整Σ933／941下兩-root44身份全部完成。
下文保留本頁當輪停止點及後續紀錄；單-root例外、45／54／55與ε≥3仍保留。

**後續（2026-10-08）。** [mixed12／21](c5_excess_two_nonadjacent_mixed12_core44.md)
已由原star面／slack與六內點完整接回排除；連同E4的mixed22，U3兩-root44身份完成。
下文保留mixed11當輪範圍與驗證；單-root例外及其他core型仍保留。
§4的01202重色pair另有24，完整列表是{03,24}；原文只列覆蓋所需的03，
不影響五pair覆蓋或當輪證書。

2026-10-08。接續 [C44″ 的 U3](../artifacts/c5_excess_two_c44pp/REPORT.md#5-最小未覆蓋子分支清單)
及 [E4 的 N1 停止點](../artifacts/c5_excess_two_e4/REPORT.md#34-n1-的精確停止點)。
目前研究線與停止點見 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)。

**結論。** 在下列來源前提中，若 sole mixed C 的原 incidence 為 (1,1)，
則任何拒絕列都不能有保留兩 roots 的 (4,4) minimal core。
spoke／unit-unary 的全部省略身份及 root 交換均涵蓋。
這關閉 U3 的 mixed11 子型；mixed12／21、N1 單-root 刪除例外、
(4,5)/(5,4)、原 (5,5) core 與 U4 保留，沒有證成 ε≥3。

證據是任意大小紙面證明、沿用的外部 degree-list／Gallai 與 degree-4 分類，
加上固定原圖的 Python 完整關係控制。有限控制不負責任意大小覆蓋，未新增 Lean theorem。

## 1. 完整前提與原省略身份

G 是有限簡單圖，B=(b₀,…,b₄) 為指定有序 induced-C₅ disk 外框；
完整 Σ 是 933／941 或整圖 D₅ 像，每條非框邊 Σ-critical。
ε=2，兩個原 roots z,w 完整 degree 五且不相鄰，其餘有效內點完整 degree 四。
H=G−B 連通、碰齊五框點，T4 全收。C 是 H−{z,w} 唯一 mixed 原分量，
各 root 恰有一條接 C 的原邊，contacts 可為同一個原頂點。

取任一拒絕列的 minimal core M，假設 z,w 都在 M 中且自身 degree 都為四。
沿用 [原 degree-4 飽和與省略表](../artifacts/c5_excess_two_e3/nonadjacent_notes.md#5-每列-q-core-的完整原省略分類)：
M 保留整個 C 及全部原接點、內邊與框附件；每側恰省略一條原 spoke，
或整份 capacity-one 原 unary。C separating，不使用 one-sided mixed 盾弧。

以下分類依賴 [全 degree-4 合成](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)、
[樹核心](c5_tree_cores.md)、[單 triangle 無分叉](c5_triangle_forks.md)
與 [雙 triangle 直接 bridge](c5_two_triangle_blocks.md#1-範圍與結果)：
H_M 只有 path、單 triangle 加不分叉 path branches，或兩個頂點互斥 triangles
加一條直接 bridge，最大內部 degree 三。這是 M 自己的實際結構，沒有縮減原 contacts。

令 t_r 是原 root r 的 spoke 數。T4 迫 t_r≤3；mixed incidence 一給
原 unary incidence 總數 4−t_r≥1。因此每側至少有一份 unary。
[盾弧定理 A](c5_unary_shield_budget.md#3-定理-a全圖至多兩份-unary-分量)
給全圖 unary≤2，故恰有 U_z、U_w 各一份。記其原容量 k_r=4−t_r。

- 省略 U_r 時，必有 k_r=1、t_r=3；M 在 r 的內部 degree 為一。
- 省略 spoke 時，整份 U_r 保留；M 在 r 的內部 degree 為 k_r+1≤3，故 k_r∈{1,2}。

原來源只剩 (k_z,k_w)=(1,1)、(1,2)、(2,1)、(2,2)。
兩份 unary 的原盾弧長只能為 (2,2) 或 (2,3)，含交換；
全部原 root spokes 與 C support 都避開兩弧內點。

## 2. 兩側容量相等的身份

### 2.1 (1,1)：原三-spoke 星給 K₃,₃

兩 roots 各有三條原 spokes。盾弧 (2,3) 僅留兩個可用框點，不足三條不同 spokes。
盾弧 (2,2) 留三個框點 T，兩 roots 都接齊 T。
在 disk 外側加一個 apex α 接全部 B，子圖以 {z,w,α} 與 T 為兩岸，
有全部九條實際 K₃,₃ 邊。disk 外加 apex 應平面，矛盾。
這涵蓋 spoke／spoke、spoke／unit-unary、unit-unary／unit-unary，沒有改寫 C 的關係。

### 2.2 (2,2)：兩個原 root triangles 不能隔著 C

兩側都只能省略 spoke，U_z、U_w 均原樣保留。每側兩個 unary contacts
與其 root 形成 cycle；全 degree-4 分類迫它是原 triangle，兩份 triangles 互斥。
雙 triangle 分類不許 tails 或中間路徑，唯一外接 bridge 的端點必是 z,w，
因各 root 已用兩條 triangle 邊，第三條內邊就是其原 C 接點邊。
因此必須有原邊 zw，與 nonadjacent 及非空 C 矛盾。
沒有把原 z–C–w 路徑收縮成一條邊後再套分類。

## 3. 容量 (1,2)：固定原 star 的面與 C 路徑

root 交換給 (2,1)。設 k_z=1、k_w=2，則 t_z=3、t_w=2。
三個不同 z-spokes 迫兩盾弧均長二。對整張圖共同重標，可寫成

σ_z=b₀b₁b₂，σ_w=b₂b₃b₄，T={b₀,b₂,b₄}。

這只用來描述實際環序；完整 Σ、拒絕列、所有原附件及色框一起搬運，
不能把原三拒絕列在新標號下仍寫成固定位置。
原 spokes N_B(z)=T，actual S_Uz={b₀,b₁,b₂}、S_Uw={b₂,b₃,b₄}。

### 3.1 只把實際連通的 W 放進原 star face

令 W=C∪{w}∪U_w，含全部原內邊及 w-contact 邊。W 原連通，避開 z 及原 z-star。
因此它的頂點和附件的非框部分都落在 B 加 z-star 的同一個內面。
三個面沿 B 分別見 012、234、40；W 包含 U_w 的全部支援 234，
所以只能在 234 面。兩份 unary 的盾弧內點 1、3 禁止 C 及 roots 接觸，故

N_B(w)={b₂,b₄}，S_C⊆{b₂,b₄}。 (1)

這裡沒有聲稱 H−z 連通：原 U_z 會在刪 z 後分離。
使用的是同一原 W，沒有虛構避開 separating C 的 z–w 外路。

### 3.2 全部原 C 點都有同一對實際框附件

w 側的容量二 unary 不能省略，故 M 有包含 w 的原 triangle。
z 的 core 內部 degree 為一（省略 U_z）或二（省略 spoke）。後者的兩條邊
分別通向 unary U_z 和 C，不能形成通過 z 的 cycle。因此 z 不在任何 triangle 中。
雙 triangle 分類的六個內點都在 triangles 中，故 M 不可能有第二個 triangle。
單 triangle 無分叉分類使從 w 的唯一 C-contact 邊出發、通向 z 的枝是 path。
整份 C 由 saturation 保留，且沒有其他 root incidences，所以 C 就是 w–z 子路徑的非 root 點，
每點在原 H 的 degree 都為二。C 可以只有一點，此時兩 contacts 共用該點。

每個 C 點原完整 degree 四，故恰有兩個不同 actual 框附件。
配合 (1)，對所有 v∈C 有

N_B(v)={b₂,b₄}。 (2)

U_w 可以在 triangle 的另一點帶原 path tail，並不必是 K₂；
以下證明保留整份 U_w，無需分類或替換它的完整 relation。

## 4. 重色列的完整原圖延拓

先把完整來源搬運到 canonical 933／941 框，三個指定拒絕列是 01212、01202、01021；
其重色的非相鄰 pairs 分別是 {13,24}、{03}、{02,14}。
它們覆蓋全部五個非相鄰框 pair，整圖 D₅ 搬運後仍覆蓋。
故 (1) 的那對實際框點在某一個**仍被 G 拒絕**的 β 上同色。
原標號若正是 234，此條件寫成 β(b₂)=β(b₄)。

**List slack 貪婪引理。** 連通圖 K 的每點 list 大小至少 deg_K，
且某點嚴格大於 deg_K，則可染色。以該點為生成樹根，先染後代再染根；
每個非根點仍有未染 parent，根最後由 slack 留下一色。
這給全頂點的同框 coloring，沒有使用四色定理。

取原側 S_z=B+z+U_z 與 S_w=B+w+U_w，所有原邊、附件都保留。
兩 root 在各自側圖的完整 degree 都為四。
固定同一字面 β 後，在 K_z=G[{z}∪U_z]、K_w=G[{w}∪U_w] 上染色；
其非 root 點 lists 均至少各自的內部 degree。
z 的三 spokes 有兩端重色，root list 至少二色，嚴格多於側內部 degree 一；
w 的兩 spokes 重色，root list 至少三色，嚴格多於側內部 degree 二。
貪婪引理各給**整份原側**的 coloring；令取得的原 pins 為 a=f(z)、b=g(w)。

現在固定同一 β,a,b 接回全部原 C。由 (2)，每點的兩個框鄰點同色；
外鄰重複使

|L_C(v)|≥deg_C(v)+1。

此式也包含 path 兩端與單點 C 的兩個 root pins，無論 a=b 或 a≠b。
貪婪引理給原 C 全頂點的 coloring，與兩份側 coloring 同時拼回 G。
沒有 zw 不等式，不能刪除同色 root pair。
所得是 G 對拒絕 β 的完整延拓，矛盾；(1,2) 及 root 交換型全部排除。

這一步依靠同一實際 C 的完整 lift；沒有將兩個 contact marginals 相乘，
也沒有以收縮星或小 K₂ 染色冒充原長圖的染色。

## 5. 固定域控制、重播與界線

[Checker](../scripts/c5_excess_two_nonadjacent_one_mixed_core44.py) 及
[證書](../artifacts/c5_excess_two_nonadjacent_one_mixed_core44/observations.json)
控制整數容量／省略表、具名原盾弧與 K₃,₃ 實際邊、重色 pair 覆蓋及局部 slack。
原圖染色控制包含不同長度 C、unit-unary 路徑、U_w triangle 的額外 path tail、
shared／distinct C contacts 及 root 交換；保存實際邊集、ownership、所有附件、
完整 ordered contact tuples 與全圖 witnesses，包含全部空 root fibres。
同一 β 的原分量接合另與獨立全圖回溯比較。

[獨立 auditor](../scripts/c5_excess_two_nonadjacent_one_mixed_core44_audit.py) 不 import primary，
從 restricted-growth words 重建十列／D₅ masks，以暴力全 piece 染色及另一份全圖枚舉
重驗全部 720 relations、3,840 fibres、1,232 joint lifts 與全部原邊；
共有 352 非空／3,488 空 fibres。另核對 10 份 K₃,₃、84 slack、50 pair-mask cases
及來源 hashes，結果保存於 [獨立證書](../artifacts/c5_excess_two_nonadjacent_one_mixed_core44/independent_audit.json)。
這只驗固定控制，任意大小分類與原拓撲仍依上述紙面前提。

```sh
python3 scripts/c5_excess_two_nonadjacent_one_mixed_core44.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_nonadjacent_one_mixed_core44.py --check
python3 scripts/c5_excess_two_nonadjacent_one_mixed_core44_audit.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_nonadjacent_one_mixed_core44_audit.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
git diff --check
```

有限原圖只是新延拓步驟的控制，不聲稱是 disk、Σ-critical 或完整來源。
無界 C、U_z、U_w 的結論由 §§1–4 與明列上游依賴承擔。
本輪不重跑上游全部分類／topology 枚舉，不把 lake build 提升為新紙面形式化。
實際檢查、數字及未跑項見 [研究紀錄](history/2026-10-08-u3-one-mixed-core44.md)。

**精確停止點：U3 的 incidence11 兩-root44 身份全排。**
U3 incidence12／21、U4、N1 單-root 例外、其他 core 型、E5 新證明要求、
三列一般推廣、ε≥3、猜想 E 任意大小、一般出口與 K∞=K≤5 均保留。
