# 驗證域、重播與封存

2026-10-16；BASE `120aae90cab8bc4881916adc598cf344f2f20f4b`。
普通 P101 任意大小非空由 [PROOF](PROOF.md) 的紙面證明及
[REVIEW](REVIEW.md) 的獨立審查負責。所有有限控制均不作來源排除 oracle。

## 已執行檢查

| 項目 | 結果與實際域 |
| --- | --- |
| 一般 excess 紙面證明 | 兩路獨立重算 PASS；重新核對原窮盡四列 Tutte 分類 |
| 幾何正常／seed17／證書重載 | PASS；canonical SHA 相同 |
| 幾何完整 fibres | 17 點 synthetic dual；17 個刪點 PM fibres、59 個刪點 lifts；128 個 port fibres、116 個 lifts、77 空格 |
| 幾何小圈 | synthetic patch 無 induced C4；五個 induced C5 各為完整 W5 link |
| 五內點局部 core 校準 | 135 個明列必要 cores 均排除；不是完整來源 census |
| 幾何三項負控制 | 錯 boundary incidence、刪除完整 matching lift、虛構非空 fibre 全拒絕 |
| Matching 正常／seed17 | PASS；四個完整平面 cubic controls，全部 PM 數 10、11、15、16 |
| Matching 完整介面 | 128 外 fibres × 8 個 exact marked patterns、128 內 fibres、1206 state cells 與空格全保留 |
| Matching 偶補 | 四個 controls 的 P111 數 1、1、2、2；even111 數 0、0、1、1；逐份整圖 Tait lifts 比對 |
| 重複外端點 | 每個 control 實測兩條零長 exterior path，均偶長；球面 rotation Euler=2 |
| Matching 四項負控制 | 缺空格、錯外側 parity、錯零長 path、刪完整 Tait lift 全 exit 1 |
| 一般 charge 校準 | 精確 affine 係數抵消；局部 excess 0,2,…,20，原 sector 度 6,…,34；正常／seed17 PASS |
| Charge 三項負控制 | 漏盤內 excess、漏 m 成本、錯 z 外面數，全 exit 1 |
| Exclusive creation | 幾何、matching、charge 三個最終證書均拒絕覆寫 |
| 前輪封存 | 原 MANIFEST 與 531 authority inputs 通過；本輪凍結共 626 inputs |
| Lean | `lake build` PASS，8832 jobs；既有 warnings 保留，沒有新 theorem |
| 文件／scoped DocGraph | PASS；97 documents、383 relations、0 errors |
| 全樹 DocGraph | 非 PASS；仍為與 exact BASE 相同的 70 個歷史 duplicate IDs |

幾何細節見 [geometry_verification](geometry_verification.json)；
matching 正常／負控制見 [matching_verification](matching_verification.json)，
獨立重播見 [rigidity_matching_review](rigidity_matching_review.json)。
主支線逐項 stdout、stderr、exit code 及 expected exit code 見 [logs](logs)。
23 份命令收據、正常／seed17 比對、626 個輸入零漂移及最終界線彙整於
[final_checks](final_checks.json)。
負控制的 exit 1 為成功拒絕，不是數學 checker 正常重播失敗。

## 來源覆蓋與中間檔

真正原最小來源數值輸入 **0 個，not triggered**。
synthetic 17 點 patch 有五個奇度內點及一個偶度內點，局部小圈和
factor-critical 條件成立，但沒有完整六 pin assignment、原扇區及合法來源 completion。
它說明局部 patch 條件不足；本輪一般證明使用完整來源 excess 和原扇區。

matching controls 的小 patch 也不符合完整最小來源前提。
普通 PM、偶補 PM、完整 Tait lifts、來源實現及 Lean 的身份均分開。
本輪不將 checker PASS 宣稱為對任意大小圖的形式化驗證。

matching_certificate.json、matching_certificate-v2.json 保留為較早控制版本，
最終重播使用 [matching_certificate-v3.json](matching_certificate-v3.json)。
[RIGIDITY](RIGIDITY.md)、[matching_EQUALITY](matching_EQUALITY.md) 及中間審查
保留原有效的較弱結果；最終 closure 以 PROOF、GEOMETRY、兩份 GENERAL review 為準。

## 重播

從 repository root 執行，下列正常重播皆只讀：

```sh
python3 -B audits/2026-10-16-r6-seven-disk-rigidity-120aae9/geometry_check.py --verify audits/2026-10-16-r6-seven-disk-rigidity-120aae9/geometry_certificate.json
PYTHONHASHSEED=17 python3 -B audits/2026-10-16-r6-seven-disk-rigidity-120aae9/geometry_check.py --seed 17 --verify audits/2026-10-16-r6-seven-disk-rigidity-120aae9/geometry_certificate.json
python3 -B audits/2026-10-16-r6-seven-disk-rigidity-120aae9/geometry_check.py --negative
python3 -B audits/2026-10-16-r6-seven-disk-rigidity-120aae9/matching_check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-16-r6-seven-disk-rigidity-120aae9/matching_check.py --seed 17
python3 -B audits/2026-10-16-r6-seven-disk-rigidity-120aae9/charge_check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-16-r6-seven-disk-rigidity-120aae9/charge_check.py
python3 -B audits/2026-10-16-r6-seven-disk-rigidity-120aae9/charge_check.py --negative missing-m-cost
python3 -B audits/2026-10-16-r6-seven-disk-rigidity-120aae9/check_bundle.py --check-manifest
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
lake build
```

幾何 `--negative` 內部確認三個破壞全部拒絕後回傳 0；
charge 的 `--negative` 模式直接比較破壞證書，預期 exit 1。
需要再次建立含負控制的 matching 收據時，
`matching_run_verification.py` 使用 exclusive output，不可重建已存在的同名收據。
一般接手使用上列只讀單項命令。

## 封存與文件核對

[BASE](BASE.json) 記錄凍結當下的 HEAD、原工作樹狀態、626 個輸入 SHA256，
以及五個前輪 audit 的完整成員名單。上一輪未追蹤 audit 完整保留。
[check_bundle](check_bundle.py) 核對所有 hashes、前輪成員、HEAD、tracked/index 無修改、
本輪 Python 語法與 Markdown 連結；[MANIFEST](MANIFEST.json) 封存本輪全部成員，
僅排除其自身與 Python cache。這是 custody checker，不是一般證明 verifier。

已核對 HANDOFF、STATUS、Kempe guide、C4 直接父題；本輪輸出限獨立 audit。
普通匹配閉合沒有被寫成偶補／完整來源閉合；共用 routing 未修改。
全樹 DocGraph 與 BASE 的 error kinds／logical IDs 相同，沒有刪歷史資料換 PASS。
本輪未 commit、未 push；既有 k+5、K≤22 與固定 r6 k≥25 不變。
