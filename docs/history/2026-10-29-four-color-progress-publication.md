# 四色消元、有限域分解與六邊割進展整理發布

2026-10-29。從基準 `aec89209e1f889f7ddaefe35fbdfd0b97691e9ee` 整理相連程式、
完整實驗紀錄、來源快照、紙證及 Lean 核心。當前入口為
[4CT導覽](../research/4ct_guide.md)、[求解工具導覽](../tools/four_color_guide.md)及[Lean導覽](../verification/lean_guide.md)。
本頁保存本輪發布範圍與驗證；commit、push及遠端CI以即時Git／GitHub核對為準。

## 成果與證據範圍

| 工作 | 本批成果 | 停止點與限制 |
| --- | --- | --- |
| 分區與增量傳播 | [分區](../tools/solver/four_color_partition.md)、[動態訊息分區](../tools/solver/four_color_information_partition.md)、[delta](../tools/solver/four_color_delta_propagation.md)與[支援流失](../tools/solver/four_color_support_loss.md)接入可選模式，保留完整有序接口、全部fibres及共同回寫；完整支援流失等價式有普通Lean。 | 固定40例有改善也有退步／超限；保留原預設，沒有一般加速保證。 |
| 全解表示及方案分析 | [部分歷史](../tools/solver/four_color_partial_history.md)以精確前綴、剩餘問題及可重算fibres表示全部解；[圈區訊息](../tools/solver/four_color_region_messages.md)、[數學優化候選](../tools/solver/four_color_mathematical_optimization.md)及[方案比較](../tools/solver/four_color_method_comparison.md)保留來源、反控制與完整紀錄。 | 原型與主引擎的整合範圍各自明列；查詢／傳播／建構checks不可混比，歷史牆鐘不當一般成本界。 |
| 有限域精確分解 | [有限色域報告](../tools/solver/four_color_bounded_projection.md)：至多q因子空交證書、anchor與完整fibre有普通Lean；獨立Python原型逐份核原解、剩餘投影及原子中斷。 | 未形式化Python精化；十葉首步省列但六葉整次可超限，沒有一般效率、固定寬度或4CT結論。 |
| 平面六邊割來源 | [hub輪圈與六割排除](../archive/reports/planar-sources/four_color_six_cut_exclusion.md)：在裸平面全體頂點最小反例的前提下，非平凡邊割至少七；同份原側換色與兩端點例外有紙證，另有有限Python控制。 | 一般拓撲論證未Lean化；七邊全族來源、932與完整4CT仍OPEN。 |

主攻方向已在[精確消元研究契約](../research/4ct_guide.md#精確消元主線的研究契約)採納：
從原平面嵌入與實際接點出發，尋找跨指定消元規則保留的結構不變量。
本次整理未新增這項不變量或封閉定理；舊D／單split無增益停止裁決保留。
完整關係保解不自行提供平面共同非空性，其他C₅來源分支的OPEN邊界不變。

## 原證據與來源保管

保留早期／最終實驗、完整逐例紀錄、失敗與超限，不覆寫原始收據。
歷史文件hash、「未提交」文字及當時檢查失敗保留當輪語境。
尤其六割的原verification曾記錄當時尚未補齊的其他文件錯誤；本次正式文件檢查另存。

[來源保管程式](2026-10-29-four-color-progress-publication/custody.py)與
[核對收據](2026-10-29-four-color-progress-publication/custody.json)
核對來源快照、原始輸入與壓縮紀錄的hash。
32份超過1 MB的相連JSON以精確路徑、大小及SHA256登記為凍結證據，
不將目前持續演進的程式冒充歷史生成器。
兩份帶行號的凍結程式摘錄在原空白行保留分隔空格；`.gitattributes`只對這兩個確切路徑
豁免行尾空白檢查，原始bytes及來源hash保持不變。

## 本次發布驗證

- [工具測試](2026-10-29-four-color-progress-publication/tool-tests.log)：504項通過，使用requirements鎖定的Python依賴。
- [Lean建置](2026-10-29-four-color-progress-publication/lean-build.log)：8,834 jobs通過；既有linter warnings保留。
- [有限域公理](2026-10-29-four-color-progress-publication/axioms.log)及
  [支援流失公理](2026-10-29-four-color-progress-publication/interface-axioms.log)：
  最多依賴 `propext`、`Classical.choice`、`Quot.sound`，沒有 `sorryAx` 或新增公理。
- 有限域分解、六割控制、部分歷史各自正常與 `PYTHONHASHSEED=17` 重播，
  同一來源的兩次輸出逐byte相等；有限域與六割另與原報告逐byte相等。
  部分歷史的所有結果與原summary相等，僅 `four_color_lab.py` 的來源hash因後續CLI演進不同；
  舊hash精確對上[已提交的原來源快照](../../audits/2026-10-26-four-color-local-messages-f30cd6f/source/four_color_lab.py)，
  原summary不改寫，目前來源hash保存在新重播中。
- [圈區驗證](2026-10-29-four-color-progress-publication/region-verify.json)：
  重核最終紀錄的來源／證據hash、訊息計數、返回見證及預設相容性，與原收據逐byte相等。
  此checker未重跑每份完整reply oracle，該部分沿用原實驗證據。
- 正式文件、docs-only DocGraph、實際Git index產物政策與空白檢查見
  [發布檢查收據](2026-10-29-four-color-progress-publication/checks.json)。
  全工作樹DocGraph仍有72項保留快照／scratch的duplicate-id錯誤；不改稱全域通過。

本次沒有重跑全部測速、擴大構形枚舉或重新證明既有C₅分類。
各份歷史效能數字仍屬其當時來源與預算；本次重播不新增一般速度保證。

## 文件傳遞與接續

L0程式、專題來源與證據及L1求解／Lean導覽、STATUS已核對；
六割來源結論的直接父題與consumers已更新，其他C₅／W7／J1／J2來源義務保持原停止點。
README與HANDOFF反映已採納的消元研究方向；詳細下一步只由4CT導覽維護。
本輪整理停止於相連證據與既有方向，不新增上層數學closure。
發布後核對本機、tracking與遠端分支SHA及clean狀態；遠端CI另行回報。
