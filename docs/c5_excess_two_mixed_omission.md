# ε=2 唯一 mixed：省略原 mixed 必全收

**提交整理（2026-10-03）**：本頁、checker 與研究紀錄的本次提交範圍、
實際重播及整理發現見 [九輪進展紀錄](history/2026-10-03-excess-two-dual-root-progress-commit.md)。
下文的未提交字句保留當輪語境；即時提交狀態以 Git 為準。

**後續（2026-10-03）**：[單 spoke 省略的原附件化約](c5_excess_two_mixed_core_single_spoke.md)
已證省略圖若拒絕便自己是唯一 degree-5 minimal core，並得 933／941
的原總 spoke 數至多四／五。941 五-spoke 型只餘四組具名附件及 root
交換。再後續[原 leaf 色纖維與雙列 palette](c5_excess_two_mixed_core_leaf_fibers.md)
全排這些五-spoke 來源，兩候選總 spokes 都≤4；單 spoke 省略尚未全排，
原 (5,5) 核心亦保留，目前停止點見 [Kempe 導覽](c5_kempe_guide.md)。

2026-10-03，接手基準 `722bfa6`，保留前序未提交成果。接續
[兩側原 unary 省略](c5_excess_two_mixed_core_two_unary.md)的停止點。
目前入口由 [Kempe 導覽](c5_kempe_guide.md)維護，實際驗證及跨對話
摘要見 [研究紀錄](history/2026-10-03-excess-two-mixed-omission.md)。

**固定完整 Σ=933／941、Σ edge-minimal、ε=2、相鄰雙 degree-5
roots、恰一份原 mixed C 的 induced-C₅ disk 來源，若 C 的原 incidence
是 (1,1)，則省略整份原 C 後必全收 Ω。** 含 root 交換型。
933 拒絕四列、941 拒絕三列；兩者均以完整十列及整圖 D₅ 像比較。

結合前序保留 mixed 的原省略排除，**此來源的任何 minimal
rejected-row core 都不可能有 (4,4) root degrees。** Proper core
只能是 (5,4)/(4,5)，或原 G 自己仍為 (5,5) q-core。
證據為任意大小紙面化約及 Python 固定必要域、完整接合與明示
subdivisions；共同下界仍 ε≥2，未證 ε≥3，未新增 Lean theorem。

## 1. 同一原來源與省略圖

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框。
完整 Σ 是 933、941 或其整圖 D₅ 像；刪任一非框邊都嚴格擴大 Σ。
有效內部 H 非空連通，恰兩個完整 degree-5 roots z,w，其餘有效
內點完整 degree 四。原 zw 存在，H−{z,w} 恰一份原 mixed C，
其餘為原 unary。原 P_C^z={x}、P_C^w={y}，容許 x=y。
保持原分量身份、有序 contacts、ownership、實際附件、原嵌入環序
及一個共同字面色框。省略是去掉原 C 的全部頂點與 incident 邊。

令 M=G−C。M 的有效內部連通且全 degree 四；zw 是原內部 bridge，
因為其他原分量均只接一個 root。若 M 拒絕 q，則 q 必是 singleton
列；minimal q-core 的 degree-4 飽和沿連通內部傳播，迫該 core
就是整張 M。M 繼承 disk、induced boundary 與全部 T4。

在 M 自己套用 [全 degree-4 合成](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)，
得到 Σ(M)=Ω∖{q}，內部只能是偶數頂點路徑、單 triangle 加原路徑枝，
或直接 bridge 相接的兩個互斥 triangles。整張來源共同搬運
q 至 q₄=01012，所有 roots、C、原附件及十列同步搬動。
雙 triangle 時 zw 必是其唯一原 bridge；單 triangle 時兩 roots
在同一原枝的相鄰位置，或 triangle parent 與原枝首點。
不是將兩個 roots 放到同一 triangle 上。

## 2. 兩側全圖及原 C 的完整接合

M−zw 的兩個原內部分量記 H_z、H_w，各包含自己的 root。
固定同一 β 後，保存兩側所有原 contacts 的完整 tuple relations
及各自全圖 coloring witnesses。兩側只共用固定 B，故它們的
聯合 relation 恰是這兩份**全圖 relation** 的字面接合；這一步
由互斥原頂點集及沒有其他跨側邊負責。

先從完整聯合 tuples 取得 root-pair relation L_β，再過濾原 zw：

\[
K_β=\{(a,b)\in L_β:a\ne b\}.
\tag{1}
\]

兩側原 root 邊刪除後各有一份 slack，逆序 spanning-tree 貪婪染色
給兩側 relation 非空；q 列的 K_q 為空，其餘九列非空。
這裡可以使用兩側全圖的接合，不能用原 C 的 endpoint marginals。

令 T_C(β) 是原 C 在有序角色 (x,y) 的完整 relation，每份 tuple
附原 C 全部內點的一份 witness。x=y 時只保留一個原頂點座標，
角色 relation 才寫成 (c,c)。原 G 的精確接回為

