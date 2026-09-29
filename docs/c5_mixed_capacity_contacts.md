# Mixed 原分量：逐欄容量、十八種側型與最小三點介面

後續（2026-09-29）：[P₃ 對稱分支](c5_mixed_p3_symmetric.md)已證原五環
內側為空，以兩份完整側支援與三份 P₃ 星狀附件的五跨度排除指定 disk
來源；不需 T4／Gallai，不限制 unary 大小。僅涵蓋兩端各一 incidence、
E_z=E_w 為同一 pair；原非平面控制與下文當輪數字保留，其他分支未完成。

2026-09-29，Git 基準 `773cdf8`。接續
[完整有序色對介面](c5_adjacent_degree5_interfaces.md)，推進
[no-mixed 共同分離](c5_no_mixed_growth_completion.md)之後的 mixed 缺口。
**只要有 mixed 原分量，source 每側 unary 禁色互不重疊，容量缺額至多一；
各一 root incidence 的任意大小 mixed 分量至多禁止兩個有序色對。**
前兩項有不依支援表、不依 planarity 或 Gallai 的初等紙面證明。

最小尚未處理的原分量有三個點，只可能 P₃ 或 triangle。新
[checker](../scripts/c5_mixed_capacity_contacts.py)／
[證書](../artifacts/c5_mixed_capacity_contacts/observations.json)另窮盡它們的
固定 q 色角色及完整逐邊接合：唯一 mixed P₃ 的必要 incidence 數只剩
(1,1)、(1,2)、(2,1)；triangle 再容許 (2,2)。這部分是**有限完整域控制**，
不是任意大分量縮到三點的定理，也不是 actual-support／disk 分類。

本輪未新增 target 分離、來源 disk 排除、Lean theorem 或出口類別。
實際驗證見[研究紀錄](history/2026-09-29-mixed-capacity-contacts.md)，
目前停止點由[weak-deletion 導覽](c5_weak_deletion_guide.md)維護。

## 1. 前提與保留的完整介面

M 有限簡單，B=(b0,…,b4) 為 induced C5，H=M−B 非空連通。
q=01012、U={0,1,2,3}；M 拒絕 q，刪任一非框邊後接受 q。
有序相鄰 roots z,w 的完整 degree=5，其餘內點完整 degree=4。
若來源有 disk embedding，保存原環序；本頁容量論證不需要 disk 或 T4。

C 始終是原 H−{z,w} 的分量。對 mixed C 記
k_C=|P_C^z|≥1、ℓ_C=|P_C^w|≥1，並令

\[
m_z=\sum_{C\text{ mixed}}k_C,\qquad
m_w=\sum_{C\text{ mixed}}\ell_C.
\]

共鄰點是同一個原頂點，對兩個 incidence 和各貢獻一次。完整接點關係
\(\mathcal T_C(\beta)\) 在固定同一 boundary row β 下產生，定義

\[
R_C(\beta)=\{(a,b):\exists t\in\mathcal T_C(\beta),\quad
 t(P_C^z)\not\ni a,\ t(P_C^w)\not\ni b\},\qquad F_C=U^2\setminus R_C.
\tag{1}
\]

兩個條件必用同一份完整 tuple。保留原 contacts、全部 bridges／旁支、
實際 boundary 附件、root-spokes 與 zw；不把同色框點識別，不拆共鄰點。
只接 root r 的 unary 原分量 D 另以 f_D^r(β) 表示一維禁色集合，避免
與 mixed 的二維 F_C 混淆。若 D 有 n_D 個 r 接點，則 |f_D^r|≤n_D。
消去 unary 後

\[
E_r(\beta)=U\setminus\left(\beta(N_B(r))\cup\bigcup_{D\text{ unary at }r}f_D^r(\beta)\right),
\]
\[
Z_M(\beta)=(E_z(\beta)\times E_w(\beta))
 \setminus\left(\Delta\cup\bigcup_{C\text{ mixed}}F_C(\beta)\right).
\tag{2}
\]

