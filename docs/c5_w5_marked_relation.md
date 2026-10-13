---
docgraph:
  id: c5.w5-marked-relation
  family: [c5, c5.w5]
  related: [c5.degree5-link-reductions]
  verified_by:
    - audits/2026-10-12-w5-marked-relation-e299ae98/REPORT.md
    - audits/2026-10-12-w5-marked-relation-e299ae98/review/INDEPENDENT.md
---

# 全內部 W5 的具名完整關係縮減

2026-10-13 整理：本頁是十 pin 完整關係的權威入口，也串接私人圈秩排除鏈。
原全內部五輪的來源前提見[全內部五輪與任務交付](c5_degree5_link_reductions.md)；
本頁的五商圖染色恆等式本身不需最小性。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)維護。

原成果日期為 2026-10-12，完整證明與證據見
[隔離報告](../audits/2026-10-12-w5-marked-relation-e299ae98/REPORT.md)、
[獨立審查](../audits/2026-10-12-w5-marked-relation-e299ae98/review/INDEPENDENT.md)
及[發布紀錄](history/2026-10-12-w5-marked-relation-publish.md)。
以下 §§1–4 保留原輪次論證、內點門檻及重播紀錄；當時的 OPEN 由後續鏈判讀，
不改凍結證據。目錄內點界後續由 [K13](c5_k13_collar.md)、[K14](c5_k14_sphere.md)
提高至 [K15](c5_k15_sphere.md)；這些界不等於一般 W5 代表存在定理。

## 0. 保存強度與私人圈秩覆蓋鏈

在同一 literal 四色框中，`J_A(β,τ)` 保存刪中心 annulus A 的完整染色，
`R_A³` 是 U 恰用三色的非空具名 cells，補中心後的完整外框關係為
`Σ(A+v)=pr_B R_A³`。三種保存目標須分別判定：

