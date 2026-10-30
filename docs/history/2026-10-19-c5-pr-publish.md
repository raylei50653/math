# C₅ P/R 三探測、實圖語義與計數解碼整理發布

2026-10-19；提交父 BASE `ed59843ff8aad66cf3dd895da101787b3daec7a0`。
使用者授權「整理目前進展並 commit + push」。本次交付原附件匯入、兩份相連
audit、研究入口、精確產物政策例外及本發布收據。實際提交與遠端狀態以 Git 為準；
來源原稿及研究輪報告中的未重播／未發布敘述保留當時語境。

## 已完成的範圍

| 來源 | 結果 | 證據及適用邊界 |
| --- | --- | --- |
| [v0.2 附件](../sources/2026-10-19-c5-grammar-v02/README.md) | 原始 RESULTS、模型證書及驗證摘要完整匯入；132 態、264 條 P/R 轉移 | 原程式、測試及 UI 未隨附；來源自述 PASS 與本地重播分開 |
| [四列三探測](../../audits/2026-10-19-c5-observation-depth-ed59843/REPORT.md) | RR／PRR／RRR 重建完整十列支援；對全部 1024 形式 masks 成立。深度≤3 的15候選中是唯一最小探測集合；任兩條至多68類，59對須看到第三步 | 所附矩陣的代數證明及三路有限證書；文法族保四列未來行為的最小機器恰132態 |
| [實圖語義與計數解碼](../../audits/2026-10-19-c5-pr-disk-semantics-ed59843/REPORT.md) | 明定外側 push／右轉在任意大小 C₅ disk 合法；完整字面 fibre 雙射給附件整數矩陣，三探測也可恢復十列固定字面計數 | 任意大小紙面證明、局部圖編譯及792個全圖案例；不需要先有文法代表，不恢復完整著色集合 |

P 保留全部舊圖，在外側增加 z，連到目前有序框的 b4、b0、b1，並以 z 取代 b0
的目前外框位置；R 把框右轉一格。舊 b0 留在同一圖中成為內點。
每次探測從同一來源圖與有序外框的副本開始，全圖統一色置換，保留全部 fibres
及空者；沒有跨候選或跨完整著色拼接。此操作與庫內既有 push 定義一致，
但沒有恢復附件未隨附原程式的歷史身份。

**一般 disk／剩餘 r6 的 F/C 文法代表覆蓋、一般 `K∞=K≤5` 仍 OPEN。**
132 態最小性限已實現的文法族，並非任意 disk 的支援上界或計數機器上界。
下一窄義務是指定剩餘來源的保完整十列文法代表，或計入接回成本的
「成功／更小 bad」實圖化約；可觀察解碼不替代來源覆蓋。無新 Lean theorem。

## 封存與文件傳播

[發布 custody](2026-10-19-c5-pr-publication/audit-custody.json) 保存三組來源／audit
合計85份檔案、8,868,831 bytes的逐檔大小與SHA。原附件及兩份audit的原始位元組
全部保留，原SHA清單及BASE契約不改寫。語義audit的巢狀來源SHA清單雖未列在
該層SHA256SUMS中，仍由BASE的輸入雜湊及本次完整custody覆蓋。

兩份約2.3 MB的全圖完整fibre證書及其精確污染複本，以
[產物政策](../../tools/generated_artifact_exceptions.json) 的 `kind=frozen` 逐檔登記
大小、SHA及封存理由，供CI驗證。沒有用忽略檔案或刪除完整fibres縮減證據。

Updated：state導覽的現況、結果及來源覆蓋停止點；STATUS直接索引及本發布入口；
HANDOFF標記state研究線進行中。Reviewed-unchanged：README的閱讀路徑及一般
主命題邊界適用。傳播止於本線及直接入口，不重寫其他來源研究的停止點。
原附件與舊audit的歷史「待證圖語義」由目前導覽及本發布紀錄連到後續，保留封存證據。

## 本發布輪驗證

[十二次唯讀重播](2026-10-19-c5-pr-publication/replay-results.json)
涵蓋觀察audit的主／A／B及語義audit的計數／局部圖／全圖checker，各跑正常與
seed17；seed17從不同cwd執行，全部通過。獨立唯讀出版審查也核對六項checker、
全部SHA清單、凍結輸入與85份檔案，未發現必要證據缺漏。

語義全圖重播核對792案例、7920完整canonical字面fibres（2278空者）與10642份
完整著色；局部編譯窮舉5120指派。B四項與C七項圖／方向／置換／計數控制亦隨
checker重播。原研究輪的三份證書污染及三次排他建立拒絕沿用未改位元組的收據；
本發布不再擴大圖枚舉，也不宣稱重播原附件缺件的測試或UI。

[工程檢查](2026-10-19-c5-pr-publication/engineering-results.json)
記錄 `lake build`（8832 jobs）及94項工具測試通過。建置保留原有linter警告，
不把紙面拓撲與Python證書升為Lean形式化。
文件、正式docs DocGraph、Git index產物政策、custody與staged whitespace的
實際結果見[提交檢查](2026-10-19-c5-pr-publication/submission-checks.json)。

全工作樹DocGraph仍有72條歷史重複ID錯誤，與本輪保存基線的錯誤行相同；
不稱為全樹PASS。完整staged whitespace以exit 2指出封存 `routing-before.diff` 的十條
空白context行；保留原bytes，只排除此封存檔的scoped檢查通過。

提交後可從repository root唯讀重播：

```bash
python3 -B audits/2026-10-19-c5-observation-depth-ed59843/check_observation_depth.py --check
python3 -B audits/2026-10-19-c5-observation-depth-ed59843/A/replay_pair_depth.py --check
python3 -B audits/2026-10-19-c5-observation-depth-ed59843/B/replay_minimum_observations.py --check
python3 -B audits/2026-10-19-c5-pr-disk-semantics-ed59843/check_count_decoder.py --check
python3 -B audits/2026-10-19-c5-pr-disk-semantics-ed59843/B/check_local_operators.py --check
python3 -B audits/2026-10-19-c5-pr-disk-semantics-ed59843/C/check_full_graph.py --check
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
python3 -B tools/check_generated_artifacts.py
```

目前接續入口由[state導覽](../archive/guides/c5_state_guide.md#3-停止點與保留缺口)維護。
