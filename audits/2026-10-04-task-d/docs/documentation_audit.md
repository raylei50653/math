# 任務 D：文件現況與後續關係稽核

稽核對象為 `/tmp/math-task-d-audit-_l2g06k7/snapshot` 的凍結副本。共享工作樹的報告、導覽、歷史及 artifacts 均未修改。本文只提供整合修訂清單；數學 `--check`、identity ledger 與 payload 差異由任務 D 主報告彙整。

## 實際檢查

| 檢查 | Exit | 實際輸出 | 完整紀錄 |
| --- | ---: | --- | --- |
| `python3 scripts/check_docs.py`，初始副本 | 1 | 81 個 missing path；全部來自副本未帶入 `LICENSE`、`CITATION.cff`、`Math.lean`、`Math/`，不是源工作樹文件錯誤 | `check_docs.log` |
| 同命令，補齊只讀連結目標及 `paper/` 後 | 0 | `OK: 510 Markdown files, 5242 local links; anchors, index, handoff checked` | `check_docs_complete_snapshot.log` |
| `python3 tools/docgraph check` | 0 | `OK: 62 documents, 213 relations, 5 families; 0 errors, 0 notes` | `docgraph_check.log` |

沒有執行 `lake build`，也沒有宣稱重驗 Lean 或形式化本輪紙面 topology。DocGraph 與文件 checker 都不檢查数学現況敘述；結構通過不消除以下人工發現。

## 已一致的主要現況

`README.md:14`、`docs/c5_kempe_guide.md:16-17,34-77` 與 `docs/c5_research_synthesis.md:3-49` 均明列：933／941 在固定完整 Σ、Σ-edge-minimal induced-C₅ disk source 前提下有共同 ε≥2；唯一 degree-6 的 ε=2 分支全排；相鄰唯一 mixed、四-spoke `(2,2)`、mixed-`(1,1)` 加兩側各一原單接點 unary 子型完成；其他 incidence 與雙 root 分支、ε≥3、一般出口、來源實現及 `K∞=K≤5` 保留。

導覽 `docs/c5_kempe_guide.md:58-60`、整合頁 `docs/c5_research_synthesis.md:35-39` 與完成報告 `docs/c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md:130-140` 的分期數字一致：

| 階段 | 933 | 941 |
| --- | ---: | ---: |
| 共用 pair | 7 | 9 |
| 短 face | 8 | 16 |
| 同一三段長 face | 10 | 10 |
| 原 unary crosscut | 8 | 16 |
| 共用短框弧 | 0 | 6 |
| 不相交 pairs | 14 | 18 |
| 總數 | 47 | 75 |
| 殘留 | 0 | 0 |

不相交階段再分一側全短 4／8 及共同兩段長框弧 10／10，與其完成報告、歷史相同。此处為文件交叉核對，計數本身不代替逐 identity 的完整性、互斥性核對。

`docs/HANDOFF.md` 維持薄導覽，無需為本輪成果改寫。`docs/history/2026-10-03-excess-two-four-spoke-disjoint-pairs.md:74-76` 保存當輪文件檢查 510／5,242 與 DocGraph 62／213／5，與本次副本實際結果相同。

## 必修的現況不一致與具體措辭

### 1. Synthesis 的 941 ε=1／H1 舊快照

`docs/c5_research_synthesis.md:61-65` 已說下文保留 `b97b107` 當輪快照；因此不能將下文原始內容一律解讀為新數學錯誤。但其章節／欄位仍叫「目前完成」「目前已知」「下一個可判定小域」，H1 又沒有局部後續註記，會作為當前接手指引被讀到。使用者指出的前後矛盾實際存在於這些位置：

