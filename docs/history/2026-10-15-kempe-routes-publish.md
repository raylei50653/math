# 四輪具名匹配、完整接回與共同圖整理提交

2026-10-15。依使用者「整理並commit」整合16個隔離audit；研究與提交父BASE為
`6ddea32a81349821ad3724ae1652bddb9c6a7b04`。本次只建立本地提交。
最新權威整合為[第四輪報告](../../audits/2026-10-15-route-round4-6ddea32/REPORT.md)，
目前接續義務由[Kempe導覽](../archive/guides/c5_kempe_guide.md#3-停止點與保留缺口)維護。

## 採納範圍與證據層

| 交付 | 可採納結果 | 保留界線 |
| --- | --- | --- |
| [第一輪](../../audits/2026-10-15-route-research-6ddea32/REPORT.md) | 原T／T0指定邊普通PM雙向分離；固定26列必要表階數恰6、F4精確表示；切割橋接 | 外部Edmonds定理＋紙面推導及有限關係控制；普通PM不保偶補，必要表不是真來源實現 |
| [第二輪](../../audits/2026-10-15-route-round2-6ddea32/REPORT.md) | 同方向PM交換連通、完整奇偶手術；合法J及迫色商圖障礙；720態交換相容性 | 固定方向下降反控制不否決原保XOR義務；抽象交換公理沒有共同原圖 |
| [第三輪](../../audits/2026-10-15-route-round3-6ddea32/REPORT.md) | 保XOR雙環同步交換連通；三邊返回判準；特定720模型單值共同圖不可能 | 46點控制成功只屬固定圖；216態E₁-free閉集仍有72份違完整all-r的E₂ |
| [第四輪](../../audits/2026-10-15-route-round4-6ddea32/REPORT.md) | 來源J四連通、兩星W完整fibres；完整all-r兩禁止事件；三標記普通匹配窄割表；Layer0二層共同圖 | 來源違規lift及偶補正值未證；兩共同圖非平面且只覆18列，不排其他平面實現 |

第四輪完整條件在同一J為`(e=f)⇔(e=g)`，其中e=d(vw)、f=d(pq)、g=d(mz)。
W保留同一份完整染色的全部hub pairs與空fibre，必要條件為
`|Am|=|Az|=2⇒Am=Az`。三標記普通PM失敗只留無非單點分量、一個5割、
兩個5割或一個7割；使用外部Tutte定理的信任界線見該組原PROOF。
這些是任意大小來源的紙面必要推論；局部patch、PM控制與共同圖另屬有限證書。

一般`K≤22=K≤5`、共同k≥23、固定三框點四度支r6⇒k≥25及k≤27⇒h≤12保留。
ω=0、完整319來源排除、r≥7、無界T／T0、一般主命題與完成後保壞嚴格下降仍OPEN。
全部交換在同一圖上；J/W施工完成後回到k+5，不能以刪點代替嚴格下降。
沒有新Lean theorem，`lake build`只檢查既有形式化工程。

## 證據保管與歷史重播

16個原audit的602份可提交檔案保持原位元組，見
[逐檔大小與SHA256](2026-10-15-kempe-routes/audit-custody.json)。
原REPORT中的「未commit／push」保留隔離交付時語境，提交狀態查Git。
BASE、INPUTS、MANIFEST、探測、損壞證書與失敗紀錄均保留。
22份至少1 MB的JSON以精確路徑、大小、SHA256登錄既有artifact例外：
完整fibres、負控制及被後輪封存的副本不得任意壓縮或刪欄。

歷史checker有兩種工作區契約：內容checker核frozen與live authority hashes；
整包checker另鎖BASE HEAD、零tracked diff與當輪目錄白名單。
本輪先在原BASE、共享文件未變時完成重播，再更新摘要。
提交後直接在新主線跑舊整包checker會因工作區契約拒絕，不能改寫原證據來消除此差異。

[凍結BASE重播腳本](2026-10-15-kempe-routes/replay-baseline.sh)建立獨立detached worktree，
按第四輪BASE清單拷入全部16個audit並逐檔核SHA，再執行原round4 bundle。
本輪已實測該流程通過，詳見[整合與detached重播收據](2026-10-15-kempe-routes/route-checks.json)。
後續可在該凍結工作樹執行各報告原命令，無需還原或改寫目前主線文件。

```sh
sh docs/history/2026-10-15-kempe-routes/replay-baseline.sh
```

## 本次驗證

- [來源／關係組](2026-10-15-kempe-routes/source-checks.json)：7個入口各normal／seed17，共14次接受；13份損壞證書均正確拒絕，198份原檔零漂移。
- [Kempe／普通分離組](2026-10-15-kempe-routes/kempe-checks.json)：7次正向、4次損壞拒絕；含兩份共同圖獨立完整染色／原分量重播、AST／本地連結與61檔manifest核對。
- [整合核心](2026-10-15-kempe-routes/route-checks.json)：8次正常接受、4次損壞拒絕；最新bundle及detached BASE bundle均通過，權威與前輪內容零漂移。
- [奇環／批次／三標記](2026-10-15-kempe-routes/matching-checks.json)：3份主證書seed17通過、6份損壞證書均拒絕；三份主證書normal亦已通過。
- `lake build`通過（8832 jobs，保留既有linter warnings）；未重跑Plantri、外部論文完整枚舉或擴大來源界。

文件與儲存規則的最後結果見[提交檢查](2026-10-15-kempe-routes/final-checks.json)。
文件檢查通過（687份Markdown、9007個本地連結），正式docs DocGraph通過
（97 documents、383 relations、0 errors）；artifact policy與使用requirements的94項工具測試通過。
全工作樹DocGraph保留70個duplicate-id錯誤鍵，與detached BASE加相同16份audit比較無新增／消失；
舊ignored audit／scratch宣告路徑差異另記於收據，不視為新凍結證據。
`git diff --cached --check`僅報原xor與three-edge兩份check.py及一份frozen副本的EOF空白；
三份封存原檔保持SHA，docs／policy範圍的cached檢查及unstaged diff檢查均通過。

Updated：16個audit、C4父入口、Kempe／State導覽、STATUS及本整理驗證紀錄。
Reviewed-unchanged：README／HANDOFF仍提供相同研究線入口，活躍標記與一般主命題狀態未變；
no4ct及跨線既有大小界未被新必要條件改變，無需傳播改寫。
Propagation stop：直接父入口與消費者；不把模型障礙或固定圖成功提升成來源排除。
