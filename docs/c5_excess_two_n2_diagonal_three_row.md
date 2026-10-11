# N2 原55：unary 三列出口採納與低接點 long 化約

**整理發布（2026-10-11）**：相連四輪成果由[發布紀錄](history/2026-10-11-n2-55-progress-publish.md)
統一保存驗證與提交範圍；下文原生成基準及當輪「未提交」語境保留。

2026-10-11；基準 HEAD `5f0979793c19e452dbb5fc7e9fe7e43cb8a991cc`，
包含當時未提交的 unary 候選及殘餘統一報告；精確工作樹輸入見
[BASE](../audits/2026-10-11-n2-unary-adoption-long-joint/BASE.json)。
目前停止點見 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)。

**本輪採納完整 N2 的 `(ℓ,u)=(0,1)` 原55來源排除。**
與既有兩 unary 排除合併，原九格中的第三 relation 族已有完整原55覆蓋，
九格由六格增加至七格。含 long 的三個參數情形仍 OPEN；
另取得共享接點及低接點 long 的限定排除，沒有完成一般 N2 或 E-ARC2。

證據層為外部 degree-list 定理＋任意大小紙面證明＋獨立紙面審查；
局部 Python 完整 fibres 另作校準，目標來源仍 `not triggered`。
沒有新 Lean theorem、10–35 內點搜尋、commit 或 push。

**後續（同日）**：[long 同列同步](c5_excess_two_n2_long_synchrony.md)另排兩份 long
接線皆至多三的完整子域，以及無 U 的葉接點 tree long（任意接線數）；含 U 的
低接點 masks 精確分類為 Eq／Diff，異類同列接回，同類剩七個必要弧模板。
本頁保留前輪已採納範圍；九格仍七格，三個含 long 父情形及 E-ARC2 仍 OPEN。

## 1. 完整來源契約