| 目標 | 必須保存的資料 | 已證內容與界線 |
| --- | --- | --- |
| 完整 fibres／lifts 重建 | 十個原 B/U pins、每列全部 1,024 cells（含空格）、每份完整私人指派及原商映射 | 本頁五商圖拉回到同一 H，按同一 lift 的重數無損重建 H/G；只存商圖的外框 Σ 無法重建 |
| 保 `R_A³=R_A′³` | 同槽位、同色框的每個三色 `(β,τ)` cell 同時非空或同時空 | [三色支援 §1](c5_w5_three_color_support.md#1-同槽位契約與精確保存目標)給保 B/U 及中心色的雙向 total full-lift 對照；不要求 fibre 雙射、重數相同、四色 U support 相同或私人指派可逆 |
| 保完整 `Σ(A+v)=Σ(A′+v)` | `pr_B R_A³=pr_B R_A′³`，並有合法同槽位替換；外部環境只沿 B 接入 | 只需保 B 色列的雙向 total full-lift 搬運，可改 U／中心色；[單環](c5_w5_private_unicyclic.md)及[雙環](c5_w5_private_rank2.md)的代表用此目標，不保 R³ |

證書保存來源與代表**各自**的全部 fibres/lifts，不表示兩圖的 fibres 相等。
來源化成必要模板時則須以原圖同構搬運全部 pins、原邊、實際附件、rotation、
ownership、分量及 bridges，再搬運全部空／非空 fibres 和 full lifts；
它保同一原圖的完整資料，不能與較小代表的 Σ-only 搬運混為一項。

私人圈秩鏈的共同前提是：G 在**所有**完整 `Σ(G)∉K132` 的有限簡單
plane disk-C5 圖中先最小化內點數 k，再最大化邊數；沿用原共面正規形、
完整 G-degree、原三角面及小分隔環限制，並保留其四色定理與外部計數依賴。
在此 G 中**任取**合法全內部 induced W5，保原 B、中心 v、循環鄰環 U，
十 pins 互異且 U 內恰為 v 與五個原三角面。令
`P=V(G)\(B∪U∪{v})`、`F=G[P]`、`r=k−6`，
`ρ(F)=|E(F)|−|V(F)|+c(F)`，c 包括私人孤立分量。
完整 degree 下界屬 G，不能當成 F 的私人 degree 下界；也不另加 F 連通、
N2、ε、edge-critical 或 Gallai 前提。

| 排除範圍與入口 | 分支覆蓋／必要模板 | 接上前一步後的下界 |
| --- | --- | --- |
| [森林：三色支援 §2](c5_w5_three_color_support.md#2-最小來源的私人森林已排除) | 任意大小、多分量及分支樹化成七／八點路徑；70 份模板完整 Σ=1023 | `ρ≥1` |
| [單環](c5_w5_private_unicyclic.md) | contractible 純紙面排除；essential 化成純環，1,652 份完整 Σ=1023；另有只保 Σ 的 prism 嚴格代表 | `ρ≥2` |
| [雙環](c5_w5_private_rank2.md) | 四種私人核心、全部細分／附樹及 essential 位置；剩 contractible theta 的 974 份模板，四個只保 Σ 的嚴格代表 | `ρ≥3` |
| [圈秩三 essential](c5_w5_private_rank3_essential.md)＋[contractible](c5_w5_private_rank3_contractible.md) | 分隔 B/U 的原環域 1,283 份；U/v 在 F 無界面域 c=1 的 2,162 份及 c=2 的 108 份；兩支窮盡，直接完整 Σ∈K132 | `ρ≥4` |
| [圈秩四兩分支](c5_w5_private_rank4.md) | 同一原嵌入的 contractible 6,389 份＋essential 2,872 份；兩支窮盡，直接完整 Σ∈K132 | **`ρ≥5`** |

2026-10-13 新接入：[W5-NO4CT-BRIDGE](../audits/2026-10-13-w5-no4ct-bridge-d521163/REPORT.md)
在 no4ct 全域最小目錄外來源契約下，逐條接通森林至圈秩四，932／933／941
三支任取合法全內部 W5 均得 **ρ≥5**，沒有剩餘低圈秩橋接引理缺口。
[依賴矩陣](../audits/2026-10-13-w5-no4ct-bridge-d521163/DEPENDENCIES.md)以原小cap及附件界重證局部前提；
新 k≥16、r≥10 屬原完整必要域子集。七份原seal／407筆記錄保留，舊完整
染色證據沿用，未重枚舉；上表的原輪次及原4CT依賴保留為歷史證明路徑。

森林至圈秩三各輪沿用 `k≥13,r≥7`；圈秩四兩支的 BASE 為 `acd2b1b`，
沿已採納 K13 使用 `k≥14,r≥8`。各輪 BASE、來源限制與模板超集以連入的
原報告為準；不以後來 K15 改寫原枚舉前提。圈秩三／四的直接目錄排除
不需要較小代表，也不宣稱模板間的 R³ 相等。

因此 **在上述完整最小目錄外來源前提下，任取合法全內部 W5 的私人圈秩至少五**。
紙面完備化約承擔任意大小量詞，Python 證書核對有限必要核心；真正最小
933／941 實例仍為 `not triggered`，零觸發不承擔排除。沒有新增 Lean theorem。
一般 `ρ≥5` 來源的合法縮減、一般小代表（含當前 K15 的 `r′≤9` 目標）、
保 R³ 的一般代表及 `K∞=K≤5` 均仍 **OPEN**；
已認出 K132 的代表與具體縮減族見[三色支援的最新界線](c5_w5_three_color_support.md)。

本次文件整理核對上述來源前提、分支覆蓋、保存強度及前後連結，沿用原報告
的染色證書與審查紀錄；未重跑研究枚舉、上游外部計算或 Lean build。

## 1. 前提與保存的完整資料

固定有限簡單 plane disk 圖 G、原有序外 C5 框 B，以及五度原內點 v。
其全部鄰點按原旋轉為 U=(u0,…,u4)，U 與 B 不交且誘導 C5；
U 的有界內側恰由 v 及五個三角面填滿。刪中心得 H=G−v。
保留同一原圖的 labels、原邊、附件、ownership、旋轉與空出的五邊面。
此槽位由 [最小來源全內部五輪定理](c5_degree5_link_reductions.md) 條件性供應；
下面的完整染色恆等式本身不需最小性或 edge-critical／N2 身份。

在共用色集 C={0,1,2,3} 下，保存

\[
J_H(\beta,\tau)=\{\eta\in\mathcal C_H(\beta):\eta(U)=\tau\},
\qquad \tau\in C^5.
\]

beta 是外框十個固定代表之一；每列全部 1024 格，包括空 fibres，均保留完整 H
染色。只能共同更名全圖顏色，不能獨立正規化 U，也不能以外框十個 bits 代替 J。

## 2. 五個合法較小圖無損重建 H 與 G

令 Q_j 由 H 在原 U 空面內單獨識別 u_j=u_(j+2) 得到，下標模五。
非鄰接保證沒有 loop；沿面內弧收縮後只簡化平行邊，保留全部原邊 preimages。
B 不被識別，仍是外面。五個操作各自合法，不同時施行。
若 G 有 k 個內點，各 Q_j 有 k−2 個。

以具名商映射 pi_j 將完整 Q_j 染色拉回同一 H，得

\[
S_j(\beta)=\{\chi\circ\pi_j:\chi\in\mathcal C_{Q_j}(\beta)\}.
\]

proper C5 的三色型為 (2,2,1)，四色型為 (2,1,1,1)。因此任一完整 H 染色 eta
在五份 S_j 中的重數 m 恰為二或一：m=2 時 U 用三色，中心可且只能取唯一缺色；
m=1 時 U 用四色，不能接中心。這逐份給出

\[
\mathcal C_H(\beta)=\bigcup_j S_j(\beta),\qquad
\operatorname{res}_H\mathcal C_G(\beta)
=\{\eta:m(\eta)=2\}.
\]

所以只需五份商圖的完整 lifts 與原映射，即可重建全部 H／G fibres；不必另枚舉 H。
商圖中的兩個 U pin 像重合，原十個 pin 名稱仍透過 pi_j 保留。
其逐 fibre 帶符號恆等式亦給計數推論

\[
|\mathcal C_G(\beta)|=\sum_j|\mathcal C_{Q_j}(\beta)|-|\mathcal C_H(\beta)|.
\]

這是完整染色資料的縮減。各 Q_j 的外框關係只保留存在性，無法辨認同一 eta
出現幾次；即使較小圖的關係都在 K，也不能僅由 K 的聯集封閉推出原 G 在 K。

## 3. 正聯集與 annulus 代表的界線

可接中心的五種互斥型以單色位置 i 指定：
u_(i+1)=u_(i+3)、u_(i+2)=u_(i+4)。兩個等式必須由同一份 H lift 同時滿足。
它們的接線交錯，不能直接當成合法的雙對商圖；prism 控制甚至給實際 K3,3
subdivision。各識別列分別接受也不保證存在共同 lift。

紙面另排除普遍適用的局部方案：只用原 U 頂點、加邊及空面內非交叉識別，
而不加新頂點的分支，不能以正聯集實現完整 wheel rim 關係。其任一三色 lift
都可拆色成仍合法的四色 lift。這不排除特定 annulus 過濾多出的 lifts，
也不排除改動 annulus 其他頂點的合法縮減。

若能找到同一 B/U 槽位、完整具名 support 相等的 annulus 代表 A'，保留兩向
完整延伸構造，且 B/U 外私人點 r≤6，補中心後即有 5+r+1≤12 個內點。
不同代表 fibres 不必等基數；此小代表尚未構造。
**一般合法正聯集縮減、r≤6 annulus 代表、十四內點以上來源及 K∞=K≤5 仍 OPEN。**

## 4. 有限證據與重播

固定域為 prism、其32種 annular triangulations 及一份有非單元素 fibre 的裝飾圖。
34 圖保存348,160格，其中345,580空格；完整 H／G／商圖 lifts 分別為
3,250／1,620／4,870。170個合法商圖的直接 DFS 與拉回相同，獨立程式亦完整重算。
只保外圈、獨立正規化 U、单對識別就可接中心、分開 witnesses 可接合四項候選均有反控制。

正式資料為 [完整壓縮證書](../audits/2026-10-12-w5-marked-relation-e299ae98/controls/certificate.json.gz)
與 [摘要](../audits/2026-10-12-w5-marked-relation-e299ae98/controls/summary.json)。
原 [verification](../audits/2026-10-12-w5-marked-relation-e299ae98/verification.json)
保存隔離階段正常／seed17、六種破損證書、拒絕覆寫及 hash 核對；發布時另記錄驗證，
不改原 manifest 或原「未採納」歷史語境。

```bash
python3 -B audits/2026-10-12-w5-marked-relation-e299ae98/controls/check_w5.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-12-w5-marked-relation-e299ae98/controls/check_w5.py --check --seed 17
python3 -B audits/2026-10-12-w5-marked-relation-e299ae98/review/independent_check.py --primary audits/2026-10-12-w5-marked-relation-e299ae98/controls/certificate.json.gz
```

本包完整 bytes 直接納入 Git，重播只需 Python 標準函式庫。
普遍結論來自上述紙面證明；有限控制標為 `triggered and holds`，真正最小目錄外
933／941 來源為 `not triggered`。沒有新增 Lean theorem 或重跑上游外部計數證書。
