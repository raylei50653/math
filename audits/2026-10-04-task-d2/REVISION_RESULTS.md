# D₂：18項修訂套用結果

2026-10-04。原清單為[任務D的REVISION_CHECKLIST](../2026-10-04-task-d/REVISION_CHECKLIST.md)，
原清單、REPORT、原checkers與原artifacts bytes均保留。本次全部18項適用。
下表位置以文件和段落定位；D₂本身的純文件差異見[integration_doc_changes.diff](integration_doc_changes.diff)。

| ID | 套用位置 | 驗收結果 |
| --- | --- | --- |
| D01 | synthesis §2 | 標2026-10-02快照；941後續t=2、3全排及共同ε≥2另述，現況回導覽 |
| D02 | synthesis §3.1表 | 改當時已知／當時下一域，補t=1、2、3後續全排與原報告 |
| D03 | synthesis H1 | 日期化後續、完整Σ／degree／連通／edge-minimal induced-C₅ disk前提及合成報告；原提案保留 |
| D04 | synthesis §6 | 改當輪建議；941 t=2標後續已完成，現行排程歸導覽 |
| D05 | synthesis末段 | 分清固定H1已成立、H2／H3與一般推廣未證 |
| D06 | STATUS equal_pair列 | 保留7／9與40／66，補mixed11整型完成與原證書保留 |
| D07 | STATUS short_face／long_face列 | 保留中間輪次，補最終disjoint_pairs入口及其他incidence保留 |
| D08 | STATUS synthesis列 | 固定H1與H2／H3及一般推廣分列；快照不作排程 |
| D09 | equal_pair頁首 | 單一日期化後續，7／9→32／50→22／40→0／0按輪保留 |
| D10 | short_face頁首 | 原8／16與32／50保留，中間長face及最終完成分期 |
| D11 | long_face頁首 | 22／40與crosscut中間14／24保留，最終0／0另述 |
| D12 | synthesis、STATUS、Kempe guide | 完整relations保留，只替換短unary witness，C與另一unary外部頂點逐點保持；只主張五角色投影相等 |
| D13 | equal_pair式(6)前 | 明寫忘C contacts後的四角色完整relation等式；原公式不變 |
| D14 | Kempe guide §3 | 合法搬運原rotation不等於另選canonical rotation；Σ／row／色框／owners同步；933→940、部分941→949保留 |
| D15 | 獨立identity重播及A／B新audit | 沿用D的audit_identity.py重新核對原47／75及各階段原陣列／source字段；A／B增補另出audit，不改舊checker |
| D16 | STATUS t=1／quaternary列 | t=0、2、3後續完成；其他(2,2)incidence保留，mixed11完成 |
| D17 | synthesis頁首、Kempe guide §4 | 前序七輪是已發布批；後續五輪與A／B／C獨立成果另述，不當作總輪數 |
| D18 | D₂ REPORT、history與checks | 原44次的40 PASS／4文件hash FAIL保留，兩份完整payload除直接hash map外相同；新增漂移另記 |

停止點同步由[Kempe guide](../../docs/c5_kempe_guide.md#3-停止點與保留缺口)
維護A／B，由[weak-deletion guide](../../docs/c5_weak_deletion_guide.md#3-精確停止點與下一個窄問題)
維護C。HANDOFF研究線與tag未變，依DOCUMENTATION保持薄索引。
歷史正文／history的當輪數字、hash失敗与未提交語境不改成現況；
詳細新增覆蓋及實際驗證見[REPORT](REPORT.md)。
