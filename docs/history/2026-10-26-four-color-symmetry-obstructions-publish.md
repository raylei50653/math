# 按需換色快取與無解必要結構整理發布

2026-10-26。從基準 `b783475a1cc24ff126c09ad276816a3b7eb4e8d8` 整理兩組相連成果：
按需子樹換色快取，以及最小無解核心／小邊割必要條件。
目前研究入口為[四色求解導覽](../four_color_guide.md)及[4CT導覽](../4ct_guide.md)。
提交、push與遠端CI狀態以即時Git／GitHub為準，本頁保存發布範圍與本地驗證。

## 成果及適用範圍

| 工作 | 結果與來源 | 保留邊界 |
| --- | --- | --- |
| 按需子樹換色快取 | [完整契約與對照](../four_color_local_symmetry.md)：保留整個子樹有效域的共同換色共用完整接口答案，最後逆換色回填。23點控制checks由3,220,975降至241,431；同預設預算由訊息超限變為精確無解。 | 可選 `color_symmetry=True`，歷史字面模式仍為預設。9×10格圖成本增4.4%，無一般加速；單一見證API沒有替換主引擎完整fibres。 |
| 最小無解核心 | [原圖證書](../four_color_critical_obstructions.md)：六圖、39份刪點與105份刪邊判定，保存300份同染色雙色路。23點例的71條邊皆不可刪，213份五圈見證去重為127圈。 | 三路定理要求裸四色與該邊刪除可染；頂點最小不能替代邊最小，一份被鎖住的染色不能替代全稱量詞。 |
| 小邊割必要條件 | 同報告以完整兩側染色共同換色及收縮證明：假設裸平面最小反例存在，兩側各至少兩點至少需六條跨邊；五邊割只能孤立一個五度點。 | 需要全體裸平面反例的頂點最小性，不需每邊不可刪。2857組至多五邊色型配對全核，六邊僅一份2×3具名控制；沒有一般六邊分類、932排除或新可約性證書。 |

子樹快取的17份具名條件三模式皆核對獨立原邊判定；其中14份逐答覆核完整接口表，
其餘三份寬接口例只核最終判定、原圖見證、分解及訊息協定。
本次一般及seed-17重播輸出均寫至 `/tmp`，沒有覆寫原報告或計時紀錄。

## 來源保管

原始兩包及各自verification收據保持原bytes：

- [換色快取稽核與凍結來源](../../audits/2026-10-26-four-color-local-symmetry-b783475/)
- [最小核心與換色表稽核](../../audits/2026-10-26-four-color-critical-obstructions-b783475/)

換色快取的舊收據綁定當時的STATUS及四色導覽；後續必要結構研究改了這兩份文件。
本次補存[當時STATUS](2026-10-26-four-color-symmetry-obstructions-publication/pre-critical-docs/STATUS.md.txt)
及[當時四色導覽](2026-10-26-four-color-symmetry-obstructions-publication/pre-critical-docs/four_color_guide.md.txt)，
兩份SHA逐一命中原收據，沒有把後來文件的hash寫回舊收據。
本次發布前的七份文件另存於[發布前快照](2026-10-26-four-color-symmetry-obstructions-publication/pre-publication-docs/)，
供必要結構收據及此次新增STATUS發布連結前的文件hash核對。
[來源核對](2026-10-26-four-color-symmetry-obstructions-publication/custody.json)
分開記錄目前來源、凍結依賴、歷史文件及本次發布文件，不要求它們混成同一版本。

## 本次發布驗證

[Python 3.14工具測試](2026-10-26-four-color-symmetry-obstructions-publication/tool-tests-python314.log)
共416項通過；使用已快取環境，Python 3.14.8與CI相同的主次版本，
依賴逐一核對 `networkx==3.5`、`numpy==2.4.3`、`rustworkx==0.17.1`。
同套測試另在Python 3.13.13通過，環境與實際命令分別存於同目錄JSON，不混稱兩次同一執行。

[重播紀錄](2026-10-26-four-color-symmetry-obstructions-publication/replays.json)
包括換色目前來源一般重播、凍結來源seed-17，以及核心／cut兩程式各自一般與seed-17，
六次確定性輸出均逐位元組符合原報告。
文件、docs-only DocGraph、實際Git index產物政策與提交空白檢查另見
[本次檢查收據](2026-10-26-four-color-symmetry-obstructions-publication/checks.json)。
未修改Lean，未執行Lean build或全工作樹DocGraph；docs-only通過不代表全域DocGraph通過。
push後另核本機、tracking、遠端分支SHA與clean狀態，遠端CI與push結果分開回報。

## 收尾範圍

這批完成指定功能、必要條件論證與有限驗證，不是4CT收尾。
一般加速、自動啟用準則、六跨邊真實平面來源限制、932、一般可約性與不可避免性仍OPEN。
L0報告／證據與L1導覽／STATUS已同步；4CT直接消費者只補必要結構，不改其OPEN。
README／HANDOFF核對後不改，研究線與排程未變，文件傳遞止於直接消費者。
