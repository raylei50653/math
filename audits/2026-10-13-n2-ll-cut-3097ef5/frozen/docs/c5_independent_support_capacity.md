# 933／941：degree-excess、條件禁色容量與第一個六跨度障礙

**後續（2026-10-02）**：[四容量子覆蓋共享](c5_excess_one_subcovers.md) 已把
933 下界提高到 ε≥2；941 的 ε=1 三型經 [single-spoke](c5_941_single_spoke.md)、
[two-spoke](c5_941_two_spoke.md)與 [three-spoke](c5_941_three_spoke.md)全部排除，
現兩候選均有 ε≥2，一般來源仍未排除。下文保留第一輪共同 ε≥1 與六跨度
禁形的推導；§5 的下一入口已由後續涵蓋。

2026-10-02，基準 `1274894`。接續 [Kempe screen](c5_kempe_screen.md)
的兩個 independent-singleton 候選，採**固定完整 Σ 的 edge-minimal source**。
本輪不新增圖枚舉。當前入口見 [Kempe 導覽](c5_kempe_guide.md)。

**已證的共同下界是 ε(G)≥1，不是 ε(G)≥6。** 有效內部連通，所有
minimal rejected-row cores 兩兩共用至少一個 degree≥5 root。
任一具有刪 root 見證的拒絕列，另有包含 mixed 分量的精確預算
`D_r+O_r=deg_G(r)−4`。對同一 root 的 unary 未用色 carriers，得到

\[
\deg_G(r)-4\ \ge\ \sum_{C\in I}(k_C-|F_C|)+|I|-1,
\qquad
5\ \ge\ \sum_{C\in I}\ell_C\ \ge\
\sum_{C\in I}\max(0,3-|F_C|). \tag{A}
\]

因此**三份 unary singleton 禁色皆為 boundary 未用色 D 時，跨度至少
2+2+2=6，不能是 disk source**。尚未證明 933 或 941 必含此配置，故
本輪沒有排除任一候選。式 (A) 的 I 必須來自同一原圖、同一 root、
同一拒絕列；不能把三列各自的一份 carrier 相加。

證據：§1–5 為任意大小紙面推導；ε≥1 另沿用既有全 degree-4 合成，
包含其外部 degree-list 定理依賴。新增容量與跨度引理本身不需 Gallai
或 4CT。§6 是三張固定圖及小色集合的 Python 控制；無新 Lean theorem。

## 1. 兩種 minimality 與來源的基本結構

G 為有限簡單圖，B=(b0,…,b4) 是指定 disk 外框；忽略孤立內點，
H=G−B。Ω 為十個 proper boundary patterns 的 S4 orbits，沿用原固定
pattern order。T4=932，兩候選為

| 完整 Σ | 接受的 singleton 位置 P | 拒絕的 singleton 位置 Q |
| --- | --- | --- |
| 933 | {4} | {0,1,2,3} |
| 941 | {2,4} | {0,1,3} |

本頁 edge-minimal 指每條非框邊 e 都有 Σ(G−e)⊋Σ(G)，不要求所有 e
釋放同一列。固定 q 的 minimal core M_q 是包含 B 的 inclusion-minimal
拒絕 q 子圖；它繼承 T4，但 Σ(M_q) 未必等於 Σ(G)。

### 1.1 Degree 與完整支援

T4 全收使 B 無 chord。每個有效內點 v 的完整 degree≥4：選 incident
非框邊 e 及 G−e 新接受的列 q，捨去 v 後保留該完整染色；若 deg_G(v)≤3，
可選剩餘色補回 v，矛盾。定義

\[
\varepsilon(G)=\sum_{v\in H}(\deg_G(v)-4),\qquad
R=\{v\in H:\deg_G(v)\ge5\}.
\]

