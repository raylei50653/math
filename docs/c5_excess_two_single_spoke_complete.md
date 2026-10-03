# ε=2：唯一 degree-6 root 的 t=1 全部分拆排除

**發布整理（2026-10-03）**：本報告與前序省略證書已納入
[本批發布紀錄](history/2026-10-03-excess-progress-publish.md)。下文的未提交
描述保留研究當輪語境；即時提交與遠端狀態以 Git 為準。

2026-10-03，接手基準 `bbd900a`。接續 [原 binary 省略](c5_excess_two_single_spoke_binary.md)
與 [兩原 unary 省略](c5_excess_two_single_spoke_two_unary.md)。目前研究入口見
[Kempe 導覽](c5_kempe_guide.md)，實際驗證見 [本輪紀錄](history/2026-10-03-excess-two-single-spoke-complete.md)。

**在 933／941 固定完整 Σ、edge-minimal C₅ disk 來源、ε=2、唯一
完整 degree-6 root 的前提下，t=1 的七種原接點分拆全部不可能。**
這次排除整型來源；既有「無全 degree-4 真子核心」只是前序結果。
證據為任意大小紙面論證與 Python 固定必要域證書，未新增 Lean theorem。

## 1. 範圍與同一原來源

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框。
完整 Σ 為 933、941 或整圖 D₅ 像，故接受全部 T4。每條非框邊 e
滿足 Σ(G−e)⊋Σ(G)。有效內部 H 連通，r 完整 degree 六，其餘
內點完整 degree 四；r 的唯一原 spoke 為 rb_s。

H−r 的原連通分量 Cᵢ 具有具名有序接點 Pᵢ=N(r)∩Cᵢ，
Σᵢ|Pᵢ|=5。保留每份原分量、全部附件、支援、ownership、環序、
原邊與同一字面色框。對同一 proper boundary coloring b，完整
有序 relation Rᵢ(b) 由原 Cᵢ 的全部合法染色產生；接點 slack
保證 Rᵢ 非空。原來源的完整接合為

\[
\{(a,t_1,\ldots,t_m):t_i\in R_i(b),\quad
 a\ne b_s,\quad a\notin\operatorname{set}(t_i)\text{ 對所有 }i\}.
\]

令 Fᵢ=∩_{t∈Rᵢ}set(t)，上述關係的 root 投影恰為
U₄∖({b_s}∪⋃Fᵢ)。這是固定原 root 查詢的精確投影，沒有以
marginals 替換多接點 relation，也沒有獨立正規化各原分量。

## 2. 固定原支援的共同下界

[兩／三外部 hubs 的短支援引理](c5_short_support_singleton.md)
給出本輪共同幾何工具。若原 C 的實際支援包含於一條框邊的兩端
{a,b}，且有避開 C 的原 r–(B∖{a,b}) 路徑，則 F_C 在全部
proper rows 都為空。定理不限 C 的大小或接點數。

