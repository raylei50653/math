# Bernhart retained 原邊交會與局部來源紀錄

2026-10-29；權威來源為 [retained 交會奇偶報告](../ck_bernhart_retained_intersection.md)。
接續兩個 41 列 full-lift 子靶，沒有 commit／push 或改寫舊證書。

## 成果及保留範圍

紙面證明同一 cut-side 內、端點集合互異的兩個 mixed retained 分量必滿足：
共同第三色原邊兩端同 rotation 色序的條數，模二等於兩條路徑的端點交錯指標；
有閉圈時右側為零。共同端點分支未涵蓋，不能當成通過。

為兩個射線各取單色字的唯一三份 signatures，以同一 14 環及三條內弦、
boundary 同時重標構成兩份真 plane 局部控制。保存全部原邊、rotation／面、
完整染色、各兩條原路徑、有序 ports、共同第三色邊與兩份完整 retained 系統。
每份第一條路徑的後繼 signatures 符合目標，另一條合法同圖交換產生目標零權重 signature。
因此排除的是這份具名局部接線作為射線來源中的染色，沒有排除所有其他接線。

對非空 cubic interior，單色字全部 2↔3 交換另證實際比例須為偶整數；
空內部由完整 literal word 質量排除。偶比例仍全部 OPEN。
另記一份六環內弦紙面反控制，否定將不變單色字配對上推全支援同色的收縮捷徑。

## 有限證據及檢查

來源及完整輸出：

- [局部控制程式](../../scripts/ck_bernhart_ray_local_witnesses.py)、[證書](../../audits/2026-10-29-bernhart-retained-parity/ray-local.json)
- [交會奇偶程式](../../scripts/ck_retained_intersection_parity.py)、[證書](../../audits/2026-10-29-bernhart-retained-parity/rotation-controls.json)

局部證書保存兩個 lift 各 4,923 條等式核對、兩份完整真來源及四條 actions，
並各有一份非切口頂點 rotation 負控制。獨立 checker 的 theta sphere／torus
正負控制皆通過；兩張舊 wheel／stack disk 各 43 份完整色名正規化染色、344 條
boundary actions，合計核對 7,124 份奇偶式；2,992 份共同端點分支明列未涵蓋。
這些數字都是固定來源的完整有限核對，不能提升為來源覆蓋。
局部四條 actions 另核 40 組交會條件，16 組共同端點未涵蓋。

重播及文件檢查命令：

```bash
python3 scripts/ck_bernhart_ray_local_witnesses.py --check audits/2026-10-29-bernhart-retained-parity/ray-local.json
python3 scripts/ck_retained_intersection_parity.py --check audits/2026-10-29-bernhart-retained-parity/rotation-controls.json
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
python3 tools/docgraph check
git diff --check
```

最終執行結果與來源 SHA256 見 [本輪收據](../../audits/2026-10-29-bernhart-retained-parity/RECEIPT.json)。
兩支數學 checker、文件連結／索引、正式 docs DocGraph 及 `git diff --check` 均通過。
全工作樹 DocGraph **失敗**：72 項 duplicate-id，來自保留的 audits／scratch 凍結副本，
與正式 docs 的 0 errors 分開記錄；[完整輸出](../../audits/2026-10-29-bernhart-retained-parity/docgraph-full.log)
保留，不刪歷史副本以換取通過。
大型 rotation 證書按[原封存規則](../../audits/README.md#新-checkout-的還原)保存 bytes；
新 checkout 先執行 `python3 tools/audit_archive.py restore --artifacts` 再重播。
本輪僅追加這一份 7,687,306 bytes 的原檔，新增 282,624 bytes deterministic gzip；
逐 byte 解壓核對成功，追加前的 6,155 份檔案及 3,130 份 blob records 均保持原值。

## 治理核對

- Closure scope：沒有完成整條射線、整個殘餘面或可約性；只完成具名 rotation／接線控制。
- Updated：L0 新報告、兩支程式及證書；原跨 split 稽核加入後續連結。
  L1 的 4CT／四色工具導覽及 STATUS 加入新來源與量詞限制。
- Reviewed-unchanged：共同切口契約的 soundness、原 76 列／兩射線分解及
  `LOCK-NO-GAIN` 單 split 裁決均不變；沒有修改主求解器或 Lean。
- Remaining OPEN：所有正比例同源接線的強迫與排除、76 列任一新座標必零、全部阻擋排除。
- Propagation stop：停在 L1；新條件不撤銷直接父題結論，不觸發 L2／L3 或 HANDOFF 活躍標記調整。

工作樹原有大量其他未提交研究變更，本輪保留它們；發布狀態不由本次 checker 判定。
