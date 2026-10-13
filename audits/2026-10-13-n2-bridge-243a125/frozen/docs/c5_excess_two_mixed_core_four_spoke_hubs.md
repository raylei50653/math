# ε=2 四-spoke binary：同列端點 hub 與整個子型排除

**後續（2026-10-03）**：[原 mixed-(1,2) 三接點身份排除](c5_excess_two_mixed_core_four_spoke_ternary.md)
已完成本頁下一窄型 mixed-(1,2) 加一單接點 unary，含 root 交換；
原 C+a 的三接點原樣銜接既有 active-triangle K₅。mixed-(1,3) 無 unary
仍保留；下文的 binary 數字與當輪停止點保持。

2026-10-03，接手基準 `b63a096`，保留前輪未提交工作樹。接續
[原 a-star 扇區排除](c5_excess_two_mixed_core_four_spoke_star.md)的
012／2、S_C=04、S_U=234 入口。現況由 [Kempe 導覽](c5_kempe_guide.md)
維護；實際驗證與貼用摘要見 [本輪紀錄](history/2026-10-03-excess-two-four-spoke-hubs.md)。

**指定入口及四-spoke (3,1)、mixed-(1,1) 加一原 binary unary 的
整個子型均已排除，含 root 交換。** 前序 933／941 的 32／64 份
具名必要域全部符合本頁同列端點 hub 引理，剩餘為 **0／0**。
不需要新增跨列 palette 定理；共同下界仍 ε≥2，其他原 incidence
型、一般單省略與 ε≥3 仍未證，沒有新增 Lean theorem。

## 1. 同一原來源及完整 relations

沿用前序全部來源前提：G 有限簡單，指定有序 induced-C₅
B=(b₀,…,b₄) 為 disk 外框；完整 Σ 為 933／941 或整圖 D₅ 像，
每條非框邊 Σ-critical；有效內部 H 非空連通，ε=2，恰兩個相鄰
完整 degree-5 roots a、b，其餘有效內點完整 degree 四。
a 有三原 spokes，b 有一原 spoke bb_s。

H−{a,b} 恰為原 mixed C 與原 unary U。C 的原 incidence-(1,1)，
contacts=(x,y)、owners=(a,b)，容許 x=y。U 的原 contacts=(u,v)
不同，皆接 b，屬於同一原連通分量。原邊為 ab、ax、by、bu、bv。
保持 actual supports S_C、S_U、原附件、環序、所有共同 lifts、
完整 R_C(β;x,y)、R_U(β;u,v) 與原 (b,a,y,u,v) joint／pinned fibres。

定義

\[
F_U(\beta)=\bigcap_{t\in R_U(\beta;u,v)}\operatorname{set}(t).
\]

原完整 R_U 非空；若 d∈F_U(β)，就是同一原 U 在兩 contacts 都
禁止 d 的 lists 不可著色。前序殘留逐份給出這樣的 d，不能把 U
拆成兩份 unary，亦不能從 marginals 判定避色。

## 2. 同色端點合併的必要條件

固定同一字面列 β 及 d∈F_U(β)。對 w∈U 取原 lists

\[
M(w)=U_4\setminus\bigl(\beta(N_B(w))\cup
(\{d\}\text{ if }w\in\{u,v\}\text{ else }\varnothing)\bigr).
\tag{1}
\]

完整 degree 四給 |M(w)|≥deg_U(w)。連通且不可著色使各點
等號成立，故每點原外鄰色兩兩不同。尤其，若 z∈S_U、β_z=d，

\[
\boxed{w\in\{u,v\}\Longrightarrow wz\notin E(G).} \tag{2}
\]

否則原 b 與 z 都向 w 禁 d，產生 list slack，按生成樹逆序貪婪
即可染整份 U，矛盾。式 (2) 使用整份 U 的拒絕，而非 contact
邊的 minimality；不要求 G 是這份 β 的 minimal q-core。

