# 既有並行更新的逐項核對

[lineage_complete.json](lineage_complete.json)列出D₃起始後13份既有檔案變更。
本輪先固定bytes，再依各份新證據核對；不以出現在工作樹或作者寫入索引
作驗收。D₂／D₃歷史REPORT、INTEGRATION_PENDING及交付表全部保持原bytes。

| 既有並行更新 | 本輪核對及整合 |
| --- | --- |
| `.gitignore` | 只有A₃／B₃兩份新大型artifact ignore lines；無刪除，D₄未改原bytes |
| `artifacts/MANIFEST.json` | 原entries均不變，只加A₃／B₃兩份大型資料；C₃小artifact直接保存；artifact status及直接SHA256另核對 |
| `README.md` | A₃18／22、B兩primary、C固定key對照獨立audit；加入D₃／D₄覆蓋入口 |
| `docs/STATUS.md` | 三成果直接報告索引保留；加D₃／D₄證據層與新history直接索引 |
| `docs/c5_kempe_guide.md` | A三角色投影／六角色反例分開；B只登記兩primary，其他19／19未判，下一候選原04／12附件{4}保持 |
| `docs/c5_weak_deletion_guide.md` | C只關閉geometry34／join20，下一geometry34／join60；兩key scope與D₃覆蓋另記 |
| `docs/c5_excess_two_mixed_core_four_spoke_mixed12.md` | A₃後續前綴18／22核對；A原22／26正文與artifact不改寫 |
| `docs/c5_excess_two_mixed_core_four_spoke_mixed12_01_12.md` | A₃後續18／22、44／70、56／102核對；A₂當輪20／24保持 |
| `docs/c5_excess_two_mixed_core_four_spoke_mixed22.md` | B₂＋B₃的兩primary閉合核對；原20／20表及root-swap對應不擴判 |
| `docs/c5_excess_two_mixed_core_four_spoke_mixed22_short_face.md` | B₃獨立長face覆蓋核對；短／長face兩份證明粒度保持 |
| `docs/c5_mixed_p3_common_endpoint.md` | C₃後續key核對；原36／140／900不刪，3500具名keys保持 |
| `docs/c5_mixed_p3_one_color_ternary_unary.md` | C₃重新葉數前綴核對；單框點論證不直接套雙框點 |
| `docs/c5_research_synthesis.md` | 原prefix的A₂／C₂停止點過時；接入A₃18／22與C₃geometry34／join20，保留歷史語境及一般缺口 |

三份新專題另加本輪獨立驗收前綴：A₃明列36個指定列固定控制只含
singleton2，singleton3由retained schedules＋任意大小paper覆蓋；B₃明列
degree二shared原bridge保留及僅兩primary；C₃明列未知D_w完整relation
保持符號fibres，partial witnesses不提升為整份M的minimality。
共14份既有README／docs的前後SHA256及精確diff見
[document_changes.json](document_changes.json)與[integration_doc_changes.diff](integration_doc_changes.diff)。
HANDOFF研究線與tags未變，維持原薄索引；沒有為保存輪次內容改写HANDOFF。
新歷史記錄的本文索引在STATUS。原checkers／artifacts／history及全部旧audits保持。

控制檔結果見[control_file_review.json](control_file_review.json)。
本表只作逐項文件語義核對，數學／完整relations／witness驗收以
三份獨立audit和[D₄ REPORT](REPORT.md)明列的範圍為準。
