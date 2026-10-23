# 獨立核對

`independent_check.py` 不匯入抽樣器、SAT、NetworkX 或既有 Σ 求解器。
它在輸入的同一張圖、同一外框上完成以下核對：

- 有向三角面恰使用完整邊集；內邊兩側方向相反，外框各邊只出現一次。
- 圖連通；內點 link 是連通 cycle，框點 link 是端點為兩個框鄰點的連通 path；Euler characteristic 為 1。
  因此所給面表確為單一 C5 外框的可定向三角化 disk。
- 十列保留原固定順序，包括空列；完整 witness 覆蓋全部頂點並符合原固定顏色。
- 每列另以四值 domain、singleton propagation、MRV 回溯獨立判斷可延拓性。
  搜尋完全部分支才回報 UNSAT；可選 node cap 一律產生 UNRESOLVED。
- 核對重算 Σ 與原整數相同，再比較凍結目錄的 132 個帶標號 keys。

`check_controls.py` 與 `controls.json` 保存 1320 個目錄列、320 個直接窮舉比較列、
兩份正 topology controls、11 份負 controls，以及 node cap 不混作 UNSAT 的控制。
控制中的 k=25 例只供工具校準，不列入隨機搜尋樣本。

```bash
python audits/2026-10-23-c5-large-k-random-78375cc/review/independent_check.py \
  audits/2026-10-23-c5-large-k-random-78375cc/production.samples.jsonl \
  --catalogue audits/2026-10-23-c5-large-k-random-78375cc/frozen/artifacts/c5_cells/cells.json \
  --max-nodes 100000 \
  --output audits/2026-10-23-c5-large-k-random-78375cc/review/production.review.json
```

結果檔以 exclusive 模式建立，記錄輸入、目錄及核對器 SHA256。
只有 `VERIFIED` 計入整十列 CSP 重搜完成數。
`complete_review.py` 另核正常／seed17 的逐列結果完全一致，並獨立驗每份原圖完整 SAT witness；
若 CSP 搜尋 cap 僅發生在已有合法完整 witness 的 SAT 列，該 witness 已充分證明可延拓性。
任何拒絕列都必須有已完成的獨立 CSP UNSAT 判定，否則 completion 直接失敗。
此區分保留原 cap 記錄，沒有把未完成搜尋變成 UNSAT。

第一階段的 `production.completed.json` 完成核對 10,800 張原圖：91,940 份完整 SAT witness，
16,060 份已完成 CSP UNSAT 判定。整十列 CSP 重搜完成 10,798 圖；另兩圖的三份
SAT 搜尋 cap 由原完整 witness 直接核對完成，報告明列原行號、pattern 及完整顏色。

`check_metadata.py` 重算第一階段的全部結構欄位與分層直方圖；
`check_targeted_metadata.py` 另獨立重建第二階段的各層五圈、每步 vertex split、
種子圖 SHA256／disk 與必要幾何，再核最終來源及全部直方圖。
核對成功仍只限輸入的有限具體來源。

第二階段 3,600 圖的 Σ 全為 `1023`。`check_full_relation.py` 獨立重核各原圖的 disk
與十份完整 pinned witness，即已證明完整十列關係；沒有拒絕列需要作 UNSAT 搜尋。
正常／seed17 的兩份 full-relation receipt bytes 相同。
額外 CSP 診斷也已完成：3,584 圖十列重搜完成、16 圖遇到 SAT 搜尋 cap，正常／seed17
逐列結果相同；這些 cap 不影響先前由完整 witness 直接證明的 Σ。
`targeted.completed.json` 將此 authority 與全部必要幾何／種子核對收據接在同一輸入 SHA 上。

完成收據可用新路徑重播，原收據不覆寫：

```bash
python audits/2026-10-23-c5-large-k-random-78375cc/review/complete_reviews.py \
  production --output /tmp/c5-large-k-production-completed-replay.json
python audits/2026-10-23-c5-large-k-random-78375cc/review/complete_reviews.py \
  targeted --output /tmp/c5-large-k-targeted-completed-replay.json
python audits/2026-10-23-c5-large-k-random-78375cc/review/check_full_relation.py \
  audits/2026-10-23-c5-large-k-random-78375cc/targeted.samples.jsonl \
  /tmp/c5-large-k-targeted-full-relation-replay.json
```
