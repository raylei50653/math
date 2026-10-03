# ε=2 四-spoke (3,1)：原 binary unary 的 marked-leaf 必要化約

**後續（2026-10-03）**：[同列端點 hub 排除](c5_excess_two_mixed_core_four_spoke_hubs.md)
覆蓋原 star 的 32／64 份殘留，完成 mixed-(1,1) 加一原 binary unary
子型及 root 交換的整型來源排除；沒有證明 ε≥3 或跨列 palette 定理。
本頁原 116／256 份化約、單列代數資料及歷史證書不覆寫。

**後續（2026-10-03）**：[原三-spoke star 的同源扇區排除](c5_excess_two_mixed_core_four_spoke_star.md)
將本頁 116／256 份必要域縮為 32／64 份，含 root 交換；原指定
012／0、S_C=012、S_U=234 已由原 C／a／外側 apex 的 K₃,₃ minor
排除。殘留只含 K pair schedules；整型及 ε≥3 仍未證。
下文保留本輪原數字、單列代數 witness 與證書，不覆寫歷史產物。

2026-10-03，接手基準 `b63a096`；保留前輪工作樹。接續
[兩原單接點 unary 的六跨度排除](c5_excess_two_mixed_core_four_spoke_singles.md)。
目前入口由 [Kempe 導覽](c5_kempe_guide.md)維護，實際驗證及跨對話摘要見
[本輪紀錄](history/2026-10-03-excess-two-four-spoke-binary.md)。

**本輪完成必要化約，尚未排除選定的 binary 子型。** 固定原支援、
原 leaf 與完整有序 relation 後，933／941 分別留下 **116／256** 份
具名必要支援域，含 root 交換。它們不是圖、完整十列 relation 模型
或 disk 實現。共同下界仍 ε≥2；ε≥3、一般出口及 K∞=K≤5 未證，
沒有新增 Lean theorem，也沒有枚舉原來源圖。

## 1. 原圖、完整 joint 與省略圖

G 有限簡單，指定有序 induced-C₅ 為 disk 外框 B=(b₀,…,b₄)。完整
Σ 是 933／941 或整圖 D₅ 像；每條非框邊的刪除都嚴格擴大 Σ。
有效內部 H 非空連通，ε=2，恰兩個相鄰完整 degree-5 roots；
其餘有效內點完整 degree 四。三-spoke 側記 a，一-spoke 側記 b，
唯一原 b-spoke 是 bb_s。

H−{a,b} 恰為原 mixed C 及原 unary U。C 的 incidence-(1,1)，
有序 contacts (x,y)、owners (a,b)，容許 x=y，仍是同一原頂點。
U 的兩個原 contacts (u,v) 不同，皆由原邊 bu、bv 接 b；它們屬於
**同一原連通分量**。a 的三 spokes、ab、ax，以及 b 的一 spoke、
ab、by、bu、bv 耗盡兩側 degree 五。

對一份 proper boundary coloring β，原完整關係為 R_C(β;x,y) 與
R_U(β;u,v)。每份 tuple 來自該原分量的整份 coloring。給定原
spoke 省略 e=ab_j，M_e=G−e，令 S_a=N_B(a)，則

\[
R_{K,e}(\beta;a,y)=\{(A,Y):\exists(X,Y)\in R_C(\beta),
\ A\notin\beta(S_a\setminus\{j\}),\ A\ne X\},\quad K=C\cup\{a\}.
\tag{1}
\]

完整五點 joint 必須接合 U 的整份二元 tuple：

\[
\mathcal J_e(\beta;b,a,y,u,v)=\{(D,A,Y,T,W):
(A,Y)\in R_{K,e}(\beta),\ (T,W)\in R_U(\beta),
D\notin\{\beta_s,A,Y,T,W\}\}. \tag{2}
\]

接回原 spoke 只作同一 tuple 的字面過濾

\[
\mathcal J_G(\beta)=\{t\in\mathcal J_e(\beta):t_a\ne\beta_j\}. \tag{3}
\]

固定 (b,a) 後保留完整 (y,u,v) 纖維，含空纖維。不能以 U 的兩個
marginals 相乘；也不能把原 C 的 x=y 複製成兩份自由 contact。

沿用 [單 spoke 原身份化約](c5_excess_two_mixed_core_single_spoke.md)：
若 e 在原拒絕列 q 與另一條保留 a-spoke 同色，M_e 仍拒絕 q，
並且自己是以 b 為唯一 degree-5 的 minimal q-core。M_e−b 恰有
兩份原 binary，K 的 contacts=(a,y)，U 的 contacts=(u,v)。
a 在 M_e 的完整 degree 四，且是 K 中的 leaf。

## 2. 固定原 U 的短支援排除

