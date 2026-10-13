# N2 原55：一 long 的末端 block 與固定 root 接回

**後續（2026-10-13，BASE 243a125）**：[N2-BRIDGE](c5_excess_two_n2_bridge.md)
另排932，完成原E4完整來源契約的廣義N2；E-ARC2仍OPEN，未新增Lean證明。
以下各輪證明與停止點保留當時語境。

**後續（2026-10-13，BASE 3097ef5）**：[同來源 LL-CUT+diag](c5_excess_two_n2_ll_cut.md)
已排指定完整Σ契約的最後 `(2,0)`，九格全覆蓋；基本LL-CUT、較廣N2／E-ARC2仍OPEN。
下文保留原輪證明、有限控制及停止點。

2026-10-13。基準 `19209f4cf68261fdce5e84a7804cfe04ae0957bf`；
[BASE](../audits/2026-10-13-n2-one-long/BASE.json)保存十九份原輸入及 SHA。
目前入口見 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)。
本頁已納入[2026-10-13整理發布](history/2026-10-13-progress-publish.md)；
下文驗證與原audit的發布狀態保留獨立交付當時語境。

**定理 OL：完整下述 N2 原55來源不存在 `(ℓ,u)=(1,0)`。**
證明對任意原 long 長度成立：先排全部末端奇環，再把末端 bridges 收窄到兩份
具名 spoke 配置，最後固定一個 root，完整染回另一 root 與 short，再接回 long。
沒有替換原圖，也不需要列舉內部 cactus 或假設大小下界。

結合既有含 U 排除，原九格有八格覆蓋；**完整原55只剩 `(2,0)`**。
父 N2、E-ARC2、N1／相鄰／單-root例外與契約外來源仍 OPEN。
證據是沿用 Gallai 輸入的無界紙面證明、獨立審閱及完整 fibres 有限校準；
未新增 Lean theorem，有限控制沒有實現完整目標來源。

## 1. 精確原來源與全部先驗縮減

