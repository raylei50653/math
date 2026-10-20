# C 對 A 的獨立交叉審查

審查結論：**PASS，限 A 所列任意大小分量／三邊五輪條件及必要 C11 介面。**
沒有從未刪邊界推出真來源、正計數解、五邊路長下界或較小 bad。

審查版本：

| 檔案 | SHA256 |
| --- | --- |
| A/PROOF.md | 244de211f129082037eb38393f1d4ebe777b29f3dcac3e5219f93f5565b4b437 |
| A/interface.py | aec925f0a3392afe1e9451e40277c063cedc9eafbab71980bc91d1f7fa58a671 |
| A/check.py | 34d06cd9971360b0c0be2571ee34cc2f7f04e6022e19f1a3b095b7f8d24ddebc |
| A/certificate.json | 67dfb50f52930aad89df38e70ce78a051fab4a325169509a1927735b00cf8380 |

人工獨立核對：

* 固定同一完整 d_a 著色，Q1 的 R-q、Q2 的 L-n 或 L-t 條件都來自前輪
  實際分量交換，不是任選必要分割。雙側分割同時保留 rim 相鄰點及精確
  接框塊數，得到2、2、7、7型；不將互補色對當成另一張來源。
* R-U-V-q 的 U、V 不會是舊 rim 點：R 的 rim 鄰點 n、L 顏色皆1，
  q 的 rim 鄰點 L、c 顏色為1、0，均不能作所需的23路下一點。Q2 同理。
* 實際 pocket `(R,L,q,V,U)` 中，L 的完整向內 star 被兩條 rim 邊與
  內部三邊路困住；L 在 D10 只失 h，故度至少4。Q2 中 R 同樣只失 h。
  這是原完整 stars 的結論，不能只靠一張抽象五邊形的頂點數。
* 保留五種空填片及單中心 W5。W5 的 middle core 度3不合下界；空填片
  唯一合 proper 與舊 induced rim 的兩弦恰為 middle fan，使 core 度4、
  原度5。完整原 h star 與同一著色排除外五圈全部可能弦，得到真正的
  原 induced W5。空 fan 本身仍合法，所以不能誤推三邊路不可能。
* 剝下 L 或 R 後，C11 保留所有其他私有點。每個被剝中心色先固定，再
  取其完整左右 cap product；Q1/Q2 同一中心色的商條件仍保持。介面只
  用非負軌道係數判零，未將它們標作固定字面 N，權威界線正確。

已獨立執行

```
python3 -B audits/2026-10-19-r6-941-chains-13dc5ff/A/check.py --negative-controls
```

目前原零列已修正為零基索引 `(1,4,6)`，真支持補mask恰941；重播得到
36487 columns、C11 live 5975／5987、四個指定短路徑邊界全部存活，八個
負控制全部拒絕。舊 `(0,3,5)` 發現版本不作任何來源證據，已在 A 的
failed-zero-indices 發現檔歸檔。審查未依賴該失敗計算。

版本補記：root 最終只規整 A/interface.py 的檔尾換行。C 已獨立讀取
`A/discovery/pre-whitespace-normalization/` 的兩份 gzip 原件，確認 Python
AST 完全相同，原始程式 bytes 除檔尾換行外亦完全相同；新舊 certificate
逐項比較僅 `inputs_sha256` 的 interface.py SHA 一值改變，全部數學欄位
相同。上表已更新為最終 SHA；原正常重播審查仍適用，最終正常／seed17
由 root 另行重播。
