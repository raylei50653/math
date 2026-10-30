# 非面五環恰三缺邊：研究與重播收據

2026-10-30，BASE `e1a90fea41702d7c98747716a5960198aecbecb3`。
開始時工作樹已有其他研究的已改及未追蹤檔；本輪不 commit／push，不清除其他工作。
權威來源：[三缺邊相容性](../../docs/c5_nonfacial_three_gap_compatibility.md)。

## 紙面結果與獨立審閱

極小性與 singleton 內側奇偶迫 `b=11000,E₁={e2,e3}`。
內弦若有，唯一是平行 e0 的 c，且嚴格內點空；無弦時內部是連通、非空偶數點的二端 cap。
全部必要命中為 `{e2},{e3},{e0,e2},{e0,e3},{e1,e4}`；完整內返奇偶不排其中任何一型。

F5-THREE-GAP-TWO-LEAVES 排除 O 至少兩點直接連不同端葉的子型：
任何避開兩端葉的 Γ 族，其每份參考都得同時匹配兩條端葉邊，
卻被完整命中表迫碰至少一個已匹配環點，故整族空。Γ 確保至少有此一族。
這涵蓋有弦／無弦兩個分支，不以端葉指派、命中輪廓或缺族作額外假設。

另證內弦 digon 消去之全部普通 PM fibres：d 不在匹配中有兩個 lifts，d 在匹配中只有一個；
補圖或增加二邊路長、或添偶二環，故每份 odd、每族極小值與全部極小者回拉都保留。
沒有僅憑 Tait n/y 倍率推論 PM，也沒有聲稱一般二端 cap 或 C1 區域逐區轉移。

獨立審閱通過側字、完整回返表、雙端葉整族量詞、內部連通性與普通 PM／odd 轉移。
審閱發現最初證書只記一種端葉指派，已改為兩種指派完整列出；數學排除本身未受影響。
每種指派還分別施加未暴露葉的強制端邊與暴露葉的強制環命中，保留全部候選。

## 驗證範圍

```bash
python3 scripts/c5_nonfacial_three_gap_verification.py --check audits/2026-10-30-five-reference-three-gap/verification.json
```

生成與重播都先獨立重算二缺邊原證書，要求逐 byte 相同；原證書不改。
舊九環、三族集中、全部原來源與舊切口比較按該原完整證書保留，沒有以本輪摘要替換原資料。

| 範圍 | 結果 |
| --- | --- |
| 側字／E₁ 必要接口 | 300 列，295 拒絕，5 個旋轉型保留；不聲稱抽象候選有來源 |
| 非空環匹配命中 | 10 候選，5 必要允許型；完整保留段含孤立點 |
| 雙端葉 | 30 無序葉對／環點對組合，60 個有序實際指派，逐份保留五族命中關係 |
| 強制缺族 | 45 筆無序組合記錄，按指派展開共 90 筆；每個子型均至少一族空 |
| 含內弦真 plane 控制 | 6 份 Γ 內參考（3 單／3 雙），10 種族對／12 份實際產品，40 批完整 C1 |
| 完整普通 PM 轉移 | 原 8,192／縮圖 1,024 邊子集獨立列舉；16 個 0／2／4 葉族、18→10 份匹配 |
| 全部 fibres | 8 個雙 lift、2 個單 lift，逐份 odd 及全部族最小值／最小者保留；嵌入／環序另核 |
| 完整 Γ 真 plane 控制 | 0，未觸發不作紙證或一般來源覆蓋 |

原控制仍 `E₁={2,3}`、含原邊 5 的內弦，偶補完整支援 `{02,03,24,34}`。
直接端葉 0、4 預測缺族 13，與真來源一致；另缺 14，相鄰 34 非空。
它不滿足完整 Γ，合法三缺控制完全保留。

最終 `--check` exit 0，重播含原證書逐 byte 相等與上述全部新核對。
最終 SHA256：

```text
scripts/c5_nonfacial_three_gap_verification.py
7e61dedd5bece36b1e9c4430c14b10a176ff4311bce400fc46191b010be86be3
scripts/c5_three_gap_chord_transfer.py
e35f32dc9825cbda5b1ad09cc2358b7453bf329886e1eec47d95b19d4a184331
audits/2026-10-30-five-reference-three-gap/verification.json
4644fde526b621b40f91f100f5c1f1c9912614535fe9cd7f1e40f4417b752e81
```

## 文件檢查

`python3 scripts/check_docs.py` 最終執行時全域 FAIL，三個缺失路徑均來自同步新增的其他線：
`four_color_no_hub_three_branch_continuation.md` 的 verification.json／three-branch.json.gz，
及 `four_color_twelve_cut_nine_side_classification.md` 的 verification.json。
用同一 `check()` 結果篩選本輪七份新建／更新 docs，錯誤為零；沒有修改其他線以隱藏失敗。

正式 `docs/**/*.md` DocGraph：98 documents、386 relations、0 errors。
全工作樹 DocGraph：72 個既有 duplicate-id 錯誤，來自保留 audits／scratch 快照與正式 docs 的重複 ID；
正式文件通過不改稱全域通過。`git diff --check` 通過。

## 文件傳播與停止點

Closure scope：非面 C₅ 恰三缺、極小 M、完整 Γ 且至少兩點直接連端葉的具名子型。
Canonical Source + Evidence：權威報告、兩份新 script、新 JSON 及逐 byte 重播的前份完整證書。
Updated：二缺報告頁首續接、Kempe／4CT 導覽相關段落、STATUS、直接父任務三及 parity 任務入口。
Reviewed-unchanged：原來源排除、共同輪轉及雙參考引理仍正確；真九環／三族控制保留。
HANDOFF 的研究線及進行中標記不變；原任務全文保留，只在前面加本次子型結果。
Remaining OPEN：零／一直接端葉的三缺全部外返及 C1 相容性、一般二端 cap 的普通 PM／odd 轉移、
面環、四／五缺、一般五參考共同阻擋、E932、4CT、P4，以及相對完整舊切口的嚴格增益。
Propagation stop：直接父主題及相關入口；父題仍 OPEN，不擴寫其他線或 README。

紙證與有限 Python 分層；無外部定理輸入、無新 Lean、無一般染色回寫。
新 JSON 約 0.58 MB，直接保留原檔；沒有改動既有 ARCHIVE records 或 blobs。
