# 七-cap 接觸排除與兩完整補圈分支整理發布

2026-10-17；研究及提交父 BASE `3d325d7197aa05815c71bedc52c1b253d736c7bb`。
使用者授權「整理目前進展 commit + push」。本次交付研究 audit、Kempe 導覽、
STATUS 與本發布紀錄。研究封存的「未 commit／未 push」保留當輪語境；
實際提交狀態以 Git 為準，不改寫原封存 bytes。

## 採納範圍與下一題

保持同一原全域最少 completed-source、次級最多邊的 no4ct C5 來源，原有序
外框 `(x,y,a,b,c)`、原 x,y,b 四度、r 六度、支持 932/933/941、原 rotation、
私人接觸及完整 U319 fibres（包括空 fibres）、全部五點及 r lifts。
字面 `J=U/(s=t), m=[s=t], D=J*` 和 `e=(vw)*, f=(pq)*, g=(mz)*`
不變。任取實際 M101，假設其補圖有含 f 的非面七圈；無原 v=5 或奇圈最小性前提。
完整前提與論證見[整合報告](../../audits/2026-10-17-r6-two-cycle-cap-3d325d7/REPORT.md)
及[紙證](../../audits/2026-10-17-r6-two-cycle-cap-3d325d7/PROOF.md)。

| 已採納結果 | 精確邊界 |
| --- | --- |
| 任意大小 cap–m 接觸排除 | `N_J(m)∩V(K)={z}`，距離界擴至整個 m-面；不推出 SEP |
| 全參考區域奇偶 | 每區含偶數個補奇圈；恰兩奇圈必同區，可另有偶圈 |
| 恰兩完整補圈 | 全部偶補參考的交換圖皆連通，固定 M 的 `|W_g|=|V(D)|` 為常數 |
| 兩圈 primal 結構 | M* 恰為中心 K2、含 vw 的樹、含 Q5/mz 的單圈分量；唯一圈 Q5 |
| SEP 精確判準 | 同一完整全異染色的實際共同色簡單 z-偶圈，於 z 具指定分隔方向 |
| 指定短圈排除 | p 中心分隔 C4 不能用 zq；c0=5 時長至少六，另一側反射；一般 C4 未排 |

原 R100 **條件下降定理保持正確**。調整的是其後續存在性任務：兩完整補圈
尚未被排除，不能要求固定 M 改參考取得 SEP。優先尋找實際頂點不交的
M-交替圈批次，避 e 並同翻／不翻 f,g，得 N101 或 N110 且全部完整補圈皆偶。
其餘未受全參考阻斷的分支再尋上述同一染色 z-圈，見[Kempe 接續入口](../archive/guides/c5_kempe_guide.md#3-停止點與保留缺口)。

**兩圈匹配修復尚未構造；剩餘 active-f 七圈、其他奇補圈、H 相連殘案、
W110+W101>0、omega_e=0 與完整319仍 OPEN。** 一般 K≤22、固定 r6 的
k≥25、completed-source 接回成本 k+5 不變。無新 Lean theorem。

## 封存與驗證

[發布盤點](2026-10-17-r6-two-cycle-cap-publication/initial-state.json)保存本輪研究
78 份檔案的 bytes／SHA256，包括 13 份 frozen inputs、三路證明與交叉審核、
完整固定圖證書、正常／seed17、污染／覆寫拒絕與失敗收據。
原 79 項研究 seal 包含 77 份研究檔及當輪兩份導覽／索引；seal 本身另被盤點。
兩份 routing 的精確研究版本以 `.md.snapshot` 保留，發布只增 STATUS 的歷史入口。
[發布 custody checker](2026-10-17-r6-two-cycle-cap-publication/check_custody.py)
驗全部研究 bytes、seal、snapshot 與已授權 STATUS 漂移，沒有數學拓撲驗證權威。

[研究驗證紀錄](../../audits/2026-10-17-r6-two-cycle-cap-3d325d7/VERIFICATION.md)
區分任意大小紙證與固定圖校準：七稜柱 28 個偶補參考皆連通；另一個兩奇圈
加一偶圈的 cubic 圖，5 個偶補參考中 1 個交換圖不連通。真正最小來源實現
仍為 **not triggered**；固定控制不證一般匹配修復。
前輪 live custody 的 routing 拒絕與新檔空白檢查首輪工具例外均保留；原 BASE
快照重播、目前研究原 bytes 與修正後檢查分開記錄，不抹去歷史失敗。

發布檢查的實際命令、exit code 及 log SHA256 見
[checks-v2.json](2026-10-17-r6-two-cycle-cap-publication/checks-v2.json)。
首輪文件檢查因當時檢查收據尚未生成而報缺連結，保留在
[checks.json](2026-10-17-r6-two-cycle-cap-publication/checks.json)；收據生成後重播通過。

```sh
python3 -B docs/history/2026-10-17-r6-two-cycle-cap-publication/check_custody.py
python3 -B audits/2026-10-17-r6-two-cycle-cap-3d325d7/check.py
python3 -B audits/2026-10-17-r6-two-cycle-cap-3d325d7/B/check_controls.py
python3 -B scripts/check_docs.py
python3 -B tools/check_generated_artifacts.py
lake build
```

formal／本 audit scoped DocGraph 與 whole-tree 歷史錯誤分開；不重跑舊大型來源
枚舉、九框計數或全樹 DocGraph。`lake build` 只驗既有 Lean 庫。
新檔案皆小於 1 MB，無新產物政策例外。明確 stage 後另驗 Git index 產物政策
及 cached whitespace；研究 custody 在提交前後再核對。

實際發布重播：root／custody 正常及 seed17 一致，兩個污染拒絕符合預期，
原 BASE custody 通過；696 份正式 Markdown／9156 條本地連結、formal／scoped
DocGraph、94 項 CI 工具測試與既有 Lean 庫 8832 jobs 通過。Git index 產物政策
與 cached whitespace 通過；新紙證未因此升為 Lean 形式化。

Updated：本發布紀錄、STATUS 歷史入口及研究時已完成的 Kempe 路由。
Reviewed-unchanged：README／HANDOFF 研究線與 tag、前輪 77 檔、本輪 78 檔
封存、原條件下降定理與一般界。
Propagation stop：父題仍 PARTIAL／OPEN；不提高 closure 或改寫跨線摘要。