沿用 [三列 diagonal §1](c5_excess_two_n2_diagonal_three_row.md#1-完整來源契約)、
[原55統一](c5_excess_two_n2_residual_unification.md)及
[含 U closure](c5_excess_two_n2_unary_diff_closure.md)的完整契約：

- G 是有限簡單 planar disk，原有序 induced 外框 `B=(b₀,…,b₄)`；完整
  `Σ=933/941` 或整圖共同 D₅ 像，T4 全收，每條非框邊 Σ-critical，`ε=2`。
- 有效 `H=G−B` 連通、full B-touch；恰兩個非相鄰完整 degree5 roots `r,s`，
  其餘有效內點完整 degree4。自由孤立座標不計入有效 H，四色乘積因子仍保留。
- `H−{r,s}` 的原分量恰為 long mixed L 與 short mixed S，沒有 unary。
  兩份皆 one-sided，S 的實際支援非空且包含於一条原框邊；
  L 的實際支援至少三點，恰為原盾弧的全部頂點。
- 所有原頂點、ordered/shared contacts、各 contact 的 owner、實際框附件、
  內邊、rotation、bridges、旁支及同一字面色框均固定；不獨立正規化兩份 piece。

共同搬運整份來源後，固定

\[
I=\{0,1,3\},\quad q_0=01212,\quad q_1=01202,\quad q_3=01021,
\qquad D=3.
\]

三列均被原 G 拒絕。完整 Σ 前提保留，沒有把只拒這三列的任意圖當成来源。

| 已採納來源結果 | 本輪保留的精確內容 |
| --- | --- |
| [44／45／54與spoke排除](c5_excess_two_arc_spoke_closure.md) | 每個拒絕列以有效原 G 自己作55 minimal core；任一非框邊刪除全收十列；每個內點含 roots 至多附兩個相鄰框點 |
| [原 block／度二附件](c5_excess_two_arc_size_bound.md) | 無 U 時 H 二連通；L、S 的 blocks 只有 bridges／奇環；多 block 的每個 leaf block 有私有 root-contact；不同 H 內度二點附不同原框邊 |
| [先前 long 排除](c5_excess_two_n2_long_synchrony.md) | L 有 shared contact、`k_L≤3`、或 L 是所有 contacts 都為葉的 tree 時已排；故本輪可設無 shared contact、`k_L≥4`，原殘留含 cycle 或 contact cutpoint |
| [盾弧](c5_unary_shield_budget.md) | 两份盾弧邊互斥；其餘 H 的支援避開 L 盾弧內點；S 若 singleton support，既有三-hub 引理迫 `t=0` |
| [N-diagonal](../artifacts/c5_excess_two_e4/REPORT.md#41-新引理-n-diagonal只指定-nc-的局部-list-版本) | 對每個 proper q、每個色 a，S 在原 pins `(a,a)` 有完整 lift，包含 singleton support／shared contacts |

令 `T_r=N_B(r), T_s=N_B(s), T=T_r∪T_s`，`t=|T_r|+|T_s|≤4`。
`k_C^r,k_C^s` 一律計原 root incidences。原度數逐側給

\[
t_r+k_L^r+k_S^r=5,\quad t_s+k_L^s+k_S^s=5,
\quad k_L+k_S=10-t,\quad k_S\ge2.
\]

共同原55容量沒有消失：對每個原拒絕列、任一 root 方向與合法對側 pin，
無 U 時 `|E_r|=k_L^r+k_S^r−1`，且 `δ+o+λ=1`，各項非負。
不能把不同列的這一單位相加。本輪最後改以完整外側的 strict slack 使用同一度數式。
既有 `|H|=35−3t−Δ, Δ≥0` 與有限 `|H|≥10` 均保留，但**不用於本證明**。

## 2. 全色共同接回與具名支援閉包

令 `W_L^r` 是 L 中原 r-contacts 的全部實際框鄰居聯集，s 側類同；
`W=W_L^r∪W_L^s`。聯集只用來找實際碰色點，不取代原附件或 fibres。

**引理 OL-C（共同同色接回）。** 若某 `i∈I`、某色
`a∈q_i(W)\q_i(T)`，則原 G 接受 `q_i`。

選一個確實同接 root 及框點 h 的原 L 頂點 v，滿足 `q_i(h)=a`。
固定兩個原 roots 同色 a；原 rs 不存在，全部 spokes 合法。
v 的兩個不同原外鄰同色，degree4 lists 在 v 有 strict slack，其餘點至少有
內度數個色。沿以 v 為根的原 spanning tree 逆序貪婪染滿全部 L。
同一列、同一 pins 的 S 完整 lift 由 N-diagonal 給出，遂接成 G 的完整 lift。
這是完整同列矛盾，沒有拼接不同列或僅比較 pair marginals。

所以來源必要條件為

\[
q_i(W)\subseteq q_i(T)\quad(i\in I),\qquad
W\subseteq\operatorname{cl}_I(T)
:=\{b\in B:\forall i\in I,\ q_i(b)\in q_i(T)\}.
\]

五個具名框點的三列 signatures 分別為
`000,111,220,102,221`，彼此不同。直接由這張字面表得到完整公式

\[
\operatorname{cl}_I(T)=T
\cup\bigl(\{b_2\}:\{b_0,b_4\}\subseteq T\bigr)
\cup\bigl(\{b_4\}:\{b_1,b_2\}\subseteq T\bigr).
\tag{C}
\]

括號表示條件成立才加入該 singleton；不作迭代閉包。
`cl_I(T)\T` 至多一點，若非空只能是 `b₂` 或 `b₄`。
這是五個固定具名框點的有限算術，並非原來源或內部圖形的枚舉。

## 3. 永久 diagonal 不容許任何末端奇環

S 三列都接受 `(D,D)`，原 spokes 亦合法。因此反設來源存在，就有
`F_L(q_i;D,D)=∅` 對全部 `i∈I` 成立。
沿用 [Gallai degree-list 輸入](c5_excess_two_n2_diagonal_three_row.md#1-完整來源契約)：
每列 lists tight，且是 incident block palettes 的互斥聯集。
以下只從這個必要條件及原平面圖取矛盾。

L 不會只有一個 block。singleton／bridge 與無 shared contact、`k_L≥4` 不合；
若是單一奇環，至少一個 contact 的 list 排除 D，迫該 cycle palette 排除 D，
故所有點都須是 contacts。每點恰一個框附件；在每一指定列中，各點同有該列的
cycle palette，配合上述 signature
單射迫全部附件同一框點，違反 long。

現在取任一 leaf cycle K。它有私有 contact。該 contact 的 list 不含 D，
所以 K 的 palette 不含 D；任何普通私有點的 list 卻含 D，故**全部私有點都是
contacts**，且每點恰附一個框點。每一指定列內私有點的 palette 相同，
加上三列 signature 單射，再次迫這些框點全部為同一 h。
取兩個相鄰私有點 p,q；它們各接一個原 root，均附 h。
`L′=L−{p,q}` 仍連通，p、q 各有一個 cycle 鄰居在 L′。

令 `R={r,s}∪S`，這是原連通集合；取 `a∈N_B(R)`，存在性由 S 支援非空。

- 若 `a=h`，五個 bags 為 `{p},{q},{h},R,L′∪(B−h)`。
  最後一袋由 L 的 h 外附件連通；R 與最後一袋有剩餘 L contact 邊
  （原 `k_L≥4`，只移去兩個 contacts）。其餘九對鄰接由原 cycle、root、框邊及附件給出。
- 若 `a≠h`，取 `b∈S_L\{a,h}`，long 保證存在且附件仍在 L′。
  原 B 的兩條 a–h 弧中，記 P 為不含 b 的那條，Q 為含 b 的那條。
  五個 bags 為

  ` {p}, {q}, {h}, R∪(V(P)−{h}), L′∪(V(Q)−{a,h}) `。

  第四袋由原 R–a 附件連通；第五袋由原 L′–b 附件連通。
  h 分別鄰第四、第五袋，Q 在 a 的首邊使第四、第五袋相鄰。
  p,q 彼此相鄰，並各以原附件、root 邊、剩餘 cycle 邊鄰另外三袋。

所有 bags 互斥連通，十對都有原邊，故原 G 含 K₅ minor，矛盾。
論證容許任意奇環長度、任意剩餘 block chain 及任意 contact ownership；
沒有先把奇環當 triangle，也沒有給 minor 指派原 Σ。
所以 **L 的全部 leaf blocks 必為 bridges**。

## 4. 末端 bridge 迫兩個具名四-spoke 配置

取 leaf bridge 的私有端 p。它恰一個 root 邊及兩個框附件，附件為原框邊
`e=ab`；所以 `e⊆W⊆cl_I(T)`。不同 leaf endpoints 是 H 內度二點，故它們的
原框邊附件彼此不同。

**引理 OL-B。** 不可能 `e⊆T`。

否則取五個原 bags

` {p}, {a}, {b}, R={r,s}∪S, F=(L−p)∪(B−{a,b}) `。

L−p 連通，long 的 ab 外附件使 F 連通；R−a、R−b 是原 spokes，
R−F 是剩餘 contact 邊。p 鄰另外四袋，a−b 是原框邊，
F−a、F−b 由補框弧的兩端邊給出，故又是原 K₅。∎

於是每個 leaf attachment edge 必含 `cl_I(T)\T` 中的唯一點 h。
有限 block-cut tree 至少兩葉；一個 C₅ 點僅有兩條 incident edges，附件單射迫
L **恰兩個 leaf blocks**，其附件正是 h 的兩條原框邊。
這覆蓋任意內部鏈與 cycles；並未假設內部只能有幾個 blocks。

公式 (C) 加上 h 的兩個鄰點亦須屬 cl，僅容許：

| h | T | 兩份 leaf attachment edges | 兩 roots 的 spoke edges（可交換 roots） |
| --- | --- | --- | --- |
| b₂ | {b₀,b₁,b₃,b₄} | b₁b₂、b₂b₃ | b₀b₁、b₃b₄ |
| b₄ | {b₀,b₁,b₂,b₃} | b₃b₄、b₄b₀ | b₀b₁、b₂b₃ |

理由：若 h=b₂，必有 b₀,b₄∈T，又必有 b₁,b₃∈T；h=b₄ 同理。
`|T|=4≤t≤4` 迫四條 spokes 無重複框端，每 root 恰兩條；
兩組相鄰 pair 是原 `B−h` 路徑唯一的 perfect matching。
原 degree 式與 `k_L≥4,k_S≥2` 再迫

\[
t=4,\quad k_L=4,\quad k_S=2,\qquad
k_L^r=k_L^s=2,\quad k_S^r=k_S^s=1.
\tag{R}
\]

這是必要中間分類，尚不是兩份可實現來源。下一節將兩型一起排除。

## 5. 固定一個 root 的完整外側接回

**引理 OL-F（任意 long／short 長度）。** 若 `k_L^s≥2`，則對任意 proper q 及
任意 `a∈[4]\q(T_r)`，原 `G−L` 有一份完整染色使 `r=a`。

固定原 B 及 r。令 `J=G[S∪{s}]`，它連通。S 各點完整 degree4，扣掉實際
外鄰的色後，lists 大小至少 `d_J(v)`；而 s 的唯一已染外鄰是原框 spokes，
因 rs 不存在，所以

\[
|L(s)|=4-|q(T_s)|\ge4-t_s
=k_S^s+k_L^s-1>k_S^s=d_J(s).
\]

沿以原 s 為根的 J spanning tree 逆序貪婪著色，即得到所有原 S 及 s 的
完整外側 lift；r 的 spokes 因 a 合法而滿足。∎

如果這個 a 也屬 `q(W_L^r)`，它在某個實際 r-contact 產生外鄰碰色，
L 因而有 strict slack。固定剛取得的**同一份完整外側染色**（含它實際的 s 色），
再染滿 L，接成原 G。對原拒絕列的必要結論是

\[
k_L^s\ge2\ \Longrightarrow\
q_i(W_L^r)\subseteq q_i(T_r)\ (i\in I),
\quad W_L^r\subseteq\operatorname{cl}_I(T_r),
\tag{F}
\]

交換 r,s 得另一側。這裏不是要求兩 roots 同色，也沒有把原圖的兩 roots 合併。
它保留全外侧 fibre 的真實 s pin，而不是任選一個 s 色。

在 (R) 下兩側均可用 (F)。表中可能的 root spoke edges 只有
`01、34、23`，由公式 (C) 各自滿足 `cl_I(T_x)=T_x`。
每個 long leaf endpoint p 只有一個原 owner x，故它的全部框附件必包含於
這個 owner's 原 spoke edge。可是表中每份 leaf edge 都不等於任一可能的
owner spoke edge；兩者同為二點集合，無法包含，矛盾。

等價地，可選到一個**同一列** `q_i` 及合法 owner 色 a，使 p 的實際框鄰色為 a；
OL-F 給完整外側，p 的碰色 slack 給完整 L，遂得到被拒絕列的原 G full lift。
所有長度、internal cycles、contact cutpoints 及 owner 分配都已在此矛盾中涵蓋。
定理 OL 得證。

## 6. 完整 fibres、四／五點介面與有限 witnesses

全程的 cell 是同一原 piece、原頂點順序及具名接口 `(S_C,r,s)` 的完整 tuple
集合，包含空 fibre。全圖 fibre 仍是同一 q、同一 ordered pins 的兩份完整 tuples
加原 external factor 的 join；其與直接全圖 DFS 的相等另作校準。
OL-F 的存在性是原 spanning-tree 構造，不由不同列非空 cells 相乘取得。

本證明沒有對四／五點支援套用三點弧 Eq／Diff：§2、§3只使用所有五個原框點
的字面 signatures 和實際外鄰；§4開始才得到原來源的中間限制。
[完整具名分割定理](c5_excess_two_n2_partition_rule.md#2-完整-fibre-的分割定理)
在四／五點支援照常作用於整份 tuple。固定完整十列×16 ordered pins 中，
四點支援有74份具名分割、五點支援有160份；連續三點弧為26份。
這些數字只是接口對稱的有限核對，不限制任意原 L 的長度。

[控制與重播](../audits/2026-10-13-n2-one-long/controls/REPORT.md)保存：

- 原四-contact path 的三列永久 `(D,D)` 拒絕及完整十列 fibres；它仍是局部
  escape 泛化的 `counterexample`，不是完整 N2 來源，亦不反駁 OL-F／原 K₅。
- 三／四／五點支援固定 controls、全部原 tuples 與空格、具名 partition transport、
  同列完整 joins 及獨立 whole-graph DFS。
- 全32份 T 的具名閉包、末端 edge 必要分類，以及最後两型每份 leaf/owner 的
  字面 `i,a` 出口 witnesses；它們驗證有限框算術，不承擔內部圖形窮盡。
- 原 K₅ bags 的連通、互斥、十條 cross-edge witnesses；其拓撲的任意長度由
  §3–4 的紙面構造承擔。完整目標來源仍標為 **`not triggered`**。

完整紙面分工與交叉審閱見
[拓撲證明](../audits/2026-10-13-n2-one-long/topology/REPORT.md)、
[染色與接回](../audits/2026-10-13-n2-one-long/colouring/REPORT.md)及
[根審查](../audits/2026-10-13-n2-one-long/REVIEW.md)。

## 7. 重播、信任範圍與精確停止點

```bash
python3 -B audits/2026-10-13-n2-one-long/controls/checker.py --check
python3 -B audits/2026-10-13-n2-one-long/controls/boundary_checker.py --check
python3 -B audits/2026-10-13-n2-one-long/controls/boundary_side_checker.py --check
python3 -B audits/2026-10-13-n2-one-long/controls/minor_checker.py --check
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
lake build
git diff --check
```

正常／seed17唯讀重播、負控制、frozen hashes 與實際文件／build結果統一記在
[verification](../audits/2026-10-13-n2-one-long/verification.json)。
四組正常／seed17重播、四個負控制、正式 DocGraph、`lake build` 與 diff 檢查通過。
全域文件檢查先通過；最終[追檢](../audits/2026-10-13-n2-one-long/documentation_followup.json)
因同期 double-long／forced-inequality 報告引用尚未產生的檔案而失敗；
本輪 audit 的本地連結均存在，未改動那些同期工作。
沒有重跑上游全部44／N45／SD-A或 ES／ER來源枚舉，沒有新 Lean 證明；
`lake build`只驗既有形式化專案，不形式化本頁任意大小拓撲。

**Closure scope：** 僅本頁§1完整 N2 原55的 `(1,0)`，合既有 `(1,1)` 排除後，
九格第二 relation 族原55已閉合，總計八格。**Remaining OPEN：** 原55 `(2,0)` 的
同列完整 joint、完整 N2、E-ARC2、N2外來源及一般出口／`K∞=K≤5`。
兩-long缺少本頁起點所用的 short 全色 diagonal，不能把整條排除鏈直接套用；
OL-F 的 greedy 引理另用時仍須核對實際度數與接口，不能從本 closure 推升父命題。
沒有 commit 或 push。
