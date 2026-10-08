# M3 公理 parser helper：v3 控制

**PASS；這是 helper 控制，並非本次 LC build／公理證據。** 原輸入為 Oct05 封存 lean_axioms.log.gz；本次 candidate 的正式 Lean 執行由 M3 root 另行處理。

新版 helper 正確解析原 558 項名稱及順序；positive／rejected／valid 各 179 項，native 數各為 0／1／1。所有個別 rejected／valid 的 native identity 與該 certificate 的 rejected axiom 相符；S4 cover identity 精確相符。Aggregate all_certificates_valid／all_certificates_sound 的 native 數另核對為 179／180。

| 控制 | exit | 結果 |
| --- | ---: | --- |
| historical_baseline | 0 | accepted，符合預期 |
| missing_first_declaration | 1 | rejected，符合預期 |
| duplicate_first_declaration | 1 | rejected，符合預期 |
| sorry_axon_first_declaration | 1 | rejected，符合預期 |
| extra_error_diagnostic | 0 | accepted，符合預期 |
| positive_native_injected | 1 | rejected，符合預期 |
| rejected_foreign_native_replaced | 1 | rejected，符合預期 |
| valid_foreign_native_replaced | 1 | rejected，符合預期 |
| s4_foreign_native_replaced | 1 | rejected，符合預期 |

Missing、duplicate、sorryAx、positive native、foreign rejected／valid native、foreign S4 native 均被拒絕。額外 error 診斷文字仍可被 helper 忽略；正式 fresh Lean 命令必須另外驗證 exit 0，不能以 parser PASS 取代。

完整 helper／來源／歷史輸入 hashes、控制命令、exit、stdout／stderr hashes 與暫存檔位置見 [axiom-helper-controls-v3.json](axiom-helper-controls-v3.json)。未修改 candidate Lean 或 helper。

早先兩次失敗全部保留：第一輪是 reviewer harness 的 regex 轉義錯誤，尚未執行 helper；第二輪發現舊 helper 把 aggregate valid 混入 per-certificate valid，root 已修正。本輪完整重核通過。
