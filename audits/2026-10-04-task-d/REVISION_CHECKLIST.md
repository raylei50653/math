# 任務 D：交給整合者的具體修訂清單

本清單依 2026-10-04 08:58:32 Asia/Taipei 副本定位；未套用任何共用文件
或歷史 artifact 修改。先以原句子定位，再更新行號。完整稽核及實際結果
見 [REPORT.md](REPORT.md)。

| ID | 位置 | 具體修訂 | 驗收 |
| --- | --- | --- | --- |
| D01 | `docs/c5_research_synthesis.md:98,107` | 標「2026-10-02 各線快照」，Kempe 列補「後續 941 t=2、t=3 全排，與 933 同得 ε≥2；現行 ε=2 停止點見 Kempe 導覽」。也可將該列改為現況，但不能保留當前式待辦。 | 後段與前段固定來源下 ε≥2 相符，舊輪次有日期。 |
| D02 | 同頁 `:131-134` | 表頭改「當時已知／當時下一域」；941 列補後續 t=1 `(2,1,1)`、t=2 `(2,1)`、t=3 `(2)` 全排，鏈 two-spoke／three-spoke 原報告。 | 不再把 ε≥1 或 t=2／3 待辦當作當前結果。 |
| D03 | 同頁 H1 `:204-220` | 局部加入：「後續（2026-10-02）：H1 在既有固定完整 Σ=933／941、Σ-edge-minimal induced-C₅ disk source 前提下已成立。以下支持／未完成／實驗保存 b97b107 當輪提案；不再是當前未解題目。」保留完整有效 degree／Σ 前提並鏈 three-spoke 合成報告。 | 不写無前提的 H1 已證；不推出 ε≥3、來源實現或一般出口。 |
| D04 | 同頁 `:264-275`，尤其 `:270` | 標「當輪建議」；原 941 t=2 第一優先列標後續已完成，鏈 t=2／t=3 證據。現行排程統一指向導覽，不另複製新 frontier。 | 已完成問題不再列為當前第一優先。 |
| D05 | 同頁 `:298` | 改為：「以上保存當輪假設與初驗；H1 已在後續固定來源前提下成立，H2、H3 及一般推廣仍未證；普遍四階來源說法已在當輪淘汰。」 | H1 與 H2／H3 狀態分開。 |
| D06 | `docs/STATUS.md:172` | 刪去當前式「整個子型未完成」；補「原 40／66 unequal 殘留由後續短／長 face、crosscut、短框弧及不相交 pairs 全部封閉；同一 mixed11+各側 unary 子型完成，原證書保留。」鏈完成報告。 | 與原 47／75 ledger 的 0／0 相符，保留當輪數字。 |
| D07 | 同頁 `:170-171` | 中間殘留數保留，補「子型由不相交 pairs 完成報告封閉；其他 incidence 保留」。 | 現況列有最終後續入口。 |
| D08 | 同頁 `:234` | 「三假設均保留未證部分」改為「H1 已在固定 933／941 source 前提下成立；H2／H3 及一般推廣仍未證；保存當輪快照，不替代導覽排程」。 | 索引不否定前段已成立的固定 H1。 |
| D09 | `docs/c5_excess_two_mixed_core_four_spoke_equal_pair.md:3-9` | 頁首改成一段日期化後續：「当輪 7／9 排除後，短／長 face 收窄；其後 crosscut、短框弧、不相交 pairs 完成此原子型。以下原輪次數字與證書保留；ε≥3 未證。」 | 頁首不再同時說 subtype 未證／完成。 |
| D10 | `docs/c5_excess_two_mixed_core_four_spoke_short_face.md:3-8` | 同上：短 face 當輪 8／16，長 face 的中間 frontier 有日期，最終 mixed11 完成以最新完成報告為準。 | 保留正文及 history 當輪 32／50，現況前綴單義。 |
| D11 | `docs/c5_excess_two_mixed_core_four_spoke_long_face.md:3-8` | 同上：當輪 22／40、crosscut 當時 14／24與最終 0／0 分期標明；整份 subtype 完成，其他 incidence／ε≥3 保留。 | 不把中間停止點改寫成最新數字。 |

以下是措辭精度與後續核對工具的改善，不是本次已發現的數學 payload 錯誤：

| ID | 位置 | 建議修訂 | 驗收 |
| --- | --- | --- | --- |
| D12 | `docs/c5_research_synthesis.md:24,27`、`docs/STATUS.md:167` | 「原 joint／witness 保持」改為「完整原 relations 保留；只替換固定短 unary 的整份 witness，C 與另一 unary 外部頂點逐點保持，主張五角色投影相等」。 | 不被解讀成所有六角色 tuples 或被替換 witness 都不變。 |
| D13 | `docs/c5_excess_two_mixed_core_four_spoke_equal_pair.md:152` | 「完整 relation 等式」可明寫「忘 C contacts 後的四角色完整 relation 等式」。 | 公式(6)角色清楚；不改正確公式。 |
| D14 | root-swap／D₅ 摘要、具名域說明 | 補「原 rotation 隨 relabeling 搬運並保持合法；不要求另行選出的 canonical rotation 相同。完整 Σ、row、共同色框與 owner 角色同時搬運。」保留 933→940、941 部分→949 的實例。 | 16 份 self-identities 不被宣稱 canonical face 集協變；不維持錯誤 source mask。 |
| D15 | 新的独立 ledger 稽核入口 | 沿用本次 `identity/audit_identity.py`；若加入一般 checker，另出版本／產物，核對 exclusion/residual 原陣列重複、每個階段 source fields 及獨立 source-filtered domain。 | 不只在 set 化後核對大小；不修改舊 checker 以重寫旧 certificates。 |
| D16 | `docs/STATUS.md:194`、`:173` | t=1 的「其餘 t 保留」標後續 t=0、2、3 全完成；(3,1) quaternary 列的「(2,2) 保留」精確為其他 `(2,2)` incidence 保留，mixed11 已完成。 | 分期後續一致；不宣稱所有雙 root 分支完成。 |
| D17 | synthesis `:5`、Kempe guide `:86` | 「四-spoke 七輪」補清楚是前序發布批，另有最新五輪未提交成果。 | 不把發布批次數當成果總輪數。 |
| D18 | 整合驗證紀錄 | 記錄本次 44 次 check 的 40 PASS／4 文件 hash FAIL，以及兩份完整 payload 相同；歷史 byte-check 不改寫為 PASS。 | 保留原 artifacts；不得為清除漂移重生成歷史證書。 |

整合後執行文件 checker、DocGraph、`git diff --check`，並在新整理紀錄中
記明文件 hashes 的新增漂移。若需修訂實際證書合約，建立新版本或獨立
audit，保留原 bytes 與原 historical scope。本次未要求、亦未執行上述
修訂或任何 commit／push。
