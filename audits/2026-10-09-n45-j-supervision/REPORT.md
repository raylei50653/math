# N45-J 監督驗收：工具與固定控制採納

2026-10-09。使用者返回 [N45-J交付](../2026-10-09-n45-j/REPORT.md)後，
本對話按 [派工驗收規則](../../docs/history/2026-10-09-n2-45-54-parallel-tasks.md#5-結果返回後的監督與第二批)
完成實際重播、來源／交付hash及獨立有限語義核對。

**裁決：N45-J已驗收，限獨立工具與固定控制校準。沒有阻斷finding，
不新增N2來源排除，不驗收尚未回傳的S／U命題。**
研究BASE／canonical HEAD均為 `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
本輪只新增此監督目錄並更新guide／STATUS／任務狀態；J的原89份交付檔及manifest保持原bytes。
其他N45-A／S／U目錄已存在，但本輪未讀其研究交付或代為驗收。

## 1. 候選版本與驗證方式

| 候選 | SHA256 |
| --- | --- |
| J checker.py | `30fea32907167ef37a30b75b82e7550ee14b73ff4303710c60d519d2453f6425` |
| J results/certificate.json | `ecdef656ec2eff887c6725cda21a6d205fce41e5387ce14b2270468f20a861d4` |

66份凍結輸入逐份對 `git show BASE:path` 原bytes、大小及inputs.json的hash。
J的MANIFEST列89項，與實際檔案集合完全相同，逐項hash一致；不只信任其摘要。
certificate內checker／inputs綁定也相同。
重播及預期拒絕前後，含MANIFEST的90份檔案bytes和mtime均相同，見
[fingerprints](input_fingerprints.json)與[checks](checks.json)。

審讀658行checker與128行verify：沒有import或執行上游決策邏輯；
局部relation先枚舉完整piece染色，整圖oracle由原邊回溯；預存relation只作比較。
verify會exclusive建立原logs，故本輪沒有重跑該有副作用的整體driver，
而在監督目錄保存新的只讀replay及拒絕logs。

[review.py](review.py)不import J或任何專案模組。
它用位元色域、強制單色傳播及完整解枚舉，從原邊獨立重建local relations／全部lifts，
按每列一次枚舉整圖染色取得完整root-pair集合，核所有pair與兩種full graph lifts。
再從原spokes、unary完整relation及mixed空fibres重算五项容量与觸發条件。
這不是只比較J checker重播的byte結果。

## 2. 裁決scope與獨立重算

量詞限J凍結的19份N2原圖、54份unit derivatives，以及另外6份N1原圖、24份derivatives；
每圖查十個canonical框列、全部16有序root pins，包含diagonal及空fibres。
依據是BASE原邊、具名contacts、共享座標和固定literal色框；證據層為有限Python。
任意大小B-C2語義仍由Phase B §3.2承擔，本輪沒有Lean或新一般定理。

| 有限域 | 原圖pair queries | derivative pair queries | 容量觸發欄 | 未觸發方向 |
| --- | ---: | ---: | ---: | ---: |
| N2 | 3040 | 8640 | 原圖74；derivative0 | 原圖342；derivative1080 |
| N1另列校準 | 960 | 3840 | 原圖24；derivative36 | 原圖96；derivative456 |

共16,480個完整pair queries重算相同；730個piece-row完整local relation及全部lift集合相同。
所有觸發欄的D／O／δ／o／λ、非負性、columns、左右值及missing前提逐項一致。
觸發欄與未觸發方向不是同一計數單位，不混成同一分母。
完整獨立結果見 [semantic_results.json](semantic_results.json)。

- **C01採納：** N2同源完整joint与原邊染色相等，含全部空fibres及原lift。
- **C02採納：** N2的47條spoke、7份整單接點unary省略查詢精確；兩mixed原relation不變。
  54份derivatives全部Σ1023，沒有拒絕列，不是N2的45／54 minimal-core正控制。
- **C03採納：** χ=0的74個N2原圖容量欄成立；N1額外12份45／54 occurrences及其校準分域保留。
  N1的β-minimality／root刪除／criticality證書由J原checker完整重播與程式審閱核對，
  本輪新solver未重做上游全部minimal-core枚舉。
- **C04／F01採納為介面負控制：** NA7-0002、β01012、P0={7,9}、pins=(1,2)，
  完整fibre及整圖fibre皆空；兩側各選的tuple在共享原頂點9不同，不能拼接。
  額外核保存的602份shared-coordinate診斷，全部選中tuple確有共享座標不一致。
  此finding反駁錯誤投影替換，不指控J或原saved checker，也不是目標來源／B-C2反例。

## 3. 實跑重播與界線

下列命令從研究根目錄執行；每份結果、耗時及log見checks.json。

```sh
python3 -B audits/2026-10-09-n45-j/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-09-n45-j/checker.py --check
python3 -B audits/2026-10-09-n45-j/checker.py --check --source audits/2026-10-09-n45-j/source_examples/NA7-0002-named-root-swap.json --out audits/2026-10-09-n45-j/source-example-results
PYTHONHASHSEED=17 python3 -B audits/2026-10-09-n45-j/checker.py --check --source audits/2026-10-09-n45-j/source_examples/NA7-0002-named-root-swap.json --out audits/2026-10-09-n45-j/source-example-results
python3 -B audits/2026-10-09-n45-j-supervision/review.py
```

五項全部exit0。另重現兩個預期exit1：對既有results重新生成拒絕覆寫；
对J明示的negative-replay比較副本，拒絕其coverage單一數字漂移。
沒有覆寫原J輸出，也沒有重生成任何上游artifact。

完整Σ933／941或整圖D5像來源前提在19份N2均 **not triggered**；
其masks為959×3、1021×4、1015×4、1007×2、1022×6。
原54份N2 derivatives全接受，所以降degree側右值0的N2拒絕實例 **仍缺控制**。
12份N1校準不能填補此缺口。沒有重新證明任意大小disk／Gallai分類或枚舉完整性。
沒有新Lean，未跑lake／axioms；未稽核S／U新命題，未重開ES／ER／U1–U4。

## 4. 採納、後續及傳播停止

N45-J狀態改「已驗收：工具及固定控制」；可供後續S／U的具名原圖增量核對。
S／U返回時，先凍結精確claim與圖／边／ordered frame／roots／rotation，再指定A紙面稽核，
J只對有具名控制或可核證書的部分重算。若需驗新minimal core，另附原core邊集及β-minimality證書。
沒有圖控制的紙面義務不能靠J的finite PASS代替，也不要求為得到控制另開廣域枚舉。

Updated：任務表的J狀態、Kempe導覽相關入口、STATUS的J原交付與本監督報告直接索引。
Reviewed-unchanged：E4／Phase B原paper停止點、U1–U4排除及原55；工具校準不改其命題。
Remaining OPEN：精確目標N2的45／54控制、S／U新命題、45／54來源排除、原55及一般猜想E。
Propagation stop：L1；沒有新來源排除／closure或共同前提失效，不上推父命題或跨線摘要。
HANDOFF活躍線與README入口不變。

未commit／push。J的大型證書保持原bytes；若之後發布Git交付，再按既有封存政策處理，
本次驗收不改原manifest或要求現在重封裝。

## 5. 文件與交付檢查

[documentation_checks.json](documentation_checks.json)保存實際命令／exit／logs。
文件檢查exit0：587份Markdown、7003本地連結；正式docs DocGraph exit0：
62 documents、213 relations、5 families、0 errors／notes。
全工作樹DocGraph exit1，仍為留存scratch副本造成62個duplicate-id，照實保留。
tracked `git diff --check`独立exit0。
[新增檔檢查](whitespace_checks.json)的no-index命令exit1且沒有診斷：比較新增內容有差異，
並非whitespace錯誤。另更正初次派工文件將整段shell最後exit誤記為個別no-index exit0的紀錄，
保留更正理由；此修正不涉及J來源、證書、hash或數學判定。
