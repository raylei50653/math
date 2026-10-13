---
docgraph:
  id: c5.k13-collar
  family: [c5, c5.minimal-source]
  requires: [c5.saturation-degree-bound, c5.neartri-boundary-collar]
  derives_from: [c5.cofacial-normal-form]
  related: [c5.no4ct-handoff]
  verified_by:
    - audits/2026-10-13-k13-collar-50d5474/REPORT.md
    - audits/2026-10-13-k13-collar-50d5474/PROOF.md
    - audits/2026-10-13-k13-collar-50d5474/generation/COMPLETENESS.md
    - audits/2026-10-13-k13-collar-50d5474/independent/compare_main.json
---

# 十三內點完整外圈排除與 K≤13 界

2026-10-13 最新後續：[K15-SPHERE](c5_k15_sphere.md)證 `K≤15=K≤5`，一般來源至少十六內點；
[C8原接點／剝層定理](c5_c8_peeling.md)另證 `h=3 ⇒ k≥19`；八項無界來源仍 OPEN。
八項無界殘留與一般主命題仍OPEN；下文及舊證書保存各原輪次語境。


2026-10-13 最新後續：[K14-SPHERE](c5_k14_sphere.md) 已證 `K≤14=K≤5`，
一般目錄外來源至少十五內點；同份新紙面證明給 `h=3 ⇒ k≥16`。
下文先前界線與證書保留當輪語境，h≥3、n₅≥9不提高。


2026-10-13。固定 BASE `50d5474f2446403f3b3001d5943571184c8c9936`。
本頁是 K13-COLLAR 的權威入口；完整證明、輸入 hashes、所有具名配置、
來源原邊／rotation／有向面、全部 fibres 與重播見
[隔離報告](../audits/2026-10-13-k13-collar-50d5474/REPORT.md)。
目前研究停止點由 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口) 維護。

## 0. 原證明與替代接入

本頁是十三內點界的權威入口；原鏈先讀
[共面正規形／K≤12](c5_cofacial_normal_form.md)及
[度數界](c5_saturation_degree_bound.md)，再讀
[完整外圈](c5_neartri_boundary_collar.md)與
[C₈ apex 度數](c5_c8_apex_degree.md)以得到下文 h=4–7 的四分支。
這組上游報告保留普遍 exterior screen／4CT、K132 witnesses 與外部
Dvořák–Lidický Corollary 20 的依賴；原 K13 完整論證及有限證據由隔離報告負責。

