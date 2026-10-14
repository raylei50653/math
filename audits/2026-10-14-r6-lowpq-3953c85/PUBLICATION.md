# 本輪成果的主線發布

2026-10-14。依使用者的 commit + push 指示，從隔離工作樹
`/home/ray/developer/ai/math-r6-lowpq-3953c85` 整合到正式主線。
發布父提交為 `664c9378c6333d07810763f4f00a5c143a111f82`；
研究的凍結 BASE 仍是 `3953c85e334b96533e44652df065640f5463715a`。

## 原始證據與整合範圍

原 [REPORT](REPORT.md)、[VERIFICATION](VERIFICATION.md)、全部證明、
證書、負控制、失敗紀錄、frozen inputs 及 MANIFEST 保持原位元組。
其中「未 commit／push」描述原隔離研究交付時的狀態；後續發布以本紀錄
及即時 Git 為準，不改寫歷史驗證。

原 MANIFEST 另含五份隔離工作樹的文件草稿 seal；正式文件加入父提交的
有限枚舉入口後不再逐字等於該草稿。原草稿由凍結 BASE 加
`publication/isolated-docs.diff.gz` 可還原，全部92項原 seal 已逐份核對，見
[原交付保管紀錄](publication/manifest-custody.json)。

只整合本 audit 與五份直接文件：STATUS、C4 父入口、Kempe 導覽、
no4ct handoff 及 research synthesis。README／HANDOFF 的路由經核對仍適用。
正式摘要明示 `r=6,p=5` 得 ell-v、ell-w 原非邊，q=5 側取整份來源反射的
對應結論；兩份指定完整 fibre 聯集各自非空，不能合併成同一染色。

父提交已發布的[獨立 r6 有限枚舉](../2026-10-14-r6-319-enumeration-676b102/REPORT.md)
在同一固定 x,y,b 四度最小來源契約內排除 k=23、24，給 r6⇒k≥25。
本輪任意大小幾何界另給 k≥ceil((3h+16)/2)，所以 k≤27⇒h≤12。
兩項取交集後，k≤27 的 r6 僅留 25≤k≤27；933／941 的 h 域為4…12，932為5…12。
一般 K≤22／k≥23、高 p,q 的條件界、完整 mask319、無界來源及 Lean 界線仍保留。

## 發布驗證

發布時重播結果記於 [publication checks](publication/checks.json)。
原來源 custody、正常／seed17 色表與計數重播、負控制、獨立原邊核算、
正式文件與儲存規則均在主線整合後核對；whole-tree DocGraph 與發布前
主線的錯誤鍵分開比較。既有 Lean 工程 build 已通過，沒有新增 Lean theorem。
本次未重跑 plantri、大型來源生成或外部論文計算。
文件連結檢查針對現有主工作樹，包含已還原的歷史 archive 及原有 ignored
的 local-only 歷史參照；這些檔案的界線見原 VERIFICATION，沒有宣稱
未補齊歷史檔案的新 checkout 已通過全部連結檢查。

提交與推送 SHA 以 `git log -- audits/2026-10-14-r6-lowpq-3953c85/PUBLICATION.md`
及遠端 main 為準；推送後核對 HEAD、origin/main、remote main 與正式工作樹狀態。