沿用外部 [Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
取得 tightness、Gallai tree 及 blockwise-uniform palettes；本輪重讀
核對。B∪{a,b} 經原 a-spokes、ab、bb_s 連通，沿用
[連通外部 K₄ 排除](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)。
該論證只需 U 的拒絕 lists：K₄ 每點的唯一外方向，若是 bridge，
其外側由 block palettes 強迫根色，故必碰連通外部；四方向合成
第五組即給 K₅。這裡不假設新的 q-minimality。於是 U 的 blocks
只有 bridges／odd cycles，後續可使用既有二／三 hub Gallai 引理。

### 指定入口的三個原外部 bags

原 a=6、b=5、a-spokes=012、b-spoke=2、S_C=04、S_U=234；
取 q=01021。前序完整 schemas 給 F_U(q)={1}，q₄=1。因此式 (2)
禁止 u、v 接 b₄。取三個原外部 branch sets

\[
X=\{b_2\},\qquad Y=\{b_3\},\qquad
Z=\{b_0,b_1,b_4,a,b\}. \tag{3}
\]

Z 沿原 b–a–b₀–b₄ 及 b₀b₁ 連通，避開整份 C、U。X–Y、Y–Z、
Z–X 分別有原邊 b₂b₃、b₃b₄、bb₂。三組互斥。

U 的原外鄰只有 b₂、b₃、b₄、b。合併 Z 時，唯一可能重複的
兩個 U 鄰居是 b、b₄，已由式 (2) 排除，所以每個 U 點在 minor
中完整 degree **仍恰四**。給 X、Y、Z 輔助顏色 0、2、1，其
對 U 的 lists 精確等於式 (1)，仍不可著色。

由 [三 hub Gallai 引理](c5_short_support_singleton.md#4-三-hub-引理排除未見色接點數不設上限)
得到 K₅ minor，與原 disk 的 planarity 矛盾。將 Z 展開回式 (3)
即得原 G 的五個 connected branch sets。原 C 對角 pair／偶數
bridge（含 x=y）及所有旁支均保留；C 不是此 minor 的一個 hub。

**上述合併只用於 topology。** Z 中中間點的原顏色不必等於 1，
它們沒有 U attachments；只有 b、b₄ 的附件色被同色合併。
沒有把 Z 改成染色 factor，沒有改寫原 R_C、R_U 或完整 Σ。

## 3. 二／三 hub 引理如何給原 K₅

沿用 [短支援報告 §§3–4](c5_short_support_singleton.md#3-兩-hub-gallai-引理五個-branch-sets)
的任意大小紙面論證；以下列出提升所需的全部情形。

**二 hubs。** U 每點完整 degree 四，外鄰最多兩個，故 min deg_U≥2。
末端 block 必是 odd cycle。取相鄰 private vertices r,t，兩者都接
兩 hubs；U′=U−{r,t} 非空連通，並含另一原 degree-two 頂點，亦接
兩 hubs。五組為兩 hubs、{r}、{t}、U′，十對鄰接都有原邊。

**三 hubs，末端 odd cycle。** Private vertices 的同一二元 list
迫它們接同一對 hubs。取相鄰 private r,t，U′ 非空連通。若第三
hub 碰 U，必碰 U′，將它加進 U′ 成第五組；其 triangle 邊給
第五組到前兩 hubs 的鄰接。若第三 hub 不碰 U，回到二 hub 引理。

**三 hubs，末端 bridge rt，r private。** r 接全部三 hubs，list
只有未用色 D。刪 rt 後 U′=U−r 在 t 有 slack，故可染；若某 coloring
令 t≠D，便能接回 r=D，故完整 t-domain 恰為 {D}。U′ 必碰全部
三 hubs，否則交換 D 與漏掉的 hub 色便改變 t，矛盾。五組為
三 hubs、{r}、U′，十對鄰接來自 hub triangle、r 的原附件、rt 及
U′ 的原附件。這裡仍用整份 U′ coloring，不以 palette 計數代替。

末端 blocks 已窮盡 K₄-free Gallai tree。論證不限 U 的大小、cycle
長度或旁支數；Python 短圖控制不承擔任意大小覆蓋。

## 4. 原 32／64 份域的完整覆蓋

[Checker](../scripts/c5_excess_two_four_spoke_binary_hubs.py)／
[artifact](../artifacts/c5_excess_two_four_spoke_binary_hubs/observations.json)
只讀前序 star 證書及短支援控制，SHA256 綁定原 bytes；原產物不覆寫。
保留每份原 frame、domain、assignment identities、逐 query 的原
candidate／整體 transport、完整 K/C options、共同 lifts 及每個完整
有序 U schema，沒有獨立正規化兩分量。

對每份 query，取 S_U 中 β_z=d 的端點。其餘一或兩個框點分別
作 singleton hubs；其餘框點與原 a、b 作 Z。逐份核對 Z 連通、
bags 互斥、原 hub 鄰接、U 外鄰的唯一可能合併，以及輔助 hub
色互異。三支援型的另兩點必相鄰；二支援型直接用二 hub 引理。

| 具名必要域，含 root 交換 | 933 | 941 |
| --- | ---: | ---: |
| 前序 star 殘留 | 32 | 64 |
| 二 hub Gallai 排除 | 16 | 32 |
| 三 hub Gallai 排除 | 16 | 32 |
| 本輪剩餘 | **0** | **0** |

192 份原 query 全覆蓋；10,752 份完整 U schemas 核對原禁色、逐
contact 解除與 actual-support 穩定子；2,208 份局部 degree／list
控制核對同色合併碰撞必產生 slack。96 次 root 交換保存原完整
assignments；1,920 次整體 D₅ 搬運核對所有外部 hub 前提。這些是
原域適用紙面引理的證書，不是 96 張未知原 U 的有限圖 witnesses。

另有 42 張完整 degree 圖，含 root 交換：C 取長度 0、2、4 的
偶數 path；U 取長度 3、5、7 的 bridge path、長度 3、5、7 的
odd cycle，以及沿用的一份末端 cycle／第三 hub 旁支控制。
保存所有原邊、actual attachments、完整 C／U tuples 與逐 tuple
coloring witnesses、空原 joint，以及五組 connected bags／全部
十對原鄰接。逐圖核對同色合併不降低 U degree。固定圖不聲稱
disk、候選完整 Σ 或 Σ-criticality。

## 5. 重播、信任層與停止點

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_binary_hubs.py --check
python3 scripts/c5_excess_two_four_spoke_binary_hubs.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_binary_star.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_four_spoke_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

實際環境與重播範圍見本輪紀錄。原 binary 重播包含 720 全圖 joints、
11,520 pinned fibres 與舊 `(2,2)` 全部數學 payload／support table。
單一舊 docs hash 漂移仍保留，沒有改寫舊 artifact 或宣稱其原
byte-check 已修復。前序證書中的 32／64、116／256 保留原輪次語境。

信任層為同列 list slack／外部 degree-list 定理／二、三 hub Gallai
紙面 minor、前序必要分類及 Python 具名域與原圖控制。沒有使用
四色定理 oracle、未重開來源圖枚舉；`lake build` 不形式化本輪 topology。

**停止點：四-spoke (3,1)、mixed-(1,1) 加一原 binary unary 子型
全作來源排除，含 root 交換；在此停止。** 下一窄型是同 spoke
分拆下 mixed-(1,2) 加一單接點 unary：保留原三接點 relation，
先核對同色原 spoke 省略後的 (3,1) q-core 身份，與
[既有三接點 active-triangle 排除](c5_single_spoke_three_one.md)的前提。
尚未在本輪證明該原來源型排除。
mixed-(1,3) 無 unary、其他四-spoke／較少 spokes、(5,5) q-core、
多 mixed／no-mixed／非相鄰 roots 仍保留。共同 ε≥2 不變；
跨列 palette 定理、ε≥3、一般出口及 K∞=K≤5 仍未證。
