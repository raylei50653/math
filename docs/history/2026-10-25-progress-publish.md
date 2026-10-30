# 目前進展分組提交與遠端整合

2026-10-25。依本次「整理目前進展並分別commit + push」整理已有成果，不啟動新研究。

## 分組結果

| 提交 | 內容與精確邊界 |
| --- | --- |
| `9bff346` | [四色求解與共同約束實驗](../tools/four_color_guide.md)：求解器／播放器、十一報告及凍結證據整包；十二點例8→0消元，九點例仍4；無一般傳播完備性或新Lean。 |
| `8a3a6bc` | [941 K8同一外側接續](2026-10-25-941-k8-publish.md)：隔一型116→115，21 cap總1710→1704；七列無新增排除、明列替換庫新覆蓋零，同一實際E與K8整支OPEN。 |
| `ee42fab` | [六份圓盤三角化與逐面編號](../tools/solver/triangle_structure.md)：原圖嵌入／身份／有限染色數與只讀checker；歷史72次擾動缺重播來源，不稱本次重跑。 |

本地原有四項提交`b6b3c2c`、`02356f8`、`698fcf8`、`494208f`保留原SHA，一併發布。
它們分別是三支等價表述、大k有限隨機搜尋、P1–P4任務登記及前提／失敗審核更正；
不因發布啟動P1–P4，也不把零命中當覆蓋定理。

fetch發現遠端另有四項4CT文件提交，最新`b59982a`；以merge保留雙方歷史，沒有改寫任何sealed BASE。
README沿用遠端主目標；HANDOFF只保4CT為進行中，保留其他研究線並接上實驗導覽。
STATUS合併主目標及本次直接來源索引；4CT導覽只增有限工具入口，明示未完成可約性／新意里程碑。
衝突只涉及HANDOFF排程及STATUS頁首，實驗與941數學證據皆未受改寫。

## 核對與後續

[本次檢查收據](2026-10-25-progress-publication/checks.json)分開記本次現場檢查、先前在同一turn完成且程式未改的驗證，以及未重跑範圍。
265項工具測試、Lean 8832 jobs、既有等價形式checker、三個941完整checker、六例三角化只讀checker均通過。
四色後續證據另核105來源快照及268份壓縮記錄；[原收據與歷史漂移界線](2026-10-25-four-color-lab-publish.md)保留。
合併只改docs，未重跑未變的整套工具測試或Lean；正式docs／DocGraph、artifact政策與whitespace作最後核對。
全工作樹DocGraph的72個歷史重複ID錯誤另記，不改稱全域通過。

推送後以即時`HEAD`、`origin/main`、`git ls-remote origin refs/heads/main`核SHA及乾淨工作樹；
遠端CI另查實際執行狀態，push成功不代表CI成功。本檔在推送前提交，不預稱遠端結果。
目前研究目標及下一義務分別由[4CT](../research/4ct_guide.md)、[四色實驗](../tools/four_color_guide.md)及[Kempe](../archive/guides/c5_kempe_guide.md)導覽維護。