對原 U 定義 F_U(β)=⋂_{t∈R_U(β)}set(t)。Σ-critical 原 contact 邊
bu 的新接受 witness 給原拒絕列 β 與同一圖 G−bu 的 coloring f。
令 d=f(b)。R_U(β) 非空：尚未固定 b 時，u 有 list slack，故連通
貪婪引理可染整份原 U。

如果有原 U 的完整 tuple 同時避開 d，只替換 f 在 U 中的整份
coloring 便能接回 bu、bv，與原 G 拒絕 β 矛盾。因此 d∈F_U(β)。
這裡沒有假設 G 是 β 的 minimal q-core，也沒有拆開 U 的兩條 incidence。

若 actual N_B(U) 包含於某份原框邊 P，三個不同 a-spoke 鄰點
保證有 h∈N_B(a)∖P。原 b–a–b_h 路徑、原 bb_s 及完整 degree-four
carrier U 符合 [短支援定理](c5_short_support_singleton.md#1-原圖完整接點-relation-與外部路徑)。
它不限制 carrier 的 contact 數，故 F_U 對每份 proper β 都為空，矛盾。
空支援、單點支援也包含於框邊，遂全部排除。

**原 U 的最小 cyclic 支援跨度至少二。** 原 H−b 只有 K、U
兩份分量；K 包含 a 的三原 spokes，跨度亦至少二。前輪的共同
lifts 論證容許 K 含 degree-5 點，這裡只得到 4≤ℓ_K+ℓ_U≤5，
沒有六跨度矛盾。每份域仍核對原 K、U 的全部相容 lifts。

## 3. leaf slack 與完整 relation 的精確反像

在每份同色省略的 q，a 的保留 spokes 見到兩色。令
L=U₄∖q(S_a∖{j})，則 |L|=2。若固定 b=d 且 d∉L，leaf a 的
list 不減少，仍比 deg_K(a)=1 大，故整份 K 有 slack 可染。因此

\[
F_K(q)\subseteq L. \tag{4}
\]

必要 (2,2) 分類保存所有完整 K schemas，而不只保存式 (4)。對
一份非空 K schema R，定義最大原 C 反像

\[
P_R=\{(X,Y):\{(A,Y):A\in L,\ A\ne X\}\subseteq R\}.
\]

令 Γ_C 為逐色固定 q(N_B(C)) 的 S₄ 穩定子，令

\[
P_R^{\Gamma_C}=\{t\in P_R:\Gamma_Ct\subseteq P_R\}.
\]

每份原 C relation 都是 Γ_C-invariant，且每個 C tuple 的 leaf image
非空。存在非空 Γ_C-invariant 二元 relation 能給完整 R，**當且僅當**

\[
\{(A,Y):(X,Y)\in P_R^{\Gamma_C},\ A\in L,\ A\ne X\}=R. \tag{5}
\]

必要性由原 C relation 包含於最大 invariant 反像得到；充分性以
這份最大反像作純 relation-algebra witness。它不是原 C 的染色
witness，不主張其中全部 tuples 必出現在實際來源。
若 x=y，還須取反像的對角部分；證書另存它是否仍給完整 R。
支援域容許原 contacts 相同或不同，沒有將這個代數判準當作圖實現。
同一原字面列的多份省略還須有共同的完整 K schema 與 C 反像。
跨不同列仍只保存必要 domains，尚未構造一份原圖的十列 joint。

**雙禁色的更強結構。** 若 |F_K(q)|=2，(2,2) 分類給
R_K={(c,d),(d,c)}。式 (4) 迫 L={c,d}。對任一原 C tuple (X,Y)，
Y 必在 L；若 X≠Y，leaf image 會含 (Y,Y)，或含 L 之外的 Y，
皆不合法。完整覆蓋兩份 K tuples 因而迫

\[
\boxed{R_C(q)=\{(c,c),(d,d)\}.} \tag{6}
\]

這是**原完整 relation 的精確等式**。沿用
[雙禁色 bridge-path 定理](c5_single_spoke_bridge_path.md)，K 的 a–y
是奇數長原 bridge path；第一條原邊是 ax。因此原 C 的 x–y
path 是偶數長、各邊仍為原 bridge。x=y 時長度零，不能排除。
另一份原 binary U 及全部實際附件仍保留。

## 4. 同源支援域與具名殘留

[Checker](../scripts/c5_excess_two_mixed_core_four_spoke_binary.py)／
[artifact](../artifacts/c5_excess_two_mixed_core_four_spoke_binary/observations.json)
讀取 [(2,2) 原表](c5_single_spoke_two_two.md)及
[已完成來源排除表](c5_single_spoke_residual_locality.md)，沿用 102 份
保留原 IDs，整圖反射後為 196 份具名 records。保留原表的全部
支援、contacts、schemas、共同 lifts、contact words 及來源 index。
反射同時搬動兩分量、原框、色框與全部列，不獨立正規化分量。

| 必要核對層 | 933 | 941 |
| --- | ---: | ---: |
| 原具名 root-spoke frames，含 root 交換 | 20 | 60 |
| 同色省略／拒絕列 queries | 40 | 160 |
| leaf 附件及 slack 後 records | 480 | 1,452 |
| 完整十列 bounds／必要 child masks 後 | 480 | 1,388 |
| 原 C 支援反像 | 1,920 | 5,552 |
| 完整 leaf relation 反像後 | 1,240 | 3,540 |
| 同源、同列完整 schemas 接合後支援域 | 376 | 776 |
| 原 U 短支援排除 | 260 | 520 |
| 保留具名必要支援域 | **116** | **256** |

每份域使用固定 (S_C,S_U)，每個原 e 同時滿足
S_{K,e}=S_C∪(S_a∖{j})，原 K 支援則為 S_C∪S_a。相同字面列
的完整 schemas 相交後才保留；各域有全部 assignment identities。
所有長支援殘留皆有原 K／U 共同 lifts，這一層未新增排除。

933 的 116 份域都只含 K 雙禁色 schedule。941 的 232 份亦然，
另外 24 份在不同原拒絕列分別要求 K singleton／pair；每份保存的
schedule 都含這兩種 query。這些數字是具名必要域，並非 distinct
graphs 或完整 Σ 的實現個數。

兩候選共同保存如下具名入口：a=6、b=5，原 a-spokes=012，
原 b-spoke=0，actual S_C=012、S_U=234。取原 q=01021，L={2,3}，
兩份同色省略的必要完整 tuples 可為

\[
R_C=\{(2,2),(3,3)\},\quad R_K=\{(2,3),(3,2)\},\quad
R_U=\{(1,2),(1,3),(2,1),(3,1)\}.
\]

K 禁 2、3，U 禁 1，b 的 spoke 禁 0，式 (2) 為空；原 U 的兩
contacts 各有放邊 witness。這份純代數資料仍容許 S_K=012、S_U=234
的共同 lifts；**它只見證一份必要字面列，不是完整十列或圖反例。**

## 5. 原完整度數圖控制、重播與停止點

[Joint helper](../scripts/c5_excess_two_four_spoke_binary_joint_controls.py)
保存 24 張含 root 交換的完整 degree 圖。原 C 為 singleton／edge／
triangle，原 U 為同支援 edge／分支援 edge／偶數 path／triangle。
所有原內邊、attachments、owners、contacts、每份 component coloring
witness、K tuples、joint tuples 及 pinned fibres 均保存。

**720** 次完整接合與獨立整圖回溯一致；**11,520** 次固定 (b,a)
的完整 (y,u,v) 纖維含空纖維一致；**144** 份同色原 spoke 等式核對。
原控制 0、row 0 的 U 有完整 tuples {(2,3),(3,2)}：b=2 時兩個
marginals 都有可用色 3，但整份 binary 沒有避開 2 的 tuple。
另保存原 C 共鄰 contact 的 marginal 假接合控制。
固定圖只核對式 (1)–(3)，不聲稱 disk、Σ-critical 或候選實現。

```bash
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_four_spoke_binary.py --check
uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_four_spoke_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_single_spoke_two_two.py --check
PYTHONHASHSEED=17 python3 scripts/c5_single_spoke_residual_locality.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

本輪原 `(2,2)` checker 的 `--check` **未通過**：唯一差異是
`inputs/docs/c5_single_spoke_cores.md` 的既有文件來源 hash。新 checker
另重算並比較原證書的**全部數學 payload**及整份 support table，
兩者完全一致；原、現 hash 與原 artifact digest 都存於
`inherited_base_replay_audit`。沒有改寫原產物或它的下游歷史證書。
其餘實際重播範圍、環境及檢查結果見本輪紀錄。

信任層：critical witness／短支援與原 bridge-path 紙面定理、沿用
外部 degree-list／Gallai 定理與既有 source minor；Python 核對明列
必要域、局部完整 schemas 及完整圖 witnesses。不使用四色定理 oracle，
未重開來源圖枚舉；`lake build` 不形式化本輪紙面 topology。

**停止點：binary 子型縮到 116／256 份必要支援域，整型排除未完成。**
下一窄入口取上述原 012／0、S_C=012、S_U=234，保留式 (6) 的原
偶數 bridge path（含 x=y）及 U 的完整二接點 relation，研究同圖
跨列 palettes／原 root cycle 是否給 minor 矛盾。不同列的必要
domains 仍不能當作一份原圖的共同十列 witnesses。
mixed-(1,2) 加一 unary、mixed-(1,3) 無 unary、其他四-spoke／較少
spokes、原單省略、(5,5) q-core、多 mixed／no-mixed／非相鄰
roots 仍保留；兩單接點 unary 的既有排除與共同 ε≥2 不變。
