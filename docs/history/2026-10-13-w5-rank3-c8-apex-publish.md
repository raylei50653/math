# W5 圈秩三環繞排除與 C₈ apex 度數整理發布

2026-10-13。使用者授權「整理你的部分 commit + push」。起點為
`45bc1c3dc9dacaee1b10df9d64f1c6a27bb0e954`；只整理本輪兩份研究、相連文件與
封存。Cell 翻邊工具、其文件及共用 STATUS 的對應條目留給原工作。

## 採納範圍

- [W5 圈秩三 essential 排除](../c5_w5_private_rank3_essential.md)：完整最小來源
  若私人圖含分隔 B/U 的環，則圈秩至少四。任意大小完備化約的 1,283 模板
  全 Σ=1023；圈秩三只剩 contractible、7≤r≤11。一般圈秩下界仍為三。
- [C₈ apex 度數](../c5_c8_apex_degree.md)：八項來源契約的 40 個具名 apex-H
  三度子域全排除，原 apex 度數皆至少六，且 h=3⇒k≥14。八項整體仍保留；
  一般 k≥13、h≥3、n₅≥9 不提高，K≤13=K≤5 未證。

紙面完備化約、精確 Python 證書與原來源前提分開。實際最小目錄外來源仍
`not triggered`；零觸發不是排除。沒有新增 Lean theorem，主命題仍 OPEN。

## 本次驗證與保存

兩份原隔離包共 75 個非快取檔案、7,989,838 bytes 保持原樣；原 manifests、
frozen bytes、失敗紀錄及「未 commit」研究截點不改。
依既有封存工具追加三個路徑、三個 gzip blobs，新增 6,288,444 compressed
bytes；舊 2,479 個路徑及 1,543 個 blob records 不變。新 checkout 先依
[封存說明](../../audits/README.md)還原，再執行原 checker。

- 本次重播 W5 主／獨立完整 checker：1,283 模板、13,137,920 cells、730,480 A
  lifts、352,020 G lifts 全一致；原串流 SHA256 不變。
- 本次重播 C₈ 主 checker、獨立支援、兩份精確 dual 及控制，全通過。
  原 39 檔 manifest、七份 BASE Git 輸入均相符。
- 兩包 73 個 manifest payload 與 21 份 frozen 輸入均核對；兩份 manifest
  本身亦列入上述 75 檔保存範圍。
- 本輪研究已執行的 normal／seed17、負控制與 `lake build`（8,831 jobs）結果
  沿用；此次發布不將它們誤稱全部重新執行。新紙面論證未 Lean 化。
- 發布用的文件、儲存政策、Git index 還原及其他檢查，以
  [發布核對](../../audits/2026-10-13-w5-c8-publication-45bc1c3/REPORT.md)為準。
  全工作樹 DocGraph 的 62 個既有 duplicate-ID 失敗保留。

## 文件傳播與提交範圍

Closure scope：W5 essential 圈秩三，以及 C₈ 的具名三度 apex 子域。
Updated：兩份正式入口、W5 父題／五度交付入口、外圈入口、Kempe 導覽、
STATUS、封存入口及本發布紀錄。
Reviewed-unchanged：README／HANDOFF 的研究線與使用方式、上游一般界、
其他研究線；沒有範圍提升。
Remaining OPEN：contractible 圈秩三、圈秩至少四、C₈ 八份更高度數来源、
h≥4 十三內點來源、一般小代表及 K∞=K≤5。
Propagation stop：L2；不將條件來源排除推升父命題。

只提交相連白名單與 STATUS 的相關變更。推送後核對 HEAD、origin/main 與
遠端 main 相等；工作樹可保留上述其他工作，最終狀態由 Git 與本次回覆確認。
