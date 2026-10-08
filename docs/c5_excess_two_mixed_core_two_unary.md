# ε=2 唯一 mixed：兩側原 unary 省略全收

**後續稽核（2026-10-07）。** [指定四份排除稽核](../audits/2026-10-07-c44pp-mixed-audit/REPORT.md)
已核對本頁共同root-pair接合、雙支援constraints／UNSAT proofs與同源雙收縮星；
沿用上游分類及原信任界線，未重稽核全部上游枚舉，也不完成E5要求的新證明。
下文保留當輪結果與重播紀錄。

**提交整理（2026-10-03）**：本頁、checker 與研究紀錄的本次提交範圍、
實際重播及整理發現見 [九輪進展紀錄](history/2026-10-03-excess-two-dual-root-progress-commit.md)。
下文的未提交字句保留當輪語境；即時提交狀態以 Git 為準。

**後續（2026-10-03）**：[省略原 mixed 必全收](c5_excess_two_mixed_omission.md)
已排除本頁留下的最後 (4,4) 身份。相鄰且恰一份 mixed 時，任何
minimal rejected-row core 都不可能有 (4,4) root degrees；
(5,4)/(4,5) 及原 G 的 (5,5) 核心仍保留。下文保留當輪語境，
共同 ε≥2 不變，目前入口由 Kempe 導覽維護。

2026-10-03，接手基準 `722bfa6`，保留前序未提交成果。接續
[原 spoke＋unary 省略](c5_excess_two_mixed_core_spoke_unary.md)的停止點。
目前入口由 [Kempe 導覽](c5_kempe_guide.md)維護，實際驗證及交接摘要見
[研究紀錄](history/2026-10-03-excess-two-mixed-core-two-unary.md)。

**固定完整 Σ=933／941、Σ edge-minimal、ε=2、相鄰雙 degree-5 roots、
恰一份原 mixed 的 induced-C₅ disk 來源，兩側各省略一份原單接點
unary U、V，所得原圖必全收 Ω。** 含 root 交換型。

結合雙 spoke 及 spoke＋unary 的前序結果，**任何 minimal rejected-row
core，若兩 roots 的 degree 都降至四，必省略唯一原 mixed；不能保留它。**
這完成 (4,4) 保留 mixed 的全部原省略身份。證據是任意大小紙面接合／
minor 化約及 Python 固定必要域證書；共同下界仍 ε≥2，未證 ε≥3，
未新增 Lean theorem。

## 1. 同一原來源及反設核心

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框。
完整 Σ 為 933、941 或其整圖 D₅ 像，每條非框邊刪除都嚴格擴大 Σ。
有效內部 H 非空連通，恰兩個完整 degree-5 roots z,w，其他有效
內點完整 degree 四。原 zw 存在，H−{z,w} 恰一份原 mixed C，
其餘為原 unary。保持原分量身份、有序 contacts、全部實際附件、
ownership、原嵌入環序及同一字面色框。

令 U 是原 z-unary，唯一 root-contact 為 u；V 是原 w-unary，
唯一 root-contact 為 v。兩份互異且頂點互斥。省略表示去掉整份
原分量及其全部 incident 邊，不是只刪原 zu、wv。記

\[
M=G-U-V.
\]

M 繼承 disk、induced boundary 與全部 T4。原 mixed 和 zw 保留，
故有效內部仍連通，且所有有效內點在 M 自己的完整 degree 都為四。
若 M 未全收，它必拒絕 singleton 列 q；任何 minimal q-core 的
degree-4 飽和沿連通內部傳播，使該 core 等於整張 M。

