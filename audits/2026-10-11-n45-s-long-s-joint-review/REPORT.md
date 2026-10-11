# N45-S-LONG-S-JOINT：獨立有限校準驗收

日期：2026-10-11。派工 BASE `f2692089ad4259808e27d9b7e882ac09505b180a`。
審查對象：[原 REPORT](../2026-10-11-n45-s-long-s-joint/REPORT.md)、[原 delivery](../2026-10-11-n45-s-long-s-joint/delivery.json)。

**裁決：接受 C 作固定有限介面校準。** 無阻斷缺陷。這項裁決不接受來源全排、來源實現、private-cover 正控制、Lean 或一般 N2/E。
原交付的 pending 欄位保持歷史 bytes；本次裁決另存 [independent-judgment.json](independent-judgment.json)，未修改原 worker、共享文件或舊證書。

## 1. 被驗收的精確交付

- 原 delivery SHA256：`5d73f75f6154863aaf43cf9746757135d3e538c0ec2950e12b3d0de2e213b9ed`。
- 原 certificate SHA256：`e6c48df13be670932f07c4cc9c4a79bb9e5cf58c1121e70cf57c64240d28f9de`。
- 原目錄恰 102 payload regular files／63,167,560 bytes，加精確 8 metadata exclusions；全部 110 regular files，18 directories，無 symlinks、特殊檔或多缺檔。
- 51 frozen/live inputs 對回共同 BASE：50 direct Git blobs、1 exact gzip archive payload。舊 v2 證書 SHA256 `41c3b82ab4afdade42f70b722a2624a9d1a726a4af22f783a09ab32a099b4ed6` 不變。

## 2. 獨立驗證與覆蓋

| 核對 | 實际結果 | 裁決 |
| --- | --- | --- |
| 原 mixed → actual unpinned-s C → C/U → direct X/G | 19 圖、21 eligible 原 spoke 省略、210 列、3,360 ordered pins；全部完整 lift 集合相等 | triggered and holds |
| 完整 X/G lift indices | 獨立原邊回溯重建 11,280 X lifts、8,007 G lifts（row×omission 計數），含 diagonal | triggered and holds |
| assignments、tuples/preimages、ambient fibres | 全 15,960 cells，其中 12,268 空；全部逐項相等 | triggered and holds |
| mixed 接合 provenance、原座標搬運 | 420 mixed records、6,720 mixed pin cells、5,505 C provenance、3,360 root transports | triggered and holds |
| 普通／seed17 只讀重播 | exit 0，stdout byte 相等 | triggered and holds |
| 改壞 C 的 r 色／刪空 ambient cell | 各 exit 1，在指定 value／length 比較階段拒絕 | triggered and holds |
| delivery、凍結／現場 inputs、原交付全檔樹 | payload hashes／sizes 相等，重播前後零漂移，tracked diff 空 | triggered and holds |

[獨立 direct 枚舉](independent_direct.py)與[mixed/provenance 核對](independent_mixed.py)均未 import worker checker 或 prior certificate；使用另寫回溯次序從原邊枚舉。
[獨立 custody 核對](independent_custody.py)直接驗 BASE blobs／archive、檔案型態及完整清單。
[重播紀錄](checks.json)及 `logs/` 保存實際命令、環境、stdout/stderr 與 exits；[replay.py](replay.py)只把新紀錄寫入本 review 目錄。

## 3. 未觸發範圍與信任界

固定 controls 的 t_s=0/1/2 為 0/14/7；singleton S 與非零自由孤立點沒有正控制。
四張有 long＋pair-short 的圖都缺 b4 full B-touch；其餘十五張兩 mixed 都 short。
所有原 G 接受九列，所有 X 接受十列，沒有完整 target Σ=933/941 或其 D5 像，也沒有拒絕 β 的 X-own minimal-witness family。

因此 target source、private-cover 正分支、t_s=0、singleton S、非零孤立點全部維持 **not triggered**。
保存 rotation bytes 不等於驗證 disk topology；原 criticality／one-sided source 義務未由此次工具驗證。
原邊 restriction/union 與恢復 e 的條件集合等式核對無誤；不將它們提升成任意大小來源排除。

本次只驗收 C。A/B 的紙面排除與批次完整覆蓋另行獨立審查。
只新增本 review 目錄；未 commit/push/PR，未更新共享研究狀態。
