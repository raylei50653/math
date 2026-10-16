# 驗證域、重播與封存

2026-10-16，BASE `120aae90cab8bc4881916adc598cf344f2f20f4b`。
任意大小結論由 [PROOF](PROOF.md) 的紙面證明及 [REVIEW](REVIEW.md)
負責；下列有限計算不作來源排除 oracle。沒有新增 Lean theorem。

## 本輪已執行的檢查

| 檢查 | 實際結果與驗證域 |
| --- | --- |
| 幾何證書，正常及 `PYTHONHASHSEED=17`、另顯式 `--seed 17` | PASS，canonical bytes 相同；一個明列 11V/23E/13F disk，全部 links、ports、induced C4/C5、24 個刪點 PM lifts |
| matching 證書正常／seed17 | PASS，stdout 相同；三個明列局部 graphs、全部 128 boundary cells、1206 狀態格及所有完整 lifts |
| 三個雙份 patch gluing controls | 全部普通 PM 數 29、44、104；逐一與直接整圖枚舉比對 complement cycles 與所有 labelled Tait lifts |
| corrupt path parity／刪除空格／corrupt odd-cycle flag | 三者皆 exit 1；與完整獨立重建不符 |
| 刪除幾何證書一面／宣稱來源實現 | 兩者皆 exit 1 |
| `--write` 重建已存在的兩個最終證書 | 皆 exit 1，exclusive creation 生效 |
| 前輪 double-W5、chorded-five 正常／seed17 | PASS，原證書未變 |
| 前輪 weighted curvature、完整 W5 fibres | PASS |
| 前輪共同 P111 saturation 正常／seed17 | PASS；5 controls、12 saturation checks、720 個獨立 uncrossing algebra checks |
| `lake build` | PASS，8832 jobs；既有 warnings 保留 |
| `python3 -B scripts/check_docs.py` | PASS |
| scoped DocGraph：`docs/**/*.md` | PASS，97 documents／383 relations／0 errors |
| 全樹 DocGraph | FAIL，70 個歷史 duplicate IDs；不是全樹 PASS |
| 精確 BASE Markdown DocGraph 比對 | PASS，3519 個 tracked Markdown；同樣 70 個錯誤種類與 logical IDs |
| audit custody、語法、audit 本地 links、whitespace、final seal | 交付檢查另有收據；原 531 個輸入 hash 與四個前輪成員名單均保持 |

原共同 saturation 控制的來源交叉割測試有 0 次，沒有將它寫成來源 uncrossing
數值驗證；720 次來自明列非來源 K3,3 algebra control。新來源 uncrossing
的量詞仍是紙面同一 P111 全族，沒有替不同割挑不同 witness。

執行細節與逐項 stdout／stderr 見 [final-verification](final-verification.json)、
[initial engineering checks](verification-initial.json)、
[delivery checks](delivery-checks.json)、[logs](logs)。
所有新 checker 使用標準函式庫，未重新執行外部有限來源 census。

## 有限域與完整 fibres

[matching_certificate-v2](matching_certificate-v2.json) 是最終三-control 證書。
初版 [matching_certificate](matching_certificate.json) 的兩-control bytes 原樣保留，
不再用目前三-control checker 當作最終 replay target。
三個局部 matching controls 的 lifts 數為 29、38、64，空 boundary cells
為 99、93、81；空狀態格分別 1177、1168、1149。偶數 selected-port
patterns 亦明確保留為空。每個 N 的實際 path、cycle 及全部 Tait lifts 都保存，
不是只留邊際 support 或數量。

[geometry_certificate](geometry_certificate.json) 的 13F patch 有四個 degree-five
內點；全部 induced C5 均為實際單中心 W5，無 induced C4，dual 是 factor-critical。
這僅校準局部 disk／FC／弱 Euler 前提，不能滿足本輪原 m 扇區新條件。
它沒有完整六 pin assignment 或合法來源接回，不是符合來源契約的反例。

兩個證書均聲明真正原最小來源 **0 個、not triggered**。
原完整染色 fibres 與所有 r lifts 沒有被本輪重新投影、丟棄或用 synthetic
補件取代；完整來源契約仍是紙面定理的假設。matching parity join 允許外端點
重合及零長外側 path，此一般情形由紙面證明，雙份 patch controls 只測了不同外端點。

## 保留的啟動失敗與修復

[final-verification](final-verification.json) 刻意保留一次整批狀態 FAIL：
當時沿用前輪文件的 `uv run --offline --with-requirements requirements.txt`
啟動 saturation checker，uv 嘗試在唯讀 cache 建立 lock 而 exit 2。
數學 checker 尚未啟動，其餘該批命令均達預期結果。

實際讀取本版 saturation checker 後確認它只用 Python 標準函式庫，
改以直接 `python3 -B` 正常／seed17 重播，兩次皆 PASS 且輸出相同。
詳見 [saturation-repair](saturation-repair.json)；失敗 stdout／stderr 原樣保留。
[run_verification](run_verification.py) 的後續重播入口已改用直接 Python，
沒有改寫前輪 checker 或偽稱原失敗批次 PASS。

## DocGraph 與封存

[docgraph-baseline-comparison](docgraph-baseline-comparison.json) 使用 exact BASE
全部 tracked Markdown 的臨時唯讀模型比對目前全樹。兩者錯誤種類／ID 完全相同，
但訊息列出的 snapshot 路徑不同。沒有刪除歷史檔或 frozen copies 製造 PASS。
[check_docgraph_baseline](check_docgraph_baseline.py) 可直接重播此比較。

[BASE](BASE.json) 記錄 531 個來源及前輪文件 SHA256，並核對四個前輪 audits
的完整成員名單。本輪 [MANIFEST](MANIFEST.json) 包含除自身及 Python cache
外的每個成員與 SHA256；cache 是本輪 import 產物，交付前移除。
[check_bundle](check_bundle.py) 檢查 custody、固定 HEAD、無 tracked/index 修改、
新 Python 語法與 audit 本地 links。它是交付 checker，不是任意大小數學證明 verifier。

## 重播命令

從 repository root 執行，單一證書檢查只讀：

```sh
python3 -B audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/check_geometry.py --check audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/geometry_certificate.json
PYTHONHASHSEED=17 python3 -B audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/check_geometry.py --seed 17 --check audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/geometry_certificate.json
python3 -B audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/matching_check.py --check audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/matching_certificate-v2.json
PYTHONHASHSEED=17 python3 -B audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/matching_check.py --check audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/matching_certificate-v2.json
python3 -B audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/matching_check.py --check audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/matching_certificate-v2.json --negative path-parity
python3 -B audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/check_geometry.py --check audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/negative-geometry-source.json
python3 -B audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/check_bundle.py --check-manifest
python3 -B audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/check_docgraph_baseline.py
lake build
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
python3 -B tools/docgraph check
```

上列兩個負控制預期 exit 1；全樹 DocGraph 目前也預期 exit 1，原因不同。
全套 [log runner](run_verification.py) 保留本輪整批執行命令；
它 exclusive-create logs／負控制檔，只適合尚未封存的新 exclusive audit，
不可在這個已封存目錄中直接重建。一般接手使用上述只讀命令。

本輪未 commit、未 push。普通101、偶補正值、完整319、一般無界主命題均 OPEN；
原 `K≤22`、固定 r6 `k≥25` 與接回成本 `k+5` 不變。