| 位置 | 現有問題 | 建議修訂 |
| --- | --- | --- |
| `:98,107` | 「各研究線目前完成」中的 Kempe 列仍寫 941 ε=1 留 t=2、3 | 若保留快照，標題改為「2026-10-02 各線快照」，在該列後加「後續：941 t=2、t=3 已排除，與 933 同得 ε≥2；當前 ε=2 停止點見 Kempe 導覽」。若改現況列，改為「同圖換色、循環流及共同 ε≥2；唯一 degree-6 ε=2 全排，指定相鄰唯一 mixed 的四-spoke 子型由前段總表列明」。 |
| `:131-134` | 表頭說「目前已知／下一個」，941 列仍 ε≥1、下一 t=2 再 t=3 | 表頭改為「2026-10-02 當時已知／當時下一域」，或把 941 列改為「ε≥2；ε=1 的 t=1 `(2,1,1)`、t=2 `(2,1)`、t=3 `(2)` 已全部排除；下一域由 Kempe 導覽維護」。附 `c5_941_two_spoke.md`、`c5_941_three_spoke.md`。 |
| `:204-220` | H1 仍是候選，寫 941 只剩 t=2、3、未完成及尚待實驗 | 在 H1 標題下新增日期註記：「後續（2026-10-02）：本 H1 在既有報告明列的固定完整 Σ=933／941、Σ-edge-minimal induced-C₅ disk source 前提下已成立。941 的 t=2、t=3 分支由後續報告完成，與既有 933 下界合成 ε≥2。以下支持／未完成／實驗段落保留 b97b107 當輪提案；不再是当前未解題目。此結果仍不排除任意 ε 候選來源，不證 ε≥3、一般出口或主命題，未新增 Lean theorem。」链接兩份原報告。 |
| `:264-275` 尤其 `:270` | 「什麼值得先做」仍把已完成的 941 t=2 列為第一優先 | 最小修訂：標題／引導明示「2026-10-02 當輪建議，後續狀態見各線導覽」，並把該列的完成條件改註「後續已完成，見 two-spoke／three-spoke 報告；当前下一題由 Kempe 導覽維護」。不要在此另複製新的研究排程。 |
| `:298` | 「全部新假設留待後續驗證」在今日無條件包含 H1 | 改為「以上保存當輪假設與初驗；H1 已在後續固定來源前提下成立，H2、H3 及更一般推廣仍未證；普遍四階來源說法已在當輪淘汰。」 |

H1 的已知邊界以 `docs/c5_941_three_spoke.md:14-27` 為準：有限簡單圖、指定有序 induced-C₅ disk 外框、接受 T4、每條非框邊刪除嚴格擴大完整 Σ，ε 為有效內點完整 degree 超額。隨整圖 D₅ 搬運；任意大小涵蓋依既有分類、紙面接合與有限 Python 證書，並非一般來源排除或 Lean 新定理。避免只改「H1 已證」而移除這些前提。

### 2. STATUS 現況列未追上最新子型完成

| 位置 | 現有問題 | 建議替换／補註 |
| --- | --- | --- |
| `docs/STATUS.md:172` | 共用 pair 列仍寫「整個子型未完成」 | 「當輪 40／66 unequal 殘留由後續短 face、長 face、crosscut、短框弧及不相交 pairs 報告全部封閉；完成同一 mixed-(1,1)+各側一 unary 子型。原共用 pair 證書與當輪數字保留。」直接鏈完成報告。 |
| `:170-171` | 長／短 face 列只追到較早 14／24、22／40 | 保留當輪排除數及後續中間數，再加「原子型由不相交 pairs 完成報告封閉；其他 incidence 仍保留」。這是後續關係更新，不改歷史數字。 |
| `:234` | synthesis 索引說 ε=1、root 樹、同 Σ 出口三假設「均保留未證部分」 | 「八線成果與證據界線整合；H1 已在固定 933／941 source 前提下成立，root 樹分離 H2 及同 Σ 出口 H3 等推廣仍未證；保留當輪快照，不替代導覽排程。」 |

旁及的現況整理項目：`docs/STATUS.md:194` 的 t=1 全分拆列仍列「其餘 t 保留」，雖前面 `:188-190` 已列 t=0、2、3 完成；可改為「其餘 t 由後續總報告完成；唯一 degree-6 ε=2 分支封閉，雙 degree-5 roots 及一般來源仍保留」。`docs/STATUS.md:173` 的「(2,2) 保留」可精確寫成「(2,2) 其他 incidence 保留；mixed-(1,1)+各側一 unary 已由後續完成」。

### 3. 三份專題頁首同時寫未完成／已完成

| 文件及位置 | 矛盾 | 最小修訂 |
| --- | --- | --- |
| `docs/c5_excess_two_mixed_core_four_spoke_equal_pair.md:3-9` | `:7` 說整份子型未證，`:9` 說已完成 | `:7` 改為「當時再排 10／10 至 22／40；下文保留各輪數字與原證書。」保留 `:8-9` 明示最终 mixed11 子型完成、其他 incidence 與 ε≥3 保留。 |
| `docs/c5_excess_two_mixed_core_four_spoke_short_face.md:3-8` | `:6` 說整份子型未證，`:8` 說已完成 | `:6` 改為「證書；長 face 當輪仍未完成整個子型。其後完成範圍見下一段及 Kempe 導覽。」或刪去當前式「整份子型及 ε≥3 仍未證」，保留 ε≥3 未證於最終註記。 |
| `docs/c5_excess_two_mixed_core_four_spoke_long_face.md:3-8` | `:6` 說整份子型未證，`:8` 說已完成 | `:6` 改為「22／40 當輪數字；crosscut 當時收窄至 14／24，其後完成範圍見下一段及 Kempe 導覽。」最终註記保留 ε≥3 未證。 |