在本題來源中，這份外路徑必存在：來源拒絕多個 singleton 列，
[完整支援引理](c5_independent_support_capacity.md#11-degree-與完整支援)
迫 G 碰齊五個框點。取 {a,b} 外的一個實際附件，其內部鄰點是
r 或另一原分量；沿該原分量接回 r 即得路徑。

另一方面，Σ edge-minimality 使每份原 C 至少有一個私有禁色
見證。故它的固定實際支援不能包含於任何單一框邊，包含空支援
與單點支援情形。沿原 spoke 切開 disk，各分量有同序、開框邊段
互斥的最小支援包絡 Iᵢ；包絡端點是真實附件，內部點不新增為附件。
因此

\[
\boxed{\ell_i\ge2,\qquad \sum_i\ell_i\le5.} \tag{1}
\]

不同原分量可以使用不同私有色見證；式 (1) 相加的是同一原圖
固定支援的幾何量，沒有相加不同列或不同核心的染色負載。
特別地，**三份或更多原分量都不可能**。

## 3. 七種分拆的完整覆蓋

五個原接點的整數分拆只有下列七種；相同容量的分量仍保持原身份。

| 原接點分拆 | 整型排除依據 |
| --- | --- |
| (5) | [共同五葉 active tree](c5_excess_two_five_contact.md)：原 spoke 私有色見證迫三個禁色；只剩一個正 C₅ 或三個正 triangles，原 tethers 均給 K₅ |
| (4,1) | [四接點與 unary](c5_excess_two_four_one.md)：兩弧跨度至少二；保留同一四接點 active forest、原末端區塊及跨列完整接合，必要域全空 |
| (3,2) | [Ternary／binary](c5_excess_two_ternary_binary.md)：三接點禁色容量至多一及跨列 D 身份守恆；同一原 binary 路徑塊與兩框弧 K₅ 關閉全部 100 個查詢 |
| (3,1,1) | 三份原分量由式 (1) 需至少六段；另有 [168 份支援／146,496 份同源 profiles](c5_excess_two_ternary_two_unary.md) 的獨立空域證書 |
| (2,2,1) | 三份原分量由式 (1) 需至少六段，直接排除整型；不只沿用原 binary 省略全收 |
| (2,1,1,1) | 四份原分量由式 (1) 需至少八段；另有 [同源 2,200 profiles](c5_excess_two_binary_three_unary.md) 的獨立整型排除 |
| (1,1,1,1,1) | 五份原分量由式 (1) 需至少十段；另有 [四因子子覆蓋與 bridge root](c5_excess_two_five_unary.md) 的獨立證明，較強地只用 T4／degree 即得 Σ=Ω |

(3,2) 的 binary 路徑定理沒有套到 (4,1) 的四接點分量。後者保留
四個原接點及共同 active forest：連通的兩個 triangles（包括共用
cut vertex）由原 tethers 給 K₅；兩條不同原 bridge 路徑則抽出兩份
固定、互不相交、各只有一個原接點的末端區塊。它們在全部指定拒絕
列的完整 rooted residual、實際支援與同一 spoke 切口一起比較。
各證書的有限必要域涵蓋由對應紙面引理承擔，不是來源圖枚舉。

## 4. 結論、證據層與停止點

由 §3 的完整分拆表，得到

\[
\boxed{\Sigma(G)\in\operatorname{Orb}_{D_5}\{933,941\},\quad
\varepsilon(G)=2,\quad R=\{r\},\ \deg_G(r)=6
\quad\Longrightarrow\quad t\ne1.}
\]

這是指定來源前提下的任意大小紙面排除，加上可重播 Python 固定域
證書。外部 degree-list／Gallai 定理及前序 topology 是明列依賴；
`lake build` 只驗證既有 Lean 專案，未形式化這些新 minor 或跨度論證。

式 (1) 亦直接給出同前提下 t=2、(2,1,1) 的三分量六跨度排除；
這是共同引理的紙面推論，未另外枚舉。共同下界仍為 ε≥2；其他 t
的完整分類、兩個 degree-5 roots（含 mixed）、一般來源排除、一般
出口與 K∞=K≤5 均不由本輪合成定理完成。此處停止於全部 t=1 整型排除，下一入口由導覽維護。
沒有作 commit／push，也未改寫接手時既有未提交研究。

## 5. 重播入口

```bash
python3 scripts/c5_short_support_singleton.py --check
python3 scripts/c5_excess_two_five_contact.py --check
python3 scripts/c5_excess_two_four_one.py --check
python3 scripts/c5_excess_two_ternary_binary.py --check
python3 scripts/c5_excess_two_ternary_two_unary.py --check
python3 scripts/c5_excess_two_binary_three_unary.py --check
python3 scripts/c5_excess_two_five_unary.py --check
lake build
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

各新增 checker 另以 `PYTHONHASHSEED=17` 重播；實際結果及本輪未重驗
的歷史依賴見 [研究紀錄](history/2026-10-03-excess-two-single-spoke-complete.md)。
