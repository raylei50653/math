# 任務 E5：相鄰 J1–J3、J5 的精確列依賴

2026-10-04；基準 `integrate-kprime-e3 @ 2ac279b6144cdfcf4ececd7b72f5d287a6f4b4ac`。
獨立 worktree `/home/ray/developer/ai/math-task-e5`，分支 `task-e5-exact-rows`。
只以 exclusive-create 新建 E5 檔案；既有 tracked 檔案零改動，沒有 commit／push。
J4、J6、待 K′、D₈ 稽核與 E4 非相鄰不在本任務範圍。

**交付為四分支依賴表及新紙面化約，仍有明列缺口，沒有證成整個相鄰分支或 ε≥3。**
新增結果：J3 的兩種 minimal 身份、ternary 四分支整型排除、J2 mixed12 四分支排除、
932 的五-spoke／J3 binary 排除、A 的 N 全收與 singleton-U 身份、A 共用 pair、
以及 B mixed22 無 unary 的全部原 faces／contacts／bridges 整型排除。

**停止原因 (c)：E3 表的 A「需要先補一般 spoke+unary (4,4) 前序」判定過強。**
原 A 證明確實引用通用 (4,4) 前序；本輪指出既有 retained-mixed 結構引理
已使 incidence12 的該前序不可能。因此這是 A 子型適用範圍／必要依賴的誤判，
不代表歷史證書數學 payload 錯誤。發現後停止新數學推進，只整理已完成論證及固定控制。
沒有修改 E3；沒有構造符合全部來源前提的候選反例。

## 1. 前提、讀取範圍與四分支

