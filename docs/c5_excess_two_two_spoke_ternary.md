# ε=2：t=2、(3,1) 復用 singleton profile 的整型排除

2026-10-03。接續 [t=1 三接點加兩 unary](c5_excess_two_ternary_two_unary.md)、
[t=1 ternary／binary](c5_excess_two_ternary_binary.md)及
[短支援引理](c5_short_support_singleton.md)。總入口見
[Kempe 導覽](c5_kempe_guide.md)。

**933／941 固定完整 Σ、edge-minimal induced-C₅ disk 來源，在 ε=2、
唯一 degree-6 root、t=2 下，不可能有原分拆 `(3,1)`。** t=1 的
三接點容量至多一及同框 singleton profiles 都可直接復用。两條原
spokes 增加共同 sector 限制；短支援引理使兩份原分量的實際支援
跨度各至少二。全部 16 份具名必要位置、107,296 份十列 profile
對，沒有一份得到 933／941 的十個 D₅ 像。

本頁排除整份 `(3,1)` 來源，不只排除某個省略核心。任意大小紙面
論證與 Python 必要域空性均保留自己的界線；沒有來源圖枚舉、disk
實現性分類或新 Lean theorem。共同 ε≥2、一般來源及 K∞=K≤5 不變。

## 1. 同一原圖與完整七接點接合

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框，有效
內部 H 連通。r 在完整 G 中 degree 六，其餘內點完整 degree 四。
r 的兩條原 spokes 為 rb_s、rb_t，s≠t；H−r 恰有原 ternary C 及
原 unary U，原有序接點為 (x,y,z)、u。全部原邊、附件、實際支援、
ownership、環序及同一嵌入保持。

固定同一字面 boundary row b，原完整 relations R_C(b;x,y,z) 與
S_U(b;u) 由接點 slack 的逆序生成樹貪婪法皆非空。完整接合恰為

\[
J_b=\{(a,b_s,b_t,c,d,e,f):(c,d,e)\in R_C(b),\ f\in S_U(b),
\quad a\notin\{b_s,b_t,c,d,e,f\}\}. \tag{1}
\]

三個 C 座標一直共同取自同一份原 tuple；兩個 spoke 色也是同一 b
的原座標。記 F_C(b)=∩_{p∈R_C(b)}set(p)，而 F_U(b)=S_U(b) 若
S_U(b) 是 singleton，否則 F_U(b)=∅。式 (1) 的精確 root 投影為

\[
\operatorname{proj}_r J_b=U_4\setminus
\bigl(\{b_s,b_t\}\cup F_C(b)\cup F_U(b)\bigr). \tag{2}
\]

此投影只用於原 root 的同色接合；F 不代替完整 relations，也不將
ternary marginals 相乘。兩份原分量的內部染色以同一 boundary b
獨立存在，才使式 (2) 成立。

## 2. 復用 t=1 的容量與固定支援下界

