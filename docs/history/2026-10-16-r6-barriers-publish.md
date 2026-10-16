# r6 聯合零值與 Tutte 障礙整理發布

2026-10-16。依使用者「整理目前進展commit + push」整合三個連續 audit。
研究與提交父 BASE 為 `c4c3d99c59cfe4f85b3e33f6831da955a8efcbc7`。
最新權威來源為 [R6-CHORDED-FIVE](../../audits/2026-10-16-r6-chorded-five-c4c3d99/REPORT.md)，
接續義務由 [Kempe 導覽](../c5_kempe_guide.md#3-停止點與保留缺口)維護。

## 採納範圍

沿用同一原 no4ct 全域最小目錄外 C5 來源、次級最大邊數、
三框點 x、y、b 四度、r 六度，以及實際 `J=U/(s=t)`、球面對偶 `D=J*`。
三標記保持 `e=(vw)*, f=(pq)*, g=(mz)*`；110 強制 e、f 並禁止 g，
101 強制 e、g 並禁止 f。完整前提、原接線與量詞以各組 PROOF 為準。

| 交付 | 任意大小紙面結果 | 保留界線 |
| --- | --- | --- |
| [R6-JOINT-ZERO](../../audits/2026-10-16-r6-joint-zero-c4c3d99/REPORT.md) | 兩族全單點 Tutte 障礙排除；原奇補圈與 C4 扇區定位 | 普通匹配存在及偶補終點均未由此取得 |
| [R6-CAP-BARRIERS](../../audits/2026-10-16-r6-cap-barriers-c4c3d99/REPORT.md) | 唯一非單點為 W5／完整 W7 的障礙排除；雙 W5 精確曲率剛性及共同 111 跨割飽和 | 雙 W5 仍可能；其原 s、t≤8、h≤6 僅限該子類 |
| [R6-CHORDED-FIVE](../../audits/2026-10-16-r6-chorded-five-c4c3d99/REPORT.md) | 101 每個五割分量均為 W5，單一五割整列排除 | 101 普通失敗仍留雙 W5／非輪七割；110 其餘割未排 |

紙面證明與有限 checker 分開：控制保留原圖、全部 fibres、空 matching
fibres 及負控制，但真正最小來源數值測試仍是 **not triggered**。
CHORDED-FIVE 原 REVIEW 是同一 agent 的第二次覆核，不是獨立 agent 或形式驗證。
本次另核對三份報告與導覽的一致性；沒有新增外部定理或 Lean theorem。

`W110+W101>0`、聯合普通族非空、偶補正值、完整 319 排除、r≥7、
一般 T／T0、完整 720 態平面 cover 及 `K∞=K≤5` 仍 OPEN。
一般 `K≤22=K≤5`、固定三框點四度 r6 支 `k≥25` 及完成來源成本 `k+5` 均不變。

## 證據保管與重播

三個 audit 共 424 份原檔、57,363,222 bytes 保持原位元組，
見[逐檔大小與 SHA256](2026-10-16-r6-barriers/audit-custody.json)。
其中 12 份大型 JSON 是已封存權威與損壞證書副本，按精確路徑、大小、SHA256
登錄 artifact 例外，保存原完整 fibres 與失敗紀錄。
原 REPORT 的「未 commit／push」保留隔離交付時語境；發布狀態以 Git 為準。

原整包 checker 鎖定 BASE HEAD、當輪 routing 或 tracked diff 白名單。
JOINT-ZERO 的 routing seal 已被後兩輪合法更新，因此目前主線直接重播
該舊 bundle 會拒絕；CAP／CHORDED 在本次整理改動前通過。
提交後應在 detached BASE 還原相應 routing，再執行整包檢查，
不改寫原 MANIFEST 或放寬原 checker。

[凍結 BASE 重播腳本](2026-10-16-r6-barriers/replay_base_bundles.py)會建立臨時
detached worktree、拷入三個 audit、重播 CAP／CHORDED，再以後輪封存的
四份精確 routing snapshots 還原 JOINT seal，完成後移除該臨時 worktree。
本次已實測三包皆通過，見[整包收據](2026-10-16-r6-barriers/audit-replays/baseline/baseline-bundle-replay.json)。

```sh
python3 -B docs/history/2026-10-16-r6-barriers/replay_base_bundles.py
```

## 本次驗證與文件傳播

- [證書重播](2026-10-16-r6-barriers/audit-replays/certificate-replay-summary.json)：
  7 個入口各 normal／seed17，共 14 次通過；7 組輸出一致。
  10 份損壞證書與 6 次 exclusive-create 負控制均正確拒絕，424 份原檔零漂移。
- [工程與文件圖收據](2026-10-16-r6-barriers/global-checks/CONTEXT.json)：
  `lake build` 通過（8832 jobs，既有 linter warnings），工具測試 94 項通過；
  正式 docs DocGraph 通過（97 documents、383 relations、0 errors）。
- [全樹 DocGraph 比較](2026-10-16-r6-barriers/global-checks/docgraph-comparison.json)：
  保留 70 個歷史 duplicate-id 錯誤鍵，與 detached BASE 及 BASE 加相同三個
  audit 完全一致，無新增錯誤鍵；沒有改寫 frozen IDs。
- [提交檢查](2026-10-16-r6-barriers/submission-checks.json)：文件連結、artifact
  policy、導覽／policy／發布文件的 staged whitespace 與 unstaged whitespace 通過。
  全部 staged 檔案的 whitespace 檢查僅報三份原 frozen checker 的 EOF 空白；
  保留原 SHA256，不改寫封存證據。

各組實際命令、退出碼與 stdout／stderr 均保存在上述收據旁。
`lake build` 只驗證既有形式化工程；未重跑外部完整枚舉、Plantri 或擴大來源界。

Updated：三份原 audit、C4 父入口、Kempe／State 導覽、STATUS 的完整索引、
精確大型檔例外與本發布紀錄。STATUS 補齊最後一輪直接索引，並標明前輪殘留的後續涵蓋。
Reviewed-unchanged：README／HANDOFF 維持相同研究入口及活躍標記；
no4ct、跨線來源大小界與一般主命題狀態未變。
Remaining OPEN：上述聯合普通非空、偶補正值與完整來源排除。
Propagation stop：直接父入口與消費者；子類排除未改變一般主命題。
