# 非正式探索

正式證據為 A/certificate.json、A/cap-lifts.json、A/chord-closures.json，重播入口 A/check.py。以下 gzip 只保存本輪尚未分片／尚未加入三條附加弦時的草稿原 bytes；不具正式證明權威。

- `count-and-c4-v1.json.gz`，uncompressed SHA256 `a432e1cb6744097fc551d91a7ade0fdfec9901d4b7285ec053587acded05a86f`。
- `draft-certificate.json.gz`，uncompressed SHA256 `789d87e3069d5ebc6aa008381e65274c11773345401d6cb1fa8362cfce288d2e`。

`.pickle` 與 `explore*.py` 只記錄浮點發現，不是精確來源實現或不可行性證書。個別 a_i=0、個別 a_i=ell_i=0、個別同一候選四列合同在舊 strongest necessary cone 的 LP 可行性均不得當作真來源。四弦排除最初由LP發現，但正式支援閉包證明完全不使用浮點或 scipy。