沿用 [未接內點引理](c5_unattached_boundary.md#1-不依賴-degree-或-disk-的改色引理)：
若一個帶框子圖接受 T4 且拒絕 singleton-i 列，其 actual boundary support
必包含 B∖{b_i}。理由是未碰到的非 singleton 框點可先改成未用色 D，
用 T4 延拓，再還原。這保留同一份完整染色。

所以每個 M_q 至少碰四個框點，其任一包含完整支援的框弧長度至少三；
G 拒絕不只一列，故 G 碰全部五個框點。

### 1.2 兩份四點支援不能由不交的內部連通圖承擔

若 S,T⊆B 各至少四點，存在環序交錯的 a,b,c,d，滿足 a,c∈S，b,d∈T。
證明：先取 S 中四點，T 至少包含其中三點；這三點含該四點環序的一組
對角點，另一組對角點留給 S。兩個內部不交的連通圖若分別支援 S,T，
便各有一條內部路徑連起對角點，違反 disk 交錯路徑分離。

這是第一個共同的 **3+3=6 支援需求**；實際排除依據是交錯路徑，
不是替所有互不相交的圖任意假設可相加的 hulls。§4 才為共同 root
的 fan 證明相容 lifts 及總跨度≤5。

每個 H 分量都必拒絕至少一列，否則刪它任何邊不改 Σ。各分量繼承
T4，故其支援各至少四點；上段排除兩分量，因此 **H 非空連通**。
每個 M_q 的有效內部連通：否則保留其中拒絕 q 的分量、刪除其餘分量，
便違反 q-minimality。同理，任意兩個 M_q、M_p 的有效內部必相交；q、p
可相同或不同。

### 1.3 ε≥1 與共同 root

若 ε=0，所有內點完整 degree=4。在任何 M_q 中，所含有效內點的
degree 至少四，故保留其在 G 中的全部 incident 邊。沿連通 H 傳播，
得到 M_q=G（忽略孤立點）。但 [全 degree-4 合成](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)
使 T4-accepting disk minimal q-core 恰只缺 q，與兩候選至少三缺失矛盾。
因此

\[
\boxed{\varepsilon(G)\ge1,\qquad 1\le|R|\le\varepsilon(G).} \tag{1}
\]

更強的接合資訊是**任何兩個 minimal cores 都共用一個原 R 頂點**。
若它們的共同內點已在 R，結論直接成立；否則它在 G[H∖R] 的原分量 C。
degree-4 飽和使兩個 cores 都包含整個 C 及其所有 incident 邊。
H 連通且 R 非空，C 接到某個原 root，兩 cores 因而都含該 root。
這只證兩兩相交，沒有把 root 集族的 pairwise intersection 升成全體共同交集。

## 2. 任意 root 的完整條件介面，包含 mixed

固定 r∈R、G 拒絕的一列 q，並要求 **G−r 可延拓 q**；取其一份完整
染色 f，令 η=f|R∖{r}。此條件不能對每個 r、每列 q 自動假設。
但對每個 r，Σ-minimality 至少提供一列：刪任一 r-incident 邊 e，
取 G−e 的新列見證，再捨去 r 即可。

C 始終指 G[H∖R] 的**原**分量，所有點在 G 中完整 degree=4。
記 P_C^r=N_G(r)∩C、k_C^r=|P_C^r|。對 k_C^r>0 的 C，固定同一 q、η，
只保留 r 未指定，令 T_C(q;η) 為 C 全部合法染色在**全部原 root contacts**
的有序 tuples；共鄰接點只有一個變數。定義

\[
F_C^r(q;\eta)=\bigcap_{t\in T_C(q;\eta)}
                 \{t(x):x\in P_C^r\}. \tag{2}
\]

每點的 list 至少為 deg_C；任一 r-contact 留下一色 slack，故以該點為根
的生成樹貪婪法給 T_C(q;η)≠∅。因此

\[
|F_C^r(q;\eta)|\le k_C^r. \tag{3}
\]

給 r 色 a，C 可填入恰好當 a∉F_C^r。所有不接 r 的 C 已由 f 證可填入；
它們無須重選 η。令 X_r=N_G(r)∩(B∪R)，對 x∈X_r 令 c_x=q(x) 或 η(x)。
精確 residual 為

\[
E_r(q;\eta)=U\setminus\left(\bigcup_{x\in X_r}\{c_x\}
                  \cup\bigcup_{C\sim r}F_C^r(q;\eta)\right). \tag{4}
\]

E_r 恰是固定 η 後所有可延拓 r 色。G 拒絕 q 使 E_r=∅。
每個 mixed C 先固定相同 η 再用完整 tuples，未改作跨 η 的 unary marginal。

## 3. Degree-excess 是缺額及重疊的精確容量預算

把每條 r–B、r–(R∖{r}) 邊的 singleton 色集視為**分開具名**的 factor；
即使顏色相同也不能預先去重。與全部 F_C^r 合成 factor 多重族 \(\mathcal F_r\)。
定義

\[
D_r=\sum_{C\sim r}(k_C^r-|F_C^r|),\qquad
O_r=\sum_{F\in\mathcal F_r}|F|-\left|\bigcup_{F\in\mathcal F_r}F\right|.
\]

兩者非負，且 |X_r|+Σk_C^r=deg_G(r)。拒絕列中 factor 聯集是 U，所以

\[
\boxed{D_r+O_r=\deg_G(r)-4.} \tag{5}
\]

不拒絕但 η 仍相容時，正確式子是 D_r+O_r=deg_G(r)−4+|E_r|。
式 (5) 不要求 q-minimality、spokes 異色或 no-mixed；root–root 色已固定，
所以沒有把 [no-mixed 骨架](c5_root_degree_excess.md)的 κ 項無故丟棄。
本頁 O_r 也包含重色 spokes、root 邊色與分量禁色之間的重疊，與舊 O 的
定義不同。不得直接混用兩個公式。

若 I 是同一 r、q、η 下都禁止某個色 d 的分量族，僅此色已造成至少
|I|−1 次重疊，故

\[
\deg_G(r)-4\ge\sum_{C\in I}(k_C^r-|F_C^r|)+|I|-1. \tag{6}
\]

每個 root 可用各自的刪邊見證得到 (5)，數值上相加為 ε(G)。這些見證
可來自不同 q，並不提供一份跨 roots／跨列共用的染色或可相加的跨度。

## 4. 未用色容量迫使實際 boundary span

### 4.1 Unary 分量的穩定子下界

令 C 只接 r 一個 root，S_C=N_B(C) 為**全部實際支援**，
F_C(q)=F_C^r(q;η) 不依賴 η。q 是三色列，D 為未用色，且 D∈F_C(q)。
此時 S_C 非空：否則 F_C 對所有 boundary rows 相同且為 S4 不變集，
非空便等於 U，使任何 T4 列也不可延拓。
任何逐色固定 q(S_C) 的全域色置換，都將 C 的完整 tuples 雙射到自身，
所以保持 F_C。它能把 D 送到任一未見色，故

\[
U\setminus q(S_C)\subseteq F_C(q),\qquad
|q(S_C)|\ge4-|F_C(q)|. \tag{7}
\]

一段長 ℓ 的框弧只有 ℓ+1 個框頂點；包含 S_C 的任何 lift 因而滿足

\[
\boxed{\ell_C\ge\max(0,3-|F_C(q)|).} \tag{8}
\]

尤其 F_C={D} 必見全部三個 boundary 色，故 ℓ_C≥2；二禁色 carrier
只由此得到 ℓ_C≥1。不能把「含 D」一概當成 singleton。

### 4.2 同一 root 的相容 lifts

任取同一 r 的 unary 原分量族 I，各支援非空。只為拓撲論證，將每個
原 C 收縮為 c_C，保留 r–c_C 的一條原邊及每個支援框點的一條原附件，
刪除無關內部；完整 T_C、F_C 的計算仍在原圖，沒有替換 relation。

內部星狀樹 r–{c_C} 的小正則鄰域是 disk，其邊界上每個 c_C 的外向
附件成一個連續區段。到外框的弧在這個 annulus 中不交，所以外框附件
按同一 cyclic order 分組；共同框端點可作無限小分開處理再合回。
沿外框一次取各組第一至最後的 lift I_C，區段內部不交，允許端點共用，
側間空隙非負。因此

\[
\sum_{C\in I}\ell_C\le5. \tag{9}
\]

這是同一嵌入共同選的 lifts，不是每份各自挑最短弧後假裝它們相容。
保留原支援的稀疏性；沒有把整段弧新增為附件。

由 (6)、(8)、(9) 得式 (A)。**三份 F_C={D} 的 unary carriers** 迫
deg_G(r)−4≥2+Σ(k_C−1)，同時跨度≥6>5，故整個配置不可能。
更一般，只要 Σ_C max(0,3−|F_C|)≥6，也有同一來源排除。

### 4.3 Mixed 與跨列的明確界線

Mixed C 的穩定子還必須固定 η 在其他鄰接 roots 的顏色。令其色集為 A，
h=|A|；只有在 d∉q(S_C)∪A 且 d∈F_C^r 時，才可推出

\[
|q(S_C)|\ge4-|F_C^r|-h,\qquad
\ell_C\ge\max(0,3-|F_C^r|-h).
\]

固定的另一 root 可提供一個必見色，不能當成 boundary attachment。
同時 mixed 分量不再是上述 unary fan，(9) 的適用性須另證。
跨 q、跨 η、不同 cores 的支援即使各有下界，也不能不扣共享負載地相加。
特別是 §1 迫 cores 相交，正是不能把其 3+3 直接當成全圖六跨度矛盾的原因。

## 5. ε=1 的精確下一入口

若候選有 ε=1，便恰有一個完整 degree-5 root r，其餘 degree-4。
§1 使所有 minimal cores 都含 r。degree-4 飽和又使每份 core 對
G[H∖{r}] 的每個原 C 必須全取或全不取，並保留全取 C 的全部附件。

因此每份 minimal q-core 只有兩種可能：

1. r 在 core 中 degree=5，於是 core 就是整個 G；
2. r 在 core 中 degree=4，恰少一條 r incidence；被省略者只能是一條
   root-spoke，或一份只有一條 r incidence 的完整原 C。其餘原區域全保留。

第二型由全 degree-4 合成恰只拒絕 q。刪該 C 任一 incident 邊會對每列
解除整個 C 的限制，沿用 [分量解除引理](c5_degree5_interfaces.md#3-刪除分量任一邊禁色全部解除)；
這裡的「省略區域」不是把不在 core 的點繼續當 degree-4 點計數。

在此單 root 情況，每列的 G−r 都可由各 C 的 slack 延拓。因此所有原拒絕列
都可使用 (5)，每列 D_r+O_r=1。但不同列可由不同四容量子覆蓋拒絕，
尚未證這些同源關係必產生 (A) 的 ≥6 需求。三份 singleton D-carriers
本身已要兩單位 excess，所以不能拿它排除 ε=1。

**當輪停止點：** 已有 ε≥1、cores 的共同 root 約束、mixed 條件容量及
unary 六跨度禁形；未證 ε≥2，更未證一般 source 的跨度需求≥6。
下一步應在此 ε=1 單 root 的完整十列關係上比較各四容量子覆蓋，或證
不同列 carrier 的共享上限。不要從雙缺失來源的出口定理直接推論
933／941；它們分別缺四／三列，繼承的完整 Σ 前提不同。

## 6. 小型控制、重播與信任範圍

[Checker](../scripts/c5_independent_support_capacity.py) 與
[artifact](../artifacts/c5_independent_support_capacity/observations.json) 保存：

- 兩候選的完整十列及強迫支援；36 個有序四／五點支援對的交錯見證。
- 固定 q=01012、32 個 actual support 子集上的 147 個未用色穩定子控制。
  只檢查四色集合，不生成圖或獨立拼裝來源 tuples。
- 三張明列邊集的小圖，46 份逐 row／root／η 條件介面；完整 contacts、
  tuples、tuple witnesses、刪 root 染色及每條刪邊新增列見證全保存。

第一張是 [既有 943 witness](c5_weak_critical_cores.md#4-既有代表的實際結構)，
`k3-t382/submask 2045`。重新直接染色證實 ε=1、T4 全收、Σ-edge-minimal，
但沒有一個拒絕列使它 q-edge-minimal；它提供 minimality 混用的負控制。
既有 disk provenance 沿用原報告，本輪未重新檢查其 rotation。

第二張是明列邊的條件 mixed 控制：固定另一 root 色 2 時，一份 singleton
原 C 的 boundary 支援只有 {b0,b1}，仍可有 F_C^r={3}。這驗證忽略固定
root 色會誤報 span≥2；不聲稱它是 933／941 來源。

第三張有三個 singleton 原 C，各接同一 root 及 {b0,b1,b4}，q 下都禁 D。
root degree=6，D_r=0、O_r=2、需求跨度=6。它含以三個 C 點與三個框點
為兩側的原 K3,3，明確是 **non-disk 容量正控制**，不是候選反例。
另保留 abstract F={2,3}、S={b0,b1}，說明二禁色 carrier 只需一單位的
穩定子下界；未聲稱該抽象資料能由 degree-4 disk 分量實現。

```bash
python3 scripts/c5_independent_support_capacity.py --check
PYTHONHASHSEED=17 python3 scripts/c5_independent_support_capacity.py --check
python3 scripts/c5_unattached_boundary.py --check
python3 scripts/c5_kempe_screen.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際執行與省略範圍見 [本輪紀錄](history/2026-10-02-independent-support-capacity.md)。
新 checker 不讀接受／排除 flags 作 oracle；不重寫既有 artifacts。
紙面拓撲與既有全 degree-4 合成未新增 Lean 形式化；build 成功不改變此界線。
一般 adjacent-singleton lemma、共同出口及 K∞=K≤5 仍未證。
