# M3：U1、指定 mixed、D9 全新 checkout 重播

受驗候選：ba0b447f09617591d9f2ba81c988f537af771791；checkout：/tmp/math-m3-ba0b447。

**本分項驗證 PASS：指定 9 次 checker／verifier 命令皆 exit 0。** 全部使用 PYTHONDONTWRITEBYTECODE=1；完整命令、exit、耗時、stdout／stderr 的 bytes 與 SHA256 見 [controls-summary.json](controls-summary.json) 與 commands/、logs/。

| 項目 | fresh 結果 |
| --- | --- |
| U1 default／seed17 --check | 344 核心、3,498 接回、34,980 逐列查詢；target hits = 0；兩份 stdout／stderr 逐 bytes 相同。 |
| 指定 mixed verifier | 新輸出 [mixed-validation.json](mixed-validation.json)；四家族 input SHA256、全部 counts、status 與原 validation 相同；完整 JSON bytes 亦相同。 |
| D9 E4 default／seed17 --check | 54 NA；兩份 stdout／stderr 逐 bytes 相同；N-diagonal／N2 的各自 11 觸發、43 未觸發。 |
| D9 E5 default／seed17 --check | 54 NA + 9 AD；兩份 stdout／stderr 逐 bytes 相同；exact E5 topics 各 0 觸發／63 未觸發。 |
| D9 E6 default／seed17 --check | 9 AD source orbits、90 同圖 D5 transports；兩份 stdout／stderr 逐 bytes 相同。 |

Mixed 詳細域：雙 spoke 126 核心／570 marked cores／5,700 核心列／6,068 接回；spoke＋unary 3,732 接回／37,320 目標比較／89,088 支援查詢／2,640 subdivisions；雙 unary 368,859 UNSAT proofs／17,189 compatible assignments／3,180 subdivisions；mixed omission 344 核心／3,440 核心列／9,152 支援查詢／188 subdivisions，另 3,386 marked compressions 與 2,112 transfer queries。

指定三拒絕列的完整來源前提仍是 **not triggered**：E4 0/54，E5 0/63，E6 0/9 source orbits、0/90 搬運 cases。三份 D9 控制中 counterexample 均為 0；這不驗證未觸發前提，不構造完整 Σ933／941 來源。D9 certificate 中原 b2ca4520da50c9d2898ac6f8f966ac25df3f9609 字串是歷史 audit baseline；本次受驗 checkout 與 scripts 是上述候選 SHA。

本分項只重播既有 verifier／獨立 controls，沒有 M2 紙面稽核、Lean 驗證或新證明。U2–U4、其他 no-mixed core 與 single-root 例外、E5 新證明、source realizability 及一般定理界線維持保留。來源與歷史 artifact 未改寫；原 producer 的歷史 byte／provenance FAIL 不屬於這三份 D9 independent controls 的命令，須由 M3 其他分項另外報告。