在 M 自己套用 [全 degree-4 合成](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)
及 [原 mixed 形狀限制](c5_excess_two_mixed_core_spokes.md#3-44-且保留-mixed原形比-contact-數更受限)：
原 C 的兩側 contacts 必同為 {x}，原 z,w,x 是 triangle；C 只能
是從 x 起的原路徑，或 x 經原直接 bridge 接第二個 triangle。
保留的 unary 都是原單接點路徑枝，每側至多一份。

對整張來源只作一次 D₅／S₄ 搬運，使 q=q₄=01012。原 U、V、
roots、附件及十列都同步搬動；不能為不同原分量獨立挑色框。

## 2. 兩份原非空 relation 的完整接合

對任意 proper boundary coloring β，定義

\[
S_U(β)=\{f(u):f\text{ 是原 }U\text{ 的完整延拓}\},\quad
S_V(β)=\{g(v):g\text{ 是原 }V\text{ 的完整延拓}\}.
\]

去掉原 root 邊後，contact 的 list 至少有 deg_U(u)+1 色，其餘
點至少有各自的內部 degree 色；以 contact 為根的 spanning-tree
逆序貪婪染色證 S_U(β)、S_V(β) 均非空。任意大小、blocks、
原路徑與全部附件都保留，沿用 [原 unary slack 證明](c5_excess_two_spoke_unary.md#2-原-v-的-relation-非空不需分類其大小或支援)。

令 P 依序包含 z,w 及所有保留原分量 contacts，共鄰 x 只佔一欄；
\(\mathcal T_β\) 是 M 的完整 P-tuple relation。原 G 的完整接合恰為

\[
\mathcal R_G(β;P,u,v)=
\{(t,a,d):t\in\mathcal T_β,\ a\in S_U(β),\ d\in S_V(β),
                 \ t_z\ne a,\ t_w\ne d\}.\tag{1}
\]

每份 t、a、d 都有各自原圖的完整 witness，三部分只共用固定 B；
檢查兩條原 root 邊後便可拼接。不是把 roots 的 marginals 相乘。

完整 tuple 算出後，才取聯合 root-pair relation
\(K_β=\{(t_z,t_w):t\in\mathcal T_β\}\)。令

\[
F_U(β)=\begin{cases}\{a\},&S_U(β)=\{a\},\\
\varnothing,&|S_U(β)|\ge2,
\end{cases}
\]

V 同理。式 (1) 等價於

\[
β\in\Sigma(G)\iff
\exists(c,d)\in K_β:\quad c\notin F_U(β),\ d\notin F_V(β).\tag{2}
\]

同一 pair 的兩座標都必存活。兩側各有存活色不保證有存活 pair。
Checker 保存兩個 endpoint 自由座標的完整接合算子；必把它們
限制到真實 S_U、S_V 才得到式 (1)。Core coloring indices 只證
M 的完整染色，不冒充 U、V 的原內點 witnesses。

## 3. 兩份固定支援的跨列換色限制

固定原實際支援 S=N_B(U)、T=N_B(V)。若 p|S=π(q|S)，將
原 U 的整份染色同時置換，給 S_U(p)=π S_U(q) 與 F_U(p)=π F_U(q)；
V 對 T 同理。π 使用同一字面四色座標。

每份原 unary 的空／singleton 禁色是其支援上 local equality shape
的同一個函數。每個 shape 選一列代表，singleton 色須被該代表
的支援色 stabilizer 固定：看到至多兩色時只能選已見色，看到
三或四色時可選任一 literal 色；空禁色是必要代數選項。

Checker 保存兩側各 32 份具名支援、local shapes 及全部逐列
transport。對每份支援對 (S,T)，每列式 (2) 給兩個 shape 變數間
的 binary constraint；同一 shape 對若重複出現，要求取交。
不能先獨立解兩側再任意拼接，也不能逐列另選原支援。

每份不相容查詢附有限 UNSAT proof：逐 constraint 精確刪去
沒有對側可用值的選項，直到一份 constraint 無可用 pair。
Verifier 直接重算每步的所有支援 pairs，不呼叫搜尋 solver。
本輪全部 368,859 份互異 UNSAT 查詢都由此 propagation 封閉，
無需分支；checker 仍完整支援並核對有限分支 proof tree。
相容查詢附全部 shape 的一份 assignment，再直接對十列原 K_β
核對式 (2)。相容僅是必要放寬，不宣稱有同圖 unary 實現。

## 4. 同源雙收縮星 minor 與任意大小傳遞

對相容的同一原 S,T，只為拓撲反證，同時把原連通 U、V 各
收縮成 a,d；保留原 za、wd 及到各自全部實際支援的邊。
U、V 互斥，且都不含 B 或 M 的內點。此收縮不保持 unary
色關係、degree 或完整 Σ，不能拿來當染色替換。

M 的原 triangle 路徑枝使用前輪相同 run 化約：單 run 的正奇長度
縮成一個非葉點；兩 runs 保留 X,Y,Y,leaf。原 z,w 都在 triangle
上，故是 singleton branch sets；其餘 branch sets 沿原路徑連通、
互斥，保留 B。這一步既是 boundary 固定 minor，又保持原
triangle／roots 的完整聯合 relation，詳見 [前輪傳遞證明](c5_excess_two_mixed_core_spokes.md#4-雙-spoke-省略的任意大小覆蓋)。

兩步可以在同一原 G 同時進行，給必要 minor

\[
J=M^*+za+wd+\{ab:b\in S\}+\{db:b\in T\}.\tag{3}
\]

在指定 disk 外側加只連五框點的 apex h，真正來源必使 J+h 平面。
對每份具名 core／原 root 邊，將所有相容支援對依包含關係取極小者；
每份實際支援對都保留並指向一份較小支援對的明示 subdivision。
這只是從同一收縮 minor **刪去多餘支援邊**，沒有換掉原 S,T，
亦不以較小支援重新選禁色或重算染色。

3,180 份較小支援對全部有 K₅／K₃,₃ subdivision。Verifier 核對
每條路徑的實際 minor 邊、簡單性、互斥內點、branch 頂點及
全部九／十個鄰接，並核對每份實際支援包含對應較小支援。
因此原 G 不可能是 disk。任意長度傳遞由互斥連通 branch sets
與 minor 傳遞負責，並非把有限圖的 Σ 當成任意來源分類。

## 5. 固定必要域及結果

沿用 126 份必要正常形：十八份帶枝單 triangle、八份兩-run、
36 份裸 triangle T4 必要支援、64 份直接-bridge 雙 triangle。
共有 570 份具名原 root 邊。裸 triangle 未先篩 disk，其放寬域
只會增加待排除案例。原 q₄-criticality、完整邊集及附件均重算。

對 933／941 各五個 D₅ 像比較：

| 目標 | 比較數 | 目標接受列已空 | 任意兩份非空 unary 都接受拒絕列 | 固定支援階段 |
| --- | ---: | ---: | ---: | ---: |
| 933 | 2,850 | 570 | 1,084 | 1,196 |
| 941 | 2,850 | 1,140 | 773 | 937 |

2,133 個殘留各覆蓋全部 1,024 支援對，共 2,184,192 次必要比較：

| 判定 | 次數 | 剩餘 |
| --- | ---: | ---: |
| 同原支援的雙 shape functions 不相容 | 2,083,333 | 0 |
| S₄ 相容，但同源雙收縮星 minor 非 disk | 100,859 | 0 |

相同字面 root-pair relation／target 共享計算，實際 solver 執行
377×1,024=386,048 份互異支援查詢；368,859 份 UNSAT proofs，
17,189 份必要相容 assignments。這種計算共享不改動原圖或接點身份。
每份 core 的相容原支援對去掉候選 mask 重複後共 43,265 份，
由 **3,176 份 K₃,₃、4 份 K₅** 證書覆蓋，零殘留。

故反設 M 未全收不成立，在 §1 全部前提下得到

\[
\boxed{\Sigma(G-U_z-V_w)=\Omega.}\tag{4}
\]

結合 [原省略身份表](c5_excess_two_mixed_core_spokes.md#2-全部-proper-core-的具名省略表)、
雙 spoke 及 spoke＋unary 排除，所有 (4,4) 且保留原 mixed 的
minimal rejected-row cores 均不可能。若仍有 (4,4) core，必恰只
省略原 C，且 C 的 incidence 向量是 (1,1)。

## 6. 完整證書、控制、重播與停止點

[Checker](../scripts/c5_excess_two_mixed_core_two_unary.py)／
[artifact](../artifacts/c5_excess_two_mixed_core_two_unary/observations.json)
保存原 core 邊、全部原 contacts／attachments／support、ownership、
完整 tuples 及全染色 witnesses、兩欄接合算子、全部固定支援 transport、
逐查詢 UNSAT proofs／assignments、每份具名實際支援到 minor 的映射
與全部 subdivision paths；空纖維明列。

5,700 次完整 core／自由 endpoint 算子與獨立全圖回溯一致。
逐 core 列核對全部 15×15 份非空 endpoint relation，合計
1,282,500 次完整雙接合控制。26 張固定原長圖保存自己的完整
components、附件、branch sets、contact tuples 及全染色 witnesses；
780 次跨縮減 root-pair 比較相等。其他 contacts 不宣稱跨縮減為
同一座標，亦不以 quotient coloring 冒充原長圖染色。

另保存 64 張實際接上兩份 singleton／edge／path／triangle unary
的原圖、640 次完整十列接合與全圖回溯比較；兩份原 unary 的
完整邊、附件、endpoint relations 與原全圖 witnesses 均明列。
這些是染色控制，不宣稱 disk 或 Σ-minimal。

負控制保存 form 0、原 roots (5,7)、target 934 的逐列自由禁色
schedule；它能在算子中匹配目標，卻無符合雙固定支援與 disk
必要 minor 的原 U、V。不能將這份自由 schedule 當成來源。

```bash
uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_two_unary.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_two_unary.py --check
python3 scripts/c5_excess_two_mixed_core_spokes.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_path_reduction.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

實際執行及未重播範圍見 [本輪紀錄](history/2026-10-03-excess-two-mixed-core-two-unary.md)。
全 degree-4 任意大小分類沿用外部 degree-list／Gallai 定理、既有
紙面與有限 topology 證書；新接合／支援 transport／minor 傳遞
屬紙面證明，新 Python 證固定必要域。`lake build` 未形式化本頁。

**停止點：** 唯一 mixed 的 (4,4) 保留 core 全部省略身份已封閉。
下一窄題是只省略原 mixed C，C 的兩側 contacts 各一份，保留
原 C 的完整二接點 relation、兩份原 root 側全圖 relation、全部
實際支援與同一色框，再接回 C 及原 zw；不能用 C 的 marginals。

(5,4)/(4,5)、G 自己為 (5,5) q-core、多 mixed、no-mixed、
非相鄰 roots／unary 側例外仍保留。未證全部 ε=2 排除、ε≥3、
一般出口、來源實現或 `K∞=K≤5`。