這三份頁首均應形成單一有日期後續註記，清楚區分中間輪次與今日結論。不要為消除矛盾把原正文的當輪 40／66、32／50、22／40 停止點或歷史驗證重寫成最新 0／0。

## 投影、完整 joint 及搬運的文件邊界

| 證據 | 文件精確陳述 | 稽核判斷 |
| --- | --- | --- |
| unary witness 替換 | short_face `:170-178`；long_face `:117-138`；disjoint_pairs `:91-105`：固定原 U 或 V，保存其外所有原頂點；五角色投影相等 | 一致；替換的是整份指定 unary witness，不是六角色 joint 等式。 |
| C witness 替換 | crosscut `:147-166`：四角色 `(a,b,u,v)` 投影等式；C 外原頂點保持；Σ 原邊刪除不變 | 一致；完整 C 染色重選會改 `(x,y)`，不得升為六角色 joint 相等。 |
| 指定拒絕列出口 | short_arc `:14-18,130-145`：在候選拒絕列的同框完整六角色 joint 構造一份 witness | 一致；不是 C 可延拓每個異色 root pair 或全 Σ 不變。 |
| 六角色完整接合控制 | equal_pair `:188-201`；short_face `:163-178`；long_face `:186-195`：具名原圖／變體完整 joint 與獨立整圖回溯相同，fibres 含空；控制圖不宣稱 disk／candidate／critical | 一致；「完整」描述儲存及重播的 relation，不代表刪邊兩圖 joint 相等。 |
| D₅ 及 root 交換 | crosscut 歷史 `:39-43`；short_arc `:130-145` 与歷史 `:27-31`：整圖共同搬 rows、colors、roles、contacts、ownership；933→940；941 indices179／239→949 | 文件一致；不可把不同搬運後 mask 當同一原來源，也不可任選 reflection 假設固定 q 仍拒絕。 |

可改善的縮句：`docs/STATUS.md:167` 的「完整 joint 與原 witness 保持」、`docs/c5_research_synthesis.md:27` 的「完整 C/U/V 與原 witness 保持」，以及完成歷史的摘要 `docs/history/2026-10-03-excess-two-four-spoke-disjoint-pairs.md:103` 容易被讀成全部 witness／六角色 joint 不變。建議當前摘要明寫「完整原 relations 保留；只替換固定短 unary 的整份 witness，其餘頂點逐點保持，主張五角色投影相等」。原歷史記錄可原樣保留；加修訂註記而非追改當輪通過結果。這是措辭精度項，不是精確公式所顯示的數學矛盾。

## 應原樣保留與沿用範圍

依 `docs/DOCUMENTATION.md:39-44`，專題正文和歷史中的舊未解／下一步／未提交是當輪語境，專題頁首負責日期化後續關係，當前導覽負責停止點。下列不應因今日零殘留而改寫：

- equal_pair `:222-227`、short_face `:196-200`、long_face `:216-223`、crosscut `:228-234`、short_arc `:187-194` 的當輪停止點；它們的前置日期註記已指向後續（前三份註記內矛盾另按上表修正）。
- 五份 `docs/history/2026-10-03-excess-two-four-spoke-*.md` 的當輪數字、actual replay、lake build、未重跑範圍、artifact bytes／hash。
- 歷史 artifacts 全部 bytes。文件 hash 漂移應在獨立稽核報告對照記錄，不靠重寫舊證書製造 byte-check 通過。
- `docs/c5_kempe_guide.md:113-166` 已將前序九份歷史 checker、本輪原單 spoke 文件漂移、singles 漂移 audit 的沿用／重跑範圍分開。這些是歷史完成紀錄，不能據此宣稱任務 D 當日全部重跑；主報告以本次實際命令結果為準。

`docs/c5_research_synthesis.md:5` 與 `docs/c5_kempe_guide.md:86` 的「四-spoke 七輪」仍指已有發布整理批，不包含最新五輪。可補「前序已發布七輪，另有本次五輪未提交進展」，避免把七輪誤讀為當前成果總數。保留發布整理紀錄的原題名與連結。

完成條件是提供上述具體修訂及實際檢查結果；本稽核不執行共用文件整合、不寫歷史 artifacts，也不 commit／push。
