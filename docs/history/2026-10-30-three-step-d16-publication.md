# 三步 D16 同源研究的發布核對

2026-10-30。此為 `01e875b` 上的連動研究提交紀錄；來源證據中的 BASE `19f2262`
保留當輪語境，不改成發布前 HEAD。使用者授權 commit＋push。

## 範圍與數學界線

本批包含[跨 split 雙反轉](../archive/reports/planar-sources/four_color_three_step_cross_split_exclusion.md)、
[固定分隔路完整 fibres](../archive/reports/planar-sources/four_color_three_step_separator_fibres.md)、
[全部遠端交換的全割／方向一致路條件](../archive/reports/planar-sources/four_color_three_step_remote_cut.md)、
[原邊 K₄ 附件無增益](../archive/reports/planar-sources/four_color_three_step_attachment_decoration.md)，
及其 producer、獨立 replay、完整證書、凍結來源、導覽與 STATUS。

雙反轉排除限於框外逐分量至多單圈的來源；一般來源的全割／分離條件為必要要求，
未證彼此矛盾。舊鄰點式單獨的來源投影無增益已證；真耳控制的整份指定框列 fibre
通過十二項必要子族仍可在其他框列逃逸。一般 D16 排除、內盤共同延伸存在性與4CT仍 OPEN。
任意大小拓撲／接合／裝飾命題為紙證；數值與原圖控制為 Python，無新增 Lean。

兩份同題 scratch 保留探索來源：SAT 搜尋只用於發現支援正證書，發布後的 replay 不依賴 SAT；
有限封閉 Kempe 類搜尋的負結果沒有被當成一般排除或點數上界。

## 證據保管與歷史版本

[發布 audit](../../audits/2026-10-30-three-step-d16-publication-01e875b/manifest.json)
記錄本批檔案的精確大小與 SHA256，另保存目前四份報告、十一份腳本與探索來源的快照。
各研究 audit 的既有 verification／archive manifest 不覆寫。

v1 separator 的 producer 已由當輪改動反向還原，SHA256 與原 verification 中
`da234a8b923a7076b827312db52f00f3c5a88969b454eff43c91a709f91499b8` 完全相同；
用此精確來源重建 v1 的四份結果 JSON，全部逐 byte 相同。
另外恢復舊 separator 報告，SHA256 為
`b0722891e3c12acea9f34b98d8fd470f24cebaf848e141e91d691f5218acfef9`，
與 cut-support、kempe-escape、separator-v2 三份歷史 archive manifest 相同。
兩份恢復資料另存於發布 audit 的 `source/historical/`，未把舊 hash 改成目前版本。
[恢復核對](../../audits/2026-10-30-three-step-d16-publication-01e875b/historical-recovery.json)保存結果。
v2 是包含遠端鄰點核對的目前完整 separator 證書；v1 保留其先前探索角色。

兩份完整證書超過專案的1 MB門檻，於
[精確例外](../../tools/generated_artifact_exceptions.json)登記 `frozen` 大小／hash：
remote-cut `results.json` 7,148,627 bytes，kempe-escape `results.json` 1,764,708 bytes。
未擴大 checker 的例外規則，也未把完整原點／切口／交換見證縮成邊際摘要。

## 提交前驗證與發布邊界

- 七份獨立 replay 通過，含原 cross-split、separator-v2、cut-support、Kempe escape、
  remote-cut、K₄ 裝飾及真耳控制；本輪另完成 v1 精確來源重建。
- `uv run --with-requirements requirements.txt python -m unittest discover -s tools/tests -p 'test_*.py'`：515 tests 通過。
- 正式文件連結／索引與 docs 範圍 DocGraph 通過；全工作樹 DocGraph 既有72項快照重複 ID
  仍明列為失敗，未刪歷史快照或稱全域通過。
- staged whitespace 與 generated-artifact policy 另於登記本批檔案後核對；
  完整紀錄見[提交檢查](../../audits/2026-10-30-three-step-d16-publication-01e875b/checks.json)。
- 本批沒有修改 Lean，未把先前 `lake build` 或遠端 CI 當成本次紙證驗證。

本紀錄保存提交前結果。push 後另外核對本地 HEAD、追蹤分支與遠端 SHA，
並即時查詢該 SHA 的 CI；push 成功本身不表示 CI 通過。
各研究報告當輪的「未 commit／push」保留為歷史敘述，後續發布由本紀錄銜接。
