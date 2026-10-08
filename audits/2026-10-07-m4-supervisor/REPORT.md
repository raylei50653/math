# M4-L 監督驗收與 M4-R 派工

**M4-L 本地驗收通過，限已記錄具名例外。尚未達到合併條件。**
受驗最終提交為 `1f21c8f09dfcb5110ea1a3d66399e9c0a54ceeaf`，
直接 parent 為 `ba0b447f09617591d9f2ba81c988f537af771791`。
main 比較基準仍為 `2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090`；
本次未連線核對 remote，不以本地 tracking refs 宣告遠端狀態。

| 階段 | 監督狀態 |
| --- | --- |
| M1 | 本地候選已驗收；兩份原檔追回，其餘原缺失證據保留不可用界線 |
| M2 | 指定 U1 條件論證與完整有限域已驗收，保留上游信任及正控制未觸發界線 |
| M3 | 計算／顯式 LC／公理與補件已驗收，五份 strict FAIL 不改成 PASS |
| M4-L | 本地最終提交與正式證據包驗收通過，沿用具名例外 |
| M4-R | 已可發布；PR、即時遠端 head/base、對應 CI 待回報 |
| 合併 | 待 M4-R 驗收與使用者另行明確指示 |

本次 [獨立核對程式](verify_delivery.py)核對 572 份 seal entries 與 seal 自身，
共 573 份工作區 bytes 逐份等於最終 Git blobs；清單恰等於 candidate→final 的全部路徑。
交付總大小 26,469,605 bytes，原 M2／M3／監督 328 檔及其 manifest 零漂移。
candidate→final 為 573 檔、154,704 行新增；相對 main 為 1,618 檔、
1,985,529 行新增／70 行刪除。這是整個整合分支的差異，PR 說明須覆蓋整分支。

最終 `/tmp` 驗證包的 128 份 inventory entries、自身 inventory、
56 份 raw/gzip log hashes、command exits、exact final SHA 與 tree 均核對。
全部 129 檔已逐 byte 保存於 [final-receipt](acceptance/final-receipt/FINAL_RECEIPT.json)，
其中仍保留歷史路徑及驗證途中尚 pending 的 integrity-review；完成狀態以其後的
FINAL_RECEIPT 與 review/verification.json 為準，不回寫歷史字句。
本次結果見 [review.json](acceptance/review.json)。

監督端另在原 scratch-free 獨立 checkout 重跑 `scripts/check_docs.py`（exit0：
573 Markdown、6,714 local links、anchors/index/handoff）與預設
`tools/docgraph check`（exit0：62 documents、213 relations、5 families、0 errors）。
工作區 seal `--check` exit0；17 份交付 Python 逐 hash 核對並 AST parse 通過。
原 final receipt 中 63 個有效 audit links 重新核對存在，六個已揭露歷史缺失連結保留。

五份 fresh／saved JSON 完整遞迴比較，只存在原具名 presence／metadata／文件 hash
leaves；本輪 guide 的 E4C hash 確為最終 bytes。strict exit1 全部保留。
原指定 29 命令仍為 28 PASS／1 FAIL；另外四項 strict FAIL 不混入「全 PASS」。
`git diff --check candidate final` exit2，85 項全部位於匯入的原 whitespace log；
`git diff --check main final` exit2，合計原 86＋匯入 85＝171，逐路徑／行號／message
等於分項清單。新 authored 診斷 0；不是整份 diff whitespace PASS。

109 份 Lean 來源／設定／生成證書 hash 與 M3 一致；監督端重新解析原公理 log，
[558 項完整結果](acceptance/axioms-supervisor-reparsed.json)與 M3 JSON 全等，
無 sorryAx／unexpected axioms、179 positive 無 native。
本次沒有重跑 build／Lean 公理程序。Rejected／valid 與 raw Sigma 的 native 信任仍保留；
原 `.olean` inventory 不可用，不聲稱 cache 相同。
U2–U4、E5 新證明、三列推廣、epsilon>=3 及一般數學缺口仍在；
它們是此部分成果 PR 的範圍界線，不藉本次驗收關閉。

下一步按 [M4-R 派工](M4_REMOTE.md)發布相同 final SHA，
可使用 [PR 說明草稿](PR_BODY.md)。此新監督包是提交後旁掛證據，未納入
1f21c8f0 的 seal／commit；原三包及 M4-L 正式包均未修改。
發布任務不需將本監督包重新 commit，以免改變已驗收 head。
本次沒有 push／PR／CI dispatch／merge，也未宣告可合併。
