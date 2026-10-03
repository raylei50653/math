# ε=2：唯一 degree-6 root 的 t=2 全部分拆排除

2026-10-03，接手基準 `1d32997`。接續
[t=1 全分拆排除](c5_excess_two_single_spoke_complete.md)，復用其原支援、
完整關係及 active 結構工具。研究入口見 [Kempe 導覽](c5_kempe_guide.md)，
本輪實際驗證與跨對話摘要見
[研究紀錄](history/2026-10-03-excess-two-two-spoke-complete.md)。

**在 933／941 固定完整 Σ、edge-minimal induced-C₅ disk 來源、ε=2、
唯一完整 degree-6 root 的前提下，t=2 的五種原接點分拆全部不可能。**
本輪完成整型來源排除；既有「省略全收／無全 degree-4 真子核心」是
前序證據，沒有用它直接替代整型反證。證據為任意大小紙面論證與
Python 固定必要域證書，未新增 Lean theorem。

## 1. 同一原來源與完整接合

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框。
Σ(G) 為 933、941 或整圖 D₅ 像，故接受全部 T4。每條非框邊 e
均有 Σ(G−e)⊋Σ(G)。有效內部 H 連通，r 完整 degree 六，其餘
有效內點完整 degree 四。兩條不同原 spokes 是 rb_s、rb_t。

H−r 的原連通分量 Cᵢ 有具名有序接點 Pᵢ=N(r)∩Cᵢ，且
Σᵢ|Pᵢ|=4。原分量、原邊、實際 attachments、support、ownership、
環序與嵌入固定，全部關係共用同一字面四色框。對 proper boundary
coloring b，令 Rᵢ(b) 為原 Cᵢ 全部合法染色產生的有序接點 relation。
接點 slack 保證 Rᵢ(b) 非空，原圖完整接合恰為

\[
J_b=\{(a,t_1,\ldots,t_m):t_i\in R_i(b),\quad
 a\notin\{b_s,b_t\}\cup\bigcup_i\operatorname{set}(t_i)\}.
\]

令 Fᵢ(b)=∩_{u∈Rᵢ(b)}set(u)。固定本題的 root 查詢時，精確投影為

\[
\operatorname{proj}_r J_b
 =U_4\setminus\bigl(\{b_s,b_t\}\cup\bigcup_iF_i(b)\bigr). \tag{1}
\]

Fᵢ 只描述式 (1) 的特殊共同避色查詢，沒有取代完整 Rᵢ、拆成接點
marginals，或把各分量独立正規化。兩條 spoke 的字面顏色可相同；
checker 保留這個情形，不先假設它們在每列各貢獻一個不同禁色。

## 2. 復用 t=1 的固定支援與共同結構

以下工具的局部前提是 r **至少有一條**原 spoke，沒有要求它恰有
一條。因此原分量與原附件不變時，可用於本題：