沿用 [E3 §1–2](../c5_excess_two_e3/REPORT.md#1-完整前提與證據層)：
有限簡單 disk 圖 G，指定有序 induced C₅ 外框 B=(b₀,…,b₄)，其餘點私有；
接受五個 T4 列，每條非框邊 Σ-critical，ε=2；本報告的 roots a,b 相鄰、各完整 degree 五，
其餘有效內點完整 degree 四。選定 q₀、q₁、q₃ 拒絕；使用 E3 已證的
triple-critical、兩個 root 刪除全收與 ab 省略全收，以及 E2 的 ε≤1 結論。
不將 Σ-critical 當作每個 q 的 minimality。

讀取 E3 REPORT §2、§3、§3.1、§6、adjacent_notes §2；Kempe 導覽 §3 的 J1–J5
相應 spoke+unary、mixed omission、五-spoke、binary／star／hubs／ternary、
A／A₂–A₄、B／B₂–B₄ 原報告；所用通用分類的原文入口見 §9。

| 完整分支 | Q | q₂=`01201`／row3 | q₄=`01012`／row0 |
| --- | --- | --- | --- |
| 941 | 013 | 接受 | 接受 |
| 933 | 0123 | 拒絕 | 接受 |
| 940 | 0134 | 接受 | 拒絕 |
| 932 | 01234 | 拒絕 | 拒絕 |

本表是四個互斥的**精確**分支。若只說「933 形、再拒 q₂」而暫不限定 q₄，
仍須拆成 933、932，不能補填 q₄ 接受。932 接受全部 T4；它沒有接受任何三色列。
三列加 triple-critical 本身沒有推出任何 optional 三色列接受。

940 使用同一整圖反射 `φ(i)=1−i (mod 5)`，即 `[1,0,4,3,2]`：
Q0134→Q0123，940→933，選定 triple013→013；q₂→q₄、q₄→q₂。
全部附件、root roles、contacts、ownership、原 rotation 與字面顏色隨同搬運。
[branches.json](branches.json) 保存十列的 literal transport 與 orbit-index 對應；
[controls.json](controls.json) 另保存精確 935 整圖的原邊、rotation 與完整染色搬運。
只在識別 boundary S₄ 軌道索引時使用 canonical row；不獨立正規化原分量。

## 2. 依賴項 × 分支狀態表

「證」指本輪任意大小**紙面**新推導，依賴明列的既有通用定理；Python 不證拓撲。
「局部證」只在原 named shape／actual-support 前提已給定時成立，不能代替整型 coverage。
G1–G4 是 §7 的精確缺口；「排」指指定子型整型來源排除。

| 依賴項 | 941 | 933 | 940（共同搬運） | 932 | 新依據／保留界線 |
| --- | --- | --- | --- | --- | --- |
| J1 retaining mixed 的 spoke+unary：額外接受列與完整十列恢復 | G1；optional 角色由分支給定 | G1；只有 q₄ 接受 | G1；只有 q₂ 接受 | G1；三色接受條件均失效 | L1 只給 predecessor 單拒絕身份，沒有新全來源排除 |
| J1 只省略 mixed11：exact-target 十列 | G1 | G1 | G1 | G1 | 可證 G−C 為 Ω 或只缺一列，不能預填 Ω |
| J2 舊 p_A/p₂ 相反接受性＋舊八框架 coverage，mixed11+U | G2；舊 normalized scope 的角色可用，coverage 未新證 | G2；新必要域可兩列皆拒絕 | G2；同左，須保留實際 transported 列 | 排；舊接受對已由 L3–L4 取代 | 新必要 S_a 域 4／2／2／0；前三分支未證原八框架涵蓋 |
| J2 mixed12、無 U 的 minimal 前序／整型 | 證／排 | 證／排 | 證／排 | 證／排 | L2＋two-spoke 三接點，不讀額外接受列 |
| J3 binary mixed11+binary-U：前序 minimal 身份 | 證 | 證 | 證 | 證 | L2：binary-U 原環使後續全四 core 不可能 |
| J3 binary 的完整 named-support／relation coverage | G3 | G3 | G3 | 排 | 前三分支不能把舊 116/256→32/64 的零殘留當新 coverage；932 用 L3–L4 |
| J3 ternary mixed12+unary1：前序 minimal 身份 | 證 | 證 | 證 | 證 | L2：retained C12 不可能有全四 core |
| J3 ternary 的全部 frame coverage／整型 | 證／排 | 證／排 | 證／排 | 證／排 | L5 對全部三-spoke 支援，繞過舊 20/60 ledger |
| J5 A：N 全收、a-spoke 省略 Ω、每拒絕列 singleton-U | 證 | 證 | 證 | 證 | L6；移除 E3 A 的過強前序依賴 |
| J5 A：equal spoke-pairs，含原 A₃／A₄ 型 | 排 | 排 | 排 | 排 | L7，三-hub 恢復原 ax；不需 NΩ |
| J5 A：原 01/23、01/12 的條件局部出口 | 局部證 | 局部證 | 局部證 | 局部證 | L6 補全身份後，原 A／A₂ 所用 q₀/q₁/q₃ 原 joint 論證可用 |
| J5 A：其餘 unequal frames／全型 coverage | G4 | G4 | G4 | G4 | 未把幾何 D₅ 或舊 70/90 必要域當全部來源涵蓋 |
| J5 B：原 spoke omission Ω／(5,5) q-core 身份 | 證 | 證 | 證 | 證 | L2＋三接點；不需歷史 exact-target 表 |
| J5 B：原 01/23 之外全部 faces、contacts、bridges | 排 | 排 | 排 | 排 | L8：共同 column／edge signatures＋所有 Gallai terminal blocks |
| J5 B：B₄ 指定 {4} 之外的 genuine shared bridge leaf | 排 | 排 | 排 | 排 | L8 cut parity，適用任何實際單框附件 h |

前兩列 G1 並非說 941／933 分支角色不足以滿足歷史精確 Σ 輸入；角色本來就相符。
本任務要求**新證明**，故沒有直接引用舊 exact-target solver 作結案。
E3 form26/target1004 使用接受 row3 的例子也不是來源反例：將該 target 列回拉
可落在原 q₂ 或 q₄，正是 optional 位；它只定位歷史證書的額外接受依賴。

## 3. L1：共同 proper-subgraph 拒絕輪廓

令 S⊊G 保留指定 B，不要求 S 自己 Σ-critical 或 degree≥4。
若 S 仍拒絕兩個非相鄰 singleton 列，取在 S 中保留這兩列拒絕的 inclusion-minimal M。
刪點補色給 M 每個有效內點 degree≥4，每條非框邊會釋放該 pair 中至少一列；
所以 M 自己 Σ-critical，接受 T4，繼承 disk。

對原 G 的有效內點集，用 E3 的同 ε 飽和式得 ε(M)≤2。
若 ε(M)=2，所有 surplus roots 保全原邊，degree 四點沿原連通 H 飽和傳播，迫 M=G，
與 M⊂S⊊G 矛盾。因此 ε(M)≤1；E2 的低 ε 定理禁止非相鄰拒絕 pair，矛盾。

所以 **每個 proper S 的 Q_S 為空、單點、或相鄰二點**。
這比「每條原邊至少釋放指定三列之一」強，但仍不等於 proper S 全收 Ω。
若 S 每個有效內點 degree≥4 且 ε(S)=0，對 minimal pair-core 用同一比較及 E2 ε=0
可得 |Q_S|≤1；若 S 已拒絕 q，就有 Σ(S)=Ω−{q}。

此引理不需要三列，實際在精確 935 的全部 2,048 原非框邊子集上核對：
2,047 proper 子圖全部符合；19 個 degree-valid 子圖亦符合 ε=0／ε=1 邊界，
只有原 G 保留 ε=2。沒有把非 critical 的省略圖直接套 E2。

## 4. L2–L5：J2/J3 的共同 minimal 身份與三-spoke 列限制

### 4.1 L2：原 incidence 排除後續全四 core

E3 root／ab 刪除全收迫任何拒絕 q-core 保留 a,b,ab。
原 degree 四分量只可全取或全不取；root 一旦降四便保留其剩餘全部原邊。
全 degree 四 minimal q-core 的通用分類只有 bridges 與互斥 triangles。

- 若 retained mixed 有一側兩個不同 contacts，取另一側 contact x 及不同的 y，
  原 C 中 x↝y 路徑加 ax、yb、ba 是長至少四的原環，故全四 core 不可能。
  這只用 actual contacts，容許 x 與另一 y 重合。C12、C22 都適用。
- J3 binary 的 C11 之外還保留同一 U 的兩個不同 b-contacts u,v；
  若全四 core retained C11，通用分類先迫原 abx triangle、共用 x。
  原 b–u↝U v–b 又是環；長≥4 不可，長3 則兩 triangles 共享 b，亦不可。
  U 容量二不能由 b 的至多一 incidence loss 省略。

對 J3 刪一同色 a-spoke 的 M，a 已四，故 C 全保留；上述理由排除 b 再降四。
所以 minimal q-core 正是 M。ternary 的 U 只可全取或全不取，兩種全四選擇都由 C12 排除。
binary 與 ternary 的 minimal 身份四分支統一成立，不需先解 J1。

J2 mixed12 無 U 亦同；若 b 再降四，只能再刪一 b-spoke。
此後續 core 由 C12 的原長環直接排除，連 E3 的 finite 雙-spoke screen 都不需要。
M−b=K=C+a，三 contacts=(a,y₀,y₁) 互異、全部完整 degree 四；
b 兩 spokes 在 q 下必異色，通用 two-spoke 三接點來源定理直接排除 M。
每份三-spoke 支援都有所選 q 的重色 query，故此 J2 子型四分支全排。

### 4.2 L3：同一省略身份不可供兩個拒絕列

J2 mixed11+唯一 b-unary U，取任一 a-spoke omission M。
L1 禁止 M 拒絕非相鄰 pair。
若 M 拒絕相鄰 p,p′，接受 T4 的唯一 degree-5 **minimal** q-core 必接受 q 的兩個框鄰列，
所以 M 不能是任一列自己的 minimal core。
因 a 已四、C 必保留，proper core 只能再省一 b-spoke，或整份 U。
前者是 E3 已證的三列版原雙-spoke (4,4) 排除；兩列因此只能共用同一 M−U。
M−U 全 degree 四、原 H 連通，拒絕 q 時其 minimal q-core 飽和取整圖，只缺 q；
同一原身份不能又拒絕 p′。故 **|Q_M|≤1**，不需先排 spoke+unary 身份。

J3 binary 的 M 已由 L2 證 q-minimal。若它拒絕相鄰 pair，就違反上述唯一 degree-5
相鄰列分離；非相鄰 pair 由 L1 排除。故同樣 |Q_M|≤1。
這裡不能把此结論擴張成 Σ(M)=Ω；951 的原 binary 省略正是警戒控制。

### 4.3 L4：完整五列共同欄位算術，932 整型排除

對 a 的原三-spoke 集 S 與 e=a b_j，定義

`D_e={q∈Q_G : ∃k∈S−{j}, β_q(j)=β_q(k)}`。

每個 q∈D_e 在同一原圖滿足 Col_q(G−e)=Col_q(G)=∅。
所以 L3 要求 |D_e|≤1。只核對十個 S 的字面欄位，得到：

| 分支 | 必要 S_a |
| --- | --- |
| 941 | 012、014、034、123 |
| 933 | 012、123 |
| 940 | 014、034 |
| 932 | 空 |

這是所有十個三-spoke 集的**必要**欄位域，不是舊八份來源框架，也不是實現證書。
932 因無任何 S，五-spoke mixed11+U 與 J3 binary 均整型排除。
其餘分支仍保留完整同圖支持／relations 的缺口，不能以此縮表自行結案。

### 4.4 L5：ternary 三接點直接繞過 frame ledger

任意三-spoke S 均有所選 q 的重色 e=a b_j；取同一原 M=G−e。
其唯一 degree-5 root b 恰一 spoke，M−b 正是原 K=C+a 与独立 U；
contacts=(a,y₀,y₁)、(u) 互異。L2 已證 M 自己 q-minimal，
因此可直接用通用 single-spoke-(3,1) active-triangle 定理，無需舊 20/60 ledger。

更明確地，以完整 R_K、R_U 定義共同 root 避色 F_K、F_U。
leaf a 的兩個保留 spoke 見兩色，L=U₄−β(S−{j}) 大小二；
任何 d∉L 固定於 b，a 仍有 list slack，故 F_K⊆L。
單 contact U 給 |F_U|≤1。b 的合法色 A=U₄−{β_s} 大小三，而拒絕迫 A⊆F_K∪F_U，
所以 F_K=L⊆A，F_U=A−L 是 singleton；若 L 不含於 A 已直接矛盾。
兩份 tight lists、同一原 block palettes 迫三接點 active triangle，原三 arms／tethers
與 b、B 給 K₅。全程保留完整六角色 joint、原 x 的共享身份及空 fibres。

[local.json](local.json) 核對 180 同框 queries、3,600 palette 候選：132 個唯一 cover，48 無 cover。
無界 arms／旁支及拓撲由既有紙面定理負責。

## 5. L6–L7：A 的前序身份與共用 pair

### 5.1 L6：N 與 a-spoke omissions 全收，恢復完整 singleton-U 身份

A 的 incidence 為 C12 加 a 側單 contact unary U，兩 roots 各兩 spokes。
令 N=G−U，roots degree 為 (4,5)。N−a、N−b、N−ab 都從對應的原全收圖再删 U，故仍 Ω。
若 N 拒絕 q，其 core 必含 a,b,ab；a 已四保全 C，b 只能再省一 spoke 或保持五。
全四選擇由 L2 的 C12 原長環排除，因此 N 自己 q-minimal。
N−b=C+a 是三接點分量，b 的兩原 spokes q 色異，two-spoke 三接點定理排除 N。
故 **Σ(N)=Ω**，四分支都成立。

對 M=G−任一 a-spoke，相同論證保留 C、U，M−b=C+a+U 仍是同一連通三接點分量；
a 在其中內度二，定理不要求 leaf。因此 **兩份 a-spoke omissions 皆 Ω**。
原 U 刪 au 後 contact 有 slack，R_U(β) 全列非空；所以 Σ(G−au)=Ω，
但 u 已降三，不能稱 G−au 自己 minimal。

完整 identity 為

`J_(G−au)(β)=T_N(β;a,b,x,y₀,y₁) × R_U(β;u)`，
`J_G(β)={(t,T)∈J_(G−au)(β): t_a≠T}`。

N 全收且 R_U 非空；若原 G 拒絕 β，所有非空直積對都須相等。
故 **P_N(β)=R_U(β)={d_β}**，每個原拒絕列都成立，包括 932 的全部五列。
只在已保留完整 witnesses 的這個精確 joint 後取 root 色投影，不以 marginals 拼接。
[branches.json](branches.json) 核對 225 非空 domain 對，只有四個相同 singleton 可使 guard 全空。

E3 [adjacent_notes 的 A 列](../c5_excess_two_e3/adjacent_notes.md#2-可移植性表)
與 REPORT §3 把本身份留在一般 spoke+unary 前序之後；但 C12 的全四 retained-core
早已由原 incidence 引理排除。這是本輪記錄的停止 (c) finding；E3 檔案維持基準原樣。

### 5.2 L7：A 所有 equal pairs，不借 NΩ

若 S_a=S_b={h,k}，原 diamond 把整個連通 C 封於 hab 或 kab 三角。
只用該 face 的 a,b,h 三個原 hubs；ab、ah、bh 存在，合法外染色使三色互異。
任意拒絕 C lists 的 Gallai／三-hub 引理給 K₅，故 C 延拓每份原合法外部染色。
對 G−ax 的整份 witness，只替換 C、固定所有其他原點，即恢復原 ax。
所以 Σ(G−ax)=Σ(G)，違 ax critical。pair 不必為框邊，root 交換亦保持原 roles。
935 的原 spoke sets123／014不同；其四外色拒絕 pin 沒有被此三-hub 引理排除。

L6 已補全 A／A₂ 已知 named shapes 的前序，原 01/23、01/12 用指定三列的局部論證可用。
其他 unequal pairs 未做逐 frame 分解；沒有登記全 mixed12 子型排除。

## 6. L8：B mixed22 無 unary 的共同 leaf 排除

以下是四分支統一的任意大小紙面論證，超出原 B₂/B₃ 的01/23 faces及 B₄的{4}附件。

### 6.1 先取得原骨架、全部合法 pins 的 tightness

任一 spoke 省略 M 使一 root 降四，原 C22 必保留；後續全四 q-core 由 L2 長環排除。
若 M 拒絕 q，M 自己唯一 degree-5 q-minimal；M−另一 root 的三 contacts 互異，
two-spoke 三接點定理排除。故 **四條原 spoke omissions 各 Ω**。
同色 spokes 在某指定拒絕列冗餘，會違此 identity；三列對五條框對角各有重色，
所以 S_a、S_b 都是原框邊。任何 proper q-core只能省 spoke，故原 q-core為G、roots(5,5)。
G−C 只是 B 加兩 roots/spokes/ab，各 root 合法域至少二色，因此全部列都有合法不同色 pins。

若 S_a=S_b，sealed triangle／三-hub 如 L7 排除。下設兩原框邊不同。
若它們共用 h，共同 faces 是 hab 與不含 h 的長 face；若不相交，共同兩 faces
各包含每側恰一個端點。因此**任何共同 face 都不含某側 spoke edge 的全部兩端**。
這是兩個相鄰框區間的幾何論證，不是逐來源 key 或逐 named frame 枚舉。

對所選三列中每個 q、每個原合法 root pair (A,D)，完整 C 必阻擋該 pin。
每點 degree 四使 exact list 大小≥deg_C；連通 slack-list 法迫全部 pins 處處 tight。
故每點外鄰色互異，C 為 Gallai tree；原 B+a+b 連通排除 K₄ block。
所選三列對任何三框點至少一列重色，對任何非框 pair 至少一列重色。
所以 actual boundary 附件最多二點，二點必框邊。

### 6.2 同一 terminal odd-cycle 的 owner 類別一致

固定一個三色 q，未用色記 d。每個 adjacent spoke edge 見兩色，故 root 域
E_a={d,h_a}、E_b={d,h_b}；兩個不同色 pins (d,h_b)、(h_a,d) 永遠合法。
leaf odd-cycle private vertices 的 block list 在每份 pin 下相同；其中色 d 的 membership 為

| 原 owner 類別 | 兩 pins 的 d-membership |
| --- | --- |
| 無 owner | (1,1) |
| 只有 a | (0,1) |
| 只有 b | (1,0) |
| shared a,b | (0,0) |

四個 signatures 不同，因此同一 leaf block 的 private vertices 必有同一 owner 類。
三列的五個 boundary column signatures 單射；五個框邊的 unordered color-set signatures 亦單射。
private vertex degree_C=2：無 owner 有二框附件、單 owner 有一附件、shared 無附件。
相同 block lists 因此迫無 owner 用同一原框邊 hk，單 owner 用同一原框點 h。

若 C 自己只有一個 odd cycle，其全部至少三點都是 private；任一非空 owner 類至多兩點，
無 owner 又不可能提供 C 的 root contacts，已矛盾。
若有 cut，選兩相鄰 private u,v；C′=C−{u,v} 非空連通，原兩 cycle 端邊分別連 u,v 至 C′。

- **無 owner**：u,v,h,k 形成原 K₄。O=C′∪{a,b}∪(B−{h,k}) 連通：
  C′ 保留所有 root contacts，ab 連 roots；S_a≠S_b 使至少一 spoke 碰補框路徑。
  O 經原 cycle 端邊碰 u,v，經補框邊碰 h,k，得 K₅ 五袋。
- **只有 a**（b 對稱）：u,v 用盡 a 的兩個 C contacts，各接同一 h。
  在原 B+a+b 中有 a↝h、b↝h 兩路，只有 h 交會且各避另一 root。
  若 h 在 spoke edge 上取相應原 spoke；否則沿兩個不同框邊區間的外端向 h 取相反方向路徑。
  用 {u}、{v}、{h}、a-route−h、(b-route−h)∪C′ 作五袋。
  C′ 保留 b contacts，所以第五袋連通；ab、兩路末邊、root incidences 與 cycle 端邊給十鄰接。
- **shared**：u,v 無框附件，a,b,u,v 是原 K₄。兩 roots 的 spokes 合共至多碰四框點；
  全 B-touch 迫 C 碰剩下框點，且不經 u,v，所以 O=C′∪B 連通。
  原 spokes 與 cycle 端邊使 O 碰四個 K₄ 頂點，得 K₅。

以上 bags 只作來源非平面反證，不主張完整六角色 relation 是 minor 不變量。

### 6.3 Terminal bridge，含任意 shared 實際附件

若 v 是 private bridge leaf，deg_C(v)=1。

- 無 owner 需三個實際框附件，違三列 tightness。
- 單 owner（例如 a）需二框附件，必原框邊 hk。對每個 q，取 a=d 的合法 pin，
  exact list tight 迫 q({h,k})=q(S_a)；三列 edge signature 單射迫 {h,k}=S_a。
  但 C 固定共同 face 不含 S_a 的兩端，矛盾。
- shared v 完整 degree 四迫**恰一**實際框附件 h。令 K=C−v，非空連通；
  C22 每 root 還有一條原 contact 在 K。K 的 cut 恰兩 root 接線、原 vK bridge 與 n_B 條框邊：

  `4|K|=2|E(K)|+3+n_B`。

  所以 n_B 正奇數，K 實際碰 B。
  {a}、{b}、{v}、整份 B、整份 K 五袋兩兩相鄰：ab、av、bv、各 root spoke、
  vh、vK、剩餘兩 root contacts、K–B 給十鄰接。
  **不限定 h={4}、不使用舊十三附件 slack 縮表或 q₂/q₄ 的角色。**

C22 不可能 singleton；K₄-free Gallai C 的 terminal block 只有上述 bridges 或 odd cycles。
全部選擇均矛盾，故 B 的整個 mixed22 無 unary 子型四分支排除。

## 7. 保留缺口與停止點

| 缺口 | 精確保留範圍 | 已移除的依賴 |
| --- | --- | --- |
| G1 | J1 spoke+unary restoring whole-source exclusions；只省略 mixed11 的完整十列來源接回，四分支均缺新無列證明 | proper predecessor 只能 Ω／單拒絕，不可當 Ω |
| G2 | 五-spoke mixed11+U 的941／933／940；單 q 的 a-child仍可有同一 M−U 全四 core | 不再需要「一省略能供多個 q」身份；932已排，mixed12全排 |
| G3 | J3 binary 941／933／940 的 actual supports、共用 C 反像、完整 U schemas／joint 與 hub coverage | M 自己 q-minimal已證，932已排 |
| G4 | A unequal frames 的整型 coverage／其餘來源排除，四分支仍保留 | NΩ、a-spokeΩ、全部拒絕列U singleton、equal pairs 已證 |

不逐 key 搬舊 116/256 或 70/90 表；需要這種做法時按停止 (a) 記缺口。
本輪未證 source realization、完整新 Σ catalogue、一般 exit、K∞=K≤5 或 ε≥3。
最終停止 (c) 是 A 的過強前序依賴 finding；沒有修改 E3，也未在 finding 後繼續新 frame 分析。

## 8. 正控制、驗證命令與實際 exit code

只使用 E3 唯讀提取的**精確 E1** `/exhaustive/2/minima_by_sigma/935`、
`/exhaustive/4/minima_by_sigma/951`；原 E1 artifact SHA
`23a92b56f325bd4bd496d7e8dfb14714d8481618253f88243df4cb7916ca999e`，
每份原 record 的 canonical-JSON SHA 重新核對。完整原 vertices、edges、attachments、
rotation、accepted colorings、critical witnesses 均保存，不與 cells scratch representatives 混合。

| 實際控制 | 結果 |
| --- | --- |
| 935 完整 Σ／degrees／原 critical edges | Σ935、ε2、degree(4,5,5)、roots5/6、11/11原非框邊critical；三列假設 false |
| 935 proper-subgraph 輪廓與飽和 | 全2,048 subsets，2,047proper，19 degree-valid，只有原圖ε2；L1全部吻合 |
| 935 兩 root 各刪一spoke的全四 predecessors | 九份：四份Ω、五份minimal-q；全部是原triangle567，retained mixed兩側同contact7；逐原非框邊 q-critical witnesses保存 |
| 935 原 K=C+a leaf slack | 兩root角色、全部同色省略queries，完整K relation及避開L外色的tuple witnesses；實際F_K⊆L |
| 935 原 singleton7 外部pins | 11 pins：外鄰2色1份、3色6份、4色4份；前7全延拓、4色4份全拒絕，完整外染色保存 |
| 935 原 rootcycle 路徑 | 原S₅123、S₆014的(12/23)×(01/04)×h，共20控制；兩原路僅交h並各避另一root |
| 935 整圖共同D₅ | 原edges/rotation/全部完整染色，字面色不變、row隨φ移動，原角色保持 |
| 951 精確 warning 控制 | Σ951、16/16原邊critical；原binary{6,9}/{7,8}省略分別959/1015，均非Ω |
| 固定三列算術 | 5/5 columns與5/5 edge signatures單射；10三-spoke均有重色；180queries/3,600候選；四分支S_a域4/2/2/0 |

不讀三列的中間機制已在935**實際適用的前提**下核對：L1、全四retained-contact identity、
leaf slack、完整 guard／外色机制、共同D₅、原rootcycle paths。
935的C是incidence11 singleton、deg_C7=0，並無B22 terminal leaf或A/J3 ternary前提；
這些不適用處逐項保存，不能把空前提稱為整型排除證明的實現控制。
935的四色外鄰拒絕沒有被排除，exact Σ935完整保留。

完整重播工作目錄為 `/home/ray/developer/ai/math-task-e5`，使用系統 `python3`（全stdlib）。
下列 commands 均已實際執行：

| command | exit code |
| --- | ---: |
| `PYTHONHASHSEED=17 python3 scripts/c5_excess_two_e5_controls.py`（首次exclusive生成） | 0 |
| `python3 scripts/c5_excess_two_e5_local.py`（首次exclusive生成） | 0 |
| `PYTHONHASHSEED=17 python3 scripts/c5_excess_two_e5_branches.py`（首次exclusive生成） | 0 |
| `python3 scripts/c5_excess_two_e5_controls.py --check` | 0 |
| `PYTHONHASHSEED=17 python3 scripts/c5_excess_two_e5_controls.py --check` | 0 |
| `python3 scripts/c5_excess_two_e5_local.py --check` | 0 |
| `PYTHONHASHSEED=17 python3 scripts/c5_excess_two_e5_local.py --check` | 0 |
| `python3 scripts/c5_excess_two_e5_branches.py --check` | 0 |
| `PYTHONHASHSEED=17 python3 scripts/c5_excess_two_e5_branches.py --check` | 0 |
| 三producer再執行、不帶`--check`（預期拒絕覆寫） | 各1：FileExistsError；三个artifact SHA不變 |
| `git diff --check` | 0 |

可直接重播：

```bash
cd /home/ray/developer/ai/math-task-e5
python3 scripts/c5_excess_two_e5_controls.py --check
python3 scripts/c5_excess_two_e5_local.py --check
python3 scripts/c5_excess_two_e5_branches.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_e5_controls.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_e5_local.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_e5_branches.py --check
git diff --check
```

[validation.json](validation.json) 保存完整命令／exit codes、最終new-files清單、各檔SHA與byte數、
tracked-file零改動及worktree head確認。所有scripts與交付文件初次寫入都使用`open('x'/'xb')`；
`--check`只讀，不更新來源或artifact。沒有使用四色定理oracle、planarity oracle或來源圖枚舉。
兩個精確控制上的有限染色迴圈不接受任意來源圖作solver。

沒有重跑舊十列大表／歷史byte-check、E1 k≤5枚舉、D₈/E4或lake build；
無新增Lean theorem，紙面Gallai／K₅與任意大小coverage不能稱為Lean證明。

## 9. 紙面依據與證據層

- [E2低ε飽和與非相鄰pair](../c5_excess_one_e2/REPORT.md#3-a-ε0-的完整飽和段落)、
  [唯一degree5最小q接受兩鄰列](../../docs/c5_excess_one_subcovers.md#2-只用-t4-的-minimal-degree-5-相鄰列分離)。
- [原proper-core incidence與retained mixed身份](../../docs/c5_excess_two_mixed_core_spokes.md#3-44-且保留-mixed原形比-contact-數更受限)、
  [全四通用分類](../../docs/c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)。
- [原spoke+unary](../../docs/c5_excess_two_mixed_core_spoke_unary.md)、
  [只省略mixed](../../docs/c5_excess_two_mixed_omission.md)、
  [原五-spoke](../../docs/c5_excess_two_mixed_core_leaf_fibers.md)。
- [binary完整leaf反像](../../docs/c5_excess_two_mixed_core_four_spoke_binary.md)、
  [star](../../docs/c5_excess_two_mixed_core_four_spoke_star.md)、
  [端點hubs](../../docs/c5_excess_two_mixed_core_four_spoke_hubs.md)、
  [ternary完整joint](../../docs/c5_excess_two_mixed_core_four_spoke_ternary.md)。
- [single-spoke三接點任意大小定理](../../docs/c5_single_spoke_three_one.md)、
  [two-spoke三接點原K₅與一般異色spokes適用](../../docs/c5_two_spoke_three_contacts.md#5-second-rows-scope-and-remaining-cases)。
- [A](../../docs/c5_excess_two_mixed_core_four_spoke_mixed12.md)、
  [A₂](../../docs/c5_excess_two_mixed_core_four_spoke_mixed12_01_12.md)、
  [A₃](../../docs/c5_excess_two_mixed_core_four_spoke_mixed12_01_01.md)、
  [A₄](../../docs/c5_excess_two_mixed_core_four_spoke_mixed12_04_04.md)。
- [B tightness／owner編碼／共同faces](../../docs/c5_excess_two_mixed_core_four_spoke_mixed22.md)、
  [B₂](../../docs/c5_excess_two_mixed_core_four_spoke_mixed22_short_face.md)、
  [B₃](../../docs/c5_excess_two_mixed_core_four_spoke_mixed22_long_face.md)、
  [B₄原cut parity](../../docs/c5_excess_two_mixed_core_four_spoke_mixed22_shared4.md)、
  [三-hub引理](../../docs/c5_short_support_singleton.md#4-三-hub-引理排除未見色接點數不設上限)。

以上degree-list tightness／Gallai blockwise palettes是既有紙面外部定理依賴；
K₅ minor不可平面亦為外部標準定理。三個新Python只核對有限列／sets／原固定控制／paths，
不證disk拓撲、通用分類或未給定complete-relation coverage。沒有把舊精確933/941表當新前提下的證明。