以下 §2 對任意 β 成立；§3–4 的缺額等式及十八側型只在 source q 成立。
§2–4 容許多個 mixed；§5 的 residual 分類與 §6 三點接合才要求唯一 mixed。

## 2. 固定另一 root 後的容量界

**逐欄／逐列容量引理。** 對任意 β、a,b∈U，

\[
|\{a:(a,b)\in F_C(\beta)\}|\le k_C,\qquad
|\{b:(a,b)\in F_C(\beta)\}|\le\ell_C.
\tag{3}
\]

**證明。** 只固定 w=b，先不固定 z。C 在 v 的 list 是
\(L_\beta(v)\setminus\{b:v\in P_C^w\}\)，大小至少
\(\deg_C(v)+1_{v\in P_C^z}\)。C 連通且有 z 接點，因此由
[slack 引理](c5_adjacent_degree5_interfaces.md#4-degree-4-的-tightness共鄰點與分量解除)
至少有一份整分量染色。令 \(\mathcal T_C^b\) 為這些染色的完整接點 tuples，則

\[
\{a:(a,b)\in F_C\}=\bigcap_{t\in\mathcal T_C^b}\{t(x):x\in P_C^z\}.
\]

交集包含於任一個至多 k_C 色的集合，第一界成立；交換 roots 得第二界。
若 x 是共鄰點，它仍只有一個變數；未固定 z 所留下的一份 slack 不會消失。
這是固定同一 b 後的完整關係運算，並非把 R_C 換成兩個 marginals。

設 t_r=|N_B(r)|。Root degree 給

\[
t_r+m_r+\sum_{D\text{ unary at }r}n_D=4,
\qquad |E_r(\beta)|\ge m_r.\tag{4}
\]

若至少有一份 mixed，兩個 m_r 都正。q 拒絕，故固定任一 b∈E_w(q)，
E_z(q)∖{b} 必被各 mixed 的第 b 欄覆蓋。由 (3)，

\[
m_r\le |E_r(q)|\le m_r+1.\tag{5}
\]

此上界沒有把不同 mixed 的完整 tuples 任意接合；各份皆在同一 (a,b) 下
判定，只有在這個精確判定之後才對禁色欄作聯集容量估計。

## 3. Unary 禁色無重疊，source 缺額至多一

先由逐邊 minimality 得三個必要性質。

1. Root-spokes 的 q 色互異；若刪其中一條仍未新增 root 色，無法解除拒絕。
2. 每個 unary f_D 都避開本側所有 spoke 色。刪色 h 的 spoke 時 root 必取 h，
   其餘原 unary 仍在，因此每份都必接受 h。
3. 每個 f_D 都有相對於同側其他 unary 的私有色。刪碰 D 的邊只解除原 D；
   若沒有新 root 色，(2) 完全不變。這只是必要條件，新增色還須通過 mixed。

有 mixed 時 \(\sum n_D=4-t_r-m_r\le3\)。如果兩份 f_D 相交，因各有私有色，
它們都至少含兩色，遂需至少四個 unary incidences，矛盾。因此所有 f_D
兩兩不交，而且與 spoke 色不交。令

\[
D_r=\sum_{D\text{ unary at }r}(n_D-|f_D(q)|).
\]

由 (4) 精確得到

\[
\boxed{|E_r(q)|=m_r+D_r,\qquad D_r\in\{0,1\}.}\tag{6}
\]

這是有 mixed 時的 source 預算；不是將
[no-mixed root 預算](c5_root_degree_excess.md)的等式硬套到 mixed 或 target。
D_r=0 時所有 unary 飽和。D_r=1 時恰一份 unary 少禁一色；該分量至少
有兩個接點，所以 m_r+t_r≤2。沒有任何 unary 時 D_r=0。

下表斜線表示不同必要側型；完全展開共 **18 型**，其中 D=1 恰四型。
同接點數的原分量仍具名；表只省略顏色名稱，不合併原分量身份。

| m_r | t_r | Unary 接點分拆 | 禁色大小 | D_r |
| ---: | ---: | --- | --- | --- |
| 1 | 0 | (3) | (3)／(2) | 0／1 |
| 1 | 0 | (2,1) | (2,1)／(1,1) | 0／1 |
| 1 | 0 | (1,1,1) | (1,1,1) | 0 |
| 1 | 1 | (2) | (2)／(1) | 0／1 |
| 1 | 1 | (1,1) | (1,1) | 0 |
| 1 | 2 | (1) | (1) | 0 |
| 1 | 3 | () | () | 0 |
| 2 | 0 | (2) | (2)／(1) | 0／1 |
| 2 | 0 | (1,1) | (1,1) | 0 |
| 2 | 1 | (1) | (1) | 0 |
| 2 | 2 | () | () | 0 |
| 3 | 0 | (1) | (1) | 0 |
| 3 | 1 | () | () | 0 |
| 4 | 0 | () | () | 0 |

這是必要側型，未套各 mixed 的精確 F_C，也未排除 unary 的幾何不可能性。
不能從表項存在推出來源存在。

## 4. 每一 mixed 欄的精確差額等式

固定 b∈E_w(q)，記 G_C(b)={a:(a,b)∈F_C(q)}，
V=⋃G_C(b)、A=E_z(q)∖{b}。由 q 拒絕，A⊆V。定義

\[
\delta=\sum_C(k_C-|G_C(b)|),\quad
o=\sum_C|G_C(b)|-|V|,\quad
\lambda=|V\setminus A|.
\]

三者皆非負；(6) 立即給

\[
\boxed{\delta+o+\lambda=1_{b\in E_z(q)}-D_z.}\tag{7}
\]

所以 D_z=1 時，E_w⊆E_z；每個 b∈E_w 都使各 G_C(b) 容量飽和、彼此
不交，且恰分割 E_z∖{b}。D_z=0 時，b∉E_z 的欄也完全飽和；b∈E_z
的欄則只有一單位可分配給容量未用、欄間重疊或覆蓋 A 以外的色。
交換 roots 得逐列版本。這些欄仍屬同一原 F_C，不可逐欄獨立挑選來源。

## 5. 各一 incidence：至多兩個禁對與新的對稱 residual

### 5.1 兩個不同原接點

設 P_C^z={x}、P_C^w={y}、x≠y。令 T 為完整有序 (x,y)-tuple 關係。
由 (3)，F_C 每列、每欄至多一格。若有兩個禁對 (a,b)、(c,d)，必有
a≠c、b≠d；每份 tuple 同時屬於「第一座標 a 或第二座標 b」與
「第一座標 c 或第二座標 d」，故

\[
T\subseteq\{(a,d),(c,b)\}.
\]

T 非空；若只留一份 tuple，F_C 就有整列或整欄，違反 (3)。因此兩份
tuple 都存在，且只有 (a,b)、(c,d) 被禁止。得到任意大小的精確結論

\[
|F_C(\beta)|\le2;\qquad |F_C|=2\Longrightarrow
T=\{(a,d),(c,b)\}.\tag{8}
\]

不要求 x,y 相鄰，不丟棄旁支。此處未進一步宣稱原圖必是路徑。

### 5.2 同一個共鄰接點

若 P_C^z=P_C^w={x}，令 T_x 為未固定 roots 時，整個 C 的 x 可取色集。
在 x，boundary list 至少比 deg_C(x) 多二色。若 |T_x|≤1，從 x 的 list
刪去 T_x 後仍有 slack，其他點仍至少 degree，應可著色，與 T_x 定義矛盾。
所以 |T_x|≥2，並且

\[
F_C(\beta)=
\begin{cases}
(T_x\times T_x)\setminus\Delta,& |T_x|=2,\\
\varnothing,& |T_x|\ge3.
\end{cases}\tag{9}
\]

這個任意大分量與 shared singleton 具有相同形式的 root 介面；T_x 卻可能
由整份旁支共同決定，不能冒認為某兩個 boundary 鄰點的補色，或在 disk
中直接把 C 換成 singleton。

### 5.3 唯一 mixed、m_z=m_w=1 的 source residual

現在要求 C 是唯一 mixed，並沿用 minimal q。刪 zw 給非空可用對角；
刪 C 的邊給非空非對角色對。由 (5)，兩 E 大小都至多二；兩側同為
singleton 無法同時滿足這兩種刪邊條件。因此大小只可能

\[
(|E_z|,|E_w|)=(1,2),(2,1),(2,2).\tag{10}
\]

前兩型仍須檢查實際 F_C。最後一型由 (7) 兩方向得到
E_z=E_w=T={a,b}；兩個非對角都必被禁止。由 (8) 或 (9)，

\[
F_C=\{(a,b),(b,a)\}.
\tag{11}
\]

不同 contacts 時，**完整**接點關係恰為 {(a,a),(b,b)}；共鄰 contact 時，
其可取色集恰為 {a,b}。兩側都 D=1，故各自只可能表中的
t=1,(2) 或 t=0,(3)／(2,1)，而非任意 unary 分拆。

這是原 K2 各一接點型沒有的新分支：原 K2 的兩個禁對若存在只能是
對角，故舊報告只留下 (1,2)／(2,1)。較大分量不能沿用該 K2 結論。

## 6. 最小三點原分量的完整 q 控制

連通簡單三點圖只可能 P₃=x₀x₁x₂ 或 K₃，這是最小大小的列舉，**不是**
將任意大 C 收縮成三點。每個 x_i 帶 root mask 0/1/2/3，分別表示
無／z／w／兩 root；三點各取一 mask，要求兩 root 都出現，故各形恰
4³−2·2³+1=49 種具名接線。保留 x₀,x₁,x₂ 次序，沒有以反射刪掉資料。

內度 d_i、root incidence 數 s_i 已定，原 boundary 鄰點數恰為
4−d_i−s_i。Source tightness 要求這些 boundary 鄰色互異，所以每點只需
遍歷 {0,1,2} 的對應大小子集 Q_i；L_i=U∖Q_i。這**只記色集合**，不記
它們用 b0 還是 b2、b1 還是 b3，不能用來判 actual support／環序／disk。

對任意 (a,b)，扣除實際 root mask 的色得到 M_i。由 degree 規格，
|M_i|≥d_i。以下公式不需 Gallai：

- P₃ 拒絕恰當 M₀={s}、M₂={t}、s≠t、M₁={s,t}。若任一點有 slack，
  由 slack 引理接受；全 tight 時端點強迫 s,t，正是此條件。
- K₃ 拒絕恰當 M₀=M₁=M₂ 為同一 pair。Slack 時接受；全 tight 的三個
  pair 若不全相同，可給三點不同色：兩集合聯集至少三、任兩聯集至少二，
  或直接按三個位置選色證明。Checker 另直接枚舉完整三點 tuples 核對。

接到十八側型時使用 **完整逐邊 minimality**：原 (2) 為空、刪 zw 釋放
非空對角、解除 mixed 釋放非空非對角；刪每份 unary 釋放的整個 f_D
與另一側 E 必有通過 F_C 的異色對；刪 spoke 同樣用釋放的原色。
在一份實際來源上，這些條件由原分量解除引理構成充要式。
代入抽象色角色後則仍只是必要資料，未保證 unary 或 boundary 接線可實現。

| 固定域控制 | P₃ | K₃ |
| --- | ---: | ---: |
| 具名 incidence masks | 49 | 49 |
| q boundary 色集合配置 | 811 | 595 |
| 16 格公式與完整 tuples 核對 | 12,976 | 9,520 |
| F_C 非空的配置 | 228 | 289 |
| 通過粗 residual／對角條件 | 102 | 181 |
| 通過完整逐邊色角色接合的配置 | 102 | 162 |
| 上列配置的全部側角色接合 | 15,990 | 13,104 |
| 至少有一份完整接合的 incidence masks | 16 | 30 |

因此唯一 mixed **恰為三點**時，得到有限域認證的必要 incidence 數：

\[
P_3:\ (1,1),(1,2),(2,1);\qquad
K_3:\ (1,1),(1,2),(2,1),(2,2).\tag{12}
\]

特別是 triangle 的粗條件曾保留 (1,3)、(3,1)、(3,3)，完整刪邊條件
再排除；沒有把粗候選當最終正常形。式 (12) 是有限 q 色域加已證容量／
解除引理的結論，不能提升為所有大小 mixed 都至多二 incidences。
證書保存全部 1,406 個局部配置的 ordered triple bitmask、完整 F_C mask、
接合數與逐配置 SHA；另保存 98 個具名 mask 統計及具體角色見證。
Triple bit 位為 16c₀+4c₁+c₂，root-pair bit 位為 4a+b。

### P₃ 對稱分支的真實圖控制

取原 mixed 路徑 x₀x₁x₂，z 只接 x₀、w 只接 x₂，三點皆接 b0,b1。
q 下三份 list 均為 {2,3}，完整接點 tuples 恰為 (2,2)、(3,3)，
故 F_C={(2,3),(3,2)}。取兩側 E_z=E_w={2,3} 即進入 (11)。

Checker 把它接到前層 shared-singleton 控制的兩個原 unary triangles，
保留全部原附件，得到完整 degree=(5,5,4,…,4) 的真正 minimal q-core。
保存 31 份逐邊刪後 coloring、全部 240 proper rows 的精確接合與獨立
全圖回溯核對、十個 canonical rows 的完整 tuples。
另明列並驗證 K5 branch sets，所以**這不是 disk 正控制**。
它證明對稱分支在實際 degree/minimality 規格下不能只靠容量刪除。

## 7. 重播、證據層與停止點

```bash
python3 scripts/c5_mixed_capacity_contacts.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_capacity_contacts.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 只用標準函式庫，重用前層完整 tuple 與獨立 pinned 回溯函式，
不讀舊 artifact 的接受 flags；不重新枚舉 no-mixed 支援。除 §6 外，另有：

- 258 個單側色角色候選；143 個通過必要容量條件，落在十八側型。
- 1,424 個覆蓋欄控制，核對 (7) 的三項非負分解。
- 全部 65,535 個非空二元 tuple 子集，65,431 個通過行列容量一；
  其中 63,935／1,424／72 份分別禁零／一／兩對，核對 (8)。
- 十一份大小至少二的共鄰色集核對 (9)，另存 marginals 誤接合的負控制。
- 前層八個 mixed 固定分量（含 path、cycle、triangle-bridge、K4），
  全 240 列共 1,920 份完整介面、30,720 個獨立 pinned queries，核對 (3)。

無 `--check` 只生成本層證書；`--check` 重算後逐 byte 比較。證書綁定
本 checker 與直接載入的前層 Python SHA，不改寫舊證書。
紙面容量／兩接點界不靠有限枚舉，未新增外部定理依賴。
有限三點色域有完整上界且逐案核對，但沒有建立平面支援表。
`lake build` 只確認既有 Lean 專案，未形式化本頁新結論。

本輪停止於任意大小容量化約、各一 incidence 的完整介面界，以及唯一
mixed 三點形的必要接線。最窄未解分支是 **唯一 mixed 原 P₃、兩端各接
一 root、E_z(q)=E_w(q) 為同一 pair**：保留原五環 z–x₀–x₁–x₂–w–z
與原 zw，先證實際附件／內外側次序及 unary 外部路徑，再研究指定 p₁、p₂。
該五環內側是否空也須證明，不能照搬原 K2 四環的 disk 排除。
更大 mixed、多 mixed 的跨列／幾何、完整 Σ、逐染色 repair、一般／共同
出口與 `K∞=K≤5` 仍未證。
