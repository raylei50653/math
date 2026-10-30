# Bernhart 共同端點補證與 r₂ 來源研究紀錄

2026-10-29。當前權威來源為 [RIP 補證及 r₂ 來源報告](../archive/reports/counting/ck_bernhart_endpoint_ray_continuation.md)。
接續 [原 retained 紀錄](2026-10-29-bernhart-retained-parity.md)，未 commit／push。

## 分開驗收

RIP 的原定同一 near-cubic disk／染色／切口範圍內，共同端點分支紙證完成。
正向邊界內域在左；依原 rotation 作推離，或以 canonical 推離加共同負 ε ports 的修正。
原葉使用明定 cap 符號，沒有假裝原葉為 cubic 頂點；同邊兩個邊界端點都計入。

兩份舊 frozen 證書完整重建相等，舊 7,164 份已涵蓋分支重核；
原 local 16 與 wheel／stack 2,992 份未涵蓋分支全部補齊。
四份新共同端點 rotation 負控制均拒絕，marked boundary 收口 genus 0→1；
舊 theta 及非共同端點正負控制保留。一般紙證與固定來源核對分開。

選 r₂，完整 4,923 條 B₈ 方程與 2,187 條 B₆ 方程精確核對。
得到全部來源、全部比例的共同配對、同圖三個共同色 fibres 雙射及合法六葉封口：
一般分支全部 full lift 為 3λ(k,h)，帶同一標記邊的全染色閉圈條件；
free-edge 分支直接刪除得 λ(k,h)。兩分支不拼接，不任意剝掉標記邊或收縮圈。
沒有證明六葉來源不存在，故**射線排除仍 OPEN**，76 列新增必零座標 0。

形式 token 模型在 λ=2 有 522 個共同 tokens，對全部 λ=2m 取標號副本。
核對 10,950 個 path-subset actions、91,206 個同 pair XOR compositions、
18,792 個全域 S₃ compositions、65,700 個 path conjugations 與 3,132 個 loop conjugations。
此為缺少原邊／rotation 的必要條件鬆弛，沒有當作實際來源或真 retained 接線。
y 仍為原 signed-signature 加權計數，沒有套用普通 PM 公式。

## 重播與保存

[驗證收據](../../audits/2026-10-29-bernhart-endpoint-ray/RECEIPT.json)記錄本輪命令、
exit code、輸出與來源 SHA256；[端點證書](../../audits/2026-10-29-bernhart-endpoint-ray/endpoint-parity.json)、
[r₂ 證書](../../audits/2026-10-29-bernhart-endpoint-ray/r2-support-actions.json)各有獨立 checker。
舊來源及舊程式保持原 bytes，重播命令見權威報告。

1,152,369 bytes 的新端點證書追加至既有 ARCHIVE，新增 deterministic gzip 為 31,828 bytes。
只選這一個新路徑；先核所有舊 records 不變，再逐 byte 解壓核對。
正式 docs DocGraph 與全工作樹 DocGraph 分開記錄，不刪歷史凍結副本以消除 duplicate-id。
本輪兩支新 checker、三支前輪重播、文件連結、正式 docs DocGraph 及 `git diff --check` 均通過。
全工作樹 DocGraph 失敗於 72 項歷史 duplicate-id，完整輸出保存在收據連結的 log；
未將該失敗寫成通過。

## 文件治理核對

- Closure scope：只收尾 RIP 原定範圍的共同端點補證；射線、整個殘餘面及可約性皆未收尾。
- Updated：L0 新權威來源、兩支獨立 checker、固定證書及本紀錄；原 retained／跨 split 報告加後續連結。
  L1 核對 4CT／四色工具導覽及 STATUS。L2 直接父整合報告更新已完成子義務與尚缺的標記六葉來源矛盾。
- Reviewed-unchanged：完整共同切口契約、原 76 列／兩射線分解、普通 PM 非函數性與
  `LOCK-NO-GAIN` 範圍不變；主求解器、Lean 及 HANDOFF 活躍標記無改動。
- Remaining OPEN：全部正偶比例實際來源排除、76 列任一新必零座標、全部阻擋排除與可約性。
- Propagation stop：L2。RIP 子引理完成不給父射線排除或 4CT 進一步 closure，無須擴至 L3。

工作樹原有其他未提交研究變更，保持原狀；本次收據不將它們當成本次研究成果。