[三接點容量論證](c5_excess_two_ternary_two_unary.md#2-三接點在所有列都至多禁一色)
只用 C 有三個原接點、內點完整 degree 四、原 root 至少一條 spoke，
以及同一 C 的兩份被拒絕 degree lists。它不使用 root 的完整 degree
五或六、spoke 恰一條、另一原分量個數，亦不要求整份 G 在該列
minimal。因此原 active triangle／三臂、三份實際 tethers 及 root
與連通 B 的五個 branch sets 在本題仍給 K₅，得到

\[
|F_C(b)|\le1\quad\text{對每個 proper boundary row }b. \tag{3}
\]

Unary 的 F_U 本來就至多一色。四個原因子因而是兩條原 spokes、
原 C、原 U，每份最多禁一色；若某列被拒絕，四份必恰禁四個不同色。

完整 Σ edge-minimality 給每份原分量私有色見證：取該分量的一條
原 contact 邊，刪邊後的新接受列及 root 色在原圖被該分量禁止，
卻可避開其他原因子。因此 C、U 的 F 各至少在一列非空。
固定 933／941 來源碰齊五個框點；若某份原分量的實際支援包含於
相鄰兩框點，另有原 r–外部框點路徑避開它。
[短支援引理](c5_short_support_singleton.md#5-固定原來源的跨度推論)
遂使該分量每列 F 都空，矛盾。所以同一來源兩份原支援都滿足

\[
\ell_C\ge2,\qquad\ell_U\ge2. \tag{4}
\]

相加的是兩份固定原支援的跨度，不是不同列的負載。t=1 的 ternary
D 身份守恆亦只需至少一條 spoke，故可以搬來；本頁搜尋在加入它
之前已無解，所以沒有把它作為新增排除前提。

## 3. 兩條原 spokes 與同一份支援 envelope

對整份來源共同作一次 D₅ 搬運，使第一條 spoke 為 rb₀，第二條為
rb_j，j∈{1,2,3,4}；完整 Σ 同時搬到兩候選的某個 D₅ 像。沒有
獨立搬運原分量或重新正規化各分量的色框。

沿原 rb₀ 切開 disk，框位置依次為 0,1,2,3,4,5，其中 0、5 均為
原 b₀。第二條原 spoke 在位置 j，將 disk 分為 [0,j]、[j,5] 兩個
sector。原 C、U 連通且都避開 r 及兩條 spokes，故每份完整分量
只能位於其中一個 sector 的閉包；附件可位於 sector 端點。

沿此共同切口，對每份原實際支援取第一、最後附件為 envelope 端點。
端點是真實原附件，envelope 內部只作容許支援範圍，沒有新增邊。
兩份分量的共同相容 lifts 依切口排列，得到 [a,b]、[c,d]，
0≤a<b≤c<d≤5，兩段跨度由式 (4) 均至少二，而且不得跨越 j。
必要區間表為：

| 第二 spoke j | 依切口排序的 envelope 對 |
| --- | --- |
| 1 | ([1,3],[3,5]) |
| 2 | ([0,2],[2,4])、([0,2],[2,5])、([0,2],[3,5]) |
| 3 | ([0,2],[3,5])、([0,3],[3,5])、([1,3],[3,5]) |
| 4 | ([0,2],[2,4]) |

每對保留 C、U 的兩種具名 ownership，共八對區間、16 placements。
j=1、4 時，長度一的 sector 容不下任何原分量，另一 sector 恰用
兩份跨度二；j=2、3 時，任何一個 sector 都容不下兩份跨度二，所以
兩份必各占一個。其他原 root-contact 邊的接線限制沒有被拿掉原圖；
有限必要域只忽略它們能增加的幾何限制，因而仍包含全部真實來源。

## 4. 原同框 singleton profile 直接復用

對固定原分量 W 及上述 envelope I，若兩列在 I 上有同一 equality
pattern，便有全域色置換 π 把其字面色序列對齐。π 同時搬運所有
實際附件色，因而原完整 relation 給 F_W(b′)=πF_W(b)。F_W(b) 也
必對固定 b(I) 的所有色置換不變。

配合式 (3)，每個 local equality class 可選空集或 singleton：I 只
見一、兩色時，非空選項只能是已見色；至少見三色時，四個 literal
singletons 都保留。每份 profile 至少一列非空由私有色見證保證。
跨列 transports 保持同一字面色框，未見色的 permutation completion
由 stabilizer 條件保證無歧義。

Checker **直接匯入 t=1 的 `profile_domain`**，不建立另一份對三接點
特設的近似。它允許 F 依賴整條 envelope，較真正的稀疏支援更寬，
因此不能漏掉原來源。對 16 placements 的全部 profile 對，以式 (2)
重建十列完整接受 mask。107,296 次比較沒有任何 mask 屬於

\[
\{933,934,940,948,996\}\cup\{941,949,950,998,1004\}. \tag{5}
\]

沒有加入 ternary D 守恆、degree-list 實現限制或額外 minor screen。
必要域已空，故本題整份 `(3,1)` 型排除。

## 5. 完整有序關係控制與固定證書

[Checker](../scripts/c5_excess_two_two_spoke_ternary.py)與
[artifact](../artifacts/c5_excess_two_two_spoke_ternary/observations.json)保存
兩條具名 spokes、八對 sector 區間、16 份 C／U ownership、全部局部
equality classes、代表字面色、24 置換驗證與 transports、完整十列
profile codes、每份完整 Σ histogram、profile 索引見證及比較 digest。
這些 profiles 是必要禁色資訊，不宣稱是原來源 relations。

獨立完整 relation 控制保留七個有序座標
(r,b_s,b_t,C_x,C_y,C_z,U_u)。2916-tuple star 算子與直接 Cartesian
定義比對：全部 64 個 ternary tuples、15 個非空 unary domains 及
16 對 literal spoke 色，共 15,360 次 singleton relation 接合；全部
2016 個二元素 ternary relations 接同一批 unary domains／spoke 色，
共 483,840 次完整接合。每次核對完整 tuples 及式 (2)，另保存一份
非 Cartesian ternary relation，明列被 marginals 乘積虛構的 tuples。

任意原 R_C 的涵蓋由逐 tuple union 恆等式負責，不枚舉全部非空
ternary relations。兩條 spokes 的 abstract 色對包含相同色作控制；
實際 proper boundary row 自行決定它們能否同色。這些代數控制
不是 disk realizability witnesses。

```bash
python3 scripts/c5_excess_two_two_spoke_ternary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_two_spoke_ternary.py --check
```

本頁只排除 t=2、`(3,1)`。t=2 的 `(2,2)` 及 `(4)` 仍由各自
報告判定；不能把三接點容量一直接搬成四接點容量一。紙面 topology、
外部 Gallai 依賴、Python 必要域及 Lean 狀態依舊分開。
