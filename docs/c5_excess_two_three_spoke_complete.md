# ε=2：唯一 degree-6 root 的 t=3 全部分拆排除

**發布整理（2026-10-03）**：本頁與 t=0 的 checker、證書及導覽更新
一併提交推送；本次重播及範圍見 [發布紀錄](history/2026-10-03-excess-two-degree-six-publish.md)。

**後續（2026-10-03）**：[t=0 全分拆排除](c5_excess_two_no_spoke_complete.md)
已完成原六接點的十一分拆。連同本頁及 t=1、2，唯一 degree-6 的
ε=2 分支全部排除；同一來源若 ε=2 只剩兩個 degree-5 roots，
共同 ε≥2 不變。下文保留本輪證據與停止點。

2026-10-03，接手基準 `4701f4c`。接續
[t=2 全分拆排除](c5_excess_two_two_spoke_complete.md)，沿用
[原短支援引理](c5_short_support_singleton.md)與
[三接點兩禁色 K₅](c5_excess_two_ternary_two_unary.md#2-三接點在所有列都至多禁一色)。
目前入口見 [Kempe 導覽](c5_kempe_guide.md)，本輪實際驗證及接手摘要見
[研究紀錄](history/2026-10-03-excess-two-three-spoke-complete.md)。

**933／941 固定完整 Σ、edge-minimal induced-C₅ disk 來源，在 ε=2、
唯一完整 degree-6 root 的前提下，t=3 的三種原接點分拆全部不可能。**
連同 t=1、t=2 及 T4 全收的 t≤3 限制，唯一 degree-6 root 若存在，
必有 **t=0**。共同 ε≥2 下界維持；兩個 degree-5 roots、一般來源與
`K∞=K≤5` 保留。證據為任意大小紙面化約及 Python 固定必要域證書，
未新增 Lean theorem。

## 1. 同一原來源與完整接合

G 有限簡單，指定有序 B=(b₀,…,b₄) 是 induced-C₅ disk 外框。
Σ(G) 為 933、941 或其整圖 D₅ 像，故接受全部 T4；每條非框邊 e
滿足 Σ(G−e)⊋Σ(G)。有效內部 H 連通，r 的完整 degree 六，其餘
有效內點完整 degree 四。三條原 spokes 的不同框端點集合為 S。

H−r 的原連通分量 Cᵢ 有具名有序接點 Pᵢ=N(r)∩Cᵢ，Σᵢ|Pᵢ|=3；
所有原邊、attachments、actual support、ownership、環序及嵌入固定。
對同一 proper boundary coloring b，Rᵢ(b) 是原 Cᵢ 完整染色產生的
有序接點 relation；接點 slack 及生成樹貪婪法保證它非空。原接合是

\[
J_b=\{(a,t_1,\ldots,t_m):t_i\in R_i(b),\quad
a\notin b(S)\cup\bigcup_i\operatorname{set}(t_i)\}.\tag{1}
\]

令 Fᵢ(b)=∩_{t∈Rᵢ(b)}set(t)。式 (1) 的精確 root 投影為

\[
\operatorname{proj}_r J_b
=U_4\setminus\bigl(b(S)\cup\bigcup_iF_i(b)\bigr).\tag{2}
\]

每個 surviving root 色都有各原分量的一份完整避色 tuple，能在同一
b 下拼接。F 只描述這個固定共同避色查詢，沒有替代完整 ordered
relations、取 marginals 或提供一般可迭代 state。全部列與分量共用
同一字面四色框；整圖 D₅ 搬運同時搬動目標、spokes 與原支援。

## 2. (1,1,1)：三份固定原支援需要六段框邊

完整 Σ edge-minimality 給每份原分量私有禁色見證：刪其一條原
root-contact 邊後的新染色，其 root 色在原分量被禁，其他原分量
及 spokes 卻容許它。來源拒絕多個 singleton 列，故
[完整支援引理](c5_independent_support_capacity.md#11-degree-與完整支援)
使同一 G 碰齊五框點。

若某份 Cᵢ 的全部實際支援包含於相鄰兩框點，取外面的已碰框點 h：
原 spoke 或另一原分量給避開 Cᵢ 的 r–h 路徑。
[短支援引理](c5_short_support_singleton.md#5-固定原來源的跨度推論)
遂迫其每列禁色集為空，與私有見證矛盾。因此各份原支援的共同
包含弧跨度 ℓᵢ≥2。

只為拓撲論證，各分量保留一條原 root 邊並收縮；
[同 root 相容 lifts](c5_independent_support_capacity.md#42-同一-root-的相容-lifts)
給同一嵌入的支援弧，開框邊段互斥，總跨度≤5。三份原 unary
因此需要 2+2+2=6>5。這相加的是固定原支援的幾何下界，各份私有
見證可以來自不同列；沒有把不同列的染色負載相加。

前序 [三原 unary 報告](c5_excess_two_three_unary.md)已排除整型；
本節復用後續較強的短支援引理，無需重做省略身份搜尋。

## 3. (2,1)：兩份 span-two 支援的同源 profiles

原 binary C 的有序接點是 (x,y)，原 unary V 的接點為 v。
|F_C|≤2、|F_V|≤1 由非空完整 relations 直接得到。
兩份共同支援包絡各跨度至少二。三條原 spokes 的扇區弧長度是
三個正整數，總和五，因此只有兩種 unordered 形狀：

- (1,1,3)：兩份 span≥2 包絡不能在同一長度三扇區內並排，短區亦
  放不下任一份，故沒有原來源。
- (1,2,2)：兩份分量各在一個長度二扇區，包絡恰為其三個框頂點。
  五份具名 spoke sets 乘兩份原 ownership，共十份固定配置。

Binary 的額外 root 邊只在上述拓撲 contraction 中刪除，原完整
R_C(b;x,y)、全部 root 邊及實際 attachments 在染色接合中完整保留。
兩包絡的首末點是同一原嵌入的實際附件；中間框點是容許位置，
不強加為原附件。

對一份三點包絡 I，若 b′|I=π∘b|I，則 π 同時搬運其全部原附件，
逐點換色給 R_W(b′)=πR_W(b)，所以 F_W(b′)=πF_W(b)。固定 b(I)
的所有色置換也須固定 F_W(b)。這只用同一原分量的完整 relation。
實際支援可能稀疏，依賴整份包絡的 profile 是安全必要放寬。

三連續框點的 equality pattern 只有 ABA、ABC。以已見色 0、1，
及第三個已見色 2 作**編碼代表**，stabilizer 與容量給：

| 原分量 | ABA 代表域 | ABC 代表域 | 完整十列 profile 數 |
| --- | --- | --- | ---: |
| Binary C | ∅、{0}、{1}、{0,1}、{2,3} | ∅、四色 singletons、六份 pairs | 5×11=55 |
| Unary V | ∅、{0}、{1} | ∅、四色 singletons | 3×5=15 |

每份代表選項先通過 stabilizer，再搬回該列的字面色框；不同
置換 completion 的結果一致。每份原分量兩個 equality classes
的選項共用於全部十列，不能逐列重選，也不將兩原分量獨立換色
後接合。全空 profile 亦保留，沒有用額外的私有見證 screen 刪域。

十份具名配置各核對 55×15 個 profile 對，共 **8,250 次完整十列
mask 比較**，沒有任何 mask 是 933／941 的十個 D₅ 像。
因此這個較寬必要域已空，整份 (2,1) 原來源不可能。
較強的固定域觀察是：其中 1,800 份接受全部 T4 的 profile 對，
1,440 份接受全部十列，360 份只缺一列；沒有三缺失或四缺失。
這是依賴前述紙面幾何的有限必要域結果，沒有宣稱所有抽象 profiles
都有來源實現。若刪掉同一原分量的跨列 profile 一致性，讓各列獨立
選禁色，100 個配置／目標查詢全部仍有選項；逐列資料不足以排除。
本輪不需要 binary 路徑、首橋局部 residual、D 身份守恆或任何
既有省略全收限制；前序
[binary 省略證書](c5_excess_two_binary_omission.md)繼續保留原範圍。

[Binary checker](../scripts/c5_excess_two_three_spoke_binary.py)及
[artifact](../artifacts/c5_excess_two_three_spoke_binary/observations.json)
保存具名扇區、ownership、包絡、完整十列字面 profiles、結果 mask
統計及精確完整接合控制。Profile 只是必要 root 查詢資料，不宣稱
每份都能實現為原 degree-4 分量或 disk source。
完整七接點 operator 保存 2,916 個 tuples；全部十五份非空 unary
domains 與 64 份字面 spoke triples，給 15,360 次 singleton binary
及 115,200 次二元素 binary relation 接合控制。另保存相同 endpoint
marginals 卻有不同完整 root 投影的碰撞，核對原有序 relation
不能被 marginals 取代。任意完整 relation 的接合由 ordered-tuple
fibers 的聯集精確重建；空纖維始終為空。

## 4. (3)：三接點容量一與三條 spokes 的虹彩位置

若原 ternary C 在任一 proper row 禁兩個不同 root 色，兩份拒絕
degree lists 的 active 結構迫原 triangle 加三條 bridge arms。
三條原 tethers、三條原 contact 邊及**任一條**原 spoke 給 K₅ minor，
與 planarity 矛盾。沿用
[三接點容量引理](c5_excess_two_ternary_two_unary.md#2-三接點在所有列都至多禁一色)，
該構造不要求 r degree 五或恰一條 spoke，因此本題每列 |F_C|≤1。
外部 degree-list／block palettes 依賴沿用
[Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)；
本輪重讀，確認其前提是連通圖及 degree assignment，不要求整份
G 在每列都是 minimal obstruction。

若 singleton 列 q_j 被拒絕，式 (2) 迫三條原 spokes 看齊三個框色，
且 F_C(q_j)={D}。q_j 唯一只用一次的框色出現在 b_j，因此 j∈S。

- 933 拒絕四個 singleton 位置，但 |S|=3，矛盾。
- 941 拒絕非連續三位置，共同 D₅ 搬運後可令 Q={0,1,3}。
  三次虹彩迫 S=Q；但 q₀=01212 在 S 上只見 {0,1}，尚缺框色 2
  及未用色 D。一份容量一的 C 無法補足，仍接受 q₀，矛盾。

[Ternary checker](../scripts/c5_excess_two_three_spoke_ternary.py)及
[artifact](../artifacts/c5_excess_two_three_spoke_ternary/observations.json)
逐項核對十份原 spoke sets、十份目標共 **100 次容量比較**。每項
保存目標拒絕但 spokes 至多見兩色的 named row，並對全部五份
容量零／一禁色選項保存非空 root domain。另核對 4,096 份
singleton 及 129,024 份二元素 ternary relation 的完整七接點接合。
Ports `(r,b_s,b_t,b_u,C_x,C_y,C_z)` 全部保留；任意非空 relation
的接合是其完整 ordered-tuple fibers 的聯集。這個代數控制不證
紙面容量引理，也沒有把 ternary marginals 相乘。

## 5. 結論、重播與精確停止點

三種原接點分拆 (3)、(2,1)、(1,1,1) 全部排除，故同一完整來源
前提下 t≠3。連同前序得 **t∉{1,2,3}**。

既有 [T4 限制](c5_excess_two_double_spoke.md#2-為何恰落在原-148-個標記核心)
又給 t≤3：任四個原框鄰點可用四色，剩餘框點設成一個非鄰點色，
得到 proper T4 row 而 r 無色。新增 ternary 證書另保存五份四-spoke
及一份五-spoke 的原框 row witnesses。因此唯一 degree-6 root 若
仍存在，必為 **t=0**；沒有排除無 spoke 或兩個 degree-5 roots。

```bash
python3 scripts/c5_excess_two_three_spoke_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_three_spoke_binary.py --check
python3 scripts/c5_excess_two_three_spoke_ternary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_three_spoke_ternary.py --check
python3 scripts/c5_short_support_singleton.py --check
python3 scripts/c5_single_spoke_three_one.py --check
python3 scripts/c5_excess_two_three_unary.py --check
python3 scripts/c5_excess_two_double_spoke.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

實際本輪重播、產物大小及檢查結果見研究紀錄；沒有重跑所有歷史
來源 catalogue、全 degree-4／Gallai 證書或 Lean axiom audit。
任意大小 tightness、K₅、相容 lifts 由紙面及明列外部依賴承擔，
Python 只證固定必要域及局部完整 relation 代數，`lake build` 不把
這些新紙面結論提升為 Lean theorem。

下一窄入口是唯一 degree-6 root 的 **t=0**：保留六個原 contacts、
全部原分量及共同框色，先核對無原 spoke 時外部 hub 的連通前提。
不能直接把本輪「至少一 spoke」的短支援／active-triangle K₅
論證移植過去。停止點由 [Kempe 導覽](c5_kempe_guide.md)維護；共同
ε≥2、一般出口與 `K∞=K≤5` 的證據界線維持。
