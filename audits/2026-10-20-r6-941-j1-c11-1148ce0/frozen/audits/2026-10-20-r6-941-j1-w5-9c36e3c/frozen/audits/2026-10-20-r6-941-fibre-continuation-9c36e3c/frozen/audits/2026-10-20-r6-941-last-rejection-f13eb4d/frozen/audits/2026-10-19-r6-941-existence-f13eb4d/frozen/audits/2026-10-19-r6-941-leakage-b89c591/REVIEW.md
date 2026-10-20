# 獨立審查與適用範圍

2026-10-19，固定 BASE `b89c5913cea9df2305845be0f65fa6f1c1aaf55f`。
三位研究者各自只寫本 audit 的 A／B／C 目錄；舊來源 bytes 以 SHA 封存，
主證明與實作交叉核對，不修改彼此證據來湊結果。

| 核對 | 獨立證據與結論 |
| --- | --- |
| B 的來源、相異點、實際 C10、兩份強制正 fibre | [A review](A/REVIEW-B-C.md)、[C review](C/REVIEW-B.md)；確認兩個不同完整 witness 不被拼接，原 b 唯一、色置換與逆映射一致 |
| C 的 941 精確洩漏等式 | [B review](B/REVIEW-C.md)、[A review](A/REVIEW-B-C.md)；另由主審獨立 LP 對偶找到 `2N01212(GB)=A_a+z17+z118+z179`，C 用精確有理消元驗證整個 44 維空間 |
| A 的共同 C10 控制與實作 | [B review](B/REVIEW-A.md)、[C review](C/REVIEW-A.md)；逐格核對 cap 矩陣、交換重數、signed-span、完整 U319、真正兩份指定正 fibre |
| 主審整合 | 對回原兩份 low-p 存在性正文；確認只淘汰 G_B 指定合同，Q1/Q2 及完整支持替代證書 OPEN；候選成本未變，沒有 P 換框或新增點漏算 |

正式數學輸出在 [OUTPUTS.json](OUTPUTS.json) 凍結後由根 checker 檢查，
前後皆核對 SHA；正常與 seed17 重播及工程結果見 [checks.json](checks.json)。
負控制和既有例外依實際結果記錄；checker PASS 不被當成實際來源存在、
Lean 形式化、或整個縮減任務完成。
