# C4 共同 Tait 判準、完整 fibre 返回與六度前緣整理發布

2026-10-14。依使用者「給兩個回覆，整理後 commit + push」授權，兩份回覆
到齊後統一整理 BASE `fdd3e2289254e3f0844e2c595af50080b19f8a05` 後的連接成果。
第 1 份曾依追加指示先整理；其初次「未提交」及其他 audit 的同類文字
保留當輪語境，發布身份、遠端同步與工作樹狀態以即時 Git 為準。

## 採納成果、來源與停止點

| 來源 | 採納的精確成果 | 保留界線 |
| --- | --- | --- |
| [共同 Tait 整理](../../audits/2026-10-14-c4-tait-lock-review-fdd3e22/REPORT.md) | T 的 b 出口及 T0 的兩面色集合問題，以 XOR、球面反積分及共同色框化為指定對偶邊異色；全染色雙環必要條件與偶補完美匹配恰含一邊的等價式 | 正二十面體整個 edge-Kempe 類可鎖定，另一類仍有異色完整染色；五角雙錐全染色鎖定的邊對共享端點。兩控制均非完整最小來源反例；全部染色鎖定的來源排除仍 OPEN |
| [JOINT6 前提](../../audits/2026-10-14-c4-mask13-joint6-fdd3e22/REPORT.md) | ABCB 的 pq 必含缺失色 D，CD／BD 兩個完整 fibre 雙射；六接點必要閉包10→8列。高 p,q 子域的 k≥28 保留 | 八列只是上界，必要閉包不證同圖實現。r 五度 mask7 與其更窄 k≥29 為先前條件推導，現由下一列整支排除 |
| [C4／C5 返回與前緣](../../audits/2026-10-14-c4-c5-recursion-fdd3e22/REPORT.md) | 原 no4ct 全域最小來源、`d_G(x)=d_G(y)=d_G(b)=4` 下，完整 fibre 返回單射證 `d_G(r)≥6`；`r=6` 時再剝除、同圖交換及反射證 `d_G(s),d_G(t)≥6` | r 六度七接點 C5 完整關係只留271／314／319；三份共同整數計數必要模型仍相容，不證來源實現或來源排除。r≥7、原 p/q 五度、一般 T／T0 及全域保壞嚴格下降仍 OPEN |

兩份回覆分别使用對偶 edge-Kempe 雙色環與原圖 vertex-Kempe 分量。
本次沒有假設兩種可達類相同；完整 fibre 的實際交換與對偶全染色匹配判準
各沿用自己的證明及原邊身份。兩支四連通 T／T0 的共同判準也不將原 x,y,b
四度子支的來源排除推廣到任意三角化圖。

活躍七接點 U 指 r 原六度時的 `U=R−r`，外框 `(z,s,v,w,t)`；
[完成契約](../../audits/2026-10-14-c4-c5-recursion-fdd3e22/DESCENT_CONTRACT.md)
另記錄較早 C4 剝除狀態的成本。純刪除再接回仍使完成內點數等於原 k，
識別 a,c 也沒有自動保存 a≠c 部分的完整 C5 關係。
一般 `K≤22=K≤5`／`k≥23` 不變，`K∞=K≤5` 未證；沒有新增 Lean theorem。

## 歷史封存與摘要修正

兩包原 audit 的 MANIFEST、INPUTS、失敗證書及早階段結果均保留原 bytes。
[R6_TRANSFER](../../audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/R6_TRANSFER.md)
最後的「返回單射仍 OPEN」是較早停止點；當前採納以
[最終 REPORT](../../audits/2026-10-14-c4-c5-recursion-fdd3e22/REPORT.md)與
[返回證明](../../audits/2026-10-14-c4-c5-recursion-fdd3e22/fibre/PROOF.md)為準。
原 JOINT6 的 r 五度／k≥29 子域同樣保留先前語境，不再列作活躍殘題。

Updated：C4 權威入口、Kempe 導覽、STATUS、no4ct 直接 consumer、synthesis 的 C4 列。
共同 Tait 判準與最新度數排除均連向各自完整來源；STATUS 過時的 r 五度摘要已修正。
Reviewed-unchanged：HANDOFF 研究線／tags、README 路由、其他研究線及一般大小界。
Propagation stop：直接父主題與使用舊 r 五度 OPEN 語義的 consumers；未擴大來源契約。

## 本次實際重播與發布檢查

JOINT6 的四份主控制正常／seed17 共八次及獨立完整染色控制，返回／前緣的
五份主控制正常／seed17 共十次，全部 PASS；各次命令、exit code 及 log 保存於
[JOINT6 receipts](../../audits/2026-10-14-c4-results-publication/joint6/receipts.json)、
[返回／前緣 receipts](../../audits/2026-10-14-c4-results-publication/recursion/receipts.json)。
所有 `--check` 均為唯讀，未重生成或覆寫既有證書。

- JOINT6 重播核對七張明列圖42份完整固定框染色、14份完整集合雙射，
  216→168標號列、10→8固定框列、四個可選邊域的128子關係及原接點幾何。
- 返回／前緣重播核對三張真圖完整 fibres、504份三度指派、16,384份 r 六度指派、
  一般／重合兩支全部 t/r lifts、542／575／63上界及共同整數計數；負控制沿用各 checker。
- Tait 控制原程式及獨立匹配普通／seed17 PASS，後兩次 stdout 逐 byte 相同。
  正二十面體36匹配／30偶補，五角雙錐11匹配／10偶補，全部540邊對等價式及
  72／144局部 XOR 指派通過；正二十面體有16個匹配恰含一條指定邊。
  刪除一個偶補匹配的破損證書被拒絕；詳見 [Tait 驗證](../../audits/2026-10-14-c4-tait-lock-review-fdd3e22/VERIFICATION.md)。
- 兩包 MANIFEST 分別74／137個檔案及各16個 frozen INPUTS 全數一致；
  live drift 只出現在有後續更新的路由文件，數學輸入零漂移。
  [保存核對](../../audits/2026-10-14-c4-results-publication/verify_input_manifests.py)及
  [本輪結果](../../audits/2026-10-14-c4-results-publication/recursion/input-manifests.stdout.log)可查。
  兩包均無 SEAL.json，不把 MANIFEST 核對稱作另一份 seal 通過。
- `lake build --no-ansi` PASS，8,832 jobs；沿用既有 linter warnings。
  本地 build 不代表本次紙面拓撲／XOR／匹配證明已形式化。

最終發布檢查：

- 文件檢查 PASS：684 份 Markdown、8,913 個本地連結，索引、anchors、HANDOFF
  及導覽現況卡通過；正式 docs DocGraph PASS：97 文件、379 relations、12 families。
- 全樹 DocGraph 仍 FAIL：70 項 retained frozen／scratch duplicate ID；本輪完整輸出
  已保存在 Tait 整理包，未刪除歷史證據，也不將正式 docs PASS 稱作全樹 PASS。
- stage 後的 `python3 tools/check_generated_artifacts.py` PASS：5,024 indexed files，
  8 個原有明列例外的大檔、166 registered outputs；本次所有新增 JSON 均小於1 MB。
  `git diff --cached --check` PASS；不需追加 archive，舊 ARCHIVE 及 blobs 保持原身份。
- 發布前 fetch 及 remote main 均為 BASE，沒有未處理分歧；此次僅提交已列白名單。
  commit／push 後另以 `HEAD=origin/main=remote main` 及 clean worktree 核對完成。

未重跑外部≤28點完整枚舉、plantri、大型無關生成器或其他已完成來源分類。
發布白名單只含三份相接 audit、這次保存／replay logs、上述直接文件及本紀錄。
