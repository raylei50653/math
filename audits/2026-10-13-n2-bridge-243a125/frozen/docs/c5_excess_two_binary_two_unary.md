# ε=2：t=2、(2,1,1) 的原 binary 省略排除

**後續（2026-10-03）**：[通用短支援引理](c5_short_support_singleton.md)
迫本型三份原分量各至少兩段跨度，因而排除整型來源；見
[合成報告的共同推論](c5_excess_two_single_spoke_complete.md#4-結論證據層與停止點)。
下文保留當輪省略核心的證明及證書。

**後續（2026-10-03）**：[四原 unary 排除](c5_excess_two_four_unary.md)
已完成本輪留下的 t=2、(1,1,1,1) 下一窄題；下文維持本輪 binary
省略的證據範圍；當輪保留的整份 (2,1,1) 來源由頁首短支援推論排除。

2026-10-03，基準 `bbd900a`，接續工作樹的
[兩原 unary 省略排除](c5_excess_two_two_unary.md)。目前接手入口見
[Kempe 導覽](c5_kempe_guide.md)，當輪驗證見
[研究紀錄](history/2026-10-03-excess-two-binary-two-unary.md)。

**結論：933／941 的固定完整 Σ、edge-minimal C₅ disk 來源，若 ε=2、
唯一 degree-6 root r、t=2，且 H−r 的原接點分拆為 (2,1,1)，則省略
整份原 binary A 後必接受全部十列。**

連同前序全部 unit-pair 省略全收，該型已無全 degree-4 的 minimal
rejected-row core。這沒有排除整份 (2,1,1) 來源；其餘 ε=2、兩個
degree-5 roots（含 mixed）、一般出口及 K∞=K≤5 仍保留，共同下界仍 ε≥2。

證據是任意大小紙面必要化約與 Python 固定集合證書，沒有來源圖枚舉、
path／tail 替換或新 Lean theorem。全 degree-4 分類、外部 degree-list
及同圖 D 守恆沿用既有報告；不是由有限支援配置外推任意大小。

## 1. 原分量及完整五接點接合

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框；完整 Σ
為 933、941 或整圖 D₅ 像。每條非框邊 e 都有 Σ(G−e)⊋Σ(G)。有效
內部 H 連通，r 完整 degree 六，其他內點完整 degree 四。
r 的兩條原 spokes 是 rb_s、rb_t，s<t；H−r 的原連通分量是 A、U、V，
接點分別為有序 (x,y)、u、v。保留全部原附件、ownership、內部邊及嵌入。

對每個 proper boundary coloring b，原完整 relations 為 R_A(b;x,y)、
S_U(b;u)、S_V(b;v)。刪 r 後以 slack 接點為生成樹根逆序貪婪，三者
均非空，詳見[容量介面](c5_independent_support_capacity.md#2-任意-root-的完整條件介面包含-mixed)。
原完整五接點關係是

\[
\mathcal R_G(b)=\{(a,c,d,e,f):(c,d)\in R_A(b),\ e\in S_U(b),\ f\in S_V(b),
\quad a\notin\{b_s,b_t,c,d,e,f\}\}. \tag{1}
\]

每個 tuple 都由同一 b 下三份原分量的完整染色拼成，再檢查四條原 root
邊。令 F_A=∩_{(c,d)∈R_A}{c,d}，容量至多二；F_U=S_U 若 |S_U|=1，
否則 F_U=∅，F_V 同理。式 (1) 的精確 root 投影為

\[
U_4\setminus(\{b_s,b_t\}\cup F_U\cup F_V\cup F_A),\qquad U_4=\{0,1,2,3\}. \tag{2}
\]

以下的 F 只用於固定原接線的 root 判斷，並非完整 relation 的替代
state。尤其 R_A 不拆成 marginals，不逐分量或逐列另選色框。所有
singleton rows 共用未用色 D=3，D₅ 只作用於整張來源。

## 2. 同一省略核心與兩份 unary 的固定身份

反設 K=G−A 拒絕 q₀。K 的有效內部連通、所有內點完整 degree 四，並
繼承 disk 與 T4 全收。任取 minimal q₀-core，degree-4 飽和沿內部
傳播使 core 等於整張 K。[全 degree-4 分類](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)給

\[
\Sigma(K)=\Omega\setminus\{q_0\}. \tag{3}
\]

q₀ 因此是原目標拒絕的 singleton 列。r 在 K 有兩條分屬 U、V 的內部
bridges，不在 cycle 上；不需要枚舉其 path／tail 長度。
在 q₀ 下，四個 unit 因子 {b_s}、{b_t}、F_U、F_V 必恰為四色互異的
singletons。因此 U、V 恰有一份禁 D，另一份禁 boundary 色。
[同一原 unary 的 D 守恆](c5_excess_one_subcovers.md#4-單接點分量的跨列-d-身份不能互換)給固定
(d_U,d_V)∈{(1,0),(0,1)}：五個 singleton 列中，d=1 的 F 只可為 ∅
或 {D}，d=0 的 F 只可為 ∅ 或某個 boundary 色。非 D 色名不必守恆。

### 2.1 支援下界屬於同一原分量

兩份 unary 及其全部附件在 K 中完整保留，故由分類是 K₄-free Gallai
trees。每份 C∈{U,V} 都至少有兩個不同實際框鄰點：

- 無框附件時，其 endpoint relation 在 S₄ 下不變，不能在 q₀ 強迫一色。
- 若只接 b_j，令 q₀(b_j)=a。固定 a 的色置換迫其 singleton 色等於 a。
  固定 r=a 後 C 的 degree lists 不可染，處處 tight。若某點有兩個
  C 外鄰居，兩者同色 a，便有 list slack，矛盾。故每點 deg_C≥3；
  但非平凡 K₄-free Gallai tree 的末端 block 有非割點的 degree≤2，
  singleton C 亦不可能，矛盾。

同一原支援的任何包含弧遂有跨度至少一。d=1 的分量在 q₀ 禁 D，
其支援必見到全部三個 boundary 色；否則交換兩個未見色會破壞 singleton。
因此共同支援 lifts 滿足

\[
\ell_U\ge1+d_U,\qquad\ell_V\ge1+d_V. \tag{4}
\]

這與[三 unary 支援引理](c5_excess_two_three_unary.md#3-三份原分量的固定支援下界)
是同一論證；本輪用已指定的 K 保證 U、V 的 Gallai 前提。
**A 不套 Gallai 或正跨度假設，允許其跨度為零。**

## 3. 全部六個 unit-pair 省略與共同支援弧

令四個具名 unit 因子 T₀={b_s}、T₁={b_t}、T₂=F_U、T₃=F_V。
[雙 spoke](c5_excess_two_double_spoke.md)、[spoke＋unary](c5_excess_two_spoke_unary.md)
及[兩 unary](c5_excess_two_two_unary.md)已證所有兩-unit 省略必全收。
用保留的兩個 unit 表示，對每列及每個 0≤j<k≤3，

\[
F_A\cup T_j\cup T_k\ne U_4. \tag{5}
\]

所有六個限制都屬同一原來源的具名子圖。式 (3) 另要求
∪ᵢTᵢ=U₄ 當且僅當該列是 q₀。作為檢核，若某拒絕列 |F_A|=2，
其餘兩色必能從兩個 unit 取到，直接違反式 (5)；故這類選項必被刪除。

兩條原 spokes 把 disk 分成兩個閉扇區 J₀、J₁，框弧長度總和五。
三份原分量各連通且不能跨 spokes，全部實際框支援各落在某一扇區。
只為拓撲論證刪除 A 的一條 root 邊，再將 A、U、V 各收縮為一個點；
由[共同 root 的相容 lifts](c5_independent_support_capacity.md#42-同一-root-的相容-lifts)，
同一嵌入有三份包含弧 I_U、I_V、I_A，各在指定原閉扇區內，同區的
開框邊段互斥，允許共享端點。取各組第一與最後實際附件為端點。
A 若無附件，可將其空支援置於相鄰間隙的端點，以零跨度包絡涵蓋。

這裡只刪邊／收縮以證明弧的位置限制，R_A、S_U、S_V 仍在原圖計算。
所有原 root 邊次序均容許，不把弧上每個框點新增為附件。
記 seen_C=b(I_C)。因為它包含原支援色，必要條件為：

1. d_C=1 且 F_C={D} 時，|seen_C|=3。
2. d_C=0 且 F_C={a} 時，a∈seen_C。
3. 對 A，任何逐色固定 seen_A 的置換都保持完整 R_A 和 F_A。令
   W=U₄∖seen_A，則 F_A∩W=∅ 或 W⊆F_A。

第三項容許 F_A 空、單色、二色，沒有把含 D 的 binary 一律視為 unary。
共同包絡弧先固定，才逐列套用見色限制；不同列不能另挑支援弧。

## 4. 固定必要域與排除證書

[Checker](../scripts/c5_excess_two_binary_two_unary.py)及
[artifact](../artifacts/c5_excess_two_binary_two_unary/observations.json)列出十種原
spoke pairs、兩種具名 D 身份、兩候選各五個 D₅ 像及目標拒絕的 q₀。
每個 singleton 列獨立放寬選兩份 unary 的空／singleton 禁色及
|F_A|≤2，套式 (2)、(3)、(5)。僅這些代數限制仍有殘留。

然後枚舉同一兩扇區內滿足式 (4) 的全部支援包絡，三份弧共用同一
原 frame，對全部五列套 §3 見色限制。每個實際來源必被某份配置涵蓋；
容許跨列獨立選 F 比同一原圖的完整 relations 更寬。因此放寬域為空
就足以排除，沒有聲稱任一抽象選項可由圖或 disk 實現。

| 必要域 | 933 五像 | 941 五像 |
| --- | ---: | ---: |
| (spokes, D 身份, target, q₀) 比較 | 400 | 300 |
| 僅代數限制後存活 | 320 | 240 |
| 存活 case 與共同支援弧的比較 | 37,200 | 27,900 |
| 加入共同弧的見色限制後存活 | 0 | 0 |

兩種 D 身份合計 2,340 份具名包絡配置；65,100 次比較全有空必要列。
證書保存全部 700 份代數 cases 的五列完整選項、全部幾何配置，以及
逐比較的原 case／geometry 索引、首個空列及五列選項數。Checker 從
具名端點及原框色重算，不讀取排除 flags。只查五個 singleton rows 已足夠；
沒有計算或宣稱抽象選項在五個 T4 rows 有共同實現。

另有 65,535 份非空有序 binary relations 的完整三接點投影控制，並
對全部十一種可達 F_A 選取完整 relation 代表，加上相關性反例及全集，
共十三份。每份保存完整五接點算子，再限制到全部 15×15 非空 unary
domain pairs 及十六個 spoke 色集，以獨立 Cartesian-product 定義核對
完整 tuples 與式 (2)，合計 46,800 次。穩定子條件以全部 24 個 S₄
置換核對 176 組輸入。這些是局部代數控制，不是原來源染色證書。
同 marginals 的 R₁={(0,1),(1,0)}、R₂={(0,0),(1,1)} 分別有
F₁={0,1}、F₂=∅，在 artifact 中保留以防誤換成 marginals。

必要域全空，反設不成立，故

\[
\boxed{\Sigma(G-A)=\Omega.}
\]

## 5. 重播與停止點

```bash
python3 scripts/c5_excess_two_binary_two_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_binary_two_unary.py --check
python3 scripts/c5_excess_two_two_unary.py --check
python3 scripts/c5_excess_two_spoke_unary.py --check
python3 scripts/c5_excess_two_double_spoke.py --check
python3 scripts/c5_single_spoke_root_conservation.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

本輪完成 t=2、(2,1,1) 的最後容量二省略身份。若全 degree-4 拒絕核心
存在，它必含 r；否則某原分量接點失去 root 邊而 degree 不足四，飽和
沿該原分量傳播便不可能留下任何內點。含 r 時，所有保留的原分量及
其 incident 邊必完整保留，r 從六降四只能省略 A 或四個 unit 中的一對。
所有這些省略都已全收，故該型沒有全 degree-4 的 minimal rejected-row core。

仍可能有含 degree-5／degree-6 的 minimal core；未排除整份 (2,1,1)、
其餘 ε=2 或一般來源。下一窄題見導覽。新證據未 Lean 化，`lake build`
只驗證現有 Lean 專案；全 degree-4 分類及外部 degree-list 前提沿用
依賴報告，沒有重播其全部歷史模板。共同下界仍 ε≥2。
