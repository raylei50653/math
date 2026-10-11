# BR-SD-1a 紙面獨立核查

日期：2026-10-11。分工：paper；只寫本專屬目錄。

**裁決：四個待驗步驟均成立；在 BR-SD-1a 明定的完整原來源合同下，不存在這樣的拒絕來源。** 這是任意有限大小的紙面直接矛盾，依外部 Gallai degree-list 刻畫；不依 screening 結論、不依 SD-A、β-minimality 或 T4。尚無本分工新增的 Lean、有限 actual source 或一般 N45 覆蓋。

本核查只讀主端凍結 `authority/current/` 中新 NEXT-TASK、舊 BR-SD-1 NEXT-TASK、N45 §1／2.11 和 degree-5 介面 §2／7；未讀 screening REPORT。任務文本指定來源 BASE 為 `4dd11f422c6fa49265a412085116b088786d0344`。執行 HEAD／BASE 差異由主端 manifest 記錄，本核查不以記憶中的舊狀態替代本輪原文。

## 精確量詞與原身份

對每一個滿足以下**完整原合同**的有限簡單原 G、具名 r/s、原 spoke e、原 M 及 literal β，都可推出矛盾：

- G 保 ordered induced-C5 框 B、Σ933／941 或同一整圖共同 D5 像、原 Σ-critical witnesses、原 nonadjacent degree5 roots r/s、其他有效原內點完整 degree4；H_G−{r,s} 恰完整 mixed L/S、無原 unary，L long、S 的 actual support 恰一真框邊兩端。
- e=rb_i 是 r 唯一原 boundary spoke；X=M=G−e，vertex set 不變，M 自己拒絕同一 proper 三色 β，且帶其 inclusion-minimal／retained-edge witnesses。M 的 s 完整 degree5，其餘內點完整 degree4。
- M 原邊直接給 N_H(s)={p,q}，p/q 為原有序不同 contacts，分別屬 L/S；s 的三原 boundary spokes 留存。C=H_M−s={r}∪L∪S 是實際 sole component；r 在 C 內度4，每側原 contacts 各2。
- C 的全部 blocks 正是三原奇環 J1/J2/J3 及原 bridges。J1∩J2={r}，J3 不交 J1/J2。J2 私有 u≠r 與 J3 私有 v 的原邊 uv 為唯一環間 bridge。原外臂由 p 到 J1 私有錨點 a1、由 q 到 J3 私有錨點 a3，臂可零長；無其他 blocks／旁支。
- Col 是同一四元素原色框，D 是 β 未用的唯一第四色；全部原 vertices、edges、actual B attachments/supports、ownership、ordered/shared contacts、bridge 端點、rotation、Σ／β witnesses、relations／fibres/full lifts 都保留。

此處始終在原 M 的全部邊上定義列表；沒有抽象 list 替代來源、沒有縮 uv、沒有移動 r、沒有把 palette 獨立重命名。N45 §1 的 root 交换只用于定位 r 是降度側，不能在本证明中再各 block 自行交换色框。

## 外部正式定理定位

