# 2026-10-07：C44″ 整合覆核與分支收尾

使用者要求「繼續推進或收尾分支」。接手 `integrate-kprime-e3 @ c9f89f0`，
已有11個未推送提交，工作樹只有既有未追蹤 `scratch/`。
發現 `task-c44pp-coverage @ a1ca89d` 已交付
[C44″ 覆蓋表](../../artifacts/c5_excess_two_c44pp/REPORT.md)，故選擇覆核並收尾該窄任務。
以 `git merge --ff-only task-c44pp-coverage` 接入既有提交，沒有建立新提交或推送。
整合後入口與覆核修訂留在工作樹；即時提交／遠端狀態以 Git 為準。

## 覆核範圍與成果

相鄰、非相鄰分支分開唯讀核對原報告的前提、省略身份、來源排除及具名例。
這是引用與分類記帳的覆核，不取代舊系列全部紙面化約的獨立稽核。

| 核對項 | 結果與出處 |
| --- | --- |
| 完整 Σ 的相鄰 m=1 | [spokes](../c5_excess_two_mixed_core_spokes.md) 身份表，加 [spoke＋unary](../c5_excess_two_mixed_core_spoke_unary.md)、[雙 unary](../c5_excess_two_mixed_core_two_unary.md)、[mixed 省略](../c5_excess_two_mixed_omission.md)，已有兩-root44全排；不依賴K′。 |
| E5 的 G1 任務邊界 | [E5 §2](../../artifacts/c5_excess_two_e5/REPORT.md#2-依賴項-×-分支狀態表)明說精確941／933角色滿足舊輸入，保留G1是要求新證明；更正C44″把這些缺口只歸因於三列前提的措辭。既有覆蓋不完成那項新證明。 |
| U1 no-mixed 記帳 | [全degree-4分類](../c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)給core內部最大度≤3；保留unary、刪spoke的root有內度5−t_r，故t_r≥2。結合[E6-D](../../artifacts/c5_excess_two_e6/REPORT.md#4-e6-dno-mixed-的整側預算與精確殘留)，雙spoke身份縮為(2,2)，spoke＋unary為(2,3)含交換，三spoke側僅941／013型。沒有排除來源。 |
| U2 相鄰 m=2 | [E6 §3](../../artifacts/c5_excess_two_e6/REPORT.md#3-e6-bcj6-的共同-core欄位與框邊預算)給恰省略一份mixed11、保留另一份共用contact；現有結果未排此身份。 |
| U3／U4 非相鄰 | [E4](../../artifacts/c5_excess_two_e4/REPORT.md)的N1 incidence11／12／21與N2五族保留；補入[CORE_CONSTRAINTS §4](../../artifacts/c5_excess_two_e4/CORE_CONSTRAINTS.md#4-三列-private-spoke-和-n2-精確-qcore-身份)的024／124禁型及N2的44拒絕列兩側spokes不得重色。 |
| 具名 AD-012-034 core | [C44](../../artifacts/c5_excess_two_c44/REPORT.md)、[C44′](../../artifacts/c5_excess_two_c44p/REPORT.md)的core邊／附件與軌道相符；更正「C44P-AD2沒有來源」為「未提供完整Σ933／941的來源構造」。兩-root44與單-root讀法分開。 |
| root 刪除與控制 | [原root刪除](../c5_excess_two_root_deletions.md)及E4的N1單-root例外保持；[E4C](../../artifacts/c5_excess_two_e4c/REPORT.md)沒有44／root-deletion觸發控制，[D₉](../../audits/2026-10-06-task-d9/REPORT.md)的63圖均未觸發指定三拒絕列，不能提升為来源排除的實验驗證。 |

沒有發現使既有排除失效的前提錯置。修訂的是任務範圍措辭與既有必要限制，
沒有新來源排除、Python證書、Lean theorem或來源實現構造。
完整Σ933／941的兩-root44仍有U1–U4；其他core degrees與三列推廣殘留保留。
ε≥3、猜想E任意大小、一般出口與K∞=K≤5未證。

## 文件整合與實際驗證

更新C44″報告、Kempe導覽、STATUS直接索引及README的入口說明；
HANDOFF的研究線與tag未變，依[文件治理](../DOCUMENTATION.md)保持薄索引。
舊報告、歷史證書、稽核輸出與scratch副本均未改寫。

| 本輪檢查 | 結果／範圍 |
| --- | --- |
| `python3 scripts/check_docs.py` | 整合前PASS；整合後569份Markdown、6661個本地連結及anchors／index／HANDOFF檢查PASS。 |
| `python3 tools/docgraph check` | 接手即FAIL：scratch/task-c44-delivery/repository副本造成62個duplicate-id；這是既有scratch副本干擾，未刪或移動該副本。 |
| `python3 tools/docgraph --include 'docs/**/*.md' check` | 正式docs metadata：62 documents、213 relations、5 families，PASS；未宣稱預設全工作樹命令通過。 |
| `git diff --check`；新紀錄另查whitespace | tracked修訂exit0；新紀錄的no-index檢查exit1、無whitespace診斷（有新增diff），另以標準函式庫檢查每行無尾空白且檔尾有換行，exit0。不取代舊整分支vendor／log紀錄。 |

本輪為紙面覆蓋表與文件整理，未重播研究producer、ES／ER搜尋或舊稽核，
未執行lake build；數學證據仍沿用各原報告明列的紙面／有限證書信任邊界。
目前停止點與未啟動窄提議由[Kempe導覽](../c5_kempe_guide.md#3-停止點與保留缺口)維護。
