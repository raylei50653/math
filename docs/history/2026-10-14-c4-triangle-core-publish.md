# C4 四連通化約與 mask13 六接點殘題整理發布

2026-10-14。依使用者「整理後 commit + push」授權，整理 BASE
`b66f592167bf7c3fab0ed89e57b092e49877be15` 後的 C4 連接成果。
原 audit 的「未 commit／push」保留研究完成當時語境；本紀錄保存本次發布
範圍及驗證，實際提交與遠端同步以即時 Git 為準。

## 成果與精確停止點

[權威入口](../c5_c4_triangle_core.md)與[原報告](../../audits/2026-10-14-c4-triangle-core-b66f592/REPORT.md)
保留 no4ct 全域最小來源、原圖接線與 rotation、全部空 fibres 及共同色名。
一般來源經指定同色點識別，化約為四連通 T 的固定三角指定 b 出口，或
四連通 T0 的兩個指定三角面能否在同一份完整染色中使用不同色集合。

更窄的[相鄰四度化約](../../audits/2026-10-14-c4-triangle-core-b66f592/ADJACENT4.md)
只在原 `d_G(b0)=d_G(b1)=d_G(b3)=4` 且目標延拓失敗的子支成立：
刪 x,y 的 R 有 `k−3<k` 內點，七種相對 C4 關係經完整 cap 接回與
`k−2<k` 的相對可染性縮至唯一 mask13，沒有引用普遍四色定理。

mask13 尚未排除。精確殘題保留六個原接點 `(z,s,r,t,p,q)`：每份 ABAB
完整染色迫 pq 色集合為 `{C,D}`，每份 ABCD 完整染色迫為 `{B,D}`。
須以同份 full lift 打破共同強迫，四框關係或不同染色的投影不能代替。
抽象六接點反控制保留，未宣稱其來源可實現。

獨立紙面覆核見[審查 §8](../../audits/2026-10-14-c4-triangle-core-b66f592/review/INDEPENDENT.md)。
紙面任意大小結構化約與 Python 有限控制分開；真正目標來源控制為零，
沒有新增 Lean theorem。`K≤22=K≤5`、共同 `k≥23` 不變，mask13、一般
T／T0 延拓、932／933／941 無界來源排除及 `K∞=K≤5` 均仍 OPEN。

## 本次實際重播與證據保存

正常及 `PYTHONHASHSEED=17` 各自重播 quotient、structure v2、cap；
另重播 negative。七份完整輸出、精確命令與 exit code 保存在
[replay receipts](../../audits/2026-10-14-c4-triangle-core-publication-b66f592/replays/receipts.json)。

- 完整 fibres：132 圖、264 份集合等式、547 份 T lifts，H 的 56 個及 T 的
  120 個空格保留；正常／seed17 均 PASS。
- 結構 v2：192 份球面控制、157 份符合 S6，10,895 個開口，其中 T 4,891、
  T0 6,004；缺交叉邊及 vertex link 單環檢查通過。初版 validator 及
  pinched surface 負控制的原 bytes 保留。
- Cap：完整局部延拓數 `(2,3,0,1)`、24 份有序 pq 指派、七關係縮至 mask13
  及抽象共同關係負控制通過。
- Negative：五項竄改／非 surface 控制均拒絕，受保護的三份 SHA 前後不變。
- [Lean build](../../audits/2026-10-14-c4-triangle-core-publication-b66f592/validation/lake-build.receipt.json)：
  `lake build --no-ansi` exit 0，8,832 jobs；既有 linter warnings 保留。
  此結果不表示新紙面化約已 Lean 化。
- [Archive verify](../../audits/2026-10-14-c4-triangle-core-publication-b66f592/validation/archive-verify.receipt.json)：
  `python3 -B tools/audit_archive.py verify --artifacts` exit 0，3,488 原路徑與
  1,983 unique blobs 全通過。

本次僅用既有 archive append 新增四個路徑：兩份大型結構證書、凍結的
K15 壓縮證書、原 manifest 已列的 ignored Python bytecode；共三個新增
blobs，其餘 bytes 去重沿用。原 46 筆 [MANIFEST](../../audits/2026-10-14-c4-triangle-core-b66f592/MANIFEST.json)
與既有 logs／frozen 文件完全不改寫。[還原核對](../../audits/2026-10-14-c4-triangle-core-publication-b66f592/validation/custody-restore.json)
在暫存目錄重建全部 46 筆，含四個 archive 路徑，逐 SHA 一致；九份 frozen
輸入亦一致；另從 Git 暫存區的實際 blobs [重建核對](../../audits/2026-10-14-c4-triangle-core-publication-b66f592/validation/custody-staged.json)
全部 46 筆一致。新 clone 先執行 `python3 tools/audit_archive.py restore`，再按
[原重播入口](../../audits/2026-10-14-c4-triangle-core-b66f592/VERIFICATION.md)執行 checks。

正式文件與全樹 DocGraph 分別記錄，發布前亦檢查 staged generated artifacts
政策及 whitespace；實際結果見[發布檢查](../../audits/2026-10-14-c4-triangle-core-publication-b66f592/validation/publication-checks.json)。
`check_docs` 與正式 docs DocGraph 均 PASS；全樹 DocGraph exit 1，69 項錯誤
全為 frozen／scratch 等保留副本的 duplicate IDs，不刪證據製造全域 PASS。
暫存區生成物政策與 `git diff --cached --check` 均 PASS。
本次未重跑來源生成器、plantri、外部 ≤28 點枚舉或無關舊分類。

## 文件傳播與發布範圍

Updated：C4 權威入口、舊來源橋的後續連結、Kempe 導覽、no4ct 接續入口及
STATUS 的短索引；將含混的「R=13」改為「R 的完整 C4 關係為 mask13」，
明確 b0／b1／b3 與六接點的同份完整染色義務。

Reviewed-unchanged：README 的使用及研究路由、HANDOFF 的研究線與活躍 tags；
既有 K≤22／k≥23、其他研究線及一般主命題的 OPEN 狀態沒有改變。
Propagation stop：L1 與直接父入口；沒有新的跨線 closure。

發布白名單僅含本次 C4 bundle、發布 logs／紀錄、五份相關文件及 archive
索引／ignore 增量與新增 blobs；保留歷史證據，未擴大枚舉或更新依賴。