親自以 browser 打開 [Zdeněk Dvořák, *List coloring and Gallai trees*](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，文首日期 March 24, 2018；核對 PDF 第6頁（zero-based page 5），即 printed p.6 的 **Theorem 10 (Gallai)**。同頁定理前的 blockwise-uniform 定義要求：奇環 palette 大小2、clique palette 大小為點數減1；**凡兩 blocks 有共同頂點，它們的 palettes 必互斥**；每個點的 list 是所有所屬 block palettes 的聯集。Theorem 10 對 connected graph 與 degree assignment（各點 list 大小至少內度）給出不可著色的上述刻畫。degree assignment 定義及 Lemma 7 位於 printed p.5。

本核查只用 Theorem 10 的必要方向及其緊接的定義。它不要求 graph 先二連通、平面、Σ-critical、T4 或 lists 預先全緊；也不限制奇環長度。K3 同時可視為 clique／奇環，兩規則均給 palette 大小2，無三角例外。

主端下載 `external/gallai.pdf` 已另以 `pdftotext -f 6 -l 6 -layout … -` 核對 printed p.6；SHA256：`50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`。

## 逐步裁決与必要符號 witness

### 第1步：degree-list 下界與 C 不可著色 — 成立

對原點 x∈V(C)，令

\[
 t_x=|N_B^M(x)|,\qquad \delta_x=\mathbf1_{sx\in E(M)},
\]

並以原邊定義

\[
 L^D(x)=\operatorname{Col}\setminus\bigl(\beta(N_B^M(x))\cup(\{D\}\text{ if }\delta_x=1\text{ else }\varnothing)\bigr).
\]

C 包含全部 M 內點除 s，所以原完整度4精確分解為

\[
 d_C(x)=4-t_x-\delta_x.
\]

因 D∉β(B)，實際有 `|L^D(x)|=4−|β(N_B^M(x))|−δ_x`，故

\[
 |L^D(x)|\ge4-t_x-\delta_x=d_C(x).
\]

這一步只需 distinct-color 數不大於原 spokes 數；不假設 boundary spokes 在 β 下異色，也不先借用 tightness。數值上完整度至多4已足以保證下界；本核查仍只宣稱合同指定的完整度4來源。

假若 f 是 C 的 proper L^D-coloring，令整圖顏色為 β 在 B、f 在 C、D 在 s：B−B 邊由 proper β 處理；C−C 邊由 f 處理；C−B 邊由列表處理；s−C 邊由 contact 扣 D 處理；s−B 邊因 D 未用而 proper。這正是**同一原 M** 的完整 coloring，與 M 拒絕 β 矛盾。因此 connected C 不可 L^D 著色。

最弱实际使用項：有限簡單 M 的原 vertex partition `B ⊔ {s} ⊔ C`、connected C、全部 C 點完整度≤4、proper β、D 未用、M 拒絕 β。s 的數值 degree5、inclusion-minimality／刪邊 witnesses、Σ933／941、disk／induced-C5 幾何與 T4 在這一步不參與推導；它們仍是原身份合同的一部分。

### 第2步：原 w1/w2 存在、非割點、非 s-contact — 成立

令 a1 為 p 外臂在 J1 的原私有錨點，所以 a1≠r。選

\[
 w_1\in V(J_1)\setminus\{r,a_1\},\qquad
 w_2\in V(J_2)\setminus\{r,u\}.
\]

各原奇環長度≥3，兩邊各排除恰兩個不同點，因此候選數分別至少 `|J1|−2≥1`、`|J2|−2≥1`；三角形也成立。不須宣稱這兩個候選唯一，只需對每個來源存在至少一個可選原點。

原完整 block 表與無旁支合同給出：J1 的所有 possible C 切接位置僅 r 與 a1（臂零長時 a1 不一定是 C 割點，但仍保守排除）；J2 的所有 C 切接位置僅 r 與 u。w_i 均不在這些位置，沒有額外 bridge／其他 block incident，因此不為 C 割點，且只屬原 block J_i。

p/q 是 s 唯二原內鄰。若 p 外臂正長，p 不在 J1，而若零長則 p=a1；兩者都不能等 w1。q 位在 J3 外臂或零長錨點 a3，不在 J1。p 所屬 J1 外臂與 q 所屬 J3 外臂都不在 J2，所以 w2 也非 p/q。外臂是合同中的原外臂；無旁支的原 block 表排除另一次進入環、額外接觸或繞經 w_i。

最弱实际使用項：兩個 J_i 至少三點且為原 blocks；J1 除 r/a1、J2 除 r/u 無其他原 block incident 點；s contacts 只為上述 p/q，且它們沿兩末端外臂配置。這裡使用 source shape 導出 witness，沒有用 SD-A 先推 source shape。J3／uv 的作用只是核实 J2 的另一切接點是 u、q 仍在外側；不使用 uv 的 palette 或 R27。

### 第3步：原鄰居、D 與原 palette identity — 成立

記 w_i 的兩個原環鄰居為 w_i^-、w_i^+。由前一步及全部 blocks／無旁支合同，完整原鄰域為

\[
 N_C(w_i)=\{w_i^-,w_i^+\},\quad sw_i\notin E(M),\quad
 N_M(w_i)=\{w_i^-,w_i^+\}\mathbin{\dot\cup}T_i,
\]

其中 `T_i=N_B^M(w_i)⊆B` 是實際原附件集合，原完整度4給 `|T_i|=2`。沒有丟棄或交換這兩條原 B 附件。因此

\[
 d_C(w_i)=2,\qquad L^D(w_i)=\operatorname{Col}\setminus\beta(T_i),\qquad D\in L^D(w_i).
\]

第1步已給 connected、degree assignment、不可著色，故可直接用外部 Theorem 10 取得**同一個全 C、同一 literal Col** 的 block palettes `(S_K)_K`。w_i 只屬 J_i，故 blockwise-uniform 的 vertex-union 等式精確給

\[
 L^D(w_i)=S_{J_i}.
\]

原 J_i 奇環給 `|S_{J_i}|=2`；因此 `|L^D(w_i)|=2=d_C(w_i)`，並且 D∈S_Ji。若原 T_i 的兩 β 色相同，list 原本≥3，便已違反此結论而更早產生矛盾；無須把原附件異色另當假設。

最弱实际使用項：第1步的 degree-list 不可著色、w_i 只屬 J_i 且非 s-contact、D 未用，以及外部 theorem 的 vertex-union／palette-size 規則。全緊是結論而非輸入。引用 theorem 前没有從非割點直接宣布各 block palettes 存在，也沒有拼不同 list assignments。

### 第4步：r 處原 palettes 相交矛盾 — 成立

原 blocks J1/J2 具有同一原 shared vertex r，故外部定義要求

\[
 S_{J_1}\cap S_{J_2}=\varnothing.
\]

第3步卻給同一 literal D∈S_J1∩S_J2，矛盾。其約束是「blocks 有共同頂點」；不是誤套「以一條 bridge 相連」也要互斥。J2/J3 不相交，外部定義並不直接要求它們互斥；本證明完全不需要對它們作那種宣稱。

在原 r 上也可核 source identity：e 是唯一 r−B spoke且已刪，r 非 s-contact，`N_B^M(r)=∅`、`d_C(r)=4`、`L^D(r)=Col`。r 所屬原 blocks 正是 J1/J2，刻畫遂要求原等式 `Col=S_J1 ⊔ S_J2`；兩個都含 D 無法滿足。這個原 shared coordinate 未被各側獨立量化或正規化。

最弱实际使用項：同一全 C 的 blockwise-uniform witness、原 J1/J2 在 r 相交、同一 D 同時在兩個原 palettes。r 的數值 list=Col 可作 identity 核對，但矛盾只需 palette 相交互斥規則和 D membership。

## 對 N45 與 degree-5 介面的映射

| 原權威項目 | 本證明中的角色 | 裁決 |
|---|---|---|
| N45 §1 exact-S：只刪原 rb_i，X=M | 保 M 的原 edges／degrees／β；不從 G 的 criticality 偷推 M 拒絕 | 明設并保留 |
| 舊 BR-SD-1 合同1–3、新任务来源首段 | 原身份、完整度、C sole、s contacts／spokes、literal β | 第1步和原边核对可用 |
| 舊合同4、新任務 source shape | 三原 odd blocks、shared r、唯一 uv、两末端可零長 arms、無旁支 | 第2步 witness 足够 |
| N45 §2.11 的 A／二連通導入 | 本任务直接明设 shape；不再次调用 SD-A 推出 | 不作 proof dependency |
| degree-5介面 §2 | 与外部 degree-list characterization 一致，保同一 shared vertex 和色框 | 外部 Theorem 10 正式核回 |
| degree-5介面 §7 四个 s-query | 固定 β 的 C−B、s−C 约束，暂不施加 s−B spokes | 本分工只需拒绝 D；不需证明 F_C(β)={D} |
| β-minimality／M逐边 witnesses、GΣ-critical／T4 | 属原合同；不用于上述四步 | 无借用或遗传 |
| uv→R27 source minor／target minimality／四query保持 | 新任务明示不要求 | 本证明无此义务 |

此表中的「不作依赖」只描述這四步的实际 proof dependencies。交付結論仍限制在完整 BR-SD-1a 合同，不另宣告弱化來源域的排除，不擴展其他位置／旁支／更多環的研究。

## 零長臂、任意長與停止界線

两原臂长度可独立为0；左臂0时 p=a1 仍已排除，右臂0时 q=a3 不在 J1/J2。两臂都0与任意正长均不影响 w_i 存在、非 s-contact 和原 palette identity。

J1/J2/J3 长度可独立取任意奇数≥3；w_i 的存在性只用至少三点，degree／palette推导无枚举上限。这里也不把 arbitrary lengths 的数学证明换成有限三角控制。

**发现的缺口：无。** 在完整指定合同下，来源排除由上述直接纸面矛盾承担；并非从有限 controls 未触发推出。没有 actual source 可实现性声明，也没有从抽象不一致列表反推真实 disk 见证。

本分工不运行 checker、不宣告 finite triggers。任何主端使用的 controls 须另标 `triggered and holds`／`not triggered`／`counterexample`；无 actual source 的 controls 不承担当纸面来源排除的理由。

保留 OPEN：一般 bridge-separated 三环、其他 shared/contact 位置、旁支、其他环数、非二连通其他 appendages、两long完整身份、其他45／54、55、无45／54来源、一般N2／E、ε≥3及主命题。未改共享 coverage/adoption 文件，本核查本身不代表已发布、Lean完成或这些一般 OPEN 新增关闭。

## 本分工 authority SHA256

路径均相对于本 audit 的 `authority/current/`；whole-file hashes 固定本轮所读 authority bytes。

| 路径 | SHA256 |
|---|---|
| audits/2026-10-11-single-deficit-publication/NEXT-TASK.md | 0b5cd72b067c72dfec8c96d527ef315a8ef7d36d2d487202f68c995574f07343 |
| audits/2026-10-11-single-deficit-applicability-804e3b0b1b/NEXT-TASK.md | db65e1dbd397d9af8e77ebbdcdebfdf0b5ce40d4403e02701f51e773d2aa093b |
| docs/c5_excess_two_nonadjacent_unit_core45.md | 602194e7c259621ca9df0fa44a14ff1cf6982bb0580e6b562d819b35202b3ce1 |
| docs/c5_degree5_interfaces.md | 818fb3973bf005ef22e3ca3c77b9b551524a577277662f7b65d1a07a0504614a |

方法性记忆仅用于 exclusive-write／同源色框／证据层级规则；数学判断全部重新以本轮 authority 和正式外部 theorem 核实。
