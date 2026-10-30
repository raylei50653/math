# 封存導覽：查舊成果、後續涵蓋與歷史重播

文件整理：2026-10-30；本頁說明封存資料的用途與閱讀方式，不新增研究結論。

## 研究概況與閱讀入口

封存保存各輪如何得到結果、當時尚缺什麼，以及當時實際驗證了什麼。
**封存不等於作廢。** 舊報告中的定理、完整關係、空 fibres、證書與失敗控制仍各有用途；
已由後續成果處理的停止點，應連同後續來源閱讀，不能只按檔案日期判定有效性。

查目前採納結論與 OPEN 先讀[當前結論](../research/CONCLUSIONS.md)，
研究方向與閱讀路徑由[研究總覽](../research_overview.md)及[研究線入口](../HANDOFF.md)進入；
查某份舊報告由[完整索引](../STATUS.md)定位，追溯當輪數字與驗證再讀
[歷史紀錄入口](../STATUS.md#歷史紀錄與舊連結)。
本頁下方整理容易誤讀的更正與後續關係，完整前提與論證沿連入的原報告查閱。
新研究在同輪核對後整合至當前結論，再封存完整研究檔；封存頁不另維護一套現況。

本次目錄遷移的原始 Markdown、路徑對照及使用方式見
[2026-10-30 遷移保存說明](migration-2026-10-30/README.md)。
要核對原 bytes 或解讀舊命令，先讀該說明，再依具名報告的重播契約操作。

## 按目的查閱

| 要做的事 | 閱讀方式 |
| --- | --- |
| 引用舊成果 | 找原報告的前提、命題及證據層，再核對後續連結；作為接續依據時對回當前結論，按需提升或引用。目錄歸檔位置不決定命題效力。 |
| 追查舊停止點 | 由下表或原報告的後續提示進入新來源，分清已涵蓋的子契約與仍 OPEN 的父問題。 |
| 理解當輪決策 | 讀原報告與對應歷史紀錄；有日期的「下一步／未提交／未驗證」保留當時語境。 |
| 重播或核對來源 | 先讀遷移保存說明，再讀原報告及具名 audit 的輸入、版本、hash 與命令；區分當輪重播和本次文件整理。 |

專題報告保存來源論證，`history/` 保存逐輪研究與發布紀錄，`sources/` 保存匯入原稿，
`audits/` 保存具名稽核資料。它們的責任不同；同一事件可能需要沿連結讀數種資料。
目前主攻、進行中標記與第一個工作仍由研究契約及導覽維護，歷史建議表不另作排程。

## 已更正的身份、稱呼與論證

| 舊說法或容易混淆的地方 | 正確讀法與權威來源 |
| --- | --- |
| Bernhart 的「接受 81、D 剩 160」 | 數字對應共對角線為 5–5 的另一張圖；古典 Bernhart 為 6–6，兩圖須保留各自完整附件。見[Bernhart 基準](reports/counting/ck_bernhart_benchmark.md)。原[單 split 無增益](reports/counting/ck_d_lock_comparison.md)停止裁決不變。 |
| Bernhart 76 列計數向量是極射線 | [跨 split 稽核](reports/counting/ck_bernhart_cross_split_audit.md)已證原向量非極端，可拆為兩個 full-lift 極射線；各自的計數投影是否極端尚未證。不能由古典 C 可約性直接推出抽象向量沒有平面來源。 |
| 盾弧證明中「兩面的閉包不交」 | [盾弧引理 1(d)](reports/c5/shared-results/c5_unary_shield_budget.md)已更正為開面論證，互斥結論不變。[q-core 補證](reports/c5/shared-results/c5_qcore_shield_budget.md)另明列不同 pieces、criticality 與 degree 前提；去掉前提的廣義說法有反例。 |

更正只作用於具名錯句、身份或性質，不把同頁其他論證、原完整資料或歷史驗收一併判為失效。
若歷史快照保留更正前的文字，應由此進入更正後來源，保留快照原貌。

## 已被後續涵蓋的停止點

| 舊報告或系列 | 後續涵蓋範圍與閱讀入口 |
| --- | --- |
| Bernhart retained 共同端點缺口 | [端點補證](reports/counting/ck_bernhart_endpoint_ray_continuation.md)補完原未涵蓋情形與完整 RIP；原[retained 報告](reports/counting/ck_bernhart_retained_intersection.md)仍保存首輪範圍和控制。一般來源排除不由此得到。 |
| Bernhart 標記分離與 bond 存在性 | 經[標記分離](reports/counting/ck_bernhart_marked_separation.md)、[bond 報告](reports/counting/ck_bernhart_marked_bond_existence.md)到[通用標記](reports/counting/ck_bernhart_universal_marking.md)，剩餘義務化為無標記六葉的實際來源問題。條件構造未提供符合目標的完整反例，r₂ 仍 OPEN。 |
| 三步 ALT、平面 twin 與 ZV 共同外側 | [不可區分控制](reports/planar-sources/four_color_three_step_relation_control.md)及[共同外側](reports/planar-sources/four_color_three_step_shared_exterior.md)保存原來源和完整關係對照；[共同註記投影](reports/planar-sources/four_color_three_step_annotation_projection.md)完成有限邊界註記公理的無增益停止裁決。拒絕指定註記不等於新增關係刪列。 |
| 三步原圖層的後續限制 | [跨 split 排除](reports/planar-sources/four_color_three_step_cross_split_exclusion.md)處理指定森林／至多單圈來源；[分隔路 fibres](reports/planar-sources/four_color_three_step_separator_fibres.md)與[全割準則](reports/planar-sources/four_color_three_step_remote_cut.md)保留更完整共同限制。[附件裝飾](reports/planar-sources/four_color_three_step_attachment_decoration.md)證鄰點條件單獨無增益。一般多圈 D16 與共同存在性仍 OPEN。 |
| 共鄰端點 P₃ 的三份個別關閉與剩餘 ledger | [原共鄰報告](reports/c5/weak-deletion/c5_mixed_p3_common_endpoint.md)及 C₂／C₃／C₄ 保存個別排除；[C-W／D₆ 補證](reports/c5/shared-results/c5_qcore_shield_budget.md)補零-unary 側，涵蓋原 C §1 的整個共鄰端點來源分支。[cw-v1 ledger](reports/c5/shared-results/c5_open_leaf_ledger.md)保存固定目錄的批次合併，舊 predecessor 不覆寫。 |
| no-mixed 的免表共同分離缺口 | [增長完備性](reports/c5/shared-results/c5_no_mixed_growth_completion.md)結合[無增長引理](reports/c5/shared-results/c5_no_mixed_no_growth.md)，完成指定兩列的存在性分離。[跨度](reports/c5/weak-deletion/c5_no_mixed_span_budget.md)、[假設驗證](reports/c5/weak-deletion/c5_no_mixed_hypothesis_audit.md)及[局部篩選](reports/c5/weak-deletion/c5_no_mixed_local_screen.md)仍承擔各自引理與有限證據；逐染色 repair、完整 Σ 與一般出口仍未證。 |
| 舊 C₅ synthesis 的建議順序與未完成清單 | [跨線綜合](reports/c5/shared-results/c5_research_synthesis.md)已在原位置保留多輪後續：H1、共鄰 P₃ 與 W 等有指定範圍完成；H2、H3 及一般推廣仍未證。其精確猜想與跨線關係仍可引用，當輪優先表須按日期閱讀。 |

mixed P₃ 的對稱、非對稱及中點／端點報告證明互補的接線分支，仍各自有效；
共鄰分支完成不替代它們的原論證。固定 ledger 歸零也不表示整條 weak-deletion 的案例樹已完備。
同樣地，[盾弧校準](reports/c5/shared-results/c5_shield_calibration.md)否定的是較廣可實現圖類的推廣，
不能當作限定完整 Σ=933／941 的原猜想已被反駁。

## 歷史 bytes 與重播

[遷移保存說明](migration-2026-10-30/README.md)管理本次搬移前的
`original-markdown.tar.gz`、`paths.tsv` 及其使用方式。
原報告正文完整保留；為維持閱讀而更新的相對連結，與保存的搬移前 bytes 各有用途。
歷史命令、hash 或具名 commit 中的路徑指向當輪版本，不能直接當作目前 checkout 的路徑。
重播前核對命令所依據的來源版本及原根目錄語境，依保存說明查路徑對照。

本次 Markdown 保存不替代研究 artifacts 與 audits 的既有封存。
大型原始證書、凍結依賴及還原入口仍見[稽核封存說明](../../audits/README.md)；
產生器是否會覆寫輸出、是否要求新目錄，以及 checker 是否只讀，依各報告的明示契約判定。
歷史失敗、空 fibres、完整關係及原 hash 均保留；重建出新結果不會改寫當輪驗證紀錄。

本頁只整理查閱與後續關係。紙證、外部定理、Python 固定域證書、Lean 普通證明與
native 證書仍分別閱讀；文件連結或 DocGraph 檢查通過不代替數學驗證。