另一條入口是[無四色定理前提交接](tasks/c5_no4ct_handoff.md)：先用
[零內點 cap 下降](../audits/2026-10-13-c5-no4ct-dependency-6cafdfb/REPORT.md)
建立全域最小 932／933／941 三支及 K≤12，再用
[替代度數與直接球面覆蓋](../audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md#5-接入-k13k15直接使用所有球面根點)
重用本域的所有十九點球面圖與全部五度 roots。此接入不使用 h≥3、外圈排除
或 C₈ 前提；受限 C4 代表仍須 `s<k`，plantri 生成定理／C 實作與
Corollary 20 的外部計算信任仍保留。

DocGraph 的 `requires`／`derives_from` 記原鏈中的前置與推導，沒有編碼兩個
證明分支的 AND／OR；未補 metadata 的 C₈ 前置由上述直接連結記錄。
`related` 只導向替代鏈，`verified_by` 是證據路徑標籤，工具不驗證其內容。
本輪只核對文件依賴與證據入口，未重跑枚舉、染色證書或外部計算。
一般 932／933／941 排除及 `K∞=K≤5` 仍 **OPEN**。

## 1. 結論與來源選擇

對固定有序 C₅ 外框的有限簡單 disk 圖，完整十列關係滿足

\[
\boxed{K_{\le13}=K_{\le5}=K132.}
\]

因而一般目錄外來源至少十四內點。一般 `K∞=K≤5` 及 `K≤14=K≤5`
仍 **OPEN**；本結果不提高共同 `h≥3` 或 `n₅≥9`，沒有新增 Lean theorem。

反設至多十三內點的目錄外來源存在，在**全部目錄外來源**中先最小化內點數，
再最大化邊數。既有 [十二內點界與正規形](c5_cofacial_normal_form.md)
給 k=13、簡單二連通、chordless 原 C₅ 及全內面三角化；
[度數界](c5_saturation_degree_bound.md) 給原框 degree≥4、原內點 degree≥5。
Euler 重新推出
`n₅=6+h+Σ_{內部 d≥7}(d−6)`，故 h≤7。
[完整外圈](c5_neartri_boundary_collar.md) 排 h≤2，
[C₈ apex 定理](c5_c8_apex_degree.md) 排 k=13 時的 h=3。
所以恰只剩下列四分支，沒有加入 N2 或 edge-critical 前提。

## 2. 全覆蓋與完整關係

| h | 原內圈／嚴格內點 | 具名超額配置 | 完整有限域中的根點刪除圖 | 排除證據 |
|---:|---|---:|---:|---|
| 4 | C₉／4 | 70 | 41：39 無弦、2 有一弦 | 全部 Σ=1023∈K132 |
| 5 | C₁₀／3 | 126 | 4：全有兩弦 | 全部 Σ=1023∈K132；無弦子域另有紙面矛盾 |
| 6 | C₁₁／2 | 210 | 0 | 紙面葉區域度數矛盾；完整分類獨立吻合 |
| 7 | C₁₂／1 | 330 | 0 | 空側弦／單輪紙面矛盾；完整分類獨立吻合 |

表中圖數保留不同根點，可能同構，不是互異未標號圖數。
每份超額 e 決定五個原框邊 apices 與各框點的有序 y 鏈；全部 736 份具名配置
及其整圖 D₅ 映射，包括無候選的空列，均保存。
沒有假設 C₉–C₁₂ 無內弦，也沒有提高它們的 apex H-degree 下界。

完備性由[紙面證明](../audits/2026-10-13-k13-collar-50d5474/PROOF.md)承擔：
在 G 外面加 z 連到原 B，得到十九點最小度五球面三角剖分；完整枚舉它們後，
刪每一個五度根點並保留十種 B 次序，必覆蓋所有原來源。
plantri 5.8 的兩個不同生成入口在十九點產生相同的 23 份嵌入類。
另一條內側覆蓋由 C 外加 cone 得十四點最小度四球面三角剖分，完整枚舉
2,472 份嵌入，再列出全部合法五 apex 選位，所得 h=4、5 類與主路徑相同。

主路徑不作 collar／cap／mask 剪枝，共計算 306 份根點刪除圖、3,060 列。
全部完整關係都是 1023；41,021 份完整 lifts 由固定順序回溯與獨立
domain propagation 搜尋逐份一致。實際 933／941 來源為 `not triggered`；
排除依據是完備來源覆蓋接精確關係驗證，不是零觸發本身。

## 3. 重播與信任邊界

```bash
python3 -B audits/2026-10-13-k13-collar-50d5474/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-k13-collar-50d5474/check.py --check
python3 -B audits/2026-10-13-k13-collar-50d5474/independent/compare_main.py --check
```

完整生成、獨立覆蓋、負控制、儲存與文件檢查命令見隔離報告。
外部依賴明列為既有正規形／K132／4CT／十二內點界，以及 plantri 的
已發表生成完備性定理與 C 實作；本輪實際重播生成和全部染色證書。
沒有重播 Dvořák–Lidický 的外部計算證书，也未把其「少於三十」擴為三十。
`lake build` 只記作既有 Lean 回歸。原隔離研究的「未 commit／push」保留當時語境；
本次主線整合、逐檔保存與重播範圍見[發布紀錄](history/2026-10-13-k13-rank3-publish.md)。
