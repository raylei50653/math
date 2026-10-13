# 十四內點完整關係界與 C₈ 分支加強

2026-10-13。本頁為 K14-SPHERE 的權威入口；BASE、完整論證、原圖與全部
fibres、外部生成依賴及獨立覆核見
[隔離報告](../audits/2026-10-13-k14-sphere-acd2b1b/REPORT.md)。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)維護。

## 1. 一般十四內點界

對有限簡單 disk 圖、固定有序原 C₅ 外框及完整十列延伸關係，

\[
\boxed{K_{\le14}=K_{\le5}=K132.}
\]

反設有至多十四內點的目錄外來源，在全部目錄外來源先最小化內點數、再
最大化邊數。[K13](c5_k13_collar.md)使其恰有十四內點；
[正規形](c5_cofacial_normal_form.md)及[度數界](c5_saturation_degree_bound.md)
使其內面全三角化，原框 degree≥4、內部 degree≥5。
外加一個只接原框的 cone 點，得到二十點最小度五球面三角剖分。
完整生成所有球面圖，再刪**每一個**五度 root，必覆蓋所有可能來源。

plantri 5.8 的 min5 及 min4＋output-only filter 兩路各得73份嵌入類，
逐嵌入相等。其1,001份根圖、10,010列、180,228份完整染色由固定次序搜尋
及獨立 domain propagation 逐字一致，**全部 Σ=1023**，完成排除。
生成不作 collar／h／mask 剪枝，完整保留原邊、rotation、指定外面及D₅搬運。

這是紙面完備化約＋有限完整證書；plantri 完備性與實作、既有正規形的
外部依賴明列於隔離報告，未新增 Lean theorem。
真正933／941來源 `not triggered`；排除理由是完整覆蓋，不是零觸發本身。

## 2. C₈ 的獨立紙面加強

在既有八個 h=3 契約下，原 C₈ 無內弦，內側 H 的全部邊界 degree≥4，
嚴格內點 degree≥5。令 Q 為嚴格內點的原 induced 圖。
曲率、原三角面 incidence 配對、Q 無葉點，以及 outerplane 必有至少兩個
degree≤2 點，排除嚴格內點恰六、七的全部情形，故

\[
\boxed{h=3\Longrightarrow k\ge16.}
\]

完整證明見 [C₈ 紙面論證](../audits/2026-10-13-k14-sphere-acd2b1b/independent/C8_PROOF.md)。
此結果不依球面生成，球面核對亦不以它剪枝。原八項無界殘留仍保留。

## 3. 重播與未解範圍

```bash
python3 -B audits/2026-10-13-k14-sphere-acd2b1b/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-k14-sphere-acd2b1b/check.py --check
python3 -B audits/2026-10-13-k14-sphere-acd2b1b/independent/compare.py
python3 -B audits/2026-10-13-k14-sphere-acd2b1b/independent/negative.py
```

兩路生成重播、seed17獨立核對及實際空fibre小控制另見隔離報告。
一般目錄外來源至少十五內點；全域最小／最大邊數正規形若恰十五內點，必 h≥4。
`K≤15=K≤5`、一般`K∞=K≤5`及933／941任意大小來源仍 **OPEN**。
共同 h≥3、n₅≥9不提高，沒有新Lean定理。
