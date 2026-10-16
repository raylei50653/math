# R6-JOINT-ZERO 驗證與交付範圍

2026-10-16，BASE `c4c3d99c59cfe4f85b3e33f6831da955a8efcbc7`。
任意大小來源定理的權威是 [A](A/PROOF.md)、[C](C/PROOF.md) 紙面證明；
有限控制不替代來源前提。主 agent 獨立採納審查見 [REVIEW](REVIEW.md)。

## 重播結果

| 組別／範圍 | 核對 | 結果與收據 |
| --- | --- | --- |
| A 普通障礙 | 四個既有控制、262784個刪點集；原面對偶與單點障礙完整重建 | normal／seed17 PASS；偽造平面來源、漏額外邊及覆寫拒絕，[A收據](A/VERIFICATION.json) |
| B 聯合族與奇補 | 81份平面PM、24份空fibre、46對聯合交換路徑；另有明列非平面的Petersen控制 | normal／seed17 PASS；刪空fibre、錯最小值及覆寫拒絕，[B收據](B/VERIFICATION.json) |
| C 全hub介面 | 432 proper局部列、13296介面列、3936 lifts、9936空fibres | normal／seed17 PASS；竄改證書及覆寫拒絕，[C收據](C/VERIFICATION.json) |
| 主 agent 獨立重播 | 三份完整證書重新運算 | 全部PASS，[執行紀錄](verification-runs.json) |
| 文件 | 正式文件連結／anchor／guide；正式docs的DocGraph | 687份Markdown／9011連結PASS；97個DocGraph文件、383關係、0錯誤，見同一執行紀錄 |
| 追蹤檔空白 | git diff --check | PASS |

C 的介面列只校準同份染色的局部代數，未聲稱所有列可延伸成同一來源。
所有真正最小來源的數值測試均為 `not triggered`。
沒有新增 Lean 或重跑既有 Lean build；沒有擴大來源枚舉。
本輪只跑正式 docs 範圍的 DocGraph，未把它報成全樹 DocGraph PASS。

重播命令（均自 repository root）：

```sh
python3 -B audits/2026-10-16-r6-joint-zero-c4c3d99/A/check.py --check audits/2026-10-16-r6-joint-zero-c4c3d99/A/certificate.json
python3 -B audits/2026-10-16-r6-joint-zero-c4c3d99/B/verify.py --check audits/2026-10-16-r6-joint-zero-c4c3d99/B/certificate.json
python3 -B audits/2026-10-16-r6-joint-zero-c4c3d99/C/check.py --check
python3 -B audits/2026-10-16-r6-joint-zero-c4c3d99/check_bundle.py
```

各組亦使用 `PYTHONHASHSEED=17` 執行相同唯讀重播；完整命令與錯誤
拒絕原輸出保留在各組收據。C 的 exclusive-create 負控制另核對
拒絕前後證書及完整壓縮關係的 hash 相同。

## 封存與驗收

[BASE](BASE.json) 封存234份原輸入；[ROUTING_BASE](ROUTING_BASE.json)
另保存允許回寫的四份導覽／索引原 bytes。整包 checker 核對原權威
與 frozen hashes、git改動範圍、新程式語法及新來源文件連結。
初次在本檔尚未建立時，bundle checker 按預期拒絕 REPORT 的缺失連結；
補齊本交付後通過。最終內容與成員集合由 [MANIFEST](MANIFEST.json)
封存；[bundle-check](bundle-check.json) 為封存前的完整檢查收據，
封存後再次唯讀驗證 MANIFEST。

驗收採納的是任意大小來源的全單點障礙排除及原C4扇區收窄。
**主任務W110+W101>0仍OPEN**；普通非空與偶補存在性分開。
未提高一般K≤22或固定r6的k≥25，未宣稱接回小於k+5。

## 文件回寫與停止傳播

- Updated：Kempe導覽改以聯合零值作本輪主任務，更新已排障礙及剩餘
  義務；STATUS索引加入精確新結論；直接父題C4入口加入來源範圍；
  State導覽只更新核對／排程，記完整720態平面cover暫緩。
- Reviewed-unchanged：HANDOFF研究線及標記、一般C4有界定理、舊四輪
  報告與證書。新結果未改變一般界或既有歷史陳述，不重寫原證據。
- Remaining OPEN：兩族剩餘cap共存、非空聯合族正最小奇環數、完整319、
  一般T／T0、r≥7及K∞。
- Propagation stop：L2直接父題；父主命題及全域界未變，不擴大到README
  或全線synthesis。

沒有 commit、push 或外部訊息傳送。
