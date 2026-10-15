# 本輪獨立審查與重播

2026-10-15。BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`。

## 紙面交叉審查

- 主 agent 逐步審查 matching PROOF 的 Edmonds face、affine hull、兩方向
  擾動、二分例外及 Euler 接回；未發現缺口。
- boundary-algebra agent 另作一次只讀交叉審查並核對原 T/T0 凍結度數；
  結論相同。採納只到普通完美匹配分離，不推偶補。
- 主 agent 審查 F4 乘積環／理想和／消元、六接點式的 all-r 推導及局部
  generator 下界；已確認 A 是必要上界，不是已實現來源。
- 主 agent 審查 split-z 模型及真圖控制；指出「找到一份split witness」
  本身不足以排除另一份unsplit witness。來源組以明確交錯四點的紙面
  證明及另存的補充檢查處理此疑點，原主證書保持不動。

## 主 agent 實際執行的獨立重播

以下命令皆從 repo root 執行，正常結束為0。

```sh
python3 -B audits/2026-10-15-tait-separation-6ddea32/check_controls.py --check audits/2026-10-15-tait-separation-6ddea32/controls.json
python3 -B audits/2026-10-15-f4-relation-6ddea32/checks/check_relation.py --check
python3 -B audits/2026-10-15-r6-seven-pin-6ddea32/check.py --check
python3 -B audits/2026-10-15-r6-seven-pin-6ddea32/check_unsplit.py --check
python3 -B audits/2026-10-15-route-research-6ddea32/check_cut_bridge.py --check audits/2026-10-15-route-research-6ddea32/cut-certificate.json
PYTHONHASHSEED=17 python3 -B audits/2026-10-15-route-research-6ddea32/check_cut_bridge.py --check audits/2026-10-15-route-research-6ddea32/cut-certificate.json
python3 scripts/check_docs.py
git diff --check
```

結果：

| 查核 | 結果 |
| --- | --- |
| 匹配六圖 | 69份普通完美匹配，762邊對；726邊對觸發無非平凡3割的定理域，全部符合 |
| 七點代數 | 全4^7賦色；624允許列、96份五投影假陽性、336八點lifts、288無r-lift列；精確階數6 |
| 切z模型 | 60 proper軌道、180 pairing cases、1080 partition options；新增排除0 |
| 切z審閱補件 | 枚舉全部unsplit候選，錯誤附加連通要求會刪去660個原模型options；具名反控制成立 |
| 319真圖 | 8點、216完整染色、319完整外框；非面三角形0，原來源未觸發 |
| 切割橋接 | 二十面體36普通／30偶補匹配；五角雙錐11普通／10偶補匹配；完整二元切割與普通匹配逐一相等 |
| root負控制 | 將二十面體普通匹配計數加1的證書遭拒，非零退出；原證書未改 |
| 權威漂移 | root凍結及live authority所有SHA256一致；各組checker亦核各自輸入drift=0 |
| 正式文件導航 | 686 Markdown檔、8957本地連結；anchors/index/HANDOFF/guide progress通過 |
| tracked diff whitespace | git diff --check通過；本輪新增目錄另由bundle檢查涵蓋 |

各組正常、seed17、損壞證書的原始收據：

- [匹配 VERIFICATION.json](../2026-10-15-tait-separation-6ddea32/VERIFICATION.json)。
- [代數 receipts.json](../2026-10-15-f4-relation-6ddea32/logs/receipts.json)。
- [七點 VERIFICATION.md](../2026-10-15-r6-seven-pin-6ddea32/VERIFICATION.md)。
- root負控制保存在 [cut-certificate.corrupted.json](cut-certificate.corrupted.json)，
  供失敗案例重播；它不是正確證書。

新audit文字連結、Python語法、凍結輸入與寫入邊界的最終查核另存
[bundle-check.json](bundle-check.json)。無新Lean程式碼，未執行Lean build；
未重跑全樹DocGraph，沒有以舊快照的重複ID改寫歷史檔。

有限控制均不包含真正最小來源；普通分離的任意大小結論來自紙面證明，
不是從69份匹配或1080個partition外推。原一般K界及r6條件界不變。
