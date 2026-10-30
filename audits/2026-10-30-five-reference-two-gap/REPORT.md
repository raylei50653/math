# 非面五環二缺邊：研究與重播收據

2026-10-30，BASE `e1a90fea41702d7c98747716a5960198aecbecb3`。
開始時 main 已有多份改動與未追蹤研究檔；本輪不 commit／push，不清除其他工作。
權威來源：[二缺邊排除](../../docs/c5_nonfacial_two_gap_exclusion.md)。

## 紙面結果

先從完整 E₁ 恰缺 e、f 導出兩個常值且相反的實際側字分量，C₅ 只剩四種旋轉型。
再證完整 singleton 參考的命中端點側別等於同一嚴格內點數的奇偶，
而 M 使該數與內向 incidence 數同奇偶。四型全被拒絕。
更強結論為任意非面奇環至少缺三條單命中原邊，不需極小性或完整 Γ。
固定字極小性另藉實際完整 C1 區域，排除全部內向 singleton。

獨立紙面審閱已核對內弦雙 incidence、長一內弦、全部未接 O 的閉環與完整 W；無阻斷漏洞。
未迫出恰命中 e、f 之一的參考；採用的是任務允許的不可行完整段接法路徑。

## 實際核對

命令：

```bash
python3 scripts/c5_nonfacial_two_gap_verification.py --check audits/2026-10-30-five-reference-two-gap/verification.json
```

結果 exit 0。原來源證書先獨立重算，與 frozen JSON 逐 byte 相同，原證書均不改。

| 核對範圍 | 實際結果 |
| --- | --- |
| 原 frozen 來源 | 17 圖，基線 4 份 M 測試／5 筆奇環，含 3 筆非面奇環 |
| 原來源全部二葉普通匹配 | 154 份；新增 8 筆實際非面 C₅ 控制，缺邊四或五 |
| 新具名三缺邊 plane 控制 | 完整輪轉、全部面走法、Euler=2、外葉環序及內弦身份通過 |
| 新控制獨立原邊子集核對 | 全部 8,192 子集，18 份零／二／四葉 PM；完整關係與補圖奇環數均相同 |
| 合計全部參考與十種族對 | 22 筆完整參考，130 筆族對記錄，26 份實際笛卡兒產品 |
| 完整 C1 區域子集 | 152 批，包含新控制 40 批；非極小控制不套極小約束 |
| 抽象 C₅ 二缺邊接口 | 10 組缺邊 × 2 個混合側字，共 20 筆；全拒絕 |
| 舊控制 | 九環 1 份、三族集中 2 份及完整舊共同切口相位比較全部保留 |
| 真 plane 完整五族來源／二缺邊觸發 | 均為 0，不當作紙面證明或來源覆蓋 |

新增三缺邊控制的完整二葉偶補支援為 `02、03、24、34`，各兩份。
它只在 Γ 內有三個非空族，**不是完整 Γ 來源**；三缺邊下界只在較弱 plane 來源上示達界。
全部 singleton 的內側補圖段明列每個嚴格內點恰出現一次，多命中參考未刪除。

最終核對輸入 SHA256：

```text
scripts/c5_nonfacial_two_gap_verification.py
f34e1f4dd3cf223f78013a8c7f90dabe3ea31e5b07e1b85f49cccf4fd092c6ea
audits/2026-10-30-five-reference-two-gap/verification.json
a4122ae951f679debcb836f7a4a104ce6cf7280feb8789ff68c653fee99611a0
```

## 文件與保存檢查

`python3 scripts/check_docs.py` 已執行；全域未通過，錯誤來自其他同步新增的
period4-S5、no-hub-min5、shared-exterior 文件之待產生路徑、錨點或 STATUS 索引。
再用同一 checker 的 `check()` 對本輪七份新建／更新文件篩選結果，錯誤為零；
不把 scoped 通過寫成全域通過，也未改動上述其他研究線。

4,234,961 bytes 的完整新 JSON 依既有政策只追加這一條路徑封存：

```bash
python3 tools/audit_archive.py append --paths audits/2026-10-30-five-reference-two-gap/verification.json
```

新增一個 deterministic gzip blob，共 160,112 bytes；原檔 bytes 保持，
逐項核對既有 ARCHIVE files／blobs records 均不變，並獨立解壓核 SHA256、大小及逐 byte 相等。
`.gitignore` 與 `audits/ARCHIVE.json` 只因本次新封存追加對應記錄。
新 checkout 先按 [既有還原流程](../README.md#新-checkout-的還原)恢復資料，再執行本輪 checker。

## 收尾與傳播

Closure scope：非面 C₅ 且完整 E₁ 恰二缺邊；並證一般非面奇環的至少三缺邊必要界。
Canonical Source + Evidence：上述權威報告、checker 與原始完整 JSON。
Updated：原來源入口、Kempe／4CT 導覽的相關段落、STATUS、直接父任務三及 parity 任務入口。
Reviewed-unchanged：共同輪轉與雙參考的原引理仍正確，九環／三族負控制保留；
父題 P1–P3 完整驗收與 E932 未完成，HANDOFF 研究線與進行中標記不變。
Remaining OPEN：一般來源如何迫出該子類、三缺以上與全部多命中、一般五族共同排除、E932、4CT、P4。
Propagation stop：直接父主題與現有相關摘要；一般主線語義不變，不擴寫其他研究線。

紙證與有限 Python 核對分開；無外部定理輸入、無新 Lean、無一般染色回寫。
未宣稱相對完整舊共同切口嚴格增益或一般無增益。
