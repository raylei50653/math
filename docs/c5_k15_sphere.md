---
docgraph:
  id: c5.k15-sphere
  family: [c5, c5.minimal-source]
  requires: [c5.cofacial-normal-form, c5.saturation-degree-bound]
  derives_from: [c5.k14-sphere]
  related: [c5.no4ct-handoff]
  verified_by:
    - audits/2026-10-13-k15-sphere-6cafdfb/REPORT.md
    - audits/2026-10-13-k15-sphere-6cafdfb/PROOF.md
    - audits/2026-10-13-k15-sphere-6cafdfb/certificate.json.gz
    - audits/2026-10-13-k15-sphere-6cafdfb/independent/compare.py
    - audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md
---

# 十五內點完整關係界

2026-10-13 整理補註：[無四色定理前提交接](tasks/c5_no4ct_handoff.md)另接
零內點 cap 下降、受限 `s<k` C4 代表與直接球面覆蓋，得到同一 `K≤15=K≤5`。
[替代度數與球面依賴](../audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md)
保留 932／933／941 三支、外部 Corollary 20 及 plantri 信任；不提高有界大小。
下文保留原 K15 證明鏈；無界三支、K∞ 及新論證 Lean 化仍 OPEN。

2026-10-13。固定 BASE `6cafdfb`；本頁是 K15-SPHERE 的權威入口。
完整前提、紙面覆蓋、全部原圖／fibres及獨立審閱見
[隔離報告](../audits/2026-10-13-k15-sphere-6cafdfb/REPORT.md)。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)維護。

## 1. 兩條證明鏈與共同有限證據

本頁是 K≤15 的權威入口；原鏈的完整覆蓋證明見
[PROOF](../audits/2026-10-13-k15-sphere-6cafdfb/PROOF.md)，替代鏈的前提重綁
由[無四色定理前提交接](tasks/c5_no4ct_handoff.md)導向各隔離權威報告。

| 鏈 | 閱讀順序與實際使用的前提 |
|---|---|
| 原證明鏈 | [共面正規形／K≤12](c5_cofacial_normal_form.md) → [度數界](c5_saturation_degree_bound.md) → [K13](c5_k13_collar.md) → [K14](c5_k14_sphere.md) → 本頁。保留普遍 screen／4CT；K13 的外圈與 C₈ 分支前置見其 §0。K14 使最小來源恰 k=15，正規形與度數界使外加 cone 成二十一點最小度五球面圖。 |
| 不以 4CT 為前提的替代鏈 | [零內點 cap 下降與三支正規形／K≤12](../audits/2026-10-13-c5-no4ct-dependency-6cafdfb/REPORT.md) → [受限 C4／度數與球面接入](../audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md)。全域最小來源保留 932／933／941；受限 C4 必須 `s<k`。直接覆蓋 k=13、14、15 的全部球面 roots，不以原 K13→K14 的逐階證明或外圈／C₈ 排除作前提。 |

兩鏈都使用同一固定有序原框的完整十列關係、所有五度 root 與逐列完整 fibres；
空 fibre 也須保存。球面域及逐圖關係核對是排除證據，`not triggered` 不是排除理由。
兩鏈仍保留 Dvořák–Lidický Corollary 20 的外部計算證明及 plantri 生成
完備性定理／C 實作；雙路生成一致不取代完備性定理，既有 Lean 回歸不認證
這套紙面化約。替代鏈的 collar／C₈ 後續需另走交接中的報告，保持相對
loopless 平面圖可染性的 `N≤k+5`；球面接入本身不需要該前提。

DocGraph 的 `requires`／`derives_from` 記原鏈的前置與推導，沒有編碼兩個
證明分支的 AND／OR；`related` 導向替代鏈，`verified_by` 只是工具不驗證
內容的證據路徑標籤。本輪核對文件與既有證據連結，未重跑枚舉或研究證書。
一般 932／933／941 排除及 `K∞=K≤5` 仍 **OPEN**。

## 2. 原證明鏈的十五內點界

對有限簡單 disk 圖、固定有序原 C5 外框與完整十列關係，

\[
\boxed{K_{\le15}=K_{\le5}=K132.}
\]

反設至多十五內點的目錄外來源存在，先全域最小化內點数、再最大化邊數。
[K14](c5_k14_sphere.md)及既有正規形／度數界使其恰十五內點、原框度數至少四、
內部至少五、內面三角化。外加只接原框的 cone 點，得到二十一點最小度五
球面三角剖分；列出全部這類球面圖並刪每個五度 root，覆蓋所有來源。

plantri 的 min5 及 min4加輸出端過濾兩路各得192份嵌入類，完整集合一致。
全部2,714份根圖、27,140列、624,617份完整染色由固定次序搜尋與獨立
domain propagation逐字比對，**完整Σ全部1023**，完成此有界排除。
原邊、rotation、指定外面、十個D5框及完整lifts均保存，生成沒有外圈剪枝。

```bash
python3 -B audits/2026-10-13-k15-sphere-6cafdfb/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-k15-sphere-6cafdfb/check.py --check
python3 -B audits/2026-10-13-k15-sphere-6cafdfb/independent/compare.py
python3 -B audits/2026-10-13-k15-sphere-6cafdfb/independent/negative.py
```

兩路完整生成、normal／seed17、負控制及完整命令見隔離報告。
此為紙面完備化約＋有限完整證書，保留plantri生成定理／實作及上游外部
依賴；沒有新增Lean theorem。真正933／941來源未觸發，排除依據是完備
覆蓋與完整Σ驗證。一般來源至少十六內點；`K≤16=K≤5`、933／941任意大小
排除及`K∞=K≤5`仍 **OPEN**。