| t=1 工具 | 本題使用方式 |
| --- | --- |
| [通用短支援引理](c5_short_support_singleton.md) | 每份原分量有 Σ-minimality 私有禁色見證；完整來源碰齊五框點，提供避開該分量的原外路徑，故固定 support 跨度至少二 |
| [三接點兩禁色 K₅](c5_excess_two_ternary_two_unary.md#2-三接點在所有列都至多禁一色) | 任一 proper row 的 ternary 禁色容量至多一；用於 (3,1)，不需要 D 身份篩選 |
| [原 binary 跨列路徑](c5_excess_two_ternary_binary.md#4-同一原-binary-路徑塊的跨列支援) | 每份 binary 的 pair rows 共用同一原奇數 bridge 路徑、全部原旁支袋與同一支援族 |
| [首橋相容性](c5_single_spoke_first_bridge.md#3-首橋的共用-β-與局部穩定子) | singleton row 的兩個首橋袋共用同一條原 bridge 的 β；局部 residual 是 {c,β}，不能改用整份 singleton 禁色 {c} |
| [四接點共同 active forest](c5_excess_two_four_one.md#3-全部拒絕列共用同一原-active-forest) | 連通雙 triangle 型由任一原 spoke 及原 tethers 給 K₅；兩條原 bridge paths 型保留兩份固定末端袋及全部實際支援 |

紙面 degree-list tightness 與 block palettes 的外部依賴，沿用
[Dvořák 講義的 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
本輪重讀原文確認前提是連通圖、degree assignment 及不可著色，
並不要求整張 G 是逐列 minimal obstruction。

短支援引理與共同 root 的相容 lifts 給

\[
\ell_i\ge2,\qquad\sum_i\ell_i\le5. \tag{2}
\]

各份私有禁色見證可以來自不同列；相加的是同一原圖的固定支援
跨度，沒有相加不同列的染色負載。式 (2) 立即排除三份以上原分量。

兩條原 spokes 再將 disk 分成兩個原扇區。每份連通 Cᵢ 的全部
接點與支援落在同一扇區；沿一條原 spoke 切開時，它的最小支援
包絡不能跨過另一條 spoke。包絡端點是真實附件，內部位置僅為
容許範圍。這是 t=2 的新增幾何資訊，不能只把 t=1 的 spoke 色
多扣一次而沿用全部舊位置。

## 3. 五種分拆的整型覆蓋

四個原接點的整數分拆只有下列五種，具名原分量身份始終保留：

| 原接點分拆 | 整型排除依據 |
| --- | --- |
| (4) | [共同 active forest 與末端袋](c5_excess_two_two_spoke_four.md)：相同 spoke 色的拒絕列需三禁色，違反四接點 K₅ 引理；其餘列的 pair 迫同一兩末端袋，全部共同扇區支援不能並排 |
| (3,1) | [Ternary／unary 同框 profiles](c5_excess_two_two_spoke_ternary.md)：兩份禁色容量均至多一，16 份具名扇區配置的 107,296 份十列共同 profiles 全無目標 |
| (2,2) | [兩原 binary 與首橋](c5_excess_two_two_spoke_binary.md)：兩份原路徑的跨列支援先保留 20 份抽象必要查詢；補入同一首橋的共用 β 與局部 residual 後全部排除 |
| (2,1,1) | 式 (2) 的三分量六跨度直接排除；前序 [binary 省略證書](c5_excess_two_binary_two_unary.md) 與 [兩 unary 省略證書](c5_excess_two_two_unary.md) 保留其原證據層 |
| (1,1,1,1) | 式 (2) 的四分量八跨度直接排除；另有既有 [四 unary 固定支援排除](c5_excess_two_four_unary.md) 的獨立證書 |

(2,2) 的 20 份初層存活資料完整保存為較弱 screen 的控制，並非
disk 來源見證。singleton／pair 比較只在既有 palettes 的固定色
條件成立時使用首橋引理；不同 singleton 列的 β 沒有強迫相同。
(4) 的四接點 pair 亦沒有冒充 binary；兩份固定末端袋來自原
四葉 active forest，並保留各只有一個原 contact 的條件。

## 4. 合成結論與保留界線

由 §3 得到

\[
\boxed{\Sigma(G)\in\operatorname{Orb}_{D_5}\{933,941\},\quad
 \varepsilon(G)=2,\quad R=\{r\},\quad\deg_G(r)=6
 \quad\Longrightarrow\quad t\ne2.}
\]

連同前序 t=1 排除，現在同一來源前提下 **t∉{1,2}**。
這不將共同下界從 ε≥2 提高到 ε≥3；其他 t、兩個 degree-5 roots
（含 mixed）、一般來源、一般單側／共同出口及 K∞=K≤5 仍保留。

各份任意大小／topology 論證由原 Gallai 結構、原 tethers 與
crosscut 前提承擔；Python 只核對明列的有限必要域、具名 minor
控制及完整 ordered-tuple 接合。`lake build` 驗證既有 Lean 專案，
未形式化本輪新排除。下一窄問題由 Kempe 導覽維護。

## 5. 重播入口

```bash
python3 scripts/c5_excess_two_two_spoke_four.py --check
python3 scripts/c5_excess_two_two_spoke_ternary.py --check
python3 scripts/c5_excess_two_two_spoke_binary.py --check
python3 scripts/c5_short_support_singleton.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_residual_locality.py --check
python3 scripts/c5_single_spoke_cross_row.py --check
python3 scripts/c5_single_spoke_two_arc.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
lake build
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

三份新增 checker 另以 `PYTHONHASHSEED=17` 重播。實際完成命令、
沿用但未重跑的依賴、文件與產物驗證見本輪研究紀錄。後續整理、
發布重播與提交範圍見 [發布紀錄](history/2026-10-03-excess-two-two-spoke-publish.md)；
目前 Git 狀態不由歷史文件代替。