沿用 [原55統一報告 §1](c5_excess_two_n2_residual_unification.md#1-九格對應與完整契約)
及 [真核心報告 §1](c5_excess_two_arc_spoke_closure.md#1-完整來源前提與依賴)
的全部契約：有限簡單 induced-C₅ disk，有序外框 B；完整 Σ933／941 或整圖共同
D₅ 像，T4 全收，每條非框邊 Σ-critical，ε=2；有效 H 連通並 full B-touch；
恰兩個非相鄰原完整 degree5 roots r,s，其餘有效內點原完整 degree4；
H−{r,s} 恰兩份原 mixed P,Q，其餘 unary，所有 pieces one-sided。
原 contacts／shared contacts、ownership、actual attachments、rotation、bridges、
旁支、共同字面色框、完整 relations／空 fibres／full lifts 均保留。

共同搬運整圖後固定

\[
I=\{0,1,3\},\quad q_0=01212,\quad q_1=01202,\quad q_3=01021,
\qquad D=3.
\]

ℓ 為 long mixed 數，u 為 unary 數。long 指實際支援不包含於任何框邊；
原盾弧定理使 long 的支援至少三點。記
`k_C=k_C^r+k_C^s` 為原 root incidences 總數，不以不同接點數替代重複 incidence。
既有結果給每份 C 至少兩 root incidences、bridges／奇環 cactus、
每 leaf block 有私有 root-contact、每奇環至多一個普通私有點，
且所有 H 內度二點的原框邊附件單射。

外部輸入為 [Dvořák 2018，Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)：
不可染的連通 degree assignment 緊，lists 是 incident Gallai block palettes 的互斥聯集。
本轮獨立審查核讀原文；本頁的三列及 joint 推論不是外部定理原文。

## 2. Unary 出口的獨立採納

**定理1。** u=1 時，原 unary U 的 owner 至少在一個 i∈I 可取 D，且有 U 的完整 lift。

原 degree5 及兩 mixed incidences 使 owner 的 U 接線數為2或3。
[原候選 §§2–4](c5_excess_two_n2_unary_three_row_escape.md#2-三列-palette-signatures)
已完整覆蓋同一 U 的單 block、兩 leaf blocks、三 leaf blocks；
任意長鏈在第一個原鄰點被處理，不以有限短圖外推。
[獨立紙面審查](../audits/2026-10-11-n2-unary-adoption-long-joint/paper/independent_review.md)
重建三列 signatures、cycle/contact 計數、兩種 branch node 及 same-row 接回，
在§1契約內採納該結論。原候選的作者核對及當輪未採納語境保留。

**推論1.1。** `(ℓ,u)=(0,1)` 不存在原55來源。

取定理1的同一 i，令原 r=s=D。D 避開原全部 spokes，原 rs 不存在。
兩份 short mixed 由 [N-diagonal](../artifacts/c5_excess_two_e4/REPORT.md#41-新引理-n-diagonal只指定-nc-的局部-list-版本)
在該同一 qᵢ／同一 `(D,D)` 各有完整 lift；U 也在該列完整接回。
三份原分量互斥，原 shared contacts 仍是各自分量中的同一頂點；
所有 root 邊、框附件及原內邊均合法，自由孤立座標的四色因子亦保留。
故得到原 G 完整染色，違 qᵢ 拒絕。

與既有 u=2 排除合併，第三 relation 族的原55格 CLOSED；
不能將這個子族結論搬到 N1、相鄰 roots 或完整契約之外。

## 3. 共享接點與低接點 mixed 的完整 diagonal

**引理2（共享接點）。** 若原 mixed C 有一個頂點同接 r,s，則對每個 proper 框列 β
及每個色 a，C 在原 pins `(a,a)` 有完整 lift。

*證明。* 固定原 pins，令

\[
L(v)=[4]\setminus\bigl(\beta(N_B(v))\cup\{a:rv\in E\text{ 或 }sv\in E\}\bigr).
\]

各點 `|L(v)|≥d_C(v)`。共享接點的兩條不同原 root 邊只禁止一色，
故該點 `|L(v)|≥d_C(v)+1`。連通 degree assignment 有 slack 時可沿生成樹逆序
貪婪染色，因此得到保留全部原邊／接點的完整 C lift。沒有合併 r,s 或原接點。∎

**引理3（低接點 long）。** 若原 long mixed C 的 `k_C≤3`，则

\[
\exists i\in I:\quad (D,D)\in A_C(q_i),
\]

並有 C 的完整 lift。

*證明。* 若有共享接點，用引理2。否則令 T 為 C 中接到任一 root 的原點集。
每個 T 點恰接一個 root，因此 `|T|=k_C∈{2,3}`。固定原 pins `(D,D)` 時，

\[
L_i(v)=[4]\setminus\bigl(q_i(N_B(v))\cup\{D:v\in T\}\bigr).
\]

這正是定理1局部 block-tree 證明使用的 lists。該證明的 contacts 計數、
leaf 私有接點、普通私有 cycle 點上限、H 內度二附件單射及支援至少三點，
全部對原 C 成立。其各步只問原點是否在 T，不問該點接 r 或 s。
所以同一單 block／兩 leaf／三 leaf case split 排除三列皆不可染。
此處只是核對相同 pins 下的原 lists，沒有製造一個合併 roots 的新來源，
也沒有變動 ownership 或完整 off-diagonal relation。
選到可染列後，該原 C 的完整 list coloring 即所需 lift。∎

獨立審查另核對此 ownership 無關的適用性，並與引理2分開裁決；
不把兩份 C 各自的存在列當成共同列。

## 4. 原 joint 的新縮減與仍缺的同步條件

對每份 mixed 定義 `M_C={i∈I:(D,D)∉A_C(q_i)}`；
對 unary 定義 `M_U={i∈I:D∈F_U(i)}`。這些集合只記 diagonal 出口位置，
完整 relations／fibres／full lifts 仍由原 pieces 保留。

short 的 M 為空；共享接點 mixed 的 M 為空；低接點 long 的 M 是 I 的真子集；
定理1給 unary 的 M 也是 I 的真子集。在原來源內，

\[
\exists i\in I\setminus(M_P\cup M_Q\cup M_U)
\quad\Longrightarrow\quad \text{同列完整 }(D,D)\text{ joint 非空}.
\]

無 U 時省略 M_U。因此取得以下**限定**來源排除：

| (ℓ,u) | 本輪已證排除 | 保留缺口 |
| --- | --- | --- |
| (0,1) | 完整子族 | 此格已關；父 N2 不升格 |
| (1,0) | long 有共享接點，或 `k_L≤3` | 剩餘 long 無共享接點且 `k_L≥4` |
| (1,1) | long 有共享接點，與 U 的同列出口接回 | 無共享接點；即使 `k_L≤3`，兩個真子集仍可能合覆 I |
| (2,0) | 一 long 有共享接點，另一 long 有共享接點或接線總數≤3 | 其他情形仍須同列完整 joint，不能拼兩個不同出口列 |

這些結論不排除 u=0 時尚容許的 singleton mixed；其 diagonal 由 N-diagonal／
引理2處理，但不能因此宣稱其他 long 已接回。
原55每欄一單位容量、大小精確式及 Δ 门檻仍沿用
[統一報告 §§2、4](c5_excess_two_n2_residual_unification.md#4-原35上界與既有下界直接矛盾及精確鬆弛)，
沒有新增一般 Δ 下界，沒有搜尋10–35內點。

## 5. 證據、重播與停止點

本輪 [稽核報告](../audits/2026-10-11-n2-unary-adoption-long-joint/REPORT.md)
保存 frozen inputs、獨立紙面裁決、完整 local fibres 核對、正／負控制與實際驗證。
97 原 U 的局部觸發仍與完整 Σ933／941 N2 target 分開：target 零觸發是
`not triggered`，本頁任意大小排除由紙面證明承擔。
沒有新增 Lean 證明；`lake build` 只核既有 Lean 專案，不形式化本頁。

```bash
python3 -B audits/2026-10-11-n2-unary-three-row-escape/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n2-unary-three-row-escape/checker.py --check
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
lake build
git diff --check
```

原55含 long 的三情形、完整 N2、E-ARC2、N1／相鄰及單-root例外仍 OPEN。
下一窄義務是以原實際支援及原 palettes 證明同列出口重合，或直接證完整
off-diagonal joint 非空；不能先假設三點弧命題再排本子域。