\[
\mathcal R_G(β)=
\{(t,u):t\in\mathcal T_{M-zw}(β),\ u\in T_C(β),
\ t_z\ne t_w,\ t_z\ne u_x,\ t_w\ne u_y\}.
\tag{2}
\]

每個 t、u 的原圖 witness 同步共用 B，檢查這三條原邊後即能拼接。
定義原 C 的二維禁對

\[
F_C(β)=\{(a,b)\in U^2:\nexists(c,d)\in T_C(β),\ a\ne c,
b\ne d\}.
\]

只有在完整式 (2) 之後才可寫

\[
β\in\Sigma(G)\iff K_β\setminus F_C(β)\ne\varnothing.
\tag{3}
\]

## 3. 任意大小原 mixed 的容量與同一支援

沿用 [逐欄／逐列容量](c5_mixed_capacity_contacts.md#2-固定另一-root-後的容量界)：
固定 w=b 時，原 x 留有 slack，C 的完整染色非空，故 F_C 的第 b
欄至多一格；交換 roots 得每列至多一格。兩個不同 contacts 時，
若 F 有 (a,b)、(c,d) 兩格，每份原 tuple 同時受兩格限制，迫
T_C={(a,d),(c,b)}；不能再有第三禁對。共鄰 contact 時，由兩份
slack 得至少兩個可取色；只有可取色恰兩個時有兩個非對角禁對。
任意大小、blocks、原 bridges 與旁支都保留，詳見
[各一 incidence 引理](c5_mixed_capacity_contacts.md#5-各一-incidence至多兩個禁對與新的對稱-residual)。

因此 F_C 是空、單格，或兩格且 rows／columns 均互異，總共
**89 份必要代數選項**。其中包含未證原 C 可實現的選項；不按列
任意另選一份原分量。Checker 另對全部 65,536 份二元原 tuple
子集重算禁對，65,431 份滿足 row／column 容量一者恰覆蓋這 89
份 F；這是 relation 代數控制，不是來源圖枚舉。

固定唯一原實際支援 S=N_B(C)。若 p|S=π(q|S)，將原 C 的**全部**
染色施以 π，便有 T_C(p)=πT_C(q)、F_C(p)=πF_C(q)。所以每個
local equality shape 只能有同一份禁對選擇，而且必被代表支援色
的 stabilizer 固定。所有逐列搬運均用同一字面四色框。

對全部 32 份具名 S，checker 保存各 shape 的完整 89 選項篩選及
全部逐列 transports。式 (3) 對同一 shape 的選項取交；交集為空
時保存所有相衝突的具名列及允許選項。非空時保存一份完整
shape assignment，再直接對全部十列 K_β 核對式 (3)。這只是
必要放寬，不是原 C 的實現證書。

## 4. 保留相鄰 roots 的任意長度覆蓋

沿用 [原路徑附件分類](c5_excess_two_path_edge.md#2-分類留下的共同原框鄰點)、
[單 triangle 原枝分類](c5_triangle_path_reduction.md)與
[雙 triangle 分類](c5_two_triangle_blocks.md)。保留原 z,w 為
singleton branch sets，並始終保留兩者間的原 zw。

在附件恆定的每個原 run 中，以 z,w 切出未標記區段。長度零
保持零，正奇長度縮成一點，正偶長度縮成兩點。單 triangle 的
單 run 原長度為奇數，保留至多兩個相鄰 markers 後只需長度
1、3、5；兩-run 枝的 X 首點保留，Y 的正偶長度只需 2、4、6。
原路徑的每個 run 為正偶數，亦只需 2、4、6；無 marker 的
run 只用其最短正奇／偶代表。原 leaf 與 triangle 頂點保持。

每個 run 在任意 β 的可用色集 A 至少有兩色。兩側 endpoint
固定後，區段的精確 transfer R_t 有 R_(t+2)=R_t，t≥1；零
區段是另外一份直接邊關係。|A|=2 由交替染色證，|A|≥3 時任意
正長度的兩側 endpoint 條件相同。因 zw 的兩端被標記且原本相鄰，
沒有未標記區段跨過 zw；刪除或保留該邊都保持完整 root-pair
relation。任何縮減都在原路徑內收縮同附件的連通、互斥 branch sets。

因此任意原 M 有一份 boundary 固定的必要 minor M*，同時保持
M 及 M−zw 的完整聯合 root-pair relation。接回原 C 只涉及這兩個
原座標，式 (2)–(3) 仍精確。其他 contacts 可能變為非 singleton
branch sets；長、短圖各自保存完整 contacts 與 joint tuples，
不宣稱不同 contact 座標跨縮減相等。

| 原核心家族 | 必要具名核心／原 bridge |
| --- | ---: |
| 單 triangle、單 run 枝 | 160 |
| 單 triangle、兩 runs 枝 | 64 |
| 原偶數路徑 | 56 |
| 雙 triangle、直接 bridge | 64 |
| 合計 | 344 |

每份必要圖都直接重算全 degree 四、q₄-critical witnesses、T4 與
Σ=1022。雙 triangle 由原 128 份完整圖的實際染色重算後取 64
份，沒有以舊 Σ flag 決定收錄；原輸入 hashes 與來源身份明列。
這是既有任意大小分類的 marked 必要域，不是新來源 catalogue。

## 5. 同一原 C 收縮星與全部比較結果

對 S₄ 相容的**同一原 S**，僅為拓撲反證，把整份連通原 C
收縮成 c，保留 zc、wc 及到全部原 S 的邊。它與 M 的所有
branch sets 及 B 互斥，所以能與 §4 同時在原 G 進行。得到

\[
J=M^*+zc+wc+\{cb:b\in S\}.
\tag{4}
\]

這不保持 C 的染色、degree 或 Σ，不能把 c 當作染色替換。
在指定外框外側加 apex α 連全 B，disk 來源必使 J+α 平面。
每份相容的必要 J+α 都保存明示 K₅／K₃,₃ subdivision：逐路徑
核對實際邊、簡單性、內點互斥、branch 頂點與全部九／十份鄰接。
反證沿同源 minor 傳遞，不依賴 planarity boolean 作證書。

344 份核心對兩候選各五個整圖 D₅ 像，共 **3,440** 次比較：

| 排除步驟 | 比較數 |
| --- | ---: |
| 目標接受的列在原 M 已空 | 1,032 |
| 目標拒絕列的完整 K 超過原 C 禁對容量 | 2,122 |
| 剩餘進入同一原支援階段 | 286 |

286×32=9,152 份具名支援查詢中，**8,508** 份跨列不相容；
其餘 **644** 份全部有非 disk 收縮星證書。去掉同一 core／S
在不同候選比較中的重複，共 **188 份明示 subdivisions：178
份 K₃,₃、10 份 K₅**。零殘留，故反設 M 拒絕不成立：

\[
\boxed{\Sigma(G-C)=\Omega.}
\tag{5}
\]

結合 [原省略身份表](c5_excess_two_mixed_core_spokes.md#2-全部-proper-core-的具名省略表)
及 [保留 mixed 全排除](c5_excess_two_mixed_core_two_unary.md)，任何
(4,4) rejected-row core 均不可能；不能由此排除所有 ε=2 來源。

## 6. 證書、控制、重播與停止點

[Checker](../scripts/c5_excess_two_mixed_omission.py)／
[artifact](../artifacts/c5_excess_two_mixed_omission/observations.json) 保存
344 原核心的完整邊、實際附件、原 unary 身份／ownership／contacts、
兩側全圖 relations、joint tuples 與完整 witnesses、全部目標比較、
32 固定支援的 transports、逐查詢 conflicts／assignments 及 subdivisions。

344 張固定原長圖將每個正未標記區段增長兩點，保持原 roots
為 singleton；保存全部收縮 branch sets，quotient 邊集與原 zw
皆直接核對。6,880 次刪／留 zw 的完整 root-pair 比較相等，
每張長圖另保存自己的全部 contact joint tuples 與全圖 witnesses。
每家族各取三份最大的控制圖，共 **1,920 次** pinned 原色對回溯
逐纖維核對，包含空纖維；雙 triangle 沿用固定原六內點，沒有原 run；
最長固定長圖有 22 個頂點，包括 B。任意長度證明仍由 §4 負責。

另有 **20 張實際原 C 接回圖／200 次十列完整接合**，包括 shared
singleton、shared edge、不同 contacts 的 edge／path／triangle；
原 C 的全部內點、實際支援、contacts 及全圖 coloring witnesses
明列。976 次同支援的原完整 C-relation transport 比較通過。
控制不宣稱 disk、Σ-minimal 或任意 C 形狀分類。

實際 marginal 負控制為 form 224、列 4：core K={(3,1)}，原 shared
singleton 的角色 T_C={(1,1),(3,3)}。兩 marginals 都為 {1,3}，
相乘會誤造可接回的 (1,3)，實際完整接合卻為空；附兩部分原
coloring witnesses。沒有用二維禁對代替其原來源的完整 relation。

```bash
uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_omission.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_omission.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

實際重播及未重跑範圍見研究紀錄。沿用既有 Gallai／degree-list
外部定理與 degree-4 分類、紙面及有限 topology 信任範圍；Python
只證明固定必要域、完整關係代數與明示 minors，沒有新外部 oracle
或 Lean theorem。`lake build` 不形式化式 (4)–(5)。

**停止點：相鄰、恰一份原 mixed 的 (4,4) 核心分支全部排除。**
下一窄入口是 (5,4)/(4,5) 的原單容量因子省略，先分析省略一條
原 spoke、接回後 root 由四升五的子型；在省略圖自己的唯一
degree-5 定理與完整 relation 下作同源接回。G 自己是 (5,5)
q-core 時不能套唯一 degree-5 分離定理。多 mixed、no-mixed、
非相鄰 roots 與 unary 側例外仍保留；共同 ε≥2 不變，未證
ε≥3、一般出口、來源實現或 K∞=K≤5。
